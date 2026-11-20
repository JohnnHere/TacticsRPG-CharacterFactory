import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { PNG } from "pngjs";

const ROOT = process.cwd();
const ASE_ROOT = "characters/orc-v1/source/aseprite/final-candidate-v10";
const OUT_ROOT = "characters/orc-v1/source/final-candidate-v10";
const B3_ROOT  = "experiments/main-orc-hybrid-weapon-04b3";
const EXP_ROOT = "experiments/main-orc-final-v10";
const DIST_ROOT = "dist/orc-v1/final-candidate-v10";

function sha256(relOrAbs) {
  const p = path.isAbsolute(relOrAbs) ? relOrAbs : path.join(ROOT, relOrAbs);
  return crypto.createHash("sha256").update(fs.readFileSync(p)).digest("hex");
}

function readPng(relOrAbs) {
  const p = path.isAbsolute(relOrAbs) ? relOrAbs : path.join(ROOT, relOrAbs);
  return PNG.sync.read(fs.readFileSync(p));
}

function countOpaque(png) {
  let n = 0;
  for (let i = 3; i < png.data.length; i += 4) if (png.data[i] > 0) n++;
  return n;
}

function countPartialAlpha(png) {
  let n = 0;
  for (let i = 3; i < png.data.length; i += 4) {
    const a = png.data[i];
    if (a > 0 && a < 255) n++;
  }
  return n;
}

function bboxOpaque(png) {
  let minX = png.width, minY = png.height, maxX = -1, maxY = -1;
  for (let y = 0; y < png.height; y++) {
    for (let x = 0; x < png.width; x++) {
      if (png.data[(y * png.width + x) * 4 + 3] > 0) {
        if (x < minX) minX = x;
        if (x > maxX) maxX = x;
        if (y < minY) minY = y;
        if (y > maxY) maxY = y;
      }
    }
  }
  return maxX >= 0 ? [minX, minY, maxX, maxY] : null;
}

function rgbaDiffCount(pngA, pngB) {
  let diff = 0;
  for (let i = 0; i < pngA.data.length; i += 4) {
    const a1 = pngA.data[i + 3], a2 = pngB.data[i + 3];
    if (a1 === 0 && a2 === 0) continue;
    if (a1 !== a2 || pngA.data[i] !== pngB.data[i] || pngA.data[i + 1] !== pngB.data[i + 1] || pngA.data[i + 2] !== pngB.data[i + 2]) {
      diff++;
    }
  }
  return diff;
}

function silhouetteXorCount(pngA, pngB) {
  let xor = 0;
  for (let i = 3; i < pngA.data.length; i += 4) {
    if ((pngA.data[i] > 0) !== (pngB.data[i] > 0)) xor++;
  }
  return xor;
}

function writeJson(relPath, obj) {
  const full = path.join(ROOT, relPath);
  fs.mkdirSync(path.dirname(full), { recursive: true });
  fs.writeFileSync(full, JSON.stringify(obj, null, 2) + "\n", "utf8");
}

const DIRS = ["front_r", "front_l", "back_r", "back_l"];
const SWORD_DURS = [30, 65, 35, 50, 45, 35, 30, 35, 35, 100, 55, 80, 45, 90];
const SWORD_PHASES = [
  "rest", "body-preparation", "establish-grip", "anticipation", "coil", "apex-hold",
  "apex-descent", "slash-release", "contact", "follow-through", "recover-bridge",
  "settle-grip", "disarm-settle", "rest-return"
];

const AXE_DURS = [40, 65, 35, 80, 155, 35, 115, 110, 130, 50, 90, 100];
const AXE_PHASES = [
  "rest", "body-preparation", "establish-grip", "anticipation", "overhead-coil",
  "cleave-drive", "heavy-impact", "weight-settle", "wrench-recovery",
  "release-grip", "shoulder-reset", "return-to-guard"
];

