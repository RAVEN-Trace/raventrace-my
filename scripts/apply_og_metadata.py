import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://raven-trace.github.io/raventrace-my/assets/og/'

STORIES = [
    {
        'path': 'news/2026/09/06/jamil-khir-reman-checkpoint/index.html',
        'image': 'jamil-khir-reman-20260906-v1.jpg',
        'headline': 'Reman Jamil Khir tamat 6 Sep — status seterusnya belum disahkan',
        'description': 'Reman lima hari dijadual berakhir 6 September. Setakat semakan RAVEN-Trace, belum ada rekod awam yang mengesahkan pembebasan, lanjutan reman atau pertuduhan.',
        'alt': 'RAVEN-Trace News Card: reman Jamil Khir tamat 6 September, status seterusnya belum disahkan',
        'canonical': 'https://raven-trace.github.io/raventrace-my/news/2026/09/06/jamil-khir-reman-checkpoint/',
        'published': '2026-09-06T06:00:00+08:00',
        'modified': '2026-09-06T14:20:00+08:00',
    },
    {
        'path': 'news/2026/09/05/ketelusan-siasatan-tabung-haji/index.html',
        'image': 'ketelusan-siasatan-th-20260905-v1.jpg',
        'headline': 'Beberapa responden mahu siasatan TH lebih telus',
        'description': 'RTM melaporkan beberapa responden mahu hasil siasatan diterangkan lebih terbuka, audit lebih berkala dan komunikasi lebih jelas. Ini vox-pop, bukan tinjauan seluruh Malaysia.',
        'alt': 'RAVEN-Trace News Card: beberapa responden mahu siasatan Tabung Haji lebih telus, vox-pop bukan tinjauan nasional',
        'canonical': 'https://raven-trace.github.io/raventrace-my/news/2026/09/05/ketelusan-siasatan-tabung-haji/',
        'published': '2026-09-05T12:00:00+08:00',
    },
    {
        'path': 'news/2026/09/04/madinah-rashid-rekod-bercanggah/index.html',
        'image': 'madinah-rashid-disputed-20260904-v1.jpg',
        'headline': 'Madinah vs Rashid: apa yang disepakati, apa yang masih bercanggah',
        'description': 'Sapina dan 75 jawapan bertulis disokong kedua-dua versi. Pertikaian kekal pada apa yang berlaku ketika Madinah hadir dan isu keterangan lisan.',
        'alt': 'RAVEN-Trace News Card: Madinah dan Rashid memberi dua versi, rekod prosiding RCI masih belum lengkap',
        'canonical': 'https://raven-trace.github.io/raventrace-my/news/2026/09/04/madinah-rashid-rekod-bercanggah/',
        'published': '2026-09-04T12:00:00+08:00',
    },
    {
        'path': 'news/2026/09/03/reformasi-tadbir-urus-tabung-haji/index.html',
        'image': 'reformasi-th-20260903-v1.jpg',
        'headline': '19 daripada 25 syor RCI selesai; pindaan Akta TH belum muktamad',
        'description': 'TH berkata enam syor lagi masih dalam tindakan. Pindaan Akta 535 melepasi 90% di peringkat dalaman tetapi masih perlu melalui proses kerajaan dan Parlimen.',
        'alt': 'RAVEN-Trace News Card: 19 daripada 25 syor RCI dilapor selesai, pindaan Akta Tabung Haji belum muktamad',
        'canonical': 'https://raven-trace.github.io/raventrace-my/news/2026/09/03/reformasi-tadbir-urus-tabung-haji/',
        'published': '2026-09-03T12:00:00+08:00',
        'modified': '2026-09-04T18:00:00+08:00',
    },
    {
        'path': 'news/2026/09/03/thp-bina-rm72000/index.html',
        'image': 'thp-bina-court-20260903-v1.jpg',
        'headline': 'Dua bekas pengurus THP Bina didakwa — pertuduhan bukan sabitan',
        'description': 'Nasahruddin Ahmad dan Tengku Kamarolhisham Tengku Kamaruddin menghadapi pertuduhan berkaitan RM72,000. Kedua-duanya mengaku tidak bersalah.',
        'alt': 'RAVEN-Trace News Card: dua bekas pengurus THP Bina didakwa, pertuduhan bukan sabitan',
        'canonical': 'https://raven-trace.github.io/raventrace-my/news/2026/09/03/thp-bina-rm72000/',
        'published': '2026-09-03T15:00:00+08:00',
    },
]


