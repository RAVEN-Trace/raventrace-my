(() => {
  if (window.__RAVEN_PUBLICATION_V2__) return;
  window.__RAVEN_PUBLICATION_V2__ = true;

  const q = (s, r = document) => r.querySelector(s);
  const qa = (s, r = document) => [...r.querySelectorAll(s)];
  const investigationIndex = '/raventrace-my/investigations/';
  document.documentElement.dataset.ravenRelease = 'publication-2.0';

  if (!q('link[data-raven-publication]')) {
    const css = document.createElement('link');
    css.rel = 'stylesheet';
    css.href = '/raventrace-my/assets/css/raven-publication.css?v=2.0.0';
    css.dataset.ravenPublication = 'true';
    document.head.appendChild(css);
  } else {
    const css = q('link[data-raven-publication]');
    if (css && !css.href.includes('v=2.0.0')) css.href = '/raventrace-my/assets/css/raven-publication.css?v=2.0.0';
  }

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
    try { history.replaceState(null, '', selector); } catch { /* optional */ }
  };

  if (isHome) {
    document.body.classList.add('raven-editorial-home');
    const lead = q('.front-lead');
    const caseId = lead ? q('.case-id', lead) : null;
    if (caseId && !q('.raven-lead-investigation', lead)) {
      const eyebrow = make('p', 'eyebrow raven-lead-investigation', 'Lead investigation');
      caseId.insertAdjacentElement('beforebegin', eyebrow);
    }

    const signal = q('.signal-strip');
    if (signal && !q('.raven-front-boundary')) {
      const section = make('section', 'raven-front-boundary');
      section.setAttribute('aria-label', 'Apa yang bukti boleh bawa setakat ini');
      section.innerHTML = `
        <div class="container">
          <div class="raven-boundary-grid">
            <article><b>KNOWN</b><p>RCI merekodkan kelemahan tadbir urus, pelaburan dan pelaporan; penguatkuasaan serta prosiding susulan masih berjalan.</p></article>
            <article><b>DISPUTED</b><p>Rekod Madinah Mohamad dan Rashid Hussain mengenai sebahagian prosiding RCI masih bercanggah pada rekod awam.</p></article>
            <article><b>UNKNOWN</b><p>Liabiliti akhir individu, keputusan semua kertas siasatan dan hasil selepas checkpoint reman semasa belum diketahui.</p></article>
          </div>
        </div>`;
      signal.insertAdjacentElement('afterend', section);
    }
  }

  const buildLens = () => {
    const readingNav = q('[data-case-nav]');
    if (!readingNav || q('.raven-lens-shell')) return;

    const lenses = [
      { key: 'story', label: 'Story', target: '#briefing', title: 'Cerita dahulu', text: 'Mulakan dengan ringkasan manusia: apa berlaku, kenapa penting dan batas kesimpulan.' },
      { key: 'evidence', label: 'Evidence', target: '#sources', title: 'Jejak buktinya', text: 'Pergi terus ke Source Room, gred bukti dan rekod yang menyokong claim utama.' },
      { key: 'timeline', label: 'Timeline', target: '#timeline', title: 'Susun kronologi', text: 'Lihat bila keputusan, siasatan dan prosiding berlaku tanpa mencampur fasa sejarah dengan penguatkuasaan semasa.' },
      { key: 'people', label: 'People', target: '#people', title: 'Siapa, bila, status apa', text: 'Semak individu, jawatan ketika tempoh berkaitan dan status undang-undang semasa tanpa menyamakan kaitan dengan kesalahan.' },
      { key: 'money', label: 'Money', target: '#money', title: 'Ikut angka', text: 'Pisahkan nilai transaksi, impairment, beban UJSB, refinancing dan metrik yang sering dicampur dalam naratif awam.' }
    ];

    const shell = make('section', 'raven-lens-shell');
    shell.setAttribute('aria-label', 'Raven Lens');
    const container = make('div', 'container');
    const intro = make('div', 'raven-lens-intro');
    intro.innerHTML = '<p class="eyebrow">Raven Lens</p><h2>Lihat kes melalui lima lensa.</h2><p>Lensa mengubah fokus navigasi sahaja. Tiada bukti disembunyikan atau dibuang.</p>';

    const panel = make('div', 'raven-lens-panel');
    const tabs = make('div', 'raven-lens-tabs');
    tabs.setAttribute('role', 'tablist');
    tabs.setAttribute('aria-label', 'Pilih lensa CASEFILE');
    const readout = make('div', 'raven-lens-readout');
    const copy = make('div');
    const title = make('strong', '', lenses[0].title);
    const desc = make('p', '', lenses[0].text);
    copy.append(title, desc);
    const open = make('a', 'raven-lens-open', 'Buka bahagian →');
    open.href = lenses[0].target;
    open.addEventListener('click', (event) => {
      event.preventDefault();
      scrollToTarget(open.getAttribute('href'));
    });
    readout.append(copy, open);

    lenses.forEach((lens, index) => {
      const button = make('button', 'raven-lens-tab', lens.label);
      button.type = 'button';
      button.setAttribute('role', 'tab');
      button.setAttribute('aria-selected', index === 0 ? 'true' : 'false');
      button.dataset.lens = lens.key;
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

  const buildEvidenceBoundary = () => {
    const briefing = q('#briefing');
    if (!briefing || q('.raven-evidence-boundary', briefing)) return;
    const lead = q('.section-lead', briefing) || q('h2', briefing);
    if (!lead) return;

    const box = make('aside', 'raven-evidence-boundary');
    box.setAttribute('aria-label', 'What the evidence can carry');
    box.innerHTML = `
      <div class="raven-evidence-boundary-head">
        <h3>What the evidence can carry</h3>
        <p>Had kesimpulan setakat cut-off CASEFILE. Bila bukti berubah, panel ini juga mesti berubah.</p>
      </div>
      <div class="raven-evidence-boundary-grid">
        <article><b>FACT</b><p>RCI merekodkan kelemahan serius; SPRM menyatakan 14 kertas siasatan dan empat NFA setakat 2 Sep; dua bekas pengurus THP Bina telah didakwa dan mengaku tidak bersalah.</p></article>
        <article><b>DISPUTED</b><p>Versi Madinah Mohamad dan Rashid Hussain mengenai sebahagian proses RCI tidak selari pada rekod awam yang tersedia.</p></article>
        <article><b>UNKNOWN</b><p>Butiran empat NFA, keputusan fail lain, liabiliti akhir individu dan hasil selepas sambungan reman hingga 8 Sep masih belum diketahui.</p></article>
        <article><b>DO NOT CONCLUDE</b><p>Reman atau pertuduhan bukan bukti bersalah. RM13 bilion juga bukan label automatik untuk “wang dicuri”.</p></article>
      </div>`;
    lead.insertAdjacentElement('afterend', box);
  };

  const buildClaimRecord = () => {
    const briefing = q('#briefing');
    if (!briefing || q('.raven-claim-record', briefing)) return;
    const anchor = q('.brief-grid', briefing) || q('.bottom-line', briefing);
    if (!anchor) return;

    const section = make('section', 'raven-claim-record');
    section.setAttribute('aria-label', 'Claim versus record');
    section.innerHTML = `
      <div class="raven-claim-record-head">
        <h3>Claim vs Record</h3>
        <p>Bahasa awam sering memendekkan cerita. Raven pisahkan slogan daripada apa yang rekod benar-benar menyokong.</p>
      </div>
      <div class="raven-claim-record-row">
        <div><b class="claim-label">CLAIM</b><p>“RM13 bilion duit Tabung Haji hilang atau dicuri.”</p></div>
        <div><b class="record-label">RECORD</b><p>Angka hampir RM13b diterangkan sebagai gabungan kira-kira RM10.2b beban pemulihan/UJSB dan RM2.6b impairment TH. Ia tidak membuktikan RM13b wang dicuri.</p><a href="#money">Trace angka →</a></div>
      </div>
      <div class="raven-claim-record-row">
        <div><b class="claim-label">CLAIM</b><p>“14 kertas siasatan bermaksud 14 kes jenayah telah terbukti.”</p></div>
        <div><b class="record-label">RECORD</b><p>Kertas siasatan ialah proses penguatkuasaan. Empat telah diklasifikasikan NFA setakat 2 Sep, dan bilangan kertas tidak sama dengan bilangan sabitan atau pelaburan yang terbukti jenayah.</p><a href="#tracks">Trace siasatan →</a></div>
      </div>`;
    anchor.insertAdjacentElement('afterend', section);
  };

  const buildChangeLog = () => {
    const updates = q('#updates');
    if (!updates || q('.raven-change-log', updates)) return;
    const anchor = q('h2', updates);
    if (!anchor) return;
    const box = make('aside', 'raven-change-log');
    box.setAttribute('aria-label', 'Apa yang berubah dalam CASEFILE v17');
    box.innerHTML = `
      <h3>What changed · v17</h3>
      <div class="raven-change-grid">
        <div><b>NEW</b><p>Mahkamah membenarkan sambungan reman dua hari hingga 8 September.</p></div>
        <div><b>UPDATED</b><p>Konteks RM11.5b sukuk UJSB dikunci sebagai refinancing, bukan kerugian baharu.</p></div>
        <div><b>UNCHANGED</b><p>Tiada asas untuk menyimpulkan guilt daripada reman, siasatan atau pertuduhan.</p></div>
        <div><b>NEXT</b><p>Semak apa berlaku selepas checkpoint 8 September dan sebarang tindakan AGC/mahkamah baharu.</p></div>
      </div>`;
    anchor.insertAdjacentElement('afterend', box);
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
    buildEvidenceBoundary();
    buildClaimRecord();
    buildChangeLog();
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
    if (meta) meta.insertAdjacentElement('afterend', avatar);
    else card.prepend(avatar);
  };

  document.addEventListener('error', (event) => {
    const target = event.target;
    if (target instanceof HTMLImageElement && target.closest('.person-source-visual')) restorePersonFallback(target);
  }, true);
})();