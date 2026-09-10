from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = '/raventrace-my/investigations/rci-tabung-haji/'
NARRATIVE = '<a href="/raventrace-my/investigations/rci-tabung-haji/narratives/">Audit naratif</a>'

# Keep standalone CASEFILE section navigation connected to the narrative audit.
slugs = ['updates','people','timeline','governance','money','investments','tracks','disputed-record','sources']
changed = []
for slug in slugs:
    path = ROOT / 'investigations' / 'rci-tabung-haji' / slug / 'index.html'
    text = path.read_text()
    if '/rci-tabung-haji/narratives/' not in text:
        marker = '<a href="/raventrace-my/investigations/rci-tabung-haji/sources/"'
        pos = text.find(marker)
        if pos < 0:
            raise SystemExit(f'Navigation marker missing in {path}')
        text = text[:pos] + NARRATIVE + text[pos:]
        path.write_text(text)
        changed.append(str(path.relative_to(ROOT)))

# Make the integration survive future rebuilds of standalone share pages.
builder = ROOT / 'scripts' / 'build_rci_share_pages.py'
text = builder.read_text()
old = "  nav = ''.join(f'<a href=\"{BASE}{slug}/\"' + (' aria-current=\"page\"' if key == slug else '') + f'>{escape(name)}</a>' for slug, (name, _) in SECTIONS.items())"
new = old + "\n  if '/rci-tabung-haji/narratives/' not in nav:\n   nav = nav.replace(f'<a href=\"{BASE}sources/\"', f'<a href=\"{BASE}narratives/\">Audit naratif</a><a href=\"{BASE}sources/\"')"
if old not in text and "nav.replace(f'<a href=\"{BASE}sources/\"'" not in text:
    raise SystemExit('Builder navigation pattern not found')
if old in text and "nav.replace(f'<a href=\"{BASE}sources/\"'" not in text:
    text = text.replace(old, new, 1)
    builder.write_text(text)
    changed.append(str(builder.relative_to(ROOT)))

# QA: every standalone RCI page must expose the narrative audit.
for slug in slugs:
    path = ROOT / 'investigations' / 'rci-tabung-haji' / slug / 'index.html'
    if '/rci-tabung-haji/narratives/' not in path.read_text():
        raise SystemExit(f'QA failed: narrative link missing in {path}')

print('Persistent narrative integration PASS')
for item in changed:
    print('updated:', item)
