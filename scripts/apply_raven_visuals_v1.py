from pathlib import Path
from io import BytesIO
from PIL import Image, ImageOps
import cairosvg
import re

ROOT = Path(__file__).resolve().parents[1]
CSS = '/raventrace-my/assets/css/raven-visuals-v1.css?v=1.0.1'
JS = '/raventrace-my/assets/js/raven-visuals-v1.js?v=1.0.1'

TARGETS = [
    ROOT / 'investigations/rci-tabung-haji/index.html',
    ROOT / 'investigations/rci-tabung-haji/narratives/index.html',
    ROOT / 'investigations/rci-tabung-haji/money/index.html',
    ROOT / 'investigations/rci-tabung-haji/updates/index.html',
    ROOT / 'news/2026/09/11/empat-atau-lima-didakwa-rekod-tidak-seragam/index.html',
]

OG_MAP = {
    ROOT / 'investigations/rci-tabung-haji/narratives/index.html': '/raventrace-my/assets/og/raven-narrative-rm13b-v1-og.jpg',
    ROOT / 'investigations/rci-tabung-haji/money/index.html': '/raventrace-my/assets/og/raven-money-rm13b-v1-og.jpg',
    ROOT / 'investigations/rci-tabung-haji/updates/index.html': '/raventrace-my/assets/og/raven-4-vs-5-v1-og.jpg',
    ROOT / 'news/2026/09/11/empat-atau-lima-didakwa-rekod-tidak-seragam/index.html': '/raventrace-my/assets/og/raven-4-vs-5-v1-og.jpg',
}

DERIVATIVES = {
    ROOT / 'assets/visuals/raven-narrative-rm13b-v1-web.svg': ROOT / 'assets/og/raven-narrative-rm13b-v1-og.jpg',
    ROOT / 'assets/visuals/raven-money-rm13b-v1-web.svg': ROOT / 'assets/og/raven-money-rm13b-v1-og.jpg',
    ROOT / 'assets/visuals/raven-4-vs-5-v1-web.svg': ROOT / 'assets/og/raven-4-vs-5-v1-og.jpg',
}


def add_assets(text: str) -> str:
    text = re.sub(r'<link rel="stylesheet" href="/raventrace-my/assets/css/raven-visuals-v1\.css\?v=[^"]+" data-raven-visuals-v1>\s*', '', text)
    text = re.sub(r'<script src="/raventrace-my/assets/js/raven-visuals-v1\.js\?v=[^"]+" defer data-raven-visuals-v1></script>\s*', '', text)
    text = text.replace('</head>', f'<link rel="stylesheet" href="{CSS}" data-raven-visuals-v1>\n</head>', 1)
    text = text.replace('</body>', f'<script src="{JS}" defer data-raven-visuals-v1></script>\n</body>', 1)
    return text


def set_og(text: str, rel_url: str) -> str:
    absolute = 'https://raven-trace.github.io' + rel_url
    text, n = re.subn(r'(<meta\s+property=["\']og:image["\']\s+content=["\'])[^"\']+(["\'])', rf'\g<1>{absolute}\g<2>', text, count=1)
    if n == 0:
        text = text.replace('</head>', f'<meta property="og:image" content="{absolute}">\n</head>', 1)
    text = re.sub(r'(<meta\s+property=["\']og:image:secure_url["\']\s+content=["\'])[^"\']+(["\'])', rf'\g<1>{absolute}\g<2>', text, count=1)
    text, tw = re.subn(r'(<meta\s+name=["\']twitter:image["\']\s+content=["\'])[^"\']+(["\'])', rf'\g<1>{absolute}\g<2>', text, count=1)
    if tw == 0:
        text = text.replace('</head>', f'<meta name="twitter:image" content="{absolute}">\n</head>', 1)
    text = re.sub(r'(<meta\s+property=["\']og:image:width["\']\s+content=["\'])\d+(["\'])', r'\g<1>1200\g<2>', text)
    text = re.sub(r'(<meta\s+property=["\']og:image:height["\']\s+content=["\'])\d+(["\'])', r'\g<1>630\g<2>', text)
    return text


for src, dst in DERIVATIVES.items():
    if not src.exists():
        raise SystemExit(f'Missing SVG source: {src.relative_to(ROOT)}')
    dst.parent.mkdir(parents=True, exist_ok=True)
    png_bytes = cairosvg.svg2png(url=str(src), output_width=1200, output_height=675)
    with Image.open(BytesIO(png_bytes)) as image:
        image = image.convert('RGB')
        og = ImageOps.fit(image, (1200, 630), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
        og.save(dst, 'JPEG', quality=90, optimize=True, progressive=True)

for path in TARGETS:
    if not path.exists():
        raise SystemExit(f'Missing public target: {path.relative_to(ROOT)}')
    text = path.read_text(encoding='utf-8')
    text = add_assets(text)
    if path in OG_MAP:
        text = set_og(text, OG_MAP[path])
    path.write_text(text, encoding='utf-8')

print('Raven Narrative Visual System V1.0.1 applied to 5 public surfaces and 3 OG derivatives generated from SVG.')
