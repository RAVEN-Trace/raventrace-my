from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JS = ROOT / 'assets/js/raven-funnel-v1.js'
CSS = ROOT / 'assets/css/raven-funnel-v1.css'
APPLY = ROOT / 'scripts/apply_raven_funnel_v1.py'
APPLY_WF = ROOT / '.github/workflows/apply-raven-funnel-v1.yml'
FUNNEL_QA = ROOT / '.github/workflows/raven-funnel-v1-qa.yml'

JS_MARK = '/* RAVEN READER V1.3 — section-page scan architecture */'
CSS_MARK = '/* RAVEN READER V1.3 — section-page scan architecture */'

js_block = r'''

  /* RAVEN READER V1.3 — section-page scan architecture */
  const readerPath = location.pathname;
  const isPoliticalSocial = readerPath === `${RCI}narratives/political-social-media/` || readerPath === `${RCI}narratives/political-social-media/index.html`;
  const isNewsroom = readerPath === `${ROOT}news/` || readerPath === `${ROOT}news/index.html`;
  const isPeoplePage = readerPath === `${RCI}people/` || readerPath === `${RCI}people/index.html`;
  const isMoneyPage = readerPath === `${RCI}money/` || readerPath === `${RCI}money/index.html`;
  const isTimelinePage = readerPath === `${RCI}timeline/` || readerPath === `${RCI}timeline/index.html`;
  const compactControllers = new Map();

  const wireCompact = (host, { kind = 'reader', keep = [], label = 'Buka butiran', closeLabel = 'Tutup butiran' } = {}) => {
    if (!host || host.dataset.ravenCompactReady === 'true') return null;
    host.dataset.ravenCompactReady = 'true';
    host.classList.add('raven-reader-compact', `raven-${kind}-scan`, 'raven-reader-card-collapsed');
    keep.filter(Boolean).forEach((node) => node.classList.add('raven-reader-keep'));

    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'raven-reader-card-toggle raven-reader-keep';
    button.dataset.ravenEvent = `${kind}_detail_toggle`;
    button.innerHTML = `<span>${label}</span><b aria-hidden="true">+</b>`;

    const setOpen = (open, { scroll = false } = {}) => {
      host.classList.toggle('raven-reader-card-collapsed', !open);
      button.setAttribute('aria-expanded', open ? 'true' : 'false');
      button.querySelector('span').textContent = open ? closeLabel : label;
      button.querySelector('b').textContent = open ? '−' : '+';
      if (scroll) requestAnimationFrame(() => host.scrollIntoView({ block: 'nearest', behavior: 'smooth' }));
      emit('reader_compact_state', { kind, id: host.id || null, open });
    };
    setOpen(false);
    button.addEventListener('click', () => setOpen(button.getAttribute('aria-expanded') !== 'true'));

    const anchor = keep.filter(Boolean).at(-1) || host.firstElementChild;
    if (anchor) anchor.insertAdjacentElement('afterend', button); else host.prepend(button);
    compactControllers.set(host, setOpen);
    return setOpen;
  };

  const revealCompactHash = ({ scroll = false } = {}) => {
    if (!location.hash) return;
    const id = decodeURIComponent(location.hash.slice(1));
    const target = document.getElementById(id);
    if (!target) return;
    const compact = target.closest?.('.raven-reader-compact');
    const open = compactControllers.get(compact);
    if (open) open(true);
    const source = target.closest?.('.raven-reader-source-room');
    if (source?._ravenSourceOpen) source._ravenSourceOpen(true);
    if (scroll) requestAnimationFrame(() => target.scrollIntoView({ block: 'start', behavior: 'smooth' }));
  };

  const enhanceSourceRoomDisclosure = () => {
    if (!(isPoliticalSocial || isPeoplePage || isMoneyPage || isTimelinePage)) return;
    const section = q('#sources.source-room, .source-room#sources');
    const heading = q(':scope > h2', section || document);
    if (!section || !heading || section.dataset.ravenSourceReader === 'true') return;
    section.dataset.ravenSourceReader = 'true';
    section.classList.add('raven-reader-source-room', 'raven-reader-source-collapsed');

    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'raven-source-room-toggle';
    button.dataset.ravenEvent = 'source_room_toggle';
    button.innerHTML = '<span>Buka Source Room</span><b aria-hidden="true">+</b>';
    const setOpen = (open) => {
      section.classList.toggle('raven-reader-source-collapsed', !open);
      button.setAttribute('aria-expanded', open ? 'true' : 'false');
      button.querySelector('span').textContent = open ? 'Tutup Source Room' : 'Buka Source Room';
      button.querySelector('b').textContent = open ? '−' : '+';
      emit('source_room_state', { open });
    };
    section._ravenSourceOpen = setOpen;
    setOpen(false);
    button.addEventListener('click', () => setOpen(button.getAttribute('aria-expanded') !== 'true'));
    heading.insertAdjacentElement('afterend', button);

    document.addEventListener('click', (event) => {
      const a = event.target.closest?.('a[href^="#"]');
      if (!a) return;
      const target = document.getElementById(decodeURIComponent((a.getAttribute('href') || '').slice(1)));
      if (target?.closest?.('#sources')) setOpen(true);
    }, { capture: true });
  };

  const enhancePoliticalSocialReader = () => {
    if (!isPoliticalSocial) return;
    document.body.classList.add('raven-reader-political');
    const article = q('.section-content');
    const sections = qa(':scope > .case-section', article || document);
    if (article && !q('.raven-question-rail', article)) {
      const rail = document.createElement('nav');
      rail.className = 'raven-question-rail';
      rail.setAttribute('aria-label', 'Pilih soalan audit naratif');
      const links = [];
      sections.filter((s) => !s.classList.contains('source-room')).forEach((section, i) => {
        const heading = q(':scope > h2', section);
        if (!heading) return;
        section.id ||= `audit-soalan-${String(i + 1).padStart(2, '0')}`;
        const a = document.createElement('a');
        a.href = `#${section.id}`;
        a.innerHTML = `<span>${String(links.length + 1).padStart(2, '0')}</span><strong>${(heading.textContent || '').trim()}</strong>`;
        links.push(a);
      });
      rail.innerHTML = '<p><strong>Pilih soalan.</strong> Tak perlu baca semuanya ikut turutan.</p>';
      links.forEach((a) => rail.append(a));
      article.prepend(rail);
    }

    const groups = [
      ['#matrix .control-grid > article', 'political-position'],
      ['#language-forensics .control-grid > article', 'narrative-technique']
    ];
    groups.forEach(([selector, prefix]) => qa(selector).forEach((card, index) => {
      card.id ||= `${prefix}-${String(index + 1).padStart(2, '0')}`;
      const title = q(':scope > h3', card);
      const status = qa(':scope > p', card).find((p) => q('.status', p));
      wireCompact(card, { kind: 'political', keep: [title, status], label: 'Apa bukti / konteks?', closeLabel: 'Tutup bukti / konteks' });
    }));
  };

  const enhanceNewsroomReader = () => {
    if (!isNewsroom) return;
    document.body.classList.add('raven-reader-newsroom');
    const timeline = q('.timeline');
    if (!timeline) return;
    const items = qa('.timeline-item', timeline);
    items.forEach((item) => {
      const body = q(':scope > div', item);
      if (!body) return;
      const meta = q(':scope > .meta-row', body);
      const title = q(':scope > h3', body);
      wireCompact(body, { kind: 'news', keep: [meta, title], label: 'Buka ringkasan & pautan', closeLabel: 'Tutup ringkasan' });
    });

    if (!q('.raven-news-desk')) {
      const count = (selector) => items.filter((item) => q(selector, item)).length;
      const confirmed = count('.status.fact');
      const process = count('.status.process');
      const caution = items.filter((item) => q('.status.disputed, .status.context, .status.unknown, .status.claim', item)).length;
      const desk = document.createElement('section');
      desk.className = 'raven-news-desk';
      desk.setAttribute('aria-label', 'Ringkasan status newsroom');
      desk.innerHTML = `
        <div><strong>${confirmed}</strong><span>Disahkan / fakta</span></div>
        <div><strong>${process}</strong><span>Proses aktif</span></div>
        <div><strong>${caution}</strong><span>Perlu konteks / semakan</span></div>`;
      timeline.before(desk);
    }
  };

  const enhancePeopleReader = () => {
    if (!isPeoplePage) return;
    document.body.classList.add('raven-reader-people');
    const grid = q('.people-grid');
    if (!grid) return;
    if (!q('.raven-status-first-note')) {
      const note = document.createElement('div');
      note.className = 'raven-status-first-note';
      note.innerHTML = '<strong>Baca status dahulu.</strong><span>Disebut ≠ disiasat ≠ ditahan ≠ direman ≠ didakwa ≠ bersalah.</span>';
      grid.before(note);
    }
    qa(':scope > .person-card', grid).forEach((card, index) => {
      const head = q(':scope > div', card);
      const title = q(':scope > h3', card);
      const role = q(':scope > .role', card);
      const num = q(':scope > div > span:first-child', card)?.textContent?.trim() || String(index + 1).padStart(2, '0');
      card.id ||= `person-${num.replace(/\D+/g, '') || String(index + 1).padStart(2, '0')}`;
      wireCompact(card, { kind: 'person', keep: [head, title, role], label: 'Lihat status penuh', closeLabel: 'Tutup status penuh' });
    });
  };

  const enhanceMoneyReader = () => {
    if (!isMoneyPage) return;
    document.body.classList.add('raven-reader-money');
    const grid = q('#money .metric-grid');
    if (!grid) return;
    if (!q('.raven-money-distinction')) {
      const strip = document.createElement('div');
      strip.className = 'raven-money-distinction';
      strip.innerHTML = '<span>Nilai transaksi</span><b>≠</b><span>Kerugian</span><b>≠</b><span>Susut nilai</span><b>≠</b><span>Kos pemulihan</span>';
      grid.before(strip);
    }
    qa(':scope > article', grid).forEach((card) => {
      wireCompact(card, { kind: 'money', keep: [q(':scope > strong', card), q(':scope > span', card), q(':scope > h3', card)], label: 'Apa maksud angka ini?', closeLabel: 'Tutup penerangan' });
    });
    const glossary = q('#money .metric-glossary');
    if (glossary) wireCompact(glossary, { kind: 'money-mechanism', keep: [q(':scope > h3', glossary)], label: 'Buka mekanisme UJSB', closeLabel: 'Tutup mekanisme UJSB' });
  };

  const enhanceTimelineReader = () => {
    if (!isTimelinePage) return;
    document.body.classList.add('raven-reader-timeline');
    const section = q('#timeline');
    if (!section) return;
    const heads = qa(':scope > .subhead', section);
    if (heads.length && !q('.raven-timeline-phase-nav', section)) {
      const nav = document.createElement('nav');
      nav.className = 'raven-timeline-phase-nav';
      nav.setAttribute('aria-label', 'Pilih fasa kronologi');
      heads.forEach((h, i) => {
        h.id ||= `timeline-phase-${String.fromCharCode(97 + i)}`;
        const a = document.createElement('a');
        a.href = `#${h.id}`;
        a.innerHTML = `<span>${String.fromCharCode(65 + i)}</span><strong>${(h.textContent || '').replace(/^\s*[A-Z]\s*·\s*/,'').trim()}</strong>`;
        nav.append(a);
      });
      q(':scope > h2', section)?.insertAdjacentElement('afterend', nav);
    }
    qa(':scope > .history-line', section).forEach((line, phaseIndex) => {
      qa(':scope > article', line).forEach((item, index) => {
        item.id ||= `timeline-${String.fromCharCode(97 + phaseIndex)}-${String(index + 1).padStart(2, '0')}`;
        wireCompact(item, { kind: 'timeline', keep: [q(':scope > time', item), q(':scope > h3', item)], label: 'Kenapa ini penting?', closeLabel: 'Tutup penerangan' });
      });
    });
  };
'''

