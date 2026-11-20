#!/usr/bin/env node
// Read-only numeric diagnostics for TacticsRPG clip.json files.
// Usage:
//   node diag.mjs --clip <path/to/clip.json> [--out <file.json>]
//   node diag.mjs --all [--out <file.json>]
// All measurements are SUSPECTS for review, never artistic verdicts.
// Pixel-change fractions count visible changes: alpha changes, or RGB changes
// where alpha > 0. Fully transparent RGB-only differences are counted separately
// as transparentRgbOnly and excluded from fraction/bbox.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { decode, composite as compositePngs } from '../../../src/images.mjs';

export const DIAG_DIR = path.dirname(fileURLToPath(import.meta.url));
export const ROOT = path.resolve(DIAG_DIR, '../../..');
const SELF_PATH = path.resolve(fileURLToPath(import.meta.url));
const normalizePath = (p) => (process.platform === 'win32' ? path.resolve(p).toLowerCase() : path.resolve(p));
const IS_MAIN = process.argv[1] && normalizePath(process.argv[1]) === normalizePath(SELF_PATH);
const MANIFEST_REL = 'characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json';
const DEFAULT_ALL_OUT = path.join(DIAG_DIR, 'diagnostics-all.json');
const BASELINE_CLIPS = [
  'characters/orc-v1/source/complete-v1/front_l/Sword/Attack/clip.json',
  'characters/orc-v1/source/complete-v1/front_r/Walk/clip.json',
  'characters/orc-v1/source/complete-v1/front_l/Walk/clip.json',
];
export const MAX_LIST = 50;
export const BRIGHT_LUMA = 200;
export const BBOX_JUMP_PX = 8;

const sha256 = (data) => crypto.createHash('sha256').update(data).digest('hex');
const r4 = (v) => (Number.isFinite(v) ? Math.round(v * 10000) / 10000 : v);

function readJSON(p) {
  return JSON.parse(fs.readFileSync(p, 'utf8').replace(/^\uFEFF/, ''));
}

function toAbs(p) {
  return path.isAbsolute(p) ? p : path.resolve(ROOT, p);
}

function resolveAsset(p, baseDir) {
  if (path.isAbsolute(p)) return p;
  if (baseDir) {
    const local = path.resolve(baseDir, p);
    if (fs.existsSync(local)) return local;
  }
  return path.resolve(ROOT, p);
}

function toRel(p) {
  const abs = path.resolve(p);
  const rel = path.relative(ROOT, abs);
  return rel && !rel.startsWith('..') ? rel.split(path.sep).join('/') : abs;
}

function resolveClip(p) {
  if (path.isAbsolute(p)) {
    if (!fs.existsSync(p)) throw new Error(`Clip not found: ${p}`);
    return p;
  }
  for (const candidate of [path.resolve(process.cwd(), p), path.resolve(ROOT, p)]) {
    if (fs.existsSync(candidate)) return candidate;
  }
  throw new Error(`Clip not found (tried cwd and repo root): ${p}`);
}

// Cache is scoped to one analyzeClip() call: a long-lived process can reuse an
// exported analyzeClip() after a PNG changes on disk, so a global cache would
// silently return stale pixels and fingerprints.
function loadPng(p, context, baseDir, cache) {
  const abs = resolveAsset(p, baseDir);
  if (cache.has(abs)) return cache.get(abs);
  if (!fs.existsSync(abs)) throw new Error(`PNG not found (${context}): ${toRel(abs)}`);
  let decoded;
  try {
    decoded = decode(abs);
  } catch (error) {
    throw new Error(`PNG decode failed (${context}): ${toRel(abs)} :: ${error.message}`);
  }
  const entry = { image: decoded.image, sha256: decoded.sha256, file: toRel(abs) };
  cache.set(abs, entry);
  return entry;
}

export function pixelSha(image) {
  return sha256(Buffer.concat([
    Buffer.from(`${image.width}x${image.height}:`),
    Buffer.from(image.data),
  ]));
}

export function alphaAt(image, x, y) {
  if (x < 0 || y < 0 || x >= image.width || y >= image.height) return 0;
  return image.data[(y * image.width + x) * 4 + 3];
}

