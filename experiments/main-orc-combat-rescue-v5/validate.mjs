import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { parseArgs } from 'node:util';
import { ROOT, hash, readJSON } from '../../src/core.mjs';
import { decode, composite, measure } from '../../src/images.mjs';
import { inspectAseprite } from '../../src/aseprite.mjs';

const { values } = parseArgs({ options: {
  manifest: { type: 'string', default: 'characters/orc-v1/source/combat-rescue-v5/candidate28manifest.json' },
  output: { type: 'string', default: 'experiments/main-orc-combat-rescue-v5/technical-validation.json' },
} });
const absolute = file => path.resolve(ROOT, file);
const digest = file => hash(fs.readFileSync(absolute(file)));
const png = file => decode(absolute(file)).image;
const layerOrder = ['weaponBack', 'body', 'weaponFront', 'handFront'];
const key = cell => `${cell.direction}/${cell.action}`;
const manifest = readJSON(absolute(values.manifest));
const parent = readJSON(absolute('characters/orc-v1/source/rear-reconstruction-v4/candidate28manifest.json'));
const parentCells = new Map(parent.cells.map(cell => [key(cell), cell]));
const seen = new Set();
const cells = [];
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

function declaredHash(object, fileField, hashField, required) {
  if (!object[fileField]) return;
  const actual = digest(object[fileField]);
  if (required) assert.equal(typeof object[hashField], 'string', `Missing ${hashField}: ${object[fileField]}`);
  if (object[hashField]) {
    assert.equal(object[hashField], actual, `Stale ${hashField}: ${object[fileField]}`);
    hashesChecked++;
  }
}

assert.equal(manifest.characterId, 'orc-v1');
assert.equal(manifest.cells.length, 28);
for (const cell of manifest.cells) {
  const id = key(cell);
  assert.ok(parentCells.has(id) && !seen.has(id), `Unknown or duplicate cell: ${id}`);
  seen.add(id);
  const parentCell = parentCells.get(id);
  const protectedClip = ['Idle', 'Hit'].includes(cell.action) ||
    (cell.action === 'Defeat' && cell.direction.startsWith('back_'));
  if (protectedClip || !cell.isAffected) {
    assert.equal(cell.clipJson, parentCell.clipJson, `Protected/alias path changed: ${id}`);
    assert.equal(cell.status, 'UNCHANGED_ALIAS', `Alias status: ${id}`);
  }
  const clip = readJSON(absolute(cell.clipJson));
  declaredHash(cell, 'clipJson', 'clipSha256', manifest.revision === 'main-orc-combat-rescue-v5');
  assert.ok(clip.frames.length > 0, `Empty clip: ${id}`);
  if (cell.isAffected) assert.ok(clip.nativeMaster, `Missing native master: ${id}`);
  assert.deepEqual(clip.canvas, [256, 256], `Canvas: ${id}`);
  assert.equal(clip.groundY, 190, `Ground contract: ${id}`);
  const durations = clip.frames.map(frame => frame.durationMs);
  assert.ok(durations.every(duration => Number.isInteger(duration) && duration > 0), `Durations: ${id}`);
  assert.equal(clip.totalDurationMs, durations.reduce((sum, duration) => sum + duration, 0), `Total time: ${id}`);
  for (const [fileField, hashField, size] of [
    ['master', 'masterSha256', [256, 256]],
    ['bodyMaster', 'bodyMasterSha256', [256, 256]],
    ['handMaster', 'handMasterSha256', [256, 256]],
    ['nativeMaster', 'nativeMasterSha256', [128, 128]],
  ]) {
    if (!clip[fileField]) continue;
    declaredHash(clip, fileField, hashField, cell.isAffected);
    const header = inspectAseprite(absolute(clip[fileField]));
    assert.deepEqual([header.width, header.height], size, `Master canvas: ${id}/${fileField}`);
    assert.deepEqual(header.durationsMs, durations, `Master timing: ${id}/${fileField}`);
  }
  assert.ok(clip.master, `Missing master: ${id}`);
  assert.ok(clip.strip, `Missing strip: ${id}`);
  declaredHash(clip, 'strip', 'stripSha256', cell.isAffected);
  const strip = png(clip.strip);
  assert.ok([128, 256].includes(strip.height), `Strip height: ${id}`);
  assert.equal(strip.width, strip.height * clip.frames.length, `Strip frame layout: ${id}`);
  const weapon = ['Sword', 'Axe'].includes(cell.action);
  for (const [index, frame] of clip.frames.entries()) {
    framesChecked++;
    const label = `${id}/${index}`;
    declaredHash(frame, 'png', 'sha256', cell.isAffected);
    if (cell.isAffected) assert.ok(frame.nativePng, `Missing native frame: ${label}`);
    declaredHash(frame, 'nativePng', 'nativeSha256', cell.isAffected);
    const image = png(frame.png);
    assert.deepEqual([image.width, image.height], [256, 256], `Frame canvas: ${label}`);
    assert.equal(measure(image).partial, 0, `Partial alpha: ${label}`);
    let body = image;
    if (weapon) {
      const layers = layerOrder.map(name => {
        const layer = frame.layers?.[name];
        assert.ok(layer?.png, `Missing layer ${name}: ${label}`);
        declaredHash(layer, 'png', 'sha256', cell.isAffected);
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
      const stripFrame = strip.height === 128 ? png(frame.nativePng) : image;
      for (let y = 0; y < strip.height; y++) for (let x = 0; x < strip.height; x++) {
        const source = (y * strip.width + index * strip.height + x) * 4;
        const target = (y * strip.height + x) * 4;
        assert.equal(strip.data[source + 3], stripFrame.data[target + 3], `Strip alpha: ${label}`);
        if (strip.data[source + 3]) for (let c = 0; c < 3; c++) {
          assert.equal(strip.data[source + c], stripFrame.data[target + c], `Strip pixels: ${label}`);
        }
      }
    }
  }
  cells.push({ id, frames: clip.frames.length, protected: protectedClip, isAffected: cell.isAffected });
}
assert.equal(seen.size, 28);
assert.equal(manifest.totalClips, 28);
if (manifest.totalFrames !== undefined) assert.equal(manifest.totalFrames, framesChecked);
for (const [field, statuses] of [
  ['activeCandidatesCount', ['ACTIVE_CANDIDATE']],
  ['unchangedAliasesCount', ['UNCHANGED_ALIAS']],
  ['inRevisionCount', ['IN_REVISION', 'ARTISTIC_REVISION_REQUIRED']],
  ['inProductionCount', ['IN_PRODUCTION']],
]) {
  assert.equal(manifest[field], manifest.cells.filter(cell => statuses.includes(cell.status)).length, `Declared ${field}`);
}
const result = {
  status: 'TECHNICAL_PASS',
  manifest: values.manifest,
  manifestSha256: digest(values.manifest),
  framesChecked,
  hashesChecked,
  cells,
  semanticWeaponAbsence: 'REQUIRES_VISUAL_QA',
  anatomyGripMotion: 'REQUIRES_VISUAL_QA',
  creatorApproval: 'PENDING_CREATOR',
};
fs.mkdirSync(path.dirname(absolute(values.output)), { recursive: true });
fs.writeFileSync(absolute(values.output), JSON.stringify(result, null, 2));
console.log(JSON.stringify({ status: result.status, cells: cells.length, framesChecked, hashesChecked }));
