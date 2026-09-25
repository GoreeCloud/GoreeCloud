#!/usr/bin/env python3
"""Audit public GoreeCloud root Platform manifests without reclassifying lifecycle.

This diagnostic records the manifest generation and lifecycle vocabulary found
on each public repository's authoritative default branch. It deliberately does
not translate legacy lifecycle values into Platform Contract 2.0 stages and does
not establish conformance, release eligibility, deployment, or production state.
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

import yaml

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "repositories.public.json"
CANONICAL_2_0 = ("seed", "lab", "forge", "weave", "seal", "anchor", "sunset", "archive")
LEGACY_LIFECYCLE = (
    "concept",
    "experimental",
    "development",
    "release-candidate",
    "stable",
    "deprecated",
    "retired",
)
LEGACY_CONTRACTS = {"0.2", "0.3", "0.4"}


def fail(message: str) -> None:
    print(f"platform-portfolio-audit: {message}", file=sys.stderr)
    raise SystemExit(1)


def github_headers() -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "goreecloud-platform-portfolio-auditor",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def get_json(url: str, *, missing_is_none: bool = False) -> Any:
    request = Request(url, headers=github_headers())
    try:
        with urlopen(request, timeout=20) as response:
            return json.load(response)
    except HTTPError as exc:
        if missing_is_none and exc.code == 404:
            return None
        fail(f"cannot read {url}: HTTP {exc.code}")
    except (URLError, TimeoutError, json.JSONDecodeError) as exc:
        fail(f"cannot read {url}: {exc}")


def load_registry() -> tuple[list[str], dict[str, str], str, str]:
    try:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot parse repositories.public.json: {exc}")
    repositories = data.get("repositories")
    defaults = data.get("defaults")
    overrides = data.get("defaultBranchOverrides")
    observed_at = data.get("observedAt")
    if not isinstance(repositories, list) or not repositories:
        fail("public repository registry is empty")
    if not isinstance(defaults, dict) or not isinstance(defaults.get("defaultBranch"), str):
        fail("registry defaults.defaultBranch is missing")
    if not isinstance(overrides, dict):
        fail("registry defaultBranchOverrides is missing")
    if not isinstance(observed_at, str):
        fail("registry observedAt is missing")
    return repositories, overrides, defaults["defaultBranch"], observed_at


def fetch_manifest(repository: str, branch: str) -> tuple[str, str] | None:
    owner, name = repository.split("/", 1)
    url = (
        f"https://api.github.com/repos/{quote(owner)}/{quote(name)}/contents/"
        f"goreecloud.platform.yaml?ref={quote(branch)}"
    )
    payload = get_json(url, missing_is_none=True)
    if payload is None:
        return None
    if not isinstance(payload, dict):
        fail(f"unexpected manifest response for {repository}")
    encoded = payload.get("content")
    encoding = payload.get("encoding")
    sha = payload.get("sha")
    if not isinstance(encoded, str) or encoding != "base64" or not isinstance(sha, str):
        fail(f"manifest bytes unavailable for {repository}")
    try:
        text = base64.b64decode(encoded, validate=False).decode("utf-8")
    except (ValueError, UnicodeDecodeError) as exc:
        fail(f"cannot decode manifest for {repository}: {exc}")
    return text, sha


def classify_manifest(repository: str, branch: str, text: str, sha: str) -> dict[str, Any]:
    row: dict[str, Any] = {
        "repository": repository,
        "default_branch": branch,
        "manifest_present": True,
        "manifest_sha": sha,
        "format": None,
        "contract_version": None,
        "declared_lifecycle": None,
        "lifecycle_vocabulary": None,
        "component_type": None,
        "migration_state": None,
        "parse_status": "parsed",
    }
    try:
        parsed = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        row.update(
            parse_status="malformed",
            migration_state="manual-review-required",
            parse_error=str(exc),
        )
        return row
    if not isinstance(parsed, dict):
        row.update(parse_status="unrecognized", migration_state="manual-review-required")
        return row

    if "schema_version" in parsed and isinstance(parsed.get("component"), dict):
        row["format"] = "versioned-platform-contract"
        version = str(parsed.get("schema_version"))
        lifecycle = parsed.get("lifecycle")
        component_type = parsed["component"].get("type")
        row["contract_version"] = version
        row["declared_lifecycle"] = lifecycle if isinstance(lifecycle, str) else None
        row["component_type"] = component_type if isinstance(component_type, str) else None

        if version == "2.0":
            row["lifecycle_vocabulary"] = "contract-2.0"
            row["migration_state"] = "current-contract"
            if row["declared_lifecycle"] not in CANONICAL_2_0:
                row["parse_status"] = "contract-2.0-invalid-lifecycle"
        elif version in LEGACY_CONTRACTS:
            row["lifecycle_vocabulary"] = f"legacy-contract-{version}"
            row["migration_state"] = "evidence-based-migration-required"
            if row["declared_lifecycle"] not in LEGACY_LIFECYCLE:
                row["parse_status"] = "legacy-contract-unexpected-lifecycle"
        else:
            row["lifecycle_vocabulary"] = "unknown-versioned-contract"
            row["migration_state"] = "manual-review-required"
        compatibility = parsed.get("compatibility")
        if isinstance(compatibility, dict):
            value = compatibility.get("platform_contract")
            if isinstance(value, str):
                row["compatibility_platform_contract"] = value
        return row

    legacy_schema = parsed.get("schema")
    product = parsed.get("product")
    if isinstance(legacy_schema, str) and legacy_schema.startswith("goreecloud.platform/") and isinstance(product, dict):
        row["format"] = "legacy-non-contract-manifest"
        row["contract_version"] = legacy_schema
        lifecycle = product.get("lifecycle")
        row["declared_lifecycle"] = lifecycle if isinstance(lifecycle, str) else None
        row["lifecycle_vocabulary"] = "legacy-non-contract"
        row["component_type"] = None
        row["migration_state"] = "manual-contract-migration-required"
        return row

    row.update(
        format="unrecognized",
        lifecycle_vocabulary="unknown",
        migration_state="manual-review-required",
        parse_status="unrecognized",
    )
    return row


def audit() -> dict[str, Any]:
    repositories, overrides, default_branch, observed_at = load_registry()
    rows: list[dict[str, Any]] = []
    for repository in repositories:
        branch = overrides.get(repository, default_branch)
        manifest = fetch_manifest(repository, branch)
        if manifest is None:
            rows.append(
                {
                    "repository": repository,
                    "default_branch": branch,
                    "manifest_present": False,
                    "manifest_sha": None,
                    "format": None,
                    "contract_version": None,
                    "declared_lifecycle": None,
                    "lifecycle_vocabulary": None,
                    "component_type": None,
                    "migration_state": "manifest-absent",
                    "parse_status": "not-present",
                }
            )
            continue
        text, sha = manifest
        rows.append(classify_manifest(repository, branch, text, sha))

    present = [row for row in rows if row["manifest_present"]]
    versioned = [row for row in present if row["format"] == "versioned-platform-contract"]
    current = [row for row in versioned if row["contract_version"] == "2.0"]
    legacy = [row for row in versioned if row["contract_version"] in LEGACY_CONTRACTS]
    non_contract = [row for row in present if row["format"] == "legacy-non-contract-manifest"]
    problematic = [
        row
        for row in present
        if row["parse_status"] not in {"parsed"}
    ]

    def count(field: str, source: list[dict[str, Any]]) -> dict[str, int]:
        values = Counter(
            str(row[field])
            for row in source
            if row.get(field) is not None
        )
        return dict(sorted(values.items(), key=lambda item: item[0].casefold()))

    return {
        "schema": "goreecloud-platform-portfolio-audit/v1",
        "observed_at": observed_at,
        "scope": "public repositories listed in repositories.public.json",
        "authority": {
            "lifecycle_reclassification": False,
            "platform_conformance": False,
            "release_eligibility": False,
            "deployment": False,
            "production_readiness": False,
            "private_repository_identity": False,
        },
        "canonical_contract": {
            "version": "2.0",
            "lifecycle": list(CANONICAL_2_0),
            "migration_rule": "Legacy state is retained verbatim until the governed unit is reclassified from current evidence.",
        },
        "summary": {
            "repositories_audited": len(rows),
            "manifest_present": len(present),
            "manifest_absent": len(rows) - len(present),
            "versioned_contract_manifests": len(versioned),
            "contract_2_0_manifests": len(current),
            "legacy_versioned_contract_manifests": len(legacy),
            "legacy_non_contract_manifests": len(non_contract),
            "manual_or_invalid_review_rows": len(problematic),
            "contract_versions": count("contract_version", versioned),
            "declared_lifecycles": count("declared_lifecycle", versioned),
            "component_types": count("component_type", versioned),
        },
        "repositories": rows,
    }


def markdown_report(result: dict[str, Any]) -> str:
    s = result["summary"]
    lines = [
        "## Platform Contract portfolio diagnostic",
        "",
        "> Diagnostic only. This audit records manifest generation and declared lifecycle vocabulary. It does not promote, demote, translate, qualify, deploy, or accept a component.",
        "",
        f"- Public repositories audited: **{s['repositories_audited']}**",
        f"- Root manifests present: **{s['manifest_present']}**",
        f"- Root manifests absent: **{s['manifest_absent']}**",
        f"- Versioned Platform Contract manifests: **{s['versioned_contract_manifests']}**",
        f"- Contract 2.0 manifests: **{s['contract_2_0_manifests']}**",
        f"- Legacy versioned manifests: **{s['legacy_versioned_contract_manifests']}**",
        f"- Legacy non-contract manifests: **{s['legacy_non_contract_manifests']}**",
        "",
        f"- Contract versions: `{json.dumps(s['contract_versions'], sort_keys=True)}`",
        f"- Declared versioned lifecycles: `{json.dumps(s['declared_lifecycles'], sort_keys=True)}`",
        "",
        "| Repository | Manifest | Contract / format | Lifecycle | Vocabulary | Migration state |",
        "| --- | :---: | --- | --- | --- | --- |",
    ]
    for row in result["repositories"]:
        contract = row["contract_version"] or "—"
        lifecycle = row["declared_lifecycle"] or "—"
        vocabulary = row["lifecycle_vocabulary"] or "—"
        present = "yes" if row["manifest_present"] else "no"
        lines.append(
            f"| `{row['repository']}` | {present} | `{contract}` | `{lifecycle}` | {vocabulary} | {row['migration_state']} |"
        )
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--markdown-summary", type=Path)
    parser.add_argument(
        "--fail-on-invalid-contract-2",
        action="store_true",
        help="fail if a Contract 2.0 manifest declares a non-canonical lifecycle value",
    )
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
    if args.fail_on_invalid_contract_2:
        invalid = [
            row
            for row in result["repositories"]
            if row["parse_status"] == "contract-2.0-invalid-lifecycle"
        ]
        if invalid:
            fail(
                "Contract 2.0 manifests with invalid lifecycle values: "
                + ", ".join(row["repository"] for row in invalid)
            )


if __name__ == "__main__":
    main()
