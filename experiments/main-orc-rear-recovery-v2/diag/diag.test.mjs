import { test, after } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { PNG } from 'pngjs';
import { composite, decode } from '../../../src/images.mjs';
import {
  DIAG_DIR, ROOT, analyzeClip, silhouette, brightEdge, deltaPixels, alphaAt,
  bboxDelta, pixelSha,
} from './diag.mjs';

const TMP = fs.mkdtempSync(path.join(DIAG_DIR, '.tmp-test-'));
after(() => fs.rmSync(TMP, { recursive: true, force: true }));

function image(width, height, pixels = []) {
  const png = new PNG({ width, height });
  png.data.fill(0);
  for (const [x, y, r, g, b, a] of pixels) {
    const i = (y * width + x) * 4;
    png.data[i] = r; png.data[i + 1] = g; png.data[i + 2] = b; png.data[i + 3] = a;
  }
  return png;
}

function writePng(name, width, height, pixels) {
  const file = path.join(TMP, name);
  fs.writeFileSync(file, PNG.sync.write(image(width, height, pixels), { colorType: 6, inputColorType: 6, bitDepth: 8 }));
  return file;
}

function writeClip(name, clip) {
  const file = path.join(TMP, `${name}.json`);
  fs.writeFileSync(file, JSON.stringify(clip));
  return file;
}

function fileSha(file) {
  return crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
}

function solid(name, width, height, rgba) {
  const pixels = [];
  for (let y = 0; y < height; y++) for (let x = 0; x < width; x++) pixels.push([x, y, ...rgba]);
  return writePng(name, width, height, pixels);
}

test('silhouette: counts opaque, partial alpha, halves, bands and bbox', () => {
  const img = image(16, 16, [
    [4, 6, 10, 10, 10, 255], [5, 6, 10, 10, 10, 255],
    [4, 7, 10, 10, 10, 255], [5, 7, 10, 10, 10, 255],
    [4, 8, 10, 10, 10, 255], [5, 8, 10, 10, 10, 255],
    [8, 6, 10, 10, 10, 128], // semi-transparent, counted opaque
    [12, 12, 10, 10, 10, 0], // transparent, not counted
  ]);
  const s = silhouette(img);
  assert.equal(s.opaque, 7);
  assert.equal(s.partialAlpha, 1);
  assert.equal(s.bandWidth, 2);
  assert.equal(s.left, 6);
  assert.equal(s.right, 1);
  assert.deepEqual(s.bands8, [0, 0, 6, 0, 1, 0, 0, 0]);
  assert.deepEqual(s.bbox, { x0: 4, y0: 6, x1: 8, y1: 8 });
  assert.equal(alphaAt(img, 4, 6), 255);
  assert.equal(alphaAt(img, 8, 6), 128);
  assert.equal(alphaAt(img, -1, 0), 0);
  assert.equal(alphaAt(img, 16, 0), 0);
  assert.equal(alphaAt(img, 0, 16), 0);

  const empty = silhouette(image(4, 4));
  assert.equal(empty.opaque, 0);
  assert.equal(empty.partialAlpha, 0);
  assert.equal(empty.bbox, null);
  assert.deepEqual(empty.bands8, [0, 0, 0, 0, 0, 0, 0, 0]);
});

test('silhouette: 256-wide band boundaries map to x0/32/64/96/128/160/192/224', () => {
  const pixels = [0, 31, 32, 95, 96, 128, 160, 192, 224, 255].map((x) => [x, 0, 1, 2, 3, 255]);
  const s = silhouette(image(256, 1, pixels));
  assert.deepEqual(s.bands8, [2, 1, 1, 1, 1, 1, 1, 2]);
  assert.equal(s.left, 5);
  assert.equal(s.right, 5);
  assert.deepEqual(s.bbox, { x0: 0, y0: 0, x1: 255, y1: 0 });
});

