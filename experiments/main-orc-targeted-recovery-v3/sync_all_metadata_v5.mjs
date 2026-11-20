import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

function sha256File(filePath) {
  if (!fs.existsSync(filePath)) {
    throw new Error(`File not found: ${filePath}`);
  }
  const buf = fs.readFileSync(filePath);
  return crypto.createHash('sha256').update(buf).digest('hex');
}

console.log('=== Synchronizing All Metadata v5 (Fixing RR-01..RR-06) ===');

const manifestPath = 'characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json';
const snapshotPath = 'experiments/main-orc-targeted-recovery-v3/before-snapshot.json';

const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
const snapshot = JSON.parse(fs.readFileSync(snapshotPath, 'utf8'));

// Exact Lua authoring configs for 4 rear attacks
const rearWeaponConfigs = {
  'back_r/Sword': {
    grips: [ [0,0], [175,106], [167,73], [167,78], [181,118], [181,122], [156,139], [0,0] ],
    angles: [ 0, 325, 350, 15, 65, 105, 135, 0 ]
  },
  'back_l/Sword': {
    grips: [ [0,0], [92,108], [104,70], [127,72], [93,71], [74,95], [100,118], [0,0] ],
    angles: [ 0, 270, 350, 20, 240, 215, 200, 0 ]
  },
  'back_r/Axe': {
    grips: [ [0,0], [175,106], [167,73], [167,78], [181,118], [181,122], [156,139], [0,0] ],
    angles: [ 0, 315, 350, 0, 70, 105, 135, 0 ]
  },
  'back_l/Axe': {
    grips: [ [0,0], [92,108], [104,78], [104,78], [86,118], [96,141], [99,145], [0,0] ],
    angles: [ 0, 270, 315, 350, 315, 270, 235, 0 ]
  }
};

// 1. Process the 13 PROTECTED clips: restore original clip.json without nativeStripSha256
let restoredProtected = 0;
const protectedStripHashes = {};

manifest.cells.forEach(cell => {
  if (cell.status === 'UNCHANGED_ALIAS') {
    const raw = fs.readFileSync(cell.clipJson, 'utf8');
    const obj = JSON.parse(raw);
    
    // Save nativeStripSha256 for manifest candidate if present
    if (obj.strip && fs.existsSync(obj.strip)) {
      protectedStripHashes[cell.cellId] = sha256File(obj.strip);
    }
    
    delete obj.nativeStripSha256;
    const restored = JSON.stringify(obj, null, 2) + '\n';
    fs.writeFileSync(cell.clipJson, restored, 'utf8');
    
    const curSha = crypto.createHash('sha256').update(restored).digest('hex');
    const snapSha = snapshot.files[cell.clipJson];
    if (curSha !== snapSha) {
      console.error(`Mismatch restoring protected clip: ${cell.cellId} cur=${curSha} snap=${snapSha}`);
    } else {
      restoredProtected++;
    }
  }
});
console.log(`Restored ${restoredProtected}/13 protected clip.json files byte-identical to before-snapshot.json.`);

// 2. Process the 15 AFFECTED clips
let updatedAffected = 0;

manifest.cells.forEach(cell => {
  if (cell.isAffected) {
    const raw = fs.readFileSync(cell.clipJson, 'utf8');
    const clip = JSON.parse(raw);
    
    // Check if rear weapon sockets/angles need update (RR-03)
    if (rearWeaponConfigs[cell.cellId]) {
      const cfg = rearWeaponConfigs[cell.cellId];
      clip.frames.forEach((f, fi) => {
        f.rightGrip = cfg.grips[fi];
        f.rotationDeg = cfg.angles[fi];
      });
      console.log(`Updated sockets and angles for ${cell.cellId} (F00..F07)`);
    }
    
    // Check if rear Unarmed durations need update (RR-02)
    if (cell.cellId === 'back_r/Unarmed' || cell.cellId === 'back_l/Unarmed') {
      const durs = [80, 110, 50, 90, 120];
      clip.durationsMs = durs;
      clip.frames.forEach((f, fi) => {
        f.durationMs = durs[fi];
      });
      console.log(`Unified durationsMs to [80, 110, 50, 90, 120] for ${cell.cellId}`);
    }
    
    // Recompute ALL top-level hash fields
    if (clip.master) {
      clip.masterSha256 = sha256File(clip.master);
    }
    if (clip.nativeMaster) {
      clip.nativeMasterSha256 = sha256File(clip.nativeMaster);
    }
    if (clip.bodyMaster) {
      clip.bodyMasterSha256 = sha256File(clip.bodyMaster);
    }
    if (clip.handMaster) {
      clip.handMasterSha256 = sha256File(clip.handMaster);
    }
    if (clip.strip) {
      clip.stripSha256 = sha256File(clip.strip);
      clip.nativeStripSha256 = clip.stripSha256;
    }
    
    // Recompute frame hashes
    if (clip.frames) {
      clip.frames.forEach(f => {
        if (f.png) {
          f.sha256 = sha256File(f.png);
        }
        if (f.nativePng) {
          f.nativeSha256 = sha256File(f.nativePng);
        }
        if (f.layers) {
          for (const lObj of Object.values(f.layers)) {
            if (lObj.png) {
              lObj.sha256 = sha256File(lObj.png);
            }
          }
        }
      });
    }
    
    fs.writeFileSync(cell.clipJson, JSON.stringify(clip, null, 2) + '\n', 'utf8');
    updatedAffected++;
  }
});
console.log(`Synchronized all hashes and metadata for ${updatedAffected}/15 affected clips.`);

// 3. Update candidate28manifest.json
manifest.affectedCount = 15;
manifest.unchangedAliasesCount = 13;
manifest.totalClips = 28;

manifest.cells.forEach(cell => {
  const clip = JSON.parse(fs.readFileSync(cell.clipJson, 'utf8'));
  cell.masterSha256 = clip.masterSha256;
  cell.nativeMasterSha256 = clip.nativeMasterSha256;
  cell.bodyMasterSha256 = clip.bodyMasterSha256;
  cell.stripSha256 = clip.stripSha256;
  cell.nativeStripSha256 = clip.nativeStripSha256 || protectedStripHashes[cell.cellId];
  cell.durationsMs = clip.durationsMs;
  cell.frameCount = clip.frames ? clip.frames.length : (clip.durationsMs ? clip.durationsMs.length : undefined);
});

fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2) + '\n', 'utf8');
console.log('Updated candidate28manifest.json successfully.');
