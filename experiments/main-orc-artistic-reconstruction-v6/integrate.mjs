import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { parseArgs } from 'node:util';
import { ROOT, hash, readJSON } from '../../src/core.mjs';

// V6 integrator: parent is the creator-rejected V5 candidate. Only the eight
// Sword/Axe cells may be replaced; Unarmed/Walk cells delivered by V5 carry
// their V5 status forward untouched (they are out of V6 scope by contract).

const { values } = parseArgs({ options: {
  'weapon-patch': { type: 'string', required: true },
  output: { type: 'string', default: 'characters/orc-v1/source/artistic-reconstruction-v6/candidate28manifest.json' },
} });
const parentPath = 'characters/orc-v1/source/combat-rescue-v5/candidate28manifest.json';
const outputPath = values.output;
const absolute = file => path.resolve(ROOT, file);
const digest = file => hash(fs.readFileSync(absolute(file)));
const key = cell => `${cell.direction}/${cell.action}`;

const parent = readJSON(absolute(parentPath));
const patch = readJSON(absolute(values['weapon-patch']));
assert.equal(patch.parentManifestSha256, digest(parentPath), 'Weapon patch parent hash must match the V5 candidate');
assert.ok(patch.weapons?.Sword && patch.weapons?.Axe, 'Patch must declare independent weapons');

const expected = new Set(['front_r', 'front_l', 'back_r', 'back_l']
  .flatMap(direction => ['Sword', 'Axe'].map(action => `${direction}/${action}`)));
assert.equal(patch.cells.length, expected.size, 'Weapon replacement must contain all eight full clips');
for (const cell of patch.cells) assert.ok(expected.delete(key(cell)), `Unknown/duplicate weapon cell: ${key(cell)}`);
assert.equal(expected.size, 0, 'Incomplete weapon replacement');

const changes = new Map();
for (const cell of patch.cells) {
  const id = key(cell);
  assert.equal(cell.clipSha256, digest(cell.clipJson), `Patch clip hash: ${id}`);
  const clip = readJSON(absolute(cell.clipJson));
  assert.ok(clip.frames.length > 1, `Representative is not a full weapon clip: ${id}`);
  assert.equal(clip.category, cell.action, `Weapon family mismatch: ${id}`);
  assert.equal(clip.direction, cell.direction, `Direction mismatch: ${id}`);
  assert.ok(clip.frames.some(frame => frame.weaponVisible === true), `No armed frame: ${id}`);
  assert.equal(clip.frames[0].weaponVisible, false, `Armed before attack: ${id}`);
  assert.equal(clip.frames.at(-1).weaponVisible, false, `Armed after attack: ${id}`);
  for (const frame of clip.frames) {
    for (const layer of ['weaponBack', 'body', 'weaponFront', 'handFront']) {
      assert.equal(typeof frame.layers?.[layer]?.png, 'string', `Missing ${layer} layer: ${id}/${frame.index}`);
    }
  }
  for (const [fileField, hashField] of [['master', 'masterSha256'], ['nativeMaster', 'nativeMasterSha256']]) {
    assert.ok(clip[fileField], `Missing ${fileField}: ${id}`);
    assert.equal(clip[hashField], digest(clip[fileField]), `Stale ${hashField}: ${id}`);
  }
  changes.set(id, cell);
}

const cells = parent.cells.map(parentCell => {
  const id = key(parentCell);
  const change = changes.get(id);
  const clipJson = change ? change.clipJson : parentCell.clipJson;
  const clip = readJSON(absolute(clipJson));
  const wasActive = parentCell.status === 'ACTIVE_CANDIDATE';
  const cell = {
    direction: parentCell.direction,
    action: parentCell.action,
    cellId: id,
    status: change ? 'ACTIVE_CANDIDATE' : parentCell.status,
    isAffected: change ? true : parentCell.isAffected,
    clipJson,
    clipSha256: digest(clipJson),
    reviewStatus: change ? 'VISUAL_REVIEW_REQUIRED'
      : (parentCell.reviewStatus ?? 'UNCHANGED_RELATIVE_TO_V5_INPUT'),
    provenance: change ? change.provenance : parentCell.provenance,
    notes: change ? change.notes
      : `${parentCell.notes ?? ''} [V6] Out of V6 scope; carried over from the V5 candidate without artwork change.`,
    frameCount: clip.frames.length,
    durationsMs: clip.frames.map(frame => frame.durationMs),
    parentCell: { manifest: parentPath, cellId: id, clipJson: parentCell.clipJson, clipSha256: digest(parentCell.clipJson) },
  };
  if (change) cell.patchManifest = values['weapon-patch'];
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
  manifestId: 'orc-v1.artistic-reconstruction-v6.candidate28',
  characterId: 'orc-v1',
  characterName: 'Verde Warcraft',
  revision: 'main-orc-artistic-reconstruction-v6',
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
  weaponDefinitions: patch.weapons,
  integrationReport: 'experiments/main-orc-artistic-reconstruction-v6/orchestration-report.md',
  technicalStatus: 'NOT_VERIFIED',
  artisticStatus: 'VISUAL_REVIEW_REQUIRED',
  creatorApproval: 'PENDING_CREATOR',
  creatorRejectedPreviousCandidate: 'combat-rescue-v5 (58152a101e16cbc031349b3308649f9ccaa38b99782d4e23bcf2ee43fddc3794)',
  eligibleForIntegration: false,
  integrationStatus: 'ISOLATED_CANDIDATE_NO_UNITY_AUTHORIZATION',
  runtimeImplemented: false,
  scope: 'Artistic reconstruction of the eight Sword/Axe attack cells (rear priority) rejected by the creator in V5; Unarmed/Walk/Idle/Hit/Defeat carried over untouched.',
};
fs.mkdirSync(path.dirname(absolute(outputPath)), { recursive: true });
fs.writeFileSync(absolute(outputPath), JSON.stringify(manifest, null, 2));
console.log(JSON.stringify({ outputPath, activeCandidatesCount: affected.length, unchangedAliasesCount: aliases.length, totalFrames: manifest.totalFrames }));
