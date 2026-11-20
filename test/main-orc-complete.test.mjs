import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { ROOT, DIRECTIONS, readJSON, hash } from '../src/core.mjs';
import { decode, measure } from '../src/images.mjs';

const sha = rel => hash(fs.readFileSync(path.join(ROOT, rel)));
const exists = rel => fs.existsSync(path.join(ROOT, rel));

test('Main Orc complete animation library (4 directions x 7 actions) and Unity-ready staging package', () => {
  const coverage = readJSON(path.join(ROOT, 'reports/orc-v1-animation-coverage-v1.json'));
  assert.equal(coverage.characterId, 'orc-v1');
  assert.equal(coverage.revision, 'main-orc-complete-v1');
  assert.equal(coverage.derivedFrom, 'orc-pixellab-05');
  assert.equal(coverage.paletteRevision, 'green-skin-v3');
  assert.equal(coverage.historicalV4Discarded, true);
  assert.equal(coverage.visibilityPolicy, 'attack-only-v1');
  assert.equal(coverage.artisticApproval, 'PENDING_CREATOR');
  assert.equal(coverage.runtimeImplemented, false);

  assert.equal(coverage.summary.directions, 4);
  assert.equal(coverage.summary.actionsPerDirection, 7);
  assert.equal(coverage.summary.totalActionDirectionCells, 28);
  assert.equal(coverage.summary.completedCells, 28);
  assert.equal(coverage.summary.missingCells, 0);
  assert.equal(coverage.nativeValidationSummary.FAIL, 0);
  assert.equal(coverage.editorBuild.summary.jobs, 75);
  assert.equal(coverage.editorBuild.summary.frames, 599);

  // Verify all 4 directional static bases exist in both 128x128 and 256x256
  for (const dir of DIRECTIONS) {
    assert.ok(exists(`characters/orc-v1/sprites/Directions/orc_v1_dir_${dir}.png`), `Missing native base ${dir}`);
    assert.ok(exists(`characters/orc-v1/source/complete-v1/${dir}/Directions/base.png`), `Missing composite base ${dir}`);
  }

  // Verify all 28 action x direction cells
  const expectedActions = ['Idle', 'Walk', 'Unarmed', 'Sword Attack', 'Axe Attack', 'Hit', 'Defeat'];
  for (const dir of DIRECTIONS) {
    for (const action of expectedActions) {
      const cell = coverage.cells.find(c => c.direction === dir && c.action === action);
      assert.ok(cell, `Missing coverage cell for ${dir} / ${action}`);
      assert.equal(cell.status, 'COMPLETE_VERIFIED');
      assert.ok(exists(cell.clipManifest), `Missing clip manifest ${cell.clipManifest}`);
      assert.ok(exists(cell.master256), `Missing 256 master ${cell.master256}`);

      const clip = readJSON(path.join(ROOT, cell.clipManifest));
      assert.equal(clip.direction, dir);
      assert.equal(clip.artisticApproval, 'PENDING_CREATOR');
      assert.equal(clip.visibilityPolicy, 'attack-only-v1');

      if (action === 'Idle') {
        assert.deepEqual(clip.durationsMs, [400, 450, 500, 450, 400]);
        assert.equal(clip.totalDurationMs, 2200);
        assert.equal(clip.weaponVisible, false);
        assert.equal(clip.loop, true);
      } else if (action === 'Walk') {
        assert.equal(clip.frameCount, 16);
        assert.equal(clip.totalDurationMs, 1280);
        assert.equal(clip.weaponVisible, false);
        assert.equal(clip.loop, true);
      } else if (action === 'Unarmed') {
        assert.deepEqual(clip.durationsMs, [80, 110, 50, 90, 120]);
        assert.equal(clip.totalDurationMs, 450);
        assert.equal(clip.weaponVisible, false);
        assert.equal(clip.oneShot, true);
      } else if (action === 'Hit') {
        assert.deepEqual(clip.durationsMs, [45, 95, 115, 95, 100]);
        assert.equal(clip.totalDurationMs, 450);
        assert.equal(clip.weaponVisible, false);
        assert.equal(clip.oneShot, true);
      } else if (action === 'Defeat') {
        assert.deepEqual(clip.durationsMs, [70, 95, 115, 130, 290]);
        assert.equal(clip.totalDurationMs, 700);
        assert.equal(clip.weaponVisible, false);
        assert.equal(clip.terminal, true);
        assert.equal(clip.terminalFrame, 4);
      } else if (action === 'Sword Attack') {
        assert.equal(clip.frameCount, 13);
        assert.equal(clip.totalDurationMs, 730);
        assert.deepEqual(clip.visibleInterval, [2, 10]);
        assert.deepEqual(clip.layerOrder, ['weaponBack', 'body', 'weaponFront', 'handFront']);
        // Verify frames 0, 1, 11, 12 have weaponVisible = false
        for (const f of clip.frames) {
          const expectedVis = f.index >= 2 && f.index <= 10;
          assert.equal(f.weaponVisible, expectedVis, `Sword ${dir} frame ${f.index} weaponVisible mismatch`);
        }
      } else if (action === 'Axe Attack') {
        assert.equal(clip.frameCount, 12);
        assert.equal(clip.totalDurationMs, 1005);
        assert.deepEqual(clip.visibleInterval, [2, 8]);
        assert.deepEqual(clip.layerOrder, ['weaponBack', 'body', 'weaponFront', 'handFront']);
        for (const f of clip.frames) {
          const expectedVis = f.index >= 2 && f.index <= 8;
          assert.equal(f.weaponVisible, expectedVis, `Axe ${dir} frame ${f.index} weaponVisible mismatch`);
        }
      }
    }
  }

  // Verify Unity handoff contract and staging package in dist/orc-v1/complete-v1/
  const handoffPath = 'dist/orc-v1/complete-v1/Assets/Resources/Characters/orc-v1/unity-handoff-contract.json';
  assert.ok(exists(handoffPath), 'Missing Unity handoff contract in dist/orc-v1/complete-v1/');
  const handoff = readJSON(path.join(ROOT, handoffPath));
  assert.equal(handoff.characterId, 'orc-v1');
  assert.equal(handoff.artisticApproval, 'PENDING_CREATOR');
  assert.equal(handoff.unityRepositoryModified, false);
  assert.equal(handoff.stateMachineSemantics.Idle.weaponVisible, false);
  assert.equal(handoff.stateMachineSemantics.Walk.weaponVisible, false);
  assert.equal(handoff.stateMachineSemantics.Defeat.terminal, true);
  const factoryManifest = readJSON(path.join(ROOT, 'dist/orc-v1/complete-v1/Assets/Resources/Characters/orc-v1/factory-manifest.json'));
  assert.equal(factoryManifest.visibilityPolicy, 'attack-only-v1');

  // Verify active selection pointer and entry candidate pointer remain untouched
  const activePtr = readJSON(path.join(ROOT, 'characters/orc-v1/source/equipment-current.json'));
  assert.equal(activePtr.revision, 'main-orc-onehanded-v3');
  const entryPtr = readJSON(path.join(ROOT, 'characters/orc-v1/source/equipment-entry-candidate.json'));
  assert.equal(entryPtr.revision, 'main-orc-onehanded-entry-v1');

  // Verify protected canonical art files are byte-identical
  const protectedMap = readJSON(path.join(ROOT, 'experiments/main-orc-complete-v1/protected-art.json'));
  for (const [f, expectedSha] of Object.entries(protectedMap)) {
    assert.equal(sha(f), expectedSha, `Protected canonical file altered: ${f}`);
  }
});

