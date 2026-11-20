// Gerador do FIXTURE SINTÉTICO do visualizador skeleton-first.
// Produce viewer/fixtures/sample-poses.json + sample-sequence.json and their
// file://-loadable JS mirrors (sample-poses.js / sample-sequence.js).
// Os dados são ESQUEMÁTICOS e claramente rotulados como sintéticos: fases e
// durações copiam a grade pública do clip.json vigente (14 quadros / 730 ms,
// contato no índice 8 @ 325 ms); o esqueleto NÃO descreve o Orc real.
//   node viewer/tools/make-fixture.mjs
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const VIEWER = path.resolve(__dirname, '..');
const FIXTURES = path.join(VIEWER, 'fixtures');
fs.mkdirSync(FIXTURES, { recursive: true });

// Rótulos COCO-18 exatos do contrato PixelLab (ARM=punho, LEG=tornozelo).
const COCO = [
  'NOSE', 'NECK',
  'RIGHT SHOULDER', 'RIGHT ELBOW', 'RIGHT ARM',
  'LEFT SHOULDER', 'LEFT ELBOW', 'LEFT ARM',
  'RIGHT HIP', 'RIGHT KNEE', 'RIGHT LEG',
  'LEFT HIP', 'LEFT KNEE', 'LEFT LEG',
  'RIGHT EYE', 'LEFT EYE', 'RIGHT EAR', 'LEFT EAR',
];
const Z = { NOSE: 14, NECK: 10, 'RIGHT SHOULDER': 12, 'RIGHT ELBOW': 13, 'RIGHT ARM': 12, 'LEFT SHOULDER': 4, 'LEFT ELBOW': 3, 'LEFT ARM': 2, 'RIGHT HIP': 6, 'LEFT HIP': 5, 'RIGHT KNEE': 7, 'LEFT KNEE': 6, 'RIGHT LEG': 8, 'LEFT LEG': 7, 'RIGHT EYE': 15, 'LEFT EYE': 15, 'RIGHT EAR': 13, 'LEFT EAR': 16 };
const DEPTH = { NOSE: 205, NECK: 170, 'RIGHT SHOULDER': 185, 'RIGHT ELBOW': 190, 'RIGHT ARM': 195, 'LEFT SHOULDER': 75, 'LEFT ELBOW': 70, 'LEFT ARM': 65, 'RIGHT HIP': 150, 'LEFT HIP': 110, 'RIGHT KNEE': 145, 'LEFT KNEE': 115, 'RIGHT LEG': 140, 'LEFT LEG': 120, 'RIGHT EYE': 200, 'LEFT EYE': 200, 'RIGHT EAR': 195, 'LEFT EAR': 210 };

