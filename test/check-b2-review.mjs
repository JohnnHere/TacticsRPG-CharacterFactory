import path from 'node:path';
import { createRequire } from 'module';
import { pathToFileURL } from 'url';
const require = createRequire(import.meta.url);
const { chromium } = require('C:/Users/João Orlando/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const CHROMIUM = 'C:/Users/João Orlando/AppData/Local/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-win64/chrome-headless-shell.exe';
const page = path.resolve('experiments/main-orc-hybrid-weapon-04b2/review/index.html');
const browser = await chromium.launch({ executablePath: CHROMIUM });
const tab = await browser.newPage({ viewport: { width: 1500, height: 1100 } });
const errors = [];
tab.on('pageerror', e => errors.push(e.message));
await tab.goto(pathToFileURL(page).href);
await tab.waitForTimeout(1500);
const snap = () => tab.evaluate(() => ({
  frames: document.querySelectorAll('#frames button').length,
  loaded: Array.from(document.querySelectorAll('#views img')).filter(i => i.naturalWidth > 0).length,
  of: document.querySelectorAll('#views img').length,
  hands: Array.from(document.querySelectorAll('#hands img')).filter(i => i.naturalWidth > 0).length,
  allImgsLoaded: Array.from(document.querySelectorAll('img')).every(i => i.complete && i.naturalWidth > 0),
  totalImgs: document.querySelectorAll('img').length,
  status: document.getElementById('status').textContent,
}));
console.log('inicial:', JSON.stringify(await snap()));
await tab.click('#frames button:nth-child(9)'); await tab.waitForTimeout(500);
console.log('F08:', JSON.stringify(await snap()));
await tab.click('#next'); await tab.waitForTimeout(300);
console.log('proximo:', JSON.stringify(await snap()));
await tab.click('[data-zoom="4"]'); await tab.waitForTimeout(200);
console.log('zoom 4x:', await tab.evaluate(() => document.querySelector('#views img').style.transform));
await tab.click('[data-zoom="2"]'); await tab.waitForTimeout(200);
await tab.click('#play-half'); await tab.waitForTimeout(800); await tab.click('#pause');
const finalSnap = await snap();
console.log('apos play:', JSON.stringify(finalSnap));
console.log('erros:', errors.length, errors.slice(0, 2).join(' | '));
await tab.screenshot({ path: 'experiments/main-orc-hybrid-weapon-04b2/review/shot.png' });
await browser.close();
if (errors.length || !finalSnap.allImgsLoaded || finalSnap.loaded !== 6 || finalSnap.hands !== 2) {
  process.exit(1);
}
