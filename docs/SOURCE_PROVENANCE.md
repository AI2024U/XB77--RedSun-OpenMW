# Source provenance and reproducibility

**Current status: partial source published; no complete, reproducible source-to-binary public release yet.**

## Upstream and custom changes

- **Engine:** OpenMW 0.52.0 RC1 (GitLab tag `openmw-52-rc1`), under GNU GPLv3.
- **Upstream:** https://gitlab.com/OpenMW/openmw
- **Derived engine modifications:** dialogue C++ focus/navigation, a native Prefs option, custom MyGUI skins, Red Sun Win32 executable icons, and optional main-menu emblem.
- **Wizard:** a custom Windows first-time setup tool. Current development wizard uses Go and contains a game-derived background image with redistribution rights **not yet confirmed**, so it is **not cleared for public binary/source distribution** in its existing form.
- **Source patches:** see `src/patches/`. Additional original engine patch archive and source-to-binary mapping are pending redaction and independent review.

## Do not misrepresent provenance

The published patch scripts by themselves are **not** complete corresponding source for the previously tested binary. The previous engine workflow relied on a private `XB77_v0.9_Lua_Native_Bridge_Source_Experimental.zip` source archive. It must be reviewed, extracted as source and made publicly available, or replaced by a complete, auditable patch series. **Do not copy or publish the original ZIP blindly.**

## Requirements before binary publication

1. Fully publish the modified OpenMW source or an exact upstream revision plus complete machine-applicable patch series and required build scripts.
2. Publish reviewed custom wizard source **and only redistributable assets**, with a documented deterministic build.
3. Pin dependencies, record source SHA and build tool versions.
4. Produce a fresh binary from public source in a public GitHub Actions run; verify it on clean Windows.
5. Release the binary together with complete corresponding source and associated license notices, checksums, and a clear `unsigned` status until signing is approved.
