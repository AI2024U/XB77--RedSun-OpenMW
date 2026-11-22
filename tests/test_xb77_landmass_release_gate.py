"""Synthetic tests only. No Bethesda files or paid CI required."""
import io
import hashlib
import json
from pathlib import Path
import struct
import tempfile
import unittest
import zipfile

from tools.xb77_landmass_release_gate import normalize, read_ltex, validate_esp, validate_zip

def record(kind, payload=b""):
    return kind + struct.pack("<III", len(payload), 0, 0) + payload

def ltex(name):
    value = name.encode("ascii") + b"\0"
    return record(b"LTEX", b"DATA" + struct.pack("<I", len(value)) + value)

def dds(width=4096, height=4096):
    data = bytearray(128)
    data[:4] = b"DDS "
    struct.pack_into("<I", data, 4, 124)
    struct.pack_into("<II", data, 12, height, width)
    return bytes(data)

def nif():
    return b"NetImmerse File Format, Version 4.0.0.2\n" + b"\0" * 100

def png(width=4096, height=4096):
    return b"\x89PNG\r\n\x1a\n" + struct.pack(">I", 13) + b"IHDR" + struct.pack(">II", width, height) + b"\x08\x06\0\0\0" + b"\0" * 20

def archive(path, entries):
    with zipfile.ZipFile(path, "w") as z:
        for name, data in entries.items():
            z.writestr(name, data)

