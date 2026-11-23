# XB77 Red Sun Jiub — Alpha04 follow-up video: native speech-animation QA

**Observed artifact:** User-provided 1920×1080, approximately 22.54-second recording `XB77 Red Sun OpenMW 2026-11-22 21-04-40.mp4`, supplied after corrected Alpha04 package. **Status:** NATURAL-SPEECH ACCEPTANCE FAIL; retain current successfully loading head and art.

## Grounded visual results

- Jiub's custom original head, red eyes and long ears remain visibly rendered in the prison ship scene; no large missing mesh/error marker is visible.
- During approximately **9–15 seconds**, the face is reasonably frontal and the mouth line remains nearly closed. No convincing repeating jaw-open/jaw-close speech cycle can be visually established while a dialogue subtitle box is present.
- The screenshot/video shows text and is accompanied by audio, but **a text subtitle does not prove that the NPC's own voice playback was active**. OpenMW normally drives talking morphs from the specific NPC sound source, not from text display or general mixed game sound. No per-NPC `sayActive` / `getSaySoundLoudness` native instrumentation was recorded. Do not assume causation without runtime trace.
- At the side view around 4–5 seconds, mouth and chin silhouette appears angular; native rig pose and morph activation at that frame are not confirmed.
- 115 old structural checks / 15 Alpha04 offline checks are not evidence of natural speech.
- Review contact and face frame contact sheets are private, sourced from the user's video; do not upload user footage to public repo.

## Scope of current Alpha04 ZIP

`XB77_RedSun_Jiub_Alpha04_Corrected_Mouth_Private.zip` contains four runtime files in `Data/RedSun_OpenMW MODs/`: head NIF, ear NIF, diffuse DDS, ESP. Its only change relative to working Alpha03 head is local geometry displacement in talk morph #1. It does **not** include or install any Red Sun engine executable or source patch. It cannot introduce audio-driven temporal smoothing by itself.

Separate prior `RedSun_SmoothSpeech_HeadAnimationTime.patch` was mathematically unit-tested but **has not been compiled or validated within the user's exact portable OpenMW build**.

## Release gate before further 'fixed' claims

1. Obtain exact XB77 Red Sun engine source revision and build process. Do not change installed portable EXE or other OpenMW installations.
2. Instrument `HeadAnimationTime::update` (NPC ref, `sayActive`, `getSaySoundLoudness`, `dt`, computed talk fraction), capture log synchronized to known voiced line.
3. If active values vary, integrate frame-rate-independent attack/release filtering, recompile and verify actual game behavior; if always inactive, diagnose voice event routing and NPC reference rather than trying a bigger NIF morph.
4. Model proper mouth aperture + inner-mouth surface and lips independently, then validate profile/intermediate pose, with all facial animation states.
5. Compare real in-game close-up before/after while speech audibly plays. Verify blink and neutral unchanged. No further ZIP release by blindly editing morph geometry.

**Hourly automation remains disabled. All future Red Sun mod ZIPs must use `Data/RedSun_OpenMW MODs/`.**