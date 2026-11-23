# XB77 Red Sun — Original Jiub Head Alpha02 (unreleased)

**Status: PRIVATE ORIGINAL-ART CANDIDATE; NOT A WORKING 4K OVERHAUL.**

### Original work delivered
- Procedurally authored head OBJ: 7,956 vertices / 15,544 triangles (not subdivision of the original head mesh).
- Two procedurally authored Dunmer ear OBJs: 493 vertices / 896 triangles each.
- New face concept generated specifically for this project at 1774×887 plus native-resolution procedural surface detail, exported as 4096×2048 DDS. The original concept is NOT a natively painted 4K master.
- Face mesh contains base, talk-offset, and blink-offset morph targets.
- New Jiub-only ESP compiled independently from the original Morrowind.esm record data. The first version had an invalid subrecord size due to longer filenames; it was corrected by rebuilding every subrecord with exact lengths.
- Private runtime package: `XB77_Jiub_OriginalArt_Alpha02_Private_Playtest.zip`: one ESP, two NIF files, one DDS, README, validation data.
- Editable source package: `XB77_Jiub_OriginalArt_Alpha02_Editable_Sources.zip`, containing OBJ, lossless PNG, concept source and Python code.
- Actual 960×960 offline 3D preview from the generated OBJ and material: `XB77_Jiub_Original_Head_A02_3D_Preview.png`.
- Independent offline archive, record, morph, skin-source, and DDS tests: **62 / 62 passed**.

### Hard release gates NOT met
- No native XB77 Red Sun OpenMW 0.52.0 RC1 game-render or facial-motion validation.
- No repaired neck/body/shoulder seams.
- No complete ten-race body and face coverage, Morrowind/Tribunal/Bloodmoon NPC coverage or performance verification.
- No genuine native-source 4K hand-painted master art (the current output is assembled from a new lower-resolution concept and native procedural microdetail).

Original Bethesda NIF file-format/controller shell is only used in the user's private adapter. Do not upload game-derived NIFs/assets to public GitHub or publish this game ZIP without a rights and in-game audit. Landscape/landmass content remains unchanged; ZIP has no LAND or LTEX records and no original ESM/BSA archives.

**Decision:** Alpha02 is a new-original-geometry and original-material technical candidate, a material visual change from Test14, **but not yet a working or finished graphics overhaul**. Hourly automation remains off.
