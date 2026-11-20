// Experimento 01 — skeleton-first back_l Sword
// Medição de fontes reais: clip.json (juntas manuais + rightGrip), silhuetas das
// camadas body, geometria da arma por quadro. Somente leitura; não altera arte.
import { readFileSync, writeFileSync, existsSync, readdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { join, dirname } from 'node:path';
import { PNG } from 'pngjs';

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, '..', '..', '..');
const rp = (rel) => join(ROOT, rel);
const R1 = (v) => Math.round(v * 10) / 10;

function loadPng(rel) {
  const p = rp(rel);
  if (!existsSync(p)) return null;
  return PNG.sync.read(readFileSync(p));
}

function silhouette(png) {
  const W = png.width, H = png.height, d = png.data;
  const solid = (x, y) => d[(y * W + x) * 4 + 3] > 8;
  let x0 = 1e9, x1 = -1e9, y0 = 1e9, y1 = -1e9, n = 0, sx = 0, sy = 0;
  const rows = [];
  for (let y = 0; y < H; y++) {
    let mn = -1, mx = -1, c = 0;
    for (let x = 0; x < W; x++) if (solid(x, y)) { if (mn < 0) mn = x; mx = x; c++; }
    if (mn >= 0) {
      rows.push([y, mn, mx, c]);
      if (y < y0) y0 = y; if (y > y1) y1 = y;
      if (mn < x0) x0 = mn; if (mx > x1) x1 = mx;
      n += c; sx += c * (mn + mx + 1) / 2; sy += c * y;
    }
  }
  if (n === 0) return { w: W, h: H, empty: true };
  return { w: W, h: H, bounds: [x0, y0, x1, y1], px: n, centroid: [R1(sx / n), R1(sy / n)], rows };
}

function runsInRow(png, y) {
  const W = png.width, d = png.data;
  const solid = (x) => d[(y * W + x) * 4 + 3] > 8;
  const runs = []; let s = -1;
  for (let x = 0; x <= W; x++) {
    const on = x < W && solid(x);
    if (on && s < 0) s = x;
    if (!on && s >= 0) { runs.push([s, x - 1, Math.round((s + x - 1) / 2)]); s = -1; }
  }
  return runs;
}

// Eixo principal (PCA da silhueta), extremos relativos a um ponto de referência.
function axisInfo(png, refPt) {
  const W = png.width, H = png.height, d = png.data;
  const pts = [];
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    if (d[(y * W + x) * 4 + 3] > 8) pts.push([x, y]);
  }
  if (!pts.length) return { empty: true };
  let cx = 0, cy = 0;
  for (const [x, y] of pts) { cx += x; cy += y; }
  cx /= pts.length; cy /= pts.length;
  let sxx = 0, syy = 0, sxy = 0;
  for (const [x, y] of pts) { const dx = x - cx, dy = y - cy; sxx += dx * dx; syy += dy * dy; sxy += dx * dy; }
  const theta = 0.5 * Math.atan2(2 * sxy, sxx - syy);
  let tproj = -1e9, bproj = 1e9, tp = null, bp = null;
  for (const [x, y] of pts) {
    const p = (x - cx) * Math.cos(theta) + (y - cy) * Math.sin(theta);
    if (p > tproj) { tproj = p; tp = [x, y]; }
    if (p < bproj) { bproj = p; bp = [x, y]; }
  }
  let tip = null, tipD = -1, pom = null, pomD = 1e18;
  if (refPt) {
    for (const [x, y] of pts) {
      const dd = (x - refPt[0]) ** 2 + (y - refPt[1]) ** 2;
      if (dd > tipD) { tipD = dd; tip = [x, y]; }
      if (dd < pomD) { pomD = dd; pom = [x, y]; }
    }
  }
  return {
    centroid: [R1(cx), R1(cy)], axisDeg: R1((theta * 180) / Math.PI),
    axisLen: R1(Math.hypot(tp[0] - bp[0], tp[1] - bp[1])), axisEnds: [bp, tp],
    tipFromRef: tip ? [tip, R1(Math.hypot(tip[0] - refPt[0], tip[1] - refPt[1]))] : null,
    nearRef: pom ? [pom, R1(Math.sqrt(pomD))] : null,
  };
}

function clipDump(rel) {
  const p = rp(rel);
  if (!existsSync(p)) return { missing: rel };
  const clip = JSON.parse(readFileSync(p, 'utf8'));
  const frames = (clip.frames || []).map((f) => ({
    i: f.index, ph: f.phase, d: f.durationMs, s: f.startMs, wv: f.weaponVisible,
    rg: f.rightGrip ?? null, rg256: f.rightGrip ? [f.rightGrip[0] + 64, f.rightGrip[1] + 64] : null,
    rot: f.rotationDeg ?? null, mj: f.manualJointsNative ?? null,
  }));
  return {
    rel, frameCount: clip.frameCount, totalMs: clip.totalDurationMs,
    canvas: clip.canvas, bodyOffset: clip.bodyOffset, groundY: clip.groundY,
    visibleInterval: clip.visibleInterval, contactEvent: clip.contactEvent,
    durations: clip.durationsMs, frames,
  };
}

