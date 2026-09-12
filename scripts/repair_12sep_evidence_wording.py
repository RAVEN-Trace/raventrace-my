from pathlib import Path

replacements = {
    'index.html': [
        ('Status undang-undang kekal; PAC TH dijadual bersidang 15 Sep.',
         'Status undang-undang kekal; prosiding PAC berkaitan TH dijadual 15 Sep.'),
    ],
    'news/index.html': [
        ('Status undang-undang belum berubah; PAC TH bersidang 15 September.',
         'Status undang-undang belum berubah; prosiding PAC berkaitan TH dijadual 15 September.'),
        ('Portal rasmi Parlimen menyenaraikan prosiding PAC TH pada 15 September.',
         'Portal rasmi Parlimen menyenaraikan prosiding PAC berhubung Tabung Haji pada 15 September.'),
    ],
    'news/2026/09/12/freshness-sweep-pac-15-sep-rm18m-claim/index.html': [
        ('12 Sep: Status undang-undang kekal, PAC TH bersidang 15 Sep | RAVEN-Trace',
         '12 Sep: Status undang-undang kekal, prosiding PAC TH dijadual 15 Sep | RAVEN-Trace'),
        ('12 Sep: Tiada perubahan undang-undang; PAC TH bersidang 15 Sep',
         '12 Sep: Tiada perubahan undang-undang; prosiding PAC TH dijadual 15 Sep'),
        ('https://www.bernama.com/en/region/news.php?id=2605582',
         'https://www.bernama.com/en/news.php?id=2605582'),
    ],
}

for path, pairs in replacements.items():
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    before = text
    for old, new in pairs:
        if old not in text and new not in text:
            raise SystemExit(f'{path}: expected wording not found: {old}')
        text = text.replace(old, new)
    if text != before:
        p.write_text(text, encoding='utf-8')
        print('updated', path)
    else:
        print('already clean', path)
