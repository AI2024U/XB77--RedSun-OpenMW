# XB77 Red Sun — Jiub Test 11 Clean Compatibility Recovery

**Date:** 2026-11-22. **Status:** Offline package checks passed; native OpenMW Test11 in-game result pending.

## Trigger and limitation

User reported **Test10 "didn't work"** but provided no new Test10 video or current `openmw.log`. That prevents a reliable diagnosis of the exact in-game Test10 failure. Test10's aggressive subdivision enlarged the head from 293 to 4,259 vertices, and hair to 6,112 triangles, but those meshes passed only offline structural QA, **not** an OpenMW render acceptance.

## What was actually changed

Created a new private, reversible recovery ZIP:

`XB77_RedSun_4K_Jiub_Test11_Clean_Compatibility_Private.zip`

SHA256: `386302000d0ecbaded23c42665c44e4bbfd12b7cd75664b01e4e273d9f911c7e`  
Size: 6,886,059 bytes (ZIP)

**Exact runtime layout:** `XB77_Portable/UserData/data/` in the user's Red Sun portable engine root, previously confirmed by the user's Test09 loading footage and historical OpenMW log.

Contains five runtime files:
- `XB77_RedSun_4K_Jiub_Test11.esp` (TES3 + 2 BODY records + 1 NPC Jiub override).
- `Meshes/b/XB77_Jiub_Head_11.nif` (exact 24,109-byte original-topology NIF data from successfully rendered Test09; only the unique DDS filename reference changed).
- `Meshes/b/XB77_Jiub_Hair_11.nif` (exact 9,569-byte original-topology NIF data from successfully rendered Test09; only the unique DDS filename reference changed).
- `Textures/tx_xb77_jiub_face_011.dds` (original-color, 4096×2048 face diffuse from Test10; explicitly no teal or XB77 stamp).
- `Textures/tx_xb77_jiub_hair_000011.dds` (4096×4096 original-color hair diffuse from Test10).

The ESP's BODY IDs and model paths use Test11-specific identifiers, and its NPC ID stays `chargen name`. Its other NPC gameplay fields are bytewise retained from Test09 (apart from the two appearance references). Original game files are not overwritten. No engines, BA(T/CMD) scripts, ESMs or BSAs included.

## Verification

Local build script completed **27 structural checks**, including:
- Real TES3 ESP parsing and record types `TES3`, `BODY`, `BODY`, `NPC_` (no `LAND` or `LTEX`).
- Referential checks ESP→two NIFs→two DDS files.
- NIF source geometry and morph-controller data are **bytewise identical to in-game-confirmed Test09 originals except for unique diffuse path strings**; no experimental Test10 geometry remains.
- Both 4K DDS images reopen correctly; face color statistics differ from Test09's teal test, consistent with natural grayscale/ash skin.
- ZIP CRC passed; no previous Test09/Test10 runtime paths, duplicate root paths, terrain/landmass files, personal directories, original BSAs/ESMs, executables, logs, or cmd/bat files.
- Fresh plugin and asset file names permit safe side-by-side testing; old ESPs must be unchecked.

**This is a stability-oriented recovery, NOT a high-poly fix.** Jiub still has original polygon counts and visible vanilla seams; 4K-sized diffuse generated from low-res original art also does not equal newly painted true 4K detail.

## Important next step

The user must test Test11 using Red Sun OpenMW 0.52 RC1 before any native-compatibility claim. If it fails, collect **new** `openmw.log`, the active content/config file, and/or video from the *Test11 run* so the failure can be identified rather than guessing. Do not touch landmass assets or Red Sun config. Later, develop independently authored high-quality character geometry with properly checked NIF morphs and head/body seam continuity.

Source-derived NIF/DDS files were used from the user's private original game assets, and remain **private**. Only this text QA report is public GitHub content. Hourly 4K automation stays paused as requested.
