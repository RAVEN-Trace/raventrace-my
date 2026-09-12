from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []

def fail(msg):
    errors.append(msg)

# 1) Runtime JavaScript must never own time-sensitive factual case state.
runtime_files = [
    ROOT / 'assets/js/raven-section.js',
    ROOT / 'assets/js/raven-evidence-ux.js',
    ROOT / 'assets/js/raven-publication-core.js',
    ROOT / 'assets/js/raven-narrative.js',
]
forbidden = [
    '.section-cutoff',
    'Jamil Khir',
    'Abdul Azeez',
    'Azmi Ahmad',
    'Prosiding dijadualkan',
    'Didakwa SPRM',
    'Data cut-off',
    'ravenCaseState',
    '9 Sep 2026',
    '9 September 2026',
    '17 September',
    'tiga individu telah didakwa',
    'addSourceRow(',
    'heroDate.textContent',
]
for path in runtime_files:
    if not path.exists():
        fail(f'missing runtime file: {path.relative_to(ROOT)}')
        continue
    text = path.read_text(encoding='utf-8')
    for token in forbidden:
        if token in text:
            fail(f'{path.relative_to(ROOT)} contains forbidden factual runtime token: {token}')

section_js = (ROOT / 'assets/js/raven-section.js').read_text(encoding='utf-8')
if 'data-nav-toggle' in section_js:
    fail('raven-section.js must not own global nav toggle; raven.js is the single controller')

narrative_js = (ROOT / 'assets/js/raven-narrative.js').read_text(encoding='utf-8')
if '__RAVEN_NARRATIVE_RUNTIME_DEPRECATED__' not in narrative_js:
    fail('legacy raven-narrative.js must remain a factual no-op')

# 2) Standalone UX guard must exist.
ux = ROOT / 'assets/css/raven-site-integrity.css'
if not ux.exists():
    fail('missing assets/css/raven-site-integrity.css')
else:
    txt = ux.read_text(encoding='utf-8')
    for token in ['overflow-x: auto', 'position: sticky', '--raven-case-rail-height']:
        if token not in txt:
            fail(f'site integrity CSS missing safeguard: {token}')

# 3) Public navigation + metadata contract for core evergreen pages.
for rel in ['about/index.html', 'methodology/index.html', 'tips/index.html', 'corrections/index.html']:
    s = (ROOT / rel).read_text(encoding='utf-8')
    if 'href="/raventrace-my/investigations/">Siasatan</a>' not in s:
        fail(f'{rel}: primary Siasatan nav must point to /investigations/')
    for meta in ['rel="canonical"', 'property="og:title"', 'property="og:image"', 'name="twitter:card"']:
        if meta not in s:
            fail(f'{rel}: missing metadata contract token {meta}')

# 4) Corrections ledger must acknowledge current material changes.
corrections = (ROOT / 'corrections/index.html').read_text(encoding='utf-8')
for token in ['11 SEP 2026', 'Empat atau lima individu didakwa', 'Pembetulan unit kiraan', 'Runtime lama']:
    if token not in corrections:
        fail(f'corrections ledger missing current material change: {token}')

# 5) Public HTML must not reference corrupt OG v5 or stale runtime generations.
stale_runtime_refs = [
    'raven-publication.js?v=1.1.0',
    'raven-publication.js?v=2.0.0',
    'raven-publication.js?v=2.1.0',
    'raven-publication.js?v=4.3.0',
    'raven-evidence-ux.js?v=2.1.0',
]
for p in ROOT.rglob('*.html'):
    s = p.read_text(encoding='utf-8', errors='ignore')
    if 'rci-tabung-haji-share-v5.jpg' in s:
        fail(f'{p.relative_to(ROOT)} references corrupt legacy OG v5')
    for ref in stale_runtime_refs:
        if ref in s:
            fail(f'{p.relative_to(ROOT)} references stale runtime: {ref}')

# 6) Main current-state boundary remains explicit and static HTML remains at 11 Sep state.
case = (ROOT / 'investigations/rci-tabung-haji/index.html').read_text(encoding='utf-8')
for token in ['Pertuduhan bukan sabitan', 'DIPERTIKAIKAN', '11 Sep 2026']:
    if token not in case:
        fail(f'main CASEFILE missing current evidence boundary: {token}')

home = (ROOT / 'index.html').read_text(encoding='utf-8')
for token in ['11 September 2026', 'empat individu telah berdepan pertuduhan', 'SPRM pula menyebut lima']:
    if token not in home:
        fail(f'homepage missing current static state: {token}')

if errors:
    print('SITE INTEGRITY V1: FAIL')
    for item in errors:
        print('-', item)
    sys.exit(1)

print('SITE INTEGRITY V1: PASS')
