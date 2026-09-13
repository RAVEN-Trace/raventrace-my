"""Rebuild RCI share pages from the casefile. Run after editing case content.
Dependencies: lxml, Pillow. Re-encodes existing artwork without crop or resize.
"""
from pathlib import Path
from copy import deepcopy
from html import escape
import re
from lxml import html
from PIL import Image
ROOT = Path(__file__).resolve().parents[1]
BASE = '/raventrace-my/investigations/rci-tabung-haji/'
ORIGIN = 'https://raven-trace.github.io'
IMAGE_PATH = 'assets/og/rci-tabung-haji-share-v6.jpg'
IMAGE_URL = ORIGIN + '/raventrace-my/' + IMAGE_PATH
SECTIONS = {
 'updates': ('Perkembangan terkini', 'Perkembangan RCI Tabung Haji dalam rekod CASEFILE: siasatan, reman, prosiding dan batas bukti.'),
 'people': ('Individu dan status', 'Individu, jawatan dan status proses dalam rekod RCI Tabung Haji. Kaitan dengan kes bukan bukti kesalahan.'),
 'timeline': ('Kronologi kes', 'Kronologi RCI Tabung Haji: keputusan institusi, siasatan dan prosiding mengikut rekod CASEFILE.'),
 'governance': ('Tadbir urus', 'Dapatan dan persoalan tadbir urus serta pelaporan kewangan Tabung Haji, bersama rujukan sumber.'),
 'money': ('Jejak wang dan angka', 'Bezakan nilai transaksi, kerugian, impairment dan pembiayaan semula dalam rekod Tabung Haji.'),
 'investments': ('14 pelaburan', 'Rekod 14 pelaburan dalam CASEFILE RCI Tabung Haji, dengan status bukti dan rujukan sumber.'),
 'tracks': ('Trek siasatan', 'Bezakan trek siasatan, dapatan institusi dan prosiding dalam CASEFILE RCI Tabung Haji.'),
 'disputed-record': ('Rekod dipertikaikan', 'Versi bercanggah dan jurang rekod RCI Tabung Haji yang masih memerlukan bukti tambahan.'),
 'sources': ('Sumber dan dokumen', 'Rujukan sumber awam, gred bukti dan batas penggunaan rekod dalam CASEFILE RCI Tabung Haji.'),
}
def serialize(node):
 return html.tostring(node, encoding='unicode', method='html')
