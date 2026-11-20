import fs from 'node:fs';
import path from 'node:path';
import { decode } from '../../src/images.mjs';

const ROOT = process.cwd();

function analyzeClip(clipJsonPath) {
  const clipPath = path.resolve(ROOT, clipJsonPath);
  if (!fs.existsSync(clipPath)) {
    console.log(`NOT FOUND: ${clipJsonPath}`);
    return;
  }
  const data = JSON.parse(fs.readFileSync(clipPath, 'utf8').replace(/^\uFEFF/, ''));
  const baseDir = path.dirname(clipPath);
  const frames = data.frames || [];
  console.log(`\n=== CLIP: ${clipJsonPath} (frames=${frames.length}) ===`);
  
  for (let idx = 0; idx < frames.length; idx++) {
    const f = frames[idx];
    const compRel = f.png || f.file;
    const compPath = compRel ? path.resolve(ROOT, compRel) : null;
    
    let compBbox = null;
    let compDecoded = null;
    if (compPath && fs.existsSync(compPath)) {
      compDecoded = decode(compPath);
      compBbox = getBbox(compDecoded.image);
    }
    
    let bodyBbox = null;
    let handBbox = null;
    let weaponBbox = null;

    if (f.layers) {
      if (Array.isArray(f.layers)) {
        for (const l of f.layers) {
          const lPath = path.resolve(baseDir, l.file || l.png);
          if (fs.existsSync(lPath)) {
            const dec = decode(lPath);
            const bb = getBbox(dec.image);
            if (l.name === 'body') bodyBbox = bb;
            else if (l.name === 'handFront') handBbox = bb;
            else if (l.name === 'weaponFront' || l.name === 'weaponBack') {
              if (bb) weaponBbox = bb;
            }
          }
        }
      } else if (typeof f.layers === 'object') {
        for (const [name, l] of Object.entries(f.layers)) {
          const lRel = l.png || l.file;
          const lPath = lRel ? path.resolve(ROOT, lRel) : null;
          if (lPath && fs.existsSync(lPath)) {
            const dec = decode(lPath);
            const bb = getBbox(dec.image);
            if (name === 'body') bodyBbox = bb;
            else if (name === 'handFront') handBbox = bb;
            else if (name === 'weaponFront' || name === 'weaponBack') {
              if (bb) weaponBbox = bb;
            }
          }
        }
      }
    }
    
    const dur = f.durationMs || f.duration;
    console.log(`  Frame ${String(idx).padStart(2, '0')}: dur=${dur}ms | comp=${fmtBbox(compBbox)} | body=${fmtBbox(bodyBbox)} | hand=${fmtBbox(handBbox)} | weapon=${fmtBbox(weaponBbox)}`);
  }
}

function getBbox(img) {
  let minX = img.width, minY = img.height, maxX = -1, maxY = -1;
  for (let y = 0; y < img.height; y++) {
    for (let x = 0; x < img.width; x++) {
      const alpha = img.data[(y * img.width + x) * 4 + 3];
      if (alpha > 0) {
        if (x < minX) minX = x;
        if (x > maxX) maxX = x;
        if (y < minY) minY = y;
        if (y > maxY) maxY = y;
      }
    }
  }
  if (maxX < minX || maxY < minY) return null;
  return [minX, minY, maxX - minX + 1, maxY - minY + 1];
}

function fmtBbox(b) {
  if (!b) return 'none';
  return `[${b[0]},${b[1]} ${b[2]}x${b[3]}]`;
}

const clipsToCheck = [
  'characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2/clip.json',
  'characters/orc-v1/source/rear-recovery-v2/back_l/Sword/Attack-representative-v1/clip.json',
  'characters/orc-v1/source/rear-recovery-v2/back_r/Axe/Attack-representative-v1/clip.json',
  'characters/orc-v1/source/rear-recovery-v2/back_l/Axe/Attack-representative-v1/clip.json',
  'characters/orc-v1/source/rear-recovery-v2/back_l/Unarmed/clip.json',
  'characters/orc-v1/source/rear-recovery-v2/back_r/Unarmed/clip.json',
  'characters/orc-v1/source/rear-recovery-v2/front_r/Unarmed/clip.json',
  'characters/orc-v1/source/rear-recovery-v2/front_l/Unarmed/clip.json',
  'characters/orc-v1/source/rear-recovery-v2/back_r/Walk/clip.json',
  'characters/orc-v1/source/rear-recovery-v2/back_l/Walk/clip.json',
  'characters/orc-v1/source/rear-recovery-v2/front_r/Defeat/clip.json',
  'characters/orc-v1/source/rear-recovery-v2/front_l/Defeat/clip.json',
  'characters/orc-v1/source/complete-v1/front_l/Sword/Attack/clip.json',
  'characters/orc-v1/source/complete-v1/front_r/Walk/clip.json',
  'characters/orc-v1/source/complete-v1/front_l/Walk/clip.json',
];

for (const c of clipsToCheck) {
  analyzeClip(c);
}
