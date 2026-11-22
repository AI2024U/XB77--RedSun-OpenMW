"""XB77 release polish: restore the original static Morrowind main menu.
Run after checkout of the pinned OpenMW 0.52.0 RC1 source tree, before build.
Only changes OpenMW's main-menu background choice; no menu button/action code.
Use with xb77_release_mainmenu.py for an adjacent decorative Red Sun badge.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream")
target = root / "apps/openmw/mwgui/mainmenu.cpp"
if not target.is_file():
    raise RuntimeError(f"OpenMW mainmenu.cpp not found: {target}")
source = target.read_text(encoding="utf-8")
needle = '''        constexpr VFS::Path::NormalizedView menuBackgroundVideo("video/menu_background.bik");

        mHasAnimatedMenu = mVFS->exists(menuBackgroundVideo);
'''
replacement = '''        // XB77 release: preserve the original Morrowind menu artwork
        // instead of loading a mod-supplied menu_background.bik video.
        // BackgroundImage uses textures/menu_morrowind.dds from the
        // player's licensed Morrowind data. No Bethesda asset is bundled.
        mHasAnimatedMenu = false;
'''
if source.count(needle) != 1:
    raise RuntimeError(f"Expected exactly one OpenMW 0.52.0 RC1 anchor, found {source.count(needle)}")
updated = source.replace(needle, replacement, 1)
if 'mBackground->setBackgroundImage("textures\\\\menu_morrowind.dds", true, stretch);' not in updated:
    raise RuntimeError("Expected vanilla static Morrowind background path missing")
target.write_text(updated, encoding="utf-8", newline="")
print("XB77 native menu source patch applied. Compile and test before release.")
