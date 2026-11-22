#!/usr/bin/env python3
"""Read-only asset / package preflight for XB77 4K OpenMW project.

Does not copy, extract, or distribute any Bethesda game data.
Does not claim to measure mesh topology, texture seams or in-game compatibility.
"""

from __future__ import annotations
import argparse
import json
import struct
from pathlib import Path

MASTER_FILES = (
    "Morrowind.esm", "Tribunal.esm", "Bloodmoon.esm",
    "Morrowind.bsa", "Tribunal.bsa", "Bloodmoon.bsa",
)
PLUGIN_NAME = "XB77_RedSun_4K_Overhaul.esp"
TEXTURE_FORMATS = {".dds", ".png", ".tga", ".bmp", ".jpg", ".jpeg"}
MESH_FORMATS = {".nif"}


def image_dimensions(path: Path):
    """Return pixel dimensions for common formats, or None if not readable.

    JPEG optionally uses Pillow; no image file is rewritten.
    """
    try:
        with path.open("rb") as handle:
            head = handle.read(128)
        ext = path.suffix.lower()
        if ext == ".dds" and head[:4] == b"DDS " and len(head) >= 20:
            height, width = struct.unpack_from("<II", head, 12)
            return (width, height) if width and height else None
        if ext == ".png" and head[:8] == b"\x89PNG\r\n\x1a\n" and len(head) >= 24:
            width, height = struct.unpack_from(">II", head, 16)
            return (width, height) if width and height else None
        if ext == ".tga" and len(head) >= 18:
            width, height = struct.unpack_from("<HH", head, 12)
            return (width, height) if width and height else None
        if ext == ".bmp" and head[:2] == b"BM" and len(head) >= 26:
            width, height = struct.unpack_from("<ii", head, 18)
            return (abs(width), abs(height)) if width and height else None
        if ext in {".jpg", ".jpeg"}:
            try:
                from PIL import Image
                with Image.open(path) as im:
                    return im.size
            except ImportError:
                return None
    except (OSError, ValueError, struct.error):
        return None
    return None


def scan_assets(directory: Path, formats: set[str]):
    if not directory.is_dir():
        return []
    return sorted(
        (p for p in directory.rglob("*") if p.is_file() and p.suffix.lower() in formats),
        key=lambda p: p.as_posix().lower(),
    )


def asset_is_nif(path: Path):
    try:
        with path.open("rb") as f:
            head = f.read(96)
        return head.startswith((b"NetImmerse File Format", b"Gamebryo File Format"))
    except OSError:
        return False


def audit(game_data: Path, mod_data: Path):
    game_data = game_data.resolve()
    mod_data = mod_data.resolve()
    source_found = {filename: (game_data / filename).is_file() for filename in MASTER_FILES}
    textures = scan_assets(mod_data / "Textures", TEXTURE_FORMATS)
    meshes = scan_assets(mod_data / "Meshes", MESH_FORMATS)
    plugin = mod_data / PLUGIN_NAME

    tex_summary = []
    unknown_dimensions = []
    below_4k_review = []
    for file in textures:
        dims = image_dimensions(file)
        relative = file.relative_to(mod_data).as_posix()
        tex_summary.append({"file": relative, "dimensions": list(dims) if dims else None})
        if dims is None:
            unknown_dimensions.append(relative)
        elif max(dims) < 4096:
            below_4k_review.append(relative)

    invalid_nifs = [p.relative_to(mod_data).as_posix() for p in meshes if not asset_is_nif(p)]
    all_files = textures + meshes + ([plugin] if plugin.is_file() else [])
    bad_names = [p.relative_to(mod_data).as_posix() for p in all_files if "%" in p.name]
    normalized = [p.relative_to(mod_data).as_posix().casefold() for p in all_files]
    collisions = sorted({path for path in normalized if normalized.count(path) > 1})

    plugin_header = None
    if plugin.is_file():
        with plugin.open("rb") as f:
            plugin_header = f.read(4) == b"TES3"

    issues = []
    if not all(source_found.values()):
        issues.append("Missing at least one original game master or archive in the supplied game data folder")
    if not plugin.is_file():
        issues.append("Final plugin is absent; ESP authoring pending")
    elif not plugin_header:
        issues.append("ESP lacks expected TES3 header; plugin is not verified")
    if not textures:
        issues.append("No replacement textures provided yet")
    if not meshes:
        issues.append("No replacement NIF meshes provided yet")
    if unknown_dimensions:
        issues.append("Some texture dimensions could not be read")
    if invalid_nifs:
        issues.append("Some mesh files lack a recognized NIF signature")
    if collisions:
        issues.append("Case-insensitive duplicate asset paths detected")
    if bad_names:
        issues.append("Disallowed filename characters detected")

    return {
        "product": "XB77 Red Sun 4K Overhaul",
        "scope": ["Morrowind", "Tribunal", "Bloodmoon"],
        "original_game_files": source_found,
        "mod_scan": {
            "esp_filename": PLUGIN_NAME,
            "esp_present": plugin.is_file(),
            "esp_tes3_signature_only": plugin_header,
            "texture_count": len(textures),
            "mesh_count": len(meshes),
            "texture_dimensions": tex_summary,
            "textures_below_4k_for_review": below_4k_review,
            "unknown_texture_dimensions": unknown_dimensions,
            "invalid_nif_headers": invalid_nifs,
            "case_collision_paths": collisions,
            "disallowed_names": bad_names,
        },
        "manual_quality_gates": {
            "real_4k_detail_not_interpolation": "unverified",
            "correct_nif_topology_and_rigging": "unverified",
            "all_race_neck_wrist_ankle_seams": "unverified",
            "facial_shading_and_polygons": "unverified",
            "animations_and_armor": "unverified",
            "esp_openmw_launcher_activation": "unverified",
            "red_sun_windows_in_game_test": "unverified",
            "rights_and_license_review": "unverified",
        },
        "issues": issues,
        "preflight_pass": not issues,
        "release_ready": False,
        "release_ready_reason": "Requires actual asset coverage, licenses, native in-game tests and all manual quality gates; audit cannot certify release",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--game-data", type=Path, required=True, help="Your own Morrowind Data Files directory; never upload or redistribute it")
    parser.add_argument("--mod-data", type=Path, required=True, help="Local XB77_RedSun_4K_Overhaul folder")
    parser.add_argument("--report", type=Path, help="Write JSON report locally")
    args = parser.parse_args()
    result = audit(args.game_data, args.mod_data)
    rendered = json.dumps(result, indent=2)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 0 if result["preflight_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())