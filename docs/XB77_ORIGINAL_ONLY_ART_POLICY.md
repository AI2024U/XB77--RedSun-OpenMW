# XB77 Red Sun — Original 4K Character Overhaul Policy

**Status: active art-direction requirement, November 22, 2026.**

## User-approved constraint

All *new* XB77 character textures, high-poly meshes, UV maps, skin materials, normals, facial morphs, and rig-binding work will be **authored specifically for XB77 from scratch**. Do not use other Morrowind mods, their textures, head/body meshes, remodels, packs, converted files, or derived assets as the starting point. Do not distribute another resampled vanilla DDS or merely subdivided vanilla NIF as an approved finished upgrade. Prior Test05–Test14 prototypes are retired as art baselines, retained only as **negative QA examples** and loading-debug history.

Original Morrowind/Tribunal/Bloodmoon ESM/BSA files supplied by the user are legal-installation references for record IDs, UV interfaces, skeleton conventions, animation requirements and appearance preservation, **not a source of redistributable replacement artwork**. Bethesda game data stays private. Exclude all landmass/terrain textures and meshes and all `LAND`/`LTEX` plugin records.

No third-party character artwork means no third-party *mod-asset* attribution obligations from incorporated artwork. However, the project must continue to provide required license notices for the modified OpenMW engine (GPL and dependencies) and accurately identify Bethesda's underlying game and trademarks. Our independently authored mod assets can be documented and licensed separately; **this cannot be described as having zero legal attribution obligations**.

## Production stages (art-first, not triangle-count-first)

1. Produce a custom XB77 sculpt/design sheet with approved facial anatomy for Jiub: scar, ears, expression zones, and original Dunmer appearance, without copying a third-party mod's geometry or image.
2. Sculpt full closed, matching anatomical geometry for head/neck, upper torso, both shoulder sockets, upper and lower arms, hands, legs and feet. Preserve game identity through references, not copied vertex arrays. Create all character topology within XB77 source files.
3. Retopologize and build native-compatibility assets with validated Morrowind NiTriShape/NiSkinData/NiGeomMorpher bindings and appropriately interpolated/validated weights. Ensure game animation and expressions survive import/export.
4. Unify physical seam rings, UV border coordinates, vertex normals and color values across adjoining parts. Validate in multiple bone poses rather than only one still frame.
5. Paint true-resolution high-detail color/skin texture maps from blank XB77 source documents; normal/specular details must be explicitly authored. Image dimensions alone are not an artistic pass.
6. Compare in-game against original Jiub under the same lighting and camera, from multiple angles and while talking/walking; obtain user close-up acceptance in Red Sun OpenMW 0.52 RC1.
7. Repeat for male and female variants of all ten playable races. Include base Morrowind + Tribunal + Bloodmoon character asset coverage; do not touch landscape or extra content.
8. When a genuine original-art prototype actually passes, package separate NIF/DDS and a functional selectable ESP; keep a clean reversible data directory and no original game archives.

## Release and credit gate

Every new NIF/DDS must be paired with an **editable XB77-created source** (`.blend`, `.kra`, `.psd`, `.xcf`, `.spp`) and a SHA256 chain in a source manifest. This technical record is necessary but is not itself proof of copyright authorship. An independent visual/source review must confirm new art was genuinely created and not a copied model, repack, upscale or subdivision-only operation.

The downloadable release ZIP must not claim quality on the basis of CRC, vertex counts, pixel dimensions, or hash validation alone. Official public release requires a passed engine-and-gameplay visual acceptance gate. 

**Current acceptance:** 0 genuinely authored/visually approved 4K characters. **Test14 is a confirmed visual failure.** Hourly automation stays paused; development continues by direct user request.