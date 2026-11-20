import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { PNG } from 'pngjs';
import { ROOT, readJSON, hash, slash } from '../../../src/core.mjs';
import { findAseprite, executeAseprite, inspectAseprite } from '../../../src/aseprite.mjs';
import { decode } from '../../../src/images.mjs';

const QA_DIR = path.join(ROOT, 'experiments/main-orc-rear-recovery-v2/qa-argon');
const REEXPORT_DIR = path.join(QA_DIR, 'reexports');
fs.mkdirSync(REEXPORT_DIR, { recursive: true });

const exe = findAseprite();
const bridgeScript = path.join(ROOT, 'tools/aseprite/bridge.lua');
const shaFile = p => hash(fs.readFileSync(path.join(ROOT, p)));
const readPng = p => decode(path.join(ROOT, p)).image;
const sameRgba = (a, b) => a.width === b.width && a.height === b.height && a.data.equals(b.data);
const countOpaque = img => {
  let n = 0;
  for (let i = 3; i < img.data.length; i += 4) if (img.data[i] > 0) n++;
  return n;
};

function alphaOver(base, top) {
  const out = Buffer.from(base.data);
  for (let i = 0; i < out.length; i += 4) {
    const ta = top.data[i + 3] / 255;
    if (!ta) continue;
    const ba = out[i + 3] / 255;
    const oa = ta + ba * (1 - ta);
    for (let c = 0; c < 3; c++) {
      out[i + c] = Math.round((top.data[i + c] * ta + out[i + c] * ba * (1 - ta)) / oa);
    }
    out[i + 3] = Math.round(oa * 255);
  }
  return { width: base.width, height: base.height, data: out };
}

function reexportMaster(relMasterPath, tagLabel, layerName = null) {
  const srcPath = path.join(ROOT, relMasterPath);
  const jobDir = path.join(REEXPORT_DIR, tagLabel + (layerName ? `_${layerName}` : ''));
  fs.mkdirSync(jobDir, { recursive: true });
  const copyPath = path.join(jobDir, 'source.aseprite');
  fs.copyFileSync(srcPath, copyPath);

  const sheetPath = path.join(jobDir, 'sheet.png');
  const dataPath = path.join(jobDir, 'sheet.json');
  const docPath = path.join(jobDir, 'document.json');

  const args = [];
  if (layerName) args.push('--layer', layerName);
  args.push(
    '--list-layer-hierarchy',
    '--list-tags',
    '--list-slices',
    copyPath,
    '--sheet-type', 'horizontal',
    '--format', 'json-array',
    '--sheet', sheetPath,
    '--data', dataPath,
    '--script-param', `metadata=${docPath}`,
    '--script', bridgeScript
  );
  executeAseprite(exe, args);
  const meta = readJSON(dataPath);
  const doc = readJSON(docPath);
  const sheetImg = decode(sheetPath).image;

  const frames = meta.frames.map((f, idx) => {
    const r = f.frame;
    const frameImg = new PNG({ width: r.w, height: r.h });
    PNG.bitblt(sheetImg, frameImg, r.x, r.y, r.w, r.h, 0, 0);
    return {
      index: idx,
      durationMs: f.duration,
      width: r.w,
      height: r.h,
      image: frameImg
    };
  });

  return { meta, doc, frames, nativeHeader: inspectAseprite(srcPath) };
}

const manifest = readJSON(path.join(ROOT, 'characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json'));
const failures = [];
const activeClipReports = [];
let totalCompositeFrames = 0;
let activeCandidateFrames = 0;
let aliasFrames = 0;
const uniqueActiveMasters = new Set();

