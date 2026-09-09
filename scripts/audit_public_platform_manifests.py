#!/usr/bin/env python3
"""Audit public GoreeCloud platform manifests against live lifecycle authority.

This script is diagnostic. It reports manifest/component/lifecycle metadata and
Glaze UI version planes without converting transitional differences into
lifecycle, production-readiness, or conformance verdicts.
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
MANIFEST_PATH = "goreecloud.platform.yaml"
GLAZE_REPOSITORY = "GoreeCloud/goreecloud-glaze-ui"
GLAZE_LIFECYCLE_PATH = "registry/lifecycle.json"


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


def audit_manifest(repository: str, branch: str, current_stable: str) -> dict[str, Any]:
    text = fetch_text(repository, MANIFEST_PATH, branch, allow_missing=True)
    if text is None:
        return {
            "repository": repository,
            "default_branch": branch,
            "manifest_present": False,
            "parseable": False,
        }

    row: dict[str, Any] = {
        "repository": repository,
        "default_branch": branch,
        "manifest_present": True,
        "parseable": False,
    }
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        row["parse_error"] = exc.__class__.__name__
        return row
    if not isinstance(data, dict):
        row["parse_error"] = "manifest root is not a mapping"
        return row

    glaze_result = nested(data, "platform_systems", "glaze_ui", "result")
    glaze_version = nested(data, "platform_systems", "glaze_ui", "version")
    compatibility_glaze = nested(data, "compatibility", "glaze_ui_required")
    row.update(
        {
            "parseable": True,
            "schema_version": data.get("schema_version"),
            "component_type": nested(data, "component", "type"),
            "component_id": nested(data, "component", "id"),
            "lifecycle": data.get("lifecycle"),
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
        }
    )
    return row


def counter_dict(values: list[Any]) -> dict[str, int]:
    counter = Counter("<absent>" if value is None else str(value) for value in values)
    return dict(sorted(counter.items(), key=lambda item: item[0].casefold()))


def audit() -> dict[str, Any]:
    repositories, overrides, default_branch = load_registry()
    glaze = live_glaze_stable()
    current_stable = glaze["current_stable"]
    assert isinstance(current_stable, str)

    rows = [
        audit_manifest(repository, overrides.get(repository, default_branch), current_stable)
        for repository in repositories
    ]
    present = [row for row in rows if row["manifest_present"]]
    parseable = [row for row in present if row["parseable"]]

    return {
        "schema": "goreecloud-public-platform-manifest-audit/v1",
        "scope": "public repository manifest metadata diagnostic only",
        "authority": {
            "lifecycle_verdict": False,
            "platform_conformance_verdict": False,
            "production_readiness_verdict": False,
            "glaze_lifecycle_source": f"{GLAZE_REPOSITORY}/{GLAZE_LIFECYCLE_PATH}@main",
            **glaze,
        },
        "summary": {
            "repositories_registered": len(rows),
            "manifests_present": len(present),
            "manifests_parseable": len(parseable),
            "manifests_unparseable": len(present) - len(parseable),
            "component_types": counter_dict([row.get("component_type") for row in parseable]),
            "schema_versions": counter_dict([row.get("schema_version") for row in parseable]),
            "lifecycle_values": counter_dict([row.get("lifecycle") for row in parseable]),
            "glaze_platform_versions": counter_dict([row.get("glaze_platform_version") for row in parseable]),
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
            "platform_systems.glaze_ui.version describes repository-declared Glaze integration state; compatibility.glaze_ui_required describes the Platform Contract compatibility plane. They may differ during a controlled contract rollout.",
            "A version difference is diagnostic evidence only and must not be converted into a conformance, lifecycle, production, or acceptance verdict without the applicable authoritative contract and evidence.",
            "Missing manifests remain part of the separate repository-baseline rollout and are not silently treated as parseable defaults.",
        ],
        "repositories": rows,
    }


def markdown_report(result: dict[str, Any]) -> str:
    authority = result["authority"]
    summary = result["summary"]
    rows = [row for row in result["repositories"] if row["manifest_present"]]
    lines = [
        "## Public Platform manifest diagnostic",
        "",
        "> Metadata-only diagnostic. It does not establish lifecycle, Platform conformance, production readiness, or application/service acceptance.",
        "",
        f"- Live Glaze current Stable: **{authority['current_stable']}**",
        f"- Public repositories registered: **{summary['repositories_registered']}**",
        f"- Platform manifests present: **{summary['manifests_present']}**",
        f"- Parseable manifests: **{summary['manifests_parseable']}**",
        f"- Manifests declaring current Stable in `platform_systems.glaze_ui.version`: **{summary['glaze_platform_version_current_stable']}**",
        f"- Manifests whose Platform Contract compatibility requirement equals current Stable: **{summary['glaze_compatibility_current_stable']}**",
        f"- Manifests with different Glaze integration/compatibility version planes: **{summary['version_plane_differences']}**",
        "",
        "| Repository | Component | Lifecycle | Glaze result | Integration version | Contract requirement |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        if not row["parseable"]:
            lines.append(f"| `{row['repository']}` | — | — | parse error | — | — |")
            continue
        lines.append(
            "| `{repository}` | {component} | {lifecycle} | {result} | {version} | {compatibility} |".format(
                repository=row["repository"],
                component=row.get("component_type") or "—",
                lifecycle=row.get("lifecycle") or "—",
                result=row.get("glaze_result") or "—",
                version=row.get("glaze_platform_version") or "—",
                compatibility=row.get("glaze_compatibility_required") or "—",
            )
        )
    lines.extend(
        [
            "",
            "`platform_systems.glaze_ui.version` and `compatibility.glaze_ui_required` are separate authority planes during the controlled Platform Contract rollout; differences are reported rather than auto-failed.",
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
