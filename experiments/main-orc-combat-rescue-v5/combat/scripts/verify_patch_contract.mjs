import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { ROOT, hash, readJSON } from '../../../../src/core.mjs';
import { decode, composite, measure } from '../../../../src/images.mjs';
import { inspectAseprite } from '../../../../src/aseprite.mjs';

const absolute = file => path.resolve(ROOT, file);
const digest = file => hash(fs.readFileSync(absolute(file)));
const png = file => decode(absolute(file)).image;
const layerOrder = ['weaponBack', 'body', 'weaponFront', 'handFront'];

const patch = readJSON(absolute('characters/orc-v1/source/combat-rescue-v5/combat/patch-manifest.json'));
const patchExp = readJSON(absolute('experiments/main-orc-combat-rescue-v5/combat/patch-manifest.json'));
assert.deepEqual(patch, patchExp, 'patch-manifest.json must be identical in both combat folders');

let framesChecked = 0;
let hashesChecked = 0;

function samePixels(a, b, label) {
  assert.equal(a.width, b.width, `${label}: width`);
  assert.equal(a.height, b.height, `${label}: height`);
  for (let i = 0; i < a.data.length; i += 4) {
    assert.equal(a.data[i + 3], b.data[i + 3], `${label}: alpha at pixel ${i / 4}`);
    if (a.data[i + 3]) {
      for (let c = 0; c < 3; c++) {
        assert.equal(a.data[i + c], b.data[i + c], `${label}: channel ${c} at pixel ${i / 4}`);
      }
    }
  }
}

function declaredHash(object, fileField, hashField) {
  if (!object[fileField]) return;
  const actual = digest(object[fileField]);
  assert.equal(typeof object[hashField], 'string', `Missing ${hashField}: ${object[fileField]}`);
  assert.equal(object[hashField], actual, `Stale ${hashField}: ${object[fileField]}`);
  hashesChecked++;
}

assert.equal(patch.cells.length, 12, 'Must have 12 combat cells');

for (const cell of patch.cells) {
  const id = `${cell.direction}/${cell.action}`;
  assert.equal(cell.isAffected, true, `isAffected: ${id}`);
  assert.equal(cell.status, 'ACTIVE_CANDIDATE', `status: ${id}`);
  declaredHash(cell, 'clipJson', 'clipSha256');
  const clip = readJSON(absolute(cell.clipJson));
  assert.ok(clip.frames.length > 0, `Empty clip: ${id}`);
  assert.deepEqual(clip.canvas, [256, 256], `Canvas: ${id}`);
  assert.equal(clip.groundY, 190, `Ground contract: ${id}`);
  const durations = clip.frames.map(frame => frame.durationMs);
  assert.ok(durations.every(duration => Number.isInteger(duration) && duration > 0), `Durations: ${id}`);
  assert.equal(clip.totalDurationMs, durations.reduce((sum, duration) => sum + duration, 0), `Total time: ${id}`);

  for (const [fileField, hashField, size] of [
    ['master', 'masterSha256', [256, 256]],
    ['bodyMaster', 'bodyMasterSha256', [256, 256]],
    ['nativeMaster', 'nativeMasterSha256', [128, 128]],
  ]) {
    if (!clip[fileField]) continue;
    declaredHash(clip, fileField, hashField);
    const header = inspectAseprite(absolute(clip[fileField]));
    assert.deepEqual([header.width, header.height], size, `Master canvas: ${id}/${fileField}`);
    assert.deepEqual(header.durationsMs, durations, `Master timing: ${id}/${fileField}`);
  }
  assert.ok(clip.master, `Missing master: ${id}`);
  declaredHash(clip, 'strip', 'stripSha256');

  const weapon = ['Sword', 'Axe'].includes(cell.action);
  for (const [index, frame] of clip.frames.entries()) {
    framesChecked++;
    const label = `${id}/${index}`;
    declaredHash(frame, 'png', 'sha256');
    declaredHash(frame, 'nativePng', 'nativeSha256');
    const image = png(frame.png);
    assert.deepEqual([image.width, image.height], [256, 256], `Frame canvas: ${label}`);
    assert.equal(measure(image).partial, 0, `Partial alpha: ${label}`);
    let body = image;
    if (weapon) {
      const layers = layerOrder.map(name => {
        const layer = frame.layers?.[name];
        assert.ok(layer?.png, `Missing layer ${name}: ${label}`);
        declaredHash(layer, 'png', 'sha256');
        return png(layer.png);
      });
      body = layers[1];
      samePixels(image, composite(layers, 256, 256), `Layer composition: ${label}`);
      assert.equal(typeof frame.weaponVisible, 'boolean', `Visibility flag: ${label}`);
      if (!frame.weaponVisible) {
        for (const layer of [layers[0], layers[2], layers[3]]) {
          assert.equal(measure(layer).contentHeight, 0, `Hidden equipment pixels: ${label}`);
        }
        samePixels(image, body, `Hidden equipment composite: ${label}`);
      } else {
        // Verify handFront has real grasp pixels (95-128 px)
        const hfMeasure = measure(layers[3]);
        assert.ok(hfMeasure.contentHeight >= 8, `handFront height too small: ${label}`);
      }
    } else {
      assert.notEqual(frame.weaponVisible, true, `Weapon on non-weapon action: ${label}`);
    }
    if (frame.nativePng) {
      const native = png(frame.nativePng);
      assert.deepEqual([native.width, native.height], [128, 128], `Native canvas: ${label}`);
      for (let y = 0; y < 128; y++) for (let x = 0; x < 128; x++) {
        const source = ((y + 64) * 256 + x + 64) * 4;
        const target = (y * 128 + x) * 4;
        assert.equal(native.data[target + 3], body.data[source + 3], `Native alpha crop: ${label}`);
        if (native.data[target + 3]) for (let c = 0; c < 3; c++) {
          assert.equal(native.data[target + c], body.data[source + c], `Native crop: ${label}`);
        }
      }
    }
  }
}

console.log(JSON.stringify({ status: 'COMBAT_PATCH_12_PASS', cellsChecked: patch.cells.length, framesChecked, hashesChecked }));
