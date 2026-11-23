# XB77 Red Sun 4K — Test14 visual failure and corrected engineering decision

**Date:** 2026-11-22. **Project:** Morrowind / Tribunal / Bloodmoon NPC-and-character artwork only. **Red Sun OpenMW target:** 0.52.0 RC1. **Automation:** hourly task remains disabled.

**Decision: STOP describing procedural resampling + per-part triangle subdivision as the promised 4K character overhaul.** User's 18:51:36 gameplay video clearly shows a vanilla-like Jiub face, shoulder caps, hard neck transition and similarly harsh polygons. Test14 must be marked **VISUAL QA FAILED**, even though prior 115 structural checks passed. No new release is accepted on numerical polygon/texture sizes alone.

## Reproducible root-cause findings from the actual archived Test14 builder and user-owned source data

1. `build_test13.py` takes original BSA DDS atlases, resizes to 4096px wide using Lanczos and adds a few RGB levels of synthetic noise. Test14 copies those texture atlas bytes with revised names. They are NOT genuinely author-created high-resolution skin artwork.
2. Measured DDS source-versus-output similarity: when the Test14 DDS is downsampled to the original resolution, the mean absolute RGB differences (0-255) are Jiub face **1.575**, hair **2.434**, neck **1.434**, chest **1.535**, upper arm **1.550**, lower arm **1.443**. Jiub head source is **256x128** and the Test14 output is **4096x2048**; the chest is 256x256->4096x4096. These are direct measurements of similarity, not a proof that every high-frequency pixel is uninformative; together with the reviewed builder they show the core artwork was not redesigned.
3. `geometry_pipeline.py` performs independent Loop subdivision per NiTriShapeData, retaining each original open boundary vertex; `skin_subdivider.py` interpolates/renormalizes NiSkinData weights per shape. No cross-mesh seam welding, skin-color matching, shared tangent-space normal alignment, authored high-poly anatomy, or in-game pose-dependent matching occurs. Thus a fourfold triangle count does not solve the visible seams or silhouette.
4. Measured Jiub head mesh 293->1098 vertices / 524->2096 triangles; mean movement of original head vertices **0.156** game units, max **0.599**. Original head bounding dimensions ~9.129x14.425x15.126; Test14 ~9.12x14.047x14.99. This quantitatively explains how triangle count can grow while the main silhouette remains nearly identical.
5. Body source is multiple separate Morrowind body-part records and NIFs. An ESP changing these record references does not automatically make joins continuous or change the OpenMW engine itself. Head/neck, shoulder/torso and hands require coordinated mesh, rig, normals, UVs, diffuse and normal artwork as a unit.
6. Historical log from 07:12 relates to Test07 only and is not enough to verify which Test14 content paths were resolved. User's Test09 teal face previously established a working custom asset route, but **a fresh Test14 log is absent**. Do not assert a current missing-asset error without it.
7. OpenMW modding documentation recommends a Blender+NIF export pipeline for authored models. MOMW's current bodies/heads selections provide examples of coherent purpose-made assets, including Better Bodies 3.2, Westly Faces Refurbished, and an available Better Bodies Improved and Westlified seam/color addon. These external resources are **not uploaded, included or authorized for redistribution**, and compatibility with the user's customized Red Sun binary is not verified.

## Corrective production standard

- Obtain/create actual authored higher-poly characters with correct morphology, UV atlases, morph targets and skeleton weights. Choose one consistent, compatible body family per race.
- Create matching real detail textures (albedo/diffuse and optionally normal/roughness adapted for engine) with true source 4K detail; do not merely upscale 128-256px samples.
- Solve seams after assembling an entire character with game-equivalent skeleton at multiple poses; check boundary vertex positions, vertex normals and UV/matching skin tones across head, neck, torso, shoulder, arm, wrist and foot.
- Preserve all landmass exclusions, all original game files, and Red Sun portable engine. Keep game-derived original assets private.
- Require (a) independently verified exact asset loading in Red Sun, (b) an in-game closeup before/after with strong and low light, (c) expression, idle, and movement tests, (d) zero visible seams/clip errors, (e) a provenance/permission inventory before a release ZIP and playable ESP are advertised.
- Don't ship another superficial Jiub Test15 repack. The next player-downloadable package should actually include reviewed, coherent authored head-and-body art; otherwise report source-development limitations honestly.

## References

- https://openmw.readthedocs.io/en/stable/reference/modding/custom-models/pipeline-blender-nif.html
- https://modding-openmw.com/lists/graphics-overhaul-bodies-heads/
- https://modding-openmw.com/lists/total-overhaul-bodies-heads/4/
- https://www.nexusmods.com/morrowind/mods/60660

Evidence files are local/private: original user Morrowind.bsa, Test14 ZIP and build source, latest video; do not commit those binaries or screenshots. Corresponding user-facing Excel audit: `XB77_Jiub_Test14_Visual_Failure_Root_Cause.xlsx`.
