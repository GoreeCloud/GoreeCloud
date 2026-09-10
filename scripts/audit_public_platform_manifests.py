#!/usr/bin/env python3
"""Audit public GoreeCloud Platform manifests against live authority.

This script is diagnostic. It reports manifest/component/lifecycle metadata,
central-schema validity, required Stable-gate integration declarations, and
Glaze UI version planes without converting repository declarations into
lifecycle, production-readiness, runtime-acceptance, or conformance proof.
"""

from __future__ import annotations

import argparse
import base64
from collections import Counter
import json
import os
from pathlib import Path
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from jsonschema import Draft202012Validator, FormatChecker
import yaml

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "repositories.public.json"
SCHEMA_PATH = ROOT / "schemas" / "goreecloud.platform.schema.json"
MANIFEST_PATH = "goreecloud.platform.yaml"
GLAZE_REPOSITORY = "GoreeCloud/goreecloud-glaze-ui"
GLAZE_LIFECYCLE_PATH = "registry/lifecycle.json"

REQUIRED_STABLE_GATES = (
    ("privacy_shield", "Privacy Shield"),
    ("wardveil_security", "Wardveil Security"),
    ("everkeep", "Everkeep"),
    ("glaze_ui", "Glaze UI"),
)
BLOCKING_RESULTS = {
    "applicable-migration-required",
    "applicable-blocked",
    "applicable-nonconformant",
}


def fail(message: str) -> None:
    print(f"public-platform-manifest-audit: {message}", file=sys.stderr)
    raise SystemExit(1)


def headers() -> dict[str, str]:
    result = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "goreecloud-public-platform-manifest-auditor",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token:
        result["Authorization"] = f"Bearer {token}"
    return result


def get_json(url: str, *, allow_missing: bool = False) -> Any | None:
    request = Request(url, headers=headers())
    try:
        with urlopen(request, timeout=20) as response:
            return json.load(response)
    except HTTPError as exc:
        if allow_missing and exc.code == 404:
            return None
        fail(f"cannot read {url}: HTTP {exc.code}")
    except (URLError, TimeoutError, json.JSONDecodeError) as exc:
        fail(f"cannot read {url}: {exc}")


def load_registry() -> tuple[list[str], dict[str, str], str]:
    try:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot parse repositories.public.json: {exc}")

    repositories = data.get("repositories")
    defaults = data.get("defaults")
    overrides = data.get("defaultBranchOverrides")
    if not isinstance(repositories, list) or any(not isinstance(item, str) for item in repositories):
        fail("registry repositories must be a list of strings")
    if not isinstance(defaults, dict) or not isinstance(defaults.get("defaultBranch"), str):
        fail("registry defaults.defaultBranch is required")
    if not isinstance(overrides, dict) or any(
        not isinstance(repository, str) or not isinstance(branch, str)
        for repository, branch in overrides.items()
    ):
        fail("registry defaultBranchOverrides must map strings to strings")
    return repositories, overrides, defaults["defaultBranch"]


def load_platform_validator() -> Draft202012Validator:
    try:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot parse central Platform manifest schema: {exc}")
    try:
        Draft202012Validator.check_schema(schema)
    except Exception as exc:  # jsonschema exposes multiple schema error subclasses
        fail(f"central Platform manifest schema is invalid: {exc}")
    return Draft202012Validator(schema, format_checker=FormatChecker())


def contents_url(repository: str, path: str, branch: str) -> str:
    owner, name = repository.split("/", 1)
    encoded_path = "/".join(quote(part, safe="") for part in path.split("/"))
    return (
        f"https://api.github.com/repos/{quote(owner, safe='')}/{quote(name, safe='')}"
        f"/contents/{encoded_path}?ref={quote(branch, safe='')}"
    )