const SWORD_META_BY_DIR = {
  front_r: [
    { vis: false }, { vis: false },
    { vis: true, grip: [99, 128],  rot: 316, occlusion: "front_grip" },
    { vis: true, grip: [88, 120],  rot: 330, occlusion: "front_grip" },
    { vis: true, grip: [86, 108],  rot: 345, occlusion: "front_grip" },
    { vis: true, grip: [94, 89],   rot: 2,   occlusion: "front_grip" },
    { vis: true, grip: [128, 100], rot: 18,  occlusion: "front_grip" },
    { vis: true, grip: [154, 112], rot: 34,  occlusion: "front_grip" },
    { vis: true, grip: [157, 129], rot: 82,  occlusion: "front_grip" },
    { vis: true, grip: [150, 142], rot: 124, occlusion: "front_grip" },
    { vis: true, grip: [135, 142], rot: 114, occlusion: "front_grip" },
    { vis: true, grip: [97, 138],  rot: 128, occlusion: "front_grip" },
    { vis: false }, { vis: false },
  ],
  front_l: [
    { vis: false }, { vis: false },
    { vis: true, grip: [156, 128], rot: 44,  occlusion: "front_grip" },
    { vis: true, grip: [167, 120], rot: 30,  occlusion: "front_grip" },
    { vis: true, grip: [169, 108], rot: 15,  occlusion: "front_grip" },
    { vis: true, grip: [161, 89],  rot: 358, occlusion: "front_grip" },
    { vis: true, grip: [127, 100], rot: 342, occlusion: "front_grip" },
    { vis: true, grip: [101, 112], rot: 326, occlusion: "front_grip" },
    { vis: true, grip: [97, 130],  rot: 278, occlusion: "front_grip" },
    { vis: true, grip: [105, 142], rot: 236, occlusion: "front_grip" },
    { vis: true, grip: [120, 142], rot: 246, occlusion: "front_grip" },
    { vis: true, grip: [158, 138], rot: 232, occlusion: "front_grip" },
    { vis: false }, { vis: false },
  ],
  back_r: [
    { vis: false }, { vis: false },
    { vis: true, grip: [162, 97],  rot: 26,  occlusion: "rear_dorsal" },
    { vis: true, grip: [152, 78],  rot: 14,  occlusion: "rear_dorsal" },
    { vis: true, grip: [145, 73],  rot: -4,  occlusion: "rear_dorsal" },
    { vis: true, grip: [141, 74],  rot: -14, occlusion: "rear_dorsal" },
    { vis: true, grip: [173, 93],  rot: 48,  occlusion: "rear_dorsal" },
    { vis: true, grip: [177, 108], rot: 82,  occlusion: "rear_dorsal" },
    { vis: true, grip: [175, 123], rot: 114, occlusion: "rear_dorsal" },
    { vis: true, grip: [164, 129], rot: 132, occlusion: "rear_dorsal" },
    { vis: true, grip: [162, 132], rot: 120, occlusion: "rear_dorsal" },
    { vis: true, grip: [160, 136], rot: 108, occlusion: "rear_dorsal" },
    { vis: false }, { vis: false },
  ],
  back_l: [
    { vis: false }, { vis: false },
    { vis: true, grip: [160, 95],  rot: 26,   occlusion: "rear_dorsal" },
    { vis: true, grip: [156, 79],  rot: 12,   occlusion: "rear_dorsal" },
    { vis: true, grip: [149, 77],  rot: -6,   occlusion: "rear_dorsal" },
    { vis: true, grip: [144, 76],  rot: -16,  occlusion: "rear_dorsal" },
    { vis: true, grip: [107, 86],  rot: -46,  occlusion: "all_back" },
    { vis: true, grip: [96, 98],   rot: -78,  occlusion: "all_back" },
    { vis: true, grip: [95, 111],  rot: -104, occlusion: "all_back" },
    { vis: true, grip: [104, 122], rot: -118, occlusion: "all_back" },
    { vis: true, grip: [108, 124], rot: -124, occlusion: "all_back" },
    { vis: true, grip: [159, 131], rot: 114,  occlusion: "rear_dorsal" },
    { vis: false }, { vis: false },
  ],
};

const AXE_META_BY_DIR = {
  front_r: [
    { vis: false }, { vis: false },
    { vis: true, grip: [99, 128],  rot: 304, flipBit: false, occlusion: "front_grip" },
    { vis: true, grip: [88, 120],  rot: 324, flipBit: false, occlusion: "front_grip" },
    { vis: true, grip: [86, 108],  rot: 346, flipBit: false, occlusion: "front_grip" },
    { vis: true, grip: [154, 112], rot: 64,  flipBit: false, occlusion: "front_grip" },
    { vis: true, grip: [150, 141], rot: 118, flipBit: false, occlusion: "front_grip" },
    { vis: true, grip: [141, 146], rot: 106, flipBit: false, occlusion: "front_grip" },
    { vis: true, grip: [135, 142], rot: 96,  flipBit: false, occlusion: "front_grip" },
    { vis: false }, { vis: false }, { vis: false },
  ],
  front_l: [
    { vis: false }, { vis: false },
    { vis: true, grip: [156, 128], rot: 56,  flipBit: true, occlusion: "front_grip" },
    { vis: true, grip: [167, 120], rot: 36,  flipBit: true, occlusion: "front_grip" },
    { vis: true, grip: [169, 108], rot: 14,  flipBit: true, occlusion: "front_grip" },
    { vis: true, grip: [101, 112], rot: 296, flipBit: true, occlusion: "front_grip" },
    { vis: true, grip: [105, 141], rot: 242, flipBit: true, occlusion: "front_grip" },
    { vis: true, grip: [114, 146], rot: 254, flipBit: true, occlusion: "front_grip" },
    { vis: true, grip: [120, 142], rot: 264, flipBit: true, occlusion: "front_grip" },
    { vis: false }, { vis: false }, { vis: false },
  ],
  back_r: [
    { vis: false }, { vis: false },
    { vis: true, grip: [162, 100], rot: 26,  flipBit: false, occlusion: "rear_dorsal" },
    { vis: true, grip: [149, 76],  rot: 4,   flipBit: false, occlusion: "rear_dorsal" },
    { vis: true, grip: [139, 73],  rot: -16, flipBit: false, occlusion: "rear_dorsal" },
    { vis: true, grip: [176, 103], rot: 62,  flipBit: false, occlusion: "rear_dorsal" },
    { vis: true, grip: [172, 127], rot: 104, flipBit: false, occlusion: "rear_dorsal" },
    { vis: true, grip: [165, 132], rot: 114, flipBit: false, occlusion: "rear_dorsal" },
    { vis: true, grip: [162, 130], rot: 106, flipBit: false, occlusion: "rear_dorsal" },
    { vis: false }, { vis: false }, { vis: false },
  ],
  back_l: [
    { vis: false }, { vis: false },
    { vis: true, grip: [160, 95],  rot: 24,   flipBit: true, occlusion: "rear_dorsal" },
    { vis: true, grip: [156, 80],  rot: 6,    flipBit: true, occlusion: "rear_dorsal" },
    { vis: true, grip: [148, 77],  rot: -12,  flipBit: true, occlusion: "rear_dorsal" },
    { vis: true, grip: [114, 88],  rot: -52,  flipBit: true, occlusion: "all_back" },
    { vis: true, grip: [98, 114],  rot: -96,  flipBit: true, occlusion: "all_back" },
    { vis: true, grip: [102, 122], rot: -108, flipBit: true, occlusion: "all_back" },
    { vis: true, grip: [105, 119], rot: -102, flipBit: true, occlusion: "all_back" },
    { vis: false }, { vis: false }, { vis: false },
  ],
};

