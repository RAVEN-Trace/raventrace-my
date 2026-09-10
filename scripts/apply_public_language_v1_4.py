#!/usr/bin/env python3
"""Last phrase cleanup for Public Language V1."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

for path in ROOT.rglob("*.html"):
    text = path.read_text(encoding="utf-8")
    updated = text.replace("MASIH DISEMAK DAKWAAN", "dakwaan awal")
    if updated != text:
        path.write_text(updated, encoding="utf-8")
        print(path.relative_to(ROOT))
