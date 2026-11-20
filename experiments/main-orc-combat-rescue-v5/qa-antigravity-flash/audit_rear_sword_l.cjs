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
const targetDir = path.join(root, 'characters/orc-v1/source/combat-rescue-v5/rear-grip-flash/full-back-l-sword');
const parentDir = path.join(root, 'characters/orc-v1/source/combat-rescue-v5/body-specialist/final-cycles/repair1/back_l-Sword-full');
const clipPath = path.join(targetDir, 'clip.json');
const clip = JSON.parse(fs.readFileSync(clipPath, 'utf8'));

const results = {
  clipSha256: sha256File(clipPath),
  masterChecks: {},
  frameChecks: [],
  structuralKeys: {},
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

// Check frames
for (let i = 0; i < clip.frameCount; i++) {
  const idxStr = String(i).padStart(2, '0');
  const frameInfo = clip.frames[i];
  
  const compPath = path.join(targetDir, 'frames', `${idxStr}.png`);
  const nativePath = path.join(targetDir, 'native', `${idxStr}.png`);
  const nativeCompPath = path.join(targetDir, 'native-composite', `${idxStr}.png`);
  const wbPath = path.join(targetDir, 'layers', 'weaponBack', `${idxStr}.png`);
  const bPath = path.join(targetDir, 'layers', 'body', `${idxStr}.png`);
  const wfPath = path.join(targetDir, 'layers', 'weaponFront', `${idxStr}.png`);
  const hfPath = path.join(targetDir, 'layers', 'handFront', `${idxStr}.png`);
  
  const compHash = sha256File(compPath);
  const nativeHash = sha256File(nativePath);
  const nativeCompHash = sha256File(nativeCompPath);
  const wbHash = sha256File(wbPath);
  const bHash = sha256File(bPath);
  const wfHash = sha256File(wfPath);
  const hfHash = sha256File(hfPath);
  
  // Verify declared hashes in clip.json
  const declaredCompMatch = compHash === frameInfo.sha256;
  const declaredNativeMatch = nativeHash === frameInfo.nativeSha256;
  const declaredNativeCompMatch = nativeCompHash === frameInfo.nativeCompositeSha256;
  const declaredWbMatch = wbHash === frameInfo.layers.weaponBack.sha256;
  const declaredBMatch = bHash === frameInfo.layers.body.sha256;
  const declaredWfMatch = wfHash === frameInfo.layers.weaponFront.sha256;
  const declaredHfMatch = hfHash === frameInfo.layers.handFront.sha256;
  
  // Body preservation check vs parent repair1 body
  const parentBPath = path.join(parentDir, 'body256', `${idxStr}.png`);
  const parentNativePath = path.join(parentDir, 'native', `${idxStr}.png`);
  const parentBHash = fs.existsSync(parentBPath) ? sha256File(parentBPath) : null;
  const bPng = loadPng(bPath);
  const parentBPng = fs.existsSync(parentBPath) ? loadPng(parentBPath) : null;
  const bodyRgbaComp = parentBPng ? comparePngRgba(bPng, parentBPng) : { match: false, reason: 'parent body missing' };
  
  const nativePng = loadPng(nativePath);
  const parentNativePng = fs.existsSync(parentNativePath) ? loadPng(parentNativePath) : null;
  const nativeRgbaComp = parentNativePng ? comparePngRgba(nativePng, parentNativePng) : { match: false, reason: 'parent native body missing' };
  
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
  // weaponBack -> body -> weaponFront -> handFront
  const step1 = alphaOver(wbPng, bPng);
  const step2 = alphaOver(step1, wfPng);
  const step3 = alphaOver(step2, hfPng);
  const alphaOverComp = comparePngRgba(step3, compPng);
  
  results.frameChecks.push({
    frame: i,
    phase: frameInfo.phase,
    durationMs: frameInfo.durationMs,
    weaponVisible: frameInfo.weaponVisible,
    declaredHashesMatch: declaredCompMatch && declaredNativeMatch && declaredNativeCompMatch && declaredWbMatch && declaredBMatch && declaredWfMatch && declaredHfMatch,
    bodyByteMatch: bHash === parentBHash,
    bodyRgbaMatch: bodyRgbaComp.match,
    bodyDiffPixels: bodyRgbaComp.diffCount || 0,
    nativeRgbaMatch: nativeRgbaComp.match,
    nativeDiffPixels: nativeRgbaComp.diffCount || 0,
    wbPixels: wbCount,
    wfPixels: wfCount,
    hfPixels: hfCount,
    alphaOverMatch: alphaOverComp.match,
    weaponBbox: weaponMaxY >= 0 ? [weaponMinX, weaponMinY, weaponMaxX, weaponMaxY] : null
  });
}

// Check structural keys F03, F04, F07
const expectedKeys = {
  F03: { body256: '5c2f2e1989381a769c4bfd5f2e54d137c8a637b22391f71b8c24707c684bde2c', native128: '4d0063ba3ec21af78fb490ff4f80c48ec71f5663316c9afd6fa60c4689884096' },
  F04: { body256: 'a9a5a860c7b6c7f52445a2d57c26bbaf01eb88cf40a2a52d9bd8a479f3189220', native128: '206a297a862278cc21649f8613199cc304d58ec1b771c97c652b09c57fb40f30' },
  F07: { body256: '3736cb7fab2e4254f6ffa0676f40e99b936a47b10c1e42aa346e46194aa985b2', native128: 'bc3f5c1102377ffeba631dfef93d843bf1c12d431f4b016286c1c2a7bad147f1' }
};

for (const [kName, exp] of Object.entries(expectedKeys)) {
  const idx = parseInt(kName.slice(1), 10);
  const idxStr = String(idx).padStart(2, '0');
  const bPath = path.join(targetDir, 'layers', 'body', `${idxStr}.png`);
  const nativePath = path.join(targetDir, 'native', `${idxStr}.png`);
  const actualBHash = sha256File(bPath);
  const actualNativeHash = sha256File(nativePath);
  results.structuralKeys[kName] = {
    body256Match: actualBHash === exp.body256,
    actualBody256: actualBHash,
    native128Match: actualNativeHash === exp.native128,
    actualNative128: actualNativeHash
  };
}

console.log(JSON.stringify(results, null, 2));
