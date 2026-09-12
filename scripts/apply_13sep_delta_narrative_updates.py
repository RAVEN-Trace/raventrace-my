from pathlib import Path

ROOT=Path('.')

def must_replace(text, old, new, label):
    if old not in text:
        raise SystemExit(f'missing anchor: {label}')
    return text.replace(old,new,1)

# 1) Abdul Azeez article: clarify RM193.5m meaning + RM18.6m hold
p=ROOT/'news/2026/09/09/abdul-azeez-didakwa-rm1935-juta/index.html'
t=p.read_text(encoding='utf-8')
t=t.replace('<meta property="article:modified_time" content="2026-09-09T23:40:00+08:00">','<meta property="article:modified_time" content="2026-09-13T01:00:00+08:00">',1)
anchor='<h2>Apa status undang-undang sekarang?</h2>'
block='''<div class="story-callout"><strong>PEMBETULAN NARATIF · RM193.5 juta bukan jumlah yang didakwa diambil</strong><p>Rekod pertuduhan yang disemak menunjukkan RM193.5 juta merujuk kepada <strong>nilai pelaburan TH dalam Putrajaya Perdana</strong> yang dikaitkan dengan dakwaan penggunaan kedudukan. Ia bukan jumlah yang pertuduhan dakwa dibayar, dipindahkan atau dimasukkan ke akaun Abdul Azeez atau keluarganya. Peguam beliau turut menegaskan perkara ini pada 12 September. Raven mengekalkan pemisahan ini kerana angka besar mudah berubah menjadi dakwaan yang lebih berat apabila konteksnya dibuang.</p><p><strong>Status bukti:</strong> FAKTA tentang struktur pertuduhan · Gred B · keyakinan tinggi. Sama ada pertuduhan itu akhirnya terbukti kekal untuk diputuskan mahkamah.</p></div>\n<div class="story-callout"><strong>RM18.6 juta akaun keluarga · BELUM DISELESAIKAN / HOLD</strong><p>Dakwaan media sosial bahawa lebih RM18.6 juta dalam akaun TH ahli keluarga Abdul Azeez telah dilucuthakkan dinafikan oleh peguamnya. Setakat semakan ini, Raven belum menemui perintah pelucuthakan mahkamah atau rekod rasmi agensi yang mengesahkan dakwaan viral tersebut. Penafian peguam membuktikan penafian itu dibuat; ia bukan bukti bebas mengenai asal-usul dana.</p></div>\n'''
t=must_replace(t,anchor,block+anchor,'Azeez status heading')
# add new sources before closing source list
src_anchor='</ul>\n<p class="story-note">'
new_src='''<li><a href="https://www.thestar.com.my/news/nation/2026/09/12/rm1935mil-refers-to-ths-investment-value-not-funds-taken-says-abdul-azeezs-lawyer" rel="noopener noreferrer">The Star — RM193.5m refers to TH investment value, not funds taken, says lawyer</a><small>12 Sep 2026 · penjelasan peguam; digunakan untuk mengesahkan tafsiran struktur pertuduhan, bukan sebagai bukti innocence.</small></li><li><a href="https://www.freemalaysiatoday.com/category/bahasa/tempatan/2026/09/11/peguam-azeez-nafi-wang-dalam-akaun-th-ahli-keluarga-telah-dilucut-hak" rel="noopener noreferrer">FMT — Peguam Azeez nafi wang akaun TH keluarga dilucuthakkan</a><small>11 Sep 2026 · counter-claim kepada dakwaan viral RM18.6 juta; tiada perintah pelucuthakan ditemui dalam semakan Raven.</small></li></ul>\n<p class="story-note">'''
t=must_replace(t,src_anchor,new_src,'Azeez source list close')
p.write_text(t,encoding='utf-8')

