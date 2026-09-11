#!/usr/bin/env python3
"""Audit public Platform-manifest coverage of the exact-revision Suite snapshot.

This script is diagnostic only. The Google Drive Suite inventory remains the
portfolio authority. This derived snapshot must never be used to infer product
lifecycle, repository ownership, Platform acceptance, production readiness, or
release status.
"""

from __future__ import annotations

import argparse
import base64
from collections import defaultdict
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
SNAPSHOT = ROOT / "suite-products.snapshot.json"
MANIFEST_PATH = "goreecloud.platform.yaml"


def fail(message: str) -> None:
    print(f"suite-product-coverage-audit: {message}", file=sys.stderr)
    raise SystemExit(1)


def normalized(value: str) -> str:
    return " ".join(value.split()).casefold()


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot parse {path.name}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path.name} root must be an object")
    return value


def load_snapshot() -> tuple[list[str], dict[str, str], dict[str, Any]]:
    data = load_json(SNAPSHOT)
    if data.get("schema") != "goreecloud-suite-products-snapshot/v1":
        fail("unsupported Suite snapshot schema")
    authority = data.get("authority")
    if not isinstance(authority, dict) or authority.get("authoritative") is not False:
        fail("Suite snapshot must explicitly remain non-authoritative")
    if not isinstance(authority.get("source_document_id"), str) or not isinstance(
        authority.get("source_revision_id"), str
    ):
        fail("Suite snapshot must pin the authoritative Drive document and revision")

    groups = data.get("groups")
    if not isinstance(groups, list):
        fail("Suite snapshot groups must be a list")
    products: list[str] = []
    for group in groups:
        if not isinstance(group, dict) or not isinstance(group.get("name"), str):
            fail("each Suite group must contain a name")
        items = group.get("products")
        if not isinstance(items, list) or any(not isinstance(item, str) for item in items):
            fail(f"Suite group {group.get('name')!r} products must be strings")
        products.extend(items)

    if len(groups) != data.get("functional_group_count"):
        fail("Suite functional_group_count does not match the snapshot groups")
    if len(products) != data.get("product_count"):
        fail("Suite product_count does not match the snapshot products")
    normalized_products = [normalized(product) for product in products]
    if len(set(normalized_products)) != len(normalized_products):
        fail("Suite snapshot contains duplicate product names")

    retired = data.get("retired_current_names", {})
    if not isinstance(retired, dict) or any(
        not isinstance(old, str) or not isinstance(new, str) for old, new in retired.items()
    ):
        fail("retired_current_names must map strings to strings")
    return products, retired, data


def load_registry() -> tuple[list[str], dict[str, str], str]:
    data = load_json(REGISTRY)
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


def headers() -> dict[str, str]:
    result = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "goreecloud-suite-product-coverage-auditor",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token:
        result["Authorization"] = f"Bearer {token}"
    return result


def contents_url(repository: str, path: str, branch: str) -> str:
    owner, name = repository.split("/", 1)
    encoded_path = "/".join(quote(part, safe="") for part in path.split("/"))
    return (
        f"https://api.github.com/repos/{quote(owner, safe='')}/{quote(name, safe='')}"
        f"/contents/{encoded_path}?ref={quote(branch, safe='')}"
    )


def fetch_manifest(repository: str, branch: str) -> tuple[bool, str | None, str | None]:
    request = Request(contents_url(repository, MANIFEST_PATH, branch), headers=headers())
    try:
        with urlopen(request, timeout=20) as response:
            payload = json.load(response)
    except HTTPError as exc:
        if exc.code == 404:
            return False, None, None
        fail(f"cannot read {repository}/{MANIFEST_PATH}@{branch}: HTTP {exc.code}")
    except (URLError, TimeoutError, json.JSONDecodeError) as exc:
        fail(f"cannot read {repository}/{MANIFEST_PATH}@{branch}: {exc}")

    if not isinstance(payload, dict) or payload.get("encoding") != "base64":
        fail(f"unexpected contents payload for {repository}/{MANIFEST_PATH}")
    content = payload.get("content")
    if not isinstance(content, str):
        fail(f"missing manifest content for {repository}")
    try:
        text = base64.b64decode(content, validate=False).decode("utf-8")
        manifest = yaml.safe_load(text)
    except (ValueError, UnicodeDecodeError, yaml.YAMLError) as exc:
        return True, None, exc.__class__.__name__
    if not isinstance(manifest, dict):
        return True, None, "manifest root is not a mapping"
    component = manifest.get("component")
    product_name = component.get("product_name") if isinstance(component, dict) else None
    if product_name is not None and not isinstance(product_name, str):
        return True, None, "component.product_name is not a string"
    return True, product_name, None


