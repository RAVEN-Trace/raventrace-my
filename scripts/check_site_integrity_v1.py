from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []

def fail(msg):
    errors.append(msg)

# 1) Runtime JS must not mutate factual case state.
section_js = (ROOT / 'assets/js/raven-section.js').read_text(encoding='utf-8')
forbidden = [
    '.section-cutoff',
    'Jamil Khir',
    'Abdul Azeez',
    'Azmi Ahmad',
    'Prosiding dijadualkan',
    'Didakwa SPRM',
    'Data cut-off ·',
    'ravenCaseState',
]
for token in forbidden:
    if token in section_js:
        fail(f'raven-section.js contains forbidden factual/runtime-state token: {token}')

if "data-nav-toggle" in section_js:
    fail('raven-section.js must not own global nav toggle; raven.js is the single controller')

# 2) Standalone UX guard must exist.
ux = ROOT / 'assets/css/raven-site-integrity.css'
if not ux.exists():
    fail('missing assets/css/raven-site-integrity.css')
else:
    txt = ux.read_text(encoding='utf-8')
    for token in ['overflow-x: auto', 'position: sticky', '--raven-case-rail-height']:
        if token not in txt:
            fail(f'site integrity CSS missing safeguard: {token}')

# 3) Public navigation contract for core evergreen pages.
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

# 5) No active public HTML may reference corrupt legacy v5 social card.
for p in ROOT.rglob('*.html'):
    s = p.read_text(encoding='utf-8', errors='ignore')
    if 'rci-tabung-haji-share-v5.jpg' in s:
        fail(f'{p.relative_to(ROOT)} references corrupt legacy OG v5')

# 6) Main current-state boundary must remain explicit.
case = (ROOT / 'investigations/rci-tabung-haji/index.html').read_text(encoding='utf-8')
for token in ['Pertuduhan bukan sabitan', 'DIPERTIKAIKAN']:
    if token not in case:
        fail(f'main CASEFILE missing evidence boundary: {token}')

if errors:
    print('SITE INTEGRITY V1: FAIL')
    for item in errors:
        print('-', item)
    sys.exit(1)

print('SITE INTEGRITY V1: PASS')