def fetch_text(repository: str, path: str, branch: str, *, allow_missing: bool = False) -> str | None:
    payload = get_json(contents_url(repository, path, branch), allow_missing=allow_missing)
    if payload is None:
        return None
    if not isinstance(payload, dict):
        fail(f"unexpected contents payload for {repository}/{path}")
    content = payload.get("content")
    encoding = payload.get("encoding")
    if not isinstance(content, str) or encoding != "base64":
        fail(f"unsupported contents encoding for {repository}/{path}")
    try:
        return base64.b64decode(content, validate=False).decode("utf-8")
    except (ValueError, UnicodeDecodeError) as exc:
        fail(f"cannot decode {repository}/{path}: {exc}")


def live_glaze_stable() -> dict[str, str | None]:
    text = fetch_text(GLAZE_REPOSITORY, GLAZE_LIFECYCLE_PATH, "main")
    assert text is not None
    try:
        lifecycle = json.loads(text)
    except json.JSONDecodeError as exc:
        fail(f"cannot parse live Glaze lifecycle: {exc}")
    current_stable = lifecycle.get("currentStable")
    current_official = lifecycle.get("currentOfficial")
    active_candidate = lifecycle.get("activeCandidate")
    planned_next = lifecycle.get("plannedNext")
    if not isinstance(current_stable, str) or not isinstance(current_official, str):
        fail("live Glaze lifecycle is missing currentStable/currentOfficial")
    if active_candidate is not None and not isinstance(active_candidate, str):
        fail("live Glaze activeCandidate must be null or a string")
    if planned_next is not None and not isinstance(planned_next, str):
        fail("live Glaze plannedNext must be null or a string")
    return {
        "current_stable": current_stable,
        "current_official": current_official,
        "active_candidate": active_candidate,
        "planned_next": planned_next,
    }


def nested(mapping: Any, *keys: str) -> Any:
    value = mapping
    for key in keys:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


def list_count(value: Any) -> int | None:
    return len(value) if isinstance(value, list) else None


def schema_error_text(error: Any) -> str:
    path = "$"
    for part in error.absolute_path:
        if isinstance(part, int):
            path += f"[{part}]"
        else:
            path += f".{part}"
    return f"{path}: {error.message}"


