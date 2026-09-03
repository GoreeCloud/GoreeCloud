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
| Current v0.2 manifest | 1 | 1 | 0 |
| Legacy v0.1 manifest | 5 | 4 | 1 |
| Missing root manifest | 56 | 54 | 2 |
| **Owned repositories** | **62** | **59** | **3** |

Only **1 of 62** owned repositories currently has a root manifest on the current Platform Contract schema.

## Confirmed current-contract application/service scope

Role and repository-manifest evidence identify **55 repositories** as confirmed application or service repositories under the current v0.2 component model: **52 public** and **3 private**.

| Confirmed application/service adoption state | Count |
| --- | ---: |
| Current v0.2 manifest | 1 |
| Legacy v0.1 manifest requiring migration | 5 |
| Missing root manifest | 49 |
| **Confirmed application/service repositories** | **55** |

Accordingly, **54 of 55 confirmed application/service repositories require Platform Contract adoption or migration work**. The sole current-v0.2 repository is not automatically conformant; its current declaration is evaluated separately below.

## Current v0.2 repository

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

## Legacy v0.1 repositories

Four public repositories and one private repository have root manifests using Platform Contract schema `0.1`.

Public legacy manifests:

1. `GoreeCloud/goreecloud-manager`
2. `GoreeCloud/goreecloud-mesh`
3. `GoreeCloud/goreecloud-tasks`
4. `GoreeCloud/goreecloud-website`

Private legacy-manifest identities remain intentionally undisclosed in this public inventory.

Contract v0.2 replaces the v0.1 integration vocabulary and evidence model. These manifests must be migrated conservatively; prior `partial`, `planned`, `unknown`, or unqualified `not-applicable` states must not be upgraded to current positive conformance without current evidence.

`GoreeCloud/goreecloud-website` already declares itself as an `application` in its v0.1 manifest, so it remains in confirmed application scope for migration unless later authoritative repository evidence deliberately changes that component classification.

## Confirmed public application/service repositories missing a manifest

The following **47 public repositories** are confirmed application/service repositories and have no repository-root `goreecloud.platform.yaml` on their verified default branch:

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
20. `GoreeCloud/goreecloud-identity`
21. `GoreeCloud/goreecloud-index`
22. `GoreeCloud/goreecloud-keyboard`
23. `GoreeCloud/goreecloud-launcher`
24. `GoreeCloud/goreecloud-location`
25. `GoreeCloud/goreecloud-mail`
26. `GoreeCloud/goreecloud-maps`
27. `GoreeCloud/goreecloud-memos`
28. `GoreeCloud/goreecloud-messenger`
29. `GoreeCloud/goreecloud-metrics`
30. `GoreeCloud/goreecloud-monitor`
31. `GoreeCloud/goreecloud-music`
32. `GoreeCloud/goreecloud-network`
33. `GoreeCloud/goreecloud-network-android`
34. `GoreeCloud/goreecloud-network-dashboard`
35. `GoreeCloud/goreecloud-notes`
36. `GoreeCloud/goreecloud-notify`
37. `GoreeCloud/goreecloud-photos`
38. `GoreeCloud/goreecloud-quill`
39. `GoreeCloud/goreecloud-redirector`
40. `GoreeCloud/goreecloud-rss`
41. `GoreeCloud/goreecloud-search`
42. `GoreeCloud/goreecloud-source-resync`
43. `GoreeCloud/goreecloud-sync`
44. `GoreeCloud/goreecloud-terminal`
45. `GoreeCloud/goreecloud-vault-server`
46. `GoreeCloud/goreecloud-video`
47. `GoreeCloud/goreecloud-waypoint`

The private scope contributes **2 additional confirmed application/service repositories with missing root manifests**, recorded only as an aggregate to preserve the established public privacy boundary.

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

The audit found cross-repository statements that conflict with the current central/canonical baseline and should be corrected in separate repository-specific work rather than silently normalized here:

1. `GoreeCloud/goreecloud-suite` currently states that Glaze UI `2.1.0` is the current Stable design-system target.
2. `GoreeCloud/goreecloud-website` currently states that Glaze UI `2.2.0` is the current GoreeCloud platform target and that its accepted implementation is `2.1.0`.
3. The central Platform Contract and the canonical `GoreeCloud/goreecloud-glaze-ui` repository currently identify Glaze UI `1.1.0` as the current Stable consumer target. This inventory therefore does not treat the Suite or Website version statements as authority for portfolio-wide Platform Contract evaluation.
4. `GoreeCloud/goreecloud-website` also contains an older repository-portfolio statement of `57 repositories — 40 public, 17 private` and describes `GoreeCloud/goreecloud-index` as private. The September 3 canonical repository inventory is `62 — 59 public, 3 private`, and current GitHub metadata identifies `GoreeCloud/goreecloud-index` as public.

These discrepancies are recorded as documentation/source-integrity findings. They do not alter the authoritative September 3 repository inventory or upgrade/downgrade application conformance by themselves.

## Required rollout work

The current rollout should proceed without manufacturing positive states:

1. Migrate the **5 confirmed in-scope legacy v0.1 manifests** to v0.2 using current evidence and the governed five-result Platform System vocabulary.
2. Add truthful v0.2 manifests to the **49 confirmed in-scope repositories** that currently lack one, including the 2 private repositories without exposing private identities in public central records.
3. Resolve the component-model decision for the **2 scope/model-review repositories** before enforcing v0.2 adoption there.
4. For every new or migrated manifest, evaluate all seven Integral Platform Systems and preserve blocked, migration-required, nonconformant, or justified-not-applicable states when that is the supported truth.
5. Add or update repository CI to call the central reusable Platform Contract workflow by immutable commit SHA where practical.
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
