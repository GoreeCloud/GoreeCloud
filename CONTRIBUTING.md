# Contributing to GoreeCloud

GoreeCloud is a personal, noncommercial hobby and learning ecosystem maintained at the founder's discretion. Suggestions and focused fixes are welcome; there is no commitment to review timelines, feature acceptance, support levels, or release schedules.

## Scope

This repository introduces the ecosystem and documents its guiding principles. Individual applications and services are developed in their own repositories under [GoreeCloud](https://github.com/GoreeCloud). Report a product-specific bug or propose a code change in the corresponding product repository whenever possible.

## Propose a change

1. Check existing issues and pull requests to avoid duplicate work.
2. For a material change, open a narrowly scoped issue first or describe the rationale clearly in the pull request.
3. Keep the founder's original intent, personal/noncommercial framing, and the distinct responsibilities of GoreeShield, Wardveil, GoreeCloud Mesh, and GoreeCloud UI intact.
4. Do not add private infrastructure details, credentials, personal or family data, unverified product claims, or third-party content without a compatible license and required attribution.
5. Run `python3 tools/check_docs.py` and `python3 -m unittest discover -s tests -v` before proposing documentation or checker changes.
6. State what changed, what you tested, and what remains unverified. Submissions may be declined or revised to preserve the project's scope and maintainability.

## Security

Do not report exploitable security details, credentials, private infrastructure addresses, or personal information in public issues or pull requests. Consult [SECURITY.md](SECURITY.md) for responsible disclosure guidance.

## Licensing

Original material in this repository is licensed under the [MIT License](LICENSE). By contributing material, you affirm that you have the rights to provide it under that license and that required third-party attributions are preserved. Other GoreeCloud repositories may have different licenses; check each one individually.
