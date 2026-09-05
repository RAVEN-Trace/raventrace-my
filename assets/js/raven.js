(() => {
  const navToggle = document.querySelector('[data-nav-toggle]');
  const nav = document.querySelector('[data-nav]');
  if (navToggle && nav) {
    navToggle.addEventListener('click', () => {
      const open = nav.classList.toggle('open');
      navToggle.setAttribute('aria-expanded', String(open));
      navToggle.textContent = open ? 'Tutup' : 'Menu';
    });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && nav.classList.contains('open')) {
        nav.classList.remove('open');
        navToggle.setAttribute('aria-expanded', 'false');
        navToggle.textContent = 'Menu';
        navToggle.focus();
      }
    });
  }

  document.querySelectorAll('[data-share]').forEach((button) => {
    button.addEventListener('click', async () => {
      const payload = { title: button.dataset.shareTitle || document.title, text: button.dataset.shareText || 'Semak laporan berasaskan bukti ini.', url: window.location.href };
      try {
        if (navigator.share) await navigator.share(payload);
        else {
          await navigator.clipboard.writeText(`${payload.text} ${payload.url}`);
          const original = button.textContent;
          button.textContent = 'Pautan disalin';
          window.setTimeout(() => { button.textContent = original; }, 1800);
        }
      } catch (error) { if (error.name !== 'AbortError') button.textContent = 'Salin gagal'; }
    });
  });

  const filters = document.querySelectorAll('[data-filter]');
  const items = document.querySelectorAll('[data-topic]');
  filters.forEach((button) => {
    button.setAttribute('aria-pressed', String(button.classList.contains('active')));
    button.addEventListener('click', () => {
      const selected = button.dataset.filter;
      filters.forEach((item) => {
        const active = item === button;
        item.classList.toggle('active', active);
        item.setAttribute('aria-pressed', String(active));
      });
      items.forEach((item) => { item.hidden = selected !== 'all' && item.dataset.topic !== selected; });
    });
  });

  const expandButton = document.querySelector('[data-expand-investments]');
  const investmentList = document.querySelector('[data-investment-list]');
  if (expandButton && investmentList) {
    const records = [...investmentList.querySelectorAll('details')];
    expandButton.addEventListener('click', () => {
      const shouldOpen = !records.every((record) => record.open);
      records.forEach((record) => { record.open = shouldOpen; });
      expandButton.setAttribute('aria-expanded', String(shouldOpen));
      expandButton.textContent = shouldOpen ? 'Tutup semua rekod' : 'Buka semua rekod';
    });
    records.forEach((record) => record.addEventListener('toggle', () => {
      const allOpen = records.every((item) => item.open);
      const allClosed = records.every((item) => !item.open);
      if (allOpen || allClosed) {
        expandButton.setAttribute('aria-expanded', String(allOpen));
        expandButton.textContent = allOpen ? 'Tutup semua rekod' : 'Buka semua rekod';
      }
    }));
  }

  const caseNav = document.querySelector('[data-case-nav]');
  if (caseNav && 'IntersectionObserver' in window) {
    const links = [...caseNav.querySelectorAll('a[href^="#"]')];
    const sections = links.map((link) => document.querySelector(link.getAttribute('href'))).filter(Boolean);
    const observer = new IntersectionObserver((entries) => {
      const visible = entries.filter((entry) => entry.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
      if (!visible) return;
      links.forEach((link) => link.classList.toggle('active', link.getAttribute('href') === `#${visible.target.id}`));
    }, { rootMargin: '-18% 0px -70% 0px', threshold: [0, 0.15, 0.35] });
    sections.forEach((section) => observer.observe(section));
  }

  if (!document.querySelector('link[data-raven-visuals]')) {
    const sheet = document.createElement('link');
    sheet.rel = 'stylesheet';
    sheet.href = '/raventrace-my/assets/css/raven-visuals.css?v=1.2.0';
    sheet.dataset.ravenVisuals = 'true';
    document.head.appendChild(sheet);
  }

  document.querySelectorAll('.brand').forEach((brand) => {
    if (brand.querySelector('.brand-seal')) return;
    const img = document.createElement('img');
    img.className = 'brand-seal';
    img.src = '/raventrace-my/assets/art/raven-trace-seal.webp';
    img.alt = '';
    img.setAttribute('aria-hidden', 'true');
    img.width = 48;
    img.height = 48;
    brand.prepend(img);
  });

  const createEditorialFigure = (src, alt, caption, className = '') => {
    const figure = document.createElement('figure');
    figure.className = `editorial-art ${className}`.trim();
    const frame = document.createElement('div');
    frame.className = 'editorial-art-frame';
    const img = document.createElement('img');
    img.src = src;
    img.alt = alt;
    img.loading = 'lazy';
    img.decoding = 'async';
    frame.appendChild(img);
    const badge = document.createElement('span');
    badge.className = 'editorial-art-badge';
    badge.textContent = 'ILUSTRASI EDITORIAL';
    const figcaption = document.createElement('figcaption');
    figcaption.textContent = caption;
    figure.append(frame, badge, figcaption);
    return figure;
  };

  const injectArtAfter = (anchor, src, alt, caption, className) => {
    if (!anchor || anchor.parentElement?.querySelector(`:scope > .${className}`)) return;
    anchor.insertAdjacentElement('afterend', createEditorialFigure(src, alt, caption, className));
  };

  const metaCache = new Map();
  const preferredDomains = ['freemalaysiatoday.com','thestar.com.my','sinarharian.com.my','astroawani.com','malaysiagazette.com','theedgemalaysia.com','malaymail.com','berita.rtm.gov.my','bernama.com','web26.bernama.com','islam.gov.my'];
  const isExternal = (href) => /^https?:\/\//i.test(href || '');
  const hostname = (url) => { try { return new URL(url).hostname.replace(/^www\./, ''); } catch { return 'sumber asal'; } };
  const chooseSource = (urls) => {
    const clean = [...new Set(urls.filter(Boolean))];
    if (!clean.length) return null;
    for (const domain of preferredDomains) {
      const hit = clean.find((url) => hostname(url).endsWith(domain));
      if (hit) return hit;
    }
    return clean[0];
  };
  const externalUrlsIn = (root) => [...root.querySelectorAll('a[href]')].map((link) => link.href).filter(isExternal).filter((url) => !url.includes('raven-trace.github.io'));
  const sourceUrlsFromCaseRefs = (root) => {
    const urls = [];
    root.querySelectorAll('a[href^="#s"]').forEach((ref) => {
      const target = document.querySelector(ref.getAttribute('href'));
      const source = target?.querySelector('a[href^="http"]');
      if (source) urls.push(source.href);
    });
    return urls;
  };
  const resolveSourceMeta = async (sourceUrl) => {
    if (!sourceUrl) return null;
    if (metaCache.has(sourceUrl)) return metaCache.get(sourceUrl);
    const task = (async () => {
      try {
        const endpoint = `https://api.microlink.io?url=${encodeURIComponent(sourceUrl)}&palette=false&audio=false&video=false&screenshot=false`;
        const response = await fetch(endpoint, { mode: 'cors', credentials: 'omit' });
        if (!response.ok) return null;
        const data = (await response.json())?.data;
        if (!data?.image?.url) return null;
        return { image: data.image.url, title: data.title || '', publisher: data.publisher || hostname(sourceUrl), url: sourceUrl };
      } catch { return null; }
    })();
    metaCache.set(sourceUrl, task);
    return task;
  };
  const createSourceFigure = async (sourceUrl, className = '', storyTitle = '') => {
    const meta = await resolveSourceMeta(sourceUrl);
    if (!meta?.image) return null;
    const figure = document.createElement('figure');
    figure.className = `source-story-visual ${className}`.trim();
    const frameLink = document.createElement('a');
    frameLink.className = 'source-story-frame';
    frameLink.href = sourceUrl;
    frameLink.rel = 'noopener noreferrer';
    frameLink.setAttribute('aria-label', `Buka sumber asal: ${storyTitle || meta.title || meta.publisher}`);
    const img = document.createElement('img');
    img.src = meta.image;
    img.alt = storyTitle ? `Gambar berkaitan berita: ${storyTitle}` : 'Gambar daripada artikel sumber asal';
    img.loading = 'lazy';
    img.decoding = 'async';
    img.referrerPolicy = 'no-referrer';
    img.addEventListener('error', () => figure.remove(), { once: true });
    frameLink.appendChild(img);
    const badge = document.createElement('span');
    badge.className = 'source-photo-badge';
    badge.textContent = 'FOTO SUMBER';
    const caption = document.createElement('figcaption');
    const source = document.createElement('a');
    source.href = sourceUrl;
    source.rel = 'noopener noreferrer';
    source.textContent = `Sumber gambar/berita: ${meta.publisher || hostname(sourceUrl)} →`;
    caption.appendChild(source);
    figure.append(frameLink, badge, caption);
    return figure;
  };
  const attachSourceFigure = async (container, sourceUrls, className) => {
    if (!container || container.querySelector(':scope > .source-story-visual')) return;
    const sourceUrl = chooseSource(sourceUrls);
    if (!sourceUrl) return;
    const title = container.querySelector('h1, h2, h3')?.textContent.trim() || '';
    const figure = await createSourceFigure(sourceUrl, className, title);
    if (!figure) { container.classList.add('source-image-unavailable'); return; }
    container.classList.add('has-source-visual');
    container.prepend(figure);
  };
  const addVisualPolicy = (container) => {
    if (!container || container.querySelector('.source-image-policy')) return;
    const note = document.createElement('p');
    note.className = 'source-image-policy';
    note.textContent = 'Foto pada berita datang daripada artikel sumber asal apabila tersedia. Ilustrasi RAVEN-Trace digunakan hanya sebagai pembuka bab atau penerangan visual dan dilabel jelas — bukan bukti atau foto kejadian.';
    container.appendChild(note);
  };

  const path = window.location.pathname;
  const isHome = path === '/raventrace-my/' || path.endsWith('/raventrace-my/index.html') || path === '/';
  const isNews = path.includes('/raventrace-my/news');
  const isCase = path.includes('/raventrace-my/investigations/rci-tabung-haji');

  if (isHome && !document.body.dataset.ravenVisualized) {
    const dek = document.querySelector('.front-lead .front-dek');
    injectArtAfter(dek, '/raventrace-my/assets/art/rci-tabung-haji-hero.webp', 'Ilustrasi editorial RAVEN-Trace bagi CASEFILE RCI Tabung Haji', 'Ilustrasi editorial RAVEN-Trace. Bukan dokumen, bukti atau foto kejadian. Fakta dan angka semasa datang daripada teks serta pautan sumber di halaman.', 'home-case-art');
    document.querySelectorAll('.update-card').forEach((card) => attachSourceFigure(card, externalUrlsIn(card), 'raven-card-visual'));
    addVisualPolicy(document.querySelector('#latest .section-head'));
    document.body.dataset.ravenVisualized = 'home';
  }

  if (isNews && !document.body.dataset.ravenVisualized) {
    document.querySelectorAll('.timeline-item').forEach((item) => {
      const content = item.children[1];
      if (!content) return;
      attachSourceFigure(content, externalUrlsIn(item), 'timeline-visual');
      item.classList.add('news-visual-ready');
    });
    addVisualPolicy(document.querySelector('.article-header .container'));
    document.body.dataset.ravenVisualized = 'news';
  }

  if (isCase && !document.body.dataset.ravenVisualized) {
    const heroDek = document.querySelector('.case-hero-grid .case-dek');
    injectArtAfter(heroDek, '/raventrace-my/assets/art/rci-tabung-haji-hero.webp', 'Ilustrasi editorial RAVEN-Trace bagi siasatan RCI Tabung Haji', 'Ilustrasi editorial RAVEN-Trace. Ia membantu orientasi pembaca dan bukan bukti. Rujuk Source Room untuk rekod yang menyokong setiap dakwaan.', 'case-hero-art');
    injectArtAfter(document.querySelector('#status > h2'), '/raventrace-my/assets/art/court-enforcement-watch.webp', 'Ilustrasi editorial bab mahkamah dan penguatkuasaan RCI Tabung Haji', 'Ilustrasi editorial RAVEN-Trace — bukan foto kejadian dan bukan gambaran individu tertentu. Status reman, pertuduhan dan prosiding dirujuk kepada rekod berita serta mahkamah di bawah.', 'enforcement-chapter-art');

    const institutionGrid = document.querySelector('.institution-grid');
    if (institutionGrid) {
      const marks = { 'RCI': 'RCI', 'SPRM': 'SPRM', 'PDRM / JSJK': 'PDRM', 'AGC': 'AGC', 'Mahkamah': 'COURT', 'PAC': 'PAC' };
      institutionGrid.querySelectorAll('article').forEach((article) => {
        const label = article.querySelector('b');
        if (!label || label.querySelector('.institution-mark')) return;
        const mark = document.createElement('span');
        mark.className = 'institution-mark';
        mark.textContent = marks[label.textContent.trim()] || label.textContent.trim().slice(0, 5);
        label.prepend(mark);
        article.classList.add('visualized');
      });
    }

    document.querySelectorAll('.trace-card').forEach((card) => attachSourceFigure(card, sourceUrlsFromCaseRefs(card), 'trace-visual'));

    document.querySelectorAll('.person-card').forEach((card) => {
      if (card.querySelector('.person-avatar')) return;
      const name = card.querySelector('h3')?.textContent.trim() || '';
      const initials = name.split(/\s+/).filter(Boolean).slice(0, 3).map((part) => part[0]).join('').toUpperCase();
      const avatar = document.createElement('div');
      avatar.className = 'person-avatar';
      avatar.setAttribute('aria-hidden', 'true');
      avatar.textContent = initials || '•';
      const meta = card.querySelector(':scope > div');
      if (meta) meta.insertAdjacentElement('afterend', avatar);
    });

    const sectorMap = [[/Perladangan|sawit|ladang/i,['🌿','Perladangan']],[/rel/i,['🚆','Rel']],[/hotel|hospitaliti/i,['🏨','Hospitaliti']],[/pembinaan|hartanah/i,['🏗','Pembinaan / hartanah']],[/marin|O&G|kapal/i,['⚓','Marin / O&G']],[/saham/i,['📈','Pasaran modal']],[/dana/i,['▦','Dana']],[/korporat/i,['▣','Korporat']]];
    document.querySelectorAll('.investment summary > div').forEach((block) => {
      if (block.querySelector('.investment-sector')) return;
      const hit = sectorMap.find(([pattern]) => pattern.test(block.textContent || ''));
      if (!hit) return;
      const sector = document.createElement('div');
      sector.className = 'investment-sector';
      const icon = document.createElement('span');
      icon.className = 'sector-icon';
      icon.setAttribute('aria-hidden', 'true');
      icon.textContent = hit[1][0];
      const label = document.createElement('span');
      label.textContent = hit[1][1];
      sector.append(icon, label);
      block.appendChild(sector);
    });

    const sources = document.querySelector('#sources');
    if (sources && !sources.querySelector('.visual-source-ledger')) {
      const ledger = document.createElement('aside');
      ledger.className = 'visual-source-ledger';
      ledger.innerHTML = '<h3>Polisi visual</h3><p><b>FOTO SUMBER</b> datang daripada metadata artikel yang dipautkan. <b>ILUSTRASI EDITORIAL</b> ialah artwork RAVEN-Trace untuk membantu pembaca memahami bab, bukan bukti dan bukan foto kejadian. Jika sumber berita tidak menyediakan imej yang boleh dimuatkan, kami tidak menggantikannya dengan gambar generik yang tidak berkaitan.</p>';
      const lead = sources.querySelector('.section-lead');
      if (lead) lead.insertAdjacentElement('afterend', ledger);
    }
    document.body.dataset.ravenVisualized = 'case';
  }
})();
