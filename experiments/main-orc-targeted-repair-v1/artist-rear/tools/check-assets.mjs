#!/usr/bin/env node
// Verifies the comparator's asset URLs exactly as file:// would resolve them:
// every URL is relative to the HTML file's own directory.
// Usage: node check-assets.mjs <comparator.html>
import fs from 'node:fs';
import path from 'node:path';

const [, , htmlPath] = process.argv;
const html = fs.readFileSync(htmlPath, 'utf8');
const dir = path.dirname(path.resolve(htmlPath));
const urls = new Set();
for (const m of html.matchAll(/"(?:comp|bodyOnly|handFront|native)":"([^"]+)"/g)) urls.add(m[1]);
const missing = [];
const ok = [];
for (const u of urls) {
  const resolved = path.resolve(dir, u);
  if (fs.existsSync(resolved)) ok.push(u);
  else missing.push(u);
}
console.log(`html=${path.relative(process.cwd(), htmlPath).split(path.sep).join('/')}`);
console.log(`baseDir(file://)=${path.relative(process.cwd(), dir).split(path.sep).join('/')}`);
console.log(`assetUrls=${urls.size} resolved=${ok.length} missing=${missing.length}`);
for (const m of missing.slice(0, 12)) console.log(`  MISSING ${m} -> ${path.resolve(dir, m)}`);
process.exit(missing.length ? 1 : 0);
