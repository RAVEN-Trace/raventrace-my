from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CUT = '13 Sep 2026 · deep verification'


def load(rel):
    p = ROOT / rel
    return p, p.read_text(encoding='utf-8')


def write(rel, text):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')


def replace_once(text, old, new, label):
    if new in text:
        return text
    if old not in text:
        raise RuntimeError(f'{label}: anchor not found')
    return text.replace(old, new, 1)


def insert_before(text, marker, block, sentinel, label):
    if sentinel in text:
        return text
    if marker not in text:
        raise RuntimeError(f'{label}: marker not found')
    return text.replace(marker, block + marker, 1)


def replace_article(text, start_marker, new_block, sentinel, label):
    if sentinel in text:
        return text
    start = text.find(start_marker)
    if start < 0:
        raise RuntimeError(f'{label}: start marker not found')
    end = text.find('</article>', start)
    if end < 0:
        raise RuntimeError(f'{label}: article end not found')
    end += len('</article>')
    return text[:start] + new_block + text[end:]


# -----------------------------------------------------------------------------
# Homepage — move the public entry point to the 13 Sep evidence state.
# -----------------------------------------------------------------------------
p, t = load('index.html')
for old, new in [
    ('Raven terakhir semak halaman ini: 12 Sep · 20:44 MYT', 'Raven terakhir semak halaman ini: 13 Sep · deep verification'),
    ('Raven terakhir semak halaman ini: 12 Sep 2026 · 20:44 MYT', 'Raven terakhir semak halaman ini: 13 Sep 2026 · deep verification'),
    ('Status mahkamah disahkan hingga: 11 Sep 2026', 'Status mahkamah disahkan hingga: 13 Sep 2026'),
    ('Semakan terbaru · 12 September · 20:44 MYT', 'Semakan terbaru · 13 September · deep verification'),
]:
    t = t.replace(old, new)

home_lead = '''<article class="home-update-lead" id="home-2026-09-13-deep-verification">
            <div>
              <div class="meta-row"><span class="status disputed">SEMAKAN BUKTI · 13 SEP</span><span>correction release</span></div>
              <h3>Audit kedua ubah lima perkara penting — termasuk dakwaan RM18.6 juta.</h3>
            </div>
            <div class="home-update-copy">
              <p><strong>Empat</strong> individu mempunyai pertuduhan yang benar-benar dibacakan setakat cut-off 13 September, walaupun SPRM pernah menyebut lima. Rekod 2022 pula menunjukkan permohonan pelucuthakan keluarga Azeez ditarik balik; dakwaan viral bahawa RM18m/RM18.6m akhirnya dilucuthakkan kini dinilai <strong>tidak disokong / mengelirukan secara material</strong>. Angka hampir RM13b kekal angka kerugian/beban rasmi — bukan bukti bahawa keseluruhan jumlah itu dicuri.</p>
              <a href="/raventrace-my/news/2026/09/13/deep-verification-rci-th/">Baca semakan 13 Sep →</a>
            </div>
          </article>'''
t = replace_article(t, '<article class="home-update-lead">', home_lead, 'home-2026-09-13-deep-verification', 'home latest lead')
write('index.html', t)


# -----------------------------------------------------------------------------
# Newsroom — 13 Sep becomes the latest editorial state.
# -----------------------------------------------------------------------------
p, t = load('news/index.html')
t = t.replace('Newsroom · semakan terbaru 12 Sep 2026 · 20:44 MYT', 'Newsroom · semakan terbaru 13 Sep 2026 · deep verification')
t = t.replace('Status undang-undang disahkan hingga · 11 Sep 2026 · semakan terbaru 12 Sep 20:44 MYT', 'Status undang-undang disahkan hingga · 13 Sep 2026 · deep verification')
news_item = '''<article id="news-2026-09-13-deep-verification" class="timeline-item" data-topic="report"><time datetime="2026-09-13">13 SEP 2026</time><div><div class="meta-row"><span class="status disputed">DEEP VERIFICATION</span><span class="source-grade">High · source reconciliation</span></div><h3>Lima pembetulan evidence-state: 4 vs 5, RM18.6m, RM13b, RCI chronology dan reman Jamil.</h3><p>Semakan kedua mengekalkan empat sebagai kiraan court-confirmed pada cut-off, tetapi tidak memadam kenyataan SPRM yang menyebut lima. Rekod pelucuthakan 2021–2022 pula mengubah status dakwaan RM18.6m daripada “belum selesai” kepada final-forfeiture claim yang tidak disokong.</p><a href="/raventrace-my/news/2026/09/13/deep-verification-rci-th/">Baca deep verification →</a></div></article>
      '''