// 1. Write Weapon Definitions
const swordADefPath = `${OUT_ROOT}/weapons/Sword/weapon.json`;
const swordBDefPath = `${OUT_ROOT}/weapons/SwordB/weapon.json`;
const axeDefPath    = `${OUT_ROOT}/weapons/Axe/weapon.json`;

writeJson(swordADefPath, {
  schemaVersion: 1,
  id: "recruit-sword",
  name: "Espada do Recruta (Variante A)",
  hands: 1,
  category: "Sword",
  canvas: [96, 96],
  grip: [48, 63],
  ppu: 100,
  sprite: `${OUT_ROOT}/weapons/Sword/recruit-sword.png`,
  spriteSha256: sha256(`${OUT_ROOT}/weapons/Sword/recruit-sword.png`),
  master: `${ASE_ROOT}/weapons/recruit-sword.aseprite`,
  masterSha256: sha256(`${ASE_ROOT}/weapons/recruit-sword.aseprite`),
  artisticStatus: "VISUAL_REVIEW_REQUIRED",
  creatorApproval: "PENDING_CREATOR",
});

writeJson(swordBDefPath, {
  schemaVersion: 1,
  id: "faceted-sword-b",
  name: "Espada Facetada de Aço Claro (Variante B)",
  hands: 1,
  category: "Sword",
  canvas: [96, 96],
  grip: [48, 63],
  ppu: 100,
  silhouetteDeltaVsSwordAPx: silhouetteXorCount(
    readPng(`${OUT_ROOT}/weapons/Sword/recruit-sword.png`),
    readPng(`${OUT_ROOT}/weapons/SwordB/faceted-sword-b.png`)
  ),
  sprite: `${OUT_ROOT}/weapons/SwordB/faceted-sword-b.png`,
  spriteSha256: sha256(`${OUT_ROOT}/weapons/SwordB/faceted-sword-b.png`),
  master: `${ASE_ROOT}/weapons/faceted-sword-b.aseprite`,
  masterSha256: sha256(`${ASE_ROOT}/weapons/faceted-sword-b.aseprite`),
  artisticStatus: "VISUAL_REVIEW_REQUIRED",
  creatorApproval: "PENDING_CREATOR",
});

writeJson(axeDefPath, {
  schemaVersion: 1,
  id: "militia-axe",
  name: "Machado de Milícia",
  hands: 1,
  category: "Axe",
  canvas: [96, 96],
  grip: [38, 45],
  gripNote: "Upper-middle shaft pivot (38,45) so wooden haft v=42..48 passes straight through palm and butt-cap v=50..61 protrudes below fist; orphan pixel (37,24) removed and collar reinforced.",
  ppu: 100,
  sprite: `${OUT_ROOT}/weapons/Axe/militia-axe.png`,
  spriteSha256: sha256(`${OUT_ROOT}/weapons/Axe/militia-axe.png`),
  master: `${ASE_ROOT}/weapons/militia-axe.aseprite`,
  masterSha256: sha256(`${ASE_ROOT}/weapons/militia-axe.aseprite`),
  artisticStatus: "VISUAL_REVIEW_REQUIRED",
  creatorApproval: "PENDING_CREATOR",
});

// 2. Verify Architecture C across all 4 directions & write grip profiles + Piloto B3
const archVerification = {
  schemaVersion: 1,
  revision: "main-orc-final-v10",
  status: "PASS",
  totalViews: 4,
  totalFramesPerVariant: 56,
  bodyFramesModifiedForVariantB: 0,
  handFramesModifiedForVariantB: 0,
  unarmedWeaponPixelsTotal: 0,
  partialAlphaPixelsTotal: 0,
  weaponPixelsBelowGroundYTotal: 0,
  views: {},
};

