from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CSS = '<link rel="stylesheet" href="/raventrace-my/assets/css/raven-signal-v6.css?v=6.0.0" data-raven-signal-v6>'
JS = '<script src="/raventrace-my/assets/js/raven-signal-v6.js?v=6.0.0" defer data-raven-signal-v6></script>'
NARRATIVE_POLISH = '<link rel="stylesheet" href="/raventrace-my/assets/css/raven-signal-v6-polish.css?v=6.0.1" data-raven-signal-v6-polish>'
SECTION_JS = '/raventrace-my/assets/js/raven-section.js?v=2.1.0'
NARRATIVE_REL = Path('investigations/rci-tabung-haji/narratives/index.html')

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


def normalize_narrative_rule(text: str) -> str:
    """Keep the Narrative closing principle inside the article/main, never after the footer."""
    pattern = re.compile(
        r'<section class="case-section" id="narrative-rule">.*?</section>',
        re.S,
    )
    match = pattern.search(text)
    if not match:
        return text

    block = match.group(0)
    text = text[:match.start()] + text[match.end():]
    anchor = '</article></main>'
    if anchor not in text:
        raise RuntimeError('Narrative closing main/article anchor missing')
    text = text.replace(anchor, f'{block}\n{anchor}', 1)
    return text


paths = []
for root in PUBLIC_ROOTS:
    if root.is_file():
        paths.append(root)
    elif root.exists():
        paths.extend(p for p in root.rglob('index.html') if is_live_public(p))

seen = set()
changed = []
for path in paths:
    path = path.resolve()
    if path in seen:
        continue
    seen.add(path)
    text = path.read_text(encoding='utf-8')
    original = text

    # Remove older Signal tags before inserting the canonical V6 pair.
    text = re.sub(r'\s*<link[^>]+data-raven-signal-v6(?!-polish)[^>]*>\s*', '\n', text)
    text = re.sub(r'\s*<script[^>]+data-raven-signal-v6[^>]*></script>\s*', '\n', text)
    text = re.sub(r'\s*<link[^>]+data-raven-signal-v6-polish[^>]*>\s*', '\n', text)

    # Standalone investigation pages use raven-section.js. Canonicalise its
    # cache key so the horizontal-only tab-centering fix reaches mobile users.
    text = re.sub(
        r'/raventrace-my/assets/js/raven-section\.js\?v=[^"\']+',
        SECTION_JS,
        text,
    )

    # Historical migration scripts once placed the Narrative closing principle
    # after the footer. Normalize the live page into semantic document order.
    is_narrative = path.relative_to(ROOT) == NARRATIVE_REL
    if is_narrative:
        text = normalize_narrative_rule(text)

    if '</head>' not in text or '</body>' not in text:
        raise RuntimeError(f'Missing closing head/body in {path.relative_to(ROOT)}')

    head_assets = CSS
    if is_narrative:
        head_assets += '\n' + NARRATIVE_POLISH
    text = text.replace('</head>', f'{head_assets}\n</head>', 1)
    # Put Signal last so it can progressively enhance V5/Narrative V5.2.1 output.
    text = text.replace('</body>', f'{JS}\n</body>', 1)

    if text.count('data-raven-signal-v6') != (3 if is_narrative else 2):
        raise RuntimeError(f'Unexpected Signal tag count in {path.relative_to(ROOT)}')

    if is_narrative:
        if text.count('data-raven-signal-v6-polish') != 1:
            raise RuntimeError('Narrative polish stylesheet must appear exactly once')
        rule_pos = text.find('id="narrative-rule"')
        main_end = text.find('</main>')
        footer_pos = text.find('<footer')
        if not (0 <= rule_pos < main_end < footer_pos):
            raise RuntimeError('Narrative rule must be inside main and before footer')

    if text != original:
        path.write_text(text, encoding='utf-8')
        changed.append(path.relative_to(ROOT).as_posix())

print(f'RAVEN SIGNAL V6: {len(changed)} live public page(s) changed')
for item in changed:
    print(item)
