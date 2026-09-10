from pathlib import Path

TARGET = '/raventrace-my/investigations/rci-tabung-haji/narratives/'

def replace_once(path, old, new):
    p = Path(path)
    s = p.read_text(encoding='utf-8')
    if TARGET in s:
        print(f'{path}: already integrated')
        return False
    if old not in s:
        raise SystemExit(f'{path}: integration anchor not found')
    p.write_text(s.replace(old, new, 1), encoding='utf-8')
    print(f'{path}: integrated')
    return True

replace_once(
    'investigations/rci-tabung-haji/index.html',
    '<a href="#controls">Audit</a><a href="#sources">Sumber</a>',
    '<a href="/raventrace-my/investigations/rci-tabung-haji/narratives/">Audit naratif</a><a href="#controls">Audit bukti</a><a href="#sources">Sumber</a>'
)

replace_once(
    'investigations/index.html',
    '<a class="board-row" href="/raventrace-my/investigations/rci-tabung-haji/#sources"><span>06</span><strong>Sumber & dokumen</strong><em>Dokumen dan laporan sokongan</em></a>',
    '<a class="board-row" href="/raventrace-my/investigations/rci-tabung-haji/narratives/"><span>06</span><strong>Audit naratif politik</strong><em>Siapa kata apa — dan apa rekod tunjuk?</em></a><a class="board-row" href="/raventrace-my/investigations/rci-tabung-haji/#sources"><span>07</span><strong>Sumber & dokumen</strong><em>Dokumen dan laporan sokongan</em></a>'
)

# QA: both discovery surfaces must expose the new audit page.
for path in ['investigations/rci-tabung-haji/index.html', 'investigations/index.html']:
    text = Path(path).read_text(encoding='utf-8')
    if TARGET not in text:
        raise SystemExit(f'{path}: QA failed — narrative audit link missing')
print('RCI narrative integration QA passed')
