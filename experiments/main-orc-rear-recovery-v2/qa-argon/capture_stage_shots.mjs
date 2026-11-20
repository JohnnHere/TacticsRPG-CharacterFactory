import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const { chromium } = require('C:/Users/João Orlando/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');

const ROOT = process.cwd();
const SHOT_DIR = path.join(ROOT, 'experiments/main-orc-rear-recovery-v2/qa-argon/playback-shots');
const CHROMIUM = 'C:/Users/João Orlando/AppData/Local/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-win64/chrome-headless-shell.exe';
const reviewHtml = path.join(ROOT, 'Biblioteca de Arte/Estudos Comparativos/Orc principal - Recuperacao traseira/index.html');

const targets = [
  { dir: 'back_l', action: 'Sword', steps: 5, zoom: '1', name: 'stage_back_l_Sword_F05_1x.png' },
  { dir: 'back_l', action: 'Sword', steps: 7, zoom: '1', name: 'stage_back_l_Sword_F07_unarmed_violation.png' },
  { dir: 'back_r', action: 'Axe', steps: 1, zoom: '1', name: 'stage_back_r_Axe_F01_double_axe.png' },
  { dir: 'back_r', action: 'Axe', steps: 4, zoom: '1', name: 'stage_back_r_Axe_F04_disconnected_arm.png' },
  { dir: 'back_r', action: 'Axe', steps: 5, zoom: '1', name: 'stage_back_r_Axe_F05_double_forearm.png' },
  { dir: 'back_l', action: 'Axe', steps: 3, zoom: '1', name: 'stage_back_l_Axe_F03_right_shoulder_hook.png' },
  { dir: 'back_l', action: 'Unarmed', steps: 3, zoom: '1', name: 'stage_back_l_Unarmed_F03_baseline_reuse.png' },
  { dir: 'front_r', action: 'Defeat', steps: 4, zoom: '1', name: 'stage_front_r_Defeat_F04_terminal.png' },
  { dir: 'back_r', action: 'Walk', steps: 2, zoom: '0.5', name: 'stage_back_r_Walk_F02_game_scale_05x.png' },
  { dir: 'back_r', action: 'Hit', steps: 2, zoom: '0.5', name: 'stage_back_r_Hit_F02_game_scale_05x.png' },
];

const browser = await chromium.launch({
  executablePath: CHROMIUM,
  headless: true,
  args: ['--allow-file-access-from-files'],
});
const hardTimer = setTimeout(() => {
  browser.close().catch(() => {}).finally(() => process.exit(1));
}, 45000);

try {
  const page = await browser.newPage({ viewport: { width: 1680, height: 1050 } });
  await page.goto(pathToFileURL(reviewHtml).href, { waitUntil: 'load', timeout: 30000 });
  await page.waitForSelector('body[data-ready="true"]', { timeout: 30000 });

  for (const t of targets) {
    await page.selectOption('#select-dir', t.dir);
    await page.selectOption('#select-action', t.action);
    await page.selectOption('#zoom', t.zoom);
    await page.click('#reset');
    for (let s = 0; s < t.steps; s++) {
      await page.click('#step-next');
    }
    await page.evaluate(() => {
      document.getElementById('main-canvas').scrollIntoView({ block: 'center' });
    });
    await page.waitForTimeout(80);
    await page.screenshot({ path: path.join(SHOT_DIR, t.name) });
  }
} finally {
  clearTimeout(hardTimer);
  await browser.close();
}
console.log('Captured stage screenshots.');
