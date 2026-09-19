(() => {
  if (window.__RAVEN_VISUALS_V1__) return;
  window.__RAVEN_VISUALS_V1__ = true;
  const path = location.pathname;
  const q=(s,r=document)=>r.querySelector(s);
  const ensureCss=()=>{if(q('link[data-raven-visuals-v1]'))return;const l=document.createElement('link');l.rel='stylesheet';l.href='/raventrace-my/assets/css/raven-visuals-v1.css?v=1.0.1';l.dataset.ravenVisualsV1='true';document.head.appendChild(l)};
  ensureCss();
  const make=(src,alt,caption,variant='evidence')=>{const wrap=document.createElement('div');wrap.className=`raven-visual raven-visual--${variant} raven-visual--wide`;wrap.innerHTML=`<figure><img src="${src}" alt="${alt}" loading="lazy" decoding="async" width="1200" height="675"><figcaption><strong>Visual explainer · RAVEN-Trace.</strong> ${caption}<span class="raven-visual-note">Editorial illustration. Ia menerangkan rekod; ia bukan dokumen atau bukti asal.</span></figcaption></figure>`;return wrap};
  const insertAfter=(target,node)=>target?.parentNode?.insertBefore(node,target.nextSibling);
  if(path.includes('/investigations/rci-tabung-haji/narratives/')){
    const target=q('#rm13b') || q('.case-section:nth-of-type(2)');
    if(target && !q('[data-raven-visual="narrative"]')){const v=make('/raventrace-my/assets/visuals/raven-narrative-rm13b-v1-web.svg','Visual Raven yang membezakan dakwaan RM13 bilion dicuri daripada rekod RM10.2 bilion beban kerajaan/UJSB dan RM2.6 bilion impairment TH, serta jurang naratif loss tidak sama dengan theft.','Claim → record → narrative gap → verdict.','narrative');v.dataset.ravenVisual='narrative';target.parentNode.insertBefore(v,target);}
  }
  if(path.includes('/investigations/rci-tabung-haji/money/')){
    const target=q('.case-section');
    if(target && !q('[data-raven-visual="money"]')){const v=make('/raventrace-my/assets/visuals/raven-money-rm13b-v1-web.svg','Visual pecahan hampir RM13 bilion kepada RM10.2 bilion government/UJSB burden dan RM2.6 bilion TH impairments, dengan peringatan bahawa kerugian bukan automatik kecurian.','Pecahan angka rasmi untuk mengelakkan category collapse.','evidence');v.dataset.ravenVisual='money';insertAfter(target.querySelector('h2')||target,v);}
  }
  const isCase=path==='/raventrace-my/investigations/rci-tabung-haji/'||path.endsWith('/investigations/rci-tabung-haji/index.html');
  const isUpdates=path.includes('/investigations/rci-tabung-haji/updates/');
  const isCountStory=path.includes('/news/2026/09/11/empat-atau-lima-didakwa-rekod-tidak-seragam/');
  if(isCase||isUpdates){
    const target=isCase?(q('#briefing')||q('#revision')):(q('.section-content .case-section')||q('article'));
    if(target && !q('[data-raven-visual="six-eight-five"]')){const v=make('/raventrace-my/assets/visuals/raven-6-8-5-v1-web.svg','Visual Raven menunjukkan enam actual arraignments, lapan isu dalam formulasi SPRM dan lima kertas siasatan yang masih aktif setakat 19 September 2026.','People, issues dan active papers ialah kategori berbeza; pertuduhan dan siasatan bukan sabitan.','evidence');v.dataset.ravenVisual='six-eight-five';if(isCase)insertAfter(target.querySelector('h2')||target,v);else target.insertBefore(v,target.firstChild);}
  }
  if(isCountStory){
    const target=q('.story-body')||q('article');
    if(target && !q('[data-raven-visual="four-five"]')){const v=make('/raventrace-my/assets/visuals/raven-4-vs-5-v1-web.svg','Historical visual Raven comparing four court-confirmed charge-readings with five in an agency statement at the 11–13 September checkpoint.','Historical discrepancy retained as an audit trail; later court developments superseded the count.','disputed');v.dataset.ravenVisual='four-five';target.insertBefore(v,target.firstChild);}
  }
})();