test('Artistic Quality Gates v1, 10 production lessons, and measured artistic recovery gates', () => {
  assert.ok(exists('config/artistic-quality-gates-v1.json'), 'Missing config/artistic-quality-gates-v1.json');
  assert.ok(exists('docs/ARTISTIC_QUALITY_GATES.md'), 'Missing docs/ARTISTIC_QUALITY_GATES.md');

  const gates = readJSON(path.join(ROOT, 'config/artistic-quality-gates-v1.json'));
  assert.equal(gates.contractId, 'factory.artistic-quality-gates.v1');
  assert.equal(gates.artisticApprovalIsCreatorOnly, true);
  assert.equal(gates.automationCannotApproveArt, true);

  // Lições semânticas obrigatórias (creator-task.md seção 15) com cobertura total dos 9 campos de evidência
  const requiredSemanticLessonIds = [
    'rear-anatomy-construction',
    'rear-motion-needs-rear-construction',
    'weapon-anchor-vs-natural-choreography',
    'incompatible-attack-reuse',
    'numeric-hit-thresholds-diagnostic-warning',
    'defeat-consistent-terminal-outcome',
    'technical-completion-not-artistic-approval',
    'validated-poses-reused-not-regenerated',
    'failed-artistic-foundations-downstream-rework',
    'complete-review-interface-mandatory',
    'successful-methods-documented-equally',
    'speed-and-scale-evaluation'
  ];
  const lessonIds = gates.productionLessons.map(l => l.id);
  for (const reqId of requiredSemanticLessonIds) {
    assert.ok(lessonIds.includes(reqId), `Missing required semantic lesson ID: ${reqId}`);
  }

  // Todos os 9 campos de evidência obrigatórios por lição com conteúdo não-vazio
  const requiredEvidenceFields = [
    'symptom',
    'verifiedCause',
    'failedApproach',
    'successfulCorrection',
    'reuse',
    'prevention',
    'validation',
    'cost',
    'applicability'
  ];

  for (const l of gates.productionLessons) {
    assert.ok(l.id && typeof l.id === 'string' && l.id.length > 0, `Lesson missing valid id`);
    assert.ok(l.title && typeof l.title === 'string' && l.title.length > 0, `Lesson ${l.id} missing valid title`);
    for (const field of requiredEvidenceFields) {
      assert.ok(field in l, `Lesson ${l.id} missing required evidence field: ${field}`);
      assert.ok(
        typeof l[field] === 'string' && l[field].trim().length > 0,
        `Lesson ${l.id} field ${field} must be a non-empty string`
      );
    }
  }

  // Verifica explicitamente que legacyRecords preserva as regras históricas com as supersessões registradas
  assert.ok(gates.legacyRecords, 'Missing legacyRecords in quality gates');
  assert.ok(gates.legacyRecords.supersededNotes['legacy-rule-4'], 'Missing superseding note for legacy rule 4');
  assert.ok(gates.legacyRecords.supersededNotes['legacy-rule-5'], 'Missing superseding note for legacy rule 5');

  for (const st of ['TECHNICALLY_COMPLETE', 'VISUAL_REVIEW_REQUIRED', 'ARTISTIC_REVISION_REQUIRED', 'CREATOR_APPROVED']) {
    assert.ok(gates.statusTaxonomy.statuses[st], `Missing status definition for ${st}`);
  }

  const coverage = readJSON(path.join(ROOT, 'reports/orc-v1-animation-coverage-v1.json'));
  assert.equal(coverage.technicalStatus, 'TECHNICALLY_COMPLETE');
  assert.equal(coverage.artisticStatus, 'VISUAL_REVIEW_REQUIRED');
  assert.equal(coverage.artisticApproval, 'PENDING_CREATOR');
  assert.equal(coverage.qualityGatesContract, 'config/artistic-quality-gates-v1.json');

  // Hit amplitude thresholds are diagnostic warnings, not hard technical failures.
  const hit = gates.choreographyGate.hit;
  assert.ok(hit.diagnosticWarnings, 'Missing hit diagnosticWarnings');
  assert.equal(hit.diagnosticWarnings.severity, 'warning');
  assert.equal(hit.diagnosticWarnings.notHardFailures, true);
  assert.ok(!('minHeadTopExcursionPx' in (hit.measurableChecks || {})), 'Hit hard minimum must not remain in measurableChecks');
  assert.equal(hit.measurableChecks.bottomPinnedToGroundY, true, 'bottomPinnedToGroundY must remain hard');

  const candidatePtr = readJSON(path.join(ROOT, 'characters/orc-v1/source/equipment-complete-candidate.json'));
  assert.equal(candidatePtr.technicalStatus, 'TECHNICALLY_COMPLETE');
  assert.equal(candidatePtr.artisticStatus, 'VISUAL_REVIEW_REQUIRED');
  assert.equal(candidatePtr.artisticApproval, 'PENDING_CREATOR');

  // 1. Before/After Integrity Gate: preserved rejected-before snapshots must differ from recovered output
  assert.notEqual(
    sha('experiments/main-orc-complete-v1/rejected-before/dir_back_r_before.png'),
    sha('characters/orc-v1/sprites/Directions/orc_v1_dir_back_r.png'),
    'dir_back_r_before.png must differ from recovered orc_v1_dir_back_r.png'
  );
  assert.notEqual(
    sha('experiments/main-orc-complete-v1/rejected-before/dir_back_l_before.png'),
    sha('characters/orc-v1/sprites/Directions/orc_v1_dir_back_l.png'),
    'dir_back_l_before.png must differ from recovered orc_v1_dir_back_l.png'
  );
  assert.notEqual(
    sha('experiments/main-orc-complete-v1/rejected-before/front_r_defeat_strip_before.png'),
    sha('characters/orc-v1/source/complete-v1/front_r/Defeat/native-strip.png'),
    'front_r_defeat_strip_before.png must differ from recovered front_r Defeat strip'
  );
  assert.notEqual(
    sha('experiments/main-orc-complete-v1/rejected-before/front_r_hit_strip_before.png'),
    sha('characters/orc-v1/source/complete-v1/front_r/Hit/native-strip.png'),
    'front_r_hit_strip_before.png must differ from recovered front_r Hit strip'
  );

  // 2. Directional View Gate: rear bases differ from frontal bases and from each other
  assert.notEqual(
    sha('characters/orc-v1/sprites/Directions/orc_v1_dir_back_r.png'),
    sha('characters/orc-v1/sprites/Directions/orc_v1_dir_front_r.png')
  );
  assert.notEqual(
    sha('characters/orc-v1/sprites/Directions/orc_v1_dir_back_r.png'),
    sha('characters/orc-v1/sprites/Directions/orc_v1_dir_back_l.png')
  );

  // 3. Choreography Gate: Hit impact excursion & Defeat multi-stage volumetric collapse across all 4 directions
  function stats(relPath) {
    const { image } = decode(path.join(ROOT, relPath));
    const m = measure(image);
    let sx = 0, sy = 0, n = 0;
    for (let y = 0; y < image.height; y++) {
      for (let x = 0; x < image.width; x++) {
        if (image.data[(y * image.width + x) * 4 + 3] > 0) { sx += x; sy += y; n++; }
      }
    }
    return { ...m, w: m.right - m.left + 1, h: m.contentHeight, cx: sx / n, cy: sy / n };
  }

  for (const d of DIRECTIONS) {
    const hs = [0, 1, 2, 3, 4].map(i => stats(`characters/orc-v1/source/complete-v1/${d}/Hit/0${i}.png`));
    const topExc = Math.max(...hs.map(s => s.top)) - Math.min(...hs.map(s => s.top));
    const hComp = Math.max(...hs.map(s => s.h)) - Math.min(...hs.map(s => s.h));
    const cShift = Math.max(...hs.map(s => Math.hypot(s.cx - hs[0].cx, s.cy - hs[0].cy)));
    // Hit amplitude/timing are diagnostic warnings, not hard technical failures.
    // Only bottom-pinned groundY and integrity remain hard for Hit.
    // Historical diagnostic values (not minimums): headTopExcursion 12-13px, centroidDisplacement 5.74-7.55px,
    // heightCompression 12-13px, motionEnergyVsIdle 5.6x. Reassess at 1x/0.75x/0.5x and game scale.
    const hitDiagnostic = {
      headTopExcursionPx: topExc,
      heightCompressionPx: hComp,
      centroidDisplacementPx: cShift,
      note: 'Diagnostic only; creator visual review at actual playback speed decides artistic acceptability.'
    };
    assert.ok(typeof hitDiagnostic.headTopExcursionPx === 'number' && Number.isFinite(hitDiagnostic.headTopExcursionPx));
    assert.ok(typeof hitDiagnostic.heightCompressionPx === 'number' && Number.isFinite(hitDiagnostic.heightCompressionPx));
    assert.ok(typeof hitDiagnostic.centroidDisplacementPx === 'number' && Number.isFinite(hitDiagnostic.centroidDisplacementPx));

    const ds = [0, 1, 2, 3, 4].map(i => stats(`characters/orc-v1/source/complete-v1/${d}/Defeat/0${i}.png`));
    assert.ok(ds[4].h >= 58, `Defeat ${d} terminal height (${ds[4].h}px) must retain 3D body volume (>= 58px)`);
    assert.ok(ds[4].w / ds[4].h >= 1.3, `Defeat ${d} terminal aspect ratio (${(ds[4].w / ds[4].h).toFixed(2)}) must be >= 1.3`);
  }

  // 3b. Warning-vs-technical-failure distinction: Hit amplitude thresholds live under diagnosticWarnings,
  // not hard measurableChecks. bottomPinnedToGroundY and integrity checks remain hard.
  assert.ok(hit.diagnosticWarnings, 'Missing hit diagnosticWarnings');
  assert.equal(hit.diagnosticWarnings.severity, 'warning');
  assert.equal(hit.diagnosticWarnings.artisticInterpretation, true);
  assert.equal(hit.diagnosticWarnings.notHardFailures, true);
  assert.ok(!('minHeadTopExcursionPx' in (hit.measurableChecks || {})), 'Hit hard minimum must not remain in measurableChecks');
  assert.ok(!('minCentroidDisplacementPx' in (hit.measurableChecks || {})), 'Hit hard minimum must not remain in measurableChecks');
  assert.ok(!('minHeightCompressionPx' in (hit.measurableChecks || {})), 'Hit hard minimum must not remain in measurableChecks');
  assert.ok(!('minMotionEnergyVsIdle' in (hit.measurableChecks || {})), 'Hit hard minimum must not remain in measurableChecks');
  assert.equal(hit.measurableChecks.bottomPinnedToGroundY, true, 'bottomPinnedToGroundY must remain hard for Hit');

  // 4. Frontal Attack Head Outline Cleanup Gate: zero bright neutral-grey halo pixels on green skull boundary
  for (const d of ['front_r', 'front_l']) {
    for (const cat of ['Sword', 'Axe']) {
      const clip = readJSON(path.join(ROOT, `characters/orc-v1/source/complete-v1/${d}/${cat}/Attack/clip.json`));
      for (const f of clip.frames) {
        const { image } = decode(path.join(ROOT, f.png));
        let haloCount = 0;
        for (let y = 68; y <= 83; y++) {
          for (let x = 116; x <= 149; x++) {
            const idx = (y * image.width + x) * 4;
            const r = image.data[idx], g = image.data[idx + 1], b = image.data[idx + 2], a = image.data[idx + 3];
            if (a > 0 && g >= r + 12 && g >= b + 14) {
              for (const [dx, dy] of [[-1, 0], [1, 0], [0, -1], [0, 1]]) {
                const ni = ((y + dy) * image.width + (x + dx)) * 4;
                const nr = image.data[ni], ng = image.data[ni + 1], nb = image.data[ni + 2], na = image.data[ni + 3];
                if (na > 0 && nr >= 90 && Math.abs(nr - ng) <= 10 && Math.abs(ng - nb) <= 16) haloCount++;
              }
            }
          }
        }
        assert.equal(haloCount, 0, `Found ${haloCount} head-crown halo pixels in ${d} ${cat} frame ${f.index}`);
      }
    }
  }

  // 5. Interactive Review Studios contain Before/After visual comparison and status badges
  for (const studioRel of [
    'Biblioteca de Arte/Personagens Jogaveis/Orc V1/index.html',
    'Biblioteca de Arte/Estudos Comparativos/Orc principal - Biblioteca completa/index.html'
  ]) {
    assert.ok(exists(studioRel), `Missing review studio ${studioRel}`);
    const htmlText = fs.readFileSync(path.join(ROOT, studioRel), 'utf8');
    assert.ok(htmlText.includes('Comparação Visual Antes (v1 Rejeitada) vs Depois (Recuperação Artística)'), `Missing Before/After section in ${studioRel}`);
    assert.ok(htmlText.includes('VISUAL_REVIEW_REQUIRED'), `Missing VISUAL_REVIEW_REQUIRED badge in ${studioRel}`);
    assert.ok(htmlText.includes('AntesDepois/dir_back_r_before.png'), `Missing AntesDepois reference in ${studioRel}`);
  }
});
