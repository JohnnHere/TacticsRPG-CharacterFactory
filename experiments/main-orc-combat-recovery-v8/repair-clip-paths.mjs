import fs from 'node:fs';
import path from 'node:path';
import { ROOT, hash } from '../../src/core.mjs';

// Repairs declared paths/hashes so a clip references ITS OWN exported files.
// Third occurrence of this defect class (V6 front subpath, V8 frontal -> V6 paths).
// Only metadata is rewritten; no pixel, timing or layer content is touched.

const targets = [
  'characters/orc-v1/source/combat-recovery-v8/frontal/front_r-Sword/clip.json',
  'characters/orc-v1/source/combat-recovery-v8/frontal/front_l-Sword/clip.json',
  'characters/orc-v1/source/combat-recovery-v8/frontal-armpit/front_l-sword/clip.json',
  'characters/orc-v1/source/combat-recovery-v8/rear-fix/back_r-sword/clip.json',
];
const absolute = file => path.resolve(ROOT, file);
const digest = file => hash(fs.readFileSync(absolute(file)));

for (const clipPath of targets) {
  const dir = path.posix.dirname(clipPath);
  const clip = JSON.parse(fs.readFileSync(absolute(clipPath), 'utf8'));
  const fixed = [];
  for (const frame of clip.frames) {
    const idx = String(frame.index).padStart(2, '0');
    const framePng = `${dir}/${idx}.png`;
    if (frame.png !== framePng) fixed.push(`frame${idx}.png`);
    frame.png = framePng;
    frame.sha256 = digest(framePng);

    const nativePng = `${dir}/native/${idx}.png`;
    if (fs.existsSync(absolute(nativePng))) {
      if (frame.nativePng !== nativePng) fixed.push(`native/${idx}.png`);
      frame.nativePng = nativePng;
      frame.nativeSha256 = digest(nativePng);
    }
    const nativeComposite = `${dir}/native-composite/${idx}.png`;
    if (frame.nativeCompositePng && fs.existsSync(absolute(nativeComposite))) {
      frame.nativeCompositePng = nativeComposite;
      frame.nativeCompositeSha256 = digest(nativeComposite);
    }
    for (const [name, layer] of Object.entries(frame.layers ?? {})) {
      const layerPng = `${dir}/layers/${name}/${idx}.png`;
      if (!fs.existsSync(absolute(layerPng))) throw new Error(`missing layer file ${layerPng}`);
      const declared = layer.png ?? layer.path;
      if (declared !== layerPng) fixed.push(`layers/${name}/${idx}.png`);
      layer.png = layerPng;
      delete layer.path;
      layer.sha256 = digest(layerPng);
    }
  }
  for (const [fileField, hashField] of [
    ['master', 'masterSha256'], ['bodyMaster', 'bodyMasterSha256'],
    ['handMaster', 'handMasterSha256'], ['nativeMaster', 'nativeMasterSha256'],
    ['strip', 'stripSha256'], ['nativeStrip', 'nativeStripSha256'],
    ['compositeStrip', 'compositeStripSha256'], ['nativeCompositeStrip', 'nativeCompositeStripSha256'],
  ]) {
    if (!clip[fileField]) continue;
    if (clip[fileField].startsWith('characters/') && !fs.existsSync(absolute(clip[fileField]))) {
      const local = `${dir}/${path.posix.basename(clip[fileField])}`;
      const localSource = `${dir}/source/${path.posix.basename(clip[fileField])}`;
      if (fs.existsSync(absolute(local))) clip[fileField] = local;
      else if (fs.existsSync(absolute(localSource))) clip[fileField] = localSource;
      else throw new Error(`cannot resolve ${fileField}: ${clip[fileField]}`);
    }
    if (clip[hashField]) clip[hashField] = digest(clip[fileField]);
  }
  fs.writeFileSync(absolute(clipPath), `${JSON.stringify(clip, null, 2)}\n`);
  console.log(`${clipPath}\n  repointed entries: ${fixed.length}\n  clip sha256: ${digest(clipPath)}`);
}
