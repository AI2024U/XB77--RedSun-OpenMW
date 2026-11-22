#!/usr/bin/env python3
"""Fail-closed XB77 landmass output gate. Standard-library only; no game assets shipped."""
import argparse
import json
from pathlib import Path
import re
import struct
import sys
import zipfile

TERRAIN = re.compile(r"(?:^|[/_. -])(?:terrain|landscape|landmass|ground|grass|sand|snow|dirt|road|ashlands|soil|cliff|mudflat|muck|lava|cobble|groundcover)(?:$|[/_. -])", re.I)
APPROVED = ("textures/tx_b_n_", "textures/tx_b_f_", "textures/tx_b_m_", "textures/tx_a_", "textures/tx_c_", "textures/tx_w_", "textures/tx_cloth_", "textures/tx_armor_", "textures/tx_weapon_", "meshes/b/", "meshes/a/", "meshes/c/", "meshes/w/")
ALLOWED = (".dds", ".tga", ".png", ".nif")
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

def validate_zip(filename, terrain_stems):
    seen = set()
    with zipfile.ZipFile(filename) as z:
        if z.testzip() is not None: raise ValueError("corrupt ZIP member")
        for item in z.infolist():
            path = normalize(item.filename.rstrip("/"))
            if path in seen: raise ValueError("duplicate ZIP path")
            seen.add(path)
            if item.is_dir(): continue
            if (item.external_attr >> 16) & 0o170000 == 0o120000:
                raise ValueError("symlink forbidden")
            suffix = Path(path).suffix
            if TERRAIN.search(path) or Path(path).stem in terrain_stems:
                raise ValueError("landmass override forbidden: " + path)
            if path == "xb77_redsun_4k_overhaul.esp":
                validate_esp(z.read(item))
            elif suffix not in ALLOWED or not path.startswith(APPROVED):
                raise ValueError("unapproved output path: " + path)
    if "xb77_redsun_4k_overhaul.esp" not in seen:
        raise ValueError("missing ESP")
    return {"checked_members": len(seen), "protected_ltex_stems": len(terrain_stems)}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("zip", type=Path)
    p.add_argument("--masters", nargs=3, type=Path, required=True, help="Local original Morrowind, Tribunal, Bloodmoon ESM paths")
    args = p.parse_args()
    try:
        if sorted(x.name.casefold() for x in args.masters) != sorted(MASTER_NAMES):
            raise ValueError("exactly the three original master ESMs are required")
        print(json.dumps(validate_zip(args.zip, read_ltex(args.masters)), indent=2))
    except (ValueError, OSError, zipfile.BadZipFile) as exc:
        print("BLOCKED: " + str(exc), file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
