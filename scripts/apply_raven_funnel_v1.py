from pathlib import Path
import html
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
CSS = '<link rel="stylesheet" href="/raventrace-my/assets/css/raven-funnel-v1.css?v=1.0.0" data-raven-funnel-v1>'
JS = '<script src="/raventrace-my/assets/js/raven-funnel-v1.js?v=1.0.0" defer data-raven-funnel-v1></script>'
NARRATIVE = ROOT / 'investigations' / 'rci-tabung-haji' / 'narratives' / 'index.html'

PUBLIC_ROOTS = [
    ROOT / 'index.html',
    ROOT / 'about',
    ROOT / 'corrections',
    ROOT / 'investigations',
    ROOT / 'methodology',
    ROOT / 'news',
    ROOT / 'tips',
]


def is_live_public(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    lowered = [p.lower() for p in rel.parts]
    if 'research' in lowered:
        return False
    if any(p.startswith('.') for p in rel.parts):
        return False
    return path.name == 'index.html'


def strip_tags(value: str) -> str:
    return html.unescape(re.sub(r'<[^>]+>', '', value))


def slugify(value: str, prefix: str) -> str:
    value = unicodedata.normalize('NFKD', strip_tags(value))
    value = value.encode('ascii', 'ignore').decode('ascii').lower()
    value = re.sub(r'[^a-z0-9]+', '-', value).strip('-')
    value = re.sub(r'-{2,}', '-', value)
    value = value[:72].rstrip('-') or 'item'
    return f'{prefix}{value}'


def unique_slug(base: str, used: set[str]) -> str:
    candidate = base
    n = 2
    while candidate in used:
        candidate = f'{base}-{n}'
        n += 1
    used.add(candidate)
    return candidate


def add_narrative_ids(text: str) -> str:
    section_re = re.compile(
        r'(<section class="case-section">\s*<div class="section-marker"><span>02</span><p>Naratif vs bukti</p></div>.*?<div class="control-grid">)(.*?)(</div></section>\s*<section class="case-section"><div class="section-marker"><span>03</span>)',
        re.S,
    )
    match = section_re.search(text)
    if not match:
        raise RuntimeError('Narrative evidence grid not found')

    body = match.group(2)
    used: set[str] = set()

    def repl_article(m: re.Match[str]) -> str:
        attrs = m.group(1) or ''
        title = m.group(2)
        existing = re.search(r'\bid="([^"]+)"', attrs)
        if existing:
            used.add(existing.group(1))
            return m.group(0)
        slug = unique_slug(slugify(title, 'naratif-'), used)
        return f'<article id="{slug}"{attrs}><h3>{title}</h3>'

    body2 = re.sub(r'<article([^>]*)><h3>(.*?)</h3>', repl_article, body, flags=re.S)
    if body2 == body:
        raise RuntimeError('No narrative article IDs were added or detected')
    return text[:match.start(2)] + body2 + text[match.end(2):]


def add_source_ids(text: str) -> str:
    source_re = re.compile(
        r'(<section class="case-section source-room" id="sources">.*?<ol class="sources-grid">)(.*?)(</ol>)',
        re.S,
    )
    match = source_re.search(text)
    if not match:
        raise RuntimeError('Narrative source room not found')

    body = match.group(2)
    used: set[str] = set()

    def repl_li(m: re.Match[str]) -> str:
        attrs = m.group(1) or ''
        inner = m.group(2)
        existing = re.search(r'\bid="([^"]+)"', attrs)
        if existing:
            used.add(existing.group(1))
            return m.group(0)
        anchor = re.search(r'<a[^>]*>(.*?)</a>', inner, re.S)
        label = anchor.group(1) if anchor else inner
        slug = unique_slug(slugify(label, 'source-'), used)
        return f'<li id="{slug}"{attrs}>{inner}</li>'

    body2 = re.sub(r'<li([^>]*)>(.*?)</li>', repl_li, body, flags=re.S)
    if body2 == body:
        raise RuntimeError('No source IDs were added or detected')
    return text[:match.start(2)] + body2 + text[match.end(2):]


def wire_assets(text: str) -> str:
    text = re.sub(r'\s*<link[^>]+data-raven-funnel-v1[^>]*>\s*', '\n', text)
    text = re.sub(r'\s*<script[^>]+data-raven-funnel-v1[^>]*></script>\s*', '\n', text)
    if '</head>' not in text or '</body>' not in text:
        raise RuntimeError('Missing head/body close')
    text = text.replace('</head>', f'{CSS}\n</head>', 1)
    text = text.replace('</body>', f'{JS}\n</body>', 1)
    return text


paths: list[Path] = []
for root in PUBLIC_ROOTS:
    if root.is_file():
        paths.append(root)
    elif root.exists():
        paths.extend(p for p in root.rglob('index.html') if is_live_public(p))

changed = []
seen = set()
for path in paths:
    path = path.resolve()
    if path in seen:
        continue
    seen.add(path)
    text = path.read_text(encoding='utf-8')
    original = text

    if path == NARRATIVE.resolve():
        text = add_narrative_ids(text)
        text = add_source_ids(text)

    text = wire_assets(text)
    if text.count('data-raven-funnel-v1') != 2:
        raise RuntimeError(f'Funnel assets not canonical in {path.relative_to(ROOT)}')

    if text != original:
        path.write_text(text, encoding='utf-8')
        changed.append(path.relative_to(ROOT).as_posix())

# Stable deep links are mandatory for the current Narrative set.
narrative = NARRATIVE.read_text(encoding='utf-8')
ids = re.findall(r'<article id="(naratif-[^"]+)"', narrative)
source_ids = re.findall(r'<li id="(source-[^"]+)"', narrative)
if len(ids) < 8 or len(ids) != len(set(ids)):
    raise RuntimeError(f'Expected >=8 unique narrative deep links, got {len(ids)}')
if len(source_ids) < 5 or len(source_ids) != len(set(source_ids)):
    raise RuntimeError(f'Expected >=5 unique source deep links, got {len(source_ids)}')

print(f'RAVEN FUNNEL V1: {len(changed)} public page(s) changed')
print(f'Narrative deep links: {len(ids)}')
for item in ids:
    print(f'  #{item}')
print(f'Source anchors: {len(source_ids)}')
