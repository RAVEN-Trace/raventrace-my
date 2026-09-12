from pathlib import Path
import re

main = Path('investigations/rci-tabung-haji/narratives/index.html')
social = Path('investigations/rci-tabung-haji/narratives/political-social-media/index.html')


def sub1(text, pattern, repl, label, flags=0):
    out, n = re.subn(pattern, repl, text, count=1, flags=flags)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 replacement, got {n}')
    return out

# MAIN PAGE
m = main.read_text(encoding='utf-8')
if 'FORENSIK NARATIF' not in m:
    m = sub1(m, r'<title>.*?</title>', '<title>RCI Tabung Haji — Forensik Naratif: cerita vs bukti | RAVEN-Trace</title>', 'main title')
    m = sub1(m, r'<meta name="description" content="[^"]*">', '<meta name="description" content="Forensik naratif RCI Tabung Haji: pecahkan bahasa, emosi, konteks dan dakwaan supaya pembaca dapat membezakan cerita politik daripada bukti yang boleh diaudit.">', 'main desc')
    m = sub1(m, r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="RCI Tabung Haji — Forensik Naratif: cerita vs bukti">', 'main og title')
    m = sub1(m, r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="Raven pecahkan naratif kepada dakwaan, bukti, konteks yang hilang dan teknik bahasa — supaya pembaca boleh menilai tanpa dipaksa menerima framing mana-mana pihak.">', 'main og desc')
    m = sub1(m, r'<p class="section-kicker">RCI TABUNG HAJI · AUDIT NARATIF</p><h1>.*?</h1>\s*<p>.*?</p>', '<p class="section-kicker">RCI TABUNG HAJI · FORENSIK NARATIF</p><h1>Apa yang cerita cuba buat kita percaya — dan apa yang bukti benar-benar tunjuk?</h1>\n<p>Naratif tidak semestinya palsu. Selalunya ia memilih fakta tertentu, membuang konteks tertentu, atau menggunakan bahasa yang menolak pembaca ke arah satu kesimpulan. Raven tidak menggantikan satu propaganda dengan propaganda lain. Kami pecahkan cerita itu, asingkan fakta daripada dakwaan, kenal pasti pencetus emosi dan kategori yang dicampur, kemudian bina semula penerangan yang bukti boleh tanggung.</p>', 'main hero', re.S)
    m = sub1(m, r'<section class="case-section"><div class="section-marker"><span>01</span><p>Lead</p></div><h2>.*?</h2><p class="section-lead">.*?</p>', '<section class="case-section"><div class="section-marker"><span>01</span><p>Bagaimana Raven membaca naratif</p></div><h2>Jangan mula dengan siapa yang bercakap. Mula dengan apa yang boleh dibuktikan.</h2><p class="section-lead">RCI merekodkan isu serius dalam tadbir urus, pelaburan dan pelaporan. Politik kemudian membina cerita di atas rekod itu. Raven mulakan dengan fakta yang boleh disahkan, baru menilai bahasa, pilihan fakta, perkara yang disenyapkan dan kesimpulan yang cuba dibentuk.</p><div class="case-warning light"><strong>Urutan Raven</strong><span><b>1 · FAKTA ASAS</b> — apa yang rekod benar-benar kata. <b>2 · DAKWAAN</b> — apa yang seseorang mahu kita percaya. <b>3 · TEKNIK NARATIF</b> — bahasa emosi, nombor tanpa kategori, pilihan fakta, identiti atau andaian motif. <b>4 · KONTEKS HILANG</b> — apa yang perlu diketahui sebelum membuat kesimpulan. <b>5 · REKONSTRUKSI</b> — penerangan paling tepat yang bukti semasa boleh tanggung.</span></div>', 'main lead', re.S)
    m = m.replace('<b>KESIMPULAN SEMENTARA</b> = tafsiran yang munasabah tetapi bukan bukti niat. <b>BELUM DIKETAHUI</b> = rekod belum cukup.', '<b>KESIMPULAN SEMENTARA</b> = tafsiran munasabah tetapi belum terbukti. <b>BELUM DIKETAHUI</b> = rekod belum cukup. <b>AMARAN NARATIF</b> = bahasa atau struktur cerita yang boleh mengubah persepsi tanpa menambah bukti.')
    m = m.replace('<p>Dakwaan vs rekod</p></div><h2>Lapan naratif utama — dibedah sebagai claim, rekod, konteks yang tertinggal, verdict dan bukti yang boleh mengubahnya.</h2>', '<p>Naratif vs bukti</p></div><h2>Lapan naratif utama — buang framing dahulu, kemudian lihat apa yang tinggal.</h2>')
    for a,b in [
        ('<b>Siapa menggunakan naratif ini?</b>','<b>Cerita yang dibawa</b>'),
        ('<b>Apa rekod tunjuk?</b>','<b>Apa yang boleh disahkan?</b>'),
        ('<b>Konteks yang sering tertinggal:</b>','<b>Apa yang cerita ini tinggalkan?</b>'),
        ('<b>Verdict Raven:</b>','<b>Selepas framing dibuang:</b>'),
        ('<b>Apa yang boleh mengubah verdict?</b>','<b>Bukti apa boleh mengubah penilaian?</b>'),
        ('<b>Confidence:</b>','<b>Tahap keyakinan:</b>')]: m=m.replace(a,b)
    anchor='<script src="/raventrace-my/assets/js/raven.js?v=3.0.0" defer></script>'
    closure='<section class="case-section" id="narrative-rule"><div class="section-marker"><span>R</span><p>Peraturan Raven</p></div><h2>Naratif yang kuat tidak semestinya benar. Naratif yang lemah tidak semestinya palsu.</h2><p class="section-lead">Kekuatan emosi, jumlah perkongsian, identiti parti atau keyakinan seseorang tidak mengubah standard bukti. Jika satu dakwaan benar, ia patut kekal benar selepas slogan, kemarahan dan identiti dibuang.</p><div class="case-warning light"><strong>Soalan terakhir sebelum percaya</strong><span>Jika ayat ini ditulis tanpa nama parti, tanpa kata-kata marah dan tanpa angka yang tidak diterangkan — adakah bukti yang tinggal masih membawa kita kepada kesimpulan yang sama?</span></div></section>\n'
    if anchor not in m: raise SystemExit('main script anchor missing')
    m=m.replace(anchor,closure+anchor,1)
main.write_text(m,encoding='utf-8')

# POLITICAL / SOCIAL PAGE
s=social.read_text(encoding='utf-8')
if 'FORENSIK POLITIK + MEDIA SOSIAL' not in s:
    s=sub1(s,r'<title>.*?</title>','<title>RCI Tabung Haji — Forensik politik & media sosial | RAVEN-Trace</title>','social title')
    s=sub1(s,r'<meta name="description" content="[^"]*">','<meta name="description" content="Forensik RAVEN-Trace terhadap bahasa politik dan media sosial sekitar RCI Tabung Haji: apa yang disahkan, apa yang dipilih, apa yang ditinggalkan dan bagaimana framing boleh mempengaruhi pembaca.">','social desc')
    s=sub1(s,r'<meta property="og:title" content="[^"]*">','<meta property="og:title" content="Forensik politik & media sosial — RCI Tabung Haji">','social og title')
    s=sub1(s,r'<meta property="og:description" content="[^"]*">','<meta property="og:description" content="Bukan siapa paling kuat bercakap. Soalannya: apa bukti, apa yang hilang, dan bagaimana bahasa cuba mengarah kesimpulan kita?">','social og desc')
    s=sub1(s,r'<p class="section-kicker">RCI TABUNG HAJI · NARATIF POLITIK \+ MEDIA SOSIAL</p><h1>.*?</h1><p>.*?</p>','<p class="section-kicker">RCI TABUNG HAJI · FORENSIK POLITIK + MEDIA SOSIAL</p><h1>Buang parti, buang slogan, buang emosi — apa bukti yang masih tinggal?</h1><p>Halaman ini menggunakan laporan deep-research sebagai peta awal untuk mencari naratif, kemudian mengujinya terhadap sumber awam. Tujuannya bukan memilih kem politik yang “betul”. Tujuannya ialah mengurangkan kuasa framing: asingkan apa yang berlaku daripada apa yang pembaca disuruh rasa atau simpulkan.</p>','social hero',re.S)
    s=sub1(s,r'<section class="case-section"><div class="section-marker"><span>01</span><p>Status laporan</p></div><h2>.*?</h2>','<section class="case-section"><div class="section-marker"><span>01</span><p>Status bukti</p></div><h2>Laporan ini ialah peta untuk mencari cerita — bukan lesen untuk mempercayainya.</h2>','social status',re.S)
    for a,b in [
        ('<b>Frame:</b>','<b>Cerita yang ditekankan:</b>'),('<b>Rekod:</b>','<b>Apa yang boleh disahkan:</b>'),('<b>Gap:</b>','<b>Apa yang belum terbukti:</b>'),('<b>Verdict:</b>','<b>Selepas framing dibuang:</b>'),('<b>Confidence:</b>','<b>Tahap keyakinan:</b>'),('<b>Interpretasi:</b>','<b>Tafsiran yang muncul:</b>'),('<b>Risiko framing:</b>','<b>Risiko manipulasi bahasa:</b>'),
        ('<b>Keyakinan:</b>','<b>Tahap keyakinan:</b>'),('<b>Kesimpulan RAVEN:</b>','<b>Selepas framing dibuang:</b>')]: s=s.replace(a,b)
    needle='<section class="case-section"><div class="section-marker"><span>03</span><p>Signal media sosial</p></div>'
    if needle not in s: raise SystemExit('social signal anchor missing')
    nlp='''<section class="case-section" id="language-forensics"><div class="section-marker"><span>03</span><p>Forensik bahasa</p></div><h2>Bagaimana naratif mengubah persepsi tanpa perlu mencipta fakta palsu.</h2><p class="section-lead">Manipulasi tidak semestinya datang sebagai pembohongan terus. Cerita yang memilih fakta tertentu, menukar kategori, mengulang label emosi atau meneka motif boleh mengubah cara orang memahami peristiwa walaupun sebahagian ayatnya benar.</p><div class="control-grid"><article><h3>1 · Pilih fakta, buang konteks</h3><p><span class="status context">SELECTION EFFECT</span></p><p>Satu cerita boleh menggunakan fakta yang betul tetapi hanya menunjukkan bahagian yang menyokong kesimpulan tertentu. Raven cari fakta relevan yang tidak dimasukkan sebelum menilai cerita.</p></article><article><h3>2 · Campur kategori</h3><p><span class="status disputed">CATEGORY COLLAPSE</span></p><p>Kerugian, defisit aset-liabiliti, impairment, transaksi meragukan dan kecurian bukan kategori yang sama. Menukarnya menjadi satu perkataan seperti “hilang” atau “sakau” boleh membuat kesimpulan jenayah terasa sudah terbukti.</p></article><article><h3>3 · Emosi sebelum bukti</h3><p><span class="status claim">EMOTIONAL PRIMING</span></p><p>Perkataan seperti “umat Islam”, “pengkhianat”, “diserang” atau “diselamatkan” boleh menentukan siapa pembaca rasa perlu dibela sebelum melihat rekod. Emosi ialah signal untuk berhenti dan semak — bukan bukti tambahan.</p></article><article><h3>4 · Tindakan menjadi niat</h3><p><span class="status context">MOTIVE INFLATION</span></p><p>Perubahan fokus, walkout, desakan RCI baharu atau timing kenyataan boleh diperhatikan. Tetapi “mahu mengalih perhatian”, “mahu melindungi parti” atau “mahu menyerang Islam” memerlukan bukti tentang niat.</p></article><article><h3>5 · Ulang dakwaan sampai terasa biasa</h3><p><span class="status claim">REPETITION RISK</span></p><p>Raven elak mengulang slogan palsu atau tidak terbukti tanpa perlu. Pembetulan bermula dengan fakta yang benar, kemudian sebut dakwaan sekali jika perlu, jelaskan tekniknya, dan tutup dengan penerangan yang betul.</p></article><article><h3>6 · Viral menjadi “suara rakyat”</h3><p><span class="status disputed">REPRESENTATIVENESS ERROR</span></p><p>Beberapa posting popular tidak mewakili penduduk Malaysia, penyokong satu parti atau seluruh platform. Tanpa sampel yang jelas, Raven hanya memanggilnya <b>signal yang diperhatikan</b>.</p></article></div><div class="case-warning light"><strong>Neutralise, bukan counter-spin</strong><span>Raven tidak membalas slogan dengan slogan. Kami utamakan fakta yang benar, terangkan teknik manipulasi secara ringkas, kemudian beri pembaca model alternatif yang lebih tepat. Tujuannya ialah meningkatkan ketepatan penilaian — bukan memindahkan kesetiaan daripada satu kem kepada kem lain.</span></div></section>\n\n<section class="case-section"><div class="section-marker"><span>04</span><p>Signal media sosial</p></div>'''
    s=s.replace(needle,nlp,1)
    # Renumber pre-existing later sections if labels exist.
    s=s.replace('<div class="section-marker"><span>04</span><p>Audit bahasa</p></div>','<div class="section-marker"><span>05</span><p>Audit bahasa</p></div>',1)
    s=s.replace('<div class="section-marker"><span>05</span><p>Sumber silang</p></div>','<div class="section-marker"><span>06</span><p>Sumber silang</p></div>',1)
    anchor='<script src="/raventrace-my/assets/js/raven.js?v=3.0.0" defer></script>'
    research='<section class="case-section"><div class="section-marker"><span>07</span><p>Prinsip komunikasi</p></div><h2>Kenapa Raven bermula dengan fakta, bukan dengan mengulang mitos.</h2><p>Reka bentuk bahasa halaman ini mengutamakan model yang benar terlebih dahulu. Pembetulan menyebut dakwaan mengelirukan hanya apabila perlu, menerangkan teknik manipulasi, kemudian kembali kepada fakta dan penerangan yang boleh diuji.</p><ul><li><a href="https://www.nature.com/articles/s41598-024-71599-6" rel="noopener noreferrer">Scientific Reports · prebunking vs debunking</a></li><li><a href="https://www.nature.com/articles/s41598-024-53337-0" rel="noopener noreferrer">Scientific Reports · confirmation framing in fact-checks</a></li><li><a href="https://www.nature.com/articles/s41598-025-29519-9" rel="noopener noreferrer">Scientific Reports · selective presentation and news framing</a></li><li><a href="https://www.nature.com/articles/s41562-024-02023-2" rel="noopener noreferrer">Nature Human Behaviour · inoculation + accuracy prompting</a></li></ul></section>\n'
    if anchor not in s: raise SystemExit('social script anchor missing')
    s=s.replace(anchor,research+anchor,1)
social.write_text(s,encoding='utf-8')

# QA
for path, tokens in [(main,['FORENSIK NARATIF','Urutan Raven','AMARAN NARATIF','Peraturan Raven']), (social,['FORENSIK POLITIK + MEDIA SOSIAL','Forensik bahasa','CATEGORY COLLAPSE','EMOTIONAL PRIMING','MOTIVE INFLATION','REPETITION RISK','REPRESENTATIVENESS ERROR','Neutralise, bukan counter-spin','Prinsip komunikasi'])]:
    x=path.read_text(encoding='utf-8')
    for tok in tokens:
        assert tok in x, f'{path}: missing {tok}'
print('Narrative Forensics NLP V4.1 applied: PASS')
