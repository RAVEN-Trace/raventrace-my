from pathlib import Path

CUT='11 Sep 2026 · 23:37 MYT'
BERNAMA_COUNT='https://www.bernama.com/en/news.php?id=2605735'
BERNAMA_MACC='https://www.bernama.com/en/news.php?id=2605582'
BERNAMA_HAJ='https://majujohor.bernama.com/news-en.php?id=2605960'
RTM_GOV='https://berita.rtm.gov.my/nasional/senarai-berita-nasional/senarai-artikel/pengekalan-kos-haji-muassasah-satu-pencapaian-th-zulkifli/'
RAVEN_COUNT='/raventrace-my/news/2026/09/11/empat-atau-lima-didakwa-rekod-tidak-seragam/'


def read(path):
    return Path(path).read_text()

def write(path, text):
    Path(path).write_text(text)

def replace_required(text, old, new, label):
    if old not in text:
        raise SystemExit(f'{label}: expected text not found: {old[:120]}')
    return text.replace(old, new, 1)

def cutoff10_to11(s):
    return (s.replace('Maklumat disemak hingga · 10 Sep 2026 · lewat malam MYT', f'Maklumat disemak hingga · {CUT}')
             .replace('Maklumat disemak hingga · 10 Sep 2026', f'Maklumat disemak hingga · {CUT}')
             .replace('disemak hingga 10 September 2026', 'disemak hingga 11 September 2026')
             .replace('Disemak hingga 10 September 2026', 'Disemak hingga 11 September 2026'))

# ------------------------------------------------------------------
# 1) HOMEPAGE — bring front door from 9 Sep to 11 Sep.
# ------------------------------------------------------------------
p='index.html'; s=read(p)
s=s.replace('9 September 2026 · disemak 18:29 MYT', '11 September 2026 · disemak 23:37 MYT')
s=s.replace('Maklumat disemak hingga · 9 Sep 2026 · 18:29 MYT', f'Maklumat disemak hingga · {CUT}')
s=s.replace('Kemas kini bukti · disemak hingga 9 September · 18:29 MYT', 'Kemas kini bukti · disemak hingga 11 September · 23:37 MYT')
s=s.replace('Setakat 9 September, tiga individu telah didakwa dalam tindakan susulan berkaitan RCI.', 'Setakat rekod mahkamah yang disemak pada 11 September, empat individu telah berdepan pertuduhan yang dibacakan. SPRM pula menyebut lima dalam kiraannya; perbezaan itu masih belum dijelaskan.')
s=s.replace('<strong>03</strong><span>individu didakwa setakat 9 Sep · belum sabit</span>', '<strong>04</strong><span>pertuduhan telah dibacakan kepada empat individu setakat rekod mahkamah 10 Sep · SPRM menyebut lima</span>')
lead='''<article id="home-2026-09-11-count-discrepancy" class="update-card lead-update"><div class="update-index">00</div><div class="meta-row"><span class="status disputed">DIPERTIKAIKAN · REKOD</span><time datetime="2026-09-11">11 Sep 2026</time></div><h3>Empat atau lima telah didakwa? Dua rekod awam tidak seragam.</h3><p>Chronology Bernama menyatakan empat individu telah didakwa di mahkamah. Dalam sidang media berasingan, Ketua Pesuruhjaya SPRM menyebut lima dan memasukkan bekas COO TH yang prosiding pertuduhannya dilaporkan ditangguhkan ke 24 September. Raven tidak menaikkan kiraan kepada lima tanpa rekonsiliasi rekod.</p><a href="'''+RAVEN_COUNT+'''">Baca siasatan Raven →</a></article>'''
marker='<div class="update-grid">'
if 'home-2026-09-11-count-discrepancy' not in s:
    s=s.replace(marker, marker+'\n      '+lead, 1)
# Renumber previous lead index to avoid duplicate visual 00.
s=s.replace('<article id="home-2026-09-09-azeez-charged" class="update-card lead-update"><div class="update-index">00</div>', '<article id="home-2026-09-09-azeez-charged" class="update-card lead-update"><div class="update-index">01</div>')
write(p,s)

