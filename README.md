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

GoreeCloud uses shared first-party systems to keep applications cohesive without making them unnecessarily dependent on one another.

| System | Role |
| --- | --- |
| **GoreeCloud Suite** | Integrated user-facing applications and services across the personal-cloud ecosystem. |
| **[Glaze UI](https://github.com/GoreeCloud/glaze-ui)** | Shared design and interaction language, including semantic tokens, reusable interface primitives, accessibility behavior, and conformance guidance. |
| **Wardveil Security by GoreeCloud** | Shared security system and integration framework for applicable controls, hardening, diagnostics, trust boundaries, and evidence-backed security experiences. |
| **GoreeCloud Privacy Shield** | Shared privacy system and privacy-control foundation for privacy-safe defaults, data minimization, diagnostics, and applicable content/tracking protection. |
| **Everkeep** | Resilience, recovery, preservation, portability, continuity, succession, and digital-legacy system. |
| **[GoreeCloud Identity](https://github.com/GoreeCloud/goreecloud-identity)** | Centralized identity, authentication, and single-sign-on platform while application authorization remains appropriately scoped. |

These are functional platform systems rather than decorative labels. Their names and visual identities represent implemented capabilities and governance boundaries.

## Selected public projects

### Platform, administration, and developer tools

- **[GoreeCloud Manager](https://github.com/GoreeCloud/goreecloud-manager)** — native administration and operations console for GoreeCloud.
- **[GoreeCloud Terminal](https://github.com/GoreeCloud/goreecloud-terminal)** — GoreeCloud-maintained Linux terminal experience with controlled fork-to-native evolution.
- **[GoreeCloud Search](https://github.com/GoreeCloud/goreecloud-search)** — privacy-focused, self-hosted search and metasearch gateway.
- **[GoreeCloud Browser](https://github.com/GoreeCloud/goreecloud-browser)** — GoreeCloud-maintained Firefox/Gecko browser distribution and service-integration gateway.

### Storage, synchronization, and knowledge

- **[GoreeCloud Drive](https://github.com/GoreeCloud/goreecloud-drive)** — private multi-user cloud storage and file-management platform.
- **[GoreeCloud Sync](https://github.com/GoreeCloud/goreecloud-sync)** — synchronization, nearby transfer, and secure sharing platform.
- **[GoreeCloud Notes](https://github.com/GoreeCloud/goreecloud-notes)** — self-hosted notes, knowledge management, and personal productivity.
- **[GoreeCloud Memos](https://github.com/GoreeCloud/goreecloud-memos)** — lightweight quick-note and Markdown-native capture experience.
- **[GoreeCloud Bookmarks](https://github.com/GoreeCloud/goreecloud-bookmarks)** — bookmark management, reading, annotation, and web preservation.

### Networking, DNS, security, and recovery

- **[GoreeCloud Network](https://github.com/GoreeCloud/goreecloud-network)** — private networking, encrypted connectivity, enrollment, routing, and access-control platform.
- **[GoreeCloud DNS](https://github.com/GoreeCloud/goreecloud-dns)** — GoreeCloud-controlled DNS filtering and policy platform.
- **[GoreeCloud Backup](https://github.com/GoreeCloud/goreecloud-backup)** — backup, verification, retention, restore, and recovery workflows under GoreeCloud control.
- **[GoreeCloud Vault Server](https://github.com/GoreeCloud/goreecloud-vault-server)** — self-hosted credential and encrypted-vault backend.

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

GoreeCloud software may be:

- original GoreeCloud-owned applications;
- GoreeCloud-maintained open-source forks with controlled fork-to-native evolution; or
- carefully selected open-source components used where maintaining a separate implementation would add unnecessary complexity.

The long-term objective is not to reproduce any commercial cloud ecosystem exactly. GoreeCloud develops or adopts software because it fulfills a verified role while strengthening privacy, ownership, interoperability, portability, maintainability, security, and recoverability.

Project maturity varies by repository. Individual repositories remain the source of truth for their current development, release, packaging, deployment, and acceptance state.

## Public presence

The **[official GoreeCloud website](https://www.goreecloud.com)** is the central public hub for platform information, project discovery, development updates, and official external links.

GitHub is the current public source-control home for GoreeCloud repositories and open-source participation. GoreeCloud's longer-term source-control architecture is designed to preserve independence from any single hosting provider.

Public repositories define their own license, contribution, issue-tracking, and release boundaries where applicable. For the complete current public repository set, use **[Browse public repositories](https://github.com/GoreeCloud?tab=repositories)**.

---

<div align="center">
  <strong>Own the infrastructure. Protect the data. Preserve the future.</strong>
</div>
