(() => {
  if (window.__RAVEN_EVIDENCE_UX_V30__) return;
  window.__RAVEN_EVIDENCE_UX_V30__ = true;

  const q = (s, r = document) => r.querySelector(s);
  const qa = (s, r = document) => [...r.querySelectorAll(s)];

  // Presentation-only: factual case state must remain in static HTML / canonical build output.
  if (!q('link[data-raven-evidence-ux]')) {
    const l = document.createElement('link');
    l.rel = 'stylesheet';
    l.href = '/raventrace-my/assets/css/raven-evidence-ux.css?v=2.1.0';
    l.dataset.ravenEvidenceUx = 'true';
    document.head.appendChild(l);
  }

  const gradeTitle = {
    A: 'Bukti primer / rekod rasmi asal',
    B: 'Laporan disahkan / boleh dijejak',
    C: 'Sokongan separa / belum lengkap',
    D: 'Lemah / konteks tidak mencukupi',
    E: 'Tafsiran pakar yang memerlukan semakan konteks',
    X: 'Tidak boleh digunakan sebagai bukti'
  };

  qa('#sources .sources-grid li').forEach((li) => {
    if (li.dataset.rvEnhanced === 'true') return;
    li.dataset.rvEnhanced = 'true';
    const grade = q(':scope > span', li);
    if (!grade) return;
    const key = grade.textContent.trim().toUpperCase();
    grade.title = gradeTitle[key] || 'Gred bukti';
  });
})();
