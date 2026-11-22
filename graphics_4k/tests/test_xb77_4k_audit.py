import importlib.util
import struct
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "xb77_4k_audit.py"
spec = importlib.util.spec_from_file_location("xb77_4k_audit", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class AuditTests(unittest.TestCase):
    def test_missing_assets_are_not_a_release(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            result = module.audit(root / "original", root / "replacement")
            self.assertFalse(result["preflight_pass"])
            self.assertFalse(result["release_ready"])
            self.assertEqual(result["mod_scan"]["texture_count"], 0)

    def test_detects_4k_dds_and_nif_header(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            game = root / "Data Files"
            game.mkdir()
            for name in module.MASTER_FILES:
                (game / name).write_bytes(b"dummy fixture")
            mod = root / "xb77"
            (mod / "Textures").mkdir(parents=True)
            (mod / "Meshes").mkdir()
            dds = bytearray(128)
            dds[:4] = b"DDS "
            struct.pack_into("<II", dds, 12, 4096, 4096)
            (mod / "Textures" / "test.dds").write_bytes(dds)
            (mod / "Meshes" / "test.nif").write_bytes(b"NetImmerse File Format, Version 4.0.0.2\n")
            (mod / module.PLUGIN_NAME).write_bytes(b"TES3" + b"fixture not a real esp")
            result = module.audit(game, mod)
            self.assertTrue(result["preflight_pass"])
            self.assertFalse(result["release_ready"])
            self.assertFalse(result["mod_scan"]["textures_below_4k_for_review"])
            self.assertEqual(result["mod_scan"]["mesh_count"], 1)

    def test_flags_small_texture_and_invalid_mesh(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "mod" / "Textures").mkdir(parents=True)
            (root / "mod" / "Meshes").mkdir(parents=True)
            png = bytearray(32)
            png[:8] = b"\x89PNG\r\n\x1a\n"
            struct.pack_into(">II", png, 16, 512, 512)
            (root / "mod" / "Textures" / "small.png").write_bytes(png)
            (root / "mod" / "Meshes" / "invalid.nif").write_bytes(b"NOT NIF")
            result = module.audit(root / "original", root / "mod")
            self.assertIn("Textures/small.png", result["mod_scan"]["textures_below_4k_for_review"])
            self.assertIn("Meshes/invalid.nif", result["mod_scan"]["invalid_nif_headers"])


if __name__ == "__main__":
    unittest.main()