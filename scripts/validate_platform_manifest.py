#!/usr/bin/env python3
"""Validate GoreeCloud goreecloud.platform.yaml manifests.

The contract validator is intentionally conservative. It validates repository
declarations, normalizes platform-system state vocabulary, and fails closed for
Stable lifecycle claims when required evidence or platform conformance is absent.
A passing declaration check never substitutes for runtime or acceptance testing.
"""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import re
import sys
from typing import Any

import yaml

SCHEMA_VERSION = "0.2"
CURRENT_GLAZE_UI_VERSION = "1.1.0"

LIFECYCLES = {
    "concept",
    "experimental",
    "development",
    "release-candidate",
    "stable",
    "deprecated",
    "retired",
}
PLATFORM_RESULTS = {
    "applicable-conformant",
    "applicable-migration-required",
    "applicable-blocked",
    "applicable-nonconformant",
    "not-applicable-justified",
}
CONFORMANCE_STATUSES = {"conformant", "nonconformant", "unverified"}
EVIDENCE_RESULTS = {"passed", "failed", "blocked", "not-run"}
RELEASE_RESULTS = {"candidate", "published", "failed", "unverified"}
EVIDENCE_CATEGORIES = {
    "manager",
    "privacy-shield",
    "wardveil-security",
    "everkeep",
    "glaze-ui",
    "mesh",
    "identity",
    "api",
    "accessibility",
    "supported-platform",
    "backup",
    "restore",
    "export-portability",
    "security",
    "privacy",
    "documentation",
    "integration",
    "migration",
    "rollback",
    "release",
}
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
    "evidence",
    "conformance",
)
STABLE_ACCEPTANCE_CATEGORIES = {
    "api",
    "accessibility",
    "supported-platform",
    "security",
    "privacy",
    "backup",
    "restore",
    "export-portability",
    "documentation",
    "integration",
    "release",
}


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


def require_exact_keys(
    mapping: dict[str, Any],
    required: tuple[str, ...] | list[str],
    path: str,
    *,
    optional: tuple[str, ...] | list[str] = (),
) -> None:
    missing = [key for key in required if key not in mapping]
    if missing:
        fail(f"{path} missing required fields: {', '.join(missing)}")
    allowed = set(required) | set(optional)
    extras = sorted(set(mapping) - allowed)
    if extras:
        fail(f"{path} contains unsupported fields: {', '.join(extras)}")


def validate_iso_datetime(value: Any, path: str) -> str:
    text = require_string(value, path)
    try:
        datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        fail(f"{path} must be ISO-8601: {exc}")
    return text


def validate_string_list(value: Any, path: str) -> list[str]:
    items = require_list(value, path)
    normalized: list[str] = []
    for index, item in enumerate(items):
        normalized.append(require_string(item, f"{path}[{index}]"))
    if len(normalized) != len(set(normalized)):
        fail(f"{path} must not contain duplicate values")
    return normalized


def validate_evidence_reference(value: Any, path: str) -> dict[str, Any]:
    data = require_mapping(value, path)
    required = ["id", "category", "path", "revision", "result", "observed_at"]
    require_exact_keys(data, required, path, optional=["notes"])
    require_string(data["id"], f"{path}.id")
    category = require_string(data["category"], f"{path}.category")
    if category not in EVIDENCE_CATEGORIES:
        fail(f"{path}.category must be one of: {', '.join(sorted(EVIDENCE_CATEGORIES))}")
    require_string(data["path"], f"{path}.path")
    require_string(data["revision"], f"{path}.revision")
    result = require_string(data["result"], f"{path}.result")
    if result not in EVIDENCE_RESULTS:
        fail(f"{path}.result must be one of: {', '.join(sorted(EVIDENCE_RESULTS))}")
    validate_iso_datetime(data["observed_at"], f"{path}.observed_at")
    if data.get("notes") is not None:
        require_string(data["notes"], f"{path}.notes")
    return data


def validate_release_evidence(value: Any, path: str) -> dict[str, Any]:
    data = require_mapping(value, path)
    required = ["id", "version", "revision", "path", "result", "observed_at"]
    require_exact_keys(data, required, path, optional=["artifact_digest", "notes"])
    require_string(data["id"], f"{path}.id")
    require_string(data["version"], f"{path}.version")
    require_string(data["revision"], f"{path}.revision")
    require_string(data["path"], f"{path}.path")
    result = require_string(data["result"], f"{path}.result")
    if result not in RELEASE_RESULTS:
        fail(f"{path}.result must be one of: {', '.join(sorted(RELEASE_RESULTS))}")
    validate_iso_datetime(data["observed_at"], f"{path}.observed_at")
    if data.get("artifact_digest") is not None:
        require_string(data["artifact_digest"], f"{path}.artifact_digest")
    if data.get("notes") is not None:
        require_string(data["notes"], f"{path}.notes")
    return data


