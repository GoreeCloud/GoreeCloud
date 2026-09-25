# Native Application and Platform Conformance

Effective August 24, 2026. Nine-system Integral Platform Systems v3.0 alignment prepared September 16, 2026. Platform Contract 2.0 lifecycle alignment prepared September 25, 2026.

All GoreeCloud applications and services must be original GoreeCloud-owned software built natively from the ground up. Existing complete-product forks or adopted implementations may remain only as controlled migration, compatibility, testing, reference, or historical sources while native replacements are built and accepted.

Narrow exceptions are permitted only for critical supporting foundations such as established cryptographic primitives, WireGuard and other standards/protocol foundations, platform interfaces, database engines, codecs, rendering/runtime components, and comparable dependencies where independent reimplementation would materially reduce security, interoperability, reliability, correctness, or maintainability. Every exception must remain limited to its minimum necessary role.

## Integral Platform Systems

Every GoreeCloud application and service must be evaluated against each of the nine Integral Platform Systems and implement every applicable responsibility:

- **GoreeCloud Manager** — bounded platform management, inventory, configuration, lifecycle, operational visibility, governance implementation, approvals, remediation, and administrative control-plane integration where applicable.
- **Privacy Shield** — consent, purpose limitation, minimization, retention, sharing, tracking/telemetry privacy, processing-boundary, and user privacy controls.
- **Wardveil Security** — protection, integrity, trust, verification, threat handling, security evidence, defensive requirements, and applicable response controls.
- **Everkeep** — resilience, backup, recovery, portability, preservation, continuity, migration readiness, succession, and long-term information survival.
- **Glaze UI** — design language, interaction behavior, accessibility, responsive presentation, policy-decision states, operational-health states, evidence states, and visual conformance.
- **GoreeCloud Mesh** — bounded first-party capability discovery, dependency/relationship awareness, coordination, governance, integration, event exchange, policy/observability capability discovery, and evidence routing where applicable.
- **GoreeCloud Identity** — user, account, device, application, service, workload, credential, claim, session, authentication, authorization-integration, and trust boundaries where applicable.
- **GoreeCloud Policy** — common policy representation, evaluation, decisions, distribution, enforcement coordination, explanation, precedence/composition, freshness, and policy evidence while preserving domain rule ownership.
- **GoreeCloud Observability** — operational health, metrics, logs, events, traces, diagnostics, performance, availability, dependency health, freshness, provenance, correlation, and operational evidence.

These are functional platform requirements, not branding labels or checklist decorations. An integration must be represented by real product behavior, contracts, authority boundaries, validation, tests, and evidence appropriate to the component. If one of the nine systems is genuinely not applicable, that non-applicability must be explicit, justified, and evidenced rather than silently omitted.

A previous seven-system evaluation remains evidence only for the original seven systems. It does not establish GoreeCloud Policy or GoreeCloud Observability conformance.

**GoreeCloud Sync is a separately governed application/service capability, not a tenth Integral Platform System.**

## Acceptance boundary

No GoreeCloud application or service may qualify as Anchor or production-ready when a required integration is missing, superseded, outdated, incompatible, placeholder-only, cosmetic-only, denied where approval is required, unknown where a verified result is required, stale, partially observed where complete evidence is required, unverified, or unaccepted for the claimed release.

A successful build or repository check proves only the checks it actually performs. Source acceptance, application/runtime acceptance, policy acceptance, observability acceptance, release acceptance, production acceptance, and Anchor qualification remain separate decisions where applicable.

Repository-local documentation must distinguish implemented and validated behavior from planned, partial, experimental, migration-gated, disabled, or acceptance-gated work. It must not manufacture positive privacy, security, recoverability, identity, policy, observability, coordination, availability, or management claims when the corresponding authority has not supplied accepted evidence.

Missing telemetry or absence of observed failure is not proof of health. A policy engine executing a rule does not become the owner of that rule. Aggregation and presentation do not transfer producer authority.

## Platform Contract

Every GoreeCloud application and service is expected to adopt the versioned GoreeCloud Platform Contract through a repository-root `goreecloud.platform.yaml` manifest as the contract rollout reaches that repository.

Contract `2.0` uses the canonical machine lifecycle values `seed`, `lab`, `forge`, `weave`, `seal`, `anchor`, `sunset`, and `archive`. It keeps lifecycle separate from deployment state, qualification state, temporary lifecycle flags, version identity, conformance, and operational health.

Contract `2.0` requires exact candidate identity for Seal and fail-closed qualification evidence for Anchor. `Mixed` remains an aggregation-only project summary, not a component lifecycle.

Contract `0.4` is the historical nine-system contract with legacy lifecycle vocabulary. Contract `0.2` is the historical seven-system contract. Historical Contract `0.3` represented GoreeCloud Sync as an eighth system and remains superseded historical evidence.

Migration from `0.4` to `2.0` is not a mass string replacement. Existing Development state must be evaluated between Forge and Weave; Release Candidate may become Seal only with exact candidate identity; Stable may become Anchor only when current qualification remains valid; Deprecated normally maps to Sunset; Retired may become Archive only after preservation and migration obligations are complete.

The current implementation reference is maintained in `PLATFORM-CONTRACT.md`, the two Platform Contract schemas, example manifests, validation/evaluation scripts, and reusable workflow.

## Evidence and Anchor qualification

For each applicable Integral Platform System, conformance requires substantive evidence appropriate to the claim. Anchor releases must provide passing structured acceptance evidence for every system declared `applicable-conformant`, plus the other required cross-cutting Anchor evidence and published release evidence.

Policy evidence must preserve the owning rule authority, policy/version identity, relevant evaluation context, decision, reason, freshness, and enforcement result where applicable. Observability evidence must preserve signal source, component identity, signal type, observation/collection time, freshness, health state, relevant correlation context, and known collection gaps where applicable.

No evidence surface may silently convert failed to passing, denied to allowed, degraded to healthy, unknown to verified, stale to current, missing to present, unauthenticated to authenticated, unrecoverable to recoverable, or nonconformant to conformant without an explicitly governed and attributable rule.

## Continuing migration requirement

Existing GoreeCloud repositories and development plans must transition toward the native-first model and the current Platform Contract without inventing maturity. Keep dependencies, CI, documentation, platform contracts, compatibility evidence, accessibility evidence, recovery evidence, policy evidence, observability evidence, lifecycle evidence, and release state current as shared platform systems evolve.

Repository-specific migration must verify the authoritative product record and implementation before changing lifecycle. Old Contract `0.4` evidence remains historical evidence under its original semantics until the governed unit is explicitly reclassified.

The canonical GoreeCloud Google Drive instructions, standards, policies, rules, preferences, and project specifications remain authoritative when this repository-local summary is less specific or becomes stale.
