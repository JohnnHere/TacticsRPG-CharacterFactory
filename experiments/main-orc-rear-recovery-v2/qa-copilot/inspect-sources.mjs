import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { PNG } from 'pngjs';
import { decode } from '../../../src/images.mjs';
import { findAseprite, executeAseprite } from '../../../src/aseprite.mjs';

const E = 'experiments\\main-orc-rear-recovery-v2';
const Q = path.join(E, 'qa-copilot');
const read = p => JSON.parse(fs.readFileSync(p, 'utf8'));
const sha = p => crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const freeze = read(path.join(E, 'delivery-freeze.json'));
const manifest = read('characters\\orc-v1\\source\\rear-recovery-v2\\candidate28manifest.json');
const previous = read(path.join(E, 'qa-argon', 'independent-aseprite-reexport-report.json'));
const failures = [], reused = [], fresh = [], sheets = [];
const same = (a, b) => a.width === b.width && a.height === b.height && a.data.equals(b.data);
fs.mkdirSync(path.join(Q, 'images'), { recursive: true });

function image(p) { return decode(path.resolve(p)).image; }
function crop(im, x, y, w, h) {
  const out = new PNG({ width: w, height: h });
  PNG.bitblt(im, out, x, y, w, h, 0, 0);
  return out;
}
function sheet(frames, output, native = false) {
  const size = native ? 128 : 256, zoom = native ? 2 : 1;
  const out = new PNG({ width: 4 * 256, height: Math.ceil(frames.length / 4) * 280 });
  for (let y = 0; y < out.height; y++) for (let x = 0; x < out.width; x++) {
    const n = (y * out.width + x) * 4, c = ((x >> 3) + (y >> 3)) % 2 ? 40 : 53;
    out.data.set([c, c + 6, c + 10, 255], n);
  }
  frames.forEach((im, i) => {
    if (native && im.width === 256) im = crop(im, 64, 64, 128, 128);
    for (let y = 0; y < size; y++) for (let x = 0; x < size; x++) {
      const n = (y * size + x) * 4, a = im.data[n + 3] / 255;
      if (!a) continue;
      for (let dy = 0; dy < zoom; dy++) for (let dx = 0; dx < zoom; dx++) {
        const px = (i % 4) * 256 + x * zoom + dx;
        const py = Math.floor(i / 4) * 280 + y * zoom + dy;
        const at = (py * out.width + px) * 4;
        for (let c = 0; c < 3; c++) out.data[at + c] = Math.round(im.data[n + c] * a + out.data[at + c] * (1 - a));
      }
    }
    // The short binary marker below each tile encodes the zero-based frame number.
    for (let bit = 0; bit < 4; bit++) for (let y = 260; y < 268; y++) for (let x = bit * 12; x < bit * 12 + 8; x++) {
      const at = ((Math.floor(i / 4) * 280 + y) * out.width + (i % 4) * 256 + x) * 4;
      out.data.set(i & (1 << bit) ? [230, 190, 90, 255] : [70, 80, 90, 255], at);
    }
  });
  fs.writeFileSync(output, PNG.sync.write(out));
}

for (const cell of manifest.cells.filter(c => c.isAffected || c.action === 'Hit')) {
  const clip = read(cell.clipJson), id = cell.cellId.replace('/', '_');
  const comp = clip.frames.map(f => image(f.png));
  const bodies = clip.frames.map(f => image(f.nativePng ?? f.png));
  const paths = [path.join(Q, 'images', `${id}-composite.png`), path.join(Q, 'images', `${id}-body-detail.png`)];
  sheet(comp, paths[0]);
  sheet(bodies, paths[1], true);
  sheets.push({ cell: cell.cellId, paths, frameOrder: clip.frames.map((_, i) => i), durationsMs: clip.frames.map(f => f.durationMs) });
}