css_block = r'''

/* RAVEN READER V1.3 — section-page scan architecture */
.raven-reader-card-toggle,
.raven-source-room-toggle { display:none; }

.raven-question-rail,
.raven-news-desk,
.raven-status-first-note,
.raven-money-distinction,
.raven-timeline-phase-nav {
  margin-block: 1.2rem 1.7rem;
}

.raven-question-rail {
  display:grid;
  grid-template-columns:repeat(2,minmax(0,1fr));
  gap:.65rem;
  padding:1rem;
  border:1px solid #d7d2c8;
  background:#f8f6f0;
}
.raven-question-rail > p { grid-column:1/-1; margin:0 0 .15rem; color:#424a50; }
.raven-question-rail > a {
  display:grid;
  grid-template-columns:auto 1fr;
  gap:.7rem;
  align-items:start;
  min-height:54px;
  padding:.75rem;
  border-top:1px solid #c9c5bc;
  color:#11171d;
  text-decoration:none;
}
.raven-question-rail > a span,
.raven-timeline-phase-nav a span {
  color:#087f98;
  font:900 .7rem/1.2 var(--sans);
  letter-spacing:.08em;
}
.raven-question-rail > a strong { font:800 .9rem/1.3 var(--sans); }

.raven-news-desk {
  display:grid;
  grid-template-columns:repeat(3,minmax(0,1fr));
  border-block:1px solid #c9c5bc;
}
.raven-news-desk > div { padding:1rem; border-right:1px solid #d8d2c7; }
.raven-news-desk > div:last-child { border-right:0; }
.raven-news-desk strong { display:block; color:#11171d; font:900 1.45rem/1 var(--sans); }
.raven-news-desk span { display:block; margin-top:.35rem; color:#5a6167; font:750 .78rem/1.3 var(--sans); }

.raven-status-first-note {
  display:flex;
  gap:.7rem 1rem;
  align-items:baseline;
  flex-wrap:wrap;
  padding:.9rem 1rem;
  border-left:4px solid #087f98;
  background:#eef8fa;
  color:#18333a;
}
.raven-status-first-note strong { font:900 .82rem/1.2 var(--sans); text-transform:uppercase; letter-spacing:.05em; }
.raven-status-first-note span { font:700 .84rem/1.45 var(--sans); }

.raven-money-distinction {
  display:flex;
  flex-wrap:wrap;
  align-items:center;
  justify-content:center;
  gap:.55rem;
  padding:1rem;
  border-block:1px solid #c9c5bc;
  background:#fbfaf6;
  color:#172027;
  font:850 .82rem/1.2 var(--sans);
}
.raven-money-distinction b { color:#a46500; font-size:1.1rem; }

.raven-timeline-phase-nav {
  display:grid;
  grid-template-columns:repeat(2,minmax(0,1fr));
  gap:.7rem;
}
.raven-timeline-phase-nav a {
  display:grid;
  grid-template-columns:auto 1fr;
  gap:.7rem;
  min-height:58px;
  align-items:center;
  padding:.85rem 1rem;
  border:1px solid #c9c5bc;
  background:#fbfaf6;
  color:#11171d;
  text-decoration:none;
}
.raven-timeline-phase-nav a strong { font:850 .9rem/1.25 var(--sans); }

@media (max-width:720px) {
  .raven-reader-compact.raven-reader-card-collapsed > :not(.raven-reader-keep) {
    display:none !important;
  }

  .raven-reader-card-toggle,
  .raven-source-room-toggle {
    display:flex;
    width:100%;
    min-height:46px;
    align-items:center;
    justify-content:space-between;
    gap:1rem;
    margin:.75rem 0 0;
    padding:.72rem .85rem;
    border:1px solid #a8cfd7;
    border-radius:.45rem;
    background:#eef8fa;
    color:#0b4653;
    font:850 .82rem/1.2 var(--sans);
    text-align:left;
    cursor:pointer;
  }
  .raven-reader-card-toggle b,
  .raven-source-room-toggle b { font:900 1.15rem/1 var(--sans); }
  .raven-reader-card-toggle:focus-visible,
  .raven-source-room-toggle:focus-visible {
    outline:3px solid rgba(8,127,152,.25);
    outline-offset:2px;
  }

  .raven-reader-compact:not(.raven-reader-card-collapsed) > .raven-reader-card-toggle { margin-bottom:.65rem; }

  .raven-reader-source-room.raven-reader-source-collapsed
    > :not(.section-marker):not(h2):not(.raven-source-room-toggle) {
    display:none !important;
  }
  .raven-reader-source-room { scroll-margin-top:5.5rem; }

  .raven-question-rail { grid-template-columns:1fr; padding:.85rem; }
  .raven-question-rail > a { min-height:48px; }

  .raven-news-desk { grid-template-columns:1fr; }
  .raven-news-desk > div {
    display:grid;
    grid-template-columns:3rem 1fr;
    align-items:center;
    gap:.75rem;
    padding:.7rem .8rem;
    border-right:0;
    border-bottom:1px solid #d8d2c7;
  }
  .raven-news-desk > div:last-child { border-bottom:0; }
  .raven-news-desk span { margin:0; }

  body.raven-reader-newsroom .timeline-item > div.raven-reader-compact { padding-bottom:.85rem; }
  body.raven-reader-newsroom .timeline-item > div.raven-reader-card-collapsed > p,
  body.raven-reader-newsroom .timeline-item > div.raven-reader-card-collapsed > a,
  body.raven-reader-newsroom .timeline-item > div.raven-reader-card-collapsed > br {
    display:none !important;
  }

  body.raven-reader-people .person-card,
  body.raven-reader-money .metric-grid > article,
  body.raven-reader-political .control-grid > article {
    padding-block:1rem !important;
  }

  .raven-money-distinction {
    justify-content:flex-start;
    gap:.4rem .55rem;
    padding:.85rem;
    font-size:.76rem;
  }

  .raven-timeline-phase-nav { grid-template-columns:1fr; }
  body.raven-reader-timeline .history-line > article { padding-block:.85rem !important; }
  body.raven-reader-timeline .history-line > article time { margin-bottom:.25rem; }

  .raven-reader-compact:target {
    scroll-margin-top:5.5rem;
    outline:2px solid rgba(8,127,152,.28);
    outline-offset:4px;
  }
}
'''

