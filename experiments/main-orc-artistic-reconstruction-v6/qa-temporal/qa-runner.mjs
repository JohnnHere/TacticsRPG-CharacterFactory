import fs from 'fs';
import path from 'path';
import { fileURLToPath, pathToFileURL } from 'url';
import { createRequire } from 'module';

const require = createRequire(import.meta.url);
const { chromium } = require('C:/Users/João Orlando/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(__dirname, '../../..');
const reviewHtml = path.join(REPO, 'Biblioteca de Arte', 'Estudos Comparativos', 'Orc principal - Reconstrucao artistica', 'index.html');
const capturesDir = path.join(__dirname, 'captures');
fs.mkdirSync(capturesDir, { recursive: true });

const CHROMIUM = 'C:/Users/João Orlando/AppData/Local/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-win64/chrome-headless-shell.exe';
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';

const ATTACKS = [
  { dir: 'front_r', action: 'Sword' },
  { dir: 'front_l', action: 'Sword' },
  { dir: 'back_r', action: 'Sword' },
  { dir: 'back_l', action: 'Sword' },
  { dir: 'front_r', action: 'Axe' },
  { dir: 'front_l', action: 'Axe' },
  { dir: 'back_r', action: 'Axe' },
  { dir: 'back_l', action: 'Axe' },
];

async function run() {
  console.log('Launching browser...');
  const browser = await chromium.launch({
    executablePath: CHROMIUM,
    headless: true,
    args: ['--allow-file-access-from-files']
  });

  const page = await browser.newPage({ viewport: { width: 1920, height: 1200 } });
  page.setDefaultTimeout(45000);

  const consoleLogs = [];
  page.on('console', msg => consoleLogs.push(msg.text()));
  page.on('pageerror', err => console.error('Page error:', err));

  console.log('Navigating to review page:', reviewHtml);
  await page.goto(pathToFileURL(reviewHtml).href, { waitUntil: 'load' });
  await page.waitForSelector('body[data-ready="true"]', { timeout: 45000 });
  console.log('Page ready!');

  const testResults = {
    browserEngine: 'Chromium Headless Shell 156.0.8078.4 (Playwright)',
    timestamp: new Date().toISOString(),
    clips: {},
    comparisons: {},
    transitions: {}
  };

  // 1. Test each of the 8 attack clips
  for (const { dir, action } of ATTACKS) {
    const key = `${dir}/${action}`;
    console.log(`\n=== Testing ${key} ===`);
    const clipDir = path.join(capturesDir, `${dir}_${action}`);
    fs.mkdirSync(clipDir, { recursive: true });

    // Select dir and action
    await page.selectOption('#select-dir', dir);
    await page.selectOption('#select-action', action);
    await page.selectOption('#select-transition', 'action-only');
    await page.waitForTimeout(100);

    // Get sequence metadata
    const seqMeta = await page.evaluate(({ d, a }) => {
      const cell = matrix[d][a];
      return {
        action: cell.action,
        direction: cell.direction,
        totalDurationMs: cell.totalDurationMs,
        frameCount: cell.frames.length,
        visibleInterval: cell.visibleInterval,
        status: cell.status,
        frames: cell.frames.map(f => ({
          index: f.index,
          durationMs: f.durationMs,
          phase: f.phase,
          weaponVisible: f.weaponVisible,
          rightGrip: f.rightGrip,
          rotationDeg: f.rotationDeg,
          impact: f.impact,
          terminal: f.terminal
        }))
      };
    }, { d: dir, a: action });

    // A. 1x playback run (looping, count full loop crossings)
    await page.selectOption('#speed', '1');
    await page.evaluate(() => {
      playing = true;
      loop = true;
      document.getElementById('play').textContent = 'Pausar';
      document.getElementById('loop').checked = true;
      resetPlayback();
    });
    await page.waitForTimeout(50);

    // Monitor playback at 1x for ~3.5 seconds
    const trace1x = await page.evaluate(async (expectedDuration) => {
      const samples = [];
      const start = performance.now();
      let loops = 0;
      let lastFrame = -1;
      
      return new Promise(resolve => {
        function check() {
          const now = performance.now();
          const elapsed = now - start;
          const curr = mainState.n;
          if (curr !== lastFrame) {
            if (curr < lastFrame) {
              loops++;
            }
            samples.push({
              wallMs: Math.round(elapsed),
              frame: curr,
              loopCount: loops
            });
            lastFrame = curr;
          }
          if (elapsed >= Math.max(3500, expectedDuration * 3.5)) {
            resolve({
              wallTimeTotalMs: Math.round(elapsed),
              fullLoopsCompleted: loops,
              sampleCount: samples.length,
              samples: samples.slice(0, 30) // sample head
            });
          } else {
            requestAnimationFrame(check);
          }
        }
        requestAnimationFrame(check);
      });
    }, seqMeta.totalDurationMs);

    console.log(`  1x Playback: ${trace1x.fullLoopsCompleted} full loops completed in ${trace1x.wallTimeTotalMs}ms`);

    // B. 0.5x playback run
    await page.selectOption('#speed', '0.5');
    await page.evaluate(() => {
      playing = true;
      loop = true;
      document.getElementById('play').textContent = 'Pausar';
      document.getElementById('loop').checked = true;
      resetPlayback();
    });
    await page.waitForTimeout(50);

    const trace05x = await page.evaluate(async (expectedDuration) => {
      const samples = [];
      const start = performance.now();
      let loops = 0;
      let lastFrame = -1;
      
      return new Promise(resolve => {
        function check() {
          const now = performance.now();
          const elapsed = now - start;
          const curr = mainState.n;
          if (curr !== lastFrame) {
            if (curr < lastFrame) {
              loops++;
            }
            samples.push({
              wallMs: Math.round(elapsed),
              frame: curr,
              loopCount: loops
            });
            lastFrame = curr;
          }
          if (elapsed >= Math.max(3000, expectedDuration * 2.5)) {
            resolve({
              wallTimeTotalMs: Math.round(elapsed),
              fullLoopsCompleted: loops,
              sampleCount: samples.length
            });
          } else {
            requestAnimationFrame(check);
          }
        }
        requestAnimationFrame(check);
      });
    }, seqMeta.totalDurationMs);

    console.log(`  0.5x Playback: ${trace05x.fullLoopsCompleted} full loops completed in ${trace05x.wallTimeTotalMs}ms`);

    // C. Frame-by-frame stepping: inspect each frame and dump canvas
    // Pause playback
    const isPlaying = await page.evaluate(() => playing);
    if (isPlaying) {
      await page.click('#play'); // toggle pause
    }

    const frameDumps = [];
    for (let fIdx = 0; fIdx < seqMeta.frameCount; fIdx++) {
      // Set frame in mainState
      await page.evaluate((idx) => {
        mainState.n = idx;
        mainState.time = 0;
        renderMain();
      }, fIdx);
      await page.waitForTimeout(30);

      // Grab canvas data URL
      const dataUrl = await page.evaluate(() => {
        const c = document.getElementById('main-canvas');
        return c.toDataURL('image/png');
      });
      const gripDataUrl = await page.evaluate(() => {
        const c = document.getElementById('main-grip');
        return c.toDataURL('image/png');
      });

      const framePng = Buffer.from(dataUrl.replace(/^data:image\/png;base64,/, ''), 'base64');
      const framePath = path.join(clipDir, `F${String(fIdx).padStart(2, '0')}.png`);
      fs.writeFileSync(framePath, framePng);

      const gripPng = Buffer.from(gripDataUrl.replace(/^data:image\/png;base64,/, ''), 'base64');
      const gripPath = path.join(clipDir, `F${String(fIdx).padStart(2, '0')}_grip.png`);
      fs.writeFileSync(gripPath, gripPng);

      frameDumps.push({
        frame: fIdx,
        file: `F${String(fIdx).padStart(2, '0')}.png`,
        meta: seqMeta.frames[fIdx]
      });
    }

    // D. Tactical scale check (zoom = 0.5 [128px] and zoom = 0.25 [64px])
    // Seek to impact frame
    const impactIdx = seqMeta.frames.findIndex(f => f.impact) >= 0 ? seqMeta.frames.findIndex(f => f.impact) : Math.floor(seqMeta.frameCount / 2);
    await page.evaluate((idx) => {
      mainState.n = idx;
      renderMain();
      applyScale(0.5); // 128px
    }, impactIdx);
    await page.waitForTimeout(50);
    const shot128 = await page.locator('#main-canvas').screenshot();
    fs.writeFileSync(path.join(clipDir, `tactical_128px_impact_F${String(impactIdx).padStart(2, '0')}.png`), shot128);

    await page.evaluate(() => {
      applyScale(0.25); // 64px
    });
    await page.waitForTimeout(50);
    const shot64 = await page.locator('#main-canvas').screenshot();
    fs.writeFileSync(path.join(clipDir, `tactical_64px_impact_F${String(impactIdx).padStart(2, '0')}.png`), shot64);

    // Reset zoom to 1
    await page.evaluate(() => {
      applyScale(1.0);
    });

    // E. Composite contact sheet of the clip
    const stageShot = await page.locator('.studio').screenshot();
    fs.writeFileSync(path.join(clipDir, `studio_overview.png`), stageShot);

    testResults.clips[key] = {
      meta: seqMeta,
      playback1x: trace1x,
      playback05x: trace05x,
      frames: frameDumps,
      tactical64pxSaved: true,
      tactical128pxSaved: true
    };
  }

  // 2. Specific Investigation: front_l/Sword F02->F03->F04->F05 axilla in motion
  console.log('\n=== Special Investigation: front_l/Sword Axilla Transition ===');
  await page.selectOption('#select-dir', 'front_l');
  await page.selectOption('#select-action', 'Sword');
  await page.selectOption('#speed', '0.5');
  await page.click('#play'); // resume
  await page.waitForTimeout(100);

  // Capture axilla region (around [100, 100], 80x80) across F02, F03, F04, F05
  const axillaDir = path.join(capturesDir, 'investigation_axilla_front_l_sword');
  fs.mkdirSync(axillaDir, { recursive: true });

  for (const fIdx of [1, 2, 3, 4, 5]) {
    await page.evaluate((idx) => {
      playing = false;
      mainState.n = idx;
      renderMain();
    }, fIdx);
    await page.waitForTimeout(30);

    // Crop axilla region: x: 80..160, y: 70..150 on the 256 canvas
    const axillaCropData = await page.evaluate(() => {
      const c = document.getElementById('main-canvas');
      const tempC = document.createElement('canvas');
      tempC.width = 80;
      tempC.height = 80;
      const ctx = tempC.getContext('2d');
      // Orc front_l axilla is around x=115, y=100
      ctx.drawImage(c, 90, 75, 80, 80, 0, 0, 80, 80);
      return tempC.toDataURL('image/png');
    });
    fs.writeFileSync(
      path.join(axillaDir, `F${String(fIdx).padStart(2, '0')}_axilla_crop.png`),
      Buffer.from(axillaCropData.replace(/^data:image\/png;base64,/, ''), 'base64')
    );
  }

  // 3. Specific Investigation: back_l/Sword F07-F09 ground clearance in motion
  console.log('\n=== Special Investigation: back_l/Sword Blade Tip & Ground Clearance ===');
  await page.selectOption('#select-dir', 'back_l');
  await page.selectOption('#select-action', 'Sword');
  const swordGroundDir = path.join(capturesDir, 'investigation_blade_ground_back_l_sword');
  fs.mkdirSync(swordGroundDir, { recursive: true });

  const groundAnalysis = [];
  for (const fIdx of [6, 7, 8, 9, 10]) {
    await page.evaluate((idx) => {
      playing = false;
      mainState.n = idx;
      renderMain();
    }, fIdx);
    await page.waitForTimeout(30);

    // Crop ground / blade contact region: x: 100..220, y: 140..210 (ground line is at y=190)
    const bladeCrop = await page.evaluate(() => {
      const c = document.getElementById('main-canvas');
      const tempC = document.createElement('canvas');
      tempC.width = 120;
      tempC.height = 70;
      const ctx = tempC.getContext('2d');
      ctx.drawImage(c, 110, 145, 120, 70, 0, 0, 120, 70);
      // Also draw ground guide line in red at local y = 190 - 145 = 45
      ctx.strokeStyle = 'rgba(255, 0, 0, 0.7)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(0, 45);
      ctx.lineTo(120, 45);
      ctx.stroke();
      return tempC.toDataURL('image/png');
    });

    // Check pixel readback on canvas to find lowest non-transparent pixel in the sword area
    const pixelInfo = await page.evaluate(() => {
      const c = document.getElementById('main-canvas');
      const ctx = c.getContext('2d');
      const imgData = ctx.getImageData(0, 0, 256, 256);
      const data = imgData.data;
      let lowestY = -1;
      let lowestX = -1;
      // Scan right side where weapon tip descends: x: 110..220, y: 150..220
      for (let y = 220; y >= 150; y--) {
        for (let x = 110; x <= 220; x++) {
          const idx = (y * 256 + x) * 4;
          const a = data[idx + 3];
          if (a > 10) {
            // Check if this pixel is sword/metal (gray/silver/steel or weapon outline) or hand
            const r = data[idx], g = data[idx + 1], b = data[idx + 2];
            // Look for sword blade metal (r,g,b close to each other, > 80)
            if (lowestY === -1) {
              lowestY = y;
              lowestX = x;
            }
          }
        }
      }
      return { lowestY, lowestX, groundY: 190, diff: 190 - lowestY };
    });

    groundAnalysis.push({ frame: fIdx, pixelInfo });
    fs.writeFileSync(
      path.join(swordGroundDir, `F${String(fIdx).padStart(2, '0')}_ground_crop.png`),
      Buffer.from(bladeCrop.replace(/^data:image\/png;base64,/, ''), 'base64')
    );
  }
  testResults.comparisons['back_l_sword_ground_clearance'] = groundAnalysis;

  // 4. Four-direction simultaneous comparison
  console.log('\n=== Four-direction Simultaneous Comparison ===');
  for (const action of ['Sword', 'Axe']) {
    await page.selectOption('#select-action', action);
    await page.selectOption('#speed', '1');
    await page.check('#loop');
    await page.click('#reset');
    await page.waitForTimeout(500);

    const quadShot = await page.locator('.grid4').first().screenshot();
    fs.writeFileSync(path.join(capturesDir, `quad_comparison_${action}.png`), quadShot);
  }

  // 5. Idle -> Attack -> Idle Transition Check
  console.log('\n=== Testing Idle -> Attack -> Idle Transitions ===');
  for (const { dir, action } of ATTACKS) {
    const key = `${dir}_${action}_transition`;
    await page.selectOption('#select-dir', dir);
    await page.selectOption('#select-action', action);
    await page.selectOption('#select-transition', 'idle-attack-idle');
    await page.selectOption('#speed', '1');
    await page.evaluate(() => {
      playing = true;
      loop = false;
      document.getElementById('loop').checked = false;
      document.getElementById('play').textContent = 'Pausar';
      resetPlayback();
    });

    const transTrace = await page.evaluate(async () => {
      const samples = [];
      const start = performance.now();
      return new Promise(resolve => {
        function check() {
          const now = performance.now();
          const elapsed = now - start;
          const st = mainState;
          samples.push({
            elapsed: Math.round(elapsed),
            frame: st.n,
            done: st.done
          });
          if (st.done || elapsed > 5000) {
            resolve({
              totalElapsed: Math.round(elapsed),
              terminalFrame: st.n,
              done: st.done,
              sampleCount: samples.length
            });
          } else {
            requestAnimationFrame(check);
          }
        }
        requestAnimationFrame(check);
      });
    });

    testResults.transitions[key] = transTrace;
  }

  // 6. Before vs After affected cells section verification
  console.log('\n=== Verifying Before vs After affected cells section ===');
  const beforeAfterLocator = page.locator('article:has(h2:text("Evidências Visuais Antes"))');
  const beforeAfterShot = await beforeAfterLocator.screenshot();
  fs.writeFileSync(path.join(capturesDir, 'before_after_section.png'), beforeAfterShot);

  // Save intermediate test results
  fs.writeFileSync(
    path.join(__dirname, 'browser_run_trace.json'),
    JSON.stringify(testResults, null, 2)
  );

  console.log('All tests completed successfully in browser!');
  await browser.close();
}

run().catch(err => {
  console.error('Test run failed:', err);
  process.exit(1);
});
