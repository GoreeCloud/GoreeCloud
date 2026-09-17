# GoreeCloud Platform Contract

## Status

- Contract version: `0.2`
- Repository role: platform-wide implementation and conformance reference
- Manifest filename: `goreecloud.platform.yaml`
- Computed result filename: `goreecloud.conformance-result.json`
- Applies to: GoreeCloud application and service repositories
- Canonical governance: GoreeCloud Google Drive instructions, policies, standards, rules, preferences, and project specifications
- Current Stable Glaze UI consumer target: `1.5.1` (`GLAZE UI V1.5 — Contextual + Capability Awareness`)

Contract `0.2` is the current governance-aligned schema. The September 12, 2026 repository commit that introduced eight-system Contract `0.3` conflicts with the newer authoritative Drive instruction that defines exactly seven Integral Platform Systems and explicitly keeps GoreeCloud Sync as a separate application/service capability. The September 15 corrective revision restores Contract `0.2` semantics as a new controlled event; it does not erase the intervening history.

This repository contains the machine-readable implementation foundation for the GoreeCloud Platform Contract. The contract records a repository's declared platform identity, lifecycle, compatibility, operational interfaces, continuity requirements, evidence references, and integration state. A manifest is a declaration and validation input; it does not by itself prove that a capability is implemented or accepted.

The CI evaluator produces a separate computed conformance result from the repository declaration and evidence metadata. GoreeCloud Mesh may aggregate declarations, relationships, capabilities, dependencies, and evidence references. GoreeCloud Manager may present bounded operational state. Neither aggregation nor presentation transfers authority away from the repository or platform authority that owns the underlying fact.

## Exactly seven Integral Platform Systems

The authoritative platform baseline contains exactly seven Integral Platform Systems:

1. **GoreeCloud Manager** — bounded administration, configuration, lifecycle, inventory, operational visibility, and authorized control-plane workflows.
2. **Privacy Shield** — privacy authorization, consent, purpose limitation, minimization, retention, sharing, and data-use controls.
3. **Wardveil Security** — protection, trust, verification, threat handling, response, and evidence-backed security controls.
4. **Everkeep** — resilience, backup, restore, recovery, preservation, portability, continuity, succession, and digital legacy.
5. **Glaze UI** — shared visual, interaction, accessibility, responsive, and design-system behavior.
6. **GoreeCloud Mesh** — bounded first-party capability discovery, private coordination, dependency/event relationships, governance, and interoperability where applicable.
7. **GoreeCloud Identity** — identity, authentication, authorization, accounts, sessions, devices, applications, services, credentials, and delegated authority.

Every application and service must be evaluated explicitly against all seven. Genuine non-applicability must be justified with evidence. Cosmetic presence, metadata, documentation, a Manager card, Mesh registration, or source-only placeholders do not establish implementation or acceptance.

**GoreeCloud Sync is not an eighth Integral Platform System.** It remains a separately governed application/service capability. A consumer that uses Sync must document and validate the relevant synchronization dataset, authorization boundary, change/version model, conflict reconciliation, replication, offline-resume, and cross-device behavior independently. Sync is not a key under Contract `0.2` `platform_systems`.

## Required manifest areas

Every application or service manifest must declare:

- Contract schema version.
- Component type, stable application/service identifier, product name, and authoritative repository.
- Lifecycle state and current version.
- Supported platforms.
- API versions and declared endpoints.
- An integration result for each of the seven Integral Platform Systems.
- GoreeCloud Mesh capabilities, dependencies, and published/consumed events where applicable.
- Health and readiness interfaces.
- Backup, restore, export, and portability requirements.
- Required external dependencies.
- Platform compatibility requirements, including the current Glaze UI target where applicable.
- Structured acceptance-test evidence references.
- Structured release evidence references.
- Declared conformance status, blockers, validation time, and evidence references.

Unknown fields are rejected. Applications and services must not invent incompatible local Platform Contract extensions. Breaking contract changes belong in a new version of the central contract with an explicit migration path.

## Platform-System result vocabulary

Contract `0.2` uses the following machine values:

- `Applicable — Conformant` → `applicable-conformant`
- `Applicable — Migration Required` → `applicable-migration-required`
- `Applicable — Blocked` → `applicable-blocked`
- `Applicable — Nonconformant` → `applicable-nonconformant`
- `Not Applicable — Justified` → `not-applicable-justified`

`not-applicable-justified` requires an explicit justification and an evidence reference supporting the applicability decision. `applicable-conformant` requires evidence references. The result records repository truth without upgrading incomplete work merely to satisfy CI.

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

`evidence.acceptance_tests` records attributable evidence references with an ID, category, repository path, exact revision, result, and observation time. Supported Platform-System categories cover the seven systems plus API, accessibility, supported-platform, backup, restore, export/portability, security, privacy, documentation, integration, migration, rollback, and release acceptance.

`evidence.release` records release evidence with an ID, version, revision, path, result, observation time, and optional artifact digest. Prose declarations never substitute for the underlying test, workflow artifact, release record, restore record, or acceptance record.

## Stable fail-closed gates

A `stable` lifecycle declaration fails validation unless all applicable Platform-System results pass, the current required Glaze UI target is `1.5.1` where applicable, conformance is declared `conformant` with a validation timestamp, required acceptance categories have passing evidence, and published release evidence exists.

A passing manifest or computed conformance result proves only the checks encoded by the validator. Runtime acceptance, representative-device/browser validation, accessibility, recovery, release approval, deployment, production acceptance, and Stable qualification remain independent gates.

## Exact-revision authority

Pull-request validation must evaluate the exact PR head rather than GitHub's synthetic merge ref. The reusable workflow records the evaluated repository revision and the exact evaluator revision in the computed result and retained evidence artifact. Any candidate-head change resets exact-head validation.

## Migration and restoration boundary

Repositories that adopted the conflicting eight-system Contract `0.3` must not silently delete or reinterpret Sync evidence. They should migrate back to Contract `0.2` by:

1. removing `platform_systems.sync` from the central seven-system set;
2. retaining Sync-specific implementation truth in appropriate repository documentation, integration metadata, roadmap/task records, or application/service contracts;
3. setting `schema_version` and `compatibility.platform_contract` to `0.2`;
4. setting the current applicable `compatibility.glaze_ui_required` target to `1.5.1`;
5. rerunning exact-head manifest, conformance, source/build, and other affected validation;
6. preserving the historical `0.3` branch/commit/PR evidence rather than rewriting it as though it never existed.

Canonical Drive governance controls the platform-system count and authority boundaries when repository-local implementation becomes stale or conflicts with it.
