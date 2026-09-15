# Native Application and Platform Conformance

Effective August 24, 2026. Current integral-platform baseline updated September 2, 2026.

All GoreeCloud applications and services must be original GoreeCloud-owned software built natively from the ground up. Existing complete-product forks or adopted implementations may remain only as controlled migration, compatibility, testing, reference, or historical sources while native replacements are built and accepted.

Narrow exceptions are permitted only for critical supporting foundations such as established cryptographic primitives, WireGuard and other standards/protocol foundations, platform interfaces, database engines, codecs, rendering/runtime components, and comparable dependencies where independent reimplementation would materially reduce security, interoperability, reliability, correctness, or maintainability. Every exception must remain limited to its minimum necessary role.

## Integral platform systems

Every GoreeCloud application and service must implement and remain current with each applicable integral platform system:

- **GoreeCloud Manager** — bounded platform management, inventory, configuration, lifecycle, operational visibility, governance implementation, and administrative control-plane integration where applicable.
- **Privacy Shield** — consent, purpose limitation, minimization, retention, sharing, processing-boundary, and user privacy controls.
- **Wardveil Security** — protection, trust, verification, threat handling, security evidence, and applicable response controls.
- **Everkeep** — resilience, backup, recovery, portability, preservation, continuity, succession, and legacy handling.
- **Glaze UI** — design language, interaction behavior, accessibility, responsive presentation, and visual conformance.
- **GoreeCloud Mesh** — bounded first-party capability discovery, coordination, governance, integration, and event/capability exchange where applicable.
- **GoreeCloud Identity** — user, account, device, application, service, credential, session, authentication, authorization, and delegated-authority boundaries where applicable.

These are functional platform requirements, not branding labels or checklist decorations. An integration must be represented by real product behavior, contracts, authority boundaries, validation, and user-visible state where applicable. If one of the seven systems is genuinely not applicable to a particular component, that non-applicability must be explicit and supportable rather than silently omitted.

## Acceptance boundary

No GoreeCloud application or service may qualify as Stable or production-ready when a required integration is missing, superseded, outdated, incompatible, placeholder-only, cosmetic-only, unverified, or unaccepted for the claimed release.

A successful build or repository check proves only the checks it actually performs. Source acceptance, application/runtime acceptance, release acceptance, production acceptance, and Stable qualification remain separate decisions.

Repository-local documentation must distinguish implemented and validated behavior from planned, partial, experimental, migration-gated, disabled, or acceptance-gated work. It must not manufacture positive privacy, security, recoverability, identity, synchronization, coordination, availability, or management claims when the corresponding authority has not supplied accepted evidence.

## Platform Contract

Every GoreeCloud application and service is expected to adopt the versioned GoreeCloud Platform Contract through a repository-root `goreecloud.platform.yaml` manifest as the contract rollout reaches that repository. The manifest records declared identity, lifecycle, compatibility, operational interfaces, continuity requirements, platform-system state, and evidence references. Manifest presence or structural validity alone does not establish implementation, acceptance, Stable qualification, or production readiness.

The current implementation reference for the Platform Contract is maintained in this repository under `PLATFORM-CONTRACT.md`, `schemas/goreecloud.platform.schema.json`, and the platform-conformance validation scripts.

## Continuing migration requirement

Existing GoreeCloud repositories and development plans must transition toward the native-first model and keep dependencies, CI, documentation, platform contracts, compatibility evidence, accessibility evidence, recovery evidence, and release state current as the shared platform systems evolve.

The canonical GoreeCloud Google Drive instructions, standards, policies, and project specifications remain authoritative when this repository-local summary is less specific or becomes stale.
