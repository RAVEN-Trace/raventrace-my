import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';

const base = process.env.RAVEN_QA_BASE || 'https://raven-trace.github.io/raventrace-my';
const output = process.env.RAVEN_QA_OUTPUT || 'visual-qa';
const root = process.cwd();

function walk(dir) {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    if (entry.name === '.git' || entry.name === 'node_modules' || entry.name === 'visual-qa') return [];
    const full = path.join(dir, entry.name);
    return entry.isDirectory() ? walk(full) : [full];
  });
}

const pages = walk(root)
  .filter((file) => file.endsWith(`${path.sep}index.html`) || file === path.join(root, 'index.html'))
  .map((file) => {
    const relative = path.relative(root, file).replaceAll(path.sep, '/');
    const route = relative === 'index.html' ? '/' : `/${relative.replace(/index\.html$/, '')}`;
    const name = relative.replace(/\/index\.html$/, '').replace(/\.html$/, '').replaceAll('/', '--') || 'home';
    return { name, route };
  })
  .sort((a, b) => a.route.localeCompare(b.route));

if (pages.length !== 32) throw new Error(`Expected 32 public pages, found ${pages.length}`);
fs.mkdirSync(output, { recursive: true });

const browser = await chromium.launch();
const failures = [];
const report = [];
const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function openDeployed(page, route) {
  for (let attempt = 0; attempt < 60; attempt += 1) {
    const url = `${base}${route}?ravenqa=7-${Date.now()}-${Math.random()}`;
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 });
    const ready = await page.evaluate(() =>
      document.body.classList.contains('raven-v7') &&
      Boolean(document.querySelector('link[href*="raven-unified-v7.css?v=7.0.0"]'))
    );
    if (ready) return url;
    await delay(5000);
  }
  throw new Error(`${route}: production did not reach Raven Unified V7`);
}

function record(condition, message) {
  if (!condition) failures.push(message);
}

