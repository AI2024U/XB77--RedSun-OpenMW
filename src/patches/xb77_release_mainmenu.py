"""XB77 public edition: attach the Red Sun to the actual New Game button.
Run after xb77_phase2_xbox_dialogue.py on the pinned OpenMW 0.52.0 RC1 tree.
This modifies no stock Morrowind assets and doesn't change input or focus.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) == 2 else "upstream")
cpp = root / "apps/openmw/mwgui/mainmenu.cpp"
hpp = root / "apps/openmw/mwgui/mainmenu.hpp"

def once(text, old, new, name):
    found = text.count(old)
    if found != 1:
        raise RuntimeError(f"{name}: expected one source anchor; found {found}")
    return text.replace(old, new, 1)

c = cpp.read_text(encoding="utf-8")
h = hpp.read_text(encoding="utf-8")
c = once(c, '#include <MyGUI_Gui.h>\n',
         '#include <MyGUI_Gui.h>\n#include <MyGUI_ImageBox.h>\n',
         "MyGUI image include")
h = once(h, 'namespace Gui\n{\n    class ImageButton;\n}\n',
         'namespace MyGUI\n{\n    class ImageBox;\n}\n\nnamespace Gui\n{\n    class ImageButton;\n}\n',
         "ImageBox forward declaration")
h = once(h, '        MyGUI::Widget* mButtonBox;\n',
         '        MyGUI::Widget* mButtonBox;\n'
         '        MyGUI::ImageBox* mXB77RedSunLogo = nullptr;\n',
         "menu logo pointer")
end = '''        else
            mButtonBox->setCoord(mWidth / 2 - maxwidth / 2, mHeight / 2 - curH / 2, maxwidth, curH);
    }
}
'''
revised = '''        else
            mButtonBox->setCoord(mWidth / 2 - maxwidth / 2, mHeight / 2 - curH / 2, maxwidth, curH);

        // XB77 public branding: keep the original Morrowind menu art and
        // original clickable New Game button. Follow its actual dynamically
        // calculated position (saves and screen size change menu geometry).
        // Decorative widget never receives mouse/gamepad focus.
        constexpr int logoSize = 32;
        // The vanilla menu_newgame texture has transparent left padding.
        // Calibrated from the XB77 1648x928 title-screen QA screenshot:
        // visual "New" begins ~11 pixels inside the button image.
        // Place the badge's right edge 1px before the visible lettering.
        constexpr int logoGap = 1;
        constexpr int newGameTextLeftInset = 11;
        if (!mXB77RedSunLogo)
        {
            mXB77RedSunLogo = mMainWidget->createWidget<MyGUI::ImageBox>(
                "ImageBox", MyGUI::IntCoord(0, 0, logoSize, logoSize), MyGUI::Align::Default);
            mXB77RedSunLogo->setImageTexture("textures\\\\xb77_red_sun_menu.png");
            mXB77RedSunLogo->setNeedMouseFocus(false);
        }
        const Gui::ImageButton* newGameButton = mButtons.at("newgame");
        mXB77RedSunLogo->setCoord(
            mButtonBox->getLeft() + newGameButton->getLeft() + newGameTextLeftInset - logoSize - logoGap,
            mButtonBox->getTop() + newGameButton->getTop() + (newGameButton->getHeight() - logoSize) / 2,
            logoSize, logoSize);
        // Only display the decorative emblem on the initial TITLE/MAIN menu.
        // Hide it on the in-game Start/Pause menu, even though New Game exists there.
        mXB77RedSunLogo->setVisible(
            state == MWBase::StateManager::State_NoGame && newGameButton->getVisible());
    }
}
'''
c = once(c, end, revised, "button-position attachment")
if "setNeedMouseFocus(false)" not in c:
    raise RuntimeError("Logo must not intercept mouse/controller input")
cpp.write_text(c, encoding="utf-8", newline="")
hpp.write_text(h, encoding="utf-8", newline="")
print("XB77 release: new game logo anchored to native dynamic menu button.")
