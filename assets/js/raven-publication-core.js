(() => {
  if (window.__RAVEN_PUBLICATION_CORE_V30__) return;
  window.__RAVEN_PUBLICATION_CORE_V30__ = true;

  const q = (s, r = document) => r.querySelector(s);
  const qa = (s, r = document) => [...r.querySelectorAll(s)];
  const investigationIndex = '/raventrace-my/investigations/';
  document.documentElement.dataset.ravenRelease = 'publication-core-3.0';

  if (!q('link[data-raven-publication]')) {
    const css = document.createElement('link');
    css.rel = 'stylesheet';
    css.href = '/raventrace-my/assets/css/raven-publication.css?v=2.0.0';
    css.dataset.ravenPublication = 'true';
    document.head.appendChild(css);
  }

  qa('.site-nav a, .footer-nav a').forEach((link) => {
    if ((link.textContent || '').trim().toLowerCase() !== 'siasatan') return;
    link.href = investigationIndex;
    if (location.pathname.includes('/raventrace-my/investigations/')) link.setAttribute('aria-current', 'page');
    else if (link.getAttribute('aria-current') === 'page') link.removeAttribute('aria-current');
  });

  const path = location.pathname;
  const isHome = path === '/raventrace-my/' || path.endsWith('/raventrace-my/index.html') || path === '/';
  const isCase = path.includes('/raventrace-my/investigations/rci-tabung-haji');
  const make = (tag, className, text) => {
    const el = document.createElement(tag);
    if (className) el.className = className;
    if (text != null) el.textContent = text;
    return el;
  };
  const scrollToTarget = (selector) => {
    const target = q(selector);
    if (!target) return;
    target.scrollIntoView({ behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start' });
    try { history.replaceState(null, '', selector); } catch {}
  };

  if (isHome) document.body.classList.add('raven-editorial-home');

  const buildLens = () => {
    const readingNav = q('[data-case-nav]');
    if (!readingNav || q('.raven-lens-shell')) return;
    const lenses = [
      { key: 'story', label: 'Story', target: '#briefing', title: 'Cerita dahulu', text: 'Mulakan dengan ringkasan, konteks dan batas kesimpulan.' },
      { key: 'evidence', label: 'Evidence', target: '#sources', title: 'Jejak buktinya', text: 'Pergi terus ke Source Room dan gred bukti.' },
      { key: 'timeline', label: 'Timeline', target: '#timeline', title: 'Susun kronologi', text: 'Lihat keputusan, siasatan dan prosiding mengikut masa.' },
      { key: 'people', label: 'People', target: '#people', title: 'Siapa dan status apa', text: 'Semak individu, jawatan dan status proses tanpa menyamakan kaitan dengan kesalahan.' },
      { key: 'money', label: 'Money', target: '#money', title: 'Ikut angka', text: 'Pisahkan transaksi, impairment, pembiayaan semula dan metrik lain.' }
    ];
    const shell = make('section', 'raven-lens-shell');
    shell.setAttribute('aria-label', 'Raven Lens');
    const container = make('div', 'container');
    const intro = make('div', 'raven-lens-intro');
    intro.innerHTML = '<p class="eyebrow">Raven Lens</p><h2>Lihat kes melalui lima lensa.</h2><p>Lensa mengubah fokus navigasi sahaja. Tiada fakta atau status kes diubah oleh JavaScript.</p>';
    const panel = make('div', 'raven-lens-panel');
    const tabs = make('div', 'raven-lens-tabs');
    tabs.setAttribute('role', 'tablist');
    const readout = make('div', 'raven-lens-readout');
    const copy = make('div');
    const title = make('strong', '', lenses[0].title);
    const desc = make('p', '', lenses[0].text);
    copy.append(title, desc);
    const open = make('a', 'raven-lens-open', 'Buka bahagian →');
    open.href = lenses[0].target;
    open.addEventListener('click', (e) => { e.preventDefault(); scrollToTarget(open.getAttribute('href')); });
    readout.append(copy, open);
    lenses.forEach((lens, index) => {
      const button = make('button', 'raven-lens-tab', lens.label);
      button.type = 'button';
      button.setAttribute('role', 'tab');
      button.setAttribute('aria-selected', index === 0 ? 'true' : 'false');
      button.addEventListener('click', () => {
        qa('.raven-lens-tab', tabs).forEach((item) => item.setAttribute('aria-selected', String(item === button)));
        title.textContent = lens.title;
        desc.textContent = lens.text;
        open.href = lens.target;
        document.body.dataset.ravenLens = lens.key;
        scrollToTarget(lens.target);
      });
      tabs.appendChild(button);
    });
    panel.append(tabs, readout);
    container.append(intro, panel);
    shell.appendChild(container);
    readingNav.insertAdjacentElement('afterend', shell);
  };

  if (isCase) {
    document.body.classList.add('raven-editorial-case');
    if (!q('script[data-raven-source-room]')) {
      const sourceRoom = document.createElement('script');
      sourceRoom.src = '/raventrace-my/assets/js/raven-source-room.js?v=1.1.1';
      sourceRoom.defer = true;
      sourceRoom.dataset.ravenSourceRoom = 'true';
      document.head.appendChild(sourceRoom);
    }
    const row = q('.case-hero .btn-row');
    if (row && !q('.raven-quick-read', row)) {
      const quick = make('a', 'btn raven-quick-read', 'Baca ringkas · ±2 min');
      quick.href = '#briefing';
      row.insertBefore(quick, row.firstChild);
    }
    const navInner = q('[data-case-nav] .container');
    if (navInner && !navInner.dataset.ravenPublicationReady) {
      navInner.dataset.ravenPublicationReady = 'true';
      const primary = new Set(['#briefing','#updates','#status','#people','#money','#investments','#sources']);
      qa('a[href^="#"]', navInner).forEach((link) => {
        if (!primary.has(link.getAttribute('href'))) link.classList.add('raven-nav-secondary');
      });
      const toggle = make('button', 'raven-case-nav-toggle', 'Semua bahagian');
      toggle.type = 'button';
      toggle.setAttribute('aria-expanded', 'false');
      toggle.addEventListener('click', () => {
        const open = navInner.classList.toggle('raven-nav-show-all');
        toggle.setAttribute('aria-expanded', String(open));
        toggle.textContent = open ? 'Ringkaskan menu' : 'Semua bahagian';
      });
      navInner.appendChild(toggle);
    }
    buildLens();
  }

  const restorePersonFallback = (img) => {
    const figure = img.closest('.person-source-visual');
    const card = img.closest('.person-card');
    if (!figure || !card) return;
    figure.remove();
    card.classList.remove('has-source-visual');
    if (q('.person-avatar', card)) return;
    const name = (q('h3', card)?.textContent || '').trim();
    const initials = name.split(/\s+/).filter(Boolean).slice(0, 3).map((part) => part[0]).join('').toUpperCase() || '•';
    const avatar = make('div', 'person-avatar', initials);
    avatar.setAttribute('aria-hidden', 'true');
    const meta = q(':scope > div', card);
    if (meta) meta.insertAdjacentElement('afterend', avatar); else card.prepend(avatar);
  };
  document.addEventListener('error', (event) => {
    const target = event.target;
    if (target instanceof HTMLImageElement && target.closest('.person-source-visual')) restorePersonFallback(target);
  }, true);
})();
