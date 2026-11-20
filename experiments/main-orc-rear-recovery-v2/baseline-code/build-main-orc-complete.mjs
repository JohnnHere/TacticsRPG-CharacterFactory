import fs from 'node:fs';
import path from 'node:path';
import { ROOT, DIRECTIONS, hash, readJSON, json, write, slash, loadCharacter } from '../src/core.mjs';
import { decode, measure, validate } from '../src/images.mjs';
import { exportAseprite, inspectAseprite } from '../src/aseprite.mjs';

const sha = rel => hash(fs.readFileSync(path.join(ROOT, rel)));
const exists = rel => fs.existsSync(path.join(ROOT, rel));

const EXP = 'experiments/main-orc-complete-v1';
const OUT_BASE = 'characters/orc-v1/source/complete-v1';
const MASTER_NAT = 'characters/orc-v1/source/aseprite/complete-v1/native';
const MASTER_COMP = 'characters/orc-v1/source/aseprite/complete-v1/composite';
const DIST_PKG = 'dist/orc-v1/complete-v1';

const PHASES = {
  Idle: ['rest-0', 'inhale-1', 'peak-2', 'exhale-3', 'rest-4'],
  Walk: Array.from({ length: 16 }, (_, i) => `walk-step-${String(i).padStart(2, '0')}`),
  Unarmed: ['guard-prep', 'shoulder-coil', 'heavy-gauntlet-impact', 'follow-through', 'recovery-settle'],
  Hit: ['impact-onset', 'peak-recoil', 'stagger-brace', 'recovery-rise', 'recovery-settle'],
  Defeat: ['fatal-stagger', 'knees-buckle', 'drop-to-knees', 'collapse-impact', 'terminal-defeated']
};

const TIMINGS = {
  Idle: [400, 450, 500, 450, 400],
  Walk: Array.from({ length: 16 }, () => 80),
  Unarmed: [80, 110, 50, 90, 120],
  Hit: [45, 95, 115, 95, 100],
  Defeat: [70, 95, 115, 130, 290]
};

const WEAPONS = {
  Sword: {
    id: 'recruit-sword',
    name: 'Espada do Recruta',
    profileId: 'basic.sword-slash',
    grip: [48, 66],
    canvas: [96, 96],
    scale: 1,
    source: 'assets/weapons/recruit-sword/source/rescue-v3/recruit-sword.aseprite',
    sprite: 'assets/weapons/recruit-sword/sprites/rescue-v3/recruit-sword.png',
    visibleInterval: [2, 10],
    contactEvent: { frame: 8, timeMs: 360, status: 'CANDIDATE_VISUAL_ONLY', appliesDamage: false }
  },
  Axe: {
    id: 'militia-axe',
    name: 'Machado de Milícia',
    profileId: 'basic.axe-chop',
    grip: [36, 55],
    canvas: [96, 96],
    scale: 1,
    source: 'assets/weapons/militia-axe/source/rescue-v3/militia-axe.aseprite',
    sprite: 'assets/weapons/militia-axe/sprites/rescue-v3/militia-axe.png',
    visibleInterval: [2, 8],
    contactEvent: { frame: 6, timeMs: 410, status: 'CANDIDATE_VISUAL_ONLY', appliesDamage: false }
  }
};

const LAYER_ORDER = ['weaponBack', 'body', 'weaponFront', 'handFront'];

// 1. Ensure Stage A protection snapshot & audit exist and verify zero protected file tampering
function walkArtFiles(relDir) {
  const fullDir = path.join(ROOT, relDir);
  if (!fs.existsSync(fullDir)) return [];
  const results = [];
  for (const entry of fs.readdirSync(fullDir, { withFileTypes: true })) {
    const p = path.join(fullDir, entry.name);
    const rel = slash(path.relative(ROOT, p));
    if (entry.isDirectory()) results.push(...walkArtFiles(rel));
    else if (/\.(png|aseprite|ase)$/i.test(entry.name)) results.push(rel);
  }
  return results.sort();
}

const protectedRoots = [
  'characters/orc-v1/concepts',
  'characters/orc-v1/source/studies',
  'characters/orc-v1/source/onehanded-rescue-v3',
  'characters/orc-v1/source/onehanded-polish-v1',
  'characters/orc-v1/source/onehanded-entry-v1',
  'characters/orc-pixellab-05',
  'assets/weapons/recruit-sword',
  'assets/weapons/militia-axe'
];

