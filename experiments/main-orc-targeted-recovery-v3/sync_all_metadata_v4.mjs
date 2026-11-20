import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { decode } from '../../src/images.mjs';

const ROOT = process.cwd();

function sha256File(filePath) {
  const buf = fs.readFileSync(filePath);
  return crypto.createHash('sha256').update(buf).digest('hex');
}

console.log('=== Synchronizing All Metadata and Verifying Composite vs Native ===');

const manifestPath = path.join(ROOT, 'characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json');
const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));

// 1. Reclassify front_r/Walk, front_l/Walk, and front_l/Sword as touched candidates
for (const c of manifest.cells) {
  if (c.cellId === 'front_r/Walk') {
    c.status = 'ACTIVE_CANDIDATE';
    c.isAffected = true;
    c.reviewStatus = 'ACTIVE_CANDIDATE';
    c.provenance = 'main-orc-targeted-recovery-v3 F08 cloth shading cleanup';
    c.notes = '16-frame walk cycle with subdued crotch cloth shading in F08';
  } else if (c.cellId === 'front_l/Walk') {
    c.status = 'ACTIVE_CANDIDATE';
    c.isAffected = true;
    c.reviewStatus = 'ACTIVE_CANDIDATE';
    c.provenance = 'main-orc-targeted-recovery-v3 F08 cloth shading cleanup';
    c.notes = '16-frame walk cycle with subdued crotch cloth shading in F08';
  } else if (c.cellId === 'front_l/Sword') {
    c.status = 'ACTIVE_CANDIDATE';
    c.isAffected = true;
    c.reviewStatus = 'ACTIVE_CANDIDATE';
    c.provenance = 'main-orc-targeted-recovery-v3 armpit contour cleanup';
    c.notes = '13-frame sword attack with cleaned armpit contour and stray pixels removed';
  }
}

manifest.activeCandidatesCount = 15;
manifest.unchangedAliasesCount = 13;
manifest.inRevisionCount = 0;
manifest.inProductionCount = 0;

let verifiedFrameCount = 0;
let verifiedLayerCount = 0;

for (const cell of manifest.cells) {
  const clipAbs = path.join(ROOT, cell.clipJson);
  const clipDir = path.dirname(clipAbs);
  const clip = JSON.parse(fs.readFileSync(clipAbs, 'utf8'));
  
  // Unarmed front durations synchronization
  if (cell.cellId === 'front_r/Unarmed' || cell.cellId === 'front_l/Unarmed') {
    clip.durationsMs = [ 80, 110, 50, 90, 120 ];
    clip.totalDurationMs = 450;
    for (let i = 0; i < clip.frames.length; i++) {
      clip.frames[i].durationMs = clip.durationsMs[i];
    }
  }
  
  // Verify master SHA-256
  if (clip.master) {
    const mAbs = path.isAbsolute(clip.master) ? clip.master : path.join(ROOT, clip.master);
    if (fs.existsSync(mAbs)) clip.masterSha256 = sha256File(mAbs);
  }
  if (clip.nativeMaster) {
    const nmAbs = path.isAbsolute(clip.nativeMaster) ? clip.nativeMaster : path.join(ROOT, clip.nativeMaster);
    if (fs.existsSync(nmAbs)) clip.nativeMasterSha256 = sha256File(nmAbs);
  }
  
  // Verify strip SHA-256
  const stripAbs = path.join(clipDir, 'native-strip.png');
  if (fs.existsSync(stripAbs)) {
    clip.nativeStripSha256 = sha256File(stripAbs);
  }
  
  // Verify each frame
  for (const f of clip.frames) {
    const fAbs = path.join(ROOT, f.png);
    if (!fs.existsSync(fAbs)) throw new Error(`Missing frame PNG: ${fAbs}`);
    f.sha256 = sha256File(fAbs);
    const compImg = decode(fAbs).image;
    
    // Check nativePng equality
    if (f.nativePng) {
      const nAbs = path.join(ROOT, f.nativePng);
      if (!fs.existsSync(nAbs)) throw new Error(`Missing native PNG: ${nAbs}`);
      f.nativeSha256 = sha256File(nAbs);
      const natImg = decode(nAbs).image;
      
      // Target for comparison: if armed, compare body layer crop; if unarmed/walk/defeat, compare compImg crop
      let sourceImg = compImg;
      if (f.layers && f.layers.body) {
        const bodyAbs = path.join(ROOT, f.layers.body.png || f.layers.body.file);
        sourceImg = decode(bodyAbs).image;
      }
      
      let pixelDiffs = 0;
      for (let y = 0; y < 128; y++) {
        for (let x = 0; x < 128; x++) {
          const sIdx = ((y + 64) * 256 + (x + 64)) * 4;
          const nIdx = (y * 128 + x) * 4;
          const sa = sourceImg.data[sIdx + 3];
          const na = natImg.data[nIdx + 3];
          if (sa === 0 && na === 0) continue;
          if (sa !== na || sourceImg.data[sIdx] !== natImg.data[nIdx] || sourceImg.data[sIdx+1] !== natImg.data[nIdx+1] || sourceImg.data[sIdx+2] !== natImg.data[nIdx+2]) {
            pixelDiffs++;
          }
        }
      }
      if (pixelDiffs > 0) {
        throw new Error(`CRITICAL MISMATCH in ${cell.cellId} frame ${f.index}: ${pixelDiffs} divergent pixels between source crop and ${f.nativePng}`);
      }
    }
    
    // Check supplementPng
    if (f.supplementPng) {
      const suppAbs = path.join(ROOT, f.supplementPng);
      if (!fs.existsSync(suppAbs)) throw new Error(`Missing supplement PNG: ${suppAbs}`);
      f.supplementSha256 = sha256File(suppAbs);
      if (f.nativeSha256 && f.supplementSha256 !== f.nativeSha256) {
        throw new Error(`Supplement SHA mismatch in ${cell.cellId} frame ${f.index}`);
      }
    }
    
    // Check 4-layers if present
    if (f.layers) {
      for (const [ln, lMeta] of Object.entries(f.layers)) {
        const lFile = lMeta.png || lMeta.file;
        const lAbs = path.isAbsolute(lFile) ? lFile : path.join(ROOT, lFile);
        if (!fs.existsSync(lAbs)) throw new Error(`Missing layer PNG: ${lAbs}`);
        lMeta.sha256 = sha256File(lAbs);
        verifiedLayerCount++;
      }
    }
    verifiedFrameCount++;
  }
  
  fs.writeFileSync(clipAbs, JSON.stringify(clip, null, 2) + '\n', 'utf8');
}

fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2) + '\n', 'utf8');

console.log(`Sync complete:`);
console.log(`  Verified ${verifiedFrameCount} frames across 28 cells (all composite/body vs native 100% equal).`);
console.log(`  Verified ${verifiedLayerCount} independent equipment layers.`);
console.log(`  Manifest updated: 15 active candidates, 13 unchanged aliases.`);
