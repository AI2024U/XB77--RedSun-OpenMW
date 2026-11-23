# XB77 Red Sun Jiub Alpha05 — mouth aperture and native audio-speech gate

**Date:** 2026-11-22 Pacific. **Release status:** PRIVATE UNVERIFIED MESH TEST. NO ACCEPTED NATURAL SPEECH FIX.

## User request and demonstrated problem
The user's Nov 22 21:04 gameplay recording showed an XB77 original custom head loading correctly but lips nearly closed during approximately 9–15 seconds, with hard mouth/chin profile. The three requested repairs are (1) check Jiub's real OpenMW speech-signal, (2) integrate/test smooth jaw timing, (3) improve 3D mouth aperture and interior.

## Actual changes delivered today
- Compared against exact OpenMW public release tag **openmw-52-rc1** `apps/openmw/mwrender/npcanimation.cpp`. Confirmed `HeadAnimationTime::update` uses `sayActive(mReference)` and directly maps `getSaySoundLoudness(mReference) * 2` to the morph interval without temporal filtering.
- Built source-only patch `RedSun_0_52_RC1_Jiub_Speech_Diagnostics_and_Envelope.patch` with per-head 45 ms attack / 90 ms release exponential filtering. Adds opt-in `XB77_SPEECH_DIAGNOSTICS` logging at 10 Hz **for NPC ID `chargen name` only**, including active, input, target, filtered, morphTime and dt; avoids logging unrelated NPC audio. Patch matches a reconstructed RC1 fixture. **It has not been applied/compiled against the exact customized Red Sun source; it does not modify the user's portable EXE.**
- Compiled and ran standalone C++17 speech-response tests at **30/60/120 FPS**; tests also verified release, silent source, nonfinite input and isolated per-head state. This tests the filtering mathematics and mock voice, not OpenMW.
- Created an **authored 3D mouth-aperture prototype** by replacing a narrow strip in our own Jiub custom head and inserting actual inset dark cavity triangles. Old custom head **7,956 vertices / 15,544 triangles**, Alpha05 **7,992 vertices / 15,576 triangles**. The NIF has the original neutral/talk/blink morph controller timing, preserved original old-vertex blink offsets and the same filenames. NIF visually rendered in neutral, half-talk, full-talk and profile. Unlike Test14 resampling, this implements a true opening backed by geometry. **The profile remains angular; not accepted as production-quality animation/art.**
- Independent runtime ZIP audit: **33 PASS / 0 FAIL**, original ESP, 4K DDS and ear mesh bytes unchanged, no landmass data, the ZIP root is exactly `Data/RedSun_OpenMW MODs/`. All three known morph arrays have valid geometry at neutral, half-talk, full-talk and blink.
- Editable source ZIP contains C++ patch, head-model generator, render/verification scripts, C++ mock test, and neutral/talk/blink OBJ sources. User-facing Excel workbook has offline results and native acceptance gate.

## Artifacts (user-private; do not upload game-derived NIFs to GitHub)
- `XB77_RedSun_Jiub_Alpha05_Mouth_Aperture_Private_Test.zip` SHA256 `2ea028810fca1daa8ab59ac10ac61b371e4e95128e514aac416656e981144010`
- `XB77_RedSun_Jiub_Alpha05_Editable_Engine_Sources.zip` SHA256 `19b72965b2432d68a71ce1046c8c577ecf1f5eeae5b080f090738dd2b52a4c63`
- `XB77_RedSun_Jiub_Alpha05_Engineering_QA.xlsx` (four worksheets)
- `XB77_Jiub_Alpha05_Mouth_Aperture_Offline_Review.png`

## Remaining acceptance gates — mandatory
1. Get **the exact customized Red Sun OpenMW Windows engine source checkout** and its build tools and **compile a separate portable candidate**; no engine source/executable is present in the current workspace. Do NOT claim the C++ patch is installed in a mod ZIP.
2. Reproduce Jiub speech with an audible voice and capture `XB77_JIUB_SPEECH active=1` plus varying nonzero `input` from same-run portable `openmw.log`. If absent, fix voice routing first. A subtitle is not proof of active voice playback.
3. Verify the filtered morph follows speech at 30/60 FPS and blinking resumes at voice end.
4. Improve profile/lip topology further (current lip corners and chin still angular), add proper inner mouth, tongue/teeth if desired, test clipping from multiple views. A 4-pose offline preview does not demonstrate natural spoken phonemes.
5. Maintain independent portable profiles, controller support, Red Sun icon, working wizard and high-contrast features. Restore Alpha04 head by overwriting its NIF; ESP remains `XB77_Jiub_OriginalArt_Alpha02.esp`.
6. NO hourly automation. NO third-party character art. NO landmass files.

**Decision:** Alpha05 is a meaningful source and private geometry prototype, **not** a fixed native voice-animation release. Don't confuse structural test passes with successful in-game engine integration.
