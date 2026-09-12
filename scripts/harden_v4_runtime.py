from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CURRENT_PUBLICATION = 'raven-publication.js?v=4.3.0'
OLD_PUBLICATION_VERSIONS = [
    'raven-publication.js?v=1.1.0',
    'raven-publication.js?v=2.0.0',
    'raven-publication.js?v=2.1.0',
]

PUBLIC_ROOTS = [
    ROOT / 'index.html',
    ROOT / 'about',
    ROOT / 'methodology',
    ROOT / 'corrections',
    ROOT / 'tips',
    ROOT / 'news',
    ROOT / 'investigations',
]


def public_html_files():
    seen = set()
    for root in PUBLIC_ROOTS:
        if root.is_file():
            files = [root]
        elif root.exists():
            files = root.rglob('*.html')
        else:
            continue
        for path in files:
            if path in seen:
                continue
            seen.add(path)
            yield path


def replace_publication_version(text: str) -> str:
    for old in OLD_PUBLICATION_VERSIONS:
        text = text.replace(old, CURRENT_PUBLICATION)
    return text


def update(path: Path, transform):
    original = path.read_text(encoding='utf-8')
    text = transform(original)
    if text != original:
        path.write_text(text, encoding='utf-8')
        print('UPDATED', path.relative_to(ROOT))
        return 1
    return 0


def patch_home(text: str) -> str:
    text = replace_publication_version(text)
    if '<body>' in text and 'raven-editorial-home' not in text:
        text = text.replace('<body>', '<body class="raven-editorial-home">', 1)
    return text


def patch_html(text: str) -> str:
    return replace_publication_version(text)


def patch_loader_ref(text: str) -> str:
    return replace_publication_version(text)


def patch_governance(text: str) -> str:
    text = replace_publication_version(text)
    old = '<a href="https://majujohor.bernama.com/news-en.php?id=2605960" rel="noopener noreferrer">Bernama · 11 Sep</a>'
    new = ('<a href="https://www.tabunghaji.gov.my/bm/siaran-media/haji/pr11092026_BM" rel="noopener noreferrer">'
           'Tabung Haji · kenyataan rasmi · 11 Sep</a> · '
           '<a href="https://majujohor.bernama.com/news-en.php?id=2605960" rel="noopener noreferrer">Bernama</a>')
    return text.replace(old, new)


def patch_sources(text: str) -> str:
    text = replace_publication_version(text)
    if 'pr11092026_BM' in text:
        return text
    needle = '<ol class="sources-grid">'
    item = ('\n            <li id="s00-seruan-istitoah"><span>A</span>'
            '<a href="https://www.tabunghaji.gov.my/bm/siaran-media/haji/pr11092026_BM" rel="noopener noreferrer">'
            'Seruan Istito’ah — RM15,000 dan giliran automatik</a>'
            '<small>Tabung Haji · kenyataan rasmi · 11 Sep 2026</small></li>')
    return text.replace(needle, needle + item, 1)


if __name__ == '__main__':
    changed = 0
    for path in public_html_files():
        if path == ROOT / 'index.html':
            changed += update(path, patch_home)
        elif path == ROOT / 'investigations/rci-tabung-haji/governance/index.html':
            changed += update(path, patch_governance)
        elif path == ROOT / 'investigations/rci-tabung-haji/sources/index.html':
            changed += update(path, patch_sources)
        else:
            changed += update(path, patch_html)

    for rel in ['assets/js/raven.js', 'assets/js/raven-share.js']:
        path = ROOT / rel
        if path.exists():
            changed += update(path, patch_loader_ref)

    print(f'V4 runtime hardening complete: {changed} files changed')