def build():
 # The repaired v6 social artwork is a canonical social asset generated from the neutral CASEFILE hero.
 # Validate it in place; do not regenerate or overwrite it from the legacy hero artwork.
 with Image.open(ROOT / IMAGE_PATH) as check:
  check.load()
  width, height = check.size
 # Repair older public image URLs too, so cached metadata can fetch valid bytes.
 for name in ['rci-tabung-haji-updates-v2.jpg', 'rci-tabung-haji-updates-v3.jpg']:
  (ROOT / 'assets/og' / name).write_bytes((ROOT / IMAGE_PATH).read_bytes())
 with Image.open(ROOT / 'assets/images/rci-tabung-haji.webp') as original:
  original.load()
  original.save(ROOT / 'assets/og/rci-tabung-haji-updates.png', 'PNG')
 case_path = ROOT / 'investigations/rci-tabung-haji/index.html'
 case = case_path.read_text()
 case = re.sub(r'https://raven-trace\.github\.io/raventrace-my/assets/og/rci-tabung-haji-(?:updates(?:-v[23])?|share-v[45])\.(?:jpg|png)(?:\?[^"\s]*)?', IMAGE_URL, case)
 for key, value in [('width', width), ('height', height)]:
  case = re.sub(r'(<meta property="og:image:' + key + r'" content=")[^"]+', lambda m: m[1] + str(value), case)
 case_path.write_text(case)
 document = html.fromstring(case)
 header = serialize(document.xpath('//header[contains(concat(" ", @class, " "), " site-header ")]')[0])
 footer = serialize(document.xpath('//footer')[0])
 source = document.get_element_by_id('sources')
 date = document.xpath('//*[contains(concat(" ", @class, " "), " date-chip ")]')[0].text_content()
 for key, (label, description) in SECTIONS.items():
  section = deepcopy(document.get_element_by_id(key))
  content = [section] if key == 'sources' else [section, deepcopy(source)]
  local_ids = {'main', 'top'} | {n.get('id') for block in content for n in block.iter() if n.get('id')}
  for block in content:
   for link in block.xpath('.//a[starts-with(@href, "#")]'):
    if link.get('href')[1:] not in local_ids:
     link.set('href', BASE + link.get('href'))
  title = 'RCI Tabung Haji — ' + label
  url = ORIGIN + BASE + key + '/'
  nav = ''.join(f'<a href="{BASE}{slug}/"' + (' aria-current="page"' if key == slug else '') + f'>{escape(name)}</a>' for slug, (name, _) in SECTIONS.items())
  if '/rci-tabung-haji/narratives/' not in nav:
   nav = nav.replace(f'<a href="{BASE}sources/"', f'<a href="{BASE}narratives/">Audit naratif</a><a href="{BASE}sources/"')
  body = '\n'.join(serialize(block) for block in content)
  page = f'''<!doctype html>
<html lang="ms"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} | RAVEN-Trace</title>
<meta name="description" content="{escape(description, quote=True)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article"><meta property="og:site_name" content="RAVEN-Trace Malaysia">
<meta property="og:title" content="{escape(title, quote=True)}">
<meta property="og:description" content="{escape(description, quote=True)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{IMAGE_URL}"><meta property="og:image:secure_url" content="{IMAGE_URL}">
<meta property="og:image:type" content="image/jpeg"><meta property="og:image:width" content="{width}"><meta property="og:image:height" content="{height}">
<meta property="og:image:alt" content="Ilustrasi editorial RCI Tabung Haji — RAVEN-Trace. Bukan foto bukti.">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{escape(title, quote=True)}">
<meta name="twitter:description" content="{escape(description, quote=True)}"><meta name="twitter:image" content="{IMAGE_URL}">
<meta name="twitter:image:alt" content="Ilustrasi editorial RCI Tabung Haji — RAVEN-Trace. Bukan foto bukti.">
<link rel="stylesheet" href="/raventrace-my/assets/css/raven.css?v=3.0.0">
<link rel="stylesheet" href="/raventrace-my/assets/css/raven-section.css?v=1.0.0">
<link rel="stylesheet" href="/raventrace-my/assets/css/raven-unified-v7.css?v=7.0.3" data-raven-unified>
</head><body class="case-share-page">
<a class="skip-link" href="#main">Terus ke kandungan</a>
{header}
<main id="main"><header class="section-intro" id="top"><div class="container">
<p class="section-kicker">RCI TABUNG HAJI · RAVEN-Trace</p><h1>{escape(label)}</h1>
<p>{escape(description)}</p><p class="section-cutoff">{escape(date)}</p>
<p class="section-boundary">Siasatan atau reman bukan pertuduhan. Pertuduhan bukan sabitan.</p>
<div class="btn-row"><button class="btn btn-primary" type="button" data-section-share>Kongsi bahagian ini</button><a class="btn" href="{BASE}#{key}">Baca dalam CASEFILE penuh</a></div>
</div></header>
<nav class="section-links container" aria-label="Bahagian siasatan">{nav}</nav>
<article class="section-content container">{body}</article></main>
{footer}
<script src="/raventrace-my/assets/js/raven-section.js?v=2.2.0" defer></script>
<script src="/raventrace-my/assets/js/raven-share.js?v=2.6.0" data-raven-share defer></script>
</body></html>'''
  output = ROOT / 'investigations/rci-tabung-haji' / key / 'index.html'
  output.parent.mkdir(parents=True, exist_ok=True)
  output.write_text('\n'.join(line.rstrip() for line in page.splitlines()) + '\n')
 print(f'Built {len(SECTIONS)} content pages and a validated {width}x{height} canonical social artwork.')
if __name__ == '__main__':
 build()