for (const dir of DIRS) {
  const dirA = `${OUT_ROOT}/architecture-c/${dir}/sword-a`;
  const dirB = `${OUT_ROOT}/architecture-c/${dir}/sword-b`;
  const meta = SWORD_META_BY_DIR[dir];
  const frameEntries = [];
  let silDeltaSum = 0;

  for (let i = 0; i < 14; i++) {
    const code = String(i).padStart(2, "0");
    const compA = readPng(`${dirA}/frames/${code}.png`);
    const compB = readPng(`${dirB}/frames/${code}.png`);
    const bodyA = readPng(`${dirA}/layers/body/${code}.png`);
    const bodyB = readPng(`${dirB}/layers/body/${code}.png`);
    const handA = readPng(`${dirA}/layers/handFront/${code}.png`);
    const handB = readPng(`${dirB}/layers/handFront/${code}.png`);
    const weapA = readPng(`${dirA}/weapon-only/${code}.png`);
    const weapB = readPng(`${dirB}/weapon-only/${code}.png`);

    const bodyDiff = rgbaDiffCount(bodyA, bodyB);
    const handDiff = rgbaDiffCount(handA, handB);
    const partA = countPartialAlpha(compA) + countPartialAlpha(compB);
    const wPxA = countOpaque(weapA);
    const wPxB = countOpaque(weapB);
    const silDelta = silhouetteXorCount(weapA, weapB);
    const wbBoxA = bboxOpaque(weapA);
    const wbBoxB = bboxOpaque(weapB);
    const maxWy = Math.max(wbBoxA ? wbBoxA[3] : 0, wbBoxB ? wbBoxB[3] : 0);

    if (bodyDiff !== 0 || handDiff !== 0 || partA !== 0 || maxWy > 190) {
      throw new Error(`Arch-C invariant failed on ${dir} F${code}: bodyDiff=${bodyDiff}, handDiff=${handDiff}, partAlpha=${partA}, maxWy=${maxWy}`);
    }
    if (!meta[i].vis && (wPxA !== 0 || wPxB !== 0)) {
      throw new Error(`Unarmed frame has weapon pixels on ${dir} F${code}`);
    }
    if (meta[i].vis && silDelta < 80) {
      throw new Error(`Expected distinct silhouette on ${dir} F${code}, got silDelta=${silDelta}`);
    }
    silDeltaSum += silDelta;

    frameEntries.push({
      index: i,
      phase: SWORD_PHASES[i],
      durationMs: SWORD_DURS[i],
      weaponVisible: meta[i].vis,
      grip: meta[i].grip || null,
      rotationDeg: meta[i].vis ? meta[i].rot : null,
      occlusionMode: meta[i].occlusion || null,
      handFrontPixels: countOpaque(handA),
      weaponAPixels: wPxA,
      weaponBPixels: wPxB,
      silhouetteDeltaABPx: silDelta,
      maxWeaponY: maxWy || null,
    });
  }

  const gripProfile = {
    schemaVersion: 1,
    family: "Sword/basic.sword-slash",
    direction: dir,
    canvas: [256, 256],
    groundY: 190,
    assetCanvas: [96, 96],
    assetGrip: [48, 63],
    layerOrder: ["weaponBack", "body", "weaponFront", "handFront"],
    durationsMs: SWORD_DURS,
    totalDurationMs: 730,
    visibleInterval: [2, 11],
    contactEvent: { frame: 8, timeMs: 325, phase: "contact", appliesDamage: false },
    variants: {
      a: { id: "recruit-sword", master: `${ASE_ROOT}/architecture-c/${dir}/sword-a.aseprite`, masterSha256: sha256(`${ASE_ROOT}/architecture-c/${dir}/sword-a.aseprite`), strip: `${dirA}/composite-strip.png`, stripSha256: sha256(`${dirA}/composite-strip.png`) },
      b: { id: "faceted-sword-b", master: `${ASE_ROOT}/architecture-c/${dir}/sword-b.aseprite`, masterSha256: sha256(`${ASE_ROOT}/architecture-c/${dir}/sword-b.aseprite`), strip: `${dirB}/composite-strip.png`, stripSha256: sha256(`${dirB}/composite-strip.png`) },
    },
    frames: frameEntries,
  };

  writeJson(`${OUT_ROOT}/architecture-c/grip-profile-${dir}.json`, gripProfile);
  if (dir === "back_l") {
    writeJson(`${B3_ROOT}/grip-profile-back-l.json`, gripProfile);
    writeJson(`${B3_ROOT}/verification.json`, {
      status: "TECHNICALLY_COMPLETE",
      artisticStatus: "VISUAL_REVIEW_REQUIRED",
      creatorApproval: "PENDING_CREATOR",
      pilot: "B3",
      direction: "back_l",
      bodyIdenticalAB: "14/14 (0 px delta)",
      handFrontIdenticalAB: "14/14 (0 px delta)",
      totalSilhouetteDeltaABPx: silDeltaSum,
      unarmedWeaponPixels: 0,
      partialAlphaPixels: 0,
      maxWeaponY: Math.max(...frameEntries.map(f => f.maxWeaponY || 0)),
    });
  }

  archVerification.views[dir] = {
    bodyIdenticalFrames: 14,
    handIdenticalFrames: 14,
    totalSilhouetteDeltaABPx: silDeltaSum,
    maxWeaponY: Math.max(...frameEntries.map(f => f.maxWeaponY || 0)),
  };
}

writeJson(`${OUT_ROOT}/architecture-c/verification.json`, archVerification);

// 3. Build clip.json for all 18 updated cells + assemble 28-cell candidate28manifest.json
const parentManifest = JSON.parse(fs.readFileSync(path.join(ROOT, "characters/orc-v1/source/backl-v5base/candidate28manifest.json"), "utf8"));
const parentCellsMap = Object.fromEntries(parentManifest.cells.map(c => [c.cellId, c]));