# ------------------------------------------------------------------
# 2) INVESTIGATIONS DESK — current state and future checkpoints.
# ------------------------------------------------------------------
p='investigations/index.html'; s=read(p)
s=s.replace('disemak hingga 10 September 2026', 'disemak hingga 11 September 2026')
s=s.replace('Meja Siasatan · Malaysia · disemak hingga 10 Sep 2026 · lewat malam MYT', f'Meja Siasatan · Malaysia · disemak hingga {CUT}')
s=s.replace('Maklumat disemak hingga · 10 Sep 2026 · lewat malam MYT', f'Maklumat disemak hingga · {CUT}')
s=s.replace('Setakat 10 September, empat individu telah didakwa dalam tindakan susulan berkaitan RCI.', 'Setakat rekod mahkamah yang disemak, empat individu telah berdepan pertuduhan yang dibacakan; SPRM menyebut lima dalam kiraannya. Perbezaan itu belum diselesaikan.')
s=s.replace('<b>Mahkamah</b><span>4 individu didakwa setakat 10 Sep · belum sabit</span>', '<b>Mahkamah</b><span>4 pertuduhan dibacakan · kiraan SPRM: 5 · rekod belum seragam</span>')
old='<aside class="investigation-side"><section class="investigation-side-card"><h2>Perkembangan terbaru</h2><p><strong>10 Sep:</strong> Azmi Ahmad didakwa atas dua pertuduhan menipu kadar sewaan harian kapal dan mengaku tidak bersalah.</p><p><a href="/raventrace-my/news/2026/09/10/azmi-ahmad-didakwa/">Baca perkembangan →</a></p></section>'
new='<aside class="investigation-side"><section class="investigation-side-card"><h2>Perkembangan terbaru</h2><p><strong>11 Sep:</strong> rekod awam tidak seragam tentang jumlah individu yang telah didakwa — chronology mahkamah menunjukkan empat, manakala SPRM menyebut lima.</p><p><a href="'+RAVEN_COUNT+'">Baca audit 4 lawan 5 →</a></p></section><section class="investigation-side-card"><h2>Checkpoint seterusnya</h2><p><strong>14 Sep:</strong> SPRM mengesahkan seorang bekas menteri akan didakwa dengan tiga pertuduhan dicadangkan di bawah Seksyen 403 Kanun Keseksaan berkaitan aset di Arab Saudi. Raven menunggu pertuduhan dibacakan sebelum mengubah status kepada “didakwa”.</p><p><a href="'+BERNAMA_MACC+'" rel="noopener noreferrer">Sumber: Bernama →</a></p></section>'
s=s.replace(old,new)
s=s.replace('Apa yang sudah disahkan setakat 10 September?', 'Apa yang sudah disahkan setakat 11 September?')
s=s.replace('<h3>Tarikh 11 dan 17 September kekal dakwaan yang perlu disemak — bukan fakta.</h3>', '<h3>14 September kini checkpoint rasmi; 24 September kekal checkpoint Adi Azuan.</h3>')
s=s.replace('Laporan', 'Laporan', 1)
write(p,s)

