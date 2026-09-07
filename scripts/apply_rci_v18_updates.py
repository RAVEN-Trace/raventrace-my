from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def write(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def replace_once(text, old, new, label):
    if old not in text:
        if new in text:
            return text
        raise RuntimeError(f"marker missing: {label}")
    return text.replace(old, new, 1)


# ---------- Homepage ----------
home = read("index.html")
home = home.replace("Isnin · 7 September 2026 · Malaysia", "7 September 2026 · lewat malam MYT")
home = home.replace("Maklumat disemak hingga · 7 Sep 2026 · awal pagi MYT", "Maklumat disemak hingga · 7 Sep 2026 · lewat malam MYT")
home = home.replace("CASEFILE / RCI-TH-2026 · v17", "CASEFILE / RCI-TH-2026 · v18")
home = home.replace("Kemas kini yang disahkan · 6–7 September", "Kemas kini bukti · 7 September + checkpoint 8 September")
home = home.replace("50+ rujukan dengan gred bukti", "52+ rujukan dengan gred bukti")

new_home_card = '''          <article id="home-2026-09-07-expected-charges" class="update-card lead-update"><div class="update-index">00</div><div class="meta-row"><span class="status claim">DEVELOPING · belum disahkan rasmi</span><time datetime="2026-09-07">7 Sep 2026</time></div><h3>Dua laporan menamakan Azeez, Jamil dan Azmi sebagai individu yang dijangka didakwa.</h3><p>Suara.TV dan Malaysia Corporate melaporkan berdasarkan sumber bahawa Abdul Azeez Abdul Rahim, Jamil Khir Baharom dan Azmi Ahmad dijangka berdepan tindakan pendakwaan secara berperingkat. Malaysia Corporate memberi tarikh, seksyen dan jumlah pertuduhan yang lebih spesifik. Setakat cut-off ini, RAVEN-Trace belum menemui pengesahan terbuka SPRM, AGC atau rekod mahkamah bagi butiran tersebut.</p><a href="/raventrace-my/news/2026/09/07/azeez-jamil-azmi-dijangka-didakwa/">Baca semakan developing claim →</a><br><a href="https://suara.tv/07/09/2026/azeez-jamil-khir-antara-tiga-dijangka-didakwa-berkaitan-rci-tabung-haji/" rel="noopener noreferrer">Suara.TV</a> · <a href="https://www.themalaysiancorporates.com/2026/09/07/rci-tabung-haji-jamil-khir-abdul-azeez-dan-azmi-dijangka-berdepan-enam-pertuduhan-bermula-minggu-ini/" rel="noopener noreferrer">Malaysia Corporate</a></article>\n'''
if 'home-2026-09-07-expected-charges' not in home:
    home = replace_once(home, '          <article id="home-2026-09-06-jamil-reman-checkpoint"', new_home_card + '          <article id="home-2026-09-06-jamil-reman-checkpoint"', "homepage developing card")

home = home.replace('raven-publication.js?v=2.0.0', 'raven-publication.js?v=2.1.0')
home = home.replace('raven.js?v=3.5.0', 'raven.js?v=3.6.0')
write("index.html", home)


# ---------- Newsroom ----------
news = read("news/index.html")
news = news.replace("Newsroom · kemas kini yang disahkan", "Newsroom · fakta, proses + developing claims")
news = news.replace("Maklumat disemak hingga · 7 Sep 2026 · awal pagi MYT", "Maklumat disemak hingga · 7 Sep 2026 · lewat malam MYT")
news = news.replace('<p class="eyebrow">Kemas kini yang disahkan</p>', '<p class="eyebrow">Perkembangan ikut tahap bukti</p>')

new_news_card = '''      <article id="news-2026-09-07-expected-charges" class="timeline-item" data-topic="enforcement"><time datetime="2026-09-07">07 SEP 2026</time><div><div class="meta-row"><span class="status claim">DEVELOPING · CLAIM</span><span class="source-grade">Gred C/D</span></div><h3>Azeez, Jamil dan Azmi dinamakan dalam laporan jangkaan pendakwaan</h3><p>Suara.TV melaporkan berdasarkan sumber bahawa Abdul Azeez Abdul Rahim, Jamil Khir Baharom dan Azmi Ahmad dijangka didakwa secara berperingkat. Malaysia Corporate melaporkan butiran lebih spesifik termasuk dakwaan izin pendakwaan, tarikh 10/11/17 September, seksyen undang-undang dan enam pertuduhan keseluruhan. Butiran itu belum disahkan secara terbuka oleh SPRM, AGC atau rekod mahkamah setakat cut-off.</p><a href="/raventrace-my/news/2026/09/07/azeez-jamil-azmi-dijangka-didakwa/">Baca semakan penuh →</a><br><a href="https://suara.tv/07/09/2026/azeez-jamil-khir-antara-tiga-dijangka-didakwa-berkaitan-rci-tabung-haji/" rel="noopener noreferrer">Suara.TV</a> · <a href="https://www.themalaysiancorporates.com/2026/09/07/rci-tabung-haji-jamil-khir-abdul-azeez-dan-azmi-dijangka-berdepan-enam-pertuduhan-bermula-minggu-ini/" rel="noopener noreferrer">Malaysia Corporate</a></div></article>\n'''
if 'news-2026-09-07-expected-charges' not in news:
    news = replace_once(news, '      <article id="news-2026-09-06-jamil-reman-checkpoint"', new_news_card + '      <article id="news-2026-09-06-jamil-reman-checkpoint"', "newsroom developing card")
news = news.replace('raven.js?v=3.4.0', 'raven.js?v=3.6.0')
write("news/index.html", news)


# ---------- CASEFILE ----------
case = read("investigations/rci-tabung-haji/index.html")
case = case.replace("CASEFILE RCI Tabung Haji v17:", "CASEFILE RCI Tabung Haji v18:")
case = case.replace("hingga 7 September 2026.", "hingga lewat malam 7 September 2026.")
case = case.replace("CASEFILE · RCI-TH-2026 · v17", "CASEFILE · RCI-TH-2026 · v18")
case = case.replace("Data cut-off · 7 Sep 2026 · awal pagi MYT", "Data cut-off · 7 Sep 2026 · lewat malam MYT")
case = case.replace("Revisi laman · 7 Sep 2026", "Revisi laman · 7 Sep 2026 · v18")
case = case.replace("<a href=\"#updates\">4 perkembangan utama</a>", "<a href=\"#updates\">6 perkembangan utama</a>")
case = case.replace("<div class=\"section-marker\"><span>02</span><p>Latest verified snapshot</p></div>", "<div class=\"section-marker\"><span>02</span><p>Latest evidence snapshot</p></div>")
case = case.replace("<h2>Lima perkembangan yang mengubah kedudukan kes.</h2>", "<h2>Enam perkembangan yang mengubah kedudukan kes.</h2>")

new_trace = '''            <article class="trace-card" data-sep7-developing="true"><div class="trace-head"><span>JEJAK / D1</span><time datetime="2026-09-07">7 Sep 2026 · laporan berasaskan sumber</time></div><div class="meta-row"><span class="status claim">DEVELOPING · CLAIM</span><span class="source-grade">Gred C/D</span></div><h3>Dua laporan menamakan Azeez, Jamil dan Azmi sebagai individu yang dijangka didakwa.</h3><dl><div><dt>Apa dilaporkan?</dt><dd>Suara.TV menamakan tiga individu sama dan menyatakan pendakwaan dijangka dibuat berperingkat. Malaysia Corporate mendakwa tiga kertas siasatan telah dibentangkan kepada Peguam Negara dan memberi butiran tarikh, seksyen serta jumlah pertuduhan.</dd></div><div><dt>Apa belum disahkan?</dt><dd>RAVEN-Trace belum menemui kenyataan terbuka SPRM/AGC atau charge sheet mahkamah yang mengesahkan izin pendakwaan, tarikh 10/11/17 September atau seksyen yang dilaporkan.</dd></div><div><dt>Had</dt><dd>Dua laporan boleh berkongsi sumber asal yang sama. Bilangan outlet tidak semestinya corroboration bebas. Semua individu kekal dianggap tidak bersalah melainkan disabitkan mahkamah.</dd></div></dl><p class="inline-sources"><a href="#s51">S51</a> <a href="#s52">S52</a></p></article>\n'''
if 'data-sep7-developing="true"' not in case:
    case = replace_once(case, '            <article class="trace-card" data-sep6-update="true">', new_trace + '            <article class="trace-card" data-sep6-update="true">', "case developing trace")

case = case.replace(
    "Ditahan 26 Ogos dan dibebaskan selepas tempoh reman. Siasatan dilaporkan diteruskan; tiada pertuduhan disahkan terhadap beliau setakat data cut-off.",
    "Ditahan 26 Ogos dan dibebaskan selepas tempoh reman. Siasatan dilaporkan diteruskan. Dua laporan 7 September menamakan beliau sebagai individu yang dijangka didakwa; Malaysia Corporate menyebut 10 September dan Seksyen 23 Akta SPRM, tetapi butiran itu belum disahkan secara rasmi setakat data cut-off."
)
case = case.replace(
    "Selepas reman lima hari bermula 2 September, Mahkamah Majistret Putrajaya membenarkan sambungan dua hari dari 7 hingga 8 September. SPRM menyatakan kes disiasat di bawah Seksyen 16(a)(A) Akta SPRM 2009. Reman bukan pertuduhan atau dapatan kesalahan.",
    "Selepas reman lima hari bermula 2 September, Mahkamah Majistret Putrajaya membenarkan sambungan dua hari dari 7 hingga 8 September. SPRM menyatakan kes disiasat di bawah Seksyen 16(a)(A) Akta SPRM 2009. Dua laporan 7 September menamakan beliau dalam jangkaan pendakwaan; Malaysia Corporate menyebut 17 September dan Seksyen 403 Kanun Keseksaan. Perbezaan dengan seksyen siasatan rasmi hanya boleh dikunci apabila rekod pertuduhan rasmi tersedia."
)
case = case.replace(
    "Syarikat mengumumkan beliau direman 17 Ogos untuk membantu siasatan SPRM dan dibebaskan 19 Ogos sebelum menyambung tugas. Syarikat menegaskan reman bukan dapatan salah laku.",
    "Syarikat mengumumkan beliau direman 17 Ogos untuk membantu siasatan SPRM dan dibebaskan 19 Ogos sebelum menyambung tugas. Dua laporan 7 September menamakan beliau sebagai individu yang dijangka didakwa; Malaysia Corporate menyebut 11 September dan dua pertuduhan Seksyen 417 Kanun Keseksaan. Tiada charge sheet rasmi ditemui setakat data cut-off."
)

new_history = '''            <article><time>7 Sep</time><h3>Laporan jangkaan pendakwaan</h3><p>Suara.TV dan Malaysia Corporate menamakan Azeez, Jamil dan Azmi sebagai individu yang dijangka didakwa. Malaysia Corporate memberi butiran lebih spesifik, tetapi setakat cut-off ia masih belum disahkan oleh SPRM, AGC atau rekod mahkamah.</p></article>\n'''
if '<time>7 Sep</time><h3>Laporan jangkaan pendakwaan</h3>' not in case:
    case = replace_once(case, '          </div>\n        </section>\n\n        <section class="case-section" id="governance">', new_history + '          </div>\n        </section>\n\n        <section class="case-section" id="governance">', "timeline 7 Sep")

case = case.replace(
    '<ol class="unknown-list"><li>Apakah pertuduhan tambahan yang benar-benar telah dibaca selepas pengumuman SPRM pada 2 September?</li>',
    '<ol class="unknown-list"><li>Adakah SPRM atau AGC akan mengesahkan laporan 7 September yang menamakan Azeez, Jamil dan Azmi serta tarikh 10/11/17 September?</li><li>Apakah pertuduhan tambahan yang benar-benar telah dibaca selepas pengumuman SPRM pada 2 September?</li>'
)
case = case.replace(
    "Dapatkan nombor kes, helaian pertuduhan, tindakan selepas reman 8 September, keputusan AGC bagi Al-Rawda, empat fail NFA, transkrip RCI, audit forensik dan status lengkap enam syor RCI yang masih berjalan.",
    "Dapatkan tindakan selepas reman 8 September, pengesahan SPRM/AGC terhadap laporan 7 September, nombor kes dan helaian pertuduhan jika prosiding benar-benar berlaku pada tarikh 10/11/17 September yang dilaporkan, keputusan AGC bagi Al-Rawda, empat fail NFA, transkrip RCI, audit forensik dan status lengkap enam syor RCI yang masih berjalan."
)

source_rows = '''            <li id="s51"><span>D</span><a href="https://www.themalaysiancorporates.com/2026/09/07/rci-tabung-haji-jamil-khir-abdul-azeez-dan-azmi-dijangka-berdepan-enam-pertuduhan-bermula-minggu-ini/" rel="noopener noreferrer">Jamil Khir, Abdul Azeez dan Azmi dijangka berdepan enam pertuduhan</a><small>Malaysia Corporate · 7 Sep · laporan berasaskan sumber; butiran belum disahkan rasmi</small></li>\n            <li id="s52"><span>D</span><a href="https://suara.tv/07/09/2026/azeez-jamil-khir-antara-tiga-dijangka-didakwa-berkaitan-rci-tabung-haji/" rel="noopener noreferrer">Azeez, Jamil Khir antara tiga dijangka didakwa</a><small>Suara.TV · 7 Sep · laporan berasaskan sumber; outlet sendiri menyatakan tiada pengumuman rasmi bentuk/tarikh pertuduhan</small></li>\n'''
if 'id="s51"' not in case:
    case = replace_once(case, '            <li id="s50"', source_rows + '            <li id="s50"', "source room S51-S52")

case = case.replace("<strong>Data cut-off:</strong> 7 September 2026 · awal pagi MYT. <strong>Semakan laman:</strong> 7 September 2026.", "<strong>Data cut-off:</strong> 7 September 2026 · lewat malam MYT. <strong>Semakan laman:</strong> 7 September 2026 · v18.")
case = case.replace('raven.js?v=3.4.0', 'raven.js?v=3.6.0')
write("investigations/rci-tabung-haji/index.html", case)


# ---------- Jamil remand story: make the 8 Sep checkpoint explicit ----------
jamil = read("news/2026/09/06/jamil-khir-reman-checkpoint/index.html")
jamil = jamil.replace('content="2026-09-07T01:55:00+08:00"', 'content="2026-09-07T23:55:00+08:00"')
jamil = jamil.replace('"dateModified":"2026-09-07T01:55:00+08:00"', '"dateModified":"2026-09-07T23:55:00+08:00"')
jamil = jamil.replace("Dikemas kini · 7 Sep 2026 · awal pagi MYT", "Dikemas kini · 7 Sep 2026 · lewat malam MYT")
jamil = jamil.replace("Setakat awal 7 September, belum ada pertuduhan disahkan terhadap beliau.", "Setakat lewat malam 7 September, belum ada pertuduhan disahkan terhadap beliau. Dua laporan berasaskan sumber pada 7 September menamakan beliau sebagai individu yang dijangka didakwa, tetapi butiran itu belum disahkan secara terbuka oleh SPRM, AGC atau rekod mahkamah.")
jamil = jamil.replace("Sambungan reman disahkan. Pertuduhan belum disahkan; tindakan selepas 8 September masih belum diketahui.", "Sambungan reman hingga 8 September disahkan. Laporan 7 September mengenai jangkaan pendakwaan masih berstatus CLAIM; tindakan selepas tamat reman belum diketahui.")
if "Malaysia Corporate — jangkaan pendakwaan" not in jamil:
    jamil = jamil.replace('</ul><p class="story-note">', '<li><a href="https://www.themalaysiancorporates.com/2026/09/07/rci-tabung-haji-jamil-khir-abdul-azeez-dan-azmi-dijangka-berdepan-enam-pertuduhan-bermula-minggu-ini/" rel="noopener noreferrer">Malaysia Corporate — jangkaan pendakwaan</a><small>7 Sep 2026 · laporan berasaskan sumber; belum disahkan rasmi.</small></li><li><a href="https://suara.tv/07/09/2026/azeez-jamil-khir-antara-tiga-dijangka-didakwa-berkaitan-rci-tabung-haji/" rel="noopener noreferrer">Suara.TV — tiga individu dijangka didakwa</a><small>7 Sep 2026 · outlet menyatakan bentuk/tarikh belum diumumkan rasmi.</small></li></ul><p class="story-note">')
jamil = jamil.replace('raven.js?v=3.4.0', 'raven.js?v=3.6.0')
write("news/2026/09/06/jamil-khir-reman-checkpoint/index.html", jamil)


# ---------- New dedicated developing story ----------
new_story = '''<!doctype html>
<html lang="ms">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="RAVEN-Trace menyemak laporan 7 September yang menamakan Abdul Azeez Abdul Rahim, Jamil Khir Baharom dan Azmi Ahmad sebagai individu yang dijangka didakwa susulan RCI Tabung Haji.">
<title>Azeez, Jamil dan Azmi: laporan jangkaan pendakwaan | RAVEN-Trace</title>
<link rel="canonical" href="https://raven-trace.github.io/raventrace-my/news/2026/09/07/azeez-jamil-azmi-dijangka-didakwa/">
<meta property="og:type" content="article"><meta property="og:site_name" content="RAVEN-Trace Malaysia"><meta property="og:title" content="Azeez, Jamil dan Azmi dinamakan dalam laporan jangkaan pendakwaan"><meta property="og:description" content="Dua laporan 7 September menamakan tiga individu sama. Butiran tarikh, seksyen dan izin pendakwaan belum disahkan secara terbuka oleh SPRM, AGC atau mahkamah setakat cut-off."><meta property="og:url" content="https://raven-trace.github.io/raventrace-my/news/2026/09/07/azeez-jamil-azmi-dijangka-didakwa/"><meta property="og:image" content="https://raven-trace.github.io/raventrace-my/assets/art/rci-tabung-haji-hero.webp"><meta name="twitter:card" content="summary_large_image"><meta property="article:published_time" content="2026-09-07T23:55:00+08:00"><meta property="article:modified_time" content="2026-09-07T23:55:00+08:00">
<link rel="stylesheet" href="/raventrace-my/assets/css/raven.css?v=3.0.0"><link rel="stylesheet" href="/raventrace-my/assets/css/raven-story.css?v=1.0.0">
<script type="application/ld+json">{"@context":"https://schema.org","@type":"NewsArticle","headline":"Azeez, Jamil dan Azmi dinamakan dalam laporan jangkaan pendakwaan","datePublished":"2026-09-07T23:55:00+08:00","dateModified":"2026-09-07T23:55:00+08:00","mainEntityOfPage":"https://raven-trace.github.io/raventrace-my/news/2026/09/07/azeez-jamil-azmi-dijangka-didakwa/","publisher":{"@type":"Organization","name":"RAVEN-Trace Malaysia"}}</script></head>
<body class="story-page">
<a class="skip-link" href="#main">Terus ke kandungan</a>
<header class="site-header"><div class="masthead"><a class="brand" href="/raventrace-my/"><span><span class="brand-name">RAVEN<em>-Trace</em></span><span class="brand-sub">Independent · Evidence-led · Malaysia</span></span></a><p class="masthead-note">Claim bukan fact.<br>Tarikh bukan pertuduhan.</p></div><div class="nav-row"><div class="nav-wrap"><button class="nav-toggle" type="button" data-nav-toggle aria-expanded="false">Menu</button><nav class="site-nav" data-nav><a href="/raventrace-my/">Utama</a><a href="/raventrace-my/news/">Newsroom</a><a href="/raventrace-my/investigations/">Siasatan</a><a href="/raventrace-my/methodology/">Metodologi</a><a href="/raventrace-my/about/">Tentang</a></nav></div></div></header>
<main id="main">
<section class="story-hero"><div class="container"><p class="story-kicker">RCI Tabung Haji · Court & Enforcement Watch</p><div class="meta-row"><span class="status claim">DEVELOPING · CLAIM</span><span class="source-grade">Gred C/D</span></div><h1>Azeez, Jamil dan Azmi dinamakan dalam laporan jangkaan pendakwaan.</h1><p class="story-dek">Dua laporan 7 September menamakan tiga individu sama. Satu daripadanya memberikan tarikh dan seksyen pertuduhan yang terperinci. RAVEN-Trace belum menganggap butiran itu sebagai fakta sehingga ada pengesahan SPRM, AGC atau rekod mahkamah.</p><div class="story-meta"><span>Diterbitkan 7 Sep 2026 · lewat malam MYT</span><span>Status boleh berubah dengan cepat</span></div><div class="story-actions"><button class="btn btn-primary" type="button" data-share data-share-title="RAVEN-Trace: Azeez, Jamil dan Azmi — developing claim" data-share-text="Dua laporan 7 September menamakan Azeez, Jamil dan Azmi sebagai individu yang dijangka didakwa. Tarikh, seksyen dan izin pendakwaan belum disahkan secara rasmi setakat cut-off.">Kongsi artikel</button><a class="btn" href="/raventrace-my/investigations/rci-tabung-haji/#updates">Buka evidence snapshot</a></div></div></section>
<div class="story-shell"><article class="story-body"><figure class="story-art"><img src="/raventrace-my/assets/art/rci-tabung-haji-hero.webp" alt="Ilustrasi editorial RAVEN-Trace untuk siasatan RCI Tabung Haji"><figcaption>ILUSTRASI EDITORIAL · Bukan bukti dan bukan foto pertuduhan mahkamah.</figcaption></figure>
<div class="story-fact-grid"><article><b>FACT</b><p>Suara.TV dan Malaysia Corporate menerbitkan laporan pada 7 September yang menamakan Abdul Azeez Abdul Rahim, Jamil Khir Baharom dan Azmi Ahmad.</p></article><article><b>CLAIM</b><p>Malaysia Corporate mendakwa izin pendakwaan telah diberikan dan menyenaraikan tarikh 10, 11 dan 17 September serta seksyen pertuduhan tertentu.</p></article><article><b>UNKNOWN</b><p>Setakat cut-off, RAVEN-Trace belum menemui pengesahan terbuka SPRM, AGC atau charge sheet mahkamah bagi butiran tersebut.</p></article></div>
<h2>Apa yang Suara.TV laporkan?</h2><p>Suara.TV melaporkan berdasarkan sumber bahawa Azeez, Jamil dan Azmi dijangka didakwa secara berperingkat pada minggu ini dan minggu berikutnya. Laporan itu sendiri menyatakan belum ada pengumuman rasmi pihak berkuasa mengenai bentuk pertuduhan atau tarikh sebenar.</p>
<h2>Apa yang Malaysia Corporate tambah?</h2><p>Malaysia Corporate melaporkan, juga berdasarkan sumber, bahawa tiga kertas siasatan telah dibentangkan kepada Peguam Negara pada 7 September dan izin pendakwaan diberikan. Ia mendakwa Azeez dijadualkan pada 10 September di bawah Seksyen 23 Akta SPRM, Azmi pada 11 September dengan dua pertuduhan Seksyen 417 Kanun Keseksaan, dan Jamil pada 17 September dengan tiga pertuduhan Seksyen 403 Kanun Keseksaan.</p>
<div class="story-callout"><strong>Had bukti</strong><p>Butiran Malaysia Corporate lebih spesifik, tetapi specificity bukan pengesahan. Dua outlet juga boleh bergantung pada sumber asal yang sama. RAVEN-Trace hanya akan menaik taraf tarikh, seksyen dan jumlah pertuduhan kepada FACT apabila kenyataan rasmi atau rekod mahkamah tersedia.</p></div>
<h2>Kenapa kes Jamil memerlukan perhatian tambahan?</h2><p>SPRM secara rasmi menyatakan siasatan reman Jamil berkaitan pajakan hotel TH di Arab Saudi dibuat di bawah Seksyen 16(a)(A) Akta SPRM 2009. Malaysia Corporate pula menjangka pertuduhan di bawah Seksyen 403 Kanun Keseksaan. Ini tidak semestinya bercanggah kerana seksyen siasatan dan seksyen pertuduhan boleh berbeza, tetapi RAVEN-Trace tidak akan menentukan seksyen akhir sebelum charge sheet dibaca.</p>
<h2>Apa yang perlu berlaku seterusnya?</h2><p>Checkpoint pertama ialah tamat tempoh sambungan reman Jamil pada 8 September. Selepas itu, tarikh 10, 11 dan 17 September yang dilaporkan akan menjadi titik verifikasi. Jika tiada tindakan pada tarikh berkenaan, claim akan diturunkan atau dibetulkan. Jika pertuduhan dibaca, status akan dinaik taraf kepada FACT dengan nombor kes, seksyen dan butiran mahkamah.</p>
<h2>Sumber</h2><ul class="story-source-list"><li><a href="https://suara.tv/07/09/2026/azeez-jamil-khir-antara-tiga-dijangka-didakwa-berkaitan-rci-tabung-haji/" rel="noopener noreferrer">Suara.TV — Azeez, Jamil Khir antara tiga dijangka didakwa</a><small>7 Sep 2026 · laporan berasaskan sumber; outlet menyatakan tiada pengumuman rasmi bentuk/tarikh.</small></li><li><a href="https://www.themalaysiancorporates.com/2026/09/07/rci-tabung-haji-jamil-khir-abdul-azeez-dan-azmi-dijangka-berdepan-enam-pertuduhan-bermula-minggu-ini/" rel="noopener noreferrer">Malaysia Corporate — enam pertuduhan dijangka bermula minggu ini</a><small>7 Sep 2026 · butiran tarikh/seksyen/izin pendakwaan berasaskan sumber dan belum disahkan rasmi.</small></li><li><a href="https://web26.bernama.com/bm/jenayah_mahkamah/news.php?id=2603643" rel="noopener noreferrer">Bernama — reman bekas menteri disambung hingga 8 Sep</a><small>6 Sep 2026 · rekod proses yang disahkan.</small></li><li><a href="https://www.bernama.com/radio/news.php?id=2602039" rel="noopener noreferrer">Bernama — SPRM: Al-Rawda dijangka dibawa ke peringkat pendakwaan</a><small>2 Sep 2026 · konteks rasmi bahawa satu lagi kertas Al-Rawda dijangka didakwa minggu berikutnya, tanpa mengesahkan identiti/tarikh laporan 7 Sep.</small></li></ul>
<p class="story-note">Semua individu dianggap tidak bersalah melainkan dan sehingga disabitkan oleh mahkamah. RAVEN-Trace akan membetulkan artikel ini jika tarikh atau butiran yang dilaporkan tidak berlaku.</p></article><aside class="story-side"><div class="story-side-card"><h2>Status semasa</h2><p><strong>DEVELOPING CLAIM</strong></p><p>Tiga nama dilaporkan oleh dua outlet. Tarikh, seksyen dan izin pendakwaan belum disahkan rasmi.</p></div><div class="story-side-card"><h2>Verify next</h2><p>8 Sep · status selepas reman Jamil</p><p>10 Sep · claim Azeez</p><p>11 Sep · claim Azmi</p><p>17 Sep · claim Jamil</p></div><div class="story-side-card"><h2>Jejak lanjut</h2><p><a href="/raventrace-my/news/">Newsroom →</a></p><p><a href="/raventrace-my/investigations/rci-tabung-haji/#people">People ledger →</a></p><p><a href="/raventrace-my/investigations/rci-tabung-haji/#sources">Source Room →</a></p></div></aside></div></main>
<footer class="site-footer"><div class="container footer-grid"><div><div class="footer-brand">RAVEN<em>-Trace</em>™</div><p class="motto">A lie wins by speed. Truth wins by audit.</p></div><nav class="footer-nav"><a href="/raventrace-my/news/">Newsroom</a><a href="/raventrace-my/investigations/">Siasatan</a><a href="/raventrace-my/methodology/">Metodologi</a><a href="/raventrace-my/corrections/">Pembetulan</a></nav><p class="legal">RAVEN-Trace™ by SharulR X(ai) Projects. Claim bukan fact; pertuduhan bukan sabitan.</p></div></footer><script src="/raventrace-my/assets/js/raven.js?v=3.6.0" defer></script></body></html>'''
write("news/2026/09/07/azeez-jamil-azmi-dijangka-didakwa/index.html", new_story)


# ---------- Publication UX: update evidence boundary and v18 changelog ----------
pub = read("assets/js/raven-publication.js")
pub = pub.replace("window.__RAVEN_PUBLICATION_V2__", "window.__RAVEN_PUBLICATION_V2_1__")
pub = pub.replace("publication-2.0", "publication-2.1")
pub = pub.replace("Liabiliti akhir individu, keputusan semua kertas siasatan dan hasil selepas checkpoint reman semasa belum diketahui.", "Liabiliti akhir individu, keputusan semua kertas siasatan dan sama ada laporan jangkaan pendakwaan 7 September akan disahkan secara rasmi masih belum diketahui.")
pub = pub.replace("Butiran empat NFA, keputusan fail lain, liabiliti akhir individu dan hasil selepas sambungan reman hingga 8 Sep masih belum diketahui.", "Butiran empat NFA, hasil selepas reman hingga 8 Sep dan dakwaan tarikh pendakwaan 10/11/17 Sep masih belum disahkan secara rasmi.")
pub = pub.replace("Apa yang berubah dalam CASEFILE v17", "Apa yang berubah dalam CASEFILE v18")
pub = pub.replace("What changed · v17", "What changed · v18")
pub = pub.replace("Mahkamah membenarkan sambungan reman dua hari hingga 8 September.", "Dua laporan 7 September menamakan Azeez, Jamil dan Azmi dalam jangkaan pendakwaan; status kekal CLAIM sehingga disahkan rasmi.")
pub = pub.replace("Konteks RM11.5b sukuk UJSB dikunci sebagai refinancing, bukan kerugian baharu.", "Checkpoint Jamil kini bergerak ke tamat reman 8 September; laporan Malaysia Corporate dan Suara.TV ditambah sebagai developing evidence.")
pub = pub.replace("Semak apa berlaku selepas checkpoint 8 September dan sebarang tindakan AGC/mahkamah baharu.", "Semak status selepas reman 8 September dan sahkan atau gugurkan claim tarikh 10/11/17 September melalui SPRM, AGC atau rekod mahkamah.")
write("assets/js/raven-publication.js", pub)


# ---------- Loader cache-bust ----------
raven = read("assets/js/raven.js")
raven = raven.replace("raven-publication.js?v=1.1.0", "raven-publication.js?v=2.1.0")
write("assets/js/raven.js", raven)


# ---------- README release marker ----------
readme = read("README.md")
readme = readme.replace("CASEFILE v17", "CASEFILE v18")
readme = readme.replace("reconciled through **7 September 2026 · early morning MYT**", "reconciled through **7 September 2026 · late evening MYT**")
if "developing prosecution reports" not in readme:
    marker = "Current publication infrastructure includes"
    if marker in readme:
        readme = readme.replace(marker, "Current publication infrastructure includes developing prosecution reports (clearly labelled CLAIM), and", 1)
write("README.md", readme)

print("RCI v18 update prepared")
