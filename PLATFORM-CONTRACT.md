# GoreeCloud Platform Contract

## Status

- Contract version: `2.0`
- Repository role: platform-wide implementation and conformance reference
- Manifest filename: `goreecloud.platform.yaml`
- Computed result filename: `goreecloud.conformance-result.json`
- Applies to: GoreeCloud application, service, and governance-recognized shared-library repositories
- Canonical governance: GoreeCloud Google Drive instructions, policies, standards, rules, preferences, and project specifications
- Integral Platform System authority: **Instructions — Integral Platform Systems v3.0**
- Release-lifecycle authority: **Standard — Application and Service Release Lifecycle v0.7**
- Current approved Glaze UI consumer target: `1.6.0` (`GLAZE UI V1.6`)

Contract `2.0` is the first Platform Contract version to implement the canonical GoreeCloud release lifecycle:

**Seed → Lab → Forge → Weave → Seal → Anchor → Sunset → Archive**

The nine-system Integral Platform Systems model carried by Contract `0.4` remains in force. Contract `2.0` changes lifecycle vocabulary and adds explicit lifecycle metadata so lifecycle, deployment, qualification, temporary flags, version identity, and conformance are not collapsed into one field.

Contract versions are not silently reinterpreted. A `0.4` manifest retains the legacy lifecycle semantics defined by the `0.4` evaluator that produced or validated it. A repository adopts `2.0` only through an explicit, evidence-backed migration.

A manifest is a declaration and validation input. It does not by itself prove that a capability is implemented, accepted, deployed, production-ready, or Anchor-qualified.

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

**GoreeCloud Sync is not a tenth Integral Platform System.** It remains a separately governed application/service capability.

## Supported component classes

Contract `2.0` recognizes:

- `application`
- `service`
- `shared-library`

Every independently governed component manifest declares exactly one lifecycle stage. Project-level `Mixed` summaries belong in aggregation or inventory records and never replace an individual component lifecycle.

## Canonical lifecycle values

| Lifecycle | Machine value | Governing meaning |
| --- | --- | --- |
| Seed | `seed` | Approved initiative; implementation commitment is not yet established. |
| Lab | `lab` | Exploratory prototypes, experiments, or disposable implementation. |
| Forge | `forge` | Committed active construction. |
| Weave | `weave` | Integration, convergence, hardening, migration, and release-completeness work dominate. |
| Seal | `seal` | One exact release candidate is frozen for qualification. |
| Anchor | `anchor` | The exact release has passed the applicable acceptance boundary and is supported for normal production use. |
| Sunset | `sunset` | Migration-away state; new dependencies require an explicit exception. |
| Archive | `archive` | Ordinary development/support/production use has ended and required preservation is complete. |

Legacy `concept`, `experimental`, `development`, `release-candidate`, `stable`, `deprecated`, and `retired` values are not valid Contract `2.0` lifecycle values.

## Lifecycle metadata and separation

Contract `2.0` requires `lifecycle_metadata` so lifecycle is not confused with other controls.

### Flags

Component manifests may use:

- `blocked`
- `security-hold`
- `privacy-hold`
- `recovery-hold`
- `migration-required`
- `superseded`

`Mixed` is aggregation-only and is not valid in an independently governed component manifest.

### Deployment state

Deployment state is separate from lifecycle and uses one of:

- `development`
- `test`
- `staging`
- `acceptance`
- `controlled-production`
- `normal-production`
- `recovery`
- `other`

A production deployment does not establish Anchor.

### Qualification state

Qualification state is separate from lifecycle and uses:

- `not-started`
- `in-progress`
- `blocked`
- `passed`
- `not-applicable`

Anchor requires `qualification_state: passed`.

### Candidate identity

A Seal manifest must provide `lifecycle_metadata.candidate_identity`. Its `source_revision` is an exact 40-character lowercase Git commit SHA. Additional identity fields may record review/build identity, artifact name or digest, container digest, package identity, SBOM, schema/migration identity, configuration boundary, dependency state, previous known-good release, and rollback target.

Changing a release-critical source, artifact, runtime dependency, package, migration, configuration, security, privacy, recovery, or supported-platform boundary invalidates the prior Seal identity and requires a new candidate plus repeated validation affected by the change.

Non-Seal manifests may retain candidate identity for accepted-release traceability.

### Transition evidence

`last_transition` records the most recent lifecycle-transition time when known. `evidence` contains repository-relative or otherwise governed references supporting the lifecycle state. Anchor requires traceable lifecycle evidence.

## Required manifest areas

Every Contract `2.0` manifest declares:

- Contract schema version.
- Component class, stable identifier, product name, and authoritative repository.
- Canonical lifecycle stage.
- Separate lifecycle metadata, flags, deployment state, qualification state, next gate, candidate identity, transition time, and lifecycle evidence.
- Current version identity.
- Supported platforms.
- API versions and declared endpoints.
- An integration result for each of the nine Integral Platform Systems.
- GoreeCloud Mesh capabilities, dependencies, and published/consumed events where applicable.
- Health and readiness interfaces.
- Backup, restore, export, and portability requirements.
- Required external dependencies.
- Compatibility requirements, including the current approved Glaze UI target where applicable.
- Structured acceptance evidence.
- Structured release evidence.
- Declared conformance status, blockers, validation time, and evidence references.

