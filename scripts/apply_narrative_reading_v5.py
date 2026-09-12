from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / 'investigations' / 'rci-tabung-haji' / 'narratives' / 'index.html'

text = PAGE.read_text(encoding='utf-8')
css = '<link rel="stylesheet" href="/raventrace-my/assets/css/raven-narrative-v5.css?v=5.1.0" data-raven-narrative-v5>'
js = '<script src="/raventrace-my/assets/js/raven-narrative-v5.js?v=5.2.1" defer data-raven-narrative-v5></script>'

# Keep the existing visual CSS; V5.2.1 is a resilience/transformer polish update.
if css not in text:
    marker = '<link rel="stylesheet" href="/raventrace-my/assets/css/raven-v5.css?v=5.0.0" data-raven-v5-static>'
    if marker not in text:
        raise SystemExit('V5 CSS marker not found')
    text = text.replace(marker, marker + '\n' + css, 1)

# Canonicalise any older Narrative V5 JS version to V5.2.1.
text = re.sub(
    r'<script src="/raventrace-my/assets/js/raven-narrative-v5\.js\?v=[^"]+" defer data-raven-narrative-v5></script>',
    js,
    text,
)
if js not in text:
    marker = '<script src="/raventrace-my/assets/js/raven-v5.js?v=5.0.1" defer data-raven-v5-static></script>'
    if marker not in text:
        raise SystemExit('V5 JS marker not found')
    text = text.replace(marker, marker + '\n' + js, 1)

PAGE.write_text(text, encoding='utf-8')

out = PAGE.read_text(encoding='utf-8')
assert 'raven-narrative-v5.css?v=5.1.0' in out
assert out.count('raven-narrative-v5.js?v=5.2.1') == 1
assert 'Cerita yang dibawa' in out
assert 'Apa yang boleh disahkan?' in out
assert 'Selepas framing dibuang:' in out
assert 'Naratif utama' in out
print('Narrative Reading Experience V5.2.1 wiring PASS')
