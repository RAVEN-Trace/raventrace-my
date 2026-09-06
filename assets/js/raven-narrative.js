(() => {
  if (!window.location.pathname.includes('/raventrace-my/investigations/rci-tabung-haji')) return;
  if (document.querySelector('#narrative-audit')) return;

  const q = (s, r = document) => r.querySelector(s);
  const qa = (s, r = document) => [...r.querySelectorAll(s)];

  if (!q('link[data-raven-narrative]')) {
    const css = document.createElement('link');
    css.rel = 'stylesheet';
    css.href = '/raventrace-my/assets/css/raven-narrative.css?v=1.0.0';
    css.dataset.ravenNarrative = 'true';
    document.head.appendChild(css);
  }

  if (!q('link[data-raven-transplant]')) {
    const css = document.createElement('link');
    css.rel = 'stylesheet';
    css.href = '/raventrace-my/assets/css/raven-case-transplant.css?v=1.0.0';
    css.dataset.ravenTransplant = 'true';
    document.head.appendChild(css);
  }

  const addSourceRow = (id, grade, href, title, note) => {
    const list = q('#sources .sources-grid');
    if (!list || q(`#${id}`)) return;
    const li = document.createElement('li');
    li.id = id;
    li.innerHTML = `<span>${grade}</span><a href="${href}" rel="noopener noreferrer">${title}</a><small>${note}</small>`;
    list.appendChild(li);
  };

  addSourceRow('s44','B','https://www.malaymail.com/news/malaysia/2026/09/03/tabung-haji-act-amendments-in-final-stages-before-parliamentary-tabling-says-th-ceo/233776','19/25 syor selesai + pindaan Akta >90%','Malay Mail / Bernama · 3 Sep');
  addSourceRow('s45','B','https://berita.rtm.gov.my/nasional/senarai-berita-nasional/senarai-artikel/pengurusan-tabung-haji-wajar-dikawal-selia-lebih-ketat-pm/','PM sokong kawal selia TH lebih ketat','RTM / Bernama · 4 Sep');
  addSourceRow('s46','B','https://berita.rtm.gov.my/nasional/senarai-berita-nasional/senarai-artikel/isu-th-rakyat-mahu-siasatan-sprm-dilaksana-secara-telus/','Beberapa responden mahu siasatan lebih telus','RTM · 5 Sep');
  addSourceRow('s47','E','https://www.malaymail.com/news/what-you-think/2026/09/05/what-happens-when-too-few-people-say-no-noor-adwa-sulaiman/233962','Analisis tadbir urus: semak dan imbang','Malay Mail · komentar · 5 Sep');
  addSourceRow('s48','B','https://www.malaysiakini.com/news/783373','Reman awal Jamil Khir lima hari','Malaysiakini · 2 Sep');
  addSourceRow('s49','B','https://web26.bernama.com/bm/jenayah_mahkamah/news.php?id=2603643','Reman bekas menteri disambung dua hari','Bernama · 6 Sep · Mahkamah Majistret Putrajaya');
  addSourceRow('s50','B','https://bernama.com/radio/news.php?id=2602611','RM11.5b sukuk UJSB ialah pembiayaan semula','Bernama · 3 Sep');

  const heroDate = q('.case-hero .date-chip');
  if (heroDate) heroDate.textContent = 'Data cut-off · 7 Sep 2026 · awal pagi MYT';
  const description = q('meta[name="description"]');
  if (description) description.content = 'CASEFILE RCI Tabung Haji v16: RCI, penguatkuasaan, individu, 14 pelaburan, tadbir urus, UJSB, pertikaian rekod, jurang bukti dan sumber awam hingga 7 September 2026.';
  const sourceNote = q('#sources .source-note');
  if (sourceNote) sourceNote.innerHTML = '<strong>Data cut-off:</strong> 7 September 2026 · awal pagi MYT. <strong>Semakan laman:</strong> 7 September 2026. Kompilasi penyelidikan digunakan sebagai indeks kerja dan disemak silang dengan rekod awam; jika kompilasi bercanggah dengan rekod primer atau mahkamah, status dikekalkan sebagai disputed atau unknown sehingga disahkan.';

  const docket = q('.case-rail section dl');
  if (docket && !q('[data-rci-pages]', docket)) {
    const row = document.createElement('div');
    row.dataset.rciPages = 'true';
    row.innerHTML = '<dt>Laporan RCI</dt><dd>211 halaman</dd>';
    docket.appendChild(row);
  }

  const jamil = qa('.person-card').find((card) => q('h3', card)?.textContent.includes('Jamil Khir'));
  if (jamil) {
    const status = q(':scope > div .status', jamil);
    if (status) { status.className = 'status process'; status.textContent = 'Reman disambung · hingga 8 Sep'; }
    const body = qa(':scope > p', jamil).find((p) => !p.classList.contains('role'));
    if (body) body.textContent = 'Selepas reman lima hari bermula 2 September, Mahkamah Majistret Putrajaya membenarkan sambungan dua hari bagi 7–8 September. SPRM menyatakan kes disiasat di bawah Seksyen 16(a)(A) Akta SPRM 2009. Reman bukan pertuduhan atau dapatan kesalahan.';
    const refs = qa('a[href^="#s"]', jamil);
    if (!refs.some((a) => a.getAttribute('href') === '#s49')) {
      const a = document.createElement('a'); a.href = '#s49'; a.textContent = 'S49'; jamil.append(' ', a);
    }
  }

  const updates = q('#updates');
  const stack = q('.trace-stack', updates);
  if (updates && stack && !q('[data-sep6-update]', stack)) {
    const heading = q('h2', updates);
    if (heading) heading.textContent = 'Lima perkembangan yang mengubah kedudukan kes.';
    const card = document.createElement('article');
    card.className = 'trace-card';
    card.dataset.sep6Update = 'true';
    card.innerHTML = '<div class="trace-head"><span>JEJAK / 00</span><time datetime="2026-09-06">6 Sep 2026 · awal pagi</time></div><div class="meta-row"><span class="status unknown">Checkpoint hari ini</span><span class="source-grade">Gred B</span></div><h3>Mahkamah membenarkan sambungan reman bekas menteri dua hari hingga 8 September.</h3><dl><div><dt>Apa diketahui?</dt><dd>Reman disambung bagi 7–8 September selepas permohonan SPRM.</dd></div><div><dt>Asas siasatan?</dt><dd>SPRM menyatakan kes disiasat di bawah Seksyen 16(a)(A) Akta SPRM 2009.</dd></div><div><dt>Had</dt><dd>Reman bukan pertuduhan atau sabitan; tindakan selepas 8 September masih belum diketahui.</dd></div></dl><p class="inline-sources"><a href="#s49">S49</a> <a href="#s22">S22</a></p>';
    stack.prepend(card);
  }

  const governance = q('#governance');
  if (governance && !q('[data-reform-status]', governance)) {
    const box = document.createElement('div');
    box.className = 'case-warning light';
    box.dataset.reformStatus = 'true';
    box.innerHTML = '<strong>Status pembaharuan · 3–4 Sep</strong><span>TH melaporkan 19 daripada 25 syor RCI telah selesai dan enam masih dalam tindakan. Pindaan Akta TH pula melepasi 90% di peringkat dalaman, tetapi masih perlu melalui proses kerajaan dan Parlimen. TH menyatakan SC dipilih untuk mengawal selia bahagian pelaburan, manakala Perdana Menteri turut menyebut SC dan BNM dalam kerangka pengawasan lebih ketat.</span><p class="inline-sources"><a href="#s44">S44</a> <a href="#s45">S45</a></p>';
    const grid = q('.control-grid', governance);
    if (grid) governance.insertBefore(box, grid);
  }

  const alRawda = qa('.investment').find((item) => q('summary strong', item)?.textContent.trim() === 'Al-Rawda');
  if (alRawda && !q('[data-alrawda-reconcile]', alRawda)) {
    const body = q('.investment-body', alRawda);
    if (body) {
      const note = document.createElement('div');
      note.dataset.alrawdaReconcile = 'true';
      note.innerHTML = '<h4>Disputed metric · impairment</h4><p>Rekod awam menggunakan sekurang-kurangnya dua angka bagi impairment/kerugian Al-Rawda: sekitar RM1.0b dalam satu penerangan rasmi dan sekitar RM1.86b dalam laporan lain terhadap ucapan Dewan Rakyat. RAVEN-Trace tidak menyatukan kedua-duanya sehingga definisi, tarikh ukuran atau pecahan perakaunan dapat dijelaskan.</p>';
      body.insertBefore(note, body.lastElementChild);
    }
  }

  const cards = [
    {
      tone: 'amber', label: 'Audit ≠ penyiasatan jenayah', verdict: 'KESIMPULAN TERLALU JAUH',
      claim: '“Audit tak jumpa bukti kecurian. Jadi memang tak ada apa-apa salah.”',
      record: 'Audit kewangan, siasatan jenayah dan RCI menjawab soalan yang berbeza. RCI kemudian merekodkan kelemahan tadbir urus, pelaburan dan pelaporan kewangan yang tetap perlu dinilai.',
      gap: 'Tiada penemuan kecurian dalam sesuatu audit tidak sama dengan bukti bahawa setiap keputusan, pelaburan atau kawalan tadbir urus bebas daripada masalah.',
      sources: ['s14','s15','s01']
    },
    {
      tone: 'red', label: 'RCI ≠ mahkamah jenayah', verdict: 'MENGELIRUKAN',
      claim: '“RCI tak sebut siapa ‘sakau’. Maknanya RCI tak jumpa salah laku.”',
      record: 'RCI bukan mahkamah yang menentukan siapa bersalah. Ia merekodkan masalah institusi dan mengesyorkan pemeriksaan lanjut terhadap 14 pelaburan.',
      gap: 'Ketiadaan nama “pencuri” dalam laporan RCI tidak memadam dapatan tadbir urus. Pada masa yang sama, dapatan RCI juga bukan sabitan jenayah terhadap individu.',
      sources: ['s01','s02','s18']
    },
    {
      tone: 'red', label: 'Semak tarikh sebelum simpul motif', verdict: 'TIDAK SELARI DENGAN REKOD',
      claim: '“RCI ini ciptaan PH untuk menyerang lawan politik.”',
      record: 'Rekod rasmi menyatakan RCI Tabung Haji dilantik oleh Yang di-Pertuan Agong pada 20 Januari 2022.',
      gap: 'Tarikh pelantikan boleh diperiksa. Dakwaan tentang motif politik memerlukan bukti tambahan; ia tidak boleh dibuktikan hanya melalui slogan atau andaian tentang siapa mendapat manfaat politik.',
      sources: ['s01','s16']
    },
    {
      tone: 'violet', label: 'Timing ≠ bukti kandungan palsu', verdict: 'INFERENS TANPA BUKTI',
      claim: '“Laporan keluar masa pilihan raya. Jadi semua dapatan itu permainan politik.”',
      record: 'Masa penerbitan memang boleh menjadi soalan yang sah tentang komunikasi politik. Tetapi tarikh penerbitan sahaja tidak membuktikan dokumen, angka atau dapatan di dalam laporan itu palsu.',
      gap: 'Untuk menolak dapatan kerana politik, perlu tunjuk bukti khusus bahawa rekod, angka atau proses telah diubah, direka atau disalahwakili.',
      sources: ['s16','s01']
    },
    {
      tone: 'green', label: 'Kerugian ≠ kecurian', verdict: 'SALAH PERSAMAAN',
      claim: '“Kalau rugi berbilion, maknanya wang itu dicuri.”',
      record: 'Rekod awam membezakan kerugian, rosot nilai, nilai pasaran, nilai pindahan dan kos pemulihan. Semua angka itu tidak membawa maksud undang-undang yang sama.',
      gap: 'Untuk membuktikan kecurian atau kesalahan jenayah, perlu jejak transaksi, penerima manfaat, perbuatan, niat dan elemen kesalahan yang berkaitan.',
      sources: ['s02','s30']
    },
    {
      tone: 'amber', label: 'Nombor sama ≠ dataset sama', verdict: 'PERLU DIPISAHKAN',
      claim: '“Ada 14 pelaburan bermasalah dan 14 kertas siasatan. Jadi itu 14 kes jenayah yang sama.”',
      record: 'RCI menyenaraikan 14 pelaburan untuk pemeriksaan lanjut. SPRM pula melaporkan 14 kertas siasatan. Pemetaan satu-ke-satu antara kedua-dua senarai itu belum diterbitkan secara lengkap.',
      gap: 'Empat kertas SPRM juga telah diklasifikasikan NFA setakat 2 September. Nombor yang sama tidak membuktikan setiap pelaburan menjadi satu kes jenayah.',
      sources: ['s03','s19']
    }
  ];

  const section = document.createElement('section');
  section.className = 'case-section';
  section.id = 'narrative-audit';
  section.innerHTML = `
    <div class="section-marker"><span>N1</span><p>Narrative forensics · Lexicon</p></div>
    <h2>Orang kata. Ini rekodnya.</h2>
    <p class="section-lead">Raven semak ayat yang nampak meyakinkan, kemudian asingkan apa yang benar, apa yang hilang daripada konteks, dan di mana kesimpulan melompat lebih jauh daripada bukti.</p>
    <div class="narrative-intro"><span>Dakwaan</span><i>→</i><span>Rekod</span><i>→</i><span>Konteks hilang</span><i>→</i><span>Verdict</span></div>
    <div class="narrative-audit-grid"></div>
    <div class="narrative-rule"><strong>Had Raven:</strong> Bahasa boleh menunjukkan framing, omission dan lompatan logik. Bahasa sahaja tidak membuktikan niat menipu, rasuah atau kesalahan jenayah.</div>`;

  const grid = q('.narrative-audit-grid', section);
  cards.forEach((item, index) => {
    const card = document.createElement('article');
    card.className = 'narrative-card';
    card.dataset.tone = item.tone;
    const sourceLinks = item.sources.map((id) => {
      const row = q(`#${id}`);
      const link = row ? q('a[href^="http"]', row) : null;
      const title = link?.textContent?.trim() || id.toUpperCase();
      const href = link?.href || `#${id}`;
      return `<a href="${href}" ${link ? 'target="_blank" rel="noopener noreferrer"' : ''} title="${title}">${id.toUpperCase()}</a>`;
    }).join('');
    card.innerHTML = `
      <header class="narrative-card-head">
        <div class="narrative-card-kicker"><span>0${index + 1} · ${item.label}</span><span class="narrative-verdict">${item.verdict}</span></div>
        <h3>${item.claim}</h3>
      </header>
      <div class="narrative-card-body">
        <dl>
          <div class="narrative-fact-row"><dt>Rekod tunjuk</dt><dd>${item.record}</dd></div>
          <div class="narrative-fact-row gap"><dt>Yang hilang</dt><dd>${item.gap}</dd></div>
        </dl>
        <div class="narrative-source-row"><span>Sumber</span>${sourceLinks}</div>
      </div>`;
    grid.appendChild(card);
  });

  const disputed = q('#disputed-record');
  if (disputed) disputed.insertAdjacentElement('beforebegin', section);
  else q('#tracks')?.insertAdjacentElement('afterend', section);

  const navInner = q('[data-case-nav] .container');
  if (navInner && !q('a[href="#narrative-audit"]', navInner)) {
    const link = document.createElement('a');
    link.href = '#narrative-audit';
    link.textContent = 'Naratif';
    const before = q('a[href="#disputed-record"]', navInner);
    if (before) navInner.insertBefore(link, before); else navInner.appendChild(link);

    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver((entries) => {
        const visible = entries.some((entry) => entry.isIntersecting);
        if (!visible) return;
        qa('a[href^="#"]', navInner).forEach((item) => item.classList.remove('active'));
        link.classList.add('active');
      }, { rootMargin: '-18% 0px -68% 0px', threshold: .08 });
      observer.observe(section);
    }
  }
})();