def remove_meta(text, key, value):
    pattern = rf'<meta\s+{re.escape(key)}=["\']{re.escape(value)}["\'][^>]*>'
    return re.sub(pattern, '', text, flags=re.I)


def image_meta(story):
    image = BASE + story['image']
    alt = story['alt'].replace('"', '&quot;')
    return (
        f'<meta property="og:image" content="{image}">'
        f'<meta property="og:image:secure_url" content="{image}">'
        f'<meta property="og:image:type" content="image/jpeg">'
        f'<meta property="og:image:width" content="1200">'
        f'<meta property="og:image:height" content="630">'
        f'<meta property="og:image:alt" content="{alt}">'
    )


def twitter_meta(story):
    image = BASE + story['image']
    title = story['headline'].replace('"', '&quot;')
    desc = story['description'].replace('"', '&quot;')
    alt = story['alt'].replace('"', '&quot;')
    return (
        '<meta name="twitter:card" content="summary_large_image">'
        f'<meta name="twitter:title" content="{title}">'
        f'<meta name="twitter:description" content="{desc}">'
        f'<meta name="twitter:image" content="{image}">'
        f'<meta name="twitter:image:alt" content="{alt}">'
    )


def json_ld(story):
    payload = {
        '@context': 'https://schema.org',
        '@type': 'NewsArticle',
        'headline': story['headline'],
        'datePublished': story['published'],
        'mainEntityOfPage': story['canonical'],
        'publisher': {'@type': 'Organization', 'name': 'RAVEN-Trace Malaysia'},
        'image': [BASE + story['image']],
    }
    if story.get('modified'):
        payload['dateModified'] = story['modified']
    return '<script type="application/ld+json">' + json.dumps(payload, ensure_ascii=False, separators=(',', ':')) + '</script>'


def patch(story):
    path = ROOT / story['path']
    text = path.read_text(encoding='utf-8')

    for prop in ['og:image', 'og:image:secure_url', 'og:image:type', 'og:image:width', 'og:image:height', 'og:image:alt']:
        text = remove_meta(text, 'property', prop)
    for name in ['twitter:card', 'twitter:title', 'twitter:description', 'twitter:image', 'twitter:image:alt']:
        text = remove_meta(text, 'name', name)

    marker = re.search(r'<meta\s+property=["\']og:url["\'][^>]*>', text, flags=re.I)
    if not marker:
        raise RuntimeError(f'og:url missing: {story["path"]}')
    insert_at = marker.end()
    text = text[:insert_at] + image_meta(story) + twitter_meta(story) + text[insert_at:]

    text = re.sub(r'<script\s+type=["\']application/ld\+json["\']>.*?</script>', '', text, flags=re.I | re.S)
    text = text.replace('</head>', json_ld(story) + '</head>', 1)

    path.write_text(text, encoding='utf-8')
    print(f'patched {story["path"]} -> {story["image"]}')


def patch_runtime_versions():
    raven = ROOT / 'assets/js/raven.js'
    text = raven.read_text(encoding='utf-8')
    old = '/raventrace-my/assets/js/raven-share.js?v=1.0.0'
    new = '/raventrace-my/assets/js/raven-share.js?v=2.1.0'
    if old in text:
        text = text.replace(old, new)
        raven.write_text(text, encoding='utf-8')
        print('bumped raven-share loader to v2.1.0')
    elif new not in text:
        raise RuntimeError('unexpected raven-share loader version')

    share = ROOT / 'assets/js/raven-share.js'
    text = share.read_text(encoding='utf-8')
    old = '/raventrace-my/assets/js/raven-publication.js?v=1.0.0'
    new = '/raventrace-my/assets/js/raven-publication.js?v=1.1.0'
    if old in text:
        text = text.replace(old, new)
        share.write_text(text, encoding='utf-8')
        print('bumped publication loader to v1.1.0')
    elif new not in text:
        raise RuntimeError('unexpected publication loader version')


def main():
    for story in STORIES:
        patch(story)
    patch_runtime_versions()


if __name__ == '__main__':
    main()
