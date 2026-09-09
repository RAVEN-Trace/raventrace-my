(() => {
  if (window.__RAVEN_PUBLICATION_LOADER_V21__) return;
  window.__RAVEN_PUBLICATION_LOADER_V21__ = true;
  const load = (src, key, done) => {
    if (document.querySelector(`script[data-${key}]`)) { if (done) done(); return; }
    const s=document.createElement('script'); s.src=src; s.defer=true; s.dataset[key]='true'; if(done)s.onload=done; document.head.appendChild(s);
  };
  load('/raventrace-my/assets/js/raven-publication-core.js?v=2.2.0','ravenPublicationCore',()=>{
    load('/raventrace-my/assets/js/raven-evidence-ux.js?v=2.1.0','ravenEvidenceUx');
  });
})();