test('brightEdge: 200-luma edge pixel, interior highlight, partial alpha, transparent RGB', () => {
  const pixels = [
    [0, 0, 255, 255, 255, 0],       // transparent white: must not count
    [1, 1, 255, 255, 255, 255],     // bright edge, isolated
    [1, 4, 255, 255, 255, 128],     // bright semi-transparent edge, counted opaque
  ];
  for (let y = 3; y <= 5; y++) for (let x = 3; x <= 5; x++) {
    const center = x === 4 && y === 4;
    pixels.push([x, y, center ? 255 : 128, center ? 255 : 128, center ? 255 : 128, 128]);
  }
  const b = brightEdge(image(6, 6, pixels));
  assert.equal(b.thresholdLuma, 200);
  assert.equal(b.clusters, 2);
  assert.equal(b.suspectPixels, 2);
  assert.equal(b.edgeLumaCounts.ge200, 2);
  assert.equal(b.lumaCounts.ge200, 3);
  assert.equal(b.largest.size, 1);
  assert.equal(b.maxEdgeLuma, 255);
  assert.equal(b.maxLuma, 255);
  assert.equal(b.secondary170.clusters, 2);
  assert.ok(b.edgePixels > b.suspectPixels);
});

test('brightEdge: 4-connectivity separates diagonal components', () => {
  const diagonal = brightEdge(image(4, 4, [
    [0, 0, 255, 255, 255, 255],
    [1, 1, 255, 255, 255, 255],
  ]));
  assert.equal(diagonal.clusters, 2);
  assert.equal(diagonal.suspectPixels, 2);
  assert.equal(diagonal.largest.size, 1);

  const connected = brightEdge(image(4, 4, [
    [0, 0, 255, 255, 255, 255],
    [1, 0, 255, 255, 255, 255],
    [1, 1, 255, 255, 255, 255],
  ]));
  assert.equal(connected.clusters, 1);
  assert.equal(connected.suspectPixels, 3);
  assert.equal(connected.largest.size, 3);
  assert.deepEqual(connected.largest.bbox, { x0: 0, y0: 0, x1: 1, y1: 1 });
});

test('deltaPixels: alpha and visible-colour changes; transparent RGB is separate', () => {
  const a = image(2, 1, [[0, 0, 255, 0, 0, 255], [1, 0, 10, 20, 30, 0]]);
  const b = image(2, 1, [[0, 0, 0, 0, 255, 255], [1, 0, 40, 50, 60, 0]]);
  const d = deltaPixels(a, b);
  assert.equal(d.changed, 1);
  assert.equal(d.transparentRgbOnly, 1);
  assert.equal(d.allRgbaChanged, 2);
  assert.equal(d.fraction, 0.5);
  assert.deepEqual(d.bbox, { x0: 0, y0: 0, x1: 0, y1: 0 });

  const opaque = image(1, 1, [[0, 0, 255, 0, 0, 255]]);
  const semi = image(1, 1, [[0, 0, 255, 0, 0, 128]]);
  const alpha = deltaPixels(opaque, semi);
  assert.equal(alpha.changed, 1);
  assert.equal(alpha.transparentRgbOnly, 0);
  assert.equal(alpha.fraction, 1);

  const invisible = deltaPixels(
    image(1, 1, [[0, 0, 255, 0, 0, 0]]),
    image(1, 1, [[0, 0, 0, 255, 0, 0]]),
  );
  assert.equal(invisible.changed, 0);
  assert.equal(invisible.transparentRgbOnly, 1);
  assert.equal(invisible.fraction, 0);
  assert.equal(invisible.bbox, null);

  assert.deepEqual(deltaPixels(opaque, opaque), {
    changed: 0, transparentRgbOnly: 0, allRgbaChanged: 0, total: 1, fraction: 0, bbox: null,
  });
  assert.equal(deltaPixels(opaque, image(2, 1)), null);
});

test('bboxDelta: >8 px threshold and empty-side handling', () => {
  assert.equal(bboxDelta({ x0: 0, y0: 0, x1: 9, y1: 9 }, { x0: 7, y0: 1, x1: 16, y1: 10 }).flagged, false);
  const flagged = bboxDelta({ x0: 0, y0: 0, x1: 9, y1: 9 }, { x0: 9, y0: 1, x1: 19, y1: 10 });
  assert.equal(flagged.flagged, true);
  assert.deepEqual(flagged, { dx: 9, dy: 1, dw: 1, dh: 0, flagged: true });
  assert.deepEqual(bboxDelta(null, { x0: 0, y0: 0, x1: 0, y1: 0 }), {
    dx: null, dy: null, dw: null, dh: null, flagged: true, empty: true,
  });
  assert.equal(bboxDelta(null, null), null);
});

