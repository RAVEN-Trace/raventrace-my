(() => {
  const q = (s, r = document) => r.querySelector(s);
  const qa = (s, r = document) => [...r.querySelectorAll(s)];

  /*
   * RAVEN-Trace section controller — interaction only.
   * IMPORTANT: factual state, dates, names, legal status and evidence content
   * must be rendered by canonical HTML/build data. This file must never mutate
   * CASEFILE facts after load.
   */

  if (!q('link[data-raven-site-integrity]')) {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = '/raventrace-my/assets/css/raven-site-integrity.css?v=1.0.0';
    link.dataset.ravenSiteIntegrity = 'true';
    document.head.appendChild(link);
  }

  if (!q('script[data-raven-reader-v13]')) {
    const reader = document.createElement('script');
    reader.src = '/raventrace-my/assets/js/raven-reader-v13.js?v=1.3.0';
    reader.defer = true;
    reader.dataset.ravenReaderV13 = 'true';
    document.head.appendChild(reader);
  }

  if (!q('script[src*="lytcdn.com/lyt.js"]')) {
    const analytics = document.createElement('script');
    analytics.async = true;
    analytics.src = 'https://lytcdn.com/lyt.js?site=7d23381ee4e5';
    analytics.dataset.ravenAnalyticsFallback = 'true';
    document.head.appendChild(analytics);
  }

  q('[data-section-share]')?.addEventListener('click', async (event) => {
    const button = event.currentTarget;
    const payload = {
      title: document.title,
      text: q('meta[name="description"]')?.content || '',
      url: q('link[rel="canonical"]')?.href || location.href
    };
    try {
      if (navigator.share) {
        await navigator.share(payload);
      } else if (navigator.clipboard) {
        await navigator.clipboard.writeText(`${payload.text}\n\n${payload.url}`);
        button.textContent = 'Pautan disalin';
      }
    } catch (error) {
      if (error?.name !== 'AbortError') button.textContent = 'Salin gagal';
    }
  });

  q('[data-expand-investments]')?.addEventListener('click', (event) => {
    const items = qa('details.investment');
    const open = !items.every((item) => item.open);
    items.forEach((item) => { item.open = open; });
    event.currentTarget.setAttribute('aria-expanded', String(open));
    event.currentTarget.textContent = open ? 'Tutup semua rekod' : 'Buka semua rekod';
  });

  const activeSection = q('.section-links a[aria-current]');
  if (activeSection && matchMedia('(max-width: 760px)').matches) {
    requestAnimationFrame(() => {
      const rail = activeSection.closest('.section-links');
      if (!rail) return;
      const left = activeSection.offsetLeft - 16;
      rail.scrollTo({ left: Math.max(0, left), behavior: 'auto' });
    });
  }
})();
