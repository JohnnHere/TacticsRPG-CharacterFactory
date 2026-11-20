import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { parseArgs } from 'node:util';
import { ROOT, hash, readJSON } from '../../src/core.mjs';

const { values } = parseArgs({ options: {
  'weapon-patch': { type: 'string' },
  output: { type: 'string', default: 'characters/orc-v1/source/combat-rescue-v5/candidate28manifest.json' },
} });
const parentPath = 'characters/orc-v1/source/rear-reconstruction-v4/candidate28manifest.json';
const outputPath = values.output;
const patchPaths = [
  ['characters/orc-v1/source/combat-rescue-v5/combat/patch-manifest.json', 'cells'],
  ['characters/orc-v1/source/combat-rescue-v5/localized/patch-manifest.json', 'changedClips'],
];
if (values['weapon-patch']) patchPaths.push([values['weapon-patch'], 'cells']);
const absolute = file => path.resolve(ROOT, file);
const digest = file => hash(fs.readFileSync(absolute(file)));
const parent = readJSON(absolute(parentPath));
const key = cell => `${cell.direction}/${cell.action}`;
const parentCells = new Map(parent.cells.map(cell => [key(cell), cell]));
const changes = new Map();
let weaponDefinitions;
for (const [patchPath, entriesField] of patchPaths) {
  const patch = readJSON(absolute(patchPath));
  assert.equal(patch.parentManifestSha256, digest(parentPath), `Patch parent hash: ${patchPath}`);
  assert.ok(Array.isArray(patch[entriesField]), `Missing ${entriesField}: ${patchPath}`);
  if (entriesField === 'cells') weaponDefinitions = patch.weapons;
  const replacement = patchPath === values['weapon-patch'];
  if (replacement) {
    const expected = new Set(['front_r', 'front_l', 'back_r', 'back_l']
      .flatMap(direction => ['Sword', 'Axe'].map(action => `${direction}/${action}`)));
    assert.equal(patch.cells.length, expected.size, 'Weapon replacement must contain all eight full clips');
    for (const cell of patch.cells) {
      assert.ok(expected.delete(key(cell)), `Unknown/duplicate weapon replacement: ${key(cell)}`);
    }
    assert.equal(expected.size, 0, 'Incomplete weapon replacement');
  }
  for (const cell of patch[entriesField]) {
    if (values['weapon-patch'] && !replacement && entriesField === 'cells' &&
      ['Sword', 'Axe'].includes(cell.action)) continue;
    const id = key(cell);
    assert.ok(parentCells.has(id) && !changes.has(id), `Unknown/duplicate patch cell: ${id}`);
    assert.ok(!['Idle', 'Hit'].includes(cell.action) &&
      !(cell.action === 'Defeat' && cell.direction.startsWith('back_')), `Protected clip patched: ${id}`);
    assert.notEqual(cell.clipJson, parentCells.get(id).clipJson, `Changed clip aliases parent: ${id}`);
    if (replacement || cell.clipSha256) {
      assert.equal(cell.clipSha256, digest(cell.clipJson), `Patch clip hash: ${id}`);
    }
    if (replacement) {
      const clip = readJSON(absolute(cell.clipJson));
      assert.ok(clip.frames.length > 1, `Representative is not a full weapon clip: ${id}`);
      assert.ok(clip.frames.some(frame => frame.weaponVisible === true),
        `Body-only keys are not an equipped weapon clip: ${id}`);
      assert.equal(clip.frames[0].weaponVisible, false, `Weapon visible before attack: ${id}`);
      assert.equal(clip.frames.at(-1).weaponVisible, false, `Weapon visible after attack: ${id}`);
      for (const frame of clip.frames) {
        for (const layer of ['weaponBack', 'body', 'weaponFront', 'handFront']) {
          assert.equal(typeof frame.layers?.[layer]?.png, 'string', `Missing ${layer} layer: ${id}`);
        }
      }
    }
    changes.set(id, { cell, patchPath });
  }
}
assert.ok(changes.size > 0, 'No delivered production patches');
assert.ok(weaponDefinitions?.Sword && weaponDefinitions?.Axe, 'Missing delivered independent weapons');
const cells = parent.cells.map(parentCell => {
  const id = key(parentCell);
  const change = changes.get(id);
  const clipJson = change ? change.cell.clipJson : parentCell.clipJson;
  const clip = readJSON(absolute(clipJson));
  const cell = {
    direction: parentCell.direction,
    action: parentCell.action,
    cellId: id,
    status: change ? 'ACTIVE_CANDIDATE' : 'UNCHANGED_ALIAS',
    isAffected: !!change,
    clipJson,
    clipSha256: digest(clipJson),
    reviewStatus: change ? 'VISUAL_REVIEW_REQUIRED' : 'UNCHANGED_RELATIVE_TO_V5_INPUT',
    provenance: change ? change.cell.provenance : 'Exact alias to immediate V5 input; no artwork or timing change.',
    notes: change ? change.cell.notes : 'Preserved source/export; no inherited artistic approval.',
    frameCount: clip.frames.length,
    durationsMs: clip.frames.map(frame => frame.durationMs),
    parentCell: { manifest: parentPath, cellId: id, clipJson: parentCell.clipJson, clipSha256: digest(parentCell.clipJson) },
  };
  if (change) cell.patchManifest = change.patchPath;
  for (const [fileField, hashField] of [
    ['master', 'masterSha256'], ['bodyMaster', 'bodyMasterSha256'],
    ['nativeMaster', 'nativeMasterSha256'], ['strip', 'stripSha256'],
    ['nativeStrip', 'nativeStripSha256'],
  ]) {
    if (clip[fileField]) cell[hashField] = digest(clip[fileField]);
  }
  return cell;
});
const affected = cells.filter(cell => cell.isAffected);
const aliases = cells.filter(cell => !cell.isAffected);
const manifest = {
  schemaVersion: 1,
  manifestId: 'orc-v1.combat-rescue-v5.candidate28',
  characterId: 'orc-v1',
  characterName: 'Verde Warcraft',
  revision: 'main-orc-combat-rescue-v5',
  baselineBuild: parent.baselineBuild,
  parentManifest: parentPath,
  parentManifestSha256: digest(parentPath),
  comparisonBaselineManifest: parentPath,
  totalClips: 28,
  activeCandidatesCount: affected.length,
  inRevisionCount: 0,
  inProductionCount: 0,
  unchangedAliasesCount: aliases.length,
  totalFrames: cells.reduce((sum, cell) => sum + cell.frameCount, 0),
  affectedFrameCount: affected.reduce((sum, cell) => sum + cell.frameCount, 0),
  aliasFrameCount: aliases.reduce((sum, cell) => sum + cell.frameCount, 0),
  cells,
  weaponDefinitions,
  integrationReport: 'experiments/main-orc-combat-rescue-v5/orchestration-report.md',
  devReport: 'experiments/main-orc-combat-rescue-v5/combat/report.md',
  technicalStatus: 'NOT_VERIFIED',
  artisticStatus: 'VISUAL_REVIEW_REQUIRED',
  creatorApproval: 'PENDING_CREATOR',
  eligibleForIntegration: false,
  integrationStatus: 'ISOLATED_CANDIDATE_NO_UNITY_AUTHORIZATION',
  runtimeImplemented: false,
  scope: 'Whole-body rear Sword/Axe/Unarmed reconstruction; anatomical grips, affected front Unarmed and localized Walk/Defeat inspection. Protected Idle/Hit/rear Defeat remain exact aliases.',
};
fs.mkdirSync(path.dirname(absolute(outputPath)), { recursive: true });
fs.writeFileSync(absolute(outputPath), JSON.stringify(manifest, null, 2));
console.log(JSON.stringify({ outputPath, activeCandidatesCount: affected.length, unchangedAliasesCount: aliases.length, totalFrames: manifest.totalFrames }));
