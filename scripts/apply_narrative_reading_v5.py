from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / 'investigations' / 'rci-tabung-haji' / 'narratives' / 'index.html'

text = PAGE.read_text()
css = '<link rel="stylesheet" href="/raventrace-my/assets/css/raven-narrative-v5.css?v=5.1.0" data-raven-narrative-v5>'
js = '<script src="/raventrace-my/assets/js/raven-narrative-v5.js?v=5.1.0" defer data-raven-narrative-v5></script>'

if css not in text:
    marker = '<link rel="stylesheet" href="/raventrace-my/assets/css/raven-v5.css?v=5.0.0" data-raven-v5-static>'
    if marker not in text:
        raise SystemExit('V5 CSS marker not found')
    text = text.replace(marker, marker + '\n' + css, 1)

if js not in text:
    marker = '<script src="/raventrace-my/assets/js/raven-v5.js?v=5.0.1" defer data-raven-v5-static></script>'
    if marker not in text:
        raise SystemExit('V5 JS marker not found')
    text = text.replace(marker, marker + '\n' + js, 1)

PAGE.write_text(text)

out = PAGE.read_text()
assert 'raven-narrative-v5.css?v=5.1.0' in out
assert 'raven-narrative-v5.js?v=5.1.0' in out
assert 'Lapan naratif utama' in out
assert 'Apa yang boleh disahkan?' in out
assert 'Selepas framing dibuang:' in out
print('Narrative Reading Experience V5.1 wiring PASS')
