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
      const payload = {
        title: button.dataset.shareTitle || document.title,
        text: button.dataset.shareText || 'Semak laporan berasaskan bukti ini.',
        url: window.location.href
      };

      try {
        if (navigator.share) {
          await navigator.share(payload);
        } else {
          await navigator.clipboard.writeText(`${payload.text} ${payload.url}`);
          const original = button.textContent;
          button.textContent = 'Pautan disalin';
          window.setTimeout(() => { button.textContent = original; }, 1800);
        }
      } catch (error) {
        if (error.name !== 'AbortError') button.textContent = 'Salin gagal';
      }
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
      items.forEach((item) => {
        item.hidden = selected !== 'all' && item.dataset.topic !== selected;
      });
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

    records.forEach((record) => {
      record.addEventListener('toggle', () => {
        const allOpen = records.every((item) => item.open);
        const allClosed = records.every((item) => !item.open);
        if (allOpen || allClosed) {
          expandButton.setAttribute('aria-expanded', String(allOpen));
          expandButton.textContent = allOpen ? 'Tutup semua rekod' : 'Buka semua rekod';
        }
      });
    });
  }

  const caseNav = document.querySelector('[data-case-nav]');
  if (caseNav && 'IntersectionObserver' in window) {
    const links = [...caseNav.querySelectorAll('a[href^="#"]')];
    const sections = links.map((link) => document.querySelector(link.getAttribute('href'))).filter(Boolean);
    const observer = new IntersectionObserver((entries) => {
      const visible = entries.filter((entry) => entry.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
      if (!visible) return;
      links.forEach((link) => {
        link.classList.toggle('active', link.getAttribute('href') === `#${visible.target.id}`);
      });
    }, { rootMargin: '-18% 0px -70% 0px', threshold: [0, 0.15, 0.35] });
    sections.forEach((section) => observer.observe(section));
  }

  // Visual layer: contextual photography with explicit attribution.
  if (!document.querySelector('link[data-raven-visuals]')) {
    const visualSheet = document.createElement('link');
    visualSheet.rel = 'stylesheet';
    visualSheet.href = '/raventrace-my/assets/css/raven-visuals.css?v=1.0.0';
    visualSheet.dataset.ravenVisuals = 'true';
    document.head.appendChild(visualSheet);
  }

  const commonsFile = (name, width = 1200) => `https://commons.wikimedia.org/wiki/Special:FilePath/${encodeURIComponent(name)}?width=${width}`;
  const visualAssets = {
    th: {
      file: 'KL- Lembaga Tabung Haji HQ.JPG',
      alt: 'Bangunan ibu pejabat Tabung Haji di Kuala Lumpur',
      source: 'https://commons.wikimedia.org/wiki/File:KL-_Lembaga_Tabung_Haji_HQ.JPG',
      credit: 'Foto: azreey · Wikimedia Commons · CC BY-SA 3.0',
      label: 'TABUNG HAJI',
      name: 'Ibu pejabat Tabung Haji'
    },
    macc: {
      file: 'Putrajaya Malaysia Anti-Corruption Commission-01.jpg',
      alt: 'Bangunan Suruhanjaya Pencegahan Rasuah Malaysia di Putrajaya',
      source: 'https://commons.wikimedia.org/wiki/File:Putrajaya_Malaysia_Anti-Corruption_Commission-01.jpg',
      credit: 'Foto: CEphoto, Uwe Aranas · Wikimedia Commons · CC BY-SA 3.0',
      label: 'SPRM',
      name: 'Suruhanjaya Pencegahan Rasuah Malaysia'
    },
    pdrm: {
      file: 'KL-Bukit Aman.JPG',
      alt: 'Ibu pejabat Polis Diraja Malaysia di Bukit Aman, Kuala Lumpur',
      source: 'https://commons.wikimedia.org/wiki/File:KL-Bukit_Aman.JPG',
      credit: 'Foto: Azreey · Wikimedia Commons · lesen terbuka',
      label: 'PDRM',
      name: 'Polis Diraja Malaysia'
    },
    parliament: {
      file: 'Malaysiaparliament.jpg',
      alt: 'Bangunan Parlimen Malaysia di Kuala Lumpur',
      source: 'https://commons.wikimedia.org/wiki/File:Malaysiaparliament.jpg',
      credit: 'Foto: Kelisi · Wikimedia Commons · domain awam',
      label: 'PARLIMEN',
      name: 'Parlimen Malaysia / PAC'
    },
    court: {
      file: 'KualaLumpurCourtsComplex-Malaysia-20080509-cropped.jpg',
      alt: 'Kompleks Mahkamah Kuala Lumpur',
      source: 'https://commons.wikimedia.org/wiki/File:KualaLumpurCourtsComplex-Malaysia-20080509-cropped.jpg',
      credit: 'Foto: Geoff / Jacklee · Wikimedia Commons · CC BY-SA 2.0',
      label: 'MAHKAMAH',
      name: 'Kompleks Mahkamah Kuala Lumpur'
    }
  };

  const createVisual = (key, className = '') => {
    const asset = visualAssets[key];
    if (!asset) return null;
    const figure = document.createElement('figure');
    figure.className = `raven-visual ${className}`.trim();
    const frame = document.createElement('div');
    frame.className = 'raven-visual-frame';
    const img = document.createElement('img');
    img.src = commonsFile(asset.file);
    img.alt = asset.alt;
    img.loading = 'lazy';
    img.decoding = 'async';
    frame.appendChild(img);
    const caption = document.createElement('figcaption');
    const link = document.createElement('a');
    link.href = asset.source;
    link.rel = 'noopener noreferrer';
    link.textContent = asset.credit;
    caption.appendChild(link);
    figure.append(frame, caption);
    return figure;
  };

  const createPhotoBand = (keys) => {
    const wrapper = document.createElement('section');
    wrapper.className = 'institution-visual-strip';
    const band = document.createElement('div');
    band.className = 'raven-photo-band';
    keys.forEach((key) => {
      const asset = visualAssets[key];
      const card = document.createElement('article');
      card.className = 'raven-photo-card';
      const img = document.createElement('img');
      img.src = commonsFile(asset.file, 800);
      img.alt = asset.alt;
      img.loading = 'lazy';
      const copy = document.createElement('div');
      copy.className = 'raven-photo-copy';
      const badge = document.createElement('b');
      badge.textContent = asset.label;
      const title = document.createElement('strong');
      title.textContent = asset.name;
      const small = document.createElement('small');
      const source = document.createElement('a');
      source.href = asset.source;
      source.rel = 'noopener noreferrer';
      source.textContent = 'Foto + lesen';
      small.appendChild(source);
      copy.append(badge, title, small);
      card.append(img, copy);
      band.appendChild(card);
    });
    const note = document.createElement('p');
    note.className = 'visual-note';
    note.textContent = 'Penanda institusi di laman ini ialah label editorial, bukan logo rasmi. Foto digunakan untuk konteks dan dipaut kepada sumber serta lesen.';
    wrapper.append(band, note);
    return wrapper;
  };

  const path = window.location.pathname;
  const isHome = path === '/raventrace-my/' || path.endsWith('/raventrace-my/index.html') || path === '/';
  const isNews = path.includes('/raventrace-my/news');
  const isCase = path.includes('/raventrace-my/investigations/rci-tabung-haji');

  if (isHome && !document.body.dataset.ravenVisualized) {
    const lead = document.querySelector('.front-lead');
    const dek = lead?.querySelector('.front-dek');
    if (lead && dek) dek.insertAdjacentElement('afterend', createVisual('th', 'raven-hero-media'));

    const cards = [...document.querySelectorAll('.update-card')];
    ['th', 'court', 'macc', 'court'].forEach((key, index) => {
      const card = cards[index];
      if (!card) return;
      card.classList.add('has-visual');
      card.prepend(createVisual(key, 'raven-card-visual'));
    });

    const signal = document.querySelector('.signal-strip');
    if (signal) {
      const section = document.createElement('section');
      section.className = 'section-sm dark';
      const container = document.createElement('div');
      container.className = 'container';
      const eyebrow = document.createElement('p');
      eyebrow.className = 'eyebrow';
      eyebrow.textContent = 'Institusi dalam jejak kes';
      const heading = document.createElement('h2');
      heading.textContent = 'Siapa menyiasat, menyemak dan mengadili?';
      container.append(eyebrow, heading, createPhotoBand(['th', 'macc', 'pdrm', 'parliament']));
      section.appendChild(container);
      signal.insertAdjacentElement('afterend', section);
    }
    document.body.dataset.ravenVisualized = 'home';
  }

  if (isNews && !document.body.dataset.ravenVisualized) {
    document.querySelectorAll('.timeline-item').forEach((item) => {
      const topic = item.dataset.topic;
      const text = item.textContent || '';
      let key = 'th';
      if (topic === 'court') key = 'court';
      else if (topic === 'enforcement') key = /PDRM|JSJK/i.test(text) ? 'pdrm' : 'macc';
      else if (topic === 'governance') key = 'parliament';
      else if (topic === 'report') key = 'th';
      const content = item.children[1];
      if (content) {
        item.classList.add('has-visual');
        content.prepend(createVisual(key, 'timeline-visual'));
      }
    });
    const header = document.querySelector('.article-header .container');
    if (header) header.appendChild(createPhotoBand(['th', 'macc', 'court', 'parliament']));
    document.body.dataset.ravenVisualized = 'news';
  }

  if (isCase && !document.body.dataset.ravenVisualized) {
    const heroLead = document.querySelector('.case-hero-grid > div');
    const heroDek = heroLead?.querySelector('.case-dek');
    if (heroLead && heroDek) heroDek.insertAdjacentElement('afterend', createVisual('th', 'case-hero-photo'));

    const institutionGrid = document.querySelector('.institution-grid');
    if (institutionGrid) {
      const marks = {
        'RCI': 'RCI', 'SPRM': 'SPRM', 'PDRM / JSJK': 'PDRM', 'AGC': 'AGC', 'Mahkamah': 'COURT', 'PAC': 'PAC'
      };
      institutionGrid.querySelectorAll('article').forEach((article) => {
        const label = article.querySelector('b');
        if (!label) return;
        const mark = document.createElement('span');
        mark.className = 'institution-mark';
        mark.textContent = marks[label.textContent.trim()] || label.textContent.trim().slice(0, 5);
        label.prepend(mark);
        article.classList.add('visualized');
      });
      institutionGrid.insertAdjacentElement('afterend', createPhotoBand(['th', 'macc', 'pdrm', 'parliament']));
    }

    const sectionVisuals = [
      ['#governance', 'parliament'],
      ['#tracks', 'macc'],
      ['#disputed-record', 'th']
    ];
    sectionVisuals.forEach(([selector, key]) => {
      const section = document.querySelector(selector);
      const heading = section?.querySelector(':scope > h2');
      if (section && heading) heading.insertAdjacentElement('afterend', createVisual(key, 'case-section-visual'));
    });

    document.querySelectorAll('.trace-card').forEach((card) => {
      const text = card.textContent || '';
      let key = 'th';
      if (/SPRM|kertas siasatan/i.test(text)) key = 'macc';
      if (/Mahkamah|didakwa|pertuduhan/i.test(text)) key = 'court';
      if (/Madinah|Rashid/i.test(text)) key = 'th';
      card.classList.add('has-visual');
      card.prepend(createVisual(key, 'trace-visual'));
    });

    document.querySelectorAll('.person-card').forEach((card) => {
      const name = card.querySelector('h3')?.textContent.trim() || '';
      const initials = name.split(/\s+/).filter(Boolean).slice(0, 3).map((part) => part[0]).join('').toUpperCase();
      const avatar = document.createElement('div');
      avatar.className = 'person-avatar';
      avatar.setAttribute('aria-hidden', 'true');
      avatar.textContent = initials || '•';
      const meta = card.querySelector(':scope > div');
      if (meta) meta.insertAdjacentElement('afterend', avatar);
    });

    const sectorMap = [
      [/Perladangan|sawit|ladang/i, ['🌿', 'Perladangan']],
      [/rel/i, ['🚆', 'Rel']],
      [/hotel|hospitaliti/i, ['🏨', 'Hospitaliti']],
      [/pembinaan|hartanah/i, ['🏗', 'Pembinaan / hartanah']],
      [/marin|O&G|kapal/i, ['⚓', 'Marin / O&G']],
      [/saham/i, ['📈', 'Pasaran modal']],
      [/dana/i, ['▦', 'Dana']],
      [/korporat/i, ['▣', 'Korporat']]
    ];
    document.querySelectorAll('.investment summary > div').forEach((block) => {
      const text = block.textContent || '';
      const hit = sectorMap.find(([pattern]) => pattern.test(text));
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
    if (sources) {
      const ledger = document.createElement('aside');
      ledger.className = 'visual-source-ledger';
      ledger.innerHTML = '<h3>Sumber visual</h3><p>Foto konteks di laman ini menggunakan bahan berlesen atau domain awam dari Wikimedia Commons. <a href="https://commons.wikimedia.org/wiki/File:KL-_Lembaga_Tabung_Haji_HQ.JPG" rel="noopener noreferrer">Tabung Haji</a> · <a href="https://commons.wikimedia.org/wiki/File:Putrajaya_Malaysia_Anti-Corruption_Commission-01.jpg" rel="noopener noreferrer">SPRM</a> · <a href="https://commons.wikimedia.org/wiki/File:KL-Bukit_Aman.JPG" rel="noopener noreferrer">PDRM</a> · <a href="https://commons.wikimedia.org/wiki/File:Malaysiaparliament.jpg" rel="noopener noreferrer">Parlimen</a> · <a href="https://commons.wikimedia.org/wiki/File:KualaLumpurCourtsComplex-Malaysia-20080509-cropped.jpg" rel="noopener noreferrer">Mahkamah</a>. Penanda institusi ialah label editorial, bukan logo rasmi dan bukan bukti kesalahan.</p>';
      const lead = sources.querySelector('.section-lead');
      if (lead) lead.insertAdjacentElement('afterend', ledger);
    }
    document.body.dataset.ravenVisualized = 'case';
  }
})();