// Reuse Argon's fresh exports only after independently binding every copied master
// to this freeze and comparing every sheet tile against the current canonical files.
for (const cell of manifest.cells.filter(c => c.isAffected)) {
  const clip = read(cell.clipJson), id = cell.cellId.replace('/', '_');
  const kinds = [['comp', clip.master], ['nat', clip.nativeMaster]];
  if (clip.bodyMaster) kinds.push(['body', clip.bodyMaster]);
  if (clip.bodyMaster) for (const layer of ['weaponBack', 'body', 'weaponFront', 'handFront']) kinds.push([`layer_${layer}`, clip.master]);
  for (const [kind, master] of kinds) {
    const dir = path.join(E, 'qa-argon', 'reexports', `${id}_${kind}`);
    const copy = path.join(dir, 'source.aseprite'), meta = read(path.join(dir, 'sheet.json'));
    const frozenHash = freeze.files[master.replaceAll('\\', '/')];
    if (!frozenHash || sha(master) !== frozenHash || sha(copy) !== frozenHash) failures.push(`${cell.cellId}/${kind}: reused source is not freeze-identical`);
    const im = image(path.join(dir, 'sheet.png'));
    let matches = 0;
    for (let i = 0; i < meta.frames.length; i++) {
      const f = meta.frames[i], r = f.frame, tile = crop(im, r.x, r.y, r.w, r.h);
      const frame = clip.frames[i];
      const target = kind === 'comp' ? frame.png : kind === 'nat' ? frame.nativePng : kind === 'body' ? frame.layers.body.png : frame.layers[kind.slice(6)].png;
      const expected = kind === 'nat' && !target ? crop(image(frame.png), 64, 64, 128, 128) : image(target);
      if (!same(tile, expected) || f.duration !== frame.durationMs) failures.push(`${cell.cellId}/${kind}/F${i}: reused pixels/timing mismatch`);
      else matches++;
    }
    if (meta.frames.length !== clip.frames.length) failures.push(`${cell.cellId}/${kind}: reused frame count mismatch`);
    reused.push({ cell: cell.cellId, kind, master, sha256: frozenHash, exactFrames: matches });
  }
}

const exe = findAseprite();
const version = executeAseprite(exe, ['--version']).stdout.trim();
for (const cell of manifest.cells.filter(c => c.isAffected && ['Sword', 'Axe'].includes(c.action))) {
  const clip = read(cell.clipJson), id = cell.cellId.replace('/', '_');
  const dir = path.join(Q, 'reexports', id);
  fs.mkdirSync(dir, { recursive: true });
  const copy = path.resolve(dir, 'source.aseprite');
  fs.copyFileSync(clip.master, copy);
  const png = path.resolve(dir, 'body.png'), json = path.resolve(dir, 'body.json');
  executeAseprite(exe, ['--layer', 'body', copy, '--sheet-type', 'horizontal', '--format', 'json-array', '--sheet', png, '--data', json]);
  const meta = read(json), im = image(png);
  let matches = 0;
  for (let i = 0; i < meta.frames.length; i++) {
    const f = meta.frames[i], r = f.frame;
    if (same(crop(im, r.x, r.y, r.w, r.h), image(clip.frames[i].layers.body.png)) && f.duration === clip.frames[i].durationMs) matches++;
    else failures.push(`${cell.cellId}/fresh-body/F${i}: source export mismatch`);
  }
  fresh.push({ cell: cell.cellId, master: clip.master, sha256: sha(copy), exactFrames: matches, directory: dir });
}
const ledger = read(path.join(E, 'cost-provenance-ledger.json'));
const gates = read('config\\artistic-quality-gates-v1.json');
const fields = ['symptom', 'verifiedCause', 'failedApproach', 'successfulCorrection', 'reuse', 'prevention', 'validation', 'cost', 'applicability'];
const lessons = gates.productionLessons.map(l => ({ id: l.id, complete: fields.every(k => typeof l[k] === 'string' && l[k].trim()) }));
if (lessons.some(l => !l.complete)) failures.push('Incomplete lesson evidence fields');
const result = {
  identity: 'GPT Sol6.1 via GitHub Copilot', freezeId: freeze.freezeId,
  status: failures.length ? 'FAIL' : 'PASS', aseprite: { executable: exe, version, mode: 'hidden --batch --noinapp; isolated profile' },
  attribution: 'Argon exports reused with fresh source-hash, decoded-RGBA and timing checks; four body-layer exports newly executed by Copilot. No artistic conclusions reused.',
  previousReportedStatus: previous.status, reusedExports: reused, freshExports: fresh, sheets, lessons,
  accounting: { jobs: ledger.jobs.length, generations: ledger.jobs.reduce((n, j) => n + j.chargedGenerations, 0), summary: ledger.summary },
  failures
};
fs.writeFileSync(path.join(Q, 'source-integrity.json'), JSON.stringify(result, null, 2) + '\n');
console.log(JSON.stringify({ status: result.status, freezeId: result.freezeId, reusedExports: reused.length, freshExports: fresh.length, lessons: lessons.length, accounting: result.accounting, failures }, null, 2));
if (failures.length) process.exitCode = 1;