# ------------------------------------------------------------------
# 3) MAIN CASEFILE — preserve 4 as court-record count, expose discrepancy.
# ------------------------------------------------------------------
p='investigations/rci-tabung-haji/index.html'; s=read(p)
s=s.replace('dengan perkembangan disemak hingga 10 September 2026.', 'dengan perkembangan disemak hingga 11 September 2026.')
s=s.replace('SIASATAN · RCI-TH-2026 · dikemas kini 10 Sep', 'SIASATAN · RCI-TH-2026 · dikemas kini 11 Sep')
s=s.replace('Maklumat disemak hingga · 10 Sep 2026 · lewat malam MYT', f'Maklumat disemak hingga · {CUT}')
s=s.replace('Kemas kini semasa · 10 Sep 2026', 'Kemas kini semasa · 11 Sep 2026')
s=s.replace('<div><dt>04</dt><dd>individu didakwa setakat 10 Sep · belum sabit</dd></div>', '<div><dt>04</dt><dd>pertuduhan dibacakan setakat chronology mahkamah · SPRM menyebut 05</dd></div>')
s=s.replace('Setakat 10 September, empat individu telah didakwa dalam tindakan susulan berkaitan RCI dan semuanya belum disabitkan.', 'Setakat chronology mahkamah yang disemak, empat individu telah berdepan pertuduhan yang dibacakan dan semuanya belum disabitkan. Dalam kenyataan berasingan, SPRM menyebut lima individu telah didakwa; perbezaan itu masih belum dijelaskan.')
s=s.replace('<article><b>04</b><h3>Empat individu kini telah didakwa.</h3><p>Setakat 10 September, empat individu telah didakwa dan semuanya mengaku tidak bersalah. Pertuduhan yang telah dibaca masih perlu diuji di mahkamah.</p></article>', '<article><b>04</b><h3>Kiraan semasa tidak seragam: empat dalam chronology mahkamah, lima menurut SPRM.</h3><p>Raven mengekalkan angka empat bagi pertuduhan yang dapat disahkan telah dibacakan. Bekas COO TH masih mempunyai prosiding yang dilaporkan ditangguhkan ke 24 September. Pertuduhan bukan sabitan.</p></article>')
stack='<div class="trace-stack">'
card='''<article class="trace-card"><div class="trace-head"><span>JEJAK / 11-01</span><time datetime="2026-09-11">11 Sep 2026 · audit rekod awam</time></div><div class="meta-row"><span class="status disputed">DIPERTIKAIKAN · REKOD</span><span class="source-grade">Gred B</span></div><h3>Empat atau lima telah didakwa? Rekod awam tidak seragam.</h3><dl><div><dt>Rekod mahkamah</dt><dd>Chronology Bernama pada 10 September menyatakan empat individu telah didakwa di mahkamah.</dd></div><div><dt>Kenyataan SPRM</dt><dd>Ketua Pesuruhjaya SPRM menyebut lima individu, termasuk bekas COO TH yang prosidingnya dilaporkan ditangguhkan ke 24 September.</dd></div><div><dt>Keputusan Raven</dt><dd>Gunakan empat sebagai bilangan pertuduhan yang dapat disahkan telah dibacakan; tandakan lima sebagai kiraan agensi yang belum direkonsiliasi.</dd></div></dl><p class="inline-sources"><a href="'''+RAVEN_COUNT+'''">Audit Raven</a> · <a href="'''+BERNAMA_COUNT+'''" rel="noopener noreferrer">Chronology Bernama</a> · <a href="'''+BERNAMA_MACC+'''" rel="noopener noreferrer">Kenyataan SPRM</a></p></article>'''
if 'JEJAK / 11-01' not in s:
    s=s.replace(stack, stack+'\n            '+card,1)
# Resolve stale unknown question on Jamil, if present.
s=s.replace('Adakah Jamil Khir akan didakwa seperti dilaporkan pada 17 September, dan jika ya di bawah seksyen apa?', 'Apakah butiran tepat pertuduhan terhadap bekas menteri pada 14 September, termasuk fakta transaksi, nilai harta dan hubungan tepat dengan aset di Arab Saudi?')
write(p,s)

