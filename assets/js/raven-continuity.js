(() => {
  if (window.__RAVEN_CONTINUITY_V1__) return;
  window.__RAVEN_CONTINUITY_V1__ = true;

  const q = (s, r = document) => r.querySelector(s);
  const qa = (s, r = document) => [...r.querySelectorAll(s)];
  const path = location.pathname;
  const isStory = document.body.classList.contains('story-page') || /\/raventrace-my\/news\/\d{4}\//.test(path);
  if (!isStory) return;

  if (!q('link[data-raven-continuity]')) {
    const css = document.createElement('link');
    css.rel = 'stylesheet';
    css.href = '/raventrace-my/assets/css/raven-continuity.css?v=1.0.0';
    css.dataset.ravenContinuity = 'true';
    document.head.appendChild(css);
  }

  document.body.classList.add('raven-story-continuity');

  const caseBase = '/raventrace-my/investigations/rci-tabung-haji/';
  const newsroom = '/raventrace-my/news/';
  const currentStory = '/raventrace-my/news/2026/09/07/azeez-jamil-azmi-dijangka-didakwa/';
  const jamilStory = '/raventrace-my/news/2026/09/06/jamil-khir-reman-checkpoint/';

  const registry = {
    [currentStory]: {
      category: 'Penguatkuasaan',
      related: [
        ['Artikel berkaitan', 'Kenapa Jamil Khir direman hingga 8 September?', jamilStory],
        ['Status individu', 'Siapa yang sudah didakwa, direman atau dibebaskan?', `${caseBase}#people`],
        ['Kronologi', 'Lihat timeline penuh RCI Tabung Haji', `${caseBase}#timeline`]
      ]
    },
    [jamilStory]: {
      category: 'Penguatkuasaan',
      related: [
        ['Perkembangan baharu', 'Azeez, Jamil dan Azmi: apa yang dilaporkan — dan apa yang belum disahkan?', currentStory],
        ['Status individu', 'Siapa yang sudah didakwa, direman atau dibebaskan?', `${caseBase}#people`],
        ['Kronologi', 'Lihat timeline penuh RCI Tabung Haji', `${caseBase}#timeline`]
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
        ['Perkembangan baharu', 'Azeez, Jamil dan Azmi: developing prosecution claim', currentStory]
      ]
    }
  };

  const fallback = {
    category: 'RCI Tabung Haji',
    related: [
      ['Kronologi', 'Lihat timeline penuh RCI Tabung Haji', `${caseBase}#timeline`],
      ['Status individu', 'Siapa yang sudah didakwa, direman atau dibebaskan?', `${caseBase}#people`],
      ['Perkembangan', 'Lihat perkembangan terbaru siasatan', newsroom]
    ]
  };

  const config = registry[path] || fallback;
  const storyTitle = (q('.story-hero h1')?.textContent || document.title).replace(/\s+/g, ' ').trim();

  const track = (kind, label, href) => {
    try { window.RavenAnalytics?.track?.('continuity_click', { kind, label, href, from: path }); } catch { /* tracking must never block navigation */ }
  };

  const prepareLink = (a, kind, label) => {
    if (!a) return a;
    a.dataset.continuity = kind;
    a.addEventListener('click', () => track(kind, label || a.textContent.trim(), a.href), { passive: true });
    return a;
  };

  const breadcrumb = () => {
    const container = q('.story-hero .container');
    if (!container || q('.raven-story-breadcrumb', container)) return;
    const nav = document.createElement('nav');
    nav.className = 'raven-story-breadcrumb';
    nav.setAttribute('aria-label', 'Kedudukan artikel dalam siasatan');
    nav.innerHTML = `
      <a href="${caseBase}">RCI Tabung Haji</a>
      <span aria-hidden="true">→</span>
      <a href="${newsroom}">${config.category}</a>
      <span aria-hidden="true">→</span>
      <span aria-current="page">Artikel semasa</span>`;
    qa('a', nav).forEach((a) => prepareLink(a, 'breadcrumb', a.textContent.trim()));
    const kicker = q('.story-kicker', container);
    if (kicker) kicker.insertAdjacentElement('beforebegin', nav);
    else container.prepend(nav);
  };

  const buildRelated = () => {
    const body = q('.story-body');
    if (!body || q('.raven-deeper', body)) return;
    const section = document.createElement('aside');
    section.className = 'raven-deeper';
    section.setAttribute('aria-label', 'Dalami kes ini');
    section.innerHTML = '<div class="raven-deeper-head"><span>DALAMI KES</span><strong>Artikel ini sebahagian daripada siasatan yang lebih besar.</strong></div>';
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
    else {
      const firstH2 = q('h2', body);
      if (firstH2) firstH2.insertAdjacentElement('beforebegin', section);
      else body.prepend(section);
    }
  };

  const buildContinue = () => {
    const body = q('.story-body');
    if (!body || q('.raven-continue', body)) return;
    const section = document.createElement('section');
    section.className = 'raven-continue';
    section.setAttribute('aria-label', 'Teruskan membaca');
    section.innerHTML = '<p class="raven-continue-kicker">TERUSKAN MEMBACA</p><h2>Jangan berhenti pada satu artikel.</h2><p class="raven-continue-dek">Ikuti konteks, kronologi dan status individu supaya satu perkembangan tidak dibaca di luar keseluruhan rekod.</p>';
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
    if (sources) sources.insertAdjacentElement('afterend', section);
    else {
      const note = q('.story-note', body);
      if (note) note.insertAdjacentElement('beforebegin', section);
      else body.appendChild(section);
    }
  };

  const humanizeExistingLinks = () => {
    const heroButtons = qa('.story-actions a, .story-actions button');
    heroButtons.forEach((node) => {
      const text = (node.textContent || '').trim().toLowerCase();
      if (text.includes('evidence snapshot')) node.textContent = 'Lihat status bukti kes';
    });

    qa('.story-side-card').forEach((card) => {
      const heading = q('h2', card)?.textContent.trim().toLowerCase();
      if (heading !== 'jejak lanjut') return;
      const links = qa('a', card);
      links.forEach((a) => {
        const href = a.getAttribute('href') || '';
        if (href.includes('/news/')) a.textContent = 'Lihat perkembangan terbaru →';
        else if (href.includes('#people')) a.textContent = 'Siapa yang terlibat dan status mereka →';
        else if (href.includes('#sources')) a.textContent = 'Semak sumber dan dokumen →';
        prepareLink(a, 'sidebar_related', a.textContent.trim());
      });
    });
  };

  const buildMobileBar = () => {
    if (q('.raven-mobile-continuity')) return;
    const nav = document.createElement('nav');
    nav.className = 'raven-mobile-continuity';
    nav.setAttribute('aria-label', 'Navigasi pantas siasatan');
    const items = [
      ['Timeline', `${caseBase}#timeline`],
      ['Individu', `${caseBase}#people`],
      ['Duit', `${caseBase}#money`],
      ['Sumber', `${caseBase}#sources`]
    ];
    items.forEach(([label, href]) => {
      const a = document.createElement('a');
      a.href = href;
      a.textContent = label;
      prepareLink(a, 'mobile_sticky', label);
      nav.appendChild(a);
    });
    document.body.appendChild(nav);
  };

  breadcrumb();
  humanizeExistingLinks();
  buildRelated();
  buildContinue();
  buildMobileBar();

  try {
    window.RavenAnalytics?.track?.('continuity_impression', {
      story: storyTitle,
      path,
      related_count: String(config.related.length)
    });
  } catch { /* optional */ }
})();