def audit_manifest(
    repository: str,
    branch: str,
    current_stable: str,
    validator: Draft202012Validator,
) -> dict[str, Any]:
    text = fetch_text(repository, MANIFEST_PATH, branch, allow_missing=True)
    if text is None:
        return {
            "repository": repository,
            "default_branch": branch,
            "manifest_present": False,
            "parseable": False,
            "schema_valid": False,
        }

    row: dict[str, Any] = {
        "repository": repository,
        "default_branch": branch,
        "manifest_present": True,
        "parseable": False,
        "schema_valid": False,
    }
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        row["parse_error"] = exc.__class__.__name__
        return row
    if not isinstance(data, dict):
        row["parse_error"] = "manifest root is not a mapping"
        return row

    schema_errors = sorted(
        validator.iter_errors(data),
        key=lambda error: tuple(str(part) for part in error.absolute_path),
    )
    row["schema_valid"] = not schema_errors
    row["schema_error_count"] = len(schema_errors)
    row["schema_error_samples"] = [schema_error_text(error) for error in schema_errors[:10]]

    gate_declarations: dict[str, dict[str, Any]] = {}
    declared_blocking_gates: list[str] = []
    declared_conformant_gates: list[str] = []
    declared_not_applicable_gates: list[str] = []
    for key, label in REQUIRED_STABLE_GATES:
        result = nested(data, "platform_systems", key, "result")
        version = nested(data, "platform_systems", key, "version")
        evidence = nested(data, "platform_systems", key, "evidence")
        gate_declarations[key] = {
            "label": label,
            "result": result,
            "version": version,
            "evidence_count": list_count(evidence),
        }
        if result in BLOCKING_RESULTS:
            declared_blocking_gates.append(key)
        elif result == "applicable-conformant":
            declared_conformant_gates.append(key)
        elif result == "not-applicable-justified":
            declared_not_applicable_gates.append(key)

    glaze_result = gate_declarations["glaze_ui"]["result"]
    glaze_version = gate_declarations["glaze_ui"]["version"]
    compatibility_glaze = nested(data, "compatibility", "glaze_ui_required")
    lifecycle = data.get("lifecycle")
    conformance_status = nested(data, "conformance", "status")
    conformance_validated_at = nested(data, "conformance", "validated_at")

    row.update(
        {
            "parseable": True,
            "schema_version": data.get("schema_version"),
            "component_type": nested(data, "component", "type"),
            "component_id": nested(data, "component", "id"),
            "lifecycle": lifecycle,
            "required_stable_gates": gate_declarations,
            "declared_blocking_stable_gates": declared_blocking_gates,
            "declared_conformant_stable_gates": declared_conformant_gates,
            "declared_not_applicable_stable_gates": declared_not_applicable_gates,
            "has_declared_blocking_stable_gate": bool(declared_blocking_gates),
            "stable_lifecycle_with_declared_gate_blocker": (
                lifecycle == "stable" and bool(declared_blocking_gates)
            ),
            "glaze_result": glaze_result,
            "glaze_platform_version": glaze_version,
            "glaze_platform_version_is_current_stable": glaze_version == current_stable,
            "glaze_compatibility_required": compatibility_glaze,
            "glaze_compatibility_is_current_stable": compatibility_glaze == current_stable,
            "version_plane_differs": (
                isinstance(glaze_version, str)
                and isinstance(compatibility_glaze, str)
                and glaze_version != compatibility_glaze
            ),
            "conformance_status": conformance_status,
            "conformance_validated_at": conformance_validated_at,
            "conformance_blocker_count": list_count(nested(data, "conformance", "blockers")),
            "acceptance_evidence_count": list_count(nested(data, "evidence", "acceptance_tests")),
            "release_evidence_count": list_count(nested(data, "evidence", "release")),
        }
    )
    return row


def counter_dict(values: list[Any]) -> dict[str, int]:
    counter = Counter("<absent>" if value is None else str(value) for value in values)
    return dict(sorted(counter.items(), key=lambda item: item[0].casefold()))


def gate_summary(rows: list[dict[str, Any]], gate_key: str) -> dict[str, Any]:
    declarations = [row["required_stable_gates"][gate_key] for row in rows]
    return {
        "result_values": counter_dict([declaration.get("result") for declaration in declarations]),
        "version_values": counter_dict([declaration.get("version") for declaration in declarations]),
        "repositories_with_zero_declared_evidence": sum(
            1 for declaration in declarations if declaration.get("evidence_count") == 0
        ),
    }


