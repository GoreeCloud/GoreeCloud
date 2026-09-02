#!/usr/bin/env python3
"""Fail closed when the repository-local GoreeCloud platform baseline drifts."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CONFORMANCE = ROOT / "NATIVE-APPLICATION-AND-PLATFORM-CONFORMANCE.md"

REQUIRED_SYSTEMS = (
    "Glaze UI",
    "Wardveil Security",
    "Privacy Shield",
    "Everkeep",
    "GoreeCloud Mesh",
    "GoreeCloud Identity",
)

REQUIRED_BOUNDARIES = (
    "applications and services",
    "original GoreeCloud-owned software built natively from the ground up",
    "functional platform requirements",
    "genuinely not applicable",
    "Stable or production-ready",
    "Source acceptance",
    "production acceptance",
)

FORBIDDEN_STALE_PHRASES = (
    "all four integral platform systems",
    "all four shared platform systems",
)


def fail(message: str) -> None:
    print(f"platform-conformance: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    if not CONFORMANCE.is_file():
        fail(f"missing {CONFORMANCE.relative_to(ROOT)}")

    text = CONFORMANCE.read_text(encoding="utf-8")
    lowered = text.lower()

    missing_systems = [name for name in REQUIRED_SYSTEMS if name not in text]
    if missing_systems:
        fail("missing integral systems: " + ", ".join(missing_systems))

    missing_boundaries = [phrase for phrase in REQUIRED_BOUNDARIES if phrase not in text]
    if missing_boundaries:
        fail("missing required conformance boundaries: " + "; ".join(missing_boundaries))

    stale = [phrase for phrase in FORBIDDEN_STALE_PHRASES if phrase in lowered]
    if stale:
        fail("stale four-system wording remains: " + "; ".join(stale))

    bullet_count = sum(1 for line in text.splitlines() if line.startswith("- **") and " — " in line)
    if bullet_count < len(REQUIRED_SYSTEMS):
        fail("integral platform system list is incomplete")

    print("platform-conformance: six-system native/platform baseline validated")


if __name__ == "__main__":
    main()
