import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { PNG } from 'pngjs';
import { checkAseprite, executeAseprite } from '../../../../src/aseprite.mjs';

const E = 'experiments\\main-orc-rear-recovery-v2';
const Q = path.join(E, 'qa-copilot', 'revision-1');
const read = p => JSON.parse(fs.readFileSync(p, 'utf8'));
const sha = p => crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const freeze = read(path.join(E, 'delivery-freeze.json'));
const old = read(path.join(E, 'qa-history', '6fa4653eabe660992acc422aa32159b48e4971122df0e995b99a19261df4a843', 'delivery-freeze.json'));
const tool = checkAseprite();
if (tool.status !== 'AVAILABLE') throw Error(tool.error);
const result = { reviewer: 'GPT Sol6.1 via GitHub Copilot', freezeId: freeze.freezeId, editor: tool.version, sets: [], failures: [] };
fs.mkdirSync(Q, { recursive: true });
for (const [direction, action] of [['back_l', 'Sword'], ['back_r', 'Axe'], ['back_l', 'Axe']]) {
  const clip = read(path.join('characters', 'orc-v1', 'source', 'rear-recovery-v2', direction, action, 'Attack-representative-v1', 'clip.json'));
  const sets = [
    ['composite', clip.master, 256, null, f => f.png],
    ['body', clip.bodyMaster, 256, null, f => f.layers.body.png],
    ['native', clip.nativeMaster, 128, null, f => f.nativePng],
    ...clip.layerOrder.map(layer => [layer, clip.master, 256, layer, f => f.layers[layer].png])
  ];
  for (const [kind, master, size, layer, target] of sets) {
    const dir = path.join(Q, 'source-proof', `${direction}_${action}`, kind);
    fs.mkdirSync(dir, { recursive: true });
    const source = path.resolve(dir, 'source.aseprite');
    const digest = sha(master);
    if (digest !== freeze.files[master.replaceAll('\\', '/')]) throw Error(`Source not bound to current freeze: ${master}`);
    fs.copyFileSync(master, source);
    executeAseprite(tool.executable, [
      ...(layer ? ['--layer', layer] : []), source, '--list-layer-hierarchy',
      '--sheet-type', 'horizontal', '--format', 'json-array',
      '--sheet', path.resolve(dir, 'sheet.png'), '--data', path.resolve(dir, 'sheet.json')
    ]);
    const sheet = PNG.sync.read(fs.readFileSync(path.join(dir, 'sheet.png')));
    const meta = read(path.join(dir, 'sheet.json'));
    if (meta.frames.length !== 8) result.failures.push(`${direction}/${action}/${kind}: frame count`);
    const frames = meta.frames.map((frame, i) => {
      const rect = frame.frame, expected = PNG.sync.read(fs.readFileSync(target(clip.frames[i])));
      const tile = new PNG({ width: rect.w, height: rect.h });
      PNG.bitblt(sheet, tile, rect.x, rect.y, rect.w, rect.h, 0, 0);
      const exact = rect.w === size && rect.h === size && expected.width === size && expected.height === size && tile.data.equals(expected.data);
      if (!exact || frame.duration !== clip.frames[i].durationMs) result.failures.push(`${direction}/${action}/${kind}/F${i}: pixels/timing`);
      return { index: i, exactDecodedRgba: exact, durationMs: frame.duration, target: target(clip.frames[i]) };
    });
    if (sha(master) !== digest || sha(source) !== digest) result.failures.push(`${master}: source mutated`);
    if (kind === 'composite' && JSON.stringify(meta.meta.layers.map(l => l.name)) !== JSON.stringify(clip.layerOrder)) result.failures.push(`${direction}/${action}: layer hierarchy`);
    result.sets.push({ cell: `${direction}/${action}`, kind, master, masterSha256: digest, frames });
  }
  console.log(`Fresh copied-master proof: ${direction}/${action}, all 7 export sets`);
}
const changed = Object.entries(old.files).filter(([p, h]) => freeze.files[p] && freeze.files[p] !== h).map(([p]) => p);
const added = Object.keys(freeze.files).filter(p => !old.files[p]);
const removed = Object.keys(old.files).filter(p => !freeze.files[p]);
const gates = read('config\\artistic-quality-gates-v1.json');
const fields = ['symptom', 'verifiedCause', 'failedApproach', 'successfulCorrection', 'reuse', 'prevention', 'validation', 'cost', 'applicability'];
result.lessons = gates.productionLessons.map(l => ({ id: l.id, allNineFieldsPresent: fields.every(k => typeof l[k] === 'string' && l[k].trim()) }));
if (result.lessons.some(l => !l.allNineFieldsPresent)) result.failures.push('Incomplete lesson fields');
result.currentAssessment = gates.currentAssessment;
result.freezeDelta = {
  oldFreeze: old.freezeId, newFreeze: freeze.freezeId, oldFiles: Object.keys(old.files).length, newFiles: Object.keys(freeze.files).length,
  changedFiles: changed.length, addedFiles: added.length, removedFiles: removed,
  changedKnowledgeAndValidators: changed.filter(p => /^(docs\/|config\/|recipes\/|handoff\/|AGENTS\.md|test\/)|validate_candidate_manifest/.test(p))
};
result.freshFrameComparisons = result.sets.reduce((n, s) => n + s.frames.length, 0);
result.status = result.failures.length ? 'FAIL' : 'PASS';
fs.writeFileSync(path.join(Q, 'source-proof.json'), JSON.stringify(result, null, 2) + '\n');
console.log(JSON.stringify({ status: result.status, sets: result.sets.length, freshFrameComparisons: result.freshFrameComparisons, freezeDelta: result.freezeDelta, failures: result.failures }, null, 2));
if (result.failures.length) process.exitCode = 1;
