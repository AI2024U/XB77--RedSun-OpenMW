"""Install XB77's native Prefs control into OpenMW 0.52.0 RC1 MyGUI layout.

Existing SettingsWindow::configureWidgets() and onButtonToggled() already
read/write SettingCategory/SettingName into Settings::get<bool>, then persist
settings.cfg when Options closes. DialogueWindow already reads the same
Settings::gui().mXB77HighContrastDialogue setting. No dialogue C++ change.
"""
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

POSITIONS = {
    "4 250 340 28": "4 245 340 28",
    "4 280 340 28": "4 271 340 28",
    "4 310 340 28": "4 297 340 28",
    "4 340 340 28": "4 323 340 28",
    "4 370 340 28": "4 349 340 28",
}
ANCHOR = '''                    <Widget type="AutoSizedTextBox" skin="SandText" position="28 4 89 16" align="Left Top">
                        <Property key="Caption" value="#{OMWEngine:MouseEmulationCursor}"/>
                    </Widget>
                </Widget>
            </Widget>'''
REPLACEMENT = '''                    <Widget type="AutoSizedTextBox" skin="SandText" position="28 4 89 16" align="Left Top">
                        <Property key="Caption" value="#{OMWEngine:MouseEmulationCursor}"/>
                    </Widget>
                </Widget>
                <!-- XB77 v1.0: uses OpenMW's existing native boolean settings handler. -->
                <Widget type="HBox" position="4 375 340 28">
                    <Widget type="AutoSizedButton" skin="MW_Button" position="0 0 24 24" align="Left Top" name="XB77HighContrastButton">
                        <UserString key="SettingCategory" value="GUI"/>
                        <UserString key="SettingName" value="xb77 high contrast dialogue"/>
                        <UserString key="SettingType" value="CheckButton"/>
                    </Widget>
                    <Widget type="AutoSizedTextBox" skin="SandText" position="28 4 300 16" align="Left Top">
                        <Property key="Caption" value="XB77: High-Contrast Dialogue Selection"/>
                    </Widget>
                </Widget>
            </Widget>'''


def main(upstream: Path) -> None:
    gui = upstream / "components/settings/categories/gui.hpp"
    layout = upstream / "files/data/mygui/openmw_settings_window.layout"
    if 'mXB77HighContrastDialogue{ mIndex, "GUI", "xb77 high contrast dialogue" }' not in gui.read_text(encoding="utf-8"):
        raise RuntimeError("XB77 native GUI setting absent; refusing incompatible layout patch")
    raw = layout.read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    newline = "\r\n" if b"\r\n" in raw else "\n"
    text = raw.decode("utf-8-sig").replace("\r\n", "\n")
    if 'name="XB77HighContrastButton"' in text:
        raise RuntimeError("Duplicate XB77 native Prefs toggle")
    tabs = [i for i in range(len(text)) if text.startswith('            <Widget type="TabItem">', i)]
    if len(tabs) < 2:
        raise RuntimeError("OpenMW Prefs tab boundaries not found")
    prefs, rest = text[:tabs[1]], text[tabs[1]:]
    for old, new in POSITIONS.items():
        key = f'<Widget type="HBox" position="{old}">'
        if prefs.count(key) != 1:
            raise RuntimeError(f"Expected precisely one native Prefs row: {key}")
        prefs = prefs.replace(key, f'<Widget type="HBox" position="{new}">')
    if prefs.count(ANCHOR) != 1:
        raise RuntimeError("XB77 native Prefs insertion anchor changed upstream")
    prefs = prefs.replace(ANCHOR, REPLACEMENT)
    output = prefs + rest

    # Test the first tab in isolation because this upstream layout contains a
    # pre-existing duplicate name attribute in a later, unrelated tab.
    first = output.index('            <Widget type="TabItem">')
    second = output.index('            <Widget type="TabItem">', first + 50)
    parsed = ET.fromstring("<Root>" + output[first:second] + "</Root>")
    matching = [w for w in parsed.iter("Widget") if w.get("name") == "XB77HighContrastButton"]
    if len(matching) != 1:
        raise RuntimeError("XB77 toggle is not present once in native Prefs tab")
    props = {p.get("key"): p.get("value") for p in matching[0].findall("UserString")}
    if props != {"SettingCategory": "GUI", "SettingName": "xb77 high contrast dialogue", "SettingType": "CheckButton"}:
        raise RuntimeError(f"Incorrect native XB77 settings binding: {props}")
    layout.write_bytes((b"\xef\xbb\xbf" if bom else b"") + output.replace("\n", newline).encode("utf-8"))
    print("XB77: native Prefs toggle patched and structurally verified.")


if __name__ == "__main__":
    main(Path(sys.argv[1] if len(sys.argv) > 1 else "upstream"))
