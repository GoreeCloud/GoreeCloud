# GoreeCloud Platform Contract

## Status

- Contract version: `0.2`
- Repository role: platform-wide implementation reference
- Manifest filename: `goreecloud.platform.yaml`
- Computed result filename: `goreecloud.conformance-result.json`
- Applies to: GoreeCloud application and service repositories
- Canonical governance: GoreeCloud Google Drive instructions, standards, policies, and project specifications
- Current Stable Glaze UI consumer target: `1.1.0` (`GLAZE UI V1.1`)

This repository contains the machine-readable implementation foundation for the GoreeCloud Platform Contract. The contract records a repository's declared platform identity, lifecycle, compatibility, operational interfaces, continuity requirements, evidence references, and integration state. A manifest is a declaration and validation input; it does not by itself prove that a capability is implemented or accepted.

The CI evaluator produces a separate computed conformance result from the repository declaration and evidence metadata. GoreeCloud Mesh may aggregate the declaration, computed result, relationships, capabilities, dependencies, and evidence references. GoreeCloud Manager may present that state. Neither aggregation nor presentation transfers authority away from the repository or Platform System that owns the underlying fact.

## Required manifest areas

Every application or service manifest must declare:

- Contract schema version.
- Component type, stable application/service identifier, product name, and authoritative repository.
- Lifecycle state and current version.
- Supported platforms.
- API versions and declared endpoints.
- Glaze UI version, current required baseline, and integration result.
- GoreeCloud Manager integration result.
- GoreeCloud Identity integration result.
- Wardveil Security integration result.
- Privacy Shield integration result.
- Everkeep integration result and recovery requirements.
- GoreeCloud Mesh integration result, capabilities, dependencies, and published/consumed events.
- Health and readiness interfaces.
- Backup, restore, export, and portability requirements.
- Required external dependencies.
- Platform compatibility requirements.
- Structured acceptance-test evidence references.
- Structured release evidence references.
- Declared conformance status, blockers, validation time, and evidence references.

Unknown fields are rejected. Applications and services must not invent incompatible local Platform Contract extensions. Breaking changes belong in a new version of the central contract with an explicit migration path.

## Integral Platform Systems

The current platform baseline contains seven Integral Platform Systems:

1. GoreeCloud Manager
2. Privacy Shield
3. Wardveil Security
4. Everkeep
5. Glaze UI
6. GoreeCloud Mesh
7. GoreeCloud Identity

Each system must be evaluated explicitly. Cosmetic presence, metadata, documentation, a Manager card, or Mesh registration does not establish implementation or acceptance.

## Platform-System result vocabulary

Contract v0.2 standardizes the authoritative platform result vocabulary. Human-readable governance terms map to these machine values:

- `Applicable — Conformant` → `applicable-conformant`
- `Applicable — Migration Required` → `applicable-migration-required`
- `Applicable — Blocked` → `applicable-blocked`
- `Applicable — Nonconformant` → `applicable-nonconformant`
- `Not Applicable — Justified` → `not-applicable-justified`

`not-applicable-justified` requires both an explicit justification and an evidence reference supporting the applicability decision. `applicable-conformant` requires evidence references. The result records repository truth without upgrading incomplete work merely to satisfy CI.

## Lifecycle values

The Platform Contract uses the following lifecycle values:

- `concept`
- `experimental`
- `development`
- `release-candidate`
- `stable`
- `deprecated`
- `retired`

Lifecycle claims are evidence-backed states. Repository existence, successful compilation, a passing structural manifest check, or documentation completion does not establish Stable maturity.

## Evidence model

Contract v0.2 distinguishes declarations from acceptance evidence.

`evidence.acceptance_tests` records attributable evidence references with an ID, category, repository path, exact revision, result, and observation time. Supported categories cover the seven Platform Systems plus API, accessibility, supported-platform, backup, restore, export/portability, security, privacy, documentation, integration, migration, rollback, and release acceptance.

`evidence.release` records release evidence with an ID, version, revision, path, result, observation time, and optional artifact digest. The manifest never treats a prose declaration as a substitute for the underlying test, workflow artifact, release record, restore record, or acceptance record.

## Conformance and Stable fail-closed behavior

Manifest-level conformance uses:

- `conformant`
- `nonconformant`
- `unverified`

