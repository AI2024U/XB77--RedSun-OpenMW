# Code signing policy

**Status: proposed policy for SignPath Foundation review. No SignPath subscription, signing key, or code signing certificate has been approved or issued for this project.**

If the SignPath Foundation application is approved, the project will state:
> Free code signing provided by SignPath.io, certificate by SignPath Foundation.

This statement is **conditional**. It must not be presented as an existing endorsement until approval.

## Scope

Only exact, publicly reviewable releases built from this repository and publicly corresponding OpenMW sources are eligible for a signing request. Intended signed executables (if upstream-derived binary conditions permit): `openmw.exe`, `openmw-launcher.exe`, and `openmw-wizard.exe`. Their status is **not yet eligible/verified**.

## Roles

- **Source maintainer and committer:** GitHub account [AI2024U](https://github.com/AI2024U).
- **Reviewer:** AI2024U for outside pull requests; another trusted reviewer should review security-sensitive changes whenever possible.
- **Signing approver:** AI2024U, subject to eligibility and approval; each release requires explicit manual signing approval.
- A real person controlling the maintainer account must confirm role assignments and enable GitHub/SignPath multi-factor authentication before any signing use.

## Build controls

1. Every release must be built by the public CI workflow from a tagged, reviewable source revision, with no private repository credentials or unreviewed artifacts.
2. Do not use prebuilt modified OpenMW executables from the private development repository as source for a signing request.
3. Record upstream source tag and commit, XB77 patch source revision, dependency versions, the workflow run ID, and SHA-256 checksums.
4. Test the unmodified output, verify executable metadata (product name and version), and submit **only** reviewed release artifacts for signing.
5. Publish signed artifacts only after checking certificate chain, signature, timestamp, version, source correlation and hash. Never alter an EXE after signing.
6. Each version requires manual approval; third-party pull requests require review before merging.

## Privacy and vulnerability reporting

See [Privacy policy](PRIVACY.md) and [Security policy](SECURITY.md). Installation must not silently alter unrelated OpenMW profiles. Public reports must exclude personal logs or locations.

## Upstream-derived executable restriction

SignPath Foundation requires a visible fork of upstream, upstream signed releases, and signing release branches derived from upstream's normally signed branches for modified upstream binaries. **These have NOT been demonstrated.** Signing `openmw.exe` or `openmw-launcher.exe` under SignPath Foundation's certificate may not be allowed; approval must be sought directly.

SignPath terms: https://signpath.org/terms
