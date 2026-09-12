#!/usr/bin/env python3
"""Fail closed when the repository-local GoreeCloud eight-system platform baseline drifts."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CONFORMANCE = ROOT / "NATIVE-APPLICATION-AND-PLATFORM-CONFORMANCE.md"
README = ROOT / "README.md"
REUSABLE_WORKFLOW = ROOT / ".github" / "workflows" / "reusable-platform-manifest.yml"
CENTRAL_WORKFLOW = ROOT / ".github" / "workflows" / "platform-conformance.yml"

REQUIRED_SYSTEMS = (
    "GoreeCloud Manager",
    "Privacy Shield",
    "Wardveil Security",
    "Everkeep",
    "Glaze UI",
    "GoreeCloud Mesh",
    "GoreeCloud Identity",
    "GoreeCloud Sync",
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
    "eight Integral Platform Systems",
)

REQUIRED_README_BOUNDARIES = (
    "applications and services cohesive",
    "original, native, GoreeCloud-owned destination",
    "Existing complete-product forks or adopted implementations may remain temporarily",
    "Required GoreeCloud Manager, Privacy Shield, Wardveil Security, Everkeep, Glaze UI, GoreeCloud Mesh, GoreeCloud Identity, and GoreeCloud Sync integrations",
    "must not be presented as Stable or production-ready merely because it builds successfully",
)

FORBIDDEN_STALE_PHRASES = (
    "all four integral platform systems",
    "all four shared platform systems",
    "seven integral platform systems",
    "seven functional platform systems",
    "seven-system native/platform baseline",
)

FORBIDDEN_README_REFERENCES = ("https://github.com/GoreeCloud/glaze-ui",)
CHECKOUT_PIN = "actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803"
PR_REVISION_EXPRESSION = "${{ github.event_name == 'pull_request' && github.event.pull_request.head.sha || github.sha }}"


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


def require_snippets(label: str, text: str, snippets: tuple[str, ...]) -> None:
    missing = [snippet for snippet in snippets if snippet not in text]
    if missing:
        fail(f"{label} missing required provenance controls: " + "; ".join(missing))


def check_workflow_provenance() -> None:
    reusable = require_file(REUSABLE_WORKFLOW)
    central = require_file(CENTRAL_WORKFLOW)
    require_snippets(
        "reusable Platform Contract workflow",
        reusable,
        (
            f"EVALUATED_REVISION: {PR_REVISION_EXPRESSION}",
            "ref: ${{ env.EVALUATED_REVISION }}",
            'test "$(git rev-parse HEAD)" = "$EVALUATED_REVISION"',
            '--revision "$EVALUATED_REVISION"',
            "name: goreecloud-platform-conformance-${{ env.EVALUATED_REVISION }}",
        ),
    )
    require_snippets(
        "central Platform Contract workflow",
        central,
        (
            f"CANDIDATE_REVISION: {PR_REVISION_EXPRESSION}",
            "ref: ${{ env.CANDIDATE_REVISION }}",
            'test "$(git rev-parse HEAD)" = "$CANDIDATE_REVISION"',
            '--revision "$CANDIDATE_REVISION"',
            '--evaluator-revision "$CANDIDATE_REVISION"',
            "uses: ./.github/workflows/reusable-platform-manifest.yml",
            "manifest-path: examples/goreecloud.platform.example.yaml",
        ),
    )
    if reusable.count(CHECKOUT_PIN) != 2:
        fail("reusable Platform Contract workflow must use the governed checkout pin exactly twice")
    if central.count(CHECKOUT_PIN) != 1:
        fail("central Platform Contract workflow must use the governed checkout pin exactly once")


def main() -> None:
    conformance = require_file(CONFORMANCE)
    readme = require_file(README)
    check_required_systems("conformance record", conformance)
    check_required_systems("README", readme)

    missing_boundaries = [x for x in REQUIRED_CONFORMANCE_BOUNDARIES if x not in conformance]
    if missing_boundaries:
        fail("missing required conformance boundaries: " + "; ".join(missing_boundaries))
    missing_readme = [x for x in REQUIRED_README_BOUNDARIES if x not in readme]
    if missing_readme:
        fail("README is missing current platform boundaries: " + "; ".join(missing_readme))

    combined_lower = (conformance + "\n" + readme).lower()
    stale = [x for x in FORBIDDEN_STALE_PHRASES if x in combined_lower]
    if stale:
        fail("stale platform-system wording remains: " + "; ".join(stale))
    stale_refs = [x for x in FORBIDDEN_README_REFERENCES if x in readme]
    if stale_refs:
        fail("README contains stale repository references: " + "; ".join(stale_refs))

    bullet_count = sum(1 for line in conformance.splitlines() if line.startswith("- **") and " — " in line)
    if bullet_count != len(REQUIRED_SYSTEMS):
        fail(f"integral platform system list has {bullet_count} entries; expected {len(REQUIRED_SYSTEMS)}")

    check_workflow_provenance()
    print("platform-conformance: eight-system native/platform baseline validated")
    print("platform-conformance: exact PR-head workflow provenance validated")


if __name__ == "__main__":
    main()
