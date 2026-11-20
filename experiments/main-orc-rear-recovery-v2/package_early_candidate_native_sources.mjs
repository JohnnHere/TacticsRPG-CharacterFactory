// Export native masters, verify them against composite crops, then package bytes and source hashes.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { PNG } from 'pngjs';
import { ROOT } from '../../src/core.mjs';
import { decode } from '../../src/images.mjs';
import { exportAseprite } from '../../src/aseprite.mjs';

const manifestPath = 'experiments/main-orc-rear-recovery-v2/native-source-metadata-export-manifest.json';
const manifest = JSON.parse(fs.readFileSync(path.join(ROOT, manifestPath), 'utf8'));
const specs = [
  { direction: 'back_r', action: 'Unarmed', job: 'unarmed-back_r-native', master: 'characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_r/unarmed-attack.aseprite', nativeMaster: 'characters/orc-v1/source/aseprite/rear-recovery-v2/native/unarmed-back_r.aseprite' },
  { direction: 'back_l', action: 'Unarmed', job: 'unarmed-back_l-native', master: 'characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_l/unarmed-attack.aseprite', nativeMaster: 'characters/orc-v1/source/aseprite/rear-recovery-v2/native/unarmed-back_l.aseprite' },
  { direction: 'front_r', action: 'Defeat', job: 'defeat-front_r-native', master: 'characters/orc-v1/source/aseprite/rear-recovery-v2/composite/front_r/defeat.aseprite', nativeMaster: 'characters/orc-v1/source/aseprite/rear-recovery-v2/native/defeat-front_r.aseprite' },
  { direction: 'front_l', action: 'Defeat', job: 'defeat-front_l-native', master: 'characters/orc-v1/source/aseprite/rear-recovery-v2/composite/front_l/defeat.aseprite', nativeMaster: 'characters/orc-v1/source/aseprite/rear-recovery-v2/native/defeat-front_l.aseprite' }
];
const pngEqual = (a, b) => a.width === b.width && a.height === b.height && a.data.equals(b.data);
const sha = p => crypto.createHash('sha256').update(fs.readFileSync(path.join(ROOT, p))).digest('hex');

const result = exportAseprite(path.join(ROOT, manifestPath));
if (result.status !== 'PASS') throw new Error(`Aseprite native export failed: ${result.status}`);
const failures = [], rows = [];
for (const spec of specs) {
  const clipPath = `characters/orc-v1/source/rear-recovery-v2/${spec.direction}/${spec.action}/clip.json`;
  const clip = JSON.parse(fs.readFileSync(path.join(ROOT, clipPath), 'utf8'));
  const job = result.jobs.find(j => j.id === spec.job);
  if (!job || job.frames.length !== 5) { failures.push(`${spec.direction}/${spec.action}: exported native job/frame count missing`); continue; }
  const durations = clip.frames.map(f => f.durationMs);
  if (JSON.stringify(durations) !== JSON.stringify(job.frames.map(f => f.durationMs))) failures.push(`${spec.direction}/${spec.action}: native master timing differs from clip timings`);
  const copied = [];
  for (let i = 0; i < 5; i++) {
    const n = String(i).padStart(2, '0');
    const compositePath = clip.frames[i].png;
    const composite = decode(path.join(ROOT, compositePath)).image;
    const nativeExport = decode(path.join(ROOT, result.path, job.frames[i].file)).image;
    const crop = new PNG({ width: 128, height: 128 });
    PNG.bitblt(composite, crop, 64, 64, 128, 128, 0, 0);
    if (!pngEqual(nativeExport, crop)) failures.push(`${spec.direction}/${spec.action}/${n}: native master export differs from 256px composite center crop`);
    copied.push({ index: i, durationMs: job.frames[i].durationMs, compositePng: compositePath, compositeSha256: sha(compositePath), nativeExport: `${result.path}/${job.frames[i].file}`, nativeExportSha256: sha(`${result.path}/${job.frames[i].file}`), rgbaMatchesCompositeCenterCrop: pngEqual(nativeExport, crop) });
  }
  rows.push({ direction: spec.direction, action: spec.action, clipPath, master: spec.master, masterSha256: sha(spec.master), nativeMaster: spec.nativeMaster, nativeMasterSha256: sha(spec.nativeMaster), exportedNativeFrames: copied });
}
if (failures.length) throw new Error(`Refusing package writes; native export verification failed:\n${failures.join('\n')}`);

// All four sources pass before any clip metadata or candidate file is modified.
for (let si = 0; si < specs.length; si++) {
  const spec = specs[si], row = rows[si];
  const clip = JSON.parse(fs.readFileSync(path.join(ROOT, row.clipPath), 'utf8'));
  const nativeDir = path.posix.join(path.posix.dirname(row.clipPath), 'native');
  fs.mkdirSync(path.join(ROOT, nativeDir), { recursive: true });
  for (let i = 0; i < 5; i++) {
    const n = String(i).padStart(2, '0');
    const relativeExport = row.exportedNativeFrames[i].nativeExport;
    const nativePath = `${nativeDir}/${n}.png`;
    fs.copyFileSync(path.join(ROOT, relativeExport), path.join(ROOT, nativePath));
    clip.frames[i].nativePng = nativePath;
    clip.frames[i].nativeSha256 = sha(nativePath);
  }
  clip.frameCount = clip.totalFrames;
  clip.master = row.master;
  clip.masterSha256 = row.masterSha256;
  clip.nativeMaster = row.nativeMaster;
  clip.nativeMasterSha256 = row.nativeMasterSha256;
  clip.stripSha256 = sha(clip.strip);
  fs.writeFileSync(path.join(ROOT, row.clipPath), `${JSON.stringify(clip, null, 2)}\n`);
  row.nativeOutputDirectory = nativeDir;
  row.nativeFrameHashes = clip.frames.map(f => ({ nativePng: f.nativePng, nativeSha256: f.nativeSha256 }));
  row.strip = clip.strip;
  row.stripSha256 = clip.stripSha256;
}

const report = { schemaVersion: 1, status: 'PASS', createdAtUtc: new Date().toISOString(), mode: 'Aseprite native export; metadata/package only; no art pixels or timings edited', nativeExportBuild: result.path, compositeExportBuild: 'dist/editor/main-orc-rear-recovery-v2-export/663e379bdd42e17b8cba', compositeProof: 'verify_export_aseprite.mjs and verify_export_pixels.mjs: 36/36 frames matched saved composite masters (timings and RGBA pixels)', checks: { clips: 4, nativeFrames: 20, nativeExportTimingsMatchClip: true, nativeExportsMatchCompositeCenterCrop: true, nativeBytesCopiedIntoCandidateFolders: true, frameCountAliasAdded: true, sourceMasterHashesRecorded: true, stripHashesRecorded: true }, results: rows, failures: [] };
const reportPath = 'experiments/main-orc-rear-recovery-v2/four-early-clips-source-metadata-verification.json';
fs.writeFileSync(path.join(ROOT, reportPath), `${JSON.stringify(report, null, 2)}\n`);
console.log(JSON.stringify({ status: report.status, reportPath, nativeExportBuild: result.path, clips: rows.map(r => ({ direction: r.direction, action: r.action, masterSha256: r.masterSha256, nativeMasterSha256: r.nativeMasterSha256, frames: r.exportedNativeFrames.length, allNativeCropMatches: r.exportedNativeFrames.every(f => f.rgbaMatchesCompositeCenterCrop) })) }, null, 2));
