from pathlib import Path

p = Path('investigations/rci-tabung-haji/narratives/index.html')
s = p.read_text(encoding='utf-8')

marker = '<section class="case-section"><div class="section-marker"><span>02</span><p>Dakwaan vs rekod</p></div>'
if marker not in s:
    raise SystemExit('Narrative insertion marker not found')

if 'political-social-media/' not in s:
    block = '''<section class="case-section" id="political-social-map"><div class="section-marker"><span>POL</span><p>Naratif politik + media sosial</p></div><h2>Peta baharu: lima blok politik, enam signal sosial — dan had bukti yang perlu dijaga.</h2><p class="section-lead">Sebuah laporan deep-research baharu yang menggabungkan kenyataan parti dan contoh kandungan Facebook, Reels dan Threads telah diaudit oleh RAVEN-Trace. Ia berguna sebagai peta naratif, tetapi bukan ukuran sentimen awam dan bukan evidence pack undang-undang.</p><div class="case-warning light"><strong>Audit Raven</strong><span>Kami mengekalkan signal yang boleh dijejak — ketelusan kerajaan/PH, kerjasama + solidariti UMNO, desakan RCI kedua/UJSB, frame “jenama Islam disasar”, perbezaan taktikal BERSATU-PAS dan desakan AMK agar penguatkuasaan tidak tunduk pada jadual parti. Kami tidak menerbitkan inferens motif atau “sentimen platform” sebagai fakta tanpa sampling dan bukti tambahan.</span></div><div class="btn-row"><a class="btn btn-primary" href="/raventrace-my/investigations/rci-tabung-haji/narratives/political-social-media/">Buka peta naratif politik →</a></div><p><b>Signal utama:</b> “tiada bahagian disembunyikan” · “siapa sakau?” · “dedah semua termasuk UJSB” · “jenama Islam disasar” · “TH lebih penting daripada PAU” · dakwaan aset dijual kepada bukan Islam/China.</p><p><b>Status bukti:</b> laporan asal = <strong>Gred C / research lead</strong>; kenyataan politik yang disahkan media = B; posting sosial tanpa konteks penuh = D sehingga disahkan pada sumber asal. · <b>Last verified:</b> 12 Sep 2026 · 22:03 MYT</p></section>\n\n'''
    s = s.replace(marker, block + marker, 1)

s = s.replace('Maklumat disemak hingga · 11 Sep 2026 · 23:37 MYT', 'Maklumat naratif disemak hingga · 12 Sep 2026 · 22:03 MYT', 1)

p.write_text(s, encoding='utf-8')
print('Integrated political/social-media research into Narrative Audit')
