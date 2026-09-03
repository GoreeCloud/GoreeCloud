# GoreeCloud Platform Conformance Inventory

## Status

- **Observed:** September 3, 2026
- **Repository footprint:** 62 owned repositories — 59 public, 3 private
- **Current Platform Contract:** `0.2`
- **Manifest filename:** `goreecloud.platform.yaml`
- **Current schema component types:** `application`, `service`
- **Current Stable Glaze UI consumer target used by the Platform Contract:** `1.1.0`

This document is the operational inventory for GoreeCloud Platform Contract adoption across the currently owned repository estate.

It is intentionally **derivative**, not a competing source of truth. Repository membership and public/private counts remain governed by `REPOSITORIES.md` and `repositories.public.json`. The Platform Contract and schema remain governed by `PLATFORM-CONTRACT.md` and `schemas/goreecloud.platform.schema.json`. Repository-local manifests remain declarations owned by their repositories and do not by themselves establish implementation, acceptance, Stable qualification, or production readiness.

Private repository identities are intentionally omitted from this public inventory. Only aggregate private-repository adoption counts are recorded here.

## Audit method

For every repository in the September 3, 2026 owned-repository inventory, the verified default branch was checked directly for a repository-root `goreecloud.platform.yaml`.

The audit distinguishes:

- **Current v0.2** — a root manifest declares `schema_version: "0.2"`.
- **Legacy v0.1** — a root manifest exists but uses superseded Platform Contract schema `0.1`; migration is required before it can represent current contract adoption.
- **Missing** — no root manifest exists on the verified default branch.
- **Scope/model review** — repository purpose does not map cleanly to the current v0.2 schema's single `application` or `service` component model and requires an explicit contract-model decision before adoption is enforced.
- **Not required by current v0.2 contract** — the repository is not currently an application or service repository under the current schema boundary. Other GoreeCloud governance and conformance requirements may still apply.

Manifest presence is not treated as conformance evidence. A current manifest may truthfully declare `nonconformant`, blocked integrations, missing evidence, or Development lifecycle state.

## Portfolio adoption summary

| Adoption state | Total | Public | Private |
| --- | ---: | ---: | ---: |
| Current v0.2 manifest | 8 | 6 | 2 |
| Legacy v0.1 manifest | 0 | 0 | 0 |
| Missing root manifest | 54 | 53 | 1 |
| **Owned repositories** | **62** | **59** | **3** |

Eight owned repositories now have a repository-root manifest on the current Platform Contract schema. No repository in the observed portfolio remains on the superseded v0.1 schema.

## Confirmed current-contract application/service scope

Role and repository-manifest evidence identify **55 repositories** as confirmed application or service repositories under the current v0.2 component model: **52 public** and **3 private**.

| Confirmed application/service adoption state | Count |
| --- | ---: |
| Current v0.2 manifest | 8 |
| Legacy v0.1 manifest requiring migration | 0 |
| Missing root manifest | 47 |
| **Confirmed application/service repositories** | **55** |

Accordingly, **47 of 55 confirmed application/service repositories still require initial Platform Contract adoption work**: 46 public and 1 private. Current manifest adoption does not automatically establish Platform conformance; each declaration retains its repository-specific lifecycle, result, blockers, and evidence state.

## Current v0.2 repositories

The following public repositories have a current v0.2 manifest on their verified default branch:

1. `GoreeCloud/goreecloud-containers`
2. `GoreeCloud/goreecloud-identity`
3. `GoreeCloud/goreecloud-manager`
4. `GoreeCloud/goreecloud-mesh`
5. `GoreeCloud/goreecloud-tasks`
6. `GoreeCloud/goreecloud-website`

Two additional private application/service repositories have current v0.2 manifests. Their identities are intentionally not centralized in this public inventory.

All eight current manifests retain Development/non-Stable boundaries appropriate to their repository evidence. Current manifest adoption must not be interpreted as Stable qualification, production approval, or complete integration with all seven Integral Platform Systems.

### `GoreeCloud/goreecloud-containers`

- Root manifest: present
- Schema: `0.2`
- Component type: `application`
- Lifecycle declaration: `development`
- Version declaration: `0.1.0-dev.0`
- Declared conformance: `nonconformant`
- Acceptance-test evidence entries: none
- Release evidence entries: none
- GoreeCloud Manager: `applicable-blocked`
- Privacy Shield: `applicable-blocked`
- Wardveil Security: `applicable-blocked`
- Everkeep: `applicable-blocked`
- Glaze UI: `applicable-blocked`
- GoreeCloud Mesh: `applicable-blocked`
- GoreeCloud Identity: `applicable-blocked`

This is a truthful Development-state v0.2 declaration. Its presence establishes current manifest adoption, not Platform conformance or Stable eligibility.

