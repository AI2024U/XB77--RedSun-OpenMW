# XB77 Red Sun — Jiub original-art Alpha03: talking and blinking repair

**Date:** November 22, 2026 · **Status:** PRIVATE USER PLAYTEST CANDIDATE — native rendering and voice animation unverified.

## User-verified input

The user's OpenMW gameplay recording (November 22, 19:29:02) demonstrated that the Alpha02 original head renders in XB77 Red Sun, but user reported mouth and eye animations absent or not perceptible. Alpha03 aims at those facial morph targets only.

## Observed technical cause and OpenMW behavior

1. Alpha02 preserved the base Morrowind `NiGeomMorpherController`, `NiTextKeyExtraData` and three `NiMorphData` targets. It did not lack those NIF blocks.
2. Alpha02's strongest *talk* displacement was **0.2962 game units**, unlike the original Morrowind head morph's ~**1.1225 units**. It moved only a narrow UV strip and was not a credible jaw opening.
3. Alpha02's strongest *blink* displacement was **0.3346 units** globally, but only **0.0512 units** near the painted eye region. Its blink was centered near UV-v=0.503 whereas the painted eyes were around UV-v=0.405.
4. OpenMW source `apps/openmw/mwrender/npcanimation.cpp` uses `sayActive(ref)` and voice loudness for mouth animation, not plain silent dialogue text. Blink timers are independent of speech. The engine maps NIF talk/blink text key times to its `HeadAnimationTime`.
5. OpenMW source `components/sceneutil/morphgeometry.cpp` takes target 0 as absolute base head coordinates and adds weighted offsets for targets 1 (talk) and 2 (blink).

## Alpha03 asset changes

- Runtime ZIP: `XB77_Jiub_OriginalArt_Alpha03_Facial_Morph_Private_Playtest.zip`, SHA256 begins `5e6dc8f7`.
- The NIF filename **remains `XB77_Jiub_Original_Head_A02.nif`** because it is already referenced by the verified Alpha02 plugin; the Alpha03 content replaces that head mesh in the same registered data directory.
- The old Alpha02 `XB77_Jiub_OriginalArt_Alpha02.esp`, original ear mesh, and facial 4096x2048 DDS are **byte-for-byte unchanged**. No plugin changes, no other races, no terrain.
- `NiTriShapeData` vertices, UVs, normals and triangles, base morph target 0, NIF controller, controller timing and textkeys are preserved exactly.
- Only morph offset target 1 and target 2's float arrays are modified. One shape, **7,956 vertices and 15,544 triangles**.
- New talk maximum displacement: **1.2209 units**. New blink maximum: **0.8111 units** and **0.8111** in the targeted upper-eye region.
- Independent offline poser renders neutral / talking / blinking; neutral is visually identical to Alpha02 and the open mouth and closed eyes can be seen in the renders. Renders are NOT screenshots of OpenMW gameplay.
- Geometry remains nondegenerate in all three poses (smallest triangle areas >0.0009 units squared), but potential self-intersection, shading folds, lip appearance and gameplay timing still require human verification.

## Offline QA

**18 checks PASS, 0 FAIL; 4 native/visual acceptance tests PENDING.** See `XB77_Jiub_Alpha03_Facial_Animation_Excel_QA.xlsx`, which documents the difference and installation.

Package is deliberately self-contained: 4 runtime files in `XB77_Portable/UserData/data`, README and JSON QA. Source ZIP `XB77_Jiub_OriginalArt_Alpha03_Editable_Morph_Source.zip` includes authoring OBJ/PNGs and the morph patcher source. No original Bethesda game archives, ESM or BSA are shipped in these ZIPs.

## User test steps

1. Disable earlier Jiub Test07–Test14 ESPs and other Jiub Alpha plugins.
2. Extract the Alpha03 ZIP into the Red Sun engine directory containing `openmw.exe`, preserving `XB77_Portable/UserData/data`. Overwrite the existing Alpha02 head file if prompted.
3. In the launcher enable ONLY **`XB77_Jiub_OriginalArt_Alpha02.esp`** (this is intentional — the ESP is unchanged and there is no separate Alpha03 ESP).
4. New game: listen to Jiub's **audible voiced line**, not just click silent dialogue topics, and watch mouth motion. Watch at least 15–20 seconds for autonomous blinking.
5. Capture an unedited video with audio and fresh `openmw.log` if there is no animation. To roll back, restore Alpha02's head NIF from its original ZIP or disable the ESP.

**Do not mark as working lip-sync or public release until tested in the native Windows Red Sun OpenMW runtime.** Automation remains off.

## Technical sources
- https://github.com/OpenMW/openmw/blob/master/apps/openmw/mwrender/npcanimation.cpp
- https://github.com/OpenMW/openmw/blob/master/components/sceneutil/morphgeometry.cpp
