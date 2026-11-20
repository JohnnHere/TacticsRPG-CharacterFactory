import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { parseArgs } from 'node:util';
import { ROOT, hash, readJSON } from '../../src/core.mjs';
import { decode } from '../../src/images.mjs';

const { values } = parseArgs({ options: {
  manifest: { type: 'string', default: 'characters/orc-v1/source/combat-recovery-v7/candidate28manifest.json' },
} });
const manifestPath = values.manifest;
const absolute = file => path.resolve(ROOT, file);
const digest = file => hash(fs.readFileSync(absolute(file)));
const manifest = readJSON(absolute(manifestPath));
const manifestSha256 = digest(manifestPath);
const output = absolute(`experiments/main-orc-combat-recovery-v7/source-reexports/${manifestSha256}`);
const profile = absolute('tmp/aseprite-v5-sourcecheck-root-continuity');
fs.mkdirSync(output, { recursive: true });
fs.mkdirSync(profile, { recursive: true });
const results = [];
for (const cell of manifest.cells.filter(cell => cell.isAffected)) {
  const clip = readJSON(absolute(cell.clipJson));
  for (const [field, framePath] of [
    ['master', frame => frame.png],
    ['nativeMaster', frame => frame.nativePng],
    ['bodyMaster', frame => frame.layers?.body?.png ?? frame.png],
    ['handMaster', frame => frame.layers.handFront.png],
  ]) {
    if (!clip[field]) continue;
    const name = `${cell.direction}-${cell.action}-${field}`;
    const sheetPath = path.join(output, `${name}.png`);
    const dataPath = path.join(output, `${name}.json`);
    const run = spawnSync('F:\\SteamLibrary\\steamapps\\common\\Aseprite\\Aseprite.exe', [
      '--batch', '--noinapp', absolute(clip[field]), '--sheet-type', 'horizontal',
      '--sheet', sheetPath, '--format', 'json-array', '--data', dataPath,
    ], {
      cwd: ROOT, windowsHide: true, timeout: 120000, encoding: 'utf8',
      env: { ...process.env, ASEPRITE_USER_FOLDER: profile },
    });
    if (run.error) throw run.error;
    assert.equal(run.status, 0, `${name}: Aseprite exit ${run.status}\n${run.stderr}\n${run.stdout}`);
    const sheet = decode(sheetPath).image;
    const metadata = readJSON(dataPath);
    assert.deepEqual(metadata.frames.map(frame => frame.duration),
      clip.frames.map(frame => frame.durationMs), `${name}: fresh exported timing`);
    for (const [index, frame] of clip.frames.entries()) {
      const expected = decode(absolute(framePath(frame))).image;
      assert.equal(sheet.height, expected.height, `${name}: source height`);
      assert.equal(sheet.width, expected.width * clip.frames.length, `${name}: source strip width`);
      for (let y = 0; y < expected.height; y++) for (let x = 0; x < expected.width; x++) {
        const source = (y * sheet.width + index * expected.width + x) * 4;
        const target = (y * expected.width + x) * 4;
        assert.equal(sheet.data[source + 3], expected.data[target + 3], `${name}/${index}: source alpha`);
        if (expected.data[target + 3]) for (let c = 0; c < 3; c++) {
          assert.equal(sheet.data[source + c], expected.data[target + c], `${name}/${index}: source RGBA`);
        }
      }
    }
    results.push({ cell: cell.cellId, field, source: clip[field],
      sourceSha256: digest(clip[field]), frames: clip.frames.length });
    console.log(`PASS ${name}: ${clip.frames.length} frames from saved source`);
  }
}
const result = { status: 'PASS_SAVED_SOURCE_EXPORTS', manifest: manifestPath,
  manifestSha256, masters: results.length, results, artisticallyApproved: false };
fs.writeFileSync(path.join(output, 'result.json'), JSON.stringify(result, null, 2));
console.log(JSON.stringify({ status: result.status, masters: results.length,
  frames: results.reduce((sum, item) => sum + item.frames, 0), output }));


