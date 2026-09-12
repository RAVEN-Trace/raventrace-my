(() => {
  if (window.__RAVEN_PUBLICATION_LOADER_V52__) return;
  window.__RAVEN_PUBLICATION_LOADER_V52__ = true;

  const loadScript = (src, key, done) => {
    const pathOnly = src.split('?')[0];
    const existing = [...document.scripts].find((node) => (node.getAttribute('src') || '').includes(pathOnly));
    if (existing) {
      if (done) {
        if (existing.dataset.loaded === 'true' || existing.readyState === 'complete') done();
        else existing.addEventListener('load', done, { once: true });
      }
      return;
    }
    const s = document.createElement('script');
    s.src = src;
    s.defer = true;
    s.dataset[key] = 'true';
    if (done) s.onload = () => { s.dataset.loaded = 'true'; done(); };
    document.head.appendChild(s);
  };

  const loadCss = (href, key) => {
    const pathOnly = href.split('?')[0];
    const existing = [...document.querySelectorAll('link[rel="stylesheet"]')].find((node) => (node.getAttribute('href') || '').includes(pathOnly));
    if (existing) return;
    const l = document.createElement('link');
    l.rel = 'stylesheet';
    l.href = href;
    l.dataset[key] = 'true';
    document.head.appendChild(l);
  };

  const existingPublicationCss = document.querySelector('link[href*="/assets/css/raven-publication.css"]');
  if (existingPublicationCss && !existingPublicationCss.dataset.ravenPublication) existingPublicationCss.dataset.ravenPublication = 'true';

  const path = location.pathname;
  const isHome = path === '/raventrace-my/' || path.endsWith('/raventrace-my/index.html');
  const isRciCase = path.includes('/raventrace-my/investigations/rci-tabung-haji');
  const isNarrative = path.includes('/raventrace-my/investigations/rci-tabung-haji/narratives');
  const isInvestigationsHub = path === '/raventrace-my/investigations/' || path.endsWith('/raventrace-my/investigations/index.html');
  const isNewsroom = path === '/raventrace-my/news/' || path.endsWith('/raventrace-my/news/index.html');
  const isStory = path.startsWith('/raventrace-my/news/') && !isNewsroom;
  const supportPaths = ['/raventrace-my/methodology/','/raventrace-my/about/','/raventrace-my/corrections/','/raventrace-my/tips/'];
  const isSupport = supportPaths.some((prefix) => path === prefix || path.endsWith(`${prefix}index.html`));

  if (isHome) document.body.classList.add('raven-v5-home');
  if (isInvestigationsHub) document.body.classList.add('raven-v4-investigations','raven-v5-investigations');
  if (isNewsroom) document.body.classList.add('raven-v4-news','raven-v5-news');
  if (isSupport) document.body.classList.add('raven-v4-support','raven-v5-support');
  if (isStory) document.body.classList.add('raven-v4-story','raven-v5-story');
  if (isRciCase) document.body.classList.add('raven-v5-case');
  if (isNarrative) document.body.classList.add('raven-v5-narrative');

  loadScript('/raventrace-my/assets/js/raven-publication-core.js?v=3.0.0','ravenPublicationCore',()=>{
    loadScript('/raventrace-my/assets/js/raven-evidence-ux.js?v=3.0.0','ravenEvidenceUx',()=>{
      if (isRciCase) loadCss('/raventrace-my/assets/css/raven-v4-case.css?v=4.0.0','ravenV4Case');
      if (isInvestigationsHub || isNewsroom) loadCss('/raventrace-my/assets/css/raven-v4-sections.css?v=4.0.0','ravenV4Sections');
      if (isSupport || isStory) loadCss('/raventrace-my/assets/css/raven-v4-support.css?v=4.0.0','ravenV4Support');

      /* V5 is intentionally last: it simplifies the established V4 publication
         system without replacing evidence semantics or factual HTML. */
      loadCss('/raventrace-my/assets/css/raven-v5.css?v=5.0.0','ravenV5');
      loadScript('/raventrace-my/assets/js/raven-v5.js?v=5.1.1','ravenV5Ux');
    });
  });
})();