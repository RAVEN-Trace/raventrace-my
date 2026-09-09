(() => {
  const q = (s, r = document) => r.querySelector(s);
  const qa = (s, r = document) => [...r.querySelectorAll(s)];
  const path = location.pathname;

  const toggle = q('[data-nav-toggle]');
  const nav = q('[data-nav]');
  const close = () => { if (nav && toggle) { nav.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); toggle.textContent = 'Menu'; } };
  toggle?.addEventListener('click', () => {
    const open = nav?.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(Boolean(open)));
    toggle.textContent = open ? 'Tutup' : 'Menu';
  });
  document.addEventListener('keydown', (event) => { if (event.key === 'Escape') close(); });

  q('[data-section-share]')?.addEventListener('click', async (event) => {
    const button = event.currentTarget;
    const payload = { title: document.title, text: q('meta[name="description"]')?.content || '', url: q('link[rel="canonical"]')?.href || location.href };
    try {
      if (navigator.share) await navigator.share(payload);
      else { await navigator.clipboard.writeText(`${payload.text}\n\n${payload.url}`); button.textContent = 'Pautan disalin'; }
    } catch (error) { if (error.name !== 'AbortError') button.textContent = 'Salin gagal'; }
  });

  q('[data-expand-investments]')?.addEventListener('click', (event) => {
    const items = qa('details.investment');
    const open = !items.every((item) => item.open);
    items.forEach((item) => { item.open = open; });
    event.currentTarget.setAttribute('aria-expanded', String(open));
    event.currentTarget.textContent = open ? 'Tutup semua rekod' : 'Buka semua rekod';
  });

  // Canonical standalone-section state for release v20.
  // Latest verified public record included: PDRM/Bernama, 9 Sep 2026 18:29 MYT.
  qa('.section-cutoff').forEach((el) => { el.textContent = 'Data cut-off · 9 Sep 2026 · 18:29 MYT'; });
  document.documentElement.dataset.ravenCaseState = 'rci-th-v20-20260909-1829';

  const addSourceRow = (id, grade, href, title, note) => {
    const list = q('#sources .sources-grid');
    if (!list || q(`#${id}`)) return;
    const li = document.createElement('li');
    li.id = id;
    li.innerHTML = `<span>${grade}</span><a href="${href}" rel="noopener noreferrer">${title}</a><small>${note}</small>`;
    list.appendChild(li);
  };

  addSourceRow('s53','B','https://www.bernama.com/en/news.php?id=2604854','Abdul Azeez didakwa di Mahkamah Sesyen','Bernama · 9 Sep · pertuduhan SPRM');
  addSourceRow('s55','B','https://www.bernama.com/bm/news.php?id=2604822','Abdul Azeez + dua bekas pegawai kanan TH direman dalam siasatan hibah','Bernama · 9 Sep · PDRM · Seksyen 420');
  addSourceRow('s56','B','https://www.bernama.com/en/region/news.php?id=2605104','PDRM: lima individu ditahan dalam siasatan hibah dan AMLA','Bernama · 9 Sep · kenyataan Bukit Aman CCID');
  addSourceRow('s57','B','https://www.bernama.com/bm/news.php?id=2605101','Azmi Ahmad dijadual didakwa 10 September','Bernama · 9 Sep · semakan sistem mahkamah');

  const updatePerson = (nameNeedle, statusClass, statusText, bodyText, sourceIds = []) => {
    const card = qa('.person-card').find((item) => q('h3', item)?.textContent.includes(nameNeedle));
    if (!card) return;
    const status = q(':scope > div .status', card);
    if (status) { status.className = `status ${statusClass}`; status.textContent = statusText; }
    const body = qa(':scope > p', card).find((p) => !p.classList.contains('role'));
    if (body) body.textContent = bodyText;
    sourceIds.forEach((id) => {
      if (qa('a[href^="#s"]', card).some((a) => a.getAttribute('href') === `#${id}`)) return;
      const a = document.createElement('a'); a.href = `#${id}`; a.textContent = id.toUpperCase(); card.append(' ', a);
    });
  };

  if (path.includes('/people/')) {
    updatePerson(
      'Abdul Azeez',
      'process',
      'Didakwa SPRM · direman PDRM · belum sabit · 9 Sep',
      'Pada 9 September, Abdul Azeez didakwa di Mahkamah Sesyen Kuala Lumpur di bawah Seksyen 23(1) Akta SPRM 2009 dan mengaku tidak bersalah. Pada hari sama, dalam trek berasingan, beliau bersama dua bekas pegawai kanan TH direman dua hari bagi membantu siasatan PDRM di bawah Seksyen 420 Kanun Keseksaan berkaitan pemberian hibah TH. Pertuduhan SPRM dan reman PDRM ialah dua proses berasingan; kedua-duanya bukan sabitan.',
      ['s53','s55']
    );
    updatePerson(
      'Jamil Khir',
      'fact',
      'Dilepaskan dengan jaminan SPRM · 8 Sep',
      'Selepas tempoh reman berakhir pada 8 September, Jamil Khir dilepaskan dengan jaminan SPRM. Pelepasan bukan NFA, acquittal atau penentuan bahawa siasatan telah tamat. Laporan jangkaan pendakwaan bagi beliau kekal belum disahkan pada cut-off ini.',
      ['s49']
    );
    updatePerson(
      'Azmi Ahmad',
      'process',
      'Prosiding dijadualkan · 10 Sep · 9 pagi',
      'Bernama melaporkan berdasarkan semakan sistem mahkamah bahawa Azmi Ahmad dijadual didakwa di Mahkamah Sesyen Jenayah 14 Kuala Lumpur pada 10 September, 9 pagi. Sehingga pertuduhan benar-benar dibaca dan direkodkan, RAVEN-Trace mengekalkan status ini sebagai prosiding dijadualkan, bukan pertuduhan yang telah berlaku dan bukan sabitan.',
      ['s57']
    );
  }

  if (path.includes('/timeline/')) {
    const lines = qa('.history-line');
    const enforcement = lines[lines.length - 1];
    if (enforcement && !q('[data-v20-timeline]', enforcement)) {
      const wrap = document.createElement('div');
      wrap.dataset.v20Timeline = 'true';
      wrap.innerHTML = `
        <article><time>8 Sep</time><h3>Jamil Khir dilepaskan</h3><p>Dilepaskan dengan jaminan SPRM selepas tamat reman. Pelepasan bukan NFA atau keputusan kes.</p></article>
        <article><time>9 Sep · SPRM</time><h3>Abdul Azeez didakwa</h3><p>Didakwa di bawah Seksyen 23(1) Akta SPRM 2009 dan mengaku tidak bersalah. Pertuduhan bukan sabitan.</p></article>
        <article><time>9 Sep · PDRM</time><h3>Trek hibah bergerak berasingan</h3><p>Abdul Azeez dan dua bekas pegawai kanan TH direman dua hari bagi membantu siasatan di bawah Seksyen 420 Kanun Keseksaan berkaitan pemberian hibah TH. PDRM kemudian menyatakan lima individu ditahan dalam trek hibah dan AMLA yang berasingan.</p></article>
        <article><time>10 Sep · checkpoint</time><h3>Azmi Ahmad dijadual didakwa</h3><p>Semakan sistem mahkamah yang dilaporkan Bernama menetapkan prosiding pada 9 pagi di Mahkamah Sesyen Jenayah 14 Kuala Lumpur. Status kekal dijadualkan sehingga pertuduhan dibaca.</p></article>`;
      [...wrap.children].forEach((node) => enforcement.appendChild(node));
    }
  }

  if (path.includes('/tracks/')) {
    const section = q('#tracks');
    const heading = q('h2', section);
    if (heading) heading.textContent = 'Beberapa dataset dan trek yang mesti dibaca berasingan.';
    const lead = q('.section-lead', section);
    if (lead) lead.textContent = 'SPRM, PDRM, prosiding mahkamah dan dataset isu RCI bergerak pada asas undang-undang serta tujuan yang berbeza. Nombor atau nama yang bertindih tidak menjadikan semua rekod satu kes yang sama.';
    const grid = q('.control-grid', section);
    if (grid && !q('[data-pdrm-hibah-track]', grid)) {
      const card = document.createElement('article');
      card.dataset.pdrmHibahTrack = 'true';
      card.innerHTML = '<h3>Phase C · PDRM · hibah + AMLA</h3><p>Pada 9 September, PDRM memperoleh reman dua hari terhadap Abdul Azeez dan dua bekas pegawai kanan TH untuk siasatan di bawah Seksyen 420 Kanun Keseksaan berkaitan hibah. Bukit Aman kemudian menyatakan lima individu ditahan: tiga bagi trek hibah dan dua lagi bagi siasatan berasingan di bawah Seksyen 4(1) AMLATFPUAA. Ini bukan pertuduhan tambahan terhadap semua individu dan tidak boleh dicampur dengan pertuduhan SPRM terhadap Abdul Azeez.</p><a href="#s55">S55</a> <a href="#s56">S56</a>';
      grid.appendChild(card);
    }
  }

  if (path.includes('/updates/')) {
    const stack = q('#updates .trace-stack');
    if (stack && !q('[data-azmi-checkpoint]', stack)) {
      const azmi = document.createElement('article');
      azmi.className = 'trace-card'; azmi.dataset.azmiCheckpoint = 'true';
      azmi.innerHTML = '<div class="trace-head"><span>CHECKPOINT / 10 SEP</span><time datetime="2026-09-10T09:00">10 Sep 2026 · 9:00 pagi</time></div><div class="meta-row"><span class="status process">DIJADUALKAN · BELUM BERLAKU</span><span class="source-grade">Gred B</span></div><h3>Azmi Ahmad dijadual didakwa di Mahkamah Sesyen Kuala Lumpur.</h3><dl><div><dt>Apa diketahui?</dt><dd>Bernama melaporkan semakan sistem mahkamah menetapkan prosiding pada 10 September, 9 pagi.</dd></div><div><dt>Status tepat</dt><dd>Prosiding dijadualkan. RAVEN-Trace belum menganggap beliau telah didakwa sehingga pertuduhan benar-benar dibaca dan direkodkan.</dd></div><div><dt>Had</dt><dd>Jadual mahkamah boleh berubah dan pertuduhan bukan sabitan.</dd></div></dl><p class="inline-sources"><a href="#s57">S57</a></p>';
      stack.prepend(azmi);
    }
    if (stack && !q('[data-pdrm-hibah-update]', stack)) {
      const card = document.createElement('article');
      card.className = 'trace-card';
      card.dataset.pdrmHibahUpdate = 'true';
      card.innerHTML = '<div class="trace-head"><span>JEJAK / PDRM</span><time datetime="2026-09-09">9 Sep 2026 · PDRM / Mahkamah Sesyen KL</time></div><div class="meta-row"><span class="status process">REMAN · SIASATAN BERASINGAN</span><span class="source-grade">Gred B</span></div><h3>Abdul Azeez dan dua bekas pegawai kanan TH direman dalam siasatan hibah.</h3><dl><div><dt>Apa diketahui?</dt><dd>Reman dua hari dibenarkan bagi membantu siasatan PDRM di bawah Seksyen 420 Kanun Keseksaan berkaitan pemberian hibah TH.</dd></div><div><dt>Kenapa mesti dipisah?</dt><dd>Ini trek PDRM yang berasingan daripada pertuduhan SPRM Seksyen 23(1) terhadap Abdul Azeez pada hari sama.</dd></div><div><dt>Had</dt><dd>Reman ialah alat siasatan, bukan pertuduhan atau sabitan. PDRM juga melaporkan dua individu lain direman dalam siasatan AMLA yang berasingan.</dd></div></dl><p class="inline-sources"><a href="#s55">S55</a> <a href="#s56">S56</a></p>';
      stack.prepend(card);
    }
  }
})();
