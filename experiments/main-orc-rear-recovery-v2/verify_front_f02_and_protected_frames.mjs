// Read-only source proof for the two localized front Unarmed F02 candidates.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { PNG } from 'pngjs';
import { ROOT } from '../../src/core.mjs';
import { inspectAseprite } from '../../src/aseprite.mjs';

const sha = p => crypto.createHash('sha256').update(fs.readFileSync(path.join(ROOT, p))).digest('hex');
const png = p => PNG.sync.read(fs.readFileSync(path.join(ROOT, p)));
const same = (a, b) => a.width === b.width && a.height === b.height && a.data.equals(b.data);
const failures = [], results = [];
const expected = [80, 110, 50, 90, 120];

for (const direction of ['front_r', 'front_l']) {
  const clipPath = `characters/orc-v1/source/rear-recovery-v2/${direction}/Unarmed/clip.json`;
  const clip = JSON.parse(fs.readFileSync(path.join(ROOT, clipPath), 'utf8'));
  if (clip.character !== 'orc-v1' || clip.direction !== direction || clip.state !== 'Unarmed' || clip.id !== 'basic.unarmed') failures.push(`${direction}: clip identity mismatch`);
  if (clip.frameCount !== 5 || clip.totalDurationMs !== 450 || JSON.stringify(clip.durationsMs) !== JSON.stringify(expected)) failures.push(`${direction}: source timing is not original 450ms cadence`);
  if (clip.artisticApproval !== 'PENDING_CREATOR') failures.push(`${direction}: creator approval must remain pending`);
  if (clip.masterSha256 && sha(clip.master) !== clip.masterSha256) failures.push(`${direction}: saved composite master SHA mismatch`);
  if (clip.nativeMasterSha256 && sha(clip.nativeMaster) !== clip.nativeMasterSha256) failures.push(`${direction}: saved native master SHA mismatch`);
  for (const [name, master, size] of [['composite', clip.master, 256], ['native', clip.nativeMaster, 128]]) {
    const info = inspectAseprite(path.join(ROOT, master));
    if (info.width !== size || info.height !== size || info.frames !== 5 || JSON.stringify(info.durationsMs) !== JSON.stringify(expected)) failures.push(`${direction}: saved ${name} master dimensions/frame timing mismatch`);
  }
  const frameResults = [];
  for (let i = 0; i < 5; i++) {
    const f = clip.frames[i], n = String(i).padStart(2, '0');
    if (f.index !== i || f.durationMs !== expected[i]) failures.push(`${direction}/${n}: frame metadata mismatch`);
    if (!fs.existsSync(path.join(ROOT, f.png)) || !fs.existsSync(path.join(ROOT, f.nativePng))) { failures.push(`${direction}/${n}: missing composite/native export`); continue; }
    if (sha(f.png) !== f.sha256) failures.push(`${direction}/${n}: composite SHA mismatch`);
    if (sha(f.nativePng) !== f.nativeSha256) failures.push(`${direction}/${n}: native SHA mismatch`);
    const composite = png(f.png), native = png(f.nativePng);
    if (composite.width !== 256 || composite.height !== 256 || native.width !== 128 || native.height !== 128) failures.push(`${direction}/${n}: dimension mismatch`);
    // Compare the declared native export to the true centered 128x128 body crop.
    const expectedNative = Buffer.alloc(128 * 128 * 4);
    for (let y = 0; y < 128; y++) composite.data.copy(expectedNative, y * 128 * 4, ((y + 64) * 256 + 64) * 4, ((y + 64) * 256 + 192) * 4);
    if (!native.data.equals(expectedNative)) failures.push(`${direction}/${n}: native PNG is not exact center crop of composite`);
    if ([0, 1, 3, 4].includes(i)) {
      const baselinePath = `characters/orc-v1/source/complete-v1/${direction}/Unarmed/${n}.png`;
      if (!same(composite, png(baselinePath))) failures.push(`${direction}/${n}: expected preserved baseline frame differs`);
    } else {
      const baselinePath = `characters/orc-v1/source/complete-v1/${direction}/Unarmed/02.png`;
      if (same(composite, png(baselinePath))) failures.push(`${direction}/02: localized candidate frame was not changed`);
    }
    frameResults.push({ index: i, durationMs: f.durationMs, composite: f.png, sha256: f.sha256, native: f.nativePng, nativeSha256: f.nativeSha256, baselinePreserved: i !== 2 });
  }
  results.push({ direction, clipJson: clipPath, frameCount: clip.frameCount, durationsMs: clip.durationsMs, totalDurationMs: clip.totalDurationMs, frames: frameResults });
}

const report = { status: failures.length ? 'FAIL' : 'PASS', mode: 'READ_ONLY_CHECK', checks: { views: 2, frames: 10, baselineFramesPreserved: 8, localizedF02FramesChanged: 2, originalDurationMs: 450, native128ExactCenterCrop: true }, results, failures };
console.log(JSON.stringify(report, null, 2));
if (failures.length) process.exitCode = 1;