// Geometria sintética por pose (frações de 256; RIGHT do personagem à esquerda da tela, vista back_l).
const P = {
  ready: {
    'NOSE': [0.508, 0.312], 'NECK': [0.502, 0.368],
    'RIGHT EYE': [0.488, 0.306], 'LEFT EYE': [0.526, 0.306],
    'RIGHT EAR': [0.468, 0.314], 'LEFT EAR': [0.546, 0.314],
    'RIGHT SHOULDER': [0.438, 0.394], 'LEFT SHOULDER': [0.566, 0.394],
    'RIGHT ELBOW': [0.398, 0.462], 'LEFT ELBOW': [0.612, 0.462],
    'RIGHT ARM': [0.428, 0.528], 'LEFT ARM': [0.578, 0.532],
    'RIGHT HIP': [0.458, 0.562], 'LEFT HIP': [0.548, 0.562],
    'RIGHT KNEE': [0.448, 0.648], 'LEFT KNEE': [0.556, 0.648],
    'RIGHT LEG': [0.442, 0.734], 'LEFT LEG': [0.560, 0.734],
  },
  elevation: {
    'NOSE': [0.512, 0.310], 'NECK': [0.506, 0.368],
    'RIGHT EYE': [0.494, 0.304], 'LEFT EYE': [0.532, 0.304],
    'RIGHT EAR': [0.472, 0.312], 'LEFT EAR': [0.552, 0.312],
    'RIGHT SHOULDER': [0.436, 0.392], 'LEFT SHOULDER': [0.566, 0.394],
    'RIGHT ELBOW': [0.410, 0.340], 'LEFT ELBOW': [0.612, 0.462],
    'RIGHT ARM': [0.430, 0.330], 'LEFT ARM': [0.584, 0.540],
    'RIGHT HIP': [0.470, 0.562], 'LEFT HIP': [0.560, 0.562],
    'RIGHT KNEE': [0.460, 0.648], 'LEFT KNEE': [0.568, 0.648],
    'RIGHT LEG': [0.454, 0.734], 'LEFT LEG': [0.572, 0.734],
  },
  strike: {
    'NOSE': [0.492, 0.314], 'NECK': [0.488, 0.370],
    'RIGHT EYE': [0.474, 0.308], 'LEFT EYE': [0.512, 0.308],
    'RIGHT EAR': [0.454, 0.316], 'LEFT EAR': [0.532, 0.316],
    'RIGHT SHOULDER': [0.432, 0.396], 'LEFT SHOULDER': [0.566, 0.394],
    'RIGHT ELBOW': [0.376, 0.462], 'LEFT ELBOW': [0.612, 0.462],
    'RIGHT ARM': [0.330, 0.520], 'LEFT ARM': [0.596, 0.500],
    'RIGHT HIP': [0.448, 0.562], 'LEFT HIP': [0.538, 0.562],
    'RIGHT KNEE': [0.438, 0.648], 'LEFT KNEE': [0.546, 0.648],
    'RIGHT LEG': [0.432, 0.734], 'LEFT LEG': [0.550, 0.734],
  },
  follow: {
    'NOSE': [0.490, 0.316], 'NECK': [0.486, 0.372],
    'RIGHT EYE': [0.472, 0.310], 'LEFT EYE': [0.510, 0.310],
    'RIGHT EAR': [0.452, 0.318], 'LEFT EAR': [0.530, 0.318],
    'RIGHT SHOULDER': [0.430, 0.398], 'LEFT SHOULDER': [0.566, 0.394],
    'RIGHT ELBOW': [0.368, 0.470], 'LEFT ELBOW': [0.612, 0.462],
    'RIGHT ARM': [0.318, 0.545], 'LEFT ARM': [0.600, 0.505],
    'RIGHT HIP': [0.448, 0.562], 'LEFT HIP': [0.538, 0.562],
    'RIGHT KNEE': [0.438, 0.648], 'LEFT KNEE': [0.546, 0.648],
    'RIGHT LEG': [0.432, 0.734], 'LEFT LEG': [0.550, 0.734],
  },
  recover: {
    'NOSE': [0.506, 0.312], 'NECK': [0.500, 0.368],
    'RIGHT EYE': [0.487, 0.306], 'LEFT EYE': [0.525, 0.306],
    'RIGHT EAR': [0.467, 0.314], 'LEFT EAR': [0.545, 0.314],
    'RIGHT SHOULDER': [0.436, 0.394], 'LEFT SHOULDER': [0.566, 0.394],
    'RIGHT ELBOW': [0.396, 0.452], 'LEFT ELBOW': [0.612, 0.462],
    'RIGHT ARM': [0.404, 0.508], 'LEFT ARM': [0.582, 0.535],
    'RIGHT HIP': [0.458, 0.562], 'LEFT HIP': [0.548, 0.562],
    'RIGHT KNEE': [0.448, 0.648], 'LEFT KNEE': [0.556, 0.648],
    'RIGHT LEG': [0.442, 0.734], 'LEFT LEG': [0.560, 0.734],
  },
};
// Direção da lâmina (normalizada) e do cabo por pose; espada reta: cabo = lâmina.
const DIR = {
  ready: [-0.45, -0.85],
  elevation: [0.43, -0.91],
  strike: [-0.88, 0.47],
  follow: [-0.82, 0.52],
  recover: [-0.58, -0.81],
};
const r4 = (v) => Math.round(v * 10000) / 10000;
function normalize([x, y]) { const m = Math.hypot(x, y); return [r4(x / m), r4(y / m)]; }
function jointsOf(name) {
  return COCO.map((label) => ({
    label,
    x: r4(P[name][label][0]),
    y: r4(P[name][label][1]),
    z_index: Z[label],
    depth: DEPTH[label],
  }));
}
function gripOf(name) {
  const wrist = P[name]['RIGHT ARM'];
  const d = normalize(DIR[name]);
  return {
    hand: 'RIGHT ARM',
    point: { x: r4(wrist[0] - 0.006), y: r4(wrist[1] + 0.012) },
    haftDirection: { x: d[0], y: d[1] },
    bladeDirection: { x: d[0], y: d[1] },
  };
}

