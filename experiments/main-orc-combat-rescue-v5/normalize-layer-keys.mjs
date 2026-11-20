import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { parseArgs } from 'node:util';
import { ROOT, hash, readJSON } from '../../src/core.mjs';

const { values } = parseArgs({ options: {
  clips: { type: 'string', multiple: true, required: true },
  output: { type: 'string', default: 'experiments/main-orc-combat-rescue-v5/layer-key-normalization.json' },
} });
const absolute = file => path.resolve(ROOT, file);
const digest = file => hash(fs.readFileSync(absolute(file)));

const collected = [];
for (const clipPath of values.clips) {
  const before = readJSON(absolute(clipPath));
  const beforeSha = digest(clipPath);
  let renamed = 0;
  const layersTouched = [];
  for (const frame of before.frames) {
    for (const [name, layer] of Object.entries(frame.layers ?? {})) {
      if (layer.png) {
        assert.equal(layer.path, undefined, `Frame ${frame.index}/${name} has both png and path`);
        continue;
      }
      assert.equal(typeof layer.path, 'string', `Layer ${name} has no file path in frame ${frame.index}`);
      layer.png = layer.path;
      delete layer.path;
      renamed++;
      layersTouched.push(`${frame.index}/${name}`);
    }
  }
  assert.ok(renamed > 0, `Nothing to normalize: ${clipPath}`);
  fs.writeFileSync(absolute(clipPath), `${JSON.stringify(before, null, 2)}\n`);

  const after = readJSON(absolute(clipPath));
  assert.equal(after.frames.length, before.frames.length);
  for (const [index, frame] of after.frames.entries()) {
    const original = before.frames[index];
    assert.equal(frame.sha256, original.sha256, `Frame composite hash changed: ${index}`);
    assert.equal(frame.nativeSha256, original.nativeSha256, `Frame native hash changed: ${index}`);
    assert.equal(frame.durationMs, original.durationMs, `Duration changed: ${index}`);
    assert.equal(frame.weaponVisible, original.weaponVisible, `Visibility changed: ${index}`);
    for (const [name, layer] of Object.entries(frame.layers)) {
      assert.equal(layer.png, original.layers[name].path ?? original.layers[name].png, `Layer path changed: ${index}/${name}`);
      assert.equal(layer.sha256, original.layers[name].sha256, `Layer hash changed: ${index}/${name}`);
      assert.equal(layer.sha256, digest(layer.png), `Layer file no longer matches its hash: ${index}/${name}`);
    }
  }
  collected.push({
    clip: clipPath,
    clipSha256Before: beforeSha,
    clipSha256After: digest(clipPath),
    layersRenamed: renamed,
    frames: after.frames.length,
    pixelDataChanged: false,
    note: 'Only the layer file key was renamed from `path` to the canonical `png`. Every frame, native frame, timing and layer hash was verified identical, and each layer file still matches its declared hash.',
  });
}

const report = {
  schemaVersion: 1,
  normalizer: 'experiments/main-orc-combat-rescue-v5/normalize-layer-keys.mjs',
  reason: 'The two newest rear cycles emitted layer entries with the non-canonical key `path`; all six earlier clips and validate.mjs use `png`.',
  clips: collected,
};
fs.mkdirSync(path.dirname(absolute(values.output)), { recursive: true });
fs.writeFileSync(absolute(values.output), JSON.stringify(report, null, 2));
console.log(JSON.stringify(report, null, 2));
