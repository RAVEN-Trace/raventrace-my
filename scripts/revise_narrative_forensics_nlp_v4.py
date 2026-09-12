from pathlib import Path

ROOT = Path('.')
main = ROOT/'investigations/rci-tabung-haji/narratives/index.html'
social = ROOT/'investigations/rci-tabung-haji/narratives/political-social-media/index.html'


def replace_required(text, old, new, label):
    if old not in text:
        raise SystemExit(f'Missing expected token for {label}: {old[:100]}')
    return text.replace(old, new)

# --- Main narrative audit: shift from political mapping to narrative forensics ---
t = main.read_text(encoding='utf-8')
t = replace_required(t,
    '<title>RCI Tabung Haji — Siapa kata apa, dan apa rekod tunjuk? | RAVEN-Trace</title>',
    '<title>RCI Tabung Haji — Forensik Naratif: cerita vs bukti | RAVEN-Trace</title>', 'main title')
t = replace_required(t,
    '<meta name="description" content="Audit naratif politik RCI Tabung Haji: apa yang kerajaan, PH, UMNO dan PN/PAS katakan, apa yang disokong rekod, dan apa yang masih sekadar tafsiran.">',
    '<meta name="description" content="Forensik naratif RCI Tabung Haji: pecahkan bahasa, emosi, konteks dan dakwaan supaya pembaca dapat membezakan cerita politik daripada bukti yang boleh diaudit.">', 'main description')
t = replace_required(t,
    '<meta property="og:title" content="RCI Tabung Haji — Siapa kata apa, dan apa rekod tunjuk?">',
    '<meta property="og:title" content="RCI Tabung Haji — Forensik Naratif: cerita vs bukti">', 'main og title')
t = replace_required(t,
    '<meta property="og:description" content="Parti boleh memilih sudut cerita. RAVEN-Trace semak apa yang benar-benar disokong rekod — dan apa yang masih dakwaan atau tafsiran.">',
    '<meta property="og:description" content="Raven pecahkan naratif kepada dakwaan, bukti, konteks yang hilang dan teknik bahasa — supaya pembaca boleh menilai tanpa dipaksa menerima framing mana-mana pihak.">', 'main og description')
t = replace_required(t,
    '<p class="section-kicker">RCI TABUNG HAJI · AUDIT NARATIF</p><h1>Siapa kata apa — dan apa rekod tunjuk?</h1>\n<p>Parti politik boleh memilih sudut cerita yang berbeza. Halaman ini tidak menentukan siapa “menang” naratif. Ia menguji setiap frame melalui lima lapisan: siapa menggunakannya, apa rekod tunjuk, konteks yang sering tertinggal, verdict RAVEN-Trace, dan bukti apa yang boleh mengubah verdict itu.</p>',
    '<p class="section-kicker">RCI TABUNG HAJI · FORENSIK NARATIF</p><h1>Apa yang cerita cuba buat kita percaya — dan apa yang bukti benar-benar tunjuk?</h1>\n<p>Naratif tidak semestinya palsu. Selalunya ia memilih fakta tertentu, membuang konteks tertentu, atau menggunakan bahasa yang menolak pembaca ke arah satu kesimpulan. Raven tidak menggantikan satu propaganda dengan propaganda lain. Kami pecahkan cerita itu, asingkan fakta daripada dakwaan, kenal pasti pencetus emosi dan kategori yang dicampur, kemudian bina semula penerangan yang bukti boleh tanggung.</p>', 'main hero')
t = replace_required(t,
    '<section class="case-section"><div class="section-marker"><span>01</span><p>Lead</p></div><h2>Masalah sebenar bukan kekurangan naratif. Masalahnya ialah naratif sering bergerak lebih laju daripada bukti.</h2><p class="section-lead">RCI merekodkan isu serius dalam tadbir urus, pelaburan dan pelaporan. Dalam masa sama, parti politik menekankan bahagian berlainan daripada rekod itu. RAVEN-Trace tidak menyamakan pilihan sudut dengan penipuan; kami semak apa yang disebut, apa yang ditinggalkan dan apa yang boleh dibuktikan.</p>',
    '<section class="case-section"><div class="section-marker"><span>01</span><p>Bagaimana Raven membaca naratif</p></div><h2>Jangan mula dengan siapa yang bercakap. Mula dengan apa yang boleh dibuktikan.</h2><p class="section-lead">RCI merekodkan isu serius dalam tadbir urus, pelaburan dan pelaporan. Politik kemudian membina cerita di atas rekod itu. Raven mulakan dengan fakta yang boleh disahkan, baru menilai bahasa, pilihan fakta, perkara yang disenyapkan dan kesimpulan yang cuba dibentuk.</p><div class="case-warning light"><strong>Urutan Raven</strong><span><b>1 · FAKTA ASAS</b> — apa yang rekod benar-benar kata. <b>2 · DAKWAAN</b> — apa yang seseorang mahu kita percaya. <b>3 · TEKNIK NARATIF</b> — bahasa emosi, nombor tanpa kategori, pilihan fakta, identiti atau andaian motif. <b>4 · KONTEKS HILANG</b> — apa yang perlu diketahui sebelum membuat kesimpulan. <b>5 · REKONSTRUKSI</b> — penerangan paling tepat yang bukti semasa boleh tanggung.</span></div>', 'main lead')