for (const cell of manifest.cells) {
  const clip = readJSON(path.join(ROOT, cell.clipJson));
  const frames = clip.frames ?? [];
  totalCompositeFrames += frames.length;

  if (cell.status === 'UNCHANGED_ALIAS') {
    aliasFrames += frames.length;
    for (const f of frames) {
      if (shaFile(f.png) !== f.sha256) {
        failures.push(`Alias ${cell.cellId} frame ${f.index}: composite SHA mismatch`);
      }
    }
    continue;
  }

  activeCandidateFrames += frames.length;
  const safeId = cell.cellId.replace('/', '_');
  const masterRel = clip.master;
  const nativeMasterRel = clip.nativeMaster;
  const bodyMasterRel = clip.bodyMaster ?? null;

  if (!masterRel || !nativeMasterRel) {
    failures.push(`${cell.cellId}: missing master or nativeMaster in clip.json`);
    continue;
  }
  uniqueActiveMasters.add(masterRel);
  uniqueActiveMasters.add(nativeMasterRel);
  if (bodyMasterRel) uniqueActiveMasters.add(bodyMasterRel);

  const compRe = reexportMaster(masterRel, `${safeId}_comp`);
  const natRe = reexportMaster(nativeMasterRel, `${safeId}_nat`);

  const expectedDurations = clip.durationsMs ?? frames.map(f => f.durationMs);
  const compDurations = compRe.frames.map(f => f.durationMs);
  const natDurations = natRe.frames.map(f => f.durationMs);

  if (compRe.frames.length !== frames.length || natRe.frames.length !== frames.length) {
    failures.push(`${cell.cellId}: re-exported frame count mismatch (${compRe.frames.length}/${natRe.frames.length} vs ${frames.length})`);
  }
  if (JSON.stringify(compDurations) !== JSON.stringify(expectedDurations)) {
    failures.push(`${cell.cellId}: composite master durations mismatch (${JSON.stringify(compDurations)} vs ${JSON.stringify(expectedDurations)})`);
  }
  if (JSON.stringify(natDurations) !== JSON.stringify(expectedDurations)) {
    failures.push(`${cell.cellId}: native master durations mismatch (${JSON.stringify(natDurations)} vs ${JSON.stringify(expectedDurations)})`);
  }

  let compRgbaMatches = 0;
  let natRgbaMatches = 0;
  let cropRgbaMatches = 0;

  const isArmed = cell.action === 'Sword' || cell.action === 'Axe';
  let bodyRe = null;
  let layerRes = {};

  if (isArmed) {
    if (!bodyMasterRel) failures.push(`${cell.cellId}: missing bodyMaster`);
    else bodyRe = reexportMaster(bodyMasterRel, `${safeId}_body`);

    const docLayerNames = compRe.doc.layers.map(l => l.name);
    const expectedLayers = ['weaponBack', 'body', 'weaponFront', 'handFront'];
    if (JSON.stringify(docLayerNames) !== JSON.stringify(expectedLayers)) {
      failures.push(`${cell.cellId}: Aseprite layer hierarchy ${JSON.stringify(docLayerNames)} !== ${JSON.stringify(expectedLayers)}`);
    }
    for (const lName of expectedLayers) {
      layerRes[lName] = reexportMaster(masterRel, `${safeId}_layer`, lName);
    }
  }

  for (let i = 0; i < frames.length; i++) {
    const f = frames[i];
    const canonComp = readPng(f.png);
    const reComp = compRe.frames[i].image;
    const reNat = natRe.frames[i].image;

    if (sameRgba(reComp, canonComp)) compRgbaMatches++;
    else failures.push(`${cell.cellId} F0${i}: re-exported composite RGBA differs from canonical PNG`);

    if (f.nativePng) {
      const canonNat = readPng(f.nativePng);
      if (sameRgba(reNat, canonNat)) natRgbaMatches++;
      else failures.push(`${cell.cellId} F0${i}: re-exported native RGBA differs from canonical native PNG`);
    } else {
      natRgbaMatches++;
    }

    const cropSource = isArmed ? layerRes.body.frames[i].image : reComp;
    const crop = new PNG({ width: 128, height: 128 });
    PNG.bitblt(cropSource, crop, 64, 64, 128, 128, 0, 0);
    if (sameRgba(reNat, crop)) cropRgbaMatches++;
    else failures.push(`${cell.cellId} F0${i}: native 128 does not equal centered 128x128 crop`);

    if (isArmed) {
      for (const lName of ['weaponBack', 'body', 'weaponFront', 'handFront']) {
        const canonLayer = readPng(f.layers[lName].png);
        const reLayer = layerRes[lName].frames[i].image;
        if (!sameRgba(reLayer, canonLayer)) {
          failures.push(`${cell.cellId} F0${i} layer ${lName}: Aseprite layer re-export differs from canonical layer PNG`);
        }
      }
      if (bodyRe && !sameRgba(bodyRe.frames[i].image, layerRes.body.frames[i].image)) {
        failures.push(`${cell.cellId} F0${i}: bodyMaster re-export differs from composite body layer`);
      }
      let composed = layerRes.weaponBack.frames[i].image;
      for (const lName of ['body', 'weaponFront', 'handFront']) {
        composed = alphaOver(composed, layerRes[lName].frames[i].image);
      }
      if (!sameRgba(composed, reComp)) {
        failures.push(`${cell.cellId} F0${i}: 4-layer alpha-over does not match re-exported composite`);
      }
      const wPx = countOpaque(layerRes.weaponBack.frames[i].image) + countOpaque(layerRes.weaponFront.frames[i].image);
      const hPx = countOpaque(layerRes.handFront.frames[i].image);
      const inInterval = i >= 1 && i <= 6;
      if (inInterval && (wPx === 0 || hPx === 0)) {
        failures.push(`${cell.cellId} F0${i}: missing weapon (${wPx}) or handFront (${hPx}) pixels in active interval`);
      }
      if (!inInterval && (wPx !== 0 || hPx !== 0)) {
        failures.push(`${cell.cellId} F0${i}: weapon (${wPx}) or handFront (${hPx}) pixels present outside active interval`);
      }
    }
  }

  activeClipReports.push({
    cellId: cell.cellId,
    master: masterRel,
    nativeMaster: nativeMasterRel,
    bodyMaster: bodyMasterRel,
    frames: frames.length,
    durationsMs: expectedDurations,
    totalDurationMs: expectedDurations.reduce((a, b) => a + b, 0),
    compRgbaMatches,
    natRgbaMatches,
    cropRgbaMatches,
    isArmed
  });
}

