# XB77 Red Sun 4K Overhaul — Test 03 Release Gate QA

Status as of 2026-11-22: **source and synthetic QA verified, no playable 4K overhaul yet.**

## Completed in this milestone

- Hardened `tools/xb77_landmass_release_gate.py` on the independent `xb77-4k-overhaul-dev` branch.
- Corrected the canonical source and regression tests to match the locally executed bytes **exactly**:
  - Gate Git blob SHA: `35d3da49adf034a3806fc6deefbef76d19b717c8`
  - Tests Git blob SHA: `bc9405569261ccc50bcdfb6093d28c000f339516`
- 17 synthetic release-gate regression tests passed locally.
- 14 earlier audit/landmass/inventory tests passed locally.
- **31 total Python tests passed** in the assembled Test 03 tools package.
- Read-only parse of the user-supplied Morrowind, Tribunal, Bloodmoon masters found **134 unique LTEX terrain texture stems**. Terrain-name alias in a synthetic asset was rejected against the genuine LTEX set.
- Test 03 development-only package verified with 12 non-game-data files; full ZIP integrity check passed. SHA256 `d8301a32ddeeb74c6d3caf03c0edbe2dd0bcb27692fc4538be0cf61565633f25`.

## Safeguards added

1. Enforce texture-vs-mesh file extensions and recognizable DDS/PNG/TGA/NIF headers.
2. Reject malformed, zero-byte, oversize, unknown, unsafe, terrain-named, and protected LTEX-name replacement assets.
3. Continue rejecting `LAND`/`LTEX` plugin records and requiring an ESP filename for a proposed package.
4. Optional `--release` mode additionally demands both texture and mesh replacements, an installation README, declared author/license/origin per replacement, and exact SHA-256 checksums for all replacements.
5. No Bethesda BSA, ESM, original art, or private paths were added to the repository or the test tools ZIP.

## QA limits and next work

- Tests use synthetic byte headers and records; **no** genuine 4K replacement textures, improved high-poly meshes, or final selectable ESP have been produced.
- Header recognition alone does not establish complete image payload validity, original art detail, NIF mesh integrity, polygon quality, licensing permission or OpenMW functionality.
- Package `--release` validation is a **structural/provenance gate**, not final rights or gameplay certification.
- No paid Windows compilation or in-game Red Sun regression test was run.
- Next: catalog license-cleared source art, establish real output-versus-original content coverage and dimensions, build and inspect genuinely improved race head/body meshes and seamless textures, and independently run graphical in-game verification. Keep all terrain assets completely untouched.

## Local test commands

```sh
python -m unittest discover -s tests -v
python tools/xb77_landmass_release_gate.py Proposed_Mod.zip --masters Morrowind.esm Tribunal.esm Bloodmoon.esm --release
```

The second command requires the user's own original master ESM files and a real proposed ZIP and is intentionally not run as a playable-release test until such a ZIP exists.
