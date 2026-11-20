#!/usr/bin/env node
// Builds the exact `animate_with_skeleton_v3` payload from the motion-design output.
// Dry run by default: it validates and writes the payload, it never calls PixelLab.
// The single authorized generation is issued by the Orchestrator, not by this script.

import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve(import.meta.dirname, '../..');
const EXPERIMENT = path.join(ROOT, 'experiments/main-orc-skeleton-first-01');
const REFERENCE = 'characters/orc-v1/source/combat-recovery-v8/rear-arc/back_l-sword/frames/02.png';

const COCO18 = [
  'NOSE', 'NECK',
  'RIGHT SHOULDER', 'RIGHT ELBOW', 'RIGHT ARM',
  'LEFT SHOULDER', 'LEFT ELBOW', 'LEFT ARM',
  'RIGHT HIP', 'RIGHT KNEE', 'RIGHT LEG',
  'LEFT HIP', 'LEFT KNEE', 'LEFT LEG',
  'RIGHT EYE', 'LEFT EYE', 'RIGHT EAR', 'LEFT EAR',
];

const read = file => JSON.parse(fs.readFileSync(path.join(EXPERIMENT, file), 'utf8'));
const fail = message => { console.error(`FALHA: ${message}`); process.exitCode = 1; };

let poses, sequence;
try {
  poses = read(process.env.POSES_FILE ?? 'poses.json');
  sequence = read(process.env.SEQUENCE_FILE ?? 'sequence.json');
} catch (error) {
  console.error(`Sem poses.json/sequence.json ainda: ${error.message}`);
  process.exit(2);
}

const frames = sequence.frames ?? [];
if (frames.length < 3 || frames.length > 15) fail(`precisa de 3 a 15 quadros, veio ${frames.length}`);

const normalize = (list, where) => {
  if (!Array.isArray(list)) { fail(`${where}: juntas ausentes`); return null; }
  const byLabel = new Map();
  for (const joint of list) {
    const label = String(joint.label ?? '').toUpperCase().replace(/\s+/g, ' ').trim();
    if (!COCO18.includes(label)) { fail(`${where}: rótulo desconhecido "${joint.label}"`); continue; }
    if (byLabel.has(label)) fail(`${where}: rótulo repetido "${label}"`);
    for (const axis of ['x', 'y']) {
      const value = Number(joint[axis]);
      if (!Number.isFinite(value) || value < 0 || value > 1) fail(`${where}/${label}: ${axis}=${joint[axis]} fora de 0..1`);
    }
    byLabel.set(label, { label, x: Number(joint.x), y: Number(joint.y), z_index: Number.isInteger(joint.z_index) ? joint.z_index : 0, ...(Number.isFinite(joint.depth) ? { depth: joint.depth } : {}) });
  }
  const missing = COCO18.filter(label => !byLabel.has(label));
  if (missing.length) fail(`${where}: faltam ${missing.join(', ')}`);
  return COCO18.map(label => byLabel.get(label)).filter(Boolean);
};

const keypoints = frames.map((frame, index) => normalize(frame.joints, `quadro ${index} (${frame.phase ?? '?'})`));
if (keypoints.some(k => k === null)) process.exit(1);

// The reference frame is the pose the sprite is already in, so it must be pose 0.
const first = normalize((poses.poses ?? [])[0]?.joints, 'pose 0 (ready)');
if (first) {
  const drifted = keypoints[0].filter((joint, i) => Math.hypot(joint.x - first[i].x, joint.y - first[i].y) > 0.01);
  if (drifted.length) fail(`keypoints[0] diverge da pose 0 em ${drifted.length} juntas: ${drifted.map(j => j.label).join(', ')}`);
}

// Anatomy sanity: limb lengths must not breathe between poses.
const dist = (a, b) => Math.hypot(a.x - b.x, a.y - b.y);
const BONES = [
  ['RIGHT SHOULDER', 'RIGHT ELBOW', 'úmero direito'],
  ['RIGHT ELBOW', 'RIGHT ARM', 'antebraço direito'],
  ['LEFT SHOULDER', 'LEFT ELBOW', 'úmero esquerdo'],
  ['LEFT ELBOW', 'LEFT ARM', 'antebraço esquerdo'],
  ['RIGHT HIP', 'RIGHT KNEE', 'coxa direita'],
  ['RIGHT KNEE', 'RIGHT LEG', 'canela direita'],
  ['LEFT HIP', 'LEFT KNEE', 'coxa esquerda'],
  ['LEFT KNEE', 'LEFT LEG', 'canela esquerda'],
];
const anatomy = [];
for (const [a, b, name] of BONES) {
  const lengths = keypoints.map(frame => {
    const ja = frame.find(j => j.label === a), jb = frame.find(j => j.label === b);
    return dist(ja, jb);
  });
  const min = Math.min(...lengths), max = Math.max(...lengths);
  const spread = min > 0 ? (max / min - 1) * 100 : Infinity;
  anatomy.push({ bone: name, min: +min.toFixed(4), max: +max.toFixed(4), spreadPercent: +spread.toFixed(1) });
  if (spread > 12) fail(`${name} varia ${spread.toFixed(1)}% entre quadros (limite 12%)`);
}

// Ground contact: ankles must not sink below the floor line.
const GROUND = 190 / 256;
for (const [index, frame] of keypoints.entries()) {
  for (const label of ['RIGHT LEG', 'LEFT LEG']) {
    const ankle = frame.find(j => j.label === label);
    if (ankle.y > GROUND + 0.03) fail(`quadro ${index}: ${label} em y=${ankle.y.toFixed(3)} abaixo do chão ${GROUND.toFixed(3)}`);
  }
}

const payload = {
  description: 'armoured green orc warrior in dark steel plate with red trim, holding a straight double-edged steel sword with leather-wrapped grip',
  action: 'sword attack',
  direction: 'north-west',
  keypoints,
  first_frame_keypoints: first,
  template_id: 'mannequin',
  view: 'low top-down',
  no_background: true,
  seed: 20261030,
};

const outPath = path.join(EXPERIMENT, 'pixellab-payload.json');
fs.writeFileSync(outPath, `${JSON.stringify(payload, null, 1)}\n`);
fs.writeFileSync(path.join(EXPERIMENT, 'pixellab-anatomy.json'), `${JSON.stringify(anatomy, null, 2)}\n`);

console.log(`payload: ${outPath}`);
console.log(`quadros: ${keypoints.length} | direção: ${payload.direction} | referência: ${REFERENCE}`);
console.log('estabilidade de membros:');
for (const row of anatomy) console.log(`  ${row.bone.padEnd(20)} min ${row.min} max ${row.max}  variação ${row.spreadPercent}%`);
console.log(process.exitCode ? 'RESULTADO: FALHOU — não enviar' : 'RESULTADO: PAYLOAD VÁLIDO — pronto para a chamada única');
