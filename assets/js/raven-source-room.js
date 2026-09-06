(() => {
  if (window.__RAVEN_SOURCE_ROOM_V1_1_1__) return;
  window.__RAVEN_SOURCE_ROOM_V1_1_1__ = true;

  if (!document.querySelector('link[data-raven-source-room]')) {
    const sheet = document.createElement('link');
    sheet.rel = 'stylesheet';
    sheet.href = '/raventrace-my/assets/css/raven-source-room.css?v=1.0.0';
    sheet.dataset.ravenSourceRoom = 'true';
    document.head.appendChild(sheet);
  }

  const section = document.querySelector('#sources');
  if (!section) return;

  const q = (s, r = document) => r.querySelector(s);
  const qa = (s, r = document) => [...r.querySelectorAll(s)];
  const clean = (value = '') => value.replace(/\s+/g, ' ').trim();
  const lower = (value = '') => clean(value).toLocaleLowerCase('ms');

  const officialHosts = [
    'gov.my', 'islam.gov.my', 'mof.gov.my', 'parlimen.gov.my', 'kehakiman.gov.my',
    'sprm.gov.my', 'macc.gov.my', 'agc.gov.my', 'tabunghaji.gov.my', 'bnm.gov.my',
    'sc.com.my'
  ];

  const findEntries = () => qa('[id]', section).filter((node) => {
    if (!/^s\d+$/i.test(node.id)) return false;
    return Boolean(q('a[href^="http"]', node));
  });
  let entries = findEntries();
  if (!entries.length) return;

  const hostOf = (url) => {
    try { return new URL(url).hostname.replace(/^www\./, '').toLowerCase(); }
    catch { return ''; }
  };
  const isOfficialHost = (host) => officialHosts.some((domain) => host === domain || host.endsWith(`.${domain}`));

  const classify = (entry) => {
    const text = lower(entry.textContent);
    const href = q('a[href^="http"]', entry)?.href || '';
    const host = hostOf(href);
    const tags = new Set();

    if (isOfficialHost(host)) tags.add('primary');
    else tags.add('media');

    if (/mahkamah|court|sesyen|reman|pertuduhan|didakwa|pendakwaan|prosid|charge|plea/.test(text)) tags.add('court');
    if (/sprm|macc|pdrm|jsjk|polis|police|penguatkuasaan|siasatan|remand|reman/.test(text)) tags.add('enforcement');
    if (/analisis|analysis|komentar|commentary|pakar|expert|what you think|opinion|pandangan/.test(text)) tags.add('expert');
    if (/rci|royal commission|suruhanjaya siasatan diraja|hansard|parlimen|akta|kementerian|kerajaan|minister|menteri/.test(text) && isOfficialHost(host)) tags.add('government');

    const gradeNode = q('.source-grade, [data-grade]', entry);
    const firstSpan = q(':scope > span', entry);
    const gradeText = clean(gradeNode?.textContent || entry.getAttribute('data-grade') || firstSpan?.textContent || '');
    const gradeMatch = gradeText.match(/^([A-E]|X)$/i) || clean(entry.textContent).match(/\bGred\s*([A-E]|X)\b/i);
    const grade = gradeMatch ? gradeMatch[1].toUpperCase() : '';

    entry.dataset.ravenSourceEntry = 'true';
    entry.dataset.ravenSourceTags = [...tags].join(' ');
    entry.dataset.ravenSourceGrade = grade;
    entry.dataset.ravenSourceSearch = lower(`${entry.id} ${entry.textContent} ${href} ${host}`);
    return { tags, grade };
  };

  entries.forEach(classify);

  const tools = document.createElement('section');
  tools.className = 'raven-source-tools';
  tools.setAttribute('aria-label', 'Cari dan tapis Source Room');
  tools.innerHTML = `
    <div class="raven-source-tools-head">
      <div>
        <p class="eyebrow">Source navigator</p>
        <h3>Cari rekod tanpa membaca semua rujukan.</h3>
      </div>
      <p class="raven-source-count" aria-live="polite"></p>
    </div>
    <label class="raven-source-search">
      <span>Cari sumber</span>
      <input type="search" inputmode="search" autocomplete="off" placeholder="Contoh: S22, Al-Rawda, SPRM, UJSB, mahkamah">
    </label>
    <div class="raven-source-filter-row" aria-label="Tapis mengikut jenis sumber">
      <button type="button" data-source-filter="all" aria-pressed="true">Semua</button>
      <button type="button" data-source-filter="primary" aria-pressed="false">Primer / rasmi</button>
      <button type="button" data-source-filter="court" aria-pressed="false">Mahkamah</button>
      <button type="button" data-source-filter="enforcement" aria-pressed="false">Penguatkuasaan</button>
      <button type="button" data-source-filter="media" aria-pressed="false">Media</button>
      <button type="button" data-source-filter="expert" aria-pressed="false">Analisis</button>
    </div>
    <div class="raven-source-grade-row">
      <label>Gred
        <select data-source-grade>
          <option value="all">Semua gred</option>
          <option value="A">A</option><option value="B">B</option><option value="C">C</option>
          <option value="D">D</option><option value="E">E</option><option value="X">X</option>
        </select>
      </label>
      <button type="button" class="raven-source-clear">Reset</button>
    </div>
    <p class="raven-source-note">Tag jenis sumber membantu navigasi sahaja. Ia tidak menggantikan gred bukti A–X atau mengubah apa yang sesuatu sumber boleh buktikan.</p>
  `;

  const lead = q('.section-lead', section);
  const marker = q('.section-marker', section);
  if (lead) lead.insertAdjacentElement('afterend', tools);
  else if (marker) marker.insertAdjacentElement('afterend', tools);
  else section.prepend(tools);

  const searchInput = q('input[type="search"]', tools);
  const gradeSelect = q('[data-source-grade]', tools);
  const count = q('.raven-source-count', tools);
  const filterButtons = qa('[data-source-filter]', tools);
  const resetButton = q('.raven-source-clear', tools);
  let activeFilter = 'all';

  const apply = () => {
    const query = lower(searchInput.value);
    const grade = gradeSelect.value;
    let visible = 0;

    entries.forEach((entry) => {
      const tags = new Set((entry.dataset.ravenSourceTags || '').split(/\s+/).filter(Boolean));
      const matchesQuery = !query || (entry.dataset.ravenSourceSearch || '').includes(query);
      const matchesType = activeFilter === 'all' || tags.has(activeFilter);
      const matchesGrade = grade === 'all' || entry.dataset.ravenSourceGrade === grade;
      const show = matchesQuery && matchesType && matchesGrade;
      entry.hidden = !show;
      entry.classList.toggle('raven-source-match', show && Boolean(query));
      if (show) visible += 1;
    });

    count.textContent = `${visible} / ${entries.length} sumber dipaparkan`;
  };

  const reset = () => {
    activeFilter = 'all';
    searchInput.value = '';
    gradeSelect.value = 'all';
    filterButtons.forEach((button) => {
      const active = button.dataset.sourceFilter === 'all';
      button.setAttribute('aria-pressed', String(active));
    });
    apply();
  };

  filterButtons.forEach((button) => button.addEventListener('click', () => {
    activeFilter = button.dataset.sourceFilter;
    filterButtons.forEach((item) => item.setAttribute('aria-pressed', String(item === button)));
    apply();
  }));
  searchInput.addEventListener('input', apply);
  gradeSelect.addEventListener('change', apply);
  resetButton.addEventListener('click', reset);

  const revealHashTarget = () => {
    const id = decodeURIComponent(location.hash.replace(/^#/, ''));
    if (!/^s\d+$/i.test(id)) return;
    const target = document.getElementById(id);
    if (!target || !section.contains(target)) return;
    if (target.hidden) reset();
    target.classList.add('raven-source-focus');
    setTimeout(() => target.classList.remove('raven-source-focus'), 2400);
  };

  const refreshEntries = () => {
    const found = findEntries();
    if (found.length === entries.length && found.every((entry, index) => entry === entries[index])) return;
    found.forEach((entry) => { if (entry.dataset.ravenSourceEntry !== 'true') classify(entry); });
    entries = found;
    apply();
  };

  let refreshTimer = null;
  const sourceObserver = new MutationObserver((mutations) => {
    if (!mutations.some((mutation) => mutation.addedNodes.length || mutation.removedNodes.length)) return;
    clearTimeout(refreshTimer);
    refreshTimer = setTimeout(refreshEntries, 80);
  });
  sourceObserver.observe(section, { childList: true, subtree: true });

  window.addEventListener('hashchange', revealHashTarget);
  apply();
  revealHashTarget();
})();