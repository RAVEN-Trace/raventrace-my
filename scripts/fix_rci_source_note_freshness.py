from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'investigations' / 'rci-tabung-haji'
OLD = '<strong>Maklumat disemak hingga:</strong> 10 September 2026 · lewat malam MYT. <strong>Semakan laman:</strong> 7 September 2026 · v18.'
NEW = '<strong>Maklumat disemak hingga:</strong> 11 September 2026 · 23:37 MYT. <strong>Semakan laman:</strong> state sync · 11 September 2026.'

changed = 0
for path in BASE.rglob('*.html'):
    text = path.read_text(encoding='utf-8')
    if OLD not in text:
        continue
    text = text.replace(OLD, NEW)
    path.write_text(text, encoding='utf-8')
    changed += 1
    print('UPDATED', path.relative_to(ROOT))

print('SOURCE NOTE FRESHNESS REPAIR:', changed, 'file(s) changed')
