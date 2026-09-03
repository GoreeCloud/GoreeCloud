# GoreeCloud Platform Releases

## Purpose

A GoreeCloud platform release is a coordinated, evidence-backed compatibility selection across independently maintained GoreeCloud components. A platform release manifest records the selected revisions, producer-declared compatibility inputs, cross-component compatibility results, release-gate evidence, and certification outcome.

The release layer does **not** manufacture component truth. Application and service repositories remain authoritative for their own implementation and producer evidence. The GoreeCloud Platform Contract computes component conformance. GoreeCloud Mesh may aggregate those records, and GoreeCloud Manager may present them, but neither aggregation nor presentation strengthens a producer claim.

## Machine-readable contract

The release contract consists of:

- `schemas/goreecloud.platform-release.schema.json` — release-manifest structure;
- `contracts/goreecloud.release-rules.v1.json` — mandatory platform-release rules;
- `scripts/validate_platform_release.py` — fail-closed schema and semantic validator;
- `releases/*.yaml` — planning, candidate, or certified release manifests.

Schema validity is not certification. A release is certified only when the semantic validator accepts a manifest whose release state and certification result are both `certified`.

## Required compatibility inputs

Each release component records:

- component and product identity;
- repository;
- release role;
- Integral Platform System slot when applicable;
- whether the component is required for the release;
- selection state;
- exact version and source revision when selected;
- lifecycle state;
- whether compatibility inputs are still unknown or are producer-declared;
- declared component dependencies;
- declared API requirements;
- producer conformance result and revision-bound evidence reference.

`compatibility_input_status: unknown` is materially different from a declared empty dependency list. A certified release requires producer-declared compatibility inputs for every required selected component.

## Compatibility matrix

The compatibility matrix records explicit consumer → provider relationships. A dependency cannot be certified merely because both components are present in the release. For every dependency declared by a required selected component, the provider must also be selected and the matrix must contain evidence-backed `compatible` relationship evidence.

The release validator does not infer compatibility from naming, shared infrastructure, private-network reachability, a successful deployment, or the absence of observed errors.

## Mandatory release gates

Release rules currently require explicit evaluation of:

1. successful CI;
2. Platform Contract validation;
3. security evidence;
4. privacy evidence;
5. recovery evidence;
6. Glaze UI acceptance for applicable user-facing surfaces;
7. API compatibility;
8. dependency compatibility;
9. rollback documentation;
10. release notes;
11. upgrade documentation where applicable.

A passing gate must cite evidence. `not_applicable` is allowed only for gates explicitly permitted by the release rules and requires justification.

## Integral Platform Systems

A certified release must include selected revisions for all seven Integral Platform Systems:

1. GoreeCloud Manager;
2. Privacy Shield;
3. Wardveil Security;
4. Everkeep;
5. Glaze UI;
6. GoreeCloud Mesh;
7. GoreeCloud Identity.

Presence is insufficient. Every required selected component must be producer-conformant, Stable-eligible, revision-bound, and represented by required compatibility evidence.

## GoreeCloud 2026.10 planning line

`releases/goreecloud-2026.10.candidate.yaml` is the first machine-readable planning line for the intended first coordinated platform release. Its release identifier uses a **provisional calendar model** because an authoritative GoreeCloud release-versioning standard has not yet been finalized.

The manifest is intentionally blocked. It must not be described as a Release Candidate lifecycle promotion, a certified compatibility release, a production approval, or a declaration that listed draft application revisions will ship. Current source revisions are included only where they are verified inputs useful to the compatibility work.

At this stage:

- Glaze UI 2.2.0 is the selected design-system baseline;
- the seven-system platform selection is incomplete;
- Manager, Website, and Tasks remain Development/non-Stable despite green source/CI work on their migration branches;
- Mesh registry/API source exists on stacked draft work but does not establish release-level compatibility;
- Identity, Wardveil Security, Privacy Shield, and Everkeep release selections/conformance evidence remain unresolved in this manifest;
- all mandatory release gates remain pending;
- platform compatibility is explicitly `false` and certification is `blocked`.

## Certification boundary

For certification, the validator requires all of the following at the same time:

- `release.state: certified` and `certification.declared_result: certified`;
- a certification timestamp;
- `certification.compatible: true`;
- no declared blockers;
- a verified compatibility matrix;
- all seven Integral Platform Systems selected;
- all required components selected with exact version, exact source revision, lifecycle, producer-declared compatibility inputs, conformant result, Stable eligibility, and revision-bound conformance evidence;
- every selected declared dependency selected and proven compatible by evidence;
- every mandatory release gate passed or, only where explicitly allowed, justified as not applicable.

CI includes a negative control that mutates the blocked planning manifest toward a superficial certified label. The validator must reject it. This prevents certification from becoming a documentation-only status change.

## Evidence and future work

Release evidence should ultimately be generated or referenced from exact component revisions and coordinated integration runs. A future certification manifest may reference CI runs, component conformance results, security/privacy/recovery evidence, Glaze acceptance, API/dependency compatibility, integration testing, rollback plans, release notes, and upgrade documentation.

The first certified release must not be published until the governing release-versioning decision, component selections, integration tests, and mandatory evidence are complete. Green application pull requests alone are not a platform release.
