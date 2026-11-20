import fs from 'node:fs';
import path from 'node:path';
import { decode } from '../../src/images.mjs';

const ROOT = process.cwd();

function inspectBackLAssets() {
  const pBase = path.resolve(ROOT, 'experiments/main-orc-complete-v1/pixellab-recovery/back_l_base.png');
  const pImpact = path.resolve(ROOT, 'experiments/main-orc-rear-recovery-v2/punch_impact_clean_l.png');
  
  if (fs.existsSync(pBase)) {
    const imB = decode(pBase).image;
    console.log(`back_l_base: size=${imB.width}x${imB.height}`);
  }
  if (fs.existsSync(pImpact)) {
    const imI = decode(pImpact).image;
    console.log(`punch_impact_clean_l: size=${imI.width}x${imI.height}`);
  }
}

inspectBackLAssets();
