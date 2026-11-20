import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

// Reuse this reviewer's previous real-page observer, not the producer's player.
const input = path.resolve('experiments\\main-orc-rear-recovery-v2\\qa-copilot\\inspect-playback.mjs');
let code = fs.readFileSync(input, 'utf8');
const replacements = [
  ["import { decode } from '../../../src/images.mjs';", `import { decode } from ${JSON.stringify(pathToFileURL(path.resolve('src\\images.mjs')).href)};`],
  ["const require = createRequire(import.meta.url);", `const require = createRequire(${JSON.stringify(pathToFileURL(input).href)});`],
  ["const Q = path.resolve('experiments\\\\main-orc-rear-recovery-v2\\\\qa-copilot');", `const Q = ${JSON.stringify(path.resolve('experiments\\main-orc-rear-recovery-v2\\qa-copilot\\revision-1'))};`],
  ["manifest.cells.filter(c => c.isAffected || c.action === 'Hit')", "manifest.cells.filter(c => ['back_l/Sword','back_r/Axe','back_l/Axe','back_r/Sword','front_r/Defeat'].includes(c.cellId))"]
];
for (const [before, after] of replacements) {
  if (!code.includes(before)) throw Error(`Prior observer changed; missing expected anchor: ${before}`);
  code = code.replace(before, after);
}
await import(`data:text/javascript;base64,${Buffer.from(code).toString('base64')}`);
