from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CSS = '/raventrace-my/assets/css/raven-v7-qa-fixes-v1.css?v=1.0.0'
JS = '/raventrace-my/assets/js/raven-route-fixes-v1.js?v=1.0.0'

CSS_TARGETS = [
    ROOT / 'index.html',
    ROOT / 'investigations/rci-tabung-haji/index.html',
    ROOT / 'investigations/rci-tabung-haji/money/index.html',
    ROOT / 'investigations/rci-tabung-haji/narratives/index.html',
    ROOT / 'investigations/rci-tabung-haji/sources/index.html',
    ROOT / 'investigations/rci-tabung-haji/updates/index.html',
    ROOT / 'news/2026/09/11/empat-atau-lima-didakwa-rekod-tidak-seragam/index.html',
]

ROUTE_TARGETS = [
    ROOT / 'index.html',
    ROOT / 'investigations/index.html',
    ROOT / 'investigations/rci-tabung-haji/index.html',
]


def add_css(text: str) -> str:
    text = re.sub(r'<link rel="stylesheet" href="/raventrace-my/assets/css/raven-v7-qa-fixes-v1\.css\?v=[^"]+" data-raven-v7-qa-fixes>\s*', '', text)
    return text.replace('</head>', f'<link rel="stylesheet" href="{CSS}" data-raven-v7-qa-fixes>\n</head>', 1)


def add_js(text: str) -> str:
    text = re.sub(r'<script src="/raventrace-my/assets/js/raven-route-fixes-v1\.js\?v=[^"]+" defer data-raven-route-fixes-v1></script>\s*', '', text)
    return text.replace('</body>', f'<script src="{JS}" defer data-raven-route-fixes-v1></script>\n</body>', 1)


for path in CSS_TARGETS:
    if not path.exists():
        raise SystemExit(f'Missing CSS target: {path.relative_to(ROOT)}')
    text = path.read_text(encoding='utf-8')
    path.write_text(add_css(text), encoding='utf-8')

for path in ROUTE_TARGETS:
    if not path.exists():
        raise SystemExit(f'Missing route target: {path.relative_to(ROOT)}')
    text = path.read_text(encoding='utf-8')
    path.write_text(add_js(text), encoding='utf-8')

print(f'Applied V7 QA fixes to {len(CSS_TARGETS)} contrast surfaces and {len(ROUTE_TARGETS)} route surfaces.')
