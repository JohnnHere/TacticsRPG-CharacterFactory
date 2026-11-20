const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { PNG } = require('pngjs');

function sha256File(filePath) {
  const buf = fs.readFileSync(filePath);
  return crypto.createHash('sha256').update(buf).digest('hex');
}

function loadPng(filePath) {
  const buf = fs.readFileSync(filePath);
  return PNG.sync.read(buf);
}

function comparePngRgba(png1, png2) {
  if (png1.width !== png2.width || png1.height !== png2.height) {
    return { match: false, reason: `dimensions mismatch: ${png1.width}x${png1.height} vs ${png2.width}x${png2.height}` };
  }
  let diffCount = 0;
  for (let i = 0; i < png1.data.length; i += 4) {
    const r1 = png1.data[i], g1 = png1.data[i+1], b1 = png1.data[i+2], a1 = png1.data[i+3];
    const r2 = png2.data[i], g2 = png2.data[i+1], b2 = png2.data[i+2], a2 = png2.data[i+3];
    if (a1 === 0 && a2 === 0) continue;
    if (r1 !== r2 || g1 !== g2 || b1 !== b2 || a1 !== a2) {
      diffCount++;
    }
  }
  return { match: diffCount === 0, diffCount };
}

function alphaOver(src, dst) {
  // dst OVER src
  const out = new PNG({ width: src.width, height: src.height });
  for (let y = 0; y < src.height; y++) {
    for (let x = 0; x < src.width; x++) {
      const idx = (src.width * y + x) << 2;
      const sr = src.data[idx], sg = src.data[idx+1], sb = src.data[idx+2], sa = src.data[idx+3] / 255;
      const dr = dst.data[idx], dg = dst.data[idx+1], db = dst.data[idx+2], da = dst.data[idx+3] / 255;
      
      const outA = da + sa * (1 - da);
      if (outA === 0) {
        out.data[idx] = 0;
        out.data[idx+1] = 0;
        out.data[idx+2] = 0;
        out.data[idx+3] = 0;
      } else {
        out.data[idx] = Math.round((dr * da + sr * sa * (1 - da)) / outA);
        out.data[idx+1] = Math.round((dg * da + sg * sa * (1 - da)) / outA);
        out.data[idx+2] = Math.round((db * da + sb * sa * (1 - da)) / outA);
        out.data[idx+3] = Math.round(outA * 255);
      }
    }
  }
  return out;
}

const root = path.resolve('.');
const targetDir = path.join(root, 'characters/orc-v1/source/combat-rescue-v5/grip-specialist/full-front-r-sword');
const parentDir = path.join(root, 'characters/orc-v1/source/combat-rescue-v5/combat/qa5-repair1/front_r/Sword');
const clipPath = path.join(targetDir, 'clip.json');
const clip = JSON.parse(fs.readFileSync(clipPath, 'utf8'));

const results = {
  clipSha256: sha256File(clipPath),
  masterChecks: {},
  frameChecks: [],
  keyframeChecks: {},
  bodyPreservation: [],
  groundContact: []
};

// Check masters
const masters = [
  { name: 'composite', path: clip.master, declared: clip.masterSha256 },
  { name: 'body', path: clip.bodyMaster, declared: clip.bodyMasterSha256 },
  { name: 'native', path: clip.nativeMaster, declared: clip.nativeMasterSha256 },
  { name: 'hand', path: clip.handMaster, declared: clip.handMasterSha256 }
];

for (const m of masters) {
  const fullP = path.join(root, m.path);
  const exists = fs.existsSync(fullP);
  const actualHash = exists ? sha256File(fullP) : null;
  results.masterChecks[m.name] = {
    exists,
    declared: m.declared,
    actual: actualHash,
    match: actualHash === m.declared
  };
}

// Check keyframes F02, F06, F08
const keys = [
  { idx: 2, name: 'F02', dir: 'characters/orc-v1/source/combat-rescue-v5/grip-specialist/F02' },
  { idx: 6, name: 'F06', dir: 'characters/orc-v1/source/combat-rescue-v5/grip-specialist/F06' },
  { idx: 8, name: 'F08', dir: 'characters/orc-v1/source/combat-rescue-v5/grip-specialist/F08' }
];

for (const k of keys) {
  const kDir = path.join(root, k.dir);
  const idxStr = String(k.idx).padStart(2, '0');
  const actualComposite = path.join(targetDir, `${idxStr}.png`);
  
  // Check layers
  const layers = ['weaponBack', 'body', 'weaponFront', 'handFront'];
  const layerMatches = {};
  for (const l of layers) {
    const actL = path.join(targetDir, 'layers', l, `${idxStr}.png`);
    const expL = path.join(kDir, 'layers', `${l}.png`);
    const actHash = fs.existsSync(actL) ? sha256File(actL) : null;
    const expHash = fs.existsSync(expL) ? sha256File(expL) : null;
    layerMatches[l] = {
      actualHash: actHash,
      expectedHash: expHash,
      match: actHash === expHash
    };
  }
  
  results.keyframeChecks[k.name] = {
    layerMatches
  };
}

