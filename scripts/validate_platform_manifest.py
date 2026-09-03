#!/usr/bin/env python3
"""Validate GoreeCloud goreecloud.platform.yaml manifests.

This validator intentionally fails closed on missing contract fields and on
unsupported Stable declarations. It validates the contract structure without
claiming that referenced evidence is itself accepted or sufficient.
"""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import sys
from typing import Any

import yaml

SCHEMA_VERSION = "0.1"
LIFECYCLES = {
    "concept",
    "experimental",
    "development",
    "release-candidate",
    "stable",
    "deprecated",
    "retired",
}
INTEGRATION_STATUSES = {
    "implemented",
    "partial",
    "planned",
    "not-applicable",
    "unknown",
}
CONFORMANCE_STATUSES = {"conformant", "partial", "nonconformant", "unverified"}
PLATFORM_SYSTEMS = (
    "manager",
    "privacy_shield",
    "wardveil_security",
    "everkeep",
    "glaze_ui",
    "mesh",
    "identity",
)
ROOT_FIELDS = (
    "schema_version",
    "component",
    "lifecycle",
    "version",
    "supported_platforms",
    "api",
    "platform_systems",
    "health",
    "continuity",
    "external_dependencies",
    "compatibility",
    "conformance",
)


class ValidationError(Exception):
    pass


def fail(message: str) -> None:
    raise ValidationError(message)


