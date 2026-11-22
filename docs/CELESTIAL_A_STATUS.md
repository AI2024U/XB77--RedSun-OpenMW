# XB77 Celestial A — public feature status

**As of 2026-11-21: UI artwork ready, native engine animation under private QA, not publicly released.**

This public repository contains the reviewable C++ source-transformation script but does **not** claim that a Windows animated build has passed gameplay testing. The separate private development repository, its Git history, logs and user files are intentionally not published here.

## Feature specification

- Xbox A controller prompt: glossy red face, bold white A, silver/blue bezel, celestial rim glow
- Base DDS texture: `omw_steam_button_a.dds`, 256×256, BC3 / DXT5, generated mipmaps
- UI prompt size: 28×28 (was 24×24); opaque white tint
- Animation: 12 RGBA PNG frames, each displayed about 100 ms, for a 1.2-second pulse
- After each completed pulse, random idle delay 3–9 seconds; default icon visible in idle periods
- Starts only while the native A prompt is visible; does not change Xbox D-pad, A activation, other button icons or accessibility focus logic

## What is implemented

- Source patch: `src/patches/xb77_celestial_controller.py` in public source / `ci/xb77_celestial_controller.py` in private development source
- Native integration point: OpenMW 0.52.0 RC1 `apps/openmw/mwgui/controllerbuttonsoverlay.cpp/.hpp`, `onFrame(float)`
- Native animation source changes require compiling `openmw.exe`; dropping PNGs/DDS into the old ZIP **does not enable animation**
- QA assets prepared: `resources/vfs/textures/xb77_celestial_a_00.png` through `xb77_celestial_a_11.png`, and `omw_steam_button_a.dds`
- New verifier: `ci/verify_celestial_assets.py` checks all 12 frame headers, 256px BC3 texture, and the untinted 28px controller layout
- Independent asset QA against the most recent local ZIP passed on 2026-11-21: base texture SHA-256 `5fc8fb259e367942a8609dbb1446f6aa361878181807aa9bd4fa70570bb0ab88`
- The existing ZIP is **STATIC** despite containing animation frames. Do not describe it as animation-enabled

## Verification before publishing any animation build

1. Build the modified engine from reviewable source and verify it contains all native frame paths.
2. Ensure the same install contains all 12 PNG frames, base DDS texture, and reviewed MyGUI controller layout.
3. Run `python ci/verify_celestial_assets.py "XB77 Red Sun OpenMW.zip"` against the newly packaged ZIP.
4. Preserve working portable configuration, menu controls, Xbox D-pad/A focus, screenshots, Game Bar capture and high-contrast dialogue toggle.
5. Test A prompt for at least 15–20 seconds each in inventory, main menu, and NPC dialogue, watching for subtle periodic glow rather than flashing.
6. Test on Windows in windowed and borderless fullscreen, including lower resolutions; verify icons are crisp and other controller buttons unchanged.
7. Record actual source revision, compiled executable hash, QA result and instructions before a public download.

## Known release blockers

- Windows native engine animation has **not yet been acceptance-tested**.
- Current public repository does not contain all corresponding original engine/wizard source, build chain and image assets needed for a complete independently reproducible binary release.
- SignPath Foundation signing eligibility for modified upstream OpenMW binaries remains unresolved. No signed release is claimed.
- Do not upload real user settings, save files, logs, recordings, screenshots or development archives to the public repository.


## User-facing release note

The currently distributed test texture package is an improved **static** A button. A true timed glow will only appear after a newly compiled OpenMW engine has been integrated and checked against the complete asset set. Avoid claims of a live 3–9-second glow for older test ZIPs.

## Native compilation and private QA integration — November 21, 2026

The OpenMW 0.52.0 RC1 native controller-overlay animation compiled successfully, and the intended 12 frame names were detected in the Windows engine binary. The new engine and matching MyGUI DLL were integrated into a separate **private test ZIP** with the existing isolated launcher, wizard, settings and animation resources preserved.

This is **not an officially published executable release**. We have not yet verified the 3–9-second glow timing on Windows or completed full source/reproducibility, rights-clearance and SignPath release gates. The public repository continues to host source patches and documentation only, not the private QA binaries, logs, screenshots, or installation profile.

Expected reviewable source: `src/patches/xb77_celestial_controller.py` and `ci/verify_celestial_assets.py`.

## Archive-level QA findings — 2026-11-21

A private, compiled, unsigned Celestial A Windows ZIP passed a static package verification audit: controller layout and high-contrast skins were included, all 12 animation PNGs matched compiled frame references, Windows GUI EXEs and DLL dependencies were present, and user-data folders remained separate.

The audit also found that the compiled engine referenced a small Red Sun New Game badge whose resource was omitted from the previous QA ZIP. This missing image was restored using existing XB77 artwork. A subsequent integrity check passed. No test artifacts or binaries were published to this public repository.

**This is not proof of runtime feature correctness.** The 3–9-second glow still needs Windows gameplay confirmation. Source-only fixes for subtitle/Options overlap and forcing the original static menu background are not included in this compiled QA engine; FOV flashing/tearing and SignPath/legal release requirements remain open.
