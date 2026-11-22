"""Apply the XB77 v0.9 change-only MyGUI skin patch after source overlay.

A per-topic cache avoids recreating MyGUI skins during every topic-format
refresh. A rebuilt MWList clears the cache. Assert exact anchors so an upstream
change fails visibly rather than silently producing an incorrect executable.
"""
from pathlib import Path
import sys


def substitute_exact(path: Path, old: str, new: str):
    original = path.read_text(encoding="utf-8")
    count = original.count(old)
    if count != 1:
        raise RuntimeError(
            f"Expected exactly one XB77 anchor in {path}; found {count}: {old[:80]!r}"
        )
    path.write_text(original.replace(old, new), encoding="utf-8", newline="")


def main():
    upstream = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("upstream")
    cpp = upstream / "apps/openmw/mwgui/dialogue.cpp"
    hpp = upstream / "apps/openmw/mwgui/dialogue.hpp"

    substitute_exact(
        hpp, "#include <memory>\n",
        "#include <memory>\n#include <string>\n#include <unordered_map>\n"
    )
    substitute_exact(
        hpp,
        "        bool mXB77Applied = false;\n",
        "        bool mXB77Applied = false;\n"
        "        std::unordered_map<std::string, std::string> mXB77TopicSkins;\n"
    )
    substitute_exact(
        cpp,
        "            mKeywords.clear();\n            mTopicsList->clear();\n",
        "            mKeywords.clear();\n            mTopicsList->clear();\n"
        "            mXB77TopicSkins.clear(); // A different actor destroyed the topic widgets.\n"
    )
    substitute_exact(
        cpp,
        "        mTopicsList->clear();\n        for (auto& linkPair",
        "        mTopicsList->clear();\n"
        "        mXB77TopicSkins.clear(); // Topic widgets have been destroyed/rebuilt.\n"
        "        for (auto& linkPair"
    )
    substitute_exact(
        cpp,
        "            if (button->getSkinName() != skin)\n",
        "            const auto previousSkin = mXB77TopicSkins.find(keyword);\n"
        "            if (previousSkin == mXB77TopicSkins.end() || previousSkin->second != skin)\n"
    )
    substitute_exact(
        cpp,
        "                button->setSize(size);\n",
        "                button->setSize(size);\n"
        "                mXB77TopicSkins[keyword] = skin;\n"
    )
    assert "getSkinName()" not in cpp.read_text(encoding="utf-8")
    print("XB77: change-only dialogue skin cache patch applied.")


if __name__ == "__main__":
    main()
