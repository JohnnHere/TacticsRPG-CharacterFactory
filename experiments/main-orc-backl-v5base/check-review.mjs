import fs from 'node:fs';import path from 'node:path';import{pathToFileURL}from'node:url';import{createRequire}from'node:module';
const require=createRequire(import.meta.url);const{chromium}=require('C:/Users/João Orlando/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const E='experiments/main-orc-backl-v5base';const errors=[];const checks=[];const browser=await chromium.launch({executablePath:'C:/Users/João Orlando/AppData/Local/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-win64/chrome-headless-shell.exe',headless:true});
try{const page=await browser.newPage({viewport:{width:1350,height:950}});page.on('pageerror',e=>errors.push(String(e)));await page.goto(pathToFileURL(path.resolve(E,'review.html')).href);await page.waitForFunction(()=>[...cache.values()].every(im=>im.complete&&im.naturalWidth>0));
for(const[cat,count]of[['0',14],['1',12]]){
 await page.selectOption('#category',cat);
 for(let i=0;i<count;i++){await page.locator('#frame').evaluate((e,v)=>{e.value=v;e.dispatchEvent(new Event('input'))},String(i));await page.waitForFunction(()=>document.querySelector('#hand').hidden||(document.querySelector('#hand').complete&&document.querySelector('#hand').naturalWidth>0));checks.push({category:cat,frame:i,imageLoaded:true});}
 for(const speed of ['1','0.75','0.5']){await page.selectOption('#speed',speed);await page.click('#play');await page.waitForFunction(()=>!running,{},{timeout:5000});const at=await page.locator('#frame').inputValue();if(+at!==count-1)throw Error('terminal');checks.push({category:cat,speed,oneShotTerminal:true});}
 await page.locator('#frame').evaluate(e=>{e.value='6';e.dispatchEvent(new Event('input'))});await page.check('#layersoff');await page.uncheck('#layersoff');await page.screenshot({path:E+'/browser-'+(cat==='0'?'sword':'axe')+'.png'});
}
if(errors.length)throw Error(errors.join('\n'));fs.writeFileSync(E+'/browser-check.json',JSON.stringify({status:'PASS',checks,pageErrors:errors},null,2));console.log('PASS: 26 frame views, 6 one-shot playback runs, layer toggle, screenshots');}finally{await browser.close()}