export function silhouette(image) {
  const { width: w, height: h, data } = image;
  const half = w / 2;
  const bandW = w / 8;
  const bands8 = new Array(8).fill(0);
  let opaque = 0, partialAlpha = 0, left = 0, right = 0;
  let x0 = w, y0 = h, x1 = -1, y1 = -1;
  for (let y = 0; y < h; y++) {
    for (let x = 0; x < w; x++) {
      const a = data[(y * w + x) * 4 + 3];
      if (a === 0) continue;
      if (a < 255) partialAlpha++;
      opaque++;
      bands8[Math.min(7, Math.floor(x / bandW))]++;
      if (x < half) left++; else right++;
      if (x < x0) x0 = x;
      if (x > x1) x1 = x;
      if (y < y0) y0 = y;
      if (y > y1) y1 = y;
    }
  }
  return {
    opaque,
    partialAlpha,
    left,
    right,
    bands8,
    bandWidth: bandW,
    bbox: opaque ? { x0, y0, x1, y1 } : null,
  };
}

export function deltaPixels(a, b) {
  if (!a || !b) return null;
  if (a.width !== b.width || a.height !== b.height) return null;
  const w = a.width, h = a.height;
  const total = w * h;
  let changed = 0;
  let transparentRgbOnly = 0;
  let x0 = w, y0 = h, x1 = -1, y1 = -1;
  const ad = a.data, bd = b.data;
  for (let i = 0; i < ad.length; i += 4) {
    const aa = ad[i + 3], ba = bd[i + 3];
    const rgbDiffers = ad[i] !== bd[i] || ad[i + 1] !== bd[i + 1] || ad[i + 2] !== bd[i + 2];
    if (aa === 0 && ba === 0 && rgbDiffers) {
      transparentRgbOnly++;
      continue;
    }
    if (aa === ba && !rgbDiffers) continue;
    changed++;
    const p = i / 4, x = p % w, y = (p - x) / w;
    if (x < x0) x0 = x; if (x > x1) x1 = x;
    if (y < y0) y0 = y; if (y > y1) y1 = y;
  }
  return {
    changed,
    transparentRgbOnly,
    allRgbaChanged: changed + transparentRgbOnly,
    total,
    fraction: r4(changed / total),
    bbox: changed ? { x0, y0, x1, y1 } : null,
  };
}

export function clusterize(mask, w, h, data) {
  const n = w * h;
  let clusters = 0;
  let suspectPixels = 0;
  let largest = null;
  const stack = [];
  for (let seed = 0; seed < n; seed++) {
    if (mask[seed] !== 1) continue;
    clusters++;
    stack.length = 0;
    stack.push(seed);
    mask[seed] = 2;
    let size = 0, sr = 0, sg = 0, sb = 0;
    let x0 = w, y0 = h, x1 = -1, y1 = -1;
    while (stack.length) {
      const idx = stack.pop();
      const x = idx % w, y = (idx - x) / w;
      const i = idx * 4;
      size++;
      sr += data[i]; sg += data[i + 1]; sb += data[i + 2];
      if (x < x0) x0 = x; if (x > x1) x1 = x;
      if (y < y0) y0 = y; if (y > y1) y1 = y;
      if (x > 0 && mask[idx - 1] === 1) { mask[idx - 1] = 2; stack.push(idx - 1); }
      if (x + 1 < w && mask[idx + 1] === 1) { mask[idx + 1] = 2; stack.push(idx + 1); }
      if (y > 0 && mask[idx - w] === 1) { mask[idx - w] = 2; stack.push(idx - w); }
      if (y + 1 < h && mask[idx + w] === 1) { mask[idx + w] = 2; stack.push(idx + w); }
    }
    suspectPixels += size;
    if (!largest || size > largest.size) {
      largest = {
        size,
        bbox: { x0, y0, x1, y1 },
        meanRGB: [Math.round(sr / size), Math.round(sg / size), Math.round(sb / size)],
      };
    }
  }
  return { clusters, suspectPixels, largest: largest || null };
}

