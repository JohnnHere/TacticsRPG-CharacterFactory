// Read-only validation for editable-source metadata and self-contained native exports.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { PNG } from 'pngjs';
import { ROOT } from '../../src/core.mjs';
import { decode } from '../../src/images.mjs';
import { inspectAseprite } from '../../src/aseprite.mjs';

const read = p => JSON.parse(fs.readFileSync(path.join(ROOT, p), 'utf8'));
const sha = p => crypto.createHash('sha256').update(fs.readFileSync(path.join(ROOT, p))).digest('hex');
const same = (a, b) => a.width === b.width && a.height === b.height && a.data.equals(b.data);
const proofPath = 'experiments/main-orc-rear-recovery-v2/four-early-clips-source-metadata-verification.json';
const proof = read(proofPath), failures = [], results = [];
if (proof.status !== 'PASS' || proof.checks?.clips !== 4 || proof.checks?.nativeFrames !== 20) failures.push('native export proof report missing or incomplete');

for (const row of proof.results ?? []) {
  const clip = read(row.clipPath), nativeDir = `characters/orc-v1/source/rear-recovery-v2/${row.direction}/${row.action}/native`;
  if (clip.master !== row.master || clip.nativeMaster !== row.nativeMaster) failures.push(`${row.direction}/${row.action}: metadata master paths differ from proof`);
  if (sha(clip.master) !== clip.masterSha256 || clip.masterSha256 !== row.masterSha256) failures.push(`${row.direction}/${row.action}: composite master SHA mismatch`);
  if (sha(clip.nativeMaster) !== clip.nativeMasterSha256 || clip.nativeMasterSha256 !== row.nativeMasterSha256) failures.push(`${row.direction}/${row.action}: native master SHA mismatch`);
  if (!clip.frameCount || clip.frameCount !== clip.totalFrames || clip.frames.length !== clip.frameCount) failures.push(`${row.direction}/${row.action}: frame count alias mismatch`);
  if (sha(clip.strip) !== clip.stripSha256) failures.push(`${row.direction}/${row.action}: strip SHA mismatch`);
  const durations = clip.frames.map(f => f.durationMs), compositeInfo = inspectAseprite(path.join(ROOT, clip.master)), nativeInfo = inspectAseprite(path.join(ROOT, clip.nativeMaster));
  if (compositeInfo.width !== 256 || compositeInfo.height !== 256 || nativeInfo.width !== 128 || nativeInfo.height !== 128) failures.push(`${row.direction}/${row.action}: saved master dimensions mismatch`);
  if (compositeInfo.frames !== clip.frameCount || nativeInfo.frames !== clip.frameCount || JSON.stringify(compositeInfo.durationsMs) !== JSON.stringify(durations) || JSON.stringify(nativeInfo.durationsMs) !== JSON.stringify(durations)) failures.push(`${row.direction}/${row.action}: saved master timing/frame count mismatch`);
  const frames = [];
  for (let i = 0; i < clip.frames.length; i++) {
    const f = clip.frames[i], ev = row.exportedNativeFrames[i], expectedNativePath = `${nativeDir}/${String(i).padStart(2, '0')}.png`;
    if (f.nativePng !== expectedNativePath || !fs.existsSync(path.join(ROOT, f.nativePng))) failures.push(`${row.direction}/${row.action}/${i}: native path is not self-contained`);
    if (sha(f.png) !== f.sha256 || sha(f.nativePng) !== f.nativeSha256) failures.push(`${row.direction}/${row.action}/${i}: candidate frame hash mismatch`);
    if (f.nativeSha256 !== ev.nativeExportSha256 || sha(ev.nativeExport) !== ev.nativeExportSha256) failures.push(`${row.direction}/${row.action}/${i}: copied native bytes differ from Aseprite export`);
    const composite = decode(path.join(ROOT, f.png)).image, native = decode(path.join(ROOT, f.nativePng)).image, exported = decode(path.join(ROOT, ev.nativeExport)).image;
    const crop = new PNG({ width: 128, height: 128 });
    PNG.bitblt(composite, crop, 64, 64, 128, 128, 0, 0);
    if (!same(native, exported) || !same(native, crop)) failures.push(`${row.direction}/${row.action}/${i}: native export differs from candidate or composite center crop`);
    if (f.durationMs !== ev.durationMs) failures.push(`${row.direction}/${row.action}/${i}: native export timing differs from clip`);
    frames.push({ index: i, durationMs: f.durationMs, nativePng: f.nativePng, nativeSha256: f.nativeSha256, equalsAsepriteExport: same(native, exported), equalsCompositeCenterCrop: same(native, crop) });
  }
  results.push({ cell: `${row.direction}/${row.action}`, clipPath: row.clipPath, masterSha256: clip.masterSha256, nativeMasterSha256: clip.nativeMasterSha256, frameCount: clip.frameCount, totalDurationMs: clip.totalDurationMs, frames });
}

const matrix = read('characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json');
const statusCounts = matrix.cells.reduce((acc, cell) => (acc[cell.status] = (acc[cell.status] ?? 0) + 1, acc), {});
if (matrix.cells.length !== 28 || statusCounts.ACTIVE_CANDIDATE !== 12 || statusCounts.UNCHANGED_ALIAS !== 16) failures.push('canonical matrix counts changed');
const rootPreservation = read('experiments/main-orc-rear-recovery-v2/root-final-preservation.json');
if (rootPreservation.status !== 'PASS' || rootPreservation.frontDefeatPreservedStages?.length !== 8 || rootPreservation.frontDefeatPreservedStages.some(x => !x.preserved)) failures.push('Root front Defeat preservation evidence failed');

console.log(JSON.stringify({ status: failures.length ? 'FAIL' : 'PASS', mode: 'READ_ONLY_CHECK', checks: { clips: results.length, nativeFrames: results.reduce((n, r) => n + r.frames.length, 0), masterPathsAndHashes: true, nativeFilesSelfContained: true, nativeBytesEqualAsepriteExports: true, nativePixelsEqualCompositeCrops: true, rootDefeatPreservation: true, matrix12Active16Aliases: true }, statusCounts, results, failures }, null, 2));
if (failures.length) process.exitCode = 1;
