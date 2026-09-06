(() => {
  if (window.__RAVEN_ANALYTICS_V1__) return;
  window.__RAVEN_ANALYTICS_V1__ = true;

  const STORAGE_KEY = 'raven-attribution-v1';
  const CAMPAIGN = 'raven_publication';
  const DNT = navigator.doNotTrack === '1' || window.doNotTrack === '1';

  const clean = (value = '') => String(value || '').trim().slice(0, 180);
  const slug = (value = '') => clean(value).toLowerCase().replace(/[^a-z0-9]+/g, '_').replace(/^_+|_+$/g, '').slice(0, 80) || 'unknown';

  const classifyReferrer = (referrer = document.referrer) => {
    if (!referrer) return 'direct';
    try {
      const host = new URL(referrer).hostname.toLowerCase().replace(/^www\./, '');
      if (host.includes('facebook.com') || host.includes('fb.com') || host.includes('fb.me')) return 'facebook';
      if (host.includes('threads.net')) return 'threads';
      if (host.includes('whatsapp.com') || host.includes('wa.me')) return 'whatsapp';
      if (host.includes('google.')) return 'google';
      if (host.includes('bing.com')) return 'bing';
      if (host.includes('x.com') || host.includes('twitter.com')) return 'x';
      if (host.includes('raven-trace.github.io')) return 'internal';
      return host || 'other';
    } catch { return 'other'; }
  };

  const readStored = () => {
    try { return JSON.parse(sessionStorage.getItem(STORAGE_KEY) || 'null'); }
    catch { return null; }
  };

  const params = new URLSearchParams(location.search);
  const incoming = {
    source: clean(params.get('utm_source')),
    medium: clean(params.get('utm_medium')),
    campaign: clean(params.get('utm_campaign')),
    content: clean(params.get('utm_content')),
    referrer: classifyReferrer()
  };

  let attribution = readStored();
  if (!attribution || incoming.source || incoming.referrer !== 'internal') {
    attribution = {
      source: incoming.source || incoming.referrer || 'direct',
      medium: incoming.medium || (incoming.source ? 'social' : 'referral'),
      campaign: incoming.campaign || CAMPAIGN,
      content: incoming.content || '',
      referrer: incoming.referrer,
      landing: `${location.pathname}${location.search}`,
      startedAt: Date.now()
    };
    try { sessionStorage.setItem(STORAGE_KEY, JSON.stringify(attribution)); } catch { /* optional */ }
  }

  const context = () => ({
    page: location.pathname,
    title: document.title,
    source: attribution?.source || 'direct',
    medium: attribution?.medium || '',
    campaign: attribution?.campaign || CAMPAIGN,
    content: attribution?.content || '',
    referrer: attribution?.referrer || classifyReferrer()
  });

  const safeProps = (props = {}) => Object.fromEntries(
    Object.entries({ ...context(), ...props })
      .filter(([, value]) => value !== undefined && value !== null && value !== '')
      .map(([key, value]) => [slug(key), clean(value)])
  );

  const dispatch = (name, props = {}) => {
    if (DNT) return;
    const eventName = slug(name);
    const payload = safeProps(props);

    try { window.dispatchEvent(new CustomEvent('raven:analytics', { detail: { name: eventName, props: payload } })); } catch { /* optional */ }
    try { if (typeof window.ravenAnalyticsSink === 'function') window.ravenAnalyticsSink(eventName, payload); } catch { /* provider bridge */ }
    try { if (typeof window.plausible === 'function') window.plausible(eventName, { props: payload }); } catch { /* optional */ }
    try { if (window.umami?.track) window.umami.track(eventName, payload); } catch { /* optional */ }
    try { if (typeof window.gtag === 'function') window.gtag('event', eventName, payload); } catch { /* optional */ }
  };

  const tagUrl = (url, source, content = '') => {
    try {
      const tagged = new URL(url, location.origin);
      tagged.searchParams.set('utm_source', slug(source));
      tagged.searchParams.set('utm_medium', 'social');
      tagged.searchParams.set('utm_campaign', CAMPAIGN);
      if (content) tagged.searchParams.set('utm_content', slug(content));
      return tagged.href;
    } catch { return url; }
  };

  window.RavenAnalytics = {
    version: '1.0.0',
    attribution: () => ({ ...(attribution || {}) }),
    context,
    track: dispatch,
    tagUrl
  };

  dispatch('raven_page_view', {
    path: location.pathname,
    landing_source: attribution?.source || 'direct',
    landing_content: attribution?.content || ''
  });

  document.addEventListener('click', (event) => {
    const target = event.target.closest('a, button');
    if (!target) return;
    if (target.matches('.story-source-list a, #sources a[href^="http"], .inline-sources a[href^="http"]')) {
      dispatch('source_click', { label: target.textContent, href: target.href || '' });
    }
  }, { passive: true });
})();