# 2) Main Narrative Forensics: add RM193.5m correction card and update cutoff
p=ROOT/'investigations/rci-tabung-haji/narratives/index.html'
t=p.read_text(encoding='utf-8')
t=t.replace('Maklumat naratif disemak hingga · 12 Sep 2026 · 22:03 MYT','Maklumat naratif disemak hingga · 13 Sep 2026 · 01:00 MYT',1)
needle='<section class="case-section"><div class="section-marker"><span>02</span><p>Naratif vs bukti</p></div><h2>Lapan naratif utama — buang framing dahulu, kemudian lihat apa yang tinggal.</h2><div class="control-grid">'
replacement='''<section class="case-section"><div class="section-marker"><span>02</span><p>Naratif vs bukti</p></div><h2>Naratif utama — buang framing dahulu, kemudian lihat apa yang tinggal.</h2><div class="control-grid"><article><h3>“Azeez ambil RM193.5 juta”</h3><p><span class="status disputed">TIDAK DISOKONG STRUKTUR PERTUDUHAN</span></p><p><b>Cerita yang dibawa</b> Angka RM193.5 juta mudah dibaca seolah-olah itulah jumlah wang yang didakwa diambil atau dimasukkan ke akaun Abdul Azeez.</p><p><b>Apa yang boleh disahkan?</b> Pertuduhan yang dilaporkan merujuk RM193.5 juta sebagai nilai pelaburan TH dalam Putrajaya Perdana. Dakwaan terhadap Abdul Azeez berkaitan penggunaan kedudukan untuk memperoleh jawatan pengerusi dan faedah berkaitan sambil mempengaruhi keputusan pelaburan tersebut.</p><p><b>Teknik naratif</b> <strong>Category collapse + number laundering.</strong> Nilai transaksi/pelaburan ditukar dalam persepsi awam menjadi jumlah wang yang kononnya diambil individu.</p><p><b>Apa yang cerita ini tinggalkan?</b> Nilai pelaburan, nilai kerugian, nilai manfaat peribadi dan jumlah wang yang didakwa diseleweng ialah kategori berbeza.</p><p><b>Selepas framing dibuang:</b> RM193.5 juta ialah nilai pelaburan yang menjadi konteks pertuduhan — bukan jumlah yang pertuduhan dakwa dibayar atau dimasukkan ke akaun Abdul Azeez atau keluarganya. Beliau mengaku tidak bersalah dan pertuduhan belum dibuktikan.</p><p><b>Bukti apa boleh mengubah penilaian?</b> Charge sheet atau rekod mahkamah yang menunjukkan pertuduhan berasingan mengenai pemindahan RM193.5 juta kepada beliau/keluarga akan mengubah assessment ini. Setakat semakan 13 Sep, rekod yang kami gunakan tidak menunjukkan perkara itu.</p><p><b>Tahap keyakinan:</b> Tinggi untuk maksud angka dalam pertuduhan semasa. · <b>Last verified:</b> 13 Sep 2026 · 01:00 MYT</p></article>'''
t=must_replace(t,needle,replacement,'narrative grid heading')
p.write_text(t,encoding='utf-8')

