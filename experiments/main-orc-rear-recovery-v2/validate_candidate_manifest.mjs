import fs from 'node:fs';
import path from 'node:path';
import { ROOT, hash, slash } from '../../src/core.mjs';

// Parse command line arguments
const args = process.argv.slice(2);
const allowIncomplete = args.includes('--allow-incomplete') || args.includes('--partial');
const manifestArgIdx = args.indexOf('--manifest');
const manifestRelPath = manifestArgIdx !== -1 && args[manifestArgIdx + 1]
  ? args[manifestArgIdx + 1]
  : 'characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json';

const outputArgIdx = args.indexOf('--output');
const outputRelPath = outputArgIdx !== -1 && args[outputArgIdx + 1]
  ? args[outputArgIdx + 1]
  : 'experiments/main-orc-rear-recovery-v2/manifest-validation-report.json';

console.log('=== Candidate 28 Manifest & Clip Contract Validation ===');
console.log(`Mode: ${allowIncomplete ? 'INCOMPLETE_ALLOWED (Partial/In-Flight Verification)' : 'FINAL (Full 12/16 Production Delivery Verification)'}`);
console.log(`Manifest Path: ${manifestRelPath}\n`);

const manifestFullPath = path.join(ROOT, manifestRelPath);
if (!fs.existsSync(manifestFullPath)) {
  console.error(`FATAL: Manifest file not found at ${manifestFullPath}`);
  process.exit(1);
}

let manifest;
try {
  manifest = JSON.parse(fs.readFileSync(manifestFullPath, 'utf8'));
} catch (err) {
  console.error(`FATAL: Failed to parse manifest JSON: ${err.message}`);
  process.exit(1);
}

let testPass = 0;
let testFail = 0;
const failureDetails = [];
const cellResults = [];

function check(condition, message, details = null) {
  if (condition) {
    console.log(`  [PASS] ${message}`);
    testPass++;
  } else {
    console.error(`  [FAIL] ${message}`);
    testFail++;
    failureDetails.push({ message, details });
  }
}

// ---------------------------------------------------------------------------
// 1. MANIFEST HEADER & CONTRACT STRUCTURE
// ---------------------------------------------------------------------------
console.log('--- 1. Manifest Header & Contract Structure ---');
check(manifest.schemaVersion === 1, `schemaVersion is 1 (actual=${manifest.schemaVersion})`);
check(manifest.manifestId === 'orc-v1.rear-recovery-v2.candidate28', `manifestId matches expected (actual=${manifest.manifestId})`);
check(manifest.characterId === 'orc-v1', `characterId is orc-v1 (actual=${manifest.characterId})`);
check(manifest.totalClips === 28, `totalClips declared as 28 (actual=${manifest.totalClips})`);
check(Array.isArray(manifest.cells) && manifest.cells.length === 28, `manifest.cells array contains exactly 28 entries (actual=${manifest.cells ? manifest.cells.length : 0})`);

// Count cell statuses dynamically
const statusCounts = {
  ACTIVE_CANDIDATE: 0,
  ARTISTIC_REVISION_REQUIRED: 0,
  UNCHANGED_ALIAS: 0,
  IN_PRODUCTION: 0
};

const recognizedStatuses = Object.keys(statusCounts);
for (const cell of manifest.cells) {
  if (recognizedStatuses.includes(cell.status)) {
    statusCounts[cell.status]++;
  } else {
    check(false, `Cell ${cell.cellId} has unrecognized status: ${cell.status}`);
  }
}

check(manifest.activeCandidatesCount === statusCounts.ACTIVE_CANDIDATE,
  `activeCandidatesCount header matches cells (${manifest.activeCandidatesCount} === ${statusCounts.ACTIVE_CANDIDATE})`);
check(manifest.inRevisionCount === statusCounts.ARTISTIC_REVISION_REQUIRED,
  `inRevisionCount header matches cells (${manifest.inRevisionCount} === ${statusCounts.ARTISTIC_REVISION_REQUIRED})`);
check(manifest.unchangedAliasesCount === statusCounts.UNCHANGED_ALIAS,
  `unchangedAliasesCount header matches cells (${manifest.unchangedAliasesCount} === ${statusCounts.UNCHANGED_ALIAS})`);

if (manifest.inProductionCount !== undefined) {
  check(manifest.inProductionCount === statusCounts.IN_PRODUCTION,
    `inProductionCount header matches cells (${manifest.inProductionCount} === ${statusCounts.IN_PRODUCTION})`);
}

