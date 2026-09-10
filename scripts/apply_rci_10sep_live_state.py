from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text()


def write(rel, text):
    (ROOT / rel).write_text(text)


def replace(text, old, new):
    return text.replace(old, new)

# --- CASEFILE master ---
rel = 'investigations/rci-tabung-haji/index.html'
s = read(rel)
s = replace(s, 'dengan perkembangan disemak hingga 9 September 2026.', 'dengan perkembangan disemak hingga 10 September 2026.')
s = replace(s, 'SIASATAN · RCI-TH-2026 · dikemas kini 9 Sep', 'SIASATAN · RCI-TH-2026 · dikemas kini 10 Sep')
s = replace(s, 'Maklumat disemak hingga · 9 Sep 2026 · 18:29 MYT', 'Maklumat disemak hingga · 10 Sep 2026 · lewat malam MYT')
s = replace(s, 'Kemas kini semasa · 9 Sep 2026', 'Kemas kini semasa · 10 Sep 2026')
s = replace(s, '<div><dt>02</dt><dd>individu THP Bina didakwa · belum sabit</dd></div>', '<div><dt>04</dt><dd>individu didakwa setakat 10 Sep · belum sabit</dd></div>')
s = replace(s, 'Setakat 9 September, tiga individu telah didakwa dalam tindakan susulan berkaitan RCI dan semuanya belum disabitkan.', 'Setakat 10 September, empat individu telah didakwa dalam tindakan susulan berkaitan RCI dan semuanya belum disabitkan. Datuk Azmi Ahmad menjadi individu keempat selepas dua bekas pengurus THP Bina dan bekas Pengerusi TH Abdul Azeez Abdul Rahim.')
s = replace(s, '<h3>Proses mahkamah masih di peringkat awal.</h3><p>Pertuduhan yang telah dibaca perlu diuji di mahkamah. Prosiding yang dijadualkan tetapi ditunda mesti diterangkan mengikut status sebenar pada tarikh tersebut.</p>', '<h3>Empat individu kini telah didakwa.</h3><p>Setakat 10 September, empat individu telah didakwa dan semuanya mengaku tidak bersalah. Pertuduhan yang telah dibaca masih perlu diuji di mahkamah.</p>')

marker = '          <div class="trace-stack">\n'
if '10 Sep 2026 · Mahkamah Sesyen Kuala Lumpur' not in s:
    cards = '''            <article class="trace-card"><div class="trace-head"><span>JEJAK / 10-02</span><time datetime="2026-09-10">10 Sep 2026 · Kuala Lumpur</time></div><div class="meta-row"><span class="status fact">DISAHKAN · REMAN TAMAT</span><span class="source-grade">Gred B</span></div><h3>Reman Abdul Azeez dalam siasatan hibah TH tidak disambung.</h3><dl><div><dt>Apa jadi?</dt><dd>Permohonan polis untuk melanjutkan reman tiga hari lagi di bawah Seksyen 420 Kanun Keseksaan ditolak. Peguam beliau berkata siasatan masih boleh diteruskan tanpa tahanan reman.</dd></div><div><dt>Apa maksudnya?</dt><dd>Pelepasan daripada reman bukan NFA, bukan penutupan siasatan hibah, dan tidak mengubah pertuduhan SPRM yang telah dibaca pada 9 September.</dd></div></dl><p class="inline-sources"><a href="#s59">S59</a></p></article>\n            <article class="trace-card"><div class="trace-head"><span>JEJAK / 10-01</span><time datetime="2026-09-10">10 Sep 2026 · Mahkamah Sesyen Kuala Lumpur</time></div><div class="meta-row"><span class="status fact">DISAHKAN · MAHKAMAH</span><span class="source-grade">Gred B</span></div><h3>Azmi Ahmad didakwa atas dua pertuduhan menipu kadar sewaan harian kapal.</h3><dl><div><dt>Apa jadi?</dt><dd>Pengarah Urusan Kumpulan merangkap CEO Alam Maritim Resources Bhd itu mengaku tidak bersalah selepas dua pertuduhan dibacakan.</dd></div><div><dt>Kenapa penting?</dt><dd>Laporan awal 7 September menjangka beliau didakwa pada 11 September. Rekod mahkamah menunjukkan pertuduhan sebenar dibaca pada 10 September.</dd></div><div><dt>Had</dt><dd>Pertuduhan bukan sabitan. Dakwaan pendakwaan masih perlu diuji di mahkamah.</dd></div></dl><p class="inline-sources"><a href="#s58">S58</a></p></article>\n'''
    s = s.replace(marker, marker + cards, 1)

