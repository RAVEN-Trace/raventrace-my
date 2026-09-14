(() => {
  'use strict';
  if (window.__RAVEN_ROUTE_FIXES_V1__) return;
  window.__RAVEN_ROUTE_FIXES_V1__ = true;

  const BASE = '/raventrace-my/investigations/rci-tabung-haji/';
  const routes = new Map([
    ['updates', `${BASE}updates/`],
    ['people', `${BASE}people/`],
    ['investments', `${BASE}investments/`],
    ['governance', `${BASE}governance/`],
    ['sources', `${BASE}sources/`],
    ['money', `${BASE}money/`]
  ]);

  const repair = () => {
    /* Repair legacy cross-page links that still point to sections moved into subpages. */
    document.querySelectorAll('a[href]').forEach((a) => {
      const raw = a.getAttribute('href') || '';
      if (!raw || raw.startsWith('#')) return;
      try {
        const u = new URL(raw, location.origin);
        if (u.pathname !== BASE || !u.hash) return;
        const key = decodeURIComponent(u.hash.slice(1));
        if (routes.has(key)) a.setAttribute('href', routes.get(key));
      } catch (_) {}
    });

    /* Truth Map and lens links on the CASEFILE root are runtime-generated local anchors. */
    const onCaseRoot = location.pathname === BASE || location.pathname === `${BASE}index.html`;
    if (!onCaseRoot) return;
    document.querySelectorAll('.signal-case-lenses a[href^="#"], .signal-truth-map a[href^="#"]').forEach((a) => {
      const key = decodeURIComponent((a.getAttribute('href') || '').slice(1));
      if (routes.has(key)) a.setAttribute('href', routes.get(key));
    });
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => setTimeout(repair, 0), { once: true });
  } else {
    setTimeout(repair, 0);
  }
})();