t = replace_required(t,
    '<div class="case-warning light"><strong>Kaedah baca</strong><span><b>FAKTA</b> = rekod menyokong. <b>DAKWAAN</b> = sesuatu pihak menyatakannya. <b>KESIMPULAN SEMENTARA</b> = tafsiran yang munasabah tetapi bukan bukti niat. <b>BELUM DIKETAHUI</b> = rekod belum cukup.</span></div>',
    '<div class="case-warning light"><strong>Kaedah baca</strong><span><b>FAKTA</b> = rekod menyokong. <b>DAKWAAN</b> = sesuatu pihak menyatakannya. <b>KESIMPULAN SEMENTARA</b> = tafsiran munasabah tetapi belum terbukti. <b>BELUM DIKETAHUI</b> = rekod belum cukup. <b>AMARAN NARATIF</b> = bahasa atau struktur cerita yang boleh mengubah persepsi tanpa menambah bukti.</span></div>', 'main method legend')
t = replace_required(t,
    '<section class="case-section"><div class="section-marker"><span>02</span><p>Dakwaan vs rekod</p></div><h2>Lapan naratif utama — dibedah sebagai claim, rekod, konteks yang tertinggal, verdict dan bukti yang boleh mengubahnya.</h2>',
    '<section class="case-section"><div class="section-marker"><span>02</span><p>Naratif vs bukti</p></div><h2>Lapan naratif utama — buang framing dahulu, kemudian lihat apa yang tinggal.</h2>', 'main narratives heading')

# Language labels used across all narrative cards.
for old,new in [
    ('<b>Siapa menggunakan naratif ini?</b>', '<b>Cerita yang dibawa</b>'),
    ('<b>Apa rekod tunjuk?</b>', '<b>Apa yang boleh disahkan?</b>'),
    ('<b>Konteks yang sering tertinggal:</b>', '<b>Apa yang cerita ini tinggalkan?</b>'),
    ('<b>Verdict Raven:</b>', '<b>Selepas framing dibuang:</b>'),
    ('<b>Apa yang boleh mengubah verdict?</b>', '<b>Bukti apa boleh mengubah penilaian?</b>'),
    ('<b>Confidence:</b>', '<b>Tahap keyakinan:</b>'),
]:
    t = t.replace(old,new)

# Strong, memorable closure before the existing scripts/footer.
anchor = '<script src="/raventrace-my/assets/js/raven.js?v=3.0.0" defer></script>'
if anchor not in t:
    raise SystemExit('Main narrative closing script anchor missing')
closure = '''<section class="case-section" id="narrative-rule"><div class="section-marker"><span>R</span><p>Peraturan Raven</p></div><h2>Naratif yang kuat tidak semestinya benar. Naratif yang lemah tidak semestinya palsu.</h2><p class="section-lead">Kekuatan emosi, jumlah perkongsian, identiti parti atau keyakinan seseorang tidak mengubah standard bukti. Jika satu dakwaan benar, ia patut kekal benar selepas slogan, kemarahan dan identiti dibuang.</p><div class="case-warning light"><strong>Soalan terakhir sebelum percaya</strong><span>Jika ayat ini ditulis tanpa nama parti, tanpa kata-kata marah dan tanpa angka yang tidak diterangkan — adakah bukti yang tinggal masih membawa kita kepada kesimpulan yang sama?</span></div></section>\n'''
t = t.replace(anchor, closure + anchor, 1)
main.write_text(t, encoding='utf-8')

# --- Political/social narrative page: reduce priming and teach manipulation resistance ---
s = social.read_text(encoding='utf-8')
s = replace_required(s,
    '<title>RCI Tabung Haji — Peta naratif politik & media sosial | RAVEN-Trace</title>',
    '<title>RCI Tabung Haji — Forensik politik & media sosial | RAVEN-Trace</title>', 'social title')
s = replace_required(s,
    '<meta name="description" content="Audit RAVEN-Trace terhadap naratif politik dan signal media sosial sekitar RCI Tabung Haji, dengan pemisahan antara kenyataan politik, rekod, inference dan perkara yang belum dapat disahkan.">',
    '<meta name="description" content="Forensik RAVEN-Trace terhadap bahasa politik dan media sosial sekitar RCI Tabung Haji: apa yang disahkan, apa yang dipilih, apa yang ditinggalkan dan bagaimana framing boleh mempengaruhi pembaca.">', 'social description')