s = replace(s, '<article class="person-card"><div><span>05</span><span class="status unknown">Bebas reman · 19 Ogos</span></div><h3>Datuk Azmi Ahmad</h3><p class="role">Group MD & CEO Alam Maritim · sejak 2 Mei 2006</p><p>Syarikat mengumumkan beliau direman 17 Ogos untuk membantu siasatan SPRM dan dibebaskan 19 Ogos sebelum menyambung tugas. Dua laporan 7 September menamakan beliau sebagai individu yang dijangka didakwa; Malaysia Corporate menyebut 11 September dan dua pertuduhan Seksyen 417 Kanun Keseksaan. Tiada kertas pertuduhan rasmi ditemui setakat data masa semakan.</p><a href="#s37">S37</a> <a href="#s38">S38</a></article>', '<article class="person-card"><div><span>05</span><span class="status process">Didakwa · belum sabit</span></div><h3>Datuk Azmi Ahmad</h3><p class="role">Group MD & CEO Alam Maritim Resources Bhd</p><p>Didakwa pada 10 September atas dua pertuduhan menipu berkaitan kadar sewaan harian kapal. Beliau mengaku tidak bersalah dan meminta dibicarakan. Laporan awal 7 September menjangka tarikh 11 September; rekod mahkamah menunjukkan pertuduhan sebenar dibaca sehari lebih awal.</p><a href="#s58">S58</a></article>')
s = replace(s, 'Dua laporan 7 September menamakan beliau sebagai individu yang dijangka didakwa; Malaysia Corporate menyebut 10 September dan Seksyen 23 Akta SPRM, tetapi butiran itu belum disahkan secara rasmi setakat data masa semakan.', 'Beliau didakwa pada 9 September di bawah Seksyen 23(1) Akta SPRM 2009. Dalam trek PDRM yang berasingan berkaitan hibah 2017, reman beliau tidak disambung pada 10 September; siasatan itu masih boleh diteruskan.')
s = replace(s, '<article><time>7 Sep</time><h3>Laporan jangkaan pendakwaan</h3><p>Suara.TV dan Malaysia Corporate menamakan Azeez, Jamil dan Azmi sebagai individu yang dijangka didakwa. Malaysia Corporate memberi butiran lebih spesifik, tetapi setakat masa semakan ia masih belum disahkan oleh SPRM, AGC atau rekod mahkamah.</p></article>', '<article><time>7 Sep</time><h3>Laporan jangkaan pendakwaan</h3><p>Suara.TV dan Malaysia Corporate menamakan Azeez, Jamil dan Azmi. Dua nama kemudian memang didakwa, tetapi tarikh yang dilaporkan berubah: Azeez pada 9 September dan Azmi pada 10 September.</p></article><article><time>10 Sep</time><h3>Azmi didakwa</h3><p>Azmi Ahmad mengaku tidak bersalah atas dua pertuduhan menipu berkaitan kadar sewaan harian kapal.</p></article><article><time>10 Sep</time><h3>Reman hibah Abdul Azeez tamat</h3><p>Permohonan lanjutan reman ditolak. Siasatan PDRM di bawah Seksyen 420 masih boleh diteruskan tanpa reman.</p></article>')
s = replace(s, '<li>Adakah SPRM atau AGC akan mengesahkan laporan 7 September yang menamakan Azeez, Jamil dan Azmi serta tarikh 10/11/17 September?</li>', '<li>Adakah Jamil Khir akan didakwa seperti dijangka dalam laporan 7 September, dan jika ya apakah tarikh, seksyen serta pertuduhan sebenar?</li>')
s = replace(s, 'Semak next</h3><p>Dapatkan tindakan selepas reman 8 September, pengesahan SPRM/AGC terhadap laporan 7 September, nombor kes dan helaian pertuduhan jika prosiding benar-benar berlaku pada tarikh 10/11/17 September yang dilaporkan, keputusan AGC bagi Al-Rawda, empat fail NFA, transkrip RCI, audit forensik dan status lengkap enam syor RCI yang masih berjalan.</p>', 'Semak next</h3><p>Pantau keputusan reman dua individu dalam trek AMLA sehingga 11 September, sebarang pengesahan rasmi mengenai Jamil Khir, perkembangan siasatan hibah selepas reman Abdul Azeez tamat, keputusan AGC bagi Al-Rawda, empat fail NFA, transkrip RCI, audit forensik dan status lengkap enam syor RCI yang masih berjalan.</p>')
source_anchor = '            <li id="s50"><span>B</span><a href="https://bernama.com/radio/news.php?id=2602611" rel="noopener noreferrer">RM11.5b sukuk UJSB ialah pembiayaan semula</a><small>Bernama · 3 Sep</small></li>\n'
if 'id="s58"' not in s:
    extra = '''            <li id="s58"><span>B</span><a href="https://www.bernama.com/bm/jenayah_mahkamah/news.php?id=2605277" rel="noopener noreferrer">Azmi Ahmad didakwa atas dua pertuduhan menipu kadar sewaan kapal</a><small>Bernama · 10 Sep · Mahkamah Sesyen Kuala Lumpur</small></li>\n            <li id="s59"><span>B</span><a href="https://www.bernama.com/bm/wilayah/news.php?id=2605390" rel="noopener noreferrer">Reman Abdul Azeez tidak disambung dalam siasatan hibah</a><small>Bernama · 10 Sep · kenyataan peguam selepas prosiding reman</small></li>\n            <li id="s60"><span>B</span><a href="https://www.bernama.com/tv/news.php?id=2605104" rel="noopener noreferrer">Lima ditahan dalam trek hibah dan AMLA</a><small>Bernama · 9 Sep · kenyataan PDRM</small></li>\n'''
    s = s.replace(source_anchor, source_anchor + extra)
