// Exercise production URL selection, without opening or posting to social platforms.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const raw = fs.readFileSync('assets/js/raven-share.js', 'utf8');
const source = raw.slice(0, raw.indexOf('  let mutationTimer = null;')) + '\n globalThis.testApi = {payloadFor, channelPayload};\n})();';
const canonical = 'https://raven-trace.github.io/raventrace-my/investigations/rci-tabung-haji/';
const document = {
 body: {classList: {contains: () => true}},
 querySelector: (s) => s === 'link[rel="canonical"]' ? {href: canonical} : {},
 querySelectorAll: () => []
};
const context = {window: {}, document, location: {origin: 'https://raven-trace.github.io', pathname: new URL(canonical).pathname}, URL};
vm.createContext(context); vm.runInContext(source, context);
const item = (section, id = 'test-card') => ({
 id, closest: () => ({id: section}),
 querySelector: (s) => s === 'h3' ? {textContent: 'Test title'} : null,
 querySelectorAll: () => []
});
for (const section of ['updates','people','timeline','governance','money','investments','tracks','disputed-record','sources']) {
 const result = context.testApi.payloadFor(item(section));
 assert.equal(result.url, canonical + section + '/');
 for (const channel of ['threads','whatsapp','facebook','copy','share_sheet']) {
  const tagged = new URL(context.testApi.channelPayload(result, channel, 'test-card').url);
  assert.equal(tagged.hash, '');
  assert.equal(tagged.pathname, new URL(canonical + section + '/').pathname);
  assert.equal(tagged.searchParams.get('utm_source'), channel);
 }
}
assert.equal(context.testApi.payloadFor(item('unmapped')).url, canonical);
assert.equal(context.testApi.payloadFor(item('updates','news-2026-09-06-jamil-reman-checkpoint')).url,
 'https://raven-trace.github.io/raventrace-my/news/2026/09/06/jamil-khir-reman-checkpoint/');
console.log('PASS: 9 section destinations, 5 share channels, story precedence and clean fallback.');
