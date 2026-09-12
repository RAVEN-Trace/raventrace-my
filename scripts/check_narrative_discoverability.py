from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
HUB = '/raventrace-my/investigations/rci-tabung-haji/narratives/'
SUB = '/raventrace-my/investigations/rci-tabung-haji/narratives/political-social-media/'
PUBLIC_ROOTS = ('about', 'corrections', 'investigations', 'methodology', 'news', 'tips')
NAV_RE = re.compile(r'<nav\b[^>]*class="[^"]*\bsite-nav\b[^"]*"[^>]*>(.*?)</nav>', re.S)


def public_html_files():
    files = [ROOT / 'index.html']
    for root_name in PUBLIC_ROOTS:
        root = ROOT / root_name
        if root.exists():
            files.extend(sorted(root.rglob('*.html')))
    return list(dict.fromkeys(files))


def contextual(rel: str) -> bool:
    # Every RCI evidence/data surface should deep-link to the narrative lens,
    # except pages already inside the narrative section itself.
    if rel.startswith('investigations/rci-tabung-haji/') and '/narratives/' not in rel:
        return True
    # Every published RCI newsroom story gets the same direct narrative route.
    if rel.startswith('news/2026/') and rel.endswith('/index.html'):
        return True
    return False


errors = []
files = public_html_files()
for path in files:
    rel = path.relative_to(ROOT).as_posix()
    text = path.read_text(encoding='utf-8')

    nav = NAV_RE.search(text)
    if not nav:
        errors.append(f'{rel}: primary site-nav missing')
    elif HUB not in nav.group(1):
        errors.append(f'{rel}: Audit Naratif hub missing from primary site-nav')

    if contextual(rel):
        if SUB not in text:
            errors.append(f'{rel}: political/social narrative deep-link missing')
        if 'data-narrative-route' not in text:
            errors.append(f'{rel}: contextual narrative route module missing')

if errors:
    print('NARRATIVE DISCOVERABILITY: FAIL')
    for error in errors:
        print(' -', error)
    sys.exit(1)

print(f'NARRATIVE DISCOVERABILITY: PASS — {len(files)} public HTML pages expose Audit Naratif')
print('Contextual RCI/news pages also expose the political + social media narrative subpage')
