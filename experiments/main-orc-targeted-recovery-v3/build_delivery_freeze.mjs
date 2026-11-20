import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const ROOT = process.cwd();

function sha256File(filePath) {
  const buf = fs.readFileSync(filePath);
  return crypto.createHash('sha256').update(buf).digest('hex');
}

function walkDir(dir, fileList = []) {
  if (!fs.existsSync(dir)) return fileList;
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      walkDir(full, fileList);
    } else if (entry.isFile()) {
      fileList.push(full);
    }
  }
  return fileList;
}

const beforeSnap = JSON.parse(fs.readFileSync(path.join(ROOT, 'experiments/main-orc-targeted-recovery-v3/before-snapshot.json'), 'utf8'));

const targets = [
  'characters/orc-v1/source/rear-recovery-v2',
  'characters/orc-v1/source/aseprite/rear-recovery-v2',
  'characters/orc-v1/source/complete-v1',
  'characters/orc-v1/sprites',
  'Biblioteca de Arte/Estudos Comparativos/Orc principal - Recuperacao traseira',
  'docs',
  'handoff'
];

const afterFiles = {};
for (const t of targets) {
  const p = path.join(ROOT, t);
  const files = walkDir(p);
  for (const f of files) {
    const rel = path.relative(ROOT, f).replace(/\\/g, '/');
    afterFiles[rel] = {
      sha256: sha256File(f),
      size: fs.statSync(f).size
    };
  }
}

const modified = [];
const created = [];
const unmodified = [];

for (const [rel, meta] of Object.entries(afterFiles)) {
  const beforeSha = typeof beforeSnap.files[rel] === 'string' ? beforeSnap.files[rel] : (beforeSnap.files[rel]?.sha256);
  if (!beforeSha) {
    created.push({ file: rel, sha256: meta.sha256, size: meta.size });
  } else if (beforeSha !== meta.sha256) {
    modified.push({
      file: rel,
      beforeSha: beforeSha,
      afterSha: meta.sha256,
      size: meta.size
    });
  } else {
    unmodified.push(rel);
  }
}

const deliveryFreeze = {
  freezeId: 'main-orc-targeted-recovery-v3',
  timestamp: new Date().toISOString(),
  totalTrackedFiles: Object.keys(afterFiles).length,
  modifiedCount: modified.length,
  createdCount: created.length,
  unmodifiedCount: unmodified.length,
  modified,
  created
};

fs.writeFileSync(
  path.join(ROOT, 'experiments/main-orc-targeted-recovery-v3/delivery-freeze.json'),
  JSON.stringify(deliveryFreeze, null, 2),
  'utf8'
);

console.log(`Delivery freeze generated:`);
console.log(`  Total tracked files: ${deliveryFreeze.totalTrackedFiles}`);
console.log(`  Modified: ${modified.length}`);
console.log(`  Created: ${created.length}`);
console.log(`  Unmodified: ${unmodified.length}`);