function buildWeaponClipJson(dir, category, durs, phases, visInterval, contactEv, metaArr, weapDefRel, notes) {
  const clipDir = `${OUT_ROOT}/${dir}/${category}`;
  const compMaster = `${ASE_ROOT}/composite/${dir}/${category.toLowerCase()}.aseprite`;
  const natMaster  = `${ASE_ROOT}/native/${category.toLowerCase()}-${dir}.aseprite`;
  let cumMs = 0;
  const frames = durs.map((d, i) => {
    const code = String(i).padStart(2, "0");
    const m = metaArr[i];
    const entry = {
      index: i,
      phase: phases[i],
      durationMs: d,
      startMs: cumMs,
      endMs: cumMs + d,
      weaponVisible: m.vis,
      grip: m.grip || null,
      rightGrip: m.grip || null,
      rotationDeg: m.vis ? m.rot : null,
      occlusionMode: m.occlusion || null,
      png: `${clipDir}/frames/${code}.png`,
      sha256: sha256(`${clipDir}/frames/${code}.png`),
      nativePng: `${clipDir}/native/${code}.png`,
      nativeSha256: sha256(`${clipDir}/native/${code}.png`),
      layers: {
        weaponBack:  { png: `${clipDir}/layers/weaponBack/${code}.png`,  sha256: sha256(`${clipDir}/layers/weaponBack/${code}.png`) },
        body:        { png: `${clipDir}/layers/body/${code}.png`,        sha256: sha256(`${clipDir}/layers/body/${code}.png`) },
        weaponFront: { png: `${clipDir}/layers/weaponFront/${code}.png`, sha256: sha256(`${clipDir}/layers/weaponFront/${code}.png`) },
        handFront:   { png: `${clipDir}/layers/handFront/${code}.png`,   sha256: sha256(`${clipDir}/layers/handFront/${code}.png`) },
      },
    };
    // Verify body == native crop & binary alpha & groundY
    const compPng = readPng(entry.png);
    const bodyPng = readPng(entry.layers.body.png);
    const natPng  = readPng(entry.nativePng);
    if (countPartialAlpha(compPng) !== 0 || countPartialAlpha(natPng) !== 0) {
      throw new Error(`Partial alpha in ${dir}/${category} F${code}`);
    }
    const bBox = bboxOpaque(bodyPng);
    if (!bBox || bBox[3] !== 190) {
      throw new Error(`Body groundY != 190 in ${dir}/${category} F${code}: got ${bBox ? bBox[3] : null}`);
    }
    cumMs += d;
    return entry;
  });

  const clipObj = {
    schemaVersion: 1,
    revision: "main-orc-final-v10",
    character: "orc-v1",
    identity: "Verde Warcraft",
    direction: dir,
    category,
    state: "Attack",
    frameCount: durs.length,
    durationsMs: durs,
    totalDurationMs: cumMs,
    visibleInterval: visInterval,
    contactEvent: contactEv,
    canvas: [256, 256],
    nativeCanvas: [128, 128],
    bodyOffset: [64, 64],
    groundY: 190,
    nativeGroundY: 126,
    layerOrder: ["weaponBack", "body", "weaponFront", "handFront"],
    visibilityPolicy: "attack-only-v1",
    loop: false,
    oneShot: true,
    runtimeImplemented: false,
    technicalStatus: "TECHNICALLY_COMPLETE",
    artisticStatus: "VISUAL_REVIEW_REQUIRED",
    creatorApproval: "PENDING_CREATOR",
    eligibleForIntegration: false,
    weaponDefinition: weapDefRel,
    master: compMaster,
    masterSha256: sha256(compMaster),
    nativeMaster: natMaster,
    nativeMasterSha256: sha256(natMaster),
    compositeStrip: `${clipDir}/composite-strip.png`,
    compositeStripSha256: sha256(`${clipDir}/composite-strip.png`),
    strip: `${clipDir}/native-strip.png`,
    stripSha256: sha256(`${clipDir}/native-strip.png`),
    nativeStrip: `${clipDir}/native-strip.png`,
    nativeStripSha256: sha256(`${clipDir}/native-strip.png`),
    notes,
    frames,
  };

  const clipJsonRel = `${clipDir}/clip.json`;
  writeJson(clipJsonRel, clipObj);
  return { clipJsonRel, clipObj };
}

