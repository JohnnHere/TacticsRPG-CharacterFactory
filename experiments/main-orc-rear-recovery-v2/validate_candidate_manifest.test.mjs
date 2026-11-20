import test from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { ROOT } from '../../src/core.mjs';

const VALIDATOR_PATH = path.join(ROOT, 'experiments/main-orc-rear-recovery-v2/validate_candidate_manifest.mjs');
const CANONICAL_MANIFEST_REL = 'characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json';
const CANONICAL_MANIFEST_FULL = path.join(ROOT, CANONICAL_MANIFEST_REL);
const REPORT_REL = 'experiments/main-orc-rear-recovery-v2/manifest-validation-report.json';
const REPORT_FULL = path.join(ROOT, REPORT_REL);

test('Candidate 28 Manifest Validator Contract Suite', async (t) => {
  await t.test('validator exists and is executable via node', () => {
    assert.ok(fs.existsSync(VALIDATOR_PATH), 'Validator file must exist at E/validate_candidate_manifest.mjs');
  });

  await t.test('canonical manifest: dynamic validation with --allow-incomplete matches manifest header and exits 0', () => {
    assert.ok(fs.existsSync(CANONICAL_MANIFEST_FULL), 'Canonical manifest must exist');
    const canonicalManifest = JSON.parse(fs.readFileSync(CANONICAL_MANIFEST_FULL, 'utf8'));

    const res = spawnSync('node', [VALIDATOR_PATH, '--allow-incomplete'], {
      cwd: ROOT,
      encoding: 'utf8'
    });
    assert.equal(res.status, 0, `Expected exit 0 with --allow-incomplete, got ${res.status}. Output:\n${res.stdout}\n${res.stderr}`);
    assert.ok(res.stdout.includes('Validation PASSED with 0 errors'), 'Stdout should report pass');
    assert.ok(fs.existsSync(REPORT_FULL), 'Validation report artifact must be emitted');

    const report = JSON.parse(fs.readFileSync(REPORT_FULL, 'utf8'));
    assert.equal(report.manifestId, canonicalManifest.manifestId);
    assert.equal(report.mode, 'INCOMPLETE_ALLOWED');
    assert.equal(report.summary.totalClips, 28);
    assert.ok(report.summary.affectedCount === 12 || report.summary.affectedCount === 15);
    assert.equal(report.summary.unchangedAliasesCount, canonicalManifest.unchangedAliasesCount);
    // Dynamic assertion derived from manifest:
    assert.equal(report.summary.activeCandidatesCount, canonicalManifest.activeCandidatesCount);
    assert.equal(report.summary.inRevisionCount, canonicalManifest.inRevisionCount);
    assert.equal(report.governance.artisticApproval, 'PENDING_CREATOR');
    assert.equal(report.governance.runtimeImplemented, false);
  });

  await t.test('canonical manifest: default FINAL mode dynamically verifies completion (exits 0 if inRevisionCount === 0, else 1)', () => {
    const canonicalManifest = JSON.parse(fs.readFileSync(CANONICAL_MANIFEST_FULL, 'utf8'));
    const expectedExit = canonicalManifest.inRevisionCount === 0 ? 0 : 1;
    const tmpFinalReportRel = 'experiments/main-orc-rear-recovery-v2/.tmp-test-final-report.json';
    const tmpFinalReportFull = path.join(ROOT, tmpFinalReportRel);

    try {
      const res = spawnSync('node', [VALIDATOR_PATH, '--output', tmpFinalReportRel], {
        cwd: ROOT,
        encoding: 'utf8'
      });
      assert.equal(res.status, expectedExit, `Expected exit ${expectedExit} in FINAL mode, got ${res.status}`);
      if (expectedExit === 1) {
        assert.ok(
          res.stdout.includes('FINAL delivery mode requires 0 ARTISTIC_REVISION_REQUIRED cells') ||
          res.stderr.includes('FINAL delivery mode requires 0 ARTISTIC_REVISION_REQUIRED cells'),
          'Stdout/stderr should report failure for in-revision cells when inRevisionCount > 0'
        );
      } else {
        assert.ok(res.stdout.includes('Validation PASSED with 0 errors'), 'Should pass FINAL mode when inRevisionCount === 0');
      }
    } finally {
      if (fs.existsSync(tmpFinalReportFull)) {
        fs.unlinkSync(tmpFinalReportFull);
      }
    }
  });

  await t.test('negative fixture: corrupted frame SHA-256 triggers hard integrity error even with --allow-incomplete', () => {
    const tmpDir = path.join(ROOT, 'experiments/main-orc-rear-recovery-v2/.tmp-test-corrupted-sha');
    const tmpManifestRel = 'experiments/main-orc-rear-recovery-v2/.tmp-test-corrupted-sha/manifest.json';
    const tmpClipRel = 'experiments/main-orc-rear-recovery-v2/.tmp-test-corrupted-sha/clip.json';
    const tmpOutputRel = 'experiments/main-orc-rear-recovery-v2/.tmp-test-corrupted-sha/report.json';

    try {
      fs.mkdirSync(tmpDir, { recursive: true });

      const manifest = JSON.parse(fs.readFileSync(CANONICAL_MANIFEST_FULL, 'utf8'));
      const baseClipPath = path.join(ROOT, 'characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2/clip.json');
      const clip = JSON.parse(fs.readFileSync(baseClipPath, 'utf8'));

      // Deliberately corrupt frame 0 sha256
      clip.frames[0].sha256 = '0000000000000000000000000000000000000000000000000000000000000000';
      fs.writeFileSync(path.join(ROOT, tmpClipRel), JSON.stringify(clip, null, 2), 'utf8');

      const swordCell = manifest.cells.find(c => c.cellId === 'back_r/Sword');
      swordCell.clipJson = tmpClipRel;
      fs.writeFileSync(path.join(ROOT, tmpManifestRel), JSON.stringify(manifest, null, 2), 'utf8');

      const res = spawnSync('node', [
        VALIDATOR_PATH,
        '--manifest', tmpManifestRel,
        '--output', tmpOutputRel,
        '--allow-incomplete'
      ], {
        cwd: ROOT,
        encoding: 'utf8'
      });

      assert.equal(res.status, 1, `Corrupted frame SHA-256 must fail validator even with --allow-incomplete (got exit ${res.status})`);
      const combinedOutput = `${res.stdout}\n${res.stderr}`;
      assert.ok(combinedOutput.includes('SHA-256 mismatch') || combinedOutput.includes('Validation FAILED'),
        'Output must report SHA-256 mismatch / validation failure');
    } finally {
      if (fs.existsSync(tmpDir)) {
        fs.rmSync(tmpDir, { recursive: true, force: true });
      }
    }
  });

  await t.test('negative fixture: missing frame PNG triggers hard integrity error even with --allow-incomplete', () => {
    const tmpDir = path.join(ROOT, 'experiments/main-orc-rear-recovery-v2/.tmp-test-missing-png');
    const tmpManifestRel = 'experiments/main-orc-rear-recovery-v2/.tmp-test-missing-png/manifest.json';
    const tmpClipRel = 'experiments/main-orc-rear-recovery-v2/.tmp-test-missing-png/clip.json';
    const tmpOutputRel = 'experiments/main-orc-rear-recovery-v2/.tmp-test-missing-png/report.json';

    try {
      fs.mkdirSync(tmpDir, { recursive: true });

      const manifest = JSON.parse(fs.readFileSync(CANONICAL_MANIFEST_FULL, 'utf8'));
      const baseClipPath = path.join(ROOT, 'characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2/clip.json');
      const clip = JSON.parse(fs.readFileSync(baseClipPath, 'utf8'));

      // Mutate frame 0 PNG path to non-existent file
      clip.frames[0].png = 'characters/orc-v1/source/rear-recovery-v2/back_r/Sword/nonexistent-frame-999.png';
      fs.writeFileSync(path.join(ROOT, tmpClipRel), JSON.stringify(clip, null, 2), 'utf8');

      const swordCell = manifest.cells.find(c => c.cellId === 'back_r/Sword');
      swordCell.clipJson = tmpClipRel;
      fs.writeFileSync(path.join(ROOT, tmpManifestRel), JSON.stringify(manifest, null, 2), 'utf8');

      const res = spawnSync('node', [
        VALIDATOR_PATH,
        '--manifest', tmpManifestRel,
        '--output', tmpOutputRel,
        '--allow-incomplete'
      ], {
        cwd: ROOT,
        encoding: 'utf8'
      });

      assert.equal(res.status, 1, `Missing frame PNG must fail validator even with --allow-incomplete (got exit ${res.status})`);
      const combinedOutput = `${res.stdout}\n${res.stderr}`;
      assert.ok(combinedOutput.includes('Missing frame composite PNG') || combinedOutput.includes('Validation FAILED'),
        'Output must report missing frame PNG');
    } finally {
      if (fs.existsSync(tmpDir)) {
        fs.rmSync(tmpDir, { recursive: true, force: true });
      }
    }
  });

  await t.test('negative fixture: corrupted 4-layer SHA-256 in armed clip triggers hard integrity error even with --allow-incomplete', () => {
    const tmpDir = path.join(ROOT, 'experiments/main-orc-rear-recovery-v2/.tmp-test-corrupted-layer');
    const tmpManifestRel = 'experiments/main-orc-rear-recovery-v2/.tmp-test-corrupted-layer/manifest.json';
    const tmpClipRel = 'experiments/main-orc-rear-recovery-v2/.tmp-test-corrupted-layer/clip.json';
    const tmpOutputRel = 'experiments/main-orc-rear-recovery-v2/.tmp-test-corrupted-layer/report.json';

    try {
      fs.mkdirSync(tmpDir, { recursive: true });

      const manifest = JSON.parse(fs.readFileSync(CANONICAL_MANIFEST_FULL, 'utf8'));
      const baseClipPath = path.join(ROOT, 'characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2/clip.json');
      const clip = JSON.parse(fs.readFileSync(baseClipPath, 'utf8'));

      // Corrupt body layer sha256 in frame 0
      clip.frames[0].layers.body.sha256 = 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff';
      fs.writeFileSync(path.join(ROOT, tmpClipRel), JSON.stringify(clip, null, 2), 'utf8');

      const swordCell = manifest.cells.find(c => c.cellId === 'back_r/Sword');
      swordCell.clipJson = tmpClipRel;
      fs.writeFileSync(path.join(ROOT, tmpManifestRel), JSON.stringify(manifest, null, 2), 'utf8');

      const res = spawnSync('node', [
        VALIDATOR_PATH,
        '--manifest', tmpManifestRel,
        '--output', tmpOutputRel,
        '--allow-incomplete'
      ], {
        cwd: ROOT,
        encoding: 'utf8'
      });

      assert.equal(res.status, 1, `Corrupted layer SHA-256 must fail validator even with --allow-incomplete (got exit ${res.status})`);
      const combinedOutput = `${res.stdout}\n${res.stderr}`;
      assert.ok(combinedOutput.includes('SHA-256 mismatch') || combinedOutput.includes('Validation FAILED'),
        'Output must report layer SHA mismatch');
    } finally {
      if (fs.existsSync(tmpDir)) {
        fs.rmSync(tmpDir, { recursive: true, force: true });
      }
    }
  });

  await t.test('negative fixture: missing composite master triggers hard failure even with --allow-incomplete', () => {
    const tmpDir = path.join(ROOT, 'experiments/main-orc-rear-recovery-v2/.tmp-test-missing-master');
    const tmpManifestRel = 'experiments/main-orc-rear-recovery-v2/.tmp-test-missing-master/manifest.json';
    const tmpClipRel = 'experiments/main-orc-rear-recovery-v2/.tmp-test-missing-master/clip.json';
    const tmpOutputRel = 'experiments/main-orc-rear-recovery-v2/.tmp-test-missing-master/report.json';

    try {
      fs.mkdirSync(tmpDir, { recursive: true });

      const manifest = JSON.parse(fs.readFileSync(CANONICAL_MANIFEST_FULL, 'utf8'));
      const baseClipPath = path.join(ROOT, 'characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2/clip.json');
      const clip = JSON.parse(fs.readFileSync(baseClipPath, 'utf8'));

      // Deliberately delete master field
      delete clip.master;
      fs.writeFileSync(path.join(ROOT, tmpClipRel), JSON.stringify(clip, null, 2), 'utf8');

      const swordCell = manifest.cells.find(c => c.cellId === 'back_r/Sword');
      swordCell.clipJson = tmpClipRel;
      fs.writeFileSync(path.join(ROOT, tmpManifestRel), JSON.stringify(manifest, null, 2), 'utf8');

      const res = spawnSync('node', [
        VALIDATOR_PATH,
        '--manifest', tmpManifestRel,
        '--output', tmpOutputRel,
        '--allow-incomplete'
      ], {
        cwd: ROOT,
        encoding: 'utf8'
      });

      assert.equal(res.status, 1, `Missing master must fail validator even with --allow-incomplete (got exit ${res.status})`);
      const combinedOutput = `${res.stdout}\n${res.stderr}`;
      assert.ok(combinedOutput.includes('Composite 256 master path declared') || combinedOutput.includes('Validation FAILED'),
        'Output must report missing master path');
    } finally {
      if (fs.existsSync(tmpDir)) {
        fs.rmSync(tmpDir, { recursive: true, force: true });
      }
    }
  });

  await t.test('negative fixture: corrupted masterSha256 triggers hard failure even with --allow-incomplete', () => {
    const tmpDir = path.join(ROOT, 'experiments/main-orc-rear-recovery-v2/.tmp-test-corrupted-master-sha');
    const tmpManifestRel = 'experiments/main-orc-rear-recovery-v2/.tmp-test-corrupted-master-sha/manifest.json';
    const tmpClipRel = 'experiments/main-orc-rear-recovery-v2/.tmp-test-corrupted-master-sha/clip.json';
    const tmpOutputRel = 'experiments/main-orc-rear-recovery-v2/.tmp-test-corrupted-master-sha/report.json';

    try {
      fs.mkdirSync(tmpDir, { recursive: true });

      const manifest = JSON.parse(fs.readFileSync(CANONICAL_MANIFEST_FULL, 'utf8'));
      const baseClipPath = path.join(ROOT, 'characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2/clip.json');
      const clip = JSON.parse(fs.readFileSync(baseClipPath, 'utf8'));

      // Corrupt masterSha256
      clip.masterSha256 = '0000000000000000000000000000000000000000000000000000000000000000';
      fs.writeFileSync(path.join(ROOT, tmpClipRel), JSON.stringify(clip, null, 2), 'utf8');

      const swordCell = manifest.cells.find(c => c.cellId === 'back_r/Sword');
      swordCell.clipJson = tmpClipRel;
      fs.writeFileSync(path.join(ROOT, tmpManifestRel), JSON.stringify(manifest, null, 2), 'utf8');

      const res = spawnSync('node', [
        VALIDATOR_PATH,
        '--manifest', tmpManifestRel,
        '--output', tmpOutputRel,
        '--allow-incomplete'
      ], {
        cwd: ROOT,
        encoding: 'utf8'
      });

      assert.equal(res.status, 1, `Corrupted masterSha256 must fail validator even with --allow-incomplete (got exit ${res.status})`);
      const combinedOutput = `${res.stdout}\n${res.stderr}`;
      assert.ok(combinedOutput.includes('master SHA-256 matches declared digest') || combinedOutput.includes('Validation FAILED'),
        'Output must report master SHA-256 failure');
    } finally {
      if (fs.existsSync(tmpDir)) {
        fs.rmSync(tmpDir, { recursive: true, force: true });
      }
    }
  });

  await t.test('negative fixture: missing nativeMaster property triggers hard failure even with --allow-incomplete', () => {
    const tmpDir = path.join(ROOT, 'experiments/main-orc-rear-recovery-v2/.tmp-test-missing-native-master');
    const tmpManifestRel = 'experiments/main-orc-rear-recovery-v2/.tmp-test-missing-native-master/manifest.json';
    const tmpClipRel = 'experiments/main-orc-rear-recovery-v2/.tmp-test-missing-native-master/clip.json';
    const tmpOutputRel = 'experiments/main-orc-rear-recovery-v2/.tmp-test-missing-native-master/report.json';

    try {
      fs.mkdirSync(tmpDir, { recursive: true });

      const manifest = JSON.parse(fs.readFileSync(CANONICAL_MANIFEST_FULL, 'utf8'));
      const baseClipPath = path.join(ROOT, 'characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2/clip.json');
      const clip = JSON.parse(fs.readFileSync(baseClipPath, 'utf8'));

      // Deliberately delete nativeMaster field
      delete clip.nativeMaster;
      fs.writeFileSync(path.join(ROOT, tmpClipRel), JSON.stringify(clip, null, 2), 'utf8');

      const swordCell = manifest.cells.find(c => c.cellId === 'back_r/Sword');
      swordCell.clipJson = tmpClipRel;
      fs.writeFileSync(path.join(ROOT, tmpManifestRel), JSON.stringify(manifest, null, 2), 'utf8');

      const res = spawnSync('node', [
        VALIDATOR_PATH,
        '--manifest', tmpManifestRel,
        '--output', tmpOutputRel,
        '--allow-incomplete'
      ], {
        cwd: ROOT,
        encoding: 'utf8'
      });

      assert.equal(res.status, 1, `Missing nativeMaster must fail validator even with --allow-incomplete (got exit ${res.status})`);
      const combinedOutput = `${res.stdout}\n${res.stderr}`;
      assert.ok(combinedOutput.includes('Native 128 master path declared') || combinedOutput.includes('Validation FAILED'),
        'Output must report missing nativeMaster');
    } finally {
      if (fs.existsSync(tmpDir)) {
        fs.rmSync(tmpDir, { recursive: true, force: true });
      }
    }
  });

  await t.test('simulated 12/0 complete delivery fixture: passes default FINAL mode with exit 0 and complete=true', () => {
    const tmpDir = path.join(ROOT, 'experiments/main-orc-rear-recovery-v2/.tmp-test-complete-12-0');
    const tmpManifestRel = 'experiments/main-orc-rear-recovery-v2/.tmp-test-complete-12-0/manifest.json';
    const tmpOutputRel = 'experiments/main-orc-rear-recovery-v2/.tmp-test-complete-12-0/report.json';

    try {
      fs.mkdirSync(tmpDir, { recursive: true });

      const manifest = JSON.parse(fs.readFileSync(CANONICAL_MANIFEST_FULL, 'utf8'));

      // If inRevisionCount > 0, simulate resolution using valid representative clips
      for (const cell of manifest.cells) {
        if (cell.status === 'ARTISTIC_REVISION_REQUIRED') {
          cell.status = 'ACTIVE_CANDIDATE';
          cell.reviewStatus = 'PASS_FOR_INTERNAL_EXPANSION';
          delete cell.rejectedEvidence;

          if (cell.cellId === 'back_l/Sword') {
            cell.clipJson = 'characters/orc-v1/source/rear-recovery-v2/back_l/Sword/Attack-representative-v1/clip.json';
          } else if (cell.cellId === 'back_r/Axe') {
            cell.clipJson = 'characters/orc-v1/source/rear-recovery-v2/back_r/Axe/Attack-representative-v1/clip.json';
          } else if (cell.cellId === 'back_l/Axe') {
            cell.clipJson = 'characters/orc-v1/source/rear-recovery-v2/back_l/Axe/Attack-representative-v1/clip.json';
          }
        }
      }
      manifest.activeCandidatesCount = manifest.cells.filter(c => c.status === 'ACTIVE_CANDIDATE').length;
      manifest.inRevisionCount = 0;

      fs.writeFileSync(path.join(ROOT, tmpManifestRel), JSON.stringify(manifest, null, 2), 'utf8');

      // Run in default FINAL mode (no --allow-incomplete)
      const res = spawnSync('node', [
        VALIDATOR_PATH,
        '--manifest', tmpManifestRel,
        '--output', tmpOutputRel
      ], {
        cwd: ROOT,
        encoding: 'utf8'
      });

      assert.equal(res.status, 0, `Simulated 12/0 fixture must pass default FINAL mode with exit 0. Output:\n${res.stdout}\n${res.stderr}`);
      assert.ok(res.stdout.includes('Validation PASSED with 0 errors'));

      const report = JSON.parse(fs.readFileSync(path.join(ROOT, tmpOutputRel), 'utf8'));
      assert.equal(report.mode, 'FINAL');
      assert.ok(report.summary.activeCandidatesCount === 12 || report.summary.activeCandidatesCount === 15);
      assert.equal(report.summary.inRevisionCount, 0);
      assert.equal(report.summary.complete, true);
    } finally {
      if (fs.existsSync(tmpDir)) {
        fs.rmSync(tmpDir, { recursive: true, force: true });
      }
    }
  });

  await t.test('armed candidate (back_r/Sword) is verified for 4 layers, visibleInterval, and valid reviewStatus taxonomy', () => {
    const report = JSON.parse(fs.readFileSync(REPORT_FULL, 'utf8'));
    const swordCell = report.cells.find(c => c.cellId === 'back_r/Sword');
    assert.ok(swordCell, 'Report must contain back_r/Sword cell');
    assert.equal(swordCell.status, 'ACTIVE_CANDIDATE');
    
    // Taxonomical check: must be in recognized review statuses, not hardcoded to a single frozen string
    const validTaxonomy = [
      'ACTIVE_CANDIDATE',
      'PASS_FOR_INTERNAL_INTEGRATION',
      'PASS_FOR_INTERNAL_EXPANSION',
      'ROOT_PASSED_FOR_INTERNAL_EXPANSION',
      'VISUAL_REVIEW_REQUIRED',
      'TECHNICALLY_COMPLETE',
      'INTEGRATED_QA_PASSED',
      'QA_PASSED_PENDING_CREATOR',
      'CREATOR_APPROVED'
    ];
    assert.ok(validTaxonomy.includes(swordCell.reviewStatus), `reviewStatus ${swordCell.reviewStatus} must be in recognized taxonomy`);
    assert.equal(swordCell.isArmed, true);
    assert.equal(swordCell.frameCount, 8);
    assert.equal(swordCell.totalDurationMs, 730);
    assert.equal(swordCell.valid, true);
  });

  await t.test('all rear weapon representative schemas (Sword R/L, Axe R/L) are verified for 4-layer composition and visibleInterval', () => {
    const weaponClips = [
      'characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2/clip.json',
      'characters/orc-v1/source/rear-recovery-v2/back_l/Sword/Attack-representative-v1/clip.json',
      'characters/orc-v1/source/rear-recovery-v2/back_r/Axe/Attack-representative-v1/clip.json',
      'characters/orc-v1/source/rear-recovery-v2/back_l/Axe/Attack-representative-v1/clip.json'
    ];

    const expectedLayers = ['weaponBack', 'body', 'weaponFront', 'handFront'];

    for (const clipRel of weaponClips) {
      const clipPath = path.join(ROOT, clipRel);
      assert.ok(fs.existsSync(clipPath), `Weapon clip must exist: ${clipRel}`);
      const clip = JSON.parse(fs.readFileSync(clipPath, 'utf8'));

      assert.equal(clip.weaponVisible, true, `${clipRel}: weaponVisible must be true`);
      assert.deepEqual(clip.visibleInterval, [1, 6], `${clipRel}: visibleInterval must be [1, 6]`);
      assert.deepEqual(clip.layerOrder, expectedLayers, `${clipRel}: layerOrder must be exactly 4 layers`);
      assert.equal(clip.frameCount, 8, `${clipRel}: frameCount must be 8`);
      assert.equal(clip.totalDurationMs, 730, `${clipRel}: totalDurationMs must be 730`);
      assert.ok(clip.master && fs.existsSync(path.join(ROOT, clip.master)), `${clipRel}: composite master must exist`);
      assert.ok(clip.nativeMaster && fs.existsSync(path.join(ROOT, clip.nativeMaster)), `${clipRel}: native master must exist`);
    }
  });

  await t.test('non-armed candidates (Unarmed/Walk/Defeat) enforce attack-only-v1 policy', () => {
    const report = JSON.parse(fs.readFileSync(REPORT_FULL, 'utf8'));
    const nonArmedCells = report.cells.filter(c => ['Unarmed', 'Walk', 'Defeat'].some(act => c.cellId.endsWith(`/${act}`)));
    assert.ok(nonArmedCells.length > 0, 'Must have non-armed candidate cells');
    for (const cell of nonArmedCells) {
      if (cell.status === 'ACTIVE_CANDIDATE') {
        assert.equal(cell.isArmed, false, `Cell ${cell.cellId} must be identified as non-armed`);
        assert.equal(cell.valid, true, `Cell ${cell.cellId} must pass validation`);
      }
    }
  });
});
