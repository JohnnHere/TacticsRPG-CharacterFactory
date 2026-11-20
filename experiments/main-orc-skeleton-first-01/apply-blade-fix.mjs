import fs from 'node:fs';
import path from 'node:path';

// Applies the measured blade correction to a COPY of the motion design. The DEV's
// original files stay untouched as evidence. Every number here is traceable:
// BLADE = 59.01 px measured from the grip to the farthest blade pixel on the
// 96x96 weapon canvas, drawn near 1:1 in the 256 composite -> 59.01/256.

const EXPERIMENT = path.resolve(import.meta.dirname);
const BLADE = 0.2305;
const GROUND = 190 / 256;
const MIN_Y = 0.02, MAX_Y = GROUND, MIN_X = 0.02, MAX_X = 0.98;

// Blade direction per frame, kept continuous through the strike and brought back
// to the guard orientation by the last frame. Frames whose original direction was
// already safe keep it; the sequence tail had to be re-aimed to stop stabbing the floor.
const DIRECTIONS = {
  0: [0.34, -0.94], 1: [0.34, -0.94], 2: [0.31, -0.95], 3: [0.27, -0.96],
  4: [0.16, -0.99], 5: [0.00, -1.00], 6: [-0.36, -0.93], 7: [-0.90, -0.44],
  8: [-0.66, 0.75], 9: [-0.75, 0.66], 10: [-0.85, 0.53], 11: [-0.70, 0.20],
  12: [-0.20, -0.60], 13: [0.34, -0.94],
};

const read = file => JSON.parse(fs.readFileSync(path.join(EXPERIMENT, file), 'utf8'));
const sequence = read('sequence.json');
const poses = read('poses.json');

const tipOf = (frame, direction) => {
  const point = frame.grip?.point ?? { x: 0, y: 0 };
  const norm = Math.hypot(direction[0], direction[1]) || 1;
  return { x: point.x + (direction[0] / norm) * BLADE, y: point.y + (direction[1] / norm) * BLADE };
};

const rows = [];
for (const frame of sequence.frames) {
  const direction = DIRECTIONS[frame.index];
  if (!direction) throw new Error(`sem direção definida para o quadro ${frame.index}`);
  const tip = tipOf(frame, direction);
  const inside = tip.x >= MIN_X && tip.x <= MAX_X && tip.y >= MIN_Y && tip.y <= MAX_Y;
  rows.push({ index: frame.index, phase: frame.phase, before: frame.grip?.bladeDirection, after: { x: direction[0], y: direction[1] }, tip, inside });
  frame.grip = {
    ...frame.grip,
    bladeDirection: { x: direction[0], y: direction[1] },
    bladeLength: BLADE,
  };
}

const outside = rows.filter(r => !r.inside);
if (outside.length) {
  for (const r of outside) console.error(`FORA: F${r.index} ponta (${r.tip.x.toFixed(3)}, ${r.tip.y.toFixed(3)})`);
  throw new Error('trajetória saiu do canvas; correção rejeitada');
}

// The descent must stay monotonic from apex to contact.
const descent = rows.filter(r => r.index >= 5 && r.index <= 8).map(r => r.tip.y);
for (let i = 1; i < descent.length; i += 1) {
  if (descent[i] <= descent[i - 1]) throw new Error(`descida não monotônica em F${4 + i}: ${descent[i - 1].toFixed(3)} -> ${descent[i].toFixed(3)}`);
}

for (const pose of poses.poses) {
  const frame = sequence.frames.find(f => f.phase === pose.phaseHint) ?? sequence.frames.find(f => f.grip && Math.abs(f.grip.point.x - pose.grip.point.x) < 1e-9 && Math.abs(f.grip.point.y - pose.grip.point.y) < 1e-9);
  if (frame) {
    pose.grip = { ...frame.grip };
  }
}

fs.writeFileSync(path.join(EXPERIMENT, 'sequence-fixed.json'), `${JSON.stringify(sequence, null, 1)}\n`);
fs.writeFileSync(path.join(EXPERIMENT, 'poses-fixed.json'), `${JSON.stringify(poses, null, 1)}\n`);

const BLADE_TABLE = [
  '# Correção da lâmina — tabela verificada',
  '',
  '`BLADE = 0,2305` derivado de 59,01 px medidos do cabo à ponta no canvas 96×96 da arma,',
  'desenhada praticamente em escala 1:1 no composto de 256. Chão em `0,7422`.',
  '',
  '| Quadro | Fase | Direção antes | Direção depois | Ponta (x, y) | Dentro |',
  '|---|---|---|---|---|---|',
  ...rows.map(r => `| F${String(r.index).padStart(2, '0')} | ${r.phase} | (${r.before?.x}, ${r.before?.y}) | (${r.after.x}, ${r.after.y}) | (${r.tip.x.toFixed(3)}, ${r.tip.y.toFixed(3)}) | ${r.inside ? 'sim' : 'NÃO'} |`),
  '',
  `Descida monotônica de F05 a F08: ${descent.map(v => v.toFixed(3)).join(' → ')}`,
];
fs.writeFileSync(path.join(EXPERIMENT, 'blade-table.md'), `${BLADE_TABLE.join('\n')}\n`);

console.log(`BLADE ${BLADE} | ${rows.length} quadros | todos dentro do canvas`);
for (const r of rows) console.log(`  F${String(r.index).padStart(2, '0')} ${String(r.phase).padEnd(16)} ponta (${r.tip.x.toFixed(3)}, ${r.tip.y.toFixed(3)})`);
console.log(`descida F05..F08: ${descent.map(v => v.toFixed(3)).join(' -> ')}`);
