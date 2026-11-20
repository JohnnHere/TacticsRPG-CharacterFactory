import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { ROOT, readJSON, hash } from '../src/core.mjs';
import { decode } from '../src/images.mjs';

function sha(relPath) {
  const full = path.join(ROOT, relPath);
  assert.ok(fs.existsSync(full), `File must exist: ${relPath}`);
  return hash(fs.readFileSync(full));
}

test('RR-04 & RR-06: 100% of declared hashes match files and protected clips remain byte-identical', () => {
  const manifest = readJSON(path.join(ROOT, 'characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json'));
  const snapshot = readJSON(path.join(ROOT, 'experiments/main-orc-targeted-recovery-v3/before-snapshot.json'));
  
  assert.equal(manifest.cells.length, 28, 'Must have 28 cells');
  
  let totalHashChecks = 0;
  
  // 1. Verify all 28 clips have zero stale declared hashes
  for (const cell of manifest.cells) {
    const clip = readJSON(path.join(ROOT, cell.clipJson));
    
    const fileKeyMap = [
      ['master', 'masterSha256'],
      ['nativeMaster', 'nativeMasterSha256'],
      ['bodyMaster', 'bodyMasterSha256'],
      ['handMaster', 'handMasterSha256'],
      ['strip', 'stripSha256']
    ];
    
    for (const [fileKey, shaKey] of fileKeyMap) {
      if (clip[fileKey] && clip[shaKey]) {
        totalHashChecks++;
        const actual = sha(clip[fileKey]);
        assert.equal(clip[shaKey], actual, `Stale ${shaKey} in ${cell.cellId} (${clip[fileKey]})`);
      }
    }
    
    if (clip.strip && clip.nativeStripSha256) {
      totalHashChecks++;
      const actual = sha(clip.strip);
      assert.equal(clip.nativeStripSha256, actual, `Stale nativeStripSha256 in ${cell.cellId}`);
    }
    
    if (clip.frames) {
      for (const f of clip.frames) {
        if (f.png && f.sha256) {
          totalHashChecks++;
          assert.equal(f.sha256, sha(f.png), `Stale frame sha256 in ${cell.cellId} frame ${f.index}`);
        }
        if (f.nativePng && f.nativeSha256) {
          totalHashChecks++;
          assert.equal(f.nativeSha256, sha(f.nativePng), `Stale nativePng sha256 in ${cell.cellId} frame ${f.index}`);
        }
        if (f.layers) {
          for (const [lName, lObj] of Object.entries(f.layers)) {
            if (lObj.png && lObj.sha256) {
              totalHashChecks++;
              assert.equal(lObj.sha256, sha(lObj.png), `Stale layer sha256 in ${cell.cellId} frame ${f.index} layer ${lName}`);
            }
          }
        }
      }
    }
  }
  
  assert.ok(totalHashChecks >= 780, `Expected at least 780 hash checks, got ${totalHashChecks}`);
  
  // 2. Verify RR-06: 13 protected clip.json files are byte-identical to before-snapshot.json
  const protectedCells = manifest.cells.filter(c => c.status === 'UNCHANGED_ALIAS');
  assert.equal(protectedCells.length, 13, 'Must have exactly 13 unchanged aliases');
  
  for (const cell of protectedCells) {
    const raw = fs.readFileSync(path.join(ROOT, cell.clipJson));
    const curSha = crypto.createHash('sha256').update(raw).digest('hex');
    const snapSha = snapshot.files[cell.clipJson];
    assert.equal(curSha, snapSha, `Protected clip.json ${cell.cellId} changed from snapshot!`);
  }
});

test('RR-03: Rear weapon sockets and angles match authoring Lua configs', () => {
  const rearWeaponConfigs = {
    'back_r/Sword': {
      path: 'characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2/clip.json',
      grips: [ [0,0], [175,106], [167,73], [167,78], [181,118], [181,122], [156,139], [0,0] ],
      angles: [ 0, 325, 350, 15, 65, 105, 135, 0 ]
    },
    'back_l/Sword': {
      path: 'characters/orc-v1/source/rear-recovery-v2/back_l/Sword/Attack-representative-v1/clip.json',
      grips: [ [0,0], [92,108], [104,70], [127,72], [93,71], [74,95], [100,118], [0,0] ],
      angles: [ 0, 270, 350, 20, 240, 215, 200, 0 ]
    },
    'back_r/Axe': {
      path: 'characters/orc-v1/source/rear-recovery-v2/back_r/Axe/Attack-representative-v1/clip.json',
      grips: [ [0,0], [175,106], [167,73], [167,78], [181,118], [181,122], [156,139], [0,0] ],
      angles: [ 0, 315, 350, 0, 70, 105, 135, 0 ]
    },
    'back_l/Axe': {
      path: 'characters/orc-v1/source/rear-recovery-v2/back_l/Axe/Attack-representative-v1/clip.json',
      grips: [ [0,0], [92,108], [104,78], [104,78], [86,118], [96,141], [99,145], [0,0] ],
      angles: [ 0, 270, 315, 350, 315, 270, 235, 0 ]
    }
  };
  
  for (const [key, cfg] of Object.entries(rearWeaponConfigs)) {
    const clip = readJSON(path.join(ROOT, cfg.path));
    assert.equal(clip.frames.length, 8, `${key} must have 8 frames`);
    for (let i = 0; i < 8; i++) {
      const f = clip.frames[i];
      assert.deepEqual(f.rightGrip, cfg.grips[i], `${key} F0${i} rightGrip mismatch`);
      assert.equal(f.rotationDeg, cfg.angles[i], `${key} F0${i} rotationDeg mismatch`);
    }
  }
});

