const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const EMPTY_HASH = '3c6c50f94ab35e9f96c772731fe6b7950048179bc81b8ab0396cc1edbde89163';

function sha256File(filePath) {
  if (!fs.existsSync(filePath)) return null;
  const data = fs.readFileSync(filePath);
  return crypto.createHash('sha256').update(data).digest('hex');
}

const manifestPath = path.resolve('characters/orc-v1/source/combat-rescue-v5/candidate28manifest.json');
const manifestRaw = fs.readFileSync(manifestPath, 'utf8');
const manifestHash = crypto.createHash('sha256').update(manifestRaw).digest('hex');
const manifest = JSON.parse(manifestRaw);

console.log('--- INTEGRATED MANIFEST AUDIT ---');
console.log('Manifest Path:', manifestPath);
console.log('Manifest SHA-256:', manifestHash);
console.log('Expected SHA-256: 58152a101e16cbc031349b3308649f9ccaa38b99782d4e23bcf2ee43fddc3794');
console.log('SHA-256 match:', manifestHash === '58152a101e16cbc031349b3308649f9ccaa38b99782d4e23bcf2ee43fddc3794');

const cells = manifest.cells || [];
console.log('Total cells defined in manifest:', cells.length);

let totalFramesAccumulated = 0;
let activeCandidatesCount = 0;
let unchangedAliasesCount = 0;
let clipHashesMatchCount = 0;
let missingFiles = [];

const cellDetails = [];
const attackOnlyAudit = [];

for (const cell of cells) {
  const cellId = cell.cellId || `${cell.direction}/${cell.action}`;
  const clipJsonRel = cell.clipJson;
  const clipJsonAbs = clipJsonRel ? path.resolve(clipJsonRel) : null;
  const expectedClipSha = cell.clipSha256;
  
  let actualClipSha = null;
  let fileExists = false;
  let clipData = null;
  let frameCount = 0;
  let durationsMs = cell.durationsMs || [];

  if (clipJsonAbs && fs.existsSync(clipJsonAbs)) {
    fileExists = true;
    actualClipSha = sha256File(clipJsonAbs);
    if (actualClipSha === expectedClipSha) {
      clipHashesMatchCount++;
    } else {
      console.warn(`Hash mismatch for ${cellId}: expected ${expectedClipSha}, got ${actualClipSha}`);
    }
    clipData = JSON.parse(fs.readFileSync(clipJsonAbs, 'utf8'));
    frameCount = clipData.frames ? clipData.frames.length : (cell.frameCount || 0);
  } else {
    missingFiles.push({ cellId, clipJsonRel });
    frameCount = cell.frameCount || 0;
  }

  totalFramesAccumulated += frameCount;

  if (cell.status === 'ACTIVE_CANDIDATE') {
    activeCandidatesCount++;
  } else if (cell.status === 'UNCHANGED_ALIAS') {
    unchangedAliasesCount++;
  }

  cellDetails.push({
    cellId,
    direction: cell.direction,
    action: cell.action,
    status: cell.status,
    frameCount,
    durationsMs,
    totalDurationMs: durationsMs.reduce((a, b) => a + b, 0),
    clipJsonRel,
    hashMatch: actualClipSha === expectedClipSha,
    actualClipSha
  });

  // Verify Attack-Only Policy & Equipment layers
  const isAttack = ['Sword', 'Axe'].includes(cell.action);
  if (isAttack && clipData) {
    const frames = clipData.frames || [];
    
    // Function to check if a frame has visible weapon layers
    function getActiveWeaponLayers(frameObj) {
      if (!frameObj) return [];
      const active = [];
      const layers = frameObj.layers || {};
      if (Array.isArray(layers)) {
        for (const l of layers) {
          if (l.name && (l.name.startsWith('weapon') || l.name.startsWith('hand'))) {
            if (l.visible !== false && l.sha256 !== EMPTY_HASH) {
              active.push(l.name);
            }
          }
        }
      } else {
        for (const [layerName, layerVal] of Object.entries(layers)) {
          if (layerName.startsWith('weapon') || layerName.startsWith('hand')) {
            if (layerVal.visible !== false && layerVal.sha256 !== EMPTY_HASH) {
              active.push(layerName);
            }
          }
        }
      }
      return active;
    }

    const firstActive = getActiveWeaponLayers(frames[0]);
    const lastActive = getActiveWeaponLayers(frames[frames.length - 1]);

    const activePerFrame = frames.map((f, i) => ({
      index: i,
      activeWeapons: getActiveWeaponLayers(f)
    }));

    attackOnlyAudit.push({
      cellId,
      direction: cell.direction,
      action: cell.action,
      frameCount,
      totalDurationMs: durationsMs.reduce((a, b) => a + b, 0),
      firstFrameWeaponActive: firstActive.length > 0,
      firstActiveLayers: firstActive,
      lastFrameWeaponActive: lastActive.length > 0,
      lastActiveLayers: lastActive,
      activeInterval: {
        firstActiveIndex: activePerFrame.findIndex(f => f.activeWeapons.length > 0),
        lastActiveIndex: activePerFrame.slice().reverse().findIndex(f => f.activeWeapons.length > 0) >= 0
          ? (frames.length - 1 - activePerFrame.slice().reverse().findIndex(f => f.activeWeapons.length > 0))
          : -1
      },
      activePerFrame
    });
  } else if (!isAttack && clipData) {
    // Non-attack cell: check that no weapon layer is present/active
    const frames = clipData.frames || [];
    let weaponFound = false;
    for (const f of frames) {
      const layers = f.layers || {};
      if (Array.isArray(layers)) {
        for (const l of layers) {
          if (l.name && (l.name.toLowerCase().includes('weapon') || l.name.toLowerCase().includes('sword') || l.name.toLowerCase().includes('axe'))) {
            if (l.sha256 !== EMPTY_HASH && l.visible !== false) weaponFound = true;
          }
        }
      } else {
        for (const [k, v] of Object.entries(layers)) {
          if (k.toLowerCase().includes('weapon') || k.toLowerCase().includes('sword') || k.toLowerCase().includes('axe')) {
            if (v.sha256 !== EMPTY_HASH && v.visible !== false) weaponFound = true;
          }
        }
      }
    }
    if (weaponFound) {
      console.warn(`WARNING: Active weapon found in non-attack cell: ${cellId}`);
    }
  }
}

