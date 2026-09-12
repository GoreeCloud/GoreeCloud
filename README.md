<div align="center">
  <!-- Canonical branding source: GoreeCloud/goreecloud-branding-assets/official/goreecloud-logo.svg -->
  <img src="./assets/goreecloud-logo.svg" alt="GoreeCloud" width="160">

# GoreeCloud

**Privacy-first, self-hosted software for personal cloud infrastructure, productivity, knowledge management, security, communication, and digital preservation.**

[Official website](https://www.goreecloud.com) · [Browse public repositories](https://github.com/GoreeCloud?tab=repositories)
</div>

## About GoreeCloud

GoreeCloud is a privacy-first, self-hosted family cloud and digital legacy platform built to preserve a family's digital life across generations.

It provides a secure, resilient, and independently controlled foundation for protecting memories, knowledge, records, communications, credentials, applications, and personal data. The goal is to keep that information **accessible, recoverable, portable, understandable, and transferable** without depending entirely on commercial cloud providers or proprietary ecosystems.

GoreeCloud is more than a homelab or a collection of self-hosted applications. It is an evolving personal-cloud platform with documented architecture, governance, software, security, privacy, recovery, and long-term continuity practices.

## Core principles

| Principle | What it means |
| --- | --- |
| **Data ownership** | Keep control of personal, family, and operational information. |
| **Privacy** | Minimize unnecessary collection, telemetry, tracking, and external exposure. |
| **Long-term preservation** | Protect memories, records, knowledge, and digital history beyond the life of any one device or service. |
| **Recoverability** | Design systems so important information and services can be restored after failure. |
| **Technology independence** | Keep applications, data, and infrastructure portable enough to replace vendors, software, or hardware when needed. |

## Platform systems

GoreeCloud uses exactly eight Integral Platform Systems to keep applications and services cohesive without making them unnecessarily dependent on one another. **GoreeCloud Suite** is the integrated user-facing product experience built across the ecosystem; it is distinct from the eight functional platform systems below.

| Integral Platform System | Role |
| --- | --- |
| **[GoreeCloud Manager](https://github.com/GoreeCloud/goreecloud-manager)** | Bounded platform management and administration, including application and service inventory, configuration, lifecycle, operational visibility, governance implementation, and authorized control-plane workflows. |
| **[GoreeCloud Privacy Shield](https://github.com/GoreeCloud/goreecloud-privacy-shield)** | Shared privacy authorization and privacy-control foundation for consent, purpose limitation, minimization, retention, sharing, processing boundaries, privacy-safe diagnostics, and applicable content/tracking protection. |
| **[Wardveil Security](https://github.com/GoreeCloud/goreecloud-wardveil)** | Shared security system and integration framework for applicable protection, hardening, diagnostics, trust boundaries, verification, response, and evidence-backed security experiences. |
| **[Everkeep](https://github.com/GoreeCloud/goreecloud-everkeep)** | Resilience, recovery, preservation, portability, continuity, succession, and digital-legacy system. |
| **[Glaze UI](https://github.com/GoreeCloud/goreecloud-glaze-ui)** | Shared design and interaction language, including semantic tokens, reusable interface primitives, accessibility behavior, responsive behavior, and conformance guidance. |
| **[GoreeCloud Mesh](https://github.com/GoreeCloud/goreecloud-mesh)** | Private connectivity, capability discovery, coordination, dependency/event relationships, governance, and service interoperability where applicable. |
| **[GoreeCloud Identity](https://github.com/GoreeCloud/goreecloud-identity)** | Central identity, account, device, application, service, credential, session, authentication, authorization, and delegated-authority foundation while application-specific authorization remains appropriately scoped. |
| **[GoreeCloud Sync](https://github.com/GoreeCloud/goreecloud-sync)** | Authorized synchronization, change tracking, state coordination, version reconciliation, conflict handling, offline continuity, and cross-device continuity. |

These are functional platform systems rather than decorative labels. Application and service repositories must represent required integrations through real behavior, contracts, authority boundaries, validation, and user-visible state where applicable. A project that has not completed required integration and acceptance must not be presented as Stable or production-ready merely because it builds successfully.

All eight are mandatory GoreeCloud foundations and are required to progress to complete, production-grade implementation of their approved responsibilities. This requirement does not override evidence-based status: a Platform System may remain Development, migration-required, blocked, or production-unaccepted until its own implementation and acceptance evidence proves completion.

The versioned **GoreeCloud Platform Contract** provides a machine-readable declaration and validation foundation for these relationships through repository-root `goreecloud.platform.yaml` manifests. Platform Contract `0.3` requires explicit evaluation of all eight systems. A valid manifest records declared state and evidence references; it does not independently prove that an integration is implemented, accepted, production-ready, or Stable. See [`PLATFORM-CONTRACT.md`](./PLATFORM-CONTRACT.md) for the current repository-local implementation reference.

### Important platform boundaries

- GoreeCloud Identity establishes actor identity and authority.
- Privacy Shield governs permitted information use.
- Wardveil Security governs trust, protection, and security response.
- GoreeCloud Manager provides bounded administration and operational control.
- GoreeCloud Mesh provides private reachability, discovery, coordination, and event/service interoperability.
- GoreeCloud Sync understands authorized application state, coordinates changes and versions, reconciles conflicts, and resumes synchronization after interruption.
- Everkeep preserves recoverable historical state and continuity; synchronization is not backup.
- Glaze UI presents accurate, accessible interfaces and state without manufacturing underlying capabilities.

## Selected public projects

### Platform, administration, and developer tools

- **[GoreeCloud Manager](https://github.com/GoreeCloud/goreecloud-manager)** — native administration and operations console for GoreeCloud.
- **[GoreeCloud Terminal](https://github.com/GoreeCloud/goreecloud-terminal)** — GoreeCloud-maintained Linux terminal experience with controlled fork-to-native evolution.
- **[GoreeCloud Search](https://github.com/GoreeCloud/goreecloud-search)** — privacy-focused, self-hosted search and metasearch gateway.
- **[GoreeCloud Browser](https://github.com/GoreeCloud/goreecloud-browser)** — GoreeCloud-maintained browser project with a controlled migration path toward the native GoreeCloud application model.

### Storage, synchronization, and knowledge

- **[GoreeCloud Drive](https://github.com/GoreeCloud/goreecloud-drive)** — private multi-user cloud storage and file-management platform.
- **[GoreeCloud Sync](https://github.com/GoreeCloud/goreecloud-sync)** — synchronization, nearby transfer, and secure sharing platform and the adopted synchronization Integral Platform System.
- **[GoreeCloud Notes](https://github.com/GoreeCloud/goreecloud-notes)** — self-hosted notes, knowledge management, and personal productivity.
- **[GoreeCloud Memos](https://github.com/GoreeCloud/goreecloud-memos)** — lightweight quick-note and Markdown-native capture experience.
- **[GoreeCloud Bookmarks](https://github.com/GoreeCloud/goreecloud-bookmarks)** — bookmark management, reading, annotation, and web preservation.

### Networking, DNS, security, and recovery

- **[GoreeCloud Network](https://github.com/GoreeCloud/goreecloud-network)** — private networking, encrypted connectivity, enrollment, routing, and access-control platform.
- **[GoreeCloud DNS](https://github.com/GoreeCloud/goreecloud-dns)** — GoreeCloud-controlled DNS filtering and policy platform.
- **[GoreeCloud Backup](https://github.com/GoreeCloud/goreecloud-backup)** — backup, verification, retention, restore, and recovery workflows under GoreeCloud control.
- **[GoreeCloud Vault](https://github.com/GoreeCloud/goreecloud-vault)** — self-hosted credential, passkey, secret, recovery-information, secure-note, and encrypted-vault platform.

### Photos, media, and personal experiences

- **[GoreeCloud Photos](https://github.com/GoreeCloud/goreecloud-photos)** — private multi-user photo and video backup, organization, search, and sharing platform.
- **[GoreeCloud Music](https://github.com/GoreeCloud/goreecloud-music)** — original multi-user self-hosted music service and application.
- **[GoreeCloud Video](https://github.com/GoreeCloud/goreecloud-video)** — private multi-user video library, playback, transcoding, and client platform.
- **[GoreeCloud Gallery](https://github.com/GoreeCloud/goreecloud-gallery)** — offline-first Android gallery for device-local photos and media.
- **[GoreeCloud Launcher](https://github.com/GoreeCloud/goreecloud-launcher)** — privacy-first Android home-screen launcher with a first-party theme engine.
- **[GoreeCloud Keyboard](https://github.com/GoreeCloud/goreecloud-keyboard)** — private Android input method with swipe typing, dictionaries, clipboard tools, and GoreeCloud workflows.
- **[GoreeCloud Location](https://github.com/GoreeCloud/goreecloud-location)** — privacy-first multi-user location and tracking platform.

### Planning, information, and service operations

- **[GoreeCloud Calendar](https://github.com/GoreeCloud/goreecloud-calendar)** — GoreeCloud-controlled calendar experience built around standards-based calendar data.
- **[GoreeCloud Feed](https://github.com/GoreeCloud/goreecloud-rss)** — private multi-user RSS experience for web, Linux desktop, and Android.
- **[GoreeCloud Monitor](https://github.com/GoreeCloud/goreecloud-monitor)** — availability, endpoint, heartbeat, certificate, incident, and recovery monitoring.

### Browser integrations and utilities

- **[GoreeCloud Bookmark Browser Extension](https://github.com/GoreeCloud/goreecloud-bookmark-browser-extension)** — browser integration for saving content to GoreeCloud Bookmarks.
- **[GoreeCloud Redirector](https://github.com/GoreeCloud/goreecloud-redirector)** — privacy-first Firefox extension for redirecting selected external-service URLs toward GoreeCloud-controlled alternatives.
- **[GoreeCloud Source Resync](https://github.com/GoreeCloud/goreecloud-source-resync)** — Firefox extension supporting the GoreeCloud ChatGPT Project Sources resynchronization workflow.

## Project status and source of truth

GoreeCloud repositories exist at different lifecycle states. Some projects are active development work, some are release candidates or transitional replacements, and some have accepted Stable releases.

A project's own repository, release records, project specification, and acceptance evidence remain authoritative for its current implementation, packaging, deployment, and lifecycle state. **Being listed on this profile does not by itself mean a project is released, deployed to production, or Stable.**

Branding is governed separately: **`GoreeCloud/goreecloud-branding-assets` is the canonical source for GoreeCloud logos, icons, artwork, wordmarks, and approved brand derivatives.** Product-local artwork is a synchronized packaging or presentation derivative, not an independent branding source of truth.

## Development approach

GoreeCloud applications and services are developed toward an original, native, GoreeCloud-owned destination.

- New application implementations are built from the ground up under GoreeCloud ownership.
- Existing complete-product forks or adopted implementations may remain temporarily for migration, compatibility, testing, reference, or historical purposes while native replacements are built and accepted.
- Narrow critical foundations may remain dependencies when independent reimplementation would materially increase security, cryptographic, protocol, standards, codec, rendering, operating-system, runtime, interoperability, or maintainability risk.
- Required GoreeCloud Manager, Privacy Shield, Wardveil Security, Everkeep, Glaze UI, GoreeCloud Mesh, GoreeCloud Identity, and GoreeCloud Sync integrations remain functional acceptance requirements rather than branding claims.

The long-term objective is not to reproduce any commercial cloud ecosystem exactly. GoreeCloud builds software around verified roles while strengthening privacy, ownership, interoperability, portability, maintainability, security, recoverability, synchronization, and long-term independence.

Project maturity varies by repository. Individual repositories and canonical GoreeCloud project records remain the source of truth for current development, release, packaging, deployment, integration evidence, and acceptance state.

## Public presence

The **[official GoreeCloud website](https://www.goreecloud.com)** is the central public hub for platform information, project discovery, development updates, and official external links.

GitHub is the current public source-control home for GoreeCloud repositories and open-source participation. GoreeCloud's longer-term source-control architecture is designed to preserve independence from any single hosting provider.

Public repositories define their own license, contribution, issue-tracking, and release boundaries where applicable. For the complete current public repository set, use **[Browse public repositories](https://github.com/GoreeCloud?tab=repositories)**.

---

<div align="center">
  <strong>Own the infrastructure. Protect the data. Preserve the future.</strong>
</div>
