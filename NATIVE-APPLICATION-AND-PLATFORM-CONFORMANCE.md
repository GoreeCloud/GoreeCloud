# Native Application and Platform Conformance

Effective August 24, 2026.

All GoreeCloud applications must be original GoreeCloud software built natively from the ground up. Narrow exceptions are permitted only for critical supporting necessities such as WireGuard, established cryptographic/encryption primitives, standards/protocol libraries, platform interfaces, database engines, codecs, and comparable foundational dependencies where reimplementation would reduce security, interoperability, reliability, or maintainability.

Complete third-party applications, forks, rebrands, patched upstream products, and other inherited end-user application implementations are not acceptable as the long-term GoreeCloud application architecture. They may be retained only as bounded transitional sources for migration, compatibility, validation, testing, service continuity, provenance, or historical reference while an original GoreeCloud-owned implementation replaces them. New product behavior must advance the first-party implementation rather than expanding the inherited application architecture unless a narrowly documented migration need requires otherwise.

Every GoreeCloud application must implement and remain current with all four integral platform systems:

- Glaze UI
- Wardveil Security
- Privacy Shield
- Everkeep

These are functional platform requirements, not optional branding. An application or service cannot qualify as Stable when any required integration is missing, outdated, incompatible, placeholder-only, cosmetic-only, unvalidated, or superseded by a newer required contract.

Repository documentation and public product descriptions must distinguish implemented source, validated integration, deployment, release acceptance, and Stable qualification. A planned capability, transitional upstream behavior, passing unit test, or source-only integration must not be described as a production or Stable capability without the corresponding evidence.

Existing application repositories and development plans must transition to this native-first model and must keep compatibility, validation, migration, and release evidence current as the four shared platform systems evolve. Each application or service must maintain its canonical project specification under `GoreeCloud/Projects`, and GoreeCloud changelog records must remain in the canonical `GoreeCloud/Changelogs` scope.
