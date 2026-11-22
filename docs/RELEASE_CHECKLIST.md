# Public release gates — XB77 Red Sun OpenMW

**A release is not complete until every required gate is checked and evidenced.**

## Done

- [x] New separate public repo created without importing private Git history
- [x] GPLv3 license in public repository
- [x] Document project purpose, requirements and install concept
- [x] Create privacy, security, contribution and signing-policy pages
- [x] Publish reviewed text-based XB77 patch scripts (not yet complete build source)

## Still required — BLOCKERS

- [ ] Complete corresponding source for **every** modified OpenMW binary
- [ ] Public, reproducible/reviewable build of engine + launcher + custom wizard
- [ ] Verify asset licensing, especially Morrowind-derived wizard background; replace it if permission is unavailable
- [ ] Confirm third-party DLL/Qt/font/runtime redistribution and license notices
- [ ] Validate no private names, addresses, paths, emails, credentials, logs, recordings, private branches or old commits leak
- [ ] **BLOCKER:** Both `openmw.exe` and `openmw-launcher.exe` must launch from a normal Windows double-click with the isolated portable profile; no CMD, BAT, or PowerShell wrappers; no pink/magenta rendering. A native-entrypoint candidate is in private QA, not yet verified
- [ ] Fresh Windows installation with only legal Morrowind Data Files, no other OpenMW installed
- [ ] Confirm native Xbox menus, mouse/keyboard focus, ON/OFF toggle persistence, save/load and one-only-highlight behavior
- [ ] Verify portable logs/saves and uninstall instructions on a second machine
- [ ] Build and publish a complete corresponding GPL source archive linked to the same release
- [ ] Publish Windows release with checksums and honest unsigned/signed designation
- [ ] For SignPath: confirm upstream signed-release rule and recognized fork/branch relationship, project reputation and approval
- [ ] Only after approval: SignPath or other valid Authenticode signatures for applicable EXEs, verify publisher/metadata/timestamp
- [ ] Full Nexus listing, accessibility images, credits, license notices and safe install/uninstall steps

Public releases MUST NOT assert a valid signature, SignPath backing, official OpenMW endorsement or warning-free SmartScreen until independently proven.
