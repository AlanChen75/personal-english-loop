// Read-only browser acceptance for the approved v11 release; no audio mocks.
import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
if (!process.env.RUNTIME_NODE_MODULES) throw new Error('Set RUNTIME_NODE_MODULES');
const {chromium}=require(path.join(process.env.RUNTIME_NODE_MODULES,'playwright'));
const [base,output]=process.argv.slice(2);
if (!base||!output) throw new Error('Usage: qa_automation_v11.mjs <url> <output-dir>');
const pack=JSON.parse(await fs.readFile(new URL('../practice-materials/automation2026/extension-v11.json',import.meta.url),'utf8'));
await fs.mkdir(output,{recursive:true});
const browser=await chromium.launch({headless:true});
try {
 const reports=await Promise.all([375,768,1280].map(async width=>{
  const context=await browser.newContext({viewport:{width,height:900},serviceWorkers:'block'});
  try {
   const page=await context.newPage();
   const errors=[];
   page.on('pageerror',e=>errors.push(e.message));
   await page.goto(base+'#automation-2026',{waitUntil:'networkidle'});
   assert.equal(await page.locator('#page-select option').count(),16);
   const collections=await page.evaluate(()=>JSON.parse(JSON.stringify(window.eval('collections'))));
   assert.deepEqual(collections.map(c=>c.items.length),[16,12,6,100]);
   for (const item of pack.overrides) {
    assert.equal(collections[0].items[item.slide-1].transcript,item.display_transcript);
   }
   for (const number of [3,5,6,8,9,10,12]) {
    await page.locator('#page-select').evaluate((e,n)=>{e.value=String(n-1);e.dispatchEvent(new Event('change',{bubbles:true}));},number);
    await page.waitForFunction(()=>Number.isFinite(document.querySelector('audio').duration));
    // Sentence spans are separated visually by CSS; compare their actual text.
    assert.equal((await page.locator('#transcript .sentence').allTextContents()).join(' '),pack.overrides[number-1].display_transcript);
    assert.ok(await page.locator('audio').evaluate(a=>a.duration>0&&a.currentSrc.includes('?v=')));
    await page.waitForFunction(()=>document.querySelector('#slide-image').naturalWidth>0);
   }
   await page.locator('#page-select').evaluate(e=>{e.value='9';e.dispatchEvent(new Event('change',{bubbles:true}));});
   await page.waitForFunction(()=>Number.isFinite(document.querySelector('audio').duration));
   for (const speed of ['0.8','0.9','1']) {
    await page.locator(`[data-speed="${speed}"]`).click();
    assert.equal(await page.locator('audio').evaluate(a=>a.playbackRate),Number(speed));
   }
   const cues=collections[0].items[9].sentence_cues;
   assert.ok(cues.some(c=>c.text==='We do this extra analysis after selection.'));
   await page.locator('audio').evaluate(async a=>{await a.play();});
   for (const cue of cues) {
    await page.waitForFunction(text=>document.querySelector('.sentence.is-speaking')?.textContent===text,cue.text,{timeout:25000});
   }
   await page.locator('audio').evaluate(a=>a.pause());
   await page.locator('#page-title').scrollIntoViewIfNeeded();
   const geometry=await page.evaluate(()=>({
    pageOverflow:document.documentElement.scrollWidth>innerWidth+1,
    elements:['#page-title','#player-desk','.controls','#collection-select','#slide-image'].map(selector=>{
     const e=document.querySelector(selector),r=e.getBoundingClientRect();
     return {selector,overflow:e.scrollWidth>e.clientWidth+1,outside:r.left<0||r.right>innerWidth+1};
    })
   }));
   assert.equal(geometry.pageOverflow,false);
   assert.ok(geometry.elements.every(e=>!e.overflow&&!e.outside),JSON.stringify(geometry));
   await page.screenshot({path:path.join(output,`automation-${width}.png`)});
   await page.locator('#next-item').click();
   assert.match(await page.locator('#page-title').innerText(),/What the evidence supports/);
   await page.locator('audio').evaluate(a=>a.pause());
   await page.locator('#page-select').evaluate(e=>{e.value='15';e.dispatchEvent(new Event('change',{bubbles:true}));});
   await page.locator('#repeat-all').click();
   await page.locator('audio').evaluate(a=>a.dispatchEvent(new Event('ended')));
   assert.match(await page.locator('#page-title').innerText(),/Engineering Bounds/);
   await page.locator('audio').evaluate(a=>a.pause());
   assert.deepEqual(errors,[]);
   return {width,changed_audio_metadata:7,transcripts:12,real_playback_cues:cues.length,repeat_wrap:true,geometry};
  } finally {await context.close();}
 }));
 await fs.writeFile(path.join(output,'report.json'),JSON.stringify(reports,null,2)+'\n');
 console.log(JSON.stringify(reports));
} finally {await browser.close();}