async function auditPage(page, view, item) {
  const url = await openDeployed(page, item.route);
  await page.addStyleTag({ content: `
    .timeline-item,.update-card,.trace-card,.person-card,details.investment,
    .narrative-card,#sources [id^="s"],.case-section {
      content-visibility: visible !important;
      contain: none !important;
    }
  ` });
  await page.waitForTimeout(180);

  const metrics = await page.evaluate(({ mobile }) => {
    const visible = (element) => {
      const style = getComputedStyle(element);
      const rect = element.getBoundingClientRect();
      return !element.hidden && style.display !== 'none' && style.visibility !== 'hidden' &&
        Number(style.opacity) > 0 && rect.width > 0 && rect.height > 0;
    };
    const rgba = (value) => {
      const parts = value.match(/[\d.]+/g)?.map(Number) || [];
      if (parts.length < 3) return null;
      return [parts[0], parts[1], parts[2], parts.length > 3 ? parts[3] : 1];
    };
    const over = (front, back) => {
      const alpha = front[3] + back[3] * (1 - front[3]);
      if (!alpha) return [255, 255, 255, 1];
      return [0, 1, 2].map((i) => (front[i] * front[3] + back[i] * back[3] * (1 - front[3])) / alpha).concat(alpha);
    };
    const background = (element) => {
      const layers = [];
      for (let node = element; node; node = node.parentElement) {
        const parsed = rgba(getComputedStyle(node).backgroundColor);
        if (parsed && parsed[3] > 0) layers.push(parsed);
      }
      let result = [255, 255, 255, 1];
      for (let i = layers.length - 1; i >= 0; i -= 1) result = over(layers[i], result);
      return result;
    };
    const luminance = (colour) => {
      const channels = colour.slice(0, 3).map((value) => {
        const channel = value / 255;
        return channel <= .03928 ? channel / 12.92 : ((channel + .055) / 1.055) ** 2.4;
      });
      return .2126 * channels[0] + .7152 * channels[1] + .0722 * channels[2];
    };
    const ratio = (foreground, backdrop) => {
      const fg = over(foreground, backdrop);
      const high = Math.max(luminance(fg), luminance(backdrop));
      const low = Math.min(luminance(fg), luminance(backdrop));
      return (high + .05) / (low + .05);
    };
    const selectorFor = (element) => {
      if (element.id) return `#${element.id}`;
      const classes = [...element.classList].slice(0, 3).join('.');
      return `${element.tagName.toLowerCase()}${classes ? `.${classes}` : ''}`;
    };

    const contrastFailures = [];
    const candidates = [...document.querySelectorAll('body *')].filter((element) => {
      if (!visible(element) || ['SCRIPT', 'STYLE', 'SVG', 'PATH'].includes(element.tagName)) return false;
      return [...element.childNodes].some((node) => node.nodeType === Node.TEXT_NODE && node.textContent.trim());
    });
    for (const element of candidates) {
      const style = getComputedStyle(element);
      const foreground = rgba(style.color);
      if (!foreground) continue;
      const backdrop = background(element);
      const value = ratio(foreground, backdrop);
      const size = Number.parseFloat(style.fontSize);
      const weight = Number.parseInt(style.fontWeight, 10) || 400;
      const large = size >= 24 || (size >= 18.66 && weight >= 700);
      const minimum = large ? 3 : 4.5;
      if (value + .001 < minimum) {
        contrastFailures.push({
          selector: selectorFor(element),
          text: element.textContent.trim().replace(/\s+/g, ' ').slice(0, 90),
          ratio: Number(value.toFixed(2)),
          minimum,
          color: style.color,
          background: backdrop.slice(0, 3).map(Math.round).join(',')
        });
      }
    }

    const controls = [...document.querySelectorAll('.btn,.filter-btn,.raven-share-btn,.raven-share-link,.section-links a,.nav-toggle,.site-nav a,.footer-nav a,.v5-quicklinks a,.raven-question-grid a,.raven-continue-list>a,.reading-nav a,main button,summary')].filter(visible);
    const smallControls = controls.map((element) => {
      const rect = element.getBoundingClientRect();
      return { selector: selectorFor(element), width: rect.width, height: rect.height };
    }).filter(({ width, height }) => width < (mobile ? 44 : 40) || height < (mobile ? 44 : 40));

    const unnamedControls = [...document.querySelectorAll('a[href],button,summary,[role="button"]')]
      .filter(visible)
      .filter((element) => !(element.getAttribute('aria-label') || element.getAttribute('aria-labelledby') || element.textContent.trim() || element.title))
      .map(selectorFor);

    const duplicateIds = [...document.querySelectorAll('[id]')]
      .map((element) => element.id)
      .filter((id, index, ids) => ids.indexOf(id) !== index);
    const missingAnchors = [...document.querySelectorAll('a[href^="#"]')]
      .map((link) => link.getAttribute('href'))
      .filter((href) => href.length > 1 && !document.getElementById(decodeURIComponent(href.slice(1))));

    return {
      title: document.title,
      bodyClass: document.body.className,
      viewport: document.documentElement.clientWidth,
      scrollWidth: document.documentElement.scrollWidth,
      contrastFailures: contrastFailures.slice(0, 60),
      contrastFailureCount: contrastFailures.length,
      smallControls: smallControls.slice(0, 30),
      smallControlCount: smallControls.length,
      unnamedControls,
      duplicateIds: [...new Set(duplicateIds)],
      missingAnchors: [...new Set(missingAnchors)],
      fakeShareLinks: document.querySelectorAll('.raven-share-link[href="#"]').length,
      unifiedCss: Boolean(document.querySelector('link[href*="raven-unified-v7.css?v=7.0.0"]')),
      skipLink: Boolean(document.querySelector('.skip-link'))
    };
  }, { mobile: view.name === 'mobile' });

  const prefix = `${view.name}/${item.name}`;
  record(metrics.unifiedCss, `${prefix}: Unified V7 stylesheet missing`);
  record(metrics.scrollWidth <= metrics.viewport + 4, `${prefix}: horizontal overflow ${metrics.scrollWidth} > ${metrics.viewport}`);
  record(metrics.contrastFailureCount === 0, `${prefix}: ${metrics.contrastFailureCount} text contrast failures`);
  record(metrics.smallControlCount === 0, `${prefix}: ${metrics.smallControlCount} undersized component controls`);
  record(metrics.unnamedControls.length === 0, `${prefix}: ${metrics.unnamedControls.length} unnamed controls`);
  record(metrics.duplicateIds.length === 0, `${prefix}: duplicate IDs ${metrics.duplicateIds.join(', ')}`);
  record(metrics.missingAnchors.length === 0, `${prefix}: missing anchors ${metrics.missingAnchors.join(', ')}`);
  record(metrics.fakeShareLinks === 0, `${prefix}: ${metrics.fakeShareLinks} fake share links remain`);
  record(metrics.skipLink, `${prefix}: skip link missing`);

  const screenshot = view.name === 'mobile' || ['home', 'news', 'investigations--rci-tabung-haji', 'investigations--rci-tabung-haji--narratives'].includes(item.name);
  if (screenshot) await page.screenshot({ path: `${output}/${view.name}-${item.name}.png`, fullPage: true });
  report.push({ view: view.name, page: item.name, route: item.route, url, ...metrics });
}

const views = [
  { name: 'mobile', viewport: { width: 390, height: 844 } },
  { name: 'desktop', viewport: { width: 1440, height: 900 } }
];

for (const view of views) {
  const context = await browser.newContext({ viewport: view.viewport, deviceScaleFactor: 1 });
  for (const item of pages) {
    const page = await context.newPage();
    try {
      await auditPage(page, view, item);
    } catch (error) {
      failures.push(`${view.name}/${item.name}: ${error.message}`);
      await page.screenshot({ path: `${output}/${view.name}-${item.name}-failure.png`, fullPage: true }).catch(() => {});
    } finally {
      await page.close();
    }
  }
  await context.close();
}

await browser.close();
fs.writeFileSync(`${output}/report.json`, JSON.stringify({ pages: pages.length, checks: report.length, report, failures }, null, 2));
console.log(JSON.stringify({ pages: pages.length, checks: report.length, failures }, null, 2));
if (failures.length) throw new Error(`Raven Unified V7 QA failed:\n${failures.join('\n')}`);