export function brightEdge(image) {
  const { width: w, height: h, data } = image;
  const n = w * h;
  const mask200 = new Uint8Array(n); // 0 none, 1 suspect-unvisited, 2 visited
  const mask170 = new Uint8Array(n);
  let maxLuma = 0;
  let edgePixels = 0;
  let maxEdgeLuma = 0;
  const lumaCounts = { ge200: 0, ge170: 0, ge140: 0 };
  const edgeLumaCounts = { ge200: 0, ge170: 0, ge140: 0 };
  for (let y = 0; y < h; y++) {
    for (let x = 0; x < w; x++) {
      const idx = y * w + x;
      const i = idx * 4;
      if (data[i + 3] === 0) continue;
      const luma = 0.2126 * data[i] + 0.7152 * data[i + 1] + 0.0722 * data[i + 2];
      if (luma > maxLuma) maxLuma = luma;
      if (luma >= 200) lumaCounts.ge200++;
      if (luma >= 170) lumaCounts.ge170++;
      if (luma >= 140) lumaCounts.ge140++;
      const isEdge =
        alphaAt(image, x - 1, y) === 0 || alphaAt(image, x + 1, y) === 0 ||
        alphaAt(image, x, y - 1) === 0 || alphaAt(image, x, y + 1) === 0;
      if (!isEdge) continue;
      edgePixels++;
      if (luma > maxEdgeLuma) maxEdgeLuma = luma;
      if (luma >= 200) { edgeLumaCounts.ge200++; mask200[idx] = 1; }
      if (luma >= 170) { edgeLumaCounts.ge170++; mask170[idx] = 1; }
      if (luma >= 140) edgeLumaCounts.ge140++;
    }
  }

  const primary = clusterize(mask200, w, h, data);
  const secondary = clusterize(mask170, w, h, data);

  return {
    thresholdLuma: BRIGHT_LUMA,
    maxLuma: Math.round(maxLuma),
    edgePixels,
    maxEdgeLuma: Math.round(maxEdgeLuma),
    edgeLumaCounts,
    lumaCounts,
    clusters: primary.clusters,
    suspectPixels: primary.suspectPixels,
    largest: primary.largest,
    secondary170: {
      thresholdLuma: 170,
      clusters: secondary.clusters,
      suspectPixels: secondary.suspectPixels,
      largest: secondary.largest,
    },
  };
}

export function bboxDelta(prevBbox, curBbox) {
  if (!prevBbox && !curBbox) return null;
  if (!prevBbox || !curBbox) {
    return { dx: null, dy: null, dw: null, dh: null, flagged: true, empty: true };
  }
  const dx = curBbox.x0 - prevBbox.x0;
  const dy = curBbox.y0 - prevBbox.y0;
  const dw = (curBbox.x1 - curBbox.x0 + 1) - (prevBbox.x1 - prevBbox.x0 + 1);
  const dh = (curBbox.y1 - curBbox.y0 + 1) - (prevBbox.y1 - prevBbox.y0 + 1);
  return {
    dx, dy, dw, dh,
    flagged: [dx, dy, dw, dh].some((v) => Math.abs(v) > BBOX_JUMP_PX),
  };
}

function orderedLayerEntries(frame, layerOrder) {
  const obj = frame.layers && typeof frame.layers === 'object' ? frame.layers : {};
  const keys = Object.keys(obj);
  const ordered = [
    ...layerOrder.filter((k) => keys.includes(k)),
    ...keys.filter((k) => !layerOrder.includes(k)),
  ];
  return ordered.map((name) => ({ name, meta: obj[name] }));
}

function composeFromLayers(layerImages, context) {
  if (!layerImages.length) throw new Error(`Cannot compose empty layer set (${context})`);
  const { width, height } = layerImages[0].image;
  for (const layer of layerImages) {
    if (layer.image.width !== width || layer.image.height !== height) {
      throw new Error(`Layer canvas mismatch in ${context}: ${layer.name} is ${layer.image.width}x${layer.image.height}`);
    }
  }
  return compositePngs(layerImages.map((l) => l.image), width, height);
}