t = insert_before(t, '<article id="news-2026-09-12-freshness-sweep"', news_item, 'news-2026-09-13-deep-verification', 'news timeline')
write('news/index.html', t)


# -----------------------------------------------------------------------------
# Preserve the 12 Sep article as historical record, but file a visible correction.
# -----------------------------------------------------------------------------
p, t = load('news/2026/09/12/freshness-sweep-pac-15-sep-rm18m-claim/index.html')
t = t.replace(
    'Semakan 12 September 2026: tiada perubahan baharu yang disahkan pada kiraan pertuduhan RCI TH; PAC Parlimen menjadualkan prosiding TH pada 15 September, sementara dakwaan viral RM18.6 juta kekal belum dibuktikan.',
    'Semakan 12 September 2026 dengan nota editorial 13 September: status mahkamah ketika itu kekal, manakala rekod 2022 kemudian mengukuhkan bahawa dakwaan final forfeiture RM18.6 juta tidak disokong.'
)
t = t.replace(
    'Semakan 12 September mengesahkan checkpoint baharu PAC pada 15 September. Dakwaan viral RM18.6 juta terhadap akaun keluarga Abdul Azeez belum disokong rekod pelucuthakan yang kami temui.',
    'Semakan 12 September dengan kemas kini editorial 13 September: rekod 2022 menunjukkan permohonan pelucuthakan keluarga Azeez telah ditarik balik.'
)
update_note = '''<div class="case-warning light" id="editorial-update-13sep"><strong>EDITORIAL UPDATE · 13 SEP</strong><span>Audit kedua menemui rekod 4 Mac 2022 bahawa kerajaan menarik balik permohonan pelucuthakan hampir RM16 juta milik isteri dan anak-anak Abdul Azeez selepas representasi diterima AGC. Ini mengubah verdict sempit kami: dakwaan bahawa RM18m/RM18.6m <em>akhirnya telah dilucuthakkan</em> tidak disokong dan mengelirukan secara material. Ia tidak membuktikan sumber asal semua wang tersebut.</span></div>
'''
t = insert_before(t, '<h2>Dakwaan viral RM18.6 juta</h2>', update_note, 'editorial-update-13sep', '12 Sep editorial update')
old_verdict = '<p><strong>RAVEN KATA:</strong> <b>BELUM SELESAI.</b> Dalam carian semasa, kami belum menemui perintah pelucuthakan, rekod mahkamah atau kenyataan rasmi agensi yang membuktikan dakwaan viral itu. Penafian peguam juga tidak, dengan sendirinya, membuktikan asal-usul semua wang tersebut. Bukti yang boleh menutup isu ini ialah perintah mahkamah, rekod pelucuthakan, atau dokumen agensi yang boleh diaudit.</p>'
new_verdict = '<p><strong>RAVEN KATA · DIKEMAS KINI 13 SEP:</strong> <b>FINAL FORFEITURE CLAIM TIDAK DISOKONG.</b> Notis 2021 membuktikan permohonan pelucuthakan memang wujud, tetapi rekod 4 Mac 2022 menunjukkan permohonan hampir RM16 juta itu ditarik balik. Penafian peguam pada 2026 ialah kenyataan pihak, namun pada isu sempit “adakah pelucuthakan muktamad berlaku”, ia konsisten dengan sejarah prosiding 2022. Asal-usul setiap ringgit tetap tidak boleh diputuskan daripada rekod ini sahaja.</p>'
t = replace_once(t, old_verdict, new_verdict, '12 Sep RM18.6 verdict')
write('news/2026/09/12/freshness-sweep-pac-15-sep-rm18m-claim/index.html', t)


