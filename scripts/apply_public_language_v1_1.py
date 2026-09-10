#!/usr/bin/env python3
"""RAVEN Public Language V1.1 cleanup pass.

This pass fixes awkward casing/jargon left by V1 and aligns the public-facing
RCI summary with newer verified status already present elsewhere in the repo.
It does not add new allegations or change legal sections/amounts.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

EXACT = {
    # Global public-language cleanup
    "Data masa semakan": "Maklumat disemak hingga",
    "Data cut-off": "Maklumat disemak hingga",
    "Baca keputusan verifikasi": "Baca keputusan semakan",
    "keputusan verifikasi": "keputusan semakan",
    "Lihat DAKWAAN asal + SEMAKAN": "Lihat dakwaan asal + semakan",
    "Semak DAKWAAN asal": "Semak dakwaan asal",
    "DAKWAAN tarikh": "dakwaan tarikh",
    "DAKWAAN asal": "dakwaan asal",
    "Baca briefing": "Baca ringkasan",
    "Buka CASEFILE penuh": "Buka siasatan penuh",
    "Kongsi casefile": "Kongsi siasatan",
    "legal state": "status undang-undang",
    "jumlah kumulatif": "jumlah terkumpul",
    "· kumulatif": "· jumlah terkumpul",
    "angka agregat": "angka keseluruhan",
    "Prinsip desk": "Prinsip kami",
    "Timeline penuh": "Garis masa penuh",
    "Timeline": "Garis masa",
    "Unknowns": "Belum diketahui",
    "Confidence": "Tahap keyakinan",
    "Medium–High": "Sederhana–Tinggi",
    "HIGH": "TINGGI",
    "MEDIUM": "SEDERHANA",
    "LOW": "RENDAH",
    "Inferens": "Kesimpulan sementara",
    "Spekulasi": "Andaian",
    "Beratribusi": "Dinyatakan oleh sumber",
    "corroboration bebas": "pengesahan bebas",
    "Bilangan outlet": "Bilangan media",
    "outlet": "media",
    "Source Room": "Sumber & dokumen",
    "People ledger": "Individu & status",
    "People & status ledger": "Individu & status",
    "Evidence room": "Bilik bukti",
    "Casefile hidup": "Siasatan yang dikemas kini",
    "public evidence room": "bilik bukti awam",
    "forensic narrative investigator": "penyiasat naratif berasaskan bukti",
    "explainer-reporter": "wartawan penerang",
    "repeatable": "boleh diulang",
    "framework": "kaedah",
    "publication": "penerbitan",
    "drafting": "penulisan draf",
    "Vox-pop": "Temu bual awam",
    "Evidence reconciliation": "Semakan silang bukti",
    "disputed metric": "angka yang dipertikaikan",
    "reconcile": "diselesaikan",
    "bailout": "bantuan kewangan",
    "acquittal": "pembebasan oleh mahkamah",
    "charge sheet": "kertas pertuduhan",
    "impairment": "susut nilai",
    "refinancing": "pembiayaan semula",
    "recovery": "pemulihan",
    "hearsay": "cerita tanpa sumber langsung",
    "spin": "cara cerita dibingkaikan",
    "workflow": "aliran kerja",
    "checkpoint": "semakan",
    "verification": "semakan",
    "developing claim": "dakwaan awal",
    "claim": "dakwaan",
    "FACT": "FAKTA",
    "CLAIM": "DAKWAAN",
    "UNKNOWN": "BELUM DIKETAHUI",
    "DISPUTED": "DIPERTIKAIKAN",
    "PARTIAL CONFIRMATION": "SEPARA DISAHKAN",
    "PARTIAL": "SEPARA",
    "VERIFIED DELTA": "PERBEZAAN YANG DISAHKAN",
    "CHECKPOINT": "SEMAKAN",
    "DEVELOPING": "MASIH DISEMAK",

    # Reader-facing phrasing improvements
    "Apa yang rekod boleh bawa?": "Apa yang boleh kita simpulkan daripada rekod?",
    "Bukan satu cerita.<br><em>Beberapa trek bergerak serentak.</em>": "Bukan satu cerita sahaja.<br><em>Beberapa siasatan bergerak serentak.</em>",
    "Trek siasatan": "Siasatan berasingan",
    "Ruang sumber": "Sumber & dokumen",
    "Evidence one click away": "Bukti satu klik sahaja",

    # RCI current-summary consistency — values already verified on homepage/newsroom.
    "CASEFILE RCI Tabung Haji v18: RCI, penguatkuasaan, individu, 14 pelaburan, tadbir urus, UJSB, pertikaian rekod, jurang bukti dan sumber awam hingga lewat malam 7 September 2026.":
        "Siasatan RCI Tabung Haji: RCI, penguatkuasaan, individu, 14 pelaburan, tadbir urus, UJSB, pertikaian rekod, jurang bukti dan sumber awam, dengan perkembangan semasa hingga 9 September 2026.",
    "Data masa semakan · 7 Sep 2026 · lewat malam MYT": "Maklumat disemak hingga · 9 Sep 2026 · 18:29 MYT",
    "Revisi laman · 7 Sep 2026 · v18": "Kemas kini semasa · 9 Sep 2026",
    "<div><dt>02</dt><dd>individu THP Bina didakwa · belum sabit</dd></div>":
        "<div><dt>03</dt><dd>individu didakwa setakat 9 Sep · belum sabit</dd></div>",
    "RCI merekodkan kelemahan serius dalam tadbir urus, pelaburan dan pelaporan kewangan TH serta mengesyorkan pemeriksaan lanjut terhadap 14 pelaburan. SPRM kemudian membuka 14 kertas siasatan; empat diklasifikasikan NFA setakat 2 September. Dua bekas pengurus THP Bina telah didakwa dan mengaku tidak bersalah. Bagi beberapa kertas lain, SPRM mengumumkan cadangan pertuduhan, tetapi CASEFILE ini tidak menyamakan pengumuman tersebut dengan pertuduhan yang benar-benar telah dibaca di mahkamah tanpa rekod prosiding yang boleh disahkan.":
        "RCI merekodkan kelemahan serius dalam tadbir urus, pelaburan dan pelaporan kewangan TH serta mengesyorkan pemeriksaan lanjut terhadap 14 pelaburan. SPRM kemudian membuka 14 kertas siasatan; empat diklasifikasikan tiada tindakan lanjut (NFA) setakat 2 September. Setakat 9 September, tiga individu telah didakwa dalam tindakan susulan berkaitan RCI dan semuanya belum disabitkan. RAVEN-Trace hanya menganggap seseorang sudah didakwa apabila pertuduhan benar-benar dapat disahkan melalui rekod mahkamah atau laporan yang kukuh.",
    "Dua bekas pengurus THP Bina telah didakwa dan mengaku tidak bersalah.":
        "Dua bekas pengurus THP Bina telah didakwa dan mengaku tidak bersalah.",
}

# Exact visible-text replacements should not modify attributes/URLs/JSON-LD.
TOKEN_RE = re.compile(r"(<script\b.*?</script\s*>|<style\b.*?</style\s*>|<[^>]+>)", re.I | re.S)


def clean_text(text: str) -> str:
    # Longest first so phrases win before single words.
    for old, new in sorted(EXACT.items(), key=lambda kv: len(kv[0]), reverse=True):
        text = text.replace(old, new)
    # Fix all-caps label leakage when the word sits inside normal running text.
    text = re.sub(r"(?<![A-Z])\bDAKWAAN\s+(tarikh|asal)\b", lambda m: "dakwaan " + m.group(1), text)
    text = re.sub(r"\bSEMAKAN\s*→", "semakan →", text)
    return text


def process_html(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    parts = TOKEN_RE.split(original)
    out = []
    for part in parts:
        if not part or part.startswith("<"):
            out.append(part)
        else:
            out.append(clean_text(part))
    updated = "".join(out)

    # Metadata-only cleanups that are safe and intentional.
    updated = updated.replace("legal state", "status undang-undang")

    if updated == original:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def main() -> None:
    changed = []
    for path in sorted(ROOT.rglob("*.html")):
        if ".git" in path.parts:
            continue
        if process_html(path):
            changed.append(path.relative_to(ROOT).as_posix())

    print(f"Public Language V1.1: changed {len(changed)} HTML files")
    for p in changed:
        print(p)


if __name__ == "__main__":
    main()
