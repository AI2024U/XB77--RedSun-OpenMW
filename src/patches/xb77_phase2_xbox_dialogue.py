"""XB77 Test09 — targeted NPC Xbox input + mouse-focus efficiency + topic colours.

Run AFTER xb77_patch.py, xb77_phase1_mouse_focus.py,
xb77_phase1_hover_skin.py, and xb77_native_prefs.py.

This is an intentionally strict, fail-closed transformation of the pinned
OpenMW 0.52.0 RC1 tree: never turn on global controller menus.
"""
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

root = Path(sys.argv[1] if len(sys.argv) == 2 else 'upstream')

def edit(text: str, old: str, new: str, context: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f'{context}: expected one source anchor, found {count}')
    return text.replace(old, new, 1)

cpp = root / 'apps/openmw/mwgui/dialogue.cpp'
hpp = root / 'apps/openmw/mwgui/dialogue.hpp'
controller = root / 'apps/openmw/mwinput/controllermanager.cpp'
controller_hpp = root / 'apps/openmw/mwinput/controllermanager.hpp'
skins = root / 'files/data/mygui/openmw_list.skin.xml'
settings = root / 'files/data/mygui/openmw_settings_window.layout'
console = root / 'files/data/mygui/openmw_console.layout'

c = cpp.read_text(encoding='utf-8')
h = hpp.read_text(encoding='utf-8')
ctrl = controller.read_text(encoding='utf-8')
ctrlh = controller_hpp.read_text(encoding='utf-8')

h = edit(h,
    '        size_t mXB77PointerFocus = static_cast<size_t>(-1);\n',
    '        size_t mXB77PointerFocus = static_cast<size_t>(-1);\n'
    '        bool mXB77ControllerNavigation = false;\n'
    '        bool mXB77MousePositionKnown = false;\n'
    '        MyGUI::IntPoint mXB77LastMousePosition;\n',
    'track dialog-only controller focus and physical mouse motion')

c = edit(c, '#include "dialogue.hpp"\n',
    '#include "dialogue.hpp"\n\n#include <algorithm>\n',
    'include std::find')

# Store actual mouse coordinates rather than MyGUI hover identity: D-pad
# scrolling can change the widget under a stationary cursor.
start = '        // Apply the setting immediately when a dialogue remains open.\n'
end = '        updateDisposition();\n'
if c.count(start) != 1:
    raise RuntimeError('expected one Phase1 onFrame start anchor')
pos1 = c.index(start)
pos2 = c.index(end, pos1)
old_frame = c[pos1:pos2]
if 'mXB77PointerFocus' not in old_frame or 'getMouseFocusWidget' not in old_frame:
    raise RuntimeError('Phase1 mouse focus logic is absent; wrong build target')