test('analyzeClip: composite-only duplicate loop, indices, durations and metadata', () => {
  const red = solid('red.png', 4, 4, [255, 0, 0, 255]);
  const blue = solid('blue.png', 4, 4, [0, 0, 255, 255]);
  const clip = writeClip('composite-loop', {
    id: 'synthetic-dup', direction: 'back_r', action: 'Test', loop: true, oneShot: false,
    durationsMs: [100, 100, 100], groundY: 3,
    frames: [
      { index: 10, durationMs: 100, png: red, sha256: fileSha(red) },
      { index: 11, durationMs: 100, png: blue },
      { index: 12, durationMs: 100, png: red },
    ],
  });
  const out = analyzeClip(clip).clip;
  assert.equal(out.frameCount, 3);
  assert.equal(out.loop, true);
  assert.equal(out.totalDurationMs, 300);
  assert.equal(out.groundY, 3);
  assert.equal(out.summary.bodyIsComposite, true);
  assert.equal(out.summary.exactDuplicatePairCount, 1);
  assert.deepEqual(out.duplicates.list, [{ surface: 'composite', a: 10, b: 12 }]);
  assert.equal(out.summary.lastVsFirst.bodyFraction, 0);
  assert.equal(out.frames[0].index, 10);
  assert.equal(out.frames[0].composite.shaSource, 'metadata');
  assert.equal(out.frames[0].composite.shaMatchesFile, true);
  assert.equal(out.frames[1].composite.shaSource, 'computed');
  assert.equal(out.frames[1].composite.shaMatchesFile, null);
  assert.equal(out.frames[0].brightEdge.body, null);
  assert.equal(out.frames[0].silhouette.body.layer, null);
  assert.equal(out.frames[0].silhouette.body.opaque, 16);
  assert.equal(out.frames[1].delta.body.fromPrev, 10);
  assert.equal(out.frames[1].delta.body.to, 11);
  assert.equal(out.frames[1].delta.body.fromPrevPixels, 16);
  assert.equal(out.frames[1].delta.body.fromPrevTransparentRgbOnly, 0);
  assert.equal(out.frames[1].delta.body.fromPrevFraction, 1);
  assert.equal(out.frames[2].delta.body.fromPrevFraction, 1);
});

test('duplicate pairs: three identical frames count three unordered pairs', () => {
  const red = solid('dup3.png', 2, 2, [255, 0, 0, 255]);
  const clip = writeClip('dup3', {
    direction: 'back_r', action: 'Test', loop: true,
    frames: [0, 1, 2].map((index) => ({ index, png: red })),
  });
  const out = analyzeClip(clip).clip;
  assert.equal(out.duplicates.totalPairs, 3);
  assert.deepEqual(out.duplicates.list, [
    { surface: 'composite', a: 0, b: 1 },
    { surface: 'composite', a: 0, b: 2 },
    { surface: 'composite', a: 1, b: 2 },
  ]);
});

