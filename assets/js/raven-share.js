(() => {
  if (window.__RAVEN_SHARE_V2_2__) return;
  window.__RAVEN_SHARE_V2_2__ = true;

  const q = (s, r = document) => r.querySelector(s);
  const qa = (s, r = document) => [...r.querySelectorAll(s)];

  if (!q('link[data-raven-share]')) {
    const css = document.createElement('link');
    css.rel = 'stylesheet';
    css.href = '/raventrace-my/assets/css/raven-share.css?v=1.1.0';
    css.dataset.ravenShare = 'true';
    document.head.appendChild(css);
  }

  if (!q('script[data-raven-analytics]')) {
    const analytics = document.createElement('script');
    analytics.src = '/raventrace-my/assets/js/raven-analytics.js?v=1.0.0';
    analytics.defer = true;
    analytics.dataset.ravenAnalytics = 'true';
    document.head.appendChild(analytics);
  }

  if (!q('script[data-raven-publication]')) {
    const publication = document.createElement('script');
    publication.src = '/raventrace-my/assets/js/raven-publication.js?v=1.1.0';
    publication.defer = true;
    publication.dataset.ravenPublication = 'true';
    document.head.appendChild(publication);
  }

  const selectors = [
    '.update-card', '.timeline-item', '.trace-card', '.person-card', 'details.investment',
    '.narrative-card', '#governance .control-grid > article', '#money .metric-grid > article',
    '#tracks .control-grid > article', '#disputed-record .control-grid > article'
  ];

  const storyMap = {
    'home-2026-09-06-jamil-reman-checkpoint':'/raventrace-my/news/2026/09/06/jamil-khir-reman-checkpoint/',
    'news-2026-09-06-jamil-reman-checkpoint':'/raventrace-my/news/2026/09/06/jamil-khir-reman-checkpoint/',
    'home-2026-09-05-ketelusan-rtm':'/raventrace-my/news/2026/09/05/ketelusan-siasatan-tabung-haji/',
    'news-2026-09-05-ketelusan-rtm':'/raventrace-my/news/2026/09/05/ketelusan-siasatan-tabung-haji/',
    'home-2026-09-04-madinah-rashid':'/raventrace-my/news/2026/09/04/madinah-rashid-rekod-bercanggah/',
    'news-2026-09-04-madinah-rashid':'/raventrace-my/news/2026/09/04/madinah-rashid-rekod-bercanggah/',
    'home-2026-09-03-reformasi-rci':'/raventrace-my/news/2026/09/03/reformasi-tadbir-urus-tabung-haji/',
    'news-2026-09-03-reformasi-rci':'/raventrace-my/news/2026/09/03/reformasi-tadbir-urus-tabung-haji/',
    'news-2026-09-03-thp-bina-rm72000':'/raventrace-my/news/2026/09/03/thp-bina-rm72000/'
  };

  const cleanText = (value = '') => value.replace(/\s+/g, ' ').trim();
  const trimText = (value, max = 260) => {
    const text = cleanText(value);
    if (text.length <= max) return text;
    const cut = text.slice(0, max - 1);
    const lastSpace = cut.lastIndexOf(' ');
    return `${lastSpace > max - 35 ? cut.slice(0, lastSpace) : cut}…`;
  };
  const slugify = (value = '') => cleanText(value).toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 58) || 'item';

  const getTitle = (item) => cleanText(q('h3', item)?.textContent || q('h2', item)?.textContent || q('summary strong', item)?.textContent || q('strong', item)?.textContent || 'Kemas kini RAVEN-Trace');
  const getSummary = (item) => {
    const candidates = qa('p, dd', item).filter((node) => !node.closest('.raven-sharebar, figcaption') && !node.classList.contains('role') && !node.classList.contains('inline-sources') && cleanText(node.textContent).length >= 35);
    return trimText(candidates[0]?.textContent || 'Semak konteks, status bukti dan sumber dalam RAVEN-Trace.', 280);
  };
  const getStatus = (item) => { const status = q('.status', item); return status ? cleanText(status.textContent) : ''; };

  const isRavenUrl = (href = '') => href.includes('raven-trace.github.io') || href.startsWith('/raventrace-my/');
  const isShareService = (href = '') => /(?:wa\.me|whatsapp\.com|facebook\.com\/sharer|threads\.(?:net|com)\/intent|twitter\.com\/intent|x\.com\/intent)/i.test(href);
  const getSourceUrl = (item) => {
    const direct = qa('a[href]', item).filter((a) => !a.closest('.raven-sharebar')).map((a) => a.href).find((href) => /^https?:\/\//i.test(href) && !isRavenUrl(href) && !isShareService(href));
    if (direct) return direct;
    for (const ref of qa('a[href^="#s"]', item)) {
      if (ref.closest('.raven-sharebar')) continue;
      const row = q(ref.getAttribute('href'));
      const source = row ? q('a[href^="http"]', row) : null;
      if (source?.href && !isShareService(source.href)) return source.href;
    }
    return '';
  };

  const stableIdFor = (item, index) => {
    if (item.id) return item.id;
    const explicit = item.dataset.shareId;
    if (explicit) { item.id = explicit; return explicit; }
    const section = item.closest('section[id]')?.id || (location.pathname.includes('/news') ? 'news' : 'story');
    const date = q('time[datetime]', item)?.getAttribute('datetime') || '';
    const base = `${section}-${date ? `${date}-` : ''}${slugify(getTitle(item))}`;
    let id = base, n = 2;
    while (document.getElementById(id) && document.getElementById(id) !== item) id = `${base}-${n++}`;
    item.id = id || `raven-share-${index + 1}`;
    return item.id;
  };

  const canonicalBase = () => q('link[rel="canonical"]')?.href?.split('#')[0] || `${location.origin}${location.pathname}`;
  const storyUrlFor = (item) => storyMap[item.id] ? new URL(storyMap[item.id], location.origin).href : '';

  const payloadFor = (item) => {
    const title = getTitle(item), summary = getSummary(item), status = getStatus(item), source = getSourceUrl(item);
    const storyUrl = storyUrlFor(item);
    const url = storyUrl || `${canonicalBase()}#${encodeURIComponent(item.id)}`;
    const lines = [`RAVEN-Trace | ${title}`, summary];
    if (status) lines.push(`Status: ${status}`);
    if (source) lines.push(`Sumber asal: ${source}`);
    lines.push(`Baca konteks penuh: ${url}`);
    return { title, summary, status, source, url, storyUrl, text: lines.join('\n\n') };
  };

  const storyPagePayload = () => {
    const title = cleanText(q('.story-hero h1')?.textContent || document.title);
    const summary = trimText(q('.story-dek')?.textContent || q('meta[name="description"]')?.content || '', 300);
    const status = cleanText(q('.story-hero .status')?.textContent || '');
    const source = q('.story-source-list a[href^="http"]')?.href || '';
    const url = canonicalBase();
    const lines = [`RAVEN-Trace | ${title}`, summary];
    if (status) lines.push(`Status: ${status}`);
    if (source) lines.push(`Sumber asal: ${source}`);
    lines.push(`Baca artikel: ${url}`);
    return { title, summary, status, source, url, text: lines.join('\n\n') };
  };

  const tagUrl = (url, channel, content = '') => {
    if (window.RavenAnalytics?.tagUrl) return window.RavenAnalytics.tagUrl(url, channel, content);
    try {
      const tagged = new URL(url, location.origin);
      tagged.searchParams.set('utm_source', channel);
      tagged.searchParams.set('utm_medium', 'social');
      tagged.searchParams.set('utm_campaign', 'raven_publication');
      if (content) tagged.searchParams.set('utm_content', slugify(content));
      return tagged.href;
    } catch { return url; }
  };

  const channelPayload = (base, channel, content = '') => {
    const url = tagUrl(base.url, channel, content || base.title);
    return { ...base, url, text: base.text.replace(base.url, url) };
  };

  const track = (name, props = {}) => {
    try { window.RavenAnalytics?.track?.(name, props); } catch { /* analytics must never break sharing */ }
  };

  const icon = (name) => {
    if (name === 'share') return '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M18 16a3 3 0 0 0-2.4 1.2L8.9 13.8a3 3 0 0 0 0-3.6l6.7-3.4A3 3 0 1 0 15 5c0 .2 0 .4.1.6L8.4 9A3 3 0 1 0 8 15l7.1 3.6A3 3 0 1 0 18 16Z"/></svg>';
    if (name === 'copy') return '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M8 7V4h10v12h-3v3H5V7h3Zm2 0h5v7h1V6h-6v1Zm3 4H7v6h6v-6Z"/></svg>';
    if (name === 'wa') return '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 3a8.7 8.7 0 0 0-7.5 13.1L3 21l5-1.4A8.8 8.8 0 1 0 12 3Zm0 15.8a7 7 0 0 1-3.6-1l-.3-.2-3 .8.8-2.9-.2-.3A7 7 0 1 1 12 18.8Zm3.9-5.2c-.2-.1-1.3-.7-1.5-.7-.2-.1-.4-.1-.5.1l-.7.9c-.1.2-.3.2-.5.1-1.4-.7-2.4-1.4-3.3-2.9-.2-.3.2-.3.6-1.1.1-.2 0-.4 0-.5l-.7-1.6c-.2-.4-.4-.4-.5-.4h-.5c-.2 0-.5.1-.7.3-.2.2-.9.9-.9 2.2 0 1.3.9 2.5 1.1 2.7.1.2 1.8 2.8 4.5 3.9.6.3 1.1.4 1.5.5.6.2 1.2.2 1.7.1.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.1-1.2-.1-.1-.3-.2-.5-.3Z"/></svg>';
    return '';
  };

  const feedback = (bar, message) => {
    const node = q('.raven-share-feedback', bar);
    if (!node) return;
    node.textContent = message;
    clearTimeout(node._ravenTimer);
    node._ravenTimer = setTimeout(() => { node.textContent = ''; }, 2200);
  };

  const copyText = async (text) => {
    if (navigator.clipboard?.writeText) return navigator.clipboard.writeText(text);
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    textarea.remove();
  };

  const socialLink = (label, handler) => {
    const link = document.createElement('a');
    link.className = 'raven-share-link';
    link.href = '#';
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
    link.textContent = label;
    link.addEventListener('click', handler);
    return link;
  };

  const buildBar = (item) => {
    if (item.dataset.ravenShareReady === 'true') return;
    item.dataset.ravenShareReady = 'true';

    const bar = document.createElement('div');
    bar.className = 'raven-sharebar compact';
    bar.setAttribute('aria-label', 'Pilihan perkongsian');

    const share = document.createElement('button');
    share.type = 'button';
    share.className = 'raven-share-btn primary';
    share.innerHTML = `${icon('share')}<span>Kongsi</span>`;
    share.addEventListener('click', async (event) => {
      event.preventDefault(); event.stopPropagation();
      const base = payloadFor(item);
      const payload = channelPayload(base, 'share_sheet', item.id);
      const nativeText = [payload.summary];
      if (payload.status) nativeText.push(`Status: ${payload.status}`);
      if (payload.source) nativeText.push(`Sumber asal: ${payload.source}`);
      try {
        if (navigator.share) {
          track('share_click', { channel: 'share_sheet', item: item.id, url: payload.url });
          await navigator.share({ title: payload.title, text: nativeText.join('\n\n'), url: payload.url });
          feedback(bar, 'Share sheet dibuka');
        } else {
          await copyText(payload.text);
          track('share_click', { channel: 'copy_fallback', item: item.id, url: payload.url });
          feedback(bar, 'Ringkasan + link disalin');
        }
      } catch (error) {
        if (error?.name !== 'AbortError') feedback(bar, 'Tidak dapat dikongsi');
      }
    });

    const wa = socialLink('WhatsApp', (event) => {
      event.preventDefault(); event.stopPropagation();
      const payload = channelPayload(payloadFor(item), 'whatsapp', item.id);
      track('share_click', { channel: 'whatsapp', item: item.id, url: payload.url });
      window.open(`https://wa.me/?text=${encodeURIComponent(payload.text)}`, '_blank', 'noopener,noreferrer');
    });
    wa.innerHTML = `${icon('wa')}<span>WhatsApp</span>`;

    const facebook = socialLink('Facebook', (event) => {
      event.preventDefault(); event.stopPropagation();
      const payload = channelPayload(payloadFor(item), 'facebook', item.id);
      track('share_click', { channel: 'facebook', item: item.id, url: payload.url });
      window.open(`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(payload.url)}`, '_blank', 'noopener,noreferrer');
    });

    const threads = socialLink('Threads', (event) => {
      event.preventDefault(); event.stopPropagation();
      const payload = channelPayload(payloadFor(item), 'threads', item.id);
      track('share_click', { channel: 'threads', item: item.id, url: payload.url });
      const text = `${payload.title}\n\n${payload.summary}\n\n${payload.url}`;
      window.open(`https://www.threads.com/intent/post?text=${encodeURIComponent(text)}`, '_blank', 'noopener,noreferrer');
    });

    const copy = document.createElement('button');
    copy.type = 'button';
    copy.className = 'raven-share-btn';
    copy.innerHTML = `${icon('copy')}<span>Salin</span>`;
    copy.addEventListener('click', async (event) => {
      event.preventDefault(); event.stopPropagation();
      const payload = channelPayload(payloadFor(item), 'copy', item.id);
      try {
        await copyText(payload.text);
        track('share_click', { channel: 'copy', item: item.id, url: payload.url });
        feedback(bar, 'Ringkasan + link disalin');
      } catch { feedback(bar, 'Salin gagal'); }
    });

    bar.append(share, wa, facebook, threads, copy);

    const storyUrl = storyUrlFor(item);
    if (storyUrl) {
      const story = document.createElement('a');
      story.className = 'raven-share-link';
      story.href = storyUrl;
      story.textContent = 'Artikel';
      story.addEventListener('click', (event) => { event.stopPropagation(); track('article_open', { item: item.id, url: story.href }); });
      bar.appendChild(story);
    }

    const source = getSourceUrl(item);
    if (source) {
      const sourceLink = document.createElement('a');
      sourceLink.className = 'raven-share-link';
      sourceLink.href = source;
      sourceLink.target = '_blank';
      sourceLink.rel = 'noopener noreferrer';
      sourceLink.textContent = 'Sumber';
      sourceLink.addEventListener('click', (event) => { event.stopPropagation(); track('source_click', { item: item.id, url: source }); });
      bar.appendChild(sourceLink);
    }

    const status = document.createElement('span');
    status.className = 'raven-share-feedback';
    status.setAttribute('aria-live', 'polite');
    bar.appendChild(status);

    if (item.matches('details.investment')) {
      const body = q('.investment-body', item);
      if (body) body.appendChild(bar); else item.appendChild(bar);
    } else if (item.matches('.timeline-item')) {
      const content = item.children[1];
      if (content) content.appendChild(bar); else item.appendChild(bar);
    } else item.appendChild(bar);
  };

  const buildStoryBar = () => {
    if (!document.body.classList.contains('story-page') || q('.story-actions .raven-story-sharebar')) return;
    const actions = q('.story-actions');
    if (!actions) return;

    const bar = document.createElement('div');
    bar.className = 'raven-sharebar raven-story-sharebar';
    bar.setAttribute('aria-label', 'Kongsi artikel ini');
    const storyId = location.pathname.split('/').filter(Boolean).slice(-1)[0] || 'story';

    const wa = socialLink('WhatsApp', (event) => {
      event.preventDefault();
      const payload = channelPayload(storyPagePayload(), 'whatsapp', storyId);
      track('share_click', { channel: 'whatsapp', item: storyId, url: payload.url });
      window.open(`https://wa.me/?text=${encodeURIComponent(payload.text)}`, '_blank', 'noopener,noreferrer');
    });
    wa.innerHTML = `${icon('wa')}<span>WhatsApp</span>`;

    const facebook = socialLink('Facebook', (event) => {
      event.preventDefault();
      const payload = channelPayload(storyPagePayload(), 'facebook', storyId);
      track('share_click', { channel: 'facebook', item: storyId, url: payload.url });
      window.open(`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(payload.url)}`, '_blank', 'noopener,noreferrer');
    });

    const threads = socialLink('Threads', (event) => {
      event.preventDefault();
      const payload = channelPayload(storyPagePayload(), 'threads', storyId);
      track('share_click', { channel: 'threads', item: storyId, url: payload.url });
      const text = `${payload.title}\n\n${payload.summary}\n\n${payload.url}`;
      window.open(`https://www.threads.com/intent/post?text=${encodeURIComponent(text)}`, '_blank', 'noopener,noreferrer');
    });

    const copy = document.createElement('button');
    copy.type = 'button';
    copy.className = 'raven-share-btn';
    copy.innerHTML = `${icon('copy')}<span>Salin ringkasan</span>`;
    copy.addEventListener('click', async () => {
      const payload = channelPayload(storyPagePayload(), 'copy', storyId);
      try {
        await copyText(payload.text);
        track('share_click', { channel: 'copy', item: storyId, url: payload.url });
        feedback(bar, 'Ringkasan + link disalin');
      } catch { feedback(bar, 'Salin gagal'); }
    });

    bar.append(wa, facebook, threads, copy);

    const source = storyPagePayload().source;
    if (source) {
      const sourceLink = document.createElement('a');
      sourceLink.className = 'raven-share-link';
      sourceLink.href = source;
      sourceLink.target = '_blank';
      sourceLink.rel = 'noopener noreferrer';
      sourceLink.textContent = 'Sumber asal';
      sourceLink.addEventListener('click', () => track('source_click', { item: storyId, url: source }));
      bar.appendChild(sourceLink);
    }

    const status = document.createElement('span');
    status.className = 'raven-share-feedback';
    status.setAttribute('aria-live', 'polite');
    bar.appendChild(status);
    actions.appendChild(bar);
  };

  const decorateAll = () => {
    const seen = new Set();
    selectors.forEach((selector) => qa(selector).forEach((item, index) => {
      if (seen.has(item)) return;
      seen.add(item);
      stableIdFor(item, index);
      buildBar(item);
    }));
    buildStoryBar();

    const hash = decodeURIComponent(location.hash.replace(/^#/, ''));
    if (hash) {
      const target = document.getElementById(hash);
      if (target) {
        if (target.matches('details')) target.open = true;
        target.classList.add('raven-share-target');
        setTimeout(() => target.scrollIntoView({ behavior: 'smooth', block: 'start' }), 80);
      }
    }
  };

  let mutationTimer = null;
  const observer = new MutationObserver((mutations) => {
    if (!mutations.some((m) => m.addedNodes.length)) return;
    clearTimeout(mutationTimer);
    mutationTimer = setTimeout(decorateAll, 80);
  });

  decorateAll();
  const root = q('main') || document.body;
  if (root) observer.observe(root, { childList: true, subtree: true });
})();
