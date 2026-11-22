"""XB77 Red Sun: hide native voice subtitles while Options/Prefs is open.

Applies to OpenMW 0.52.0 RC1 (openmw-52-rc1) source.
This is an ENGINE SOURCE patch; it is NOT an installable mod or runtime fix.
Must be compiled into modified OpenMW binaries and Windows-tested.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) == 2 else "upstream")
target = root / "apps/openmw/mwgui/windowmanagerimp.cpp"
if not target.is_file():
    raise RuntimeError("OpenMW windowmanagerimp.cpp not found")
source = target.read_text(encoding="utf-8")
before_visibility = "        mHud->setVisible(mHudEnabled && !loading);\n        mToolTips->setVisible(mHudEnabled && !loading);\n\n        bool gameMode = !isGuiMode();"
after_visibility = "        mHud->setVisible(mHudEnabled && !loading);\n        mToolTips->setVisible(mHudEnabled && !loading);\n\n        // XB77: Hide transient NPC subtitles and ordinary notifications while\n        // Options/Prefs is visible. Unlike an interactive modal message box,\n        // these captions can obscure accessibility settings and button prompts.\n        // MessageBoxManager::setVisible only affects non-interactive boxes.\n        if (mMessageBoxManager)\n            mMessageBoxManager->setVisible(mHudEnabled && !loading && !isSettingsWindowVisible());\n\n        bool gameMode = !isGuiMode();"
before_hud = "        mHudEnabled = show;\n        updateVisible();\n        mMessageBoxManager->setVisible(mHudEnabled);\n        return mHudEnabled;"
after_hud = "        mHudEnabled = show;\n        // Visibility of transient message boxes is updated along with all\n        // windows, including the Options/Prefs overlay. Do not override it.\n        updateVisible();\n        return mHudEnabled;"
for label, old in (("Options subtitle visibility", before_visibility), ("HUD visibility", before_hud)):
    if source.count(old) != 1:
        raise RuntimeError(f"{label}: expected one upstream source anchor, found {source.count(old)}")
source = source.replace(before_visibility, after_visibility, 1)
source = source.replace(before_hud, after_hud, 1)
if "mMessageBoxManager->setVisible(mHudEnabled && !loading && !isSettingsWindowVisible());" not in source:
    raise RuntimeError("Native subtitle visibility predicate missing")
target.write_text(source, encoding="utf-8", newline="")
print("XB77 native Options subtitle-hide patch applied. Rebuild required.")