## September 3 v0.1 migration checkpoint

The five repositories that carried legacy v0.1 manifests at the initial September 3 audit have now been migrated to v0.2 on their authoritative default branches.

The migration work followed these constraints:

- legacy `partial`, `planned`, and similar states were mapped conservatively rather than upgraded into positive current conformance;
- genuine self-authority relationships were retained only as evidence-backed `not-applicable-justified` results;
- required but unaccepted integrations remain `applicable-migration-required`, `applicable-blocked`, or otherwise non-positive as supported by repository evidence;
- structured v0.2 acceptance and release evidence collections were not populated with invented evidence;
- each migrated repository remains below Stable where required implementation or acceptance is incomplete;
- reusable Platform Contract validation was pinned to an immutable central contract revision rather than a moving branch;
- repository-specific validation was allowed to fail closed and was corrected where a stale v0.1 consumer validator conflicted with the v0.2 implemented-version versus required-baseline model.

The four public migrations were:

1. `GoreeCloud/goreecloud-manager`
2. `GoreeCloud/goreecloud-mesh`
3. `GoreeCloud/goreecloud-tasks`
4. `GoreeCloud/goreecloud-website`

The fifth migration occurred in a private repository whose identity remains intentionally omitted from this public inventory.

This checkpoint records Platform Contract migration and validation only. It does not establish product Stable qualification, production deployment, or producer-system acceptance.

## September 3 initial-adoption wave checkpoint

`GoreeCloud/goreecloud-identity` and one additional private Integral Platform System repository now have v0.2 declarations on their authoritative default branches.

`GoreeCloud/goreecloud-identity` declares itself as a Development service in active native migration. Its substantial inherited runtime remains transitional, its native Identity Center and several Integral Platform System relationships remain blocked, and its GoreeCloud Mesh relationship is migration-required rather than production-accepted. The repository's dedicated Platform Contract validation passed on the adoption revision. Broader inherited repository CI remains an independent source-quality concern and does not convert the manifest into a positive conformance claim.

The additional private adoption is recorded only in aggregate in this public inventory. Its repository-local manifest remains authoritative for its lifecycle, integration states, evidence, and blockers.

Neither adoption adds acceptance-test or release evidence merely because a v0.2 declaration exists. Both remain non-Stable and nonconformant at the Platform Contract level.

## Confirmed public application/service repositories missing a manifest

The following **46 public repositories** are confirmed application/service repositories and have no repository-root `goreecloud.platform.yaml` on their verified default branch:

1. `GoreeCloud/goreecloud-ai`
2. `GoreeCloud/goreecloud-app-store`
3. `GoreeCloud/goreecloud-backup`
4. `GoreeCloud/goreecloud-bookmark-browser-extension`
5. `GoreeCloud/goreecloud-bookmarks`
6. `GoreeCloud/goreecloud-boot`
7. `GoreeCloud/goreecloud-browser`
8. `GoreeCloud/goreecloud-calendar`
9. `GoreeCloud/goreecloud-changelogs`
10. `GoreeCloud/goreecloud-code`
11. `GoreeCloud/goreecloud-contacts`
12. `GoreeCloud/goreecloud-dav`
13. `GoreeCloud/goreecloud-dns`
14. `GoreeCloud/goreecloud-documents`
15. `GoreeCloud/goreecloud-drive`
16. `GoreeCloud/goreecloud-file-manager`
17. `GoreeCloud/goreecloud-gallery`
18. `GoreeCloud/goreecloud-gateway`
19. `GoreeCloud/goreecloud-github-dashboard`
20. `GoreeCloud/goreecloud-index`
21. `GoreeCloud/goreecloud-keyboard`
22. `GoreeCloud/goreecloud-launcher`
23. `GoreeCloud/goreecloud-location`
24. `GoreeCloud/goreecloud-mail`
25. `GoreeCloud/goreecloud-maps`
26. `GoreeCloud/goreecloud-memos`
27. `GoreeCloud/goreecloud-messenger`
28. `GoreeCloud/goreecloud-metrics`
29. `GoreeCloud/goreecloud-monitor`
30. `GoreeCloud/goreecloud-music`
31. `GoreeCloud/goreecloud-network`
32. `GoreeCloud/goreecloud-network-android`
33. `GoreeCloud/goreecloud-network-dashboard`
34. `GoreeCloud/goreecloud-notes`
35. `GoreeCloud/goreecloud-notify`
36. `GoreeCloud/goreecloud-photos`
37. `GoreeCloud/goreecloud-quill`
38. `GoreeCloud/goreecloud-redirector`
39. `GoreeCloud/goreecloud-rss`
40. `GoreeCloud/goreecloud-search`
41. `GoreeCloud/goreecloud-source-resync`
42. `GoreeCloud/goreecloud-sync`
43. `GoreeCloud/goreecloud-terminal`
44. `GoreeCloud/goreecloud-vault-server`
45. `GoreeCloud/goreecloud-video`
46. `GoreeCloud/goreecloud-waypoint`

