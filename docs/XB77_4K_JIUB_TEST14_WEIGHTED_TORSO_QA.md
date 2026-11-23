# XB77 Red Sun — Jiub Test14 weighted torso prototype

**Date:** November 22, 2026. **Working mode:** On-demand development; the previous hourly 4K automation remains paused. **Project boundary:** Red Sun portable OpenMW 0.52.0 RC1 only; do not conflate with Magic Orbis.

## Outcome

Created a new *private, installable but experimental* Test14 package from the privately held Test13 game-derived assets. It has **real subdivided skinned torso and hand geometry with rebuilt bone weights**, unlike Test13's unchanged torso topology.

**This is NOT yet confirmed working in OpenMW.** The Linux offline test environment cannot establish native game rendering, skin deformation under animation, shoulder/neck joins, or authentic artistic 4K detail. Do not mark production-ready without the user's Windows playtest.

- Private gameplay ZIP: `XB77_RedSun_4K_Jiub_Test14_Weighted_Torso_Experimental_Private.zip`
- SHA256: `00cbff01df2744fd0949b92d843e7316abf58d431b7bfb86beb5d78b3a78e2c2`
- Size: 30,685,708 bytes.
- Runtime files: **27** = 1 ESP, 12 NIF and 14 DDS. README and QA JSON make 29 ZIP entries.
- ESP: `XB77_RedSun_4K_Jiub_Test14.esp` — TES3 header, 13 BODY records and one `chargen name` Jiub NPC override, no `LAND` or `LTEX`. BODY record effects intentionally also apply to original male Dunmer anatomical records; female Dunmer and other races are untouched.
- Portable installation data path: `XB77_Portable/UserData/data`, matching the earlier Red Sun Test09 successfully loaded custom texture path.
- No original BSA, ESM, engine binary, CMD/BAT, original game data archive or terrain/landmass assets included. Original user BSA/ESM remains unchanged.

## Actual Test14 skinned geometry

Original/Test13 seven skinned shapes:
- Combined vertices: **718**
- Combined triangles: **1,098**

Test14:
- Combined vertices: **2,523**
- Combined triangles: **4,392**
- Original skin bone transforms and bone ordering retained.
- Weight tables expanded to cover all newly created vertices, with up to **four** normalized bone influences per vertex.
- Each shape retains the original physical boundary vertices; current boundary normals are retained from the source where applicable.
- Per-shape triangle counts, original → Test14: `180→720`, `38→152`, `72→288`, `180→720`, `38→152`, `72→288`, `518→2072`.
- Head, hair and nine previously subdivided unskinned male Dunmer body meshes remain geometrically unchanged from Test13; references and filenames are versioned for Test14. Head facial morphs were not newly rewritten in this milestone.

## Checks and evidence

- **115/115 independent offline structural checks passed**, including ZIP CRC and hashes, path safety, expected TES3/Body/NPC records and targets, texture readback, 7 skinned shapes, all newly weighted vertices, bone-transform preservation, no degenerate triangle indices or invalid normals, no old Test13 texture references, and exact non-geometry NIF byte preservation.
- Geometry and weighting checks are reproducible on the user's provided private originals, but source-derived meshes/texture bytes and user recordings **must not be committed to this public repository**.
- Separate editable Excel workbook: `XB77_RedSun_Jiub_Test14_Excel_QA_Results.xlsx`; six sheets: Dashboard, Geometry, Package Assets, QA Checks, Acceptance, Install Guide. The workbook tracks 115 verifications and native playtest requirements.
- Workbook QA manually inspected: formula results show 115/115, 1,098→4,392 triangles, 718→2,523 vertices, 0 accepted native/manual tests, and correct `BLOCKED / PENDING` release gate.

## Unresolved blockers

1. Windows XB77 Red Sun 0.52.0 RC1 in-game render and animation confirmation, with same-run fresh `openmw.log` and screenshots.
2. Smooth skinned torso/shoulder/neck boundary consistency under motion: pinned boundaries prevent artificial displacement but do not guarantee original seams have been corrected.
3. Real author-created 4K skin art for heads/neck/chest/arms, rather than resized low-resolution textures with synthetic micrograin.
4. Other character races, female Dunmer, full Morrowind/Tribunal/Bloodmoon non-landmass asset coverage, performance and compatibility.
5. License rights: source-derived game textures and meshes are for the supplying user's private test only.

## Safe testing

Disable all earlier Jiub Test07–Test13 ESPs. Extract the new private ZIP into the Red Sun portable engine root containing `openmw.exe`, preserving `XB77_Portable/UserData/data`. Enable **only** `XB77_RedSun_4K_Jiub_Test14.esp` under Launcher → Data Files → Content Files; start a new game at Imperial Prison Ship. Inspect Jiub's head, morphs, neck, both shoulders, chest and hands under movement and changing light. If the mesh breaks, uncheck Test14 ESP and restart, retaining original game data untouched. Record the result in the Excel Acceptance sheet.

**The 115 passing checks do not mean a verified working product; they mean an offline structural test pass.**
