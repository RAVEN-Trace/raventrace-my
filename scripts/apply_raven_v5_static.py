from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS = '<link rel="stylesheet" href="/raventrace-my/assets/css/raven-v5.css?v=5.0.0" data-raven-v5-static>'
UNIFIED_CSS = '<link rel="stylesheet" href="/raventrace-my/assets/css/raven-unified-v7.css?v=7.0.2" data-raven-unified>'
JS = '<script src="/raventrace-my/assets/js/raven-v5.js?v=5.1.2" defer data-raven-v5-static></script>'

paths = []
for rel in [
    'index.html',
    'about/index.html',
    'methodology/index.html',
    'tips/index.html',
    'corrections/index.html',
    'investigations/index.html',
    'news/index.html',
]:
    p = ROOT / rel
    if p.exists():
        paths.append(p)

for base in [ROOT / 'investigations', ROOT / 'news']:
    if base.exists():
        paths.extend(base.rglob('index.html'))

seen = set()
changed = []
for path in paths:
    if path in seen:
        continue
    seen.add(path)
    text = path.read_text(encoding='utf-8')
    original = text
    if 'data-raven-v5-static' not in text:
        if '</head>' in text:
            text = text.replace('</head>', f'{CSS}\n</head>', 1)
        if '</body>' in text:
            text = text.replace('</body>', f'{JS}\n</body>', 1)
    else:
        # Keep a cache-busted JS URL when the UX layer changes.
        text = text.replace('/assets/js/raven-v5.js?v=5.0.0', '/assets/js/raven-v5.js?v=5.1.2')
    if 'data-raven-unified' not in text and '</head>' in text:
        text = text.replace('</head>', f'{UNIFIED_CSS}\n</head>', 1)
    if text != original:
        path.write_text(text, encoding='utf-8')
        changed.append(path.relative_to(ROOT).as_posix())

print(f'RAVEN V5 STATIC INJECTION: {len(changed)} file(s) changed')
for item in changed:
    print(item)
