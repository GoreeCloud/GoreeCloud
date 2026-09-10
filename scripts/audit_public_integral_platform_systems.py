#!/usr/bin/env python3
"""Audit declarations for all seven GoreeCloud Integral Platform Systems.

This is a public-repository structure-and-metadata diagnostic. It reports the
repository-declared Manager, Privacy Shield, Wardveil Security, Everkeep,
Glaze UI, Mesh, and Identity integration planes without treating declarations,
schema validity, evidence-path counts, or lifecycle labels as independent
runtime acceptance, Platform conformance, production readiness, or Stable
qualification.
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

INTEGRAL_PLATFORM_SYSTEMS = (
    ("manager", "GoreeCloud Manager"),
    ("privacy_shield", "Privacy Shield"),
    ("wardveil_security", "Wardveil Security"),
    ("everkeep", "Everkeep"),
    ("glaze_ui", "Glaze UI"),
    ("mesh", "GoreeCloud Mesh"),
    ("identity", "GoreeCloud Identity"),
)

BLOCKING_RESULTS = {
    "applicable-migration-required",
    "applicable-blocked",
    "applicable-nonconformant",
}


def fail(message: str) -> None:
    print(f"integral-platform-system-audit: {message}", file=sys.stderr)
    raise SystemExit(1)


def headers() -> dict[str, str]:
    result = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "goreecloud-integral-platform-system-auditor",
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


def load_validator() -> Draft202012Validator:
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


def nested(mapping: Any, *keys: str) -> Any:
    value = mapping
    for key in keys:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


def list_count(value: Any) -> int | None:
    return len(value) if isinstance(value, list) else None


def counter_dict(values: list[Any]) -> dict[str, int]:
    counter = Counter("<absent>" if value is None else str(value) for value in values)
    return dict(sorted(counter.items(), key=lambda item: item[0].casefold()))


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
    declarations: dict[str, dict[str, Any]] = {}
    blocking: list[str] = []
    conformant: list[str] = []
    not_applicable: list[str] = []

    for key, label in INTEGRAL_PLATFORM_SYSTEMS:
        result = nested(data, "platform_systems", key, "result")
        version = nested(data, "platform_systems", key, "version")
        evidence = nested(data, "platform_systems", key, "evidence")
        notes = nested(data, "platform_systems", key, "notes")
        declarations[key] = {
            "label": label,
            "result": result,
            "version": version,
            "evidence_count": list_count(evidence),
            "notes_present": isinstance(notes, str) and bool(notes.strip()),
        }
        if result in BLOCKING_RESULTS:
            blocking.append(key)
        elif result == "applicable-conformant":
            conformant.append(key)
        elif result == "not-applicable-justified":
            not_applicable.append(key)

    lifecycle = data.get("lifecycle")
    row.update(
        {
            "parseable": True,
            "schema_valid": not schema_errors,
            "schema_error_count": len(schema_errors),
            "schema_error_samples": [schema_error_text(error) for error in schema_errors[:10]],
            "schema_version": data.get("schema_version"),
            "component_type": nested(data, "component", "type"),
            "component_id": nested(data, "component", "id"),
            "lifecycle": lifecycle,
            "conformance_status": nested(data, "conformance", "status"),
            "integral_platform_systems": declarations,
            "declared_blocking_integral_systems": blocking,
            "declared_conformant_integral_systems": conformant,
            "declared_not_applicable_integral_systems": not_applicable,
            "has_declared_blocking_integral_system": bool(blocking),
            "stable_lifecycle_with_declared_integral_blocker": lifecycle == "stable" and bool(blocking),
        }
    )
    return row


def system_summary(rows: list[dict[str, Any]], key: str) -> dict[str, Any]:
    declarations = [row["integral_platform_systems"][key] for row in rows]
    return {
        "result_values": counter_dict([declaration.get("result") for declaration in declarations]),
        "version_values": counter_dict([declaration.get("version") for declaration in declarations]),
        "repositories_with_zero_declared_evidence": sum(
            1 for declaration in declarations if declaration.get("evidence_count") == 0
        ),
        "repositories_with_no_notes": sum(
            1 for declaration in declarations if declaration.get("notes_present") is False
        ),
    }


def audit() -> dict[str, Any]:
    repositories, overrides, default_branch = load_registry()
    validator = load_validator()
    rows = [
        audit_manifest(repository, overrides.get(repository, default_branch), validator)
        for repository in repositories
    ]
    present = [row for row in rows if row["manifest_present"]]
    parseable = [row for row in present if row["parseable"]]
    schema_valid = [row for row in parseable if row["schema_valid"]]

    system_summaries = {
        key: {
            "label": label,
            **system_summary(parseable, key),
        }
        for key, label in INTEGRAL_PLATFORM_SYSTEMS
    }

    return {
        "schema": "goreecloud-public-integral-platform-system-audit/v1",
        "scope": "public repository Platform manifest declarations for all seven Integral Platform Systems",
        "authority": {
            "application_service_applicability_verdict": False,
            "lifecycle_verdict": False,
            "platform_conformance_verdict": False,
            "production_readiness_verdict": False,
            "runtime_acceptance_verdict": False,
            "declarations_are_independent_acceptance_proof": False,
            "evidence_path_count_is_acceptance": False,
            "schema_validity_is_acceptance": False,
            "platform_manifest_schema_source": str(SCHEMA_PATH.relative_to(ROOT)),
        },
        "integral_platform_system_keys": [key for key, _ in INTEGRAL_PLATFORM_SYSTEMS],
        "summary": {
            "repositories_registered": len(rows),
            "manifests_present": len(present),
            "manifests_parseable": len(parseable),
            "manifests_unparseable": len(present) - len(parseable),
            "manifests_schema_valid": len(schema_valid),
            "manifests_schema_invalid": len(parseable) - len(schema_valid),
            "component_types": counter_dict([row.get("component_type") for row in parseable]),
            "lifecycle_values": counter_dict([row.get("lifecycle") for row in parseable]),
            "conformance_status_values": counter_dict(
                [row.get("conformance_status") for row in parseable]
            ),
            "integral_platform_systems": system_summaries,
            "repositories_with_declared_blocking_integral_system": sum(
                1 for row in parseable if row.get("has_declared_blocking_integral_system") is True
            ),
            "stable_lifecycle_with_declared_integral_blocker": sum(
                1
                for row in parseable
                if row.get("stable_lifecycle_with_declared_integral_blocker") is True
            ),
        },
        "notes": [
            "All seven Integral Platform System planes required by the central schema are reported: Manager, Privacy Shield, Wardveil Security, Everkeep, Glaze UI, Mesh, and Identity.",
            "Repository declarations are metadata. They must not replace producer-system authority, runtime evidence, repository-local acceptance, or the applicable GoreeCloud governing record.",
            "A blocking declaration is surfaced as unresolved evidence, not converted into a new lifecycle or Platform conformance verdict by this diagnostic.",
            "A not-applicable-justified declaration is reported separately and is not silently treated as accepted; applicability remains governed by actual architecture and authoritative project records.",
            "Evidence counts report declared paths only. This diagnostic does not assert that a path exists, is current, proves implementation, or has been independently accepted.",
            "Missing manifests remain part of the separate rollout/applicability work and are not assigned inferred Platform System states.",
        ],
        "repositories": rows,
    }


def compact_system_results(row: dict[str, Any]) -> str:
    if not row.get("parseable"):
        return "—"
    abbreviations = {
        "manager": "Manager",
        "privacy_shield": "Privacy",
        "wardveil_security": "Wardveil",
        "everkeep": "Everkeep",
        "glaze_ui": "Glaze",
        "mesh": "Mesh",
        "identity": "Identity",
    }
    return "; ".join(
        f"{abbreviations[key]}={row['integral_platform_systems'][key].get('result') or '—'}"
        for key, _ in INTEGRAL_PLATFORM_SYSTEMS
    )


def markdown_report(result: dict[str, Any]) -> str:
    summary = result["summary"]
    rows = [row for row in result["repositories"] if row["manifest_present"]]
    lines = [
        "## Seven Integral Platform Systems diagnostic",
        "",
        "> Declaration diagnostic only. It does not establish application/service applicability, runtime acceptance, Platform conformance, production readiness, lifecycle, or Stable qualification.",
        "",
        f"- Public repositories registered: **{summary['repositories_registered']}**",
        f"- Platform manifests present: **{summary['manifests_present']}**",
        f"- Parseable manifests: **{summary['manifests_parseable']}**",
        f"- Schema-valid manifests: **{summary['manifests_schema_valid']}**",
        f"- Schema-invalid parseable manifests: **{summary['manifests_schema_invalid']}**",
        f"- Manifests with at least one declared blocking Integral Platform System: **{summary['repositories_with_declared_blocking_integral_system']}**",
        f"- Stable-lifecycle manifests with at least one declared Integral Platform System blocker: **{summary['stable_lifecycle_with_declared_integral_blocker']}**",
        "",
        "### Integral Platform System declaration distributions",
        "",
    ]
    for key, label in INTEGRAL_PLATFORM_SYSTEMS:
        system = summary["integral_platform_systems"][key]
        distribution = ", ".join(
            f"`{result_name}`={count}"
            for result_name, count in system["result_values"].items()
        )
        lines.append(
            f"- **{label}:** {distribution}; zero declared evidence paths: **{system['repositories_with_zero_declared_evidence']}**; no notes: **{system['repositories_with_no_notes']}**"
        )

    lines.extend(
        [
            "",
            "| Repository | Schema | Component | Lifecycle | Seven Integral Platform System declarations | Conformance declaration |",
            "| --- | :---: | --- | --- | --- | --- |",
        ]
    )
    for row in rows:
        if not row["parseable"]:
            lines.append(f"| `{row['repository']}` | parse error | — | — | — | — |")
            continue
        schema_state = "valid" if row["schema_valid"] else f"invalid ({row['schema_error_count']})"
        lines.append(
            "| `{repository}` | {schema} | {component} | {lifecycle} | {systems} | {conformance} |".format(
                repository=row["repository"],
                schema=schema_state,
                component=row.get("component_type") or "—",
                lifecycle=row.get("lifecycle") or "—",
                systems=compact_system_results(row),
                conformance=row.get("conformance_status") or "—",
            )
        )
        if not row["schema_valid"]:
            for sample in row.get("schema_error_samples", []):
                lines.append(f"  - `{row['repository']}` schema: {sample}")

    lines.extend(
        [
            "",
            "The seven values above are repository declarations only. Applicability, implementation, evidence validity, runtime acceptance, lifecycle, and release eligibility remain controlled by the authoritative project records and producer systems.",
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
