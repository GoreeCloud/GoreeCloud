# GoreeCloud Platform Contract

## Status

- Contract version: `0.3`
- Repository role: platform-wide implementation and conformance reference
- Manifest filename: `goreecloud.platform.yaml`
- Computed result filename: `goreecloud.conformance-result.json`
- Applies to: GoreeCloud applications, services, and Integral Platform Systems
- Canonical governance: GoreeCloud Google Drive instructions, decisions, standards, policies, and project specifications
- Current Stable Glaze UI consumer target: `1.3.0` (`GLAZE UI V1.3`)

This repository contains the machine-readable implementation foundation for the GoreeCloud Platform Contract. The contract records a repository's declared identity, lifecycle, compatibility, operational interfaces, continuity requirements, evidence references, and integration state. A manifest is a declaration and validation input; it does not by itself prove that a capability is implemented or accepted.

The CI evaluator produces a separate computed conformance result from the repository declaration and evidence metadata. GoreeCloud Mesh may coordinate transport and platform relationships, GoreeCloud Sync may coordinate authorized synchronized state, and GoreeCloud Manager may present bounded operational state. None of those roles transfers authority away from the repository or Platform System that owns the underlying fact.

## Exactly eight Integral Platform Systems

The authoritative platform baseline contains exactly eight Integral Platform Systems:

1. **GoreeCloud Manager** — administration, configuration, lifecycle, inventory, and operational control.
2. **Privacy Shield** — privacy authorization, consent, minimization, purpose limitation, retention, sharing, and data-use control.
3. **Wardveil Security** — security, trust, protection, verification, threat handling, response, and security evidence.
4. **Everkeep** — resilience, backup, restore, recovery, preservation, portability, continuity, succession, and digital legacy.
5. **Glaze UI** — shared visual, interaction, accessibility, responsive, and design-system behavior.
6. **GoreeCloud Mesh** — private connectivity, discovery, coordination, capability relationships, dependency relationships, events, and service interoperability.
7. **GoreeCloud Identity** — identity, authentication, authorization, accounts, sessions, devices, applications, services, and delegated authority.
8. **GoreeCloud Sync** — synchronization, change tracking, state coordination, version reconciliation, conflict handling, authorized replication, offline continuity, and cross-device continuity.

Every application, service, and Platform System must be evaluated explicitly against all eight. Genuine non-applicability must be justified with evidence. Cosmetic presence, metadata, documentation, a Manager card, Mesh registration, a Sync badge, or source-only placeholders do not establish implementation or acceptance.

Full implementation of the eight Platform Systems is a GoreeCloud completion objective and release obligation. This requirement does not authorize false maturity claims: Development, partial, migration-required, blocked, or production-unaccepted state must remain labeled accurately until implementation and acceptance evidence proves otherwise.

## Authority boundaries

The contract keeps the eight systems complementary rather than interchangeable:

- **Identity** determines who or what is acting and the authority it possesses.
- **Privacy Shield** determines whether the intended data use is permitted.
- **Wardveil Security** determines applicable trust, protection, and security response.
- **Manager** provides bounded administration and operational control.
- **Mesh** establishes private reachability, discovery, coordination, and event/service interoperability.
- **Sync** determines what authorized state should synchronize, how versions and conflicts are reconciled, and how offline synchronization resumes.
- **Everkeep** preserves recoverable historical state and continuity; synchronization is not backup.
- **Glaze UI** presents accurate, accessible state and interaction behavior without manufacturing capabilities.

A system must not silently absorb or bypass another system's authority.

## Required manifest areas

Every manifest must declare:

- Contract schema version.
- Component type (`application`, `service`, or `platform-system`), stable identifier, product name, and authoritative repository.
- Lifecycle state and current version.
- Supported platforms.
- API versions and declared endpoints.
- An integration result for each of all eight Integral Platform Systems.
- GoreeCloud Mesh capabilities, dependencies, and published/consumed events where applicable.
- Health and readiness interfaces.
- Backup, restore, export, and portability requirements.
- Required external dependencies.
- Platform compatibility requirements, including the current Glaze UI target where applicable.
- Structured acceptance-test evidence references.
- Structured release evidence references.
- Declared conformance status, blockers, validation time, and evidence references.

Unknown fields are rejected. Components must not invent incompatible local Platform Contract extensions. Breaking contract changes require an explicit version and migration path.

## Platform-System result vocabulary

Contract v0.3 retains the governed result vocabulary introduced by v0.2:

- `Applicable — Conformant` → `applicable-conformant`
- `Applicable — Migration Required` → `applicable-migration-required`
- `Applicable — Blocked` → `applicable-blocked`
- `Applicable — Nonconformant` → `applicable-nonconformant`
- `Not Applicable — Justified` → `not-applicable-justified`

`not-applicable-justified` requires an explicit justification and evidence reference. `applicable-conformant` requires evidence references. The result records repository truth without upgrading incomplete work merely to satisfy CI.