Unknown fields are rejected. Breaking contract changes require a new contract version and an explicit migration path.

## Platform-System result vocabulary

Contract `2.0` retains the Contract `0.4` integration-result vocabulary:

- `Applicable — Conformant` → `applicable-conformant`
- `Applicable — Migration Required` → `applicable-migration-required`
- `Applicable — Blocked` → `applicable-blocked`
- `Applicable — Nonconformant` → `applicable-nonconformant`
- `Not Applicable — Justified` → `not-applicable-justified`

`not-applicable-justified` requires explicit justification and evidence. `applicable-conformant` requires evidence references. The result records truth without upgrading incomplete work merely to satisfy CI.

## Evidence model

`evidence.acceptance_tests` records attributable evidence references with an ID, category, repository path, exact revision, result, and observation time. Supported categories cover all nine Integral Platform Systems plus API, accessibility, supported-platform, backup, restore, export/portability, security, privacy, documentation, integration, migration, rollback, and release acceptance.

`evidence.release` records release evidence with an ID, version, revision, path, result, observation time, and optional artifact digest.

Prose declarations never substitute for the underlying workflow artifact, release record, restore record, policy decision, observability record, or acceptance record.

## Anchor fail-closed gate

An `anchor` lifecycle declaration fails validation unless:

- all nine Integral Platform Systems have passing results (`applicable-conformant` or evidence-backed `not-applicable-justified`);
- every applicable-conformant Integral Platform System has passing structured system acceptance evidence;
- `lifecycle_metadata.qualification_state` is `passed`;
- lifecycle-transition/qualification evidence is traceable through `lifecycle_metadata.evidence`;
- the current approved Glaze UI target is `1.6.0` where applicable;
- conformance is declared `conformant` with a validation timestamp;
- required cross-cutting Anchor acceptance categories for the component class have passing evidence; and
- published release evidence exists.

The computed result exposes `anchor_eligible`; Contract `2.0` does not expose the old `stable_eligible` field.

Unknown, stale, missing, denied, failed, blocked, migration-required, or unverified mandatory state does not become passing state through aggregation, absence of observed failure, or metadata alone.

A passing manifest or computed conformance result proves only the checks encoded by the validator. Runtime acceptance, representative-device/browser validation, accessibility, recovery, policy behavior, observability completeness, release approval, deployment, production acceptance, and Anchor qualification remain independent gates where applicable.

## Exact-revision authority

Pull-request validation evaluates the exact PR head rather than GitHub's synthetic merge ref. The reusable workflow records both the evaluated repository revision and the exact evaluator revision in the computed result and retained evidence artifact. Any candidate-head change resets exact-head validation.

## Migration from Contract 0.4

Migration is evidence-based and must not be implemented as mass string replacement.

1. Verify the repository's current implementation, project/service record, release line, and applicable evidence.
2. Preserve Contract `0.4` evidence with its original lifecycle vocabulary and evaluator identity.
3. Reclassify the governed unit under the canonical lifecycle:
   - `concept` normally maps to `seed` after current-state verification.
   - `experimental` normally maps to `lab` after current-state verification.
   - `development` requires an evidence-based choice between `forge` and `weave`.
   - `release-candidate` may become `seal` only when an exact candidate identity is established.
   - `stable` may become `anchor` only when current Anchor qualification remains valid.
   - `deprecated` normally maps to `sunset`.
   - `retired` may become `archive` only after required migration, preservation, recovery, and historical-record obligations are complete.
4. Add truthful `lifecycle_metadata`; keep version, deployment, qualification, flags, and lifecycle distinct.
5. For Seal, record exact candidate identity rather than a moving label such as `latest` or `current`.
6. Preserve the nine Integral Platform System results unless current evidence justifies a change.
7. Set `schema_version` and `compatibility.platform_contract` to `2.0` only after the manifest is structurally and semantically migrated.
8. Rerun exact-head manifest, conformance, source/build, and affected runtime validation.
9. Synchronize the authoritative project/service record, repository manifest, release records, inventories, and operational views without falsely increasing maturity.

A repository that cannot yet justify its new lifecycle remains on its historical contract/evidence boundary or records a truthful blocked migration in its authoritative task/project records. Unsupported new lifecycle values must not be emitted under an older contract.

## Earlier contract versions

- Contract `0.2` represented the earlier seven-system model.
- Contract `0.3` was a superseded experiment that represented GoreeCloud Sync as an eighth Integral Platform System.
- Contract `0.4` established the current nine-system Integral Platform Systems model while retaining the legacy lifecycle vocabulary.

Historical evidence remains historical. Contract `2.0` does not reinterpret prior evaluator output.

## Authority

Canonical GoreeCloud Drive governance controls lifecycle meaning, platform-system count, authority boundaries, qualification requirements, and documentation precedence when repository-local implementation becomes stale or conflicts with it.
