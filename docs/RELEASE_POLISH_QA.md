# XB77 Red Sun — focused release-polish QA

**Status (2026-11-21): Source work staged; runtime polish not fully tested. No signed public release.**

## Controller A-button prompt

- Requested UI design: light-red, glossy **A** controller prompt with white lettering.
- OpenMW 0.52.0 RC1's `ControllerButtonsOverlay` maps SDL A to `textures/omw_steam_button_a.dds` for Xbox/Steam devices. The MyGUI layout is `resources/vfs/mygui/openmw_controllerbuttons.layout`.
- QA asset replacement uses a custom DXT5 128px icon, with **BtnAImage** image tint white and alpha 1.0. It changes no SDL button mappings or C++ gameplay logic.
- **Limitation:** Steam A shares this same icon source; PlayStation Cross uses a different icon. A future native source refinement can give Xbox A a dedicated texture without affecting Steam.
- Full Windows QA package was assembled from the original working portable ZIP; the engine/launcher/wizard binaries and MyGUI DLL are unchanged byte-for-byte. **Xbox visual test still required.**
- This project must publish the generated icon source artwork and exact source-to-binary mapping before any public binary release.

## Classic Morrowind main menu

- The stock OpenMW menu loads an animated `video/menu_background.bik` if present. XB77 is intended to retain the **original Morrowind static background**, not any mod-supplied video.
- Source-only patch `src/patches/xb77_classic_menu.py` forces the stock `textures/menu_morrowind.dds` fallback. The texture must come from the player's legally owned game assets; it must **not** be redistributed.
- The previously prepared `src/patches/xb77_release_mainmenu.py` adds a decorative Red Sun badge adjacent to New Game, but **has not been compiled and acceptance-tested**.
- Both main-menu source changes require a new OpenMW Windows executable build and gameplay testing. They are **not** part of the resource-only A-button QA package.

## Dialogue readability, transparency

The official OpenMW launcher exposes Interface settings for **GUI Scaling Factor** and **Font Size**. For accessibility testing, compare GUI scale 1.0 against 1.15 at both 1920x1080 and 2560x1440. The Options > Prefs **Menu Transparency** slider can make menu panels more opaque; a value around 0.95 is a reasonable test rather than changing existing player preferences.

Acceptance tests: no clipped menu labels, exactly one yellow focus outline, correct cobalt/grey topic state, native ON/OFF toggle persistence, mouse/controller navigation and focus handoff.

## FOV / presentation testing

The prior QA recording did not prove the occasional FOV-slider flashing/tearing resolved. Test FOV changes with VSync on/off and post-processing on/off, in both windowed and borderless modes; record GPU driver, screen mode, setting and timestamp. Do not claim a source-level FOV fix without a reproducible failure and focused regression test.

## Portable folders and Game Bar

- Native screenshots: `XB77_Portable/UserData/screenshots`
- Local diagnostics: `XB77_Portable/Config/openmw.log`
- User-confirmed Game Bar recording is working in a recent private QA run. Both display modes need an explicit acceptance check.
- Do not distribute player screenshots/logs/saves in a clean public package.

## Release hold

No release while complete modified upstream source, wizard source, redistributable image provenance, source-to-binary public build, unsigned/signed labeling and SignPath upstream eligibility remain unresolved. Maintain the original private development repository independently.
