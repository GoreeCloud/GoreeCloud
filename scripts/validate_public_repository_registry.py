#!/usr/bin/env python3
"""Validate the privacy-bounded public GoreeCloud repository registry."""

from __future__ import annotations

from datetime import date, datetime
import json
import os
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "repositories.public.json"
INVENTORY = ROOT / "REPOSITORIES.md"
EXPECTED_SCHEMA = "goreecloud-public-repository-registry/v1"
REPOSITORY_PATTERN = re.compile(r"^GoreeCloud/[A-Za-z0-9._-]+$")
INVENTORY_REPOSITORY_PATTERN = re.compile(
    r"^\d+\. \[`(?P<repository>GoreeCloud/[A-Za-z0-9._-]+)`\]"
    r"\(https://github\.com/(?P=repository)\)$",
    re.MULTILINE,
)
REQUIRED_PUBLIC_REPOSITORIES = {
    "GoreeCloud/GoreeCloud",
    "GoreeCloud/goreecloud-glaze-ui",
    "GoreeCloud/goreecloud-identity",
    "GoreeCloud/goreecloud-mesh",
}
GITHUB_PUBLIC_REPOSITORIES_URL = (
    "https://api.github.com/users/GoreeCloud/repos"
    "?type=owner&sort=full_name&direction=asc&per_page=100&page={page}"
)


def fail(message: str) -> None:
    print(f"public-repository-registry: {message}", file=sys.stderr)
    raise SystemExit(1)


def require_iso_date(value: object, field: str) -> date:
    if not isinstance(value, str):
        fail(f"{field} must be an ISO date")
    try:
        return date.fromisoformat(value)
    except ValueError:
        fail(f"{field} must use YYYY-MM-DD")


def parse_inventory(inventory_text: str) -> tuple[date, int, int, int, int, list[str]]:
    observed_match = re.search(r"^\*\*Observed:\*\* (.+)$", inventory_text, re.MULTILINE)
    if not observed_match:
        fail("REPOSITORIES.md must contain an Observed date")
    try:
        observed = datetime.strptime(observed_match.group(1), "%B %d, %Y").date()
    except ValueError:
        fail("REPOSITORIES.md Observed date must use Month D, YYYY")

    def summary_count(label: str) -> int:
        match = re.search(
            rf"^\| {re.escape(label)} \| (?P<count>\d+) \|$",
            inventory_text,
            re.MULTILINE,
        )
        if not match:
            fail(f"REPOSITORIES.md summary is missing {label!r}")
        return int(match.group("count"))

    repositories = [match.group("repository") for match in INVENTORY_REPOSITORY_PATTERN.finditer(inventory_text)]
    return (
        observed,
        summary_count("Total owned repositories"),
        summary_count("Public repositories"),
        summary_count("Private repositories"),
        summary_count("Archived repositories"),
        repositories,
    )


def verify_inventory_sync(data: dict[str, object], repositories: list[str]) -> None:
    if not INVENTORY.is_file():
        fail("REPOSITORIES.md is missing")
    try:
        inventory_text = INVENTORY.read_text(encoding="utf-8")
    except OSError as exc:
        fail(f"cannot read REPOSITORIES.md: {exc}")

    observed, total, public, private, archived, inventory_repositories = parse_inventory(inventory_text)
    registry_observed = require_iso_date(data.get("observedAt"), "observedAt")
    if observed != registry_observed:
        fail("REPOSITORIES.md and repositories.public.json Observed dates differ")
    if inventory_repositories != repositories:
        fail("REPOSITORIES.md public repository list differs from repositories.public.json")
    if public != len(repositories):
        fail("REPOSITORIES.md public count does not match the public repository list")
    if total != public + private:
        fail("REPOSITORIES.md total count must equal public plus private counts")
    if archived != 0:
        fail("REPOSITORIES.md currently requires zero archived repositories")


def fetch_live_public_repositories() -> dict[str, dict[str, object]]:
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "goreecloud-public-repository-registry-validator",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    repositories: dict[str, dict[str, object]] = {}
    page = 1
    while True:
        request = Request(GITHUB_PUBLIC_REPOSITORIES_URL.format(page=page), headers=headers)
        try:
            with urlopen(request, timeout=20) as response:
                payload = json.load(response)
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
            fail(f"cannot verify live public repository metadata: {exc}")
        if not isinstance(payload, list):
            fail("live public repository API response must be a list")
        for item in payload:
            if not isinstance(item, dict):
                fail("live public repository API returned a malformed repository record")
            full_name = item.get("full_name")
            if not isinstance(full_name, str) or not REPOSITORY_PATTERN.fullmatch(full_name):
                fail("live public repository API returned an unexpected repository identity")
            if item.get("private") is not False:
                fail(f"live public endpoint returned a non-public repository: {full_name}")
            repositories[full_name] = item
        if len(payload) < 100:
            break
        page += 1
        if page > 100:
            fail("live public repository pagination exceeded safety bound")
    return repositories


def verify_live_public_metadata(data: dict[str, object], repositories: list[str]) -> None:
    live = fetch_live_public_repositories()
    registered = set(repositories)
    live_names = set(live)
    missing = sorted(live_names - registered, key=str.casefold)
    stale = sorted(registered - live_names, key=str.casefold)
    if missing:
        fail("live public repositories missing from registry: " + ", ".join(missing))
    if stale:
        fail("registry contains repositories absent from live public metadata: " + ", ".join(stale))

    defaults = data["defaults"]
    overrides = data["defaultBranchOverrides"]
    assert isinstance(defaults, dict)
    assert isinstance(overrides, dict)
    for repository in repositories:
        item = live[repository]
        if item.get("archived") is not False:
            fail(f"public repository is archived but registry assumes active: {repository}")
        expected_branch = overrides.get(repository, defaults["defaultBranch"])
        if item.get("default_branch") != expected_branch:
            fail(
                f"default branch drift for {repository}: "
                f"registry={expected_branch!r}, live={item.get('default_branch')!r}"
            )


def main() -> None:
    if not REGISTRY.is_file():
        fail("repositories.public.json is missing")

    try:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot parse registry: {exc}")

    if not isinstance(data, dict):
        fail("registry root must be an object")
    if data.get("schema") != EXPECTED_SCHEMA:
        fail(f"schema must be {EXPECTED_SCHEMA!r}")
    require_iso_date(data.get("observedAt"), "observedAt")

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

    verify_inventory_sync(data, repositories)
    if "--verify-live-public" in sys.argv[1:]:
        verify_live_public_metadata(data, repositories)

    print(
        "public-repository-registry: validated "
        f"{len(repositories)} public repositories with {len(overrides)} branch overrides"
    )


if __name__ == "__main__":
    main()