# -----------------------------------------------------------------------------
# New 13 Sep story page — one question, one clear evidence revision.
# -----------------------------------------------------------------------------
article = '''<!doctype html>
<html lang="ms"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>13 Sep: Lima pembetulan penting selepas deep verification RCI TH | RAVEN-Trace</title>
<meta name="description" content="Deep verification 13 September 2026 untuk RCI Tabung Haji: kiraan 4 vs 5, RM18.6m, RM13b, kronologi RCI dan reman Jamil Khir diperketat mengikut rekod.">
<link rel="canonical" href="https://raven-trace.github.io/raventrace-my/news/2026/09/13/deep-verification-rci-th/">
<meta property="og:type" content="article"><meta property="og:site_name" content="RAVEN-Trace Malaysia"><meta property="og:title" content="13 Sep: Lima pembetulan penting selepas deep verification RCI TH"><meta property="og:description" content="Apa yang berubah selepas audit kedua — dan apa yang masih belum boleh dipastikan."><meta property="og:url" content="https://raven-trace.github.io/raventrace-my/news/2026/09/13/deep-verification-rci-th/"><meta property="og:image" content="https://raven-trace.github.io/raventrace-my/assets/og/rci-tabung-haji-share-v8.jpg"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="https://raven-trace.github.io/raventrace-my/assets/og/rci-tabung-haji-share-v8.jpg">
<link rel="stylesheet" href="/raventrace-my/assets/css/raven.css?v=3.0.0"><link rel="stylesheet" href="/raventrace-my/assets/css/raven-publication.css?v=2.0.0"><script async src="https://lytcdn.com/lyt.js?site=7d23381ee4e5"></script><link rel="stylesheet" href="/raventrace-my/assets/css/raven-v5.css?v=5.0.0" data-raven-v5-static><link rel="stylesheet" href="/raventrace-my/assets/css/raven-signal-v6.css?v=6.0.0" data-raven-signal-v6><link rel="stylesheet" href="/raventrace-my/assets/css/raven-unified-v7.css?v=7.0.5" data-raven-unified><link rel="stylesheet" href="/raventrace-my/assets/css/raven-funnel-v1.css?v=1.2.1" data-raven-funnel-v1>
</head><body><a class="skip-link" href="#main">Terus ke kandungan</a>
<header class="site-header"><div class="masthead"><a class="brand" href="/raventrace-my/"><span><span class="brand-name">RAVEN<em>-Trace</em></span><span class="brand-sub">Bebas · Berasaskan bukti · Malaysia</span></span></a><p class="masthead-note">Bukti dahulu.<br>Kesimpulan kemudian.</p></div><div class="nav-row"><div class="nav-wrap"><nav class="site-nav"><a href="/raventrace-my/">Utama</a><a aria-current="page" href="/raventrace-my/news/">Newsroom</a><a href="/raventrace-my/investigations/">Siasatan</a><a class="narrative-nav-link" href="/raventrace-my/investigations/rci-tabung-haji/narratives/">Audit Naratif</a><a href="/raventrace-my/methodology/">Metodologi</a></nav></div></div></header>
<main id="main"><section class="story-hero"><div class="container"><p class="story-kicker">RCI Tabung Haji · Deep verification · 13 September</p><div class="meta-row"><span class="status disputed">CORRECTION RELEASE</span><span class="source-grade">High confidence · evidence reconciliation</span></div><h1>Lima benda yang Raven ubah selepas audit kedua.</h1><p class="lede">Bukan semua perkembangan baharu ialah berita baharu. Kadang-kadang perkara paling penting ialah membetulkan kategori, tarikh dan kesimpulan yang terlalu jauh daripada bukti.</p><p class="date-chip">Cut-off bukti · 13 Sep 2026</p></div></section>
<section class="section paper"><div class="container story-body">
<div class="case-warning light"><strong>LEGAL BOUNDARY</strong><span>Direman ≠ didakwa. Didakwa ≠ disabitkan. Dapatan RCI ≠ sabitan jenayah. Bila sumber summary bercanggah dengan status prosiding, Raven utamakan rekod mahkamah yang boleh diperiksa.</span></div>
<h2>1 · Empat court-confirmed, lima agency-stated</h2><p><strong>FAKTA:</strong> Setakat cut-off 13 September, Raven boleh mengesahkan empat individu mempunyai pertuduhan yang benar-benar dibacakan. Pada 10 September, Ketua Pesuruhjaya SPRM menyebut lima. Bekas COO Adi Azuan Abdul Ghani pula mempunyai prosiding yang ditangguhkan ke 24 September kerana rawatan kesihatan.</p><p><strong>VERDICT:</strong> Jangan padam percanggahan. Paparkan kedua-duanya: <b>4 court-confirmed</b> dan <b>5 agency-stated</b>, dengan penjelasan kenapa counter undang-undang menggunakan empat.</p>
<h2>2 · RM18m/RM18.6m: warta permohonan bukan pelucuthakan muktamad</h2><p><strong>FAKTA:</strong> Notis 2021 menunjukkan permohonan pelucuthakan terhadap akaun isteri dan empat anak Abdul Azeez. Jumlah akaun TH yang disenaraikan sekitar RM13.337 juta. Pada 4 Mac 2022, kerajaan menarik balik permohonan pelucuthakan hampir RM16 juta selepas representasi diterima AGC.</p><p><strong>VERDICT:</strong> Dakwaan viral bahawa RM18m/RM18.6m <em>akhirnya telah dilucuthakkan</em> tidak disokong dan mengelirukan secara material. Rekod itu tidak, dengan sendiri, menentukan sumber asal semua wang.</p>
<h2>3 · Hampir RM13b ialah angka kerugian/beban — bukan shorthand “RM13b dicuri”</h2><p><strong>FAKTA:</strong> Angka rasmi hampir RM13b merangkumi kira-kira RM10.2b beban kerajaan melalui penyelamatan UJSB dan RM2.6b rosot nilai yang ditanggung TH bagi pelaburan yang masih diurus.</p><p><strong>NARRATIVE GAP:</strong> Kerugian, impairment, transaksi bermasalah dan kecurian ialah kategori berbeza. Bukti jenayah perlu dipadankan kepada transaksi dan individu secara spesifik.</p>
<h2>4 · RCI selesai pada 19 Julai 2022 — kemudian melalui beberapa checkpoint</h2><p><strong>KRONOLOGI:</strong> 19 Julai 2022 — suruhanjaya selesai siasatan/kerja. 30 Ogos — laporan dipersembahkan kepada Yang di-Pertuan Agong. 14 Disember — dibentang kepada Kabinet. 29 Julai 2026 — kerajaan mengarahkan laporan diterbitkan dan dibuka kepada awam.</p>
<h2>5 · Jamil Khir: 1 Sep ditahan, 5 hari reman + 2 hari lanjutan</h2><p><strong>FAKTA:</strong> Jamil Khir ditahan sekitar petang 1 September selepas hadir memberi keterangan. Mahkamah membenarkan reman lima hari bermula 2 September, kemudian reman dilanjutkan dua hari. Beliau dibebaskan dengan jaminan SPRM pada 8 September.</p><p><strong>STATUS SETAKAT CUT-OFF:</strong> Pendakwaan 14 September telah diumumkan/dijadualkan, tetapi Raven tidak menukar status kepada “didakwa” sehingga pertuduhan sebenar dibacakan.</p>
<h2>Politik: dua claim wujud; motive masih tidak terbukti</h2><p><strong>DISPUTED / UNKNOWN:</strong> Pemimpin UMNO mendakwa wujud intimidasi atau penggunaan institusi sebagai alat politik. Pada 13 September, jurucakap kerajaan Fahmi Fadzil menafikannya dan menegaskan tiada campur tangan. Kedua-dua kenyataan membuktikan pertarungan naratif wujud; kedua-duanya tidak cukup untuk membuktikan motif sebenar penguatkuasaan.</p>
<h2>Apa yang Raven tak akan simpulkan</h2><p>Kami tidak akan menulis “RM13b dicuri”, “lima orang sudah didakwa” atau “kerajaan pasti menggunakan pendakwaan sebagai senjata” tanpa bukti yang sepadan dengan dakwaan tersebut. Jika bukti lebih kuat muncul, status akan berubah dan perubahan itu akan direkodkan.</p>
<p><a href="https://www.parlimen.gov.my/files/jindex/pdf/JDR22052023.pdf" rel="noopener noreferrer">Parlimen · kronologi RCI 2022 →</a></p>
<p><a href="https://www.mof.gov.my/portal/ms/berita/akhbar/th-catat-kerugian-rm13-bilion-daripada-14-pelaburan-tujuh-rugi-100-peratus-amir-hamzah" rel="noopener noreferrer">MOF · pecahan hampir RM13b →</a></p>
<p><a href="https://www.freemalaysiatoday.com/category/nation/2022/03/04/prosecution-withdraws-bid-to-forfeit-rm16mil-from-azeezs-family" rel="noopener noreferrer">FMT · permohonan pelucuthakan ditarik balik · 4 Mac 2022 →</a></p>
<p><a href="https://rebuild.freemalaysiatoday.com/category/nation/2026/09/13/fahmi-denies-unity-govt-using-courts-enforcement-agencies-to-threaten-umno-leaders" rel="noopener noreferrer">FMT · denial kerajaan + counter-claim UMNO · 13 Sep →</a></p>
<p><a href="/raventrace-my/investigations/rci-tabung-haji/">Buka CASEFILE penuh →</a> · <a href="/raventrace-my/corrections/">Lihat rekod pembetulan →</a></p>
</div></section>
</main>
<footer class="site-footer"><div class="container footer-grid"><div><div class="footer-brand">RAVEN<em>-Trace</em>™</div><p class="motto">A lie wins by speed. Truth wins by audit.</p></div><p class="legal">RAVEN-Trace™ by SharulR X(ai) Projects. Semua individu dianggap tidak bersalah melainkan disabitkan oleh mahkamah.</p></div></footer><script src="/raventrace-my/assets/js/raven-v5.js?v=5.1.2" defer data-raven-v5-static></script><script src="/raventrace-my/assets/js/raven-signal-v6.js?v=6.0.0" defer data-raven-signal-v6></script><script src="/raventrace-my/assets/js/raven-funnel-v1.js?v=1.2.1" defer data-raven-funnel-v1></script>
</body></html>'''
write('news/2026/09/13/deep-verification-rci-th/index.html', article)


