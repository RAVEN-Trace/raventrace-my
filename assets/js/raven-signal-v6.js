(() => {
  'use strict';
  if (window.__RAVEN_SIGNAL_V6__) return;
  window.__RAVEN_SIGNAL_V6__ = true;

  const q = (s, r = document) => r.querySelector(s);
  const qa = (s, r = document) => [...r.querySelectorAll(s)];
  const path = location.pathname;
  const ROOT = '/raventrace-my/';
  const RCI = `${ROOT}investigations/rci-tabung-haji/`;
  const isRoot = path === ROOT || path === `${ROOT}index.html`;
  const isRci = path.startsWith(RCI);
  const isRciRoot = path === RCI || path === `${RCI}index.html`;
  const isNarrative = path.startsWith(`${RCI}narratives/`);
  const isMoney = path.startsWith(`${RCI}money/`);
  const isPeople = path.startsWith(`${RCI}people/`);
  const isTimeline = path.startsWith(`${RCI}timeline/`);
  const isSources = path.startsWith(`${RCI}sources/`);
  const isNewsHub = path === `${ROOT}news/` || path === `${ROOT}news/index.html`;
  const supportMap = new Map([
    [`${ROOT}methodology/`, '<strong>Senang cakap:</strong> Raven tak minta kau percaya kami. Kami tunjuk macam mana satu claim diperiksa, mana sumber datang, dan bila kami perlu cakap “belum tahu”.'],
    [`${ROOT}about/`, '<strong>Kenapa Raven wujud?</strong> Internet penuh cerita. Masalahnya, fakta betul pun boleh disusun sampai orang faham benda yang salah. Raven dibina untuk part itu.'],
    [`${ROOT}corrections/`, '<strong>Raven boleh silap.</strong> Kalau bukti berubah, Raven berubah — dan perubahan itu kekal boleh dilihat.'],
    [`${ROOT}tips/`, '<strong>Ada benda yang Raven patut tengok?</strong> Hantar claim viral, dokumen atau perkara yang rasa tak kena. Jangan hantar password, nombor IC penuh atau maklumat yang boleh bahayakan kau.']
  ]);
  const supportPath = [...supportMap.keys()].find((p) => path === p || path === `${p}index.html`);

  document.body.classList.add('raven-signal');
  if (isRoot) document.body.classList.add('raven-signal-home');
  if (isRci) document.body.classList.add('raven-signal-case');
  if (isNarrative) document.body.classList.add('raven-signal-narrative');
  if (isMoney) document.body.classList.add('raven-signal-money');
  if (isPeople) document.body.classList.add('raven-signal-people');
  if (isTimeline) document.body.classList.add('raven-signal-timeline');
  if (isSources) document.body.classList.add('raven-signal-sources');
  if (isNewsHub) document.body.classList.add('raven-signal-news');
  if (supportPath) document.body.classList.add('raven-signal-support');

  const insertAfter = (target, node) => {
    if (target?.parentNode) target.parentNode.insertBefore(node, target.nextSibling);
  };

  const make = (tag, cls, html = '') => {
    const el = document.createElement(tag);
    if (cls) el.className = cls;
    if (html) el.innerHTML = html;
    return el;
  };

  /* ---------------------------------------------------------
     HOME: Truth Desk
     --------------------------------------------------------- */
  const upgradeHome = () => {
    if (!isRoot) return;
    let hero = q('.v5-truth-intro');
    if (!hero) {
      const main = q('#main');
      if (!main) return;
      hero = make('section', 'v5-truth-intro signal-home-hero', `
        <div class="container">
          <p class="v5-kicker">Benda complicated. Kita pecahkan.</p>
          <h1>Cerita boleh dibentuk. Bukti tak boleh dipaksa.</h1>
          <p class="v5-dek">Raven pecahkan cerita kepada apa orang kata, apa rekod boleh sahkan, apa yang tak disebut dan apa yang masih belum tahu.</p>
          <p class="v5-case-now">Sekarang Raven tengah bedah: <strong>RCI Tabung Haji</strong></p>
          <div class="v5-paths">
            <a class="v5-path" href="${RCI}#briefing"><span class="v5-path-icon">01</span><span><strong>Faham kes</strong><small>Apa berlaku, kenapa orang kecoh, dan apa yang penting.</small></span></a>
            <a class="v5-path" href="${RCI}narratives/"><span class="v5-path-icon">02</span><span><strong>Check naratif</strong><small>Apa cerita yang dimainkan — dan apa rekod tunjuk.</small></span></a>
            <a class="v5-path" href="${RCI}#sources"><span class="v5-path-icon">03</span><span><strong>Tengok bukti</strong><small>Dokumen, sumber dan rekod yang boleh kau semak sendiri.</small></span></a>
          </div>
        </div>`);
      main.prepend(hero);
    } else {
      hero.classList.add('signal-home-hero');
      const kicker = q('.v5-kicker', hero);
      const title = q('h1', hero);
      const dek = q('.v5-dek', hero);
      const now = q('.v5-case-now', hero);
      if (kicker) kicker.textContent = 'Benda complicated. Kita pecahkan.';
      if (title) title.textContent = 'Cerita boleh dibentuk. Bukti tak boleh dipaksa.';
      if (dek) dek.textContent = 'Raven pecahkan cerita kepada apa orang kata, apa rekod boleh sahkan, apa yang tak disebut dan apa yang masih belum tahu.';
      if (now) now.innerHTML = 'Sekarang Raven tengah bedah: <strong>RCI Tabung Haji</strong>';
      const paths = qa('.v5-path', hero);
      const data = [
        ['01','Faham kes','Apa berlaku, kenapa orang kecoh, dan apa yang penting.',`${RCI}#briefing`],
        ['02','Check naratif','Apa cerita yang dimainkan — dan apa rekod tunjuk.',`${RCI}narratives/`],
        ['03','Tengok bukti','Dokumen, sumber dan rekod yang boleh kau semak sendiri.',`${RCI}#sources`]
      ];
      paths.slice(0,3).forEach((a, i) => {
        const [n,t,d,h] = data[i];
        a.href = h;
        const icon = q('.v5-path-icon', a); if (icon) icon.textContent = n;
        const strong = q('strong', a); if (strong) strong.textContent = t;
        const small = q('small', a); if (small) small.textContent = d;
      });
    }

    if (!q('.signal-live-strip', hero)) {
      const strip = make('div','signal-live-strip');
      const docketStats = qa('.front-docket .docket-stat').slice(0,3);
      const parts = docketStats.map((row) => {
        const n = q('strong', row)?.textContent?.trim();
        const label = q('span', row)?.textContent?.trim();
        return n && label ? `<span><strong>${n}</strong> ${label}</span>` : '';
      }).filter(Boolean);
      strip.innerHTML = parts.length ? parts.join('') : '<span><strong>Kes aktif</strong> RCI Tabung Haji</span><span>Audit naratif tersedia</span>';
      q('.container', hero)?.append(strip);
    }
  };

  /* ---------------------------------------------------------
     CASEFILE: four permanent lenses + Truth Map
     --------------------------------------------------------- */
  const upgradeCasefile = () => {
    if (!isRciRoot) return;
    const hero = q('.case-hero');
    if (hero && !q('.signal-case-lenses')) {
      const lenses = make('section','signal-case-lenses');
      lenses.setAttribute('aria-label','Empat cara baca CASEFILE');
      lenses.innerHTML = `
        <div class="signal-case-lenses-inner">
          <a class="signal-lens" href="#briefing"><span class="signal-lens-no">01</span><strong>Faham</strong><small>Apa benda sebenarnya berlaku?</small></a>
          <a class="signal-lens" href="${RCI}narratives/"><span class="signal-lens-no">02</span><strong>Naratif</strong><small>Apa cerita yang sedang dibentuk?</small></a>
          <a class="signal-lens" href="#sources"><span class="signal-lens-no">03</span><strong>Bukti</strong><small>Apa rekod boleh sahkan?</small></a>
          <a class="signal-lens" href="#updates"><span class="signal-lens-no">04</span><strong>Status</strong><small>Apa yang berubah sekarang?</small></a>
        </div>`;
      insertAfter(hero, lenses);
    }

    const reading = q('.reading-nav');
    if (reading && !q('.signal-truth-map')) {
      const map = make('section','signal-truth-map');
      map.innerHTML = `
        <div class="signal-map-head">
          <h2>Macam mana semua benda ni berkait?</h2>
          <p>RCI ialah titik mula. Lepas itu cerita bercabang kepada pelaburan, tadbir urus, individu, tindakan penguatkuasaan, mahkamah, naratif politik dan bukti. Tekan mana-mana bahagian untuk terus ke situ.</p>
        </div>
        <div class="signal-map-flow" aria-label="Peta hubungan kes RCI Tabung Haji">
          <a class="signal-map-node" href="#briefing"><span>01</span><strong>RCI & dapatan</strong></a>
          <a class="signal-map-node" href="#investments"><span>02</span><strong>14 pelaburan</strong></a>
          <a class="signal-map-node" href="#governance"><span>03</span><strong>Tadbir urus</strong></a>
          <a class="signal-map-node" href="#people"><span>04</span><strong>Individu</strong></a>
          <a class="signal-map-node" href="#updates"><span>05</span><strong>SPRM & mahkamah</strong></a>
          <a class="signal-map-node" href="${RCI}narratives/"><span>06</span><strong>Naratif</strong></a>
          <a class="signal-map-node" href="#sources"><span>07</span><strong>Sumber</strong></a>
        </div>`;
      insertAfter(reading, map);
    }
  };

  /* ---------------------------------------------------------
     Contextual plain-language terms on RCI pages
     --------------------------------------------------------- */
  const glossary = [
    ['Reman', 'Tahanan sementara untuk membantu siasatan. Ia bukan bukti seseorang bersalah.'],
    ['NFA', '“No Further Action” — fail itu ditutup tanpa tindakan lanjut setakat keputusan agensi pada masa tersebut.'],
    ['Impairment', 'Nilai aset diturunkan dalam akaun. Ia tak sama dengan wang dicuri.'],
    ['AMLA', 'Undang-undang berkaitan pengubahan wang haram dan hasil aktiviti haram. Siasatan di bawah AMLA bukan sabitan.'],
    ['UJSB', 'Urusharta Jamaah Sdn Bhd — entiti yang digunakan dalam pelan pemulihan aset Tabung Haji.'],
    ['RCI', 'Suruhanjaya Siasatan Diraja. Ia menyiasat dan membuat dapatan atau syor; ia bukan mahkamah yang mensabitkan orang.']
  ];

  const addPlainTerms = () => {
    if (!isRci || isNarrative) return;
    const bodyText = document.body.textContent || '';
    const found = glossary.filter(([term]) => new RegExp(`\\b${term.replace(/[.*+?^${}()|[\\]\\\\]/g,'\\$&')}\\b`,'i').test(bodyText)).slice(0,3);
    if (!found.length || q('.signal-explain-strip')) return;
    const strip = make('div','signal-explain-strip');
    strip.innerHTML = '<strong>Jumpa istilah pelik?</strong> Tekan istilah di bawah. Raven explain tanpa bahasa pejabat.';
    const terms = make('div','signal-explain-terms');
    const pop = make('div','signal-explain-pop');
    pop.setAttribute('aria-live','polite');
    found.forEach(([term, definition]) => {
      const b = make('button','signal-explain-term');
      b.type = 'button';
      b.textContent = `${term} · apa benda ni?`;
      b.addEventListener('click', () => { pop.innerHTML = `<strong>${term}:</strong> ${definition}`; });
      terms.append(b);
    });
    strip.append(terms,pop);
    const host = q('.section-intro .container') || q('.case-hero .container') || q('.section-content') || q('.case-content');
    host?.append(strip);
  };

  /* ---------------------------------------------------------
     Narrative Forensics: claim → record → gap → verdict
     --------------------------------------------------------- */
  const upgradeNarratives = () => {
    if (!isNarrative) return;
    qa('.narrative-v5-card').forEach((card) => {
      if (card.dataset.signalNarrative === 'true') return;
      const title = q(':scope > h3', card);
      const status = q(':scope > .narrative-status-row', card);
      const record = q(':scope > .narrative-v5-record', card);
      const verdict = q(':scope > .narrative-v5-verdict', card);
      const details = q(':scope > .narrative-v5-details', card);
      if (!title || !record || !verdict) return;

      card.dataset.signalNarrative = 'true';
      card.classList.add('signal-narrative-card');

      const split = make('div','signal-narrative-grid');
      const claim = make('div','signal-claim-zone');
      claim.append(make('span','signal-claim-label','Orang kata'));
      claim.append(title);
      if (status) claim.append(status);

      const recordZone = make('div','signal-record-zone');
      recordZone.append(make('span','signal-record-label','Apa rekod tunjuk'));
      recordZone.append(record);
      split.append(claim,recordZone);
      card.prepend(split);

      if (details) {
        const blocks = qa('.narrative-v5-detail-block', details);
        const omitted = blocks.find((b) => /cerita tak sebut|konteks/i.test(q('h4',b)?.textContent || ''));
        if (omitted) {
          const gap = make('div','signal-gap');
          gap.append(make('span','signal-gap-label','Jurang cerita'));
          const p = q('p', omitted);
          if (p) gap.append(p);
          omitted.remove();
          split.after(gap);
        }
      }

      const verdictZone = make('div','signal-verdict-zone');
      verdictZone.append(make('span','signal-verdict-label','Raven verdict'));
      verdictZone.append(verdict);
      const gap = q(':scope > .signal-gap', card);
      if (gap) insertAfter(gap, verdictZone); else insertAfter(split, verdictZone);
    });
  };

  /* ---------------------------------------------------------
     MONEY: make category differences visible
     --------------------------------------------------------- */
  const upgradeMoney = () => {
    if (!isMoney || q('.signal-money-clarifier')) return;
    const article = q('.section-content') || q('.case-content');
    const first = q('.case-section', article || document);
    if (!article || !first) return;
    const block = make('section','signal-money-clarifier');
    block.innerHTML = `
      <h2>Empat benda ni tak sama.</h2>
      <p>Bila nombor kewangan dicampur, cerita boleh nampak lebih mudah daripada realiti. Raven pisahkan kategori dulu sebelum buat kesimpulan.</p>
      <div class="signal-money-equation">
        <div class="signal-money-term"><strong>Rugi</strong><small>Nilai atau hasil jatuh.</small></div>
        <div class="signal-money-term"><strong>Impairment</strong><small>Nilai aset diturunkan dalam akaun.</small></div>
        <div class="signal-money-term"><strong>Jurang aset-liabiliti</strong><small>Aset dan tanggungan tak seimbang.</small></div>
        <div class="signal-money-term"><strong>Wang dicuri</strong><small>Perlukan bukti salah laku jenayah.</small></div>
      </div>`;
    article.insertBefore(block, first);
  };

  /* ---------------------------------------------------------
     PEOPLE: legal-state sequence
     --------------------------------------------------------- */
  const upgradePeople = () => {
    if (!isPeople || q('.signal-process-rail')) return;
    const article = q('.section-content') || q('.case-content');
    const first = q('.case-section', article || document);
    if (!article || !first) return;
    const rail = make('section','signal-process-rail');
    rail.innerHTML = `
      <strong>Jangan lompat terus ke “bersalah”.</strong>
      <div class="signal-process-flow">
        <div class="signal-process-step"><b>Disebut</b><small>Nama muncul dalam rekod.</small></div>
        <div class="signal-process-step"><b>Disiasat</b><small>Agensi periksa sesuatu.</small></div>
        <div class="signal-process-step"><b>Ditahan / direman</b><small>Proses siasatan, bukan sabitan.</small></div>
        <div class="signal-process-step"><b>Didakwa</b><small>Pertuduhan dibawa ke mahkamah.</small></div>
        <div class="signal-process-step"><b>Disabitkan</b><small>Mahkamah memutuskan bersalah.</small></div>
      </div>`;
    article.insertBefore(rail, first);
  };

  /* ---------------------------------------------------------
     NEWSROOM: change desk legend
     --------------------------------------------------------- */
  const upgradeNews = () => {
    if (!isNewsHub || q('.signal-change-key')) return;
    const timeline = q('.timeline') || q('.update-grid') || q('.news-list');
    if (!timeline) return;
    const key = make('div','signal-change-key');
    key.innerHTML = '<span><b>BARU</b> · fakta/status baharu</span><span><b>TAK BERUBAH</b> · checkpoint kekal</span><span><b>BELUM JELAS</b> · bukti belum cukup</span><span><b>NARATIF BARU</b> · framing baru muncul</span>';
    timeline.parentNode.insertBefore(key, timeline);
  };

  /* ---------------------------------------------------------
     SOURCES: explain source roles
     --------------------------------------------------------- */
  const upgradeSources = () => {
    if (!isSources || q('.signal-source-key')) return;
    const article = q('.section-content') || q('.case-content');
    const first = q('.case-section', article || document);
    if (!article || !first) return;
    const key = make('section','signal-source-key');
    key.innerHTML = `
      <div><strong>Primary records</strong><span>Mahkamah, Parlimen, agensi, laporan rasmi dan dokumen asal. Paling dekat dengan kejadian.</span></div>
      <div><strong>Reliable reporting</strong><span>Laporan media beratribusi yang membantu sahkan tarikh, kenyataan dan konteks.</span></div>
      <div><strong>Claims / leads</strong><span>Ucapan, posting, screenshot atau dakwaan. Berguna sebagai petunjuk — bukan automatik bukti.</span></div>`;
    article.insertBefore(key, first);
  };

  const upgradeSupport = () => {
    if (!supportPath || q('.signal-purpose-note')) return;
    const html = supportMap.get(supportPath);
    const intro = q('.article-header .container') || q('.section-intro .container') || q('main .container');
    if (!intro) return;
    const note = make('div','signal-purpose-note',html);
    intro.append(note);
  };

  const boot = () => {
    upgradeHome();
    upgradeCasefile();
    addPlainTerms();
    upgradeNarratives();
    upgradeMoney();
    upgradePeople();
    upgradeNews();
    upgradeSources();
    upgradeSupport();
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot, { once:true });
  else boot();
})();
