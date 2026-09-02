#!/usr/bin/env python3
"""Validate goreecloud.platform.yaml and emit a machine-readable conformance result."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys

try:
    import yaml
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:
    print("platform-contract: install PyYAML and jsonschema", file=sys.stderr)
    raise SystemExit(2) from exc

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = ROOT / "schemas" / "goreecloud.platform.schema.json"
DEFAULT_RESULT_SCHEMA = ROOT / "schemas" / "goreecloud.conformance-result.schema.json"
DEFAULT_RULES = ROOT / "contracts" / "goreecloud.platform-rules.v1.json"


def fail(message: str, code: int = 1) -> None:
    print(f"platform-contract: {message}", file=sys.stderr)
    raise SystemExit(code)


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing {path}")
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path}: {exc}")


def load_yaml(path: Path) -> dict:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing {path}")
    except yaml.YAMLError as exc:
        fail(f"invalid YAML in {path}: {exc}")
    if not isinstance(data, dict):
        fail(f"{path} must contain one YAML mapping")
    return data


def schema_errors(schema: dict, instance: dict) -> list[str]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(instance), key=lambda item: list(item.absolute_path))
    rendered = []
    for error in errors:
        where = ".".join(str(part) for part in error.absolute_path) or "<root>"
        rendered.append(f"{where}: {error.message}")
    return rendered


def evidence_index(contract: dict) -> dict[str, dict]:
    by_id = {}
    for item in contract["evidence"]["acceptance"] + contract["evidence"]["release"]:
        evidence_id = item["id"]
        if evidence_id in by_id:
            fail(f"duplicate evidence id {evidence_id}")
        by_id[evidence_id] = item
    return by_id


def check_inventory(contract: dict, rules: dict) -> dict[str, dict]:
    by_id = {}
    for check in contract["conformance"]["checks"]:
        if check["id"] in by_id:
            fail(f"duplicate conformance check id {check['id']}")
        by_id[check["id"]] = check
    missing = sorted(set(rules["required_checks"]) - set(by_id))
    if missing:
        fail("missing required conformance checks: " + ", ".join(missing))
    return by_id


def verify_references(contract: dict, evidence: dict[str, dict]) -> None:
    referenced = [
        ("glaze_ui", contract["glaze_ui"]["evidence"]),
        ("mesh", contract["mesh"]["evidence"]),
        ("recovery", contract["recovery"]["evidence"]),
        ("data_portability", contract["data_portability"]["evidence"]),
    ]
    referenced.extend(
        (f"platform_systems.{name}", value["evidence"])
        for name, value in contract["platform_systems"].items()
    )
    referenced.extend(
        (f"conformance.checks.{check['id']}", check["evidence"])
        for check in contract["conformance"]["checks"]
    )
    for where, refs in referenced:
        missing = [ref for ref in refs if ref not in evidence]
        if missing:
            fail(f"{where} references missing evidence ids: {', '.join(missing)}")


def evaluate(contract: dict, rules: dict, source_revision: str | None) -> dict:
    evidence = evidence_index(contract)
    verify_references(contract, evidence)
    checks = check_inventory(contract, rules)
    implementation_kinds = set(rules["implementation_evidence_kinds"])
    requirements = []
    missing_evidence = []
    all_mandatory_pass = True

    for check_id in rules["required_checks"]:
        check = checks[check_id]
        refs = check["evidence"]
        items = [evidence[ref] for ref in refs]
        reason = ""
        if check["status"] == "not_applicable":
            result = "not_applicable" if not check["mandatory"] else "fail"
            if check["mandatory"]:
                reason = "mandatory requirement cannot be waived as not_applicable"
        elif check["status"] != "pass":
            result = "fail"
            reason = f"declared {check['status']}"
        elif not refs:
            result = "fail"
            reason = "pass has no evidence"
        elif check["mandatory"] and not any(item["kind"] in implementation_kinds for item in items):
            result = "fail"
            reason = "mandatory pass is supported only by documentation evidence"
        else:
            result = "pass"

        if check["mandatory"] and result != "pass":
            all_mandatory_pass = False
            if not refs or not any(item["kind"] in implementation_kinds for item in items):
                missing_evidence.append(check_id)

        requirements.append({
            "id": check_id,
            "mandatory": check["mandatory"],
            "declared_status": check["status"],
            "result": result,
            "evidence": refs,
            "reason": reason,
        })

    current_glaze = rules["current_glaze_ui"]
    glaze = contract["glaze_ui"]
    glaze_ok = (not glaze["applicable"]) or (
        glaze["implemented_version"] == current_glaze and glaze["migration_status"] == "current"
    )
    systems_ok = all(
        value["status"] in {"Applicable — Conformant", "Not Applicable — Justified"}
        for value in contract["platform_systems"].values()
    )
    recovery = contract["recovery"]
    restore_ok = (not recovery["restore_required"]) or (
        recovery["restore_status"] == "verified" and recovery["last_verified_restore"] is not None
    )
    overall_ok = all_mandatory_pass and glaze_ok and systems_ok and restore_ok

    if contract["conformance"]["declared_state"] == "conformant" and not overall_ok:
        fail("declaration claims conformant but computed conformance is non-conformant")
    if contract["conformance"]["stable_eligible"] and not overall_ok:
        fail("declaration claims Stable eligibility but computed Stable eligibility is false")

    return {
        "result_version": "1.0",
        "component_id": contract["component"]["id"],
        "repository": contract["component"]["repository"],
        "source_revision": source_revision,
        "evaluated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "contract_schema_version": contract["schema_version"],
        "overall_result": "conformant" if overall_ok else "non-conformant",
        "declared_state": contract["conformance"]["declared_state"],
        "stable_eligible": overall_ok,
        "lifecycle": contract["component"]["lifecycle"],
        "requirements": requirements,
        "missing_mandatory_evidence": sorted(set(missing_evidence)),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("contract", type=Path)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--result-schema", type=Path, default=DEFAULT_RESULT_SCHEMA)
    parser.add_argument("--rules", type=Path, default=DEFAULT_RULES)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--expected-repository")
    parser.add_argument("--source-revision", default=os.environ.get("GITHUB_SHA"))
    args = parser.parse_args()

    contract = load_yaml(args.contract)
    schema = load_json(args.schema)
    rules = load_json(args.rules)
    errors = schema_errors(schema, contract)
    if errors:
        fail("schema validation failed:\n  - " + "\n  - ".join(errors))
    if args.expected_repository and contract["component"]["repository"] != args.expected_repository:
        fail(f"component.repository must be {args.expected_repository}")
    if contract["glaze_ui"]["required_version"] != rules["current_glaze_ui"]:
        fail("Glaze UI required_version does not match the current platform rule")

    result = evaluate(contract, rules, args.source_revision)
    result_errors = schema_errors(load_json(args.result_schema), result)
    if result_errors:
        fail("generated result failed schema validation:\n  - " + "\n  - ".join(result_errors))
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")

    if contract["component"]["lifecycle"] == "Stable" and not result["stable_eligible"]:
        fail("Stable lifecycle is not eligible: mandatory platform conformance is incomplete")


if __name__ == "__main__":
    main()
