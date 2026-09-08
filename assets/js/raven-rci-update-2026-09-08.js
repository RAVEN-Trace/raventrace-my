(() => {
  if (window.__RAVEN_RCI_UPDATE_2026_09_08__) return;
  window.__RAVEN_RCI_UPDATE_2026_09_08__ = true;

  const q = (s, r = document) => r.querySelector(s);
  const qa = (s, r = document) => [...r.querySelectorAll(s)];
  const path = location.pathname;
  const isHome = path === '/raventrace-my/' || path.endsWith('/raventrace-my/index.html') || path === '/';
  const isNewsroom = path === '/raventrace-my/news/' || path.endsWith('/raventrace-my/news/index.html');
  const isCase = path.includes('/raventrace-my/investigations/rci-tabung-haji');
  const storyUrl = '/raventrace-my/news/2026/09/08/jamil-khir-dilepaskan-jaminan-sprm/';
  const bernama = 'https://www.bernama.com/en/region/news.php?id=2604573';

  const setText = (selector, text) => { const el = q(selector); if (el) el.textContent = text; };
  const replacePhrase = (root, from, to) => {
    if (!root) return;
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach((node) => { if (node.nodeValue.includes(from)) node.nodeValue = node.nodeValue.replaceAll(from, to); });
  };

  const makeStatusCard = (kind) => {
    const article = document.createElement('article');
    article.className = kind === 'timeline' ? 'timeline-item' : 'update-card lead-update';
    article.id = kind === 'timeline' ? 'news-2026-09-08-jamil-release' : 'home-2026-09-08-jamil-release';
    if (kind === 'timeline') article.dataset.topic = 'enforcement';
    article.innerHTML = kind === 'timeline' ? `
      <time datetime="2026-09-08">08 SEP 2026</time><div>
        <div class="meta-row"><span class="status fact">FACT · STATUS BERUBAH</span><span class="source-grade">Gred B</span></div>
        <h3>Jamil Khir dilepaskan dengan jaminan SPRM selepas tempoh reman tamat</h3>
        <p>Ketua Pesuruhjaya SPRM mengesahkan beliau dilepaskan dengan jaminan SPRM pada 8 September. Ini menamatkan status reman, bukan siasatan. Setakat cut-off, belum ada pertuduhan baharu yang dapat disahkan.</p>
        <a href="${storyUrl}">Baca semakan status penuh →</a><br><a href="${bernama}" rel="noopener noreferrer">Sumber: Bernama →</a>
      </div>` : `
      <div class="update-index">00</div><div class="meta-row"><span class="status fact">FACT · STATUS BERUBAH</span><time datetime="2026-09-08">8 Sep 2026</time></div>
      <h3>Jamil Khir dilepaskan dengan jaminan SPRM selepas tempoh reman tamat.</h3>
      <p>Pembebasan selepas reman tidak bermaksud NFA atau kes selesai. Status semasa: dilepaskan dengan jaminan SPRM · siasatan berterusan · belum didakwa setakat cut-off.</p>
      <a href="${storyUrl}">Apa sebenarnya status Jamil sekarang? →</a><br><a href="${bernama}" rel="noopener noreferrer">Sumber: Bernama →</a>`;
    return article;
  };

  if (isHome) {
    setText('.utility-bar .utility-inner > span', '8 September 2026 · malam MYT');
    setText('.front-lead .date-chip', 'Maklumat disemak hingga · 8 Sep 2026 · malam MYT');
    setText('.front-lead .case-id', 'CASEFILE / RCI-TH-2026 · v19');
    const eyebrow = q('#latest .section-head .eyebrow');
    if (eyebrow) eyebrow.textContent = 'Kemas kini bukti · 8 September 2026';
    const grid = q('#latest .update-grid');
    if (grid && !q('#home-2026-09-08-jamil-release')) grid.prepend(makeStatusCard('home'));
    const old = q('#home-2026-09-06-jamil-reman-checkpoint');
    if (old) {
      const status = q('.status', old); if (status) status.textContent = 'REKOD TERDAHULU · reman tamat 8 Sep';
      const p = q('p', old); if (p) p.textContent = 'Mahkamah sebelum ini menyambung reman hingga 8 September. Rekod itu kini telah diatasi oleh perkembangan 8 September: Jamil Khir dilepaskan dengan jaminan SPRM selepas tempoh reman tamat.';
    }
  }

  if (isNewsroom) {
    setText('.article-header .date-chip', 'Maklumat disemak hingga · 8 Sep 2026 · malam MYT');
    const timeline = q('.timeline');
    if (timeline && !q('#news-2026-09-08-jamil-release')) timeline.prepend(makeStatusCard('timeline'));
    const old = q('#news-2026-09-06-jamil-reman-checkpoint');
    if (old) {
      const status = q('.status', old); if (status) status.textContent = 'REKOD TERDAHULU · reman tamat';
      const p = q('p', old); if (p) p.textContent = 'Rekod 6 September: reman dilanjutkan hingga 8 September. Perkembangan 8 September kemudian mengesahkan beliau dilepaskan dengan jaminan SPRM selepas reman tamat.';
    }
  }

  if (isCase) {
    setText('.utility-bar .utility-inner > span', 'CASEFILE · RCI-TH-2026 · v19');
    setText('.case-hero .date-chip', 'Data cut-off · 8 Sep 2026 · malam MYT');
    const rev = q('.case-hero .source-grade'); if (rev) rev.textContent = 'Revisi laman · 8 Sep 2026 · v19';

    const updates = q('#updates .trace-stack');
    if (updates && !q('[data-sep8-release]')) {
      const card = document.createElement('article');
      card.className = 'trace-card';
      card.dataset.sep8Release = 'true';
      card.innerHTML = `<div class="trace-head"><span>JEJAK / D2</span><time datetime="2026-09-08">8 Sep 2026 · status proses</time></div><div class="meta-row"><span class="status fact">FACT · STATUS BERUBAH</span><span class="source-grade">Gred B</span></div><h3>Jamil Khir dilepaskan dengan jaminan SPRM selepas tempoh reman tamat.</h3><dl><div><dt>Apa diketahui?</dt><dd>Ketua Pesuruhjaya SPRM mengesahkan pembebasan dengan jaminan SPRM pada 8 September.</dd></div><div><dt>Apa maksudnya?</dt><dd>Status reman tamat. Siasatan kekal berjalan; release bukan NFA dan bukan bukti salah atau tidak salah.</dd></div><div><dt>Apa belum diketahui?</dt><dd>Tiada charge sheet atau pertuduhan baharu yang dapat disahkan setakat cut-off.</dd></div></dl><p class="inline-sources"><a href="${storyUrl}">Baca story →</a> <a href="${bernama}" rel="noopener noreferrer">Bernama →</a></p>`;
      updates.prepend(card);
    }

    const old = q('[data-sep6-update]');
    if (old) {
      const status = q('.status', old); if (status) status.textContent = 'REKOD TERDAHULU · reman tamat 8 Sep';
      const limit = [...qa('dd', old)].pop(); if (limit) limit.textContent = 'Perkembangan seterusnya pada 8 September mengesahkan beliau dilepaskan dengan jaminan SPRM selepas reman tamat.';
    }

    const evidence = q('.raven-evidence-boundary');
    if (evidence) {
      const unknown = qa('article', evidence).find((a) => q('b', a)?.textContent.trim() === 'UNKNOWN');
      if (unknown) q('p', unknown).textContent = 'Butiran empat NFA, hasil baki kertas siasatan dan sama ada laporan jangkaan pendakwaan 10/11/17 Sep akan disahkan secara rasmi masih belum diketahui. Status selepas reman Jamil kini diketahui: dilepaskan dengan jaminan SPRM.';
    }

    const changelog = q('.raven-change-log');
    if (changelog) {
      q('h3', changelog).textContent = 'What changed · v19';
      const items = qa('.raven-change-grid > div', changelog);
      if (items[0]) q('p', items[0]).textContent = 'Jamil Khir dilepaskan dengan jaminan SPRM pada 8 September selepas tempoh reman tamat.';
      if (items[1]) q('p', items[1]).textContent = 'Status proses kini: release on MACC bail · siasatan berterusan · belum didakwa setakat cut-off.';
      if (items[2]) q('p', items[2]).textContent = 'Laporan 7 September mengenai tarikh/sekysen pertuduhan Azeez, Azmi dan Jamil kekal CLAIM sehingga disahkan SPRM, AGC atau mahkamah.';
      if (items[3]) q('p', items[3]).textContent = 'Checkpoint seterusnya: sahkan atau gugurkan claim 10/11/17 September dan pantau perkembangan Al-Rawda serta 24 September bagi prosiding Adi Azuan.';
    }

    const briefing = q('#briefing');
    if (briefing && !q('.raven-narrative-watch')) {
      const box = document.createElement('aside');
      box.className = 'raven-evidence-boundary raven-narrative-watch';
      box.innerHTML = `<div class="raven-evidence-boundary-head"><h3>Narrative Watch · 8 Sep</h3><p>Sentimen awam bergerak lebih pantas daripada proses undang-undang. Empat framing utama perlu dipisahkan daripada bukti.</p></div><div class="raven-evidence-boundary-grid"><article><b>ACCOUNTABILITY</b><p>RCI kini dilihat melalui lensa “siapa akan dipertanggungjawabkan”, tetapi tindakan siasatan belum sama dengan liabiliti jenayah.</p></article><article><b>REFORM</b><p>19 daripada 25 syor dilaporkan selesai; enam masih berjalan. Cerita institusi tidak berhenti pada tangkapan.</p></article><article><b>PROCESS</b><p>Pertikaian Madinah–Rashid kekal DISPUTED tanpa transkrip penuh yang menyelesaikan percanggahan.</p></article><article><b>MANIPULATION RISK</b><p>“Release = kes selesai”, “RM13b dicuri”, “RM11.5b bailout baharu” dan “14 IP = 14 jenayah terbukti” ialah simplifikasi yang bukti tidak bawa.</p></article></div>`;
      const anchor = q('.raven-claim-record', briefing) || q('.brief-grid', briefing) || q('.bottom-line', briefing);
      if (anchor) anchor.insertAdjacentElement('afterend', box);
    }

    replacePhrase(document, 'v18', 'v19');
  }
})();