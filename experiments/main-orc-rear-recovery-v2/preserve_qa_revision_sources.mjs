// One-time, verified byte snapshot of the three candidate packages before QA revisions.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { ROOT } from '../../src/core.mjs';

const outRel = 'experiments/main-orc-rear-recovery-v2/E/rejected/qa-revision-1-before';
const outRoot = path.resolve(ROOT, outRel), rootResolved = path.resolve(ROOT);
if (!outRoot.startsWith(rootResolved + path.sep)) throw new Error(`Backup path escapes workspace: ${outRoot}`);
if (fs.existsSync(outRoot)) throw new Error(`Refusing overwrite of existing QA backup: ${outRoot}`);
const hash = p => crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const sources = [
  { direction: 'back_l', action: 'Sword', version: 'Attack-representative-v1' },
  { direction: 'back_r', action: 'Axe', version: 'Attack-representative-v1' },
  { direction: 'back_l', action: 'Axe', version: 'Attack-representative-v1' }
];
const files = [];
function copy(rel, destRel) {
  const src = path.resolve(ROOT, rel), dest = path.resolve(outRoot, destRel);
  if (!src.startsWith(rootResolved + path.sep) || !dest.startsWith(outRoot + path.sep)) throw new Error(`Path containment failure: ${rel} -> ${destRel}`);
  if (!fs.statSync(src).isFile()) throw new Error(`Expected file: ${rel}`);
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  fs.copyFileSync(src, dest);
  const sourceHash = hash(src), backupHash = hash(dest);
  if (sourceHash !== backupHash) throw new Error(`Copy hash mismatch: ${rel}`);
  files.push({ source: rel.replaceAll('\\', '/'), backup: path.relative(outRoot, dest).replaceAll('\\', '/'), bytes: fs.statSync(src).size, sha256: sourceHash, byteIdentical: true });
}
function copyTree(relDir, backupDir) {
  const srcRoot = path.resolve(ROOT, relDir), destRoot = path.resolve(outRoot, backupDir);
  if (!srcRoot.startsWith(rootResolved + path.sep) || !destRoot.startsWith(outRoot + path.sep)) throw new Error(`Directory containment failure: ${relDir}`);
  for (const entry of fs.readdirSync(srcRoot, { withFileTypes: true })) {
    const rel = path.posix.join(relDir.replaceAll('\\', '/'), entry.name);
    const dst = path.posix.join(backupDir, entry.name);
    if (entry.isDirectory()) copyTree(rel, dst);
    else if (entry.isFile()) copy(rel, dst);
    else throw new Error(`Unexpected entry type: ${rel}`);
  }
}
fs.mkdirSync(outRoot, { recursive: true });
for (const spec of sources) {
  const packageRel = `characters/orc-v1/source/rear-recovery-v2/${spec.direction}/${spec.action}/${spec.version}`;
  copyTree(packageRel, `packages/${spec.direction}/${spec.action}/${spec.version}`);
  const clip = JSON.parse(fs.readFileSync(path.join(ROOT, packageRel, 'clip.json'), 'utf8'));
  for (const key of ['master', 'bodyMaster', 'nativeMaster']) if (clip[key]) copy(clip[key], `source-masters/${clip[key]}`);
}
for (const file of [
  'experiments/main-orc-rear-recovery-v2/author_back_l_sword_and_back_r_axe_representatives.lua',
  'experiments/main-orc-rear-recovery-v2/repair_back_l_axe_clipped_arm.lua',
  'experiments/main-orc-rear-recovery-v2/clean_generated_axe_and_build_body.lua',
  'experiments/main-orc-rear-recovery-v2/reexport_representatives_from_saved_masters.lua',
  'characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json'
]) copy(file, `source-records/${file}`);
const report = { schemaVersion: 1, createdAtUtc: new Date().toISOString(), purpose: 'Byte-identical before-state preservation for QA revision-1 of SwordL, AxeR, AxeL', backupAbsolutePath: outRoot, workspaceContainmentVerified: true, packages: sources.map(s => ({ cell: `${s.direction}/${s.action}`, path: `packages/${s.direction}/${s.action}/${s.version}` })), copiedFileCount: files.length, allCopiesByteIdentical: files.every(f => f.byteIdentical), files };
fs.writeFileSync(path.join(outRoot, 'backup-inventory.json'), `${JSON.stringify(report, null, 2)}\n`);
console.log(JSON.stringify({ status: 'PASS', backupAbsolutePath: outRoot, copiedFileCount: files.length, allCopiesByteIdentical: report.allCopiesByteIdentical }, null, 2));
