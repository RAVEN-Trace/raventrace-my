from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / 'investigations' / 'rci-tabung-haji' / 'narratives' / 'index.html'
s = PAGE.read_text(encoding='utf-8')

# Refresh hero/method language.
s = s.replace(
    'Ia menguji setiap frame melalui empat lapisan: siapa menggunakannya, apa rekod tunjuk, konteks yang sering tertinggal, dan verdict RAVEN-Trace.',
    'Ia menguji setiap frame melalui lima lapisan: siapa menggunakannya, apa rekod tunjuk, konteks yang sering tertinggal, verdict RAVEN-Trace, dan bukti apa yang boleh mengubah verdict itu.'
)
s = s.replace('Maklumat disemak hingga · 10 Sep 2026 · MYT', 'Maklumat disemak hingga · 11 Sep 2026 · 01:15 MYT')
s = s.replace(
    'Enam naratif paling kerap muncul — dibedah sebagai claim, rekod, konteks yang tertinggal dan verdict.',
    'Lapan naratif utama — dibedah sebagai claim, rekod, konteks yang tertinggal, verdict dan bukti yang boleh mengubahnya.'
)

# Helper to add evidence-change and confidence after each existing verdict.
repls = {
'''<p><b>Verdict Raven:</b> Slogan politik yang merumuskan isu kompleks secara agresif. Rekod menyokong kewujudan masalah serius, tetapi tidak menyokong kesimpulan bahawa setiap kerugian ialah kecurian.</p>''':
'''<p><b>Verdict Raven:</b> Slogan politik yang merumuskan isu kompleks secara agresif. Rekod menyokong kewujudan masalah serius, tetapi tidak menyokong kesimpulan bahawa setiap kerugian ialah kecurian.</p><p><b>Apa yang boleh mengubah verdict?</b> Sabitan mahkamah, asset-tracing atau forensic accounting yang menghubungkan jumlah tertentu kepada appropriation jenayah akan menguatkan dakwaan bagi transaksi atau individu yang terbukti — bukan secara automatik untuk seluruh kerugian TH.</p><p><b>Confidence:</b> Tinggi bahawa slogan digunakan; sederhana-rendah jika digunakan sebagai deskripsi undang-undang menyeluruh. · <b>Last verified:</b> 11 Sep 2026</p>''',
'''<p><b>Verdict Raven:</b> Berdasarkan rekod yang telah disemak, dakwaan bahawa aset TH “dijual kepada China” atau bukan Islam tidak disokong. Status ini tidak dinaikkan kepada “palsu mutlak” tanpa audit dokumen primer penuh.</p>''':
'''<p><b>Verdict Raven:</b> Berdasarkan rekod yang telah disemak, dakwaan bahawa aset TH “dijual kepada China” atau bukan Islam tidak disokong. Status ini tidak dinaikkan kepada “palsu mutlak” tanpa audit dokumen primer penuh.</p><p><b>Apa yang boleh mengubah verdict?</b> SPA, shareholder register, beneficial-ownership record, sukuk terms dan transaction trail primer yang menunjukkan pemilikan atau pelupusan sebenar kepada pihak yang didakwa.</p><p><b>Confidence:</b> Sederhana-tinggi. · <b>Last verified:</b> 11 Sep 2026</p>''',
'''<p><b>Verdict Raven:</b> Soalan dasar yang sah. Perbahasan sebenar ialah mekanisme paling sesuai — RCI baharu, PAC, audit forensik atau siasatan agensi — dan bukannya sama ada tempoh selepas itu langsung tidak patut diperiksa.</p>''':
'''<p><b>Verdict Raven:</b> Soalan dasar yang sah. Perbahasan sebenar ialah mekanisme paling sesuai — RCI baharu, PAC, audit forensik atau siasatan agensi — dan bukannya sama ada tempoh selepas itu langsung tidak patut diperiksa.</p><p><b>Apa yang boleh mengubah verdict?</b> Bukti bahawa mekanisme sedia ada tidak mempunyai kuasa, akses dokumen atau skop yang diperlukan akan menguatkan hujah untuk RCI baharu; bukti bahawa PAC/audit/agensi sudah menjawab jurang yang sama akan melemahkannya.</p><p><b>Confidence:</b> Tinggi bahawa tuntutan ini wujud sebagai posisi dasar. · <b>Last verified:</b> 11 Sep 2026</p>''',
'''<p><b>Verdict Raven:</b> Munasabah sebagai analisis terhadap kesan naratif, tetapi tidak boleh dipersembahkan sebagai fakta tentang niat UMNO, PAS atau mana-mana individu.</p>''':
'''<p><b>Verdict Raven:</b> Munasabah sebagai analisis terhadap kesan naratif, tetapi tidak boleh dipersembahkan sebagai fakta tentang niat UMNO, PAS atau mana-mana individu.</p><p><b>Apa yang boleh mengubah verdict?</b> Minit dalaman, komunikasi strategi, arahan parti atau kenyataan langsung yang menunjukkan tujuan sebenar boleh menaikkan status daripada inference kepada dakwaan motif yang disokong bukti.</p><p><b>Confidence:</b> Sederhana bahawa fokus perbahasan berubah; rendah bagi motif sebenar. · <b>Last verified:</b> 11 Sep 2026</p>''',
'''<p><b>Verdict Raven:</b> Ini pilihan dasar, bukan fakta. Soalan utama ialah jurang bukti atau kuasa apa yang benar-benar memerlukan RCI baharu berbanding mekanisme sedia ada.</p>''':
'''<p><b>Verdict Raven:</b> Ini pilihan dasar, bukan fakta. Soalan utama ialah jurang bukti atau kuasa apa yang benar-benar memerlukan RCI baharu berbanding mekanisme sedia ada.</p><p><b>Apa yang boleh mengubah verdict?</b> Perbandingan rasmi mandat RCI, PAC, SPRM, PDRM dan audit forensik — termasuk apa yang masing-masing boleh subpoena, akses atau dedahkan — boleh menunjukkan sama ada RCI kedua menutup jurang sebenar atau hanya menggandakan proses.</p><p><b>Confidence:</b> Tinggi bahawa ia ialah policy position, bukan finding undang-undang. · <b>Last verified:</b> 11 Sep 2026</p>''',
'''<p><b>Verdict Raven:</b> Lebih tepat menyebut terdapat beberapa pendekatan dalam UMNO, bukan satu posisi tunggal yang seragam.</p>''':
'''<p><b>Verdict Raven:</b> Lebih tepat menyebut terdapat beberapa pendekatan dalam UMNO, bukan satu posisi tunggal yang seragam.</p><p><b>Apa yang boleh mengubah verdict?</b> Resolusi rasmi parti, kenyataan Majlis Kerja Tertinggi atau arahan rasmi yang menetapkan satu mekanisme dan satu skop akan menyokong dakwaan bahawa UMNO mempunyai posisi tunggal.</p><p><b>Confidence:</b> Tinggi berdasarkan variasi kenyataan awam yang telah direkodkan. · <b>Last verified:</b> 11 Sep 2026</p>'''
}
for old,new in repls.items():
    if old not in s:
        raise SystemExit(f'Missing target block: {old[:80]}')
    s = s.replace(old,new)

