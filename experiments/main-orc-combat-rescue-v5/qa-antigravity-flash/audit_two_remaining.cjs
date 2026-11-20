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

function auditClip(clipName, targetRel, parentRel) {
  const targetDir = path.join(root, targetRel);
  const parentDir = path.join(root, parentRel);
  const clipPath = path.join(targetDir, 'clip.json');
  const clip = JSON.parse(fs.readFileSync(clipPath, 'utf8'));
  
  const report = {
    clipName,
    clipSha256: sha256File(clipPath),
    totalDurationMs: clip.totalDurationMs,
    masterChecks: {},
    frameChecks: []
  };
  
  // Masters
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
    report.masterChecks[m.name] = {
      exists,
      declared: m.declared,
      actual: actualHash,
      match: actualHash === m.declared
    };
  }
  
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
    
    // Hash declaration matches
    const hashesMatch = (
      compHash === frameInfo.sha256 &&
      nativeHash === frameInfo.nativeSha256 &&
      nativeCompHash === frameInfo.nativeCompositeSha256 &&
      wbHash === frameInfo.layers.weaponBack.sha256 &&
      bHash === frameInfo.layers.body.sha256 &&
      wfHash === frameInfo.layers.weaponFront.sha256 &&
      hfHash === frameInfo.layers.handFront.sha256
    );
    
    // Parent comparison
    const parentBPath = path.join(parentDir, 'body256', `${idxStr}.png`);
    const parentNativePath = path.join(parentDir, 'native', `${idxStr}.png`);
    const parentBHash = fs.existsSync(parentBPath) ? sha256File(parentBPath) : null;
    const bPng = loadPng(bPath);
    const parentBPng = fs.existsSync(parentBPath) ? loadPng(parentBPath) : null;
    const bodyRgbaComp = parentBPng ? comparePngRgba(bPng, parentBPng) : { match: false, reason: 'missing' };
    
    const nativePng = loadPng(nativePath);
    const parentNativePng = fs.existsSync(parentNativePath) ? loadPng(parentNativePath) : null;
    const nativeRgbaComp = parentNativePng ? comparePngRgba(nativePng, parentNativePng) : { match: false, reason: 'missing' };
    
    // Equipment pixel count
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
    
    // Alpha over composition
    const step1 = alphaOver(wbPng, bPng);
    const step2 = alphaOver(step1, wfPng);
    const step3 = alphaOver(step2, hfPng);
    const alphaOverComp = comparePngRgba(step3, compPng);
    
    report.frameChecks.push({
      frame: i,
      phase: frameInfo.phase,
      durationMs: frameInfo.durationMs,
      weaponVisible: frameInfo.weaponVisible,
      hashesMatch,
      bodyByteMatch: bHash === parentBHash,
      bodyDiffPixels: bodyRgbaComp.diffCount || 0,
      nativeDiffPixels: nativeRgbaComp.diffCount || 0,
      wbPixels: wbCount,
      wfPixels: wfCount,
      hfPixels: hfCount,
      alphaOverMatch: alphaOverComp.match,
      weaponBbox: weaponMaxY >= 0 ? [weaponMinX, weaponMinY, weaponMaxX, weaponMaxY] : null
    });
  }
  return report;
}

const swordAudit = auditClip(
  'back_r/Sword',
  'characters/orc-v1/source/combat-rescue-v5/rear-grip-flash/full-back-r-sword',
  'characters/orc-v1/source/combat-rescue-v5/body-specialist/glm-fixes/back_r-Sword-full'
);

const axeAudit = auditClip(
  'back_l/Axe',
  'characters/orc-v1/source/combat-rescue-v5/rear-grip-flash/full-back-l-axe',
  'characters/orc-v1/source/combat-rescue-v5/body-specialist/glm-fixes/back_l-Axe-full'
);

console.log(JSON.stringify({ swordAudit, axeAudit }, null, 2));
