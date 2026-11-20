const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

function sha256File(filePath) {
  const buf = fs.readFileSync(filePath);
  return crypto.createHash('sha256').update(buf).digest('hex');
}

const root = path.resolve('.');

function verifyNormalization(name, currentRel, preNormRel, expectedPreHash, expectedPostHash) {
  const currentPath = path.join(root, currentRel);
  const preNormPath = path.join(root, preNormRel);
  
  const currentActualHash = sha256File(currentPath);
  const preNormActualHash = sha256File(preNormPath);
  
  const currentJson = JSON.parse(fs.readFileSync(currentPath, 'utf8'));
  const preNormJson = JSON.parse(fs.readFileSync(preNormPath, 'utf8'));
  
  const res = {
    clip: name,
    preNormHashMatch: preNormActualHash === expectedPreHash,
    preNormActualHash,
    expectedPreHash,
    currentHashMatch: currentActualHash === expectedPostHash,
    currentActualHash,
    expectedPostHash,
    layersRenamedCount: 0,
    layersChecked: 0,
    layersMissingPath: true,
    layersHavePng: true,
    layerFilesExistAndMatchHash: true,
    frameMetadataMatch: true,
    frameHashMismatches: [],
    mastersAndStripsMatch: true,
    mastersMismatches: []
  };
  
  // Verify masters and strips
  const masterKeys = ['master', 'bodyMaster', 'nativeMaster', 'handMaster'];
  const stripKeys = ['strip', 'nativeStrip', 'compositeStrip', 'nativeCompositeStrip'];
  
  for (const k of [...masterKeys, ...stripKeys]) {
    if (!currentJson[k]) continue;
    const curP = currentJson[k];
    const preP = preNormJson[k];
    const curHashDecl = currentJson[k + 'Sha256'];
    const preHashDecl = preNormJson[k + 'Sha256'];
    
    if (curP !== preP || curHashDecl !== preHashDecl) {
      res.mastersAndStripsMatch = false;
      res.mastersMismatches.push(`${k}: path or declared hash mismatch between current and pre-norm`);
    }
    
    const fullOnDisk = path.join(root, curP);
    if (!fs.existsSync(fullOnDisk)) {
      res.mastersAndStripsMatch = false;
      res.mastersMismatches.push(`${k}: file does not exist at ${curP}`);
    } else {
      const diskHash = sha256File(fullOnDisk);
      if (diskHash !== curHashDecl) {
        res.mastersAndStripsMatch = false;
        res.mastersMismatches.push(`${k}: disk hash ${diskHash} !== declared ${curHashDecl}`);
      }
    }
  }
  
  // Verify frames
  if (currentJson.frames.length !== preNormJson.frames.length) {
    res.frameMetadataMatch = false;
    res.frameHashMismatches.push(`Frame length differs: ${currentJson.frames.length} vs ${preNormJson.frames.length}`);
  }
  
  const layerNames = ['weaponBack', 'body', 'weaponFront', 'handFront'];
  
  for (let i = 0; i < currentJson.frames.length; i++) {
    const curF = currentJson.frames[i];
    const preF = preNormJson.frames[i];
    
    if (curF.durationMs !== preF.durationMs ||
        curF.weaponVisible !== preF.weaponVisible ||
        curF.sha256 !== preF.sha256 ||
        curF.nativeSha256 !== preF.nativeSha256) {
      res.frameMetadataMatch = false;
      res.frameHashMismatches.push(`Frame ${i} metadata or composite hash mismatch`);
    }
    
    for (const lName of layerNames) {
      const curL = curF.layers[lName];
      const preL = preF.layers[lName];
      res.layersChecked++;
      
      if (curL.path !== undefined) {
        res.layersMissingPath = false;
      }
      if (typeof curL.png !== 'string') {
        res.layersHavePng = false;
      }
      if (preL.path && curL.png === preL.path) {
        res.layersRenamedCount++;
      }
      if (curL.sha256 !== preL.sha256) {
        res.layerFilesExistAndMatchHash = false;
        res.frameHashMismatches.push(`Frame ${i} layer ${lName} declared sha mismatch`);
      }
      
      const layerFilePath = path.join(root, curL.png);
      if (!fs.existsSync(layerFilePath)) {
        res.layerFilesExistAndMatchHash = false;
        res.frameHashMismatches.push(`Frame ${i} layer ${lName} file missing: ${curL.png}`);
      } else {
        const diskLayerHash = sha256File(layerFilePath);
        if (diskLayerHash !== curL.sha256) {
          res.layerFilesExistAndMatchHash = false;
          res.frameHashMismatches.push(`Frame ${i} layer ${lName} disk hash mismatch: ${diskLayerHash} !== ${curL.sha256}`);
        }
      }
    }
  }
  
  return res;
}

const swordRes = verifyNormalization(
  'back_r/Sword',
  'characters/orc-v1/source/combat-rescue-v5/rear-grip-flash/full-back-r-sword/clip.json',
  'experiments/main-orc-combat-rescue-v5/rear-grip-flash/pre-normalization/full-back-r-sword.clip.json',
  'eb379d1d699ab51203ec633d645a29d9c63e377e36fe8b15b8fda44fc1a9aac6',
  'a63aa1ac4648eba9605fb26720a7b51d9a863539d6d76cc8e79fc3115ff8b739'
);

const axeRes = verifyNormalization(
  'back_l/Axe',
  'characters/orc-v1/source/combat-rescue-v5/rear-grip-flash/full-back-l-axe/clip.json',
  'experiments/main-orc-combat-rescue-v5/rear-grip-flash/pre-normalization/full-back-l-axe.clip.json',
  '9f7d01e726f3f6dc63b24aeb23da97ac9cad29a7fd31572ccdf59a3ee384a0f3',
  'b61b87deed2c547d8d01112b0f30e956f02fee12eff04dab6ba25b833eb7cbf6'
);

console.log(JSON.stringify({ swordRes, axeRes }, null, 2));
