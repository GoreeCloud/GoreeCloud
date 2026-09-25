#!/usr/bin/env python3
"""Compute a GoreeCloud Platform Contract 2.0 conformance result."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import re
import sys
from typing import Any

HERE = Path(__file__).resolve().parent
VALIDATOR_PATH = HERE / "validate_platform_manifest.py"
FULL_GIT_REVISION = re.compile(r"^[0-9a-f]{40}$")
EVALUATOR_REPOSITORY = "GoreeCloud/GoreeCloud"

spec = importlib.util.spec_from_file_location("goreecloud_platform_validator", VALIDATOR_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError(f"unable to load validator from {VALIDATOR_PATH}")
validator = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = validator
spec.loader.exec_module(validator)

PLATFORM_SYSTEMS = validator.PLATFORM_SYSTEMS
DISPLAY_NAMES = {
    "manager": "GoreeCloud Manager",
    "privacy_shield": "Privacy Shield",
    "wardveil_security": "Wardveil Security",
    "everkeep": "Everkeep",
    "glaze_ui": "Glaze UI",
    "mesh": "GoreeCloud Mesh",
    "identity": "GoreeCloud Identity",
    "policy": "GoreeCloud Policy",
    "observability": "GoreeCloud Observability",
}


def require_git_revision(value: str, label: str) -> str:
    if not FULL_GIT_REVISION.fullmatch(value):
        raise validator.ValidationError(f"{label} must be an exact 40-character lowercase Git revision")
    return value


def evaluate(manifest: dict[str, Any], *, revision: str, evaluator_revision: str, evaluated_at: str) -> dict[str, Any]:
    revision = require_git_revision(revision, "evaluated revision")
    evaluator_revision = require_git_revision(evaluator_revision, "evaluator revision")
    systems = manifest["platform_systems"]
    acceptance = manifest["evidence"]["acceptance_tests"]
    releases = manifest["evidence"]["release"]
    lifecycle = manifest["lifecycle"]
    lifecycle_metadata = manifest["lifecycle_metadata"]
    candidate_identity = lifecycle_metadata["candidate_identity"]

    checks: list[dict[str, Any]] = []
    blockers: list[str] = []

    for name in PLATFORM_SYSTEMS:
        entry = systems[name]
        result = entry["result"]
        passing = result in validator.PASSING_PLATFORM_RESULTS
        checks.append({
            "id": f"platform-system:{name}",
            "category": "platform-system",
            "result": "passed" if passing else "failed",
            "declared_result": result,
            "evidence": entry["evidence"],
            "message": (
                f"{DISPLAY_NAMES[name]} is {result}."
                if passing else
                f"{DISPLAY_NAMES[name]} remains {result} and cannot satisfy Anchor eligibility."
            ),
        })
        if not passing:
            blockers.append(f"{DISPLAY_NAMES[name]}: {result}")

    glaze = systems["glaze_ui"]
    required_glaze = manifest["compatibility"]["glaze_ui_required"]
    if glaze["result"] != "not-applicable-justified":
        current = (
            required_glaze == validator.CURRENT_GLAZE_UI_VERSION
            and (glaze["result"] != "applicable-conformant" or glaze["version"] == required_glaze)
        )
        checks.append({
            "id": "compatibility:glaze-ui",
            "category": "compatibility",
            "result": "passed" if current else "failed",
            "declared_result": glaze["result"],
            "evidence": glaze["evidence"],
            "message": (
                f"Glaze UI target is current approved {validator.CURRENT_GLAZE_UI_VERSION}."
                if current else
                f"Glaze UI target must be current approved {validator.CURRENT_GLAZE_UI_VERSION}."
            ),
        })
        if not current:
            blockers.append(f"Glaze UI compatibility target is not current approved {validator.CURRENT_GLAZE_UI_VERSION}")

    passed_categories = {item["category"] for item in acceptance if item["result"] == "passed"}
    missing_acceptance = sorted(validator.anchor_acceptance_categories(manifest) - passed_categories)
    checks.append({
        "id": "evidence:anchor-acceptance",
        "category": "evidence",
        "result": "passed" if not missing_acceptance else "failed",
        "evidence": [item["id"] for item in acceptance if item["result"] == "passed"],
        "message": (
            "Required Anchor acceptance evidence categories are present."
            if not missing_acceptance else
            "Missing passing Anchor acceptance categories: " + ", ".join(missing_acceptance)
        ),
    })
    if missing_acceptance:
        blockers.append("Missing passing Anchor acceptance categories: " + ", ".join(missing_acceptance))

    for system, category in validator.SYSTEM_ACCEPTANCE_CATEGORIES.items():
        if systems[system]["result"] == "applicable-conformant" and category not in passed_categories:
            checks.append({
                "id": f"evidence:platform-system:{system}",
                "category": "evidence",
                "result": "failed",
                "declared_result": systems[system]["result"],
                "evidence": systems[system]["evidence"],
                "message": f"Applicable-conformant {DISPLAY_NAMES[system]} lacks passing {category} acceptance evidence.",
            })
            blockers.append(f"{DISPLAY_NAMES[system]} lacks passing {category} acceptance evidence")

    published = [item for item in releases if item["result"] == "published"]
    checks.append({
        "id": "evidence:release",
        "category": "release",
        "result": "passed" if published else "failed",
        "evidence": [item["id"] for item in published],
        "message": "Published release evidence is present." if published else "Published release evidence is missing.",
    })
    if not published:
        blockers.append("Published release evidence is missing")

    declared = manifest["conformance"]
    if declared["status"] != "conformant":
        blockers.extend(declared["blockers"])
    qualification_ready = (
        lifecycle_metadata["qualification_state"] == "passed"
        and bool(lifecycle_metadata["evidence"])
    )
    checks.append({
        "id": "lifecycle:anchor-qualification",
        "category": "evidence",
        "result": "passed" if qualification_ready else "failed",
        "evidence": lifecycle_metadata["evidence"],
        "message": (
            "Anchor qualification state is passed with traceable lifecycle evidence."
            if qualification_ready else
            "Anchor eligibility requires qualification_state=passed and traceable lifecycle evidence."
        ),
    })
    if not qualification_ready:
        blockers.append("Anchor qualification has not passed with traceable lifecycle evidence")

    blockers = list(dict.fromkeys(blockers))
    anchor_eligible = not blockers and declared["status"] == "conformant" and declared["validated_at"] is not None
    if anchor_eligible:
        computed = "conformant"
    elif lifecycle == "anchor":
        computed = "nonconformant"
    elif declared["status"] == "unverified":
        computed = "unverified"
    else:
        computed = "nonconformant"

    return {
        "schema_version": validator.SCHEMA_VERSION,
        "component": manifest["component"]["id"],
        "repository": manifest["component"]["repository"],
        "manifest_schema_version": manifest["schema_version"],
        "evaluated_revision": revision,
        "evaluator_repository": EVALUATOR_REPOSITORY,
        "evaluator_revision": evaluator_revision,
        "evaluated_at": evaluated_at,
        "lifecycle": lifecycle,
        "lifecycle_flags": lifecycle_metadata["flags"],
        "deployment_state": lifecycle_metadata["deployment_state"],
        "qualification_state": lifecycle_metadata["qualification_state"],
        "next_gate": lifecycle_metadata["next_gate"],
        "candidate_source_revision": candidate_identity["source_revision"] if candidate_identity else None,
        "last_lifecycle_transition": lifecycle_metadata["last_transition"],
        "lifecycle_evidence": lifecycle_metadata["evidence"],
        "declared_conformance": declared["status"],
        "computed_conformance": computed,
        "anchor_eligible": anchor_eligible,
        "checks": checks,
        "blockers": blockers,
        "authority": {
            "declaration_owner": manifest["component"]["repository"],
            "aggregation_role": "read-only",
            "aggregators_may_transfer_authority": False,
            "notes": (
                "This computed result evaluates repository declarations and evidence metadata. "
                "GoreeCloud Mesh and GoreeCloud Manager may coordinate or present bounded state; "
                "GoreeCloud Policy may evaluate approved rules; and GoreeCloud Observability may "
                "correlate operational evidence. None acquires another producer's domain authority. "
                "GoreeCloud Sync remains a separately governed application/service capability and is "
                "not part of the nine-system Integral Platform System set."
            ),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--evaluator-revision", required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--evaluated-at")
    args = parser.parse_args()

    try:
        manifest = validator.validate_manifest(args.manifest)
        result = evaluate(
            manifest,
            revision=args.revision,
            evaluator_revision=args.evaluator_revision,
            evaluated_at=args.evaluated_at or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        )
    except validator.ValidationError as exc:
        print(f"platform-conformance: {exc}", file=sys.stderr)
        return 1

    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)

    if manifest["lifecycle"] == "anchor" and not result["anchor_eligible"]:
        print("platform-conformance: Anchor eligibility failed closed", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