## Lifecycle values

- `concept`
- `experimental`
- `development`
- `release-candidate`
- `stable`
- `deprecated`
- `retired`

Lifecycle claims are evidence-backed states. Repository existence, successful compilation, structural manifest validity, or documentation completion does not establish Stable maturity.

## Evidence model

`evidence.acceptance_tests` records attributable evidence references with an ID, category, repository path, exact revision, result, and observation time. Supported Platform-System categories cover all eight systems: `manager`, `privacy-shield`, `wardveil-security`, `everkeep`, `glaze-ui`, `mesh`, `identity`, and `sync`, plus API, accessibility, supported-platform, backup, restore, export/portability, security, privacy, documentation, integration, migration, rollback, and release acceptance.

`evidence.release` records release evidence with an ID, version, revision, path, result, observation time, and optional artifact digest. Prose declarations never substitute for underlying test, workflow, release, restore, or acceptance evidence.

## Conformance and Stable fail-closed behavior

Manifest-level conformance uses `conformant`, `nonconformant`, or `unverified`.

The reusable CI workflow validates the manifest and computes `goreecloud.conformance-result.json`. The result records the exact evaluated revision, individual checks for all eight Platform Systems, compatibility checks, missing Stable evidence categories, blockers, and `stable_eligible`.

A Development or Release Candidate repository may truthfully compute as nonconformant without ordinary development CI pretending the repository is Stable. A repository declaring lifecycle `stable` fails closed unless:

- all eight Platform Systems are `applicable-conformant` or supportably `not-applicable-justified`;
- declared conformance is `conformant` and time-bounded by a validation timestamp;
- required API, accessibility, supported-platform, security, privacy, backup, restore, export/portability, documentation, integration, and release acceptance evidence has a passing result; and
- published release evidence exists.

Additional application-, service-, or Platform-System-specific evidence can remain mandatory even when the generic contract gate passes. A generic passing result never overrides a more specific security, privacy, identity, sync, recovery, platform, release, or production-acceptance requirement.

## Glaze UI baseline

The canonical `GoreeCloud/goreecloud-glaze-ui` repository identifies `GLAZE UI V1.3 / 1.3.0` as the current Stable consumer target. Contract v0.3 requires applicable consumers to declare `compatibility.glaze_ui_required: "1.3.0"`. A current baseline declaration does not establish downstream conformance by itself.

## Mesh, Sync, and Everkeep separation

GoreeCloud Mesh, GoreeCloud Sync, and Everkeep must remain distinct:

- Mesh establishes private reachability, discovery, coordination, and transport/event relationships.
- Sync understands authorized application state, tracks changes, coordinates versions, handles conflicts, and resumes replication after interruption.
- Everkeep preserves recoverable historical state and continuity after loss, corruption, deletion, failure, or migration.

A synchronized replica, synchronized deletion, or successful transfer must never be represented as Everkeep recovery evidence unless an actual Everkeep mechanism preserves a recoverable state.

## Repository adoption

Applications, services, and Integral Platform Systems place `goreecloud.platform.yaml` at repository root as contract rollout reaches them. Rollout must preserve truthfulness: blocked, migration-required, nonconformant, or genuinely non-applicable integrations must be declared as such rather than upgraded merely to satisfy automation.

Repositories should call `.github/workflows/reusable-platform-manifest.yml` from this repository by immutable commit SHA. Updating that SHA is an explicit validator upgrade. The reusable workflow publishes a computed conformance artifact tied to the exact caller revision.

## Files in this repository

- `schemas/goreecloud.platform.schema.json` — strict JSON Schema for repository declarations.
- `schemas/goreecloud.conformance-result.schema.json` — strict schema for computed conformance results.
- `examples/goreecloud.platform.example.yaml` — truthful non-production example manifest.
- `scripts/validate_platform_manifest.py` — semantic manifest validator and Stable declaration gate.
- `scripts/evaluate_platform_conformance.py` — exact-revision conformance evaluator.
- `scripts/validate_platform_conformance.py` — repository-local eight-system baseline guard.
- `.github/workflows/platform-conformance.yml` — central validation workflow.
- `.github/workflows/reusable-platform-manifest.yml` — reusable repository validation workflow.

## Migration from contract v0.2

Contract v0.3 adopts the authoritative eight-system architecture and is a breaking schema migration from v0.2. Repositories migrating from v0.2 must:

1. Change `schema_version` and `compatibility.platform_contract` to `0.3`.
2. Add the required `platform_systems.sync` declaration.
3. Evaluate Sync applicability honestly and preserve blockers where implementation or acceptance is incomplete.
4. Use `component.type: platform-system` for repositories whose primary role is one of the eight Integral Platform Systems.
5. Update `compatibility.requires` to the v0.3 contract target.
6. Preserve all existing evidence and lifecycle truth; migration must not upgrade incomplete integrations to conformant.

Contract v0.2 remains historical migration context only once v0.3 is accepted on the default branch.