# Add two high-value narratives from the deep-research report before the grid closes.
marker = '''<article><h3>“UMNO satu suara tentang RCI kedua”</h3>'''
start = s.index(marker)
close = s.index('</article>', start) + len('</article>')
extra = '''\n<article><h3>“RM12 bilion hilang / disakau”</h3><p><span class="status claim">ANGKA POLITIK · PERLU REKONSILIASI</span></p><p><b>Siapa menggunakan naratif ini?</b> Angka RM12 bilion disebut dalam wacana politik untuk menerangkan skala masalah TH.</p><p><b>Apa rekod tunjuk?</b> Rekod awam menggunakan beberapa angka besar yang merujuk perkara berlainan — defisit aset-liabiliti, nilai pasaran aset, premium transaksi UJSB, kerugian atau rosot nilai dan jumlah pertimbangan penstrukturan.</p><p><b>Konteks yang sering tertinggal:</b> RM9.7 bilion, sekitar RM10 bilion, RM10.2 bilion, RM12 bilion dan RM19.9 bilion tidak boleh dicampur sebagai satu kategori kewangan.</p><p><b>Verdict Raven:</b> Jangan tulis “RCI membuktikan RM12 bilion dicuri” tanpa rekonsiliasi angka. Nilai itu perlu diaudit melalui Number Ledger berasingan.</p><p><b>Apa yang boleh mengubah verdict?</b> Dokumen RCI, penyata kewangan, valuation report dan forensic ledger yang memetakan tepat asal angka RM12 bilion serta kategorinya.</p><p><b>Confidence:</b> Tinggi bahawa angka itu digunakan; sederhana-rendah bahawa perkataan “hilang” menggambarkan satu kategori kewangan tunggal. · <b>Last verified:</b> 11 Sep 2026</p></article>\n<article><h3>“Tiada bukti kecurian, jadi tiada salah laku”</h3><p><span class="status context">FAKTA TERHAD · INFERENCE TERLALU LUAS</span></p><p><b>Siapa menggunakan naratif ini?</b> Kenyataan bekas Ketua Audit Negara Madinah Mohamad digunakan sebagai counter-narrative kepada dakwaan “sakau”.</p><p><b>Apa rekod tunjuk?</b> Madinah berkata audit semasa tempohnya tidak menemui bukti kecurian atau penyelewengan dan beliau akan melaporkan jika menemuinya.</p><p><b>Konteks yang sering tertinggal:</b> Audit kewangan, RCI, audit forensik dan siasatan jenayah mempunyai mandat dan threshold bukti yang berbeza. “Tidak menemui bukti” tidak sama dengan “bukti menunjukkan ia tidak berlaku”.</p><p><b>Verdict Raven:</b> Kenyataan Madinah sah sebagai rekod tentang apa yang pasukan auditnya temui dalam skop mereka. Ia tidak menutup kemungkinan isu tadbir urus, accounting treatment atau siasatan jenayah lain.</p><p><b>Apa yang boleh mengubah verdict?</b> Laporan audit penuh, working papers, scope notes dan comparison dengan bahan RCI/forensik boleh menunjukkan sama ada kedua-dua proses sebenarnya menilai perkara yang sama atau berlainan.</p><p><b>Confidence:</b> Tinggi bagi kenyataan Madinah; rendah bagi kesimpulan universal bahawa tiada salah laku. · <b>Last verified:</b> 11 Sep 2026</p></article>'''
s = s[:close] + extra + s[close:]

