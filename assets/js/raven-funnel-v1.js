(() => {
  'use strict';
  if (window.__RAVEN_FUNNEL_V1__) return;
  window.__RAVEN_FUNNEL_V1__ = true;

  const q = (s, r = document) => r.querySelector(s);
  const qa = (s, r = document) => [...r.querySelectorAll(s)];
  const ROOT = '/raventrace-my/';
  const RCI = `${ROOT}investigations/rci-tabung-haji/`;
  const isNarrative = location.pathname.startsWith(`${RCI}narratives/`);

  const emit = (name, detail = {}) => {
    const payload = {
      name,
      path: location.pathname,
      ts: Date.now(),
      ...detail
    };
    window.dispatchEvent(new CustomEvent('raven:metric', { detail: payload }));
    document.dispatchEvent(new CustomEvent('raven:metric', { detail: payload }));
    window.ravenReadMetrics.events.push(payload);
  };

  window.ravenReadMetrics = window.ravenReadMetrics || {
    startedAt: Date.now(),
    events: [],
    getSession() {
      return {
        startedAt: this.startedAt,
        elapsedMs: Date.now() - this.startedAt,
        events: [...this.events]
      };
    }
  };

  /* ---------------------------------------------------------
     Semantic journey instrumentation for existing Lytical data.
     Lytical already exposes click text/href, duration and scroll.
     These attributes make Raven's own funnel semantics consistent
     without inventing a second analytics backend.
     --------------------------------------------------------- */
  const annotateLinks = () => {
    qa('a[href]').forEach((a) => {
      const href = a.getAttribute('href') || '';
      if (a.dataset.ravenEvent) return;
      if (/\/narratives\//.test(href)) a.dataset.ravenEvent = 'narrative_entry';
      else if (/#sources\b|\/sources\//.test(href)) a.dataset.ravenEvent = 'evidence_entry';
      else if (/\/investigations\/rci-tabung-haji\//.test(href)) a.dataset.ravenEvent = 'case_entry';
      if (/^https?:\/\//.test(href) && !href.includes('raven-trace.github.io')) {
        if (a.closest('.sources-grid, .source-room, .raven-evidence-bridge')) {
          a.dataset.ravenEvent = 'primary_source_click';
        }
      }
    });

    document.addEventListener('click', (event) => {
      const a = event.target.closest?.('a[data-raven-event], button[data-raven-event]');
      if (!a) return;
      emit('journey_click', {
        event: a.dataset.ravenEvent,
        text: (a.textContent || '').trim().slice(0, 120),
        href: a.getAttribute?.('href') || null
      });
    }, { capture: true });
  };

  /* ---------------------------------------------------------
     Raven Read Metrics abstraction.
     Existing analytics can still calculate these externally from
     session duration + scroll. This emits the same semantic tiers
     inside the page so future adapters do not need a rewrite.
     --------------------------------------------------------- */
  const startReadMetrics = () => {
    const thresholds = [
      [30000, 'read_30s'],
      [60000, 'read_60s'],
      [180000, 'deep_read_180s']
    ];
    let visibleSince = document.visibilityState === 'visible' ? performance.now() : null;
    let activeMs = 0;
    const fired = new Set();

    const sample = () => {
      const now = performance.now();
      const active = activeMs + (visibleSince == null ? 0 : now - visibleSince);
      thresholds.forEach(([ms, name]) => {
        if (active >= ms && !fired.has(name)) {
          fired.add(name);
          document.body.dataset.ravenReadTier = name;
          emit(name, { activeMs: Math.round(active) });
        }
      });
    };

    document.addEventListener('visibilitychange', () => {
      const now = performance.now();
      if (document.visibilityState === 'visible') {
        visibleSince = now;
      } else if (visibleSince != null) {
        activeMs += now - visibleSince;
        visibleSince = null;
        sample();
      }
    });
    setInterval(sample, 5000);

    const scrollFired = new Set();
    const onScroll = () => {
      const max = Math.max(1, document.documentElement.scrollHeight - innerHeight);
      const pct = Math.max(0, Math.min(100, Math.round((scrollY / max) * 100)));
      [50, 75, 100].forEach((mark) => {
        if (pct >= mark && !scrollFired.has(mark)) {
          scrollFired.add(mark);
          document.body.dataset.ravenScrollDepth = String(mark);
          emit(`scroll_${mark}`, { depth: pct });
        }
      });
    };
    addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  };

  const normalize = (s = '') => s.replace(/\s+/g, ' ').trim().toLowerCase();

  const findPreferredSource = (card, sourceItems) => {
    const text = normalize(card.textContent);
    const sourceBy = (patterns) => sourceItems.find((item) => {
      const t = normalize(item.textContent);
      return patterns.some((p) => p.test(t));
    });

    /*
     * Rules are deliberately specific. Never use loose substrings such as
     * /pas\b/ because Malay words like "selepas" contain the same letters.
     * A wrong source bridge is worse than falling back to the official RCI.
     */
    const rules = [
      [/azeez|rm193\.5 juta/, [/tiga individu didakwa|pertuduhan/]],
      [/china|bukan islam/, [/aset dijual|bukan islam|china/]],
      [/madinah|tiada bukti kecurian|tiada salah laku/, [/madinah|audit tidak menemui bukti kecurian/]],
      [/baitul maqdis|\bpas\b|rci baharu/, [/\bpas\b.*rci baharu|baitul maqdis/]],
      [/zahid|\bpac\b/, [/zahid|\bpac\b/]],
      [/\bamk\b|alat mencari keputusan politik/, [/\bamk\b|keputusan politik/]],
      [/14 kertas|18 individu|11 direman|kertas siasatan/, [/14 kertas siasatan|18 ditahan|11 direman/]],
      [/didakwa|pertuduhan|mahkamah/, [/tiga individu didakwa|pertuduhan/]]
    ];

    for (const [cardPattern, sourcePatterns] of rules) {
      if (cardPattern.test(text)) {
        const hit = sourceBy(sourcePatterns);
        if (hit) return hit;
      }
    }
    return sourceBy([/laporan rci tabung haji|laporan suruhanjaya siasatan diraja/]) || sourceItems[0] || null;
  };

  const copyText = async (value) => {
    if (navigator.clipboard?.writeText) return navigator.clipboard.writeText(value);
    const ta = document.createElement('textarea');
    ta.value = value;
    ta.setAttribute('readonly', '');
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.append(ta);
    ta.select();
    document.execCommand('copy');
    ta.remove();
  };

  const enhanceNarratives = () => {
    if (!isNarrative) return;
    document.body.classList.add('raven-funnel-ready');

    const sourceItems = qa('#sources .sources-grid > li[id]');
    sourceItems.forEach((li) => li.classList.add('raven-source-target'));

    qa('.narrative-v5-card[id]').forEach((card) => {
      if (card.dataset.ravenFunnelReady === 'true') return;
      card.dataset.ravenFunnelReady = 'true';

      const claimZone = q('.signal-claim-zone', card);
      if (claimZone && !q('.raven-narrative-sharelink', claimZone)) {
        const copy = document.createElement('button');
        copy.type = 'button';
        copy.className = 'raven-narrative-sharelink';
        copy.dataset.ravenEvent = 'narrative_deeplink_copy';
        copy.textContent = 'Salin link naratif';
        copy.addEventListener('click', async () => {
          const url = `${location.origin}${location.pathname}#${card.id}`;
          try {
            await copyText(url);
            copy.dataset.copied = 'true';
            copy.textContent = 'Link disalin ✓';
            setTimeout(() => {
              copy.dataset.copied = 'false';
              copy.textContent = 'Salin link naratif';
            }, 1800);
          } catch (_) {
            copy.textContent = 'Tak dapat salin';
          }
        });
        claimZone.append(copy);
      }

      if (q('.raven-evidence-bridge', card)) return;
      const sourceLi = findPreferredSource(card, sourceItems);
      const sourceA = sourceLi?.querySelector('a[href]') || null;
      const grade = sourceLi?.querySelector(':scope > span')?.textContent?.trim() || 'S';
      const sourceTitle = sourceA?.textContent?.trim() || 'Source Room Raven';

      const bridge = document.createElement('section');
      bridge.className = 'raven-evidence-bridge';
      bridge.setAttribute('aria-label', 'Langkah seterusnya selepas verdict');
      bridge.innerHTML = `
        <p class="raven-evidence-bridge-kicker">Nak check sendiri?</p>
        <h4>Jangan berhenti pada verdict Raven.</h4>
        <div class="raven-evidence-source"><span class="raven-evidence-source-grade"></span><span class="raven-evidence-source-title"></span></div>
        <div class="raven-evidence-actions"></div>`;
      q('.raven-evidence-source-grade', bridge).textContent = grade;
      q('.raven-evidence-source-title', bridge).textContent = sourceTitle;
      const actions = q('.raven-evidence-actions', bridge);

      const primary = document.createElement('a');
      primary.dataset.ravenEvent = 'primary_source_click';
      primary.textContent = sourceA ? 'Buka sumber asal ↗' : 'Tengok Source Room';
      primary.href = sourceA?.href || '#sources';
      if (sourceA) {
        primary.target = '_blank';
        primary.rel = 'noopener noreferrer';
      }

      const caseLink = document.createElement('a');
      caseLink.dataset.ravenEvent = 'case_continuation';
      caseLink.textContent = 'Faham keseluruhan kes';
      caseLink.href = `${RCI}#briefing`;
      actions.append(primary, caseLink);

      const verdict = q('.signal-verdict-zone', card) || q('.narrative-v5-verdict', card);
      if (verdict) verdict.insertAdjacentElement('afterend', bridge);
      else card.append(bridge);
    });

    const focusHash = () => {
      if (!location.hash) return;
      const id = decodeURIComponent(location.hash.slice(1));
      const target = document.getElementById(id);
      if (!target || !target.matches('.narrative-v5-card[id], .raven-source-target')) return;
      requestAnimationFrame(() => target.scrollIntoView({ block: 'start', behavior: 'auto' }));
      if (target.matches('.narrative-v5-card')) emit('narrative_deeplink_land', { narrative: id });
    };
    setTimeout(focusHash, 180);
    addEventListener('hashchange', focusHash);
  };

  const boot = () => {
    annotateLinks();
    startReadMetrics();
    enhanceNarratives();
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot, { once: true });
  else boot();
})();