const protectedSnapshotPath = `${EXP}/protected-art.json`;
let protectedMap = {};
if (exists(protectedSnapshotPath)) {
  protectedMap = readJSON(path.join(ROOT, protectedSnapshotPath));
} else {
  for (const r of protectedRoots) {
    for (const f of walkArtFiles(r)) protectedMap[f] = sha(f);
  }
  json(path.join(ROOT, protectedSnapshotPath), protectedMap);
}

for (const [f, expectedSha] of Object.entries(protectedMap)) {
  if (!exists(f) || sha(f) !== expectedSha) {
    throw new Error(`Protected canonical art file altered or missing: ${f}`);
  }
}

// Move any legacy sprites/Actions supplement into source/actions so validate() only sees expectedSlots()
const legacySpritesActions = path.join(ROOT, 'characters/orc-v1/sprites/Actions');
const sourceActionsDir = path.join(ROOT, 'characters/orc-v1/source/actions');
if (fs.existsSync(legacySpritesActions)) {
  fs.mkdirSync(sourceActionsDir, { recursive: true });
  fs.cpSync(legacySpritesActions, sourceActionsDir, { recursive: true });
  fs.rmSync(legacySpritesActions, { recursive: true, force: true });
}

const authoredGeometry = readJSON(path.join(ROOT, `${OUT_BASE}/authored-geometry.json`));
const editorJobs = [];
const allClips = [];
const coverageCells = [];

// Static base job
editorJobs.push({
  id: 'native-static-base',
  source: `${MASTER_NAT}/static-base.aseprite`,
  sourceSha256: sha(`${MASTER_NAT}/static-base.aseprite`),
  profile: { width: 128, height: 128, frames: 1, groundY: 126, alpha: 'binary', requireContent: true, requireTransparency: true },
  compare: ['characters/orc-v1/sprites/orc_v1_mvp1_static_128.png']
});

