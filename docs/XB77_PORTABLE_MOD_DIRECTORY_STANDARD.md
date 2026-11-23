# XB77 canonical portable MOD packaging convention

**Owner-approved convention:** November 22, 2026. Applies to XB77 Red Sun OpenMW portable releases and every compatible XB77 UI, dialogue-accessibility, HUD, character, texture, mesh, script, and ESP mod **packaged for that Red Sun portable installation**.

## Canonical ZIP layout

The root of each installable ZIP must be:

```text
Data/
└── RedSun_OpenMW MODs/
    ├── <Descriptive_Mod_Name>.esp        # if an ESP is required
    ├── Meshes/                            # only if required by this mod
    │   └── ...                           # preserve internal paths in ESP/NIF references
    ├── Textures/                          # only if required
    │   └── ...
    ├── Scripts/                           # only if needed and supported by OpenMW version
    │   └── ...
    └── ...                                # only other engine-required asset folders
```

- Zip entries begin with exactly `Data/RedSun_OpenMW MODs/`; NO `XB77_Portable/` wrapper or nested `XB77_Portable/UserData/data/` inside distributable ZIP files.
- Every ESP/ESM (when needed) lives directly in `Data/RedSun_OpenMW MODs/`, not within `Meshes`, `Textures`, `Scripts` or another nested root.
- Put runtime resources only in appropriate standard OpenMW paths relative to the registered mod folder, and make sure all ESP/NIF/script asset references resolve. Keep correct capitalization, spaces and simple filename conventions.
- Do not include duplicate mod copies, QA documents, backups, CMD/BAT launchers, user profile configs, source projects or unnecessary files in clean runtime ZIPs.
- Empty folders are optional; include only actually used runtime resources. Mods that do not need an ESP must not add a fake empty ESP.
- Treat `Data/RedSun_OpenMW MODs` as the **data-directory root**. OpenMW must register this **exact folder**, which contains ESPs and root asset directories: `data="<absolute_path_to_portable_root>/Data/RedSun_OpenMW MODs"` (Windows path syntax/escaping as appropriate) or via launcher data directory registration. The parent `Data/` is not the data root.
- Register the folder in the **Red Sun portable profile** without changing or hijacking another OpenMW installation's configuration, logs, saves or user data.
- Do not imply simply moving files causes the engine to discover the new folder. Verify the portable launcher/engine data-path is correct and that the active ESP and assets load in a real game before marking a build working.
- For a self-contained **non-Red-Sun** version (such as a standalone Magic Orbis distribution), do not silently change its configured OpenMW installation root; require that target's independently configured data directory or explicitly package a Red Sun-compatible variant with this standard.

## QA acceptance (each new XB77 runtime ZIP)

1. Archive paths match this canonical tree; no legacy `XB77_Portable/UserData/data/` entries.
2. A single intended mod data root exists; ESPs at that root; all referenced meshes/textures/scripts exist with correct case.
3. Red Sun profile points at `Data/RedSun_OpenMW MODs`; no other user's OpenMW paths, saves or logs affected.
4. ESP contents parsed and not mistaken for a working in-game feature merely because records exist.
5. Native OpenMW loading and in-game behavior verified separately from archive and parser tests.
6. Preserve no-modified-landmass constraints for XB77 4K overhaul; include only Morrowind / Tribunal / Bloodmoon relevant character assets.

This is a **packaging and configuration standard**, not evidence that any existing package works or that the assistant has directly changed saved ChatGPT memory. For continuity across chats, use this repository document as the source of truth.
