#!/usr/bin/env node
// Verify a candidate clip dir against its baseline: byte equality per file plus
// exact pixel-diff census for the files that differ.
// Usage: node verify-candidate.mjs <baselineDir> <candidateDir> <out.json>
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { PNG } from 'pngjs';

const [, , baseDir, candDir, outJson] = process.argv;
const sha = (p) => crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const walk = (dir, base = dir, acc = []) => {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, e.name);
    if (e.isDirectory()) walk(full, base, acc);
    else acc.push(path.relative(base, full).replaceAll('\\', '/'));
  }
  return acc;
};
const baseFiles = new Set(walk(baseDir));
const candFiles = new Set(walk(candDir));
const onlyBase = [...baseFiles].filter((f) => !candFiles.has(f));
const onlyCand = [...candFiles].filter((f) => !baseFiles.has(f));
const report = { baselineDir: baseDir, candidateDir: candDir, identical: [], changed: [], onlyBaseline: onlyBase, onlyCandidate: onlyCand };
for (const rel of [...baseFiles].filter((f) => candFiles.has(f)).sort()) {
  const a = path.join(baseDir, rel);
  const b = path.join(candDir, rel);
  const ha = sha(a);
  const hb = sha(b);
  if (ha === hb) {
    report.identical.push({ file: rel, sha256: ha });
    continue;
  }
  const entry = { file: rel, baselineSha256: ha, candidateSha256: hb };
  if (rel.endsWith('.png')) {
    const A = PNG.sync.read(fs.readFileSync(a));
    const B = PNG.sync.read(fs.readFileSync(b));
    entry.size = `${A.width}x${A.height}`;
    if (A.width === B.width && A.height === B.height) {
      const diff = [];
      for (let y = 0; y < A.height; y += 1) {
        for (let x = 0; x < A.width; x += 1) {
          const s = (y * A.width + x) * 4;
          if (A.data[s] !== B.data[s] || A.data[s + 1] !== B.data[s + 1] || A.data[s + 2] !== B.data[s + 2] || A.data[s + 3] !== B.data[s + 3]) diff.push([x, y]);
        }
      }
      entry.diffPixels = diff.length;
      entry.diffBBox = diff.length
        ? [Math.min(...diff.map((d) => d[0])), Math.min(...diff.map((d) => d[1])), Math.max(...diff.map((d) => d[0])), Math.max(...diff.map((d) => d[1]))]
        : null;
      entry.diffList = diff.slice(0, 40);
    }
  }
  report.changed.push(entry);
}
fs.writeFileSync(outJson, JSON.stringify(report, null, 2));
console.log(`identical=${report.identical.length} changed=${report.changed.length} onlyBaseline=${onlyBase.length} onlyCandidate=${onlyCand.length}`);
for (const c of report.changed) console.log(`  CHANGED ${c.file} diffPixels=${c.diffPixels ?? 'n/a'} bbox=${c.diffBBox ? c.diffBBox.join(',') : '-'}`);
for (const f of onlyBase) console.log(`  ONLY BASELINE ${f}`);
for (const f of onlyCand) console.log(`  ONLY CANDIDATE ${f}`);
