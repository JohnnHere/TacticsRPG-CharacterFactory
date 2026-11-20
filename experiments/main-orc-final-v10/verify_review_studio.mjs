import path from "node:path";
import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";

const require = createRequire(import.meta.url);
const { chromium } = require("C:/Users/João Orlando/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright");
const CHROMIUM = "C:/Users/João Orlando/AppData/Local/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-win64/chrome-headless-shell.exe";

const pagePath = path.resolve("Biblioteca de Arte/Estudos Comparativos/Orc principal - Candidato Final e Arquitetura C/index.html");
const shotPath = "C:/Users/João Orlando/.gemini/antigravity/brain/5fe480f6-d661-411c-b120-c9742e395c32/scratch/audit/review_studio_shot.png";

const browser = await chromium.launch({ executablePath: CHROMIUM });
const tab = await browser.newPage({ viewport: { width: 1640, height: 1280 } });
const errors = [];
tab.on("pageerror", e => errors.push(e.message));
tab.on("console", m => { if (m.type() === "error") errors.push(m.text()); });

await tab.goto(pathToFileURL(pagePath).href);
await tab.waitForTimeout(1200);

async function checkAllImgs(stepLabel) {
  const res = await tab.evaluate(() => {
    const imgs = Array.from(document.querySelectorAll("img"));
    const broken = imgs.filter(i => !i.complete || i.naturalWidth === 0).map(i => i.getAttribute("src"));
    return { total: imgs.length, loaded: imgs.length - broken.length, broken };
  });
  console.log(`[${stepLabel}] loaded=${res.loaded}/${res.total}`, res.broken.length ? `BROKEN: ${res.broken[0]}` : "OK");
  if (res.broken.length > 0) throw new Error(`Broken images at ${stepLabel}: ${res.broken.join(", ")}`);
}

await tab.click("#btn-pause");
await tab.click("#sword-frames button:nth-child(9)"); // F08 contact
await tab.click("#axe-frames button:nth-child(7)");   // F06 impact
await tab.waitForTimeout(300);
await checkAllImgs("initial-F08-F06");

// Exercise all Sword comparison modes
for (const mode of ["after-before", "layers", "weapons", "ab"]) {
  await tab.click(`[data-swmode="${mode}"]`);
  await tab.waitForTimeout(250);
  await checkAllImgs(`sword-mode-${mode}`);
}

// Exercise all Body actions
for (const act of ["Unarmed", "Walk", "Hit", "Idle", "Combo", "Defeat"]) {
  await tab.click(`[data-bact="${act}"]`);
  await tab.waitForTimeout(250);
  await checkAllImgs(`body-act-${act}`);
}

// Exercise tactical scale 0.5x and back to 1x
await tab.click('[data-scale="0.5"]');
await tab.waitForTimeout(150);
await tab.click('[data-scale="1"]');
await tab.waitForTimeout(150);

await tab.screenshot({ path: shotPath, fullPage: false });
await browser.close();

if (errors.length > 0) {
  console.error("Browser errors:", errors);
  process.exit(1);
}
console.log("Review studio verified cleanly with 0 errors.");
