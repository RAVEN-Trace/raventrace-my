import { chromium } from 'playwright';

const base=process.env.RAVEN_QA_BASE||'https://raven-trace.github.io/raventrace-my';
const caseRoute='/investigations/rci-tabung-haji/';
const narrativeRoute='/investigations/rci-tabung-haji/narratives/';
const browser=await chromium.launch();
const failures=[];
const record=(ok,msg)=>{if(!ok) failures.push(msg)};
const bust=()=>`ravenreaderv8=${Date.now()}-${Math.random()}`;

async function waitForCaseReader(page){
  await page.waitForFunction(()=>document.body.classList.contains('raven-reader-v8')&&document.querySelectorAll('.raven-reader-toggle').length>=8,{timeout:45000});
  await page.waitForTimeout(250);
}
async function waitForNarrativeReader(page){
  await page.waitForFunction(()=>document.body.classList.contains('raven-funnel-ready')&&document.querySelectorAll('.narrative-v5-card.signal-narrative-card').length>=8,{timeout:45000});
  await page.waitForTimeout(250);
}

// CASEFILE mobile: briefing first, depth on demand.
{
  const context=await browser.newContext({viewport:{width:390,height:844},deviceScaleFactor:1});
  const page=await context.newPage();
  await page.goto(`${base}${caseRoute}?${bust()}`,{waitUntil:'domcontentloaded',timeout:45000});
  await waitForCaseReader(page);
  const initial=await page.evaluate(()=>{
    const visible=(el)=>{const s=getComputedStyle(el),r=el.getBoundingClientRect();return s.display!=='none'&&s.visibility!=='hidden'&&r.width>0&&r.height>0};
    const toggles=[...document.querySelectorAll('.raven-reader-toggle')];
    const collapsed=[...document.querySelectorAll('.case-content > .case-section.raven-reader-collapsed')];
    const updates=document.querySelector('#updates'), trace=updates?.querySelector('.trace-card'), briefing=document.querySelector('#briefing');
    return {toggleCount:toggles.length,collapsedCount:collapsed.length,minToggleHeight:Math.min(...toggles.map(b=>b.getBoundingClientRect().height)),updatesCollapsed:updates?.classList.contains('raven-reader-collapsed')||false,updatesTraceVisible:trace?visible(trace):null,briefingVisible:briefing?visible(briefing):false,bodyHeight:document.documentElement.scrollHeight};
  });
  record(initial.toggleCount>=8,`mobile CASEFILE: expected >=8 toggles, got ${initial.toggleCount}`);
  record(initial.collapsedCount===initial.toggleCount,`mobile CASEFILE: ${initial.collapsedCount}/${initial.toggleCount} deep sections collapsed`);
  record(initial.minToggleHeight>=44,`mobile CASEFILE: target too small (${initial.minToggleHeight}px)`);
  record(initial.updatesCollapsed,'mobile CASEFILE: #updates should start collapsed');
  record(initial.updatesTraceVisible===false,'mobile CASEFILE: collapsed #updates leaked content');
  record(initial.briefingVisible,'mobile CASEFILE: #briefing should stay visible');
  record(initial.bodyHeight<30000,`mobile CASEFILE: still excessively tall (${initial.bodyHeight}px)`);
  await page.locator('#updates > .raven-reader-toggle').click(); await page.waitForTimeout(100);
  const opened=await page.evaluate(()=>{const s=document.querySelector('#updates'),t=s?.querySelector('.trace-card'),st=t?getComputedStyle(t):null;return {collapsed:s?.classList.contains('raven-reader-collapsed')||false,aria:s?.querySelector('.raven-reader-toggle')?.getAttribute('aria-expanded'),visible:Boolean(t&&st&&st.display!=='none'&&st.visibility!=='hidden')}});
  record(!opened.collapsed,'mobile CASEFILE: #updates did not expand'); record(opened.aria==='true',`mobile CASEFILE: aria=${opened.aria}`); record(opened.visible,'mobile CASEFILE: content hidden after expansion');
  await page.goto(`${base}${caseRoute}?${bust()}#money`,{waitUntil:'domcontentloaded',timeout:45000}); await waitForCaseReader(page); await page.waitForTimeout(350);
  const deep=await page.evaluate(()=>{const s=document.querySelector('#money');return {exists:Boolean(s),collapsed:s?.classList.contains('raven-reader-collapsed')||false,aria:s?.querySelector('.raven-reader-toggle')?.getAttribute('aria-expanded')}});
  record(deep.exists,'mobile CASEFILE: #money missing'); record(!deep.collapsed,'mobile CASEFILE: #money deep link not revealed'); record(deep.aria==='true',`mobile CASEFILE: #money aria=${deep.aria}`);
  await context.close();
}

