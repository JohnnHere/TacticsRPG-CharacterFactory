import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';
import { decode } from '../../../src/images.mjs';

const require = createRequire(import.meta.url);
const { chromium } = require('C:\\Users\\João Orlando\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\node\\node_modules\\playwright');
const Q = path.resolve('experiments\\main-orc-rear-recovery-v2\\qa-copilot');
const manifest = JSON.parse(fs.readFileSync('characters\\orc-v1\\source\\rear-recovery-v2\\candidate28manifest.json', 'utf8'));
fs.mkdirSync(path.join(Q, 'playback'), { recursive: true });
const browser = await chromium.launch({
  executablePath: 'C:\\Users\\João Orlando\\AppData\\Local\\ms-playwright\\chromium_headless_shell-1248\\chrome-headless-shell-win64\\chrome-headless-shell.exe',
  headless: true, args: ['--allow-file-access-from-files']
});
const deadline = setTimeout(() => { console.error('Playback review exceeded 300s'); void browser.close(); process.exitCode = 1; }, 300000);
const integrationOnly = process.argv.includes('--integration-only');
const prior = integrationOnly ? JSON.parse(fs.readFileSync(path.join(Q, 'playback-verification.json'), 'utf8')) : null;
if (prior) fs.copyFileSync(path.join(Q, 'playback-verification.json'), path.join(Q, 'playback-initial-path-assumption.json'));
const result = { identity: 'GPT Sol6.1 via GitHub Copilot', freezeId: JSON.parse(fs.readFileSync('experiments\\main-orc-rear-recovery-v2\\delivery-freeze.json')).freezeId, runs: prior?.runs ?? [], integrated: [], failures: [] };
if (prior) result.harnessCorrection = 'Initial path-equality assertion incorrectly rejected valid staged preview copies. Rechecked actual staged RGBA and timings against canonical frames; retained the 48 successful actual playback runs without rerunning them. Initial result preserved.';
try {
  const page = await browser.newPage({ viewport: { width: 1600, height: 1000 } });
  page.on('pageerror', e => result.failures.push(e.message));
  page.on('requestfailed', r => result.failures.push(`${r.url()}: ${r.failure()?.errorText}`));
  await page.goto(pathToFileURL(path.resolve('Biblioteca de Arte\\Estudos Comparativos\\Orc principal - Recuperacao traseira\\index.html')).href);
  await page.waitForSelector('body[data-ready="true"]');
  await page.click('#play');
  for (const cell of manifest.cells) {
    await page.selectOption('#select-dir', cell.direction);
    await page.selectOption('#select-action', cell.action);
    const r = await page.evaluate(() => ({
      source: matrix[selectedDir][selectedAction].clipJson,
      first: matrix[selectedDir][selectedAction].frames[0].png,
      painted: document.querySelector('#main-canvas').getContext('2d').getImageData(0, 0, 256, 256).data.some((x, i) => i % 4 === 3 && x > 0),
      status: matrix[selectedDir][selectedAction].status,
      frames: matrix[selectedDir][selectedAction].frames.map(f => ({ png: f.png, durationMs: f.durationMs }))
    }));
    const clip = JSON.parse(fs.readFileSync(cell.clipJson, 'utf8'));
    const base = path.dirname('Biblioteca de Arte\\Estudos Comparativos\\Orc principal - Recuperacao traseira\\index.html');
    let exactFrames = 0;
    for (let i = 0; i < r.frames.length; i++) {
      const staged = decode(path.resolve(base, decodeURI(r.frames[i].png))).image;
      const canonical = decode(path.resolve(clip.frames[i].png)).image;
      if (staged.width === canonical.width && staged.height === canonical.height && staged.data.equals(canonical.data) && r.frames[i].durationMs === clip.frames[i].durationMs) exactFrames++;
    }
    const canonicalContentMatches = r.frames.length === clip.frames.length && exactFrames === clip.frames.length;
    if (!r.painted || !canonicalContentMatches || r.status !== cell.status) result.failures.push(`Integrated cell ${cell.cellId} failed source/paint/status check`);
    result.integrated.push({ cell: cell.cellId, ...r, exactFrames, canonicalContentMatches });
  }
  const clips = integrationOnly ? [] : manifest.cells.filter(c => c.isAffected || c.action === 'Hit');
  for (const cell of clips) {
    await page.selectOption('#select-dir', cell.direction);
    await page.selectOption('#select-action', cell.action);
    await page.evaluate(() => {
      if (!document.querySelector('#copilot-evidence')) {
        const box = document.createElement('div');
        box.id = 'copilot-evidence';
        box.style.cssText = 'background:#202a30;padding:12px;position:fixed;inset:0;z-index:9999;overflow:auto;pointer-events:none;color:white;font:14px monospace';
        box.innerHTML = '<div id="copilot-title"></div><div style="display:flex;gap:12px"><div><p>Actual main canvas (full 256)</p><canvas id="copilot-live" width="256" height="256"></canvas></div><div><p>Native center 128</p><canvas id="copilot-native" width="128" height="128"></canvas></div><div><p>Approximate game 64</p><canvas id="copilot-game" width="64" height="64"></canvas></div></div><div id="copilot-films"></div>';
        document.body.append(box);
      }
      document.querySelector('#copilot-films').innerHTML = '';
    });
    for (const speed of ['1', '0.75', '0.5']) {
      await page.selectOption('#speed', speed);
      await page.click('#reset', { force: true });
      await page.evaluate(({ id, speed }) => {
        window.qaRun = { id, speed, start: performance.now(), samples: [], images: [], last: -1 };
        const title = document.createElement('p');
        title.textContent = `${id} @ ${speed}x: actual RAF transitions; zero-based frames; full canvas at 0.5 display scale`;
        const film = document.createElement('canvas');
        film.width = 8 * 144; film.height = 154;
        film.style.background = '#303d44';
        document.querySelector('#copilot-films').append(title, film);
        window.qaRun.film = film;
        const observedRun = window.qaRun;
        const observe = () => {
          const r = observedRun;
          if (!r || r.stopped) return;
          const info = document.querySelector('#main-info').textContent;
          const m = /Quadro (\d+)\/(\d+)/.exec(info);
          const n = m ? Number(m[1]) - 1 : -1;
          const c = document.querySelector('#main-canvas');
          for (const [id, size, crop] of [['copilot-live', 256, false], ['copilot-native', 128, true], ['copilot-game', 64, true]]) {
            const ctx = document.getElementById(id).getContext('2d');
            ctx.imageSmoothingEnabled = false;
            ctx.clearRect(0, 0, size, size);
            if (crop) ctx.drawImage(c, 64, 64, 128, 128, 0, 0, size, size);
            else ctx.drawImage(c, 0, 0);
          }
          document.querySelector('#copilot-title').textContent = `${r.id} @ ${r.speed}x | ${info}`;
          if (n !== r.last) {
            r.samples.push({ frame: n, elapsedMs: Math.round(performance.now() - r.start), terminal: info.includes('TERMINAL HOLD') });
            if (r.images[n] === undefined && n >= 0) {
              const ctx = r.film.getContext('2d');
              ctx.imageSmoothingEnabled = false;
              ctx.drawImage(c, 0, 0, 256, 256, n * 144, 0, 128, 128);
              ctx.fillStyle = '#fff'; ctx.font = '12px monospace';
              ctx.fillText(`F${n} ${r.samples.at(-1).elapsedMs}ms`, n * 144, 146);
              r.images[n] = true;
            }
            r.last = n;
          }
          requestAnimationFrame(observe);
        };
        requestAnimationFrame(observe);
        playing = true;
        document.querySelector('#play').textContent = 'Pausar';
      }, { id: cell.cellId, speed });
      const clip = JSON.parse(fs.readFileSync(cell.clipJson, 'utf8'));
      const total = clip.frames.reduce((n, f) => n + f.durationMs, 0);
      await page.waitForTimeout(Math.ceil(total * 2.25 / Number(speed)) + 150);
      const run = await page.evaluate(() => {
        playing = false;
        document.querySelector('#play').textContent = 'Reproduzir';
        const r = window.qaRun; r.stopped = true;
        const { film, images, ...data } = r;
        return { ...data, observedFrames: images.flatMap((v, i) => v ? [i] : []), finalInfo: document.querySelector('#main-info').textContent };
      });
      run.expectedFrames = clip.frames.length;
      run.fullCycleObserved = run.observedFrames.length === clip.frames.length;
      run.loopObserved = run.samples.some((s, i) => i > 0 && s.frame < run.samples[i - 1].frame);
      run.terminalHeld = cell.action === 'Defeat' ? !run.loopObserved && run.finalInfo.includes('TERMINAL HOLD') : null;
      if (!run.fullCycleObserved || (cell.action === 'Defeat' ? !run.terminalHeld : !run.loopObserved)) result.failures.push(`Playback coverage ${cell.cellId} @ ${speed}`);
      result.runs.push(run);
    }
    await page.locator('#copilot-evidence').screenshot({ path: path.join(Q, 'playback', `${cell.cellId.replace('/', '_')}.png`) });
    console.log(`Captured full cycles ${cell.cellId} at 1/.75/.5`);
  }
  const images = await page.evaluate(() => [...document.querySelectorAll('img')].map(i => ({ src: i.src, decoded: i.complete && i.naturalWidth > 0 })));
  if (images.some(i => !i.decoded)) result.failures.push('Undecoded review images');
  result.decodedImages = images.length;
  await page.close();
} catch (error) {
  result.failures.push(error.stack ?? error.message);
  console.error(error);
} finally {
  clearTimeout(deadline);
  await browser.close();
  result.status = result.failures.length ? 'FAIL' : 'PASS';
  fs.writeFileSync(path.join(Q, 'playback-verification.json'), JSON.stringify(result, null, 2) + '\n');
}
console.log(JSON.stringify({ status: result.status, cells: result.integrated.length, runs: result.runs.length, failures: result.failures }, null, 2));
if (result.failures.length) process.exitCode = 1;