for (const dir of DIRECTIONS) {
  const dirPng = `characters/orc-v1/sprites/Directions/orc_v1_dir_${dir}.png`;
  const dirMaster = `${MASTER_NAT}/dir-${dir}.aseprite`;
  const compDirPng = `${OUT_BASE}/${dir}/Directions/base.png`;
  const compDirMaster = `${MASTER_COMP}/${dir}/dir-base.aseprite`;

  editorJobs.push({
    id: `native-dir-${dir}`,
    source: dirMaster,
    sourceSha256: sha(dirMaster),
    profile: { width: 128, height: 128, frames: 1, groundY: 126, alpha: 'binary', requireContent: true, requireTransparency: true },
    compare: [dirPng]
  });
  editorJobs.push({
    id: `comp-dir-${dir}`,
    source: compDirMaster,
    sourceSha256: sha(compDirMaster),
    profile: { width: 256, height: 256, frames: 1, groundY: 190, alpha: 'binary', requireContent: true, requireTransparency: true },
    compare: [compDirPng]
  });

  // Unarmed states: Idle, Walk, Unarmed (Attack), Hit, Defeat
  const unarmedStates = [
    { key: 'Idle', slotState: 'Idle', profileId: 'idle-balanced-v1', loop: true, terminal: false, contactEvent: null },
    { key: 'Walk', slotState: 'Walk', profileId: 'locomotion.walk-v1', loop: true, terminal: false, contactEvent: null },
    { key: 'Unarmed', slotState: 'Attack', profileId: 'basic.unarmed', loop: false, terminal: false, contactEvent: { frame: 2, timeMs: 190, status: 'CANDIDATE_VISUAL_ONLY', appliesDamage: false } },
    { key: 'Hit', slotState: 'Hit', profileId: 'reaction.hit', loop: false, terminal: false, contactEvent: null },
    { key: 'Defeat', slotState: 'Defeat', profileId: 'reaction.defeat', loop: false, terminal: true, terminalFrame: 4, contactEvent: null }
  ];

  for (const st of unarmedStates) {
    const durations = TIMINGS[st.key];
    const phases = PHASES[st.key];
    const natStem = st.slotState.toLowerCase();
    const natMaster = `${MASTER_NAT}/${natStem}-${dir}.aseprite`;
    const compStem = st.key === 'Unarmed' ? 'unarmed-attack' : `${st.key.toLowerCase()}-unarmed`;
    const compMaster = `${MASTER_COMP}/${dir}/${compStem}.aseprite`;
    const outDir = `${OUT_BASE}/${dir}/${st.key}`;
    const strip = `${outDir}/native-strip.png`;

    const frames = durations.map((dMs, i) => {
      const idx = String(i).padStart(2, '0');
      const png = `${outDir}/${idx}.png`;
      const nativePng = `characters/orc-v1/sprites/Animations/${st.slotState}/${natStem}_${dir}_${idx}.png`;
      const actionSupplementPng = st.key === 'Unarmed'
        ? `characters/orc-v1/source/actions/basic-unarmed/v1/${dir}/attack_${dir}_${idx}.png`
        : null;
      return {
        index: i,
        png,
        sha256: sha(png),
        nativePng,
        nativeSha256: sha(nativePng),
        ...(actionSupplementPng ? { supplementPng: actionSupplementPng, supplementSha256: sha(actionSupplementPng) } : {}),
        durationMs: dMs,
        phase: phases[i],
        weaponVisible: false
      };
    });

    const totalDurationMs = durations.reduce((a, b) => a + b, 0);
    const reuseMode = (dir === 'front_r' && st.key === 'Idle') ? 'REUSE_DIRECT'
      : (dir === 'front_r' && st.key === 'Walk') ? 'REUSE_ADAPTED'
      : 'AUTHORED_ASEPRITE_COMPLETE_V1';

    const clip = {
      schemaVersion: 1,
      revision: 'main-orc-complete-v1',
      id: st.profileId,
      character: 'orc-v1',
      state: st.key,
      legacySlotState: st.slotState,
      direction: dir,
      loop: st.loop,
      oneShot: !st.loop,
      terminal: st.terminal,
      ...(st.terminal ? { terminalFrame: st.terminalFrame } : {}),
      canvas: [256, 256],
      bodyOffset: [64, 64],
      groundY: 190,
      nativeCanvas: [128, 128],
      nativeGroundY: 126,
      ppu: 100,
      frameCount: frames.length,
      durationsMs: durations,
      totalDurationMs,
      master: compMaster,
      masterSha256: sha(compMaster),
      nativeMaster: natMaster,
      nativeMasterSha256: sha(natMaster),
      strip,
      stripSha256: sha(strip),
      visibilityPolicy: 'attack-only-v1',
      weaponVisible: false,
      weaponOverlay: false,
      contactEvent: st.contactEvent,
      frames,
      reuseAssessment: reuseMode,
      technicalStatus: 'TECHNICALLY_COMPLETE',
      artisticStatus: 'VISUAL_REVIEW_REQUIRED',
      artisticApproval: 'PENDING_CREATOR',
      qualityGatesContract: 'config/artistic-quality-gates-v1.json',
      runtimeImplemented: false
    };

    const clipPath = `${outDir}/clip.json`;
    json(path.join(ROOT, clipPath), clip);
    allClips.push({ state: st.key, category: null, direction: dir, profile: st.profileId, clip: clipPath, master: compMaster, nativeMaster: natMaster });

    coverageCells.push({
      character: 'orc-v1',
      action: st.key,
      profileId: st.profileId,
      direction: dir,
      status: 'COMPLETE_VERIFIED',
      technicalStatus: 'TECHNICALLY_COMPLETE',
      artisticStatus: 'VISUAL_REVIEW_REQUIRED',
      artisticApproval: 'PENDING_CREATOR',
      reuseAssessment: reuseMode,
      frameCount: frames.length,
      durationsMs: durations,
      totalDurationMs,
      loop: st.loop,
      oneShot: !st.loop,
      terminal: st.terminal,
      weaponVisible: false,
      visibleInterval: null,
      contactEvent: st.contactEvent,
      canvas256: [256, 256],
      groundY256: 190,
      canvas128: [128, 128],
      groundY128: 126,
      master256: compMaster,
      master256Sha256: sha(compMaster),
      master128: natMaster,
      master128Sha256: sha(natMaster),
      clipManifest: clipPath
    });

    editorJobs.push({
      id: `native-${natStem}-${dir}`,
      source: natMaster,
      sourceSha256: sha(natMaster),
      profile: { width: 128, height: 128, frames: frames.length, durationsMs: durations, groundY: 126, alpha: 'binary', requireContent: true, requireTransparency: true },
      compare: frames.map(f => f.nativePng)
    });

    editorJobs.push({
      id: `comp-${st.key.toLowerCase()}-${dir}`,
      source: compMaster,
      sourceSha256: sha(compMaster),
      profile: { width: 256, height: 256, frames: frames.length, durationsMs: durations, groundY: 190, alpha: 'binary', requireContent: true, requireTransparency: true },
      compare: frames.map(f => f.png)
    });
  }

  // Armed one-handed attack states: Sword, Axe
  for (const [category, wSpec] of Object.entries(WEAPONS)) {
    const geomList = authoredGeometry[category][dir];
    const outDir = `${OUT_BASE}/${dir}/${category}/Attack`;
    const stem = `${MASTER_COMP}/${dir}/${category.toLowerCase()}`;
    const master = `${stem}-attack.aseprite`;
    const bodyMaster = `${stem}-body.aseprite`;
    const handMaster = `${stem}-hand-front.aseprite`;
    const strip = `${outDir}/native-strip.png`;

    const frames = geomList.map((g, i) => {
      const idx = String(i).padStart(2, '0');
      const png = `${outDir}/${idx}.png`;
      const layers = Object.fromEntries(LAYER_ORDER.map(lname => {
        const lfile = `${outDir}/layers/${lname}/${idx}.png`;
        return [lname, { png: lfile, sha256: sha(lfile) }];
      }));
      return {
        index: i,
        png,
        sha256: sha(png),
        durationMs: g.durationMs,
        phase: g.phase,
        weaponVisible: g.weaponVisible,
        rightGrip: g.rightGrip,
        rotationDeg: g.rotationDeg,
        scale: 1,
        weaponBehindBody: g.weaponBehindBody,
        handSource: 'Own current posed glove; traced finger and thumb contours wrapping handle',
        layers
      };
    });

    const durations = frames.map(f => f.durationMs);
    const totalDurationMs = durations.reduce((a, b) => a + b, 0);
    const reuseMode = dir === 'front_r' ? 'REUSE_DIRECT' : 'AUTHORED_ASEPRITE_COMPLETE_V1';

    const clip = {
      schemaVersion: 1,
      revision: 'main-orc-complete-v1',
      id: wSpec.profileId,
      character: 'orc-v1',
      category,
      state: 'Attack',
      direction: dir,
      loop: false,
      oneShot: true,
      terminal: false,
      canvas: [256, 256],
      bodyOffset: [64, 64],
      groundY: 190,
      ppu: 100,
      frameCount: frames.length,
      durationsMs: durations,
      totalDurationMs,
      master,
      masterSha256: sha(master),
      bodyMaster,
      bodyMasterSha256: sha(bodyMaster),
      handMaster,
      handMasterSha256: sha(handMaster),
      strip,
      stripSha256: sha(strip),
      weapon: {
        id: wSpec.id,
        name: wSpec.name,
        grip: wSpec.grip,
        canvas: wSpec.canvas,
        scale: wSpec.scale,
        source: wSpec.source,
        master: wSpec.source,
        sprite: wSpec.sprite,
        sourceSha256: sha(wSpec.source),
        masterSha256: sha(wSpec.source),
        spriteSha256: sha(wSpec.sprite)
      },
      frames,
      layerOrder: LAYER_ORDER,
      visibilityPolicy: 'attack-only-v1',
      visibleInterval: wSpec.visibleInterval,
      hideAfterAction: true,
      contactEvent: wSpec.contactEvent,
      reuseAssessment: reuseMode,
      technicalStatus: 'TECHNICALLY_COMPLETE',
      artisticStatus: 'VISUAL_REVIEW_REQUIRED',
      artisticApproval: 'PENDING_CREATOR',
      qualityGatesContract: 'config/artistic-quality-gates-v1.json',
      runtimeImplemented: false
    };

    const profile = {
      schemaVersion: 1,
      revision: 'main-orc-complete-v1',
      id: wSpec.profileId,
      character: 'orc-v1',
      category,
      direction: dir,
      canvas: [256, 256],
      ppu: 100,
      bodyOffset: [64, 64],
      groundY: 190,
      bodyMaster,
      handMaster,
      frames: frames.map(f => ({
        index: f.index,
        body: f.layers.body,
        handFront: f.layers.handFront,
        durationMs: f.durationMs,
        phase: f.phase,
        grip: f.rightGrip,
        angle: f.rotationDeg,
        scale: 1,
        weaponVisible: f.weaponVisible,
        weaponBehindBody: f.weaponBehindBody
      })),
      itemContract: {
        grip: 'Integer local point on actual handle',
        scale: 1,
        canvas: 'Per-item native dimensions; no automatic body regeneration',
        category,
        direction: dir,
        occlusion: 'weaponBack -> body -> weaponFront -> handFront',
        compatibility: 'One-handed items of this category only; check shaft width, blade/head/guard clearance and camera'
      },
      technicalStatus: 'TECHNICALLY_COMPLETE',
      artisticStatus: 'VISUAL_REVIEW_REQUIRED',
      artisticApproval: 'PENDING_CREATOR'
    };

    const clipPath = `${outDir}/clip.json`;
    const profilePath = `${outDir}/profile.json`;
    json(path.join(ROOT, clipPath), clip);
    json(path.join(ROOT, profilePath), profile);

    allClips.push({ state: 'Attack', category, direction: dir, profile: wSpec.profileId, clip: clipPath, binding: profilePath, master });

    coverageCells.push({
      character: 'orc-v1',
      action: `${category} Attack`,
      profileId: wSpec.profileId,
      direction: dir,
      status: 'COMPLETE_VERIFIED',
      technicalStatus: 'TECHNICALLY_COMPLETE',
      artisticStatus: 'VISUAL_REVIEW_REQUIRED',
      artisticApproval: 'PENDING_CREATOR',
      reuseAssessment: reuseMode,
      frameCount: frames.length,
      durationsMs: durations,
      totalDurationMs,
      loop: false,
      oneShot: true,
      terminal: false,
      weaponVisible: true,
      visibleInterval: wSpec.visibleInterval,
      contactEvent: wSpec.contactEvent,
      weaponAsset: wSpec.id,
      layerOrder: LAYER_ORDER,
      canvas256: [256, 256],
      groundY256: 190,
      master256: master,
      master256Sha256: sha(master),
      bodyMaster256: bodyMaster,
      bodyMaster256Sha256: sha(bodyMaster),
      handMaster256: handMaster,
      handMaster256Sha256: sha(handMaster),
      clipManifest: clipPath,
      bindingProfile: profilePath
    });

    editorJobs.push({
      id: `comp-${category.toLowerCase()}-attack-${dir}`,
      source: master,
      sourceSha256: sha(master),
      profile: { width: 256, height: 256, frames: frames.length, durationsMs: durations, groundY: 190, alpha: 'binary', requireContent: true, requireTransparency: true },
      compare: frames.map(f => f.png)
    });
    editorJobs.push({
      id: `comp-${category.toLowerCase()}-body-${dir}`,
      source: bodyMaster,
      sourceSha256: sha(bodyMaster),
      profile: { width: 256, height: 256, frames: frames.length, durationsMs: durations, groundY: 190, alpha: 'binary', requireContent: true, requireTransparency: true },
      compare: frames.map(f => f.layers.body.png)
    });
    editorJobs.push({
      id: `comp-${category.toLowerCase()}-hand-${dir}`,
      source: handMaster,
      sourceSha256: sha(handMaster),
      profile: { width: 256, height: 256, frames: frames.length, durationsMs: durations, alpha: 'binary', requireContent: false, requireTransparency: true },
      compare: frames.map(f => f.layers.handFront.png)
    });
  }
}

