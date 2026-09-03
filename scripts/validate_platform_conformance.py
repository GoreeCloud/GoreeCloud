#!/usr/bin/env python3
"""Fail closed when the repository-local GoreeCloud platform baseline drifts."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CONFORMANCE = ROOT / "NATIVE-APPLICATION-AND-PLATFORM-CONFORMANCE.md"
README = ROOT / "README.md"

REQUIRED_SYSTEMS = (
    "GoreeCloud Manager",
    "Privacy Shield",
    "Wardveil Security",
    "Everkeep",
    "Glaze UI",
    "GoreeCloud Mesh",
    "GoreeCloud Identity",
)

REQUIRED_CONFORMANCE_BOUNDARIES = (
    "applications and services",
    "original GoreeCloud-owned software built natively from the ground up",
    "functional platform requirements",
    "genuinely not applicable",
    "Stable or production-ready",
    "Source acceptance",
    "production acceptance",
    "goreecloud.platform.yaml",
)

REQUIRED_README_BOUNDARIES = (
    "applications and services cohesive",
    "original, native, GoreeCloud-owned destination",
    "Existing complete-product forks or adopted implementations may remain temporarily",
    "Required GoreeCloud Manager, Privacy Shield, Wardveil Security, Everkeep, Glaze UI, GoreeCloud Mesh, and GoreeCloud Identity integrations",
    "must not be presented as Stable or production-ready merely because it builds successfully",
)

FORBIDDEN_STALE_PHRASES = (
    "all four integral platform systems",
    "all four shared platform systems",
)

FORBIDDEN_README_REFERENCES = (
    "https://github.com/GoreeCloud/glaze-ui",
)


def fail(message: str) -> None:
    print(f"platform-conformance: {message}", file=sys.stderr)
    raise SystemExit(1)


def require_file(path: Path) -> str:
    if not path.is_file():
        fail(f"missing {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def check_required_systems(label: str, text: str) -> None:
    missing = [name for name in REQUIRED_SYSTEMS if name not in text]
    if missing:
        fail(f"{label} missing integral systems: " + ", ".join(missing))


def main() -> None:
    conformance = require_file(CONFORMANCE)
    readme = require_file(README)

    check_required_systems("conformance record", conformance)
    check_required_systems("README", readme)

    missing_boundaries = [
        phrase for phrase in REQUIRED_CONFORMANCE_BOUNDARIES if phrase not in conformance
    ]
    if missing_boundaries:
        fail("missing required conformance boundaries: " + "; ".join(missing_boundaries))

    missing_readme = [phrase for phrase in REQUIRED_README_BOUNDARIES if phrase not in readme]
    if missing_readme:
        fail("README is missing current platform boundaries: " + "; ".join(missing_readme))

    combined_lower = (conformance + "\n" + readme).lower()
    stale = [phrase for phrase in FORBIDDEN_STALE_PHRASES if phrase in combined_lower]
    if stale:
        fail("stale four-system wording remains: " + "; ".join(stale))

    stale_refs = [reference for reference in FORBIDDEN_README_REFERENCES if reference in readme]
    if stale_refs:
        fail("README contains stale repository references: " + "; ".join(stale_refs))

    bullet_count = sum(
        1 for line in conformance.splitlines() if line.startswith("- **") and " — " in line
    )
    if bullet_count != len(REQUIRED_SYSTEMS):
        fail(
            f"integral platform system list has {bullet_count} entries; "
            f"expected {len(REQUIRED_SYSTEMS)}"
        )

    print("platform-conformance: seven-system native/platform baseline validated")


if __name__ == "__main__":
    main()
