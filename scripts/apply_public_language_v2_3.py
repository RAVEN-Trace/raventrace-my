#!/usr/bin/env python3
"""RAVEN Public Language V2.3 — final public-voice micro-clean.

Only presentation language changes. Factual findings, legal states, names, dates,
amounts, source links, evidence grades, IDs and public routes remain untouched.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def swap(rel: str, replacements: list[tuple[str, str]]) -> None:
    path = ROOT / rel
    text = path.read_text(encoding='utf-8')
    before = text
    for old, new in replacements:
        text = text.replace(old, new)
    if text != before:
        path.write_text(text, encoding='utf-8')
        print('updated', rel)


# Narrative hub — keep the evidence model; remove remaining analyst voice.
swap('investigations/rci-tabung-haji/narratives/index.html', [
    ('Naratif utama — ketepikan cara cerita dibingkaikan, tengok apa yang tinggal.',
     'Naratif utama — ketepikan cara cerita dibawa. Tengok apa yang tinggal.'),
    ('Status ini tidak dinaikkan kepada “palsu mutlak” tanpa audit dokumen primer penuh.',
     'Raven belum panggil dakwaan ini “palsu mutlak” selagi dokumen asal belum disemak sepenuhnya.'),
    ('Tinggi bahawa tuntutan ini wujud sebagai posisi dasar.',
     'Tinggi bahawa tuntutan ini memang wujud sebagai pendirian dasar.'),
    ('Munasabah sebagai analisis terhadap kesan naratif, tetapi tidak boleh dipersembahkan sebagai fakta tentang niat UMNO, PAS atau mana-mana individu.',
     'Masuk akal sebagai analisis tentang kesan cerita itu, tetapi ia belum membuktikan niat UMNO, PAS atau mana-mana individu.'),
    ('Kami tidak memilih frame yang paling sedap didengar. Kami asingkan <b>apa yang didakwa</b>, <b>apa yang direkodkan</b>, <b>apa yang belum dibuktikan</b> dan <b>apa yang masih memerlukan dokumen primer</b>.',
     'Kami tidak memilih cerita yang paling sedap didengar. Kami asingkan <b>apa yang didakwa</b>, <b>apa yang direkodkan</b>, <b>apa yang belum dibuktikan</b> dan <b>apa yang masih memerlukan dokumen asal</b>.'),
    ('Kita tidak mempunyai metodologi sampel yang cukup untuk mendakwa keseluruhan X, Facebook, TikTok, Instagram atau Threads dikuasai satu naratif tertentu.',
     'Kita belum ada sampel dan cara memilihnya yang cukup jelas untuk mendakwa keseluruhan X, Facebook, TikTok, Instagram atau Threads dikuasai satu naratif tertentu.'),
    ('Kompilasi penyelidikan yang kami semak menyebut lapan kertas siasatan dalam satu bahagian.',
     'Bahan penyelidikan yang kami semak menyebut lapan kertas siasatan dalam satu bahagian.'),
    ('Kompilasi penyelidikan bertarikh 9 September 2026 digunakan sebagai indeks awal untuk mengenal pasti naratif. Dakwaan sensitif kemudian disemak semula terhadap laporan rasmi atau pelaporan beratribusi. Generalisasi sentimen platform yang tidak mempunyai sampel dan metodologi tidak diterbitkan sebagai fakta.',
     'Bahan penyelidikan bertarikh 9 September 2026 digunakan sebagai senarai awal untuk mencari naratif yang perlu diperiksa. Dakwaan sensitif kemudian disemak semula terhadap laporan rasmi atau laporan media yang menyatakan sumbernya. Kesimpulan tentang sentimen seluruh platform tidak diterbitkan sebagai fakta tanpa sampel dan cara ukur yang jelas.'),
    ('RAVEN-Trace™ by SharulR X(ai) Projects. Evidence-bounded public explanation. Status boleh berubah apabila bukti lebih kuat muncul.',
     'RAVEN-Trace™ by SharulR X(ai) Projects. Penerangan awam yang terikat pada bukti. Status boleh berubah apabila bukti lebih kuat muncul.'),
])


# Political/social narrative — convert remaining research/consultant phrasing.
swap('investigations/rci-tabung-haji/narratives/political-social-media/index.html', [
    ('Corak yang kelihatan di media sosial pula tidak sama dengan sentimen seluruh rakyat tanpa sampel dan kaedah pengukuran yang boleh diaudit.',
     'Corak yang nampak di media sosial pula tidak sama dengan sentimen seluruh rakyat tanpa sampel dan cara ukur yang jelas.'),
    ('<div class="section-marker"><span>02</span><p>Peta aktor</p></div><h2>Lima kelompok politik membawa sudut yang berbeza.</h2>',
     '<div class="section-marker"><span>02</span><p>Siapa bawa cerita apa?</p></div><h2>Lima kumpulan politik, lima perkara yang lebih banyak mereka tekankan.</h2>'),
    ('rendah-sederhana bagi dakwaan sebab-musabab.',
     'rendah-sederhana bahawa sebab yang didakwa sudah terbukti.'),
    ('rendah-sederhana untuk implikasi terhadap gabungan.',
     'rendah-sederhana tentang apa maknanya kepada gabungan.'),
    ('tidak boleh digunakan untuk menetapkan motif agensi penguatkuasaan.',
     'tidak boleh digunakan untuk membuktikan niat agensi penguatkuasaan.'),
    ('Laporan ini kuat untuk mengesan naratif, sederhana sebagai sintesis politik, dan lemah jika digunakan untuk membuktikan motif atau mengukur sentimen seluruh masyarakat.',
     'Laporan ini kuat untuk mengesan naratif, sederhana sebagai ringkasan politik, dan lemah jika digunakan untuk membuktikan niat atau mengukur sentimen seluruh masyarakat.'),
    ('Kita perlukan kumpulan perbandingan: institusi lain, tahap salah laku yang setara, liputan, tindakan agensi dan tempoh masa yang sama.',
     'Kita perlukan institusi lain untuk dibandingkan: tahap salah laku yang setara, liputan, tindakan agensi dan tempoh masa yang sama.'),
    ('Jika sumber bercanggah, RAVEN mengekalkan pertikaian itu sehingga bukti yang lebih kuat tersedia.',
     'Jika sumber bercanggah, Raven tandakan ia sebagai bercanggah sehingga bukti yang lebih kuat muncul.'),
])


# About — public identity in ordinary language; retain disclosure substance.
swap('about/index.html', [
    ('bagaimana sesuatu cerita dibingkaikan', 'cara cerita itu disusun'),
    ('Bahasa, framing dan pengulangan boleh mempengaruhi persepsi.',
     'Bahasa, cara cerita disusun dan pengulangan boleh mempengaruhi persepsi.'),
    ('<strong>RAVEN-Trace Protocol</strong> pula ialah cara kerja di belakang tabir untuk menyusun kronologi, menilai kekuatan bukti, membezakan fakta daripada dakwaan dan menandakan apa yang masih belum diketahui.',
     '<strong>Cara kerja RAVEN-Trace</strong> pula digunakan di belakang tabir untuk menyusun kronologi, menilai kekuatan bukti, membezakan fakta daripada dakwaan dan menandakan apa yang masih belum diketahui.'),
    ('<div class="dossier-head">Independence &amp; AI-assisted disclosure</div>',
     '<div class="dossier-head">Kebebasan editorial + penggunaan AI</div>'),
    ('akauntabiliti editorial kekal di bawah Penerbit RAVEN-Trace / SharulR X(ai) Projects.',
     'tanggungjawab editorial kekal di bawah Penerbit RAVEN-Trace / SharulR X(ai) Projects.'),
])


# Methodology — this is allowed to be technical, but public terminology comes first.
swap('methodology/index.html', [
    ('<meta property="og:description" content="Bagaimana RAVEN-Trace membezakan fakta, dakwaan, inferens, andaian, perkara belum diketahui dan rekod dipertikaikan.">',
     '<meta property="og:description" content="Bagaimana RAVEN-Trace membezakan fakta, dakwaan, kesimpulan sementara, andaian, perkara belum diketahui dan rekod bercanggah.">'),
    ('<div class="utility-bar"><div class="utility-inner"><span>RAVEN-Trace Protocol</span>',
     '<div class="utility-bar"><div class="utility-inner"><span>Cara Raven bekerja</span>'),
    ('<strong>A · Bukti primer langsung</strong>', '<strong>A · Sumber asal / bukti langsung</strong>'),
    ('Dapatan utama, timeline, nama, status kes dan angka penting mesti boleh dijejak kepada Sumber & dokumen atau sumber terus.',
     'Dapatan utama, kronologi, nama, status kes dan angka penting mesti boleh dijejak kepada Sumber & dokumen atau sumber terus.'),
    ('Angka yang boleh mengubah pemahaman cerita mesti mempunyai sumber dan definisi metrik yang jelas.',
     'Angka yang boleh mengubah pemahaman cerita mesti mempunyai sumber dan penerangan jelas tentang apa sebenarnya angka itu mengukur.'),
    ('Simpan bahan asal, URL, metadata yang ada, tarikh akses dan asal-usul sumber sebelum bahan berubah.',
     'Simpan bahan asal, URL, maklumat fail (metadata) yang ada, tarikh akses dan asal-usul sumber sebelum bahan berubah.'),
    ('Cari sumber primer, pengesahan bebas, konteks penuh, percanggahan dan hak menjawab apabila perlu.',
     'Cari sumber asal, pengesahan bebas, konteks penuh, percanggahan dan hak menjawab apabila perlu.'),
    ('Raven cuba beri model yang betul dahulu.', 'Raven cuba beri fakta yang betul dahulu.'),
])


# Homepage — align status vocabulary and one remaining bureaucratic sentence.
swap('index.html', [
    ('<span class="status disputed">DIPERTIKAIKAN · REKOD</span>',
     '<span class="status disputed">REKOD TAK SEPADAN</span>'),
    ('Pelaksanaan penuh masih perlu dinilai pada tahap setiap syor, bukan hanya angka keseluruhan.',
     'Kita masih perlu tengok satu per satu sama ada setiap syor benar-benar dilaksanakan — bukan hanya angka keseluruhan.'),
])


# Updates — use the question a normal reader would ask.
swap('investigations/rci-tabung-haji/updates/index.html', [
    ('<dt>Apa perlu ditahan?</dt>', '<dt>Apa yang belum boleh disahkan?</dt>'),
])


# Invariants: content meaning and legal boundary must survive the tone pass.
main=(ROOT/'investigations/rci-tabung-haji/narratives/index.html').read_text(encoding='utf-8')
social=(ROOT/'investigations/rci-tabung-haji/narratives/political-social-media/index.html').read_text(encoding='utf-8')
about=(ROOT/'about/index.html').read_text(encoding='utf-8')
method=(ROOT/'methodology/index.html').read_text(encoding='utf-8')
home=(ROOT/'index.html').read_text(encoding='utf-8')
updates=(ROOT/'investigations/rci-tabung-haji/updates/index.html').read_text(encoding='utf-8')

for tok in ['RM193.5 juta','14 kertas siasatan','Pertuduhan bukan sabitan','naratif-azeez-ambil-rm193-5-juta','naratif-sakau-duit-umat-islam']:
    assert tok in main, tok
for tok in ['Naratif utama — ketepikan cara cerita dibawa. Tengok apa yang tinggal.','dokumen asal','sampel dan cara memilihnya yang cukup jelas','Penerangan awam yang terikat pada bukti']:
    assert tok in main, tok
for tok in ['Siapa bawa cerita apa?','sampel dan cara ukur yang jelas','sederhana sebagai ringkasan politik','Raven tandakan ia sebagai bercanggah']:
    assert tok in social, tok
assert 'Cara kerja RAVEN-Trace' in about
assert 'Kebebasan editorial + penggunaan AI' in about
assert 'Cara Raven bekerja' in method
assert 'A · Sumber asal / bukti langsung' in method
assert 'REKOD TAK SEPADAN' in home
assert 'Apa yang belum boleh disahkan?' in updates

stale=['dokumen primer penuh','frame yang paling sedap didengar','metodologi sampel','pelaporan beratribusi','Generalisasi sentimen platform','Peta aktor','sintesis politik','menetapkan motif agensi','RAVEN-Trace Protocol','Independence & AI-assisted disclosure','DIPERTIKAIKAN · REKOD','Apa perlu ditahan?']
for label,text in [('main',main),('social',social),('about',about),('method',method),('home',home),('updates',updates)]:
    for tok in stale:
        assert tok not in text, f'{label}: stale public phrase {tok}'

print('RAVEN PUBLIC LANGUAGE V2.3: PASS')