# ------------------------------------------------------------------
# 4) PEOPLE — fix stale badges and Jamil checkpoint.
# ------------------------------------------------------------------
p='investigations/rci-tabung-haji/people/index.html'; s=cutoff10_to11(read(p))
s=s.replace('<span class="status unknown">Bebas reman · 1 Sep</span></div><h3>Datuk Seri Abdul Azeez Abdul Rahim</h3>', '<span class="status process">Didakwa · belum sabit</span></div><h3>Datuk Seri Abdul Azeez Abdul Rahim</h3>')
old='<article class="person-card"><div><span>03</span><span class="status process">Reman disambung · hingga 8 Sep</span></div><h3>Datuk Seri Jamil Khir Baharom</h3><p class="role">Menteri di JPM (Hal Ehwal Agama) · 2009–2018</p><p>Selepas reman lima hari bermula 2 September, Mahkamah Majistret Putrajaya membenarkan sambungan dua hari dari 7 hingga 8 September. SPRM menyatakan kes disiasat di bawah Seksyen 16(a)(A) Akta SPRM 2009. Dua laporan 7 September menamakan beliau dalam jangkaan pendakwaan; Malaysia Corporate menyebut 17 September dan Seksyen 403 Kanun Keseksaan. Perbezaan dengan seksyen siasatan rasmi hanya boleh dikunci apabila rekod pertuduhan rasmi tersedia.</p><a href="#s22">S22</a> <a href="#s49">S49</a></article>'
new='<article class="person-card"><div><span>03</span><span class="status process">Tindakan mahkamah dijadual · 14 Sep</span></div><h3>Datuk Seri Jamil Khir Baharom</h3><p class="role">Menteri di JPM (Hal Ehwal Agama) · 2009–2018</p><p>SPRM mengesahkan seorang bekas menteri akan didakwa pada 14 September dengan tiga pertuduhan dicadangkan di bawah Seksyen 403 Kanun Keseksaan berkaitan aset di Arab Saudi. Beberapa media mengenal pasti individu itu sebagai Jamil Khir Baharom. Raven mengekalkan status sebagai notis pendakwaan sehingga pertuduhan benar-benar dibacakan di mahkamah.</p><a href="'+BERNAMA_MACC+'" rel="noopener noreferrer">Bernama · 10 Sep</a></article>'
if old in s: s=s.replace(old,new,1)
else: raise SystemExit('people: stale Jamil card not found')
write(p,s)

# ------------------------------------------------------------------
# 5) TIMELINE — append official prosecution notice + record discrepancy.
# ------------------------------------------------------------------
p='investigations/rci-tabung-haji/timeline/index.html'; s=cutoff10_to11(read(p))
needle='<article><time>10 Sep</time><h3>Reman hibah Abdul Azeez tamat</h3><p>Permohonan lanjutan reman ditolak. Siasatan PDRM di bawah Seksyen 420 masih boleh diteruskan tanpa reman.</p></article>'
extra=needle+'<article><time>10 Sep</time><h3>SPRM sahkan bekas menteri akan didakwa 14 Sep</h3><p>SPRM mengesyorkan tiga pertuduhan di bawah Seksyen 403 Kanun Keseksaan dan menyatakan individu itu berkait dengan aset di Arab Saudi. Ini masih notis pendakwaan sehingga pertuduhan dibacakan.</p></article><article><time>11 Sep</time><h3>Audit 4 lawan 5</h3><p>Chronology Bernama menyatakan empat individu telah didakwa di mahkamah; kenyataan Ketua Pesuruhjaya SPRM menyebut lima. Raven menandakan perbezaan ini sebagai rekod dipertikaikan sehingga ada penjelasan.</p></article>'
if 'Audit 4 lawan 5' not in s:
    s=replace_required(s,needle,extra,'timeline')
write(p,s)

# ------------------------------------------------------------------
# 6) TRACKS — AMLA status after 11 Sep remains unknown/open.
# ------------------------------------------------------------------
p='investigations/rci-tabung-haji/tracks/index.html'; s=cutoff10_to11(read(p))
s=s.replace('Dua individu bagi trek AMLA direman hingga 11 September.</p><p>Siasatan, tahanan dan reman bukan pertuduhan atau sabitan.', 'Dua individu bagi trek AMLA direman hingga 11 September. Setakat semakan 11 September, kami belum menemui sumber awam yang cukup kukuh untuk mengesahkan sama ada reman mereka disambung, mereka dibebaskan atau status lain ditetapkan. Status selepas reman: <b>BELUM DIKETAHUI / OPEN</b>.</p><p>Siasatan, tahanan dan reman bukan pertuduhan atau sabitan.')
s=s.replace('<strong>Betulkanion lock</strong>', '<strong>Correction lock</strong>')
write(p,s)