The reusable CI workflow validates the manifest and then computes `goreecloud.conformance-result.json`. That result records the exact evaluated revision, individual Platform-System checks, compatibility checks, missing Stable evidence categories, blockers, and a `stable_eligible` decision.

Revision provenance is event-specific and fail closed. For a `pull_request` invocation, the caller repository is checked out at `github.event.pull_request.head.sha`, and that same immutable SHA is recorded as `evaluated_revision`; GitHub's synthetic pull-request merge SHA is not accepted as the evaluated source revision. For push/main and other non-PR invocations, `github.sha` remains the evaluated revision. The reusable workflow separately records its pinned central implementation revision as `evaluator_revision`, so the caller source and the validator implementation remain independently attributable.

A Development or Release Candidate repository may truthfully compute as nonconformant without ordinary development CI pretending the repository is Stable. A repository declaring lifecycle `stable` fails closed unless:

- every Platform System is `applicable-conformant` or supportably `not-applicable-justified`;
- declared conformance is `conformant` and time-bounded by a validation timestamp;
- required API, accessibility, supported-platform, security, privacy, backup, restore, export/portability, documentation, integration, and release acceptance evidence has a passing result; and
- published release evidence exists.

Additional application-specific or governance-required evidence can remain mandatory even when the generic contract gate passes. A passing generic contract check never overrides a more specific security, privacy, recovery, platform, release, or production-acceptance requirement.

## Glaze UI baseline

The current specific Glaze UI authority and canonical `GoreeCloud/goreecloud-glaze-ui` repository identify `GLAZE UI V1.1 / 1.1.0` as the current Stable consumer target. Contract v0.2 therefore requires applicable applications to declare `compatibility.glaze_ui_required: "1.1.0"`.

Older version-number references in broader platform documents do not establish downstream consumer conformance. Each application still requires application-specific implementation and acceptance evidence for the current Stable Glaze UI contract.

## Authority preservation and Mesh aggregation

The declaration owner remains authoritative for repository-owned facts. Platform Systems remain authoritative for their own domains. GoreeCloud Mesh is a coordination and evidence-transport boundary, not an authorization or truth-upgrade mechanism. GoreeCloud Manager is initially a read-only operational presentation surface for this platform state.

The computed conformance result explicitly records that aggregation is read-only and does not transfer authority. Mesh or Manager must not transform missing, stale, blocked, nonconformant, or unverified producer evidence into a positive platform claim.

## Files in this repository

- `schemas/goreecloud.platform.schema.json` — strict JSON Schema for the repository declaration.
- `schemas/goreecloud.conformance-result.schema.json` — schema for computed CI conformance results.
- `examples/goreecloud.platform.example.yaml` — truthful non-production example manifest.
- `scripts/validate_platform_manifest.py` — semantic manifest validator and Stable declaration gate.
- `scripts/evaluate_platform_conformance.py` — conformance evaluator for an exact repository revision.
- `.github/workflows/platform-conformance.yml` — CI validating the central platform baseline.
- `.github/workflows/reusable-platform-manifest.yml` — reusable application/service validation and conformance-evidence workflow.

## Repository adoption

Application and service repositories place `goreecloud.platform.yaml` at the repository root. Rollout must preserve truthfulness: blocked, migration-required, nonconformant, or genuinely non-applicable integrations must be declared as such rather than being upgraded to a positive result merely to satisfy automation.

Repositories should call `.github/workflows/reusable-platform-manifest.yml` from this repository by immutable commit SHA. Updating that SHA is an explicit Platform Contract validator upgrade. The reusable workflow publishes the computed conformance result as a CI artifact tied to the exact caller revision resolved by the event-specific provenance rule above.

## Migration from contract v0.1

Contract v0.1 used ambiguous `implemented`, `partial`, `planned`, `not-applicable`, and `unknown` integration states and did not require structured acceptance/release evidence. Contract v0.2 replaces those values with the governed five-result vocabulary, removes manifest-level `partial`, adds exact evidence structures, adds current Glaze UI compatibility metadata, rejects unrecognized fields, and generates a computed conformance record.

Repositories migrating from v0.1 must map their current state conservatively. A previous `partial`, `planned`, or `unknown` value must not be upgraded to `applicable-conformant` without current accepted evidence.