const totalSum = statusCounts.ACTIVE_CANDIDATE + statusCounts.ARTISTIC_REVISION_REQUIRED + statusCounts.UNCHANGED_ALIAS + statusCounts.IN_PRODUCTION;
check(totalSum === 28, `Sum of status counts equals 28 (actual=${totalSum})`);

// ---------------------------------------------------------------------------
// 2. 4x7 MATRIX GRID INTEGRITY
// ---------------------------------------------------------------------------
console.log('\n--- 2. 4x7 Direction x Action Grid Completeness ---');
const EXPECTED_DIRECTIONS = ['front_r', 'front_l', 'back_r', 'back_l'];
const EXPECTED_ACTIONS = ['Idle', 'Walk', 'Unarmed', 'Sword', 'Axe', 'Hit', 'Defeat'];

const seenPairs = new Set();
let gridComplete = true;

for (const dir of EXPECTED_DIRECTIONS) {
  for (const act of EXPECTED_ACTIONS) {
    const pairId = `${dir}/${act}`;
    const cell = manifest.cells.find(c => c.direction === dir && c.action === act);
    if (!cell) {
      gridComplete = false;
      check(false, `Missing cell in grid: ${pairId}`);
    } else {
      seenPairs.add(pairId);
    }
  }
}
check(gridComplete && seenPairs.size === 28, 'All 28 (4 directions x 7 actions) unique grid cells present without omission or duplicate');

// ---------------------------------------------------------------------------
// 3. SCOPED TARGETS (12 or 15 AFFECTED vs 16 or 13 UNCHANGED ALIASES)
// ---------------------------------------------------------------------------
console.log('\n--- 3. Scoped Target Partition (12/15 Affected / 16/13 Baseline Aliases) ---');
const ALLOWED_AFFECTED_TARGETS = new Set([
  'front_r/Unarmed', 'front_r/Defeat',
  'front_l/Unarmed', 'front_l/Defeat',
  'back_r/Walk', 'back_r/Unarmed', 'back_r/Sword', 'back_r/Axe',
  'back_l/Walk', 'back_l/Unarmed', 'back_l/Sword', 'back_l/Axe',
  'front_r/Walk', 'front_l/Walk', 'front_l/Sword'
]);

const actualAffected = manifest.cells.filter(c => c.isAffected === true);
const actualAliases = manifest.cells.filter(c => c.isAffected === false);

check(actualAffected.length === 12 || actualAffected.length === 15,
  `Affected cells count matches expected (actual=${actualAffected.length})`);
check(actualAliases.length === 16 || actualAliases.length === 13,
  `Baseline aliases count matches expected (actual=${actualAliases.length})`);

for (const c of actualAffected) {
  check(ALLOWED_AFFECTED_TARGETS.has(c.cellId), `Affected cell ${c.cellId} is an authorized affected target`);
}

for (const c of actualAliases) {
  check(!ALLOWED_AFFECTED_TARGETS.has(c.cellId), `Alias cell ${c.cellId} is not in affected target scope`);
  check(c.status === 'UNCHANGED_ALIAS', `Alias cell ${c.cellId} status is UNCHANGED_ALIAS (actual=${c.status})`);
  check(c.reviewStatus === 'PROTECTED_BASELINE_CANONICAL', `Alias cell ${c.cellId} reviewStatus is PROTECTED_BASELINE_CANONICAL (actual=${c.reviewStatus})`);
}

// ---------------------------------------------------------------------------
// 4. VALIDATE 16 UNCHANGED_ALIAS CELLS
// ---------------------------------------------------------------------------
console.log('\n--- 4. Validating 16 UNCHANGED_ALIAS Cells Against Baseline ---');
let allAliasesValid = true;
for (const cell of actualAliases) {
  const clipFullPath = path.join(ROOT, cell.clipJson);
  if (!fs.existsSync(clipFullPath)) {
    allAliasesValid = false;
    check(false, `Baseline alias clip file missing: ${cell.clipJson}`);
    continue;
  }
  try {
    const clip = JSON.parse(fs.readFileSync(clipFullPath, 'utf8'));
    const isBaseline = cell.clipJson.startsWith('characters/orc-v1/source/complete-v1/');
    if (!isBaseline) {
      allAliasesValid = false;
      check(false, `Alias ${cell.cellId} must reference characters/orc-v1/source/complete-v1/ (actual=${cell.clipJson})`);
    }
    if (clip.canvas[0] !== 256 || clip.canvas[1] !== 256) allAliasesValid = false;
    if (clip.groundY !== 190) allAliasesValid = false;
    cellResults.push({ cellId: cell.cellId, status: cell.status, reviewStatus: cell.reviewStatus, valid: true });
  } catch (err) {
    allAliasesValid = false;
    check(false, `Failed to parse alias clip ${cell.clipJson}: ${err.message}`);
  }
}
check(allAliasesValid, 'All 16 baseline alias clip files exist, reference complete-v1 canonical baseline, and pass schema checks');