// ===== Interpolação dos 14 quadros na grade real do clip.json =====
const LERP = [
  { p: 'ready', t: 1 },                        // 0 rest
  { a: 'ready', b: 'elevation', t: 0.20 },     // 1 body-preparation
  { p: 'ready', t: 1 },                        // 2 establish-grip (pose 0 = postura da referência)
  { a: 'ready', b: 'elevation', t: 0.45 },     // 3 anticipation
  { p: 'elevation', t: 1 },                    // 4 coil-behind
  { p: 'elevation', t: 1 },                    // 5 apex-hold
  { a: 'elevation', b: 'strike', t: 0.35 },    // 6 apex-descent
  { a: 'elevation', b: 'strike', t: 0.70 },    // 7 slash-release
  { p: 'strike', t: 1 },                       // 8 contact
  { p: 'follow', t: 1 },                       // 9 follow-through
  { a: 'follow', b: 'recover', t: 0.30 },      // 10 recoil
  { a: 'follow', b: 'recover', t: 0.60 },      // 11 settle-grip
  null,                                        // 12 release-grip (herda o anterior — exercita carry-forward)
  { a: 'recover', b: 'ready', t: 0.50 },       // 13 return-to-guard
];
// Fases e durações REAIS do clip.json vigente (characters/orc-v1/.../rear-arc/back_l-sword/clip.json).
const PHASES = ['rest', 'body-preparation', 'establish-grip', 'anticipation', 'coil-behind', 'apex-hold', 'apex-descent', 'slash-release', 'contact', 'follow-through', 'recoil', 'settle-grip', 'release-grip', 'return-to-guard'];
const DUR = [30, 65, 35, 50, 45, 35, 30, 35, 35, 100, 55, 80, 45, 90];

function mixPose(w) {
  if (w === null) return null;
  if (w.p) return { joints: jointsOf(w.p), grip: gripOf(w.p) };
  const joints = COCO.map((label) => {
    const ax = P[w.a][label][0], ay = P[w.a][label][1];
    const bx = P[w.b][label][0], by = P[w.b][label][1];
    return { label, x: r4(ax + (bx - ax) * w.t), y: r4(ay + (by - ay) * w.t), z_index: Z[label], depth: DEPTH[label] };
  });
  const wa = wristGrip(w.a), wb = wristGrip(w.b);
  const point = { x: r4(wa.point.x + (wb.point.x - wa.point.x) * w.t), y: r4(wa.point.y + (wb.point.y - wa.point.y) * w.t) };
  const mx = wa.bladeDirection.x + (wb.bladeDirection.x - wa.bladeDirection.x) * w.t;
  const my = wa.bladeDirection.y + (wb.bladeDirection.y - wa.bladeDirection.y) * w.t;
  const d = normalize([mx, my]);
  return { joints, grip: { hand: 'RIGHT ARM', point, haftDirection: { x: d[0], y: d[1] }, bladeDirection: { x: d[0], y: d[1] } } };
}
function wristGrip(name) { return gripOf(name); }