// Check frames
for (let i = 0; i < clip.frameCount; i++) {
  const idxStr = String(i).padStart(2, '0');
  const frameInfo = clip.frames[i];
  
  const compPath = path.join(targetDir, `${idxStr}.png`);
  const nativePath = path.join(targetDir, 'native', `${idxStr}.png`);
  const wbPath = path.join(targetDir, 'layers', 'weaponBack', `${idxStr}.png`);
  const bPath = path.join(targetDir, 'layers', 'body', `${idxStr}.png`);
  const wfPath = path.join(targetDir, 'layers', 'weaponFront', `${idxStr}.png`);
  const hfPath = path.join(targetDir, 'layers', 'handFront', `${idxStr}.png`);
  
  const compHash = sha256File(compPath);
  const nativeHash = sha256File(nativePath);
  const wbHash = sha256File(wbPath);
  const bHash = sha256File(bPath);
  const wfHash = sha256File(wfPath);
  const hfHash = sha256File(hfPath);
  
  // Verify declared hashes
  const declaredCompMatch = compHash === frameInfo.sha256;
  const declaredNativeMatch = nativeHash === frameInfo.nativeSha256;
  const declaredWbMatch = wbHash === frameInfo.layers.weaponBack.sha256;
  const declaredBMatch = bHash === frameInfo.layers.body.sha256;
  const declaredWfMatch = wfHash === frameInfo.layers.weaponFront.sha256;
  const declaredHfMatch = hfHash === frameInfo.layers.handFront.sha256;
  
  // Body preservation check vs parent
  const parentBPath = path.join(parentDir, 'layers', 'body', `${idxStr}.png`);
  const parentBHash = fs.existsSync(parentBPath) ? sha256File(parentBPath) : null;
  const bPng = loadPng(bPath);
  const parentBPng = fs.existsSync(parentBPath) ? loadPng(parentBPath) : null;
  const bodyRgbaComp = parentBPng ? comparePngRgba(bPng, parentBPng) : { match: false, reason: 'parent body missing' };
  
  // Non-zero pixels in equipment layers
  const wbPng = loadPng(wbPath);
  const wfPng = loadPng(wfPath);
  const hfPng = loadPng(hfPath);
  const compPng = loadPng(compPath);
  
  let wbCount = 0, wfCount = 0, hfCount = 0;
  let weaponMinY = 999, weaponMaxY = -1;
  let weaponMinX = 999, weaponMaxX = -1;
  
  for (let p = 0; p < wbPng.data.length; p += 4) {
    const x = (p / 4) % wbPng.width;
    const y = Math.floor((p / 4) / wbPng.width);
    if (wbPng.data[p+3] > 0) {
      wbCount++;
      if (y < weaponMinY) weaponMinY = y;
      if (y > weaponMaxY) weaponMaxY = y;
      if (x < weaponMinX) weaponMinX = x;
      if (x > weaponMaxX) weaponMaxX = x;
    }
    if (wfPng.data[p+3] > 0) {
      wfCount++;
      if (y < weaponMinY) weaponMinY = y;
      if (y > weaponMaxY) weaponMaxY = y;
      if (x < weaponMinX) weaponMinX = x;
      if (x > weaponMaxX) weaponMaxX = x;
    }
    if (hfPng.data[p+3] > 0) {
      hfCount++;
    }
  }
  
  // Check alpha over composition
  // Layer order: weaponBack -> body -> weaponFront -> handFront
  // step 1: body OVER weaponBack
  const step1 = alphaOver(wbPng, bPng);
  // step 2: weaponFront OVER step1
  const step2 = alphaOver(step1, wfPng);
  // step 3: handFront OVER step2
  const step3 = alphaOver(step2, hfPng);
  const alphaOverComp = comparePngRgba(step3, compPng);
  
  results.frameChecks.push({
    frame: i,
    phase: frameInfo.phase,
    durationMs: frameInfo.durationMs,
    weaponVisible: frameInfo.weaponVisible,
    declaredHashesMatch: declaredCompMatch && declaredNativeMatch && declaredWbMatch && declaredBMatch && declaredWfMatch && declaredHfMatch,
    bodyRgbaMatch: bodyRgbaComp.match,
    bodyDiffPixels: bodyRgbaComp.diffCount || 0,
    wbPixels: wbCount,
    wfPixels: wfCount,
    hfPixels: hfCount,
    alphaOverMatch: alphaOverComp.match,
    weaponBbox: weaponMaxY >= 0 ? [weaponMinX, weaponMinY, weaponMaxX, weaponMaxY] : null
  });
}

console.log(JSON.stringify(results, null, 2));