def validate_integration(name: str, value: Any, *, mesh: bool = False) -> dict[str, Any]:
    path = f"platform_systems.{name}"
    data = require_mapping(value, path)
    required = ["result", "version", "evidence", "notes"]
    if mesh:
        required.extend(["capabilities", "dependencies", "published_events", "consumed_events"])
    require_exact_keys(data, required, path)

    result = require_string(data["result"], f"{path}.result")
    if result not in PLATFORM_RESULTS:
        fail(f"{path}.result must be one of: {', '.join(sorted(PLATFORM_RESULTS))}")

    version = data["version"]
    if version is not None:
        require_string(version, f"{path}.version")

    evidence = validate_string_list(data["evidence"], f"{path}.evidence")

    notes = data["notes"]
    if notes is not None:
        require_string(notes, f"{path}.notes")

    if result == "applicable-conformant" and not evidence:
        fail(f"{path} declares applicable-conformant but has no evidence references")
    if result == "not-applicable-justified":
        if notes is None or not notes.strip():
            fail(f"{path} declares not-applicable-justified but has no justification")
        if not evidence:
            fail(f"{path} declares not-applicable-justified but has no evidence reference")

    if mesh:
        for key in ("capabilities", "dependencies", "published_events", "consumed_events"):
            validate_string_list(data[key], f"{path}.{key}")

    return data


