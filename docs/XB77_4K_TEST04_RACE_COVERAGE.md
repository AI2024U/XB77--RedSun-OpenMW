# XB77 Red Sun 4K — Test 04 Race-Mesh Baseline

**Date:** 2026-11-22. **Status:** original-game reference audit completed; NO high-poly replacement NIF, 4K skin texture, or playable ESP has been produced.

This stage is **Morrowind + Tribunal + Bloodmoon only** and never modifies/repackages landmass materials or their terrain meshes. The original user-provided ESMs were inspected read-only; no ESM/BSA, Bethesda texture, mesh, or user path was committed.

## Reproducible local audit results

The new source-only test tools (`tools/xb77_race_mesh_inventory.py` and `tests/test_xb77_race_mesh_inventory.py`) were built and run in the conversation's local working environment, along with the Test 03 tools. Results are provided in `XB77_RedSun_4K_Development_Tools_Test04_Race_Baseline.zip` (a development-tools ZIP **not** a playable mod).

- **41/41 automated local tests passed**, covering BSA listing, terrain exclusion, release-archive checks, and race BODY record parsing.
- Original RACE definitions: **10 playable races**, each with male and female paths (20 QA categories).
- Original BODY record references: 1,387 (1,125 base, 94 Tribunal, 168 Bloodmoon).
- Anatomical `b_n_RACE_SEX_*` BODY records: **543**, referencing **510 distinct original NIF pathnames**, all found in the vanilla BSA filename inventory.
- Remaining race-assigned non-anatomical BODY records: **844**; do NOT count these as anatomical work. Many armor/clothing records use Argonian as a record race field despite being generic.
- **178 seam/attachment inspection targets** across all male/female playable-race categories; these are not yet inspected or cleared.
- **0 new 4K textures**, **0 reconstructed high-poly NIFs**, **0 finished ESPs**, **0 in-game tests**.

## Race-by-race anatomical BODY record counts

| Race | Male | Female |
| --- | ---: | ---: |
| Argonian | 22 | 20 |
| Breton | 26 | 23 |
| Dark Elf / Dunmer | 57 | 48 |
| High Elf / Altmer | 23 | 22 |
| Imperial | 29 | 26 |
| Khajiit | 22 | 22 |
| Nord | 34 | 31 |
| Orc | 21 | 20 |
| Redguard | 25 | 23 |
| Wood Elf / Bosmer | 26 | 23 |

## What needs to happen next

1. Assess mesh polygon/triangle counts, UVs and skinning from original vanilla assets, without redistributing them.
2. Create or obtain license-cleared **truly improved** character meshes and textures. Do not merely subdivide old geometry or enlarge old DDS files.
3. Test neck/head, wrists/hands, ankle/foot, joints, colors, normals, armor/clothing compatibility and animations for all 20 race/sex combinations.
4. Keep `LAND`/`LTEX`, ground textures, landscape and other landmass visuals unchanged.
5. Finally prepare native OpenMW 0.52.0 RC1 Red Sun install ZIP with separate `Meshes/`, `Textures/`, and selectable `XB77_RedSun_4K_Overhaul.esp`. Acceptance requires actual Red Sun Windows gameplay QA.

**Note:** This GitHub document records local results. The Test 04 source scripts are shipped in the locally verified development-tools ZIP; they are not yet mirrored into this branch and should not be described as such.

**Test 04 ZIP SHA256:** `3c2822cc8c757261627aa03d57845d35e18c7941726cc84ebcca81ef32722f83`.
