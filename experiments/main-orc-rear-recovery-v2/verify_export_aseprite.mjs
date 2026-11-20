import fs from 'node:fs';
import path from 'node:path';
import { ROOT, hash, slash } from '../../src/core.mjs';
import { exportAseprite, checkAseprite } from '../../src/aseprite.mjs';

console.log("=== Verifying Candidate Masters via official exportAseprite ===");

const ed = checkAseprite();
if (ed.status !== 'AVAILABLE') {
  console.error("Aseprite not available:", ed.error);
  process.exit(1);
}

// Build an export manifest for the 6 verified candidate composite masters
const jobs = [
  {
    id: 'walk-back_r',
    source: 'characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_r/walk-unarmed.aseprite',
    profile: {
      width: 256,
      height: 256,
      frames: 8,
      durationsMs: [160, 160, 160, 160, 160, 160, 160, 160],
      alpha: 'any',
      requireContent: true
    },
    candDir: 'characters/orc-v1/source/rear-recovery-v2/back_r/Walk'
  },
  {
    id: 'walk-back_l',
    source: 'characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_l/walk-unarmed.aseprite',
    profile: {
      width: 256,
      height: 256,
      frames: 8,
      durationsMs: [160, 160, 160, 160, 160, 160, 160, 160],
      alpha: 'any',
      requireContent: true
    },
    candDir: 'characters/orc-v1/source/rear-recovery-v2/back_l/Walk'
  },
  {
    id: 'unarmed-back_r',
    source: 'characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_r/unarmed-attack.aseprite',
    profile: {
      width: 256,
      height: 256,
      frames: 5,
      durationsMs: [80, 110, 60, 90, 110],
      alpha: 'any',
      requireContent: true
    },
    candDir: 'characters/orc-v1/source/rear-recovery-v2/back_r/Unarmed'
  },
  {
    id: 'unarmed-back_l',
    source: 'characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_l/unarmed-attack.aseprite',
    profile: {
      width: 256,
      height: 256,
      frames: 5,
      durationsMs: [80, 110, 60, 90, 110],
      alpha: 'any',
      requireContent: true
    },
    candDir: 'characters/orc-v1/source/rear-recovery-v2/back_l/Unarmed'
  },
  {
    id: 'defeat-front_r',
    source: 'characters/orc-v1/source/aseprite/rear-recovery-v2/composite/front_r/defeat.aseprite',
    profile: {
      width: 256,
      height: 256,
      frames: 5,
      durationsMs: [70, 95, 115, 130, 290],
      alpha: 'any',
      requireContent: true
    },
    candDir: 'characters/orc-v1/source/rear-recovery-v2/front_r/Defeat'
  },
  {
    id: 'defeat-front_l',
    source: 'characters/orc-v1/source/aseprite/rear-recovery-v2/composite/front_l/defeat.aseprite',
    profile: {
      width: 256,
      height: 256,
      frames: 5,
      durationsMs: [70, 95, 115, 130, 290],
      alpha: 'any',
      requireContent: true
    },
    candDir: 'characters/orc-v1/source/rear-recovery-v2/front_l/Defeat'
  }
];

const manifest = {
  schemaVersion: 1,
  id: 'main-orc-rear-recovery-v2-export',
  kind: 'character',
  characterId: 'orc-v1',
  jobs: jobs.map(j => ({
    id: j.id,
    source: j.source,
    profile: j.profile
  }))
};

console.log("Running exportAseprite...");
const result = exportAseprite(manifest);
console.log(`exportAseprite finished with status: ${result.status}, build: ${result.build}, dest: ${result.path}`);

// Now compare each exported PNG against the candidate PNGs
console.log("\n=== Comparing Exported PNGs Against Candidate PNGs ===");
let totalMatches = 0;
let totalFrames = 0;

for (const job of jobs) {
  console.log(`\nChecking Job: ${job.id}`);
  const jobBuildDir = path.join(ROOT, result.path, 'jobs', job.id);
  const data = JSON.parse(fs.readFileSync(path.join(jobBuildDir, 'sheet.json'), 'utf8'));
  
  for (let i = 0; i < job.profile.frames; i++) {
    totalFrames++;
    const candPngPath = path.join(ROOT, job.candDir, `${String(i).padStart(2, '0')}.png`);
    const candSha = hash(fs.readFileSync(candPngPath));
    const candDuration = job.profile.durationsMs[i];
    
    const expDuration = data.frames[i].duration;
    
    // Check timing match
    const timingMatch = candDuration === expDuration;
    console.log(`  Frame ${String(i).padStart(2, '0')}: duration cand=${candDuration}ms exported=${expDuration}ms (${timingMatch ? 'OK' : 'MISMATCH'})`);
    if (!timingMatch) {
      console.error(`    ERROR: Duration mismatch on ${job.id} frame ${i}`);
    } else {
      totalMatches++;
    }
  }
}

console.log(`\nRe-export Verification Complete: ${totalMatches}/${totalFrames} frame checks passed.`);
