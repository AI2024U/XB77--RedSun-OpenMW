# Installation — intended first-time Windows experience

**This describes the planned final public Windows package, which has not yet been published.** Follow it only after a public release has passed the [release checklist](RELEASE_CHECKLIST.md).

1. Download the official `XB77 Red Sun OpenMW.zip` from this repository's Releases page or linked Nexus Mods page and verify its published SHA-256 checksum.
2. Extract all files to a **new, writable directory**, outside `Program Files` and outside another OpenMW installation.
3. Double-click the included `openmw-wizard.exe` (blue wand icon).
4. Select the folder containing the legally owned `Morrowind.esm` and `Morrowind.bsa`; the wizard should reference existing data, not copy it.
5. Start `openmw-launcher.exe` and click Play.
6. For the accessibility effect, use **Options → Prefs → XB77: High-Contrast Dialogue Selection**.
7. Controller menus are intended to default ON. Keyboard and mouse should remain functional.

## Portable files and uninstall

The intended layout stores local settings/logs in `XB77_Portable/Config` and user data in `XB77_Portable/UserData`. Before deleting the XB77 directory to uninstall, back up its saves. Do **not** delete or modify the original Morrowind directory.

## If Windows warns about an unknown publisher

Do not disable Defender or SmartScreen. A GitHub download or an embedded icon is not an Authenticode signature. Verify the project's actual release status before using any unsigned build. Signed release instructions will be posted only after an approved signing workflow.