# -----------------------------------------------------------------------------
# Investigation desk — sitewide status must not lag behind the CASEFILE.
# -----------------------------------------------------------------------------
p, t = load('investigations/index.html')
t = t.replace('disemak hingga 11 September 2026', 'disemak hingga 13 September 2026')
t = t.replace('Meja Siasatan · Malaysia · disemak hingga 11 Sep 2026 · 23:37 MYT', 'Meja Siasatan · Malaysia · disemak hingga 13 Sep 2026 · deep verification')
t = t.replace('Maklumat disemak hingga · 11 Sep 2026 · 23:37 MYT', 'Maklumat disemak hingga · 13 Sep 2026 · deep verification')
t = t.replace('Apa yang sudah disahkan setakat 11 September?', 'Apa yang sudah disahkan setakat 13 September?')
old_latest = '<section class="investigation-side-card"><h2>Perkembangan terbaru</h2><p><strong>11 Sep:</strong> rekod awam tidak seragam tentang jumlah individu yang telah didakwa — kronologi mahkamah menunjukkan empat, manakala SPRM menyebut lima.</p><p><a href="/raventrace-my/news/2026/09/11/empat-atau-lima-didakwa-rekod-tidak-seragam/">Baca audit 4 lawan 5 →</a></p></section>'
new_latest = '<section class="investigation-side-card"><h2>Perkembangan terbaru</h2><p><strong>13 Sep:</strong> deep verification mengekalkan empat sebagai kiraan court-confirmed, sambil merekod kenyataan SPRM yang menyebut lima. Audit sama juga mengubah status dakwaan RM18.6m: permohonan pelucuthakan keluarga ditarik balik pada 2022, jadi final-forfeiture claim tidak disokong.</p><p><a href="/raventrace-my/news/2026/09/13/deep-verification-rci-th/">Baca deep verification →</a></p></section>'
t = replace_once(t, old_latest, new_latest, 'investigation desk latest')
write('investigations/index.html', t)


