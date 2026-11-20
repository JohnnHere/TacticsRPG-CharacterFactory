import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const ROOT = process.cwd();
const sha = (p) => {
  const abs = path.resolve(ROOT, p);
  if (!fs.existsSync(abs)) return null;
  return crypto.createHash('sha256').update(fs.readFileSync(abs)).digest('hex');
};

console.log("=== Synchronizing Clip Metadata and Hashes ===");

// 1. Armed rear clips
const armedClips = [
  {
    path: 'characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2/clip.json',
    grips: [[0,0], [170,104], [166,74], [164,80], [180,94], [180,120], [168,126], [0,0]],
    angles: [0, 325, 350, 15, 60, 100, 135, 0],
    durations: [90, 80, 90, 80, 100, 80, 100, 110]
  },
  {
    path: 'characters/orc-v1/source/rear-recovery-v2/back_l/Sword/Attack-representative-v1/clip.json',
    grips: [[0,0], [92,106], [100,72], [112,70], [88,88], [76,108], [96,120], [0,0]],
    angles: [0, 325, 350, 15, 60, 100, 135, 0],
    durations: [90, 80, 90, 80, 100, 80, 100, 110]
  },
  {
    path: 'characters/orc-v1/source/rear-recovery-v2/back_r/Axe/Attack-representative-v1/clip.json',
    grips: [[0,0], [168,100], [166,72], [166,76], [174,112], [162,120], [154,136], [0,0]],
    angles: [0, 315, 345, 15, 65, 110, 140, 0],
    durations: [90, 80, 90, 80, 100, 80, 100, 110]
  },
  {
    path: 'characters/orc-v1/source/rear-recovery-v2/back_l/Axe/Attack-representative-v1/clip.json',
    grips: [[0,0], [92,106], [100,72], [104,74], [86,112], [92,130], [98,142], [0,0]],
    angles: [0, 315, 345, 15, 65, 110, 140, 0],
    durations: [90, 80, 90, 80, 100, 80, 100, 110]
  }
];

for (const entry of armedClips) {
  const clipPath = path.resolve(ROOT, entry.path);
  const clip = JSON.parse(fs.readFileSync(clipPath, 'utf8').replace(/^\uFEFF/, ''));
  clip.masterSha256 = sha(clip.master);
  if (clip.bodyMaster) clip.bodyMasterSha256 = sha(clip.bodyMaster);
  if (clip.handMaster) clip.handMasterSha256 = sha(clip.handMaster);
  if (clip.nativeMaster) clip.nativeMasterSha256 = sha(clip.nativeMaster);
  if (clip.strip) clip.stripSha256 = sha(clip.strip);
  
  const baseDir = path.dirname(clipPath);
  for (let i = 0; i < clip.frames.length; i++) {
    const f = clip.frames[i];
    f.rightGrip = entry.grips[i];
    f.rotationDeg = entry.angles[i];
    f.durationMs = entry.durations[i];
    f.sha256 = sha(f.png || f.file);
    if (f.nativePng) f.nativeSha256 = sha(f.nativePng);
    if (f.layers) {
      for (const [name, layer] of Object.entries(f.layers)) {
        layer.sha256 = sha(layer.png || layer.file);
      }
    }
  }
  fs.writeFileSync(clipPath, JSON.stringify(clip, null, 2) + '\n', 'utf8');
  console.log(`Updated armed clip: ${entry.path}`);
}

// 2. Unarmed and Walk and Defeat clips
const simpleClips = [
  'characters/orc-v1/source/rear-recovery-v2/front_r/Unarmed/clip.json',
  'characters/orc-v1/source/rear-recovery-v2/front_l/Unarmed/clip.json',
  'characters/orc-v1/source/rear-recovery-v2/back_r/Unarmed/clip.json',
  'characters/orc-v1/source/rear-recovery-v2/back_l/Unarmed/clip.json',
  'characters/orc-v1/source/rear-recovery-v2/front_r/Defeat/clip.json',
  'characters/orc-v1/source/rear-recovery-v2/front_l/Defeat/clip.json',
  'characters/orc-v1/source/rear-recovery-v2/back_r/Walk/clip.json',
  'characters/orc-v1/source/rear-recovery-v2/back_l/Walk/clip.json',
  'characters/orc-v1/source/complete-v1/front_l/Sword/Attack/clip.json',
  'characters/orc-v1/source/complete-v1/front_r/Walk/clip.json',
  'characters/orc-v1/source/complete-v1/front_l/Walk/clip.json',
];