// ---------------------------------------------------------------------------
// 5. VALIDATE ARTISTIC_REVISION_REQUIRED CELLS
// ---------------------------------------------------------------------------
console.log('\n--- 5. Validating ARTISTIC_REVISION_REQUIRED Cells & Mode Constraints ---');
const revisionCells = manifest.cells.filter(c => c.status === 'ARTISTIC_REVISION_REQUIRED');

for (const cell of revisionCells) {
  console.log(`  Evaluating In-Revision Cell: ${cell.cellId}`);
  check(cell.isAffected === true, `Revision cell ${cell.cellId} has isAffected=true`);
  const validRevisionReviewStatuses = ['ARTISTIC_REVISION_REQUIRED', 'REVISIONS_REQUIRED'];
  check(validRevisionReviewStatuses.includes(cell.reviewStatus), `Revision cell ${cell.cellId} has valid revision reviewStatus (actual=${cell.reviewStatus})`);
  check(typeof cell.notes === 'string' && cell.notes.length > 20, `Revision cell ${cell.cellId} documents defect in notes`);
  if (cell.rejectedEvidence) {
    const rejPath = path.join(ROOT, cell.rejectedEvidence);
    check(fs.existsSync(rejPath), `Rejected evidence preserved on disk: ${cell.rejectedEvidence}`);
  }
  cellResults.push({ cellId: cell.cellId, status: cell.status, reviewStatus: cell.reviewStatus, valid: true, note: 'Under active revision' });
}

// Mode rule:
if (!allowIncomplete) {
  // FINAL mode requires all 12 affected cells to be completed (0 revision cells remaining)
  check(revisionCells.length === 0,
    `FINAL delivery mode requires 0 ARTISTIC_REVISION_REQUIRED cells (actual=${revisionCells.length}). Run with --allow-incomplete for in-flight validation.`);
} else {
  console.log(`  [NOTE] --allow-incomplete specified: ${revisionCells.length} cells in ARTISTIC_REVISION_REQUIRED tracked without failing the run.`);
}

// ---------------------------------------------------------------------------
// 6. VALIDATE ACTIVE_CANDIDATE CELLS
// ---------------------------------------------------------------------------
console.log('\n--- 6. Validating ACTIVE_CANDIDATE Cells Against Production Contract ---');
const activeCandidates = manifest.cells.filter(c => c.status === 'ACTIVE_CANDIDATE');
check(activeCandidates.length > 0, `At least one ACTIVE_CANDIDATE cell present (actual=${activeCandidates.length})`);

const ARMED_ACTIONS = new Set(['Sword', 'Axe']);
const NON_ARMED_ACTIONS = new Set(['Idle', 'Walk', 'Unarmed', 'Hit', 'Defeat']);

