# GoreeCloud Platform Contract

## Status

- Contract version: `0.1`
- Repository role: platform-wide implementation reference
- Manifest filename: `goreecloud.platform.yaml`
- Applies to: GoreeCloud application and service repositories
- Canonical governance: GoreeCloud Google Drive instructions, standards, policies, and project specifications

This repository contains the machine-readable implementation foundation for the GoreeCloud Platform Contract. The contract records a repository's declared platform identity, lifecycle, compatibility, operational interfaces, continuity requirements, and evidence-backed integration state. A manifest is a declaration and validation input; it does not by itself prove that a capability is implemented or accepted.

## Required manifest areas

Every application or service manifest must declare:

- Contract schema version.
- Component type, stable application/service identifier, product name, and authoritative repository.
- Lifecycle state and current version.
- Supported platforms.
- API versions and declared endpoints.
- Glaze UI version and integration status.
- GoreeCloud Manager integration status.
- GoreeCloud Identity integration status.
- Wardveil Security integration status.
- Privacy Shield integration status.
- Everkeep integration status and recovery requirements.
- GoreeCloud Mesh integration status, capabilities, dependencies, and published/consumed events.
- Health and readiness interfaces.
- Backup, restore, export, and portability requirements.
- Required external dependencies.
- Platform compatibility requirements.
- Conformance status, blockers, validation time, and evidence references.

## Integral Platform Systems

The current platform baseline contains seven Integral Platform Systems:

1. GoreeCloud Manager
2. Privacy Shield
3. Wardveil Security
4. Everkeep
5. Glaze UI
6. GoreeCloud Mesh
7. GoreeCloud Identity

Each system must be evaluated explicitly. `not-applicable` may be used only with a supportable explanation. Cosmetic presence, metadata, documentation, or an empty adapter is not implementation evidence.

## Lifecycle values

The platform contract uses the following lifecycle values:

- `concept`
- `experimental`
- `development`
- `release-candidate`
- `stable`
- `deprecated`
- `retired`

A manifest using `stable` must not pass Stable gating unless the required platform-system entries are either `implemented` with evidence or supportably `not-applicable`, and the manifest's conformance state is `conformant`.

## Integration status values

Each platform-system integration uses one of:

- `implemented`
- `partial`
- `planned`
- `not-applicable`
- `unknown`

These values describe declared state only. Acceptance evidence remains necessary where required.

## Conformance values

The manifest-level conformance state uses one of:

- `conformant`
- `partial`
- `nonconformant`
- `unverified`

`conformant` is reserved for a state supported by the required evidence and validation for the claimed lifecycle.

## Evidence

Evidence references should identify durable repository paths, workflow artifacts, test reports, release records, acceptance records, or other verifiable sources. A bare statement such as `implemented: true` is not sufficient evidence.

The validator enforces structural requirements and limited fail-closed Stable gating. It does not replace application/runtime testing, security review, privacy review, restore testing, accessibility acceptance, release acceptance, or production acceptance.

## Files in this repository

- `schemas/goreecloud.platform.schema.json` — machine-readable JSON Schema for editors and tooling.
- `examples/goreecloud.platform.example.yaml` — non-production example manifest.
- `scripts/validate_platform_manifest.py` — semantic manifest validator.
- `.github/workflows/platform-conformance.yml` — CI that validates the central platform baseline and example contract.

## Repository adoption

Application and service repositories should place `goreecloud.platform.yaml` at the repository root. Rollout should preserve truthfulness: unknown or planned integrations should be declared as such rather than being upgraded to `implemented` merely to satisfy automation.

The central contract can evolve through versioned schema changes. Breaking contract changes require a new schema version and an explicit migration path.