def require_mapping(value: Any, path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail(f"{path} must be a mapping")
    return value


def require_list(value: Any, path: str) -> list[Any]:
    if not isinstance(value, list):
        fail(f"{path} must be a list")
    return value


def require_string(value: Any, path: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str):
        fail(f"{path} must be a string")
    if not allow_empty and not value.strip():
        fail(f"{path} must not be empty")
    return value


def require_bool(value: Any, path: str) -> bool:
    if not isinstance(value, bool):
        fail(f"{path} must be a boolean")
    return value


def require_keys(mapping: dict[str, Any], keys: tuple[str, ...] | list[str], path: str) -> None:
    missing = [key for key in keys if key not in mapping]
    if missing:
        fail(f"{path} missing required fields: {', '.join(missing)}")


def validate_string_list(value: Any, path: str) -> list[str]:
    items = require_list(value, path)
    for index, item in enumerate(items):
        require_string(item, f"{path}[{index}]")
    if len(items) != len(set(items)):
        fail(f"{path} must not contain duplicate values")
    return items


def validate_integration(name: str, value: Any, *, mesh: bool = False) -> dict[str, Any]:
    path = f"platform_systems.{name}"
    data = require_mapping(value, path)
    required = ["status", "version", "evidence", "notes"]
    if mesh:
        required.extend(["capabilities", "dependencies", "published_events", "consumed_events"])
    require_keys(data, required, path)

    status = require_string(data["status"], f"{path}.status")
    if status not in INTEGRATION_STATUSES:
        fail(f"{path}.status must be one of: {', '.join(sorted(INTEGRATION_STATUSES))}")

    version = data["version"]
    if version is not None:
        require_string(version, f"{path}.version")

    evidence = validate_string_list(data["evidence"], f"{path}.evidence")

    notes = data["notes"]
    if notes is not None:
        require_string(notes, f"{path}.notes")

    if status == "implemented" and not evidence:
        fail(f"{path} declares implemented but has no evidence references")
    if status == "not-applicable" and (notes is None or not notes.strip()):
        fail(f"{path} declares not-applicable but has no supportable explanation")

    if mesh:
        for key in ("capabilities", "dependencies", "published_events", "consumed_events"):
            validate_string_list(data[key], f"{path}.{key}")

    return data


def validate_manifest(path: Path) -> None:
    try:
        parsed = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing manifest: {path}")
    except yaml.YAMLError as exc:
        fail(f"invalid YAML: {exc}")

    root = require_mapping(parsed, "manifest")
    require_keys(root, ROOT_FIELDS, "manifest")

    if root["schema_version"] != SCHEMA_VERSION:
        fail(f"schema_version must be {SCHEMA_VERSION!r}")

    component = require_mapping(root["component"], "component")
    require_keys(component, ["type", "id", "product_name", "repository"], "component")
    component_type = require_string(component["type"], "component.type")
    if component_type not in {"application", "service"}:
        fail("component.type must be 'application' or 'service'")
    component_id = require_string(component["id"], "component.id")
    if any(ch not in "abcdefghijklmnopqrstuvwxyz0123456789-" for ch in component_id):
        fail("component.id must contain only lowercase letters, digits, and hyphens")
    require_string(component["product_name"], "component.product_name")
    repository = require_string(component["repository"], "component.repository")
    if not repository.startswith("GoreeCloud/"):
        fail("component.repository must identify a GoreeCloud repository")

    lifecycle = require_string(root["lifecycle"], "lifecycle")
    if lifecycle not in LIFECYCLES:
        fail(f"lifecycle must be one of: {', '.join(sorted(LIFECYCLES))}")
    require_string(root["version"], "version")
    validate_string_list(root["supported_platforms"], "supported_platforms")

    api = require_mapping(root["api"], "api")
    require_keys(api, ["versions", "endpoints"], "api")
    validate_string_list(api["versions"], "api.versions")
    endpoints = require_list(api["endpoints"], "api.endpoints")
    for index, endpoint_value in enumerate(endpoints):
        endpoint = require_mapping(endpoint_value, f"api.endpoints[{index}]")
        require_keys(endpoint, ["name", "url", "purpose"], f"api.endpoints[{index}]")
        for key in ("name", "url", "purpose"):
            require_string(endpoint[key], f"api.endpoints[{index}].{key}")

    systems = require_mapping(root["platform_systems"], "platform_systems")
    require_keys(systems, list(PLATFORM_SYSTEMS), "platform_systems")
    for name in PLATFORM_SYSTEMS:
        validate_integration(name, systems[name], mesh=name == "mesh")

    health = require_mapping(root["health"], "health")
    require_keys(health, ["health_endpoint", "readiness_endpoint"], "health")
    for key in ("health_endpoint", "readiness_endpoint"):
        if health[key] is not None:
            require_string(health[key], f"health.{key}")

    continuity = require_mapping(root["continuity"], "continuity")
    require_keys(continuity, ["backup", "restore", "export", "portability"], "continuity")
    for name in ("backup", "restore", "export", "portability"):
        item = require_mapping(continuity[name], f"continuity.{name}")
        require_keys(item, ["required", "requirements"], f"continuity.{name}")
        require_bool(item["required"], f"continuity.{name}.required")
        requirements = validate_string_list(item["requirements"], f"continuity.{name}.requirements")
        if item["required"] and not requirements:
            fail(f"continuity.{name} is required but has no requirements")

    dependencies = require_list(root["external_dependencies"], "external_dependencies")
    for index, dependency_value in enumerate(dependencies):
        dependency = require_mapping(dependency_value, f"external_dependencies[{index}]")
        require_keys(dependency, ["name", "purpose", "required"], f"external_dependencies[{index}]")
        require_string(dependency["name"], f"external_dependencies[{index}].name")
        require_string(dependency["purpose"], f"external_dependencies[{index}].purpose")
        require_bool(dependency["required"], f"external_dependencies[{index}].required")

    compatibility = require_mapping(root["compatibility"], "compatibility")
    require_keys(compatibility, ["requires", "provides"], "compatibility")
    validate_string_list(compatibility["requires"], "compatibility.requires")
    validate_string_list(compatibility["provides"], "compatibility.provides")

    conformance = require_mapping(root["conformance"], "conformance")
    require_keys(conformance, ["status", "validated_at", "evidence", "blockers"], "conformance")
    conformance_status = require_string(conformance["status"], "conformance.status")
    if conformance_status not in CONFORMANCE_STATUSES:
        fail(f"conformance.status must be one of: {', '.join(sorted(CONFORMANCE_STATUSES))}")
    if conformance["validated_at"] is not None:
        validated_at = require_string(conformance["validated_at"], "conformance.validated_at")
        try:
            datetime.fromisoformat(validated_at.replace("Z", "+00:00"))
        except ValueError as exc:
            fail(f"conformance.validated_at must be ISO-8601: {exc}")
    validate_string_list(conformance["evidence"], "conformance.evidence")
    blockers = validate_string_list(conformance["blockers"], "conformance.blockers")

    if conformance_status == "conformant" and blockers:
        fail("conformance.status is conformant but blockers are present")

    if lifecycle == "stable":
        unacceptable = [
            name
            for name in PLATFORM_SYSTEMS
            if systems[name]["status"] not in {"implemented", "not-applicable"}
        ]
        if unacceptable:
            fail(
                "Stable lifecycle is blocked by unresolved platform-system states: "
                + ", ".join(unacceptable)
            )
        if conformance_status != "conformant":
            fail("Stable lifecycle requires conformance.status=conformant")

    print(f"platform-manifest: {path} validated")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifests", nargs="+", type=Path)
    args = parser.parse_args()

    try:
        for path in args.manifests:
            validate_manifest(path)
    except ValidationError as exc:
        print(f"platform-manifest: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