# -----------------------------------------------------------------------------
# Standalone RCI subpages — sync freshness and add the missing evidence boundary.
# -----------------------------------------------------------------------------
# Governance
p, t = load('investigations/rci-tabung-haji/governance/index.html')
t = t.replace('Maklumat disemak hingga · 11 Sep 2026 · 23:37 MYT', f'Maklumat disemak hingga · {CUT}')
gov_card = '''<article id="governance-recovery-accountability"><h3>13 Sep · pemulihan kewangan ≠ akauntabiliti selesai</h3><p>TH melaporkan agihan keuntungan FY2025 sebanyak 3.50%, aset RM98.58b dan liabiliti RM95.63b. Indikator kewangan yang lebih kukuh tidak membuktikan semua isu tadbir urus atau akauntabiliti sejarah telah selesai. Raven mengekalkan dua trek berasingan: <strong>recovery</strong> dan <strong>accountability</strong>.</p><a href="https://www.tabunghaji.gov.my/bm/siaran-media/haji/tabung-haji-catat-prestasi-terbaik-dalam-lapan-tahun" rel="noopener noreferrer">Tabung Haji · FY2025</a></article>'''
t = insert_before(t, '<article><h3>11 Sep · pembaharuan operasi haji</h3>', gov_card, 'governance-recovery-accountability', 'governance recovery card')
write('investigations/rci-tabung-haji/governance/index.html', t)

