import { chromium } from 'playwright';

const base=process.env.RAVEN_QA_BASE||'https://raven-trace.github.io/raventrace-my';
const caseRoute='/investigations/rci-tabung-haji/';
const narrativeRoute='/investigations/rci-tabung-haji/narratives/';
const narrativeIds=['rm13b','four-five','rm18m','political','rci-crime','fully-fixed'];
const browser=await chromium.launch();
const failures=[];
const record=(ok,msg)=>{if(!ok) failures.push(msg)};
const bust=()=>`ravenreaderv8=${Date.now()}-${Math.random()}`;

async function waitForCaseReader(page){
  await page.waitForFunction(()=>{
    const content=document.querySelector('#case-content')||document.querySelector('.case-content');
    if(!document.body.classList.contains('raven-reader-v8')||!content) return false;
    const expected=[...content.children].filter((el)=>el.matches('.case-section[id]')&&el.id!=='briefing').length;
    return expected>0&&document.querySelectorAll('.raven-reader-toggle').length===expected;
  },null,{timeout:45000});
  await page.waitForTimeout(250);
}
async function waitForNarrativeReader(page){
  await page.waitForFunction((ids)=>{
    const units=ids.map((id)=>document.getElementById(id));
    const visual=document.querySelector('[data-raven-visual="narrative"] img');
    const copyLocked=units.every((unit)=>unit?.dataset?.copyLock==='preserved');
    return document.body.dataset.ravenNarrativeStructure==='locked-v1'&&units.every(Boolean)&&copyLocked&&Boolean(visual);
  },narrativeIds,{timeout:45000});
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
    const content=document.querySelector('#case-content')||document.querySelector('.case-content');
    const expectedDeep=content?[...content.children].filter((el)=>el.matches('.case-section[id]')&&el.id!=='briefing').length:0;
    const toggles=[...document.querySelectorAll('.raven-reader-toggle')];
    const collapsed=[...document.querySelectorAll('.case-content > .case-section.raven-reader-collapsed')];
    const revision=document.querySelector('#revision'), trace=revision?.querySelector('.trace-card'), briefing=document.querySelector('#briefing');
    return {expectedDeep,toggleCount:toggles.length,collapsedCount:collapsed.length,minToggleHeight:Math.min(...toggles.map(b=>b.getBoundingClientRect().height)),revisionCollapsed:revision?.classList.contains('raven-reader-collapsed')||false,revisionTraceVisible:trace?visible(trace):null,briefingVisible:briefing?visible(briefing):false,bodyHeight:document.documentElement.scrollHeight};
  });
  record(initial.expectedDeep>=1,'mobile CASEFILE: no deep sections found');
  record(initial.toggleCount===initial.expectedDeep,`mobile CASEFILE: expected ${initial.expectedDeep} toggles, got ${initial.toggleCount}`);
  record(initial.collapsedCount===initial.toggleCount,`mobile CASEFILE: ${initial.collapsedCount}/${initial.toggleCount} deep sections collapsed`);
  record(initial.minToggleHeight>=44,`mobile CASEFILE: target too small (${initial.minToggleHeight}px)`);
  record(initial.revisionCollapsed,'mobile CASEFILE: #revision should start collapsed');
  record(initial.revisionTraceVisible===false,'mobile CASEFILE: collapsed #revision leaked content');
  record(initial.briefingVisible,'mobile CASEFILE: #briefing should stay visible');
  record(initial.bodyHeight<30000,`mobile CASEFILE: still excessively tall (${initial.bodyHeight}px)`);
  await page.locator('#revision > .raven-reader-toggle').click(); await page.waitForTimeout(100);
  const opened=await page.evaluate(()=>{const s=document.querySelector('#revision'),t=s?.querySelector('.trace-card'),st=t?getComputedStyle(t):null;return {collapsed:s?.classList.contains('raven-reader-collapsed')||false,aria:s?.querySelector('.raven-reader-toggle')?.getAttribute('aria-expanded'),visible:Boolean(t&&st&&st.display!=='none'&&st.visibility!=='hidden')}});
  record(!opened.collapsed,'mobile CASEFILE: #revision did not expand'); record(opened.aria==='true',`mobile CASEFILE: aria=${opened.aria}`); record(opened.visible,'mobile CASEFILE: content hidden after expansion');
  await page.goto(`${base}${caseRoute}?${bust()}#money`,{waitUntil:'domcontentloaded',timeout:45000}); await waitForCaseReader(page); await page.waitForTimeout(350);
  const deep=await page.evaluate(()=>{const s=document.querySelector('#money');return {exists:Boolean(s),collapsed:s?.classList.contains('raven-reader-collapsed')||false,aria:s?.querySelector('.raven-reader-toggle')?.getAttribute('aria-expanded')}});
  record(deep.exists,'mobile CASEFILE: #money missing'); record(!deep.collapsed,'mobile CASEFILE: #money deep link not revealed'); record(deep.aria==='true',`mobile CASEFILE: #money aria=${deep.aria}`);
  await context.close();
}

// CASEFILE desktop remains a full dossier.
{
  const context=await browser.newContext({viewport:{width:1440,height:900},deviceScaleFactor:1}); const page=await context.newPage();
  await page.goto(`${base}${caseRoute}?${bust()}`,{waitUntil:'domcontentloaded',timeout:45000}); await waitForCaseReader(page);
  const d=await page.evaluate(()=>{const b=document.querySelector('.raven-reader-toggle'),t=document.querySelector('#revision .trace-card');return {toggle:b?getComputedStyle(b).display:null,trace:t?getComputedStyle(t).display:null}});
  record(d.toggle==='none',`desktop CASEFILE: toggle should hide, got ${d.toggle}`); record(d.trace!=='none','desktop CASEFILE: content should remain visible');
  await context.close();
}

