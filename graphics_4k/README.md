# XB77 Red Sun 4K Overhaul — Development Foundation

**Status: initial audit tooling only. Not a graphics mod and not a playable release.**

## Approved scope

Only Bethesda's original **Morrowind**, **Tribunal**, and **Bloodmoon** assets. No other world mods or unrelated asset packs. Red Sun OpenMW's portable Windows accessibility experience should remain intact.

The intended finished ZIP will include one ESP, plus separate replacement textures and NIF meshes under a single new OpenMW data directory. **Selecting an ESP in OpenMW's launcher is not sufficient to disable loose-file replacements**: the separate XB77 data directory also must be disabled or removed to fully roll back the overhaul. Original game files must never be overwritten.

## Current engineering milestone

- Isolated source-development branch and read-only asset audit script.
- Scans three game ESMs and three game BSAs for presence without extracting or copying them.
- Lists replacement textures and detects PNG, DDS, TGA, BMP dimensions, with JPEG via optional Pillow.
- Detects NIF file signature, filename conflicts and ESP's expected TES3 header signature.
- Does **not** claim valid ESP records, genuine high-polygon meshes, accurate normal maps, UV continuity, licenses, complete coverage, or playable game integration. The report always marks release as not ready.

## Audit command (on user's machine, when real assets exist)

```
python tools/xb77_4k_audit.py --game-data "C:/Games/Morrowind/Data Files" --mod-data "C:/Games/OpenMWMods/XB77_RedSun_4K_Overhaul" --report "XB77_4K_Audit.json"
```

The paths above are examples, not knowledge of the user's Windows installation. Audit reports should remain local; do not commit local paths or copyrighted game data.

## Pending pipeline

1. Inventory and legally clear assets for only the three official game content files, including female and male variants of all playable races.
2. Set per-category performance and texture-resolution budgets. 4096-by-4096 should be used only where appropriate; low-detail upscaling alone is not genuine 4K restoration.
3. Produce high-detail mesh topology with proper UVs, normals, correct NIF format and rigging.
4. Integrate texture seams and high-poly characters; systematically validate neck, wrists, ankles, hands, face meshes, armor and animations for all 10 playable races.
5. Build a clean TES3 ESP with real records, only where record changes are needed; otherwise don't pretend the ESP controls loose files.
6. Validate original engine and Red Sun launcher behavior on Windows, and create the final mod folder ZIP only after human visual and legal QA.

## Zero-redistribution rule

Never commit or package Bethesda's original BSA/ESM files, extracted original textures, models, copyrighted third-party mod assets without permission, or user-specific logs. A legitimate Morrowind installation is required for use.