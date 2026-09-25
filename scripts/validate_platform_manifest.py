#!/usr/bin/env python3
"""Validate GoreeCloud goreecloud.platform.yaml manifests against Platform Contract 2.0."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import sys
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

SCHEMA_VERSION = "2.0"
CURRENT_GLAZE_UI_VERSION = "1.6.0"
LIFECYCLE_STAGES = ("seed", "lab", "forge", "weave", "seal", "anchor", "sunset", "archive")
PLATFORM_SYSTEMS = (
    "manager",
    "privacy_shield",
    "wardveil_security",
    "everkeep",
    "glaze_ui",
    "mesh",
    "identity",
    "policy",
    "observability",
)
PASSING_PLATFORM_RESULTS = {"applicable-conformant", "not-applicable-justified"}
SYSTEM_ACCEPTANCE_CATEGORIES = {
    "manager": "manager",
    "privacy_shield": "privacy-shield",
    "wardveil_security": "wardveil-security",
    "everkeep": "everkeep",
    "glaze_ui": "glaze-ui",
    "mesh": "mesh",
    "identity": "identity",
    "policy": "policy",
    "observability": "observability",
}
ANCHOR_ACCEPTANCE_CATEGORIES = {
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
SHARED_LIBRARY_ANCHOR_ACCEPTANCE_CATEGORIES = {
    "accessibility",
    "supported-platform",
    "security",
    "privacy",
    "documentation",
    "integration",
    "release",
}


def anchor_acceptance_categories(manifest: dict[str, Any]) -> set[str]:
    """Return the class-level Anchor acceptance baseline for a manifest."""
    if manifest["component"]["type"] == "shared-library":
        return SHARED_LIBRARY_ANCHOR_ACCEPTANCE_CATEGORIES
    return ANCHOR_ACCEPTANCE_CATEGORIES


class ValidationError(Exception):
    pass


def fail(message: str) -> None:
    raise ValidationError(message)


def _schema_path() -> Path:
    return Path(__file__).resolve().parents[1] / "schemas" / "goreecloud.platform.schema.json"


def _load_schema() -> dict[str, Any]:
    try:
        return json.loads(_schema_path().read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"unable to load Platform Contract schema: {exc}")


def _validate_structural(manifest: dict[str, Any]) -> None:
    validator = Draft202012Validator(_load_schema(), format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(manifest), key=lambda err: list(err.absolute_path))
    if errors:
        err = errors[0]
        path = ".".join(str(part) for part in err.absolute_path) or "manifest"
        fail(f"{path}: {err.message}")


def _validate_iso_datetime(value: str, label: str) -> None:
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        fail(f"{label} must be ISO-8601: {exc}")


def _validate_unique_ids(items: list[dict[str, Any]], label: str) -> None:
    ids = [item["id"] for item in items]
    if len(ids) != len(set(ids)):
        fail(f"{label} ids must be unique")


def _validate_platform_semantics(manifest: dict[str, Any]) -> None:
    systems = manifest["platform_systems"]
    if set(systems) != set(PLATFORM_SYSTEMS):
        fail("platform_systems must contain exactly the nine Integral Platform Systems; GoreeCloud Sync remains separate")
    for name in PLATFORM_SYSTEMS:
        entry = systems[name]
        result = entry["result"]
        evidence = entry["evidence"]
        notes = entry["notes"]
        if result == "applicable-conformant" and not evidence:
            fail(f"platform_systems.{name} declares applicable-conformant but has no evidence references")
        if result == "not-applicable-justified":
            if not evidence:
                fail(f"platform_systems.{name} declares not-applicable-justified but has no evidence reference")
            if not notes or not notes.strip():
                fail(f"platform_systems.{name} declares not-applicable-justified but has no justification")


def _validate_lifecycle_semantics(manifest: dict[str, Any]) -> None:
    lifecycle = manifest["lifecycle"]
    metadata = manifest["lifecycle_metadata"]
    if lifecycle not in LIFECYCLE_STAGES:
        fail(f"unsupported lifecycle {lifecycle!r}")
    if lifecycle == "seal" and metadata["candidate_identity"] is None:
        fail("Seal lifecycle requires exact lifecycle_metadata.candidate_identity")
    if lifecycle == "anchor":
        if metadata["qualification_state"] != "passed":
            fail("Anchor lifecycle requires lifecycle_metadata.qualification_state=passed")
        if not metadata["evidence"]:
            fail("Anchor lifecycle requires traceable lifecycle_metadata.evidence")


def _validate_anchor_gate(manifest: dict[str, Any]) -> None:
    if manifest["lifecycle"] != "anchor":
        return

    systems = manifest["platform_systems"]
    failing = [
        name for name in PLATFORM_SYSTEMS
        if systems[name]["result"] not in PASSING_PLATFORM_RESULTS
    ]
    if failing:
        fail("Anchor lifecycle requires passing results for all nine Integral Platform Systems; failing: " + ", ".join(failing))

    conformance = manifest["conformance"]
    if conformance["status"] != "conformant":
        fail("Anchor lifecycle requires conformance.status=conformant")
    if conformance["validated_at"] is None:
        fail("Anchor lifecycle requires conformance.validated_at")
    _validate_iso_datetime(conformance["validated_at"], "conformance.validated_at")

    glaze = systems["glaze_ui"]
    if glaze["result"] != "not-applicable-justified":
        required = manifest["compatibility"]["glaze_ui_required"]
        if required != CURRENT_GLAZE_UI_VERSION:
            fail(f"Anchor lifecycle requires compatibility.glaze_ui_required={CURRENT_GLAZE_UI_VERSION!r}")
        if glaze["result"] == "applicable-conformant" and glaze["version"] != required:
            fail("Anchor lifecycle requires the conformant Glaze UI version to equal the required approved target")

    acceptance = manifest["evidence"]["acceptance_tests"]
    passed_categories = {item["category"] for item in acceptance if item["result"] == "passed"}
    missing = sorted(anchor_acceptance_categories(manifest) - passed_categories)
    if missing:
        fail("Anchor lifecycle missing passing acceptance categories: " + ", ".join(missing))

    for system, category in SYSTEM_ACCEPTANCE_CATEGORIES.items():
        if systems[system]["result"] == "applicable-conformant" and category not in passed_categories:
            fail(f"Anchor lifecycle requires passing {category!r} acceptance evidence for applicable-conformant platform_systems.{system}")

    releases = manifest["evidence"]["release"]
    if not any(item["result"] == "published" for item in releases):
        fail("Anchor lifecycle requires published release evidence")


def validate_manifest(path: Path) -> dict[str, Any]:
    try:
        parsed = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing manifest: {path}")
    except yaml.YAMLError as exc:
        fail(f"invalid YAML: {exc}")

    if not isinstance(parsed, dict):
        fail("manifest must be a mapping")

    _validate_structural(parsed)
    if parsed["schema_version"] != SCHEMA_VERSION:
        fail(f"schema_version must be {SCHEMA_VERSION!r}")
    if parsed["compatibility"]["platform_contract"] != SCHEMA_VERSION:
        fail("compatibility.platform_contract must match schema_version")

    _validate_unique_ids(parsed["evidence"]["acceptance_tests"], "evidence.acceptance_tests")
    _validate_unique_ids(parsed["evidence"]["release"], "evidence.release")
    _validate_platform_semantics(parsed)
    _validate_lifecycle_semantics(parsed)
    _validate_anchor_gate(parsed)
    return parsed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    try:
        manifest = validate_manifest(args.manifest)
    except ValidationError as exc:
        print(f"platform-contract: {exc}", file=sys.stderr)
        return 1

    print(
        "platform-contract: valid declaration "
        f"for {manifest['component']['repository']} at schema {manifest['schema_version']} "
        "with the canonical eight-stage lifecycle and exactly nine Integral Platform Systems declared"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
