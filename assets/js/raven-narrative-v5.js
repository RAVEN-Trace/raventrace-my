(() => {
  'use strict';

  const path = location.pathname;
  const ROOT = '/raventrace-my/investigations/rci-tabung-haji/narratives/';
  if (path !== ROOT && path !== `${ROOT}index.html`) return;

  const qa = (s, r = document) => [...r.querySelectorAll(s)];
  const normalize = (s = '') => s.replace(/\s+/g, ' ').trim();
  const directPs = (card) => qa(':scope > p', card);
  const labelled = (card, labels) => directPs(card).find((p) => {
    const b = p.querySelector(':scope > b, :scope > strong');
    const lead = normalize(b?.textContent || '');
    return labels.some((label) => lead.toLowerCase().startsWith(label.toLowerCase()));
  });
  const valueAfterLabel = (p) => {
    if (!p) return '';
    const b = p.querySelector(':scope > b, :scope > strong');
    const full = normalize(p.textContent);
    const lead = normalize(b?.textContent || '');
    return lead ? normalize(full.slice(lead.length).replace(/^\s*[:—-]?\s*/, '')) : full;
  };
  const classify = (status = '') => {
    const t = status.toLowerCase();
    if (/inferens|inference|analisis|motif.*belum/.test(t)) return 'analysis';
    if (/tidak disokong|tak sokong|dipertikai|unsupported|bercanggah|terlalu mudah|belum sepadan/.test(t)) return 'unsupported';
    if (/fakta|posisi.*direkodkan|tindakan.*berlaku|dasar/.test(t)) return 'fact';
    return 'claim';
  };

  /*
   * The evidence set is living content and can grow. Detect the narrative
   * structure itself so a new narrative cannot silently break the reading UX.
   */
  const sections = qa('.case-section');
  const section = sections.find((candidate) => {
    const candidateGrid = candidate.querySelector(':scope > .control-grid, .control-grid');
    if (!candidateGrid) return false;
    const candidateCards = [...candidateGrid.children].filter((el) => el.tagName === 'ARTICLE');
    if (candidateCards.length < 2) return false;
    const structured = candidateCards.filter((card) =>
      labelled(card, ['Cerita yang dibawa']) &&
      labelled(card, ['Apa yang boleh disahkan', 'Apa rekod tunjuk']) &&
      labelled(card, ['Selepas framing dibuang', 'Raven kata macam mana', 'Verdict Raven'])
    );
    return structured.length >= Math.min(2, candidateCards.length);
  });
  if (!section) return;

  const grid = section.querySelector('.control-grid');
  if (!grid) return;

  qa('.narrative-status-strip, .narrative-filterbar, .narrative-board', section).forEach((el) => el.remove());
  grid.classList.add('narrative-v5-grid');

  const cards = [...grid.children].filter((el) => el.tagName === 'ARTICLE');

  cards.forEach((card, index) => {
    if (card.dataset.narrativeV5Ready === 'true') return;
    card.dataset.narrativeV5Ready = 'true';
    card.classList.add('narrative-v5-card');
    card.id ||= `naratif-${String(index + 1).padStart(2, '0')}`;

    qa(':scope > details:not(.narrative-v5-details)', card).forEach((legacy) => {
      qa('.narrative-detail > p', legacy).forEach((p) => card.appendChild(p));
      legacy.remove();
    });
    qa(':scope > .narrative-meta', card).forEach((el) => el.remove());

    const statusP = card.querySelector(':scope > p:has(.status)');
    const statusText = normalize(statusP?.textContent || 'Dakwaan / naratif');
    card.dataset.narrativeCategory = classify(statusText);
    statusP?.classList.add('narrative-status-row');

    const storyP = labelled(card, ['Cerita yang dibawa']);
    const verifiedP = labelled(card, ['Apa yang boleh disahkan', 'Apa rekod tunjuk']);
    const techniqueP = labelled(card, ['Teknik naratif', 'Teknik framing', 'Mekanisme naratif', 'Apa trick cerita ni']);
    const omittedP = labelled(card, ['Apa yang cerita ini tinggalkan', 'Apa yang cerita tak sebut', 'Konteks yang sering tertinggal']);
    const verdictP = labelled(card, ['Selepas framing dibuang', 'Raven kata macam mana', 'Verdict Raven']);
    const changeP = labelled(card, ['Bukti apa boleh mengubah penilaian', 'Apa bukti yang boleh ubah keputusan Raven', 'Apa yang boleh mengubah verdict']);
    const confidenceP = labelled(card, ['Tahap keyakinan', 'Confidence']);

    const story = valueAfterLabel(storyP);
    const verified = valueAfterLabel(verifiedP);
    const technique = valueAfterLabel(techniqueP);
    const omitted = valueAfterLabel(omittedP);
    const verdict = valueAfterLabel(verdictP);
    const change = valueAfterLabel(changeP);

    let confidence = valueAfterLabel(confidenceP);
    let lastVerified = '';
    if (confidence) {
      const split = confidence.split(/·\s*(?:Last verified|Disemak terakhir):\s*/i);
      confidence = normalize(split[0] || '');
      lastVerified = normalize(split[1] || '');
    }

    [storyP, verifiedP, techniqueP, omittedP, verdictP, changeP, confidenceP]
      .filter(Boolean)
      .forEach((p) => p.remove());

    const title = card.querySelector(':scope > h3');
    if (title) {
      const idx = document.createElement('div');
      idx.className = 'narrative-v5-index';
      idx.textContent = `Naratif ${String(index + 1).padStart(2, '0')}`;
      card.insertBefore(idx, title);
    }

    if (verdict) {
      const box = document.createElement('div');
      box.className = 'narrative-v5-verdict';
      box.innerHTML = '<span>Raven kata macam mana?</span><p></p>';
      box.querySelector('p').textContent = verdict;
      card.append(box);
    }

    if (verified) {
      const box = document.createElement('div');
      box.className = 'narrative-v5-record';
      box.innerHTML = '<span>Apa rekod boleh sahkan</span><p></p>';
      box.querySelector('p').textContent = verified;
      card.append(box);
    }

    const detailItems = [
      ['Cerita yang dibawa', story],
      ['Apa trick cerita ni?', technique],
      ['Apa yang cerita tak sebut', omitted],
      ['Apa bukti yang boleh ubah keputusan?', change]
    ].filter(([, text]) => text);

    if (detailItems.length) {
      const details = document.createElement('details');
      details.className = 'narrative-v5-details';
      const summary = document.createElement('summary');
      summary.textContent = 'Kenapa Raven kata begitu?';
      const wrap = document.createElement('div');
      wrap.className = 'narrative-v5-detail-wrap';
      detailItems.forEach(([heading, text]) => {
        const block = document.createElement('div');
        block.className = 'narrative-v5-detail-block';
        const h = document.createElement('h4');
        h.textContent = heading;
        const p = document.createElement('p');
        p.textContent = text;
        block.append(h, p);
        wrap.append(block);
      });
      details.append(summary, wrap);
      card.append(details);
    }

    if (confidence || lastVerified) {
      const meta = document.createElement('div');
      meta.className = 'narrative-v5-meta';
      if (confidence) {
        const c = document.createElement('span');
        c.textContent = `Keyakinan Raven · ${confidence}`;
        meta.append(c);
      }
      if (lastVerified) {
        const d = document.createElement('span');
        d.textContent = `Disemak · ${lastVerified}`;
        meta.append(d);
      }
      card.append(meta);
    }

    qa(':scope > .raven-sharebar', card).forEach((bar) => bar.remove());
  });

  const counts = cards.reduce((acc, card) => {
    const key = card.dataset.narrativeCategory || 'claim';
    acc[key] = (acc[key] || 0) + 1;
    return acc;
  }, {});

  const intro = document.createElement('div');
  intro.className = 'narrative-v5-intro';
  intro.innerHTML = '<strong>Tak perlu telan semua sekaligus.</strong> Pilih satu cerita. Tengok keputusan Raven dulu. Kalau nak tahu kenapa, baru buka bukti dan konteks.';

  const overview = document.createElement('div');
  overview.className = 'narrative-v5-overview';
  overview.innerHTML = `
    <div class="narrative-v5-overview-main"><strong>${cards.length}</strong><span>naratif diperiksa</span></div>
    <div class="narrative-v5-overview-chips">
      <span>${counts.unsupported || 0} tak disokong / dipertikai</span>
      <span>${counts.analysis || 0} analisis</span>
      <span>${counts.fact || 0} fakta / posisi</span>
    </div>`;

  const filter = document.createElement('div');
  filter.className = 'narrative-v5-filterbar';
  filter.setAttribute('aria-label', 'Tapis audit naratif');
  const options = [
    ['all', 'Semua'],
    ['claim', 'Dakwaan'],
    ['unsupported', 'Tak disokong'],
    ['analysis', 'Analisis'],
    ['fact', 'Fakta / posisi']
  ];
  options.forEach(([key, label], i) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.textContent = label;
    button.dataset.narrativeFilter = key;
    button.setAttribute('aria-pressed', i === 0 ? 'true' : 'false');
    button.addEventListener('click', () => {
      qa('button', filter).forEach((b) => b.setAttribute('aria-pressed', 'false'));
      button.setAttribute('aria-pressed', 'true');
      cards.forEach((card) => {
        card.hidden = key !== 'all' && card.dataset.narrativeCategory !== key;
      });
    });
    filter.append(button);
  });

  grid.before(intro, overview, filter);
})();