export function analyzeClip(clipPath) {
  const abs = resolveClip(clipPath);
  const clipDir = path.dirname(abs);
  const pngCache = new Map();
  const clip = readJSON(abs);
  const framesIn = Array.isArray(clip.frames) ? clip.frames : [];
  if (!framesIn.length) throw new Error(`Clip has no frames: ${toRel(abs)}`);

  const layerOrder = Array.isArray(clip.layerOrder) ? clip.layerOrder : [];
  const frames = [];
  const bboxJumps = [];
  const duplicateGroups = { body: new Map(), composite: new Map() };
  const seenFrameNos = new Set();
  let prev = null;
  let first = null;

  for (let index = 0; index < framesIn.length; index++) {
    const f = framesIn[index];
    const frameNo = Number.isInteger(f.index) ? f.index : index;
    const context = `${toRel(abs)} frame ${frameNo}`;
    if (seenFrameNos.has(frameNo)) throw new Error(`Duplicate frame index ${frameNo} (${toRel(abs)})`);
    seenFrameNos.add(frameNo);
    const layerEntries = orderedLayerEntries(f, layerOrder);

    let layerImages = [];
    for (const { name, meta } of layerEntries) {
      const pngPath = typeof meta === 'string' ? meta : meta && meta.png;
      if (!pngPath) continue;
      const decoded = loadPng(pngPath, `${context} layer ${name}`, clipDir, pngCache);
      const metaSha = meta && typeof meta === 'object' && typeof meta.sha256 === 'string' ? meta.sha256 : null;
      layerImages.push({
        name,
        file: decoded.file,
        sha256: metaSha || decoded.sha256,
        shaSource: metaSha ? 'metadata' : 'computed',
        shaMatchesFile: metaSha ? metaSha === decoded.sha256 : null,
        image: decoded.image,
      });
    }

    let compositeImage;
    let compositeFile;
    let compositeFileSha = null;
    let compositeMetaSha = null;
    if (f.png) {
      const decoded = loadPng(f.png, `${context} composite`, clipDir, pngCache);
      compositeImage = decoded.image;
      compositeFile = decoded.file;
      compositeFileSha = decoded.sha256;
      compositeMetaSha = typeof f.sha256 === 'string' ? f.sha256 : null;
    } else if (layerImages.length) {
      compositeImage = composeFromLayers(layerImages, context);
      compositeFile = null;
    } else {
      throw new Error(`Frame has neither png nor layers (${context})`);
    }

    // A supplied composite bypasses composeFromLayers(), so validate the layer
    // canvases here too. Without this, mismatched layers only surface later as
    // null deltas instead of an explicit error.
    for (const layer of layerImages) {
      if (layer.image.width !== compositeImage.width || layer.image.height !== compositeImage.height) {
        throw new Error(
          `Layer canvas mismatch in ${context}: ${layer.name} is ${layer.image.width}x${layer.image.height}, composite is ${compositeImage.width}x${compositeImage.height}`,
        );
      }
    }

    const bodyLayer = layerImages.find((l) => l.name.toLowerCase() === 'body')
      || layerImages.find((l) => /body/i.test(l.name))
      || null;
    const bodyIsComposite = !bodyLayer;
    const bodyImage = bodyIsComposite ? compositeImage : bodyLayer.image;
    if (frames.length && frames[0].bodyIsComposite !== bodyIsComposite) {
      throw new Error(`Inconsistent body layer presence across frames (${context})`);
    }

    const compositeSil = silhouette(compositeImage);
    const bodySil = bodyIsComposite ? compositeSil : silhouette(bodyImage);

    const bodyLayers = layerImages.filter((l) => /body/i.test(l.name));
    const silhouetteOut = {
      composite: compositeSil,
      body: { layer: bodyIsComposite ? null : bodyLayer.name, ...bodySil },
    };
    if (bodyLayers.length > 1) {
      silhouetteOut.bodyLayers = Object.fromEntries(
        bodyLayers.map((l) => [l.name, silhouette(l.image)]),
      );
    }

    const brightComposite = brightEdge(compositeImage);
    const brightBody = bodyIsComposite ? null : brightEdge(bodyImage);

    const feat = {
      index: frameNo,
      file: compositeFile || (bodyLayer ? bodyLayer.file : null),
      durationMs: Number.isFinite(f.durationMs) ? f.durationMs : null,
      size: [compositeImage.width, compositeImage.height],
      bodyIsComposite,
      composite: {
        file: compositeFile,
        sha256: compositeMetaSha || compositeFileSha || pixelSha(compositeImage),
        shaSource: compositeMetaSha ? 'metadata' : 'computed',
        shaMatchesFile: compositeMetaSha ? compositeMetaSha === compositeFileSha : null,
      },
      layers: layerImages.map(({ image, ...rest }) => rest),
      silhouette: silhouetteOut,
      brightEdge: { body: brightBody, composite: brightComposite },
    };

    if (f.rightGrip !== undefined || f.rotationDeg !== undefined || f.weaponVisible !== undefined) {
      feat.meta = {};
      if (f.rightGrip !== undefined) feat.meta.rightGrip = f.rightGrip;
      if (f.rotationDeg !== undefined) feat.meta.rotationDeg = f.rotationDeg;
      if (f.weaponVisible !== undefined) feat.meta.weaponVisible = f.weaponVisible;
    }

    const keyFor = (img) => `${img.width}x${img.height}|${pixelSha(img)}`;
    const addDuplicateKey = (surface, img) => {
      const k = keyFor(img);
      if (!duplicateGroups[surface].has(k)) duplicateGroups[surface].set(k, []);
      duplicateGroups[surface].get(k).push(frameNo);
    };
    addDuplicateKey('composite', compositeImage);
    if (!bodyIsComposite) addDuplicateKey('body', bodyImage);

    if (prev) {
      const nextComposite = deltaPixels(compositeImage, prev.compositeImage);
      const nextBody = bodyIsComposite
        ? nextComposite
        : deltaPixels(bodyImage, prev.bodyImage);
      const vsFirstComposite = deltaPixels(compositeImage, first.compositeImage);
      const vsFirstBody = bodyIsComposite
        ? vsFirstComposite
        : deltaPixels(bodyImage, first.bodyImage);

      feat.delta = {
        body: {
          fromPrev: prev.frameNo,
          to: frameNo,
          fromPrevFraction: nextBody ? nextBody.fraction : null,
          fromPrevPixels: nextBody ? nextBody.changed : null,
          fromPrevTransparentRgbOnly: nextBody ? nextBody.transparentRgbOnly : null,
          fromPrevAllRgbaChanged: nextBody ? nextBody.allRgbaChanged : null,
          fromPrevBbox: nextBody ? nextBody.bbox : null,
          vsFirstFraction: vsFirstBody ? vsFirstBody.fraction : null,
          vsFirstPixels: vsFirstBody ? vsFirstBody.changed : null,
          vsFirstTransparentRgbOnly: vsFirstBody ? vsFirstBody.transparentRgbOnly : null,
          vsFirstAllRgbaChanged: vsFirstBody ? vsFirstBody.allRgbaChanged : null,
        },
        composite: {
          fromPrev: prev.frameNo,
          to: frameNo,
          fromPrevFraction: nextComposite ? nextComposite.fraction : null,
          fromPrevPixels: nextComposite ? nextComposite.changed : null,
          fromPrevTransparentRgbOnly: nextComposite ? nextComposite.transparentRgbOnly : null,
          fromPrevAllRgbaChanged: nextComposite ? nextComposite.allRgbaChanged : null,
          fromPrevBbox: nextComposite ? nextComposite.bbox : null,
          vsFirstFraction: vsFirstComposite ? vsFirstComposite.fraction : null,
          vsFirstPixels: vsFirstComposite ? vsFirstComposite.changed : null,
          vsFirstTransparentRgbOnly: vsFirstComposite ? vsFirstComposite.transparentRgbOnly : null,
          vsFirstAllRgbaChanged: vsFirstComposite ? vsFirstComposite.allRgbaChanged : null,
        },
      };

      const bodyJump = bboxDelta(prev.bodySil.bbox, bodySil.bbox);
      const compositeJump = bboxDelta(prev.compositeSil.bbox, compositeSil.bbox);
      feat.bboxDelta = { body: bodyJump, composite: compositeJump };
      if (bodyJump && bodyJump.flagged) {
        bboxJumps.push({ surface: 'body', from: prev.frameNo, to: frameNo, ...bodyJump });
      }
      if (!bodyIsComposite && compositeJump && compositeJump.flagged) {
        bboxJumps.push({ surface: 'composite', from: prev.frameNo, to: frameNo, ...compositeJump });
      }
    } else {
      feat.delta = {
        body: { fromPrev: null, to: frameNo, fromPrevFraction: null, fromPrevPixels: null, fromPrevTransparentRgbOnly: null, fromPrevAllRgbaChanged: null, fromPrevBbox: null, vsFirstFraction: 0, vsFirstPixels: 0, vsFirstTransparentRgbOnly: 0, vsFirstAllRgbaChanged: 0 },
        composite: { fromPrev: null, to: frameNo, fromPrevFraction: null, fromPrevPixels: null, fromPrevTransparentRgbOnly: null, fromPrevAllRgbaChanged: null, fromPrevBbox: null, vsFirstFraction: 0, vsFirstPixels: 0, vsFirstTransparentRgbOnly: 0, vsFirstAllRgbaChanged: 0 },
      };
      feat.bboxDelta = { body: null, composite: null };
    }

    prev = { compositeImage, bodyImage, bodySil, compositeSil, frameNo };
    if (!first) first = { compositeImage, bodyImage };

    frames.push(feat);
  }

  // Exact-duplicate pairs (identical RGBA buffers), capped for compactness.
  const duplicatePairs = [];
  let duplicatePairCount = 0;
  for (const surface of ['body', 'composite']) {
    for (const indices of duplicateGroups[surface].values()) {
      for (let i = 0; i < indices.length; i++) {
        for (let j = i + 1; j < indices.length; j++) {
          duplicatePairCount++;
          if (duplicatePairs.length < MAX_LIST) {
            duplicatePairs.push({ surface, a: indices[i], b: indices[j] });
          }
        }
      }
    }
  }
  duplicatePairs.sort((x, y) => {
    const order = { body: 0, composite: 1 };
    return (order[x.surface] - order[y.surface]) || x.a - y.a || x.b - y.b;
  });

  // Metadata drift (only fields actually present on frames).
  const gripFields = new Set();
  for (const f of framesIn) {
    for (const key of Object.keys(f)) if (/grip/i.test(key) && Array.isArray(f[key]) && f[key].length === 2) gripFields.add(key);
  }
  const gripSteps = [];
  const rotationSteps = [];
  const weaponVisibleChanges = [];
  for (let i = 1; i < framesIn.length; i++) {
    const a = framesIn[i - 1], b = framesIn[i];
    const from = Number.isInteger(a.index) ? a.index : i - 1;
    const to = Number.isInteger(b.index) ? b.index : i;
    for (const field of [...gripFields].sort()) {
      if (!Array.isArray(a[field]) || !Array.isArray(b[field])) continue;
      gripSteps.push({
        field, from, to,
        dx: b[field][0] - a[field][0],
        dy: b[field][1] - a[field][1],
      });
    }
    if (Number.isFinite(a.rotationDeg) && Number.isFinite(b.rotationDeg)) {
      const raw = b.rotationDeg - a.rotationDeg;
      rotationSteps.push({
        from, to,
        rawDeltaDeg: r4(raw),
        shortestDeltaDeg: r4(((raw % 360) + 540) % 360 - 180),
      });
    }
    if (a.weaponVisible !== undefined && b.weaponVisible !== undefined && a.weaponVisible !== b.weaponVisible) {
      weaponVisibleChanges.push({ from, to, fromValue: a.weaponVisible, toValue: b.weaponVisible });
    }
  }

  const bodyDeltas = [];
  const compositeDeltas = [];
  for (let i = 0; i < frames.length; i++) {
    const a = frames[i];
    if (a.delta.body.fromPrevFraction !== null) {
      bodyDeltas.push({ from: a.delta.body.fromPrev, to: a.delta.body.to, fraction: a.delta.body.fromPrevFraction });
    }
    if (a.delta.composite.fromPrevFraction !== null) {
      compositeDeltas.push({ from: a.delta.composite.fromPrev, to: a.delta.composite.to, fraction: a.delta.composite.fromPrevFraction });
    }
  }
  const maxBy = (list) => list.reduce((best, cur) => (!best || cur.fraction > best.fraction ? cur : best), null);

  const peakOf = (f) => (f.bodyIsComposite ? f.brightEdge.composite : f.brightEdge.body);
  let brightPeak = null;
  for (const f of frames) {
    const b = peakOf(f);
    if (!b) continue;
    if (!brightPeak
      || b.suspectPixels > brightPeak.suspectPixels
      || (b.suspectPixels === brightPeak.suspectPixels && b.maxEdgeLuma > brightPeak.maxEdgeLuma)) {
      brightPeak = {
        frame: f.index,
        surface: f.bodyIsComposite ? 'composite' : 'body',
        clusters: b.clusters,
        suspectPixels: b.suspectPixels,
        largestSize: b.largest ? b.largest.size : 0,
        largestBbox: b.largest ? b.largest.bbox : null,
        maxLuma: b.maxLuma,
        maxEdgeLuma: b.maxEdgeLuma,
        edgePixels: b.edgePixels,
      };
    }
  }

  const last = frames[frames.length - 1];
  const maxBody = maxBy(bodyDeltas);
  const maxComposite = maxBy(compositeDeltas);

  return {
    clip: {
      path: toRel(abs),
      label: [clip.direction, clip.category || clip.action || clip.state].filter(Boolean).join('/') || path.basename(path.dirname(abs)),
      id: clip.id || null,
      direction: clip.direction || null,
      action: clip.action || clip.state || clip.category || null,
      loop: clip.loop === true,
      oneShot: clip.oneShot === true,
      frameCount: frames.length,
      durationsMs: Array.isArray(clip.durationsMs) ? clip.durationsMs : frames.map((f) => f.durationMs),
      totalDurationMs: Number.isFinite(clip.totalDurationMs)
        ? clip.totalDurationMs
        : frames.reduce((sum, f) => sum + (f.durationMs || 0), 0),
      groundY: Number.isFinite(clip.groundY) ? clip.groundY : null,
      bodyOffset: clip.bodyOffset || null,
      summary: {
        frameCount: frames.length,
        exactDuplicatePairCount: duplicatePairCount,
        maxBodyDelta: maxBody,
        maxCompositeDelta: maxComposite,
        brightEdgePeak: brightPeak,
        bboxJumpCount: bboxJumps.filter((j) => j.surface === 'body').length,
        compositeBboxJumpCount: bboxJumps.filter((j) => j.surface === 'composite').length,
        bodyIsComposite: frames[0].bodyIsComposite,
        lastVsFirst: last
          ? {
            bodyFraction: last.delta.body.vsFirstFraction,
            bodyPixels: last.delta.body.vsFirstPixels,
            bodyTransparentRgbOnly: last.delta.body.vsFirstTransparentRgbOnly,
            bodyAllRgbaChanged: last.delta.body.vsFirstAllRgbaChanged,
            compositeFraction: last.delta.composite.vsFirstFraction,
            compositePixels: last.delta.composite.vsFirstPixels,
            compositeTransparentRgbOnly: last.delta.composite.vsFirstTransparentRgbOnly,
            compositeAllRgbaChanged: last.delta.composite.vsFirstAllRgbaChanged,
          }
          : null,
      },
      duplicates: { totalPairs: duplicatePairCount, list: duplicatePairs, truncated: duplicatePairCount > MAX_LIST },
      bboxJumps: bboxJumps.slice(0, MAX_LIST),
      bboxJumpsTruncated: bboxJumps.length > MAX_LIST,
      metadataDrift: {
        gripFields: [...gripFields].sort(),
        gripSteps: gripSteps.slice(0, MAX_LIST),
        rotationSteps: rotationSteps.slice(0, MAX_LIST),
        weaponVisibleChanges: weaponVisibleChanges.slice(0, MAX_LIST),
      },
      frames,
    },
  };
}

