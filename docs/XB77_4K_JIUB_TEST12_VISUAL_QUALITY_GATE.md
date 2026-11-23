# XB77 Red Sun — Jiub Test 12 Visual QA and Structural Regression

**2026-11-22, after user Test11 screenshot.**
Status: **FAIL** — Test11 does not meet 4K character or smooth/high-poly acceptance. The screenshot shows sharp head/neck/shoulder/torso transitions, visible faceting and insufficient detail. Do not call it an approved visual overhaul.

## Reproducible archive comparison

User-private game-derived files were inspected locally only; none were uploaded to this repository.

- Known-working Test09 ZIP SHA256: `05c71fb298b406fdfb3ad4b59cfa8d282d3b96c6eeb9e6daafb2754b4a47a27b`
- User-rejected Test10 ZIP SHA256: `16a6b359894369d2c8470cab2a676bbacb49f84f3dc44f3eb628de41d372f434`
- User-rejected Test11 ZIP SHA256: `386302000d0ecbaded23c42665c44e4bbfd12b7cd75664b01e4e273d9f911c7e`

Test11 head and hair NIFs are each the **exact same length** and binary content as Test09 apart from **two bytes in the DDS filenames per NIF**. The differences are only `009`→`011` in the custom texture references. There is absolutely no change in head or hair geometry. The Test11 package also contains **zero body-part NIF replacements**. Its DDS images are 4096×2048 and 4096×4096 but are derived from low-resolution original artwork. Therefore pixel dimensions do not equal genuinely newly authored 4K texture detail.

Test10 had changed NIF data (head 340,957 bytes vs original 24,109, hair 135,917 bytes vs 9,569), but no body NIFs; it failed the user's native test, and mere binary differences do not prove better topology or compatibility.

## New quality gate

Created locally: `XB77_RedSun_4K_Jiub_Test12_Quality_Audit_Tools.zip`. Source-only, no Bethesda art.

The audit tool compares candidate head/hair NIFs with a baseline after normalizing **only** the Jiub-private texture path strings, verifies actual DDS dimension fields, checks the number of body mesh replacements, recognizes a Jiub ESP, and excludes terrain names. It intentionally fails Tests 10 and 11. **8 synthetic tests passed locally.** Archive SHA256 `68023d9c39d17c0057a9d301919805a339d59608a434fa5b98d0bd0262378bfa`. This tool does NOT certify OpenMW rendering, photorealism, morphology, edge continuity, normal quality or copyright licenses.

## Real production required

1. Use an OpenMW-compatible Morrowind NIF pipeline, such as the documented Blender Morrowind plugin and NifSkope verification. Preserve NiGeomMorpher/face expression targets and rig/weight/UV attachments.
2. Build genuinely higher-resolution **authored** skin diffuse artwork for the face, neck, shoulders and full torso rather than rescaling 128–256px original textures.
3. Build matching high-poly head **and** all visible segmented body meshes; match physical and UV boundaries across neck/wrist/shoulder/ankles. Do not claim smoothing a low-poly silhouette or adding polygons blindly equals quality.
4. Validate all assets in XB77 Red Sun portable OpenMW 0.52 RC1 under strong and soft light and during gameplay expression/animation. Regress against user's original Jiub screenshot.
5. Continue hard landscape/terrain exclusion. Do NOT alter `LAND`/`LTEX` or Morrowind/Tribunal/Bloodmoon landmass textures and meshes.
6. Do not publish additional user-facing "4K fixed" ZIPs until genuine new artwork, complete geometry and native gameplay QA exist.

**No paid Windows CI was triggered; the hourly automation remains paused by user's explicit instruction.**
