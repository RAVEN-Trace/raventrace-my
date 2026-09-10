#!/usr/bin/env python3
"""Final deterministic cleanup for RAVEN Public Language V1.

Only exact, low-risk string replacements are used. This pass exists to catch
phrases that can appear across metadata or generated fragments outside normal
text nodes.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REPLACEMENTS = {
    "DAKWAAN asal": "dakwaan asal",
    "DAKWAAN tarikh": "dakwaan tarikh",
    "SEMAKAN →": "semakan →",
    "Unknowns": "Belum diketahui",
    "Data masa semakan": "Maklumat disemak hingga",
    "Data cut-off": "Maklumat disemak hingga",
    "Baca keputusan verifikasi": "Baca keputusan semakan",
    "keputusan verifikasi": "keputusan semakan",
    "Semak DAKWAAN asal": "Semak dakwaan asal",
    "Lihat DAKWAAN asal + SEMAKAN": "Lihat dakwaan asal + semakan",
    "Baca briefing": "Baca ringkasan",
    "Buka CASEFILE penuh": "Buka siasatan penuh",
    "Kongsi casefile": "Kongsi siasatan",
    "legal state": "status undang-undang",
    "Timeline penuh": "Garis masa penuh",
    ">Timeline<": ">Garis masa<",
    ">Confidence<": ">Tahap keyakinan<",
    "Confidence</dt>": "Tahap keyakinan</dt>",
    "Medium–High": "Sederhana–Tinggi",
    "People ledger": "Individu & status",
    "Source Room": "Sumber & dokumen",
    "Claim bukan fact": "Dakwaan bukan fakta",
    "Release bukan NFA": "Dilepaskan tidak bermaksud kes ditutup",
}


def main():
    changed = []
    for path in sorted(ROOT.rglob("*.html")):
        original = path.read_text(encoding="utf-8")
        updated = original
        for old, new in REPLACEMENTS.items():
            updated = updated.replace(old, new)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed.append(path.relative_to(ROOT).as_posix())
    print(f"Public Language V1.2: changed {len(changed)} HTML files")
    for p in changed:
        print(p)


if __name__ == "__main__":
    main()
