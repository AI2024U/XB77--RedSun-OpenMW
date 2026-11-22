# XB77 4K Overhaul — Test 05 Private Dunmer Skin Prototype

**Date:** November 22, 2026. **State:** source-asset prototype and local synthetic QA, **NOT** approved 4K artwork or playable graphics overhaul.

## Real private output (NOT in public GitHub)
Three personally testable DXT5 DDS diffuse replacements were generated **locally from the user's provided original Morrowind.bsa**, with original atlas UV proportions preserved:
- `Textures/tx_b_n_dark elf_m_h01.dds` — Dunmer male default head, source 256×128, output **4096×2048**
- `Textures/tx_b_n_dark elf_m_n.dds` — neck, source 128×64, output **4096×2048**
- `Textures/tx_b_n_dark elf_m_c.dds` — chest, source 256×256, output **4096×4096**

**Important:** This technique is Lanczos scaling plus deterministic, independently generated multiscale surface microdetail. It **does not recover lost original high-resolution detail**, does not independently paint a 4K face, and is not equivalent to true professionally created source art. Side-by-side visual inspection found subtle detail differences and **did not approve final texture quality**. No real high-poly NIFs, final ESP, or in-game seam/performance testing are complete.

## QA evidence
- **48 Python tests passed locally**: previously verified 41 tests plus 7 new synthetic texture-generation/extraction tests.
- Original Morrowind BSA used read-only. No terrain/landmass/landscape/mud/ground textures or meshes selected or modified.
- All three private DDS exported and successfully reopened at correct dimensions; aspect ratios retained. Output archive integrity and member type/filename checks passed.
- Output contains no original game BSA, ESM, unrelated resource, high-poly NIF, engine executable, or ESP.
- The private test can be loaded as a separate OpenMW data directory for testing, without altering Red Sun OpenMW 0.52 RC1 itself; **no claim of in-game compatibility yet**.
- Original source archive remains unchanged. Source-derived **texture bytes must never be committed publicly or redistributed**.

## Local private artifacts (delivered only to supplying user)
- `XB77_RedSun_4K_Dunmer_Skin_Test05_Private.zip` (personal testing only; Bethesda-art derivative, **do not distribute**); local SHA256: `f28d1bce76a5deb4a2a1ed39833dbbf32defafea0f4be7d97b8fcf3544f9ab35`
- `XB77_RedSun_4K_Development_Tools_Test05.zip` (source/test tooling, no protected originals); local SHA256: `4c150b189b915aabab541b6f3e9ebf7c05774602728582cb37cbf7743da0f354`

## Pending QA and production
1. License/provenance-clear original 4K artwork authored at real target resolution and matching the original UVs for all ten races.
2. Real character high-poly model pipeline, compatible with vanilla rigs, weights and animations. Do not mistake subdivision or synthetic pores for completed polished art.
3. Multi-light and animation-based head/neck/chest seam testing in user's Red Sun OpenMW. Reject visible polygon faceting, UV seams and mismatched skin.
4. Full Morrowind/Tribunal/Bloodmoon non-landmass asset coverage audit.
5. Final ESP plus actual loose Textures and Meshes, separate Data Directory and rollback, followed by tested release ZIP.

**All hourly automation is paused by user request; future work proceeds on demand in conversation.**
