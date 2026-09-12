from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = '/raventrace-my/news/2026/09/12/freshness-sweep-pac-15-sep-rm18m-claim/'


def load(rel):
    p = ROOT / rel
    return p, p.read_text(encoding='utf-8')


def save(p, text):
    p.write_text(text, encoding='utf-8')
    print('UPDATED', p.relative_to(ROOT))


def replace_once(text, old, new, label):
    if new in text:
        return text
    if old not in text:
        raise SystemExit(f'MISSING ANCHOR [{label}]')
    return text.replace(old, new, 1)

# Homepage: distinguish legal-state cutoff from freshness sweep.
p, s = load('index.html')
s = s.replace('11 September 2026 · disemak 23:37 MYT', 'Status mahkamah: 11 Sep · freshness sweep: 12 Sep 20:44 MYT', 1)
s = s.replace('Kemas kini bukti · disemak hingga 11 September · 23:37 MYT', 'Freshness sweep · 12 September · 20:44 MYT · status undang-undang tidak berubah', 1)
marker = '<div class="update-grid">'
card = f'''<article class="update-card lead-update"><div class="meta-row"><span class="status fact">SEMAKAN 12 SEP</span><span class="source-grade">Gred A/B</span></div><h3>Status undang-undang kekal; PAC TH dijadual bersidang 15 Sep.</h3><p>Tiada rekod baharu yang mengubah kiraan pertuduhan dibacakan. Portal rasmi Parlimen menyenaraikan prosiding PAC berhubung TH pada 15 September. Dakwaan viral RM18.6 juta pula kekal BELUM DISELESAIKAN kerana tiada perintah pelucuthakan yang dapat kami sahkan.</p><a href="{ARTICLE}">Baca freshness sweep →</a></article>'''
if card not in s:
    if marker not in s: raise SystemExit('MISSING HOMEPAGE update-grid')
    s = s.replace(marker, marker + card, 1)
save(p, s)

# Newsroom: publish the 12 Sep checkpoint first while preserving legal cutoff wording.
p, s = load('news/index.html')
s = s.replace('Newsroom · disemak hingga 11 Sep 2026 · 23:37 MYT', 'Newsroom · freshness sweep 12 Sep 2026 · 20:44 MYT', 1)
s = s.replace('Maklumat disemak hingga · 11 Sep 2026 · 23:37 MYT', 'Status undang-undang disahkan hingga · 11 Sep 2026 · freshness sweep 12 Sep 20:44 MYT', 1)
marker = '<div class="timeline">'
item = f'''<article id="news-2026-09-12-freshness-sweep" class="timeline-item" data-topic="governance"><time datetime="2026-09-12">12 SEP 2026</time><div><div class="meta-row"><span class="status fact">FRESHNESS SWEEP</span><span class="source-grade">Gred A/B</span></div><h3>Status undang-undang belum berubah; PAC TH bersidang 15 September.</h3><p>Portal rasmi Parlimen menyenaraikan prosiding PAC TH pada 15 September. Dakwaan viral RM18.6 juta terhadap akaun keluarga Abdul Azeez kekal belum dibuktikan; peguam beliau menafikannya.</p><a href="{ARTICLE}">Baca semakan 12 Sep →</a></div></article>'''
if item not in s:
    if marker not in s: raise SystemExit('MISSING NEWS timeline')
    s = s.replace(marker, marker + item, 1)
save(p, s)

# Tracker: add top freshness card and update next-checkpoint queue.
p, s = load('investigations/rci-tabung-haji/updates/index.html')
s = s.replace('Disemak hingga 11 September 2026.', 'Status undang-undang disemak hingga 11 September 2026; freshness sweep 12 September.', 1)
s = s.replace('Maklumat disemak hingga · 11 Sep 2026 · 23:37 MYT', 'Status undang-undang · 11 Sep 2026 · freshness sweep 12 Sep 20:44 MYT', 1)
marker = '<div class="trace-stack">'
card = f'''<article class="trace-card"><div class="trace-head"><span>JEJAK / 12-01</span><time datetime="2026-09-12">12 Sep 2026 · freshness sweep 20:44 MYT</time></div><div class="meta-row"><span class="status fact">SEMAKAN SEMASA</span><span class="source-grade">Gred A/B</span></div><h3>Tiada perubahan baharu pada status undang-undang; PAC TH dijadual 15 September.</h3><dl><div><dt>Apa disahkan?</dt><dd>Portal rasmi Parlimen menyenaraikan Prosiding 5(a) berhubung Lembaga Tabung Haji pada 15 September, 10 pagi.</dd></div><div><dt>Apa belum berubah?</dt><dd>Kiraan empat pertuduhan yang telah dibacakan kekal; kiraan SPRM lima masih belum direkonsiliasi.</dd></div><div><dt>Apa perlu ditahan?</dt><dd>Dakwaan viral lebih RM18.6 juta dalam akaun TH keluarga Abdul Azeez telah dilucuthakkan belum disokong perintah mahkamah atau rekod agensi yang kami temui. Peguam beliau menafikan dakwaan itu.</dd></div></dl><p class="inline-sources"><a href="{ARTICLE}">Semakan Raven 12 Sep</a> · <a href="https://www.parlimen.gov.my/pac/senarai-mesyuarat.html?lang=en" rel="noopener noreferrer">Parlimen · PAC</a></p></article>'''
if card not in s:
    if marker not in s: raise SystemExit('MISSING UPDATES trace-stack')
    s = s.replace(marker, marker + card, 1)
