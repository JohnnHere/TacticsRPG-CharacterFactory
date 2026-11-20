#!/usr/bin/env node
// QA-only dry run: grow the handFront occlusion patch by BFS from the existing patch,
// expanding only into body pixels that the weapon layers actually cover.
// Never writes to masters: emits new PNGs + a JSON summary into the output dir.
// Usage: node dryrun-handfront.mjs <clip.json> <outDir> <prefix>
import fs from 'node:fs';
import path from 'node:path';
import { PNG } from 'pngjs';

const [, , clipArg, outDir, prefix = 'cand', maxDistArg = '7'] = process.argv;
const maxDist = Number(maxDistArg);
const clip = JSON.parse(fs.readFileSync(clipArg, 'utf8'));
fs.mkdirSync(outDir, { recursive: true });
const read = (p) => PNG.sync.read(fs.readFileSync(p));
const A = (img, x, y) => img.data[(y * img.width + x) * 4 + 3];
const summary = { clip: clipArg, frames: [] };

for (const f of clip.frames) {
  const body = read(f.layers.body.png);
  const wb = read(f.layers.weaponBack.png);
  const wf = read(f.layers.weaponFront.png);
  const hf = read(f.layers.handFront.png);
  const W = body.width;
  const H = body.height;
  // candidate expansion set: body pixels covered by any weapon layer
  const inSet = new Uint8Array(W * H);
  for (let y = 0; y < H; y += 1) {
    for (let x = 0; x < W; x += 1) {
      const i = y * W + x;
      if (A(body, x, y) && (A(wb, x, y) || A(wf, x, y))) inSet[i] = 1;
    }
  }
  const keep = new Uint8Array(W * H);
  const queue = [];
  for (let y = 0; y < H; y += 1) {
    for (let x = 0; x < W; x += 1) {
      const i = y * W + x;
      if (A(hf, x, y)) {
        keep[i] = 1;
        queue.push(i);
      }
    }
  }
  let added = 0;
  const addedPx = [];
  while (queue.length) {
    const i = queue.pop();
    const x = i % W;
    const y = (i - x) / W;
    for (let dy = -1; dy <= 1; dy += 1) {
      for (let dx = -1; dx <= 1; dx += 1) {
        if (!dx && !dy) continue;
        const nx = x + dx;
        const ny = y + dy;
        if (nx < 0 || ny < 0 || nx >= W || ny >= H) continue;
        const [gx, gy] = f.rightGrip ?? [0, 0];
        if (Math.max(Math.abs(nx - gx), Math.abs(ny - gy)) > maxDist) continue;
        const ni = ny * W + nx;
        if (keep[ni] || !inSet[ni]) continue;
        keep[ni] = 1;
        added += 1;
        addedPx.push([nx, ny]);
        queue.push(ni);
      }
    }
  }
  // build the new handFront image from body pixels
  const nh = new PNG({ width: W, height: H });
  nh.data.fill(0);
  let moved = 0;
  for (let y = 0; y < H; y += 1) {
    for (let x = 0; x < W; x += 1) {
      const i = y * W + x;
      if (!keep[i]) continue;
      const s = (y * W + x) * 4;
      nh.data[s] = body.data[s];
      nh.data[s + 1] = body.data[s + 1];
      nh.data[s + 2] = body.data[s + 2];
      nh.data[s + 3] = body.data[s + 3];
      if (!A(hf, x, y)) moved += 1;
    }
  }
  // weapon visibility connectivity: the weapon must not be severed by the added patch
  const weaponComponents = (useHf) => {
    const seen = new Uint8Array(W * H);
    let count = 0;
    let largest = 0;
    for (let y = 0; y < H; y += 1) {
      for (let x = 0; x < W; x += 1) {
        const i = y * W + x;
        if (seen[i]) continue;
        const visible = (A(wb, x, y) || A(wf, x, y)) && !A(useHf, x, y);
        if (!visible) continue;
        const stack = [i];
        seen[i] = 1;
        let n = 0;
        while (stack.length) {
          const j = stack.pop();
          n += 1;
          const jx = j % W;
          const jy = (j - jx) / W;
          for (let dy = -1; dy <= 1; dy += 1) {
            for (let dx = -1; dx <= 1; dx += 1) {
              if (!dx && !dy) continue;
              const nx = jx + dx;
              const ny = jy + dy;
              if (nx < 0 || ny < 0 || nx >= W || ny >= H) continue;
              const ni = ny * W + nx;
              if (seen[ni]) continue;
              if (!((A(wb, nx, ny) || A(wf, nx, ny)) && !A(useHf, nx, ny))) continue;
              seen[ni] = 1;
              stack.push(ni);
            }
          }
        }
        count += 1;
        if (n > largest) largest = n;
      }
    }
    return { count, largest };
  };
  const wcBefore = weaponComponents(hf);
  const wcAfter = weaponComponents(nh);
  // composite before/after
  const render = (useHf) => {
    const out = new PNG({ width: W, height: H });
    for (let y = 0; y < H; y += 1) {
      for (let x = 0; x < W; x += 1) {
        const layersInOrder = [wb, body, wf, useHf];
        let r = 0;
        let g = 0;
        let b = 0;
        let a = 0;
        for (const img of layersInOrder) {
          if (!A(img, x, y)) continue;
          const s = (y * W + x) * 4;
          r = img.data[s];
          g = img.data[s + 1];
          b = img.data[s + 2];
          a = 255;
        }
        const d = (y * W + x) * 4;
        out.data[d] = r;
        out.data[d + 1] = g;
        out.data[d + 2] = b;
        out.data[d + 3] = a;
      }
    }
    return out;
  };
  const before = render(hf);
  const after = render(nh);
  let changed = 0;
  for (let i = 0; i < W * H; i += 1) {
    const s = i * 4;
    if (
      before.data[s] !== after.data[s] ||
      before.data[s + 1] !== after.data[s + 1] ||
      before.data[s + 2] !== after.data[s + 2] ||
      before.data[s + 3] !== after.data[s + 3]
    ) changed += 1;
  }
  fs.writeFileSync(path.join(outDir, `${prefix}-f${String(f.index).padStart(2, '0')}-handFront.png`), PNG.sync.write(nh));
  fs.writeFileSync(path.join(outDir, `${prefix}-f${String(f.index).padStart(2, '0')}-before.png`), PNG.sync.write(before));
  fs.writeFileSync(path.join(outDir, `${prefix}-f${String(f.index).padStart(2, '0')}-after.png`), PNG.sync.write(after));
  const bb = addedPx.length
    ? [Math.min(...addedPx.map((p) => p[0])), Math.min(...addedPx.map((p) => p[1])), Math.max(...addedPx.map((p) => p[0])), Math.max(...addedPx.map((p) => p[1]))]
    : null;
  summary.frames.push({ index: f.index, grip: f.rightGrip, weaponVisible: f.weaponVisible, added, moved, changed, addedBBox: bb, weaponComponents: { before: wcBefore, after: wcAfter } });
  console.log(
    `f${f.index} weaponVisible=${f.weaponVisible} addedToPatch=${added} newPixels=${moved} compositeChanged=${changed} bbox=${bb ? bb.join(',') : 'none'} weaponParts ${wcBefore.count}->${wcAfter.count}`,
  );
}
fs.writeFileSync(path.join(outDir, `${prefix}-summary.json`), JSON.stringify(summary, null, 2));
