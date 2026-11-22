#!/usr/bin/env python3
"""Fail-closed checks against accidentally committing obvious private user data."""
from pathlib import Path
import re
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
files = subprocess.check_output(["git", "-C", str(root), "ls-files"], text=True).splitlines()

bad_paths = [
    re.compile(p, re.IGNORECASE) for p in (
        r"(^|/)(?:logs?|diagnostics?|saves?|screenshots?|private|secrets?|user-data)(/|$)",
        r"\.(?:pfx|p12|pem|key|kdbx|dmp|mp4|avi)$",
        r"(^|/)XB77_(?:CURRENT_STATUS|PROJECT_HANDOFF|ENGINEERING_AUDIT)",
    )
]
bad_content = [
    re.compile(p, re.IGNORECASE) for p in (
        r"[A-Z]:[\\/](?:Users|Documents and Settings)[\\/][^\s\"']+",
        r"(?:OneDrive)[\\/][^\s\"']+",
        r"(?:github_pat_|ghp_|gho_|sk-)[A-Za-z0-9_-]{18,}",
        r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
    )
]
failed = False
for file in files:
    if any(p.search(file) for p in bad_paths):
        print(f"BLOCKED filename: {file}")
        failed = True
        continue
    f = root / file
    if not f.is_file() or f.stat().st_size > 2_000_000:
        continue
    try:
        data = f.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    if any(p.search(data) for p in bad_content):
        print(f"BLOCKED content in: {file}")
        failed = True
if failed:
    sys.exit("Public source hygiene check failed; review locally before pushing.")
print(f"Checked {len(files)} tracked paths for common leaks; manual audit still required.")
