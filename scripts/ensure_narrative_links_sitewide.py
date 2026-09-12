from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
HUB = '/raventrace-my/investigations/rci-tabung-haji/narratives/'
SUB = '/raventrace-my/investigations/rci-tabung-haji/narratives/political-social-media/'
NAV_LINK = f'<a class="narrative-nav-link" href="{HUB}">Audit Naratif</a>'
FOOT_LINK = f'<a class="narrative-footer-link" href="{HUB}">Audit Naratif</a>'

PUBLIC_ROOTS = {
    'about', 'corrections', 'investigations', 'methodology', 'news', 'tips'
}

NAV_RE = re.compile(r'(<nav\b[^>]*class="[^"]*\bsite-nav\b[^"]*"[^>]*>)(.*?)(</nav>)', re.S)
FOOT_RE = re.compile(r'(<nav\b[^>]*class="[^"]*\bfooter-nav\b[^"]*"[^>]*>)(.*?)(</nav>)', re.S)
METHODOLOGY_ANCHOR_RE = re.compile(r'<a\b[^>]*href="/raventrace-my/methodology/"[^>]*>')
INVESTIGATIONS_ANCHOR_RE = re.compile(r'(<a\b[^>]*href="/raventrace-my/investigations/"[^>]*>.*?</a>)', re.S)

CONTEXT_BLOCK = f'''\n    <section class="section paper rule-top narrative-route" data-narrative-route>
      <div class="container evidence-band">
        <div><p class="eyebrow">Audit Naratif</p><h2>Fakta cerita satu hal. Cara cerita dibingkaikan satu hal lagi.</h2></div>
        <div><p>Raven asingkan bukti daripada framing, slogan, pilihan bahasa dan signal media sosial supaya pembaca boleh melihat bukan sahaja <em>apa yang berlaku</em>, tetapi juga <em>bagaimana cerita itu cuba dibentuk</em>.</p><p><a href="{HUB}">Buka Audit Naratif RCI →</a> · <a href="{SUB}">Politik + media sosial →</a></p></div>
      </div>
    </section>\n'''


def public_html_files():
    files = [ROOT / 'index.html']
    for root_name in PUBLIC_ROOTS:
        root = ROOT / root_name
        if root.exists():
            files.extend(sorted(root.rglob('*.html')))
    # deterministic unique list
    return list(dict.fromkeys(files))


def ensure_primary_nav(text: str, rel: str) -> str:
    m = NAV_RE.search(text)
    if not m:
        raise SystemExit(f'Primary site-nav missing in {rel}')
    body = m.group(2)
    if HUB in body:
        return text
    target = METHODOLOGY_ANCHOR_RE.search(body)
    if target:
        body = body[:target.start()] + NAV_LINK + body[target.start():]
    else:
        body = body + NAV_LINK
    return text[:m.start()] + m.group(1) + body + m.group(3) + text[m.end():]


def ensure_footer_nav(text: str) -> str:
    m = FOOT_RE.search(text)
    if not m:
        return text
    body = m.group(2)
    if HUB in body:
        return text
    target = INVESTIGATIONS_ANCHOR_RE.search(body)
    if target:
        body = body[:target.end()] + FOOT_LINK + body[target.end():]
    else:
        body = body + FOOT_LINK
    return text[:m.start()] + m.group(1) + body + m.group(3) + text[m.end():]


def needs_contextual_route(rel: str) -> bool:
    if rel.startswith('investigations/rci-tabung-haji/') and '/narratives/' not in rel:
        return True
    if rel.startswith('news/2026/') and rel.endswith('/index.html'):
        return True
    return False


def ensure_contextual_route(text: str, rel: str) -> str:
    if not needs_contextual_route(rel):
        return text
    if 'data-narrative-route' in text and SUB in text:
        return text
    marker = '</main>'
    if marker not in text:
        raise SystemExit(f'</main> missing in contextual page {rel}')
    return text.replace(marker, CONTEXT_BLOCK + marker, 1)


changed = []
for path in public_html_files():
    rel = path.relative_to(ROOT).as_posix()
    text = path.read_text(encoding='utf-8')
    original = text
    text = ensure_primary_nav(text, rel)
    text = ensure_footer_nav(text)
    text = ensure_contextual_route(text, rel)
    if text != original:
        path.write_text(text, encoding='utf-8')
        changed.append(rel)

# Coverage gate inside the migration itself.
for path in public_html_files():
    rel = path.relative_to(ROOT).as_posix()
    text = path.read_text(encoding='utf-8')
    nav = NAV_RE.search(text)
    if not nav or HUB not in nav.group(2):
        raise SystemExit(f'QA failed: Audit Naratif absent from primary nav: {rel}')
    if needs_contextual_route(rel) and SUB not in text:
        raise SystemExit(f'QA failed: contextual narrative subpage absent: {rel}')

print(f'Narrative discoverability PASS across {len(public_html_files())} public HTML pages')
for rel in changed:
    print('updated:', rel)
