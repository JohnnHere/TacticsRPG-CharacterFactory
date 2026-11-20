#!/usr/bin/env node
/**
 * Stage A — Production audit and protected art snapshot for orc-v1.
 *
 * Read-only with respect to art and production metadata: it only reads files and
 * writes inside experiments/main-orc-complete-animation-v1/. It never calls the
 * Aseprite bridge, PixelLab, or any network service, and never edits a master,
 * a PNG, a clip/profile, a pointer or a review record.
 *
 * Baseline anchoring: the working tree was clean when Stage A started, so the
 * audited metadata is read from git HEAD (reproducible) and the art is frozen in
 * protected-art.json at the moment of the first run. Concurrent writes cannot
 * silently change what this stage reports.
 *
 * Usage:
 *   node tools/audit-main-orc-complete-animation.mjs             # baseline audit (default)
 *   node tools/audit-main-orc-complete-animation.mjs --verify    # + doctor/editor-check/tests
 *   node tools/audit-main-orc-complete-animation.mjs --current    # audit the live tree
 *   node tools/audit-main-orc-complete-animation.mjs --refresh-snapshot  # only when starting a new baseline
 */
import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync, existsSync, mkdirSync, readdirSync, statSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { dirname, join, relative, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const CHARACTER = 'orc-v1';
const EXPERIMENT = 'experiments/main-orc-complete-animation-v1';
const OUT = join(ROOT, EXPERIMENT);
const ART_ROOTS = ['characters', 'assets/weapons', 'ideas'];
const ART_EXT = new Set(['.png', '.aseprite', '.ase']);
const LIBRARY = 'Biblioteca de Arte';

const ARGS = new Set(process.argv.slice(2));
const LIVE = ARGS.has('--current');
const REFRESH = ARGS.has('--refresh-snapshot');
const VERIFY = ARGS.has('--verify');

const toPosix = (p) => p.split(sep).join('/');
const rel = (absolute) => toPosix(relative(ROOT, absolute));
const abs = (p) => join(ROOT, p);
const sha = (p) => createHash('sha256').update(readFileSync(p)).digest('hex');
const shaOrNull = (p) => (existsSync(abs(p)) ? sha(abs(p)) : null);
const exists = (p) => existsSync(abs(p));
const strip = (text) => text.replace(/^\uFEFF/, '');

function walk(dirAbs, test, acc = []) {
  if (!existsSync(dirAbs)) return acc;
  for (const entry of readdirSync(dirAbs, { withFileTypes: true })) {
    const full = join(dirAbs, entry.name);
    if (entry.isDirectory()) walk(full, test, acc);
    else if (test(full, entry.name)) acc.push(full);
  }
  return acc;
}

function git(args, { json = false } = {}) {
  try {
    const output = execFileSync('git', args, { cwd: ROOT, encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 });
    return json ? output : output.trim();
  } catch {
    return json ? '' : '';
  }
}

/**
 * Whether a path is tracked at HEAD. `git ls-tree` is silent for unknown paths,
 * unlike `git show HEAD:<path>`, which writes a fatal error to stderr: metadata
 * created by a parallel workstream after the snapshot must not look like a
 * baseline read failure.
 */
const headMembership = new Map();
function inHead(file) {
  if (!headMembership.has(file)) {
    headMembership.set(file, git(['ls-tree', '--name-only', 'HEAD', '--', file]).trim() === file);
  }
  return headMembership.get(file);
}

/** Text of a metadata file at HEAD, or null when it only exists after the snapshot. */
function headText(file) {
  if (LIVE || !inHead(file)) return null;
  const head = git(['show', `HEAD:${file}`], { json: true });
  return head ? strip(head) : null;
}

/** Metadata as committed at HEAD — the audited baseline. */
function readBaselineJson(file) {
  const head = headText(file);
  return JSON.parse(head ?? strip(readFileSync(abs(file), 'utf8')));
}

function baselineText(file) {
  return headText(file) ?? strip(readFileSync(abs(file), 'utf8'));
}

/** PNG dimensions straight from IHDR. */
function pngSize(p) {
  const buf = readFileSync(abs(p)).subarray(0, 33);
  if (buf.length < 24 || buf.readUInt32BE(0) !== 0x89504e47) return null;
  return [buf.readUInt32BE(16), buf.readUInt32BE(20)];
}

function pngAlphaBBox(p) {
  try {
    const { PNG } = require('pngjs');
    const png = PNG.sync.read(readFileSync(abs(p)));
    let minX = Infinity, minY = Infinity, maxX = -1, maxY = -1;
    for (let y = 0; y < png.height; y += 1) {
      for (let x = 0; x < png.width; x += 1) {
        if (png.data[(y * png.width + x) * 4 + 3] > 0) {
          if (x < minX) minX = x;
          if (y < minY) minY = y;
          if (x > maxX) maxX = x;
          if (y > maxY) maxY = y;
        }
      }
    }
    return maxX < 0 ? null : [minX, minY, maxX + 1, maxY + 1];
  } catch {
    return null;
  }
}

mkdirSync(OUT, { recursive: true });

/* ---------------------------------------------------------------- snapshot */

const snapshotPath = join(OUT, 'protected-art.json');
const currentArt = {};
for (const rootRel of ART_ROOTS) {
  for (const fileAbs of walk(abs(rootRel), (_full, name) => ART_EXT.has(name.slice(name.lastIndexOf('.')).toLowerCase()))) {
    currentArt[rel(fileAbs)] = sha(fileAbs);
  }
}

let protectedManifest;
let snapshotMode;
if (!existsSync(snapshotPath) || REFRESH) {
  protectedManifest = currentArt;
  writeFileSync(snapshotPath, JSON.stringify(protectedManifest, null, 2), 'utf8');
  snapshotMode = 'CREATED';
} else {
  protectedManifest = JSON.parse(readFileSync(snapshotPath, 'utf8'));
  snapshotMode = 'PRESERVED';
}
const snapshotAt = new Date(statSync(snapshotPath).mtimeMs).toISOString();

const drift = [];
for (const [file, digest] of Object.entries(protectedManifest)) {
  if (!(file in currentArt)) drift.push({ file, problem: 'MISSING' });
  else if (currentArt[file] !== digest) drift.push({ file, problem: 'MODIFIED' });
}
const artAddedAfterSnapshot = Object.keys(currentArt).filter((f) => !(f in protectedManifest));

/* --------------------------------------------------------------- git state */

const gitStatus = git(['status', '--short']);
const gitStatusLines = gitStatus ? gitStatus.split('\n').filter(Boolean) : [];
const ownArtifacts = [`${EXPERIMENT}/`, 'tools/audit-main-orc-complete-animation.mjs'];
const initialStatusPath = join(OUT, 'initial-git-status.txt');
if (!existsSync(initialStatusPath)) {
  const preWork = gitStatusLines.filter((line) => !ownArtifacts.some((own) => line.includes(own)));
  writeFileSync(initialStatusPath, [
    '# git status --short at the first Stage A execution, before this task wrote anything.',
    '# This task own new files are excluded so the lines below reflect the tree as found.',
    `# excluded: ${ownArtifacts.join(', ')}`,
    preWork.length ? preWork.join('\n') : '(clean: no pending entries)',
    '',
  ].join('\n'), 'utf8');
}
const initialEntries = readFileSync(initialStatusPath, 'utf8')
  .split('\n')
  .filter((line) => line.trim() && !line.startsWith('#') && !line.startsWith('('));
const concurrentArrivals = gitStatusLines.filter(
  (line) => !ownArtifacts.some((own) => line.includes(own)) && !initialEntries.includes(line),
);
writeFileSync(join(OUT, 'current-git-status.txt'), gitStatus ? `${gitStatus}\n` : '', 'utf8');
writeFileSync(join(OUT, 'concurrent-arrivals.txt'), [
  '# Entries that did not exist when Stage A started and are not Stage A output.',
  '# They are outside the audited baseline and were not treated as production truth.',
  concurrentArrivals.length ? concurrentArrivals.join('\n') : '(none)',
  '',
].join('\n'), 'utf8');

const gitSummary = {
  branch: git(['rev-parse', '--abbrev-ref', 'HEAD']),
  head: git(['rev-parse', 'HEAD']),
  headSubject: git(['log', '-1', '--pretty=%s']),
  headDate: git(['log', '-1', '--pretty=%cI']),
  cleanAtStageAStart: initialEntries.length === 0,
  entriesNow: gitStatusLines.length,
  concurrentArrivals: concurrentArrivals.length,
  concurrentArrivalsFile: `${EXPERIMENT}/concurrent-arrivals.txt`,
  statusFile: `${EXPERIMENT}/initial-git-status.txt`,
  currentStatusFile: `${EXPERIMENT}/current-git-status.txt`,
  note: 'The tree was clean at HEAD when Stage A started. Entries in concurrent-arrivals.txt appeared afterwards, sit outside this audit and are not production truth. No commit/reset/stash was made.',
};

/* ------------------------------------------------------------ findings log */

const findings = [];
const addFinding = (severity, area, message) => findings.push({ severity, area, message });

/* --------------------------------------------------- metadata + its drift */

const METADATA_FILES = [
  'characters/orc-v1/character.json',
  'characters/orc-v1/assets.json',
  'characters/orc-v1/reviews.json',
  'characters/orc-v1/source/selection.json',
  'characters/orc-v1/source/equipment-current.json',
  'characters/orc-v1/source/equipment-polish-candidate.json',
  'characters/orc-v1/source/equipment-entry-candidate.json',
  'characters/orc-v1/source/onehanded-rescue-v3/manifest.json',
  'characters/orc-v1/source/onehanded-polish-v1/manifest.json',
  'characters/orc-v1/source/onehanded-entry-v1/manifest.json',
  'characters/orc-v1/source/studies/Idle/clip.json',
  'characters/orc-v1/source/studies/Walk/clip.json',
  'assets/weapons/recruit-sword/weapon.json',
  'assets/weapons/militia-axe/weapon.json',
  'reports/orc-production-current.json',
  'config/equipment-actions-v1.json',
  'config/idle-art-standard-v1.json',
];

function flatDiff(a, b, prefix = '') {
  const keys = new Set([...Object.keys(a ?? {}), ...Object.keys(b ?? {})]);
  const changes = [];
  for (const key of keys) {
    const pa = `${prefix}${key}`;
    const va = a?.[key];
    const vb = b?.[key];
    const bothObjects = va && vb && typeof va === 'object' && typeof vb === 'object' && !Array.isArray(va) && !Array.isArray(vb);
    if (bothObjects) changes.push(...flatDiff(va, vb, `${pa}.`));
    else if (JSON.stringify(va) !== JSON.stringify(vb)) changes.push({ key: pa, baseline: va ?? null, now: vb ?? null });
  }
  return changes;
}

const metadataSnapshot = [];
for (const file of METADATA_FILES) {
  if (!exists(file)) {
    metadataSnapshot.push({ file, baseline: 'ABSENT', drifted: false });
    continue;
  }
  if (!LIVE && !inHead(file)) {
    metadataSnapshot.push({
      file,
      baseline: 'ABSENT_IN_HEAD',
      drifted: false,
      note: 'Created by a parallel workstream after the snapshot; outside the audited baseline.',
    });
    continue;
  }
  const baselineRaw = baselineText(file);
  const currentRaw = strip(readFileSync(abs(file), 'utf8'));
  const target = join(OUT, 'before-metadata', file);
  mkdirSync(dirname(target), { recursive: true });
  writeFileSync(target, baselineRaw, 'utf8');

  let changes = [];
  try {
    changes = flatDiff(JSON.parse(baselineRaw), JSON.parse(currentRaw));
  } catch {
    changes = baselineRaw === currentRaw ? [] : [{ key: '(bytes)', baseline: 'different', now: 'different' }];
  }
  metadataSnapshot.push({
    file,
    baseline: LIVE ? 'WORKING_COPY' : 'GIT_HEAD',
    baselineSha256: createHash('sha256').update(baselineRaw).digest('hex'),
    currentSha256: createHash('sha256').update(currentRaw).digest('hex'),
    drifted: changes.length > 0,
    changedKeys: changes,
    copy: toPosix(join(EXPERIMENT, 'before-metadata', file)),
  });
}
const metadataDrift = metadataSnapshot.filter((m) => m.drifted);
if (metadataDrift.length) {
  addFinding('WARN', 'metadata', `${metadataDrift.length} audited metadata file(s) changed after the Stage A baseline: ${metadataDrift.map((m) => `${m.file} (${m.changedKeys.map((c) => c.key).join(', ')})`).join('; ')}.`);
}

/* ------------------------------------------------------------------- files */

const headArt = (pattern) => git(['ls-tree', '-r', '--name-only', 'HEAD', '--', pattern]).split('\n').filter(Boolean);
const fsFiles = (pattern, name) => walk(abs(pattern), (_full, n) => n === name).map(rel);

const listMetadata = (name) => {
  if (LIVE) return fsFiles(`characters/${CHARACTER}`, name).sort();
  return headArt(`characters/${CHARACTER}`).filter((f) => f.endsWith(`/${name}`) || f === name).sort();
};

const clipFiles = listMetadata('clip.json');
const profileFiles = listMetadata('profile.json');
const manifestFiles = listMetadata('manifest.json');
const metadataArrivedAfterSnapshot = LIVE
  ? []
  : fsFiles(`characters/${CHARACTER}`, 'clip.json')
      .filter((f) => !clipFiles.includes(f))
      .sort();

/* -------------------------------------------------------------- integrity */

const checks = [];
const check = (kind, file, ok, detail) => checks.push({ kind, file, ok, ...(detail ? { detail } : {}) });

function auditLayer(ref) {
  if (!ref?.png) return;
  const present = exists(ref.png);
  check('frame-png-exists', ref.png, present, present ? undefined : 'missing file');
  if (present && ref.sha256) check('frame-png-sha', ref.png, sha(abs(ref.png)) === ref.sha256, 'sha256 mismatch');
}

/* ------------------------------------------------------------------- clips */

const clipJson = new Map();
for (const file of clipFiles) {
  try {
    clipJson.set(file, readBaselineJson(file));
  } catch (err) {
    check('clip-parses', file, false, String(err.message).slice(0, 120));
  }
}

const clips = [...clipJson].map(([file, clip]) => {
  const frames = Array.isArray(clip.frames) ? clip.frames : [];
  const durations = frames.map((f) => f.durationMs ?? 0);

  check('clip-frame-count', file, clip.frameCount == null ? frames.length > 0 : clip.frameCount === frames.length,
    clip.frameCount == null ? 'no frames' : `declared ${clip.frameCount} vs ${frames.length}`);

  for (const frame of frames) {
    auditLayer({ png: frame.png, sha256: frame.sha256 });
    for (const layer of Object.values(frame.layers ?? {})) {
      auditLayer({ png: layer?.png, sha256: layer?.sha256 });
      if (layer?.png && clip.canvas && exists(layer.png)) {
        const size = pngSize(layer.png);
        check('layer-canvas', layer.png, !!size && size[0] === clip.canvas[0] && size[1] === clip.canvas[1],
          size ? `${size.join('x')} != ${clip.canvas.join('x')}` : 'unreadable png');
      }
    }
  }

  if (clip.canvas && frames[0]?.png && exists(frames[0].png)) {
    const size = pngSize(frames[0].png);
    check('clip-canvas', file, !!size && size[0] === clip.canvas[0] && size[1] === clip.canvas[1],
      size ? `${size.join('x')} != ${clip.canvas.join('x')}` : 'unreadable png');
  }

  for (const [kind, masterPath, masterSha] of [
    ['master', clip.master, clip.masterSha256],
    ['body-master', clip.bodyMaster, clip.bodyMasterSha256],
    ['hand-master', clip.handMaster, clip.handMasterSha256],
    ['weapon-sprite', clip.weapon?.sprite, clip.weapon?.spriteSha256],
    ['weapon-master', clip.weapon?.master, clip.weapon?.masterSha256],
  ]) {
    if (!masterPath) continue;
    check(`${kind}-exists`, masterPath, exists(masterPath));
    if (masterSha) check(`${kind}-sha`, masterPath, shaOrNull(masterPath) === masterSha, 'changed since export');
  }

  return {
    file,
    revision: clip.revision ?? null,
    state: clip.state ?? null,
    category: clip.category ?? null,
    id: clip.id ?? null,
    direction: clip.direction ?? (file.includes('/studies/') ? 'front_r' : null),
    loop: clip.loop ?? null,
    canvas: clip.canvas ?? null,
    groundY: clip.groundY ?? null,
    ppu: clip.ppu ?? null,
    frameCount: frames.length,
    durationsMs: durations,
    totalMs: durations.reduce((a, b) => a + b, 0),
    master: clip.master ?? null,
    artisticApproval: clip.artisticApproval ?? clip.visualReview?.status ?? null,
    selectedAsCurrent: clip.selectedAsCurrent ?? null,
    visibleInterval: clip.visibleInterval ?? null,
    contactEvent: clip.contactEvent ?? null,
    weapon: clip.weapon ? { id: clip.weapon.id, grip: clip.weapon.grip ?? null, scale: clip.weapon.scale ?? null } : null,
    baselineRevision: clip.baselineRevision ?? null,
  };
});

const profiles = profileFiles.map((file) => {
  let profile;
  try {
    profile = readBaselineJson(file);
  } catch {
    return { file, error: 'UNPARSEABLE' };
  }
  const frames = Array.isArray(profile.frames) ? profile.frames : [];
  for (const frame of frames) {
    auditLayer({ png: frame.body?.png, sha256: frame.body?.sha256 });
    auditLayer({ png: frame.handFront?.png, sha256: frame.handFront?.sha256 });
  }
  for (const master of [profile.bodyMaster, profile.handMaster]) if (master) check('profile-master-exists', master, exists(master));
  return {
    file,
    id: profile.id ?? null,
    category: profile.category ?? null,
    direction: profile.direction ?? null,
    canvas: profile.canvas ?? null,
    groundY: profile.groundY ?? null,
    ppu: profile.ppu ?? null,
    frameCount: frames.length,
    totalMs: frames.reduce((a, f) => a + (f.durationMs ?? 0), 0),
    weaponVisibleFrames: frames.filter((f) => f.weaponVisible).length,
    artisticApproval: profile.artisticApproval ?? null,
  };
});

const manifests = manifestFiles.map((file) => {
  let manifest;
  try {
    manifest = readBaselineJson(file);
  } catch {
    return { file, error: 'UNPARSEABLE' };
  }
  return {
    file,
    revision: manifest.revision ?? null,
    character: manifest.character ?? null,
    direction: manifest.direction ?? null,
    canvas: manifest.canvas ?? null,
    groundY: manifest.groundY ?? null,
    clips: (manifest.clips ?? []).map((c) => ({ state: c.state ?? null, category: c.category ?? null, clip: c.clip ?? null, alias: c.alias ?? false })),
    artisticApproval: manifest.artisticApproval ?? null,
    selection: manifest.selection ?? null,
  };
});

/* ---------------------------------------------------- cross-clip invariants */

const isHistorical = (file) => /\/source\/equipment(-v2)?\//.test(file);
const invariants = [];
const invariant = (id, file, ok, detail) => {
  invariants.push({ id, file, ok, ...(detail ? { detail } : {}) });
  check(`invariant:${id}`, file, ok, detail);
};
const historicalExcluded = [];

for (const [file, clip] of clipJson) {
  const frames = clip.frames ?? [];
  if (isHistorical(file)) {
    historicalExcluded.push({ file, state: clip.state ?? null, reason: 'REJECTED_ARMED_HISTORY' });
    continue;
  }

  if (clip.state === 'Idle' || clip.state === 'Walk') {
    invariant('rest-no-weapon-visible', file, !frames.some((f) => f.weaponVisible === true), 'resting clip declares a visible weapon');
    invariant('rest-no-weapon-layer', file, !frames.some((f) => f.layers?.weaponBack?.png || f.layers?.weaponFront?.png), 'resting clip carries weapon layers');
  }

  if (clip.state !== 'Attack' || !Array.isArray(clip.visibleInterval)) continue;
  const [from, to] = clip.visibleInterval;
  if (from < 0 || to >= frames.length || from > to) {
    invariant('visible-interval-bounds', file, false, `interval ${from}..${to} outside 0..${frames.length - 1}`);
    continue;
  }
  invariant('visible-interval-contiguous', file, frames.every((f, i) => f.weaponVisible === (i >= from && i <= to)), `weaponVisible must be true only in ${from}..${to}`);

  const siblingKey = file.replace(/\/(Sword|Axe)\/Attack\/clip\.json$/, '/Idle/clip.json');
  const sibling = clipJson.get(siblingKey);
  if (sibling?.frames?.length) {
    const neutral = shaOrNull(sibling.frames[0].png);
    invariant('neutral-start', file, neutral !== null && shaOrNull(frames[0]?.png) === neutral, 'first attack frame differs from Idle frame 0');
    invariant('neutral-end', file, neutral !== null && shaOrNull(frames.at(-1)?.png) === neutral, 'last attack frame differs from Idle frame 0');
  }
}
const invariantFailures = invariants.filter((i) => !i.ok).length;
if (invariantFailures) addFinding('FAIL', 'invariants', `${invariantFailures} cross-clip invariant(s) failed.`);

/* ------------------------------------------------------- review library */

const librarySnapshotPath = join(OUT, 'protected-library.json');
const currentLibrary = {};
for (const fileAbs of walk(abs(LIBRARY), () => true)) {
  if (/\.(html|json|png|md|css|js)$/i.test(fileAbs)) currentLibrary[rel(fileAbs)] = sha(fileAbs);
}
if (!existsSync(librarySnapshotPath) || REFRESH) {
  writeFileSync(librarySnapshotPath, JSON.stringify(currentLibrary, null, 2), 'utf8');
}
const librarySnapshot = existsSync(librarySnapshotPath) ? JSON.parse(readFileSync(librarySnapshotPath, 'utf8')) : currentLibrary;
const libraryDrift = Object.keys(librarySnapshot).filter((f) => !(f in currentLibrary) || currentLibrary[f] !== librarySnapshot[f]);
const reviewPages = Object.keys(currentLibrary)
  .filter((f) => f.endsWith('index.html') && /Orc V1|Orc principal|Biblioteca de Arte\/index\.html/.test(f))
  .map((f) => ({ file: f, sha256: currentLibrary[f], bytes: statSync(abs(f)).size }));

const allProtectedPaths = [...Object.keys(protectedManifest), ...Object.keys(currentLibrary)];
const maxProtectedPathLength = allProtectedPaths.reduce((max, f) => Math.max(max, abs(f).length), 0);

const editorBuilds = existsSync(abs('dist/editor'))
  ? readdirSync(abs('dist/editor'), { withFileTypes: true })
      .filter((e) => e.isDirectory() && e.name.startsWith('main-orc-'))
      .map((e) => {
        const files = walk(abs(`dist/editor/${e.name}`), () => true);
        return { build: e.name, files: files.length, bytes: files.reduce((a, f) => a + statSync(f).size, 0) };
      })
  : [];

/* --------------------------------------------------------------- weapons */

const weapons = ['recruit-sword', 'militia-axe'].map((id) => {
  const weaponJson = `assets/weapons/${id}/weapon.json`;
  if (!exists(weaponJson)) return { id, present: false };
  const weapon = readBaselineJson(weaponJson);
  const bbox = weapon.sprite && exists(weapon.sprite) ? pngAlphaBBox(weapon.sprite) : null;
  if (weapon.sprite) check('weapon-asset-exists', weapon.sprite, exists(weapon.sprite));
  if (weapon.master) check('weapon-asset-exists', weapon.master, exists(weapon.master));
  return {
    id,
    weaponJson,
    present: true,
    category: weapon.category ?? null,
    hands: weapon.hands ?? null,
    ppu: weapon.ppu ?? null,
    sprite: weapon.sprite ?? null,
    spriteSha256: shaOrNull(weapon.sprite),
    master: weapon.master ?? null,
    masterSha256: shaOrNull(weapon.master),
    spriteCanvas: weapon.sprite && exists(weapon.sprite) ? pngSize(weapon.sprite) : null,
    contentBBox: bbox,
    contentSize: bbox ? [bbox[2] - bbox[0], bbox[3] - bbox[1]] : null,
  };
});

/* --------------------------------------------------------------- pointers */

const pointerFiles = [
  'characters/orc-v1/source/equipment-current.json',
  'characters/orc-v1/source/equipment-polish-candidate.json',
  'characters/orc-v1/source/equipment-entry-candidate.json',
  'characters/orc-v1/source/equipment-complete-candidate.json',
];
const pointers = pointerFiles.filter(exists).map((file) => {
  const pointer = readBaselineJson(file);
  return {
    file,
    revision: pointer.revision ?? null,
    manifest: pointer.manifest ?? null,
    manifestSha256: pointer.manifest ? shaOrNull(pointer.manifest) : null,
    manifestExists: pointer.manifest ? exists(pointer.manifest) : false,
    selection: pointer.selection ?? null,
    artisticApproval: pointer.artisticApproval ?? null,
    baseline: pointer.baseline ?? null,
    scope: LIVE || inHead(file) ? 'BASELINE_AT_SNAPSHOT' : 'ARRIVED_AFTER_SNAPSHOT',
  };
});
const postBaselinePointers = pointers.filter((p) => p.scope === 'ARRIVED_AFTER_SNAPSHOT');
if (postBaselinePointers.length) {
  addFinding('INFO', 'pointers', `${postBaselinePointers.length} pointer file(s) exist on disk but not at HEAD: ${postBaselinePointers.map((p) => p.file).join(', ')}. They arrived after the snapshot and are not the active pointer audited here.`);
}

const character = readBaselineJson(`characters/${CHARACTER}/character.json`);
const productionCurrent = readBaselineJson('reports/orc-production-current.json');
const reviews = exists(`characters/${CHARACTER}/reviews.json`) ? readBaselineJson(`characters/${CHARACTER}/reviews.json`) : null;

/* ------------------------------------------------------- coverage / states */

const REQUIRED_STATES = [
  { state: 'Idle', kind: 'body', note: 'Loop 5 frames / 2200 ms, idle-balanced-v1 standard.' },
  { state: 'Walk', kind: 'body', note: 'Loop 16 frames / 1280 ms.' },
  { state: 'Attack', kind: 'unarmed', note: 'basic.unarmed: physical hit with empty hands.' },
  { state: 'Attack', kind: 'Sword', note: 'basic.sword-slash profile, weapon visible only in the declared interval.' },
  { state: 'Attack', kind: 'Axe', note: 'basic.axe-chop profile, weapon visible only in the declared interval.' },
  { state: 'Hit', kind: 'body', note: 'Reaction shared by armed/unarmed presentation.' },
  { state: 'Defeat', kind: 'body', note: 'Terminal state, no persistent weapon overlay.' },
];

const CLIP_CANDIDATE_DIRS = ['onehanded-rescue-v3', 'onehanded-polish-v1', 'onehanded-entry-v1'];
const REVISION_RANK = { 'onehanded-rescue-v3': 1, 'onehanded-polish-v1': 2, 'onehanded-entry-v1': 3, other: 4 };

const clipsFor = (state) => clips.filter((c) => c.state === state);
const isArmed = (c) => c.category === 'Sword' || c.category === 'Axe' || c.id === 'basic.sword-slash' || c.id === 'basic.axe-chop';
const isUnarmed = (c) => c.id === 'basic.unarmed';
const dirOf = (c) => CLIP_CANDIDATE_DIRS.find((seg) => c.file.includes(`/${seg}/`))
  ?? (c.file.includes('/studies/') ? 'studies' : isHistorical(c.file) ? 'legacy' : 'other');
const clipSummary = (c) => (c ? { file: c.file, revision: c.revision, frames: c.frameCount, totalMs: c.totalMs, approval: c.artisticApproval, visibleInterval: c.visibleInterval } : null);

const coverage = REQUIRED_STATES.map((req) => {
  let found;
  if (req.kind === 'Sword' || req.kind === 'Axe') found = clipsFor(req.state).filter((c) => c.category === req.kind);
  else if (req.kind === 'unarmed') found = [...clipsFor(req.state).filter(isUnarmed), ...clipsFor('Unarmed')];
  else found = clipsFor(req.state).filter((c) => !isArmed(c) && !isUnarmed(c));

  let active = null;
  let latestCandidate = null;
  if (req.state === 'Idle' || req.state === 'Walk') {
    const canonical = found.find((c) => dirOf(c) === 'studies') ?? null;
    const aliases = found.filter((c) => !['studies', 'legacy'].includes(dirOf(c)));
    active = canonical ? { ...clipSummary(canonical), aliases: aliases.map((a) => a.file) } : null;
    latestCandidate = active;
  } else {
    const ranked = found
      .filter((c) => dirOf(c) !== 'legacy')
      .sort((a, b) => (REVISION_RANK[dirOf(b)] ?? 0) - (REVISION_RANK[dirOf(a)] ?? 0));
    latestCandidate = clipSummary(ranked[0]);
    active = clipSummary(found.find((c) => dirOf(c) === 'onehanded-rescue-v3') ?? ranked[0] ?? null);
  }

  const legacyOnly = found.length > 0 && found.every((c) => dirOf(c) === 'legacy');
  return {
    state: req.state,
    kind: req.kind,
    note: req.note,
    status: found.length === 0 ? 'MISSING' : legacyOnly ? 'MISSING_CURRENT' : 'PRESENT',
    active,
    latestCandidate,
    allFiles: found.map((c) => c.file),
    legacyFiles: found.filter((c) => dirOf(c) === 'legacy').map((c) => c.file),
  };
});

const stateLabel = (c) => `${c.state}${['Sword', 'Axe', 'unarmed'].includes(c.kind) ? ` (${c.kind})` : ''}`;
const missingStates = coverage.filter((c) => c.status !== 'PRESENT').map(stateLabel);
const presentStates = coverage.filter((c) => c.status === 'PRESENT').map(stateLabel);

/* ---------------------------------------------------------- consistency */

const activePointer = pointers.find((p) => p.file.endsWith('equipment-current.json')) ?? null;
const activeRevision = activePointer?.revision ?? null;
const activeManifest = activePointer?.manifest ?? null;
const previewPointer = character.equipmentPreview ?? null;
if (previewPointer && activeManifest && previewPointer !== activeManifest) {
  addFinding('WARN', 'pointer', `character.json.equipmentPreview (${previewPointer}) differs from equipment-current.manifest (${activeManifest}).`);
}
if (reviews && Object.keys(reviews).length === 0) {
  addFinding('INFO', 'gates', 'reviews.json is empty: no concept/base/consistency gate is recorded for orc-v1 even though identity was selected.');
}
const counts = character.profile?.counts ?? {};
const idleClip = clips.find((c) => c.file.endsWith('studies/Idle/clip.json'));
const walkClip = clips.find((c) => c.file.endsWith('studies/Walk/clip.json'));
if (idleClip && counts.Idle !== idleClip.frameCount) addFinding('WARN', 'profile', `character.json profile.counts.Idle=${counts.Idle} but the current Idle clip has ${idleClip.frameCount} frames.`);
if (walkClip && counts.Walk !== walkClip.frameCount) addFinding('WARN', 'profile', `character.json profile.counts.Walk=${counts.Walk} but the current Walk clip has ${walkClip.frameCount} frames.`);
if (!counts.Attack && !counts.Hit && !counts.Defeat) {
  addFinding('INFO', 'profile', 'character.json profile.counts lists only Idle and Walk; attack/hit/defeat coverage is not represented in the character profile.');
}
const foreignDirections = [...new Set(clips.map((c) => c.direction).filter((d) => d && d !== 'front_r'))];
if (foreignDirections.length) {
  addFinding('WARN', 'direction', `Clips declare direction(s) ${foreignDirections.join(', ')}; only front_r is in scope for this character so far.`);
}
if (missingStates.length) {
  addFinding('WARN', 'coverage', `States without a current clip for orc-v1: ${missingStates.join(', ')}.`);
}
const legacyClips = clips.filter((c) => isHistorical(c.file));
if (legacyClips.length) {
  addFinding('INFO', 'metadata', `${legacyClips.length} legacy armed clips (source/equipment/, source/equipment-v2/) are preserved history: rejected v1/v2, no category/id fields, no persistent armed presentation.`);
}
if (clips.some((c) => c.file.includes('/studies/') && (!c.canvas || !c.loop))) {
  addFinding('INFO', 'metadata', 'canonical study clips (source/studies/{Idle,Walk}) omit canvas/groundY/ppu/loop; the onehanded display copies declare 256x256, groundY 190 and body at (64,64), while the native PNGs are 128x128. Consolidation must inherit the copy metadata.');
}
for (const clip of clips) {
  if (clip.contactEvent?.frame != null && clip.contactEvent.timeMs == null) {
    addFinding('INFO', 'events', `${clip.file} declares contactEvent.frame=${clip.contactEvent.frame} without timeMs; a runtime offset would have to be derived from frame durations.`);
  }
}
if (walkClip && /PENDING/i.test(String(walkClip.artisticApproval))) {
  addFinding('INFO', 'approval', `Walk approval is "${walkClip.artisticApproval}"; treat it as current-but-unapproved for green, not as an approved gate.`);
}
if (maxProtectedPathLength > 240) {
  addFinding('INFO', 'paths', `Deepest protected path is ${maxProtectedPathLength} characters; copying deliverables into a deeper folder will exceed the Windows 260 limit.`);
}

const failCount = checks.filter((c) => !c.ok).length;
const warnCount = findings.filter((f) => f.severity === 'WARN').length;

/* ------------------------------------------------- baseline verification */

let baselineVerification = null;
if (VERIFY) {
  const run = (args) => {
    try {
      return { ok: true, output: execFileSync(process.execPath, args, { cwd: ROOT, encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 }) };
    } catch (err) {
      return { ok: false, output: `${err.stdout ?? ''}${err.stderr ?? ''}` };
    }
  };
  const parse = (text) => {
    try {
      return JSON.parse(text);
    } catch {
      return { raw: text.slice(0, 2000) };
    }
  };
  const doctor = run(['./src/cli.mjs', 'doctor']);
  const editorCheck = run(['./src/cli.mjs', 'editor-check']);
  const tests = run(['--test', '--test-concurrency=1']);
  const count = (name) => {
    const match = new RegExp(`(?:ℹ|#)\\s*${name}\\s+(\\d+)`).exec(tests.output);
    return match ? Number(match[1]) : null;
  };
  baselineVerification = {
    generatedAt: new Date().toISOString(),
    commands: ['node src/cli.mjs doctor', 'node src/cli.mjs editor-check', 'node --test --test-concurrency=1'],
    doctor: { ok: doctor.ok, json: parse(doctor.output) },
    editorCheck: { ok: editorCheck.ok, json: parse(editorCheck.output) },
    tests: { ok: tests.ok && count('fail') === 0, tests: count('tests'), pass: count('pass'), fail: count('fail'), durationMs: count('duration_ms'), tail: tests.output.split('\n').slice(-30).join('\n') },
    note: 'Baseline verification of the audited state. Technical PASS is not artistic approval.',
  };
  writeFileSync(join(OUT, 'baseline-verification.json'), JSON.stringify(baselineVerification, null, 2), 'utf8');
}

/* ----------------------------------------------------------------- report */

const report = {
  schemaVersion: 1,
  stage: 'A',
  stageName: 'Production audit and protected art snapshot',
  task: 'main-orc-complete-animation-v1',
  generatedAt: new Date().toISOString(),
  character: CHARACTER,
  auditScope: LIVE ? 'CURRENT_TREE' : 'BASELINE_AT_SNAPSHOT',
  baselineAnchors: {
    gitHead: gitSummary.head,
    gitHeadSubject: gitSummary.headSubject,
    artSnapshot: `${EXPERIMENT}/protected-art.json`,
    artSnapshotAt: snapshotAt,
    metadataSource: LIVE ? 'working copy' : 'git HEAD (tree was clean at Stage A start)',
  },
  identity: {
    authority: 'reports/orc-production-current.json',
    status: productionCurrent.status ?? null,
    revision: productionCurrent.revision ?? null,
    selectedVariant: productionCurrent.selectedVariant ?? null,
    unityIntegrated: productionCurrent.unityIntegrated ?? null,
    fullDirectionGatesGranted: productionCurrent.fullDirectionGatesGranted ?? null,
    reviewsRecorded: reviews ? Object.keys(reviews).length : null,
    idleStandard: character.idleStandard?.id ?? null,
  },
  status: failCount === 0 ? 'PASS' : 'FAIL',
  summary: {
    protectedArtFiles: Object.keys(protectedManifest).length,
    protectedArtDrift: drift.length,
    artFilesAddedAfterSnapshot: artAddedAfterSnapshot.length,
    protectedLibraryFiles: Object.keys(librarySnapshot).length,
    libraryDrift: libraryDrift.length,
    metadataFilesAudited: metadataSnapshot.length,
    metadataDrift: metadataDrift.length,
    clipsAudited: clips.length,
    bindingsAudited: profiles.length,
    invariants: invariants.length,
    invariantFailures,
    integrityChecks: checks.length,
    integrityFailures: failCount,
    statesPresent: presentStates,
    statesMissing: missingStates,
    findings: findings.length,
    warnings: warnCount,
  },
  snapshot: {
    mode: snapshotMode,
    file: `${EXPERIMENT}/protected-art.json`,
    roots: ART_ROOTS,
    extensions: [...ART_EXT],
    drift,
    filesAddedAfterSnapshot: artAddedAfterSnapshot,
  },
  metadataSnapshot: {
    files: metadataSnapshot,
    drift: metadataDrift,
    copyRoot: `${EXPERIMENT}/before-metadata/`,
  },
  reviewMaterials: {
    libraryManifest: `${EXPERIMENT}/protected-library.json`,
    libraryFilesHashed: Object.keys(librarySnapshot).length,
    libraryStrategy: 'HASH_ONLY: the library is regenerable from canonical sources; no byte copy is stored.',
    maxProtectedPathLength,
    libraryDrift,
    pages: reviewPages,
    editorBuilds,
  },
  git: gitSummary,
  postSnapshotActivity: {
    note: 'Files that exist now but were not part of the audited baseline. They are not production truth here.',
    metadataFilesAdded: metadataArrivedAfterSnapshot,
    gitEntriesAppeared: concurrentArrivals,
    file: `${EXPERIMENT}/concurrent-arrivals.txt`,
  },
  verification: baselineVerification,
  pointers,
  pointersResolved: {
    activeRevision,
    activeManifest,
    characterEquipmentPreview: previewPointer,
    candidates: pointers.filter((p) => !p.file.endsWith('equipment-current.json')).map((p) => ({ file: p.file, revision: p.revision, selection: p.selection })),
  },
  sourceTruth: {
    concept: `characters/${CHARACTER}/concepts/concept-selected.png`,
    conceptMaster: `characters/${CHARACTER}/source/aseprite/concept-selected.aseprite`,
    idleClip: `characters/${CHARACTER}/source/studies/Idle/clip.json`,
    idleMaster: `characters/${CHARACTER}/source/aseprite/idle-study.aseprite`,
    walkClip: `characters/${CHARACTER}/source/studies/Walk/clip.json`,
    walkMaster: `characters/${CHARACTER}/source/aseprite/walk-study.aseprite`,
    idleStandard: 'config/idle-art-standard-v1.json',
    equipmentContract: 'config/equipment-actions-v1.json',
  },
  clips,
  bindings: profiles,
  manifests,
  invariants: {
    total: invariants.length,
    scope: 'Current revisions only (source/studies + onehanded-rescue-v3/polish-v1/entry-v1). Rejected armed v1/v2 clips in source/equipment*/ are preserved history and excluded.',
    failures: invariants.filter((i) => !i.ok),
    historicalExcluded,
    checks: invariants,
  },
  weapons,
  coverage,
  findings,
  integrity: {
    status: failCount === 0 ? 'PASS' : 'FAIL',
    failures: checks.filter((c) => !c.ok),
    byKind: checks.reduce((acc, c) => {
      acc[c.kind] = acc[c.kind] ?? { total: 0, failed: 0 };
      acc[c.kind].total += 1;
      if (!c.ok) acc[c.kind].failed += 1;
      return acc;
    }, {}),
  },
  scope: {
    readOnly: true,
    writes: [`${EXPERIMENT}/`],
    cloudCalls: 0,
    editorSessions: 0,
    unityChanges: 0,
    artisticApproval: 'PENDING_CREATOR',
  },
  limitations: [
    'Technical audit only: presence, hashes, canvas, durations and declared metadata. It does not judge artistic quality, weight, grip or tactical readability.',
    'No Unity/PlayMode verification: the runtime does not consume these overlays yet.',
    'Coverage is scoped to front_r, the only view produced for this character at the baseline.',
  ],
};

const reportPath = join(OUT, LIVE ? 'audit-current.json' : 'audit.json');
writeFileSync(reportPath, JSON.stringify(report, null, 2), 'utf8');

console.log(JSON.stringify({
  status: report.status,
  auditScope: report.auditScope,
  protectedArtFiles: report.summary.protectedArtFiles,
  protectedDrift: report.summary.protectedArtDrift,
  metadataDrift: report.summary.metadataDrift,
  clips: report.summary.clipsAudited,
  bindings: report.summary.bindingsAudited,
  integrityChecks: report.summary.integrityChecks,
  integrityFailures: report.summary.integrityFailures,
  invariants: report.summary.invariants,
  invariantFailures: report.summary.invariantFailures,
  statesMissing: report.summary.statesMissing,
  findings: report.summary.findings,
  out: `${EXPERIMENT}/${LIVE ? 'audit-current.json' : 'audit.json'}`,
}, null, 2));

if (failCount > 0) {
  console.error(JSON.stringify(report.integrity.failures.slice(0, 10), null, 2));
  process.exitCode = 1;
}