# ------------------------------------------------------------------
# 7) GOVERNANCE — add 11 Sep reform state; do not mix with criminal guilt.
# ------------------------------------------------------------------
p='investigations/rci-tabung-haji/governance/index.html'; s=cutoff10_to11(read(p))
anchor='<div class="control-grid">'
reform='''<article><h3>11 Sep · pembaharuan operasi haji</h3><p>TH mengumumkan Pelan Persediaan Haji – Seruan Istito’ah: mulai 1 Januari 2029, pendeposit yang mencapai baki minimum RM15,000 akan dimasukkan secara automatik ke dalam giliran haji, dengan prinsip first-come, first-served dikekalkan. Langkah ini ialah pembaharuan operasi; ia bukan bukti kesalahan jenayah sesiapa.</p><a href="'''+BERNAMA_HAJ+'''" rel="noopener noreferrer">Bernama · 11 Sep</a></article><article><h3>Pelaksanaan syor RCI</h3><p>RTM melaporkan 76% daripada 25 syor RCI telah dilaksanakan, manakala baki tindakan termasuk perkara yang memerlukan pindaan Akta TH. Angka peratusan perlu dibaca sebagai status pelaksanaan institusi, bukan ukuran penyelesaian semua isu akauntabiliti.</p><a href="'''+RTM_GOV+'''" rel="noopener noreferrer">RTM · 11 Sep</a></article>'''
if '11 Sep · pembaharuan operasi haji' not in s:
    s=s.replace(anchor,anchor+reform,1)
write(p,s)

# ------------------------------------------------------------------
# 8) NARRATIVE AUDIT — sync only the live legal-count statement/cutoff.
# ------------------------------------------------------------------
p='investigations/rci-tabung-haji/narratives/index.html'; s=read(p)
s=s.replace('Maklumat disemak hingga · 11 Sep 2026 · 01:15 MYT', f'Maklumat disemak hingga · {CUT}')
s=s.replace('Setakat 10 September, empat individu telah didakwa', 'Setakat chronology mahkamah yang disemak, empat individu telah berdepan pertuduhan yang dibacakan; SPRM pula menyebut lima dalam kiraannya')
write(p,s)

# ------------------------------------------------------------------
# 9) SOURCES — add the four sources that materially change 11 Sep state.
# ------------------------------------------------------------------
p='investigations/rci-tabung-haji/sources/index.html'; s=cutoff10_to11(read(p))
source_rows='''<li id="s61"><span>B</span><a href="'''+BERNAMA_COUNT+'''" rel="noopener noreferrer">Empat individu didakwa dalam chronology mahkamah</a><small>Bernama · 10 Sep 2026 · 22:41</small></li><li id="s62"><span>B</span><a href="'''+BERNAMA_MACC+'''" rel="noopener noreferrer">SPRM menyebut lima; bekas menteri dijadual didakwa 14 Sep</a><small>Bernama · 10 Sep 2026 · 18:05</small></li><li id="s63"><span>B</span><a href="'''+BERNAMA_HAJ+'''" rel="noopener noreferrer">Pelan Persediaan Haji – Seruan Istito’ah</a><small>Bernama · 11 Sep 2026</small></li><li id="s64"><span>B</span><a href="'''+RTM_GOV+'''" rel="noopener noreferrer">76% daripada 25 syor RCI dilaporkan dilaksanakan</a><small>RTM · 11 Sep 2026</small></li>'''
if 'id="s61"' not in s:
    s=s.replace('</ol>', source_rows+'</ol>',1)
write(p,s)

# Fix stale/wrong Bernama path introduced in prior 11 Sep article/update, where present.
for rel in ['news/2026/09/11/empat-atau-lima-didakwa-rekod-tidak-seragam/index.html','investigations/rci-tabung-haji/updates/index.html']:
    s=read(rel)
    s=s.replace('https://www.bernama.com/bm/wilayah/news.php?id=2605567', BERNAMA_MACC)
    s=s.replace('https://www.bernama.com/bm/am/news.php?id=2605694', BERNAMA_COUNT)
    write(rel,s)

print('11 Sep sitewide state sync applied')
