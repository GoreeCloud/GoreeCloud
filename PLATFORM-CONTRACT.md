# GoreeCloud Platform Contract

## Status

- Contract version: `0.4`
- Repository role: platform-wide implementation and conformance reference
- Manifest filename: `goreecloud.platform.yaml`
- Computed result filename: `goreecloud.conformance-result.json`
- Applies to: GoreeCloud application, service, and governance-recognized shared-library repositories
- Canonical governance: GoreeCloud Google Drive instructions, policies, standards, rules, preferences, and project specifications
- Integral Platform System authority: **Instructions — Integral Platform Systems v3.0**
- Current Stable Glaze UI consumer target: `1.5.1` (`GLAZE UI V1.5 — Contextual + Capability Awareness`)

Contract `0.4` is the governance-aligned machine-readable contract for the nine-system Integral Platform Systems v3.0 model. It adds **GoreeCloud Policy** and **GoreeCloud Observability** as required evaluation keys while keeping **GoreeCloud Sync** separately governed.

Contract version history matters. Contract `0.2` represented the earlier seven-system model. A historical Contract `0.3` experiment represented GoreeCloud Sync as an eighth Integral Platform System and was superseded because Sync is not an Integral Platform System. Contract `0.4` does not reuse or reinterpret `0.3`; it is a new controlled contract version implementing the current nine-system authority.

This repository contains the machine-readable implementation foundation for the GoreeCloud Platform Contract. The contract records a repository's declared platform identity, lifecycle, compatibility, operational interfaces, continuity requirements, evidence references, and integration state. A manifest is a declaration and validation input; it does not by itself prove that a capability is implemented or accepted.

The CI evaluator produces a separate computed conformance result from the repository declaration and evidence metadata. GoreeCloud Mesh may aggregate declarations, relationships, capabilities, dependencies, and evidence references. GoreeCloud Manager may present bounded administrative and operational state. GoreeCloud Policy may evaluate approved policy inputs. GoreeCloud Observability may normalize and correlate operational evidence. None of those activities transfers another producer's domain authority.

## Exactly nine Integral Platform Systems

The authoritative platform baseline contains exactly nine Integral Platform Systems:

1. **GoreeCloud Manager** — administration, configuration, lifecycle, inventory, operational control, approvals, remediation, and management-plane visibility.
2. **Privacy Shield** — privacy protection, consent, purpose limitation, minimization, retention, tracking/telemetry privacy, sharing, and information-use controls.
3. **Wardveil Security** — protection, integrity, trust, threat handling, defensive requirements, security posture, response, and security evidence.
4. **Everkeep** — resilience, backup, restore, recovery, preservation, portability, continuity, migration readiness, succession, and long-term information survival.
5. **Glaze UI** — shared visual, interaction, accessibility, adaptive, status, policy-decision, operational-health, and evidence-state presentation behavior.
6. **GoreeCloud Mesh** — bounded first-party capability discovery, dependency/relationship awareness, private coordination, event exchange, interoperability, and evidence routing where applicable.
7. **GoreeCloud Identity** — identity, authentication, authorization integration, accounts, sessions, devices, applications, services, credentials, claims, workload identity, and trust relationships.
8. **GoreeCloud Policy** — shared policy representation, evaluation, decisions, distribution, enforcement coordination, explanation, version/freshness, precedence/composition, and policy evidence while preserving domain rule ownership.
9. **GoreeCloud Observability** — operational health, metrics, logs, events, traces, diagnostics, performance, availability, dependency health, correlation, freshness, provenance, and operational evidence.

Every in-scope component must be evaluated explicitly against all nine. Genuine non-applicability must be justified with evidence. Cosmetic presence, metadata, documentation, a Manager card, Mesh registration, policy label, dashboard, or source-only placeholder does not establish implementation or acceptance.

**GoreeCloud Sync is not a tenth Integral Platform System.** It remains a separately governed application/service capability. A consumer that uses Sync must document and validate the relevant synchronization dataset, authorization boundary, change/version model, conflict reconciliation, replication, offline-resume, and cross-device behavior independently. Sync is not a key under Contract `0.4` `platform_systems`.

## Required manifest areas

Every in-scope component manifest must declare:

- Contract schema version.
- Component type, stable component identifier, product name, and authoritative repository.
- Lifecycle state and current version.
- Supported platforms.
- API versions and declared endpoints.
- An integration result for each of the nine Integral Platform Systems.
- GoreeCloud Mesh capabilities, dependencies, and published/consumed events where applicable.
- Health and readiness interfaces.
- Backup, restore, export, and portability requirements.
- Required external dependencies.
- Platform compatibility requirements, including the current Glaze UI target where applicable.
- Structured acceptance-test evidence references.
- Structured release evidence references.
- Declared conformance status, blockers, validation time, and evidence references.

Unknown fields are rejected. In-scope components must not invent incompatible local Platform Contract extensions. Breaking contract changes belong in a new version of the central contract with an explicit migration path.

## Supported component classes

Contract `0.4` recognizes these machine-readable component classes:

- `application`
- `service`
- `shared-library`

`shared-library` is the governed representation for reusable GoreeCloud platform libraries, design systems, frameworks, and comparable shared components that are not themselves deployable applications or services. This is a backward-compatible Contract `0.4` extension: existing application and service manifests remain valid without reclassification.