# Investments
p, t = load('investigations/rci-tabung-haji/investments/index.html')
t = t.replace('Maklumat disemak hingga · 10 Sep 2026 · lewat malam MYT', f'Maklumat disemak hingga · {CUT}')
inv_note = '''<div class="case-warning light" id="rm13b-category-lock"><strong>NARRATIVE GAP · RM13b bukan satu kategori jenayah</strong><span>Angka rasmi hampir RM13b menggabungkan kira-kira RM10.2b beban kerajaan melalui penyelamatan UJSB dan RM2.6b rosot nilai yang ditanggung TH. Kerugian / bailout / impairment tidak boleh ditukar terus menjadi “RM13b dicuri” tanpa bukti transaksi jenayah spesifik.</span></div>
'''
t = insert_before(t, '<div class="investment-list" data-investment-list>', inv_note, 'rm13b-category-lock', 'investments RM13b note')
write('investigations/rci-tabung-haji/investments/index.html', t)

# Tracks
p, t = load('investigations/rci-tabung-haji/tracks/index.html')
t = t.replace('Maklumat disemak hingga · 11 Sep 2026 · 23:37 MYT', f'Maklumat disemak hingga · {CUT}')
track_note = '''<div class="case-warning light" id="track-count-lock"><strong>COUNT LOCK · 13 SEP</strong><span>Empat individu mempunyai pertuduhan yang dibacakan setakat cut-off. SPRM pernah menyebut lima, tetapi prosiding Adi Azuan dilaporkan ditangguhkan ke 24 September. Raven memaparkan kedua-dua rekod dan menggunakan empat untuk counter mahkamah.</span></div>
'''
t = insert_before(t, '<div class="control-grid">', track_note, 'track-count-lock', 'tracks count lock')
write('investigations/rci-tabung-haji/tracks/index.html', t)

# Disputed record
p, t = load('investigations/rci-tabung-haji/disputed-record/index.html')
t = t.replace('Maklumat disemak hingga · 10 Sep 2026 · lewat malam MYT', f'Maklumat disemak hingga · {CUT}')
t = t.replace('Madinah Mohamad vs Rashid Hussain: apa yang disokong rekod, dan apa yang masih dipertikaikan.', 'Rekod bercanggah: kiraan pertuduhan dan keterangan RCI perlu dipisahkan mengikut jenis bukti.')
dispute_note = '''<div class="case-warning light" id="charged-count-dispute"><strong>REKOD TAK SEPADAN · 4 vs 5</strong><span>Kronologi mahkamah yang disemak menyokong empat individu dengan pertuduhan dibacakan. Ketua Pesuruhjaya SPRM pula menyebut lima pada 10 September. Kerana pertuduhan bekas COO dilaporkan ditangguhkan ke 24 September, Raven mengekalkan percanggahan ini sebagai <strong>DIPERTIKAIKAN</strong> dan tidak menganggap aggregate count mengatasi status prosiding.</span></div>
'''
t = insert_before(t, '<div class="control-grid">', dispute_note, 'charged-count-dispute', 'disputed count block')
write('investigations/rci-tabung-haji/disputed-record/index.html', t)


