# XB77 Red Sun OpenMW

**Public source and release-preparation repository** for an independent, accessibility-focused modification of the [OpenMW](https://openmw.org/) engine for *The Elder Scrolls III: Morrowind*.

**Status (2026-11-21): release preparation; NOT a verified, signed public executable release.**

**ACTIVE RELEASE BLOCKER (2026-11-21):** Direct double-click launches of the experimental OpenMW executable/launcher have been reported to produce a rendering problem despite successful tests through the isolated development launcher. A native GUI portable-entrypoint repair is undergoing Windows testing. **Do not redistribute or endorse a test ZIP as a finished public build.** Do not confuse this repository with an official OpenMW release. XB77 is not affiliated with or endorsed by the OpenMW team, Bethesda, or Microsoft.

## What XB77 changes

- A thin yellow outline, yellow selection text and arrow to make the currently focused NPC topic more visible.
- Cobalt-blue available dialogue topics and grey exhausted/read topics.
- Native **Options → Prefs → XB77: High-Contrast Dialogue Selection** ON/OFF toggle.
- Keyboard, mouse and Xbox controller menu support using the underlying OpenMW interface.
- Standalone Windows x64 portable configuration and first-time installation wizard in the tested candidate.
- Optional Celestial A visual polish: upgraded blue-silver Xbox A prompt; **timed 3–9s animation is source-prepared but not verified in a native public build**.

## Requirements

A legally obtained Morrowind installation with **Morrowind.esm** and **Morrowind.bsa** is required. This project does **not** distribute Morrowind game data, its commercial assets, or the original Morrowind executable.

The tested development build targets **OpenMW 0.52.0 RC1**, not the latest OpenMW master branch. Windows 64-bit is the intended platform.

## Public release status

There is **no completed signed release in this repository yet**. Gameplay has been tested during development, but the existing test ZIP has not passed the full public-source, asset-rights, and independent first-run audit. Do not upload a development ZIP to the public release tab as a final build.

See the [Celestial A implementation status](docs/CELESTIAL_A_STATUS.md), [release readiness](docs/RELEASE_CHECKLIST.md), [source provenance](docs/SOURCE_PROVENANCE.md), and [build instructions](docs/BUILDING.md).

## Privacy, security and trust

- This is a **new public repository**; it contains no imported private development Git history.
- Do not upload player logs, save files, diagnostics, screenshots containing private data, private keys, personal paths, or third-party copyrighted assets.
- Review [Privacy policy](PRIVACY.md), [Security policy](SECURITY.md), and [Code signing policy](CODE_SIGNING_POLICY.md).
- **No SignPath approval or certificate is claimed.** A certificate would not guarantee that Windows SmartScreen will never show a warning.

## License and upstream

OpenMW and the derived XB77 engine changes are distributed under the **GNU GPLv3** subject to applicable third-party notices. See [LICENSE](LICENSE) and [licensing and attribution](docs/LICENSES.md). The public source and exact build for any redistributed executable must accompany that release; an upstream link alone is not a substitute for the corresponding source of our modifications.

Upstream source: [OpenMW/openmw](https://gitlab.com/OpenMW/openmw). XB77 uses an independent source-patch workflow today, **not a GitHub fork recognized by SignPath's modified-upstream rules**. SignPath eligibility is unresolved; see [SignPath prerequisites](docs/SIGNPATH_ELIGIBILITY.md).

## Maintainer and contributions

Maintained through GitHub account [AI2024U](https://github.com/AI2024U). See [CONTRIBUTING.md](CONTRIBUTING.md). Do not post private personal information in issues.
