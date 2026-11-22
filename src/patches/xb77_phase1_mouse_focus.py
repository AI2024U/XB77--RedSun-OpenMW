"""Phase 1: allow mouse/keyboard topic focus with native controller menus disabled.

Apply AFTER ci/xb77_patch.py. This intentionally doesn't change the Xbox input
path. Fail on any unexpected upstream/source edit rather than guessing.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream")
cpp = root / "apps/openmw/mwgui/dialogue.cpp"
hpp = root / "apps/openmw/mwgui/dialogue.hpp"
a, b = cpp.read_text(encoding="utf-8"), hpp.read_text(encoding="utf-8")

def edit(contents, original, replacement, label):
    if contents.count(original) != 1:
        raise RuntimeError(f"{label}: expected one exact source anchor; got {contents.count(original)}")
    return contents.replace(original, replacement)

b = edit(b,
    '        bool mXB77Applied = false;\n',
    '        bool mXB77Applied = false;\n'
    '        // Visual focus with controller menus disabled (not Xbox navigation).\n'
    '        size_t mXB77PointerFocus = static_cast<size_t>(-1);\n',
    "dialogue.hpp: one visual focus state")

a = edit(a,
    '#include <MyGUI_Button.h>\n',
    '#include <MyGUI_Button.h>\n#include <MyGUI_InputManager.h>\n',
    "dialogue.cpp: MyGUI input manager include")

a = edit(a,
    '        mTopicsList->clear();\n'
    '        mXB77TopicSkins.clear(); // Topic widgets have been destroyed/rebuilt.\n'
    '        for (auto& linkPair : mTopicLinks)\n',
    '        mTopicsList->clear();\n'
    '        mXB77TopicSkins.clear(); // Topic widgets have been destroyed/rebuilt.\n'
    '        mXB77PointerFocus = static_cast<size_t>(-1); // Selection was destroyed.\n'
    '        for (auto& linkPair : mTopicLinks)\n',
    "dialogue.cpp: invalidate focus after topic list rebuild")

old = """        // Apply the setting immediately when a dialogue remains open.
        if (mXB77Applied != Settings::gui().mXB77HighContrastDialogue)
        {
            updateTopicFormat();
            if (Settings::gui().mControllerMenus)
                setControllerFocus(mControllerFocus, true);
        }

        updateDisposition();"""
new = """        // Apply the setting immediately when a dialogue remains open.
        const bool contrastChanged = mXB77Applied != Settings::gui().mXB77HighContrastDialogue;
        if (contrastChanged)
        {
            updateTopicFormat();
            if (Settings::gui().mControllerMenus)
                setControllerFocus(mControllerFocus, true);
        }

        // Phase 1 accessibility does not require native controller menus.
        // Track mouse/keyboard topic selection independently; only visuals change.
        if (!Settings::gui().mControllerMenus)
        {
            const size_t count = mTopicsList->getItemCount();
            size_t desired = static_cast<size_t>(-1);

            if (Settings::gui().mXB77HighContrastDialogue)
            {
                MyGUI::Widget* mouse = MyGUI::InputManager::getInstance().getMouseFocusWidget();
                MyGUI::Widget* keyboard = MyGUI::InputManager::getInstance().getKeyFocusWidget();
                for (size_t i = 0; i < count; ++i)
                {
                    const std::string& name = mTopicsList->getItemNameAt(i);
                    if (name.empty()) // Skip list separators.
                        continue;
                    MyGUI::Button* button = mTopicsList->getItemWidget(name);
                    for (MyGUI::Widget* w = mouse; w; w = w->getParent())
                    {
                        if (w == button)
                        {
                            desired = i;
                            break;
                        }
                    }
                    if (desired != static_cast<size_t>(-1))
                        break;
                    for (MyGUI::Widget* w = keyboard; w; w = w->getParent())
                    {
                        if (w == button)
                        {
                            desired = i;
                            break;
                        }
                    }
                    if (desired != static_cast<size_t>(-1))
                        break;
                }
                // Always have one visual topic when XB77 is enabled.
                if (desired == static_cast<size_t>(-1))
                    for (size_t i = 0; i < count; ++i)
                        if (!mTopicsList->getItemNameAt(i).empty())
                        {
                            desired = i;
                            break;
                        }
            }

            if (mXB77PointerFocus != desired || contrastChanged)
            {
                for (size_t i = 0; i < count; ++i)
                {
                    const std::string& name = mTopicsList->getItemNameAt(i);
                    if (!name.empty())
                        mTopicsList->getItemWidget(name)->setStateSelected(i == desired);
                }
                mXB77PointerFocus = desired;
            }
        }

        updateDisposition();"""
a = edit(a, old, new, "dialogue.cpp: live visual focus")
cpp.write_text(a, encoding="utf-8", newline="\n")
hpp.write_text(b, encoding="utf-8", newline="\n")
print("XB77 Phase 1 C++ accessibility focus installed: independent mouse/keyboard topic selection.")