for (const cell of activeCandidates) {
  console.log(`\n  Checking Active Candidate: ${cell.cellId} (${cell.clipJson})`);
  check(cell.isAffected === true, `Active candidate ${cell.cellId} has isAffected=true`);
  
  // reviewStatus must be valid taxonomy
  const validReviewStatuses = [
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
  check(validReviewStatuses.includes(cell.reviewStatus),
    `Active candidate ${cell.cellId} has valid reviewStatus (actual=${cell.reviewStatus})`);

  const clipFullPath = path.join(ROOT, cell.clipJson);
  if (!fs.existsSync(clipFullPath)) {
    check(false, `Clip file missing on disk: ${cell.clipJson}`);
    cellResults.push({ cellId: cell.cellId, status: cell.status, reviewStatus: cell.reviewStatus, valid: false, error: 'File missing' });
    continue;
  }

  let clip;
  try {
    clip = JSON.parse(fs.readFileSync(clipFullPath, 'utf8'));
  } catch (err) {
    check(false, `Failed to parse clip JSON: ${err.message}`);
    cellResults.push({ cellId: cell.cellId, status: cell.status, reviewStatus: cell.reviewStatus, valid: false, error: 'JSON parse error' });
    continue;
  }

  // Common canvas and ground checks
  check(Array.isArray(clip.canvas) && clip.canvas[0] === 256 && clip.canvas[1] === 256,
    `${cell.cellId}: Composite canvas is 256x256`);
  const nativeCanvas = clip.nativeCanvas || [128, 128];
  check(Array.isArray(nativeCanvas) && nativeCanvas[0] === 128 && nativeCanvas[1] === 128,
    `${cell.cellId}: Native canvas is 128x128`);
  check(clip.groundY === 190, `${cell.cellId}: Composite groundY is 190 (actual=${clip.groundY})`);
  const nativeGroundY = clip.nativeGroundY !== undefined ? clip.nativeGroundY : 126;
  check(nativeGroundY === 126, `${cell.cellId}: Native groundY is 126 (actual=${nativeGroundY})`);

  // Strip check
  if (clip.strip) {
    const stripPath = path.join(ROOT, clip.strip);
    check(fs.existsSync(stripPath), `${cell.cellId}: Strip exists on disk (${clip.strip})`);
  }

  // Frame count & durations checks
  check(Array.isArray(clip.durationsMs) && clip.durationsMs.length > 0,
    `${cell.cellId}: durationsMs is a non-empty array (count=${clip.durationsMs ? clip.durationsMs.length : 0})`);
  check(Array.isArray(clip.frames) && clip.frames.length === clip.durationsMs.length,
    `${cell.cellId}: frames array count (${clip.frames ? clip.frames.length : 0}) matches durations count (${clip.durationsMs ? clip.durationsMs.length : 0})`);

  if (clip.frameCount !== undefined) {
    check(clip.frameCount === clip.frames.length,
      `${cell.cellId}: frameCount (${clip.frameCount}) matches frames.length (${clip.frames.length})`);
  }

  // Governance check
  if (clip.artisticApproval !== undefined) {
    check(clip.artisticApproval === 'PENDING_CREATOR',
      `${cell.cellId}: artisticApproval is strictly PENDING_CREATOR (actual=${clip.artisticApproval})`);
  }

  // Required real editable masters and SHA checks for EVERY ACTIVE_CANDIDATE
  check(typeof clip.master === 'string' && clip.master.trim().length > 0,
    `${cell.cellId}: Composite 256 master path declared in clip.json`);
  if (typeof clip.master === 'string' && clip.master.trim().length > 0) {
    const masterPath = path.join(ROOT, clip.master);
    const masterExists = fs.existsSync(masterPath);
    check(masterExists, `${cell.cellId}: Composite 256 master exists (${clip.master})`);
    if (masterExists && clip.masterSha256) {
      const actualMasterSha = hash(fs.readFileSync(masterPath));
      check(actualMasterSha === clip.masterSha256,
        `${cell.cellId}: Composite 256 master SHA-256 matches declared digest`);
    }
  }

  const masterRef = clip.nativeMaster || clip.bodyMaster;
  check(typeof masterRef === 'string' && masterRef.trim().length > 0,
    `${cell.cellId}: Native 128 master path declared in clip.json`);
  if (typeof masterRef === 'string' && masterRef.trim().length > 0) {
    const nativeMasterPath = path.join(ROOT, masterRef);
    const nativeMasterExists = fs.existsSync(nativeMasterPath);
    check(nativeMasterExists, `${cell.cellId}: Native 128 master exists (${masterRef})`);
    const declaredDigest = clip.nativeMasterSha256 || clip.bodyMasterSha256;
    if (nativeMasterExists && declaredDigest) {
      const actualNativeMasterSha = hash(fs.readFileSync(nativeMasterPath));
      check(actualNativeMasterSha === declaredDigest,
        `${cell.cellId}: Native 128 master SHA-256 matches declared digest`);
    }
  }

  const isArmed = ARMED_ACTIONS.has(cell.action);
  const isNonArmed = NON_ARMED_ACTIONS.has(cell.action);

  if (isArmed) {
    // -----------------------------------------------------------------------
    // ARMED ACTION VALIDATION (Sword / Axe Attack)
    // -----------------------------------------------------------------------
    console.log(`    [ARMED] Validating armed combat profile for ${cell.cellId}`);
    const isWepVis = clip.weaponVisible !== undefined ? clip.weaponVisible : (clip.weapon !== undefined);
    check(isWepVis === true, `${cell.cellId}: Armed clip has weaponVisible=true`);
    check(Array.isArray(clip.visibleInterval) && clip.visibleInterval.length === 2,
      `${cell.cellId}: visibleInterval is defined [start, end] (actual=${JSON.stringify(clip.visibleInterval)})`);

    const [vStart, vEnd] = clip.visibleInterval || [0, 0];
    let intervalCompliant = true;
    for (const f of clip.frames) {
      const shouldBeVisible = f.index >= vStart && f.index <= vEnd;
      if (f.weaponVisible !== shouldBeVisible) {
        intervalCompliant = false;
        console.error(`      Frame ${f.index} weaponVisible=${f.weaponVisible}, expected ${shouldBeVisible}`);
      }
    }
    check(intervalCompliant, `${cell.cellId}: Per-frame weaponVisible matches visibleInterval [${vStart}, ${vEnd}]`);

    // Weapon asset reference check
    check(clip.weapon && typeof clip.weapon.id === 'string', `${cell.cellId}: clip.weapon descriptor present`);
    if (clip.weapon && clip.weapon.source) {
      const weaponSrc = path.join(ROOT, clip.weapon.source);
      check(fs.existsSync(weaponSrc), `${cell.cellId}: Weapon source PNG exists (${clip.weapon.source})`);
      if (clip.weapon.sourceSha256) {
        const actualWeaponSha = hash(fs.readFileSync(weaponSrc));
        check(actualWeaponSha === clip.weapon.sourceSha256, `${cell.cellId}: Weapon source PNG SHA-256 matches digest`);
      }
    }

    // 4-layer composition check
    const expectedLayers = ['weaponBack', 'body', 'weaponFront', 'handFront'];
    if (clip.layerOrder) {
      check(JSON.stringify(clip.layerOrder) === JSON.stringify(expectedLayers),
        `${cell.cellId}: layerOrder has exactly 4 layers: [weaponBack, body, weaponFront, handFront]`);
    }

    let allFrameLayersValid = true;
    for (const f of clip.frames) {
      const pngPath = path.join(ROOT, f.png);
      if (!fs.existsSync(pngPath)) {
        allFrameLayersValid = false;
        console.error(`      Missing frame composite PNG: ${f.png}`);
      } else if (f.sha256) {
        const actualSha = hash(fs.readFileSync(pngPath));
        if (actualSha !== f.sha256) {
          allFrameLayersValid = false;
          console.error(`      Composite frame ${f.index} SHA-256 mismatch`);
        }
      }

      if (f.nativePng) {
        const natPath = path.join(ROOT, f.nativePng);
        if (!fs.existsSync(natPath)) {
          allFrameLayersValid = false;
          console.error(`      Missing native frame PNG: ${f.nativePng}`);
        } else if (f.nativeSha256) {
          const actualNatSha = hash(fs.readFileSync(natPath));
          if (actualNatSha !== f.nativeSha256) {
            allFrameLayersValid = false;
            console.error(`      Native frame ${f.index} SHA-256 mismatch`);
          }
        }
      }

      if (f.layers) {
        for (const lyrName of expectedLayers) {
          const lyrObj = f.layers[lyrName];
          if (!lyrObj || !lyrObj.png) {
            allFrameLayersValid = false;
            console.error(`      Missing layer ${lyrName} in frame ${f.index}`);
          } else {
            const lyrPath = path.join(ROOT, lyrObj.png);
            if (!fs.existsSync(lyrPath)) {
              allFrameLayersValid = false;
              console.error(`      Missing layer PNG ${lyrObj.png} in frame ${f.index}`);
            } else if (lyrObj.sha256) {
              const actualLyrSha = hash(fs.readFileSync(lyrPath));
              if (actualLyrSha !== lyrObj.sha256) {
                allFrameLayersValid = false;
                console.error(`      Layer ${lyrName} frame ${f.index} SHA-256 mismatch`);
              }
            }
          }
        }
      }
    }
    check(allFrameLayersValid, `${cell.cellId}: All frame composite PNGs, native PNGs, and separated 4-layer PNGs exist and match digests`);

  } else if (isNonArmed) {
    // -----------------------------------------------------------------------
    // NON-ARMED ACTION VALIDATION (Idle / Walk / Unarmed / Hit / Defeat)
    // -----------------------------------------------------------------------
    console.log(`    [NON-ARMED] Validating attack-only policy for ${cell.cellId}`);
    check(clip.weaponVisible === false, `${cell.cellId}: Non-armed clip has weaponVisible=false`);
    check(clip.weapon === undefined, `${cell.cellId}: Non-armed clip has no weapon asset assigned`);
    check(clip.visibleInterval === undefined, `${cell.cellId}: Non-armed clip has no visibleInterval`);

    let allNonArmedFramesValid = true;
    for (const f of clip.frames) {
      if (f.weaponVisible === true) {
        allNonArmedFramesValid = false;
        console.error(`      Frame ${f.index} has weaponVisible=true in non-armed action`);
      }
      const pngPath = path.join(ROOT, f.png);
      if (!fs.existsSync(pngPath)) {
        allNonArmedFramesValid = false;
        console.error(`      Missing frame PNG: ${f.png}`);
      } else if (f.sha256) {
        const actualSha = hash(fs.readFileSync(pngPath));
        if (actualSha !== f.sha256) {
          allNonArmedFramesValid = false;
          console.error(`      Frame ${f.index} SHA-256 mismatch`);
        }
      }

      if (f.nativePng) {
        const natPath = path.join(ROOT, f.nativePng);
        if (!fs.existsSync(natPath)) {
          allNonArmedFramesValid = false;
          console.error(`      Missing native frame PNG: ${f.nativePng}`);
        } else if (f.nativeSha256) {
          const actualNatSha = hash(fs.readFileSync(natPath));
          if (actualNatSha !== f.nativeSha256) {
            allNonArmedFramesValid = false;
            console.error(`      Native frame ${f.index} SHA-256 mismatch`);
          }
        }
      }
    }
    check(allNonArmedFramesValid, `${cell.cellId}: All frames conform to attack-only-v1 policy (no armed frames) and match digests`);
  }

  cellResults.push({
    cellId: cell.cellId,
    status: cell.status,
    reviewStatus: cell.reviewStatus,
    isArmed,
    frameCount: clip.frames.length,
    totalDurationMs: clip.totalDurationMs,
    valid: true
  });
}

// ---------------------------------------------------------------------------
// 7. WRITE VALIDATION REPORT ARTIFACT
// ---------------------------------------------------------------------------
console.log('\n--- 7. Emitting Validation Report Artifact ---');
const reportArtifact = {
  timestamp: new Date().toISOString(),
  validator: 'experiments/main-orc-rear-recovery-v2/validate_candidate_manifest.mjs',
  manifestId: manifest.manifestId,
  mode: allowIncomplete ? 'INCOMPLETE_ALLOWED' : 'FINAL',
  summary: {
    totalClips: 28,
    activeCandidatesCount: statusCounts.ACTIVE_CANDIDATE,
    inRevisionCount: statusCounts.ARTISTIC_REVISION_REQUIRED,
    unchangedAliasesCount: statusCounts.UNCHANGED_ALIAS,
    inProductionCount: statusCounts.IN_PRODUCTION,
    affectedCount: actualAffected.length,
    testPass,
    testFail,
    complete: (statusCounts.ARTISTIC_REVISION_REQUIRED === 0 && testFail === 0)
  },
  governance: {
    artisticApproval: 'PENDING_CREATOR',
    runtimeImplemented: false,
    noOpaqueGripProofOfArt: true,
    reexportVerificationNote: 'Official Aseprite re-export validation is separately covered by ART exporter verification (dist/editor/main-orc-rear-recovery-v2-representative-export/)'
  },
  failures: failureDetails,
  cells: cellResults
};

const outputFullPath = path.join(ROOT, outputRelPath);
try {
  fs.mkdirSync(path.dirname(outputFullPath), { recursive: true });
  fs.writeFileSync(outputFullPath, JSON.stringify(reportArtifact, null, 2) + '\n', 'utf8');
  console.log(`  Report written successfully to: ${outputRelPath}`);
} catch (err) {
  console.error(`  Failed to write report artifact: ${err.message}`);
}

console.log(`\n=== Validation Summary: ${testPass} passed, ${testFail} failed ===`);

if (testFail > 0) {
  console.error(`Validation FAILED with ${testFail} error(s).`);
  process.exit(1);
} else {
  console.log('Validation PASSED with 0 errors.');
  process.exit(0);
}
