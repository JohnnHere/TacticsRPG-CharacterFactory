import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { spawnSync } from 'node:child_process';
import { ROOT } from '../src/core.mjs';

// Regression: `--entry` preview construction must not depend on the obsolete
// 'Biblioteca de Arte/Historico de Entregas/Orc V1 - Armas v2' directory (or on a
// previous-review copy source that only exists in the rescue-v3 workspace).
const BUILDER = 'tools/build-main-orc-rescue-review.py';
const PAGE = 'Biblioteca de Arte/Estudos Comparativos/Orc principal - Entrada de combate/index.html';
const TREES = [
  'characters/orc-v1/source/onehanded-entry-v1',
  'characters/orc-v1/source/aseprite/onehanded-entry-v1',
  'characters/orc-v1/source/onehanded-polish-v1/Sword/Attack',
  'characters/orc-v1/source/onehanded-polish-v1/Axe/Attack',
  'characters/orc-v1/source/aseprite/onehanded-polish-v1',
  'characters/orc-v1/source/onehanded-rescue-v3/Idle',
  'characters/orc-v1/source/onehanded-rescue-v3/Walk',
  'characters/orc-v1/source/aseprite/onehanded-rescue-v3',
  'assets/weapons/recruit-sword',
  'assets/weapons/militia-axe',
];
const FILES = [
  BUILDER,
  'characters/orc-v1/concepts/concept-selected.png',
  'characters/orc-v1/source/aseprite/concept-selected.aseprite',
  'experiments/main-orc-entry-v1/sword-hands.png',
  'experiments/main-orc-entry-v1/axe-hands.png',
  'docs/MAIN_ORC_COMBAT_POLISH.md',
  'docs/WEAPON_ART_STANDARD.md',
  'docs/ART_LIBRARY_COMPARISONS.json',
];

function findPython() {
  const venv = path.join(ROOT, 'tmp', 'pixel-venv', 'Scripts', 'python.exe');
  if (fs.existsSync(venv)) return venv;
  for (const name of ['python', 'python3']) {
    if (spawnSync(name, ['--version'], { encoding: 'utf8' }).status === 0) return name;
  }
  return null;
}

const python = findPython();
const missing = [...TREES, ...FILES].filter(rel => !fs.existsSync(path.join(ROOT, rel)));
test('entry preview builds without the historical deliveries directory', {
  skip: python ? (missing.length ? `requires local candidate assets: ${missing[0]}` : false)
    : 'python optional: install tmp/pixel-venv or put python on PATH',
}, () => {
  const name = 'preview-entry-' + crypto.randomBytes(5).toString('hex');
  const box = path.join(ROOT, 'tmp', name);
  const copyTree = rel => fs.cpSync(path.join(ROOT, rel), path.join(box, rel), { recursive: true });
  try {
    fs.mkdirSync(box, { recursive: true });
    for (const rel of FILES) fs.mkdirSync(path.dirname(path.join(box, rel)), { recursive: true }), fs.copyFileSync(path.join(ROOT, rel), path.join(box, rel));
    for (const rel of TREES) copyTree(rel);
    // The sandbox deliberately has NO 'Biblioteca de Arte/Historico de Entregas' at all.
    const run = spawnSync(python, [BUILDER, '--entry'], { cwd: box, encoding: 'utf8' });
    assert.equal(run.status, 0, `builder failed without historical directory:\n${run.stdout}\n${run.stderr}`);
    assert.ok(fs.existsSync(path.join(box, PAGE)), 'entry review page was not generated');
    assert.ok(!fs.existsSync(path.join(box, 'Biblioteca de Arte/Historico de Entregas')),
      'entry build created or required the historical deliveries directory');
    const catalog = JSON.parse(fs.readFileSync(path.join(box, path.dirname(PAGE), 'catalogo.json'), 'utf8'));
    assert.equal(catalog.revision, 'main-orc-onehanded-entry-v1');
    assert.equal(catalog.artisticApproval, 'PENDING_CREATOR');
    const registry = JSON.parse(fs.readFileSync(path.join(box, 'docs/ART_LIBRARY_COMPARISONS.json'), 'utf8'));
    assert.equal(registry[0].id, 'main-orc-onehanded-entry-v1', 'entry page registered in library comparisons');
  } finally {
    fs.rmSync(box, { recursive: true, force: true });
  }
});
