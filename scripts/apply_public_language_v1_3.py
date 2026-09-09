#!/usr/bin/env python3
"""Final human-language polish after automated label translation."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REPLACEMENTS = {
    # Remove mechanical label combinations created by the first translation pass.
    "tarikh MASIH DISEMAK DAKWAAN terdahulu tidak tepat": "tarikh dalam dakwaan awal tidak tepat",
    "MASIH DISEMAK DAKWAAN 7 September": "Dakwaan awal 7 September",
    "MASIH DISEMAK · DAKWAAN": "DAKWAAN · BELUM DISAHKAN",
    "arah DAKWAAN": "arah dakwaan",
    "Hasil: arah DAKWAAN": "Hasil: arah dakwaan",
    "hasil: arah DAKWAAN": "Hasil: arah dakwaan",
    "<article><b>perbezaan</b>": "<article><b>SEMAKAN TARIKH</b>",
    "Rekod asal untuk perbandingan SEMAKAN.": "Rekod asal untuk perbandingan selepas semakan.",
    "dakwaan asal: 10 Sep": "Dakwaan asal: 10 Sep",
    "hasil: arah dakwaan": "Hasil: arah dakwaan",

    # Make figures and labels easier for non-specialists.
    "RM10.2b beban pemulihan UJSB + RM2.6b susut nilai ditanggung TH":
        "RM10.2 bilion beban pemulihan UJSB + RM2.6 bilion susut nilai ditanggung TH",
    "Docket semasa": "Status semasa",
    "Docket dan legenda": "Status dan panduan label",

    # Public metadata/current-state consistency.
    "CASEFILE RCI Tabung Haji v18: RCI, penguatkuasaan, individu, 14 pelaburan, tadbir urus, UJSB, pertikaian rekod, jurang bukti dan sumber awam hingga lewat malam 7 September 2026.":
        "RCI Tabung Haji: penguatkuasaan, individu, 14 pelaburan, tadbir urus, UJSB, pertikaian rekod, jurang bukti dan sumber awam, dengan perkembangan disemak hingga 9 September 2026.",
    "CASEFILE · RCI-TH-2026 · v18": "SIASATAN · RCI-TH-2026 · dikemas kini 9 Sep",
    "Perkembangan terkini, individu, timeline, jejak wang dan sumber untuk siasatan RCI Tabung Haji":
        "Perkembangan terkini, individu, garis masa, jejak wang dan sumber untuk siasatan RCI Tabung Haji",
    "timeline, jejak wang": "garis masa, jejak wang",
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
    print(f"Public Language V1.3: changed {len(changed)} HTML files")
    for p in changed:
        print(p)


if __name__ == "__main__":
    main()
