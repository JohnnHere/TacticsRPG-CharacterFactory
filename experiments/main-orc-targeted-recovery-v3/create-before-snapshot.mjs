import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const ROOT = process.cwd();
const out = path.join(ROOT, 'experiments/main-orc-targeted-recovery-v3/before-snapshot.json');

const sha = (p) => crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');

const files = new Set();
function add(p) {
  if (/(?:^|\/|\\)(__pycache__|node_modules|\.pytest_cache)(?:\/|\\|$)|(?:\.pyc$)/.test(p)) return;
  const abs = path.resolve(ROOT, p);
  if (!fs.existsSync(abs)) return;
  if (fs.statSync(abs).isDirectory()) {
    for (const n of fs.readdirSync(abs)) {
      add(path.join(p, n));
    }
  } else {
    files.add(p.replaceAll('\\', '/'));
  }
}

const targets = [
  'characters/orc-v1/source/rear-recovery-v2',
  'characters/orc-v1/source/aseprite/rear-recovery-v2',
  'characters/orc-v1/source/complete-v1',
  'Biblioteca de Arte/Estudos Comparativos/Orc principal - Recuperacao traseira',
  'config/artistic-quality-gates-v1.json',
  'docs/ARTISTIC_QUALITY_GATES.md',
  'docs/RECIPES.md',
  'docs/MAIN_ORC_COMBAT_POLISH.md',
  'handoff/AGENT_CONTEXT.md',
  'experiments/main-orc-rear-recovery-v2/candidate28manifest.json',
  'experiments/main-orc-rear-recovery-v2/qa-result.json',
  'experiments/main-orc-rear-recovery-v2/delivery-freeze.json'
];

for (const t of targets) add(t);

const snapshot = {
  timestamp: new Date().toISOString(),
  baselineFreezeId: "0ad263a63d88586dda7c847d7be9f74ba9f855beb2526a5a2fdce7ecd25c9841",
  filesCount: files.size,
  files: Object.fromEntries([...files].sort().map(p => [p, sha(path.resolve(ROOT, p))]))
};

fs.writeFileSync(out, JSON.stringify(snapshot, null, 2) + '\n', 'utf8');
console.log(`Saved before-snapshot with ${files.size} files to ${out}`);
