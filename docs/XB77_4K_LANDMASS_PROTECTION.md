# XB77 4K Overhaul — Landmass Exclusion Gate (2026-11-22)

**Scope:** Morrowind, Tribunal, and Bloodmoon only. This is experimental graphics-development work, not a playable release. The original terrain, ground, landscape and landmass textures and meshes must not be modified or distributed.

## Verified local baseline
- All three user-provided ESMs and BSAs were inventoried read-only; archive files and game assets are NOT committed here.
- Total effective original game asset paths: 13,734, including 6,245 texture paths and 7,319 mesh paths.
- Original ESMs include 159 LTEX records: Morrowind 107, Tribunal 13, Bloodmoon 39; 134 unique ground texture filename stems.
- The new Test 02 landmass gate identifies 132 exact input texture path matches to LTEX references even when master references TGA and BSA contains DDS.
- Conservative staging classifications: 3,580 character/equipment-prefix *candidates* (not finished); 2,029 blocked paths (including 1,470 other asset-folder exclusions and 427 terrain-named paths); 8,125 unclassified paths requiring manual review.
- Local automated tests: 14 passing, including 8 new terrain-protection tests. A proposed ESP with LAND or LTEX records is explicitly rejected. The absent real ESP and zero replacement assets correctly fail release readiness.
- No completed replacement 4K textures or high-poly models have been verified.

## Required staging rules
1. Protect all LTEX DATA-referenced texture base names across DDS, TGA, PNG and other supported extensions; reject loose replacements whose names match.
2. Reject texture/mesh paths indicating terrain, landscape, landmass, ground, grass, snow, dirt, road, ashland, mud, or other ground materials.
3. Fail closed on unknown or unapproved paths; do not silently assume a generic texture is a non-landscape asset.
4. Reject ESP files containing LAND or LTEX records, malformed TES3 records, unexpected BSA/ESM files, symlinks, unsafe ZIP paths, percent symbols and unverified output files.
5. Use the original source assets only for private read-only inventory, and never upload BSA/ESM, copied original art, or user logs into GitHub or a redistributable ZIP.
6. The artwork quality gates (actual 4K detail, genuine high-poly replacements, all 10 race seams, skin matching, UVs, normals, equipment fitting, animation tests, Windows OpenMW in-game checks) remain separate and still **pending**.

## Next engineering task
Port the locally tested `tools/xb77_landmass_gate.py` and `tests/test_xb77_landmass_gate.py` from Test 02 into the dedicated `xb77-4k-overhaul-dev` branch, verify against synthetic fixtures on CI, and establish approved replacement asset provenance. Do not use paid Windows compilation on a mere metadata/audit milestone.

## Provenance and QA limits
Package: `XB77_RedSun_4K_Development_Tools_Test02_Landmass_Gate.zip`.
SHA256: `39a2f2572d8db4e792aa5dea1e2e329fe5e48b3c4392543ed769ab4c23e6b6f7`.
The gate passed its own synthetic unit tests and classified the original inventories; it **did not** pass on a nonexistent replacement package (this failure is correct). Test source is included in the conversation package; do not confuse unit-test validation with graphical in-game validation.