test('analyzeClip: body layer, layer order, composed composite and body highlight', () => {
  const body = writePng('body.png', 4, 4, [
    [0, 0, 80, 80, 80, 255], [1, 0, 80, 80, 80, 255],
    [0, 1, 80, 80, 80, 255], [1, 1, 80, 80, 80, 255],
  ]);
  const weapon = writePng('weapon.png', 4, 4, [[3, 3, 255, 255, 255, 255]]);
  const clip = writeClip('layered-body', {
    direction: 'back_l', action: 'Test', loop: false,
    layerOrder: ['weapon', 'body'],
    frames: [
      { index: 0, layers: { body: { png: body }, weapon: { png: weapon } } },
      { index: 1, layers: { body: { png: body }, weapon: { png: weapon } } },
    ],
  });
  const out = analyzeClip(clip).clip;
  const f = out.frames[0];
  assert.equal(out.frameCount, 2);
  assert.deepEqual(out.duplicates.list, [
    { surface: 'body', a: 0, b: 1 },
    { surface: 'composite', a: 0, b: 1 },
  ]);
  assert.equal(f.bodyIsComposite, false);
  assert.deepEqual(f.layers.map((l) => l.name), ['weapon', 'body']);
  assert.equal(f.silhouette.body.layer, 'body');
  assert.equal(f.silhouette.body.opaque, 4);
  assert.equal(f.silhouette.composite.opaque, 5);
  assert.notEqual(f.brightEdge.body, null);
  assert.equal(f.brightEdge.body.suspectPixels, 0);
  assert.equal(f.brightEdge.composite.suspectPixels, 1);
  assert.equal(f.composite.file, null);
  assert.equal(f.composite.shaSource, 'computed');
  assert.match(f.composite.sha256, /^[0-9a-f]{64}$/);
  assert.equal(f.file, path.relative(ROOT, body).split(path.sep).join('/'));
  const expected = pixelSha(composite([decode(weapon).image, decode(body).image], 4, 4));
  assert.equal(f.composite.sha256, expected);
});

test('analyzeClip: layers without a body fall back to composite', () => {
  const weapon = writePng('only-weapon.png', 4, 4, [[2, 2, 255, 255, 255, 255]]);
  const clip = writeClip('no-body', {
    direction: 'back_r', action: 'Test',
    frames: [{ index: 0, layers: { weapon: { png: weapon } } }],
  });
  const out = analyzeClip(clip).clip;
  const f = out.frames[0];
  assert.equal(f.bodyIsComposite, true);
  assert.equal(f.silhouette.body.layer, null);
  assert.equal(f.silhouette.body.opaque, f.silhouette.composite.opaque);
  assert.equal(f.brightEdge.body, null);
  assert.equal(f.composite.file, null);
  assert.equal(f.composite.shaSource, 'computed');
});

test('analyzeClip: BOM-tolerant clip JSON and uppercase body name', () => {
  const body = writePng('Body.png', 2, 2, [[0, 0, 10, 20, 30, 255]]);
  const file = path.join(TMP, 'bom.json');
  fs.writeFileSync(file, `\uFEFF${JSON.stringify({
    direction: 'front_r', action: 'Test',
    frames: [{ index: 0, layers: { Body: { png: body } } }],
  })}`);
  const out = analyzeClip(file).clip;
  assert.equal(out.frames[0].bodyIsComposite, false);
  assert.equal(out.frames[0].silhouette.body.layer, 'Body');
});

test('analyzeClip: relative layer paths resolve against the clip directory first', () => {
  const localDir = path.join(TMP, 'local-assets');
  fs.mkdirSync(localDir);
  const body = writePng('local-body.png', 2, 2, [[0, 0, 9, 8, 7, 255]]);
  fs.copyFileSync(body, path.join(localDir, 'body.png'));
  const clipFile = path.join(localDir, 'clip.json');
  fs.writeFileSync(clipFile, JSON.stringify({
    direction: 'front_l', action: 'Local',
    frames: [{ index: 0, layers: { body: { png: 'body.png' } } }],
  }));
  const out = analyzeClip(clipFile).clip;
  assert.equal(out.frames[0].silhouette.body.opaque, 1);
  assert.equal(out.frames[0].file, path.relative(ROOT, path.join(localDir, 'body.png')).split(path.sep).join('/'));
});

