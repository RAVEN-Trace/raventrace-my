(() => {
  if (window.__RAVEN_PUBLICATION_LOADER_V42__) return;
  window.__RAVEN_PUBLICATION_LOADER_V42__ = true;

  const loadScript = (src, key, done) => {
    const existing = document.querySelector(`script[data-${key}]`);
    if (existing) { if (done) done(); return; }
    const s = document.createElement('script');
    s.src = src;
    s.defer = true;
    s.dataset[key] = 'true';
    if (done) s.onload = done;
    document.head.appendChild(s);
  };

  const loadCss = (href, key) => {
    if (document.querySelector(`link[data-${key}]`)) return;
    const l = document.createElement('link');
    l.rel = 'stylesheet';
    l.href = href;
    l.dataset[key] = 'true';
    document.head.appendChild(l);
  };

  const existingPublicationCss = document.querySelector('link[href*="/assets/css/raven-publication.css"]');
  if (existingPublicationCss && !existingPublicationCss.dataset.ravenPublication) {
    existingPublicationCss.dataset.ravenPublication = 'true';
  }

  const path = location.pathname;
  const isRciCase = path.includes('/raventrace-my/investigations/rci-tabung-haji');
  const isInvestigationsHub = path === '/raventrace-my/investigations/' || path.endsWith('/raventrace-my/investigations/index.html');
  const isNewsroom = path === '/raventrace-my/news/' || path.endsWith('/raventrace-my/news/index.html');

  if (isInvestigationsHub) document.body.classList.add('raven-v4-investigations');
  if (isNewsroom) document.body.classList.add('raven-v4-news');

  loadScript('/raventrace-my/assets/js/raven-publication-core.js?v=2.2.0','ravenPublicationCore',()=>{
    loadScript('/raventrace-my/assets/js/raven-evidence-ux.js?v=2.1.0','ravenEvidenceUx',()=>{
      if (isRciCase) {
        loadCss('/raventrace-my/assets/css/raven-v4-case.css?v=4.0.0','ravenV4Case');
      }
      if (isInvestigationsHub || isNewsroom) {
        loadCss('/raventrace-my/assets/css/raven-v4-sections.css?v=4.0.0','ravenV4Sections');
      }
    });
  });
})();