s = replace_required(s,
    '<meta property="og:title" content="Peta naratif politik & media sosial — RCI Tabung Haji">',
    '<meta property="og:title" content="Forensik politik & media sosial — RCI Tabung Haji">', 'social og title')
s = replace_required(s,
    '<meta property="og:description" content="Siapa membawa naratif apa, apa yang disokong rekod, dan di mana media sosial mengamplifikasi tuntutan yang masih memerlukan bukti.">',
    '<meta property="og:description" content="Bukan siapa paling kuat bercakap. Soalannya: apa bukti, apa yang hilang, dan bagaimana bahasa cuba mengarah kesimpulan kita?">', 'social og desc')
s = replace_required(s,
    '<body class="case-share-page"><a class="skip-link" href="#main">Terus ke kandungan</a>',
    '<body class="case-share-page"><a class="skip-link" href="#main">Terus ke kandungan</a>', 'social body')
s = replace_required(s,
    '<main id="main"><header class="section-intro"><div class="container"><p class="section-kicker">RCI TABUNG HAJI · NARATIF POLITIK + MEDIA SOSIAL</p><h1>Siapa kata apa — dan apa yang rekod sebenarnya tunjuk?</h1><p>Halaman ini menggabungkan sebuah laporan deep-research yang dihantar kepada RAVEN-Trace dengan semakan silang terhadap sumber awam. Laporan asal berguna sebagai peta aktor, slogan dan signal media sosial, tetapi ia bukan evidence pack muktamad.</p>',
    '<main id="main"><header class="section-intro"><div class="container"><p class="section-kicker">RCI TABUNG HAJI · FORENSIK POLITIK + MEDIA SOSIAL</p><h1>Buang parti, buang slogan, buang emosi — apa bukti yang masih tinggal?</h1><p>Halaman ini menggunakan laporan deep-research sebagai peta awal untuk mencari naratif, kemudian mengujinya terhadap sumber awam. Tujuannya bukan memilih kem politik yang “betul”. Tujuannya ialah mengurangkan kuasa framing: asingkan apa yang berlaku daripada apa yang pembaca disuruh rasa atau simpulkan.</p>', 'social hero')
s = replace_required(s,
    '<section class="case-section"><div class="section-marker"><span>01</span><p>Status laporan</p></div><h2>Laporan ini berguna sebagai peta naratif — tetapi beberapa bahagian perlu dibersihkan sebelum menjadi fakta penerbitan.</h2>',
    '<section class="case-section"><div class="section-marker"><span>01</span><p>Status bukti</p></div><h2>Laporan ini ialah peta untuk mencari cerita — bukan lesen untuk mempercayainya.</h2>', 'social status heading')

for old,new in [
    ('<b>Frame:</b>', '<b>Cerita yang ditekankan:</b>'),
    ('<b>Rekod:</b>', '<b>Apa yang boleh disahkan:</b>'),
    ('<b>Gap:</b>', '<b>Apa yang belum terbukti:</b>'),
    ('<b>Verdict:</b>', '<b>Selepas framing dibuang:</b>'),
    ('<b>Confidence:</b>', '<b>Tahap keyakinan:</b>'),
    ('<b>Interpretasi:</b>', '<b>Tafsiran yang muncul:</b>'),
    ('<b>Risiko framing:</b>', '<b>Risiko manipulasi bahasa:</b>'),
]:
    s = s.replace(old,new)

# Insert a forensic language/NLP section before current social signals.
needle = '<section class="case-section"><div class="section-marker"><span>03</span><p>Signal media sosial</p></div>'
if needle not in s:
    raise SystemExit('Social signal section anchor missing')
