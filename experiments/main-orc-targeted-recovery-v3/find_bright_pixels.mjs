import fs from 'node:fs';
import path from 'node:path';
import { decode } from '../../src/images.mjs';

const ROOT = process.cwd();

function luma(r, g, b) {
  return Math.round(0.299 * r + 0.587 * g + 0.114 * b);
}

function analyzeBrightEdges(clipPathRel) {
  const clipPath = path.resolve(ROOT, clipPathRel);
  const data = JSON.parse(fs.readFileSync(clipPath, 'utf8').replace(/^\uFEFF/, ''));
  const baseDir = path.dirname(clipPath);
  console.log(`\n======================================================`);
  console.log(`ANALYZING BRIGHT EDGES IN: ${clipPathRel}`);
  
  for (let fIdx = 0; fIdx < data.frames.length; fIdx++) {
    const f = data.frames[fIdx];
    const compRel = f.png || f.file;
    const compPath = path.resolve(ROOT, compRel);
    if (!fs.existsSync(compPath)) continue;
    
    const comp = decode(compPath).image;
    const w = comp.width, h = comp.height;
    
    // Check composite outer edge pixels (pixels with alpha > 0 that touch an alpha === 0 pixel in 8-neighborhood)
    const edgeBrights = [];
    for (let y = 0; y < h; y++) {
      for (let x = 0; x < w; x++) {
        const idx = (y * w + x) * 4;
        const a = comp.data[idx + 3];
        if (a === 0) continue;
        
        // check 8-neighborhood
        let isEdge = false;
        for (let dy = -1; dy <= 1; dy++) {
          for (let dx = -1; dx <= 1; dx++) {
            if (dx === 0 && dy === 0) continue;
            const nx = x + dx, ny = y + dy;
            if (nx < 0 || ny < 0 || nx >= w || ny >= h || comp.data[(ny * w + nx) * 4 + 3] === 0) {
              isEdge = true;
              break;
            }
          }
          if (isEdge) break;
        }
        
        if (isEdge) {
          const r = comp.data[idx], g = comp.data[idx + 1], b = comp.data[idx + 2];
          const lum = luma(r, g, b);
          // Highlight/stray bright pixels: lum >= 160 or (r > 180 && g > 180 && b > 180) or pale colors
          if (lum >= 150 || (r > 170 && g > 170 && b > 150)) {
            // Find which layer has this pixel
            let layerOwner = 'unknown';
            if (f.layers) {
              for (const [layerName, layerObj] of Object.entries(f.layers)) {
                const lPath = path.resolve(ROOT, layerObj.png || layerObj.file);
                if (fs.existsSync(lPath)) {
                  const lImg = decode(lPath).image;
                  if (lImg.data[idx + 3] > 0) {
                    const lr = lImg.data[idx], lg = lImg.data[idx+1], lb = lImg.data[idx+2];
                    layerOwner = `${layerName}(${lr},${lg},${lb})`;
                  }
                }
              }
            }
            edgeBrights.push({ x, y, r, g, b, lum, a, layerOwner });
          }
        }
      }
    }
    
    if (edgeBrights.length > 0) {
      console.log(`  Frame ${fIdx} (dur=${f.durationMs}ms): ${edgeBrights.length} bright edge pixels:`);
      for (const p of edgeBrights.slice(0, 15)) {
        console.log(`    at (${p.x},${p.y}): rgba(${p.r},${p.g},${p.b},${p.a}) luma=${p.lum} layer=${p.layerOwner}`);
      }
      if (edgeBrights.length > 15) {
        console.log(`    ... and ${edgeBrights.length - 15} more`);
      }
    } else {
      console.log(`  Frame ${fIdx}: 0 bright edge pixels (clean)`);
    }
  }
}

const armedClips = [
  'characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2/clip.json',
  'characters/orc-v1/source/rear-recovery-v2/back_l/Sword/Attack-representative-v1/clip.json',
  'characters/orc-v1/source/rear-recovery-v2/back_r/Axe/Attack-representative-v1/clip.json',
  'characters/orc-v1/source/rear-recovery-v2/back_l/Axe/Attack-representative-v1/clip.json',
];

for (const c of armedClips) {
  analyzeBrightEdges(c);
}