# 3) Political/social page: add new political persecution narrative, carefully bounded
p=ROOT/'investigations/rci-tabung-haji/narratives/political-social-media/index.html'
t=p.read_text(encoding='utf-8')
t=t.replace('Naratif disemak hingga · 12 Sep 2026 · 22:03 MYT','Naratif disemak hingga · 13 Sep 2026 · 01:00 MYT',1)
anchor='<section class="case-section"><div class="section-marker"><span>04</span><p>Audit bahasa</p></div>'
card='''<section class="case-section" id="political-intimidation"><div class="section-marker"><span>POL+</span><p>Naratif baharu · 12 Sep</p></div><h2>“Penguatkuasaan digunakan sebagai senjata politik” — dakwaan politik, bukan dapatan kes.</h2><p class="section-lead">Perwakilan UMNO Kedah Shaiful Hazizy Zainol Abidin mendakwa penahanan dan reman beberapa pemimpin UMNO merupakan “political intimidation” dan “political harassment”, serta menuduh institusi kerajaan digunakan terhadap lawan politik.</p><div class="case-warning light"><strong>Apa yang boleh disahkan?</strong><span>Kenyataan itu memang dibuat dan dilaporkan pada 12 September. Beberapa pemimpin UMNO memang melalui proses siasatan, tangkapan atau reman.</span></div><div class="case-warning light"><strong>Apa yang belum terbukti?</strong><span>Timing, pakaian lokap atau kesan politik tidak dengan sendiri membuktikan bahawa SPRM/PDRM menerima arahan politik. Untuk menaikkan dakwaan ini menjadi fakta, perlu ada bukti seperti arahan, communication trail, decision record atau comparative selective-enforcement analysis.</span></div><p><b>Selepas framing dibuang:</b> <strong>CLAIM · POSISI POLITIK.</strong> Wujud bukti bahawa dakwaan political intimidation dibuat; belum ada bukti awam yang kami semak yang membuktikan enforcement dalam kes RCI TH dikawal secara politik.</p><p><b>Tahap keyakinan:</b> Tinggi bahawa dakwaan dibuat · rendah untuk kebenaran sebab-musabab yang didakwa.</p><p class="inline-sources"><a href="https://www.thestar.com.my/news/nation/2026/09/12/kedah-umno-urges-action-on-promised-parliamentary-oversight-of-macc" rel="noopener noreferrer">The Star · 12 Sep</a> · <a href="https://malaysiagazette.com/2026/09/12/reformasi-jadi-reformati-umno-kedah-gesa-sprm-di-bawah-parlimen/" rel="noopener noreferrer">MalaysiaGazette · 12 Sep</a></p></section>\n'''
t=must_replace(t,anchor,card+anchor,'political audit language section')
p.write_text(t,encoding='utf-8')

# 4) Source Room: update source cutoff and add new source cards
p=ROOT/'investigations/rci-tabung-haji/sources/index.html'
t=p.read_text(encoding='utf-8')
t=t.replace('Maklumat disemak hingga · 11 Sep 2026 · 23:37 MYT','Status undang-undang · 11 Sep 2026 · sumber/naratif disemak 13 Sep 2026 · 01:00 MYT',1)
needle='<ol class="sources-grid">'
new='''<ol class="sources-grid"><li id="s67"><span>B</span><a href="https://www.thestar.com.my/news/nation/2026/09/12/rm1935mil-refers-to-ths-investment-value-not-funds-taken-says-abdul-azeezs-lawyer" rel="noopener noreferrer">RM193.5 juta = nilai pelaburan TH, bukan jumlah yang didakwa diambil</a><small>The Star · 12 Sep 2026 · penjelasan peguam; dibaca bersama rekod pertuduhan 9 Sep</small></li><li id="s68"><span>B</span><a href="https://www.freemalaysiatoday.com/category/bahasa/tempatan/2026/09/11/peguam-azeez-nafi-wang-dalam-akaun-th-ahli-keluarga-telah-dilucut-hak" rel="noopener noreferrer">Peguam nafi dakwaan viral pelucuthakan >RM18.6 juta akaun keluarga</a><small>FMT · 11 Sep 2026 · counter-claim; bukan bukti bebas tentang asal dana</small></li><li id="s69"><span>B</span><a href="https://www.thestar.com.my/news/nation/2026/09/12/kedah-umno-urges-action-on-promised-parliamentary-oversight-of-macc" rel="noopener noreferrer">UMNO Kedah dakwa political intimidation / harassment</a><small>The Star · 12 Sep 2026 · bukti kenyataan politik dibuat, bukan bukti enforcement dikawal politik</small></li>'''
t=must_replace(t,needle,new,'source grid')
p.write_text(t,encoding='utf-8')

print('13 SEP DELTA NARRATIVE UPDATE: APPLIED')
