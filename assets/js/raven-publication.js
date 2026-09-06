(() => {
  if (window.__RAVEN_PUBLICATION_V1_1__) return;
  window.__RAVEN_PUBLICATION_V1_1__ = true;

  const q = (s, r = document) => r.querySelector(s);
  const qa = (s, r = document) => [...r.querySelectorAll(s)];
  const investigationIndex = '/raventrace-my/investigations/';
  document.documentElement.dataset.ravenRelease = 'publication-1.1';

  if (!q('link[data-raven-publication]')) {
    const css = document.createElement('link');
    css.rel = 'stylesheet';
    css.href = '/raventrace-my/assets/css/raven-publication.css?v=1.1.0';
    css.dataset.ravenPublication = 'true';
    document.head.appendChild(css);
  }

  /* Siasatan is a desk, not a synonym for one case. */
  qa('.site-nav a, .footer-nav a').forEach((link) => {
    const label = (link.textContent || '').trim().toLowerCase();
    if (label !== 'siasatan') return;
    link.href = investigationIndex;
    if (location.pathname.includes('/raventrace-my/investigations/')) link.setAttribute('aria-current', 'page');
    else if (link.getAttribute('aria-current') === 'page') link.removeAttribute('aria-current');
  });

  const path = location.pathname;
  const isHome = path === '/raventrace-my/' || path.endsWith('/raventrace-my/index.html') || path === '/';
  const isCase = path.includes('/raventrace-my/investigations/rci-tabung-haji');

  if (isHome) {
    const lead = q('.front-lead');
    const caseId = lead ? q('.case-id', lead) : null;
    if (caseId && !q('.raven-lead-investigation', lead)) {
      const eyebrow = document.createElement('p');
      eyebrow.className = 'eyebrow raven-lead-investigation';
      eyebrow.textContent = 'Lead investigation';
      caseId.insertAdjacentElement('beforebegin', eyebrow);
    }
  }

  if (isCase) {
    if (!q('script[data-raven-source-room]')) {
      const sourceRoom = document.createElement('script');
      sourceRoom.src = '/raventrace-my/assets/js/raven-source-room.js?v=1.0.0';
      sourceRoom.defer = true;
      sourceRoom.dataset.ravenSourceRoom = 'true';
      document.head.appendChild(sourceRoom);
    }

    const row = q('.case-hero .btn-row');
    if (row && !q('.raven-quick-read', row)) {
      const quick = document.createElement('a');
      quick.className = 'btn raven-quick-read';
      quick.href = '#briefing';
      quick.textContent = 'Baca ringkas · ±2 min';
      row.insertBefore(quick, row.firstChild);
    }

    const navInner = q('[data-case-nav] .container');
    if (navInner && !navInner.dataset.ravenPublicationReady) {
      navInner.dataset.ravenPublicationReady = 'true';
      const primary = new Set(['#briefing','#updates','#status','#people','#money','#investments','#sources']);
      qa('a[href^="#"]', navInner).forEach((link) => {
        if (!primary.has(link.getAttribute('href'))) link.classList.add('raven-nav-secondary');
      });
      const toggle = document.createElement('button');
      toggle.type = 'button';
      toggle.className = 'raven-case-nav-toggle';
      toggle.setAttribute('aria-expanded', 'false');
      toggle.textContent = 'Semua bahagian';
      toggle.addEventListener('click', () => {
        const open = navInner.classList.toggle('raven-nav-show-all');
        toggle.setAttribute('aria-expanded', String(open));
        toggle.textContent = open ? 'Ringkaskan menu' : 'Semua bahagian';
      });
      navInner.appendChild(toggle);
    }
  }

  /* Late source-image failures should restore the person fallback instead of leaving a blank card. */
  const restorePersonFallback = (img) => {
    const figure = img.closest('.person-source-visual');
    const card = img.closest('.person-card');
    if (!figure || !card) return;
    figure.remove();
    card.classList.remove('has-source-visual');
    if (q('.person-avatar', card)) return;
    const name = (q('h3', card)?.textContent || '').trim();
    const initials = name.split(/\s+/).filter(Boolean).slice(0, 3).map((part) => part[0]).join('').toUpperCase() || '•';
    const avatar = document.createElement('div');
    avatar.className = 'person-avatar';
    avatar.setAttribute('aria-hidden', 'true');
    avatar.textContent = initials;
    const meta = q(':scope > div', card);
    if (meta) meta.insertAdjacentElement('afterend', avatar);
    else card.prepend(avatar);
  };

  document.addEventListener('error', (event) => {
    const target = event.target;
    if (target instanceof HTMLImageElement && target.closest('.person-source-visual')) restorePersonFallback(target);
  }, true);
})();