console.log('Active candidates count:', activeCandidatesCount, '(expected 13)');
console.log('Unchanged aliases count:', unchangedAliasesCount, '(expected 15)');
console.log('Total frames accumulated:', totalFramesAccumulated, '(expected 226)');
console.log('Clip hashes matching count:', clipHashesMatchCount, 'of', cells.length);
console.log('Missing files:', missingFiles.length);

console.log('\n--- ATTACK ONLY & RECOVERY TERMINAL AUDIT ---');
for (const a of attackOnlyAudit) {
  console.log(`${a.cellId} (${a.frameCount}f, ${a.totalDurationMs}ms): firstWeapon=${a.firstFrameWeaponActive}, lastWeapon=${a.lastFrameWeaponActive}, weaponFrames=[${a.activeInterval.firstActiveIndex}..${a.activeInterval.lastActiveIndex}]`);
}

console.log('\n--- CROSS-VIEW UNIQUENESS & INDEPENDENCE ---');
const crossPairs = [
  ['front_r/Sword', 'front_l/Sword'],
  ['front_r/Axe', 'front_l/Axe'],
  ['back_r/Sword', 'back_l/Sword'],
  ['back_r/Axe', 'back_l/Axe'],
  ['front_r/Unarmed', 'front_l/Unarmed'],
  ['back_r/Unarmed', 'back_l/Unarmed'],
  ['front_r/Walk', 'front_l/Walk'],
  ['back_r/Walk', 'back_l/Walk']
];

for (const [idA, idB] of crossPairs) {
  const cellA = cellDetails.find(c => c.cellId === idA);
  const cellB = cellDetails.find(c => c.cellId === idB);
  if (cellA && cellB) {
    console.log(`${idA} (${cellA.actualClipSha.slice(0, 10)}) vs ${idB} (${cellB.actualClipSha.slice(0, 10)}) -> Unique?`, cellA.actualClipSha !== cellB.actualClipSha);
  }
}

console.log('\n--- GATING & APPROVAL FLAGS ---');
console.log('manifest.eligibleForIntegration:', manifest.eligibleForIntegration);
console.log('manifest.runtimeImplemented:', manifest.runtimeImplemented);
console.log('manifest.creatorApproved:', manifest.creatorApproved);
console.log('manifest.creatorApproval:', manifest.creatorApproval);
console.log('manifest.technicalStatus:', manifest.technicalStatus);
console.log('manifest.artisticStatus:', manifest.artisticStatus);

const outResults = {
  manifestHash,
  manifestExpectedHash: '58152a101e16cbc031349b3308649f9ccaa38b99782d4e23bcf2ee43fddc3794',
  cellsCount: cells.length,
  activeCandidatesCount,
  unchangedAliasesCount,
  totalFramesAccumulated,
  clipHashesMatchCount,
  gating: {
    eligibleForIntegration: manifest.eligibleForIntegration,
    runtimeImplemented: manifest.runtimeImplemented,
    creatorApproved: manifest.creatorApproved,
    creatorApproval: manifest.creatorApproval,
    technicalStatus: manifest.technicalStatus,
    artisticStatus: manifest.artisticStatus
  },
  attackOnlyAudit,
  cellDetails
};

fs.writeFileSync(path.resolve('experiments/main-orc-combat-rescue-v5/qa-antigravity-flash/audit-integrated-details.json'), JSON.stringify(outResults, null, 2), 'utf8');
console.log('Wrote audit-integrated-details.json successfully.');
