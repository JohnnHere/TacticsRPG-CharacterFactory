import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { parseArgs } from 'node:util';
import { ROOT, hash, readJSON } from '../../src/core.mjs';

const { values } = parseArgs({ options: {
  config: { type: 'string', default: 'experiments/main-orc-combat-rescue-v5/final-weapon-clips.json' },
  output: { type: 'string', required: true },
  probe: { type: 'boolean', default: false },
} });
const absolute = file => path.resolve(ROOT, file);
const digest = file => hash(fs.readFileSync(absolute(file)));
const readText = file => fs.readFileSync(absolute(file), 'utf8');

const config = readJSON(absolute(values.config));
const parentPath = config.parentManifest;
const parentSha = digest(parentPath);
assert.equal(config.parentManifestSha256, parentSha, 'Configured parent hash is stale');

const EXPECTED = new Set(['front_r', 'front_l', 'back_r', 'back_l']
  .flatMap(direction => ['Sword', 'Axe'].map(action => `${direction}/${action}`)));
const probe = values.probe;
if (!probe) assert.equal(config.clips.length, EXPECTED.size, `Need all eight weapon clips, got ${config.clips.length}`);

const cells = [];
const seen = new Set();
const pending = [];
for (const entry of config.clips) {
  if (probe && !fs.existsSync(absolute(entry.clipJson))) {
    pending.push(entry.clipJson);
    continue;
  }

  const id = `${entry.direction}/${entry.action}`;
  assert.ok(EXPECTED.has(id), `Unexpected cell ${id}`);
  assert.ok(!seen.has(id), `Duplicate cell ${id}`);
  seen.add(id);

  const clip = readJSON(absolute(entry.clipJson));
  const clipSha = digest(entry.clipJson);
  assert.equal(clip.direction, entry.direction, `Clip direction mismatch: ${id}`);
  assert.equal(clip.category, entry.action, `Clip weapon family mismatch: ${id}`);
  assert.ok(Array.isArray(clip.frames) && clip.frames.length > 1, `Not a full cycle: ${id}`);
  assert.deepEqual(clip.canvas, [256, 256], `Canvas contract: ${id}`);
  assert.equal(clip.groundY, 190, `Ground contract: ${id}`);
  assert.deepEqual(clip.nativeCanvas, [128, 128], `Native canvas contract: ${id}`);
  assert.equal(clip.nativeGroundY, 126, `Native ground contract: ${id}`);
  const visible = clip.frames.filter(frame => frame.weaponVisible === true);
  assert.ok(visible.length > 0, `No armed frame: ${id}`);
  assert.equal(clip.frames[0].weaponVisible, false, `Armed before the action: ${id}`);
  assert.equal(clip.frames.at(-1).weaponVisible, false, `Armed after the action: ${id}`);
  for (const frame of clip.frames) {
    for (const layer of ['weaponBack', 'body', 'weaponFront', 'handFront']) {
      assert.ok(frame.layers?.[layer]?.png, `Missing ${layer} layer: ${id}/${frame.index}`);
      assert.ok(fs.existsSync(absolute(frame.layers[layer].png)), `Missing ${layer} file: ${id}/${frame.index}`);
      if (frame.layers[layer].sha256) {
        assert.equal(frame.layers[layer].sha256, digest(frame.layers[layer].png),
          `Stale ${layer} hash: ${id}/${frame.index}`);
      }
    }
  }
  for (const [fileField, hashField] of [['master', 'masterSha256'], ['nativeMaster', 'nativeMasterSha256']]) {
    assert.ok(clip[fileField], `Missing ${fileField}: ${id}`);
    assert.equal(clip[hashField], digest(clip[fileField]), `Stale ${hashField}: ${id}`);
  }
  const definition = entry.weaponDefinition;
  assert.ok(fs.existsSync(absolute(definition)), `Missing weapon definition: ${definition}`);

  const qaText = entry.qaEvidence.map(readText).join('\n').toLowerCase();
  assert.ok(qaText.includes(clipSha.toLowerCase()),
    `Independent QA evidence does not reference this exact clip hash: ${id}`);
  const accepted = entry.acceptedVerdicts.some(verdict => qaText.includes(verdict.toLowerCase()));
  assert.ok(accepted, `Independent QA has not accepted this clip: ${id}`);

  cells.push({
    direction: entry.direction,
    action: entry.action,
    cellId: id,
    clipJson: entry.clipJson,
    clipSha256: clipSha,
    provenance: entry.provenance,
    notes: entry.notes,
    qaEvidence: entry.qaEvidence,
    qaVerdict: entry.acceptedVerdicts.find(verdict => qaText.includes(verdict.toLowerCase())),
  });
}

if (!probe) assert.equal(cells.length, EXPECTED.size);
const patch = {  schemaVersion: 1,
  patchId: 'orc-v1.combat-rescue-v5.final-weapon-clips',
  characterId: 'orc-v1',
  characterName: 'Verde Warcraft',
  revision: 'main-orc-combat-rescue-v5',
  parentManifest: parentPath,
  parentManifestSha256: parentSha,
  scope: 'Eight final equipped Sword/Axe attack cycles: four preserved front bodies with new anatomical grips and four reconstructed rear bodies with independent weapons.',
  technicalStatus: 'TECHNICALLY_COMPLETE',
  artisticStatus: 'VISUAL_REVIEW_REQUIRED',
  artisticApproval: 'PENDING_CREATOR',
  eligibleForIntegration: false,
  weapons: config.weapons,
  cells,
};
fs.mkdirSync(path.dirname(absolute(values.output)), { recursive: true });
fs.writeFileSync(absolute(values.output), JSON.stringify(patch, null, 2));
console.log(JSON.stringify({ output: values.output, cells: cells.length, parentSha, probe, pending }));