// Add independent weapon jobs
for (const [category, wSpec] of Object.entries(WEAPONS)) {
  editorJobs.push({
    id: `weapon-${wSpec.id}`,
    source: wSpec.source,
    sourceSha256: sha(wSpec.source),
    profile: { width: 96, height: 96, frames: 1, alpha: 'binary', requireContent: true, requireTransparency: true },
    compare: [wSpec.sprite]
  });
}

// Write complete package manifest
const completeManifest = {
  schemaVersion: 1,
  revision: 'main-orc-complete-v1',
  character: 'orc-v1',
  sourceTruth: 'reports/orc-production-current.json',
  directions: DIRECTIONS,
  actions: ['Idle', 'Walk', 'Unarmed', 'Sword', 'Axe', 'Hit', 'Defeat'],
  canvas: [256, 256],
  bodyOffset: [64, 64],
  groundY: 190,
  nativeCanvas: [128, 128],
  nativeGroundY: 126,
  ppu: 100,
  visibilityPolicy: 'attack-only-v1',
  armedIdle: false,
  armedWalk: false,
  profiles: {
    Idle: 'idle-balanced-v1',
    Walk: 'locomotion.walk-v1',
    Unarmed: 'basic.unarmed',
    Sword: 'basic.sword-slash',
    Axe: 'basic.axe-chop',
    Hit: 'reaction.hit',
    Defeat: 'reaction.defeat'
  },
  clips: allClips,
  technicalStatus: 'TECHNICALLY_COMPLETE',
  artisticStatus: 'VISUAL_REVIEW_REQUIRED',
  artisticApproval: 'PENDING_CREATOR',
  qualityGatesContract: 'config/artistic-quality-gates-v1.json',
  runtimeImplemented: false
};
json(path.join(ROOT, `${OUT_BASE}/manifest.json`), completeManifest);
json(path.join(ROOT, 'characters/orc-v1/source/equipment-complete-candidate.json'), {
  revision: 'main-orc-complete-v1',
  manifest: `${OUT_BASE}/manifest.json`,
  coverageMatrix: 'reports/orc-v1-animation-coverage-v1.json',
  stagingPackage: DIST_PKG,
  presentationPolicy: 'attack-only-v1',
  technicalStatus: 'TECHNICALLY_COMPLETE',
  artisticStatus: 'VISUAL_REVIEW_REQUIRED',
  artisticApproval: 'PENDING_CREATOR',
  qualityGatesContract: 'config/artistic-quality-gates-v1.json',
  basedOn: 'main-orc-onehanded-entry-v1',
  preservesActiveSelection: 'characters/orc-v1/source/equipment-current.json',
  preservesEntryCandidate: 'characters/orc-v1/source/equipment-entry-candidate.json',
  review: 'Biblioteca de Arte/Personagens Jogaveis/Orc V1/index.html',
  runtimeImplemented: false
});

