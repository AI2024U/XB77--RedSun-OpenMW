#!/usr/bin/env python3
"""Fail-closed XB77 landmass output gate. Standard-library only; no game assets shipped."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import sys
import zipfile

TERRAIN = re.compile(r"(?:^|[/_. -])(?:terrain|landscape|landmass|ground|grass|sand|snow|dirt|road|ashlands|soil|cliff|mudflat|muck|lava|cobble|groundcover)(?:$|[/_. -])", re.I)
APPROVED = ("textures/tx_b_n_", "textures/tx_b_f_", "textures/tx_b_m_", "textures/tx_a_", "textures/tx_c_", "textures/tx_w_", "textures/tx_cloth_", "textures/tx_armor_", "textures/tx_weapon_", "meshes/b/", "meshes/a/", "meshes/c/", "meshes/w/")
TEXTURE_EXT = (".dds", ".tga", ".png")
# Do not allow texture data disguised as meshes or NIFs disguised as textures.
MAX_FILE_BYTES = 256 * 1024 * 1024
MAX_ARCHIVE_BYTES = 12 * 1024 * 1024 * 1024
METADATA_FILES = {"readme.txt", "asset_provenance.json"}
MASTER_NAMES = ("morrowind.esm", "tribunal.esm", "bloodmoon.esm")

def normalize(path):
    if not isinstance(path, str) or not path or "\x00" in path or "%" in path:
        raise ValueError("unsafe asset path")
    p = path.replace("\\", "/")
    if p.startswith("/") or re.match(r"^[a-z]:", p, re.I) or ":" in p or any(x in ("", ".", "..") for x in p.split("/")):
        raise ValueError("unsafe asset path: " + path)
    return p.casefold()

def read_ltex(esms):
    stems = set()
    for filename in esms:
        with open(filename, "rb") as f:
            total = Path(filename).stat().st_size
            while f.tell() < total:
                hdr = f.read(16)
                if len(hdr) != 16: raise ValueError("truncated ESM record")
                size = struct.unpack_from("<I", hdr, 4)[0]
                if size > total - f.tell(): raise ValueError("bad ESM record size")
                if hdr[:4] != b"LTEX":
                    f.seek(size, 1)
                    continue
                data = f.read(size)
                pos = 0
                while pos < len(data):
                    if len(data)-pos < 8: raise ValueError("truncated LTEX subrecord")
                    kind = data[pos:pos+4]
                    n = struct.unpack_from("<I", data, pos+4)[0]
                    pos += 8
                    if n > len(data)-pos: raise ValueError("bad LTEX subrecord")
                    if kind == b"DATA":
                        raw = data[pos:pos+n].split(b"\x00", 1)[0].decode("cp1252")
                        path = normalize(raw)
                        stems.add(Path(path).stem)
                    pos += n
    return stems

def validate_esp(data):
    pos = 0
    if len(data) < 16 or data[:4] != b"TES3": raise ValueError("not a TES3 plugin")
    while pos < len(data):
        if len(data)-pos < 16: raise ValueError("truncated plugin record")
        typ = data[pos:pos+4]
        size = struct.unpack_from("<I", data, pos+4)[0]
        pos += 16
        if size > len(data)-pos: raise ValueError("invalid plugin record size")
        if typ in (b"LAND", b"LTEX"): raise ValueError("forbidden landscape record")
        pos += size

def inspect_asset(z, item, category):
    """Validate basic file identity, NOT actual visual detail or NIF geometry quality."""
    path = normalize(item.filename)
    if item.file_size == 0 or item.file_size > MAX_FILE_BYTES:
        raise ValueError("invalid asset size: " + path)
    ext = Path(path).suffix
    if category == "mesh":
        if ext != ".nif":
            raise ValueError("wrong mesh extension: " + path)
        with z.open(item) as f:
            prefix = f.read(128)
        if not (prefix.startswith(b"NetImmerse File Format") or prefix.startswith(b"Gamebryo File Format")) or b"\n" not in prefix:
            raise ValueError("invalid NIF header: " + path)
        return {"kind": "mesh"}
    if ext not in TEXTURE_EXT:
        raise ValueError("wrong texture extension: " + path)
    with z.open(item) as f:
        prefix = f.read(128)
    if ext == ".dds":
        if len(prefix) < 128 or prefix[:4] != b"DDS " or struct.unpack_from("<I", prefix, 4)[0] != 124:
            raise ValueError("invalid DDS header: " + path)
        height, width = struct.unpack_from("<II", prefix, 12)
    elif ext == ".png":
        if len(prefix) < 24 or prefix[:8] != b"\x89PNG\r\n\x1a\n" or prefix[12:16] != b"IHDR" or struct.unpack_from(">I", prefix, 8)[0] != 13:
            raise ValueError("invalid PNG header: " + path)
        width, height = struct.unpack_from(">II", prefix, 16)
    else:
        if len(prefix) < 18 or prefix[2] not in (1, 2, 3, 9, 10, 11) or prefix[16] not in (8, 16, 24, 32):
            raise ValueError("invalid TGA header: " + path)
        width, height = struct.unpack_from("<HH", prefix, 12)
    if width < 1 or height < 1 or width > 16384 or height > 16384:
        raise ValueError("invalid texture dimensions: " + path)
    return {"kind": "texture", "width": width, "height": height}


def verify_provenance(z, asset_names):
    """Require exact checksums and a declared origin; licenses still need human review."""
    try:
        raw = z.read("asset_provenance.json")
    except KeyError:
        # Case-insensitivity handled by normalize and metadata member validation.
        matches = [i for i in z.infolist() if normalize(i.filename) == "asset_provenance.json"]
        if len(matches) != 1:
            raise ValueError("release requires asset_provenance.json")
        raw = z.read(matches[0])
    if len(raw) > 5 * 1024 * 1024:
        raise ValueError("oversized provenance manifest")
    try:
        manifest = json.loads(raw)
    except (ValueError, UnicodeDecodeError) as exc:
        raise ValueError("invalid provenance manifest") from exc
    if not isinstance(manifest, dict) or not isinstance(manifest.get("assets"), list):
        raise ValueError("provenance assets list required")
    declared = {}
    for row in manifest["assets"]:
        if not isinstance(row, dict):
            raise ValueError("invalid provenance row")
        name = normalize(row.get("path"))
        if name in declared:
            raise ValueError("duplicate provenance path")
        if not all(isinstance(row.get(k), str) and row[k].strip() for k in ("author", "license", "origin", "sha256")):
            raise ValueError("incomplete provenance metadata: " + name)
        if not re.fullmatch(r"[a-fA-F0-9]{64}", row["sha256"]):
            raise ValueError("invalid provenance digest: " + name)
        declared[name] = row
    if set(declared) != set(asset_names):
        raise ValueError("provenance paths differ from packaged assets")
    for member in z.infolist():
        name = normalize(member.filename.rstrip("/"))
        if name not in declared:
            continue
        h = hashlib.sha256()
        with z.open(member) as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
        if h.hexdigest() != declared[name]["sha256"].lower():
            raise ValueError("provenance checksum mismatch: " + name


def validate_zip(filename, terrain_stems, *, release=False):
    seen = set()
    asset_names = set()
    kinds = {"texture": 0, "mesh": 0}
    with zipfile.ZipFile(filename) as z:
        if sum(i.file_size for i in z.infolist()) > MAX_ARCHIVE_BYTES:
            raise ValueError("unreasonable total archive size")
        if z.testzip() is not None: raise ValueError("corrupt ZIP member")
        for item in z.infolist():
            path = normalize(item.filename.rstrip("/"))
            if path in seen: raise ValueError("duplicate ZIP path")
            seen.add(path)
            if (item.external_attr >> 16) & 0o170000 == 0o120000:
                raise ValueError("symlink forbidden")
            if item.is_dir():
                continue
            suffix = Path(path).suffix
            if TERRAIN.search(path) or Path(path).stem in terrain_stems:
                raise ValueError("landmass override forbidden: " + path)
            if path == "xb77_redsun_4k_overhaul.esp":
                validate_esp(z.read(item))
            elif path in METADATA_FILES:
                if item.file_size > 5 * 1024 * 1024:
                    raise ValueError("oversized metadata file: " + path)
            elif path.startswith(APPROVED):
                category = "texture" if path.startswith("textures/") else "mesh"
                inspect_asset(z, item, category)
                kinds[category] += 1
                asset_names.add(path)
            else:
                raise ValueError("unapproved output path: " + path)
        if "xb77_redsun_4k_overhaul.esp" not in seen:
            raise ValueError("missing ESP")
        if release:
            if not all(kinds.values()):
                raise ValueError("release requires real texture and mesh assets")
            if "readme.txt" not in seen:
                raise ValueError("release requires README.txt")
            verify_provenance(z, asset_names)
    return {"checked_members": len(seen), "protected_ltex_stems": len(terrain_stems),
            "textures": kinds["texture"], "meshes": kinds["mesh"], "release_gate": release,
            "note": "Headers and hashes are not proof of 4K detail, high-poly geometry, license rights, or in-game compatibility"}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("zip", type=Path)
    p.add_argument("--masters", nargs=3, type=Path, required=True, help="Local original Morrowind, Tribunal, Bloodmoon ESM paths")
    p.add_argument("--release", action="store_true", help="Require both asset types and per-file provenance hashes")
    args = p.parse_args()
    try:
        if sorted(x.name.casefold() for x in args.masters) != sorted(MASTER_NAMES):
            raise ValueError("exactly the three original master ESMs are required")
        print(json.dumps(validate_zip(args.zip, read_ltex(args.masters), release=args.release), indent=2))
    except (ValueError, OSError, zipfile.BadZipFile) as exc:
        print("BLOCKED: " + str(exc), file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
