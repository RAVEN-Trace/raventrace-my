from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'investigations' / 'rci-tabung-haji'
V6 = 'https://raven-trace.github.io/raventrace-my/assets/og/rci-tabung-haji-share-v6.jpg'

html_files = [BASE / 'index.html'] + list(BASE.glob('*/index.html'))

for path in html_files:
    s = path.read_text()
    # Migrate any older RCI social preview reference to the repaired v6 asset.
    s = re.sub(
        r'https://raven-trace\.github\.io/raventrace-my/assets/og/rci-tabung-haji-(?:share-v[45]|updates(?:-v[23])?)\.(?:jpg|png)',
        V6,
        s,
    )
    # v6 is a validated 1200x630 JPEG. Update dimensions where these tags exist.
    s = re.sub(r'(<meta property="og:image:width" content=")[^"]+', r'\g<1>1200', s)
    s = re.sub(r'(<meta property="og:image:height" content=")[^"]+', r'\g<1>630', s)
    path.write_text(s)

# Update the public Updates page metadata and NEXT queue so it matches the verified 10 Sep state.
updates = BASE / 'updates' / 'index.html'
s = updates.read_text()
s = s.replace(
    'Perkembangan terkini RCI Tabung Haji: mahkamah, siasatan, reman, claim yang diuji dan batas bukti. Disemak hingga 9 September 2026.',
    'Perkembangan terkini RCI Tabung Haji: mahkamah, siasatan, reman, dakwaan yang diuji dan batas bukti. Disemak hingga 10 September 2026.'
)
s = s.replace(
    'Dakwaan → kami semak → apa yang terbukti. Perkembangan RCI Tabung Haji disemak hingga 9 September 2026.',
    'Dakwaan → kami semak → apa yang terbukti. Perkembangan RCI Tabung Haji disemak hingga 10 September 2026.'
)
s = s.replace(
    '<h2>Apa yang Raven tunggu seterusnya?</h2><p class="section-lead"><strong>11 Sep:</strong> DAKWAAN berkaitan Azmi. <strong>17 Sep:</strong> DAKWAAN berkaitan Jamil. Kedua-duanya kekal DAKWAAN sehingga rekod mahkamah atau pengesahan rasmi tersedia. <strong>24 Sep:</strong> prosiding seterusnya bagi Adi Azuan selepas pertuduhan terdahulu ditunda.</p>',
    '<h2>Apa yang Raven tunggu seterusnya?</h2><p class="section-lead"><strong>11 Sep:</strong> pantau keputusan reman dua individu dalam trek AMLA serta sebarang perkembangan PDRM berkaitan hibah. <strong>Jamil Khir:</strong> laporan awal menyebut kemungkinan tindakan mahkamah pada 17 September, tetapi tarikh, seksyen dan pertuduhan sebenar masih belum disahkan. <strong>24 Sep:</strong> prosiding seterusnya bagi Adi Azuan selepas pertuduhan terdahulu ditunda.</p>'
)
updates.write_text(s)

# QA: enforce critical public surfaces, but do not require optional dimension tags on every section page.
main = (BASE / 'index.html').read_text()
updates_text = updates.read_text()
assert V6 in main
assert 'share-v4.jpg' not in main
assert 'og:image:width" content="1200"' in main
assert 'og:image:height" content="630"' in main
assert V6 in updates_text
assert 'Disemak hingga 10 September 2026.' in updates_text
assert '<strong>11 Sep:</strong> DAKWAAN berkaitan Azmi.' not in updates_text
for path in html_files:
    text = path.read_text()
    assert 'share-v4.jpg' not in text
    assert 'share-v5.jpg' not in text
print(f'RCI OG metadata v6 QA PASS across {len(html_files)} pages')
