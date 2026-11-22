# XB77 Red Sun 4K — Jiub Test10 Private Head/ Hair High-Poly Prototype QA

**Date:** November 22, 2026. **Scope:** Original Morrowind NPC Jiub (`chargen name`), not Magic Orbis. **Status:** Private experimental output, offline structural checks passed. **Native OpenMW gameplay and visual seam QA are NOT yet performed.**

## History and intent

- Test07 produced large missing-resource markers because the custom NIFs were not available to the running engine.
- Test08 restored a vanilla-looking head using unmodified source meshes and did not improve polygon faceting.
- Test09 proved Jiub's uniquely referenced face DDS was loaded in the user's XB77 Red Sun portable OpenMW 0.52 RC1: his face was visibly teal.
- Test10 keeps **the proven Test09 portable `XB77_Portable/UserData/data` layout**, but removes teal coloring and replaces only Jiub's head/hair references with geometrically subdivided NIFs.

## Actual private prototype produced

Archive: `XB77_RedSun_4K_Jiub_Test10_HighPoly_Prototype_Private.zip` (7,205,393 compressed bytes).

SHA256: `16a6b359894369d2c8470cab2a676bbacb49f84f3dc44f3eb628de41d372f434`.

Exact runtime members nested within `XB77_Portable/UserData/data/`:

- `XB77_RedSun_4K_Jiub_Test10.esp` — actual TES3 plugin, 4 records (`TES3`, `BODY`, `BODY`, `NPC_`); Jiub NPC ID remains `chargen name`, only head and hair selections changed.
- `Meshes/b/XB77_Jiub_Head_10.nif` — experimental 4.0.0.2 head model, **293→4,259 vertices, 524→8,384 triangles**, with morph data rewritten for all 3 original facial morph targets.
- `Meshes/b/XB77_Jiub_Hair_10.nif` — two unskinned source hair shape blocks subdivided to **6,112 combined triangles** (4,480 and 1,632), versus 382 combined original triangles.
- `Textures/tx_xb77_jiub_face_010.dds` — original-colored 4096 × 2048 diffuse DDS (no teal / XB77 mark).
- `Textures/tx_xb77_jiub_hair_000010.dds` — original-colored 4096 × 4096 diffuse DDS.

The two DDS files are **derived upscales of original low-res art**, not newly painted high-detail 4K artwork, and this test does not claim facial photorealism. Jiub's **neck, chest, shoulders, arms, body-parts and all other NPCs remain vanilla**. No new body polygons, weights, terrain files or landscape records were included.

## Verification performed

- Build script rebuilt head geometry and three facial morph data arrays together, preserving their vertex counts.
- The modified head and hair NIFs parse again as NetImmerse 4.0.0.2 data, with valid shape/triangle bounds, finite vertex positions, normalized normals and no zero-area head triangles.
- For the head, all **10 original physical mesh boundary vertices** are pinned identically to source for the base and both expression targets (coordinate delta 0). This helps avoid pulling the head boundary away from the vanilla neck but **does not prove in-game absence of seams**.
- Original head UV coordinates are unchanged for the original vertices; edge UV coordinates are interpolated during subdivision.
- Independent package validation PASSED **33 checks** covering CRC, exact path membership, extension and resource references, both DDS decodes/dimensions, ESP master/record types, NPC unmodified nonappearance fields, morph/head topology, the two hair shape sections, and intentionally unverified native/visual status.
- Original Morrowind BSA and ESM accessed read-only. No BSA, ESM, original game executables, landmass textures or mesh records packaged.
- The 7-file private archive passed a full ZIP integrity test.
- Source-derived art is **for user's personal game testing only**. Do not upload private NIF/DDS binaries to this public repo, Nexus, or redistribute them.

## Critical unverified risks and quality limits

1. **OpenMW render compatibility is NOT yet verified:** NIF self-parse, normals, morph tests do not guarantee flawless facial animation or correct engine rendering. Previous Test07 failure makes game-side validation essential.
2. Actual skin and body seam appearance under animation and different light conditions is unknown. Vertex count growth does not imply finished high-poly visual quality.
3. This is **Jiub head/hair only**, not all Dunmer NPCs, the player character, all races, Tribunal, or Bloodmoon.
4. The portable folder is known from Test09's successful gameplay but Test10 may still fail if the install path or content plugin setting differs.

## Required Test10 user test

Uncheck all older Jiub ESPs; unzip into the folder containing the XB77 Red Sun `openmw.exe` and `XB77_Portable`, preserving paths. Check `XB77_RedSun_4K_Jiub_Test10.esp` under OpenMW Launcher → Data Files → Content Files. Start a new game aboard Imperial Prison Ship. Confirm correct natural coloring, no yellow error geometry, healthy head/hair, forehead/eye/mouth expressions, and neck/shoulder seams from multiple angles. Report game capture and a fresh `openmw.log` before any compatibility claim.

## Next development

If Test10 renders successfully, create genuinely new high-resolution Jiub/Dunmer head and body artwork, and a separately tested body mesh pipeline that fits clothing and animated body-part transitions. Respect complete landmass exclusion. The hourly 4K automation remains paused by user request.