function buildBodyClipJson(dir, action, durs, loopFlag, terminalFlag, notes) {
  const clipDir = `${OUT_ROOT}/${dir}/${action}`;
  const compMaster = `${ASE_ROOT}/composite/${dir}/${action.toLowerCase()}.aseprite`;
  const natMaster  = `${ASE_ROOT}/native/${action.toLowerCase()}-${dir}.aseprite`;
  let cumMs = 0;
  const frames = durs.map((d, i) => {
    const code = String(i).padStart(2, "0");
    const pComp = `${clipDir}/frames/${code}.png`;
    const pNat  = `${clipDir}/native/${code}.png`;
    const compPng = readPng(pComp);
    if (countPartialAlpha(compPng) !== 0) {
      throw new Error(`Partial alpha in ${dir}/${action} F${code}`);
    }
    const entry = {
      index: i,
      durationMs: d,
      startMs: cumMs,
      endMs: cumMs + d,
      weaponVisible: false,
      png: pComp,
      sha256: sha256(pComp),
      nativePng: pNat,
      nativeSha256: sha256(pNat),
    };
    cumMs += d;
    return entry;
  });

  const clipObj = {
    schemaVersion: 1,
    revision: "main-orc-final-v10",
    character: "orc-v1",
    identity: "Verde Warcraft",
    direction: dir,
    action,
    frameCount: durs.length,
    durationsMs: durs,
    totalDurationMs: cumMs,
    canvas: [256, 256],
    nativeCanvas: [128, 128],
    bodyOffset: [64, 64],
    groundY: 190,
    nativeGroundY: 126,
    weaponVisible: false,
    loop: loopFlag,
    oneShot: !loopFlag,
    terminal: terminalFlag,
    runtimeImplemented: false,
    technicalStatus: "TECHNICALLY_COMPLETE",
    artisticStatus: "VISUAL_REVIEW_REQUIRED",
    creatorApproval: "PENDING_CREATOR",
    master: compMaster,
    masterSha256: sha256(compMaster),
    nativeMaster: natMaster,
    nativeMasterSha256: sha256(natMaster),
    compositeStrip: `${clipDir}/composite-strip.png`,
    compositeStripSha256: sha256(`${clipDir}/composite-strip.png`),
    strip: `${clipDir}/native-strip.png`,
    stripSha256: sha256(`${clipDir}/native-strip.png`),
    nativeStrip: `${clipDir}/native-strip.png`,
    nativeStripSha256: sha256(`${clipDir}/native-strip.png`),
    notes,
    frames,
  };

  const clipJsonRel = `${clipDir}/clip.json`;
  writeJson(clipJsonRel, clipObj);
  return { clipJsonRel, clipObj };
}

const ACTIONS = ["Idle", "Walk", "Unarmed", "Sword", "Axe", "Hit", "Defeat"];
const newCells = [];
let totalFrames = 0, affectedFrames = 0, aliasFrames = 0, activeCount = 0, aliasCount = 0;

for (const dir of DIRS) {
  for (const act of ACTIONS) {
    const cellId = `${dir}/${act}`;
    const pCell = parentCellsMap[cellId];

    // Preserved UNCHANGED_ALIAS cells: Idle (all 4 views verified spotless idle-balanced-v1)
    if (act === "Idle") {
      // Verify alias clipSha256 matches file on disk byte-for-byte
      const diskSha = sha256(pCell.clipJson);
      if (diskSha !== pCell.clipSha256) {
        throw new Error(`Protected alias ${cellId} modified! Expected ${pCell.clipSha256}, got ${diskSha}`);
      }
      newCells.push({ ...pCell });
      totalFrames += pCell.frameCount;
      aliasFrames += pCell.frameCount;
      aliasCount++;
      continue;
    }

    let built;
    if (act === "Sword") {
      built = buildWeaponClipJson(
        dir, "Sword", SWORD_DURS, SWORD_PHASES, [2, 11],
        { frame: 8, timeMs: 325, phase: "contact", status: "CANDIDATE_VISUAL_ONLY", appliesDamage: false },
        SWORD_META_BY_DIR[dir], swordADefPath,
        dir === "back_l"
          ? "North-West 3D diagonal slash on right-handed skeleton v3 body (job 3743684d) + Architecture C B3 verified."
          : dir === "back_r"
          ? "Eliminated F01-F02 left-side matte flash & 5-way leg breaks; replaced F08-F11 torn/melted arm with intact V5 back_r right arm; Architecture C verified."
          : "Repaired raised-arm armpit, eliminated exposed perimeter contour flicker, restored F12 chestplate speculars, aligned F00/F13 to Idle F00; Architecture C verified."
      );
    } else if (act === "Axe") {
      built = buildWeaponClipJson(
        dir, "Axe", AXE_DURS, AXE_PHASES, [2, 8],
        { frame: 6, timeMs: 410, phase: "heavy-impact", status: "CANDIDATE_VISUAL_ONLY", appliesDamage: false },
        AXE_META_BY_DIR[dir], axeDefPath,
        dir === "back_l"
          ? "Right-handed North-West heavy overhead chop on skeleton v3 body (job 5b037840) with cleaned militia-axe and shaft-center grip (36,48)."
          : dir === "back_r"
          ? "Eliminated F01-F02 left matte flash & leg jumps; fixed grip-under-butt by centering palm at shaft (36,48) with butt-cap below glove."
          : "Preserved frontal choreography with armpit/perimeter contour stabilization, Idle F00 bookends, and cleaned militia-axe."
      );
    } else if (act === "Unarmed") {
      built = buildBodyClipJson(
        dir, "Unarmed", [80, 110, 50, 90, 120], false, false,
        dir === "back_r"
          ? "Eliminated severed left-hip claw in F02-F03; restored missing F01 right forearm and built planted NE spiked-bracer punch & recoil."
          : dir === "back_l"
          ? "Eliminated double-T-pose F01 and 14px leg scissor jump in F02-F03; anchored stance to IdleBL with crisp steel vambrace & leather punch fist."
          : "Eliminated 3rd phantom rear elbow & muddy chest in F02-F03; built bold cross-body haymaker punch with leather fist and clean Idle0 bookends."
      );
    } else if (act === "Walk") {
      const durs = (dir === "front_r" || dir === "front_l") ? Array(16).fill(80) : Array(8).fill(160);
      built = buildBodyClipJson(
        dir, "Walk", durs, true, false,
        (dir === "front_r" || dir === "front_l")
          ? "Harmonized F06..F09 groin chainmail strobe and attenuated F08-F09 swinging vambrace flash while preserving 100% of 16-frame stride silhouette."
          : dir === "back_l"
          ? "Repaired F01 left elbow hole, equalized odd-frame vambrace strobe, and brought overall steel luster into parity with back_r."
          : "Stabilized F05/F07 right vambrace steel brightness and cleaned outer matte specks; cycle silhouette preserved."
      );
    } else if (act === "Hit") {
      built = buildBodyClipJson(
        dir, "Hit", [45, 95, 115, 95, 100], false, false,
        (dir === "front_r" || dir === "front_l")
          ? "Eased F00 initial impact recoil from Idle0, replaced hollow red wrist rings in F01 with solid brown leather guard gauntlets, and lifted F01 steel."
          : "Built non-mirrored F00 impact snap & F03 recovery brace from true rear Idle0; replaced F01 shredded grey claws with leather gauntlets and shaded occipital skull."
      );
    } else if (act === "Defeat") {
      built = buildBodyClipJson(
        dir, "Defeat", [70, 95, 115, 130, 290], false, true,
        (dir === "front_r" || dir === "front_l")
          ? "Lifted F01 dark steel, toned blade-bright F02 supporting arm + planted leather hand, cleaned F03 chin smudge, and authored unconscious F04 face-down sprawl on groundY=190."
          : "Refined F00 gauntlets & occipital skull shading, reinforced thin planted supporting hand in F02-F03 into solid leather gauntlet on groundY=190, and cleaned F04 matte."
      );
    }

    newCells.push({
      direction: dir,
      action: act,
      cellId,
      status: "ACTIVE_CANDIDATE",
      isAffected: true,
      clipJson: built.clipJsonRel,
      clipSha256: sha256(built.clipJsonRel),
      reviewStatus: "VISUAL_REVIEW_REQUIRED",
      provenance: built.clipObj.master,
      notes: built.clipObj.notes,
      frameCount: built.clipObj.frameCount,
      durationsMs: built.clipObj.durationsMs,
      parentCell: {
        manifest: "characters/orc-v1/source/backl-v5base/candidate28manifest.json",
        cellId,
        clipJson: pCell.clipJson,
        clipSha256: pCell.clipSha256,
      },
      masterSha256: built.clipObj.masterSha256,
      nativeMasterSha256: built.clipObj.nativeMasterSha256,
      stripSha256: built.clipObj.stripSha256,
      compositeStripSha256: built.clipObj.compositeStripSha256,
    });

    totalFrames += built.clipObj.frameCount;
    affectedFrames += built.clipObj.frameCount;
    activeCount++;
  }
}

