# Native Application and Platform Conformance

Effective August 24, 2026. Current seven-system Integral Platform baseline reconciled to authoritative GoreeCloud governance on September 14, 2026.

All GoreeCloud applications and services must be original GoreeCloud-owned software built natively from the ground up. Existing complete-product forks or adopted implementations may remain only as controlled migration, compatibility, testing, reference, or historical sources while native replacements are built and accepted.

Narrow exceptions are permitted only for critical supporting foundations such as established cryptographic primitives, WireGuard and other standards/protocol foundations, platform interfaces, database engines, codecs, rendering/runtime components, and comparable dependencies where independent reimplementation would materially reduce security, interoperability, reliability, correctness, or maintainability. Every exception must remain limited to its minimum necessary role.

## Integral Platform Systems

Every GoreeCloud application and service must be evaluated against all seven Integral Platform Systems and implement every applicable responsibility:

- **GoreeCloud Manager** — bounded platform management, inventory, configuration, lifecycle, operational visibility, governance implementation, and administrative control-plane integration where applicable.
- **Privacy Shield** — consent, purpose limitation, minimization, retention, sharing, processing-boundary, and user privacy controls.
- **Wardveil Security** — protection, trust, verification, threat handling, security evidence, and applicable response controls.
- **Everkeep** — resilience, backup, recovery, portability, preservation, continuity, succession, and legacy handling.
- **Glaze UI** — design language, interaction behavior, accessibility, responsive presentation, and visual conformance.
- **GoreeCloud Mesh** — private connectivity, capability discovery, coordination, dependency/event relationships, governance, and interoperability where applicable.
- **GoreeCloud Identity** — user, account, device, application, service, credential, session, authentication, authorization, and delegated-authority boundaries where applicable.

These are functional platform requirements, not branding labels or checklist decorations. An integration must be represented by real product behavior, contracts, authority boundaries, validation, and user-visible state where applicable. If one of the seven Integral Platform Systems is genuinely not applicable to a component, that non-applicability must be explicit and supportable rather than silently omitted.

The seven Platform Systems themselves are required to progress to complete, production-grade implementations of their approved responsibilities. Repository existence, a design document, prototype, partial adapter, source-only implementation, logo, badge, or interface presentation does not satisfy that requirement. Current status must remain evidence-based and truthful until production acceptance exists.

## GoreeCloud Sync

GoreeCloud Sync is an important GoreeCloud synchronization and state-continuity application/service capability, but it is not one of the seven Integral Platform Systems. Products that use synchronization must still define and validate their Sync datasets, authorization, privacy constraints, conflict handling, deletion behavior, offline continuity, and other applicable synchronization requirements. Sync must respect the authority of GoreeCloud Identity, Privacy Shield, Wardveil Security, Everkeep, GoreeCloud Mesh, GoreeCloud Manager, and the owning application or service.

Sync-specific implementation or acceptance evidence may be tracked where applicable, but a product must not describe Sync as an Integral Platform System or make generic seven-system conformance depend on an invented eighth system.

## Acceptance boundary

No GoreeCloud application or service may qualify as Stable or production-ready when a required integration is missing, superseded, outdated, incompatible, placeholder-only, cosmetic-only, unverified, or unaccepted for the claimed release.

A successful build or repository check proves only the checks it actually performs. Source acceptance, application/runtime acceptance, release acceptance, production acceptance, and Stable qualification remain separate decisions.

Repository-local documentation must distinguish implemented and validated behavior from planned, partial, experimental, migration-gated, disabled, blocked, or acceptance-gated work. It must not manufacture positive privacy, security, recoverability, identity, synchronization, coordination, availability, management, or accessibility claims when the corresponding authority has not supplied accepted evidence.

## Authority boundaries

The seven systems are complementary:

- Identity establishes actors and authority.
- Privacy Shield governs permitted information use.
- Wardveil Security governs trust and protection.
- Manager governs bounded administration and operational control.
- Mesh governs private reachability, discovery, coordination, and event/service interoperability.
- Everkeep governs recoverable historical state and continuity.
- Glaze UI governs shared visual, interaction, and accessibility behavior and must accurately represent underlying capability state.

GoreeCloud Sync coordinates authorized synchronized state when an application/service uses it, but synchronization is not identity, privacy authorization, security trust, management authority, Mesh reachability, backup/recovery, or UI conformance. No system or service may silently bypass another authority.

## Platform Contract

Every GoreeCloud application, service, and Integral Platform System is expected to adopt the versioned GoreeCloud Platform Contract through a repository-root `goreecloud.platform.yaml` manifest as the contract rollout reaches that repository. The manifest records declared identity, lifecycle, compatibility, operational interfaces, continuity requirements, all seven platform-system states, and evidence references. Manifest presence or structural validity alone does not establish implementation, acceptance, Stable qualification, or production readiness.

Platform Contract `0.3` is the current draft seven-system contract baseline. Its implementation reference is maintained in this repository under `PLATFORM-CONTRACT.md`, `schemas/goreecloud.platform.schema.json`, and the platform-conformance validation scripts. Until the contract is accepted on the default branch, downstream repositories may pin an exact candidate revision for deterministic Development validation but must not represent that candidate as accepted production authority.

## Continuing migration requirement

Existing GoreeCloud repositories and development plans must transition toward the native-first, seven-system model and keep dependencies, CI, documentation, platform contracts, compatibility evidence, accessibility evidence, recovery evidence, synchronization evidence where applicable, and release state current as shared platform capabilities evolve.

The canonical GoreeCloud Google Drive instructions, decisions, standards, policies, and project specifications remain authoritative when this repository-local summary is less specific or becomes stale.
