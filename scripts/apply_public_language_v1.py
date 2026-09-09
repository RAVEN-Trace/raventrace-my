#!/usr/bin/env python3
"""Apply RAVEN Public Language Standard V1 to public-facing HTML.

This is an editorial post-processor. It does not change source URLs, IDs, legal
sections, dates, amounts or evidence grades. It simplifies public wording while
leaving scripts/styles/structured data untouched.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

# Exact phrases with context-specific rewrites. Longest/specific phrases first.
RAW_REPLACEMENTS = {
    # Brand/public positioning
    "Independent · Evidence-led · Malaysia": "Bebas · Berasaskan bukti · Malaysia",
    "Story first.<br>Evidence one click away.": "Cerita dahulu.<br>Bukti satu klik sahaja.",
    "Public evidence room<br>Casefile hidup": "Bilik bukti awam<br>Siasatan yang dikemas kini",

    # Homepage — lead and reader journey
    "Tabung Haji selepas RCI:<br>Apa yang rosak, siapa sedang disiasat —<br><em>dan apa yang masih belum terbukti.</em>":
        "Tabung Haji selepas RCI:<br>Apa yang RCI temui, siapa sedang disiasat —<br><em>dan apa yang masih belum terbukti.</em>",
    "RCI merekodkan kelemahan tadbir urus dan 14 pelaburan yang memerlukan pemeriksaan lanjut. Setakat 9 September, tiga individu telah didakwa dalam tindakan susulan berkaitan RCI. Pada hari sama, PDRM turut mengesahkan trek siasatan berasingan berkaitan hibah 2017 dan AMLA. Pertuduhan, tangkapan dan reman bukan sabitan.":
        "RCI menemui kelemahan dalam cara Tabung Haji diurus dan meminta 14 pelaburan diperiksa dengan lebih lanjut. Setakat 9 September, tiga individu telah didakwa dalam tindakan susulan berkaitan RCI. Polis pula mengesahkan siasatan berasingan mengenai hibah 2017 dan isu di bawah AMLA. Penting: ditahan, direman atau didakwa tidak bermaksud seseorang sudah bersalah.",
    "Kami utamakan perkembangan yang mengubah cara kes ini perlu difahami — dan merekod apabila claim lama tepat, separa tepat atau salah.":
        "Kami utamakan perubahan yang betul-betul mengubah cerita. Jika dakwaan lama ternyata tepat, separa tepat atau salah, rekod asal tidak dipadam — kami tunjuk apa yang berubah.",
    "Bernama mengesahkan Abdul Azeez didakwa di bawah Seksyen 23(1) Akta SPRM 2009 berkaitan penggunaan kedudukan dan cadangan pelaburan RM193.5 juta dalam Putrajaya Perdana. Beliau mengaku tidak bersalah. Developing claim 7 September menjangka pertuduhan pada 10 September; prosiding sebenar berlaku 9 September.":
        "Bernama mengesahkan Abdul Azeez didakwa di bawah Seksyen 23(1) Akta SPRM 2009 berkaitan dakwaan penggunaan kedudukan dan cadangan pelaburan RM193.5 juta dalam Putrajaya Perdana. Beliau mengaku tidak bersalah. Laporan awal 7 September menjangka pertuduhan pada 10 September, tetapi prosiding sebenar berlaku pada 9 September.",
    "Claim asal dikekalkan untuk audit. Outcome bagi Azeez kini disahkan, tetapi tarikh spesifik yang diberi salah satu laporan tidak tepat. Azmi mempunyai prosiding yang dijadualkan pada 10 September; Jamil kekal belum disahkan didakwa pada cut-off ini.":
        "Dakwaan asal dikekalkan supaya pembaca boleh melihat apa yang berubah. Bagi Azeez, pertuduhan kini disahkan tetapi tarikh yang diberi salah satu laporan tidak tepat. Status Azmi dan Jamil perlu dibaca mengikut rekod mahkamah atau kenyataan rasmi terkini.",
    "Pembebasan daripada reman bukan NFA, acquittal atau penentuan bahawa seseorang tidak bersalah; status siasatan dan kemungkinan tindakan lanjut mesti dinilai berasingan.":
        "Dilepaskan daripada reman tidak bermaksud kes sudah ditutup atau seseorang telah dibersihkan daripada semua siasatan. Status seterusnya perlu dilihat pada rekod rasmi.",
    "RAVEN-Trace tidak hanya memberi kesimpulan. Kami tunjuk sumber, konteks yang hilang, perkara yang masih bercanggah dan apa yang belum diketahui.":
        "RAVEN-Trace tidak hanya memberi kesimpulan. Kami tunjuk sumber, konteks yang mungkin hilang, perkara yang masih bercanggah dan apa yang belum diketahui.",
    "Claim → checkpoint → verification": "Dakwaan → kami semak → apa yang terbukti",
    "Reman, bebas, didakwa, belum sabit": "Direman, dilepaskan, didakwa, belum sabit",
    "Transaksi, kerugian, impairment, refinancing": "Transaksi, kerugian, susut nilai, pembiayaan semula",
    "Claim lama tidak dipadam. Delta direkod supaya pembaca boleh melihat apa yang berubah.":
        "Dakwaan lama tidak dipadam. Kami rekod apa yang berubah supaya pembaca boleh melihat perjalanan bukti.",

    # Investigations index
    "Pintu masuk kepada siasatan mendalam RAVEN-Trace. Rekod yang disahkan, proses penguatkuasaan, prosiding mahkamah, developing claim dan perkara yang masih terbuka dipisahkan supaya status tidak bercampur.":
        "Di sinilah siasatan mendalam RAVEN-Trace bermula. Kami asingkan perkara yang sudah disahkan, tindakan penguatkuasaan, proses mahkamah, dakwaan yang masih diuji dan perkara yang belum diketahui supaya pembaca tidak mencampurkan status yang berbeza.",
    "1 CASEFILE aktif": "1 siasatan utama aktif",
    "Lead investigation · aktif": "Siasatan utama · aktif",
    "Evidence state · evolving": "Status bukti · masih berubah",
    "Verification delta": "Apa yang berubah selepas semakan?",
    "Developing claim 7 September menjangka Azeez didakwa pada <strong>10 September</strong>. Rekod mahkamah menunjukkan prosiding sebenar berlaku <strong>9 September</strong>. Raven mengekalkan claim asal dan merekod perbezaan itu.":
        "Laporan awal 7 September menjangka Azeez didakwa pada <strong>10 September</strong>. Rekod mahkamah menunjukkan prosiding sebenar berlaku pada <strong>9 September</strong>. Kami kekalkan laporan asal dan tunjuk perbezaan itu supaya pembaca boleh menilai ketepatannya.",
    "Tamat reman bukan NFA, acquittal atau penentuan salah/tidak salah. Siasatan berkaitan hotel TH di Arab Saudi kekal perlu dibaca berasingan daripada claim pendakwaan kemudian.":
        "Tamat reman tidak bermaksud fail ditutup dan tidak menentukan seseorang bersalah atau tidak. Siasatan berkaitan hotel TH di Arab Saudi juga perlu dibaca berasingan daripada laporan pendakwaan yang muncul kemudian.",
    "RCI ialah titik mula. Selepas itu, pembaca perlu membezakan enforcement, mahkamah, wang, reform institusi dan rekod yang masih dipertikaikan.":
        "RCI ialah titik mula. Selepas itu, beberapa perkara bergerak serentak: siasatan penguatkuasaan, mahkamah, wang, pembaharuan institusi dan rekod yang masih dipertikaikan.",
    "RM13b, impairment, recovery, refinancing": "RM13b, susut nilai, pemulihan, pembiayaan semula",
    "<strong>FACT:</strong> RCI merekodkan kelemahan serius dan tindakan susulan sedang berjalan. <strong>UNKNOWN:</strong> hasil akhir setiap fail dan liabiliti akhir setiap individu.":
        "<strong>FAKTA:</strong> RCI merekodkan kelemahan serius dan tindakan susulan sedang berjalan. <strong>BELUM DIKETAHUI:</strong> hasil akhir setiap fail dan sama ada mana-mana individu akhirnya akan disabitkan.",
    "Elak shortcut yang mengelirukan.": "Elak kesimpulan cepat yang mengelirukan.",
    "Claim 11 dan 17 September kekal checkpoint — bukan fakta.": "Tarikh 11 dan 17 September kekal dakwaan yang perlu disemak — bukan fakta.",
    "Laporan 7 September menyebut tarikh bagi Azmi dan Jamil. Raven hanya akan menaik taraf status selepas rekod mahkamah atau pengesahan rasmi tersedia.":
        "Laporan 7 September menyebut tarikh bagi Azmi dan Jamil. Status hanya akan dinaik taraf selepas rekod mahkamah atau pengesahan rasmi tersedia.",

    # RCI CASEFILE opening layer
    "Evidence room awam yang memisahkan dapatan RCI, siasatan penguatkuasaan, prosiding mahkamah, dakwaan politik dan perkara yang masih belum diketahui.":
        "Bilik bukti awam yang memisahkan apa yang RCI temui, apa yang sedang disiasat, apa yang sudah sampai ke mahkamah, apa yang hanya dakwaan dan apa yang masih belum diketahui.",
    "Masalah institusi direkodkan. Liabiliti jenayah individu masih perlu dibuktikan.":
        "RCI memang menemui masalah. Tetapi siapa yang melakukan kesalahan jenayah masih perlu dibuktikan.",
    "Kes ini tidak patut dipermudahkan kepada dua slogan: “semua dicuri” atau “tiada apa berlaku”. Rekod menunjukkan gambaran yang lebih kompleks.":
        "Kes ini tidak boleh diringkaskan kepada dua slogan: “semua dicuri” atau “tiada apa berlaku”. Rekod menunjukkan cerita yang lebih rumit — dan setiap bahagian perlu dibuktikan berasingan.",
    "RM13b bukan label “wang dicuri”.": "RM13 bilion tidak sama dengan “wang dicuri”.",
    "Audit bukan siasatan jenayah.": "Audit dan siasatan jenayah ialah dua perkara berbeza.",
    "Kes mahkamah baru bermula.": "Proses mahkamah masih di peringkat awal.",
    "Enam perkembangan yang mengubah kedudukan kes.": "Apa yang berubah setakat ini?",
    "People & status ledger": "Individu dan status",
    "14 rekod pelaburan": "14 pelaburan yang diperiksa",
    "Madinah vs RCI": "Pertikaian rekod Madinah",
    "Soalan terbuka": "Apa yang masih belum diketahui",

    # Newsroom
    "Berita terbaru muncul dahulu. Developing claim tidak dipadam apabila dunia berubah; kami tambah checkpoint dan tunjuk apa yang tepat, separa tepat atau salah.":
        "Berita terbaru muncul dahulu. Dakwaan awal tidak dipadam apabila fakta baharu muncul; kami tambah semakan dan tunjuk apa yang tepat, separa tepat atau salah.",
    "Claim asal kekal dalam rekod. Outcome bagi Azeez kini disahkan, tetapi tarikh 10 September yang dilaporkan salah satu outlet tidak tepat. Claim bagi Azmi dan Jamil kekal belum disahkan pada cut-off ini.":
        "Dakwaan asal kekal dalam rekod. Bagi Azeez, pertuduhan kini disahkan tetapi tarikh 10 September yang dilaporkan salah satu media tidak tepat. Status Azmi dan Jamil perlu disahkan secara berasingan melalui rekod rasmi.",
    "RM11.5 bilion sukuk UJSB bukan bailout baharu": "RM11.5 bilion sukuk UJSB bukan bantuan kewangan baharu",

    # Story articles — common reader-facing simplifications
    "Claim bukan fact.<br>Tarikh mesti diuji.": "Dakwaan bukan fakta.<br>Tarikh mesti disemak.",
    "Release bukan NFA.<br>Reman bukan sabitan.": "Dilepaskan bukan bermaksud kes ditutup.<br>Reman bukan sabitan.",
    "Developing claim 7 September kini diuji: Abdul Azeez didakwa pada 9 September, bukan 10 September seperti tarikh spesifik yang dilaporkan salah satu outlet.":
        "Dakwaan awal 7 September kini sudah diuji: Abdul Azeez didakwa pada 9 September, bukan 10 September seperti tarikh yang dilaporkan salah satu media.",
    "Mahkamah mengesahkan pertuduhan Abdul Azeez pada 9 September. Raven membandingkan rekod sebenar dengan developing claim terdahulu dan mengekalkan perbezaan tarikh sebagai rekod audit.":
        "Rekod mahkamah mengesahkan pertuduhan Abdul Azeez pada 9 September. Kami bandingkan rekod sebenar dengan dakwaan awal dan kekalkan perbezaan tarikh supaya pembaca boleh melihat apa yang berubah.",
    "Raven verification checkpoint": "Apa yang berubah selepas kami semak?",
    "Specificity bukan pengesahan. Dua outlet juga boleh bergantung pada sumber asal yang sama.":
        "Butiran yang sangat spesifik masih bukan bukti dengan sendirinya. Dua media juga boleh bergantung pada sumber asal yang sama.",
    "Selepas checkpoint Azeez pada 9 September, tarikh 11 September bagi Azmi dan 17 September bagi Jamil kekal sebagai claim yang belum disahkan.":
        "Selepas semakan Azeez pada 9 September, tarikh 11 September bagi Azmi dan 17 September bagi Jamil kekal sebagai dakwaan yang belum disahkan.",
    "Release ≠ NFA": "Dilepaskan ≠ kes ditutup",
    "Release bukan NFA dan bukan pertuduhan.": "Dilepaskan tidak bermaksud kes ditutup dan bukan pertuduhan.",
    "Tiada charge sheet atau pertuduhan baharu yang boleh disahkan setakat cut-off malam ini.":
        "Tiada kertas pertuduhan atau pertuduhan baharu yang boleh disahkan setakat masa semakan ini.",
    "baseline status sebelumnya": "status rujukan sebelumnya",
    "People ledger": "Individu & status",
    "Source Room": "Sumber & dokumen",

    # Methodology
    "Human clarity lock": "Bahasa mudah",
    "Source-link rule": "Peraturan pautan sumber",
    "Ayat seperti NFA, impairment atau charge sheet": "Istilah seperti NFA, susut nilai atau kertas pertuduhan",
    "Intake": "Terima petunjuk",
    "Preserve": "Simpan bahan asal",
    "Triage": "Tapis perkara penting",
    "Verify": "Semak",
    "Brief": "Terangkan",
    "Publish / Hold": "Terbit / Tahan",
    "Correct": "Betulkan",

    # About
    "RAVEN-Trace Malaysia ialah publication penyiasatan dan explainer yang menguji dakwaan awam terhadap rekod yang boleh diperiksa, memisahkan fakta daripada dakwaan, spin dan perkara yang belum diketahui, kemudian menerangkannya dengan bahasa yang boleh difahami pembaca biasa.":
        "RAVEN-Trace Malaysia ialah penerbitan penyiasatan yang menyemak dakwaan awam terhadap rekod yang boleh diperiksa. Kami asingkan fakta, dakwaan, cara sesuatu cerita dibingkaikan dan perkara yang belum diketahui — kemudian terangkan semuanya dalam bahasa yang mudah diikuti.",
    "Raven ialah identiti editorial penyiasatan RAVEN-Trace: forensic narrative investigator dan explainer-reporter yang menjejak sumber, menguji percanggahan dan menjaga batas bukti. RAVEN-Trace Protocol ialah kaedah repeatable untuk membina timeline, menilai kekuatan bukti, membezakan fakta daripada dakwaan dan menunjukkan perkara yang masih belum diketahui.":
        "Raven ialah identiti editorial penyiasatan RAVEN-Trace: penyiasat naratif berasaskan bukti yang menjejak sumber, menguji percanggahan dan menjaga batas bukti. RAVEN-Trace Protocol ialah kaedah kerja yang boleh diulang untuk membina garis masa, menilai kekuatan bukti, membezakan fakta daripada dakwaan dan menunjukkan perkara yang masih belum diketahui.",
    "Pembaca tidak perlu memahami keseluruhan framework untuk membaca berita. Artikel datang dahulu; evidence room kekal satu klik di belakangnya.":
        "Pembaca tidak perlu memahami seluruh kaedah dalaman untuk membaca berita. Cerita datang dahulu; bukti dan dokumen kekal satu klik di belakangnya.",
    "RAVEN-Trace™ dibangunkan sebagai publication dan sistem penyiasatan bebas untuk pembaca Malaysia.":
        "RAVEN-Trace™ dibangunkan sebagai penerbitan dan sistem penyiasatan bebas untuk pembaca Malaysia.",
    "AI-assisted workflow:": "Aliran kerja dibantu AI:",
    "penyelidikan, analisis, penyusunan dan drafting boleh menggunakan sistem AI sebagai alat kerja.":
        "penyelidikan, analisis, penyusunan dan penulisan draf boleh menggunakan sistem AI sebagai alat kerja.",

    # Tips
    "Send a tip": "Hantar petunjuk",
    "Corroboration": "Pengesahan bebas",
    "Preserve before interpret": "Simpan bahan asal sebelum membuat kesimpulan",
    "forward yang kehilangan konteks": "mesej yang diteruskan tanpa konteks penuh",
    "Unknown yang jelas lebih bertanggungjawab daripada jaminan yang tidak boleh dipenuhi.":
        "Mengaku bahawa sesuatu belum tersedia lebih bertanggungjawab daripada memberi jaminan keselamatan yang kita belum mampu penuhi.",

    # Corrections
    "Ledger semasa": "Rekod semasa",
    "v16 · Human Clarity · Visual Journalism · Evidence Reconciliation.":
        "v16 · Bahasa Mudah · Visual Berita · Semakan Silang Bukti.",
    "Bagaimana ledger berfungsi:": "Bagaimana rekod ini berfungsi:",
    "Evidence reconciliation": "Semakan silang bukti",
    "outcome Jamil Khir kekal UNKNOWN": "status akhir Jamil Khir ketika itu masih belum diketahui",
    "Metrik bercanggah": "Angka bercanggah",
    "Expectation ≠ fact": "Jangkaan ≠ fakta",
    "Vox-pop": "Temu bual awam",
    "Visual journalism": "Visual berita",
    "Human clarity": "Bahasa mudah",
    "Wording lama": "Ayat lama",
    "Wording penerbitan": "Ayat penerbitan",
    "disputed metric": "angka yang dipertikaikan",
    "reconcile melalui rekod primer": "diselesaikan melalui rekod primer",
    "dataset": "set data",
    "Gred bukti": "Kekuatan bukti",
    "Wording politik": "Ayat politik",
}

# Visible text only: do not touch HTML attributes, URLs, classes, IDs, CSS or JS.
TEXT_REGEX_REPLACEMENTS = [
    (r"\bPARTIAL CONFIRMATION\b", "SEPARA DISAHKAN"),
    (r"\bPARTIAL\b", "SEPARA"),
    (r"\bVERIFIED DELTA\b", "PERBEZAAN YANG DISAHKAN"),
    (r"\bCHECKPOINT\b", "SEMAKAN"),
    (r"\bDEVELOPING\b", "MASIH DISEMAK"),
    (r"\bFACT\b", "FAKTA"),
    (r"\bCLAIM\b", "DAKWAAN"),
    (r"\bUNKNOWN\b", "BELUM DIKETAHUI"),
    (r"\bDISPUTED\b", "DIPERTIKAIKAN"),
    (r"\bINFERENCE\b", "KESIMPULAN SEMENTARA"),
    (r"\bSPECULATION\b", "ANDAIAN"),
    (r"\bHigh confidence\b", "Keyakinan tinggi"),
    (r"\bMedium confidence\b", "Keyakinan sederhana"),
    (r"\bLow confidence\b", "Keyakinan rendah"),
    (r"\bExecutive briefing\b", "Ringkasan mudah"),
    (r"\bLatest evidence snapshot\b", "Apa yang terbaru?"),
    (r"\bCase docket\b", "Status kes"),
    (r"\bBottom line\b", "Kesimpulan setakat ini"),
    (r"\bInvestigation desk\b", "Meja siasatan"),
    (r"\bCurrent case status\b", "Status kes semasa"),
    (r"\bEvidence boundary\b", "Batas bukti"),
    (r"\bNarrative check\b", "Semak naratif"),
    (r"\bNarrative watch\b", "Semak naratif"),
    (r"\bNext verification\b", "Semakan seterusnya"),
    (r"\bVerification delta\b", "Apa yang berubah selepas semakan?"),
    (r"\bverification checkpoint\b", "semakan"),
    (r"\bdeveloping claim\b", "dakwaan awal"),
    (r"\bclaim asal\b", "dakwaan asal"),
    (r"\bclaim\b", "dakwaan"),
    (r"\bcheckpoint\b", "semakan"),
    (r"\bverification\b", "semakan"),
    (r"\bverified through\b", "disemak hingga"),
    (r"\bVerified against\b", "Disemak dengan"),
    (r"\bverified\b", "disemak"),
    (r"\bcut-off\b", "masa semakan"),
    (r"\boutcome\b", "hasil"),
    (r"\bactual\b", "rekod sebenar"),
    (r"\bdelta\b", "perbezaan"),
    (r"\bledger\b", "rekod"),
    (r"\bimpairment\b", "susut nilai"),
    (r"\brefinancing\b", "pembiayaan semula"),
    (r"\brecovery\b", "pemulihan"),
    (r"\bbailout\b", "bantuan kewangan"),
    (r"\bacquittal\b", "pembebasan oleh mahkamah"),
    (r"\bcharge sheet\b", "kertas pertuduhan"),
    (r"\bhearsay\b", "cerita tanpa sumber langsung"),
    (r"\bframework\b", "kaedah"),
    (r"\bpublication\b", "penerbitan"),
    (r"\bPublisher\b", "Penerbit"),
    (r"\bpublisher\b", "penerbit"),
    (r"\bdrafting\b", "penulisan draf"),
    (r"\bSource Room\b", "Sumber & dokumen"),
    (r"\bPeople ledger\b", "Individu & status"),
    (r"\bPeople & status ledger\b", "Individu & status"),
    (r"\bEvidence room\b", "Bilik bukti"),
    (r"\bSource room\b", "Sumber & dokumen"),
    (r"\bCourt & Enforcement Watch\b", "Mahkamah & penguatkuasaan"),
    (r"\bEnforcement Update\b", "Kemas kini penguatkuasaan"),
]

# A tag/script/style splitter sufficient for the repository's static HTML. Script/style
# blocks are preserved byte-for-byte to avoid altering JSON-LD or JavaScript.
TOKEN_RE = re.compile(r"(<script\b.*?</script\s*>|<style\b.*?</style\s*>|<[^>]+>)", re.I | re.S)


def simplify_visible_text(html: str) -> str:
    parts = TOKEN_RE.split(html)
    out = []
    for part in parts:
        if not part or part.startswith("<"):
            out.append(part)
            continue
        text = part
        for pattern, repl in TEXT_REGEX_REPLACEMENTS:
            text = re.sub(pattern, repl, text, flags=re.I)
        out.append(text)
    return "".join(out)


def apply(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    updated = original
    for old, new in sorted(RAW_REPLACEMENTS.items(), key=lambda kv: len(kv[0]), reverse=True):
        updated = updated.replace(old, new)
    updated = simplify_visible_text(updated)
    if updated == original:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def main() -> None:
    changed = []
    for path in sorted(ROOT.rglob("*.html")):
        # .git cannot appear in checkout glob, but keep the guard explicit.
        if ".git" in path.parts:
            continue
        if apply(path):
            changed.append(path.relative_to(ROOT).as_posix())

    # Remove scratch files accidentally created while preparing the branch.
    for scratch in ROOT.glob("docs/test*.txt"):
        scratch.unlink(missing_ok=True)
        changed.append(f"removed:{scratch.relative_to(ROOT).as_posix()}")

    print(f"Public Language V1: changed {len(changed)} items")
    for item in changed:
        print(item)


if __name__ == "__main__":
    main()
