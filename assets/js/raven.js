(() => {
  const q = (s, r = document) => r.querySelector(s);
  const qa = (s, r = document) => [...r.querySelectorAll(s)];

  const navToggle = q('[data-nav-toggle]');
  const nav = q('[data-nav]');
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

  qa('[data-share]').forEach((button) => {
    button.addEventListener('click', async () => {
      const payload = {
        title: button.dataset.shareTitle || document.title,
        text: button.dataset.shareText || 'Semak laporan berasaskan bukti ini.',
        url: window.location.href
      };
      try {
        if (navigator.share) await navigator.share(payload);
        else {
          await navigator.clipboard.writeText(`${payload.text} ${payload.url}`);
          const original = button.textContent;
          button.textContent = 'Pautan disalin';
          setTimeout(() => { button.textContent = original; }, 1800);
        }
      } catch (error) {
        if (error.name !== 'AbortError') button.textContent = 'Salin gagal';
      }
    });
  });

  const filters = qa('[data-filter]');
  const topics = qa('[data-topic]');
  filters.forEach((button) => {
    button.setAttribute('aria-pressed', String(button.classList.contains('active')));
    button.addEventListener('click', () => {
      const selected = button.dataset.filter;
      filters.forEach((item) => {
        const active = item === button;
        item.classList.toggle('active', active);
        item.setAttribute('aria-pressed', String(active));
      });
      topics.forEach((item) => { item.hidden = selected !== 'all' && item.dataset.topic !== selected; });
    });
  });

  const expandButton = q('[data-expand-investments]');
  const investmentList = q('[data-investment-list]');
  if (expandButton && investmentList) {
    const records = qa('details', investmentList);
    expandButton.addEventListener('click', () => {
      const open = !records.every((record) => record.open);
      records.forEach((record) => { record.open = open; });
      expandButton.setAttribute('aria-expanded', String(open));
      expandButton.textContent = open ? 'Tutup semua rekod' : 'Buka semua rekod';
    });
  }

  const caseNav = q('[data-case-nav]');
  if (caseNav && 'IntersectionObserver' in window) {
    const links = qa('a[href^="#"]', caseNav);
    const sections = links.map((link) => q(link.getAttribute('href'))).filter(Boolean);
    const observer = new IntersectionObserver((entries) => {
      const visible = entries.filter((entry) => entry.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
      if (!visible) return;
      links.forEach((link) => link.classList.toggle('active', link.getAttribute('href') === `#${visible.target.id}`));
    }, { rootMargin: '-16% 0px -72% 0px', threshold: [0, .12, .3] });
    sections.forEach((section) => observer.observe(section));
  }

  if (!q('link[data-raven-visuals]')) {
    const sheet = document.createElement('link');
    sheet.rel = 'stylesheet';
    sheet.href = '/raventrace-my/assets/css/raven-visuals.css?v=1.3.0';
    sheet.dataset.ravenVisuals = 'true';
    document.head.appendChild(sheet);
  }

  qa('.brand').forEach((brand) => {
    if (q('.brand-seal', brand)) return;
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
  const preferredDomains = [
    'freemalaysiatoday.com','thestar.com.my','sinarharian.com.my','astroawani.com',
    'malaysiagazette.com','theedgemalaysia.com','malaymail.com','berita.rtm.gov.my',
    'bernama.com','web26.bernama.com','islam.gov.my','maccfm.my'
  ];
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
  const externalUrlsIn = (root) => qa('a[href]', root).map((link) => link.href).filter(isExternal).filter((url) => !url.includes('raven-trace.github.io'));
  const sourceUrlsFromCaseRefs = (root) => {
    const urls = [];
    qa('a[href^="#s"]', root).forEach((ref) => {
      const target = q(ref.getAttribute('href'));
      const source = target ? q('a[href^="http"]', target) : null;
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
    img.alt = storyTitle ? `Gambar berkaitan: ${storyTitle}` : 'Gambar daripada artikel sumber asal';
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
    source.textContent = `Sumber foto/berita: ${meta.publisher || hostname(sourceUrl)} →`;
    caption.appendChild(source);
    figure.append(frameLink, badge, caption);
    return figure;
  };

  const attachSourceFigure = async (container, sourceUrls, className) => {
    if (!container || q(':scope > .source-story-visual', container)) return true;
    const sourceUrl = chooseSource(sourceUrls);
    if (!sourceUrl) return false;
    const title = q('h1, h2, h3', container)?.textContent.trim() || '';
    const figure = await createSourceFigure(sourceUrl, className, title);
    if (!figure) return false;
    container.classList.add('has-source-visual');
    container.prepend(figure);
    return true;
  };

  const addAvatar = (card) => {
    if (q('.person-avatar', card)) return;
    const name = q('h3', card)?.textContent.trim() || '';
    const initials = name.split(/\s+/).filter(Boolean).slice(0, 3).map((part) => part[0]).join('').toUpperCase();
    const avatar = document.createElement('div');
    avatar.className = 'person-avatar';
    avatar.setAttribute('aria-hidden', 'true');
    avatar.textContent = initials || '•';
    const meta = q(':scope > div', card);
    if (meta) meta.insertAdjacentElement('afterend', avatar);
  };

  const addVisualPolicy = (container) => {
    if (!container || q('.source-image-policy', container)) return;
    const note = document.createElement('p');
    note.className = 'source-image-policy';
    note.textContent = 'Foto berita datang daripada sumber asal apabila tersedia. Ilustrasi RAVEN-Trace dilabel jelas dan tidak dianggap sebagai bukti atau foto kejadian.';
    container.appendChild(note);
  };

  const path = window.location.pathname;
  const isHome = path === '/raventrace-my/' || path.endsWith('/raventrace-my/index.html') || path === '/';
  const isNews = path.includes('/raventrace-my/news');
  const isCase = path.includes('/raventrace-my/investigations/rci-tabung-haji');

  if (isHome && !document.body.dataset.ravenVisualized) {
    injectArtAfter(
      q('.front-lead .front-dek'),
      '/raventrace-my/assets/art/rci-tabung-haji-hero.webp',
      'Ilustrasi editorial RAVEN-Trace bagi CASEFILE RCI Tabung Haji',
      'Ilustrasi editorial — bukan bukti atau foto kejadian.',
      'home-case-art'
    );
    qa('.update-card').forEach((card) => attachSourceFigure(card, externalUrlsIn(card), 'raven-card-visual'));
    addVisualPolicy(q('#latest .section-head'));
    document.body.dataset.ravenVisualized = 'home';
  }

  if (isNews && !document.body.dataset.ravenVisualized) {
    qa('.timeline-item').forEach((item) => {
      const content = item.children[1];
      if (!content) return;
      attachSourceFigure(content, externalUrlsIn(item), 'timeline-visual');
      item.classList.add('news-visual-ready');
    });
    addVisualPolicy(q('.article-header .container'));
    document.body.dataset.ravenVisualized = 'news';
  }

  if (isCase && !document.body.dataset.ravenVisualized) {
    injectArtAfter(
      q('.case-hero-grid .case-dek'),
      '/raventrace-my/assets/art/rci-tabung-haji-hero.webp',
      'Ilustrasi editorial RAVEN-Trace bagi siasatan RCI Tabung Haji',
      'Ilustrasi editorial — bukan bukti. Rujuk Source Room untuk rekod sokongan.',
      'case-hero-art'
    );
    injectArtAfter(
      q('#status > h2'),
      '/raventrace-my/assets/art/court-enforcement-watch.webp',
      'Ilustrasi editorial bab mahkamah dan penguatkuasaan RCI Tabung Haji',
      'Ilustrasi editorial — bukan foto kejadian atau gambaran individu tertentu.',
      'enforcement-chapter-art'
    );

    const institutionGrid = q('.institution-grid');
    if (institutionGrid) {
      const marks = { 'RCI':'RCI','SPRM':'SPRM','PDRM / JSJK':'PDRM','AGC':'AGC','Mahkamah':'COURT','PAC':'PAC' };
      qa('article', institutionGrid).forEach((article) => {
        const label = q('b', article);
        if (!label || q('.institution-mark', label)) return;
        const mark = document.createElement('span');
        mark.className = 'institution-mark';
        mark.textContent = marks[label.textContent.trim()] || label.textContent.trim().slice(0, 5);
        label.prepend(mark);
        article.classList.add('visualized');
      });
    }

    qa('.trace-card').forEach((card) => attachSourceFigure(card, sourceUrlsFromCaseRefs(card), 'trace-visual'));

    qa('.person-card').forEach(async (card) => {
      const ok = await attachSourceFigure(card, sourceUrlsFromCaseRefs(card), 'person-source-visual');
      if (!ok) addAvatar(card);
    });

    const sectorMap = [[/Perladangan|sawit|ladang/i,['🌿','Perladangan']],[/rel/i,['🚆','Rel']],[/hotel|hospitaliti/i,['🏨','Hospitaliti']],[/pembinaan|hartanah/i,['🏗','Pembinaan / hartanah']],[/marin|O&G|kapal/i,['⚓','Marin / O&G']],[/saham/i,['📈','Pasaran modal']],[/dana/i,['▦','Dana']],[/korporat/i,['▣','Korporat']]];
    qa('.investment summary > div').forEach((block) => {
      if (q('.investment-sector', block)) return;
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

    const sources = q('#sources');
    if (sources && !q('.visual-source-ledger', sources)) {
      const ledger = document.createElement('aside');
      ledger.className = 'visual-source-ledger';
      ledger.innerHTML = '<h3>Polisi visual</h3><p><b>FOTO SUMBER</b> datang daripada artikel yang dipautkan. <b>ILUSTRASI EDITORIAL</b> membantu menerangkan bab tetapi bukan bukti atau foto kejadian. Jika sumber tidak menyediakan imej, RAVEN-Trace tidak menggantikannya dengan gambar generik yang mengelirukan.</p>';
      q('.section-lead', sources)?.insertAdjacentElement('afterend', ledger);
    }
    document.body.dataset.ravenVisualized = 'case';
  }
})();