def audit() -> dict[str, Any]:
    repositories, overrides, default_branch = load_registry()
    validator = load_platform_validator()
    glaze = live_glaze_stable()
    current_stable = glaze["current_stable"]
    assert isinstance(current_stable, str)

    rows = [
        audit_manifest(
            repository,
            overrides.get(repository, default_branch),
            current_stable,
            validator,
        )
        for repository in repositories
    ]
    present = [row for row in rows if row["manifest_present"]]
    parseable = [row for row in present if row["parseable"]]
    schema_valid = [row for row in parseable if row["schema_valid"]]

    required_gate_summaries = {
        gate_key: {
            "label": label,
            **gate_summary(parseable, gate_key),
        }
        for gate_key, label in REQUIRED_STABLE_GATES
    }

    return {
        "schema": "goreecloud-public-platform-manifest-audit/v3",
        "scope": "public repository manifest structure and metadata diagnostic only",
        "authority": {
            "lifecycle_verdict": False,
            "platform_conformance_verdict": False,
            "production_readiness_verdict": False,
            "runtime_acceptance_verdict": False,
            "required_gate_declarations_are_proof": False,
            "schema_validity_is_acceptance": False,
            "platform_manifest_schema_source": str(SCHEMA_PATH.relative_to(ROOT)),
            "glaze_lifecycle_source": f"{GLAZE_REPOSITORY}/{GLAZE_LIFECYCLE_PATH}@main",
            **glaze,
        },
        "required_stable_gate_keys": [gate_key for gate_key, _ in REQUIRED_STABLE_GATES],
        "summary": {
            "repositories_registered": len(rows),
            "manifests_present": len(present),
            "manifests_parseable": len(parseable),
            "manifests_unparseable": len(present) - len(parseable),
            "manifests_schema_valid": len(schema_valid),
            "manifests_schema_invalid": len(parseable) - len(schema_valid),
            "component_types": counter_dict([row.get("component_type") for row in parseable]),
            "schema_versions": counter_dict([row.get("schema_version") for row in parseable]),
            "lifecycle_values": counter_dict([row.get("lifecycle") for row in parseable]),
            "conformance_status_values": counter_dict(
                [row.get("conformance_status") for row in parseable]
            ),
            "required_stable_gates": required_gate_summaries,
            "repositories_with_declared_blocking_stable_gate": sum(
                1 for row in parseable if row.get("has_declared_blocking_stable_gate") is True
            ),
            "stable_lifecycle_with_declared_gate_blocker": sum(
                1
                for row in parseable
                if row.get("stable_lifecycle_with_declared_gate_blocker") is True
            ),
            "glaze_platform_versions": counter_dict(
                [row.get("glaze_platform_version") for row in parseable]
            ),
            "glaze_compatibility_requirements": counter_dict(
                [row.get("glaze_compatibility_required") for row in parseable]
            ),
            "glaze_platform_version_current_stable": sum(
                1 for row in parseable if row.get("glaze_platform_version_is_current_stable") is True
            ),
            "glaze_compatibility_current_stable": sum(
                1 for row in parseable if row.get("glaze_compatibility_is_current_stable") is True
            ),
            "version_plane_differences": sum(
                1 for row in parseable if row.get("version_plane_differs") is True
            ),
        },
        "notes": [
            "Schema validation uses the exact central schemas/goreecloud.platform.schema.json carried by the audit candidate. Schema validity establishes structural compatibility only; it is not runtime, lifecycle, release, or Platform acceptance evidence.",
            "Privacy Shield, Wardveil Security, Everkeep, and Glaze UI are reported as required Stable-gate declaration planes. Manifest declarations are diagnostic metadata and are not substituted for the latest applicable Stable contract, runtime evidence, or acceptance decision.",
            "A blocking declaration (applicable-migration-required, applicable-blocked, or applicable-nonconformant) is surfaced as unresolved portfolio evidence. A not-applicable-justified declaration is reported separately and is not silently treated as accepted.",
            "platform_systems.glaze_ui.version describes repository-declared Glaze integration state; compatibility.glaze_ui_required describes the Platform Contract compatibility plane. They may differ during a controlled contract rollout.",
            "A version difference is diagnostic evidence only and must not be converted into a conformance, lifecycle, production, or acceptance verdict without the applicable authoritative contract and evidence.",
            "Missing manifests remain part of the separate repository-baseline rollout and are not silently treated as parseable defaults.",
        ],
        "repositories": rows,
    }


def compact_gate_results(row: dict[str, Any]) -> str:
    if not row.get("parseable"):
        return "—"
    abbreviations = {
        "privacy_shield": "Privacy",
        "wardveil_security": "Wardveil",
        "everkeep": "Everkeep",
        "glaze_ui": "Glaze",
    }
    parts = []
    for gate_key, _ in REQUIRED_STABLE_GATES:
        result = row["required_stable_gates"][gate_key].get("result") or "—"
        parts.append(f"{abbreviations[gate_key]}={result}")
    return "; ".join(parts)


