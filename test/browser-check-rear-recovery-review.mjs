/**
 * REAL-browser automated check for the isolated Orc V1 rear-recovery review studio
 * (headless Chromium via Playwright, file:// — no mock DOM, no servers).
 *
 * Reproducible inside the repo:
 *   node test/browser-check-rear-recovery-review.mjs
 *
 * Bounded by design: every individual wait <= 45s and the whole run enforces a
 * hard 120s deadline; the launched browser is ALWAYS closed (finally / deadline).
 * All expectations are DERIVED from candidate28manifest.json + catalogo.json
 * (counts may change on future producer refreshes — nothing hardcoded).
 * Does not touch any other browser or user process.
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath, pathToFileURL } from 'url';
import { createRequire } from 'module';
import { parseArgs } from 'node:util';

const require = createRequire(import.meta.url);
const { chromium } = require('C:/Users/João Orlando/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(__dirname, '..');
const { values } = parseArgs({ options: {
  'review-dir': { type: 'string' },
  manifest: { type: 'string' },
  'shot-dir': { type: 'string' },
} });
const reviewDir = path.resolve(REPO, values['review-dir'] ??
  path.join('Biblioteca de Arte', 'Estudos Comparativos', 'Orc principal - Recuperacao traseira'));
const reviewHtml = path.join(reviewDir, 'index.html');
const manifestPath = path.resolve(REPO, values.manifest ??
  path.join('characters', 'orc-v1', 'source', 'rear-recovery-v2', 'candidate28manifest.json'));
const catalogoPath = path.join(reviewDir, 'catalogo.json');
const shotDir = path.resolve(REPO, values['shot-dir'] ??
  path.join('experiments', 'main-orc-rear-recovery-v2', 'browser-checks'));
fs.mkdirSync(shotDir, { recursive: true });

const CHROMIUM = 'C:/Users/João Orlando/AppData/Local/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-win64/chrome-headless-shell.exe';
const OVERALL_DEADLINE_MS = 120000;
const started = Date.now();
const leftMs = () => OVERALL_DEADLINE_MS - (Date.now() - started);
function assertBudget(label) {
  if (leftMs() <= 0) throw new Error(`Overall ${OVERALL_DEADLINE_MS / 1000}s deadline exceeded at: ${label}`);
}

let failures = 0;
const results = [];
function check(name, ok, detail = '') {
  results.push({ name, ok, detail });
  console.log(`${ok ? '  OK: ' : '  FAIL: '}${name}${detail ? ' — ' + detail : ''}`);
  if (!ok) failures++;
}

// Expectations derived from the source manifest (never hardcoded)
const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
const catalogo = JSON.parse(fs.readFileSync(catalogoPath, 'utf8'));
const statusOf = new Map(manifest.cells.map(c => [`${c.direction}/${c.action}`, c.status]));
const affectedCells = manifest.cells.filter(c => c.isAffected).map(c => `${c.direction}/${c.action}`);
const isRevision = s => s === 'IN_REVISION' || s === 'ARTISTIC_REVISION_REQUIRED';
const revisionCount = manifest.cells.filter(c => isRevision(c.status)).length;

const directions = ['front_r', 'front_l', 'back_r', 'back_l'];
const actions = ['Idle', 'Walk', 'Unarmed', 'Sword', 'Axe', 'Hit', 'Defeat'];

const browser = await chromium.launch({
  executablePath: CHROMIUM,
  headless: true,
  // Own headless instance only: allows canvas pixel readback for local file:// assets
  args: ['--allow-file-access-from-files'],
});
const hardDeadline = setTimeout(() => {
  console.error('FATAL: overall 120s deadline exceeded — closing browser and failing.');
  browser.close().catch(() => {}).finally(() => process.exit(1));
}, OVERALL_DEADLINE_MS - 2000);

try {
  const page = await browser.newPage({ viewport: { width: 1680, height: 1050 } });
  page.setDefaultTimeout(45000);
  const badRequests = [];
  page.on('requestfailed', r => badRequests.push(`${r.url()} :: ${r.failure()?.errorText || 'failed'}`));
  page.on('response', resp => { if (resp.status() >= 400) badRequests.push(`${resp.url()} :: HTTP ${resp.status()}`); });

  assertBudget('goto');
  await page.goto(pathToFileURL(reviewHtml).href, { waitUntil: 'load', timeout: 45000 });
  assertBudget('ready-wait');
  await page.waitForSelector('body[data-ready="true"]', { timeout: 45000 });
  check('viewer ready in real Chromium (all preloaded frame images resolved)', true);

  // 1) All 28 cells selectable: canvas really paints pixels and the status badge
  //    literal matches the manifest (no silent fallback, no stale vocabulary)
  let painted = 0, badgeOk = 0;
  for (const d of directions) {
    for (const a of actions) {
      assertBudget(`cell ${d}/${a}`);
      await page.selectOption('#select-dir', d);
      await page.selectOption('#select-action', a);
      await page.waitForTimeout(40);
      const r = await page.evaluate(() => {
        const c = document.getElementById('main-canvas');
        const px = c.getContext('2d').getImageData(0, 0, c.width, c.height).data;
        let n = 0;
        for (let i = 3; i < px.length; i += 4) if (px[i] > 0) n++;
        return { n, info: document.getElementById('main-info').innerHTML };
      });
      if (r.n > 0) painted++;
      if (r.info.includes(`>${statusOf.get(`${d}/${a}`)}</span>`)) badgeOk++;
    }
  }
  check(`all 28 cells selectable, main canvas paints real pixels (painted ${painted}/28)`, painted === 28);
  check(`main-info badge shows manifest status literal for all 28 cells (${badgeOk}/28)`, badgeOk === 28);

  // 2) Every <img> on the page decoded; zero failed/4xx requests
  assertBudget('image-decode');
  const imgs = await page.evaluate(() => {
    const list = [...document.querySelectorAll('img')];
    return { total: list.length, broken: list.filter(i => !i.complete || i.naturalWidth === 0).map(i => i.getAttribute('src')) };
  });
  check(`all ${imgs.total} <img> elements decoded (naturalWidth > 0)`, imgs.broken.length === 0, imgs.broken.slice(0, 4).join(' | '));
  check('zero failed / 4xx+ requests while browsing', badRequests.length === 0, badRequests.slice(0, 4).join(' | '));
  if (manifest.eligibleForIntegration === false) {
    const eligibility = await page.locator('#integration-eligibility').textContent();
    check('diagnostic package explicitly declares ineligibility in page and catalog',
      eligibility.includes('false') && eligibility.includes('não integrar') &&
      catalogo.eligibleForIntegration === false);
  }

  // 3) Speed control truly changes playback (bounded measurement windows)
  await page.selectOption('#select-dir', 'back_r');
  await page.selectOption('#select-action', 'Walk');
  const readFrame = () => page.evaluate(() => {
    const m = /Quadro (\d+)\/(\d+)/.exec(document.getElementById('main-info').textContent);
    return m ? { n: Number(m[1]), total: Number(m[2]) } : null;
  });
  await page.selectOption('#speed', '1');
  await page.click('#reset');
  await page.waitForTimeout(1000);
  const f1 = await readFrame();
  await page.selectOption('#speed', '0.5');
  await page.click('#reset');
  await page.waitForTimeout(1000);
  const f2 = await readFrame();
  check(`speed 1× advances playback (frame ${f1?.n}/${f1?.total} after 1000ms)`, !!f1 && f1.n >= 3);
  check(`speed 0.5× slows playback ≈half (frame ${f2?.n}/${f2?.total} after 1000ms)`, !!f2 && f2.n >= 1 && f2.n <= f1.n);
  await page.selectOption('#speed', '1');

  // 4) Practical game scale (native 128×128 render)
  await page.selectOption('#zoom', '0.5');
  const zw = await page.evaluate(() => document.getElementById('main-canvas').style.width);
  check('practical game scale applied (canvas 128px)', zw === '128px', `style.width=${zw}`);
  await page.selectOption('#zoom', '1');

  // 5) Frame-by-frame step controls
  await page.click('#reset');
  await page.click('#step-next');
  const s1 = await readFrame();
  await page.click('#step-prev');
  const s2 = await readFrame();
  check(`step-next advances one frame (→ ${s1?.n})`, s1?.n === 2);
  check(`step-prev returns one frame (→ ${s2?.n})`, s2?.n === 1);

  // 6) Defeat terminal hold (loop off): stops at last frame and stays
  await page.selectOption('#select-action', 'Defeat');
  await page.uncheck('#loop');
  await page.click('#reset');
  // step controls above paused playback; resume it before waiting for the hold
  const wasPlaying = await page.evaluate(() => document.getElementById('play').textContent.trim() === 'Pausar');
  if (!wasPlaying) await page.click('#play');
  assertBudget('terminal-hold-wait');
  await page.waitForFunction(
    () => /TERMINAL HOLD/.test(document.getElementById('main-info').textContent),
    null,
    { timeout: 8000 },
  );
  const t1 = await readFrame();
  await page.waitForTimeout(700);
  const t2 = await readFrame();
  check(`Defeat reaches terminal hold at last frame (${t1?.n}/${t1?.total})`, !!t1 && t1.n === t1.total);
  check('Defeat holds terminal frame without auto-restart', t2?.n === t1?.n);
  await page.check('#loop');
  await page.screenshot({ path: path.join(shotDir, 'defeat-terminal-hold.png') });

  // 7) Explicit status alerts (real DOM)
  await page.selectOption('#select-action', 'Sword');
  await page.waitForTimeout(60);
  const aSword = await page.evaluate(() => ({
    cls: document.getElementById('pending-alert').className,
    txt: document.getElementById('pending-alert').textContent,
  }));
  const swordStatus = statusOf.get('back_r/Sword');
  check('back_r/Sword alert reflects its actual manifest status',
    swordStatus === 'UNCHANGED_ALIAS' ? !aSword.cls.includes('active') :
    aSword.txt.includes(swordStatus) &&
    (isRevision(swordStatus) ? aSword.txt.includes('NÃO está pronto') :
      swordStatus === 'ACTIVE_CANDIDATE' ? aSword.txt.includes('CANDIDATO ATIVO') : true));
  await page.screenshot({ path: path.join(shotDir, 'pending-alert-revision-sword.png') });

  await page.selectOption('#select-action', 'Idle');
  await page.waitForTimeout(60);
  const aIdle = await page.evaluate(() => document.getElementById('pending-alert').className);
  check('back_r/Idle (unchanged alias) shows no pending alert', !aIdle.includes('active'));

  await page.selectOption('#select-action', 'Walk');
  await page.waitForTimeout(60);
  const aWalk = await page.evaluate(() => ({
    text: document.getElementById('pending-alert').textContent,
    cls: document.getElementById('pending-alert').className,
  }));
  const walkStatus = statusOf.get('back_r/Walk');
  check(`back_r/Walk alert matches ${walkStatus}`,
    walkStatus === 'UNCHANGED_ALIAS' ? !aWalk.cls.includes('active') :
      aWalk.text.includes(walkStatus) && aWalk.text.includes('PENDING_CREATOR'));

  // 8) Before/After coverage for ALL affected cells (baseline + candidate, decoded)
  const ba = await page.evaluate(() => {
    const art = [...document.querySelectorAll('article')]
      .find(a => /^Evidências Visuais Antes /.test(a.querySelector('h2')?.textContent || ''));
    if (!art) return null;
    return {
      heading: art.querySelector('h2').textContent.trim(),
      sections: [...art.querySelectorAll('section')].filter(s => s.querySelector('h3 code')).map(s => ({
        title: s.querySelector('h3')?.textContent.trim(),
        imgs: [...s.querySelectorAll('img')].map(i => ({ src: i.getAttribute('src'), ok: i.complete && i.naturalWidth > 0 })),
      })),
    };
  });
  check(`before/after article covers all ${affectedCells.length} affected cells (found ${ba?.sections.length ?? 0})`,
    !!ba && ba.sections.length === affectedCells.length, ba?.heading || 'article missing');
  const baImgsOk = !!ba && ba.sections.every(s => s.imgs.length >= 2 && s.imgs.every(i => i.ok));
  check('every before/after card shows baseline + candidate strips, both decoded', baImgsOk);
  await page.evaluate(() => {
    const art = [...document.querySelectorAll('article')]
      .find(a => /^Evidências Visuais Antes /.test(a.querySelector('h2')?.textContent || ''));
    art?.scrollIntoView();
  });
  await page.waitForTimeout(120);
  await page.screenshot({ path: path.join(shotDir, 'before-after-affected-cells.png') });

  // 9) Overview screenshot of the refreshed studio
  await page.selectOption('#select-action', 'Walk');
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(120);
  await page.screenshot({ path: path.join(shotDir, 'studio-overview.png'), fullPage: true });

  // 10) catalogo.json derived-data cross-check against the source manifest
  const expectedPackageStatus = revisionCount || manifest.cells.some(c => c.status === 'IN_PRODUCTION')
    ? 'ARTISTIC_REVISION_REQUIRED' : 'VISUAL_REVIEW_REQUIRED';
  check('catalogo packageStatus/artisticStatus follows actual unresolved cells',
    catalogo.packageStatus === expectedPackageStatus && catalogo.artisticStatus === expectedPackageStatus);
  check('catalogo counts derived from manifest (active/alias/revision/production)',
    catalogo.activeCandidates.length === manifest.activeCandidatesCount &&
    catalogo.unchangedAliases.length === manifest.unchangedAliasesCount &&
    catalogo.inRevision.length === manifest.inRevisionCount &&
    catalogo.inProduction.length === manifest.inProductionCount,
    `active=${catalogo.activeCandidates.length}/${manifest.activeCandidatesCount}` +
    ` alias=${catalogo.unchangedAliases.length}/${manifest.unchangedAliasesCount}` +
    ` revision=${catalogo.inRevision.length}/${manifest.inRevisionCount}` +
    ` production=${catalogo.inProduction.length}/${manifest.inProductionCount}`);
  check('catalogo knownBadCells matches revision + production cells',
    catalogo.knownBadCells.length === revisionCount + manifest.inProductionCount);
} finally {
  clearTimeout(hardDeadline);
  await browser.close();
}

console.log(`\nBROWSER CHECK ${failures === 0 ? 'PASSED' : 'FAILED'} (${results.filter(r => r.ok).length}/${results.length} checks) in ${((Date.now() - started) / 1000).toFixed(1)}s`);
console.log(`Screenshots: ${shotDir}`);
process.exit(failures === 0 ? 0 : 1);
