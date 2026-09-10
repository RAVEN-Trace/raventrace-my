from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def patch(rel, fn):
    p = ROOT / rel
    if not p.exists():
        return
    s = p.read_text()
    s2 = fn(s)
    if s2 != s:
        p.write_text(s2)


def common(s):
    s = s.replace('Maklumat disemak hingga · 9 Sep 2026 · 18:29 MYT', 'Maklumat disemak hingga · 10 Sep 2026 · lewat malam MYT')
    s = s.replace('Maklumat disemak hingga · 9 Sep 2026', 'Maklumat disemak hingga · 10 Sep 2026')
    s = s.replace('Kemas kini semasa · 9 Sep 2026', 'Kemas kini semasa · 10 Sep 2026')
    return s


def updates(s):
    s = common(s)
    marker = '<div class="trace-stack">'
    if 'JEJAK / 10-01' not in s and marker in s:
        cards = '''<article class="trace-card"><div class="trace-head"><span>JEJAK / 10-02</span><time datetime="2026-09-10">10 Sep 2026 · Kuala Lumpur</time></div><div class="meta-row"><span class="status fact">DISAHKAN · REMAN TAMAT</span><span class="source-grade">Gred B</span></div><h3>Reman Abdul Azeez dalam siasatan hibah TH tidak disambung.</h3><dl><div><dt>Apa jadi?</dt><dd>Permohonan polis untuk melanjutkan reman tiga hari lagi di bawah Seksyen 420 Kanun Keseksaan ditolak.</dd></div><div><dt>Apa maksudnya?</dt><dd>Siasatan masih boleh diteruskan tanpa reman. Pelepasan daripada reman bukan NFA dan tidak mengubah pertuduhan SPRM yang telah dibaca pada 9 September.</dd></div></dl><p class="inline-sources"><a href="#s59">S59</a></p></article><article class="trace-card"><div class="trace-head"><span>JEJAK / 10-01</span><time datetime="2026-09-10">10 Sep 2026 · Mahkamah Sesyen Kuala Lumpur</time></div><div class="meta-row"><span class="status fact">DISAHKAN · MAHKAMAH</span><span class="source-grade">Gred B</span></div><h3>Azmi Ahmad didakwa atas dua pertuduhan menipu kadar sewaan harian kapal.</h3><dl><div><dt>Apa jadi?</dt><dd>Azmi mengaku tidak bersalah dan meminta dibicarakan.</dd></div><div><dt>Kenapa penting?</dt><dd>Laporan awal 7 September menjangka 11 September. Rekod mahkamah menunjukkan pertuduhan sebenar dibaca pada 10 September.</dd></div><div><dt>Had</dt><dd>Pertuduhan bukan sabitan.</dd></div></dl><p class="inline-sources"><a href="#s58">S58</a></p></article>'''
        s = s.replace(marker, marker + cards, 1)
    return s


def people(s):
    s = common(s)
    s = s.replace('<span class="status unknown">Bebas reman · 19 Ogos</span></div><h3>Datuk Azmi Ahmad</h3>', '<span class="status process">Didakwa · belum sabit</span></div><h3>Datuk Azmi Ahmad</h3>')
    old = 'Syarikat mengumumkan beliau direman 17 Ogos untuk membantu siasatan SPRM dan dibebaskan 19 Ogos sebelum menyambung tugas. Dua laporan 7 September menamakan beliau sebagai individu yang dijangka didakwa; Malaysia Corporate menyebut 11 September dan dua pertuduhan Seksyen 417 Kanun Keseksaan. Tiada kertas pertuduhan rasmi ditemui setakat data masa semakan.'
    new = 'Didakwa pada 10 September atas dua pertuduhan menipu berkaitan kadar sewaan harian kapal. Beliau mengaku tidak bersalah dan meminta dibicarakan. Laporan awal 7 September menjangka tarikh 11 September; rekod mahkamah menunjukkan pertuduhan sebenar dibaca sehari lebih awal.'
    s = s.replace(old, new)
    s = s.replace('Dua laporan 7 September menamakan beliau sebagai individu yang dijangka didakwa; Malaysia Corporate menyebut 10 September dan Seksyen 23 Akta SPRM, tetapi butiran itu belum disahkan secara rasmi setakat data masa semakan.', 'Beliau didakwa pada 9 September di bawah Seksyen 23(1) Akta SPRM 2009. Dalam trek PDRM berasingan berkaitan hibah 2017, reman beliau tidak disambung pada 10 September; siasatan masih boleh diteruskan.')
    return s


