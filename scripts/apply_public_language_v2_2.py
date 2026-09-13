#!/usr/bin/env python3
"""RAVEN Public Language V2.2 — sitewide residue cleanup.

Cleans remaining public analyst/ops language after V2/V2.1. Factual values,
legal states, source links, IDs, routes and evidence grades are preserved.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def swap(rel, replacements):
    p = ROOT / rel
    s = p.read_text(encoding='utf-8')
    before = s
    for a,b in replacements:
        s = s.replace(a,b)
    if s != before:
        p.write_text(s,encoding='utf-8')
        print('updated',rel)

# Homepage
swap('index.html',[
    ('Status mahkamah: 11 Sep · freshness sweep: 12 Sep 20:44 MYT','Status mahkamah: 11 Sep · semakan terbaru: 12 Sep 20:44 MYT'),
])

# Newsroom
swap('news/index.html',[
    ('Newsroom · freshness sweep 12 Sep 2026 · 20:44 MYT','Newsroom · semakan terbaru 12 Sep 2026 · 20:44 MYT'),
    ('Status undang-undang disahkan hingga · 11 Sep 2026 · freshness sweep 12 Sep 20:44 MYT','Status undang-undang disahkan hingga · 11 Sep 2026 · semakan terbaru 12 Sep 20:44 MYT'),
    ('>FRESHNESS SWEEP<','>SEMAKAN TERBARU<'),
    ('>DISPUTED RECORD<','>REKOD TAK SEPADAN<'),
    ('Chronology mahkamah','Kronologi mahkamah'),
    ('Asal C/D → diverifikasi B','Asal C/D → disahkan B'),
])

# RCI updates page
swap('investigations/rci-tabung-haji/updates/index.html',[
    ('Status undang-undang disemak hingga 11 September 2026; freshness sweep 12 September.','Status undang-undang disemak hingga 11 September 2026; semakan terbaru dibuat 12 September.'),
    ('claim mana yang masih menunggu checkpoint','dakwaan mana yang masih menunggu bukti'),
    ('DAKWAAN → SEMAKAN<br>→ semakan','DAKWAAN → SEMAKAN<br>→ APA YANG DISAHKAN'),
    ('RCI TABUNG HAJI · CASE TRACKER','RCI TABUNG HAJI · PERKEMBANGAN KES'),
    ('Status undang-undang · 11 Sep 2026 · freshness sweep 12 Sep 20:44 MYT','Status undang-undang · 11 Sep 2026 · semakan terbaru 12 Sep 20:44 MYT'),
    ('Kongsi tracker','Kongsi perkembangan'),
    ('<span>NOW</span><p>Latest disemak evidence</p>','<span>NOW</span><p>Apa yang paling baru?</p>'),
    ('DAKWAAN lama diuji terhadap rekod baharu.','Dakwaan lama dibandingkan dengan rekod baharu.'),
    ('12 Sep 2026 · freshness sweep 20:44 MYT','12 Sep 2026 · semakan 20:44 MYT'),
    ('belum direkonsiliasi','belum dipadankan'),
    ('>DISPUTED RECORD<','>REKOD TAK SEPADAN<'),
    ('<dt>Verdict Raven</dt>','<dt>Raven kata macam mana?</dt>'),
    ('Ini ialah prosecution notice; pertuduhan belum dibacakan.','Ini ialah notis bahawa pendakwaan dirancang; pertuduhan masih belum dibacakan di mahkamah.'),
    ('Pelepasan daripada reman bukan NFA','Dilepaskan daripada reman bukan bermaksud fail ditutup (NFA)'),
    ('Apa masih DAKWAAN?','Apa yang masih dakwaan?'),
    ('hasil bagi Azeez kini mempunyai rekod mahkamah.','Bagi Azeez, rekod mahkamah kini tersedia.'),
    ('dakwaan asal dikekalkan supaya pembaca boleh audit ketepatan ramalan terhadap hasil sebenar.','Dakwaan asal dikekalkan supaya pembaca boleh bandingkan apa yang dilaporkan dahulu dengan apa yang benar-benar berlaku.'),
    ('dakwaan asal + SEMAKAN','Dakwaan asal + semakan'),
])

# Main RCI casefile: only public-language residue, not factual content.
swap('investigations/rci-tabung-haji/index.html',[
    ('ROYAL COMMISSION OF INQUIRY / TABUNG HAJI / 2014—2020','RCI TABUNG HAJI / 2014—2020'),
    ('Setakat chronology mahkamah yang disemak','Setakat kronologi mahkamah yang disemak'),
    ('empat dalam chronology mahkamah','empat dalam kronologi mahkamah'),
    ('12 Sep 2026 · freshness sweep','12 Sep 2026 · semakan terbaru'),
    ('belum direkonsiliasi','belum dipadankan'),
    ('<dt>HOLD</dt>','<dt>Belum selesai</dt>'),
])

# 12 Sep article: translate the reader-facing newsroom/analyst shorthand.
swap('news/2026/09/12/freshness-sweep-pac-15-sep-rm18m-claim/index.html',[
    ('content="Freshness sweep 12 September 2026:', 'content="Semakan 12 September 2026:'),
    ('RCI Tabung Haji · Freshness sweep','RCI Tabung Haji · Semakan 12 September'),
    ('checkpoint baharu yang patut dipantau','perkembangan baharu yang patut dipantau'),
    ('Ini ialah checkpoint institusi yang disahkan, bukan dapatan atau keputusan PAC yang sudah wujud.','Ini ialah jadual prosiding yang disahkan — bukan dapatan atau keputusan PAC.'),
    ('mengubah state semasa','mengubah keadaan semasa'),
    ('kekal belum direkonsiliasi','masih belum dipadankan'),
    ('<strong>CHECKPOINT:</strong>','<strong>SETERUSNYA:</strong>'),
    ('<strong>COUNTER-CLAIM:</strong>','<strong>JAWAPAN BALAS:</strong>'),
    ('<strong>VERDICT RAVEN:</strong> <b>BELUM DISELESAIKAN / HOLD.</b>','<strong>RAVEN KATA:</strong> <b>BELUM SELESAI.</b>'),
    ('<h2>Next verified checkpoints</h2>','<h2>Apa yang perlu diperhatikan seterusnya?</h2>'),
    ('Bernama · prosecution notice 14 Sep','Bernama · notis pendakwaan dirancang 14 Sep'),
    ('framing, slogan, pilihan bahasa dan signal media sosial','cara cerita dibingkaikan, slogan, pilihan bahasa dan petunjuk media sosial'),
])

# Source-level/meta public polish on narrative hub/social page after V2.1.
swap('investigations/rci-tabung-haji/narratives/index.html',[
    ('cara sesuatu cerita dibingkaikan','cara sesuatu cerita disusun'),
])
swap('investigations/rci-tabung-haji/narratives/political-social-media/index.html',[
    ('bagaimana framing boleh mempengaruhi pembaca','bagaimana cara cerita disusun boleh mempengaruhi pembaca'),
    ('Batas bukti:','Batas bukti:'),
])

# Guardrails
home=(ROOT/'index.html').read_text(encoding='utf-8')
news=(ROOT/'news/index.html').read_text(encoding='utf-8')
updates=(ROOT/'investigations/rci-tabung-haji/updates/index.html').read_text(encoding='utf-8')
case=(ROOT/'investigations/rci-tabung-haji/index.html').read_text(encoding='utf-8')
article=(ROOT/'news/2026/09/12/freshness-sweep-pac-15-sep-rm18m-claim/index.html').read_text(encoding='utf-8')

assert 'semakan terbaru: 12 Sep 20:44 MYT' in home
assert 'Newsroom · semakan terbaru 12 Sep 2026 · 20:44 MYT' in news
assert 'REKOD TAK SEPADAN' in news
assert 'RCI TABUNG HAJI · PERKEMBANGAN KES' in updates
assert 'Raven kata macam mana?' in updates
assert 'Pertuduhan bukan sabitan' in updates
assert '12 Sep 2026 · semakan terbaru' in case
assert '<strong>RAVEN KATA:</strong> <b>BELUM SELESAI.</b>' in article
assert 'RM18.6 juta' in article
assert '/freshness-sweep-pac-15-sep-rm18m-claim/' in article  # route stays unchanged

# Public pages should no longer expose these operational phrases.
for label,text in [('home',home),('news',news),('updates',updates),('article',article)]:
    for stale in ['freshness sweep','DISPUTED RECORD','Chronology mahkamah']:
        assert stale not in text, f'{label}: stale public phrase {stale}'

print('RAVEN PUBLIC LANGUAGE V2.2: PASS')
