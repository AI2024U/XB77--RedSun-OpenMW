# Building XB77 Red Sun OpenMW

**This repository is currently source-preparation only. A full public build cannot yet be reproduced from the published files; do not claim that the private Test 09 binaries were compiled from this public repository.**

## Engine target

OpenMW 0.52.0 RC1 tag: `openmw-52-rc1` (https://gitlab.com/OpenMW/openmw/-/tags).

The original development build uses MSVC / CMake / Qt 6 / bundled MyGUI and a multi-stage Python patch process. Review scripts in `src/patches/`.

## Missing public-build prerequisites

- Complete audited original C++/MyGUI patch base (formerly private source archive).
- Full source for the first-time setup wizard and a replacement background graphic with explicit redistribution rights.
- Sanitized, verified Windows Actions workflow that builds **only** from this public repository and pinned upstream dependencies.
- Verification that all third-party binaries and fonts have required notices.
- An independent Windows fresh-install test and generated source-to-binary provenance.

Once these requirements pass, a public workflow can assemble OpenMW and XB77 modifications, generate three Windows binaries, run checks, create a runtime ZIP and a complete GPL source ZIP. Signing must be a separate, manually approved step.

**Do not copy development ZIPs or logs into public Git history.**
