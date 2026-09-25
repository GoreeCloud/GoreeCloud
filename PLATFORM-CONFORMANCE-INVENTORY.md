# GoreeCloud Platform Conformance Inventory

## Status

- **Observed:** September 25, 2026
- **Record type:** Current public Platform Contract adoption and lifecycle-vocabulary diagnostic
- **Central Platform Contract implementation:** `2.0`
- **Central implementation authority:** `GoreeCloud/GoreeCloud` `main` at merge commit `9f44b25d4ff461858c124b687e494edcdf43a226`
- **Public repository registry:** 93 repositories
- **Private repository count:** 4; identities intentionally omitted from this public record
- **Lifecycle authority:** repository/project governance and verified component evidence, not this inventory

This inventory supersedes the September 3–8 historical snapshot as the current operational diagnostic. Git history preserves the earlier snapshot and its dated evidence.

This file is **diagnostic only**. It records what default-branch root manifests declare; it does not translate legacy lifecycle vocabulary, establish implementation completeness, qualify a release, authorize deployment, or promote any component to a Contract 2.0 stage.

## Current audit summary

The September 25 live audit of all **93 registered public repositories** found:

| Measurement | Count |
| --- | ---: |
| Public repositories audited | 93 |
| Root `goreecloud.platform.yaml` present | 46 |
| Root manifest absent | 47 |
| Versioned Platform Contract manifests | 45 |
| Contract 2.0 consumer manifests | 0 |
| Legacy versioned Contract manifests | 45 |
| Legacy non-contract manifests | 1 |

Versioned contract generations currently declared:

| Contract version | Manifests |
| --- | ---: |
| 0.2 | 20 |
| 0.3 | 2 |
| 0.4 | 23 |
| 2.0 | 0 |

Legacy lifecycle strings in the 45 versioned manifests are retained verbatim:

| Declared lifecycle | Manifests |
| --- | ---: |
| `development` | 40 |
| `release-candidate` | 2 |
| `stable` | 1 |
| `concept` | 1 |
| `experimental` | 1 |

`GoreeCloud/goreecloud-network` has a root manifest using the older non-contract `goreecloud.platform/v1` structure and declares `Development`. It therefore requires an explicit contract migration rather than version-string substitution.

An authorized non-public aggregate check found four private repositories: three had Contract 0.4 / `development` root manifests and one had no root manifest. Private repository identities are not centralized here.

## Contract 2.0 migration boundary

The canonical Contract 2.0 lifecycle is:

**Seed → Lab → Forge → Weave → Seal → Anchor → Sunset → Archive**

The audit does not translate older values. Migration must remain evidence-based:

- `concept` normally requires current-state verification before Seed.
- `experimental` normally requires current-state verification before Lab.
- `development` must be evaluated between Forge and Weave.
- `release-candidate` may become Seal only for an exact candidate identity.
- `stable` may become Anchor only when current Anchor qualification remains valid.
- `deprecated` normally maps toward Sunset.
- `retired` may become Archive only after preservation, recovery, migration, and historical-record obligations are complete.

Version identity, deployment state, qualification state, stabilization mode, operational health, temporary flags, and conformance remain separate controls.

## Present public manifests

The table below records each public root manifest observed in this audit. The lifecycle column is the repository's **verbatim legacy declaration**, not a Contract 2.0 reclassification.