new_frame = '''        // Keep the existing native Prefs toggle live while a conversation is open.
        const bool contrastChanged = mXB77Applied != Settings::gui().mXB77HighContrastDialogue;
        if (contrastChanged)
        {
            updateTopicFormat();
            if (Settings::gui().mControllerMenus)
                setControllerFocus(mControllerFocus, true);
        }

        // XB77 routes D-pad events to *dialogue only*, so global controller
        // menus remain disabled and the previously working main menu is safe.
        if (!Settings::gui().mControllerMenus)
        {
            MyGUI::InputManager& input = MyGUI::InputManager::getInstance();
            const MyGUI::IntPoint mousePosition = input.getMousePosition();
            if (mXB77MousePositionKnown
                && (mousePosition.left != mXB77LastMousePosition.left
                    || mousePosition.top != mXB77LastMousePosition.top))
                mXB77ControllerNavigation = false;
            mXB77LastMousePosition = mousePosition;
            mXB77MousePositionKnown = true;

            const size_t count = mTopicsList->getItemCount();
            const size_t none = static_cast<size_t>(-1);
            size_t desired = none;
            if (Settings::gui().mXB77HighContrastDialogue)
            {
                if (mXB77ControllerNavigation)
                {
                    // The final item is the Goodbye button outside this list.
                    if (mControllerFocus < count && !mTopicsList->getItemNameAt(mControllerFocus).empty())
                        desired = mControllerFocus;
                }
                else
                {
                    MyGUI::Widget* mouse = input.getMouseFocusWidget();
                    MyGUI::Widget* keyboard = input.getKeyFocusWidget();
                    for (size_t i = 0; i < count; ++i)
                    {
                        const std::string& name = mTopicsList->getItemNameAt(i);
                        if (name.empty())
                            continue;
                        MyGUI::Button* button = mTopicsList->getItemWidget(name);
                        for (MyGUI::Widget* w = mouse; w; w = w->getParent())
                        {
                            if (w == button) { desired = i; break; }
                        }
                        if (desired != none)
                            break;
                        for (MyGUI::Widget* w = keyboard; w; w = w->getParent())
                        {
                            if (w == button) { desired = i; break; }
                        }
                        if (desired != none)
                            break;
                    }
                    if (desired == none)
                        for (size_t i = 0; i < count; ++i)
                            if (!mTopicsList->getItemNameAt(i).empty())
                            { desired = i; break; }
                    // Start subsequent D-pad navigation at the row last selected
                    // with the pointer, not an obsolete controller index.
                    if (desired != none)
                        mControllerFocus = desired;
                }
            }

            // Only update the two affected widgets. Phase1 updated *every*
            // topic after a change, causing expensive MyGUI state invalidation.
            if (mXB77PointerFocus != desired || contrastChanged)
            {
                if (mXB77PointerFocus < count)
                {
                    const std::string& oldName = mTopicsList->getItemNameAt(mXB77PointerFocus);
                    if (!oldName.empty())
                        mTopicsList->getItemWidget(oldName)->setStateSelected(false);
                }
                if (desired < count)
                {
                    const std::string& newName = mTopicsList->getItemNameAt(desired);
                    if (!newName.empty())
                        mTopicsList->getItemWidget(newName)->setStateSelected(true);
                }
                mXB77PointerFocus = desired;
            }
        }

'''
c = c[:pos1] + new_frame + c[pos2:]

c = edit(c,
    '''        if (Settings::gui().mControllerMenus && !sameActor)
        {
            setControllerFocus(mControllerFocus, false);
            // Reset focus to very top. Maybe change this to mTopicsList->getItemCount() - mKeywords.size()?
            mControllerFocus = 0;
            setControllerFocus(mControllerFocus, true);
        }
''',
    '''        if (Settings::gui().mControllerMenus && !sameActor)
        {
            setControllerFocus(mControllerFocus, false);
            // Reset focus to very top. Maybe change this to mTopicsList->getItemCount() - mKeywords.size()?
            mControllerFocus = 0;
            setControllerFocus(mControllerFocus, true);
        }
        else if (!sameActor)
        {
            // New NPC: do not carry a selection or mouse position from another actor.
            mControllerFocus = 0;
            mXB77ControllerNavigation = false;
            mXB77MousePositionKnown = false;
        }
''',
    'reset controller on new NPC only')

c = edit(c,
    '        if (Settings::gui().mControllerMenus && mControllerFocus < mTopicsList->getItemCount())\n'
    '            focusedTopic = mTopicsList->getItemNameAt(mControllerFocus);',
    '        if ((Settings::gui().mControllerMenus || mXB77ControllerNavigation)\n'
    '            && mControllerFocus < mTopicsList->getItemCount())\n'
    '            focusedTopic = mTopicsList->getItemNameAt(mControllerFocus);',
    'preserve Xbox topic when topics regenerate')

c = edit(c,
    '''        if (Settings::gui().mControllerMenus)
            setControllerFocus(mControllerFocus, true);
    }

    void DialogueWindow::updateHistory''',
    '''        if (Settings::gui().mControllerMenus
            || (mXB77ControllerNavigation && mControllerFocus < mTopicsList->getItemCount()))
            setControllerFocus(mControllerFocus, true);
    }

    void DialogueWindow::updateHistory''',
    'restore dialogue-only Xbox focus after list rebuild')