old = '<strong>14 Sep:</strong> pantau prosiding bekas menteri yang SPRM sahkan akan menghadapi tiga pertuduhan dicadangkan di bawah Seksyen 403 Kanun Keseksaan; media mengenal pasti beliau sebagai Jamil Khir Baharom, tetapi Raven menunggu pertuduhan dibacakan. <strong>AMLA:</strong> status selepas tamat tempoh reman 11 September masih belum disahkan melalui sumber awam yang kami semak. <strong>24 Sep:</strong> prosiding seterusnya bagi Adi Azuan; checkpoint ini juga penting untuk menyelesaikan discrepancy kiraan empat lawan lima.'
new = '<strong>14 Sep:</strong> pantau prosiding bekas menteri yang SPRM sahkan akan menghadapi tiga pertuduhan dicadangkan di bawah Seksyen 403 Kanun Keseksaan; Raven menunggu pertuduhan dibacakan. <strong>15 Sep:</strong> portal rasmi Parlimen menjadualkan Prosiding PAC 5(a) berhubung Lembaga Tabung Haji pada 10 pagi. <strong>AMLA:</strong> status selepas tamat tempoh reman 11 September masih belum disahkan melalui sumber awam yang kami semak. <strong>24 Sep:</strong> prosiding seterusnya bagi Adi Azuan; checkpoint ini juga penting untuk menyelesaikan discrepancy kiraan empat lawan lima.'
s = replace_once(s, old, new, 'updates-next-queue')
save(p, s)

# Main CASEFILE: prepend freshness card, without advancing legal-state cutoff.
p, s = load('investigations/rci-tabung-haji/index.html')
marker = '          <div class="trace-stack">'
card = f'''\n            <article class="trace-card"><div class="trace-head"><span>JEJAK / 12-01</span><time datetime="2026-09-12">12 Sep 2026 · freshness sweep</time></div><div class="meta-row"><span class="status fact">SEMAKAN SEMASA</span><span class="source-grade">Gred A/B</span></div><h3>Status undang-undang kekal; PAC TH dijadual 15 September.</h3><dl><div><dt>Disahkan</dt><dd>Portal rasmi Parlimen menyenaraikan prosiding PAC TH pada 15 September, jam 10 pagi.</dd></div><div><dt>Tidak berubah</dt><dd>Empat pertuduhan yang telah dibacakan kekal sebagai kiraan mahkamah yang Raven gunakan; SPRM menyebut lima dan perbezaan itu belum direkonsiliasi.</dd></div><div><dt>HOLD</dt><dd>Dakwaan viral RM18.6 juta terhadap akaun keluarga Abdul Azeez belum mempunyai perintah pelucuthakan yang dapat kami sahkan.</dd></div></dl><p class="inline-sources"><a href="{ARTICLE}">Freshness sweep 12 Sep →</a></p></article>'''
if card not in s:
    if marker not in s: raise SystemExit('MISSING CASEFILE trace-stack')
    s = s.replace(marker, marker + card, 1)
save(p, s)

# Timeline: add confirmed future PAC checkpoint after 14 Sep checkpoint if available.
p, s = load('investigations/rci-tabung-haji/timeline/index.html')
if '15 Sep</time><h3>PAC Parlimen' not in s:
    anchor = '<article><time>14 Sep</time>'
    pos = s.find(anchor)
    if pos < 0: raise SystemExit('MISSING TIMELINE 14 Sep anchor')
    end = s.find('</article>', pos)
    if end < 0: raise SystemExit('MISSING TIMELINE 14 Sep article end')
    end += len('</article>')
    add = '<article><time>15 Sep</time><h3>PAC Parlimen · checkpoint disahkan</h3><p>Portal rasmi Parlimen menjadualkan Prosiding 5(a) berhubung Lembaga Tabung Haji pada 10 pagi. Jadual prosiding bukan dapatan PAC.</p></article>'
    s = s[:end] + add + s[end:]
save(p, s)

# Source Room: add official PAC schedule and attributed denial of RM18.6m viral claim.
p, s = load('investigations/rci-tabung-haji/sources/index.html')
if 'id="s65"' not in s:
    anchor = '</ol>'
    if anchor not in s: raise SystemExit('MISSING SOURCES list end')
    add = '<li id="s65"><span>A</span><a href="https://www.parlimen.gov.my/pac/senarai-mesyuarat.html?lang=en" rel="noopener noreferrer">PAC Meeting · Prosiding 5(a) berhubung Lembaga Tabung Haji · 15 Sep 2026</a><small>Parlimen Malaysia · jadual rasmi · disemak 12 Sep</small></li><li id="s66"><span>B</span><a href="https://rebuild.freemalaysiatoday.com/category/nation/2026/09/11/azeez-s-lawyer-denies-family-funds-in-th-accounts-were-forfeited" rel="noopener noreferrer">Peguam Abdul Azeez menafikan dakwaan viral pelucuthakan RM18.6 juta</a><small>FMT · 11 Sep · kenyataan peguam; bukan bukti bebas asal-usul dana</small></li>'
    s = s.replace(anchor, add + anchor, 1)
save(p, s)

print('RCI 12 SEP FRESHNESS SWEEP PATCH: PASS')
