import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';
import { pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const { chromium } = require('C:/Users/João Orlando/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');

const ROOT = process.cwd();
const QA_DIR = path.join(ROOT, 'experiments/main-orc-rear-recovery-v2/qa-argon');
const SHOT_DIR = path.join(QA_DIR, 'playback-shots');
fs.mkdirSync(SHOT_DIR, { recursive: true });

function readPng(filePath) {
  const buf = fs.readFileSync(filePath);
  let offset = 8;
  let width = 0;
  let height = 0;
  const idat = [];
  while (offset < buf.length) {
    const len = buf.readUInt32BE(offset);
    const type = buf.toString('ascii', offset + 4, offset + 8);
    const data = buf.subarray(offset + 8, offset + 8 + len);
    if (type === 'IHDR') {
      width = data.readUInt32BE(0);
      height = data.readUInt32BE(4);
    } else if (type === 'IDAT') {
      idat.push(data);
    } else if (type === 'IEND') {
      break;
    }
    offset += 12 + len;
  }
  const raw = zlib.inflateSync(Buffer.concat(idat));
  const stride = width * 4;
  const rgba = Buffer.alloc(width * height * 4);
  const paeth = (a, b, c) => {
    const p = a + b - c;
    const pa = Math.abs(p - a);
    const pb = Math.abs(p - b);
    const pc = Math.abs(p - c);
    if (pa <= pb && pa <= pc) return a;
    if (pb <= pc) return b;
    return c;
  };
  for (let y = 0; y < height; y++) {
    const filter = raw[y * (stride + 1)];
    const rowIn = y * (stride + 1) + 1;
    const rowOut = y * stride;
    for (let x = 0; x < stride; x++) {
      const b = raw[rowIn + x];
      const left = x >= 4 ? rgba[rowOut + x - 4] : 0;
      const up = y > 0 ? rgba[rowOut - stride + x] : 0;
      const upLeft = y > 0 && x >= 4 ? rgba[rowOut - stride + x - 4] : 0;
      let val = b;
      if (filter === 1) val = (b + left) & 0xff;
      else if (filter === 2) val = (b + up) & 0xff;
      else if (filter === 3) val = (b + ((left + up) >> 1)) & 0xff;
      else if (filter === 4) val = (b + paeth(left, up, upLeft)) & 0xff;
      rgba[rowOut + x] = val;
    }
  }
  return { width, height, rgba };
}

function bboxInRegion(img, x0 = 0, y0 = 0, x1 = img.width - 1, y1 = img.height - 1) {
  let minX = Infinity, minY = Infinity, maxX = -1, maxY = -1, count = 0;
  for (let y = Math.max(0, y0); y <= Math.min(img.height - 1, y1); y++) {
    for (let x = Math.max(0, x0); x <= Math.min(img.width - 1, x1); x++) {
      const idx = (y * img.width + x) * 4;
      if (img.rgba[idx + 3] > 0) {
        count++;
        if (x < minX) minX = x;
        if (y < minY) minY = y;
        if (x > maxX) maxX = x;
        if (y > maxY) maxY = y;
      }
    }
  }
  if (count === 0) return { count: 0, minX: null, minY: null, maxX: null, maxY: null, width: 0, height: 0, aspect: 0 };
  const width = maxX - minX + 1;
  const height = maxY - minY + 1;
  return { count, minX, minY, maxX, maxY, width, height, aspect: Number((width / height).toFixed(3)) };
}

function diffPixels(imgA, imgB) {
  let diffCount = 0;
  let minX = Infinity, minY = Infinity, maxX = -1, maxY = -1;
  for (let y = 0; y < imgA.height; y++) {
    for (let x = 0; x < imgA.width; x++) {
      const i = (y * imgA.width + x) * 4;
      const a0 = imgA.rgba[i + 3], b0 = imgB.rgba[i + 3];
      const same = (a0 === 0 && b0 === 0) || (
        a0 === b0 &&
        imgA.rgba[i] === imgB.rgba[i] &&
        imgA.rgba[i + 1] === imgB.rgba[i + 1] &&
        imgA.rgba[i + 2] === imgB.rgba[i + 2]
      );
      if (!same) {
        diffCount++;
        if (x < minX) minX = x;
        if (y < minY) minY = y;
        if (x > maxX) maxX = x;
        if (y > maxY) maxY = y;
      }
    }
  }
  return {
    diffCount,
    minX: diffCount ? minX : null,
    minY: diffCount ? minY : null,
    maxX: diffCount ? maxX : null,
    maxY: diffCount ? maxY : null,
  };
}

function connectedComponents(img) {
  const visited = new Uint8Array(img.width * img.height);
  const comps = [];
  const dirs = [
    [-1, -1], [0, -1], [1, -1],
    [-1, 0],           [1, 0],
    [-1, 1],  [0, 1],  [1, 1],
  ];
  for (let y = 0; y < img.height; y++) {
    for (let x = 0; x < img.width; x++) {
      const p = y * img.width + x;
      if (visited[p] || img.rgba[p * 4 + 3] === 0) continue;
      visited[p] = 1;
      const q = [[x, y]];
      let minX = x, maxX = x, minY = y, maxY = y, count = 0;
      while (q.length > 0) {
        const [cx, cy] = q.pop();
        count++;
        if (cx < minX) minX = cx;
        if (cx > maxX) maxX = cx;
        if (cy < minY) minY = cy;
        if (cy > maxY) maxY = cy;
        for (const [dx, dy] of dirs) {
          const nx = cx + dx, ny = cy + dy;
          if (nx < 0 || ny < 0 || nx >= img.width || ny >= img.height) continue;
          const np = ny * img.width + nx;
          if (!visited[np] && img.rgba[np * 4 + 3] > 0) {
            visited[np] = 1;
            q.push([nx, ny]);
          }
        }
      }
      comps.push({ count, minX, minY, maxX, maxY });
    }
  }
  comps.sort((a, b) => b.count - a.count);
  return comps;
}

// 1. Quantitative Defect Measurements
const defectEvidence = {};

// A. back_l/Sword body/native weapon contamination & detached components
const swordLDir = 'characters/orc-v1/source/rear-recovery-v2/back_l/Sword/Attack-representative-v1';
const swordLBase = readPng(path.join(ROOT, swordLDir, 'native/00.png'));
defectEvidence.back_l_Sword = {
  baseBbox: bboxInRegion(swordLBase),
  frames: [],
};
for (let i = 0; i < 8; i++) {
  const fn = String(i).padStart(2, '0') + '.png';
  const nat = readPng(path.join(ROOT, swordLDir, 'native', fn));
  const comp = readPng(path.join(ROOT, swordLDir, fn));
  const natComps = connectedComponents(nat);
  // Check right-hand / right-side extensions beyond base maxX (90) or lower-right dagger (x >= 80, y >= 65)
  const rightSideBeyondBase = bboxInRegion(nat, 91, 0, 127, 127);
  const rightHandDaggerRegion = bboxInRegion(nat, 80, 68, 118, 108);
  const topShoulderBladeRegion = bboxInRegion(nat, 18, 12, 62, 32);
  defectEvidence.back_l_Sword.frames.push({
    frame: i,
    nativePath: `${swordLDir}/native/${fn}`,
    compositePath: `${swordLDir}/${fn}`,
    nativeBbox: bboxInRegion(nat),
    compositeBbox: bboxInRegion(comp),
    nativeConnectedComponentsCount: natComps.length,
    detachedIslands: natComps.slice(1),
    rightSideBeyondBaseX90: rightSideBeyondBase,
    rightHandDaggerRegion_x80_118_y68_108: rightHandDaggerRegion,
    topLeftShoulderBladeRegion_x18_62_y12_32: topShoulderBladeRegion,
  });
}

// B. back_r/Axe body/native weapon contamination, amputated arm, and disconnected grip
const axeRDir = 'characters/orc-v1/source/rear-recovery-v2/back_r/Axe/Attack-representative-v1';
const axeRBase = readPng(path.join(ROOT, axeRDir, 'native/00.png'));
defectEvidence.back_r_Axe = {
  baseBbox: bboxInRegion(axeRBase),
  frames: [],
};
for (let i = 0; i < 8; i++) {
  const fn = String(i).padStart(2, '0') + '.png';
  const nat = readPng(path.join(ROOT, axeRDir, 'native', fn));
  const comp = readPng(path.join(ROOT, axeRDir, fn));
  const bodyLayer = readPng(path.join(ROOT, axeRDir, 'layers/body', fn));
  const wfLayer = readPng(path.join(ROOT, axeRDir, 'layers/weaponFront', fn));
  const hfLayer = readPng(path.join(ROOT, axeRDir, 'layers/handFront', fn));
  const natComps = connectedComponents(nat);
  const compComps = connectedComponents(comp);
  defectEvidence.back_r_Axe.frames.push({
    frame: i,
    nativePath: `${axeRDir}/native/${fn}`,
    compositePath: `${axeRDir}/${fn}`,
    nativeBbox: bboxInRegion(nat),
    compositeBbox: bboxInRegion(comp),
    nativeConnectedComponentsCount: natComps.length,
    nativeDetachedIslands: natComps.slice(1),
    compositeConnectedComponentsCount: compComps.length,
    compositeDetachedIslands: compComps.slice(1),
    bodyRightRegion_x148_191_y64_191: bboxInRegion(bodyLayer, 148, 64, 191, 191),
    weaponFrontBbox: bboxInRegion(wfLayer),
    handFrontBbox: bboxInRegion(hfLayer),
    upperCanvasShaftRegion_native_x75_115_y0_28: bboxInRegion(nat, 75, 0, 115, 28),
    rightSideAxeHeadRegion_native_x92_127_y15_68: bboxInRegion(nat, 92, 15, 127, 68),
    lowerRightHandleStubRegion_native_x88_115_y65_105: bboxInRegion(nat, 88, 65, 115, 105),
  });
}

// C. back_l/Axe residual opposite-shoulder axe fragments & grip check
const axeLDir = 'characters/orc-v1/source/rear-recovery-v2/back_l/Axe/Attack-representative-v1';
const axeLBase = readPng(path.join(ROOT, axeLDir, 'native/00.png'));
defectEvidence.back_l_Axe = {
  baseBbox: bboxInRegion(axeLBase),
  frames: [],
};
for (let i = 0; i < 8; i++) {
  const fn = String(i).padStart(2, '0') + '.png';
  const nat = readPng(path.join(ROOT, axeLDir, 'native', fn));
  const comp = readPng(path.join(ROOT, axeLDir, fn));
  const natComps = connectedComponents(nat);
  const compComps = connectedComponents(comp);
  defectEvidence.back_l_Axe.frames.push({
    frame: i,
    nativePath: `${axeLDir}/native/${fn}`,
    compositePath: `${axeLDir}/${fn}`,
    nativeBbox: bboxInRegion(nat),
    compositeBbox: bboxInRegion(comp),
    nativeConnectedComponentsCount: natComps.length,
    nativeDetachedIslands: natComps.slice(1),
    compositeConnectedComponentsCount: compComps.length,
    compositeDetachedIslands: compComps.slice(1),
    rightShoulderResidueBeyondX90: bboxInRegion(nat, 91, 0, 127, 60),
    upperRightPauldronSpikeHook_x82_106_y14_34: bboxInRegion(nat, 82, 14, 106, 34),
    diffVsBaseF00: i === 7 ? diffPixels(nat, axeLBase) : undefined,
  });
}

// D. back_r/Sword check
const swordRDir = 'characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2';
const swordRBase = readPng(path.join(ROOT, swordRDir, 'native/00.png'));
defectEvidence.back_r_Sword = {
  baseBbox: bboxInRegion(swordRBase),
  frames: [],
};
for (let i = 0; i < 8; i++) {
  const fn = String(i).padStart(2, '0') + '.png';
  const nat = readPng(path.join(ROOT, swordRDir, 'native', fn));
  const comp = readPng(path.join(ROOT, swordRDir, fn));
  const natComps = connectedComponents(nat);
  const compComps = connectedComponents(comp);
  defectEvidence.back_r_Sword.frames.push({
    frame: i,
    nativePath: `${swordRDir}/native/${fn}`,
    compositePath: `${swordRDir}/${fn}`,
    nativeBbox: bboxInRegion(nat),
    compositeBbox: bboxInRegion(comp),
    nativeConnectedComponentsCount: natComps.length,
    compositeConnectedComponentsCount: compComps.length,
    diffVsBaseF00: i === 7 ? diffPixels(nat, swordRBase) : undefined,
  });
}

// E. Defeat 4-direction terminal comparison & baseline vs candidate diff
const manifest = JSON.parse(fs.readFileSync(path.join(ROOT, 'characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json'), 'utf8'));
function getCellClip(dir, action) {
  const cell = manifest.cells.find(c => c.direction === dir && c.action === action);
  return JSON.parse(fs.readFileSync(path.join(ROOT, cell.clipJson), 'utf8'));
}

defectEvidence.Defeat = {};
for (const dir of ['front_r', 'front_l', 'back_r', 'back_l']) {
  const clip = getCellClip(dir, 'Defeat');
  const baseDir = `characters/orc-v1/source/complete-v1/${dir}/Defeat`;
  const stages = [];
  for (let i = 0; i < 5; i++) {
    const fn = String(i).padStart(2, '0') + '.png';
    const candCompPath = clip.frames[i].png;
    const candNatPath = clip.frames[i].nativePng;
    const candComp = readPng(path.join(ROOT, candCompPath));
    const baseComp = readPng(path.join(ROOT, baseDir, fn));
    const candNat = readPng(path.join(ROOT, candNatPath));
    stages.push({
      frame: i,
      candidateCompositePath: candCompPath,
      candidateNativePath: candNatPath,
      bboxComposite: bboxInRegion(candComp),
      bboxNative: bboxInRegion(candNat),
      diffVsBaselineCompleteV1: diffPixels(candComp, baseComp),
    });
  }
  defectEvidence.Defeat[dir] = stages;
}

// F. Unarmed 4-direction comparison
defectEvidence.Unarmed = {};
for (const dir of ['front_r', 'front_l', 'back_r', 'back_l']) {
  const clip = getCellClip(dir, 'Unarmed');
  const baseDir = `characters/orc-v1/source/complete-v1/${dir}/Unarmed`;
  const stages = [];
  for (let i = 0; i < 5; i++) {
    const fn = String(i).padStart(2, '0') + '.png';
    const candCompPath = clip.frames[i].png;
    const candNatPath = clip.frames[i].nativePng;
    const candComp = readPng(path.join(ROOT, candCompPath));
    const baseComp = readPng(path.join(ROOT, baseDir, fn));
    const candNat = readPng(path.join(ROOT, candNatPath));
    stages.push({
      frame: i,
      candidateCompositePath: candCompPath,
      candidateNativePath: candNatPath,
      bboxComposite: bboxInRegion(candComp),
      bboxNative: bboxInRegion(candNat),
      diffVsBaselineCompleteV1: diffPixels(candComp, baseComp),
    });
  }
  defectEvidence.Unarmed[dir] = stages;
}

fs.writeFileSync(
  path.join(QA_DIR, 'visual-defect-measurements.json'),
  JSON.stringify(defectEvidence, null, 2),
  'utf8'
);
console.log('Saved visual-defect-measurements.json');

// 2. Real Headless Chromium Playback across all 12 affected clips + 4 Hit clips at 1x, 0.75x, 0.5x and native + practical game scale
const CHROMIUM = 'C:/Users/João Orlando/AppData/Local/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-win64/chrome-headless-shell.exe';
const reviewHtml = path.join(ROOT, 'Biblioteca de Arte/Estudos Comparativos/Orc principal - Recuperacao traseira/index.html');

const clipsToPlay = [
  ['back_r', 'Walk'],
  ['back_l', 'Walk'],
  ['front_r', 'Unarmed'],
  ['front_l', 'Unarmed'],
  ['back_r', 'Unarmed'],
  ['back_l', 'Unarmed'],
  ['back_r', 'Sword'],
  ['back_l', 'Sword'],
  ['back_r', 'Axe'],
  ['back_l', 'Axe'],
  ['front_r', 'Defeat'],
  ['front_l', 'Defeat'],
  ['back_r', 'Defeat'],
  ['back_l', 'Defeat'],
  ['front_r', 'Hit'],
  ['front_l', 'Hit'],
  ['back_r', 'Hit'],
  ['back_l', 'Hit'],
];

const playbackReport = {
  browserExecutable: CHROMIUM,
  reviewPage: 'Biblioteca de Arte/Estudos Comparativos/Orc principal - Recuperacao traseira/index.html',
  speedsTested: ['1', '0.75', '0.5'],
  scalesTested: ['1', '0.5'],
  clips: [],
};

const browser = await chromium.launch({
  executablePath: CHROMIUM,
  headless: true,
  args: ['--allow-file-access-from-files'],
});
const hardTimer = setTimeout(() => {
  browser.close().catch(() => {}).finally(() => process.exit(1));
}, 110000);

try {
  const page = await browser.newPage({ viewport: { width: 1680, height: 1050 } });
  page.setDefaultTimeout(30000);
  await page.goto(pathToFileURL(reviewHtml).href, { waitUntil: 'load', timeout: 30000 });
  await page.waitForSelector('body[data-ready="true"]', { timeout: 30000 });

  for (const [dir, action] of clipsToPlay) {
    await page.selectOption('#select-dir', dir);
    await page.selectOption('#select-action', action);
    await page.check('#loop');
    const clipEntry = { id: `${dir}/${action}`, speedRuns: {}, scaleChecks: {} };

    for (const speed of ['1', '0.75', '0.5']) {
      await page.selectOption('#speed', speed);
      await page.selectOption('#zoom', '1');
      await page.click('#reset');
      const isPlaying = await page.evaluate(() => document.getElementById('play').textContent.trim() === 'Pausar');
      if (!isPlaying) await page.click('#play');

      const samples = [];
      for (let t = 0; t < 5; t++) {
        await page.waitForTimeout(140);
        const state = await page.evaluate(() => {
          const c = document.getElementById('main-canvas');
          const px = c.getContext('2d').getImageData(0, 0, c.width, c.height).data;
          let opaque = 0;
          for (let i = 3; i < px.length; i += 4) if (px[i] > 0) opaque++;
          const info = document.getElementById('main-info').textContent;
          const m = /Quadro (\d+)\/(\d+)/.exec(info);
          return {
            frame: m ? Number(m[1]) : null,
            total: m ? Number(m[2]) : null,
            opaquePixels: opaque,
            canvasCssWidth: c.style.width,
          };
        });
        samples.push(state);
      }
      clipEntry.speedRuns[speed] = {
        framesObserved: samples.map(s => s.frame),
        totalFrames: samples[0]?.total ?? null,
        allFramesPaintedOpaque: samples.every(s => s.opaquePixels > 0),
        minOpaquePixels: Math.min(...samples.map(s => s.opaquePixels)),
        maxOpaquePixels: Math.max(...samples.map(s => s.opaquePixels)),
      };
    }

    // Test practical game scale (zoom=0.5 -> 128px) and native (zoom=1 -> 256px)
    for (const zoom of ['1', '0.5']) {
      await page.selectOption('#zoom', zoom);
      await page.waitForTimeout(30);
      const zState = await page.evaluate(() => {
        const c = document.getElementById('main-canvas');
        const rect = c.getBoundingClientRect();
        return { styleWidth: c.style.width, clientWidth: Math.round(rect.width), clientHeight: Math.round(rect.height) };
      });
      clipEntry.scaleChecks[zoom] = zState;
    }

    // Capture screenshot of problematic frames in the viewer for key clips
    if (
      (dir === 'back_l' && action === 'Sword') ||
      (dir === 'back_r' && action === 'Axe') ||
      (dir === 'back_l' && action === 'Axe') ||
      (dir === 'front_r' && action === 'Defeat')
    ) {
      await page.selectOption('#zoom', '1');
      await page.click('#reset');
      // Step to frame 5 (1-based) or 6 where defect is super clear
      const targetSteps = action === 'Defeat' ? 4 : (dir === 'back_l' && action === 'Sword' ? 5 : 4);
      for (let s = 0; s < targetSteps; s++) {
        await page.click('#step-next');
      }
      await page.waitForTimeout(50);
      const shotPath = path.join(SHOT_DIR, `viewer_${dir}_${action}_step_${targetSteps + 1}.png`);
      await page.screenshot({ path: shotPath });
      clipEntry.viewerScreenshot = `experiments/main-orc-rear-recovery-v2/qa-argon/playback-shots/viewer_${dir}_${action}_step_${targetSteps + 1}.png`;
    }

    playbackReport.clips.push(clipEntry);
  }
} finally {
  clearTimeout(hardTimer);
  await browser.close();
}

fs.writeFileSync(
  path.join(QA_DIR, 'real-playback-verification.json'),
  JSON.stringify(playbackReport, null, 2),
  'utf8'
);
console.log(`Saved real-playback-verification.json (${playbackReport.clips.length} clips tested across 1x/0.75x/0.5x and 1x/0.5x zoom)`);