test('errors: missing, corrupt, empty, malformed and mismatched canvases', () => {
  const missing = writeClip('missing-png', { frames: [{ index: 0, png: path.join(TMP, 'nope.png') }] });
  assert.throws(() => analyzeClip(missing), /PNG not found/);

  const corruptPath = path.join(TMP, 'corrupt.png');
  fs.writeFileSync(corruptPath, 'not a png');
  const corrupt = writeClip('corrupt-png', { frames: [{ index: 0, png: corruptPath }] });
  assert.throws(() => analyzeClip(corrupt), /PNG decode failed/);

  assert.throws(() => analyzeClip(writeClip('empty', { frames: [] })), /no frames/);
  assert.throws(() => analyzeClip(writeClip('neither', { frames: [{ index: 0 }] })), /neither png nor layers/);

  const body = writePng('mismatch-body.png', 4, 4, [[0, 0, 1, 2, 3, 255]]);
  const weapon = writePng('mismatch-weapon.png', 5, 4, [[0, 0, 1, 2, 3, 255]]);
  const mismatch = writeClip('mismatch', {
    frames: [{ index: 0, layers: { body: { png: body }, weapon: { png: weapon } } }],
  });
  assert.throws(() => analyzeClip(mismatch), /Layer canvas mismatch/);
  const compositeOnly = solid('mixed-composite.png', 4, 4, [1, 2, 3, 255]);
  const mixed = writeClip('mixed-body', {
    frames: [
      { index: 0, layers: { body: { png: body } } },
      { index: 1, png: compositeOnly },
    ],
  });
  assert.throws(() => analyzeClip(mixed), /Inconsistent body layer presence/);
  const dupIndex = writeClip('dup-index', {
    frames: [
      { index: 0, layers: { body: { png: body } } },
      { index: 0, layers: { body: { png: body } } },
    ],
  });
  assert.throws(() => analyzeClip(dupIndex), /Duplicate frame index/);
  assert.throws(() => analyzeClip(path.join(TMP, 'does-not-exist.json')), /Clip not found/);
});

test('analyzeClip: composite 4x4 with 5x4 layers fails explicitly; valid layers still pass', () => {
  const composite = solid('composite-4x4.png', 4, 4, [10, 20, 30, 255]);
  const body5 = writePng('body-5x4.png', 5, 4, [[0, 0, 80, 80, 80, 255]]);
  const weapon5 = writePng('weapon-5x4.png', 5, 4, [[4, 3, 255, 255, 255, 255]]);
  const mismatch = writeClip('composite-mismatch-layer', {
    direction: 'back_r', action: 'Mismatch',
    frames: [{
      index: 0,
      png: composite,
      layers: { body: { png: body5 }, weapon: { png: weapon5 } },
    }],
  });
  assert.throws(
    () => analyzeClip(mismatch),
    /Layer canvas mismatch .*body is 5x4, composite is 4x4/,
  );

  const body4 = writePng('body-4x4.png', 4, 4, [[0, 0, 80, 80, 80, 255]]);
  const weapon4 = writePng('weapon-4x4.png', 4, 4, [[3, 3, 255, 255, 255, 255]]);
  const valid = writeClip('composite-matching-layers', {
    direction: 'back_r', action: 'Matching',
    frames: [{
      index: 0,
      png: composite,
      layers: { body: { png: body4 }, weapon: { png: weapon4 }, omitted: {} },
    }],
  });
  const out = analyzeClip(valid).clip;
  assert.equal(out.frames[0].bodyIsComposite, false);
  assert.deepEqual(out.frames[0].layers.map((l) => l.name), ['body', 'weapon']);
  assert.deepEqual(out.frames[0].size, [4, 4]);

  const noBody = writeClip('composite-no-body-layer', {
    direction: 'back_r', action: 'NoBody',
    frames: [{ index: 0, png: composite, layers: { weapon: { png: weapon4 } } }],
  });
  const fallback = analyzeClip(noBody).clip;
  assert.equal(fallback.frames[0].bodyIsComposite, true);
  assert.equal(fallback.frames[0].brightEdge.body, null);
  assert.equal(
    fallback.frames[0].silhouette.body.opaque,
    fallback.frames[0].silhouette.composite.opaque,
  );
});

test('analyzeClip: overwriting a PNG between calls is not masked by a stale cache', () => {
  const pngFile = solid('cache-overwrite.png', 2, 2, [255, 0, 0, 255]);
  const clip = writeClip('cache-overwrite', {
    direction: 'back_r', action: 'Cache',
    frames: [{ index: 0, png: pngFile }],
  });
  const first = analyzeClip(clip).clip;
  const firstSha = first.frames[0].composite.sha256;
  assert.equal(first.frames[0].composite.shaSource, 'computed');
  assert.equal(first.frames[0].silhouette.composite.opaque, 4);

  writePng('cache-overwrite.png', 2, 2, [[0, 0, 0, 0, 255, 255]]);
  const second = analyzeClip(clip).clip;
  assert.notEqual(second.frames[0].composite.sha256, firstSha);
  assert.equal(second.frames[0].composite.shaSource, 'computed');
  assert.equal(second.frames[0].silhouette.composite.opaque, 1);
  assert.deepEqual(second.frames[0].silhouette.composite.bbox, { x0: 0, y0: 0, x1: 0, y1: 0 });

  writePng('cache-overwrite.png', 2, 2, [[0, 0, 0, 0, 128, 128]]);
  const third = analyzeClip(clip).clip;
  assert.equal(third.frames[0].silhouette.composite.opaque, 1);
  assert.equal(third.frames[0].silhouette.composite.partialAlpha, 1);
  assert.notEqual(third.frames[0].composite.sha256, second.frames[0].composite.sha256);
});

