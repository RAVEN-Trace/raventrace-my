import { chromium } from 'playwright';

const base = process.env.RAVEN_QA_BASE || 'https://raven-trace.github.io/raventrace-my';
const route = '/investigations/rci-tabung-haji/';
const browser = await chromium.launch();
const failures = [];
const record = (condition, message) => { if (!condition) failures.push(message); };
const bust = () => `ravenreaderv8=${Date.now()}-${Math.random()}`;

async function waitForReader(page) {
  await page.waitForFunction(() =>
    document.body.classList.contains('raven-reader-v8') &&
    document.querySelectorAll('.raven-reader-toggle').length >= 8,
    { timeout: 45000 }
  );
  await page.waitForTimeout(250);
}

// Mobile: one idea at a time.
{
  const context = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 });
  const page = await context.newPage();
  await page.goto(`${base}${route}?${bust()}`, { waitUntil: 'domcontentloaded', timeout: 45000 });
  await waitForReader(page);

  const initial = await page.evaluate(() => {
    const visible = (el) => {
      const s = getComputedStyle(el);
      const r = el.getBoundingClientRect();
      return s.display !== 'none' && s.visibility !== 'hidden' && r.width > 0 && r.height > 0;
    };
    const toggles = [...document.querySelectorAll('.raven-reader-toggle')];
    const collapsed = [...document.querySelectorAll('.case-content > .case-section.raven-reader-collapsed')];
    const updates = document.querySelector('#updates');
    const updatesTrace = updates?.querySelector('.trace-card');
    const briefing = document.querySelector('#briefing');
    return {
      toggleCount: toggles.length,
      collapsedCount: collapsed.length,
      minToggleHeight: Math.min(...toggles.map((b) => b.getBoundingClientRect().height)),
      updatesCollapsed: updates?.classList.contains('raven-reader-collapsed') || false,
      updatesTraceVisible: updatesTrace ? visible(updatesTrace) : null,
      briefingVisible: briefing ? visible(briefing) : false,
      bodyHeight: document.documentElement.scrollHeight
    };
  });

  record(initial.toggleCount >= 8, `mobile: expected >=8 reader toggles, got ${initial.toggleCount}`);
  record(initial.collapsedCount === initial.toggleCount, `mobile: ${initial.collapsedCount}/${initial.toggleCount} deep sections collapsed initially`);
  record(initial.minToggleHeight >= 44, `mobile: toggle target too small (${initial.minToggleHeight}px)`);
  record(initial.updatesCollapsed, 'mobile: #updates should start collapsed');
  record(initial.updatesTraceVisible === false, 'mobile: collapsed #updates leaked trace content');
  record(initial.briefingVisible, 'mobile: #briefing should remain visible');
  record(initial.bodyHeight < 30000, `mobile: initial CASEFILE remains excessively tall (${initial.bodyHeight}px)`);

  await page.locator('#updates > .raven-reader-toggle').click();
  await page.waitForTimeout(100);
  const opened = await page.evaluate(() => {
    const section = document.querySelector('#updates');
    const trace = section?.querySelector('.trace-card');
    const style = trace ? getComputedStyle(trace) : null;
    return {
      collapsed: section?.classList.contains('raven-reader-collapsed') || false,
      aria: section?.querySelector('.raven-reader-toggle')?.getAttribute('aria-expanded'),
      traceVisible: Boolean(trace && style && style.display !== 'none' && style.visibility !== 'hidden')
    };
  });
  record(!opened.collapsed, 'mobile: #updates did not expand on click');
  record(opened.aria === 'true', `mobile: expanded toggle aria-expanded=${opened.aria}`);
  record(opened.traceVisible, 'mobile: #updates content remained hidden after expansion');

  await page.goto(`${base}${route}?${bust()}#money`, { waitUntil: 'domcontentloaded', timeout: 45000 });
  await waitForReader(page);
  await page.waitForTimeout(350);
  const deepLink = await page.evaluate(() => {
    const section = document.querySelector('#money');
    return {
      exists: Boolean(section),
      collapsed: section?.classList.contains('raven-reader-collapsed') || false,
      aria: section?.querySelector('.raven-reader-toggle')?.getAttribute('aria-expanded')
    };
  });
  record(deepLink.exists, 'mobile: #money section missing');
  record(!deepLink.collapsed, 'mobile: direct #money deep link did not auto-reveal section');
  record(deepLink.aria === 'true', `mobile: #money deep-link aria-expanded=${deepLink.aria}`);

  await context.close();
}

// Desktop: progressive-disclosure markup exists, but full dossier stays visible.
{
  const context = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
  const page = await context.newPage();
  await page.goto(`${base}${route}?${bust()}`, { waitUntil: 'domcontentloaded', timeout: 45000 });
  await waitForReader(page);
  const desktop = await page.evaluate(() => {
    const toggle = document.querySelector('.raven-reader-toggle');
    const updatesTrace = document.querySelector('#updates .trace-card');
    return {
      toggleDisplay: toggle ? getComputedStyle(toggle).display : null,
      traceDisplay: updatesTrace ? getComputedStyle(updatesTrace).display : null,
      bodyHeight: document.documentElement.scrollHeight
    };
  });
  record(desktop.toggleDisplay === 'none', `desktop: reader toggle should be hidden, got ${desktop.toggleDisplay}`);
  record(desktop.traceDisplay !== 'none', 'desktop: full CASEFILE content should remain visible');
  await context.close();
}

await browser.close();
console.log(JSON.stringify({ feature: 'Raven Reader V8', failures }, null, 2));
if (failures.length) throw new Error(`Raven Reader V8 QA failed:\n${failures.join('\n')}`);
