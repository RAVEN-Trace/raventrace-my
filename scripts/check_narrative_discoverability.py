from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
HUB = '/raventrace-my/investigations/rci-tabung-haji/narratives/'
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
    # RCI evidence/data surfaces and published RCI newsroom stories should expose
    # Audit Naratif both globally and contextually. The V6 truth-navigation model
    # no longer requires every surface to route through one political/social subpage.
    if rel.startswith('investigations/rci-tabung-haji/') and '/narratives/' not in rel:
        return True
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
        # One link is the global navigation. A second occurrence must appear in
        # the case/section navigation or contextual continuation route.
        hub_links = text.count(f'href="{HUB}"')
        if hub_links < 2:
            errors.append(f'{rel}: contextual Audit Naratif route missing (found {hub_links} hub link)')

if errors:
    print('NARRATIVE DISCOVERABILITY: FAIL')
    for error in errors:
        print(' -', error)
    sys.exit(1)

print(f'NARRATIVE DISCOVERABILITY: PASS — {len(files)} public HTML pages expose Audit Naratif')
print('Contextual RCI/news pages expose a second direct route to the Audit Naratif hub')
