#!/usr/bin/env python3
"""RAVEN Public Language V2.

Purpose:
- simplify public-facing language without changing factual findings;
- keep legal/evidence boundaries intact;
- move analyst jargon behind the public layer;
- repair known narrative content hierarchy defects.

This script intentionally does NOT alter source URLs, dates, amounts, names,
case status, evidence grades, narrative IDs or canonical URLs.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def apply_replacements(path: Path, replacements: list[tuple[str, str]]) -> None:
    text = path.read_text(encoding='utf-8')
    original = text
    for old, new in replacements:
        if old in text:
            text = text.replace(old, new)
    if text != original:
        path.write_text(text, encoding='utf-8')
        print('updated', path.relative_to(ROOT))


# ---------------------------------------------------------------------------
# Narrative hub — preserve findings, simplify the public layer.
# ---------------------------------------------------------------------------
NARR = ROOT / 'investigations/rci-tabung-haji/narratives/index.html'
apply_replacements(NARR, [
    ('<meta name="description" content="Forensik naratif RCI Tabung Haji: pecahkan bahasa, emosi, konteks dan dakwaan supaya pembaca dapat membezakan cerita politik daripada bukti yang boleh diaudit.">',
     '<meta name="description" content="Audit naratif RCI Tabung Haji: apa orang kata, apa rekod tunjuk, apa yang tak disebut dan apa yang masih belum terbukti.">'),
    ('<meta property="og:description" content="Raven pecahkan naratif kepada dakwaan, bukti, konteks yang hilang dan teknik bahasa — supaya pembaca boleh menilai tanpa dipaksa menerima framing mana-mana pihak.">',
     '<meta property="og:description" content="Raven asingkan cerita daripada rekod supaya pembaca boleh nampak apa yang disahkan, apa yang masih dakwaan dan apa yang belum cukup bukti.">'),
    ('<p class="section-kicker">RCI TABUNG HAJI · FORENSIK NARATIF</p><h1>Apa yang cerita cuba buat kita percaya — dan apa yang bukti benar-benar tunjuk?</h1>',
     '<p class="section-kicker">RCI TABUNG HAJI · AUDIT NARATIF</p><h1>Orang tengah cakap macam-macam. Yang mana cerita, yang mana bukti?</h1>'),
    ('<p>Naratif tidak semestinya palsu. Selalunya ia memilih fakta tertentu, membuang konteks tertentu, atau menggunakan bahasa yang menolak pembaca ke arah satu kesimpulan. Raven tidak menggantikan satu propaganda dengan propaganda lain. Kami pecahkan cerita itu, asingkan fakta daripada dakwaan, kenal pasti pencetus emosi dan kategori yang dicampur, kemudian bina semula penerangan yang bukti boleh tanggung.</p>',
     '<p><strong>Cerita yang mengelirukan tak semestinya penuh dengan benda palsu.</strong> Kadang-kadang fakta memang betul — cuma sebahagian cerita ditinggalkan, dua benda berbeza dicampur, atau ayat emosi digunakan sampai kita cepat buat kesimpulan. Raven buat satu benda: <strong>asingkan cerita daripada rekod.</strong></p>'),
    ('<div class="section-marker"><span>01</span><p>Bagaimana Raven membaca naratif</p></div><h2>Jangan mula dengan siapa yang bercakap. Mula dengan apa yang boleh dibuktikan.</h2>',
     '<div class="section-marker"><span>01</span><p>Macam mana Raven check cerita?</p></div><h2>Jangan mula dengan siapa yang cakap. Mula dengan apa yang boleh dibuktikan.</h2>'),
    ('<p class="section-lead">RCI merekodkan isu serius dalam tadbir urus, pelaburan dan pelaporan. Politik kemudian membina cerita di atas rekod itu. Raven mulakan dengan fakta yang boleh disahkan, baru menilai bahasa, pilihan fakta, perkara yang disenyapkan dan kesimpulan yang cuba dibentuk.</p>',
     '<p class="section-lead">RCI memang merekodkan masalah serius dalam tadbir urus, pelaburan dan pelaporan. Lepas itu datang pula pelbagai cerita politik. Raven mula dengan rekod dulu: apa yang sah, apa yang cuma dakwaan, apa yang tak disebut dan apa kesimpulan paling selamat.</p>'),
    ('<div class="case-warning light"><strong>Urutan Raven</strong><span><b>1 · FAKTA ASAS</b> — apa yang rekod benar-benar kata. <b>2 · DAKWAAN</b> — apa yang seseorang mahu kita percaya. <b>3 · TEKNIK NARATIF</b> — bahasa emosi, nombor tanpa kategori, pilihan fakta, identiti atau andaian motif. <b>4 · KONTEKS HILANG</b> — apa yang perlu diketahui sebelum membuat kesimpulan. <b>5 · REKONSTRUKSI</b> — penerangan paling tepat yang bukti semasa boleh tanggung.</span></div>',
     '<div class="case-warning light"><strong>Cara Raven check</strong><span><b>1 · APA KITA TAHU?</b> — apa yang rekod betul-betul kata. <b>2 · APA ORANG KATA?</b> — dakwaan atau cerita yang sedang dibawa. <b>3 · APA TRICK CERITA NI?</b> — emosi, nombor, pilihan fakta atau andaian yang boleh mengubah persepsi. <b>4 · APA YANG TAK DISEBUT?</b> — konteks penting sebelum kita buat kesimpulan. <b>5 · JADI, APA YANG SELAMAT UNTUK DISIMPULKAN?</b> — penerangan paling tepat yang bukti semasa boleh sokong.</span></div>'),
    ('<div class="case-warning light"><strong>Kaedah baca</strong><span><b>FAKTA</b> = rekod menyokong. <b>DAKWAAN</b> = sesuatu pihak menyatakannya. <b>KESIMPULAN SEMENTARA</b> = tafsiran munasabah tetapi belum terbukti. <b>BELUM DIKETAHUI</b> = rekod belum cukup. <b>AMARAN NARATIF</b> = bahasa atau struktur cerita yang boleh mengubah persepsi tanpa menambah bukti.</span></div>',
     '<div class="case-warning light"><strong>Label yang Raven guna</strong><span><b>DISAHKAN</b> = rekod menyokong. <b>DAKWAAN</b> = seseorang memang berkata begitu, tetapi isi dakwaan belum semestinya benar. <b>ANALISIS</b> = masuk akal, tapi belum terbukti. <b>BELUM TAHU</b> = rekod belum cukup. <b>AMARAN NARATIF</b> = cara cerita disusun boleh mengubah persepsi tanpa menambah bukti.</span></div>'),
    ('<div class="case-warning light"><strong>V3 · Verdict boleh berubah</strong><span>Setiap verdict ialah status bukti semasa, bukan cap kekal. Medan <b>Bukti apa boleh mengubah penilaian?</b> menerangkan bukti yang diperlukan untuk menguatkan, melemahkan atau membatalkan penilaian Raven.</span></div>',
     '<div class="case-warning light"><strong>Keputusan Raven boleh berubah</strong><span>Kalau bukti baru yang lebih kuat muncul, penilaian ini pun berubah. Bahagian <b>Apa bukti yang boleh ubah keputusan Raven?</b> tunjuk apa yang perlu muncul untuk menguatkan, melemahkan atau membatalkan penilaian semasa.</span></div>'),
    ('Peta baharu: lima blok politik, enam signal sosial — dan had bukti yang perlu dijaga.',
     'Peta baharu: lima blok politik, enam petunjuk sosial — dan had bukti yang perlu dijaga.'),
    ('Sebuah laporan deep-research baharu yang menggabungkan kenyataan parti dan contoh kandungan Facebook, Reels dan Threads telah diaudit oleh RAVEN-Trace. Ia berguna sebagai peta naratif, tetapi bukan ukuran sentimen awam dan bukan evidence pack undang-undang.',
     'Satu laporan penyelidikan yang menggabungkan kenyataan parti dan contoh kandungan Facebook, Reels dan Threads telah Raven semak. Ia berguna untuk mencari naratif yang perlu diperiksa — tetapi ia bukan ukuran sentimen seluruh rakyat dan bukan set bukti undang-undang.'),
    ('Kami mengekalkan signal yang boleh dijejak —', 'Kami mengekalkan petunjuk yang boleh dijejak —'),
    ('frame “jenama Islam disasar”', 'naratif “jenama Islam disasar”'),
    ('inferens motif atau “sentimen platform” sebagai fakta tanpa sampling dan bukti tambahan.',
     'andaian tentang motif atau “sentimen platform” sebagai fakta tanpa sampel yang jelas dan bukti tambahan.'),
    ('<p><b>Signal utama:</b>', '<p><b>Petunjuk utama:</b>'),
    ('<strong>Gred C / research lead</strong>', '<strong>Gred C / petunjuk penyelidikan</strong>'),
    ('posting sosial tanpa konteks penuh', 'hantaran sosial tanpa konteks penuh'),
    ('<b>Last verified:</b>', '<b>Disemak terakhir:</b>'),
    ('Naratif utama — buang framing dahulu, kemudian lihat apa yang tinggal.',
     'Naratif utama — ketepikan cara cerita dibingkaikan, tengok apa yang tinggal.'),

    # Azeez / RM193.5m
    ('TIDAK DISOKONG STRUKTUR PERTUDUHAN', 'REKOD PERTUDUHAN TAK SOKONG DAKWAAN INI'),
    ('<p><b>Teknik naratif</b> <strong>Category collapse + number laundering.</strong> Nilai transaksi/pelaburan ditukar dalam persepsi awam menjadi jumlah wang yang kononnya diambil individu.</p>',
     '<p><b>Teknik naratif</b> <strong>Nombor dan kategori dicampur.</strong> Nilai pelaburan dibuat seolah-olah sama dengan jumlah wang yang kononnya diambil oleh individu.</p>'),
    ('Charge sheet atau rekod mahkamah yang menunjukkan pertuduhan berasingan mengenai pemindahan RM193.5 juta kepada beliau/keluarga akan mengubah assessment ini.',
     'Kertas pertuduhan atau rekod mahkamah yang menunjukkan pertuduhan berasingan mengenai pemindahan RM193.5 juta kepada beliau atau keluarganya akan mengubah penilaian ini.'),

    # “Sakau”
    ('Sabitan mahkamah, asset-tracing atau forensic accounting yang menghubungkan jumlah tertentu kepada appropriation jenayah akan menguatkan dakwaan bagi transaksi atau individu yang terbukti — bukan secara automatik untuk seluruh kerugian TH.',
     'Keputusan mahkamah atau bukti jejak wang yang menghubungkan jumlah tertentu kepada perbuatan jenayah akan menguatkan dakwaan itu — untuk transaksi atau individu yang terbukti. Bukan secara automatik untuk semua kerugian TH.'),

    # UJSB / China
    ('SPA, shareholder register, beneficial-ownership record, sukuk terms dan transaction trail primer yang menunjukkan pemilikan atau pelupusan sebenar kepada pihak yang didakwa.',
     'Dokumen jual beli, rekod pemegang saham, rekod siapa sebenarnya memiliki aset dan jejak transaksi yang menunjukkan aset itu benar-benar pergi kepada pihak yang didakwa.'),

    # Policy / motive cards
    ('ANALISIS / INFERENCE · MOTIF TIDAK DIBUKTIKAN', 'FOKUS MEMANG BERUBAH · MOTIF BELUM TERBUKTI'),
    ('Minit dalaman, komunikasi strategi, arahan parti atau kenyataan langsung yang menunjukkan tujuan sebenar boleh menaikkan status daripada inference kepada dakwaan motif yang disokong bukti.',
     'Minit dalaman, komunikasi strategi, arahan parti atau kenyataan langsung tentang tujuan sebenar boleh menguatkan dakwaan mengenai motif.'),
    ('Tinggi bahawa ia ialah policy position, bukan finding undang-undang.',
     'Tinggi bahawa ini ialah pilihan dasar — bukan keputusan mahkamah.'),
    ('Perbandingan rasmi mandat RCI, PAC, SPRM, PDRM dan audit forensik — termasuk apa yang masing-masing boleh subpoena, akses atau dedahkan — boleh menunjukkan sama ada RCI kedua menutup jurang sebenar atau hanya menggandakan proses.',
     'Perbandingan rasmi kuasa RCI, PAC, SPRM, PDRM dan audit forensik — termasuk siapa boleh memanggil saksi, mendapatkan dokumen dan mendedahkan dapatan — boleh menunjukkan sama ada RCI kedua benar-benar menutup jurang atau sekadar mengulang proses.'),

    # RM12b
    ('ANGKA POLITIK · PERLU REKONSILIASI', 'ANGKA DISEBUT · TAPI BENDA YANG DIKIRA BELUM SAMA'),
    ('Jangan tulis “RCI membuktikan RM12 bilion dicuri” tanpa rekonsiliasi angka. Nilai itu perlu diaudit melalui Number Ledger berasingan.',
     'Jangan terus tulis “RCI membuktikan RM12 bilion dicuri” sebelum angka-angka itu dipadankan. Nilai tersebut perlu diperiksa satu per satu dalam jadual semakan angka.'),
    ('Dokumen RCI, penyata kewangan, valuation report dan forensic ledger yang memetakan tepat asal angka RM12 bilion serta kategorinya.',
     'Dokumen RCI, penyata kewangan, laporan penilaian dan rekod angka yang menunjukkan tepat dari mana angka RM12 bilion datang dan apa yang sebenarnya dikira.'),

    # Madinah / audit
    ('FAKTA TERHAD · INFERENCE TERLALU LUAS', 'KENYATAAN ITU SAH · KESIMPULAN BESARNYA BELUM TENTU'),
    ('Audit kewangan, RCI, audit forensik dan siasatan jenayah mempunyai mandat dan threshold bukti yang berbeza. “Tidak menemui bukti” tidak sama dengan “bukti menunjukkan ia tidak berlaku”.',
     'Audit kewangan, RCI, audit forensik dan siasatan jenayah tak semestinya mencari benda yang sama atau menggunakan proses yang sama. <strong>“Tak jumpa bukti” tidak sama dengan “bukti menunjukkan ia tak pernah berlaku”.</strong>'),
    ('Laporan audit penuh, working papers, scope notes dan comparison dengan bahan RCI/forensik boleh menunjukkan sama ada kedua-dua proses sebenarnya menilai perkara yang sama atau berlainan.',
     'Laporan audit penuh, kertas kerja audit, catatan skop dan perbandingan dengan bahan RCI atau audit forensik boleh menunjukkan sama ada proses-proses itu sebenarnya menilai perkara yang sama atau berlainan.'),

    # Section-level public language
    ('<div class="section-marker"><span>03</span><p>Peta posisi</p></div><h2>Apa yang setiap blok lebih banyak tekankan?</h2>',
     '<div class="section-marker"><span>03</span><p>Parti fokus benda berbeza</p></div><h2>Siapa lebih banyak tekankan apa?</h2>'),
    ('<p><b>Yang perlu diaudit:</b>', '<p><b>Yang Raven check:</b>'),
    ('<div class="section-marker"><span>04</span><p>Perkara yang belum boleh disimpulkan</p></div><h2>Empat garis merah.</h2>',
     '<div class="section-marker"><span>04</span><p>Apa yang masih belum tahu</p></div><h2>Empat benda yang kita belum boleh simpulkan.</h2>'),
    ('Setakat chronology mahkamah yang disemak,', 'Setakat kronologi mahkamah yang disemak,'),
    ('Gred menilai kegunaan sumber untuk dakwaan tertentu. Kenyataan tokoh membuktikan bahawa kenyataan itu dibuat; ia tidak semestinya membuktikan isi kenyataan tersebut benar.',
     'Gred menunjukkan sejauh mana satu sumber membantu kita semak dakwaan tertentu. Kalau seorang tokoh berkata sesuatu, itu membuktikan <strong>kenyataan itu memang dibuat</strong> — bukan automatik membuktikan isi kenyataan itu benar.'),
])


# ---------------------------------------------------------------------------
# Political/social narrative subpage — public language, same evidence state.
# ---------------------------------------------------------------------------
SOCIAL = ROOT / 'investigations/rci-tabung-haji/narratives/political-social-media/index.html'
apply_replacements(SOCIAL, [
    ('Halaman ini menggunakan laporan deep-research sebagai peta awal untuk mencari naratif, kemudian mengujinya terhadap sumber awam. Tujuannya bukan memilih kem politik yang “betul”. Tujuannya ialah mengurangkan kuasa framing: asingkan apa yang berlaku daripada apa yang pembaca disuruh rasa atau simpulkan.',
     'Halaman ini guna laporan penyelidikan sebagai peta awal untuk mencari cerita yang perlu diperiksa, kemudian Raven semak semula terhadap sumber awam. Tujuannya bukan pilih kem politik yang “betul”. Tujuannya lebih mudah: <strong>asingkan apa yang berlaku daripada apa yang kita disuruh rasa atau simpulkan.</strong>'),
    ('Laporan ini ialah peta untuk mencari cerita — bukan lesen untuk mempercayainya.',
     'Laporan ini bantu kita cari cerita yang perlu diperiksa — bukan alasan untuk terus percaya.'),
    ('RAVEN menilai laporan ini sebagai <strong>Gred C · bahan penyelidikan / sintesis</strong>. Ia berguna untuk mengenal pasti aktor, slogan, pertikaian dan contoh kandungan sosial. Tetapi sebahagian kesimpulan politiknya ialah tafsiran, manakala beberapa butiran undang-undang telah berubah selepas laporan disediakan.',
     'Raven letakkan laporan ini pada <strong>Gred C · bahan penyelidikan</strong>. Ia berguna untuk mengenal pasti siapa yang bercakap, slogan apa yang muncul, apa yang dipertikaikan dan contoh kandungan sosial. Tetapi sebahagian kesimpulan politiknya masih tafsiran, dan beberapa butiran undang-undang sudah berubah selepas laporan itu disediakan.'),
    ('Ayat yang menyimpulkan motif seperti “mengalih fokus”, “defensif” atau “perpecahan” tidak dibawa sebagai fakta tanpa bukti tambahan.',
     'Ayat yang meneka niat seperti “mengalih fokus”, “defensif” atau “perpecahan” tidak Raven bawa sebagai fakta tanpa bukti tambahan.'),
    ('Guna rekod primer atau laporan yang boleh disemak untuk menentukan fakta.',
     'Untuk tentukan fakta, kembali kepada rekod asal atau laporan yang boleh disemak.'),

    ('FAKTA · POSISI POLITIK', 'POSISI INI MEMANG DIREKODKAN'),
    ('DUA NARATIF SERENTAK', 'DUA PERKARA BOLEH WUJUD SERENTAK'),
    ('FAKTA · TINDAKAN PARLIMEN', 'TINDAKAN INI MEMANG BERLAKU'),

    ('Timing, pakaian lokap atau kesan politik tidak dengan sendiri membuktikan bahawa SPRM/PDRM menerima arahan politik. Untuk menaikkan dakwaan ini menjadi fakta, perlu ada bukti seperti arahan, communication trail, decision record atau comparative selective-enforcement analysis.',
     'Masa penahanan, pakaian lokap atau kesan politik tak cukup untuk membuktikan SPRM atau PDRM menerima arahan politik. Untuk buktikan dakwaan itu, kita perlukan sesuatu yang lebih keras: contohnya arahan, jejak komunikasi, rekod keputusan atau perbandingan kes yang menunjukkan penguatkuasaan pilih kasih.'),
    ('<strong>CLAIM · POSISI POLITIK.</strong> Wujud bukti bahawa dakwaan political intimidation dibuat; belum ada bukti awam yang kami semak yang membuktikan enforcement dalam kes RCI TH dikawal secara politik.',
     '<strong>DAKWAAN · POSISI POLITIK.</strong> Kita boleh sahkan dakwaan “political intimidation” itu memang dibuat. Setakat bukti awam yang Raven semak, belum ada bukti yang menunjukkan penguatkuasaan dalam kes RCI TH dikawal secara politik.'),
    ('Tinggi bahawa dakwaan dibuat · rendah untuk kebenaran sebab-musabab yang didakwa.',
     'Tinggi bahawa dakwaan itu memang dibuat · rendah bahawa sebab yang didakwa sudah terbukti.'),

    ('Bagaimana naratif mengubah persepsi tanpa perlu mencipta fakta palsu.',
     'Macam mana cerita boleh mengubah persepsi walaupun tak semestinya guna fakta palsu.'),
    ('Manipulasi tidak semestinya datang sebagai pembohongan terus. Cerita yang memilih fakta tertentu, menukar kategori, mengulang label emosi atau meneka motif boleh mengubah cara orang memahami peristiwa walaupun sebahagian ayatnya benar.',
     'Cerita yang mengelirukan tak semestinya menipu secara terus. Kadang-kadang fakta dipilih sebelah sahaja, dua kategori dicampur, perkataan emosi diulang atau niat orang diteka. Ayatnya mungkin ada bahagian yang benar — tetapi gambaran akhirnya boleh lari.'),
    ('SELECTION EFFECT', 'DIA TUNJUK YANG INI JE'),
    ('CATEGORY COLLAPSE', 'EH, BENDA NI TAK SAMA'),
    ('EMOTIONAL PRIMING', 'DIA BAGI KITA RASA DULU'),
    ('MOTIVE INFLATION', 'KITA NAMPAK TINDAKAN. NIAT? BELUM TENTU'),
    ('REPETITION RISK', 'ULANG BANYAK KALI TAK JADIKAN IA BETUL'),
    ('REPRESENTATIVENESS ERROR', 'VIRAL TAK BERMAKSUD SUARA SEMUA ORANG'),
    ('walkout', 'tindakan keluar Dewan'),
    ('timing kenyataan', 'masa kenyataan'),
    ('ialah signal;', 'ialah petunjuk;'),

    ('Empat lompatan bahasa yang boleh mengubah persepsi tanpa menambah bukti.',
     'Empat shortcut bahasa yang boleh buat kita cepat salah faham.'),
    ('Daripada “beberapa posting” kepada “rakyat berpendapat”', 'Daripada “beberapa hantaran” kepada “rakyat berpendapat”'),
    ('ini lompatan daripada sampel tidak diketahui kepada populasi.', 'beberapa hantaran tak boleh terus dianggap suara seluruh rakyat.'),
    ('Jika mahu ukur sentimen', 'Kalau nak kata “ramai orang fikir macam ni”'),
    ('Kita perlukan tempoh pemerhatian, platform, kata kunci, jumlah posting/akaun, kaedah pemilihan, engagement, deduplikasi dan batas demografi.',
     'Kita perlukan sampel yang jelas: tempoh masa, platform, kata kunci, jumlah hantaran dan akaun, cara sampel dipilih, akaun berulang dan siapa sebenarnya yang diwakili. <strong>Viral? Ya. Wakil seluruh Malaysia? Belum tentu.</strong>'),
    ('Jika mahu dakwa pengalihan fokus', 'Kalau nak kata “mereka sengaja alih fokus”'),
    ('Kita perlukan bukti keputusan, komunikasi, timing atau pola tindakan yang menunjukkan strategi itu — bukan hanya kerana topik baharu muncul selepas topik lama.',
     'Kita perlukan bukti keputusan, komunikasi, masa atau pola tindakan yang menunjukkan strategi itu — bukan sekadar kerana topik baharu muncul selepas topik lama.'),
    ('Jika mahu dakwa bias terhadap institusi Islam', 'Kalau nak kata institusi Islam memang disasar'),
    ('Jika mahu dakwa PN retak', 'Kalau nak kata PN memang retak'),

    ('<div class="section-marker"><span>05</span><p>Apa yang perlu dibuktikan seterusnya</p></div>',
     '<div class="section-marker"><span>06</span><p>Apa yang perlu dibuktikan seterusnya</p></div>'),
    ('<div class="section-marker"><span>06</span><p>Sumber silang</p></div>',
     '<div class="section-marker"><span>07</span><p>Sumber silang</p></div>'),
])

# Remove the legacy “Prinsip komunikasi” section that was accidentally rendered
# after </footer>. It is moved into Methodology below.
social_text = SOCIAL.read_text(encoding='utf-8')
legacy_pattern = re.compile(
    r'<section class="case-section"><div class="section-marker"><span>07</span><p>Prinsip komunikasi</p></div>.*?</section>\s*',
    re.S,
)
social_text, removed = legacy_pattern.subn('', social_text, count=1)
if removed:
    SOCIAL.write_text(social_text, encoding='utf-8')
    print('moved legacy communication principle out of', SOCIAL.relative_to(ROOT))


# ---------------------------------------------------------------------------
# Homepage — remove analyst/internal leakage while preserving case facts.
# ---------------------------------------------------------------------------
HOME = ROOT / 'index.html'
apply_replacements(HOME, [
    ('SIASATAN UTAMA · CASEFILE RCI-TH-2026 · v20', 'SIASATAN UTAMA · RCI TABUNG HAJI'),
    ('Freshness sweep · 12 September · 20:44 MYT · status undang-undang tidak berubah',
     'Semakan terbaru · 12 September · 20:44 MYT · status undang-undang tidak berubah'),
    ('Baca freshness sweep →', 'Baca semakan terbaru →'),
    ('Raven tidak menaikkan kiraan kepada lima tanpa rekonsiliasi rekod.',
     'Jadi Raven kekalkan angka empat buat masa ini. Dua rekod itu belum sepadan.'),
])


# ---------------------------------------------------------------------------
# About — human frontstage, same disclosure and independence boundary.
# ---------------------------------------------------------------------------
ABOUT = ROOT / 'about/index.html'
apply_replacements(ABOUT, [
    ('<h1>Cari kebenaran.<br>Asingkan daripada kabus.</h1>', '<h1>Cari yang benar.<br>Pecahkan cerita.</h1>'),
    ('RAVEN-Trace Malaysia ialah penerbitan penyiasatan yang menyemak dakwaan awam terhadap rekod yang boleh diperiksa. Kami asingkan fakta, dakwaan, cara sesuatu cerita dibingkaikan dan perkara yang belum diketahui — kemudian terangkan semuanya dalam bahasa yang mudah diikuti.',
     'RAVEN-Trace semak dakwaan awam terhadap rekod yang orang ramai boleh periksa. Raven asingkan apa yang memang disahkan, apa yang masih dakwaan, bagaimana sesuatu cerita dibingkaikan dan apa yang kita masih belum tahu — kemudian terangkan semuanya dengan bahasa manusia.'),
    ('Kerja siasatan di belakang tabir boleh teknikal. Hasil berita di depan orang ramai mesti jelas:',
     'Kerja di belakang tabir boleh teknikal. Tapi bila sampai kepada pembaca, ia mesti jelas:'),
    ('<p class="eyebrow">Identiti editorial + kaedah</p><h2>Raven ialah identiti penyiasatan. RAVEN-Trace ialah kaedahnya.</h2>',
     '<p class="eyebrow">Siapa Raven sebenarnya?</p><h2>Raven ialah penyiasatnya. RAVEN-Trace ialah cara kerja.</h2>'),
    ('<strong>Raven</strong> ialah identiti editorial penyiasatan RAVEN-Trace: penyiasat naratif berasaskan bukti dan wartawan penerang yang menjejak sumber, menguji percanggahan dan menjaga batas bukti. <strong>RAVEN-Trace Protocol</strong> ialah kaedah boleh diulang untuk membina timeline, menilai kekuatan bukti, membezakan fakta daripada dakwaan dan menunjukkan perkara yang masih belum diketahui.',
     '<strong>Raven</strong> ialah suara penyiasatan RAVEN-Trace: cari sumber, check percanggahan dan jangan melangkaui apa yang bukti boleh sokong. <strong>RAVEN-Trace Protocol</strong> pula ialah cara kerja di belakang tabir untuk menyusun kronologi, menilai kekuatan bukti, membezakan fakta daripada dakwaan dan menandakan apa yang masih belum diketahui.'),
])


# ---------------------------------------------------------------------------
# Methodology — receive the communication principle in the correct place.
# ---------------------------------------------------------------------------
METHOD = ROOT / 'methodology/index.html'
method = METHOD.read_text(encoding='utf-8')
if 'Kenapa Raven mula dengan fakta, bukan dengan mengulang mitos?' not in method:
    block = '''\n    <section class="section paper rule-top" id="communication-principle"><div class="measure"><p class="eyebrow">Cara Raven bercakap</p><h2>Kenapa Raven mula dengan fakta, bukan dengan mengulang mitos?</h2><p>Raven cuba beri model yang betul dahulu. Dakwaan mengelirukan disebut bila perlu, tetapi tujuan utamanya bukan mengulang slogan itu berkali-kali. Kami terangkan apa yang rekod tunjuk, apa trick cerita yang digunakan, kemudian kembali kepada fakta yang boleh diuji.</p><p class="muted">Prinsip ini disokong oleh penyelidikan tentang prebunking, pembetulan fakta dan selective presentation.</p><ul><li><a href="https://www.nature.com/articles/s41598-024-71599-6" rel="noopener noreferrer">Scientific Reports · prebunking vs debunking</a></li><li><a href="https://www.nature.com/articles/s41598-024-53337-0" rel="noopener noreferrer">Scientific Reports · confirmation framing in fact-checks</a></li><li><a href="https://www.nature.com/articles/s41598-025-29519-9" rel="noopener noreferrer">Scientific Reports · selective presentation and news framing</a></li><li><a href="https://www.nature.com/articles/s41562-024-02023-2" rel="noopener noreferrer">Nature Human Behaviour · inoculation + accuracy prompting</a></li></ul></div></section>\n'''
    method = method.replace('  </main>', block + '  </main>', 1)
    METHOD.write_text(method, encoding='utf-8')
    print('added communication principle to', METHOD.relative_to(ROOT))


# ---------------------------------------------------------------------------
# Guardrails — factual and routing invariants.
# ---------------------------------------------------------------------------
main = NARR.read_text(encoding='utf-8')
social = SOCIAL.read_text(encoding='utf-8')
home = HOME.read_text(encoding='utf-8')
method = METHOD.read_text(encoding='utf-8')

assert 'RM193.5 juta' in main
assert '14 kertas siasatan' in main
assert 'empat individu telah berdepan pertuduhan' in main
assert 'Pertuduhan bukan sabitan' in main
assert 'naratif-azeez-ambil-rm193-5-juta' in main
assert 'naratif-sakau-duit-umat-islam' in main
assert 'Orang tengah cakap macam-macam. Yang mana cerita, yang mana bukti?' in main
assert 'Cara Raven check' in main
assert 'Raven kata macam mana?' not in main  # rendered by JS; canonical finding text remains source-first
assert 'DIA TUNJUK YANG INI JE' in social
assert 'EH, BENDA NI TAK SAMA' in social
assert 'DIA BAGI KITA RASA DULU' in social
assert 'VIRAL TAK BERMAKSUD SUARA SEMUA ORANG' in social
assert social.count('<span>05</span>') == 1
assert '<span>06</span><p>Apa yang perlu dibuktikan seterusnya' in social
assert '<span>07</span><p>Sumber silang' in social
assert 'Prinsip komunikasi' not in social
assert 'Kenapa Raven mula dengan fakta, bukan dengan mengulang mitos?' in method
assert 'https://raven-trace.github.io/raventrace-my/' in home
assert 'rcitabunghaji' not in home

print('RAVEN PUBLIC LANGUAGE V2: PASS')