| Repository | Contract / format | Declared lifecycle | Component type |
| --- | --- | --- | --- |
| `GoreeCloud/advanced-download-manager` | `0.2` | `development` | application |
| `GoreeCloud/backups` | `0.4` | `development` | application |
| `GoreeCloud/browser` | `0.4` | `development` | application |
| `GoreeCloud/dialer` | `0.4` | `development` | application |
| `GoreeCloud/drive` | `0.2` | `development` | application |
| `GoreeCloud/feeds-server` | `0.4` | `development` | server |
| `GoreeCloud/feeds-web` | `0.4` | `development` | application |
| `GoreeCloud/file-manager` | `0.2` | `development` | application |
| `GoreeCloud/gallery` | `0.4` | `development` | application |
| `GoreeCloud/glaze-ui` | `0.4` | `stable` | shared-library |
| `GoreeCloud/goreecloud-bookmarks` | `0.4` | `development` | application |
| `GoreeCloud/goreecloud-camera` | `0.2` | `concept` | application |
| `GoreeCloud/goreecloud-containers` | `0.2` | `development` | application |
| `GoreeCloud/goreecloud-design-center` | `0.3` | `development` | application |
| `GoreeCloud/goreecloud-dns` | `0.2` | `development` | service |
| `GoreeCloud/goreecloud-gateway` | `0.4` | `development` | service |
| `GoreeCloud/goreecloud-health` | `0.2` | `development` | application |
| `GoreeCloud/goreecloud-identity` | `0.2` | `development` | service |
| `GoreeCloud/goreecloud-maps` | `0.2` | `development` | application |
| `GoreeCloud/goreecloud-memos` | `0.4` | `development` | application |
| `GoreeCloud/goreecloud-network` | `goreecloud.platform/v1` | `Development` | legacy-non-contract |
| `GoreeCloud/goreecloud-photos` | `0.4` | `experimental` | application |
| `GoreeCloud/goreecloud-research-library` | `0.2` | `development` | application |
| `GoreeCloud/goreecloud-router-os` | `0.2` | `development` | service |
| `GoreeCloud/index` | `0.4` | `development` | application |
| `GoreeCloud/keyboard` | `0.4` | `development` | application |
| `GoreeCloud/launcher` | `0.4` | `development` | application |
| `GoreeCloud/location` | `0.2` | `development` | application |
| `GoreeCloud/mail` | `0.4` | `development` | application |
| `GoreeCloud/manager` | `0.4` | `development` | application |
| `GoreeCloud/mesh` | `0.4` | `development` | service |
| `GoreeCloud/messenger` | `0.4` | `development` | application |
| `GoreeCloud/metrics` | `0.2` | `development` | application |
| `GoreeCloud/monitor` | `0.4` | `release-candidate` | application |
| `GoreeCloud/music` | `0.2` | `development` | application |
| `GoreeCloud/notify` | `0.4` | `release-candidate` | application |
| `GoreeCloud/observability` | `0.4` | `development` | service |
| `GoreeCloud/plugin` | `0.2` | `development` | application |
| `GoreeCloud/policy` | `0.4` | `development` | service |
| `GoreeCloud/reader` | `0.2` | `development` | application |
| `GoreeCloud/search` | `0.4` | `development` | service |
| `GoreeCloud/social` | `0.2` | `development` | application |
| `GoreeCloud/sync` | `0.3` | `development` | platform-system |
| `GoreeCloud/tasks` | `0.2` | `development` | application |
| `GoreeCloud/vault` | `0.2` | `development` | service |
| `GoreeCloud/youtube-player` | `0.2` | `development` | application |

## Corrective finding resolved during audit

The audit initially identified `GoreeCloud/backups/goreecloud.platform.yaml` as malformed YAML because several existing Privacy Shield evidence entries were misindented. The repair preserved current Contract 0.4, `development`, version `0.1.0-dev.0`, conformance, evidence, and blocker semantics. It merged through Backups PR #7 to authoritative `main` commit `a08e4557e9159ca57a521175260944947e21f628`; exact-head Rust Foundation #10 and post-merge push Rust Foundation #11 passed, including the new manifest YAML/identity regression gate.

## Missing manifests

Forty-seven public repositories have no root `goreecloud.platform.yaml` at their current default branch. Absence is not automatically a defect or lifecycle judgment: repository purpose and component applicability must be verified before a manifest is required. Where a governed application, service, shared library, server, or other supported component requires Contract participation, initial adoption must use the current Contract 2.0 model rather than creating a new legacy manifest.

## Verification model

The repeatable audit is implemented by `scripts/audit_platform_manifest_portfolio.py` and runs from the central Platform conformance workflow. It:

- reads only repositories in the privacy-bounded public registry;
- checks each authoritative default branch;
- records root-manifest presence and exact manifest blob identity;
- parses both YAML and JSON-shaped manifests;
- distinguishes Contract 0.2, 0.3, 0.4, Contract 2.0, and legacy non-contract formats;
- retains declared lifecycle values verbatim;
- marks migration state without deciding the replacement lifecycle;
- fails closed if a Contract 2.0 manifest itself declares a non-canonical lifecycle value; and
- publishes an exact-head JSON diagnostic artifact.

## Remaining work

1. Reclassify each governed component from verified implementation and release evidence before changing its lifecycle.
2. Migrate repository manifests to Contract 2.0 in controlled component-specific changes.
3. Synchronize each component's project/service lifecycle record, manifest, release records, inventories, and operational views.
4. Reconcile the Drive lifecycle inventories only after the underlying components have been evaluated.
5. Repeat this portfolio audit as migrations land; do not infer progress from repository presence alone.
