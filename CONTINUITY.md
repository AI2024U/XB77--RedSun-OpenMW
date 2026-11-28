# XB77 Continuity — RedSun OpenMW — public source and release status

**Established:** 2026-11-27 (America/Los_Angeles)  
**Repository:** AI2024U/XB77--RedSun-OpenMW  
**Permanent global standards:** [XB77_GLOBAL_WORKFLOW_POLICY.md](XB77_GLOBAL_WORKFLOW_POLICY.md)

## Mandatory first step in EVERY new chat

Read this file, [XB77_GLOBAL_WORKFLOW_POLICY.md](XB77_GLOBAL_WORKFLOW_POLICY.md), and the repository's README / referenced engineering documents. Check the latest branch/commit and actual GitHub run logs before claiming a build worked or modifying approved files.

## Project-specific continuity

Read README.md and docs/DEVELOPMENT_STATUS_2026-11-23.md. This is a PUBLIC repository: publish only public-safe source, instructions and verified release evidence. Do not mirror the private engine, game binaries, development logs, secrets or incomplete release claims.

## Critical cross-project lesson — GitHub and workflow dispatch

The installed ChatGPT GitHub connector can commit files and inspect run logs but currently does not expose a direct new-workflow `workflow_dispatch` operation. This is NOT a repository permission fix. A narrowly filtered, user-authorized GitHub push-trigger approach has been configured ONLY in a separate private XB77 NPC project; it is not installed or validated in this repository. Do NOT enable trigger-on-all-push or create a new workflow as a workaround without explicit user authorization and billing protection.

If the user requests execution, distinguish:
- **Source committed** from **syntax independently tested** from **actual Blender/NIF/DDS/OpenMW execution** from **user visual approval**.
- **RUN ALLOWED** only as a specifically scoped diagnostic after actual preflight plus billing authorization.
- **DO NOT RUN YET** when essential verification is absent or potential charges have not been accepted.
- Never fabricate workflow inputs, exact commit, live run ID, rendered screenshots or artifact status.

## Every workflow handoff

Include a prominent clickable GitHub workflow link/button; exact `main` or actual selected branch, verified full commit SHA, inputs, manual Run workflow instructions, billing verification, and explicit RUN ALLOWED or DO NOT RUN YET. Repair existing source first, verify actual job logs, preserve backups and native asset hashes, and do not claim unexecuted fixes are proven.

## Working rules

No AI-generated project textures/imagery; genuine Blender/OpenMW evidence only. No installations on the user's PC. Do not modify unrelated projects or their baselines. No unauthorized paid builds. File names use plain underscores without percent symbols. Keep GitHub public/private boundaries.

**Restart message:** "Continue XB77 in AI2024U/XB77--RedSun-OpenMW. Read CONTINUITY.md, XB77_GLOBAL_WORKFLOW_POLICY.md and README.md first; verify GitHub commits and real Actions logs; preserve approved baselines and binary backups. Give a clickable GitHub workflow link with exact branch/SHA/inputs/billing and RUN ALLOWED or DO NOT RUN YET. No paid run, fabricated renders or new workflow without authorization."
