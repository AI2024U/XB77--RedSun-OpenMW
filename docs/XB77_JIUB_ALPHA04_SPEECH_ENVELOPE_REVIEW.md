# XB77 Red Sun OpenMW — Jiub Alpha04 sound-driven speech review

**Scope:** On-demand Jiub speech animation, November 22 2026. **Hourly automation off.** Runtime package uses canonical `Data/RedSun_OpenMW MODs/`.

## User video

User supplied `XB77 Red Sun OpenMW 2026-11-22 20-34-27.mp4` (~22.7 s, 800×600). Jiub's custom head is present. Talking mouth motion has visible variation but stiff/limited contour. Frame-by-frame inspection does **not** prove the Red Sun engine's actual getSaySoundLoudness per-NPC values; recorded audio includes other sound sources.

## Root diagnosis with OpenMW source

`apps/openmw/mwrender/npcanimation.cpp` `HeadAnimationTime::update(dt)` directly maps the active spoken-voice sound loudness to the NIF talk interval each update with no temporal filtering:
`mValue=mTalkStart+(mTalkStop-mTalkStart)*min(1.f, getSaySoundLoudness(mReference)*2)`.
It instantly switches back to blink interval when `sayActive(ref)` is false.

**Important correction made during development:**
`NiMorphData` has three targets. Target 0 is neutral base, target 1 is TALK (time 0 through 1.3333), target 2 is BLINK (time 1.4 through 2). OpenMW `components/nif/data.cpp` explicitly reads each target's float keys **before** its vertex offset array. An initial Alpha04 attempt altered the *blink*, not talk, interpolation curve. **DO NOT INSTALL THAT FIRST BUILD.** It was rejected; the initially linked local ZIP path was overwritten with corrected bytes, and a new unambiguous name was used. Previously downloaded cached copies must be discarded.

The original talk curve already opens monotonically as voice amplitude increases; the earlier assertion that it closed with loudness was false because it examined the **blink** curve. This correction must be preserved in project continuity.

## Deliverables and boundaries

**Corrected Alpha04 PRIVATE runtime ZIP:**
`XB77_RedSun_Jiub_Alpha04_Corrected_Mouth_Private.zip`
SHA256 `562e82b45ce82f97057d699c0afb4892e96ae4548b9c6039ac9d4860fde60734`.

Contains *only* existing user-tested ESP, ear mesh, 4K diffuse DDS, and a revised Jiub head NIF under `Data/RedSun_OpenMW MODs`. 7,956 vertices, 15,544 triangles. Neutral pose and body part/UVs/normals/faces, animation keyframes and BLINK target are byte-identical to Alpha03. Only target 1's vertex displacements in the lip region are changed: slightly raises upper lip, lowers lower lip, and widens corners when spoken morph is active. ZIP integrity and offline geometry checks pass. The full talk pose still looks stretched on a single surface; **mouth cavity, teeth, tongue and proper spoken phonemes NOT implemented**. Native Windows user playtest pending.

**Separate optional source-only C++ patch:** `RedSun_SmoothSpeech_HeadAnimationTime.patch`. Implements per-head attack/release envelope (45 ms attack, 90 ms release), per-frame dt compensation and soft end-of-speech tail in `HeadAnimationTime`. Companion standalone C++17 test passed consistent mathematical timing at 30/60/120 FPS. **NOT compiled into the user's XB77 Red Sun engine**; no claim of native compile/working EXE. Patch must be verified against the *exact* Red Sun OpenMW source revision, compiled and tested for all NPCs before calling it a working temporal smoothing fix. Source ZIP `XB77_RedSun_Jiub_Alpha04_Editable_Sources.zip`.

Workbook `XB77_RedSun_Jiub_Alpha04_Excel_QA.xlsx`: 15 offline PASS, 2 PENDING, 1 NOT COMPLETE. Contains a synthetic envelope plot—not captured actual engine audio data. Do not substitute its results for native gameplay proof.

### Reference source locations
- https://github.com/OpenMW/openmw/blob/master/apps/openmw/mwrender/npcanimation.cpp
- https://github.com/OpenMW/openmw/blob/master/components/nif/data.cpp
- https://github.com/OpenMW/openmw/blob/master/components/nifosg/controller.hpp

## Next release gate
Native Red Sun source integration and compile; voiced NPC playtest and eyelid response; a real mouth topology with cavity/teeth/tongue; fallback/rollback. Keep third-party mod artwork excluded; preserve original game files and landmass restriction.