const frames = LERP.map((w, i) => {
  const m = mixPose(w);
  return m
    ? { index: i, phase: PHASES[i], durationMs: DUR[i], joints: m.joints, grip: m.grip }
    : { index: i, phase: PHASES[i], durationMs: DUR[i] }; // sem joints/grip: o visualizador herda do anterior
});
const totalMs = DUR.reduce((a, b) => a + b, 0);

const now = new Date().toISOString();
const SYNTH_NOTE = 'FIXTURE SINTÉTICO para verificação do visualizador — NÃO é o movimento real do DEV de motion design. Fases e durações copiam a grade pública do clip.json vigente; esqueleto e empunhadura são esquemáticos.';
const POSES = {
  synthetic: true,
  note: SYNTH_NOTE,
  reference: {
    image: 'characters/orc-v1/source/combat-recovery-v8/rear-arc/back_l-sword/frames/02.png',
    width: 256,
    height: 256,
  },
  provenance: { generator: 'experiments/main-orc-skeleton-first-01/viewer/tools/make-fixture.mjs', generatedAtUtc: now, synthetic: true },
  poses: [
    { id: 'ready', label: 'Prontidão (estabelecer pegada)', phase: 'establish-grip', joints: jointsOf('ready'), grip: gripOf('ready') },
    { id: 'elevation', label: 'Elevação e antecipação', phase: 'coil-behind', joints: jointsOf('elevation'), grip: gripOf('elevation') },
    { id: 'strike', label: 'Golpe principal (contato)', phase: 'contact', joints: jointsOf('strike'), grip: gripOf('strike') },
    { id: 'follow', label: 'Seguimento', phase: 'follow-through', joints: jointsOf('follow'), grip: gripOf('follow') },
    { id: 'recover', label: 'Recuperação', phase: 'return-to-guard', joints: jointsOf('recover'), grip: gripOf('recover') },
  ],
};
const SEQUENCE = {
  synthetic: true,
  note: SYNTH_NOTE,
  fps: 19.2,
  totalMs,
  provenance: { generator: 'experiments/main-orc-skeleton-first-01/viewer/tools/make-fixture.mjs', generatedAtUtc: now, synthetic: true },
  frames,
};

function writeJSON(p, obj) { fs.writeFileSync(p, JSON.stringify(obj, null, 2) + '\n'); }
function writeMirror(p, globalName, obj) {
  fs.writeFileSync(p, '// Espelho gerado a partir do .json irmão (não editar à mão; gere com tools/make-fixture.mjs).\n'
    + '// Necessário porque file:// bloqueia fetch() de JSON no Chromium; <script> é permitido.\n'
    + 'window.' + globalName + ' = ' + JSON.stringify(obj, null, 2) + ';\n');
}
writeJSON(path.join(FIXTURES, 'sample-poses.json'), POSES);
writeJSON(path.join(FIXTURES, 'sample-sequence.json'), SEQUENCE);
writeMirror(path.join(FIXTURES, 'sample-poses.js'), '__SV_FIXTURE_POSES', POSES);
writeMirror(path.join(FIXTURES, 'sample-sequence.js'), '__SV_FIXTURE_SEQUENCE', SEQUENCE);

// Auditoria no console: ponta da lâmina por quadro e deslocamento (grade 0.30 de exibição).
console.log('fixtures gravados em ' + FIXTURES);
console.log('quadros: ' + frames.length + ' · totalMs: ' + totalMs);
let prev = null;
for (const f of frames) {
  const g = f.grip;
  if (!g) { console.log('F' + f.index, f.phase, '(herda o anterior)'); continue; }
  const tip = { x: g.point.x + g.bladeDirection.x * 0.30, y: g.point.y + g.bladeDirection.y * 0.30 };
  const d = prev ? (Math.hypot(tip.x - prev.x, tip.y - prev.y) * 256).toFixed(1) + ' px' : '—';
  console.log('F' + f.index, f.phase.padEnd(16), 'tip=(' + tip.x.toFixed(3) + ',' + tip.y.toFixed(3) + ')', 'Δ=' + d);
  prev = tip;
}