# Add V3 methodology box after the reading-method box.
needle = '''<div class="case-warning light"><strong>Kaedah baca</strong><span><b>FAKTA</b> = rekod menyokong. <b>DAKWAAN</b> = sesuatu pihak menyatakannya. <b>KESIMPULAN SEMENTARA</b> = tafsiran yang munasabah tetapi bukan bukti niat. <b>BELUM DIKETAHUI</b> = rekod belum cukup.</span></div>'''
replacement = needle + '''<div class="case-warning light"><strong>V3 · Verdict boleh berubah</strong><span>Setiap verdict ialah status bukti semasa, bukan cap kekal. Medan <b>Apa yang boleh mengubah verdict?</b> menerangkan bukti yang diperlukan untuk menguatkan, melemahkan atau membatalkan penilaian Raven.</span></div>'''
if needle not in s:
    raise SystemExit('Method box not found')
s = s.replace(needle, replacement, 1)

# Update OG description to reflect V3 audit.
s = s.replace(
    'Audit dakwaan dan naratif politik berdasarkan rekod yang boleh disemak.',
    'Audit naratif politik berdasarkan rekod, konteks yang tertinggal dan bukti yang boleh mengubah verdict.'
)

# QA gates.
checks = [
    'Apa yang boleh mengubah verdict?',
    'RM12 bilion hilang / disakau',
    'Tiada bukti kecurian, jadi tiada salah laku',
    '11 Sep 2026 · 01:15 MYT',
    'Lapan naratif utama',
    'Verdict boleh berubah',
]
for x in checks:
    assert x in s, x
assert s.count('Apa yang boleh mengubah verdict?</b>') >= 8
assert s.count('Last verified:</b> 11 Sep 2026') >= 8

PAGE.write_text(s, encoding='utf-8')
print('RCI Narrative Audit V3 QA PASS')