def audit() -> dict[str, Any]:
    products, retired_names, snapshot = load_snapshot()
    repositories, overrides, default_branch = load_registry()

    canonical = {normalized(name): name for name in products}
    retired = {normalized(name): replacement for name, replacement in retired_names.items()}
    declarations: dict[str, list[dict[str, str]]] = defaultdict(list)
    non_suite: list[dict[str, str]] = []
    retired_declarations: list[dict[str, str]] = []
    unparseable: list[dict[str, str]] = []
    manifests_present = 0
    manifests_with_product_name = 0

    for repository in repositories:
        branch = overrides.get(repository, default_branch)
        present, product_name, parse_error = fetch_manifest(repository, branch)
        if not present:
            continue
        manifests_present += 1
        if parse_error is not None:
            unparseable.append(
                {"repository": repository, "default_branch": branch, "parse_error": parse_error}
            )
            continue
        if not product_name:
            continue
        manifests_with_product_name += 1
        key = normalized(product_name)
        row = {
            "repository": repository,
            "default_branch": branch,
            "declared_product_name": product_name,
        }
        if key in canonical:
            declarations[key].append(row)
        elif key in retired:
            retired_declarations.append({**row, "canonical_replacement": retired[key]})
        else:
            non_suite.append(row)

    represented = [canonical[key] for key in canonical if declarations.get(key)]
    missing = [canonical[key] for key in canonical if not declarations.get(key)]
    duplicates = [
        {
            "product_name": canonical[key],
            "declarations": rows,
        }
        for key, rows in declarations.items()
        if len(rows) > 1
    ]

    return {
        "schema": "goreecloud-suite-product-coverage-audit/v1",
        "scope": "public default-branch Platform-manifest product-name coverage diagnostic only",
        "authority": {
            "suite_snapshot_is_authoritative": False,
            "suite_source_title": snapshot["authority"]["source_title"],
            "suite_source_document_id": snapshot["authority"]["source_document_id"],
            "suite_source_revision_id": snapshot["authority"]["source_revision_id"],
            "repository_mapping_verdict": False,
            "lifecycle_verdict": False,
            "platform_conformance_verdict": False,
            "runtime_acceptance_verdict": False,
            "production_readiness_verdict": False,
            "missing_manifest_is_product_absence": False,
        },
        "summary": {
            "suite_products": len(products),
            "public_repositories_registered": len(repositories),
            "public_manifests_present": manifests_present,
            "public_manifests_with_product_name": manifests_with_product_name,
            "suite_products_represented_by_public_manifest": len(represented),
            "suite_products_without_public_manifest_name_match": len(missing),
            "non_suite_public_manifest_product_names": len(non_suite),
            "duplicate_suite_product_declarations": len(duplicates),
            "retired_current_name_declarations": len(retired_declarations),
            "unparseable_public_manifests": len(unparseable),
        },
        "suite_products_represented_by_public_manifest": represented,
        "suite_products_without_public_manifest_name_match": missing,
        "non_suite_public_manifest_product_names": non_suite,
        "duplicate_suite_product_declarations": duplicates,
        "retired_current_name_declarations": retired_declarations,
        "unparseable_public_manifests": unparseable,
    }


def markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    missing = report["suite_products_without_public_manifest_name_match"]
    lines = [
        "## Suite product coverage diagnostic",
        "",
        f"- Authoritative Suite products in pinned Drive snapshot: **{summary['suite_products']}**",
        f"- Public repositories registered: **{summary['public_repositories_registered']}**",
        f"- Public Platform manifests present: **{summary['public_manifests_present']}**",
        f"- Suite products represented by a public manifest product name: **{summary['suite_products_represented_by_public_manifest']}**",
        f"- Suite products without a public manifest product-name match: **{summary['suite_products_without_public_manifest_name_match']}**",
        f"- Non-Suite public manifest product names: **{summary['non_suite_public_manifest_product_names']}**",
        f"- Duplicate Suite product declarations: **{summary['duplicate_suite_product_declarations']}**",
        f"- Retired current-name declarations: **{summary['retired_current_name_declarations']}**",
        "",
        "> Diagnostic only. The pinned Google Drive Suite inventory remains authoritative. Missing or differing manifest coverage does not establish product absence, lifecycle state, repository ownership, Platform acceptance, release eligibility, or production readiness.",
    ]
    if missing:
        lines.extend(["", "### Suite products without a public manifest product-name match", ""])
        lines.extend(f"- {name}" for name in missing)
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--markdown-summary", type=Path)
    args = parser.parse_args()

    report = audit()
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    if args.markdown_summary:
        with args.markdown_summary.open("a", encoding="utf-8") as handle:
            handle.write(markdown(report))


if __name__ == "__main__":
    main()