class GateTests(unittest.TestCase):
    def test_paths_reject_traversal_absolute_and_percent(self):
        for name in ("../Textures/x.dds", "/Textures/x.dds", "C:/x.dds", "textures//x.dds", "textures/%2e%2e/x.dds"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                normalize(name)

    def test_ltex_cross_extension(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d)/"Morrowind.esm"
            f.write_bytes(record(b"TES3") + ltex("textures/tx_ground_01.tga"))
            self.assertEqual(read_ltex([f]), {"tx_ground_01"})

    def test_land_and_ltex_rejected(self):
        for kind in (b"LAND", b"LTEX"):
            with self.subTest(kind=kind), self.assertRaisesRegex(ValueError, "landscape"):
                validate_esp(record(b"TES3") + record(kind))

    def test_malformed_plugin_rejected(self):
        with self.assertRaises(ValueError):
            validate_esp(record(b"TES3") + b"LAND")

    def test_good_candidate(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d)/"test.zip"
            archive(f, {"XB77_RedSun_4K_Overhaul.esp": record(b"TES3"), "Textures/tx_b_n_head.dds": dds()})
            self.assertEqual(validate_zip(f, set())["checked_members"], 2)

    def test_ltex_alias_blocked(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d)/"test.zip"
            archive(f, {"XB77_RedSun_4K_Overhaul.esp": record(b"TES3"), "Textures/tx_b_n_ground01.dds": b"test"})
            with self.assertRaisesRegex(ValueError, "landmass"):
                validate_zip(f, {"tx_b_n_ground01"})

    def test_unknown_asset_blocked(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d)/"test.zip"
            archive(f, {"XB77_RedSun_4K_Overhaul.esp": record(b"TES3"), "Textures/mystery.dds": b"test"})
            with self.assertRaisesRegex(ValueError, "unapproved"):
                validate_zip(f, set())

    def test_no_esp_blocked(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d)/"test.zip"
            archive(f, {"Textures/tx_b_n_head.dds": dds()})
            with self.assertRaisesRegex(ValueError, "missing ESP"):
                validate_zip(f, set())


    def test_extensions_match_file_category(self):
        for path, data in (("Textures/tx_b_n_face.nif", nif()), ("Meshes/b/face.dds", dds())):
            with self.subTest(path=path), tempfile.TemporaryDirectory() as d:
                f = Path(d)/"test.zip"
                archive(f, {"XB77_RedSun_4K_Overhaul.esp": record(b"TES3"), path: data})
                with self.assertRaisesRegex(ValueError, "wrong .* extension"):
                    validate_zip(f, set())

    def test_fake_file_headers_rejected(self):
        for path in ("Textures/tx_b_n_face.dds", "Textures/tx_b_n_face.png", "Textures/tx_b_n_face.tga", "Meshes/b/head.nif"):
            with self.subTest(path=path), tempfile.TemporaryDirectory() as d:
                f = Path(d)/"test.zip"
                archive(f, {"XB77_RedSun_4K_Overhaul.esp": record(b"TES3"), path: b"fake"})
                with self.assertRaisesRegex(ValueError, "invalid"):
                    validate_zip(f, set())

    def test_zero_byte_assets_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d)/"test.zip"
            archive(f, {"XB77_RedSun_4K_Overhaul.esp": record(b"TES3"), "Textures/tx_b_n_head.dds": b""})
            with self.assertRaisesRegex(ValueError, "size"):
                validate_zip(f, set())

    def test_protected_terrain_stems_still_rejected(self):
        for ext, asset in (("dds", dds()), ("png", png()), ("tga", bytes([0, 0, 2]) + b"\0" * 9 + struct.pack("<HH", 64, 64) + b"\x18\0")):
            with self.subTest(ext=ext), tempfile.TemporaryDirectory() as d:
                f = Path(d)/"test.zip"
                archive(f, {"XB77_RedSun_4K_Overhaul.esp": record(b"TES3"), "Textures/tx_b_n_scenery."+ext: asset})
                with self.assertRaisesRegex(ValueError, "landmass"):
                    validate_zip(f, {"tx_b_n_scenery"})

    def test_release_requires_both_asset_types(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d)/"test.zip"
            archive(f, {"XB77_RedSun_4K_Overhaul.esp": record(b"TES3"), "Textures/tx_b_n_head.dds": dds()})
            with self.assertRaisesRegex(ValueError, "texture and mesh"):
                validate_zip(f, set(), release=True)

    def test_release_requires_readme_and_provenance(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d)/"test.zip"
            entries={"XB77_RedSun_4K_Overhaul.esp": record(b"TES3"),
                     "Textures/tx_b_n_head.dds": dds(), "Meshes/b/head.nif": nif()}
            archive(f, entries)
            with self.assertRaisesRegex(ValueError, "README"):
                validate_zip(f, set(), release=True)
            entries["README.txt"] = b"Development-only test"
            archive(f, entries)
            with self.assertRaisesRegex(ValueError, "provenance"):
                validate_zip(f, set(), release=True)

    def test_release_provenance_hashes_verified(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d)/"test.zip"
            assets={"Textures/tx_b_n_head.dds": dds(), "Meshes/b/head.nif": nif()}
            manifest={"assets": [{"path": p, "sha256": hashlib.sha256(blob).hexdigest(),
                                  "author": "synthetic test", "license": "test only", "origin": "test fixture"}
                                 for p, blob in assets.items()]}
            entries={"XB77_RedSun_4K_Overhaul.esp": record(b"TES3"), "README.txt": b"Synthetic fixtures",
                     "asset_provenance.json": json.dumps(manifest).encode(), **assets}
            archive(f, entries)
            result=validate_zip(f, set(), release=True)
            self.assertEqual((result["textures"], result["meshes"]), (1, 1))
            manifest["assets"][0]["sha256"] = "f" * 64
            entries["asset_provenance.json"] = json.dumps(manifest).encode()
            archive(f, entries)
            with self.assertRaisesRegex(ValueError, "checksum"):
                validate_zip(f, set(), release=True)

    def test_asset_formats_are_recognized(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d)/"test.zip"
            tga = bytes([0, 0, 2]) + b"\0" * 9 + struct.pack("<HH", 4096, 4096) + b"\x18\0"
            archive(f, {"XB77_RedSun_4K_Overhaul.esp": record(b"TES3"),
                        "Textures/tx_b_n_head.png": png(), "Textures/tx_b_n_body.tga": tga,
                        "Meshes/b/head.nif": nif()})
            result = validate_zip(f, set())
            self.assertEqual((result["textures"], result["meshes"]), (2, 1))

    def test_landscape_records_block_even_with_provenance(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d)/"test.zip"
            archive(f, {"XB77_RedSun_4K_Overhaul.esp": record(b"TES3") + record(b"LAND"),
                        "Textures/tx_b_n_head.dds": dds(), "Meshes/b/head.nif": nif()})
            with self.assertRaisesRegex(ValueError, "landscape"):
                validate_zip(f, set(), release=True)

if __name__ == "__main__":
    unittest.main()