// Export & verify all Aseprite masters via exportAseprite
const editorManifest = {
  schemaVersion: 1,
  id: 'orc-v1-complete-v1',
  kind: 'character',
  characterId: 'orc-v1',
  jobs: editorJobs
};
const prevEditorSha = exists(`${EXP}/editor.json`) ? sha(`${EXP}/editor.json`) : null;
json(path.join(ROOT, `${EXP}/editor.json`), editorManifest);
const newEditorSha = sha(`${EXP}/editor.json`);

let editorBuild;
if (
  !process.argv.includes('--force-aseprite') &&
  prevEditorSha === newEditorSha &&
  exists(`${EXP}/build.json`)
) {
  const cached = readJSON(path.join(ROOT, `${EXP}/build.json`));
  if (cached?.summary?.status === 'PASS' && cached?.path && exists(cached.path)) {
    console.log(`Reusing verified Aseprite build (${cached.summary.jobs} jobs / ${cached.summary.frames} frames PASS): ${cached.path}`);
    editorBuild = cached;
  }
}
if (!editorBuild) {
  editorBuild = exportAseprite(editorManifest, {
    onProgress: p => {
      if (p.completed % 15 === 0 || p.completed === p.total) {
        console.log(`Aseprite export ${p.completed}/${p.total}: ${p.id}`);
      }
    }
  });
  json(path.join(ROOT, `${EXP}/build.json`), editorBuild);
}