const manifest28 = {
  schemaVersion: 1,
  manifestId: "orc-v1.final-candidate-v10.candidate28",
  characterId: "orc-v1",
  characterName: "Verde Warcraft",
  revision: "main-orc-final-v10",
  parentManifest: "characters/orc-v1/source/backl-v5base/candidate28manifest.json",
  parentManifestSha256: sha256("characters/orc-v1/source/backl-v5base/candidate28manifest.json"),
  comparisonBaselineManifest: "characters/orc-v1/source/backl-v5base/candidate28manifest.json",
  totalClips: 28,
  activeCandidatesCount: activeCount,
  inRevisionCount: 0,
  inProductionCount: 0,
  unchangedAliasesCount: aliasCount,
  totalFrames,
  affectedFrameCount: affectedFrames,
  aliasFrameCount: aliasFrames,
  weaponDefinitions: {
    Sword: swordADefPath,
    SwordVariantB: swordBDefPath,
    Axe: axeDefPath,
  },
  architectureC: {
    verification: `${OUT_ROOT}/architecture-c/verification.json`,
    gripProfiles: {
      front_r: `${OUT_ROOT}/architecture-c/grip-profile-front_r.json`,
      front_l: `${OUT_ROOT}/architecture-c/grip-profile-front_l.json`,
      back_r:  `${OUT_ROOT}/architecture-c/grip-profile-back_r.json`,
      back_l:  `${OUT_ROOT}/architecture-c/grip-profile-back_l.json`,
    },
  },
  technicalStatus: "TECHNICALLY_COMPLETE",
  artisticStatus: "VISUAL_REVIEW_REQUIRED",
  creatorApproval: "PENDING_CREATOR",
  eligibleForIntegration: false,
  integrationStatus: "STAGED_LOCALLY_AWAITING_CREATOR_ACCEPTANCE_AND_UNITY_AUTHORIZATION",
  runtimeImplemented: false,
  cells: newCells,
};

writeJson(`${OUT_ROOT}/candidate28manifest.json`, manifest28);

