/**
 * QA Independente Substituto — verificação técnica de pixels dos 3 ciclos frontais armados
 * front_l/Sword (13f/730ms), front_r/Axe (12f/1005ms), front_l/Axe (12f/1005ms)
 * Escrita restrita a experiments/main-orc-combat-rescue-v5/qa-sol/qa-front-three/
 * Somente leitura sobre characters/ e experiments/ (fontes do produtor).
 */
import fs from 'node:fs';
import path from 'node:path';
import { PNG } from 'pngjs';

const root = process.cwd();
const P = (p) => path.join(root, p);
const load = (p) => PNG.sync.read(fs.readFileSync(P(p)));

const cycles = [
  {
    id: 'front_l/Sword',
    dir: 'characters/orc-v1/source/combat-rescue-v5/grip-specialist/front_l-Sword-full',
    parentDir: 'characters/orc-v1/source/combat-rescue-v5/combat/front_l/Sword',
    mirrorOfDir: 'characters/orc-v1/source/combat-rescue-v5/grip-specialist/full-front-r-sword',
    expectFrames: 13,
    expectTotalMs: 730,
  },
  {
    id: 'front_r/Axe',
    dir: 'characters/orc-v1/source/combat-rescue-v5/grip-specialist/front_r-Axe-full',
    parentDir: 'characters/orc-v1/source/combat-rescue-v5/combat/front_r/Axe',
    mirrorOfDir: null,
    expectFrames: 12,
    expectTotalMs: 1005,
  },
  {
    id: 'front_l/Axe',
    dir: 'characters/orc-v1/source/combat-rescue-v5/grip-specialist/front_l-Axe-full',
    parentDir: 'characters/orc-v1/source/combat-rescue-v5/combat/front_l/Axe',
    mirrorOfDir: 'characters/orc-v1/source/combat-rescue-v5/grip-specialist/front_r-Axe-full',
    expectFrames: 12,
    expectTotalMs: 1005,
  },
];

function cmp(a, b) {
  if (a.width !== b.width || a.height !== b.height) return { sizeMismatch: true, diffPixels: -1, total: -1, maxChannelDiff: -1 };
  const n = a.data.length;
  let diff = 0;
  let maxCh = 0;
  for (let i = 0; i < n; i += 4) {
    const m = Math.max(
      Math.abs(a.data[i] - b.data[i]),
      Math.abs(a.data[i + 1] - b.data[i + 1]),
      Math.abs(a.data[i + 2] - b.data[i + 2]),
      Math.abs(a.data[i + 3] - b.data[i + 3]),
    );
    if (m > maxCh) maxCh = m;
    if (m > 0) diff++;
  }
  return { sizeMismatch: false, diffPixels: diff, total: n / 4, maxChannelDiff: maxCh };
}

function alphaOverBuf(baseBuf, top) {
  const out = Buffer.from(baseBuf);
  for (let i = 0; i < out.length; i += 4) {
    const ta = top.data[i + 3] / 255;
    if (ta === 0) continue;
    const sa = out[i + 3] / 255;
    const oa = ta + sa * (1 - ta);
    out[i] = Math.round((top.data[i] * ta + out[i] * sa * (1 - ta)) / oa);
    out[i + 1] = Math.round((top.data[i + 1] * ta + out[i + 1] * sa * (1 - ta)) / oa);
    out[i + 2] = Math.round((top.data[i + 2] * ta + out[i + 2] * sa * (1 - ta)) / oa);
    out[i + 3] = Math.round(oa * 255);
  }
  return out;
}

function bbox(layer) {
  let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity, px = 0;
  for (let y = 0; y < layer.height; y++) {
    for (let x = 0; x < layer.width; x++) {
      const i = (layer.width * y + x) << 2;
      if (layer.data[i + 3] > 0) {
        px++;
        if (x < x0) x0 = x;
        if (x > x1) x1 = x;
        if (y < y0) y0 = y;
        if (y > y1) y1 = y;
      }
    }
  }
  return px === 0 ? null : { x0, y0, x1, y1, px };
}

function hFlip(png) {
  const out = new PNG({ width: png.width, height: png.height });
  for (let y = 0; y < png.height; y++) {
    for (let x = 0; x < png.width; x++) {
      const si = (png.width * y + x) << 2;
      const di = (png.width * y + (png.width - 1 - x)) << 2;
      out.data[di] = png.data[si];
      out.data[di + 1] = png.data[si + 1];
      out.data[di + 2] = png.data[si + 2];
      out.data[di + 3] = png.data[si + 3];
    }
  }
  return out;
}

const report = { generatedAtUtc: new Date().toISOString(), cycles: [] };

