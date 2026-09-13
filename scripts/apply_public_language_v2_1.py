#!/usr/bin/env python3
"""RAVEN Public Language V2.1 deep-clean pass.

Second pass after V2: removes remaining analyst-first wording from public
Narrative pages while preserving factual findings, names, dates, amounts,
source links, evidence grades, legal status and canonical URLs.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def swap(path: Path, replacements: list[tuple[str, str]]) -> None:
    text = path.read_text(encoding='utf-8')
    old_text = text
    for old, new in replacements:
        if old in text:
            text = text.replace(old, new)
    if text != old_text:
        path.write_text(text, encoding='utf-8')
        print('updated', path.relative_to(ROOT))


NARR = ROOT / 'investigations/rci-tabung-haji/narratives/index.html'
SOCIAL = ROOT / 'investigations/rci-tabung-haji/narratives/political-social-media/index.html'
ABOUT = ROOT / 'about/index.html'
METHOD = ROOT / 'methodology/index.html'

swap(NARR, [
    ('<title>RCI Tabung Haji — Forensik Naratif: cerita vs bukti | RAVEN-Trace</title>',
     '<title>RCI Tabung Haji — Audit Naratif: cerita vs bukti | RAVEN-Trace</title>'),
    ('<meta property="og:title" content="RCI Tabung Haji — Forensik Naratif: cerita vs bukti">',
     '<meta property="og:title" content="RCI Tabung Haji — Audit Naratif: cerita vs bukti">'),
    ('<meta name="twitter:description" content="Audit naratif politik berdasarkan rekod, konteks yang tertinggal dan bukti yang boleh mengubah verdict.">',
     '<meta name="twitter:description" content="Audit naratif politik berdasarkan rekod, konteks yang tertinggal dan bukti yang boleh mengubah keputusan Raven.">'),

    # Make the canonical HTML readable even if enhancement JS fails.
    ('<b>Teknik naratif</b>', '<b>Apa trick cerita ni?</b>'),
    ('<b>Apa yang cerita ini tinggalkan?</b>', '<b>Apa yang cerita tak sebut?</b>'),
    ('<b>Selepas framing dibuang:</b>', '<b>Raven kata macam mana?</b>'),
    ('<b>Bukti apa boleh mengubah penilaian?</b>', '<b>Apa bukti yang boleh ubah keputusan Raven?</b>'),
    ('<b>Tahap keyakinan:</b>', '<b>Keyakinan Raven:</b>'),

    # Remaining jargon / formal leakage.
    ('Kerugian, impairment atau transaksi bermasalah tidak dengan sendirinya membuktikan wang dicuri.',
     'Kerugian, susut nilai (impairment) atau transaksi bermasalah tidak dengan sendirinya membuktikan wang dicuri.'),
    ('Namun, pemilikan benefisial dan rantaian transaksi paling kukuh jika disokong terus oleh dokumen korporat serta transaksi primer.',
     'Namun, siapa sebenarnya memiliki aset dan bagaimana transaksi itu bergerak paling kukuh jika disokong terus oleh dokumen korporat dan rekod transaksi asal.'),
    ('FAKTA · POSISI POLITIK', 'POSISI INI MEMANG DIREKODKAN'),
    ('Permintaan untuk pemeriksaan lebih luas memang wujud dalam rekod awam dan boleh disahkan sebagai posisi politik.',
     'Permintaan untuk pemeriksaan lebih luas memang wujud dalam rekod awam. Yang boleh kita sahkan ialah <strong>pendirian itu memang dibuat</strong>.'),
    ('Soalan dasar yang sah. Perbahasan sebenar ialah mekanisme paling sesuai — RCI baharu, PAC, audit forensik atau siasatan agensi — dan bukannya sama ada tempoh selepas itu langsung tidak patut diperiksa.',
     'Ini soalan dasar yang sah. Perbahasan sebenar ialah cara mana paling sesuai — RCI baharu, PAC, audit forensik atau siasatan agensi — bukan sama ada tempoh selepas itu langsung tak patut diperiksa.'),
    ('Bukti bahawa mekanisme sedia ada tidak mempunyai kuasa, akses dokumen atau skop yang diperlukan akan menguatkan hujah untuk RCI baharu; bukti bahawa PAC/audit/agensi sudah menjawab jurang yang sama akan melemahkannya.',
     'Kalau saluran sedia ada tak mempunyai kuasa, akses dokumen atau skop yang diperlukan, hujah untuk RCI baharu jadi lebih kuat. Kalau PAC, audit atau agensi lain sudah menjawab jurang yang sama, hujah itu jadi lebih lemah.'),
    ('POSISI / HUJAH DASAR', 'HUJAH DASAR · BUKAN FAKTA MUKTAMAD'),
    ('Ini pilihan dasar, bukan fakta. Soalan utama ialah jurang bukti atau kuasa apa yang benar-benar memerlukan RCI baharu berbanding mekanisme sedia ada.',
     'Ini pilihan dasar, bukan fakta muktamad. Soalan sebenarnya: ada tak jurang bukti atau kuasa yang memang memerlukan RCI baharu, atau saluran sedia ada sudah mencukupi?'),
    ('Posisi awam tidak seragam.', 'Pendirian awam tidak seragam.'),
    ('bukan satu posisi tunggal yang seragam.', 'bukan satu pendirian tunggal yang seragam.'),
    ('akan menyokong dakwaan bahawa UMNO mempunyai posisi tunggal.', 'akan menyokong dakwaan bahawa UMNO mempunyai satu pendirian rasmi.'),
    ('Kenyataan bekas Ketua Audit Negara Madinah Mohamad digunakan sebagai counter-narrative kepada dakwaan “sakau”.',
     'Kenyataan bekas Ketua Audit Negara Madinah Mohamad digunakan sebagai jawapan balas kepada dakwaan “sakau”.'),
    ('Ia tidak menutup kemungkinan isu tadbir urus, accounting treatment atau siasatan jenayah lain.',
     'Ia tidak menutup kemungkinan isu tadbir urus, cara perakaunan atau siasatan jenayah lain.'),
    ('rendah bagi kesimpulan universal bahawa tiada salah laku.',
     'rendah bagi kesimpulan menyeluruh bahawa tiada salah laku.'),
    ('defisit aset-liabiliti, nilai pasaran aset, premium transaksi UJSB, kerugian atau rosot nilai dan jumlah pertimbangan penstrukturan',
     'jurang antara aset dan tanggungan, nilai pasaran aset, nilai berkaitan transaksi UJSB, kerugian atau susut nilai dan nilai yang digunakan dalam penstrukturan'),
])

swap(SOCIAL, [
    ('<title>RCI Tabung Haji — Forensik politik & media sosial | RAVEN-Trace</title>',
     '<title>RCI Tabung Haji — Audit naratif politik & media sosial | RAVEN-Trace</title>'),
    ('<meta name="description" content="Forensik RAVEN-Trace terhadap bahasa politik dan media sosial sekitar RCI Tabung Haji: apa yang disahkan, apa yang dipilih, apa yang ditinggalkan dan bagaimana framing boleh mempengaruhi pembaca.">',
     '<meta name="description" content="Audit Raven terhadap naratif politik dan media sosial sekitar RCI Tabung Haji: apa yang disahkan, apa yang dipilih, apa yang tak disebut dan apa yang masih belum terbukti.">'),
    ('<meta property="og:title" content="Forensik politik & media sosial — RCI Tabung Haji">',
     '<meta property="og:title" content="Audit naratif politik & media sosial — RCI Tabung Haji">'),
    ('<p class="section-kicker">RCI TABUNG HAJI · FORENSIK POLITIK + MEDIA SOSIAL</p>',
     '<p class="section-kicker">RCI TABUNG HAJI · AUDIT NARATIF POLITIK + MEDIA SOSIAL</p>'),

    ('<b>Selepas framing dibuang:</b>', '<b>Raven kata macam mana?</b>'),
    ('<b>Tahap keyakinan:</b>', '<b>Keyakinan Raven:</b>'),
    ('<div class="section-marker"><span>03</span><p>Forensik bahasa</p></div>',
     '<div class="section-marker"><span>03</span><p>Macam mana bahasa mainkan persepsi?</p></div>'),
    ('Kerugian, defisit aset-liabiliti, impairment, transaksi meragukan dan kecurian bukan kategori yang sama.',
     'Kerugian, jurang antara aset dan tanggungan, susut nilai (impairment), transaksi meragukan dan kecurian bukan benda yang sama.'),
    ('Emosi ialah signal untuk berhenti dan semak — bukan bukti tambahan.',
     'Emosi ialah tanda untuk berhenti dan semak — bukan bukti tambahan.'),
    ('Beberapa posting popular tidak mewakili penduduk Malaysia, penyokong satu parti atau seluruh platform. Tanpa sampel yang jelas, Raven hanya memanggilnya <b>signal yang diperhatikan</b>.',
     'Beberapa hantaran popular tidak mewakili penduduk Malaysia, penyokong satu parti atau seluruh platform. Tanpa sampel yang jelas, Raven hanya panggil ia <b>petunjuk yang kami nampak</b>.'),
    ('<strong>Neutralise, bukan counter-spin</strong><span>Raven tidak membalas slogan dengan slogan. Kami utamakan fakta yang benar, terangkan teknik manipulasi secara ringkas, kemudian beri pembaca model alternatif yang lebih tepat. Tujuannya ialah meningkatkan ketepatan penilaian — bukan memindahkan kesetiaan daripada satu kem kepada kem lain.</span>',
     '<strong>Betulkan cerita, bukan balas slogan dengan slogan</strong><span>Raven tak lawan satu spin dengan spin lain. Kami mula dengan fakta, tunjuk trick yang digunakan, kemudian beri penerangan yang lebih tepat. Tujuannya bukan suruh pembaca pindah kem — tujuannya supaya pembaca boleh nilai sendiri.</span>'),
    ('<div class="section-marker"><span>04</span><p>Signal media sosial</p></div>',
     '<div class="section-marker"><span>04</span><p>Petunjuk media sosial</p></div>'),
    ('cara akaun atau posting dipilih, pemberat engagement, atau sama ada aktiviti terkoordinasi diperiksa.',
     'cara akaun atau hantaran dipilih, jumlah interaksi, atau sama ada aktiviti yang disusun bersama diperiksa.'),
    ('RAVEN menggunakan istilah <strong>signal naratif yang diperhatikan</strong>, bukan “sentimen platform”.',
     'Raven panggilnya <strong>petunjuk naratif yang kami nampak</strong>, bukan “sentimen seluruh platform”.'),
    ('SIGNAL · PRO-KERAJAAN', 'PETUNJUK · PRO-KERAJAAN'),
    ('IDENTITI · RISIKO PRIMING EMOSI', 'IDENTITI · BOLEH CETUS EMOSI DULU'),
    ('ia tidak membuktikan selective targeting. Itu memerlukan perbandingan data terhadap institusi lain.',
     'ia tidak membuktikan layanan pilih kasih. Untuk buktikan itu, kita perlu bandingkan data dengan institusi lain.'),
    ('Laporan deep-research yang dihantar kepada RAVEN digunakan sebagai bahan penyelidikan sekunder. Ia tidak menggantikan dokumen primer, rekod mahkamah atau kenyataan rasmi.',
     'Laporan penyelidikan yang dihantar kepada Raven digunakan sebagai bahan rujukan awal. Ia tidak menggantikan dokumen asal, rekod mahkamah atau kenyataan rasmi.'),
    ('rekod primer atau laporan yang boleh disemak', 'rekod asal atau laporan yang boleh disemak'),
])

swap(ABOUT, [
    ('<meta name="description" content="Tentang RAVEN-Trace Malaysia: publication penyiasatan evidence-led yang memisahkan fakta, dakwaan, naratif dan perkara yang belum diketahui, kemudian menerangkannya kepada pembaca Malaysia.">',
     '<meta name="description" content="Tentang RAVEN-Trace Malaysia: semak dakwaan, asingkan cerita daripada bukti dan terangkan apa yang masih belum diketahui dengan bahasa manusia.">'),
    ('RAVEN-Trace™ by SharulR X(ai) Projects. Independent Evidence-Led Journalism untuk Malaysia.',
     'RAVEN-Trace™ by SharulR X(ai) Projects. Penerbitan bebas berasaskan bukti untuk Malaysia.'),
])

swap(METHOD, [
    ('Prinsip ini disokong oleh penyelidikan tentang prebunking, pembetulan fakta dan selective presentation.',
     'Prinsip ini disokong oleh penyelidikan tentang cara memberi konteks sebelum orang terdedah kepada manipulasi, cara membetulkan fakta dan kesan apabila sesuatu cerita hanya menunjukkan sebahagian maklumat.'),
    ('RAVEN-Trace™ by SharulR X(ai) Projects. Metodologi berpandukan Master Blueprint V3.0 dan Reporter Domain Addendum V3.1.',
     'RAVEN-Trace™ by SharulR X(ai) Projects. Bukti dahulu, batas jelas, pembetulan terbuka.'),
])

# Hard editorial invariants.
main = NARR.read_text(encoding='utf-8')
social = SOCIAL.read_text(encoding='utf-8')

for tok in ['RM193.5 juta','14 kertas siasatan','Pertuduhan bukan sabitan','naratif-azeez-ambil-rm193-5-juta','naratif-sakau-duit-umat-islam']:
    assert tok in main, tok
for tok in ['Raven kata macam mana?','Apa trick cerita ni?','Apa yang cerita tak sebut?','Apa bukti yang boleh ubah keputusan Raven?','Keyakinan Raven:']:
    assert tok in main, tok
for tok in ['Petunjuk media sosial','Betulkan cerita, bukan balas slogan dengan slogan','VIRAL TAK BERMAKSUD SUARA SEMUA ORANG']:
    assert tok in social, tok

for stale in ['counter-narrative','accounting treatment','selective targeting','signal yang diperhatikan','Signal media sosial','pemberat engagement','Category collapse + number laundering','policy position, bukan finding undang-undang']:
    assert stale not in main, 'main stale: '+stale
    assert stale not in social, 'social stale: '+stale

print('RAVEN PUBLIC LANGUAGE V2.1: PASS')