for (const p of simpleClips) {
  const clipPath = path.resolve(ROOT, p);
  if (!fs.existsSync(clipPath)) continue;
  const clip = JSON.parse(fs.readFileSync(clipPath, 'utf8').replace(/^\uFEFF/, ''));
  if (clip.master) clip.masterSha256 = sha(clip.master);
  if (clip.bodyMaster) clip.bodyMasterSha256 = sha(clip.bodyMaster);
  if (clip.handMaster) clip.handMasterSha256 = sha(clip.handMaster);
  if (clip.nativeMaster) clip.nativeMasterSha256 = sha(clip.nativeMaster);
  if (clip.strip) clip.stripSha256 = sha(clip.strip);
  
  if (clip.frames) {
    for (let i = 0; i < clip.frames.length; i++) {
      const f = clip.frames[i];
      f.sha256 = sha(f.png || f.file);
      if (f.nativePng) f.nativeSha256 = sha(f.nativePng);
      if (f.layers) {
        if (Array.isArray(f.layers)) {
          for (const l of f.layers) l.sha256 = sha(path.resolve(path.dirname(clipPath), l.file || l.png));
        } else {
          for (const [name, l] of Object.entries(f.layers)) l.sha256 = sha(l.png || l.file);
        }
      }
    }
  }
  fs.writeFileSync(clipPath, JSON.stringify(clip, null, 2) + '\n', 'utf8');
  console.log(`Updated simple clip: ${p}`);
}

// 3. Update candidate28manifest.json notes and statuses
const manifestPath = path.resolve(ROOT, 'characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json');
const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8').replace(/^\uFEFF/, ''));
manifest.revision = 'main-orc-targeted-recovery-v3';

for (const cell of manifest.cells) {
  if (cell.cellId === 'front_r/Defeat' || cell.cellId === 'front_l/Defeat') {
    cell.status = 'ACTIVE_CANDIDATE';
    cell.reviewStatus = 'ACTIVE_CANDIDATE';
    cell.notes = '5-frame defeat sequence; terminal stage 04 replaced with incapacitated ground collapse retaining volume (700ms)';
  } else if (cell.cellId === 'front_r/Unarmed' || cell.cellId === 'front_l/Unarmed') {
    cell.status = 'ACTIVE_CANDIDATE';
    cell.reviewStatus = 'ACTIVE_CANDIDATE';
    cell.notes = '5-frame unarmed strike with opposite arm continuous throughout punch (450ms)';
  } else if (cell.cellId === 'back_r/Unarmed') {
    cell.status = 'ACTIVE_CANDIDATE';
    cell.reviewStatus = 'ACTIVE_CANDIDATE';
    cell.notes = '5-frame heavy gauntlet strike reaching x=186 with smooth follow-through recoil in F03 (450ms)';
  } else if (cell.cellId === 'back_l/Unarmed') {
    cell.status = 'ACTIVE_CANDIDATE';
    cell.reviewStatus = 'ACTIVE_CANDIDATE';
    cell.notes = '5-frame NW heavy gauntlet strike reaching x=70 built with authentic NW rear body frames (450ms)';
  } else if (cell.cellId === 'back_r/Walk' || cell.cellId === 'back_l/Walk') {
    cell.status = 'ACTIVE_CANDIDATE';
    cell.reviewStatus = 'ACTIVE_CANDIDATE';
    cell.notes = 'Method-02 temporal 8-frame cycle (160ms/frame, 1280ms total) with stabilized left arm contour and ground registration';
  } else if (cell.cellId === 'back_r/Sword') {
    cell.status = 'ACTIVE_CANDIDATE';
    cell.reviewStatus = 'ACTIVE_CANDIDATE';
    cell.notes = 'Corrected 8-pose representative cycle with natural slashing trajectory, authentic curled glove wrapping handle, zero bright edge artifacts';
  } else if (cell.cellId === 'back_l/Sword') {
    cell.status = 'ACTIVE_CANDIDATE';
    cell.reviewStatus = 'ACTIVE_CANDIDATE';
    cell.notes = 'Corrected 8-pose NW representative cycle with natural slashing arc, authentic curled glove wrapping handle, zero bright edge artifacts';
  } else if (cell.cellId === 'back_r/Axe') {
    cell.status = 'ACTIVE_CANDIDATE';
    cell.reviewStatus = 'ACTIVE_CANDIDATE';
    cell.notes = 'Corrected 8-pose representative overhead chopping cycle, authentic curled glove wrapping handle, zero bright edge artifacts';
  } else if (cell.cellId === 'back_l/Axe') {
    cell.status = 'ACTIVE_CANDIDATE';
    cell.reviewStatus = 'ACTIVE_CANDIDATE';
    cell.notes = 'Corrected 8-pose NW representative overhead chopping cycle, authentic curled glove wrapping handle, zero bright edge artifacts';
  }
}

manifest.activeCandidatesCount = 12;
manifest.unchangedAliasesCount = 16;
manifest.inRevisionCount = 0;
manifest.inProductionCount = 0;
manifest.totalClips = 28;

fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2) + '\n', 'utf8');
console.log(`Updated candidate28manifest.json successfully.`);
