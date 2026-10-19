# Platform Contract 2.1 — GoreeCloud UI successor contract

**Status:** Versioned schema and tooling merged on October 19, 2026; ecosystem adoption remains candidate/pending. **Implementation:** additive schema, validator, evaluator, examples, exact-head CI; not yet a deployed estate-wide contract. **Owner mandate:** GoreeCloud UI (GC UI) is the fifth of the existing **nine** Integral Platform Systems. Glaze and Glaze UI are permanently retired as active design authorities.

## Motivation and exact authority

The current 2.0 Platform Contract schema and validator still require `platform_systems.glaze_ui`, `compatibility.glaze_ui_required`, and a Glaze 1.7.0 Anchor compatibility target. Existing 0.4 consumer manifests can also retain those old machine keys. They are *historical and migration input*, not authority to design or develop with Glaze after October 19.

This **separately versioned** 2.1 candidate provides an explicit replacement rather than silently repurposing the meaning of 2.0 evidence or breaking SHA-pinned historical validation.

| Concern | Historical Contract 2.0 | Proposed Contract 2.1 |
| --- | --- | --- |
| Experience system, slot 5/9 | `glaze_ui` | `gc_ui` — GoreeCloud UI |
| Required experience version | `compatibility.glaze_ui_required` | `compatibility.gc_ui_required` |
| Experience evidence category | `glaze-ui` | `gc-ui` |
| Current scoped release | Glaze 1.7.0 historical baseline | `foundations-v1.0.1` — **Foundations subset only** |
| Active predecessor dependency | Accepted in old evidence contract | Forbidden in new `compatibility.requires` |
| Lifecycle model | Seed, Lab, Forge, Weave, Seal, Anchor, Sunset, Archive | Unchanged |
| Number of Integral Platform Systems | Nine | **Nine**, not ten |
| Sync classification | Separate service capability | Unchanged |
| Conformance evidence | Exact release and runtime acceptance necessary | Unchanged; a name swap does not prove migration |

## What is added

- [2.1 manifest schema](../schemas/goreecloud.platform.v2.1.schema.json) requires all nine platform slots and forbids `glaze_ui` as a new key.
- [2.1 validator](../scripts/validate_platform_manifest_v2_1.py) checks structural and lifecycle validity, refuses active Glaze dependencies, checks declared `gc_ui` release consistency, and preserves fail-closed Anchor controls.
- [2.1 evaluator](../scripts/evaluate_platform_conformance_v2_1.py) and [2.1 result schema](../schemas/goreecloud.conformance-result.v2.1.schema.json) retain producer provenance, source revision and independently evidenced eligibility.
- [Application example](../examples/goreecloud.platform.v2.1.example.yaml), [shared-library example](../examples/goreecloud.platform.v2.1.shared-library.example.yaml), and [CI workflow](../.github/workflows/gc-ui-platform-contract-2-1.yml) verify truthful **nonconformant** source declarations and negative tests.
- The existing Contract 2.0 schema, validator, evaluator, examples and reusable workflow are **not modified**; existing callers remain pinned to their evaluator revisions.

## Consumer-callable, exact-revision CI

The [versioned reusable validation workflow](../.github/workflows/reusable-platform-manifest-v2-1.yml) uses the same versioned 2.1 validator, evaluator and conformance-result schema. It checks out the **caller's exact pull-request head**, then checks out the **workflow's own pinned implementation revision**; it validates the caller path and evidence-provenance identities before reporting results.

A migrated consumer may reference the new workflow **only after explicitly qualifying its 2.1 manifest and the selected evaluator revision**:

```yaml
jobs:
  platform-contract-gc-ui:
    uses: GoreeCloud/GoreeCloud/.github/workflows/reusable-platform-manifest-v2-1.yml@<verified-GoreeCloud-contract-commit>
    with:
      manifest-path: goreecloud.platform.yaml
```

Replace the placeholder with a **verified immutable 40-character commit SHA**; never pin an unverified ref or assume that changing the workflow automatically updates the consumer to GC UI. The old `reusable-platform-manifest.yml` continues to validate historical Contract 2.0 manifests at their own pinned revisions. Passing reusable validation means source declarations and schema provenance passed, **not** that GC UI is installed, the UI has migrated, or the product is production accepted.

## GC UI release and scope truth

The GC UI development workspace is `0.2.0-alpha.1`; its scoped `foundations-v1.0.1` GitHub distribution covers semantic tokens, color engine and browser theme controller, **not** the full component catalog or native UI. Declaring that identifier as a target is not conformance and cannot silently certify experimental components, app-level UX, accessibility, privacy, native interaction, platform adapter, rollout, rollback, or production readiness.

A headless service can declare `platform_systems.gc_ui.result: not-applicable-justified` only with a genuine explanation and referenced evidence. It must re-evaluate GC UI if it later exposes an owned dashboard, app, admin UI or graphical workflow.

## Migration sequence — not automatic

1. Record the exact current repository and user-visible UI source at a pinned revision. Perform a read-only legacy import, asset, dependency, and build-output audit; retain unknown/incomplete findings.
2. Determine applicable GC UI component scope and supported target. Design genuine independent GC UI replacements and explicitly verify licensing; **never** mass-rename Glaze source or import predecessor assets under a GC UI prefix.
3. Validate a separately proposed 2.1 manifest with `python3 scripts/validate_platform_manifest_v2_1.py <manifest>`. Preserve old 2.0 acceptance records as historical, including their original versioned evaluator.
4. Run scoped runtime/browser/native, accessibility, keyboard, visual, privacy, security, performance, and failure-state tests. Verify exact artifact, dependency graph, rollback, and signed owner acceptance where required.
5. Update the owning repo's CI to invoke the new 2.1 evaluator *only after* it and the migration are qualified; pin the chosen release/evaluator SHA and record its contract version. No existing 0.4/2.0 caller is automatically upgraded.
6. Update the canonical GoreeCloud Markdown Instructions/Policies/Standards in place with original file identity and approved format. Product and ecosystem cutover/retirement flags remain false until independently verified.

## Verification and status boundaries

The 2.1 candidate's exact-head workflow checks schema-valid new examples, output provenance, historic 2.0 examples, legacy field rejection, predecessor dependency rejection and Anchor fail-closed behavior. Passing those source checks proves only the **candidate tooling**, not that any consumer migrated or that the higher-authority Drive governance has been amended.

Owner implementation source: [GC UI succession contract](https://github.com/GoreeCloud/gc-ui/blob/main/docs/DESIGN_SYSTEM_SUCCESSION.md). Consumer work is tracked in [GC UI issue #13](https://github.com/GoreeCloud/gc-ui/issues/13).
