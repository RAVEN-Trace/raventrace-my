(() => {
  if (window.__RAVEN_CONTINUITY_V2__) return;
  window.__RAVEN_CONTINUITY_V2__ = true;

  const q = (s, r = document) => r.querySelector(s);
  const qa = (s, r = document) => [...r.querySelectorAll(s)];
  const path = location.pathname;
  const caseBase = '/raventrace-my/investigations/rci-tabung-haji/';
  const desk = '/raventrace-my/investigations/';
  const newsroom = '/raventrace-my/news/';

  if (!q('link[data-raven-continuity]')) {
    const css = document.createElement('link');
    css.rel = 'stylesheet';
    css.href = '/raventrace-my/assets/css/raven-continuity.css?v=2.0.0';
    css.dataset.ravenContinuity = 'true';
    document.head.appendChild(css);
  }

  const isStory = document.body.classList.contains('story-page') || /\/raventrace-my\/news\/\d{4}\//.test(path);
  const isHome = path === '/raventrace-my/' || path.endsWith('/raventrace-my/index.html') || path === '/';
  const isNewsroom = path === '/raventrace-my/news/' || path.endsWith('/raventrace-my/news/index.html');
  const isDesk = path === '/raventrace-my/investigations/' || path.endsWith('/raventrace-my/investigations/index.html');
  const isCase = path.includes('/raventrace-my/investigations/rci-tabung-haji');
  const isMethodology = path.includes('/raventrace-my/methodology');
  const isAbout = path.includes('/raventrace-my/about');

  const track = (kind, label, href) => {
    try { window.RavenAnalytics?.track?.('continuity_click', { kind, label, href, from: path }); } catch { /* optional */ }
  };

  const prepareLink = (a, kind, label) => {
    if (!a) return a;
    a.dataset.continuity = kind;
    a.addEventListener('click', () => track(kind, label || a.textContent.trim(), a.href), { passive: true });
    return a;
  };

  const questionLinks = [
    ['Apa berlaku?', 'Ringkasan kes', `${caseBase}#briefing`, 'BRIEFING'],
    ['Apa terbaru?', 'Perkembangan semasa', `${caseBase}#updates`, 'UPDATES'],
    ['Siapa terlibat?', 'Status individu', `${caseBase}#people`, 'PEOPLE'],
    ['Bila ia berlaku?', 'Timeline penuh', `${caseBase}#timeline`, 'TIMELINE'],
    ['Ke mana wang pergi?', 'Jejak wang & angka', `${caseBase}#money`, 'MONEY'],
    ['Mana buktinya?', 'Sumber & dokumen', `${caseBase}#sources`, 'SOURCES']
  ];

  const buildQuestionRail = (anchor, mode = 'block') => {
    if (!anchor || q('.raven-question-rail')) return;
    const section = document.createElement('section');
    section.className = `raven-question-rail ${mode}`;
    section.setAttribute('aria-label', 'Dalami siasatan RCI Tabung Haji');
    section.innerHTML = '<div class="raven-question-head"><span>DALAMI SIASATAN</span><strong>Baca ikut soalan yang kau mahu jawab.</strong><p>Bahasa pembaca di depan; CASEFILE dan bukti kekal satu klik di belakang.</p></div>';
    const grid = document.createElement('div');
    grid.className = 'raven-question-grid';
    questionLinks.forEach(([question, label, href, protocol]) => {
      const a = document.createElement('a');
      a.href = href;
      a.innerHTML = `<small>${protocol}</small><strong>${question}</strong><span>${label}</span><b aria-hidden="true">→</b>`;
      prepareLink(a, 'investigation_question', question);
      grid.appendChild(a);
    });
    section.appendChild(grid);
    anchor.insertAdjacentElement('afterend', section);
  };

  const buildContextBridge = (anchor, variant) => {
    if (!anchor || q(`.raven-context-bridge[data-variant="${variant}"]`)) return;
    const copy = {
      home: ['DALAMI SIASATAN', 'Jangan berhenti pada headline.', 'Masuk terus ke timeline, individu, wang dan sumber RCI Tabung Haji.'],
      newsroom: ['KONTEKS KES', 'Berita ialah perkembangan. Siasatan menyimpan keseluruhan rekod.', 'Gunakan CASEFILE untuk melihat apa berlaku sebelum dan selepas sesuatu headline.'],
      methodology: ['KAEDAH → KES SEBENAR', 'Lihat bagaimana evidence discipline digunakan pada rekod sebenar.', 'FACT, CLAIM, DISPUTED dan UNKNOWN lebih berguna bila pembaca boleh melihat aplikasinya.'],
      about: ['LIHAT RAVEN BEKERJA', 'Identiti diterangkan di sini. Siasatan menunjukkan kaedah itu digunakan.', 'Buka investigation aktif untuk melihat konteks, individu, timeline, wang dan sumber.']
    }[variant];
    if (!copy) return;
    const section = document.createElement('section');
    section.className = 'raven-context-bridge';
    section.dataset.variant = variant;
    section.innerHTML = `<div class="raven-context-copy"><span>${copy[0]}</span><h2>${copy[1]}</h2><p>${copy[2]}</p></div>`;
    const links = document.createElement('div');
    links.className = 'raven-context-links';
    const chosen = variant === 'methodology'
      ? [questionLinks[0], questionLinks[4], questionLinks[5]]
      : variant === 'about'
        ? [questionLinks[0], questionLinks[2], questionLinks[5]]
        : [questionLinks[1], questionLinks[2], questionLinks[4], questionLinks[5]];
    chosen.forEach(([question, label, href, protocol]) => {
      const a = document.createElement('a');
      a.href = href;
      a.innerHTML = `<small>${protocol}</small><strong>${question}</strong><span>${label}</span><b aria-hidden="true">→</b>`;
      prepareLink(a, `context_${variant}`, question);
      links.appendChild(a);
    });
    const deskLink = document.createElement('a');
    deskLink.className = 'raven-context-desk';
    deskLink.href = desk;
    deskLink.textContent = 'Buka Meja Siasatan →';
    prepareLink(deskLink, `context_${variant}`, 'Buka Meja Siasatan');
    section.append(links, deskLink);
    anchor.insertAdjacentElement('afterend', section);
  };

  const buildMobileBar = () => {
    if (q('.raven-mobile-continuity')) return;
    const nav = document.createElement('nav');
    nav.className = 'raven-mobile-continuity';
    nav.setAttribute('aria-label', 'Navigasi pantas siasatan');
    [['Terkini', '#updates'], ['Individu', '#people'], ['Duit', '#money'], ['Sumber', '#sources']].forEach(([label, hash]) => {
      const a = document.createElement('a');
      a.href = `${caseBase}${hash}`;
      a.textContent = label;
      prepareLink(a, 'mobile_sticky', label);
      nav.appendChild(a);
    });
    document.body.appendChild(nav);
  };

  if (isDesk) {
    document.body.classList.add('raven-investigation-continuity');
    const meta = q('.investigation-lead .investigation-meta-grid');
    if (meta) buildQuestionRail(meta, 'desk');
    const buttons = qa('.investigation-lead .btn-row a');
    buttons.forEach((a) => {
      const href = a.getAttribute('href') || '';
      if (href.includes('#briefing')) a.textContent = 'Baca ringkasan kes';
      else if (href.endsWith('/rci-tabung-haji/')) a.textContent = 'Lihat semua jejak';
      else if (href.includes('#sources')) a.textContent = 'Semak sumber & dokumen';
      prepareLink(a, 'desk_primary', a.textContent.trim());
    });
    const heroStatus = q('.investigation-status-line');
    if (heroStatus && !q('.raven-desk-spine-note', heroStatus.parentElement)) {
      const note = document.createElement('p');
      note.className = 'raven-desk-spine-note';
      note.textContent = 'Siasatan ialah hub: pilih soalan, bukan format.';
      heroStatus.insertAdjacentElement('afterend', note);
    }
  }

  if (isCase) {
    document.body.classList.add('raven-investigation-continuity');
    const hero = q('.case-hero');
    if (hero) buildQuestionRail(hero, 'case');
    buildMobileBar();
  }

  if (isHome) {
    const anchor = q('#latest') || q('.signal-strip') || q('.front-hero');
    buildContextBridge(anchor, 'home');
  }

  if (isNewsroom) {
    const anchor = q('.article-header') || q('main > section');
    buildContextBridge(anchor, 'newsroom');
  }

  if (isMethodology) {
    const sections = qa('main > section');
    const anchor = sections[sections.length - 1] || q('main');
    buildContextBridge(anchor, 'methodology');
  }

  if (isAbout) {
    const sections = qa('main > section');
    const anchor = sections[sections.length - 1] || q('main');
    buildContextBridge(anchor, 'about');
  }

  if (isStory) {
    document.body.classList.add('raven-story-continuity');
    const currentStory = '/raventrace-my/news/2026/09/07/azeez-jamil-azmi-dijangka-didakwa/';
    const jamilStory = '/raventrace-my/news/2026/09/08/jamil-khir-dilepaskan-jaminan-sprm/';
    const registry = {
      [currentStory]: {
        category: 'Penguatkuasaan',
        related: [
          ['Perkembangan disahkan', 'Jamil Khir dilepaskan dengan jaminan SPRM selepas reman tamat', jamilStory],
          ['Status individu', 'Siapa yang sudah didakwa, direman atau dilepaskan?', `${caseBase}#people`],
          ['Kronologi', 'Lihat timeline penuh RCI Tabung Haji', `${caseBase}#timeline`]
        ]
      },
      [jamilStory]: {
        category: 'Penguatkuasaan',
        related: [
          ['Status individu', 'Apa beza direman, dilepaskan, didakwa dan NFA?', `${caseBase}#people`],
          ['Kronologi', 'Lihat timeline penuh RCI Tabung Haji', `${caseBase}#timeline`],
          ['Sumber', 'Semak dokumen dan laporan sokongan', `${caseBase}#sources`]
        ]
      },
      ['/raventrace-my/news/2026/09/04/madinah-rashid-rekod-bercanggah/']: {
        category: 'Rekod bercanggah',
        related: [
          ['Rekod', 'Apa sebenarnya yang bercanggah antara dua versi ini?', `${caseBase}#disputed-record`],
          ['Kronologi', 'Lihat timeline penuh RCI Tabung Haji', `${caseBase}#timeline`],
          ['Sumber', 'Semak dokumen dan sumber yang menyokong rekod', `${caseBase}#sources`]
        ]
      },
      ['/raventrace-my/news/2026/09/03/reformasi-tadbir-urus-tabung-haji/']: {
        category: 'Tadbir urus',
        related: [
          ['Pembaharuan', 'Apa yang sudah berubah selepas RCI — dan apa yang belum selesai?', `${caseBase}#governance`],
          ['Kronologi', 'Lihat timeline penuh RCI Tabung Haji', `${caseBase}#timeline`],
          ['Sumber', 'Semak dokumen dan sumber pembaharuan', `${caseBase}#sources`]
        ]
      },
      ['/raventrace-my/news/2026/09/03/thp-bina-rm72000/']: {
        category: 'Mahkamah',
        related: [
          ['Status individu', 'Siapa yang telah didakwa — dan siapa masih dalam siasatan?', `${caseBase}#people`],
          ['Kronologi', 'Lihat timeline penuh RCI Tabung Haji', `${caseBase}#timeline`],
          ['Sumber', 'Semak sumber dan dokumen mahkamah', `${caseBase}#sources`]
        ]
      }
    };
    const fallback = {
      category: 'RCI Tabung Haji',
      related: [
        ['Kronologi', 'Lihat timeline penuh RCI Tabung Haji', `${caseBase}#timeline`],
        ['Status individu', 'Siapa yang sudah didakwa, direman atau dilepaskan?', `${caseBase}#people`],
        ['Perkembangan', 'Lihat perkembangan terbaru siasatan', newsroom]
      ]
    };
    const config = registry[path] || fallback;

    const container = q('.story-hero .container');
    if (container && !q('.raven-story-breadcrumb', container)) {
      const nav = document.createElement('nav');
      nav.className = 'raven-story-breadcrumb';
      nav.setAttribute('aria-label', 'Kedudukan artikel dalam siasatan');
      nav.innerHTML = `<a href="${desk}">Siasatan</a><span aria-hidden="true">→</span><a href="${caseBase}">RCI Tabung Haji</a><span aria-hidden="true">→</span><span aria-current="page">${config.category}</span>`;
      qa('a', nav).forEach((a) => prepareLink(a, 'breadcrumb', a.textContent.trim()));
      const kicker = q('.story-kicker', container);
      if (kicker) kicker.insertAdjacentElement('beforebegin', nav); else container.prepend(nav);
    }

    const body = q('.story-body');
    if (body && !q('.raven-deeper', body)) {
      const section = document.createElement('aside');
      section.className = 'raven-deeper';
      section.setAttribute('aria-label', 'Dalami kes ini');
      section.innerHTML = '<div class="raven-deeper-head"><span>KONTEKS KES</span><strong>Artikel ini cuma satu perkembangan dalam siasatan yang lebih besar.</strong></div>';
      const list = document.createElement('div');
      list.className = 'raven-deeper-list';
      config.related.forEach(([eyebrow, label, href], index) => {
        const a = document.createElement('a');
        a.className = index === 0 ? 'raven-deeper-link lead' : 'raven-deeper-link';
        a.href = href;
        a.innerHTML = `<small>${eyebrow}</small><span>${label}</span><b aria-hidden="true">→</b>`;
        prepareLink(a, index === 0 ? 'inline_primary' : 'inline_related', label);
        list.appendChild(a);
      });
      section.appendChild(list);
      const grid = q('.story-fact-grid', body);
      if (grid) grid.insertAdjacentElement('afterend', section);
      else { const firstH2 = q('h2', body); if (firstH2) firstH2.insertAdjacentElement('beforebegin', section); else body.prepend(section); }
    }

    if (body && !q('.raven-continue', body)) {
      const section = document.createElement('section');
      section.className = 'raven-continue';
      section.setAttribute('aria-label', 'Teruskan membaca');
      section.innerHTML = '<p class="raven-continue-kicker">TERUSKAN MENYIASAT</p><h2>Jangan berhenti pada satu headline.</h2><p class="raven-continue-dek">Ikuti konteks, kronologi dan status individu supaya satu perkembangan tidak dibaca di luar keseluruhan rekod.</p>';
      const list = document.createElement('div');
      list.className = 'raven-continue-list';
      config.related.forEach(([eyebrow, label, href], index) => {
        const a = document.createElement('a');
        a.href = href;
        a.innerHTML = `<span class="raven-continue-no">0${index + 1}</span><span><small>${eyebrow}</small><strong>${label}</strong></span><b aria-hidden="true">→</b>`;
        prepareLink(a, 'continue_reading', label);
        list.appendChild(a);
      });
      section.appendChild(list);
      const sources = q('.story-source-list', body);
      if (sources) sources.insertAdjacentElement('afterend', section); else body.appendChild(section);
    }
    buildMobileBar();
  }

  try { window.RavenAnalytics?.track?.('continuity_impression', { path, version: '2.0' }); } catch { /* optional */ }
})();
