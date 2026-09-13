(() => {
  'use strict';
  if (window.__RAVEN_DEEPCASE_V14__) return;
  window.__RAVEN_DEEPCASE_V14__ = true;

  const q = (s, r = document) => r.querySelector(s);
  const qa = (s, r = document) => [...r.querySelectorAll(s)];
  const ROOT = '/raventrace-my/';
  const RCI = `${ROOT}investigations/rci-tabung-haji/`;
  const normalizedPath = location.pathname.endsWith('/index.html')
    ? location.pathname.replace(/index\.html$/, '')
    : location.pathname;

  const route = normalizedPath.startsWith(RCI)
    ? normalizedPath.slice(RCI.length).replace(/\/$/, '')
    : '';
  const isGovernance = route === 'governance';
  const isInvestments = route === 'investments';
  const isTracks = route === 'tracks';
  const isDisputed = route === 'disputed-record';
  const isSources = route === 'sources';

  if (!(isGovernance || isInvestments || isTracks || isDisputed || isSources)) return;

  document.body.classList.add('raven-deepcase-v14', `raven-deepcase-${route}`);
  const controllers = new Map();

  const emit = (name, detail = {}) => {
    const payload = { name, path: location.pathname, ts: Date.now(), ...detail };
    try { window.dispatchEvent(new CustomEvent('raven:metric', { detail: payload })); } catch (_) {}
    try { window.ravenReadMetrics?.events?.push(payload); } catch (_) {}
  };

  const make = (tag, className, text) => {
    const el = document.createElement(tag);
    if (className) el.className = className;
    if (text != null) el.textContent = text;
    return el;
  };

  const wireCompact = (host, {
    kind = 'deepcase',
    keep = [],
    label = 'Buka butiran',
    closeLabel = 'Tutup butiran'
  } = {}) => {
    if (!host || host.dataset.ravenDeepcaseReady === 'true') return controllers.get(host) || null;
    host.dataset.ravenDeepcaseReady = 'true';
    host.classList.add('raven-deepcase-compact', `raven-${kind}-scan`, 'raven-deepcase-collapsed');
    keep.filter(Boolean).forEach((node) => node.classList.add('raven-deepcase-keep'));

    const button = make('button', 'raven-deepcase-toggle raven-deepcase-keep');
    button.type = 'button';
    button.dataset.ravenEvent = `${kind}_detail_toggle`;
    button.setAttribute('aria-expanded', 'false');
    button.innerHTML = `<span>${label}</span><b aria-hidden="true">+</b>`;

    const setOpen = (open, { scroll = false } = {}) => {
      host.classList.toggle('raven-deepcase-collapsed', !open);
      button.setAttribute('aria-expanded', open ? 'true' : 'false');
      q('span', button).textContent = open ? closeLabel : label;
      q('b', button).textContent = open ? '−' : '+';
      if (scroll) requestAnimationFrame(() => host.scrollIntoView({ block: 'nearest', behavior: 'smooth' }));
      emit('deepcase_compact_state', { kind, id: host.id || null, open });
    };

    button.addEventListener('click', () => setOpen(button.getAttribute('aria-expanded') !== 'true'));
    const anchor = keep.filter(Boolean).at(-1) || host.firstElementChild;
    if (anchor) anchor.insertAdjacentElement('afterend', button);
    else host.prepend(button);
    controllers.set(host, setOpen);
    return setOpen;
  };

  const enhanceSourceRoom = () => {
    if (isSources) return;
    const section = q('#sources.source-room, .source-room#sources');
    const heading = q(':scope > h2', section || document);
    if (!section || !heading || section.dataset.ravenDeepSource === 'true') return;
    section.dataset.ravenDeepSource = 'true';
    section.classList.add('raven-deepcase-source-room', 'raven-deepcase-source-collapsed');

    const button = make('button', 'raven-deepcase-source-toggle');
    button.type = 'button';
    button.dataset.ravenEvent = 'deepcase_source_room_toggle';
    button.setAttribute('aria-expanded', 'false');
    button.innerHTML = '<span>Buka Source Room</span><b aria-hidden="true">+</b>';

    const setOpen = (open) => {
      section.classList.toggle('raven-deepcase-source-collapsed', !open);
      button.setAttribute('aria-expanded', open ? 'true' : 'false');
      q('span', button).textContent = open ? 'Tutup Source Room' : 'Buka Source Room';
      q('b', button).textContent = open ? '−' : '+';
      emit('deepcase_source_room_state', { open });
    };
    section._ravenDeepSourceOpen = setOpen;
    button.addEventListener('click', () => setOpen(button.getAttribute('aria-expanded') !== 'true'));
    heading.insertAdjacentElement('afterend', button);
  };

  const insertScanIntro = (section, title, copy, count) => {
    if (!section || q(':scope > .raven-deepcase-intro', section)) return;
    const intro = make('div', 'raven-deepcase-intro');
    intro.innerHTML = `<div><strong>${count}</strong><span>${title}</span></div><p>${copy}</p>`;
    const grid = q(':scope > .control-grid, :scope > .investment-list', section);
    if (grid) grid.before(intro);
  };

  const enhanceGovernance = () => {
    if (!isGovernance) return;
    const section = q('#governance');
    const cards = qa(':scope > .control-grid > article', section || document);
    if (!section || !cards.length) return;
    document.body.classList.add('raven-deepcase-governance');
    insertScanIntro(
      section,
      'dapatan / isu untuk discan',
      'Baca tajuk dulu. Buka hanya isu yang kau nak semak — semua teks dan sumber asal masih kekal dalam halaman.',
      cards.length
    );
    cards.forEach((card, index) => {
      card.id ||= `governance-${String(index + 1).padStart(2, '0')}`;
      wireCompact(card, {
        kind: 'governance',
        keep: [q(':scope > h3', card)],
        label: 'Buka dapatan & sumber',
        closeLabel: 'Tutup dapatan'
      });
    });
  };

  const enhanceInvestments = () => {
    if (!isInvestments) return;
    const section = q('#investments');
    const list = q('.investment-list', section || document);
    const items = qa(':scope > details.investment', list || document);
    if (!section || !list || !items.length) return;
    document.body.classList.add('raven-deepcase-investments');

    items.forEach((item, index) => {
      const code = q('summary > span', item)?.textContent?.trim() || `I${String(index + 1).padStart(2, '0')}`;
      item.id ||= `investment-${code.toLowerCase()}`;
      item.dataset.ravenSearch = (item.textContent || '').replace(/\s+/g, ' ').toLowerCase();
      item.dataset.ravenDisputed = item.classList.contains('disputed-investment') ? 'true' : 'false';
      item.addEventListener('toggle', () => emit('investment_record_state', { id: item.id, open: item.open }));
    });

    if (!q('.raven-investment-browser', section)) {
      const browser = make('section', 'raven-investment-browser');
      browser.setAttribute('aria-label', 'Tapis 14 rekod pelaburan');
      browser.innerHTML = `
        <div class="raven-browser-heading">
          <div><strong>14 rekod. Cari yang kau perlukan.</strong><span>Filter hanya mengubah paparan — bukan status bukti.</span></div>
          <output aria-live="polite"></output>
        </div>
        <label class="raven-browser-search"><span>Cari nama / isu</span><input type="search" placeholder="Contoh: Al-Rawda, bonus, susut nilai"></label>
        <div class="raven-browser-filters" role="group" aria-label="Filter rekod pelaburan">
          <button type="button" data-mode="all" aria-pressed="true">Semua</button>
          <button type="button" data-mode="disputed" aria-pressed="false">Dipertikaikan</button>
          <button type="button" data-mode="impairment" aria-pressed="false">Rosot / susut nilai</button>
          <button type="button" data-mode="investigation" aria-pressed="false">Siasatan</button>
        </div>`;
      list.before(browser);

      const input = q('input', browser);
      const output = q('output', browser);
      const buttons = qa('[data-mode]', browser);
      let mode = 'all';

      const apply = () => {
        const term = input.value.trim().toLowerCase();
        let visible = 0;
        items.forEach((item) => {
          const text = item.dataset.ravenSearch || '';
          const modeMatch =
            mode === 'all' ||
            (mode === 'disputed' && item.dataset.ravenDisputed === 'true') ||
            (mode === 'impairment' && /rosot|susut nilai|kemerosotan nilai/.test(text)) ||
            (mode === 'investigation' && /siasatan|sprm|pdrm|audit|pemeriksaan/.test(text));
          const termMatch = !term || text.includes(term);
          item.hidden = !(modeMatch && termMatch);
          if (!item.hidden) visible += 1;
        });
        output.textContent = `${visible} / ${items.length}`;
        emit('investment_filter', { mode, term: term.slice(0, 80), visible });
      };

      input.addEventListener('input', apply);
      buttons.forEach((button) => button.addEventListener('click', () => {
        mode = button.dataset.mode;
        buttons.forEach((b) => b.setAttribute('aria-pressed', String(b === button)));
        apply();
      }));
      apply();
    }
  };

  const enhanceTracks = () => {
    if (!isTracks) return;
    const section = q('#tracks');
    const grid = q(':scope > .control-grid', section || document);
    const cards = qa(':scope > article', grid || document);
    if (!section || !grid || !cards.length) return;
    document.body.classList.add('raven-deepcase-tracks');

    if (!q('.raven-track-rail', section)) {
      const rail = make('nav', 'raven-track-rail');
      rail.setAttribute('aria-label', 'Pilih trek siasatan');
      rail.innerHTML = '<p><strong>Jangan campur set data.</strong><span>Setiap kad di bawah merujuk trek / fasa yang berbeza.</span></p>';
      cards.forEach((card, index) => {
        card.id ||= `track-${String(index + 1).padStart(2, '0')}`;
        const title = q(':scope > h3', card)?.textContent?.trim() || `Trek ${index + 1}`;
        const a = make('a');
        a.href = `#${card.id}`;
        a.innerHTML = `<span>${String(index + 1).padStart(2, '0')}</span><strong>${title}</strong>`;
        rail.append(a);
      });
      grid.before(rail);
    }

    cards.forEach((card, index) => {
      card.id ||= `track-${String(index + 1).padStart(2, '0')}`;
      wireCompact(card, {
        kind: 'track',
        keep: [q(':scope > h3', card)],
        label: 'Buka status & bukti',
        closeLabel: 'Tutup status'
      });
    });
  };

  const enhanceDisputed = () => {
    if (!isDisputed) return;
    const section = q('#disputed-record');
    const grid = q(':scope > .control-grid', section || document);
    const cards = qa(':scope > article', grid || document);
    if (!section || !grid || !cards.length) return;
    document.body.classList.add('raven-deepcase-disputed');

    if (!q('.raven-disputed-desk', section)) {
      const count = (selector) => cards.filter((card) => q(selector, card)).length;
      const desk = make('section', 'raven-disputed-desk');
      desk.setAttribute('aria-label', 'Ringkasan status rekod dipertikaikan');
      desk.innerHTML = `
        <div><strong>${count('.status.fact')}</strong><span>Fakta bersama</span></div>
        <div><strong>${count('.status.disputed')}</strong><span>Dipertikaikan</span></div>
        <div><strong>${count('.status.unknown')}</strong><span>Belum diketahui</span></div>
        <p>Status dulu, hujah kemudian. “Dipertikaikan” bukan bermaksud salah satu pihak automatik menipu.</p>`;
      grid.before(desk);
    }

    cards.forEach((card, index) => {
      card.id ||= `disputed-${String(index + 1).padStart(2, '0')}`;
      wireCompact(card, {
        kind: 'disputed',
        keep: [q(':scope > h3', card)],
        label: 'Kenapa status ini?',
        closeLabel: 'Tutup penjelasan'
      });
    });
  };

  const enhanceSources = () => {
    if (!isSources) return;
    const section = q('#sources.source-room, .source-room#sources');
    const list = q(':scope > .sources-grid', section || document);
    const rows = qa(':scope > li[id]', list || document);
    if (!section || !list || !rows.length) return;
    document.body.classList.add('raven-deepcase-sources');

    rows.forEach((row) => {
      row.dataset.ravenGrade = q(':scope > span', row)?.textContent?.trim().toUpperCase() || '?';
      row.dataset.ravenSearch = (row.textContent || '').replace(/\s+/g, ' ').toLowerCase();
    });

    if (!q('.raven-source-browser', section)) {
      const grades = [...new Set(rows.map((row) => row.dataset.ravenGrade))].filter(Boolean).sort();
      const browser = make('section', 'raven-source-browser');
      browser.setAttribute('aria-label', 'Cari dan tapis sumber');
      browser.innerHTML = `
        <div class="raven-browser-heading">
          <div><strong>Evidence browser</strong><span>Cari ikut nombor sumber, organisasi, individu atau tajuk.</span></div>
          <output aria-live="polite"></output>
        </div>
        <label class="raven-browser-search"><span>Cari sumber</span><input type="search" placeholder="Contoh: S31, Madinah, MOF, SPRM"></label>
        <div class="raven-browser-filters" role="group" aria-label="Filter gred sumber"></div>`;
      list.before(browser);

      const filterHost = q('.raven-browser-filters', browser);
      const all = make('button', '', 'Semua');
      all.type = 'button';
      all.dataset.grade = 'all';
      all.setAttribute('aria-pressed', 'true');
      filterHost.append(all);
      grades.forEach((grade) => {
        const button = make('button', '', `Gred ${grade}`);
        button.type = 'button';
        button.dataset.grade = grade;
        button.setAttribute('aria-pressed', 'false');
        filterHost.append(button);
      });

      const input = q('input', browser);
      const output = q('output', browser);
      const buttons = qa('[data-grade]', browser);
      let grade = 'all';

      const apply = () => {
        const term = input.value.trim().toLowerCase();
        let visible = 0;
        rows.forEach((row) => {
          const gradeMatch = grade === 'all' || row.dataset.ravenGrade === grade;
          const termMatch = !term || row.dataset.ravenSearch.includes(term) || row.id.toLowerCase().includes(term);
          row.hidden = !(gradeMatch && termMatch);
          if (!row.hidden) visible += 1;
        });
        output.textContent = `${visible} / ${rows.length}`;
        emit('source_filter', { grade, term: term.slice(0, 80), visible });
      };

      input.addEventListener('input', apply);
      buttons.forEach((button) => button.addEventListener('click', () => {
        grade = button.dataset.grade;
        buttons.forEach((b) => b.setAttribute('aria-pressed', String(b === button)));
        apply();
      }));
      browser._ravenSourceFilterReset = () => {
        grade = 'all';
        input.value = '';
        buttons.forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.grade === 'all')));
        apply();
      };
      apply();
    }
  };

  const revealHash = ({ scroll = false } = {}) => {
    if (!location.hash) return;
    const id = decodeURIComponent(location.hash.slice(1));
    const target = document.getElementById(id);
    if (!target) return;

    const compact = target.closest?.('.raven-deepcase-compact');
    const open = controllers.get(compact);
    if (open) open(true);

    const sourceRoom = target.closest?.('.raven-deepcase-source-room');
    if (sourceRoom?._ravenDeepSourceOpen) sourceRoom._ravenDeepSourceOpen(true);

    const investment = target.closest?.('details.investment');
    if (investment) investment.open = true;

    if (isSources && target.matches('#sources .sources-grid > li[id]')) {
      q('.raven-source-browser')?._ravenSourceFilterReset?.();
      target.hidden = false;
    }

    if (scroll) requestAnimationFrame(() => target.scrollIntoView({ block: 'start', behavior: 'smooth' }));
  };

  enhanceGovernance();
  enhanceInvestments();
  enhanceTracks();
  enhanceDisputed();
  enhanceSources();
  enhanceSourceRoom();
  setTimeout(() => revealHash(), 180);
  addEventListener('hashchange', () => revealHash({ scroll: true }));
})();
