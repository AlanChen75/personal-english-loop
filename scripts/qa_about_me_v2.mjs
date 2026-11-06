// Actual browser checks against a built player, not mocked audio or page content.
import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const runtime=process.env.RUNTIME_NODE_MODULES;
if (!runtime) throw new Error('Set RUNTIME_NODE_MODULES to the installed workspace runtime');
const {chromium}=require(path.join(runtime,'playwright'));
const base=process.argv[2];
const output=process.argv[3];
if (!base || !output) throw new Error('Usage: qa_about_me_v2.mjs <player-url> <output-dir>');
await fs.mkdir(output,{recursive:true});
const browser=await chromium.launch({headless:true});
const results=[];
try {
 for (const width of [375,768,1280]) {
  const context=await browser.newContext({viewport:{width,height:900},serviceWorkers:'block'});
  const page=await context.newPage();
  const errors=[];
  page.on('pageerror',error=>errors.push(error.message));
  await page.goto(base+'#about-me',{waitUntil:'networkidle'});
  assert.equal(await page.locator('#page-select option').count(),6);
  assert.equal(await page.locator('.sentence').count(),4);
  assert.match(await page.locator('#page-title').innerText(),/我是誰/);
  assert.equal(await page.locator('#previous-item').isDisabled(),true);
  await page.waitForFunction(()=>Number.isFinite(document.querySelector('audio').duration));
  for (const speed of ['0.8','0.9','1']) {
   await page.locator(`[data-speed="${speed}"]`).click();
   assert.equal(await page.locator('audio').evaluate(a=>a.playbackRate),Number(speed));
  }
  // Real media decoding/playback; intentionally no claim of human pronunciation review.
  await page.locator('audio').evaluate(async a=>{await a.play();});
  await page.waitForFunction(()=>document.querySelector('audio').currentTime>0.2);
  const cues=await page.evaluate(()=>activeItems()[0].sentence_cues);
  // Verify actual timeupdate events during playback. Python's local static server
  // does not support byte ranges, so seeking there can reset media time to zero.
  for (let i=0;i<cues.length;i++) {
   const cue=cues[i];
   await page.waitForFunction(text=>document.querySelector('.sentence.is-speaking')?.textContent===text,cue.text);
   assert.equal(await page.locator('.sentence.is-speaking').innerText(),cue.text);
  }
  await page.locator('audio').evaluate(a=>a.pause());
  const geometry=await page.evaluate(()=>{
   const selectors=['#page-title','#player-desk','.controls','#collection-select'];
   return {pageOverflow:document.documentElement.scrollWidth>innerWidth+1,
     elements:selectors.map(selector=>{const e=document.querySelector(selector);const r=e.getBoundingClientRect();
      return {selector,overflow:e.scrollWidth>e.clientWidth+1,outside:r.left<0||r.right>innerWidth+1};})};
  });
  assert.equal(geometry.pageOverflow,false);
  assert.ok(geometry.elements.every(x=>!x.overflow&&!x.outside),JSON.stringify(geometry));
  await page.screenshot({path:path.join(output,`about-${width}.png`),fullPage:false});
  // Native mobile select is hidden on wide screens; change event is the same code path.
  await page.locator('#page-select').evaluate(e=>{e.value='5';e.dispatchEvent(new Event('change',{bubbles:true}));});
  assert.match(await page.locator('#page-title').innerText(),/接下來想做什麼/);
  assert.equal(await page.locator('#next-item').isDisabled(),true);
  await page.locator('#previous-item').click();
  assert.match(await page.locator('#page-title').innerText(),/最近做了什麼/);
  await page.locator('#next-item').click();
  await page.locator('#repeat-all').click();
  await page.locator('audio').evaluate(a=>a.dispatchEvent(new Event('ended')));
  assert.match(await page.locator('#page-title').innerText(),/我是誰/);
  await page.locator('audio').evaluate(a=>a.pause());
  assert.deepEqual(errors,[]);
  results.push({width,units:6,sentence_cues:4,playback:true,repeat_wrap:true,geometry});
  await context.close();
 }
 await fs.writeFile(path.join(output,'report.json'),JSON.stringify(results,null,2)+'\n');
 console.log(JSON.stringify(results));
} finally {await browser.close();}