const out = {};
out.clips = {
  rearArcBackL: clipDump('characters/orc-v1/source/combat-recovery-v8/rear-arc/back_l-sword/clip.json'),
  frontRSword: clipDump('characters/orc-v1/source/combat-recovery-v8/frontal-inbetween/front_r-sword/clip.json'),
  frontLSword: clipDump('characters/orc-v1/source/combat-recovery-v8/frontal-inbetween/front_l-sword/clip.json'),
};
// ---- Corpo de referência: Idle back_l F00 (128 nativo) ----
const idle = loadPng('characters/orc-v1/source/complete-v1/back_l/Idle/00.png');
if (idle) {
  const s = silhouette(idle);
  out.idleBackL00 = {
    dims: [idle.width, idle.height], bounds: s.bounds, centroid: s.centroid, px: s.px,
    rowsStep2: s.rows.filter((r) => r[0] % 2 === 0),
    legRuns: [118, 121, 124, 126].filter((y) => y < idle.height).map((y) => [y, runsInRow(idle, y)]),
  };
}

const CELL = 'characters/orc-v1/source/combat-recovery-v8/rear-arc/back_l-sword';
const rgF2 = out.clips.rearArcBackL.frames?.find((f) => f.i === 2)?.rg256 ?? null;
out.rearArc02 = { rightGrip256: rgF2 };
for (const layer of ['body', 'weaponFront', 'weaponBack', 'handFront']) {
  const png = loadPng(`${CELL}/layers/${layer}/02.png`);
  if (!png) { out.rearArc02[layer] = { missing: true }; continue; }
  const s = silhouette(png);
  out.rearArc02[layer] = {
    dims: [png.width, png.height], bounds: s.bounds, centroid: s.centroid, px: s.px,
    axis: layer.startsWith('weapon') ? axisInfo(png, rgF2) : undefined,
    rowsStep2: layer === 'body' ? s.rows.filter((r) => r[0] % 2 === 0) : undefined,
    legRuns: layer === 'body' ? [178, 182, 186, 190].map((y) => [y, runsInRow(png, y)]) : undefined,
  };
}
const comp02 = loadPng(`${CELL}/02.png`);
if (comp02) {
  const s = silhouette(comp02);
  out.rearArc02.composite = { dims: [comp02.width, comp02.height], bounds: s.bounds, centroid: s.centroid, px: s.px };
}

out.rearArcBodyBookends = {};
for (const idx of ['00', '13']) {
  const png = loadPng(`${CELL}/layers/body/${idx}.png`);
  if (!png) { out.rearArcBodyBookends[idx] = { missing: true }; continue; }
  const s = silhouette(png);
  out.rearArcBodyBookends[idx] = {
    bounds: s.bounds, centroid: s.centroid,
    rowsStep2: s.rows.filter((r) => r[0] % 2 === 0),
    legRuns: [178, 182, 186, 190].map((y) => [y, runsInRow(png, y)]),
  };
}

const sw = loadPng('characters/orc-v1/source/combat-rescue-v5/combat/weapons/Sword/recruit-sword.png');
if (sw) {
  const s = silhouette(sw);
  out.recruitSword = { dims: [sw.width, sw.height], bounds: s.bounds, px: s.px, axis: axisInfo(sw, [48, 66]) };
}

function weaponPath(cellRel, layer) {
  const dirp = rp(`${cellRel}/layers/${layer}`);
  if (!existsSync(dirp)) return { missing: dirp };
  const files = readdirSync(dirp).filter((f) => f.endsWith('.png')).sort();
  const arr = [];
  for (const f of files) {
    const png = loadPng(`${cellRel}/layers/${layer}/${f}`);
    if (!png) continue;
    const s = silhouette(png);
    if (s.empty) { arr.push({ f, empty: true }); continue; }
    arr.push({ f, b: s.bounds, c: s.centroid, a: axisInfo(png, null) });
  }
  return arr;
}
out.weaponPaths = {
  frontR_weaponFront: weaponPath('characters/orc-v1/source/combat-recovery-v8/frontal-inbetween/front_r-sword', 'weaponFront'),
  rearArcBackL_weaponFront: weaponPath(CELL, 'weaponFront'),
  rearArcBackL_weaponBack: weaponPath(CELL, 'weaponBack'),
};

// Dump seletivo: clips resumidos + medições completas em arquivo separado
writeFileSync(join(HERE, 'measure-out.json'), JSON.stringify(out, null, 1));
const brief = {
  clipsSummary: Object.fromEntries(Object.entries(out.clips).map(([k, c]) => [k, c.missing ? 'MISSING' : {
    frames: c.frameCount, totalMs: c.totalMs, contact: c.contactEvent,
    mjFrames: c.frames.filter((f) => f.mj).map((f) => f.i),
    rgByFrame: c.frames.map((f) => [f.i, f.rg]),
    mjByFrame: c.frames.filter((f) => f.mj).map((f) => [f.i, f.mj]),
  }])),
  idleBackL00: out.idleBackL00 ?? null,
  rearArc02: { rightGrip256: rgF2, body: out.rearArc02.body, weaponFront: out.rearArc02.weaponFront, weaponBack: out.rearArc02.weaponBack, handFront: out.rearArc02.handFront, composite: out.rearArc02.composite },
  recruitSword: out.recruitSword ?? null,
  weaponPaths: out.weaponPaths,
};
console.log(JSON.stringify(brief));