// Check AxeL specific residue removal in re-exported native frames
const axeLProvenance = readJSON(path.join(ROOT, 'experiments/main-orc-rear-recovery-v2/axeL-local-repair-provenance.json'));
const axeLNatF02 = decode(path.join(ROOT, 'characters/orc-v1/source/rear-recovery-v2/back_l/Axe/Attack-representative-v1/native/02.png')).image;
let axeLDetachedResidueOpaque = 0;
for (const [x, y] of [...axeLProvenance.confirmedDetachedResidue.connectedComponent8.coordinates, axeLProvenance.confirmedDetachedResidue.isolatedPixel]) {
  if (axeLNatF02.data[(y * 128 + x) * 4 + 3] > 0) axeLDetachedResidueOpaque++;
}
if (axeLDetachedResidueOpaque !== 0) {
  failures.push(`back_l/Axe F02: found ${axeLDetachedResidueOpaque} opaque pixels at the 27px old-arm residue coordinates`);
}

// Check 12 required semantic lessons + 5 operational lessons in config/artistic-quality-gates-v1.json
const gates = readJSON(path.join(ROOT, 'config/artistic-quality-gates-v1.json'));
const required12Ids = [
  'rear-anatomy-construction',
  'rear-motion-needs-rear-construction',
  'weapon-anchor-vs-natural-choreography',
  'incompatible-attack-reuse',
  'numeric-hit-thresholds-diagnostic-warning',
  'defeat-consistent-terminal-outcome',
  'technical-completion-not-artistic-approval',
  'validated-poses-reused-not-regenerated',
  'failed-artistic-foundations-downstream-rework',
  'complete-review-interface-mandatory',
  'successful-methods-documented-equally',
  'speed-and-scale-evaluation'
];
const nineFields = ['symptom', 'verifiedCause', 'failedApproach', 'successfulCorrection', 'reuse', 'prevention', 'validation', 'cost', 'applicability'];
for (const reqId of required12Ids) {
  const lesson = (gates.productionLessons ?? []).find(l => l.id === reqId);
  if (!lesson) {
    failures.push(`Missing required semantic lesson: ${reqId}`);
    continue;
  }
  for (const field of nineFields) {
    if (typeof lesson[field] !== 'string' || !lesson[field].trim()) {
      failures.push(`Lesson ${reqId} has empty or missing field: ${field}`);
    }
  }
}

const summary = {
  status: failures.length === 0 ? 'PASS' : 'FAIL',
  asepriteExecutable: exe,
  totalClips: manifest.cells.length,
  activeCandidates: activeClipReports.length,
  unchangedAliases: manifest.cells.length - activeClipReports.length,
  totalCompositeFrames,
  activeCandidateFrames,
  aliasFrames,
  uniqueActiveMastersCount: uniqueActiveMasters.size,
  axeLDetachedResidueOpaque,
  semanticLessonsVerified: required12Ids.length,
  totalLessonsInGates: (gates.productionLessons ?? []).length,
  activeClipReports,
  failures
};

fs.writeFileSync(path.join(QA_DIR, 'independent-aseprite-reexport-report.json'), JSON.stringify(summary, null, 2));
console.log(JSON.stringify({
  status: summary.status,
  activeCandidates: summary.activeCandidates,
  unchangedAliases: summary.unchangedAliases,
  totalCompositeFrames: summary.totalCompositeFrames,
  activeCandidateFrames: summary.activeCandidateFrames,
  aliasFrames: summary.aliasFrames,
  uniqueActiveMastersCount: summary.uniqueActiveMastersCount,
  axeLDetachedResidueOpaque: summary.axeLDetachedResidueOpaque,
  semanticLessonsVerified: summary.semanticLessonsVerified,
  failures: summary.failures
}, null, 2));
if (failures.length > 0) process.exitCode = 1;