// Validate native 128x128 character package via src/images.mjs validate()
const { dir: charDir, spec: charSpec } = loadCharacter('orc-v1');
const validationReport = validate(charSpec, charDir, 'full');
json(path.join(charDir, 'reports/validation.json'), validationReport);
if (validationReport.summary.FAIL > 0) {
  throw new Error(`Native 128x128 validation failed with ${validationReport.summary.FAIL} FAILs`);
}

// Write machine-readable Coverage Matrix
const coverageMatrix = {
  schemaVersion: 1,
  revision: 'main-orc-complete-v1',
  characterId: 'orc-v1',
  characterName: charSpec.name,
  derivedFrom: 'orc-pixellab-05',
  paletteRevision: 'green-skin-v3',
  historicalV4Discarded: true,
  visibilityPolicy: 'attack-only-v1',
  editorBuild: {
    path: editorBuild.path,
    preview: `${editorBuild.path}/preview.html`,
    summary: editorBuild.summary
  },
  nativeValidationSummary: validationReport.summary,
  summary: {
    directions: 4,
    actionsPerDirection: 7,
    totalActionDirectionCells: coverageCells.length,
    completedCells: coverageCells.filter(c => c.status === 'COMPLETE_VERIFIED').length,
    missingCells: 0,
    staticDirectionalBases: 4,
    independentWeaponAssets: 2,
    native128PngCount: validationReport.measurements.length,
    editorJobsVerified: editorBuild.summary.jobs,
    editorFramesVerified: editorBuild.summary.frames
  },
  cells: coverageCells,
  technicalStatus: 'TECHNICALLY_COMPLETE',
  artisticStatus: 'VISUAL_REVIEW_REQUIRED',
  artisticApproval: 'PENDING_CREATOR',
  qualityGatesContract: 'config/artistic-quality-gates-v1.json',
  runtimeImplemented: false
};
json(path.join(ROOT, 'reports/orc-v1-animation-coverage-v1.json'), coverageMatrix);
json(path.join(ROOT, `${OUT_BASE}/coverage-matrix.json`), coverageMatrix);

// Build reproducible Unity-Ready Asset Package in dist/orc-v1/complete-v1/
const distRoot = path.join(ROOT, DIST_PKG);
fs.rmSync(distRoot, { recursive: true, force: true });
const resCharDir = path.join(distRoot, 'Assets/Resources/Characters/orc-v1');