def timeline(s):
    s = common(s)
    if '<time>10 Sep</time><h3>Azmi didakwa</h3>' not in s:
        anchor = '<article><time>7 Sep</time><h3>Laporan jangkaan pendakwaan</h3>'
        i = s.find(anchor)
        if i != -1:
            end = s.find('</article>', i)
            if end != -1:
                end += len('</article>')
                extra = '<article><time>10 Sep</time><h3>Azmi didakwa</h3><p>Azmi Ahmad mengaku tidak bersalah atas dua pertuduhan menipu berkaitan kadar sewaan harian kapal.</p></article><article><time>10 Sep</time><h3>Reman hibah Abdul Azeez tamat</h3><p>Permohonan lanjutan reman ditolak. Siasatan PDRM di bawah Seksyen 420 masih boleh diteruskan tanpa reman.</p></article>'
                s = s[:end] + extra + s[end:]
    return s


def tracks(s):
    s = common(s)
    if 'PDRM · hibah 2017 + AMLA' not in s:
        marker = '<div class="control-grid">'
        card = '<article><h3>PDRM · hibah 2017 + AMLA</h3><p>PDRM menahan lima individu dalam dua trek berasingan: tiga bagi siasatan pembayaran hibah 2017 dan dua lagi di bawah Seksyen 4(1) AMLATFPUAA. Pada 10 September, reman Abdul Azeez dalam trek hibah tidak disambung. Dua individu bagi trek AMLA direman hingga 11 September.</p><p>Siasatan, tahanan dan reman bukan pertuduhan atau sabitan.</p><a href="#s60">S60</a> <a href="#s59">S59</a></article>'
        s = s.replace(marker, marker + card, 1)
    return s


def sources(s):
    s = common(s)
    if 'id="s58"' not in s:
        anchor = '</ol>'
        extra = '<li id="s58"><span>B</span><a href="https://www.bernama.com/bm/jenayah_mahkamah/news.php?id=2605277" rel="noopener noreferrer">Azmi Ahmad didakwa atas dua pertuduhan menipu kadar sewaan kapal</a><small>Bernama · 10 Sep · Mahkamah Sesyen Kuala Lumpur</small></li><li id="s59"><span>B</span><a href="https://www.bernama.com/bm/wilayah/news.php?id=2605390" rel="noopener noreferrer">Reman Abdul Azeez tidak disambung dalam siasatan hibah</a><small>Bernama · 10 Sep · prosiding reman</small></li><li id="s60"><span>B</span><a href="https://www.bernama.com/tv/news.php?id=2605104" rel="noopener noreferrer">Lima ditahan dalam trek hibah dan AMLA</a><small>Bernama · 9 Sep · kenyataan PDRM</small></li>'
        pos = s.rfind(anchor)
        if pos != -1:
            s = s[:pos] + extra + s[pos:]
    s = s.replace('<strong>Maklumat disemak hingga:</strong> 7 September 2026 · lewat malam MYT.', '<strong>Maklumat disemak hingga:</strong> 10 September 2026 · lewat malam MYT.')
    return s

patch('investigations/rci-tabung-haji/updates/index.html', updates)
patch('investigations/rci-tabung-haji/people/index.html', people)
patch('investigations/rci-tabung-haji/timeline/index.html', timeline)
patch('investigations/rci-tabung-haji/tracks/index.html', tracks)
patch('investigations/rci-tabung-haji/sources/index.html', sources)

# Other section pages still expose the shared source ledger. Update cutoff and append new sources there too.
for rel in [
    'investigations/rci-tabung-haji/governance/index.html',
    'investigations/rci-tabung-haji/money/index.html',
    'investigations/rci-tabung-haji/investments/index.html',
    'investigations/rci-tabung-haji/disputed-record/index.html',
]:
    patch(rel, sources)

print('Standalone RCI sections synced through 10 Sep.')