// CASEFILE desktop remains a full dossier.
{
  const context=await browser.newContext({viewport:{width:1440,height:900},deviceScaleFactor:1}); const page=await context.newPage();
  await page.goto(`${base}${caseRoute}?${bust()}`,{waitUntil:'domcontentloaded',timeout:45000}); await waitForCaseReader(page);
  const d=await page.evaluate(()=>{const b=document.querySelector('.raven-reader-toggle'),t=document.querySelector('#updates .trace-card');return {toggle:b?getComputedStyle(b).display:null,trace:t?getComputedStyle(t).display:null}});
  record(d.toggle==='none',`desktop CASEFILE: toggle should hide, got ${d.toggle}`); record(d.trace!=='none','desktop CASEFILE: content should remain visible');
  await context.close();
}

// Narrative mobile: scan claim + verdict; evidence opens on demand.
{
  const context=await browser.newContext({viewport:{width:390,height:844},deviceScaleFactor:1}); const page=await context.newPage();
  await page.goto(`${base}${narrativeRoute}?${bust()}`,{waitUntil:'domcontentloaded',timeout:45000}); await waitForNarrativeReader(page);
  const initial=await page.evaluate(()=>{const card=document.querySelector('.narrative-v5-card.signal-narrative-card'),rec=card?.querySelector('.signal-record-zone'),bridge=card?.querySelector('.raven-evidence-bridge'),verdict=card?.querySelector('.signal-verdict-zone'),details=card?.querySelector('.narrative-v5-details'); const vis=(x)=>x&&getComputedStyle(x).display!=='none'; return {id:card?.id,recordVisible:vis(rec),bridgeVisible:vis(bridge),verdictVisible:vis(verdict),detailsOpen:details?.open||false,bodyHeight:document.documentElement.scrollHeight};});
  record(Boolean(initial.id),'mobile Narrative: no narrative card'); record(initial.verdictVisible,'mobile Narrative: verdict must remain visible'); record(!initial.recordVisible,'mobile Narrative: record should be folded initially'); record(!initial.bridgeVisible,'mobile Narrative: source bridge should be folded initially'); record(!initial.detailsOpen,'mobile Narrative: details should start closed'); record(initial.bodyHeight<19000,`mobile Narrative: still excessively tall (${initial.bodyHeight}px)`);
  await page.locator('.narrative-v5-card.signal-narrative-card').first().locator('.narrative-v5-details > summary').click(); await page.waitForTimeout(120);
  const open=await page.evaluate(()=>{const c=document.querySelector('.narrative-v5-card.signal-narrative-card'),r=c?.querySelector('.signal-record-zone'),b=c?.querySelector('.raven-evidence-bridge'),d=c?.querySelector('.narrative-v5-details');return {record:getComputedStyle(r).display!=='none',bridge:getComputedStyle(b).display!=='none',open:d?.open||false}});
  record(open.open&&open.record&&open.bridge,'mobile Narrative: evidence/context did not reveal with details');
  await page.goto(`${base}${narrativeRoute}?${bust()}#${initial.id}`,{waitUntil:'domcontentloaded',timeout:45000}); await waitForNarrativeReader(page); await page.waitForTimeout(350);
  const target=await page.evaluate((id)=>{const c=document.getElementById(id),r=c?.querySelector('.signal-record-zone'),b=c?.querySelector('.raven-evidence-bridge');return {targeted:location.hash===`#${id}`,record:r?getComputedStyle(r).display!=='none':false,bridge:b?getComputedStyle(b).display!=='none':false}},initial.id);
  record(target.targeted&&target.record&&target.bridge,'mobile Narrative: direct narrative deep link should expose evidence');
  await context.close();
}

// Narrative desktop remains fully readable.
{
  const context=await browser.newContext({viewport:{width:1440,height:900},deviceScaleFactor:1}); const page=await context.newPage();
  await page.goto(`${base}${narrativeRoute}?${bust()}`,{waitUntil:'domcontentloaded',timeout:45000}); await waitForNarrativeReader(page);
  const d=await page.evaluate(()=>{const c=document.querySelector('.narrative-v5-card.signal-narrative-card'),r=c?.querySelector('.signal-record-zone'),b=c?.querySelector('.raven-evidence-bridge');return {record:r?getComputedStyle(r).display:null,bridge:b?getComputedStyle(b).display:null}});
  record(d.record!=='none'&&d.bridge!=='none','desktop Narrative: evidence should remain visible');
  await context.close();
}

await browser.close();
console.log(JSON.stringify({feature:'Raven Reader V8',failures},null,2));
if(failures.length) throw new Error(`Raven Reader V8 QA failed:\n${failures.join('\n')}`);
