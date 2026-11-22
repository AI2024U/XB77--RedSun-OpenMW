#!/usr/bin/env python3
"""XB77 release filename and ZIP entry guard.

Always use ASCII alphanumeric, underscores, dashes and periods in distributed ZIP
filenames. In particular, filenames must not contain spaces or URL escapes.

Usage:
    python ci/verify_release_filename.py XB77_RedSun_OpenMW_Celestial_A_QA.zip
    python ci/verify_release_filename.py XB77_RedSun_OpenMW_Celestial_A_QA.zip --name-only

The latter supports checking CI artifact names before a ZIP exists.
"""
from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path, PurePosixPath

SAFE_ZIP = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]*\.zip\Z", re.ASCII)


def verify(path_text: str, name_only: bool = False) -> None:
    filename = Path(path_text).name
    if not SAFE_ZIP.fullmatch(filename):
        raise ValueError(
            "Unsafe XB77 release filename: use only ASCII letters, digits, "
            "underscores, hyphens and periods; no spaces, percent signs, or URL escaping. "
            f"Received: {filename!r}"
        )
    if name_only:
        print(f"PASS: safe XB77 release name: {filename}")
        return

    path = Path(path_text)
    if not path.is_file():
        raise ValueError(f"Release ZIP missing: {path}")
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if not names:
            raise ValueError("Release ZIP has no entries")
        for member in names:
            parts = PurePosixPath(member).parts
            if ("%" in member or "\\" in member or member.startswith("/")
                    or ".." in parts):
                raise ValueError(f"Unsafe or encoded ZIP entry: {member!r}")
        if len(set(names)) != len(names):
            raise ValueError("Duplicate archive entries detected")
        corrupt = archive.testzip()
        if corrupt is not None:
            raise ValueError(f"Corrupt ZIP member: {corrupt}")
    print(f"PASS: {filename}; {len(names)} clean ZIP entries; CRC verified")


def main() -> int:
    if len(sys.argv) not in {2, 3} or (len(sys.argv) == 3 and sys.argv[2] != "--name-only"):
        print("Usage: verify_release_filename.py ZIP_PATH [--name-only]", file=sys.stderr)
        return 2
    try:
        verify(sys.argv[1], "--name-only" in sys.argv)
    except (ValueError, OSError, zipfile.BadZipFile) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
