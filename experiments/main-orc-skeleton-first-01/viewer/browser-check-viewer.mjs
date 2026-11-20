/**
 * REAL-browser automated check for the skeleton-first viewer
 * (experiments/main-orc-skeleton-first-01/viewer/index.html).
 * Headless Chromium via Playwright, same runtime used by
 * test/browser-check-rear-recovery-review.mjs — file:// AND http:// scenarios.
 *
 * Reproducible inside the repo:
 *   node experiments/main-orc-skeleton-first-01/viewer/browser-check-viewer.mjs
 *
 * Bounded by design: every individual wait <= 45s, whole run hard 150s deadline,
 * browser ALWAYS closed (finally). Expectations are DERIVED from the fixture JSON
 * on disk (counts/frames may change on regeneration — nothing hardcoded except
 * the documented DEFAULT_BLADE_FRACTION 0.30 shared with app.js).
 *
 * Known-asset allowlist: the correction's canonical background
 * characters/orc-v1/source/combat-recovery-v8/rear-arc/back_l-sword/02.png does
 * NOT exist yet (the viewer falls back to back_l-sword/frames/02.png). Exactly
 * ONE resource error for that URL is expected and allowlisted; anything else fails.
 */
import fs from 'fs';
import path from 'path';
import http from 'http';
import { fileURLToPath, pathToFileURL } from 'url';
import { createRequire } from 'module';

const require = createRequire(import.meta.url);
const { chromium } = require('C:/Users/João Orlando/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const VIEWER = path.resolve(__dirname);                      // .../viewer
const EXP = path.resolve(VIEWER, '..');                      // experimento
const REPO = path.resolve(EXP, '..', '..');                  // raiz da fábrica
const PAGE_REL = 'experiments/main-orc-skeleton-first-01/viewer/index.html';
const shotDir = path.join(VIEWER, 'tmp-check');
fs.mkdirSync(shotDir, { recursive: true });

const CHROMIUM = 'C:/Users/João Orlando/AppData/Local/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-win64/chrome-headless-shell.exe';
const OVERALL_DEADLINE_MS = 150000;
const started = Date.now();
const leftMs = () => OVERALL_DEADLINE_MS - (Date.now() - started);
function assertBudget(label) {
  if (leftMs() <= 0) throw new Error(`Overall ${OVERALL_DEADLINE_MS / 1000}s deadline exceeded at: ${label}`);
}

let failures = 0;
const results = [];
function check(name, ok, detail = '') {
  results.push({ name, ok, detail });
  console.log(`${ok ? '  OK: ' : '  FAIL: '}${name}${detail ? ' — ' + detail : ''}`);
  if (!ok) failures++;
}

// Expectations derived from the fixture on disk (never hardcoded counts)
const posesFx = JSON.parse(fs.readFileSync(path.join(VIEWER, 'fixtures', 'sample-poses.json'), 'utf8'));
const seqFx = JSON.parse(fs.readFileSync(path.join(VIEWER, 'fixtures', 'sample-sequence.json'), 'utf8'));
const N_FRAMES = seqFx.frames.length;
const N_POSES = posesFx.poses.length;
const DEFAULT_BLADE_FRACTION = 0.30; // shared contract with app.js
const tipOf = (f) => {
  const g = f.grip;
  return { x: g.point.x + g.bladeDirection.x * DEFAULT_BLADE_FRACTION, y: g.point.y + g.bladeDirection.y * DEFAULT_BLADE_FRACTION };
};
const dist256 = (a, b) => Math.hypot(a.x - b.x, a.y - b.y) * 256;
const DELTA_F8 = dist256(tipOf(seqFx.frames[8]), tipOf(seqFx.frames[7]));
const COCO18 = ['NOSE', 'NECK', 'RIGHT SHOULDER', 'RIGHT ELBOW', 'RIGHT ARM', 'LEFT SHOULDER', 'LEFT ELBOW', 'LEFT ARM', 'RIGHT HIP', 'RIGHT KNEE', 'RIGHT LEG', 'LEFT HIP', 'LEFT KNEE', 'LEFT LEG', 'RIGHT EYE', 'LEFT EYE', 'RIGHT EAR', 'LEFT EAR'];
const poseFrameByKey = (key) => {
  const norm = (s) => String(s).toLowerCase().replace(/[\s_]+/g, '-');
  const p = posesFx.poses.find((q) => norm(q.id) === norm(key));
  let idx = -1;
  for (let k = seqFx.frames.length - 1; k >= 0; k--) if (norm(seqFx.frames[k].phase) === norm(p.phase)) { idx = k; break; }
  return idx;
};
const EXPECT_POSE_FRAMES = {
  ready: poseFrameByKey('ready'),
  elevation: poseFrameByKey('elevation'),
  strike: poseFrameByKey('strike'),
  follow: poseFrameByKey('follow'),
  recover: poseFrameByKey('recover'),
};
//[[PART2]]
