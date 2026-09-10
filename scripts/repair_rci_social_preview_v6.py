from pathlib import Path
import re
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'assets/images/rci-tabung-haji.webp'
DST = ROOT / 'assets/og/rci-tabung-haji-share-v6.jpg'
TARGET = (1200, 630)

with Image.open(SRC) as im:
    im = im.convert('RGB')
    sw, sh = im.size
    target_ratio = TARGET[0] / TARGET[1]
    src_ratio = sw / sh
    if src_ratio > target_ratio:
        nw = round(sh * target_ratio)
        left = (sw - nw) // 2
        im = im.crop((left, 0, left + nw, sh))
    else:
        nh = round(sw / target_ratio)
        top = max(0, (sh - nh) // 2)
        im = im.crop((0, top, sw, top + nh))
    im = im.resize(TARGET, Image.Resampling.LANCZOS)
    DST.parent.mkdir(parents=True, exist_ok=True)
    im.save(DST, 'JPEG', quality=92, optimize=True, progressive=True)

with Image.open(DST) as check:
    check.load()
    assert check.format == 'JPEG'
    assert check.size == TARGET

old = 'rci-tabung-haji-share-v6.jpg'
new = 'rci-tabung-haji-share-v6.jpg'
for path in ROOT.rglob('*'):
    if not path.is_file() or path == DST:
        continue
    if path.suffix.lower() not in {'.html', '.py', '.md', '.yml', '.yaml', '.js'}:
        continue
    try:
        text = path.read_text()
    except UnicodeDecodeError:
        continue
    if old in text:
        path.write_text(text.replace(old, new))

# Keep builder metadata dimensions explicit and current.
builder = ROOT / 'scripts/build_rci_share_pages.py'
text = builder.read_text()
text = text.replace('approved v5 editorial artwork', 'repaired v6 social artwork')
text = text.replace('canonical social asset', 'canonical social asset generated from the neutral CASEFILE hero')
builder.write_text(text)

print(f'Created {DST.relative_to(ROOT)}: {DST.stat().st_size} bytes, 1200x630 JPEG')
