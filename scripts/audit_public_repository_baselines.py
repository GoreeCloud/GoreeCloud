#!/usr/bin/env python3
"""Audit public GoreeCloud repositories for repository-baseline file presence.

This is a diagnostic inventory, not a lifecycle or conformance evaluator. The
GoreeCloud repository-structure instructions apply mandatory root files to
application/service repositories, while the public estate also contains
supporting repositories whose applicability still requires authoritative
classification. Missing files are therefore reported but do not fail the audit
unless an explicit strict mode is introduced after scope classification.
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
    "BENEFITS.md",
    "COMPETITIVE-OBJECTIVES.md",
    "BRANDING.md",
    "USER-MANUAL.md",
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


def root_names(repository: str, branch: str) -> set[str]:
    owner, name = repository.split("/", 1)
    url = (
        f"https://api.github.com/repos/{quote(owner)}/{quote(name)}/contents"
        f"?ref={quote(branch)}"
    )
    payload = get_json(url)
    if not isinstance(payload, list):
        fail(f"root contents response for {repository} must be a list")

    names: set[str] = set()
    for item in payload:
        if isinstance(item, dict) and isinstance(item.get("name"), str):
            names.add(item["name"])
    return names


def audit() -> dict[str, Any]:
    repositories, overrides, default_branch = load_registry()
    rows: list[dict[str, Any]] = []

    for repository in repositories:
        branch = overrides.get(repository, default_branch)
        names = root_names(repository, branch)
        missing = [path for path in BASELINE_FILES if path not in names]
        rows.append(
            {
                "repository": repository,
                "default_branch": branch,
                "present": len(BASELINE_FILES) - len(missing),
                "required_file_count": len(BASELINE_FILES),
                "missing": missing,
            }
        )

    complete = sum(1 for row in rows if not row["missing"])
    manifest_present = sum(
        1 for row in rows if "goreecloud.platform.yaml" not in row["missing"]
    )

    return {
        "schema": "goreecloud-public-repository-baseline-audit/v1",
        "scope": "public repository file-presence diagnostic only",
        "authority": {
            "lifecycle": False,
            "platform_conformance": False,
            "application_service_classification": False,
        },
        "required_root_files": list(BASELINE_FILES),
        "summary": {
            "repositories_audited": len(rows),
            "all_baseline_files_present": complete,
            "platform_manifest_present": manifest_present,
            "repositories_with_one_or_more_missing_baseline_files": len(rows) - complete,
        },
        "repositories": rows,
    }


def markdown_report(result: dict[str, Any]) -> str:
    summary = result["summary"]
    rows = result["repositories"]
    lines = [
        "## Public repository baseline diagnostic",
        "",
        "> Presence-only diagnostic. Missing files do not by themselves establish lifecycle, Platform conformance, or application/service applicability.",
        "",
        f"- Public repositories audited: **{summary['repositories_audited']}**",
        f"- Repositories with all {len(BASELINE_FILES)} baseline files present: **{summary['all_baseline_files_present']}**",
        f"- Repositories with `goreecloud.platform.yaml` present: **{summary['platform_manifest_present']}**",
        f"- Repositories with one or more missing baseline files: **{summary['repositories_with_one_or_more_missing_baseline_files']}**",
        "",
        "| Repository | Present | Missing |",
        "| --- | ---: | --- |",
    ]
    for row in rows:
        missing = ", ".join(f"`{name}`" for name in row["missing"]) or "—"
        lines.append(
            f"| `{row['repository']}` | {row['present']}/{row['required_file_count']} | {missing} |"
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