c = edit(c,
    '''            std::string skin = "MW_ListLine";
            if (colorTopics)
            {
                const int flag = MWBase::Environment::get().getDialogueManager()->getTopicFlag(
                    ESM::RefId::stringRefId(keyword));
                if (flag & MWBase::DialogueManager::TopicType::Specific)
                    skin = "MW_ListLine_Specific";
                else if (flag & MWBase::DialogueManager::TopicType::Exhausted)
                    skin = "MW_ListLine_Exhausted";
            }
            if (highContrast)
                skin = "XB77_" + skin;
''',
    '''            std::string skin = "MW_ListLine";
            // Only real available NPC conversation topics get unread/read
            // colours; Barter/Persuasion/etc. are service actions, not topics.
            const bool conversation = std::find(mKeywords.begin(), mKeywords.end(), keyword) != mKeywords.end();
            if (highContrast && conversation)
            {
                const int flag = MWBase::Environment::get().getDialogueManager()->getTopicFlag(
                    ESM::RefId::stringRefId(keyword));
                // Engine's journal-backed exhausted flag means already read.
                skin = (flag & MWBase::DialogueManager::TopicType::Exhausted)
                    ? "XB77_MW_ListLine_Exhausted" : "XB77_MW_ListLine_Specific";
            }
            else if (colorTopics && !highContrast)
            {
                const int flag = MWBase::Environment::get().getDialogueManager()->getTopicFlag(
                    ESM::RefId::stringRefId(keyword));
                if (flag & MWBase::DialogueManager::TopicType::Specific)
                    skin = "MW_ListLine_Specific";
                else if (flag & MWBase::DialogueManager::TopicType::Exhausted)
                    skin = "MW_ListLine_Exhausted";
            }
            if (highContrast && !conversation)
                skin = "XB77_MW_ListLine";
''',
    'assign blue available NPC topics and grey journal-exhausted topics, services neutral')

c = edit(c,
    '''    bool DialogueWindow::onControllerButtonEvent(const SDL_ControllerButtonEvent& arg)
    {
        if (arg.button == SDL_CONTROLLER_BUTTON_A)
''',
    '''    bool DialogueWindow::onControllerButtonEvent(const SDL_ControllerButtonEvent& arg)
    {
        if (!Settings::gui().mControllerMenus
            && (arg.button == SDL_CONTROLLER_BUTTON_DPAD_UP || arg.button == SDL_CONTROLLER_BUTTON_DPAD_DOWN))
            mXB77ControllerNavigation = true;

        if (arg.button == SDL_CONTROLLER_BUTTON_A)
''',
    'select dialogue-only D-pad control when used')

# Controller manager: route D-pad/A/B *only* for the active NPC Dialogue
# window. This avoids the global controller-menus focus path that caused the
# pink/invisible main menu regression. Preserve other input handling entirely.
ctrl = edit(ctrl,
    '''        MWBase::WindowManager* winMgr = MWBase::Environment::get().getWindowManager();

        if (Settings::gui().mControllerMenus)
        {
            // Update cursor state.
''',
    '''        MWBase::WindowManager* winMgr = MWBase::Environment::get().getWindowManager();

        // XB77: dialogue-only navigation with the globally safe controller
        // menus mode OFF. All other menus keep OpenMW's existing input path.
        if (!Settings::gui().mControllerMenus
            && (arg.button == SDL_CONTROLLER_BUTTON_DPAD_UP || arg.button == SDL_CONTROLLER_BUTTON_DPAD_DOWN
                || arg.button == SDL_CONTROLLER_BUTTON_A || arg.button == SDL_CONTROLLER_BUTTON_B))
        {
            MWGui::WindowBase* dialogue = winMgr->getActiveControllerWindow();
            if (dialogue && dialogue->isVisible() && dialogue->getWindowIdForLua() == "Dialogue")
            {
                if (arg.button == SDL_CONTROLLER_BUTTON_A)
                    mXB77DialogueAConsumed = true;
                return dialogue->onControllerButtonEvent(arg);
            }
        }

        if (Settings::gui().mControllerMenus)
        {
            // Update cursor state.
''',
    'route only active dialogue Xbox button presses')

ctrlh = edit(ctrlh,
    '''        bool mGamepadMousePressed;
''',
    '''        bool mGamepadMousePressed;
        // Prevent A-button *release* from clicking the mouse after XB77
        // has already selected a dialogue topic on A-button press.
        bool mXB77DialogueAConsumed = false;
''',
    'track separately consumed Xbox A press')

ctrl = edit(ctrl,
    '''        mJoystickLastUsed = true;
        if (MWBase::Environment::get().getWindowManager()->isGuiMode())
        {
            if (mGamepadGuiCursorEnabled && (!Settings::gui().mControllerMenus || mGamepadMousePressed))
''',
    '''        mJoystickLastUsed = true;
        if (arg.button == SDL_CONTROLLER_BUTTON_A && mXB77DialogueAConsumed)
        {
            // Button press was handled as a native topic activation, not a
            // simulated mouse click. Swallow its matching mouse release.
            mXB77DialogueAConsumed = false;
            return;
        }
        if (MWBase::Environment::get().getWindowManager()->isGuiMode())
        {
            if (mGamepadGuiCursorEnabled && (!Settings::gui().mControllerMenus || mGamepadMousePressed))
''',
    'do not inject a second mouse click on Xbox A release')

