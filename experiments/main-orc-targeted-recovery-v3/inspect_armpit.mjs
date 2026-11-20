import fs from 'node:fs';
import path from 'node:path';
import { decode } from '../../src/images.mjs';

const ROOT = process.cwd();

function inspectArmpitDefect() {
  const dir = path.resolve(ROOT, 'characters/orc-v1/source/complete-v1/front_l/Sword/Attack');
  const clip = JSON.parse(fs.readFileSync(path.join(dir, 'clip.json'), 'utf8').replace(/^\uFEFF/, ''));
  console.log("=== Inspecting front_l/Sword/Attack armpit ===");
  // front_l attacking arm: in front_l (facing SW), attacking arm is right arm or left arm?
  // Let's check layers: body layer and composite
  for (let f = 0; f < clip.frames.length; f++) {
    const frame = clip.frames[f];
    const compP = path.join(dir, `${String(f).padStart(2, '0')}.png`);
    const compImg = decode(compP).image;
    
    // Check body layer if exists
    const bodyP = path.join(dir, 'layers/body', `${String(f).padStart(2, '0')}.png`);
    let bodyImg = fs.existsSync(bodyP) ? decode(bodyP).image : null;
    
    // Look for disconnected pixels, stray pixels, or abrupt holes near armpit (y: 80..130, x: 90..160)
    // Let's check for isolated pixels or transparency defects
    console.log(`Frame ${f}:`);
    // Let's inspect armpit region
    if (bodyImg) {
      // Look for stray pixels or transparency holes near armpit
      // Let's count alpha in armpit box
    }
  }
}

inspectArmpitDefect();
