(() => {
  if (window.__RAVEN_V5_PUBLIC_TRUTH__) return;
  window.__RAVEN_V5_PUBLIC_TRUTH__ = true;

  const q = (s, r = document) => r.querySelector(s);
  const qa = (s, r = document) => [...r.querySelectorAll(s)];
  const path = location.pathname;
  const isRoot = path === '/raventrace-my/' || path.endsWith('/raventrace-my/index.html');
  const isInvestigationsHub = path === '/raventrace-my/investigations/' || path.endsWith('/raventrace-my/investigations/index.html');
  const isRci = path.includes('/raventrace-my/investigations/rci-tabung-haji');
  const isNarrative = path.includes('/raventrace-my/investigations/rci-tabung-haji/narratives');
  const isNews = path === '/raventrace-my/news/' || path.endsWith('/raventrace-my/news/index.html');
  const isSupport = ['/raventrace-my/methodology/','/raventrace-my/about/','/raventrace-my/corrections/','/raventrace-my/tips/'].some((p) => path === p || path.endsWith(`${p}index.html`));

  document.body.classList.add('raven-v5');
  document.body.classList.add('raven-v7');

  // Every public page should include this stylesheet statically. Keep a
  // runtime fallback so future pages cannot silently miss the final layer.
  if (!q('link[data-raven-unified]')) {
    const unified = document.createElement('link');
    unified.rel = 'stylesheet';
    unified.href = '/raventrace-my/assets/css/raven-unified-v7.css?v=7.0.0';
    unified.dataset.ravenUnified = 'true';
    document.head.appendChild(unified);
  }
  if (isRoot) document.body.classList.add('raven-v5-home');
  if (isInvestigationsHub) document.body.classList.add('raven-v5-investigations');
  if (isNews) document.body.classList.add('raven-v5-news');
  if (isRci) document.body.classList.add('raven-v5-case');
  if (isNarrative) document.body.classList.add('raven-v5-narrative');
  if (isSupport) document.body.classList.add('raven-v5-support');
  if (path.startsWith('/raventrace-my/news/') && !isNews) document.body.classList.add('raven-v5-story');

  /* Public nav uses human language. URL architecture stays untouched. */
  const navNames = new Map([
    ['/raventrace-my/news/', 'Apa berubah?'],
    ['/raventrace-my/investigations/', 'Kes'],
    ['/raventrace-my/methodology/', 'Cara Raven check'],
    ['/raventrace-my/about/', 'Kenapa Raven']
  ]);
  qa('.site-nav a').forEach((a) => {
    const href = new URL(a.href, location.href).pathname;
    if (navNames.has(href)) a.textContent = navNames.get(href);
  });
  qa('.footer-nav a').forEach((a) => {
    const href = new URL(a.href, location.href).pathname;
    if (navNames.has(href)) a.textContent = navNames.get(href);
    if (href === '/raventrace-my/tips/') a.textContent = 'Bagi petunjuk';
    if (href === '/raventrace-my/corrections/') a.textContent = 'Apa kami betulkan';
  });

  const insertBefore = (target, node) => {
    if (target?.parentNode) target.parentNode.insertBefore(node, target);
  };

  const pathCard = (num, title, desc, href) => `
    <a class="v5-path" href="${href}">
      <span class="v5-path-icon">${num}</span>
      <span><strong>${title}</strong><small>${desc}</small></span>
    </a>`;

  if (isRoot && !q('.v5-truth-intro')) {
    const main = q('#main');
    const first = main?.firstElementChild;
    const intro = document.createElement('section');
    intro.className = 'v5-truth-intro';
    intro.innerHTML = `
      <div class="container">
        <p class="v5-kicker">RAVEN-Trace · bukti dulu, cerita kemudian</p>
        <h1>Benda complicated. Kita pecahkan.</h1>
        <p class="v5-dek">Ada orang kata macam-macam. Raven tak suruh kau percaya kami. Kita tengok apa yang betul, apa yang belum terbukti, dan apa yang cerita tu tak sebut.</p>
        <p class="v5-case-now">Sekarang Raven tengah bedah: <strong>RCI Tabung Haji</strong></p>
        <div class="v5-paths">
          ${pathCard('1','Aku nak faham dulu','Ringkasan paling cepat: apa berlaku dan kenapa orang kecoh.','/raventrace-my/investigations/rci-tabung-haji/#briefing')}
          ${pathCard('2','Apa cerita yang tengah dimainkan?','Tengok narrative politik, viral claim dan apa yang hilang dari cerita.','/raventrace-my/investigations/rci-tabung-haji/narratives/')}
          ${pathCard('3','Aku nak tengok bukti sendiri','Buka sumber, dokumen dan rekod yang Raven guna.','/raventrace-my/investigations/rci-tabung-haji/#sources')}
        </div>
      </div>`;
    insertBefore(first, intro);

    const primary = q('.front-lead .btn-primary');
    if (primary) primary.textContent = 'Faham kes ni';
    const latest = q('.front-lead .btn-row .btn:not(.btn-primary)');
    if (latest) latest.textContent = 'Apa berubah?';

    const docket = q('.front-docket');
    if (docket && !q('.v5-human-note', docket)) {
      const note = document.createElement('p');
      note.className = 'v5-human-note';
      note.innerHTML = '<strong>Senang cakap:</strong> ada banyak siasatan bergerak. Tapi siasatan, reman dan pertuduhan bukan bukti seseorang sudah bersalah.';
      docket.appendChild(note);
    }
  }

  const quickstart = (items, label = 'Nak mula kat mana?') => {
    if (q('.v5-quickstart')) return;
    const block = document.createElement('div');
    block.className = 'v5-quickstart';
    block.innerHTML = `<div class="v5-quickstart-inner"><strong>${label}</strong><div class="v5-quicklinks">${items.map(([t,h]) => `<a href="${h}">${t}</a>`).join('')}</div></div>`;
    return block;
  };

  if (isInvestigationsHub) {
    const hero = q('.investigation-desk-hero');
    const block = quickstart([
      ['Faham RCI dalam 60 saat','/raventrace-my/investigations/rci-tabung-haji/#briefing'],
      ['Apa latest?','/raventrace-my/investigations/rci-tabung-haji/#updates'],
      ['Check narrative','/raventrace-my/investigations/rci-tabung-haji/narratives/'],
      ['Tengok bukti','/raventrace-my/investigations/rci-tabung-haji/#sources']
    ], 'Ada satu kes aktif. Pilih cara nak masuk:');
    if (hero && block) hero.insertAdjacentElement('afterend', block);

    const title = q('.investigation-desk-hero h1');
    if (title) title.textContent = 'Pilih kes. Lepas tu kita pecahkan sama-sama.';
    const lede = q('.investigation-desk-hero .lede');
    if (lede) lede.textContent = 'Tak perlu jadi peguam atau auditor. Raven susun apa yang berlaku, apa yang orang kata, dan apa yang bukti betul-betul boleh tanggung.';
  }

  if (isRci && !isNarrative) {
    const hero = q('.case-hero') || q('.article-header') || q('main > section');
    const block = quickstart([
      ['Faham dulu','/raventrace-my/investigations/rci-tabung-haji/#briefing'],
      ['Apa berubah?','/raventrace-my/investigations/rci-tabung-haji/#updates'],
      ['Siapa & status','/raventrace-my/investigations/rci-tabung-haji/#people'],
      ['Check narrative','/raventrace-my/investigations/rci-tabung-haji/narratives/'],
      ['Bukti & sumber','/raventrace-my/investigations/rci-tabung-haji/#sources']
    ], 'Kes ni panjang. Kau nak mula kat mana?');
    if (hero && block) hero.insertAdjacentElement('afterend', block);
  }

  if (isNews) {
    const header = q('.article-header .container');
    if (header && !q('.v5-human-note', header)) {
      const note = document.createElement('p');
      note.className = 'v5-human-note';
      note.innerHTML = '<strong>Tak sempat follow semua?</strong> Tengok yang paling baru dulu. Kalau status tak berubah, Raven akan cakap terus: tak berubah.';
      const filters = q('.filters', header);
      if (filters) header.insertBefore(note, filters);
      else header.appendChild(note);
    }
  }

  if (isNarrative) {
    const intro = q('.section-intro');
    const block = quickstart([
      ['Cerita dia apa?','#top'],
      ['Apa yang betul?','#matrix'],
      ['Apa yang hilang?','#matrix'],
      ['Trick bahasa?','#language-forensics'],
      ['Tengok sumber','/raventrace-my/investigations/rci-tabung-haji/sources/']
    ], 'Cara Raven bedah narrative:');
    if (intro && block) intro.insertAdjacentElement('afterend', block);

    const translations = new Map([
      ['SELECTION EFFECT','Dia tunjuk yang ini je.'],
      ['CATEGORY COLLAPSE','Eh, benda ni tak sama.'],
      ['EMOTIONAL PRIMING','Dia bagi kita rasa dulu.'],
      ['MOTIVE INFLATION','Kita nampak tindakan. Niat? Belum tentu.'],
      ['REPETITION RISK','Ulang banyak kali tak jadikan benda tu betul.'],
      ['REPRESENTATIVENESS ERROR','Viral tak semestinya suara semua orang.']
    ]);
    qa('.status').forEach((status) => {
      const key = status.textContent.trim();
      if (!translations.has(key) || status.parentElement?.querySelector('.v5-mechanism-translation')) return;
      const friendly = document.createElement('span');
      friendly.className = 'v5-mechanism-translation';
      friendly.textContent = translations.get(key);
      status.insertAdjacentElement('afterend', friendly);
    });
  }

  if (isSupport) {
    if (path.includes('/methodology/')) {
      const head = q('.article-header .container');
      if (head && !q('.v5-human-note', head)) {
        const note = document.createElement('p');
        note.className = 'v5-human-note';
        note.innerHTML = '<strong>Versi pendek:</strong> cari claim asal → check sumber → cari benda yang tak disebut → cakap apa yang kita tahu → jangan reka benda yang kita tak tahu.';
        head.appendChild(note);
      }
    }
    if (path.includes('/about/')) {
      const head = q('.article-header .container');
      if (head) {
        const h1 = q('h1', head);
        if (h1) h1.innerHTML = 'Internet penuh cerita.<br>Raven check cerita tu.';
        const dek = q('.article-dek', head);
        if (dek) dek.textContent = 'Kadang-kadang benda yang menipu kita bukan fakta palsu. Fakta betul pun boleh disusun sampai cerita jadi lain. Raven wujud untuk check part tu.';
      }
    }
    if (path.includes('/tips/')) {
      const head = q('.article-header .container');
      if (head) {
        const h1 = q('h1', head);
        if (h1) h1.textContent = 'Ada benda pelik yang Raven patut tengok?';
        const dek = q('.article-dek', head);
        if (dek) dek.textContent = 'Claim viral, dokumen pelik, nombor yang tak masuk akal — bagi kami petunjuk. Tapi jangan bahayakan diri atau hantar benda sulit melalui saluran yang belum selamat.';
      }
    }
    if (path.includes('/corrections/')) {
      const head = q('.article-header .container');
      if (head) {
        const h1 = q('h1', head);
        if (h1) h1.innerHTML = 'Raven boleh silap.<br>Kat sini kami betulkan.';
        const dek = q('.article-dek', head);
        if (dek) dek.textContent = 'Kalau bukti berubah, Raven berubah. Kami tunjuk apa yang salah, apa yang bertukar, dan sama ada kesimpulan utama pun kena tukar.';
      }
    }
  }

  /* Explain common technical shorthand without touching the canonical source text. */
  const firstTextMatch = (root, pattern) => {
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    let n;
    while ((n = walker.nextNode())) {
      if (pattern.test(n.nodeValue || '')) return n.parentElement;
    }
    return null;
  };
  const glossary = [
    [/\bNFA\b/i, 'NFA = fail ditutup tanpa tindakan lanjut. Ia tak semestinya cerita tentang fail lain.'],
    [/\breman\b/i, 'Reman = tahan sementara untuk bantu siasatan. Bukan bukti bersalah.'],
    [/\bimpairment\b/i, 'Impairment = nilai aset diturunkan dalam akaun. Ia bukan automatik bermaksud duit dicuri.']
  ];
  const main = q('main');
  if (main) glossary.forEach(([pattern, text]) => {
    const target = firstTextMatch(main, pattern);
    if (!target || target.closest('.v5-human-note') || target.dataset.v5Explained) return;
    target.dataset.v5Explained = 'true';
    target.title = text;
  });

  /* Accessible titles for evidence labels — useful on hover and screen readers. */
  const statusHelp = {
    fact: 'Memang disahkan oleh rekod yang Raven semak.',
    claim: 'Ada pihak yang menyatakan perkara ini. Ia masih perlu dinilai terhadap bukti.',
    disputed: 'Sumber atau rekod penting belum sepadan.',
    unknown: 'Belum ada rekod yang cukup untuk buat keputusan.',
    context: 'Betul atau berguna, tapi perlukan konteks supaya tak tersalah faham.',
    process: 'Proses masih berjalan. Jangan lompat ke keputusan akhir.'
  };
  qa('.status').forEach((el) => {
    const key = Object.keys(statusHelp).find((k) => el.classList.contains(k));
    if (key && !el.title) el.title = statusHelp[key];
  });
})();