# Skin: two layers of hover yellow + checked yellow could visually select two
# topics and cause work on both rows. From Test09 onwards only the checked
# (C++-owned) row gets the yellow outline/arrow.
s = skins.read_text(encoding='utf-8')
for name, neutral in [
    ('XB77_MW_ListLine', '#{fontcolour=normal_over}'),
    ('XB77_MW_ListLine_Specific', '#7FAFFF'),  # light cobalt blue
    ('XB77_MW_ListLine_Exhausted', '#A3A3A3'), # readable grey
]:
    pat = re.compile(r'(<Resource\s+type="ResourceSkin"\s+name="' + re.escape(name) + r'"[\s\S]*?</Resource>)')
    matches = list(pat.finditer(s))
    if len(matches) != 1:
        raise RuntimeError(f'{name}: expected one custom skin, found {len(matches)}')
    m = matches[0]
    block = m.group(1)
    # Undo Phase1's *hover* highlight, not the checked yellow visuals.
    if block.count('<State name="highlighted" offset="0 0 2 2"') != 4:
        raise RuntimeError(f'{name}: missing Phase1 border hover states')
    if block.count('<State name="highlighted" offset="4 0 7 11"') != 1:
        raise RuntimeError(f'{name}: missing Phase1 arrow hover state')
    block = block.replace('<State name="highlighted" offset="0 0 2 2"',
                          '<State name="highlighted" offset="2 0 2 2"')
    block = block.replace('<State name="highlighted" offset="4 0 7 11"',
                          '<State name="highlighted" offset="2 0 2 2"')
    # Keep yellow exactly on the C++ selected row; not general mouse hover.
    block, n = re.subn(r'(<State name="highlighted" colour=")[^"]+("[^>]*/>)',
                       lambda match: match.group(1) + neutral + match.group(2), block)
    if n != 1:
        raise RuntimeError(f'{name}: unexpected hover text-state count {n}')
    if name != 'XB77_MW_ListLine':
        # Make blue/grey explicit even if the user changes Morrowind's generic
        # topic colors; preserve the selected yellow text states.
        block, n = re.subn(r'(<State name="normal" colour=")[^"]+("[^>]*/>)',
                           lambda match: match.group(1) + neutral + match.group(2), block)
        if n != 1:
            raise RuntimeError(f'{name}: missing normal text state')
        block, n = re.subn(r'(<State name="pushed" colour=")[^"]+("[^>]*/>)',
                           lambda match: match.group(1) + neutral + match.group(2), block)
        if n != 1:
            raise RuntimeError(f'{name}: missing pushed text state')
    if '#FFE500' not in block or 'name="normal_checked" offset="4 0 7 11"' not in block:
        raise RuntimeError(f'{name}: checked yellow visuals were damaged')
    s = s[:m.start(1)] + block + s[m.end(1):]
ET.fromstring(s)

# Carry forward the two independent XML safety fixes from the user-successful
# Audited Test08; they do not alter executable or controller logic.
l = settings.read_text(encoding='utf-8-sig')
l = edit(l,
    '<Widget name="ScriptBox" type="Widget" align="Stretch" name="ScriptBox">',
    '<Widget name="ScriptBox" type="Widget" align="Stretch">',
    'remove duplicate original settings layout XML attribute')
k = console.read_text(encoding='utf-8-sig')
k = edit(k, '<Property key="Caption" value="<"/>',
         '<Property key="Caption" value="&lt;"/>',
         'escape original console XML caption')
for path, text in ((settings,l),(console,k)):
    ET.fromstring(text)

# Commit only after ALL source and XML transformations have validated.
for path, text in ((cpp,c),(hpp,h),(controller,ctrl),(controller_hpp,ctrlh),
                   (skins,s),(settings,l),(console,k)):
    path.write_text(text,encoding='utf-8',newline='')

print('XB77 Test09: active dialogue-only Xbox Up/Down/A/B, isolated A release,')
print('pointer state optimized, blue unread/grey exhausted, old XML defects fixed.')
