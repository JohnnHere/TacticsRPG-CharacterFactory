import fs from 'node:fs';
import path from 'node:path';
import { ROOT, hash } from '../../src/core.mjs';

// Recomputes declared hashes for a cell whose export was regenerated after the
// clip was written. Layout-agnostic on purpose: cells either keep frame PNGs at
// the cell root or under frames/, and guessing the wrong one is how the earlier
// path defects happened. Declared paths are preserved when the file exists.

const targets = process.argv.slice(2);
if (!targets.length) throw new Error('usage: node sync-cell-hashes.mjs <clip.json> [...]');

const absolute = file => path.resolve(ROOT, file);
const digest = file => hash(fs.readFileSync(absolute(file)));

for (const clipPath of targets) {
  const clip = JSON.parse(fs.readFileSync(absolute(clipPath), 'utf8'));
  const dir = path.posix.dirname(clipPath);
  const updated = [];
  const sync = (holder, fileField, hashField) => {
    const file = holder[fileField];
    if (!file || !fs.existsSync(absolute(file))) return;
    const next = digest(file);
    if (holder[hashField] !== next) {
      holder[hashField] = next;
      updated.push(path.posix.basename(file));
    }
  };
  for (const frame of clip.frames) {
    sync(frame, 'png', 'sha256');
    sync(frame, 'nativePng', 'nativeSha256');
    sync(frame, 'nativeCompositePng', 'nativeCompositeSha256');
    for (const layer of Object.values(frame.layers ?? {})) sync(layer, 'png', 'sha256');
  }
  for (const [fileField, hashField] of [
    ['master', 'masterSha256'], ['bodyMaster', 'bodyMasterSha256'],
    ['handMaster', 'handMasterSha256'], ['nativeMaster', 'nativeMasterSha256'],
    ['strip', 'stripSha256'], ['nativeStrip', 'nativeStripSha256'],
    ['compositeStrip', 'compositeStripSha256'], ['nativeCompositeStrip', 'nativeCompositeStripSha256'],
  ]) sync(clip, fileField, hashField);

  fs.writeFileSync(absolute(clipPath), `${JSON.stringify(clip, null, 2)}\n`);
  console.log(`${clipPath}: ${updated.length} hashes resynced (${updated.slice(0, 6).join(', ')}${updated.length > 6 ? '…' : ''})`);
}
