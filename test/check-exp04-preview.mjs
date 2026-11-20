import path from 'node:path';
import { createRequire } from 'module';
import { pathToFileURL } from 'url';
const require = createRequire(import.meta.url);
const { chromium } = require('C:/Users/João Orlando/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const CHROMIUM = 'C:/Users/João Orlando/AppData/Local/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-win64/chrome-headless-shell.exe';
const page = path.resolve('experiments/main-orc-hybrid-weapon-04/pipeline/dist/editor/hybrid-weapon-04/822a6b68ef2b23b8a766/preview.html');
const browser = await chromium.launch({ executablePath: CHROMIUM });
const tab = await browser.newPage({ viewport: { width: 1400, height: 950 } });
const errors = [];
tab.on('pageerror', e => errors.push(e.message));
await tab.goto(pathToFileURL(page).href);
await tab.waitForTimeout(2000);
const info = await tab.evaluate(() => ({
  title: document.title,
  images: Array.from(document.images).map(i => ({ src: i.getAttribute('src'), ok: i.naturalWidth > 0 })),
  text: document.body.innerText.slice(0, 300),
}));
const broken = info.images.filter(i => !i.ok);
console.log('title:', info.title);
console.log('images:', info.images.length, '| broken:', broken.length);
console.log('errors:', errors.length, errors.slice(0,2).join(' | '));
console.log('text:', info.text.replace(/\s+/g,' ').slice(0,200));
await tab.screenshot({ path: 'experiments/main-orc-hybrid-weapon-04/pipeline-preview-shot.png' });
await browser.close();