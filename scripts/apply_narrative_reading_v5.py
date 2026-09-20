from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / 'investigations' / 'rci-tabung-haji' / 'narratives' / 'index.html'

text = PAGE.read_text(encoding='utf-8')
css = '<link rel="stylesheet" href="/raventrace-my/assets/css/raven-narrative-v5.css?v=5.3.1" data-raven-narrative-v5>'
js = '<script src="/raventrace-my/assets/js/raven-narrative-v5.js?v=5.3.0" defer data-raven-narrative-v5></script>'

# Retire the dead V3 presentation layer from the canonical Narrative page only.
text = re.sub(
    r'<link rel="stylesheet" href="/raventrace-my/assets/css/raven-narrative-v3-1\.css\?v=[^"]+">',
    '',
    text,
)

# Canonicalise the Narrative V5 stylesheet without touching visible copy.
text = re.sub(
    r'<link rel="stylesheet" href="/raventrace-my/assets/css/raven-narrative-v5\.css\?v=[^"]+"(?: data-raven-narrative-v5)?>',
    css,
    text,
)
if css not in text:
    marker = '<link rel="stylesheet" href="/raventrace-my/assets/css/raven-v5.css?v=5.0.0" data-raven-v5-static>'
    if marker not in text:
        raise SystemExit('V5 CSS marker not found')
    text = text.replace(marker, marker + '\n' + css, 1)

# Mark the canonical page as copy-locked. This is non-visible metadata.
text = re.sub(
    r'<body class="case-share-page"(?: data-raven-copy-lock="true")?>',
    '<body class="case-share-page" data-raven-copy-lock="true">',
    text,
    count=1,
)

# Canonicalise Narrative V5 JS and keep it ahead of Funnel/Signal.
text = re.sub(
    r'<script src="/raventrace-my/assets/js/raven-narrative-v5\.js\?v=[^"]+" defer data-raven-narrative-v5></script>\s*',
    '',
    text,
)
marker = '<script src="/raventrace-my/assets/js/raven-v5.js?v=5.1.2" defer data-raven-v5-static></script>'
if marker not in text:
    raise SystemExit('V5 JS marker not found')
text = text.replace(marker, marker + '\n' + js, 1)

PAGE.write_text(text, encoding='utf-8')

out = PAGE.read_text(encoding='utf-8')
assert out.count('raven-narrative-v5.css?v=5.3.1') == 1
assert out.count('raven-narrative-v5.js?v=5.3.0') == 1
assert 'data-raven-copy-lock="true"' in out
assert 'raven-narrative-v3-1.css' not in out
assert '<b>Rekod:</b>' in out
assert '<b>Jurang cerita:</b>' in out
assert '<b>Raven:</b>' in out
assert out.find('raven-narrative-v5.js?v=5.3.0') < out.find('raven-funnel-v1.js?v=1.2.1')
assert out.find('raven-narrative-v5.js?v=5.3.0') < out.find('raven-signal-v6.js?v=6.0.0')
print('Narrative Reading Experience V5.3.0 copy-lock wiring PASS')
