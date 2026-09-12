from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PHOTO = ROOT / 'assets/photos/sprm-hq-putrajaya.jpg'

public = []
for base in ['index.html','about','methodology','corrections','tips','news','investigations']:
    p = ROOT / base
    if p.is_file(): public.append(p)
    elif p.exists(): public.extend(p.rglob('*.html'))

errors = []
for p in public:
    s = p.read_text(encoding='utf-8')
    rel = p.relative_to(ROOT)
    if 'href="/raventrace-my/investigations/rci-tabung-haji/">Siasatan</a>' in s:
        errors.append(f'{rel}: top-level Siasatan still bypasses investigation desk')
    if 'upload.wikimedia.org/wikipedia/commons' in s and 'Anti-Corruption_Commission-01.jpg' in s:
        errors.append(f'{rel}: external Wikimedia photo hotlink remains')
    if 'rci-tabung-haji-share-v5.jpg' in s:
        errors.append(f'{rel}: corrupt OG v5 is referenced')

rci = ROOT / 'investigations/rci-tabung-haji'
for p in rci.glob('*/index.html'):
    s = p.read_text(encoding='utf-8')
    rel = p.relative_to(ROOT)
    if 'raven-section.js?v=1.0.0' in s:
        errors.append(f'{rel}: stale section controller cache key')
    if 'raven-section.js?v=2.0.0' not in s:
        errors.append(f'{rel}: section controller v2 missing')
    if 'data-raven-site-integrity' not in s:
        errors.append(f'{rel}: site integrity CSS missing')
    if 'lytcdn.com/lyt.js' not in s:
        errors.append(f'{rel}: analytics snippet missing')

section_js = (ROOT / 'assets/js/raven-section.js').read_text(encoding='utf-8')
for forbidden in ['section-cutoff', 'Jamil Khir', 'Abdul Azeez', 'Azmi Ahmad', 'updatePerson(', 'addSourceRow(']:
    if forbidden in section_js:
        errors.append(f'raven-section.js: factual mutation token remains: {forbidden}')

if not PHOTO.exists():
    errors.append('assets/photos/sprm-hq-putrajaya.jpg: missing')
elif PHOTO.stat().st_size < 100_000:
    errors.append(f'assets/photos/sprm-hq-putrajaya.jpg: unexpectedly small ({PHOTO.stat().st_size} bytes)')
else:
    data = PHOTO.read_bytes()[:3]
    if data != b'\xff\xd8\xff':
        errors.append('assets/photos/sprm-hq-putrajaya.jpg: not JPEG')

credits = (ROOT / 'assets/PHOTO_CREDITS.md').read_text(encoding='utf-8')
for token in ['CEphoto, Uwe Aranas', 'CC BY-SA 3.0', 'assets/photos/sprm-hq-putrajaya.jpg']:
    if token not in credits:
        errors.append(f'PHOTO_CREDITS.md: missing {token}')

if errors:
    print('\n'.join('FAIL: ' + e for e in errors))
    raise SystemExit(1)
print(f'PASS: Phase 2 publication hygiene across {len(public)} public HTML pages')