function printSummaryTable(clips) {
  const rows = clips.map((entry) => {
    const c = entry.clip;
    const s = c.summary;
    const dup = s.exactDuplicatePairCount ? String(s.exactDuplicatePairCount) : '-';
    const maxBody = s.maxBodyDelta ? `${s.maxBodyDelta.from}->${s.maxBodyDelta.to} ${(s.maxBodyDelta.fraction * 100).toFixed(1)}%` : '-';
    const peak = s.brightEdgePeak
      ? s.brightEdgePeak.suspectPixels > 0
        ? `f${String(s.brightEdgePeak.frame).padStart(2, '0')} ${s.brightEdgePeak.suspectPixels}px/${s.brightEdgePeak.clusters}cl`
        : `f${String(s.brightEdgePeak.frame).padStart(2, '0')} 0 (edge max ${s.brightEdgePeak.maxEdgeLuma})`
      : '-';
    const jumps = s.bboxJumpCount || s.compositeBboxJumpCount
      ? `${s.bboxJumpCount}b/${s.compositeBboxJumpCount}c`
      : '-';
    return [
      c.label || `${c.direction || '-'}/${c.action || '-'}`,
      c.frameCount,
      dup,
      maxBody,
      peak,
      jumps,
    ];
  });
  const header = ['clip', 'frames', 'exact dups', 'biggest body delta', 'bright-edge suspect peak', 'bbox jumps'];
  const widths = header.map((h, i) => Math.max(h.length, ...rows.map((r) => String(r[i]).length)));
  const fmt = (r) => r.map((v, i) => String(v).padEnd(widths[i])).join(' | ');
  console.log(fmt(header));
  console.log(widths.map((w) => '-'.repeat(w)).join('-+-'));
  for (const row of rows) console.log(fmt(row));
}

