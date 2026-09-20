(() => {
  'use strict';

  const path = location.pathname;
  const ROOT = '/raventrace-my/investigations/rci-tabung-haji/narratives/';
  if (path !== ROOT && path !== `${ROOT}index.html`) return;

  const qa = (selector, root = document) => [...root.querySelectorAll(selector)];
  const normalize = (value = '') => value.replace(/\s+/g, ' ').trim();
  const labelText = (p) => normalize(p?.querySelector(':scope > b, :scope > strong')?.textContent || '').toLowerCase();

  const roleFor = (p) => {
    const label = labelText(p);
    if (!label) return 'extra';
    if (label.startsWith('jurang cerita')) return 'gap';
    if (label === 'raven:' || label.startsWith('raven:')) return 'verdict';
    if (
      label.startsWith('rekod') ||
      label.startsWith('government position') ||
      label.startsWith('umno position') ||
      label.startsWith('apa baharu') ||
      label.startsWith('apa berubah')
    ) return 'record';
    return 'extra';
  };

  const grids = qa('.case-section .control-grid');
  const grid = grids.find((candidate) => {
    const cards = [...candidate.children].filter((el) => el.tagName === 'ARTICLE');
    if (cards.length < 2) return false;
    return cards.filter((card) => {
      const roles = qa(':scope > p', card).map(roleFor);
      return roles.includes('record') && (roles.includes('gap') || roles.includes('verdict'));
    }).length >= Math.min(2, cards.length);
  });
  if (!grid) return;

  grid.classList.add('narrative-locked-grid');
  const cards = [...grid.children].filter((el) => el.tagName === 'ARTICLE');

  cards.forEach((card, index) => {
    if (card.dataset.narrativeLockedReady === 'true') return;

    const before = normalize(card.textContent);
    const title = card.querySelector(':scope > h3');
    const status = card.querySelector(':scope > p:has(.status)');
    if (!title) return;

    card.dataset.narrativeLockedReady = 'true';
    card.classList.add('narrative-locked-card');
    card.id ||= `naratif-${String(index + 1).padStart(2, '0')}`;
    title.id ||= `${card.id}-title`;
    card.setAttribute('aria-labelledby', title.id);

    if (status) status.classList.add('narrative-status-row');

    const paragraphs = qa(':scope > p', card).filter((p) => p !== status);
    const recordPs = paragraphs.filter((p) => roleFor(p) === 'record');
    const gapPs = paragraphs.filter((p) => roleFor(p) === 'gap');
    const verdictPs = paragraphs.filter((p) => roleFor(p) === 'verdict');
    const extraPs = paragraphs.filter((p) => roleFor(p) === 'extra');

    const split = document.createElement('div');
    split.className = 'narrative-locked-split';

    const claim = document.createElement('div');
    claim.className = 'narrative-locked-claim signal-claim-zone';
    claim.append(title);
    if (status) claim.append(status);

    const record = document.createElement('div');
    record.className = 'narrative-locked-record signal-record-zone';
    recordPs.forEach((p) => record.append(p));

    split.append(claim, record);
    card.append(split);

    if (gapPs.length) {
      const gap = document.createElement('div');
      gap.className = 'narrative-locked-gap signal-gap';
      gapPs.forEach((p) => gap.append(p));
      card.append(gap);
    }

    if (verdictPs.length) {
      const verdict = document.createElement('div');
      verdict.className = 'narrative-locked-verdict signal-verdict-zone';
      verdictPs.forEach((p) => verdict.append(p));
      card.append(verdict);
    }

    if (extraPs.length) {
      const extra = document.createElement('div');
      extra.className = 'narrative-locked-extra';
      extraPs.forEach((p) => extra.append(p));
      card.append(extra);
    }

    const after = normalize(card.textContent);
    card.dataset.copyLock = before === after ? 'preserved' : 'mismatch';
    if (before !== after) {
      console.error('RAVEN narrative copy-lock mismatch', card.id);
    }
  });

  document.body.dataset.ravenNarrativeStructure = 'locked-v1';
})();