nlp = '''<section class="case-section" id="language-forensics"><div class="section-marker"><span>03</span><p>Forensik bahasa</p></div><h2>Bagaimana naratif mengubah persepsi tanpa perlu mencipta fakta palsu.</h2><p class="section-lead">Manipulasi tidak semestinya datang dalam bentuk pembohongan terus. Cerita yang hanya memilih fakta tertentu, menukar kategori, mengulang label emosi atau meneka motif boleh mengubah cara orang memahami peristiwa walaupun sebahagian ayatnya benar.</p><div class="control-grid"><article><h3>1 · Pilih fakta, buang konteks</h3><p><span class="status context">SELECTION EFFECT</span></p><p>Satu cerita boleh menggunakan fakta yang betul tetapi hanya menunjukkan bahagian yang menyokong kesimpulan tertentu. Raven cari fakta relevan yang tidak dimasukkan sebelum menilai cerita.</p></article><article><h3>2 · Campur kategori</h3><p><span class="status disputed">CATEGORY COLLAPSE</span></p><p>Kerugian, defisit aset-liabiliti, impairment, transaksi meragukan dan kecurian bukan kategori yang sama. Menukarnya menjadi satu perkataan seperti “hilang” atau “sakau” boleh membuat kesimpulan jenayah terasa sudah terbukti.</p></article><article><h3>3 · Emosi sebelum bukti</h3><p><span class="status claim">EMOTIONAL PRIMING</span></p><p>Perkataan seperti “umat Islam”, “pengkhianat”, “diserang” atau “diselamatkan” boleh menentukan siapa pembaca rasa perlu dibela sebelum mereka melihat rekod. Emosi ialah signal untuk berhenti dan semak — bukan bukti tambahan.</p></article><article><h3>4 · Tindakan menjadi niat</h3><p><span class="status context">MOTIVE INFLATION</span></p><p>Perubahan fokus, walkout, desakan RCI baharu atau timing kenyataan boleh diperhatikan. Tetapi “mahu mengalih perhatian”, “mahu melindungi parti” atau “mahu menyerang Islam” memerlukan bukti tentang niat.</p></article><article><h3>5 · Ulang dakwaan sampai terasa biasa</h3><p><span class="status claim">REPETITION RISK</span></p><p>Raven elak mengulang slogan palsu atau tidak terbukti tanpa perlu. Pembetulan bermula dengan fakta yang benar, kemudian sebut dakwaan sekali jika perlu, jelaskan tekniknya, dan tutup dengan penerangan yang betul.</p></article><article><h3>6 · Viral menjadi “suara rakyat”</h3><p><span class="status disputed">REPRESENTATIVENESS ERROR</span></p><p>Beberapa posting popular tidak mewakili penduduk Malaysia, penyokong satu parti atau seluruh platform. Tanpa sampel yang jelas, Raven hanya memanggilnya <b>signal yang diperhatikan</b>.</p></article></div><div class="case-warning light"><strong>Neutralise, bukan counter-spin</strong><span>Raven tidak membalas slogan dengan slogan. Kami utamakan fakta yang benar, terangkan teknik manipulasi secara ringkas, kemudian beri pembaca model alternatif yang lebih tepat. Tujuannya ialah meningkatkan ketepatan penilaian — bukan memindahkan kesetiaan daripada satu kem kepada kem lain.</span></div></section>\n\n<section class="case-section"><div class="section-marker"><span>04</span><p>Signal media sosial</p></div>'''
s = s.replace(needle, nlp, 1)
# Renumber later section markers to avoid duplicate 04/05 where practical.
s = s.replace('<div class="section-marker"><span>04</span><p>Red-team</p></div>', '<div class="section-marker"><span>05</span><p>Red-team</p></div>', 1)
s = s.replace('<div class="section-marker"><span>05</span><p>Sumber silang</p></div>', '<div class="section-marker"><span>06</span><p>Sumber silang</p></div>', 1)

# Add research principles to source section before closing scripts if source URLs exist.
script_anchor = '<script src="/raventrace-my/assets/js/raven.js?v=3.0.0" defer></script>'
if script_anchor not in s:
    raise SystemExit('Social closing script anchor missing')
research = '''<section class="case-section"><div class="section-marker"><span>07</span><p>Prinsip komunikasi</p></div><h2>Kenapa Raven bermula dengan fakta, bukan dengan mengulang mitos.</h2><p>Reka bentuk bahasa halaman ini mengikuti satu prinsip mudah: pembetulan perlu menguatkan model yang benar, bukan menjadikan dakwaan salah lebih mudah diingati. Kajian eksperimen menunjukkan pembetulan dan prebunking boleh mengurangkan kepercayaan terhadap maklumat mengelirukan; penyampaian yang menegaskan fakta tepat juga boleh meningkatkan engagement berbanding hanya membingkai mesej sebagai penafian. Kajian framing terkini turut menunjukkan pemilihan fakta yang tepat tetapi tidak seimbang boleh mengubah sikap dan emosi pembaca.</p><ul><li><a href="https://www.nature.com/articles/s41598-024-71599-6" rel="noopener noreferrer">Scientific Reports · prebunking vs debunking, 2024</a></li><li><a href="https://www.nature.com/articles/s41598-024-53337-0" rel="noopener noreferrer">Scientific Reports · confirmation framing in fact-checks, 2024</a></li><li><a href="https://www.nature.com/articles/s41598-025-29519-9" rel="noopener noreferrer">Scientific Reports · selective presentation and news framing, 2025</a></li><li><a href="https://www.nature.com/articles/s41562-024-02023-2" rel="noopener noreferrer">Nature Human Behaviour · inoculation + accuracy prompting, 2024/2025</a></li></ul></section>\n'''
s = s.replace(script_anchor, research + script_anchor, 1)
social.write_text(s, encoding='utf-8')

print('Narrative Forensics NLP V4 applied successfully')