export function main(argv) {
  let clipArg = null;
  let outArg = null;
  let all = false;
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--clip') {
      clipArg = argv[++i];
      if (!clipArg) throw new Error('--clip requires a path');
    } else if (a === '--out') {
      outArg = argv[++i];
      if (!outArg) throw new Error('--out requires a path');
    } else if (a === '--all') {
      all = true;
    } else if (a === '--help' || a === '-h') {
      console.log('Usage: node diag.mjs --clip <clip.json> [--out <file.json>] | --all [--out <file.json>]');
      return;
    } else {
      throw new Error(`Unknown argument: ${a}`);
    }
  }
  if (all && clipArg) throw new Error('Use either --all or --clip, not both');
  if (!all && !clipArg) throw new Error('Missing --clip <clip.json> or --all');

  let targets;
  let manifestMeta = null;
  if (all) {
    const manifestAbs = path.resolve(ROOT, MANIFEST_REL);
    if (!fs.existsSync(manifestAbs)) throw new Error(`Manifest not found: ${MANIFEST_REL}`);
    const manifest = readJSON(manifestAbs);
    const active = (manifest.cells || []).filter((c) => c.status === 'ACTIVE_CANDIDATE');
    if (active.length !== 12 && active.length !== 15) {
      throw new Error(`Expected 12 or 15 ACTIVE_CANDIDATE cells in manifest, found ${active.length}`);
    }
    targets = [...active.map((c) => c.clipJson), ...BASELINE_CLIPS];
    const seen = new Set();
    targets = targets.filter((p) => {
      const k = normalizePath(toAbs(p));
      if (seen.has(k)) return false;
      seen.add(k);
      return true;
    });
    if (targets.length !== 15) throw new Error(`Expected 15 targets, built ${targets.length}`);
    manifestMeta = {
      path: MANIFEST_REL,
      manifestId: manifest.manifestId || null,
      totalClips: manifest.totalClips ?? null,
      activeCandidateCount: active.length,
      baselineClips: BASELINE_CLIPS,
    };
  } else {
    targets = [clipArg];
  }

  const results = targets.map((target) => analyzeClip(target));
  const doc = {
    schemaVersion: 1,
    tool: 'experiments/main-orc-rear-recovery-v2/diag/diag.mjs',
    scope: 'Numeric diagnostics only. Pixel-change fractions count visible changes (alpha, or RGB where alpha > 0); fully transparent RGB-only differences are reported separately as transparentRgbOnly. Bright-edge clusters, silhouette drops, duplicates and jumps are review SUSPECTS, never artistic verdicts.',
    ...(manifestMeta ? { manifest: manifestMeta } : {}),
    clipCount: results.length,
    clips: results.map((r) => r.clip),
  };
  const json = `${JSON.stringify(doc)}\n`;

  if (outArg) {
    const outAbs = path.resolve(process.cwd(), outArg);
    fs.mkdirSync(path.dirname(outAbs), { recursive: true });
    fs.writeFileSync(outAbs, json);
    console.log(`Wrote ${toRel(outAbs)} (${Buffer.byteLength(json)} bytes, ${results.length} clip(s)).`);
    if (all) printSummaryTable(results);
  } else if (all) {
    fs.writeFileSync(DEFAULT_ALL_OUT, json);
    console.log(`Wrote ${toRel(DEFAULT_ALL_OUT)} (${Buffer.byteLength(json)} bytes, ${results.length} clips).`);
    printSummaryTable(results);
  } else {
    process.stdout.write(json);
  }
}

if (IS_MAIN) {
  try {
    main(process.argv.slice(2));
  } catch (error) {
    console.error(`diag: ${error.message}`);
    process.exitCode = 1;
  }
}