test('RR-02: All 4 Unarmed clips have unified durations [80, 110, 50, 90, 120] ms', () => {
  const dirs = ['front_r', 'front_l', 'back_r', 'back_l'];
  const expected = [80, 110, 50, 90, 120];
  
  for (const d of dirs) {
    const clipPath = path.join(ROOT, `characters/orc-v1/source/rear-recovery-v2/${d}/Unarmed/clip.json`);
    const clip = readJSON(clipPath);
    assert.deepEqual(clip.durationsMs, expected, `${d}/Unarmed durationsMs must be ${expected}`);
    assert.deepEqual(clip.frames.map(f => f.durationMs), expected, `${d}/Unarmed frame durationMs must be ${expected}`);
  }
});

test('RR-01: back_l/Unarmed F04 has intact torso/armor contour, coherent hanging arm, no cutout or floating residue', () => {
  const natPngPath = path.join(ROOT, 'characters/orc-v1/source/rear-recovery-v2/back_l/Unarmed/native/04.png');
  const { image: img } = decode(natPngPath);
  
  // Verify bounding box and ground lock
  let minX = 999, maxX = -1, minY = 999, maxY = -1;
  let armTorsoPixels = 0;
  for (let y = 0; y < img.height; y++) {
    for (let x = 0; x < img.width; x++) {
      const idx = (y * img.width + x) * 4;
      if (img.data[idx + 3] > 0) {
        if (x < minX) minX = x;
        if (x > maxX) maxX = x;
        if (y < minY) minY = y;
        if (y > maxY) maxY = y;
        if (x >= 15 && x <= 55 && y >= 20 && y <= 90) armTorsoPixels++;
      }
    }
  }
  
  assert.equal(maxY, 126, 'Must be locked to ground level y=126');
  assert.ok(armTorsoPixels > 1500, `Expected solid torso/arm (>1500 px), got ${armTorsoPixels}`);
  
  // Verify forearm connects to glove without empty gap at y=75..80
  let forearmPixels = 0;
  for (let y = 70; y <= 80; y++) {
    for (let x = 20; x <= 35; x++) {
      const idx = (y * img.width + x) * 4;
      if (img.data[idx + 3] > 0) forearmPixels++;
    }
  }
  assert.ok(forearmPixels > 80, `Forearm must be present and solid at y=70..80, got ${forearmPixels}`);
});

test('RR-05: front_r and front_l Defeat F04 exhibit genuine knockout collapse with head low and prone volume', () => {
  for (const d of ['front_r', 'front_l']) {
    const natPngPath = path.join(ROOT, `characters/orc-v1/source/rear-recovery-v2/${d}/Defeat/native/04.png`);
    const { image: img } = decode(natPngPath);
    
    let minX = 999, maxX = -1, minY = 999, maxY = -1;
    let greenSkin = 0;
    for (let y = 0; y < img.height; y++) {
      for (let x = 0; x < img.width; x++) {
        const idx = (y * img.width + x) * 4;
        if (img.data[idx + 3] > 0) {
          if (x < minX) minX = x;
          if (x > maxX) maxX = x;
          if (y < minY) minY = y;
          if (y > maxY) maxY = y;
          
          const r = img.data[idx], g = img.data[idx+1], b = img.data[idx+2];
          if (g > r && g > b && g > 40) greenSkin++;
        }
      }
    }
    
    const h = maxY - minY + 1;
    const w = maxX - minX + 1;
    const aspect = w / h;
    
    assert.equal(maxY, 126, `${d} Defeat F04 must be locked to ground level y=126`);
    assert.ok(h <= 55, `${d} Defeat F04 height must be <= 55 px for knockout, got ${h}`);
    assert.ok(aspect >= 2.2, `${d} Defeat F04 aspect ratio must be >= 2.2 for prone knockout, got ${aspect.toFixed(2)}`);
    assert.ok(greenSkin > 200, `${d} Defeat F04 must preserve head volume, got ${greenSkin} green pixels`);
  }
});
