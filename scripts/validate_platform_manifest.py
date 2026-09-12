#!/usr/bin/env python3
"""Validate GoreeCloud goreecloud.platform.yaml manifests against Platform Contract 0.3."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import sys
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

SCHEMA_VERSION = "0.3"
CURRENT_GLAZE_UI_VERSION = "1.3.0"
PLATFORM_SYSTEMS = (
    "manager",
    "privacy_shield",
    "wardveil_security",
    "everkeep",
    "glaze_ui",
    "mesh",
    "identity",
    "sync",
)
PASSING_PLATFORM_RESULTS = {"applicable-conformant", "not-applicable-justified"}
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


def _validate_stable_gate(manifest: dict[str, Any]) -> None:
    if manifest["lifecycle"] != "stable":
        return

    systems = manifest["platform_systems"]
    failing = [
        name for name in PLATFORM_SYSTEMS
        if systems[name]["result"] not in PASSING_PLATFORM_RESULTS
    ]
    if failing:
        fail("Stable lifecycle requires passing results for all eight Platform Systems; failing: " + ", ".join(failing))

    conformance = manifest["conformance"]
    if conformance["status"] != "conformant":
        fail("Stable lifecycle requires conformance.status=conformant")
    if conformance["validated_at"] is None:
        fail("Stable lifecycle requires conformance.validated_at")
    _validate_iso_datetime(conformance["validated_at"], "conformance.validated_at")

    glaze = systems["glaze_ui"]
    if glaze["result"] != "not-applicable-justified":
        required = manifest["compatibility"]["glaze_ui_required"]
        if required != CURRENT_GLAZE_UI_VERSION:
            fail(f"Stable lifecycle requires compatibility.glaze_ui_required={CURRENT_GLAZE_UI_VERSION!r}")
        if glaze["result"] == "applicable-conformant" and glaze["version"] != required:
            fail("Stable lifecycle requires the conformant Glaze UI version to equal the required Stable target")

    acceptance = manifest["evidence"]["acceptance_tests"]
    passed_categories = {item["category"] for item in acceptance if item["result"] == "passed"}
    missing = sorted(STABLE_ACCEPTANCE_CATEGORIES - passed_categories)
    if missing:
        fail("Stable lifecycle missing passing acceptance categories: " + ", ".join(missing))

    releases = manifest["evidence"]["release"]
    if not any(item["result"] == "published" for item in releases):
        fail("Stable lifecycle requires published release evidence")


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
    _validate_stable_gate(parsed)
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
        f"with all eight Integral Platform Systems declared"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
