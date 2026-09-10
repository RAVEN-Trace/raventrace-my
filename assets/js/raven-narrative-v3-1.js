(() => {
  'use strict';
  const path = location.pathname;
  if (!path.endsWith('/investigations/rci-tabung-haji/narratives/') && !path.endsWith('/investigations/rci-tabung-haji/narratives/index.html')) return;

  document.body.classList.add('narrative-v31');
  const sections = [...document.querySelectorAll('.case-section')];
  const narrativeSection = sections.find(s => /naratif utama/i.test(s.querySelector('h2')?.textContent || ''));
  if (!narrativeSection) return;
  const grid = narrativeSection.querySelector('.control-grid');
  if (!grid) return;
  const cards = [...grid.children].filter(el => el.tagName === 'ARTICLE');

  const textAfterLabel = (p, label) => {
    if (!p) return '';
    const txt = p.textContent.trim();
    return txt.replace(new RegExp('^' + label.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '\\s*:?\\s*', 'i'), '').trim();
  };
  const findP = (card, starts) => [...card.querySelectorAll(':scope > p')].find(p => {
    const b = p.querySelector('b');
    const t = (b?.textContent || p.textContent).trim().toLowerCase();
    return starts.some(s => t.startsWith(s));
  });
  const classify = status => {
    const t = status.toLowerCase();
    if (/inference|analisis/.test(t)) return 'inference';
    if (/posisi|dasar|hujah/.test(t)) return 'policy';
    if (/tidak disokong|dipertikai|terlalu mudah|bercanggah/.test(t)) return 'disputed';
    if (/dakwaan|slogan/.test(t)) return 'claim';
    if (/fakta/.test(t)) return 'fact';
    return 'claim';
  };

  cards.forEach((card, i) => {
    card.classList.add('narrative-card');
    card.id = card.id || `naratif-${String(i+1).padStart(2,'0')}`;

    const statusP = card.querySelector(':scope > p:has(.status)');
    const statusText = statusP?.textContent.trim() || 'Status belum diklasifikasi';
    const category = classify(statusText);
    card.dataset.narrativeCategory = category;
    if (statusP) statusP.classList.add('narrative-status-row');

    const verdictP = findP(card, ['verdict raven']);
    const recordP = findP(card, ['apa rekod tunjuk']);
    const confidenceP = findP(card, ['confidence']);
    const whoP = findP(card, ['siapa menggunakan naratif ini', 'siapa menggunakan / membawa frame']);
    const omittedP = findP(card, ['konteks yang sering tertinggal']);
    const changeP = findP(card, ['apa yang boleh mengubah verdict']);

    if (verdictP) {
      const verdictText = textAfterLabel(verdictP, 'Verdict Raven');
      const box = document.createElement('div');
      box.className = 'narrative-verdict';
      box.innerHTML = `<span class="label">RAVEN VERDICT</span><strong></strong>`;
      box.querySelector('strong').textContent = verdictText;
      verdictP.replaceWith(box);
    }

    if (recordP) {
      const why = document.createElement('p');
      why.className = 'narrative-why';
      const t = textAfterLabel(recordP, 'Apa rekod tunjuk');
      why.innerHTML = '<b>Kenapa?</b> ';
      why.append(document.createTextNode(t));
      recordP.replaceWith(why);
    }

    let confidenceText = '', lastVerified = '';
    if (confidenceP) {
      const raw = textAfterLabel(confidenceP, 'Confidence');
      const parts = raw.split(/·\s*Last verified:\s*/i);
      confidenceText = (parts[0] || '').replace(/\s*·\s*$/, '').trim();
      lastVerified = (parts[1] || '').trim();
      confidenceP.remove();
    }
    const meta = document.createElement('div');
    meta.className = 'narrative-meta';
    if (confidenceText) {
      const c = document.createElement('span'); c.textContent = `Confidence · ${confidenceText}`; meta.append(c);
    }
    if (lastVerified) {
      const d = document.createElement('span'); d.textContent = `Last verified · ${lastVerified}`; meta.append(d);
    }

    const details = document.createElement('details');
    const summary = document.createElement('summary');
    summary.textContent = 'Buka bukti & konteks';
    const detail = document.createElement('div'); detail.className = 'narrative-detail';
    [whoP, omittedP, changeP].filter(Boolean).forEach(p => detail.append(p));
    details.append(summary, detail);
    card.append(meta, details);
  });

  const counts = cards.reduce((a,c) => (a[c.dataset.narrativeCategory]=(a[c.dataset.narrativeCategory]||0)+1,a),{});
  const strip = document.createElement('div');
  strip.className = 'narrative-status-strip';
  const entries = [
    [cards.length, 'Naratif aktif'],
    [counts.disputed || 0, 'Disputed / unsupported'],
    [counts.inference || 0, 'Inference / analisis'],
    [(counts.policy || 0) + (counts.fact || 0), 'Dasar / posisi fakta']
  ];
  entries.forEach(([n,label]) => {
    const d = document.createElement('div');
    d.innerHTML = `<strong>${String(n).padStart(2,'0')}</strong><span>${label}</span>`;
    strip.append(d);
  });

  const filterbar = document.createElement('div');
  filterbar.className = 'narrative-filterbar';
  filterbar.setAttribute('aria-label','Tapis audit naratif');
  filterbar.innerHTML = '<strong>Tapis naratif</strong>';
  const filters = [
    ['all','Semua'],['claim','Dakwaan'],['disputed','Disputed'],['inference','Inference'],['policy','Dasar']
  ];
  filters.forEach(([key,label], i) => {
    const b = document.createElement('button');
    b.type='button'; b.dataset.narrativeFilter=key; b.textContent=label; b.setAttribute('aria-pressed', i===0 ? 'true':'false');
    b.addEventListener('click', () => {
      filterbar.querySelectorAll('button').forEach(x => x.setAttribute('aria-pressed','false'));
      b.setAttribute('aria-pressed','true');
      cards.forEach(card => {
        const cat = card.dataset.narrativeCategory;
        const match = key === 'all' || cat === key || (key === 'policy' && cat === 'fact');
        card.hidden = !match;
      });
    });
    filterbar.append(b);
  });
  grid.before(strip, filterbar);

  const board = document.createElement('div');
  board.className = 'narrative-board';
  board.setAttribute('aria-label','Kelompok naratif');
  const groups = [
    ['01','Wang & angka','RM12b, sakau, kerugian dan tafsiran angka'],
    ['02','UJSB & pemulihan','Pemindahan aset, bailout dan tempoh selepas 2018'],
    ['03','Politik & motif','RCI kedua, alih fokus dan posisi parti'],
    ['04','Proses & bukti','Audit, siasatan, pertuduhan dan batas kesimpulan']
  ];
  groups.forEach(([idx,title,desc], i) => {
    const a = document.createElement('a');
    a.href = cards[Math.min(i*2, cards.length-1)] ? `#${cards[Math.min(i*2, cards.length-1)].id}` : '#top';
    a.innerHTML = `<span class="index">${idx}</span><span><strong>${title}</strong><span>${desc}</span></span>`;
    board.append(a);
  });
  grid.after(board);
})();
