(() => {
  'use strict';
  if (window.__RAVEN_READER_V13__) return;
  window.__RAVEN_READER_V13__ = true;

  const q = (s, r = document) => r.querySelector(s);
  const qa = (s, r = document) => [...r.querySelectorAll(s)];
  const ROOT = '/raventrace-my/';
  const RCI = `${ROOT}investigations/rci-tabung-haji/`;
  const path = location.pathname;
  const isPolitical = path === `${RCI}narratives/political-social-media/` || path === `${RCI}narratives/political-social-media/index.html`;
  const isNews = path === `${ROOT}news/` || path === `${ROOT}news/index.html`;
  const isPeople = path === `${RCI}people/` || path === `${RCI}people/index.html`;
  const isMoney = path === `${RCI}money/` || path === `${RCI}money/index.html`;
  const isTimeline = path === `${RCI}timeline/` || path === `${RCI}timeline/index.html`;
  if (!(isPolitical || isNews || isPeople || isMoney || isTimeline)) return;

  if (!q('link[data-raven-reader-v13]')) {
    const css = document.createElement('link');
    css.rel = 'stylesheet';
    css.href = `${ROOT}assets/css/raven-reader-v13.css?v=1.3.1`;
    css.dataset.ravenReaderV13 = '';
    document.head.append(css);
  }

  document.body.classList.add('raven-reader-v13');
  const controllers = new Map();

  const emit = (name, detail = {}) => {
    const payload = { name, path, ts: Date.now(), ...detail };
    window.dispatchEvent(new CustomEvent('raven:metric', { detail: payload }));
    if (window.ravenReadMetrics?.events) window.ravenReadMetrics.events.push(payload);
  };

  const wireCompact = (host, { kind = 'reader', keep = [], label = 'Buka butiran', closeLabel = 'Tutup butiran' } = {}) => {
    if (!host || host.dataset.ravenCompactReady === 'true') return null;
    host.dataset.ravenCompactReady = 'true';
    host.classList.add('raven-reader-compact', `raven-${kind}-scan`, 'raven-reader-card-collapsed');
    keep.filter(Boolean).forEach((node) => node.classList.add('raven-reader-keep'));

    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'raven-reader-card-toggle raven-reader-keep';
    button.dataset.ravenEvent = `${kind}_detail_toggle`;
    button.setAttribute('aria-expanded', 'false');
    button.innerHTML = `<span>${label}</span><b aria-hidden="true">+</b>`;

    const setOpen = (open, { scroll = false } = {}) => {
      host.classList.toggle('raven-reader-card-collapsed', !open);
      button.setAttribute('aria-expanded', open ? 'true' : 'false');
      button.querySelector('span').textContent = open ? closeLabel : label;
      button.querySelector('b').textContent = open ? '−' : '+';
      if (scroll) requestAnimationFrame(() => host.scrollIntoView({ block: 'nearest', behavior: 'smooth' }));
      emit('reader_compact_state', { kind, id: host.id || null, open });
    };

    button.addEventListener('click', () => setOpen(button.getAttribute('aria-expanded') !== 'true'));
    const anchor = keep.filter(Boolean).at(-1) || host.firstElementChild;
    if (anchor) anchor.insertAdjacentElement('afterend', button); else host.prepend(button);
    controllers.set(host, setOpen);
    return setOpen;
  };

  const enhanceSourceRoom = () => {
    if (!(isPolitical || isPeople || isMoney || isTimeline)) return;
    const section = q('#sources.source-room, .source-room#sources');
    const heading = q(':scope > h2', section || document);
    if (!section || !heading || section.dataset.ravenSourceReader === 'true') return;
    section.dataset.ravenSourceReader = 'true';
    section.classList.add('raven-reader-source-room', 'raven-reader-source-collapsed');

    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'raven-source-room-toggle';
    button.dataset.ravenEvent = 'source_room_toggle';
    button.setAttribute('aria-expanded', 'false');
    button.innerHTML = '<span>Buka Source Room</span><b aria-hidden="true">+</b>';
    const setOpen = (open) => {
      section.classList.toggle('raven-reader-source-collapsed', !open);
      button.setAttribute('aria-expanded', open ? 'true' : 'false');
      button.querySelector('span').textContent = open ? 'Tutup Source Room' : 'Buka Source Room';
      button.querySelector('b').textContent = open ? '−' : '+';
      emit('source_room_state', { open });
    };
    section._ravenSourceOpen = setOpen;
    button.addEventListener('click', () => setOpen(button.getAttribute('aria-expanded') !== 'true'));
    heading.insertAdjacentElement('afterend', button);
  };

  const enhancePolitical = () => {
    if (!isPolitical) return;
    document.body.classList.add('raven-reader-political');
    const article = q('.section-content');
    const sections = qa(':scope > .case-section', article || document);

    const sourceSection = sections.find((section) => /sumber silang/i.test(q('.section-marker p', section)?.textContent || ''));
    if (sourceSection) {
      sourceSection.id ||= 'sources';
      sourceSection.classList.add('source-room');
    }

    if (article && !q('.raven-question-rail', article)) {
      const rail = document.createElement('nav');
      rail.className = 'raven-question-rail';
      rail.setAttribute('aria-label', 'Pilih soalan audit naratif');
      rail.innerHTML = '<p><strong>Pilih soalan.</strong> Tak perlu baca semuanya ikut turutan.</p>';
      let no = 0;
      sections.filter((s) => !s.classList.contains('source-room')).forEach((section, i) => {
        const heading = q(':scope > h2', section);
        if (!heading) return;
        section.id ||= `audit-soalan-${String(i + 1).padStart(2, '0')}`;
        no += 1;
        const a = document.createElement('a');
        a.href = `#${section.id}`;
        a.innerHTML = `<span>${String(no).padStart(2, '0')}</span><strong>${heading.textContent.trim()}</strong>`;
        rail.append(a);
      });
      article.prepend(rail);
    }

    [['#matrix .control-grid > article','political-position'],['#language-forensics .control-grid > article','narrative-technique']].forEach(([selector,prefix]) => {
      qa(selector).forEach((card,index) => {
        card.id ||= `${prefix}-${String(index + 1).padStart(2, '0')}`;
        const title = q(':scope > h3', card);
        const status = qa(':scope > p', card).find((p) => q('.status', p));
        wireCompact(card,{kind:'political',keep:[title,status],label:'Apa bukti / konteks?',closeLabel:'Tutup bukti / konteks'});
      });
    });

    qa('.control-grid > article').forEach((card,index) => {
      if (card.dataset.ravenCompactReady === 'true') return;
      card.id ||= `political-proof-${String(index + 1).padStart(2, '0')}`;
      const title = q(':scope > h3', card);
      const status = qa(':scope > p', card).find((p) => q('.status', p));
      wireCompact(card,{kind:'political-proof',keep:[title,status],label:'Apa perlu dibuktikan?',closeLabel:'Tutup butiran bukti'});
    });
  };

  const enhanceNews = () => {
    if (!isNews) return;
    document.body.classList.add('raven-reader-newsroom');
    const timeline = q('.timeline');
    if (!timeline) return;
    const items = qa('.timeline-item', timeline);
    items.forEach((item) => {
      const body = q(':scope > div', item);
      if (!body) return;
      wireCompact(body,{kind:'news',keep:[q(':scope > .meta-row',body),q(':scope > h3',body)],label:'Buka ringkasan & pautan',closeLabel:'Tutup ringkasan'});
    });
    if (!q('.raven-news-desk')) {
      const count = (selector) => items.filter((item) => q(selector,item)).length;
      const desk = document.createElement('section');
      desk.className = 'raven-news-desk';
      desk.setAttribute('aria-label','Ringkasan status newsroom');
      desk.innerHTML = `<div><strong>${count('.status.fact')}</strong><span>Disahkan / fakta</span></div><div><strong>${count('.status.process')}</strong><span>Proses aktif</span></div><div><strong>${items.filter((item)=>q('.status.disputed,.status.context,.status.unknown,.status.claim',item)).length}</strong><span>Perlu konteks / semakan</span></div>`;
      timeline.before(desk);
    }
  };

  const enhancePeople = () => {
    if (!isPeople) return;
    document.body.classList.add('raven-reader-people');
    const grid = q('.people-grid');
    if (!grid) return;
    if (!q('.raven-status-first-note')) {
      const note = document.createElement('div');
      note.className = 'raven-status-first-note';
      note.innerHTML = '<strong>Baca status dahulu.</strong><span>Disebut ≠ disiasat ≠ ditahan ≠ direman ≠ didakwa ≠ bersalah.</span>';
      grid.before(note);
    }
    qa(':scope > .person-card',grid).forEach((card,index)=>{
      const head=q(':scope > div',card), title=q(':scope > h3',card), role=q(':scope > .role',card);
      const num=q(':scope > div > span:first-child',card)?.textContent?.trim() || String(index+1).padStart(2,'0');
      card.id ||= `person-${num.replace(/\D+/g,'') || String(index+1).padStart(2,'0')}`;
      wireCompact(card,{kind:'person',keep:[head,title,role],label:'Lihat status penuh',closeLabel:'Tutup status penuh'});
    });
  };

  const enhanceMoney = () => {
    if (!isMoney) return;
    document.body.classList.add('raven-reader-money');
    const grid=q('#money .metric-grid') || q('.section-content .metric-grid') || q('.metric-grid');
    if (!grid) return;
    if (!q('.raven-money-distinction')) {
      const strip=document.createElement('div');
      strip.className='raven-money-distinction';
      strip.innerHTML='<span>Nilai transaksi</span><b>≠</b><span>Kerugian</span><b>≠</b><span>Susut nilai</span><b>≠</b><span>Kos pemulihan</span>';
      grid.before(strip);
    }
    qa(':scope > article',grid).forEach((card)=>wireCompact(card,{kind:'money',keep:[q(':scope > strong',card),q(':scope > span',card),q(':scope > h3',card)],label:'Apa maksud angka ini?',closeLabel:'Tutup penerangan'}));
    const glossary=q('#money .metric-glossary') || q('.metric-glossary');
    if (glossary) wireCompact(glossary,{kind:'money-mechanism',keep:[q(':scope > h3',glossary)],label:'Buka mekanisme UJSB',closeLabel:'Tutup mekanisme UJSB'});
  };

  const enhanceTimeline = () => {
    if (!isTimeline) return;
    document.body.classList.add('raven-reader-timeline');
    const section=q('#timeline') || q('.section-content');
    if (!section) return;
    const heads=qa('.subhead',section);
    if (heads.length && !q('.raven-timeline-phase-nav',section)) {
      const nav=document.createElement('nav');
      nav.className='raven-timeline-phase-nav';
      nav.setAttribute('aria-label','Pilih fasa kronologi');
      heads.forEach((h,i)=>{
        h.id ||= `timeline-phase-${String.fromCharCode(97+i)}`;
        const a=document.createElement('a');
        a.href=`#${h.id}`;
        a.innerHTML=`<span>${String.fromCharCode(65+i)}</span><strong>${h.textContent.replace(/^\s*[A-Z]\s*·\s*/,'').trim()}</strong>`;
        nav.append(a);
      });
      q('h2',section)?.insertAdjacentElement('afterend',nav);
    }
    qa('.history-line',section).forEach((line,phaseIndex)=>qa(':scope > article',line).forEach((item,index)=>{
      item.id ||= `timeline-${String.fromCharCode(97+phaseIndex)}-${String(index+1).padStart(2,'0')}`;
      wireCompact(item,{kind:'timeline',keep:[q(':scope > time',item),q(':scope > h3',item)],label:'Kenapa ini penting?',closeLabel:'Tutup penerangan'});
    }));
  };

  const revealHash = ({scroll=false}={}) => {
    if (!location.hash) return;
    const id=decodeURIComponent(location.hash.slice(1));
    const target=document.getElementById(id);
    if (!target) return;
    const compact=target.closest?.('.raven-reader-compact');
    const open=controllers.get(compact);
    if (open) open(true);
    const source=target.closest?.('.raven-reader-source-room');
    if (source?._ravenSourceOpen) source._ravenSourceOpen(true);
    if (scroll) requestAnimationFrame(()=>target.scrollIntoView({block:'start',behavior:'smooth'}));
  };

  enhancePolitical();
  enhanceNews();
  enhancePeople();
  enhanceMoney();
  enhanceTimeline();
  enhanceSourceRoom();
  setTimeout(()=>revealHash(),180);
  addEventListener('hashchange',()=>revealHash({scroll:true}));
})();
