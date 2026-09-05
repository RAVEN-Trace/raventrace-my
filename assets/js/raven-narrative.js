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
    <div class="section-marker"><span>10</span><p>Narrative forensics · Lexicon</p></div>
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