// 1. Copy native 128x128 sprites (Directions, Animations, Actions/basic-unarmed)
function copyTreeRel(srcRel, dstFull) {
  const srcFull = path.join(ROOT, srcRel);
  fs.cpSync(srcFull, dstFull, { recursive: true });
}
copyTreeRel('characters/orc-v1/sprites', resCharDir);
if (exists('characters/orc-v1/source/actions')) {
  copyTreeRel('characters/orc-v1/source/actions', path.join(resCharDir, 'Actions'));
}

// 2. Copy composite 256x256 directional action clips & manifests
copyTreeRel(OUT_BASE, path.join(resCharDir, 'Composite256'));

// 3. Copy independent weapon sprites & metadata
for (const wSpec of Object.values(WEAPONS)) {
  const wOut = path.join(resCharDir, 'Weapons', wSpec.id);
  fs.mkdirSync(wOut, { recursive: true });
  fs.copyFileSync(path.join(ROOT, wSpec.sprite), path.join(wOut, `${wSpec.id}.png`));
  fs.copyFileSync(path.join(ROOT, `assets/weapons/${wSpec.id}/weapon.json`), path.join(wOut, 'weapon.json'));
}

// 4. Write Unity Handoff Contract & Factory Manifest inside dist package
const unityHandoffContract = {
  schemaVersion: 1,
  contractId: 'tacticsrpg.unity-character-handoff.orc-v1.complete-v1',
  characterId: 'orc-v1',
  characterName: charSpec.name,
  technicalStatus: 'TECHNICALLY_COMPLETE',
  artisticStatus: 'VISUAL_REVIEW_REQUIRED',
  artisticApproval: 'PENDING_CREATOR',
  qualityGatesContract: 'config/artistic-quality-gates-v1.json',
  unityRepositoryModified: false,
  runtimeIntegrationStatus: 'READY_FOR_FUTURE_UNITY_INTEGRATION_TASK',
  canvases: {
    nativeBody128: {
      width: 128,
      height: 128,
      ppu: 100,
      groundYFromTop: 126,
      pivotNormalized: [0.5, (128 - 126) / 128],
      filterMode: 'Point',
      textureCompression: 'None',
      alphaIsTransparency: true,
      usage: 'Weaponless Directions, Idle, Walk, Unarmed Attack, Hit, Defeat'
    },
    compositeCombat256: {
      width: 256,
      height: 256,
      ppu: 100,
      bodyOffsetFromTopLeft: [64, 64],
      groundYFromTop: 190,
      pivotNormalized: [0.5, (256 - 190) / 256],
      filterMode: 'Point',
      textureCompression: 'None',
      alphaIsTransparency: true,
      usage: 'Registered 256x256 sequences for Sword Attack, Axe Attack, and zero-shift transitions with Idle/Walk/Unarmed/Hit/Defeat'
    },
    independentWeapons96: {
      width: 96,
      height: 96,
      ppu: 100,
      filterMode: 'Point',
      textureCompression: 'None',
      items: WEAPONS
    }
  },
  directions: DIRECTIONS,
  stateMachineSemantics: {
    Idle: { profile: 'idle-balanced-v1', frames: 5, durationsMs: TIMINGS.Idle, totalMs: 2200, loop: true, oneShot: false, terminal: false, weaponVisible: false },
    Walk: { profile: 'locomotion.walk-v1', frames: 16, durationsMs: TIMINGS.Walk, totalMs: 1280, loop: true, oneShot: false, terminal: false, weaponVisible: false },
    Unarmed: { profile: 'basic.unarmed', frames: 5, durationsMs: TIMINGS.Unarmed, totalMs: 450, loop: false, oneShot: true, terminal: false, weaponVisible: false, returnState: 'Idle', contactEvent: { frame: 2, timeMs: 190, appliesDamage: false } },
    SwordAttack: { profile: 'basic.sword-slash', frames: 13, durationsMs: authoredGeometry.Sword.front_r.map(f => f.durationMs), totalMs: 730, loop: false, oneShot: true, terminal: false, weaponVisible: true, visibleInterval: [2, 10], layerOrder: LAYER_ORDER, returnState: 'Idle', contactEvent: WEAPONS.Sword.contactEvent },
    AxeAttack: { profile: 'basic.axe-chop', frames: 12, durationsMs: authoredGeometry.Axe.front_r.map(f => f.durationMs), totalMs: 1005, loop: false, oneShot: true, terminal: false, weaponVisible: true, visibleInterval: [2, 8], layerOrder: LAYER_ORDER, returnState: 'Idle', contactEvent: WEAPONS.Axe.contactEvent },
    Hit: { profile: 'reaction.hit', frames: 5, durationsMs: TIMINGS.Hit, totalMs: 450, loop: false, oneShot: true, terminal: false, weaponVisible: false, returnState: 'Idle' },
    Defeat: { profile: 'reaction.defeat', frames: 5, durationsMs: TIMINGS.Defeat, totalMs: 700, loop: false, oneShot: true, terminal: true, terminalFrame: 4, weaponVisible: false, returnState: null }
  },
  requiredUnityRuntimeExtensions: [
    'Register orc-v1 in UnitVisuals / CharacterCatalog (currently fixed to WarriorPilot in snapshot).',
    'Support per-frame durationsMs from clip.json for variable-timing clips (Idle 2200ms, Walk 16x80ms, Unarmed 450ms, Sword 730ms, Axe 1005ms, Hit 450ms, Defeat 700ms).',
    'Resolve basic-attack visual profile by actual equippedWeaponKind (null -> basic.unarmed, Sword -> basic.sword-slash, Axe -> basic.axe-chop) rather than Job.',
    'When rendering 256x256 composite weapon attacks (or layered weaponBack/body/weaponFront/handFront), use pivot (128, 190) = normalized (0.5, 0.2578125) to match 128x128 pivot (64, 126) = normalized (0.5, 0.015625) in world units (1.28x1.28 vs 2.56x2.56 at PPU 100).',
    'Enforce attack-only-v1 weapon visibility: hide weapon outside visibleInterval and immediately upon transition to Idle, Walk, Hit, or Defeat.'
  ]
};

