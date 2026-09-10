#!/usr/bin/env python3
"""Final vocabulary polish for Public Language V1."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPLACEMENTS = {
    "developing claim": "dakwaan awal",
    "Developing claim": "Dakwaan awal",
    "arah umum DAKWAAN": "arah umum dakwaan",
    "DAKWAAN itu": "dakwaan itu",
    "DAKWAAN tersebut": "dakwaan tersebut",
    "remunerasi": "imbuhan",
    "tarikh spesifik": "tarikh khusus",
    "butiran spesifik": "butiran khusus",
}

for path in ROOT.rglob("*.html"):
    text = path.read_text(encoding="utf-8")
    updated = text
    for old, new in REPLACEMENTS.items():
        updated = updated.replace(old, new)
    if updated != text:
        path.write_text(updated, encoding="utf-8")
        print(path.relative_to(ROOT))
