import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import test from 'node:test';
import { ROOT, hash, readJSON } from '../src/core.mjs';

const original = readJSON(path.join(ROOT,
  'characters/orc-v1/source/combat-rescue-v5/combat/patch-manifest.json'));
const script = path.join(ROOT, 'experiments/main-orc-combat-rescue-v5/integrate.mjs');
const weaponPatch = () => ({
  ...original,
  cells: original.cells.filter(cell => ['Sword', 'Axe'].includes(cell.action)),
});

function runPatch(patch, check, prepare) {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'orc-v5-integration-'));
  try {
    const patchPath = path.join(directory, 'patch.json');
    const output = path.join(directory, 'candidate.json');
    if (prepare) prepare(patch, directory);
    fs.writeFileSync(patchPath, JSON.stringify(patch));
    const result = spawnSync(process.execPath,
      [script, '--weapon-patch', patchPath, '--output', output],
      { cwd: ROOT, encoding: 'utf8' });
    check(result, output);
  } finally {
    fs.rmSync(directory, { recursive: true, force: true });
  }
}

test('full replacement selects eight weapon clips, four Unarmed and one Walk without promotion', () => {
  runPatch(weaponPatch(), (result, output) => {
    assert.equal(result.status, 0, result.stderr);
    const manifest = readJSON(output);
    assert.equal(manifest.totalClips, 28);
    assert.equal(manifest.activeCandidatesCount, 13);
    assert.equal(manifest.unchangedAliasesCount, 15);
    assert.equal(manifest.totalFrames, 210);
    assert.equal(manifest.creatorApproval, 'PENDING_CREATOR');
    assert.equal(manifest.eligibleForIntegration, false);
    assert.equal(manifest.artisticStatus, 'VISUAL_REVIEW_REQUIRED');
    for (const cell of manifest.cells.filter(cell => ['Sword', 'Axe'].includes(cell.action))) {
      assert.equal(cell.clipJson, original.cells.find(item =>
        item.direction === cell.direction && item.action === cell.action).clipJson);
      assert.equal(cell.patchManifest, path.join(path.dirname(output), 'patch.json'));
    }
  });
});

test('partial keyframe patch cannot replace the eight full weapon clips', () => {
  const patch = weaponPatch();
  patch.cells.pop();
  runPatch(patch, (result, output) => {
    assert.notEqual(result.status, 0);
    assert.match(result.stderr, /all eight full clips/);
    assert.equal(fs.existsSync(output), false);
  });
});

test('duplicate replacement and stale clip hashes fail before writing candidate', () => {
  const duplicate = weaponPatch();
  duplicate.cells[1] = duplicate.cells[0];
  runPatch(duplicate, (result, output) => {
    assert.notEqual(result.status, 0);
    assert.match(result.stderr, /Unknown\/duplicate weapon replacement/);
    assert.equal(fs.existsSync(output), false);
  });
  const stale = weaponPatch();
  stale.cells[0] = { ...stale.cells[0], clipSha256: hash('not the delivered clip') };
  runPatch(stale, (result, output) => {
    assert.notEqual(result.status, 0);
    assert.match(result.stderr, /Patch clip hash/);
    assert.equal(fs.existsSync(output), false);
  });
});

test('three body-only keys cannot masquerade as a complete weapon clip', () => {
  runPatch(weaponPatch(), (result, output) => {
    assert.notEqual(result.status, 0);
    assert.match(result.stderr, /Body-only keys are not an equipped weapon clip/);
    assert.equal(fs.existsSync(output), false);
  }, (patch, directory) => {
    const clip = readJSON(path.resolve(ROOT, patch.cells[0].clipJson));
    clip.frames = clip.frames.slice(0, 3).map(frame => ({ ...frame, weaponVisible: false }));
    const clipJson = path.join(directory, 'keys.json');
    const bytes = JSON.stringify(clip);
    fs.writeFileSync(clipJson, bytes);
    patch.cells[0] = { ...patch.cells[0], clipJson, clipSha256: hash(bytes) };
  });
});
