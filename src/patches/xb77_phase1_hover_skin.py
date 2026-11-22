"""XB77 Phase 1 TEST07 resource-only mouse-hover accessibility patch.
Apply to the *packaged* OpenMW 0.52 Red Sun list skin:
  python ci/xb77_phase1_hover_skin.py path/to/openmw_list.skin.xml
It does not change controller navigation or executable C++.
"""
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

if len(sys.argv) != 2:
    raise SystemExit("Usage: python ci/xb77_phase1_hover_skin.py <openmw_list.skin.xml>")
path=Path(sys.argv[1])
original=path.read_text(encoding="utf-8")
updated=original
names=("XB77_MW_ListLine","XB77_MW_ListLine_Specific","XB77_MW_ListLine_Exhausted")
for name in names:
    pattern=r'(<Resource\s+type="ResourceSkin"\s+name="'+re.escape(name)+r'"[\s\S]*?</Resource>)'
    matches=list(re.finditer(pattern,updated))
    if len(matches)!=1:
        raise RuntimeError(f"{name}: found {len(matches)} exact resource blocks; expected one")
    match=matches[0]
    block=match.group(1)
    # First four states are outer border pieces; fifth is the arrow.
    before='name="highlighted" offset="2 0 2 2"'
    if block.count(before)!=5:
        raise RuntimeError(f"{name}: unexpected source subskin count")
    changed=block.replace(before,'name="highlighted" offset="0 0 2 2"',4)
    changed=changed.replace(before,'name="highlighted" offset="4 0 7 11"',1)
    changed=re.sub(r'(<State name="highlighted" colour=")[^"]+(")',
                   r'\g<1>#FFE500\g<2>',changed)
    if 'name="highlighted" colour="#FFE500"' not in changed:
        raise RuntimeError(f"{name}: hovered yellow text was not installed")
    updated=updated[:match.start(1)]+changed+updated[match.end(1):]
if updated==original:
    raise RuntimeError("No change made")
ET.fromstring(updated)
# No original Morrowind or non-XB77 skin blocks may be edited.
def remove_xb77_blocks(text):
    for name in names:
        pattern=r'<Resource\s+type="ResourceSkin"\s+name="'+re.escape(name)+r'"[\s\S]*?</Resource>'
        text=re.sub(pattern,'<Resource name="'+name+'" />',text)
    return text
if remove_xb77_blocks(original)!=remove_xb77_blocks(updated):
    raise RuntimeError("Unexpected modification of non-XB77 skins")
path.write_text(updated,encoding="utf-8",newline="")
print("XB77 TEST07: three custom skins updated; XML validated; non-XB77 skins unchanged.")
