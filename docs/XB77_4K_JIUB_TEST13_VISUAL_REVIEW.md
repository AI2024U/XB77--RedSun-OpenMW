# XB77 Red Sun 4K — Jiub Test 13 in-game screenshot review

**Recorded:** 2026-11-22, user's screenshot at approximately 6:02 PM Pacific. 
**Result:** **VISUAL QA FAIL** — next package must improve actual skinned torso, neck and shoulder joins before release. This is a *review*, not an updated mod.

## Evidence and limits

- User's 800×600 screenshot shows Jiub visible aboard Imperial Prison Ship at the character-name prompt. No oversized yellow missing-model error markers are visible, unlike the known Test07 failure.
- Facial scar, ears and head are present, but the lower face/chin still looks faceted. The neck terminates in a hard, angular seam.
- Upper arms appear as rounded, separately shaded shoulder caps with distinct hard borders against the torso on **both sides**. The chest and shoulder silhouette still has obvious angular geometry, especially noticeable under the dim ship lighting.
- Name-dialog overlay hides part of the abdomen; no claim of full body/feet/hand visual clearance is possible.
- Screenshot alone does not prove exact ESP/texture paths loaded or animation correctness. No same-session `openmw.log` is attached for this frame. It DOES prove the user-facing result is not acceptable for the desired seamless high-detail character look.

## Inspection of Test13 original packaged meshes (offline)

Archived Test13 package: `XB77_RedSun_4K_Jiub_Test13_MorphSafe_FullBody_Experimental_Private.zip` (29 ZIP entries, CRC passed). ESP plus 12 NIFs, 14 DDS assets. No original Bethesda game master/archive files or terrain texture files in the ZIP.

- Jiub head `XB77_Jiub_Head_13.nif`: 1,098 vertices and 2,096 triangles, up from 293 vertices / 524 triangles in original. Facial morph shape data was changed but not visually verified for animation.
- `XB77_Dunmer_M_upper_arm_13.nif`: 301 vertices and 560 triangles, up from 81 vertices and 140 triangles.
- `XB77_Dunmer_M_neck_13.nif`: 201 vertices and 336 triangles, up from 59 vertices and 84 triangles.
- **Crucial bottleneck:** `XB77_Dunmer_M_skins_13.nif` still contains exactly **seven skinned shapes, 718 combined vertices and 1,098 combined triangles**. It is **not subdivided**; the original `NiSkinInstance` and `NiSkinData` were retained, with conservative interior-vertex relaxation only. Thus it cannot honestly be described as a high-poly torso.
- The separate body shapes' original open boundary vertices were pinned rather than matched to the animated skinned torso. Pinned boundaries can prevent gaps from new displacement but cannot eliminate original junction offsets, lighting/normal discontinuities, or texture-color seams.
- DDS dimensions alone are not proof of original 4K surface detail; Test13 texture artwork derives from low-resolution Morrowind textures. No production-quality 4K artwork has been approved.

## Required changes before a new playable claim

1. Properly subdivide/remodel the skinned torso and shoulders in a validated Morrowind NIF pipeline; **interpolate and normalize NiSkinData skin weights on every new vertex**, preserving bone partitions, weights and animation attachment.
2. Align physical junction boundaries and tangential shading/vertex normals between torso, upper arms, neck and hands in compatible local/bind-pose coordinates. Check multiple body animation poses.
3. Generate coherent diffuse artwork across head/neck/chest/arms with original UV mapping or carefully authored replacement UVs; do not call resampling original 128–256px art a real 4K repaint.
4. Evaluate at close range with bright and low light, during idle/walk/talk, in Red Sun OpenMW 0.52.0 RC1, with fresh logs; do not infer a working gameplay fix from static mesh/ZIP integrity alone.
5. Preserve all ten playable races as eventual target, and keep Morrowind, Tribunal, Bloodmoon landmass textures/meshes and LAND/LTEX records untouched. Separate broad male-Dunmer BODY replacement scope from Jiub-only validation.
6. Keep all Bethesda-derived source assets private. No paid Windows build needed for this QA report.

**Decision:** Test13 remains an experimental visual failure, *not* an approved 4K high-poly Dunmer release. Prior automated archive checks remain true as structural checks, but do not satisfy the required aesthetic acceptance.