# -----------------------------------------------------------------------------
# Political/social narrative page — record both claim and counter-claim.
# -----------------------------------------------------------------------------
p, t = load('investigations/rci-tabung-haji/narratives/political-social-media/index.html')
t = t.replace('Naratif disemak hingga · 13 Sep 2026 · 01:00 MYT', 'Naratif disemak hingga · 13 Sep 2026 · deep verification')
response = '''<div class="case-warning light" id="gov-response-13sep"><strong>13 Sep · jawapan kerajaan</strong><span>Jurucakap kerajaan Fahmi Fadzil menafikan mahkamah atau agensi penguatkuasaan digunakan untuk mengugut pemimpin UMNO dan berkata pentadbiran tidak campur tangan dalam siasatan. Ini mengesahkan wujudnya <em>counter-claim</em>; ia bukan bukti bebas bahawa proses benar-benar bebas daripada campur tangan.</span></div>'''
t = insert_before(t, '<div class="case-warning light"><strong>Apa yang belum terbukti?</strong>', response, 'gov-response-13sep', 'political counter-claim')
old_politics = '<p><b>Raven kata macam mana?</b> <strong>DAKWAAN · POSISI POLITIK.</strong> Kita boleh sahkan dakwaan “political intimidation” itu memang dibuat. Setakat bukti awam yang Raven semak, belum ada bukti yang menunjukkan penguatkuasaan dalam kes RCI TH dikawal secara politik.</p>'
new_politics = '<p><b>Raven kata macam mana?</b> <strong>DISPUTED / UNKNOWN.</strong> Kita boleh sahkan dakwaan “political intimidation” dibuat dan kerajaan menafikannya. Setakat bukti awam yang Raven semak, timing politik sahaja tidak membuktikan arahan politik; official denial pula tidak membuktikan secara bebas bahawa tiada campur tangan. Motif sebenar kekal belum dipastikan.</p>'
t = replace_once(t, old_politics, new_politics, 'political verdict')
write('investigations/rci-tabung-haji/narratives/political-social-media/index.html', t)