def validate_manifest(path: Path) -> dict[str, Any]:
    try:
        parsed = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing manifest: {path}")
    except yaml.YAMLError as exc:
        fail(f"invalid YAML: {exc}")

    root = require_mapping(parsed, "manifest")
    require_exact_keys(root, list(ROOT_FIELDS), "manifest")

    if root["schema_version"] != SCHEMA_VERSION:
        fail(f"schema_version must be {SCHEMA_VERSION!r}")

    component = require_mapping(root["component"], "component")
    require_exact_keys(component, ["type", "id", "product_name", "repository"], "component")
    component_type = require_string(component["type"], "component.type")
    if component_type not in {"application", "service"}:
        fail("component.type must be 'application' or 'service'")
    component_id = require_string(component["id"], "component.id")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", component_id):
        fail("component.id must use lowercase kebab-case")
    require_string(component["product_name"], "component.product_name")
    repository = require_string(component["repository"], "component.repository")
    if not re.fullmatch(r"GoreeCloud/[A-Za-z0-9._-]+", repository):
        fail("component.repository must identify a GoreeCloud repository")

    lifecycle = require_string(root["lifecycle"], "lifecycle")
    if lifecycle not in LIFECYCLES:
        fail(f"lifecycle must be one of: {', '.join(sorted(LIFECYCLES))}")
    require_string(root["version"], "version")
    supported_platforms = validate_string_list(root["supported_platforms"], "supported_platforms")
    if not supported_platforms:
        fail("supported_platforms must contain at least one platform")

    api = require_mapping(root["api"], "api")
    require_exact_keys(api, ["versions", "endpoints"], "api")
    validate_string_list(api["versions"], "api.versions")
    endpoints = require_list(api["endpoints"], "api.endpoints")
    for index, endpoint_value in enumerate(endpoints):
        endpoint = require_mapping(endpoint_value, f"api.endpoints[{index}]")
        require_exact_keys(endpoint, ["name", "url", "purpose"], f"api.endpoints[{index}]")
        for key in ("name", "url", "purpose"):
            require_string(endpoint[key], f"api.endpoints[{index}].{key}")

    systems = require_mapping(root["platform_systems"], "platform_systems")
    require_exact_keys(systems, list(PLATFORM_SYSTEMS), "platform_systems")
    for name in PLATFORM_SYSTEMS:
        validate_integration(name, systems[name], mesh=name == "mesh")

    health = require_mapping(root["health"], "health")
    require_exact_keys(health, ["health_endpoint", "readiness_endpoint"], "health")
    for key in ("health_endpoint", "readiness_endpoint"):
        if health[key] is not None:
            require_string(health[key], f"health.{key}")

    continuity = require_mapping(root["continuity"], "continuity")
    require_exact_keys(continuity, ["backup", "restore", "export", "portability"], "continuity")
    for name in ("backup", "restore", "export", "portability"):
        item = require_mapping(continuity[name], f"continuity.{name}")
        require_exact_keys(item, ["required", "requirements"], f"continuity.{name}")
        require_bool(item["required"], f"continuity.{name}.required")
        requirements = validate_string_list(item["requirements"], f"continuity.{name}.requirements")
        if item["required"] and not requirements:
            fail(f"continuity.{name} is required but has no requirements")

    dependencies = require_list(root["external_dependencies"], "external_dependencies")
    for index, dependency_value in enumerate(dependencies):
        dependency = require_mapping(dependency_value, f"external_dependencies[{index}]")
        require_exact_keys(
            dependency,
            ["name", "purpose", "required"],
            f"external_dependencies[{index}]",
            optional=["version_constraint"],
        )
        require_string(dependency["name"], f"external_dependencies[{index}].name")
        require_string(dependency["purpose"], f"external_dependencies[{index}].purpose")
        require_bool(dependency["required"], f"external_dependencies[{index}].required")
        if dependency.get("version_constraint") is not None:
            require_string(
                dependency["version_constraint"],
                f"external_dependencies[{index}].version_constraint",
            )

    compatibility = require_mapping(root["compatibility"], "compatibility")
    require_exact_keys(
        compatibility,
        ["platform_contract", "glaze_ui_required", "requires", "provides"],
        "compatibility",
    )
    platform_contract = require_string(compatibility["platform_contract"], "compatibility.platform_contract")
    if platform_contract != SCHEMA_VERSION:
        fail(
            "compatibility.platform_contract must match schema_version "
            f"({SCHEMA_VERSION})"
        )
    if compatibility["glaze_ui_required"] is not None:
        require_string(compatibility["glaze_ui_required"], "compatibility.glaze_ui_required")
    validate_string_list(compatibility["requires"], "compatibility.requires")
    validate_string_list(compatibility["provides"], "compatibility.provides")

    evidence = require_mapping(root["evidence"], "evidence")
    require_exact_keys(evidence, ["acceptance_tests", "release"], "evidence")
    acceptance_tests = require_list(evidence["acceptance_tests"], "evidence.acceptance_tests")
    acceptance_ids: list[str] = []
    for index, item in enumerate(acceptance_tests):
        validated = validate_evidence_reference(item, f"evidence.acceptance_tests[{index}]")
        acceptance_ids.append(validated["id"])
    if len(acceptance_ids) != len(set(acceptance_ids)):
        fail("evidence.acceptance_tests ids must be unique")

    release_items = require_list(evidence["release"], "evidence.release")
    release_ids: list[str] = []
    for index, item in enumerate(release_items):
        validated = validate_release_evidence(item, f"evidence.release[{index}]")
        release_ids.append(validated["id"])
    if len(release_ids) != len(set(release_ids)):
        fail("evidence.release ids must be unique")

    conformance = require_mapping(root["conformance"], "conformance")
    require_exact_keys(
        conformance,
        ["status", "validated_at", "evidence", "blockers"],
        "conformance",
    )
    conformance_status = require_string(conformance["status"], "conformance.status")
    if conformance_status not in CONFORMANCE_STATUSES:
        fail(
            "conformance.status must be one of: "
            + ", ".join(sorted(CONFORMANCE_STATUSES))
        )
    if conformance["validated_at"] is not None:
        validate_iso_datetime(conformance["validated_at"], "conformance.validated_at")
    validate_string_list(conformance["evidence"], "conformance.evidence")
    blockers = validate_string_list(conformance["blockers"], "conformance.blockers")
    if conformance_status == "conformant" and blockers:
        fail("conformance.status is conformant but blockers are present")

    glaze = systems["glaze_ui"]
    if component_type == "application" and glaze["result"] != "not-applicable-justified":
        required_glaze = compatibility["glaze_ui_required"]
        if not required_glaze:
            fail("applications with a Glaze UI responsibility must declare compatibility.glaze_ui_required")
        if required_glaze != CURRENT_GLAZE_UI_VERSION:
            fail(
                "compatibility.glaze_ui_required must match the current Stable "
                f"Glaze UI baseline {CURRENT_GLAZE_UI_VERSION}"
            )
        if glaze["result"] == "applicable-conformant" and glaze["version"] != required_glaze:
            fail(
                "platform_systems.glaze_ui.version must equal compatibility.glaze_ui_required "
                "when Glaze UI is applicable-conformant"
            )

    if lifecycle == "stable":
        unacceptable = [
            name
            for name in PLATFORM_SYSTEMS
            if systems[name]["result"]
            not in {"applicable-conformant", "not-applicable-justified"}
        ]
        if unacceptable:
            fail(
                "Stable lifecycle is blocked by unresolved platform-system results: "
                + ", ".join(unacceptable)
            )
        if conformance_status != "conformant":
            fail("Stable lifecycle requires conformance.status=conformant")
        if conformance["validated_at"] is None:
            fail("Stable lifecycle requires conformance.validated_at")
        categories_passed = {
            item["category"]
            for item in acceptance_tests
            if item["result"] == "passed"
        }
        missing_categories = sorted(STABLE_ACCEPTANCE_CATEGORIES - categories_passed)
        if missing_categories:
            fail(
                "Stable lifecycle is missing passing acceptance evidence categories: "
                + ", ".join(missing_categories)
            )
        if not any(item["result"] == "published" for item in release_items):
            fail("Stable lifecycle requires published release evidence")

    return root


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifests", nargs="+", type=Path)
    args = parser.parse_args()

    try:
        for path in args.manifests:
            validate_manifest(path)
            print(f"platform-manifest: {path} validated")
    except ValidationError as exc:
        print(f"platform-manifest: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