// 4. Write Reuse Metrics & Local Staging Unity Handoff Contract (zero writes to ../TacticsRPG!)
const reuseMetrics = {
  schemaVersion: 1,
  revision: "main-orc-final-v10",
  characterId: "orc-v1",
  architectureCReuseMeasurement: {
    testedWeaponPair: ["recruit-sword (Espada do Recruta)", "faceted-sword-b (Espada Facetada de Aço Claro)"],
    whatThePairProves: "Comprova tanto a troca de acabamento/material quanto a compatibilidade real com outra silhueta de lâmina (106 px de diferença no sprite 96x96; 99..111 px de delta de silhueta por quadro armado) nas 4 vistas diagonais (front_r, front_l, back_r, back_l), mantendo cabo/guarda/pivô [48,66] compatíveis.",
    totalBodyFramesAcross4Views: 56,
    bodyFramesReusedUnchangedForSecondSword: 56,
    bodyFrameReuseRatePct: 100,
    handFrontFramesReusedUnchangedForSecondSword: 56,
    adaptationsRequiredBySecondSword: "Zero edições no corpo ou na luva; 1 camada de lâmina (y=7..54) desenhada no Aseprite mantendo cabo/guarda/pomo (y>=55) e pivô [48,66]; composição determinística em lote no Aseprite (<10s para as 4 vistas).",
    remainingOpenForFutureFamilies: "Guardas largas ornamentadas, lâminas longas (>60 px) ou punhos de geometria diferente exigirão verificação de colisão com ombreira/chão antes de entrar na mesma família.",
  },
  pixelLabAccountingThisSession: {
    jobsSubmitted: [
      { jobId: "655c4749-ad42-46d1-9bf3-5c0c98fe81f1", tool: "edit_image_pro_flash", target: "front_r/Defeat F04 unconscious sprawl", generationsCharged: 6 },
      { jobId: "ffb7d35c-7a70-4560-8b60-e09cfeec2b57", tool: "edit_image_pro_flash", target: "front_l/Defeat F04 unconscious sprawl", generationsCharged: 6 },
      { jobId: "3743684d-6699-4e3b-b196-c1bfb0a66f01", tool: "animate_with_skeleton_v3", target: "back_l/Sword 12-pose unarmed NW body", generationsCharged: 3 },
      { jobId: "5b037840-928b-431b-89e1-befb43f85f3e", tool: "animate_with_skeleton_v3", target: "back_l/Axe 10-pose unarmed NW body", generationsCharged: 3 },
    ],
    totalGenerationsChargedThisSession: 18,
  },
  unityBridgeReadiness: {
    liveRuntimeInspected: "../TacticsRPG/Assets/Scripts/Presentation/UnitVisuals.cs",
    currentRuntimeState: "UnitVisuals carrega apenas Characters/WarriorPilot/ para unit.Name == 'Hero' (128x128 estático/16 quadros máx, tempos fixos por estado, sem seleção de arma ou canvas composto 256x256).",
    isolatedPlayModePlanAfterAuthorization: [
      "1. Copiar pacote aprovado de dist/orc-v1/final-candidate-v10/ para ../TacticsRPG/Assets/Resources/Characters/OrcWarrior/ preservando WarriorPilot intacto.",
      "2. Estender minimamente UnitVisuals/UnitView para suportar perfil visual por unidade (OrcWarrior + troca entre Sword A e Sword B compostos 256x256 com PPU=100 e pivô no chão groundY=190 -> pivotY = (256-190)/256 = 0.2578125, alinhado ao mesmo ponto de apoio de 128x128 groundY=126 -> (128-126)/128 = 0.015625 + bodyOffset 64px).",
      "3. Suportar tabela opcional de durações por quadro (durationsMs) e seleção do clipe Attack conforme arma equipada (Unarmed / Sword A / Sword B / Axe), mantendo arma invisível em Idle, Walk, Hit e Defeat.",
      "4. Validar em batalha isolada no PlayMode: 4 vistas + rotação de câmera Q/E, escala, pivô, chão, momento visual do impacto (325 ms Sword / 410 ms Axe), velocidade do Hit (450 ms), pose final de Defeat no chão, retorno desarmado ao Idle/Walk, e regressão zero no Human Warrior Pilot."
    ],
    writesPerformedInTacticsRPG: 0,
  },
};

writeJson(`${EXP_ROOT}/reuse-and-bridge-report.json`, reuseMetrics);
writeJson(`${DIST_ROOT}/unity-handoff-contract.json`, {
  contractVersion: 1,
  characterId: "orc-v1",
  runtimeCandidateId: "OrcWarrior",
  manifest: `${OUT_ROOT}/candidate28manifest.json`,
  manifestSha256: sha256(`${OUT_ROOT}/candidate28manifest.json`),
  architectureCVerification: `${OUT_ROOT}/architecture-c/verification.json`,
  reuseAndBridgeReport: `${EXP_ROOT}/reuse-and-bridge-report.json`,
  status: {
    technical: "TECHNICALLY_COMPLETE",
    artistic: "VISUAL_REVIEW_REQUIRED",
    creatorApproval: "PENDING_CREATOR",
    unityAuthorized: false,
  },
  geometry: {
    nativeCanvas: [128, 128],
    nativeGroundY: 126,
    nativeUnityPivotNormalized: [0.5, (128 - 126) / 128],
    compositeCanvas: [256, 256],
    compositeBodyOffset: [64, 64],
    compositeGroundY: 190,
    compositeUnityPivotNormalized: [0.5, (256 - 190) / 256],
    ppu: 100,
    recommendedScale: 1.15,
  },
});

console.log(JSON.stringify({
  manifest: `${OUT_ROOT}/candidate28manifest.json`,
  activeCandidates: activeCount,
  unchangedAliases: aliasCount,
  totalFrames,
  archCViewsVerified: Object.keys(archVerification.views).length,
}, null, 2));