test('real back_l/Walk: alpha-aware delta regression and binary alpha', () => {
  const clip = path.join(ROOT, 'characters/orc-v1/source/rear-recovery-v2/back_l/Walk/clip.json');
  const a = analyzeClip(clip).clip;
  const b = analyzeClip(clip).clip;
  assert.equal(JSON.stringify(a), JSON.stringify(b));
  assert.equal(a.frameCount, 8);
  assert.equal(a.loop, true);
  assert.equal(a.summary.maxBodyDelta.from, 6);
  assert.equal(a.summary.maxBodyDelta.to, 7);
  assert.equal(a.summary.maxBodyDelta.fraction, 0.0732);
  assert.equal(a.summary.lastVsFirst.bodyFraction, 0.074);
  assert.equal(a.summary.lastVsFirst.bodyPixels, 4849);
  assert.equal(a.summary.lastVsFirst.bodyTransparentRgbOnly, 10172);
  assert.equal(a.summary.lastVsFirst.bodyAllRgbaChanged, 15021);
  assert.equal(a.frames[1].delta.body.fromPrevPixels, 4613);
  assert.equal(a.frames[1].delta.body.fromPrevTransparentRgbOnly, 10352);
  assert.equal(a.frames[1].delta.body.fromPrevAllRgbaChanged, 14965);
  assert.equal(a.frames[7].delta.body.vsFirstFraction, 0.074);
  assert.equal(a.frames[0].silhouette.composite.partialAlpha, 0);
});

test('CLI --all: two runs are byte-identical and keep the 15-clip scope', () => {
  const diag = path.join(DIAG_DIR, 'diag.mjs');
  const one = path.join(TMP, 'all-1.json');
  const two = path.join(TMP, 'all-2.json');
  execFileSync(process.execPath, [diag, '--all', '--out', one], { cwd: ROOT, stdio: 'pipe' });
  execFileSync(process.execPath, [diag, '--all', '--out', two], { cwd: ROOT, stdio: 'pipe' });
  assert.equal(fs.readFileSync(one).equals(fs.readFileSync(two)), true);
  const doc = JSON.parse(fs.readFileSync(one, 'utf8'));
  assert.equal(doc.clipCount, 15);
  assert.equal(doc.manifest.activeCandidateCount, 15);
  assert.equal(doc.clips.reduce((s, c) => s + c.frameCount, 0), 123);
  assert.equal(doc.clips.reduce((s, c) => s + c.frames.reduce((n, f) => n + f.layers.length, 0), 0), 180);
  for (const c of doc.clips) {
    for (const f of c.frames) {
      assert.deepEqual(f.size, [256, 256], `${c.label} f${f.index} size`);
      assert.equal(f.silhouette.composite.partialAlpha, 0, `${c.label} f${f.index} composite partial alpha`);
      assert.equal(f.silhouette.body.partialAlpha, 0, `${c.label} f${f.index} body partial alpha`);
      if (f.composite.file) assert.equal(f.composite.shaMatchesFile, true, `${c.label} f${f.index} composite sha`);
      for (const l of f.layers) assert.equal(l.shaMatchesFile, true, `${c.label} f${f.index} layer ${l.name} sha`);
    }
  }
  assert.equal(doc.clips.find((c) => c.label === 'back_l/Walk').summary.maxBodyDelta.from, 6);
  assert.equal(doc.clips.find((c) => c.label === 'back_l/Walk').summary.lastVsFirst.bodyFraction, 0.074);
});
