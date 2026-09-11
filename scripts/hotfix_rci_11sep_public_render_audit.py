from pathlib import Path


def patch(path, replacements):
    p = Path(path)
    s = p.read_text()
    original = s
    for old, new in replacements:
        if old not in s:
            raise SystemExit(f'{path}: missing expected text: {old[:80]}')
        s = s.replace(old, new)
    if s != original:
        p.write_text(s)

# Homepage: avoid implying only four charges total; fix duplicated update indices; Malay-first wording.
patch('index.html', [
    ('<div class="docket-stat"><strong>04</strong><span>pertuduhan telah dibacakan kepada empat individu setakat rekod mahkamah 10 Sep · SPRM menyebut lima</span></div>',
     '<div class="docket-stat"><strong>04</strong><span>individu telah berdepan pertuduhan yang dibacakan setakat rekod mahkamah 10 Sep · SPRM menyebut lima</span></div>'),
    ('Chronology Bernama menyatakan empat individu telah didakwa di mahkamah.',
     'Kronologi Bernama menyatakan empat individu telah didakwa di mahkamah.'),
    ('<article id="home-2026-09-07-expected-charges" class="update-card lead-update"><div class="update-index">01</div>',
     '<article id="home-2026-09-07-expected-charges" class="update-card lead-update"><div class="update-index">02</div>'),
    ('<article id="home-2026-09-06-jamil-reman-checkpoint" class="update-card"><div class="update-index">02</div>',
     '<article id="home-2026-09-06-jamil-reman-checkpoint" class="update-card"><div class="update-index">03</div>'),
    ('<article id="home-2026-09-03-reformasi-rci" class="update-card"><div class="update-index">03</div>',
     '<article id="home-2026-09-03-reformasi-rci" class="update-card"><div class="update-index">04</div>'),
])

# Investigations desk: use people count, not charge count; remove stale relative date wording.
patch('investigations/index.html', [
    ('<span>4 pertuduhan dibacakan · kiraan SPRM: 5 · rekod belum seragam</span>',
     '<span>4 individu dengan pertuduhan dibacakan · kiraan SPRM: 5 · rekod belum seragam</span>'),
    ('Datuk Azmi Ahmad didakwa hari ini atas dua pertuduhan menipu berkaitan kadar sewaan harian kapal dan mengaku tidak bersalah.',
     'Datuk Azmi Ahmad didakwa pada 10 September atas dua pertuduhan menipu berkaitan kadar sewaan harian kapal dan mengaku tidak bersalah.'),
    ('chronology mahkamah menunjukkan empat, manakala SPRM menyebut lima.',
     'kronologi mahkamah menunjukkan empat, manakala SPRM menyebut lima.'),
])

# Main CASEFILE: same unit-of-count correction and Malay-first wording.
patch('investigations/rci-tabung-haji/index.html', [
    ('<div><dt>04</dt><dd>pertuduhan dibacakan setakat chronology mahkamah · SPRM menyebut 05</dd></div>',
     '<div><dt>04</dt><dd>individu dengan pertuduhan dibacakan setakat kronologi mahkamah · SPRM menyebut 05</dd></div>'),
])

# 11 Sep forensic article: public language consistency.
patch('news/2026/09/11/empat-atau-lima-didakwa-rekod-tidak-seragam/index.html', [
    ('Chronology mahkamah menunjukkan empat individu telah berdepan pertuduhan yang dibacakan.',
     'Kronologi mahkamah menunjukkan empat individu telah berdepan pertuduhan yang dibacakan.'),
    ('Berdasarkan chronology mahkamah dan laporan yang boleh diaudit,',
     'Berdasarkan kronologi mahkamah dan laporan yang boleh diaudit,'),
])

# Updates tracker: same language cleanup.
p = Path('investigations/rci-tabung-haji/updates/index.html')
s = p.read_text()
s2 = s.replace('Chronology mahkamah menunjukkan empat individu telah berdepan pertuduhan yang dibacakan.',
               'Kronologi mahkamah menunjukkan empat individu telah berdepan pertuduhan yang dibacakan.')
if s2 != s:
    p.write_text(s2)

print('Public render audit hotfix applied')
