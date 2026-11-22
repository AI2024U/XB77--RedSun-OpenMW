"""XB77 Red Sun: a time-delayed celestial glow for native Xbox A prompts.

Usage: python xb77_celestial_controller.py <OpenMW-0.52-RC1-source-directory>

Compile the patched OpenMW engine. Do NOT drop this Python file into a
running OpenMW installation expecting in-game animation without recompiling.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) == 2 else "upstream")
hpp = root / "apps/openmw/mwgui/controllerbuttonsoverlay.hpp"
cpp = root / "apps/openmw/mwgui/controllerbuttonsoverlay.cpp"
for f in (hpp, cpp):
    if not f.is_file():
        raise RuntimeError(f"OpenMW 0.52.0 RC1 source missing: {f}")
h = hpp.read_text(encoding="utf-8")
c = cpp.read_text(encoding="utf-8")

def once(source, before, after, note):
    n = source.count(before)
    if n != 1:
        raise RuntimeError(f"{note}: expected 1 source anchor, found {n}")
    return source.replace(before, after, 1)

h = once(h, "#include <array>\n", "#include <array>\n#include <random>\n", "random include")
h = once(h, "        void setButtons(ControllerButtons* buttons);\n",
         "        void setButtons(ControllerButtons* buttons);\n        void onFrame(float duration) override;\n", "frame override")
h = once(h, "        std::array<ButtonWidgets, Button::Button_Max> mButtons;\n        Gui::HBox* mHBox;\n",
         """        std::array<ButtonWidgets, Button::Button_Max> mButtons;
        Gui::HBox* mHBox;

        // XB77: randomized 3-9 second idle pause between gentle 1.2s
        // celestial A-button glows. Other buttons are never animated.
        bool mXB77AnimateA = false;
        bool mXB77PulseActive = false;
        float mXB77GlowClock = 0.f;
        float mXB77NextPulse = 5.f;
        int mXB77GlowFrame = -1;
        std::mt19937 mXB77Random{ std::random_device{}() };
        std::uniform_real_distribution<float> mXB77Delay{ 3.f, 9.f };
""", "private members")
c = once(c, '#include "controllerbuttonsoverlay.hpp"\n',
         '#include "controllerbuttonsoverlay.hpp"\n\n#include <algorithm>\n#include <array>\n', "frame includes")
c = once(c,
'''            if (sButtonDefs[i].mInputType == InputType_Axis)
                setIcon(mButtons[i].mImage, inputMgr->getControllerAxisIcon(sButtonDefs[i].mId.mAxis));
            else
                setIcon(mButtons[i].mImage, inputMgr->getControllerButtonIcon(sButtonDefs[i].mId.mButton));
''',
'''            if (sButtonDefs[i].mInputType == InputType_Axis)
                setIcon(mButtons[i].mImage, inputMgr->getControllerAxisIcon(sButtonDefs[i].mId.mAxis));
            else
            {
                const std::string texture = inputMgr->getControllerButtonIcon(sButtonDefs[i].mId.mButton);
                setIcon(mButtons[i].mImage, texture);
                // Do not replace PlayStation's X or any other controller icon.
                if (sButtonDefs[i].mButton == Button_A)
                    mXB77AnimateA = texture == "textures/omw_steam_button_a.dds";
            }
''', "controller icon guard")
anchor='''    int ControllerButtonsOverlay::getHeight()
    {
'''
function='''    void ControllerButtonsOverlay::onFrame(float duration)
    {
        if (!mXB77AnimateA || !mButtons[Button_A].mImage)
            return;

        MyGUI::ImageBox* icon = mButtons[Button_A].mImage;
        constexpr std::string_view baseTexture = "textures/omw_steam_button_a.dds";
        static constexpr std::array<const char*, 12> frames = {
            "textures/xb77_celestial_a_00.png", "textures/xb77_celestial_a_01.png",
            "textures/xb77_celestial_a_02.png", "textures/xb77_celestial_a_03.png",
            "textures/xb77_celestial_a_04.png", "textures/xb77_celestial_a_05.png",
            "textures/xb77_celestial_a_06.png", "textures/xb77_celestial_a_07.png",
            "textures/xb77_celestial_a_08.png", "textures/xb77_celestial_a_09.png",
            "textures/xb77_celestial_a_10.png", "textures/xb77_celestial_a_11.png",
        };

        if (!isVisible() || !mButtons[Button_A].mHBox->getVisible())
        {
            if (mXB77GlowFrame >= 0)
                icon->setImageTexture(std::string(baseTexture));
            mXB77GlowFrame = -1;
            mXB77PulseActive = false;
            mXB77GlowClock = 0.f;
            mXB77NextPulse = mXB77Delay(mXB77Random);
            return;
        }

        mXB77GlowClock += std::clamp(duration, 0.f, 0.25f);
        if (!mXB77PulseActive)
        {
            if (mXB77GlowClock < mXB77NextPulse)
                return;
            mXB77PulseActive = true;
            mXB77GlowClock = 0.f;
        }

        constexpr float frameSeconds = 0.1f;
        const int frame = static_cast<int>(mXB77GlowClock / frameSeconds);
        if (frame >= static_cast<int>(frames.size()))
        {
            icon->setImageTexture(std::string(baseTexture));
            mXB77GlowFrame = -1;
            mXB77PulseActive = false;
            mXB77GlowClock = 0.f;
            mXB77NextPulse = mXB77Delay(mXB77Random); // 3-9s until next pulse
            return;
        }

        if (frame != mXB77GlowFrame)
        {
            icon->setImageTexture(frames[static_cast<std::size_t>(frame)]);
            mXB77GlowFrame = frame;
        }
    }

'''
c = once(c,anchor,function+anchor,"onFrame insertion")
hpp.write_text(h,encoding="utf-8",newline="")
cpp.write_text(c,encoding="utf-8",newline="")
print("Applied celestial Xbox A controller overlay source patch (requires native build).")