s = replace(s, '<strong>Maklumat disemak hingga:</strong> 7 September 2026 · lewat malam MYT. <strong>Semakan laman:</strong> 7 September 2026 · v18.', '<strong>Maklumat disemak hingga:</strong> 10 September 2026 · lewat malam MYT. <strong>Semakan laman:</strong> 10 September 2026.')
write(rel, s)

# --- investigations desk ---
rel = 'investigations/index.html'
s = read(rel)
s = s.replace('disemak hingga 9 September 2026.', 'disemak hingga 10 September 2026.')
s = s.replace('disemak hingga 9 Sep 2026 · 17:26 MYT', 'disemak hingga 10 Sep 2026 · lewat malam MYT')
s = s.replace('Maklumat disemak hingga · 9 Sep 2026 · 17:26 MYT', 'Maklumat disemak hingga · 10 Sep 2026 · lewat malam MYT')
s = s.replace('Pada 9 September, Bernama melaporkan tiga individu telah didakwa setakat itu dalam tindakan susulan berkaitan RCI, termasuk bekas Pengerusi TH Abdul Azeez Abdul Rahim. Pertuduhan bukan sabitan.', 'Setakat 10 September, empat individu telah didakwa dalam tindakan susulan berkaitan RCI. Datuk Azmi Ahmad didakwa hari ini atas dua pertuduhan menipu berkaitan kadar sewaan harian kapal dan mengaku tidak bersalah. Pertuduhan bukan sabitan.')
s = s.replace('<div><b>Mahkamah</b><span>3 individu didakwa setakat 9 Sep · belum sabit</span></div>', '<div><b>Mahkamah</b><span>4 individu didakwa setakat 10 Sep · belum sabit</span></div>')
old = '<aside class="investigation-side"><section class="investigation-side-card"><h2>Perkembangan terbaru</h2><p><strong>9 Sep:</strong> Abdul Azeez Abdul Rahim didakwa di Mahkamah Sesyen Kuala Lumpur di bawah Seksyen 23(1) Akta SPRM 2009 berkaitan penggunaan kedudukan dan cadangan pelaburan sehingga RM193.5 juta dalam Putrajaya Perdana. Beliau mengaku tidak bersalah.</p><p><a href="/raventrace-my/news/2026/09/09/abdul-azeez-didakwa-rm1935-juta/">Baca keputusan semakan →</a></p></section>'
new = '<aside class="investigation-side"><section class="investigation-side-card"><h2>Perkembangan terbaru</h2><p><strong>10 Sep:</strong> Azmi Ahmad didakwa atas dua pertuduhan menipu kadar sewaan harian kapal dan mengaku tidak bersalah.</p><p><a href="/raventrace-my/news/2026/09/10/azmi-ahmad-didakwa/">Baca perkembangan →</a></p></section><section class="investigation-side-card"><h2>Trek hibah berasingan</h2><p><strong>10 Sep:</strong> reman Abdul Azeez tidak disambung dalam siasatan PDRM di bawah Seksyen 420. Siasatan masih boleh diteruskan tanpa reman.</p><p><a href="/raventrace-my/news/2026/09/10/abdul-azeez-reman-tidak-disambung/">Semak status →</a></p></section>'
s = s.replace(old, new)
s = s.replace('Apa yang sudah disahkan setakat 9 September?', 'Apa yang sudah disahkan setakat 10 September?')
if 'news-2026-09-10-azmi' not in s:
    anchor = '<div class="update-grid">\n'
    card = '<article id="news-2026-09-10-azmi" class="update-card lead-update"><div class="update-index">00</div><div class="meta-row"><span class="status fact">DIDAKWA · BELUM SABIT</span><time datetime="2026-09-10">10 Sep 2026</time></div><h3>Azmi Ahmad didakwa atas dua pertuduhan menipu kadar sewaan kapal.</h3><p>Beliau mengaku tidak bersalah. Laporan awal menjangka 11 September; rekod mahkamah menunjukkan prosiding berlaku pada 10 September.</p><a href="/raventrace-my/news/2026/09/10/azmi-ahmad-didakwa/">Baca perkembangan →</a></article>\n'
    s = s.replace(anchor, anchor + card, 1)
