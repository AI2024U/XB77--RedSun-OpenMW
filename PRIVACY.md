# Privacy policy — XB77 Red Sun OpenMW

**Public source preparation, version 2026-11-21.**

XB77 is a local, standalone OpenMW-based game distribution and does not provide a project-operated player account or telemetry server. The first-time wizard source reviewed for this release-preparation work selects local Morrowind game data and writes a local configuration file; it has no explicit network-client imports. The OpenMW engine, launcher, plugins, operating system, connected services and third-party modifications may behave independently; no unsupported blanket guarantee about all network activity is made.

## Local data

- Morrowind data folder chosen by the player.
- Portable configuration and settings: `XB77_Portable/Config/`.
- Saves, screenshots and other per-user files: `XB77_Portable/UserData/`.
- Logs generated during gameplay may include machine-specific paths, usernames or enabled-mod names. **Do not upload logs publicly without review/redaction.**

## External data and network behavior

No XB77-owned telemetry or remote-account service is part of the documented wizard. We have not completed an independent network audit of every third-party runtime component; check this policy again before public binary distribution. When users explicitly open GitHub, Nexus Mods or other websites, those third-party services apply their own privacy policies. Third-party mods may implement separate functions and policies.

## System changes, installation and removal

The intended release is extracted into a user-selected writable folder, does not require administrator privileges, and only configures files within its own XB77 portable directory. It points to the existing Morrowind game files instead of copying them. To uninstall, close the application and delete the extracted XB77 directory; back up local saves first. Verify these behaviors on a clean Windows machine before any public release.

## Contact and questions

Use [GitHub Issues](https://github.com/AI2024U/XB77--RedSun-OpenMW/issues) for general questions, but **never post private logs, passwords, keys, or personally identifying data in a public issue**.