All supported component classes still evaluate all nine Integral Platform Systems. A shared-library declaration does not waive security, privacy, lifecycle, evidence, release, authority-boundary, or other applicable governance. Genuine non-applicability must remain evidence-backed.

Stable acceptance requirements are component-aware. Applications and services retain the existing cross-cutting Stable acceptance baseline: API, accessibility, supported-platform, backup, restore, export/portability, security, privacy, documentation, integration, and release evidence. A shared library has the class baseline of accessibility, supported-platform, security, privacy, documentation, integration, and release evidence. API, backup, restore, and export/portability evidence remain required for a shared library whenever its actual Role and Purpose or another governing requirement makes those capabilities applicable; omission from the class baseline is not a waiver or an automatic not-applicable determination.

## Platform-System result vocabulary

Contract `0.4` uses the following machine values:

- `Applicable — Conformant` → `applicable-conformant`
- `Applicable — Migration Required` → `applicable-migration-required`
- `Applicable — Blocked` → `applicable-blocked`
- `Applicable — Nonconformant` → `applicable-nonconformant`
- `Not Applicable — Justified` → `not-applicable-justified`

`not-applicable-justified` requires an explicit justification and an evidence reference supporting the applicability decision. `applicable-conformant` requires evidence references. The result records repository truth without upgrading incomplete work merely to satisfy CI.

A previous seven-system declaration does not establish Policy or Observability state. Migration to `0.4` requires explicit component-specific evaluation of both new systems.

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

`evidence.acceptance_tests` records attributable evidence references with an ID, category, repository path, exact revision, result, and observation time. Supported Platform-System categories cover all nine systems, including `policy` and `observability`, plus API, accessibility, supported-platform, backup, restore, export/portability, security, privacy, documentation, integration, migration, rollback, and release acceptance.

When an Integral Platform System is declared `applicable-conformant` for a Stable product, the validator requires a passing structured acceptance-evidence category for that system. Genuine `not-applicable-justified` results do not require a passing system acceptance category, but they do require explicit justification and supporting evidence.

Policy evidence should identify the owning rule authority, policy/version identity, evaluation context, decision, reason, evaluation time/freshness, and enforcement result where applicable without exposing unnecessary private or secret information.

Observability evidence should preserve signal source, component identity, signal type, observation/collection time, freshness, health state, correlation context where applicable, known collection gaps, and completeness where relevant. Missing telemetry, stale evidence, unknown state, or partial observation must not be converted into a healthy result.

`evidence.release` records release evidence with an ID, version, revision, path, result, observation time, and optional artifact digest. Prose declarations never substitute for the underlying test, workflow artifact, release record, restore record, policy-decision record, observability record, or acceptance record.

## Stable fail-closed gates

A `stable` lifecycle declaration fails validation unless:

- all nine Integral Platform Systems have passing results (`applicable-conformant` or evidence-backed `not-applicable-justified`);
- each applicable-conformant Integral Platform System has passing structured system acceptance evidence;
- the current required Glaze UI target is `1.5.1` where applicable;
- conformance is declared `conformant` with a validation timestamp;
- required cross-cutting Stable acceptance categories for the declared component class have passing evidence; and
- published release evidence exists.

Unknown, stale, missing, denied, failed, blocked, migration-required, or unverified mandatory state does not become passing state through aggregation, absence of observed failure, or metadata alone.

A passing manifest or computed conformance result proves only the checks encoded by the validator. Runtime acceptance, representative-device/browser validation, accessibility, recovery, policy behavior, observability completeness, release approval, deployment, production acceptance, and Stable qualification remain independent gates where applicable.

## Exact-revision authority

Pull-request validation must evaluate the exact PR head rather than GitHub's synthetic merge ref. The reusable workflow records the evaluated repository revision and the exact evaluator revision in the computed result and retained evidence artifact. Any candidate-head change resets exact-head validation.

## Migration from Contract 0.2

Repositories using Contract `0.2` must migrate deliberately rather than mass-normalizing version strings:

1. verify the repository's current implementation and evidence;
2. add `platform_systems.policy` and explicitly evaluate its applicability and current state;
3. add `platform_systems.observability` and explicitly evaluate its applicability and current state;
4. preserve truthful existing seven-system results rather than upgrading them automatically;
5. set `schema_version` and `compatibility.platform_contract` to `0.4` only after the manifest shape is updated;
6. retain GoreeCloud Sync as a separately governed capability rather than adding it to `platform_systems`;
7. add or update Policy and Observability evidence references where substantive evidence exists;
8. rerun exact-head manifest, conformance, source/build, and affected runtime validation; and
9. preserve historical `0.2` and `0.3` evidence rather than rewriting history.

A repository that has not yet evaluated Policy and Observability remains migration-required or otherwise nonconformant for v3.0 nine-system qualification; prior seven-system Stable evidence does not prove those new systems.

## Migration from historical Contract 0.3

Any retained `0.3` declaration must first preserve its Sync-specific evidence outside the Integral Platform System set. It must not reinterpret the historical Sync key as GoreeCloud Policy or GoreeCloud Observability. Migration proceeds to `0.4` by adopting the nine current keys and retaining Sync under its separately governed application/service integration records.

Canonical Drive governance controls the platform-system count, meanings, and authority boundaries when repository-local implementation becomes stale or conflicts with it.