write(rel, s)

# --- newsroom index ---
rel = 'news/index.html'
s = read(rel)
if 'news-2026-09-10-azmi-charged' not in s:
    idx = s.find('<article id="news-2026-09-09-azeez-charged"')
    if idx != -1:
        cards = '''<article id="news-2026-09-10-azmi-charged" class="timeline-item" data-topic="court"><time datetime="2026-09-10">10 SEP 2026</time><div><div class="meta-row"><span class="status fact">DISAHKAN · MAHKAMAH</span><span class="source-grade">Gred B</span></div><h3>Azmi Ahmad didakwa atas dua pertuduhan menipu kadar sewaan kapal.</h3><p>Beliau mengaku tidak bersalah. Pertuduhan bukan sabitan.</p><a href="/raventrace-my/news/2026/09/10/azmi-ahmad-didakwa/">Baca perkembangan →</a></div></article>\n<article id="news-2026-09-10-azeez-remand" class="timeline-item" data-topic="enforcement"><time datetime="2026-09-10">10 SEP 2026</time><div><div class="meta-row"><span class="status fact">DISAHKAN · REMAN TAMAT</span><span class="source-grade">Gred B</span></div><h3>Reman Abdul Azeez tidak disambung dalam siasatan hibah TH.</h3><p>Permohonan lanjutan reman ditolak. Siasatan masih boleh diteruskan tanpa tahanan reman.</p><a href="/raventrace-my/news/2026/09/10/abdul-azeez-reman-tidak-disambung/">Baca perkembangan →</a></div></article>\n'''
        s = s[:idx] + cards + s[idx:]
write(rel, s)

# --- section enhancement JS ---
rel = 'assets/js/raven-section.js'
s = read(rel)
s = s.replace('<article><time>10 Sep · checkpoint</time><h3>Azmi Ahmad dijadual didakwa</h3><p>Semakan sistem mahkamah yang dilaporkan Bernama', '<article><time>10 Sep · mahkamah</time><h3>Azmi Ahmad didakwa</h3><p>Bernama melaporkan Azmi mengaku tidak bersalah atas dua pertuduhan menipu berkaitan kadar sewaan harian kapal. Rekod sebenar menggantikan checkpoint terdahulu. Semakan sistem mahkamah yang dilaporkan Bernama')
if "addSourceRow('s58'" not in s:
    insert = "  addSourceRow('s58','B','https://www.bernama.com/bm/jenayah_mahkamah/news.php?id=2605277','Azmi Ahmad didakwa atas dua pertuduhan menipu','Bernama · 10 Sep · Mahkamah Sesyen');\n  addSourceRow('s59','B','https://www.bernama.com/bm/wilayah/news.php?id=2605390','Reman Abdul Azeez tidak disambung','Bernama · 10 Sep · siasatan hibah PDRM');\n  addSourceRow('s60','B','https://www.bernama.com/tv/news.php?id=2605104','Lima ditahan dalam trek hibah dan AMLA','Bernama · 9 Sep · kenyataan PDRM');\n"
    pos = s.find("  addSourceRow('s53'")
    if pos != -1:
        s = s[:pos] + insert + s[pos:]
write(rel, s)

# --- narrative page live-state correction ---
rel = 'investigations/rci-tabung-haji/narratives/index.html'
s = read(rel)
s = s.replace('Setakat 9 September, Bernama melaporkan tiga individu telah didakwa dalam tindakan susulan berkaitan RCI.', 'Setakat 10 September, empat individu telah didakwa dalam tindakan susulan berkaitan RCI. Azmi Ahmad didakwa pada 10 September selepas Abdul Azeez dan dua bekas pengurus THP Bina.')
write(rel, s)

print('Applied verified 10 Sep RCI live state.')
