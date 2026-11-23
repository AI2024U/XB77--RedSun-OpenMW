# XB77 Red Sun — Jiub Test 13 full-body geometry prototype

**Date:** November 22, 2026. **Status:** OFFLINE EXPERIMENTAL BUILD; MUST NOT BE CALLED A NATIVE GAME FIX YET.

Private personal-use package built from user-provided legally owned `Morrowind.bsa` and `Morrowind.esm`, and the known Test11 ESP/texture prototype. No copyrighted game assets in this public repository.

## Package

- Name: `XB77_RedSun_4K_Jiub_Test13_MorphSafe_FullBody_Experimental_Private.zip`
- SHA256: `cb8a12b7c14a86bd8cc7b14a419097191cb855d9be1d326b25f490429839e4af`
- Size: 30,438,387 bytes compressed.
- 29 archive entries, including 27 runtime files: one genuine ESP, 12 NIF meshes, 14 DDS textures, plus README and QA manifest. Full CRC passed.
- Runtime folder: `XB77_Portable/UserData/data`, the Red Sun portable data root verified to load Jiub's Test09 custom face texture in user footage.

## Actual mesh work

- Jiub head one-pass Loop subdivision, original **293 vertices / 524 triangles** to **1,098 vertices / 2,096 triangles**.
- Original three facial morph targets (base, talking, blinking) rebuilt using the **same vertex weights and output topology** as the head mesh. All 63 original open boundary vertices pinned to original base and morph coordinates.
- Hair two independent shapes: **382 triangles to 1,528**.
- Nine other unskinned male-Dunmer anatomical meshes (neck, foot, forearm, groin, knee, ankle, upper arm, upper leg, wrist) each subdivided 4× in triangle count with open boundary vertices pinned to source positions.
- Shared male Dunmer skinned chest/hand file: conservative 0.25 interior-vertex relaxation, **original 7 shape triangle counts and all NiSkinInstance / NiSkinData bone weights preserved**. **Skinned chest is NOT high-poly** yet; body/shoulder visual quality remains an unresolved risk.
- All 12 NIFs use newly unique private DDS references; no vanilla mesh or texture paths are overwritten. The ESP has 13 BODY records (2 new Jiub head/hair and 11 male Dunmer original anatomical BODY record overrides), one Jiub NPC override, one TES3 header. No LAND/LTEX records. Effect on all male Dunmer anatomical models is intentional for this private test.

## Texture honesty

- All 14 packaged DDS atlases are 4096 pixels wide; some 2:1 vertical-atlas textures are **4096×8192** to preserve UV aspect ratios.
- The two Jiub face/hair DDS are natural-color scaled originals from Test11. The remaining 12 textures are upscaled original art with independently generated low-amplitude surface micrograin.
- They are **NOT genuinely hand-painted 4K art**, and neither file size nor dimensions proves improved fine facial detail or seam quality.

## Verification

- Build-time record/asset validation and ZIP integrity: PASSED.
- Independent source-vs-package audit: **201 checks PASSED**, including exact manifest hash verification, all NIF references resolving to the 14 DDS, original ESM BODY overrides pointing to 10 unique generated body meshes, ESP record count and Jiub identity, NiMorphData count matching head vertices, and no degenerate triangles among the generated shapes.
- Prior Test12 quality regression gate: **PASSED** on Test13 against proven Test09; head/hair are no longer geometry no-ops and 10 body NIF replacements exist. Structural pass is **not** native rendering acceptance.
- No original BSA, ESM, logs, personal paths, executable, shell script, BAT/CMD, landscape texture or mesh delivered.
- No OpenMW binary/Windows runtime was available in the build container, so **NIF load, morph animation, lighting and seams are UNVERIFIED in the target XB77 Red Sun OpenMW 0.52 RC1**.

## User test

Disable all Jiub Test07–Test11 ESPs. Extract Test13 into the root of the XB77 Red Sun portable build containing `openmw.exe` and `XB77_Portable/`. Enable only `XB77_RedSun_4K_Jiub_Test13.esp` in the Content Files tab. Start a new game; inspect Jiub's face in dialogue (blink/talk), neck seams, hair and all Dunmer-male body parts. The BODY overrides also affect other male Dunmer NPCs and player bodies. If there are yellow missing-resource markers, broken facial morphs, gaps or limbs, uncheck Test13 and restart. Obtain `openmw.log` from the same run.

**Not a public release.** Correct the in-game failure first; subsequent work needs a real blender export/skin weight repair path and artist-authored high detail textures.

The hourly automation remains paused by user request.