The private scope contributes **1 additional confirmed application/service repository with a missing root manifest**, recorded only as an aggregate to preserve the established public privacy boundary.

## Scope/model review

These repositories require an explicit current-contract modeling decision rather than an automatic exemption or an invented component type:

| Repository | Root manifest | Review reason |
| --- | --- | --- |
| `GoreeCloud/goreecloud-firefox-extensions` | Missing | Canonical monorepository containing multiple independently identified Firefox extension applications and release boundaries; current v0.2 schema models one `application` or `service` component per manifest. |
| `GoreeCloud/goreecloud-suite` | Missing | Repository owns the public Suite website/application-service directory, but no existing manifest establishes whether the repository itself should be modeled as one `application`, one `service`, or whether the contract needs an explicit portfolio/website model. |

Until that modeling decision is made, these repositories must not be marked `Not Applicable` merely to avoid implementation, and they must not invent local schema extensions that conflict with the central contract.

## Not required by the current v0.2 manifest contract

The following public repositories are currently outside the application/service manifest boundary:

| Repository | Current role | Manifest state |
| --- | --- | --- |
| `GoreeCloud/GoreeCloud` | Central platform governance, schemas, validation, inventory, and implementation reference | Missing / not required |
| `GoreeCloud/goreecloud-autobiography` | Continuously updated autobiography/content repository | Missing / not required |
| `GoreeCloud/goreecloud-branding-assets` | Canonical branding and visual-asset authority | Missing / not required |
| `GoreeCloud/goreecloud-concepts` | Concept/review artifact workspace | Missing / not required |
| `GoreeCloud/goreecloud-glaze-ui` | Shared visual and interaction design system authority | Missing / not required under current application/service-only schema |

This classification is limited to the **current Platform Contract manifest schema**. It does not exempt these repositories from repository governance, security, privacy, documentation, lifecycle truthfulness, source-control, or other applicable GoreeCloud requirements.

## Discrepancies discovered during the audit

The audit found cross-repository statements that conflict with the current central/canonical baseline and should be corrected through repository-specific work rather than silently normalized here:

1. `GoreeCloud/goreecloud-suite` currently states that Glaze UI `2.1.0` is the current Stable design-system target.
2. `GoreeCloud/goreecloud-website` currently states that Glaze UI `2.2.0` is the current GoreeCloud platform target and that its accepted implementation is `2.1.0`.
3. The central Platform Contract and the canonical `GoreeCloud/goreecloud-glaze-ui` repository currently identify Glaze UI `1.1.0` as the current Stable consumer target. This inventory therefore does not treat the Suite or Website version statements as authority for portfolio-wide Platform Contract evaluation.
4. `GoreeCloud/goreecloud-website` also contains an older repository-portfolio statement of `57 repositories — 40 public, 17 private` and describes `GoreeCloud/goreecloud-index` as private. The September 3 canonical repository inventory is `62 — 59 public, 3 private`, and current GitHub metadata identifies `GoreeCloud/goreecloud-index` as public.

These discrepancies are documentation/source-integrity findings. They do not alter the authoritative September 3 repository inventory or upgrade/downgrade application conformance by themselves.

## Required rollout work

The current rollout should proceed without manufacturing positive states:

1. **Completed:** migrate the five legacy v0.1 manifests to v0.2 using current evidence and the governed five-result Platform System vocabulary.
2. Add truthful v0.2 manifests to the **47 confirmed in-scope repositories** that currently lack one, including the 1 private repository without exposing its identity in public central records.
3. Resolve the component-model decision for the **2 scope/model-review repositories** before enforcing v0.2 adoption there.
4. For every new manifest, evaluate all seven Integral Platform Systems and preserve blocked, migration-required, nonconformant, or justified-not-applicable states when that is the supported truth.
5. Add repository CI that calls the central reusable Platform Contract workflow by immutable commit SHA where practical.
6. Do not represent a repository as Stable or Platform-conformant unless required implementation and acceptance evidence independently supports that claim.
7. Correct the identified stale cross-repository Glaze UI and repository-inventory statements through their own authoritative repository workflows.

## Maintenance

Refresh this inventory when:

- the owned repository set changes;
- repository visibility or default branches change;
- a root Platform Contract manifest is added, removed, or migrated;
- the central Platform Contract schema changes;
- a repository's role changes enough to affect contract applicability;
- a scope/model-review decision is resolved; or
- a private/public boundary changes.

When refreshing, re-check the root file on each repository's actual default branch. Do not rely solely on code-search indexing for manifest presence. Preserve private repository identities outside this public central inventory.
