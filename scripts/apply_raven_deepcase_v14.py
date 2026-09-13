from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CSS = '<link rel="stylesheet" href="/raventrace-my/assets/css/raven-deepcase-v14.css?v=1.4.0" data-raven-deepcase-v14>'
JS = '<script src="/raventrace-my/assets/js/raven-deepcase-v14.js?v=1.4.0" defer data-raven-deepcase-v14></script>'

TARGETS = [
    ROOT / 'investigations' / 'rci-tabung-haji' / 'governance' / 'index.html',
    ROOT / 'investigations' / 'rci-tabung-haji' / 'investments' / 'index.html',
    ROOT / 'investigations' / 'rci-tabung-haji' / 'tracks' / 'index.html',
    ROOT / 'investigations' / 'rci-tabung-haji' / 'disputed-record' / 'index.html',
    ROOT / 'investigations' / 'rci-tabung-haji' / 'sources' / 'index.html',
]

def wire(text: str) -> str:
    text = re.sub(r'\s*<link[^>]+data-raven-deepcase-v14[^>]*>\s*', '\n', text)
    text = re.sub(r'\s*<script[^>]+data-raven-deepcase-v14[^>]*></script>\s*', '\n', text)
    if '</head>' not in text or '</body>' not in text:
        raise RuntimeError('Missing head/body close')
    text = text.replace('</head>', f'{CSS}\n</head>', 1)
    text = text.replace('</body>', f'{JS}\n</body>', 1)
    return text

changed = []
for path in TARGETS:
    if not path.exists():
        raise RuntimeError(f'Missing target: {path.relative_to(ROOT)}')
    original = path.read_text(encoding='utf-8')
    text = wire(original)
    if text.count('data-raven-deepcase-v14') != 2:
        raise RuntimeError(f'Deepcase assets not canonical in {path.relative_to(ROOT)}')
    if text != original:
        path.write_text(text, encoding='utf-8')
        changed.append(path.relative_to(ROOT).as_posix())

for path in ROOT.rglob('investigations/rci-tabung-haji/research/**/index.html'):
    text = path.read_text(encoding='utf-8')
    if 'data-raven-deepcase-v14' in text:
        raise RuntimeError(f'Historical research must stay untouched: {path.relative_to(ROOT)}')

print(f'RAVEN DEEP CASE V1.4.0: {len(changed)} target page(s) changed')
for item in changed:
    print(f'  {item}')