// Narrative mobile: six canonical narrative units + signature visual stay readable.
{
  const context=await browser.newContext({viewport:{width:390,height:844},deviceScaleFactor:1}); const page=await context.newPage();
  await page.goto(`${base}${narrativeRoute}?${bust()}`,{waitUntil:'domcontentloaded',timeout:45000}); await waitForNarrativeReader(page);
  const initial=await page.evaluate((ids)=>{
    const visible=(el)=>{if(!el)return false;const s=getComputedStyle(el),r=el.getBoundingClientRect();return s.display!=='none'&&s.visibility!=='hidden'&&r.width>0&&r.height>0};
    const units=ids.map((id)=>document.getElementById(id));
    const visual=document.querySelector('[data-raven-visual="narrative"]');
    const img=visual?.querySelector('img');
    const caption=visual?.querySelector('figcaption');
    const firstSplit=units[0]?.querySelector('.narrative-locked-split');
    const splitColumns=firstSplit?getComputedStyle(firstSplit).gridTemplateColumns.split(/\s+/).filter(Boolean).length:0;
    return {
      unitCount:units.filter(Boolean).length,
      allUnitsVisible:units.every(visible),
      copyPreserved:units.filter((unit)=>unit?.dataset?.copyLock==='preserved').length,
      allStructured:units.every((unit)=>Boolean(unit?.querySelector('.narrative-locked-claim')&&unit?.querySelector('.narrative-locked-record'))),
      splitColumns,
      visualVisible:visible(visual),
      visualSrc:img?.getAttribute('src')||'',
      editorialLabel:(caption?.textContent||'').includes('Editorial illustration'),
      bodyHeight:document.documentElement.scrollHeight
    };
  },narrativeIds);
  record(initial.unitCount===narrativeIds.length,`mobile Narrative: expected ${narrativeIds.length} units, got ${initial.unitCount}`);
  record(initial.allUnitsVisible,'mobile Narrative: one or more canonical narrative units hidden');
  record(initial.copyPreserved===narrativeIds.length,`mobile Narrative: copy-lock preserved on ${initial.copyPreserved}/${narrativeIds.length} units`);
  record(initial.allStructured,'mobile Narrative: Claim/Record structural wrappers missing');
  record(initial.splitColumns===1,`mobile Narrative: expected one-column split, got ${initial.splitColumns}`);
  record(initial.visualVisible,'mobile Narrative: signature visual missing or hidden');
  record(initial.visualSrc.endsWith('raven-narrative-rm13b-v1-web.svg'),`mobile Narrative: unexpected visual source ${initial.visualSrc}`);
  record(initial.editorialLabel,'mobile Narrative: editorial-illustration boundary missing');
  record(initial.bodyHeight<19000,`mobile Narrative: excessively tall (${initial.bodyHeight}px)`);
  await page.goto(`${base}${narrativeRoute}?${bust()}#rm13b`,{waitUntil:'domcontentloaded',timeout:45000}); await waitForNarrativeReader(page); await page.waitForTimeout(350);
  const target=await page.evaluate(()=>{const c=document.getElementById('rm13b'),s=c?getComputedStyle(c):null,r=c?.getBoundingClientRect();return {targeted:location.hash==='#rm13b',visible:Boolean(c&&s&&s.display!=='none'&&s.visibility!=='hidden'&&r.width>0&&r.height>0)}});
  record(target.targeted&&target.visible,'mobile Narrative: direct #rm13b deep link should expose the narrative unit');
  await context.close();
}

// Narrative desktop remains fully readable with all six units and signature visual.
{
  const context=await browser.newContext({viewport:{width:1440,height:900},deviceScaleFactor:1}); const page=await context.newPage();
  await page.goto(`${base}${narrativeRoute}?${bust()}`,{waitUntil:'domcontentloaded',timeout:45000}); await waitForNarrativeReader(page);
  const d=await page.evaluate((ids)=>{
    const visible=(el)=>{if(!el)return false;const s=getComputedStyle(el),r=el.getBoundingClientRect();return s.display!=='none'&&s.visibility!=='hidden'&&r.width>0&&r.height>0};
    const units=ids.map((id)=>document.getElementById(id));
    const visual=document.querySelector('[data-raven-visual="narrative"]');
    const firstSplit=units[0]?.querySelector('.narrative-locked-split');
    return {
      count:units.filter(Boolean).length,
      allVisible:units.every(visible),
      copyPreserved:units.filter((unit)=>unit?.dataset?.copyLock==='preserved').length,
      splitColumns:firstSplit?getComputedStyle(firstSplit).gridTemplateColumns.split(/\s+/).filter(Boolean).length:0,
      visualVisible:visible(visual)
    };
  },narrativeIds);
  record(d.count===narrativeIds.length&&d.allVisible,'desktop Narrative: canonical narrative units should remain fully readable');
  record(d.copyPreserved===narrativeIds.length,`desktop Narrative: copy-lock preserved on ${d.copyPreserved}/${narrativeIds.length} units`);
  record(d.splitColumns===2,`desktop Narrative: expected two-column Claim/Record split, got ${d.splitColumns}`);
  record(d.visualVisible,'desktop Narrative: signature visual should remain visible');
  await context.close();
}

await browser.close();
console.log(JSON.stringify({feature:'Raven Reader V8',failures},null,2));
if(failures.length) throw new Error(`Raven Reader V8 QA failed:\n${failures.join('\n')}`);
