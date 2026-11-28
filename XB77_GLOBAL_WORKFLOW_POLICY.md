# XB77 — Permanent Global Workflow and Continuity Policy

**Effective:** 2026-11-27 (America/Los_Angeles)  
**Scope:** Every XB77 project/repository, public and private.  
**Status:** A workflow or repository file change does not prove a build or engine test passed.

## Global handoff contract

Every workflow handoff, in every new chat and across all XB77 repositories, MUST include:

1. A prominent, clickable **Open GitHub Workflow** control linking to the real existing workflow. In chat use a large clickable button when available; in Markdown use the actual workflow URL. Never fabricate the link.
2. Exact repository, workflow name, branch, verified full head commit SHA, input values or "no custom inputs", and the step-by-step execution procedure.
3. GitHub Actions billing protection verification *before execution*. Do not imply that an "included-minutes" log line enforces billing. If the GitHub account's available minutes, budgets and stop-use controls are not independently visible, explicitly say **BILLING NOT VERIFIED**. User must confirm zero-extra-charge protection or separately authorize potential charges.
4. Diagnose actual failures from the original run's GitHub job logs; repair the **existing** source and workflow before considering any new workflow. Confirm changes with committed SHA and readback.
5. Independent checks as relevant: actual Bash parser execution; Python parser/compile checks; Blender model geometry and evaluated modifiers; topology, weights and UV preservation; NIF import/export/native inspection; DDS file existence, hashes and OpenMW asset access; genuine unobstructed OpenMW rendering, movement and logs. Source-only checks must never be called engine proof.
6. Exactly one unambiguous execution status: **RUN ALLOWED** (specify diagnostic vs release, exact scope and verified billing) or **DO NOT RUN YET** (state concrete blocker). Do not alternate conclusions without new evidence.
7. Exact manual instructions when applicable: open workflow; select Run workflow; choose branch; verify SHA and inputs; confirm included minutes and additional-charge protection; click green Run workflow; provide run URL/artifacts for independent verification.

## GitHub connector — verified capabilities and limitations

- The installed ChatGPT GitHub connector can read repositories, edit text files, commit and inspect GitHub Actions runs and logs.
- Its currently exposed actions **do not include** the GitHub REST `workflow_dispatch` operation for starting a fresh run directly.
- The ability to commit to a repository is **not** proof that the plugin's permissions were expanded. Do not say "GitHub connection fixed" without the new operation appearing.
- **NPC-Dunmer-2k only, at this policy's creation:** the existing `.github/workflows/test06-attachment-runtime.yml` also accepts a tightly filtered push to `ci/xb77-test06.run` on `main`. The job runs only if the push head commit message starts with the exact prefix `[XB77_RUN_TEST06]`. This *repository-side bridge* is separate from native workflow_dispatch; its first live trigger has **not** been verified. No trigger file was committed when it was installed.
- That trigger bridge **does not exist automatically in other XB77 repos**. Never create a replacement workflow or turn on broad push triggers to imitate it.
- For a future bridge-triggered run, require explicit user request, exact approved commit, source preflight, confirmed billing safety or separately approved costs, deliberate trigger-file commit, and a **real new run ID** from GitHub. A successful commit alone is not a successful dispatch.
- Never rerun an old failed GitHub job as a substitute for a new run on corrected code; rerun generally uses the old run's commit.

## Permanent XB77 engineering rules

- No AI-generated or AI-edited project textures, character renders or gameplay proof. Use actual Blender/OpenMW and native NIF/DDS work; label diagnostic visuals accurately.
- Never install project software on the user's personal computer; use isolated remote/GitHub runners or assistant-side verification when available.
- Preserve original binary models/assets; back up approved .blend, .nif, .dds and genuine captures with SHA256 manifests. Never claim GitHub binary backups exist without verifying the objects and links.
- Do not silently change game asset identifiers, saved-game script IDs, approved baselines, or separate project boundaries.
- Do not approve a build based on workflow existence, synthetic images, source linting alone, hash-only validation, or unreviewed artifacts.
- Keep runtime releases clean (no debug/QA files or BAT/CMD in user releases), with simple underscore filenames and no percent symbols.
- User visual approval is required before claiming completed appearance/texture changes.
- Public repositories must not expose private game binaries, confidential run artifacts, tokens, private URLs or unpublished engineering data. This file is a PUBLIC-SAFE policy.

## Restart procedure for future chats

1. Read this file and the repository's `CONTINUITY.md` before modifying or running anything.
2. Verify the live repository branch/commit, workflow, last run's exact logs, artifacts, billing authorization and any project-specific constraints.
3. Continue from verified evidence, not assistant confidence or previous promises.
4. If an external limitation prevents execution, say so clearly and use a verified supported path; do not invent capabilities.
5. Show a clickable GitHub workflow control and clear RUN ALLOWED / DO NOT RUN YET decision on each workflow handoff.

**No paid builds or Actions dispatches are authorized merely by this document.**