def markdown_report(result: dict[str, Any]) -> str:
    authority = result["authority"]
    summary = result["summary"]
    rows = [row for row in result["repositories"] if row["manifest_present"]]
    lines = [
        "## Public Platform manifest diagnostic",
        "",
        "> Structure-and-metadata diagnostic only. It does not establish lifecycle, Platform conformance, runtime acceptance, production readiness, or application/service acceptance.",
        "",
        f"- Live Glaze current Stable: **{authority['current_stable']}**",
        f"- Public repositories registered: **{summary['repositories_registered']}**",
        f"- Platform manifests present: **{summary['manifests_present']}**",
        f"- Parseable manifests: **{summary['manifests_parseable']}**",
        f"- Manifests valid against the candidate's central Platform schema: **{summary['manifests_schema_valid']}**",
        f"- Parseable manifests invalid against the candidate's central Platform schema: **{summary['manifests_schema_invalid']}**",
        f"- Manifests with at least one declared blocking Stable-gate result: **{summary['repositories_with_declared_blocking_stable_gate']}**",
        f"- Stable-lifecycle manifests that also declare a blocking Stable-gate result: **{summary['stable_lifecycle_with_declared_gate_blocker']}**",
        f"- Manifests declaring current Stable in `platform_systems.glaze_ui.version`: **{summary['glaze_platform_version_current_stable']}**",
        f"- Manifests whose Platform Contract compatibility requirement equals current Stable: **{summary['glaze_compatibility_current_stable']}**",
        f"- Manifests with different Glaze integration/compatibility version planes: **{summary['version_plane_differences']}**",
        "",
        "### Required Stable-gate declaration distributions",
        "",
    ]
    for gate_key, label in REQUIRED_STABLE_GATES:
        gate = summary["required_stable_gates"][gate_key]
        distribution = ", ".join(
            f"`{result}`={count}" for result, count in gate["result_values"].items()
        )
        lines.append(
            f"- **{label}:** {distribution}; zero declared evidence paths: **{gate['repositories_with_zero_declared_evidence']}**"
        )

    lines.extend(
        [
            "",
            "| Repository | Schema | Component | Lifecycle | Required Stable-gate declarations | Glaze integration | Contract requirement | Conformance declaration |",
            "| --- | :---: | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in rows:
        if not row["parseable"]:
            lines.append(f"| `{row['repository']}` | parse error | — | — | — | — | — | — |")
            continue
        schema_state = "valid" if row["schema_valid"] else f"invalid ({row['schema_error_count']})"
        lines.append(
            "| `{repository}` | {schema} | {component} | {lifecycle} | {gates} | {version} | {compatibility} | {conformance} |".format(
                repository=row["repository"],
                schema=schema_state,
                component=row.get("component_type") or "—",
                lifecycle=row.get("lifecycle") or "—",
                gates=compact_gate_results(row),
                version=row.get("glaze_platform_version") or "—",
                compatibility=row.get("glaze_compatibility_required") or "—",
                conformance=row.get("conformance_status") or "—",
            )
        )
        if not row["schema_valid"]:
            for sample in row.get("schema_error_samples", []):
                lines.append(f"  - `{row['repository']}` schema: {sample}")
    lines.extend(
        [
            "",
            "Schema validity is structural compatibility only, not acceptance. Required Stable-gate values above are repository declarations, not independent acceptance evidence. `platform_systems.glaze_ui.version` and `compatibility.glaze_ui_required` are separate authority planes during controlled Platform Contract rollout; differences are reported rather than auto-failed.",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--markdown-summary", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = audit()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    print(rendered, end="")
    if args.json_output:
        args.json_output.write_text(rendered, encoding="utf-8")
    if args.markdown_summary:
        with args.markdown_summary.open("a", encoding="utf-8") as handle:
            handle.write(markdown_report(result))


if __name__ == "__main__":
    main()
