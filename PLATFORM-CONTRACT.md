# GoreeCloud Platform Contract

`goreecloud.platform.yaml` is the repository-owned machine-readable declaration for a GoreeCloud application, service, website, library, or platform component.

## Authority model

The component repository remains authoritative for component-owned facts and evidence. GoreeCloud Mesh may ingest and aggregate declarations, relationships, capabilities, dependencies, and evidence references, but aggregation does not transfer producer authority to Mesh. GoreeCloud Manager consumes the Mesh representation read-only and must not manufacture stronger security, privacy, identity, recovery, design-conformance, runtime, or release claims than the authoritative evidence supports.

The canonical contract schema is `schemas/goreecloud.platform.schema.json`. The canonical computed result schema is `schemas/goreecloud.conformance-result.schema.json`. Platform-wide compatibility and evidence rules are in `contracts/goreecloud.platform-rules.v1.json`.

Repositories must not copy and independently evolve these schemas. Consumer CI checks out a pinned revision of this repository and validates its local `goreecloud.platform.yaml` against that revision.

## Stable fail-closed behavior

A `Stable` lifecycle declaration is rejected when mandatory conformance is incomplete. The validator computes conformance from the contract rather than trusting `conformance.declared_state` or `conformance.stable_eligible`.

Mandatory implementation checks cannot pass using documentation evidence alone. Missing evidence, missing required checks, stale Glaze UI, unresolved mandatory platform-system integration, or missing verified restore evidence where restoration is required results in non-conformance. A Development component may intentionally remain non-conformant while CI still validates that its declaration is truthful and structurally valid; this does not make it Stable-eligible.

The required baseline checks are:

- Glaze UI.
- GoreeCloud Identity.
- Wardveil Security.
- Privacy Shield.
- Everkeep recovery.
- Mesh registration.
- API compatibility.
- Accessibility acceptance.
- Supported-platform acceptance.
- Backup configuration/evidence.
- Restore validation/evidence.
- Export and portability.
- Security validation.
- Privacy validation.
- Required documentation.
- Required tests.
- Release evidence.

## Recovery semantics

Backup and restore are independent fields. A running or successful backup must never be interpreted as a verified restoration. When restoration is required, Stable eligibility requires `restore_status: verified` and a concrete `last_verified_restore` timestamp backed by recovery evidence.

## Lifecycle vocabulary

The schema uses the authoritative GoreeCloud lifecycle vocabulary:

`Concept → Experimental → Development → Release Candidate → Stable → Deprecated → Retired`.

The authoritative Drive record `Standard — Application and Service Release Lifecycle` was reconciled to this seven-state vocabulary as version v0.2. Alpha, Beta, Maintenance, and End of Life are retained there only as superseded historical labels; current lifecycle declarations must use the seven approved values and must be evidence-based rather than mechanically translated from a historical label.

## Evidence

Evidence records are immutable references to source, automated tests, integration tests, runtime observations, rendered validation, accessibility validation, recovery validation, security/privacy validation, releases, deployments, or documentation. Evidence should identify the producer and exact revision or observation time where applicable.

The contract records evidence references; it does not duplicate private or sensitive payloads. Sensitive producer evidence should remain in its authoritative protected system and be represented through minimized, policy-approved Mesh evidence envelopes.
