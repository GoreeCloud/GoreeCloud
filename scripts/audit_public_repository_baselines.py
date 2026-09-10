#!/usr/bin/env python3
"""Audit public GoreeCloud repositories for repository-baseline controls.

This is a diagnostic inventory, not a lifecycle or conformance evaluator. The
GoreeCloud repository-structure instructions apply mandatory root controls to
application/service repositories, while the public estate also contains
supporting repositories whose applicability still requires authoritative
classification. Missing or structurally invalid controls are therefore reported
but do not fail the audit unless an explicit strict mode is introduced after
scope classification.

The governing baseline also requires each in-scope application/service
FEATURE-ROADMAP.md to remain synchronized with a corresponding Drive
FEATURE-ROADMAP.docx. This GitHub-only diagnostic measures repository-file
presence and basic structural materiality (regular-file type and non-zero size);
Drive counterpart synchronization, semantic completeness, freshness, accuracy,
and placeholder-only content remain outside this script's authority.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "repositories.public.json"

BASELINE_FILES = (
    "README.md",
    "SPECIFICATIONS.md",
    "FEATURES.md",
    "FEATURE-ROADMAP.md",
    "BENEFITS.md",
    "COMPETITIVE-OBJECTIVES.md",
    "BRANDING.md",
    "USER-MANUAL.md",
    "PRIVACY POLICY.md",
    "NOTES.md",
    "SECURITY.md",
    ".gitignore",
    ".editorconfig",
    "goreecloud.platform.yaml",
)


def fail(message: str) -> None:
    print(f"public-repository-baseline-audit: {message}", file=sys.stderr)
    raise SystemExit(1)


def github_headers() -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "goreecloud-public-repository-baseline-auditor",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def get_json(url: str) -> Any:
    request = Request(url, headers=github_headers())
    try:
        with urlopen(request, timeout=20) as response:
            return json.load(response)
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        fail(f"cannot read {url}: {exc}")


def load_registry() -> tuple[list[str], dict[str, str], str]:
    try:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot parse repositories.public.json: {exc}")

    repositories = data.get("repositories")
    if not isinstance(repositories, list) or not repositories:
        fail("repositories.public.json must contain a non-empty repositories list")
    if any(not isinstance(repository, str) for repository in repositories):
        fail("repository identities must be strings")

    defaults = data.get("defaults")
    if not isinstance(defaults, dict) or not isinstance(defaults.get("defaultBranch"), str):
        fail("registry defaults.defaultBranch is required")
    default_branch = defaults["defaultBranch"]

    overrides = data.get("defaultBranchOverrides")
    if not isinstance(overrides, dict) or any(
        not isinstance(repository, str) or not isinstance(branch, str)
        for repository, branch in overrides.items()
    ):
        fail("registry defaultBranchOverrides must map repository names to branch names")

    observed_at = data.get("observedAt")
    if not isinstance(observed_at, str):
        fail("registry observedAt is required")

    return repositories, overrides, default_branch


def root_entries(repository: str, branch: str) -> dict[str, dict[str, Any]]:
    owner, name = repository.split("/", 1)
    url = (
        f"https://api.github.com/repos/{quote(owner)}/{quote(name)}/contents"
        f"?ref={quote(branch)}"
    )
    payload = get_json(url)
    if not isinstance(payload, list):
        fail(f"root contents response for {repository} must be a list")

    entries: dict[str, dict[str, Any]] = {}
    for item in payload:
        if not isinstance(item, dict) or not isinstance(item.get("name"), str):
            continue
        entries[item["name"]] = {
            "type": item.get("type"),
            "size": item.get("size"),
        }
    return entries


def audit() -> dict[str, Any]:
    repositories, overrides, default_branch = load_registry()
    rows: list[dict[str, Any]] = []

    for repository in repositories:
        branch = overrides.get(repository, default_branch)
        entries = root_entries(repository, branch)
        missing = [path for path in BASELINE_FILES if path not in entries]
        invalid_type = [
            path
            for path in BASELINE_FILES
            if path in entries and entries[path].get("type") != "file"
        ]
        zero_byte = [
            path
            for path in BASELINE_FILES
            if path in entries
            and entries[path].get("type") == "file"
            and entries[path].get("size") == 0
        ]
        present = len(BASELINE_FILES) - len(missing)
        structurally_valid = not missing and not invalid_type and not zero_byte
        rows.append(
            {
                "repository": repository,
                "default_branch": branch,
                "present": present,
                "required_file_count": len(BASELINE_FILES),
                "feature_roadmap_present": "FEATURE-ROADMAP.md" in entries,
                "platform_manifest_present": "goreecloud.platform.yaml" in entries,
                "missing": missing,
                "invalid_type": invalid_type,
                "zero_byte": zero_byte,
                "structurally_valid": structurally_valid,
            }
        )

    complete_presence = sum(1 for row in rows if not row["missing"])
    structurally_valid = sum(1 for row in rows if row["structurally_valid"])
    manifest_present = sum(1 for row in rows if row["platform_manifest_present"])
    feature_roadmap_present = sum(1 for row in rows if row["feature_roadmap_present"])
    repositories_with_zero_byte = sum(1 for row in rows if row["zero_byte"])
    repositories_with_invalid_type = sum(1 for row in rows if row["invalid_type"])

    return {
        "schema": "goreecloud-public-repository-baseline-audit/v3",
        "scope": "public repository baseline structural diagnostic only",
        "authority": {
            "lifecycle": False,
            "platform_conformance": False,
            "application_service_classification": False,
            "drive_feature_roadmap_sync": False,
            "semantic_completeness": False,
            "freshness": False,
            "accuracy": False,
            "placeholder_detection": False,
        },
        "required_root_files": list(BASELINE_FILES),
        "structural_checks": {
            "presence": True,
            "regular_file_type": True,
            "non_zero_size": True,
            "semantic_materiality": False,
        },
        "feature_roadmap_requirement": {
            "repository_file": "FEATURE-ROADMAP.md",
            "drive_counterpart": "GoreeCloud/Feature Roadmap/FEATURE-ROADMAP.docx",
            "drive_sync_evaluated_by_this_script": False,
        },
        "summary": {
            "repositories_audited": len(rows),
            "all_baseline_files_present": complete_presence,
            "all_baseline_controls_structurally_valid": structurally_valid,
            "feature_roadmap_present": feature_roadmap_present,
            "platform_manifest_present": manifest_present,
            "repositories_with_one_or_more_missing_baseline_files": len(rows) - complete_presence,
            "repositories_with_zero_byte_baseline_files": repositories_with_zero_byte,
            "repositories_with_non_file_baseline_paths": repositories_with_invalid_type,
        },
        "repositories": rows,
    }


def markdown_report(result: dict[str, Any]) -> str:
    summary = result["summary"]
    rows = result["repositories"]
    lines = [
        "## Public repository baseline diagnostic",
        "",
        "> Structural diagnostic only. Missing, non-file, or zero-byte controls are reported, but the audit does not establish lifecycle, Platform conformance, application/service applicability, semantic completeness, freshness, accuracy, placeholder status, or Drive FEATURE-ROADMAP.docx synchronization.",
        "",
        f"- Public repositories audited: **{summary['repositories_audited']}**",
        f"- Repositories with all {len(BASELINE_FILES)} current baseline paths present: **{summary['all_baseline_files_present']}**",
        f"- Repositories with all {len(BASELINE_FILES)} controls present as non-empty regular files: **{summary['all_baseline_controls_structurally_valid']}**",
        f"- Repositories with `FEATURE-ROADMAP.md` present: **{summary['feature_roadmap_present']}**",
        f"- Repositories with `goreecloud.platform.yaml` present: **{summary['platform_manifest_present']}**",
        f"- Repositories with one or more missing baseline files: **{summary['repositories_with_one_or_more_missing_baseline_files']}**",
        f"- Repositories with zero-byte baseline files: **{summary['repositories_with_zero_byte_baseline_files']}**",
        f"- Repositories with baseline paths that are not regular files: **{summary['repositories_with_non_file_baseline_paths']}**",
        "",
        "| Repository | Present | Structural | Roadmap | Missing | Zero-byte | Invalid type |",
        "| --- | ---: | :---: | :---: | --- | --- | --- |",
    ]
    for row in rows:
        missing = ", ".join(f"`{name}`" for name in row["missing"]) or "—"
        zero_byte = ", ".join(f"`{name}`" for name in row["zero_byte"]) or "—"
        invalid_type = ", ".join(f"`{name}`" for name in row["invalid_type"]) or "—"
        roadmap = "yes" if row["feature_roadmap_present"] else "no"
        structural = "yes" if row["structurally_valid"] else "no"
        lines.append(
            f"| `{row['repository']}` | {row['present']}/{row['required_file_count']} | {structural} | {roadmap} | {missing} | {zero_byte} | {invalid_type} |"
        )
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--json-output",
        type=Path,
        help="write the diagnostic JSON to this path in addition to stdout",
    )
    parser.add_argument(
        "--markdown-summary",
        type=Path,
        help="append a Markdown diagnostic to this file (for example GITHUB_STEP_SUMMARY)",
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


if __name__ == "__main__":
    main()
