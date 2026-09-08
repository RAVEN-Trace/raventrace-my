"""Validate published HTML and fully decode the images crawlers actually receive."""
from pathlib import Path
from urllib.parse import urlsplit
from collections import Counter
from lxml import html
from PIL import Image
from build_rci_share_pages import ROOT, BASE, ORIGIN, SECTIONS

def check():
 source = html.fromstring((ROOT / 'investigations/rci-tabung-haji/index.html').read_text())
 pages = [('casefile', ROOT / 'investigations/rci-tabung-haji/index.html')]
 pages += [(key, ROOT / 'investigations/rci-tabung-haji' / key / 'index.html') for key in SECTIONS]
 for key, path in pages:
  raw = path.read_text()
  doc = html.fromstring(raw)
  def meta(name):
   values = doc.xpath(f'//meta[@property="{name}" or @name="{name}"]/@content')
   assert len(values) == 1, (path, name, values)
   return values[0]
  url = ORIGIN + BASE + (key + '/' if key != 'casefile' else '')
  assert doc.xpath('//link[@rel="canonical"]/@href') == [url]
  assert meta('og:url') == url
  assert meta('og:image') == meta('og:image:secure_url') == meta('twitter:image')
  image = urlsplit(meta('og:image'))
  assert image.netloc == 'raven-trace.github.io' and not image.query
  local = ROOT / image.path.removeprefix('/raventrace-my/')
  with Image.open(local) as im:
   im.load()  # Header recognition/verify() alone missed the corrupt v3 JPEG.
   assert im.format == 'JPEG'
   assert im.size == (int(meta('og:image:width')), int(meta('og:image:height')))
   assert im.width >= 1200
  assert meta('og:image:type') == 'image/jpeg'
  if key != 'casefile':
   assert not doc.xpath('//meta[translate(@http-equiv,"REFSH","refsh")="refresh"]')
   assert 'location.replace' not in raw and 'location.href =' not in raw
   expected = ' '.join(source.get_element_by_id(key).text_content().split())
   actual = ' '.join(doc.get_element_by_id(key).text_content().split())
   assert actual == expected, ('Content drift', key)
   ids = [n.get('id') for n in doc.xpath('//*[@id]')]
   assert len(ids) == len(set(ids)), ('Duplicate IDs', key)
   for href in doc.xpath('//a[starts-with(@href,"#")]/@href'):
    assert href[1:] in ids, ('Missing anchor', key, href)
   for src in doc.xpath('//script/@src | //link[@rel="stylesheet"]/@href'):
    assert (ROOT / urlsplit(src).path.removeprefix('/raventrace-my/')).is_file(), src
  print('PASS', key)
 print('PASS: 10 pages; full image decode, metadata, content preservation, references and assets.')
if __name__ == '__main__':
 check()
