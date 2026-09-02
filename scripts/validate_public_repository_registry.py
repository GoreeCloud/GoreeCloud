#!/usr/bin/env python3
"""Validate the privacy-bounded public GoreeCloud repository registry."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "repositories.public.json"
EXPECTED_SCHEMA = "goreecloud-public-repository-registry/v1"
REPOSITORY_PATTERN = re.compile(r"^GoreeCloud/[A-Za-z0-9._-]+$")
REQUIRED_PUBLIC_REPOSITORIES = {
    "GoreeCloud/GoreeCloud",
    "GoreeCloud/goreecloud-glaze-ui",
    "GoreeCloud/goreecloud-identity",
    "GoreeCloud/goreecloud-mesh",
}


def fail(message: str) -> None:
    print(f"public-repository-registry: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    if not REGISTRY.is_file():
        fail("repositories.public.json is missing")

    try:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot parse registry: {exc}")

    if data.get("schema") != EXPECTED_SCHEMA:
        fail(f"schema must be {EXPECTED_SCHEMA!r}")

    authority = data.get("authority")
    if not isinstance(authority, dict):
        fail("authority object is required")
    if authority.get("owner") != "GoreeCloud":
        fail("authority.owner must remain GoreeCloud")
    for key in ("lifecycleAuthority", "productionAuthority", "platformAcceptanceAuthority"):
        if authority.get(key) is not False:
            fail(f"authority.{key} must remain false")

    privacy = data.get("privacyBoundary")
    if not isinstance(privacy, dict):
        fail("privacyBoundary object is required")
    if privacy.get("publicOnly") is not True:
        fail("registry must remain public-only")
    if privacy.get("privateRepositoryNamesIncluded") is not False:
        fail("private repository identities must not be centralized in this public registry")

    defaults = data.get("defaults")
    if defaults != {"visibility": "public", "archived": False, "defaultBranch": "main"}:
        fail("public repository defaults drifted")

    repositories = data.get("repositories")
    if not isinstance(repositories, list) or not repositories:
        fail("repositories must be a non-empty list")
    if any(not isinstance(repository, str) or not REPOSITORY_PATTERN.fullmatch(repository) for repository in repositories):
        fail("repository names must use GoreeCloud/<repository> syntax")
    if len(repositories) != len(set(repositories)):
        fail("repository names must be unique")
    if repositories != sorted(repositories, key=str.casefold):
        fail("repository names must remain deterministically sorted")
    if len(repositories) < 50:
        fail("public inventory unexpectedly contracted below 50 repositories")

    missing_required = sorted(REQUIRED_PUBLIC_REPOSITORIES - set(repositories))
    if missing_required:
        fail("required public repositories missing: " + ", ".join(missing_required))

    overrides = data.get("defaultBranchOverrides")
    if not isinstance(overrides, dict):
        fail("defaultBranchOverrides must be an object")
    unknown_overrides = sorted(set(overrides) - set(repositories))
    if unknown_overrides:
        fail("branch overrides reference unregistered repositories: " + ", ".join(unknown_overrides))
    for repository, branch in overrides.items():
        if not isinstance(branch, str) or not branch.strip() or branch == defaults["defaultBranch"]:
            fail(f"invalid default-branch override for {repository}")

    notes = data.get("notes")
    if not isinstance(notes, list) or not any("does not imply" in str(note) for note in notes):
        fail("registry must retain its non-acceptance disclaimer")

    print(
        "public-repository-registry: validated "
        f"{len(repositories)} public repositories with {len(overrides)} branch overrides"
    )


if __name__ == "__main__":
    main()
