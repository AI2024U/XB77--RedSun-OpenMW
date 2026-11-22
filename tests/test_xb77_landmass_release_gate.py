"""Synthetic tests only. No Bethesda files or paid CI required."""
import io
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
            archive(f, {"XB77_RedSun_4K_Overhaul.esp": record(b"TES3"), "Textures/tx_b_n_head.dds": b"test"})
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
            archive(f, {"Textures/tx_b_n_head.dds": b"test"})
            with self.assertRaisesRegex(ValueError, "missing ESP"):
                validate_zip(f, set())

if __name__ == "__main__":
    unittest.main()