json(path.join(resCharDir, 'unity-handoff-contract.json'), unityHandoffContract);
json(path.join(resCharDir, 'animation-coverage-matrix.json'), coverageMatrix);
json(path.join(resCharDir, 'factory-manifest.json'), {
  schemaVersion: 1,
  id: 'orc-v1',
  revision: 'main-orc-complete-v1',
  ppu: 100,
  profile: charSpec.profile,
  compositeProfile: { width: 256, height: 256, bodyOffset: [64, 64], groundY: 190, ppu: 100 },
  visibilityPolicy: 'attack-only-v1',
  technicalStatus: 'TECHNICALLY_COMPLETE',
  artisticStatus: 'VISUAL_REVIEW_REQUIRED',
  artisticApproval: 'PENDING_CREATOR',
  qualityGatesContract: 'config/artistic-quality-gates-v1.json',
  gate1: 'PENDING_CREATOR',
  gate2: 'PENDING_CREATOR',
  gate3: 'PENDING_PLAYMODE',
  runtimeRegistration: 'REQUIRES_EXTENSION: UnitVisuals is fixed to WarriorPilot in snapshot; see unity-handoff-contract.json',
  editorBuild: editorBuild.path,
  nativeFilesCount: validationReport.measurements.length
});

write(path.join(distRoot, 'Assets/Editor/CharacterFactoryImporter.cs'), fs.readFileSync(path.join(ROOT, 'unity/CharacterFactoryImporter.cs')));
write(path.join(distRoot, 'INTEGRATION.md'), fs.readFileSync(path.join(ROOT, 'docs/UNITY.md')));
json(path.join(distRoot, 'validation.json'), validationReport);

// Collect all file hashes in dist/orc-v1/complete-v1
function walkDistFiles(dir) {
  const out = [];
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) out.push(...walkDistFiles(p));
    else if (e.name !== 'hashes.json') out.push({ file: slash(path.relative(distRoot, p)), sha256: hash(fs.readFileSync(p)) });
  }
  return out.sort((a, b) => a.file.localeCompare(b.file));
}
const distHashes = walkDistFiles(distRoot);
json(path.join(distRoot, 'hashes.json'), distHashes);

// Verify protected art files one more time after all builds
for (const [f, expectedSha] of Object.entries(protectedMap)) {
  if (!exists(f) || sha(f) !== expectedSha) {
    throw new Error(`Protected canonical art file altered after build: ${f}`);
  }
}

console.log(JSON.stringify({
  status: 'COMPLETE_PACKAGE_BUILT_AND_VERIFIED',
  editorBuild: editorBuild.path,
  editorJobs: editorBuild.summary.jobs,
  editorFrames: editorBuild.summary.frames,
  nativeValidation: validationReport.summary,
  coverageCells: coverageCells.length,
  distFiles: distHashes.length,
  protectedFilesVerified: Object.keys(protectedMap).length
}, null, 2));