# -----------------------------------------------------------------------------
# Corrections — publish the correction release instead of silently mutating copy.
# -----------------------------------------------------------------------------
p, t = load('corrections/index.html')
t = t.replace('<span class="date-chip">11 Sep 2026 · 23:37 MYT</span>', '<span class="date-chip">13 Sep 2026 · deep verification</span>')
t = t.replace('Rekod perubahan material dikemas kini hingga 11 September.', 'Rekod perubahan material dikemas kini hingga 13 September.')
t = t.replace('Rekod ini kini merangkumi perubahan status mahkamah, percanggahan kiraan pertuduhan, pembetulan unit kiraan dan pembaikan integriti runtime CASEFILE.', 'Rekod ini kini merangkumi deep verification 13 September: status mahkamah, kronologi RCI, reman Jamil Khir, kategori RM13b dan pembetulan dakwaan final forfeiture RM18m/RM18.6m.')
corrections = '''      <h2 style="margin-top:3rem" id="revision-13sep">Revisi 13 September 2026</h2><div class="timeline" style="margin-top:1.5rem">
        <article class="timeline-item"><time datetime="2026-09-13">13 SEP 2026</time><div><div class="meta-row"><span class="status disputed">Pembetulan material</span></div><h3>RM18m/RM18.6m: daripada “belum selesai” kepada final-forfeiture claim tidak disokong</h3><p><strong>Dulu:</strong> Raven belum menemui perintah pelucuthakan dan mengekalkan isu sebagai belum selesai. <strong>Apa berubah:</strong> rekod 4 Mac 2022 menunjukkan kerajaan menarik balik permohonan pelucuthakan hampir RM16 juta milik isteri dan anak-anak Abdul Azeez. <strong>Kenapa:</strong> permohonan pelucuthakan tidak sama dengan pelucuthakan muktamad.</p></div></article>
        <article class="timeline-item"><time datetime="2026-09-13">13 SEP 2026</time><div><div class="meta-row"><span class="status disputed">Reconciliation</span></div><h3>4 vs 5: Raven kekalkan percanggahan, tetapi counter mahkamah menggunakan empat</h3><p><strong>Dulu:</strong> angka empat dan lima dipaparkan sebagai konflik tanpa adjudication rule yang cukup jelas. <strong>Apa berubah:</strong> court-observed status diberi keutamaan untuk counter undang-undang; kenyataan SPRM yang menyebut lima tetap dipelihara sebagai agency-stated record. <strong>Kenapa:</strong> prosiding bekas COO dilaporkan ditangguhkan ke 24 September.</p></div></article>
        <article class="timeline-item"><time datetime="2026-09-13">13 SEP 2026</time><div><div class="meta-row"><span class="status context">Pembetulan kronologi</span></div><h3>RCI: 19 Jul → 30 Ogos → 14 Dis 2022 → 29 Jul 2026</h3><p>Suruhanjaya menyelesaikan kerja pada 19 Julai 2022, laporan dipersembahkan kepada Yang di-Pertuan Agong pada 30 Ogos, dibentang kepada Kabinet pada 14 Disember, dan dibuka kepada awam pada 29 Julai 2026. Ini menggantikan shorthand “siap Mei 2022”.</p></div></article>
        <article class="timeline-item"><time datetime="2026-09-13">13 SEP 2026</time><div><div class="meta-row"><span class="status context">Pembetulan proses</span></div><h3>Jamil Khir: tahan 1 Sep, reman 5 hari, lanjutan 2 hari</h3><p>Chronology diperketat: ditahan sekitar petang 1 September; reman lima hari bermula 2 September; dilanjutkan dua hari; dibebaskan dengan jaminan SPRM pada 8 September. “Reman tujuh hari” terlalu memampatkan dua perintah berasingan.</p></div></article>
      </div>

'''
t = insert_before(t, '      <h2 style="margin-top:3rem">Revisi 8–11 September 2026</h2>', corrections, 'revision-13sep', 'corrections 13 Sep')
write('corrections/index.html', t)


# -----------------------------------------------------------------------------
# Production evidence lock — internal state must match public state.
# -----------------------------------------------------------------------------
p, t = load('docs/PRODUCTION_INTEGRITY_LOCK.md')
if '## Current evidence boundary' in t:
    start = t.find('## Current evidence boundary')
    next_heading = t.find('\n## ', start + 5)
    if next_heading < 0:
        next_heading = len(t)
    new_boundary = '''## Current evidence boundary

- Cut-off for this lock: **13 September 2026 deep verification**.
- Court-confirmed charge-reading count: **4 individuals**. MACC/SPRM separately stated **5**; the former COO charge-reading was reported postponed to 24 September. Preserve this as a source conflict rather than flattening it.
- The viral claim that RM18m/RM18.6m in family TH accounts was finally forfeited is **unsupported / materially misleading**: a 2021 forfeiture application existed, but the government withdrew the application in March 2022.
- The official nearly-RM13b figure is a loss/burden construct (~RM10.2b government/UJSB + RM2.6b TH impairment), not proof that RM13b was stolen.
- RCI process chronology: work completed 19 Jul 2022; report to Yang di-Pertuan Agong 30 Aug; Cabinet 14 Dec; public release 29 Jul 2026.
- Political weaponisation vs government-independence claims remain **DISPUTED / UNKNOWN** absent decision-chain evidence.
- Financial recovery indicators and historical accountability are separate tracks.
'''
    t = t[:start] + new_boundary + t[next_heading:]
write('docs/PRODUCTION_INTEGRITY_LOCK.md', t)

print('13 SEP SITEWIDE SYNC V2: generated')
