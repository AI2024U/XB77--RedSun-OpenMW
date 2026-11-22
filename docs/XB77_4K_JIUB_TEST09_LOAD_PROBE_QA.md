# XB77 4K Jiub Test 09 — load isolation, not 4K art approval

**November 22, 2026.** Project: XB77 Red Sun OpenMW 0.52.0 RC1. Scope: original Morrowind; landmass, Tribunal and Bloodmoon untouched.

## Evidence from the user

- User's Test 08 prison-ship recording shows Jiub's visible head and otherwise largely vanilla appearance with angular body silhouette and uncorrected seams. Test 08 intentionally used original vanilla NIF geometry, so it **could not improve polygons or seam geometry**.
- Earlier 07:12 OpenMW log recorded **Test 07** loaded as a content file, with errors stating `meshes/b/xb77_jiub_head_07.nif` and `meshes/b/xb77_jiub_hair_07.nif` were *not found*, using `marker_error`.
- The 07:12 user-provided `openmw.cfg` listed `content=XB77_RedSun_4K_Jiub_Test07.esp` but no Test 07 loose-asset data directory. This explains the earlier Test 07 missing resource marker; it does **not** prove the later 07:22 Test 08 settings, as those logs predate the new footage.
- The 07:12 run confirms `XB77_Portable/UserData/data` is an already registered Red Sun data directory. Test 09 is intentionally packaged under this path in the portable engine root to avoid relying on an added launcher data directory.

## Test 09 private diagnostic

- Output `XB77_RedSun_Jiub_Test09_Loading_Proof_Private.zip`, SHA256 `05c71fb298b406fdfb3ad4b59cfa8d282d3b96c6eeb9e6daafb2754b4a47a27b`.
- ZIP includes exactly five gameplay files, nested under `XB77_Portable/UserData/data`: a real TES3 ESP, two uniquely named Jiub NIF files, and two uniquely named 4096px DDS textures. It also includes a README and a manifest.
- ESP adds `BODY` records for `xb77_jiub_head_09` and `xb77_jiub_hair_09`; overrides only Jiub NPC ID `chargen name` to select those models. NPC script, stats and inventory remain original.
- Model geometry is **still original**; two NIFs have uniquely named DDS references; no new vertices, rig weights, seamless textures, or mesh geometry work.
- Experimental face DDS is teal-tinted over the full atlas and stamped `XB77` on a cheek for unmistakable visual texture-load verification. This coloring is intentionally diagnostic and **not approved or suitable for aesthetic release**.
- Independent offline verification passed: archive CRC, seven archive members, five game files, ESP TES3/BODY/BODY/NPC_ records, zero LAND/LTEX records, cross-resolved NIF→DDS paths, DDS 4096px dimensions, and no ground/landmass files.
- Actual OpenMW native gameplay rendering of Test 09 is **unverified** and still requires a user-side check. The prior photorealistic concept preview was not a texture/mesh production result.
- ZIP contains Bethesda-derived mesh/texture assets from user-provided originals, so must remain private/personal use; it must NOT be committed to this public GitHub repo or redistributed.

## Next real development

Use proven loading route before investing in modeling. Then develop/verify *genuinely new* higher-resolution artwork and rig-compatible high-poly NIF geometry with improved seam continuity. Changing file dimensions alone cannot remove faceting or recover absent source detail. Do not count this prototype toward final asset-completion percentage. The user requested that hourly 4K automation remain paused; this is an on-demand development pass.
