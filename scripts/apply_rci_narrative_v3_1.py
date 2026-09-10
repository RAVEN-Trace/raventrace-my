from pathlib import Path

path = Path('investigations/rci-tabung-haji/narratives/index.html')
text = path.read_text(encoding='utf-8')

css_tag = '<link rel="stylesheet" href="/raventrace-my/assets/css/raven-narrative-v3-1.css?v=3.1.0">'
js_tag = '<script src="/raventrace-my/assets/js/raven-narrative-v3-1.js?v=3.1.0" defer></script>'

if css_tag not in text:
    anchor = '<link rel="stylesheet" href="/raventrace-my/assets/css/raven-section.css?v=1.0.0">'
    if anchor not in text:
        raise SystemExit('section CSS anchor not found')
    text = text.replace(anchor, anchor + css_tag, 1)

if js_tag not in text:
    if '</body>' not in text:
        raise SystemExit('body end not found')
    text = text.replace('</body>', js_tag + '</body>', 1)

# Publication copy tweak: V3.1 is UX only; evidence model remains V3.
old = '<strong>V3 · Verdict boleh berubah</strong>'
new = '<strong>V3 · Verdict boleh berubah</strong>'
if old not in text:
    raise SystemExit('V3 evidence gate marker not found')

path.write_text(text, encoding='utf-8')

# QA
out = path.read_text(encoding='utf-8')
assert 'raven-narrative-v3-1.css?v=3.1.0' in out
assert 'raven-narrative-v3-1.js?v=3.1.0' in out
assert 'Apa yang boleh mengubah verdict?' in out
assert 'Confidence:' in out
assert 'Last verified:' in out
assert 'Pertuduhan bukan sabitan.' in out
print('Narrative Audit UX V3.1 injection PASS')
