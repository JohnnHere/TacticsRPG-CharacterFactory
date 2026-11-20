// Experimento 01 — constrói poses.json e sequence.json (espaço 256x256, frações /256)
// Interpolação ANGULAR por segmento (FK com comprimento canônico), raízes interpoladas
// linearmente, keyframes 0/5/8/9/13 idênticos às poses. Sem arte, sem PixelLab.
import { writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { join, dirname } from 'node:path';

const HERE = dirname(fileURLToPath(import.meta.url));
const EXP = join(HERE, '..');
const R4 = (v) => Math.round(v * 10000) / 10000;

// ---------- Poses em px 256 (medidas de 02.png + silhueta + redesenho do golpe) ----------
const PX = {
  ready: {
    'NOSE': [118, 84], 'NECK': [124, 100],
    'RIGHT SHOULDER': [150, 102], 'RIGHT ELBOW': [173, 101], 'RIGHT ARM': [174, 122],
    'LEFT SHOULDER': [106, 105], 'LEFT ELBOW': [95, 123], 'LEFT ARM': [93, 144],
    'RIGHT HIP': [146, 150], 'RIGHT KNEE': [148, 166], 'RIGHT LEG': [147, 184],
    'LEFT HIP': [112, 150], 'LEFT KNEE': [108, 166], 'LEFT LEG': [110, 184],
    'RIGHT EYE': [122, 86], 'LEFT EYE': [114, 82], 'RIGHT EAR': [136, 88], 'LEFT EAR': [113, 90],
  },
  raise: {
    'NOSE': [117, 82], 'NECK': [123, 99],
    'RIGHT SHOULDER': [153, 103], 'RIGHT ELBOW': [164, 83], 'RIGHT ARM': [146, 72],
    'LEFT SHOULDER': [104, 105], 'LEFT ELBOW': [97, 126], 'LEFT ARM': [96, 147],
    'RIGHT HIP': [148, 150], 'RIGHT KNEE': [150, 166], 'RIGHT LEG': [147, 184],
    'LEFT HIP': [116, 151], 'LEFT KNEE': [109, 166], 'LEFT LEG': [110, 184],
    'RIGHT EYE': [121, 84], 'LEFT EYE': [113, 80], 'RIGHT EAR': [135, 86], 'LEFT EAR': [112, 88],
  },
  strike: {
    'NOSE': [115, 86], 'NECK': [122, 101],
    'RIGHT SHOULDER': [141, 101], 'RIGHT ELBOW': [160, 113], 'RIGHT ARM': [148, 130],
    'LEFT SHOULDER': [110, 108], 'LEFT ELBOW': [99, 127], 'LEFT ARM': [97, 148],
    'RIGHT HIP': [141, 151], 'RIGHT KNEE': [152, 162], 'RIGHT LEG': [150, 180],
    'LEFT HIP': [117, 152], 'LEFT KNEE': [107, 166], 'LEFT LEG': [108, 184],
    'RIGHT EYE': [119, 88], 'LEFT EYE': [111, 84], 'RIGHT EAR': [134, 90], 'LEFT EAR': [111, 92],
  },
  follow: {
    'NOSE': [114, 88], 'NECK': [121, 102],
    'RIGHT SHOULDER': [139, 102], 'RIGHT ELBOW': [156, 118], 'RIGHT ARM': [148, 138],
    'LEFT SHOULDER': [111, 108], 'LEFT ELBOW': [100, 127], 'LEFT ARM': [98, 148],
    'RIGHT HIP': [140, 152], 'RIGHT KNEE': [153, 161], 'RIGHT LEG': [151, 179],
    'LEFT HIP': [118, 152], 'LEFT KNEE': [108, 166], 'LEFT LEG': [107, 184],
    'RIGHT EYE': [118, 90], 'LEFT EYE': [110, 86], 'RIGHT EAR': [133, 92], 'LEFT EAR': [110, 94],
  },
  recover: {
    'NOSE': [118, 84], 'NECK': [124, 100],
    'RIGHT SHOULDER': [150, 104], 'RIGHT ELBOW': [166, 121], 'RIGHT ARM': [160, 141],
    'LEFT SHOULDER': [106, 105], 'LEFT ELBOW': [95, 123], 'LEFT ARM': [93, 144],
    'RIGHT HIP': [146, 150], 'RIGHT KNEE': [148, 166], 'RIGHT LEG': [147, 184],
    'LEFT HIP': [112, 150], 'LEFT KNEE': [108, 166], 'LEFT LEG': [110, 184],
    'RIGHT EYE': [122, 86], 'LEFT EYE': [114, 82], 'RIGHT EAR': [136, 88], 'LEFT EAR': [113, 90],
  },
};

// Lâmina: direção (unitária, do punho para a ponta) e comprimento projetado (px 256).
const BLADE = {
  ready: { dir: [0.336, -0.941], len: 60 },
  raise: { dir: [0, -1], len: 60 },
  strike: { dir: [-0.6604, 0.7510], len: 52.5 },
  follow: { dir: [-0.3015, 0.9535], len: 47 },
  recover: { dir: [0.3393, 0.9407], len: 48 },
};

const POSE_META = [
  { id: 'ready', label: 'Prontidão', frameIndex: 0, phase: 'rest', note: 'Postura medida de 02.png (establish-grip armado; referência do PixelLab).' },
  { id: 'raise', label: 'Elevação / antecipação', frameIndex: 5, phase: 'apex-hold', note: 'Ápice: punho acima da cabeça, lâmina vertical (técnica frontal).' },
  { id: 'strike', label: 'Golpe principal', frameIndex: 8, phase: 'contact', note: 'Contato 325 ms: descida diagonal para a linha do oponente (baixo-esquerda).' },
  { id: 'follow', label: 'Seguimento', frameIndex: 9, phase: 'follow-through', note: 'Corte passa do contato; peso no pé esquerdo, calcanhar direito elevado.' },
  { id: 'recover', label: 'Recuperação', frameIndex: 13, phase: 'return-to-guard', note: 'Retorno à guarda medida (quadro 13 do clipe vigente).' },
];
const POSE_IDS = POSE_META.map((p) => p.id);
const KEYFRAMES = [0, 5, 8, 9, 13];
const DUR = [30, 65, 35, 50, 45, 35, 30, 35, 35, 100, 55, 80, 45, 90];
const STARTS = (() => { let a = 0; return DUR.map((d) => { const s = a; a += d; return s; }); })();
const PHASES = ['rest', 'body-preparation', 'establish-grip', 'anticipation', 'coil-behind', 'apex-hold', 'apex-descent', 'slash-release', 'contact', 'follow-through', 'recoil', 'settle-grip', 'release-grip', 'return-to-guard'];

// Ordem de desenho (z_index) e profundidade (0-255; ~128 centro, maior = mais perto).
// Vista back_l: flanco ESQUERDO próximo (esquerda da imagem), flanco DIREITO afastado.
const ZI = {
  'RIGHT LEG': 9, 'RIGHT KNEE': 9, 'RIGHT HIP': 11,
  'RIGHT SHOULDER': 13, 'RIGHT ELBOW': 14, 'RIGHT ARM': 15,
  'NECK': 20, 'NOSE': 20, 'RIGHT EYE': 19, 'LEFT EYE': 19, 'RIGHT EAR': 18, 'LEFT EAR': 22,
  'LEFT HIP': 22,
  'LEFT KNEE': 30, 'LEFT LEG': 31,
  'LEFT SHOULDER': 34, 'LEFT ELBOW': 35, 'LEFT ARM': 36,
};
const DEP = {
  'RIGHT LEG': 86, 'RIGHT KNEE': 82, 'RIGHT HIP': 108,
  'RIGHT SHOULDER': 88, 'RIGHT ELBOW': 82, 'RIGHT ARM': 92,
  'NECK': 128, 'NOSE': 78, 'RIGHT EYE': 76, 'LEFT EYE': 80, 'RIGHT EAR': 84, 'LEFT EAR': 172,
  'LEFT HIP': 146,
  'LEFT KNEE': 172, 'LEFT LEG': 176,
  'LEFT SHOULDER': 168, 'LEFT ELBOW': 178, 'LEFT ARM': 184,
};
// ---------- Cadeias e comprimentos canônicos ----------
const CHAINS = [
  { name: 'rightArm', joints: ['RIGHT SHOULDER', 'RIGHT ELBOW', 'RIGHT ARM'], sword: true },
  { name: 'leftArm', joints: ['LEFT SHOULDER', 'LEFT ELBOW', 'LEFT ARM'] },
  { name: 'rightLeg', joints: ['RIGHT HIP', 'RIGHT KNEE', 'RIGHT LEG'] },
  { name: 'leftLeg', joints: ['LEFT HIP', 'LEFT KNEE', 'LEFT LEG'] },
];
const segLen = (pose, a, b) => Math.hypot(PX[pose][b][0] - PX[pose][a][0], PX[pose][b][1] - PX[pose][a][1]);
const CANON = {}; // nome -> comprimento canônico (média das poses)
const POSE_SEGLEN = {}; // pose -> nome -> comprimento medido
for (const ch of CHAINS) {
  for (let s = 0; s < 2; s++) {
    const key = `${ch.name}.${s}`;
    const lens = POSE_IDS.map((p) => segLen(p, ch.joints[s], ch.joints[s + 1]));
    CANON[key] = lens.reduce((x, y) => x + y, 0) / lens.length;
    lens.forEach((l, i) => { (POSE_SEGLEN[POSE_IDS[i]] ??= {})[key] = l; });
  }
}
// Ângulos por segmento, com desembrulho contínuo ao longo das 5 poses.
const segAng = (pose, a, b) => Math.atan2(PX[pose][b][1] - PX[pose][a][1], PX[pose][b][0] - PX[pose][a][0]);
const ANGS = {}; // key -> [θ0..θ4] contínuo
for (const ch of CHAINS) {
  for (let s = 0; s < 2; s++) {
    const key = `${ch.name}.${s}`;
    const raw = POSE_IDS.map((p) => segAng(p, ch.joints[s], ch.joints[s + 1]));
    const out = [raw[0]];
    for (let i = 1; i < raw.length; i++) {
      let d = raw[i] - raw[i - 1];
      while (d > Math.PI) d -= 2 * Math.PI;
      while (d < -Math.PI) d += 2 * Math.PI;
      out.push(out[i - 1] + d);
    }
    ANGS[key] = out;
  }
}
// Lâmina: ângulo contínuo + comprimento por pose.
const bladeAng = POSE_IDS.map((p) => Math.atan2(BLADE[p].dir[1], BLADE[p].dir[0]));
const bladeAngU = [bladeAng[0]];
for (let i = 1; i < bladeAng.length; i++) {
  let d = bladeAng[i] - bladeAng[i - 1];
  while (d > Math.PI) d -= 2 * Math.PI;
  while (d < -Math.PI) d += 2 * Math.PI;
  bladeAngU.push(bladeAngU[i - 1] + d);
}
const bladeLen = POSE_IDS.map((p) => BLADE[p].len);

// ---------- Curvas de easing por transição e grupo ----------
// corpo: move cedo (body-preparation); braçoDaEspada+lâmina: mora no início e acelera.
const smooth = (t) => t * t * (3 - 2 * t);
const easeFor = (segIdx, sword) => {
  if (segIdx === 0) return sword ? (t) => Math.pow(t, 2.8) : (t) => Math.pow(t, 1.4);
  if (segIdx === 1) return sword ? (t) => Math.pow(t, 1.5) : (t) => Math.pow(t, 1.6);
  if (segIdx === 2) return (t) => t;
  return smooth;
};
// ---------- Geração dos 14 quadros ----------
const lerp = (a, b, t) => a + (b - a) * t;
const ROOTS = ['NECK', 'RIGHT SHOULDER', 'LEFT SHOULDER', 'RIGHT HIP', 'LEFT HIP',
  'NOSE', 'RIGHT EYE', 'LEFT EYE', 'RIGHT EAR', 'LEFT EAR']; // interpolados linearmente (não membros)

function buildFrame(fi) {
  const kIdx = KEYFRAMES.indexOf(fi);
  if (kIdx >= 0) return { pose: POSE_IDS[kIdx], joints: structuredClone(PX[POSE_IDS[kIdx]]), blade: { ...BLADE[POSE_IDS[kIdx]] } };
  const time = STARTS[fi];
  let seg = 0;
  while (!(time >= STARTS[KEYFRAMES[seg]] && time <= STARTS[KEYFRAMES[seg + 1]])) seg++;
  const ta = STARTS[KEYFRAMES[seg]], tb = STARTS[KEYFRAMES[seg + 1]];
  const rawT = (time - ta) / (tb - ta);
  const pa = POSE_IDS[seg], pb = POSE_IDS[seg + 1];
  const joints = {};
  for (const j of ROOTS) {
    joints[j] = [lerp(PX[pa][j][0], PX[pb][j][0], rawT), lerp(PX[pa][j][1], PX[pb][j][1], rawT)];
  }
  for (const ch of CHAINS) {
    const easeA = easeFor(seg, false)(rawT);
    const easeS = easeFor(seg, ch.sword === true)(rawT);
    let px = joints[ch.joints[0]][0], py = joints[ch.joints[0]][1];
    for (let s = 0; s < 2; s++) {
      const key = `${ch.name}.${s}`;
      const th = lerp(ANGS[key][seg], ANGS[key][seg + 1], ch.sword ? easeS : easeA);
      const L = CANON[key];
      px += L * Math.cos(th); py += L * Math.sin(th);
      joints[ch.joints[s + 1]] = [px, py];
    }
  }
  const easeBlade = easeFor(seg, true)(rawT);
  const th = lerp(bladeAngU[seg], bladeAngU[seg + 1], easeBlade);
  const L = lerp(bladeLen[seg], bladeLen[seg + 1], rawT);
  return { pose: null, joints, blade: { dir: [Math.cos(th), Math.sin(th)], len: L } };
}

const tipOf = (joints, blade) => [
  joints['RIGHT ARM'][0] + blade.len * blade.dir[0],
  joints['RIGHT ARM'][1] + blade.len * blade.dir[1],
];

// ---------- Serialização (frações /256, 4 decimais) ----------
const frac = (v) => R4(v / 256);
const jointArray = (joints) => Object.keys(ZI).map((label) => ({
  label, x: frac(joints[label][0]), y: frac(joints[label][1]), z_index: ZI[label], depth: DEP[label],
}));
const gripOf = (joints, blade) => ({
  hand: 'RIGHT ARM',
  point: { x: frac(joints['RIGHT ARM'][0]), y: frac(joints['RIGHT ARM'][1]) },
  haftDirection: { x: R4(-blade.dir[0]), y: R4(-blade.dir[1]) },
  bladeDirection: { x: R4(blade.dir[0]), y: R4(blade.dir[1]) },
  bladeLengthPx: R4(blade.len),
  tipPx: { x: R4(tipOf(joints, blade)[0]), y: R4(tipOf(joints, blade)[1]) },
});

const framesPx = [];
for (let i = 0; i < 14; i++) framesPx.push(buildFrame(i));
const posesJson = {
  schema: 'main-orc-skeleton-first-01/poses',
  character: 'orc-v1', direction: 'back_l', action: 'Sword Attack (basic.sword-slash)',
  reference: {
    image: 'characters/orc-v1/source/combat-recovery-v8/rear-arc/back_l-sword/02.png',
    width: 256, height: 256, groundY: 190, groundYFraction: 0.7422, bodyOffset: [64, 64],
    note: 'Frações x/y relativas a esta imagem 256x256, y para baixo. Pose ready reproduz a postura dela.',
  },
  convention: {
    sides: 'LEFT/RIGHT são lados do personagem. Em back_l o flanco ESQUERDO é o próximo da câmera (esquerda da imagem, depth alto); o DIREITO é o afastado (direita da imagem, depth baixo). Não espelhe.',
    arm: 'RIGHT ARM é o punho fechado sobre o cabo; coincide exatamente com grip.point. LEFT ARM é a mão livre (guarda junto ao quadril esquerdo).',
    blade: 'bladeDirection aponta do punho para a ponta; haftDirection aponta do punho para o pomo (espada reta: eixos opostos). bladeLengthPx é o comprimento projetado na tela (encurtar = apontar para dentro da profundidade).',
    weapon: 'Espada do Recruta, uma mão, binding hand right; canvas próprio 96x96 com grip [48,66]; no palco 256 o cabo está sempre no RIGHT ARM.',
  },
  poses: POSE_META.map((m) => ({
    id: m.id, label: m.label, frameIndex: m.frameIndex, phase: m.phase, note: m.note,
    joints: jointArray(PX[m.id]), grip: gripOf(PX[m.id], BLADE[m.id]),
  })),
};

const seqFrames = framesPx.map((f, i) => ({
  index: i, phase: PHASES[i], durationMs: DUR[i], startMs: STARTS[i], endMs: STARTS[i] + DUR[i],
  keyframePose: f.pose ?? undefined,
  joints: jointArray(f.joints), grip: gripOf(f.joints, f.blade),
}));

const sequenceJson = {
  schema: 'main-orc-skeleton-first-01/sequence',
  character: 'orc-v1', direction: 'back_l', action: 'Sword Attack (basic.sword-slash)',
  fps: 19.2, totalMs: 730, frameCount: 14,
  durationsMs: DUR, phases: PHASES,
  canvas: { width: 256, height: 256 }, groundY: 190, groundYFraction: 0.7422,
  contactEvent: { frame: 8, timeMs: 325, phase: 'contact' },
  keyframeIndices: KEYFRAMES,
  interpolation: 'Angular por articulação (ângulo do segmento com comprimento canônico fixo via FK); raízes (pescoço, ombros, quadris, cabeça) interpoladas linearmente; lâmina por ângulo contínuo e comprimento projetado. Quadros 0/5/8/9/13 são bit-idênticos às poses.',
  frames: seqFrames,
};

writeFileSync(join(EXP, 'poses.json'), JSON.stringify(posesJson, null, 1));
writeFileSync(join(EXP, 'sequence.json'), JSON.stringify(sequenceJson, null, 1));
console.log('OK — poses.json e sequence.json gravados.');
console.log('CANON', JSON.stringify(Object.fromEntries(Object.entries(CANON).map(([k, v]) => [k, +v.toFixed(2)]))));
// ---------- Tabelas para o relatório ----------
const deg = (r) => (r * 180) / Math.PI;
const lines = [];
lines.push('### Comprimentos por pose (px 256) e desvio máximo vs canônico');
lines.push('| Segmento | ' + POSE_IDS.join(' | ') + ' | canônico | desv.máx |');
lines.push('|---|' + POSE_IDS.map(() => '---').join('|') + '|---|---|');
for (const key of Object.keys(CANON)) {
  const lens = POSE_IDS.map((p) => POSE_SEGLEN[p][key]);
  const dev = Math.max(...lens.map((l) => Math.abs(l - CANON[key]) / CANON[key])) * 100;
  lines.push(`| ${key} | ${lens.map((l) => l.toFixed(1)).join(' | ')} | ${CANON[key].toFixed(1)} | ${dev.toFixed(1)}% |`);
}
lines.push('');
lines.push('### Ângulos por pose');
lines.push('| Pose | Ombro D (°) | Cotovelo D (°) | Antebraço D vs lâmina (°) | Ombro E (°) | Cotovelo E (°) | Linha ombros vs quadris (°) | Lâmina vs solo (°) | COM px |');
lines.push('|---|---|---|---|---|---|---|---|---|');
const comOf = (j) => {
  const mid = [(j.NECK[0] + (j['RIGHT HIP'][0] + j['LEFT HIP'][0]) / 2) / 2, (j.NECK[1] + (j['RIGHT HIP'][1] + j['LEFT HIP'][1]) / 2) / 2];
  const parts = [[mid, 0.40], [j.NOSE, 0.15], [j['RIGHT ELBOW'], 0.05], [j['LEFT ELBOW'], 0.05], [j['RIGHT ARM'], 0.02], [j['LEFT ARM'], 0.02], [j['RIGHT KNEE'], 0.09], [j['LEFT KNEE'], 0.09], [j['RIGHT LEG'], 0.06], [j['LEFT LEG'], 0.07]];
  let x = 0, y = 0, w = 0;
  for (const [pt, ww] of parts) { x += pt[0] * ww; y += pt[1] * ww; w += ww; }
  return [x / w, y / w];
};
for (const p of POSE_IDS) {
  const j = PX[p];
  const ang = (a, b, c) => {
    const v1 = [j[a][0] - j[b][0], j[a][1] - j[b][1]], v2 = [j[c][0] - j[b][0], j[c][1] - j[b][1]];
    return deg(Math.acos((v1[0] * v2[0] + v1[1] * v2[1]) / (Math.hypot(v1[0], v1[1]) * Math.hypot(v2[0], v2[1]))));
  };
  const shoulder = (s, e) => deg(Math.atan2(j[e][0] - j[s][0], -(j[e][1] - j[s][1])));
  const shLine = Math.atan2(j['RIGHT SHOULDER'][1] - j['LEFT SHOULDER'][1], j['RIGHT SHOULDER'][0] - j['LEFT SHOULDER'][0]);
  const hpLine = Math.atan2(j['RIGHT HIP'][1] - j['LEFT HIP'][1], j['RIGHT HIP'][0] - j['LEFT HIP'][0]);
  const forearm = Math.atan2(j['RIGHT ARM'][1] - j['RIGHT ELBOW'][1], j['RIGHT ARM'][0] - j['RIGHT ELBOW'][0]);
  const bl = Math.atan2(BLADE[p].dir[1], BLADE[p].dir[0]);
  let wristRel = deg(forearm - bl); while (wristRel > 180) wristRel -= 360; while (wristRel < -180) wristRel += 360;
  const com = comOf(j);
  lines.push(`| ${p} | ${shoulder('RIGHT SHOULDER', 'RIGHT ELBOW').toFixed(0)} | ${ang('RIGHT SHOULDER', 'RIGHT ELBOW', 'RIGHT ARM').toFixed(0)} | ${wristRel.toFixed(0)} | ${shoulder('LEFT SHOULDER', 'LEFT ELBOW').toFixed(0)} | ${ang('LEFT SHOULDER', 'LEFT ELBOW', 'LEFT ARM').toFixed(0)} | ${deg(shLine - hpLine).toFixed(1)} | ${deg(bl).toFixed(0)} | ${com[0].toFixed(0)},${com[1].toFixed(0)} |`);
}
lines.push('');
lines.push('### Trajetória da ponta (px 256) — 14 quadros');
lines.push('| F | fase | ponta | passo (px) | punho D |');
lines.push('|---|---|---|---|---|');
let prev = null;
for (let i = 0; i < 14; i++) {
  const f = framesPx[i]; const tip = tipOf(f.joints, f.blade);
  const step = prev ? Math.hypot(tip[0] - prev[0], tip[1] - prev[1]) : 0;
  lines.push(`| ${i} | ${PHASES[i]} | ${tip[0].toFixed(0)},${tip[1].toFixed(0)} | ${step.toFixed(1)} | ${f.joints['RIGHT ARM'][0].toFixed(0)},${f.joints['RIGHT ARM'][1].toFixed(0)} |`);
  prev = tip;
}
lines.push('');
lines.push('### Quadril e tornozelos por quadro (px)');
lines.push('| F | quadril D | quadril E | tornozelo D | tornozelo E |');
lines.push('|---|---|---|---|---|');
for (let i = 0; i < 14; i++) {
  const j = framesPx[i].joints;
  lines.push(`| ${i} | ${j['RIGHT HIP'][0].toFixed(0)},${j['RIGHT HIP'][1].toFixed(0)} | ${j['LEFT HIP'][0].toFixed(0)},${j['LEFT HIP'][1].toFixed(0)} | ${j['RIGHT LEG'][0].toFixed(0)},${j['RIGHT LEG'][1].toFixed(0)} | ${j['LEFT LEG'][0].toFixed(0)},${j['LEFT LEG'][1].toFixed(0)} |`);
}
writeFileSync(join(HERE, 'tables.md'), lines.join('\n'));
console.log('dev/tables.md gravado.');