js = JS.read_text(encoding='utf-8')
if JS_MARK not in js:
    needle = '  const boot = () => {'
    if needle not in js:
        raise RuntimeError('Funnel boot marker not found')
    js = js.replace(needle, js_block + '\n' + needle, 1)
    boot_old = "    enhanceCasefileProgressiveDisclosure();\n"
    boot_new = "    enhanceCasefileProgressiveDisclosure();\n    enhancePoliticalSocialReader();\n    enhanceNewsroomReader();\n    enhancePeopleReader();\n    enhanceMoneyReader();\n    enhanceTimelineReader();\n    enhanceSourceRoomDisclosure();\n    setTimeout(() => revealCompactHash(), 180);\n    addEventListener('hashchange', () => revealCompactHash({ scroll: true }));\n"
    if boot_old not in js:
        raise RuntimeError('Funnel boot call not found')
    js = js.replace(boot_old, boot_new, 1)
    JS.write_text(js, encoding='utf-8')

css = CSS.read_text(encoding='utf-8')
if CSS_MARK not in css:
    CSS.write_text(css.rstrip() + css_block + '\n', encoding='utf-8')

for path in (APPLY, APPLY_WF, FUNNEL_QA):
    text = path.read_text(encoding='utf-8')
    text = text.replace('1.2.0', '1.3.0')
    path.write_text(text, encoding='utf-8')

qa = FUNNEL_QA.read_text(encoding='utf-8')
qa = qa.replace("await page.waitForSelector('.raven-evidence-bridge',{timeout:15000});", "await page.waitForSelector('.raven-evidence-bridge',{state:'attached',timeout:15000});")
FUNNEL_QA.write_text(qa, encoding='utf-8')

apply_text = APPLY.read_text(encoding='utf-8').replace('RAVEN FUNNEL V1.2.0', 'RAVEN FUNNEL V1.3.0')
APPLY.write_text(apply_text, encoding='utf-8')
print('Raven Reader V1.3 migration prepared')