for (const c of cycles) {
  const clip = JSON.parse(fs.readFileSync(P(path.join(c.dir, 'clip.json')), 'utf8'));
  const out = {
    id: c.id,
    frameCount: clip.frameCount,
    expectFrameCount: c.expectFrames,
    totalDurationMs: clip.totalDurationMs,
    expectTotalMs: c.expectTotalMs,
    sumDurationsMs: clip.durationsMs.reduce((a, b) => a + b, 0),
    visibleInterval: clip.visibleInterval,
    layerOrder: clip.layerOrder,
    frames: [],
  };
  for (const f of clip.frames) {
    const name = path.basename(f.png);
    const parentPngPath = P(path.join(c.parentDir, 'layers', 'body', name));
    const parentNativePath = P(path.join(c.parentDir, 'native', name));

    const composite = load(f.png);
    const body = load(path.join(c.dir, 'layers', 'body', name));
    const wBack = load(path.join(c.dir, 'layers', 'weaponBack', name));
    const wFront = load(path.join(c.dir, 'layers', 'weaponFront', name));
    const hand = load(path.join(c.dir, 'layers', 'handFront', name));

    const fr = {
      index: f.index,
      phase: f.phase,
      durationMs: f.durationMs,
      weaponVisible: f.weaponVisible,
      handFrontPixelsDeclared: f.handFrontPixels,
      handFrontPixelsCounted: bbox(hand)?.px ?? 0,
      weaponBackBbox: bbox(wBack),
      weaponFrontBbox: bbox(wFront),
      handBbox: bbox(hand),
    };

    // 1) preservação do corpo vs parent combat v5 (camada body 256)
    if (fs.existsSync(parentPngPath)) {
      fr.bodyVsParentCombat = cmp(body, load(path.join(c.parentDir, 'layers', 'body', name)));
    }
    // 1b) nativo 128 vs parent combat v5
    if (fs.existsSync(parentNativePath)) {
      fr.nativeVsParentCombat = cmp(load(f.nativePng), load(path.join(c.parentDir, 'native', name)));
    }

    // 2) álgebra alpha-over: weaponBack -> body -> weaponFront -> handFront == composite
    let acc = Buffer.from(wBack.data);
    acc = alphaOverBuf(acc, body);
    acc = alphaOverBuf(acc, wFront);
    acc = alphaOverBuf(acc, hand);
    let over1 = 0;
    let maxCh = 0;
    for (let i = 0; i < composite.data.length; i += 4) {
      const m = Math.max(
        Math.abs(composite.data[i] - acc[i]),
        Math.abs(composite.data[i + 1] - acc[i + 1]),
        Math.abs(composite.data[i + 2] - acc[i + 2]),
        Math.abs(composite.data[i + 3] - acc[i + 3]),
      );
      if (m > maxCh) maxCh = m;
      if (m > 1) over1++;
    }
    fr.alphaOverVsComposite = { pixelsDiffOver1: over1, maxChannelDiff: maxCh };

    out.frames.push(fr);
  }

  // 3) espelhamento: corpo front_l NÃO deve ser flip horizontal do corpo front_r
  if (c.mirrorOfDir && fs.existsSync(P(path.join(c.mirrorOfDir, 'clip.json')))) {
    const clip2 = JSON.parse(fs.readFileSync(P(path.join(c.mirrorOfDir, 'clip.json')), 'utf8'));
    out.mirrorTest = [];
    for (let i = 0; i < Math.min(clip.frameCount, clip2.frameCount); i++) {
      const a = load(path.join(c.dir, 'layers', 'body', String(i).padStart(2, '0') + '.png'));
      const b = load(path.join(c.mirrorOfDir, 'layers', 'body', String(i).padStart(2, '0') + '.png'));
      out.mirrorTest.push({ frame: i, bodyVsFlippedCounterpart: cmp(a, hFlip(b)) });
    }
  }

  report.cycles.push(out);
}

fs.writeFileSync(P('experiments/main-orc-combat-rescue-v5/qa-sol/qa-front-three/verify-pixels.json'), JSON.stringify(report, null, 2));
console.log('OK verify-pixels.json');
for (const c of report.cycles) {
  const bodyBad = c.frames.filter((f) => f.bodyVsParentCombat && f.bodyVsParentCombat.diffPixels !== 0).length;
  const natBad = c.frames.filter((f) => f.nativeVsParentCombat && f.nativeVsParentCombat.diffPixels !== 0).length;
  const overBad = c.frames.filter((f) => f.alphaOverVsComposite.pixelsDiffOver1 > 0).length;
  const handMismatch = c.frames.filter((f) => f.handFrontPixelsDeclared !== f.handFrontPixelsCounted).length;
  const weaponOutside = c.frames.filter((f) => !f.weaponVisible && (f.weaponBackBbox || f.weaponFrontBbox || f.handBbox)).length;
  const weaponInside = c.frames.filter((f) => f.weaponVisible && (!f.weaponFrontBbox && !f.weaponBackBbox)).length;
  console.log(`${c.id}: frames=${c.frameCount}/${c.expectFrameCount} total=${c.totalDurationMs}/${c.expectTotalMs} sum=${c.sumDurationsMs} bodyDeltaNeq0=${bodyBad} nativeDeltaNeq0=${natBad} alphaOverDiffOver1=${overBad} handPxMismatch=${handMismatch} weaponPixelsOutsideInterval=${weaponOutside} weaponMissingInsideInterval=${weaponInside}`);
  if (c.mirrorTest) {
    const mirrored = c.mirrorTest.filter((m) => m.bodyVsFlippedCounterpart.diffPixels === 0).map((m) => m.frame);
    const minDiff = Math.min(...c.mirrorTest.map((m) => m.bodyVsFlippedCounterpart.diffPixels));
    console.log(`  mirrorTest: fullyMirroredFrames=${JSON.stringify(mirrored)} minDiffPixels=${minDiff}`);
  }
}
