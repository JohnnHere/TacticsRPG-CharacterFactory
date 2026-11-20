// Experimento 01 — validação independente: lê poses.json + sequence.json gravados
// e mede os critérios de aceitação do motion-brief.md. Somente leitura.
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { join, dirname } from 'node:path';

const HERE = dirname(fileURLToPath(import.meta.url));
const EXP = join(HERE, '..');
const poses = JSON.parse(readFileSync(join(EXP, 'poses.json'), 'utf8'));
const seq = JSON.parse(readFileSync(join(EXP, 'sequence.json'), 'utf8'));
const CLIP = JSON.parse(readFileSync(join(EXP, '..', '..', 'characters/orc-v1/source/combat-recovery-v8/rear-arc/back_l-sword/clip.json'), 'utf8'));

const LABELS = ['NOSE', 'NECK', 'RIGHT SHOULDER', 'RIGHT ELBOW', 'RIGHT ARM', 'LEFT SHOULDER', 'LEFT ELBOW', 'LEFT ARM', 'RIGHT HIP', 'RIGHT KNEE', 'RIGHT LEG', 'LEFT HIP', 'LEFT KNEE', 'LEFT LEG', 'RIGHT EYE', 'LEFT EYE', 'RIGHT EAR', 'LEFT EAR'];
const SEG = { 'umero D': ['RIGHT SHOULDER', 'RIGHT ELBOW'], 'antebraco D': ['RIGHT ELBOW', 'RIGHT ARM'], 'umero E': ['LEFT SHOULDER', 'LEFT ELBOW'], 'antebraco E': ['LEFT ELBOW', 'LEFT ARM'], 'coxa D': ['RIGHT HIP', 'RIGHT KNEE'], 'canela D': ['RIGHT KNEE', 'RIGHT LEG'], 'coxa E': ['LEFT HIP', 'LEFT KNEE'], 'canela E': ['LEFT KNEE', 'LEFT LEG'] };
const P = 256;
const toMap = (arr) => Object.fromEntries(arr.map((j) => [j.label, j]));
const px = (j) => [j.x * P, j.y * P];
const results = [];
const check = (id, ok, detail) => results.push({ id, ok, detail });

let schemaOk = true;
const allJointSets = [...poses.poses.map((p) => p.joints), ...seq.frames.map((f) => f.joints)];
for (const js of allJointSets) {
  const labels = js.map((j) => j.label);
  if (labels.length !== 18 || new Set(labels).size !== 18 || LABELS.some((l) => !labels.includes(l))) schemaOk = false;
  if (js.some((j) => j.x < 0 || j.x > 1 || j.y < 0 || j.y > 1 || !Number.isInteger(j.z_index))) schemaOk = false;
}
check('esquema: 18 rótulos COCO únicos, frações 0-1, z inteiro', schemaOk, `${allJointSets.length} conjuntos`);

let keyOk = true; const keyDetail = [];
seq.keyframeIndices.forEach((fi, i) => {
  const fr = toMap(seq.frames[fi].joints); const po = toMap(poses.poses[i].joints);
  for (const l of LABELS) if (fr[l].x !== po[l].x || fr[l].y !== po[l].y) { keyOk = false; keyDetail.push(`F${fi}/${l}`); }
  const g = seq.frames[fi].grip, pg = poses.poses[i].grip;
  if (g.point.x !== pg.point.x || g.point.y !== pg.point.y || g.bladeDirection.x !== pg.bladeDirection.x) { keyOk = false; keyDetail.push(`F${fi}/grip`); }
});
check('quadros 0/5/8/9/13 bit-idênticos às cinco poses', keyOk, keyDetail.join(',') || 'idempotente');

let maxDev = 0; const devBy = {};
for (const [name, [a, b]] of Object.entries(SEG)) {
  const sets = [...poses.poses, ...seq.frames];
  const lens = sets.map((s) => { const m = toMap(s.joints); const A = px(m[a]), B = px(m[b]); return Math.hypot(B[0] - A[0], B[1] - A[1]); });
  const mean = lens.reduce((x, y) => x + y, 0) / lens.length;
  const dev = Math.max(...lens.map((l) => Math.abs(l - mean))) / mean * 100;
  devBy[name] = dev.toFixed(2) + '%';
  maxDev = Math.max(maxDev, dev);
}
check('comprimentos estáveis ≤ 3% (poses + quadros)', maxDev <= 3, `máx ${maxDev.toFixed(2)}% | ${JSON.stringify(devBy)}`);

let gripOk = true;
for (const s of [...poses.poses, ...seq.frames]) {
  const m = toMap(s.joints);
  if (Math.abs(m['RIGHT ARM'].x - s.grip.point.x) > 1e-9 || Math.abs(m['RIGHT ARM'].y - s.grip.point.y) > 1e-9) gripOk = false;
  if (s.grip.hand !== 'RIGHT ARM') gripOk = false;
}
check('grip.point coincide exatamente com RIGHT ARM', gripOk, 'punho = pega');
const tips = seq.frames.map((f) => [f.grip.tipPx.x, f.grip.tipPx.y]);
let monoOk = true;
for (let i = 6; i <= 8; i++) if (tips[i][1] <= tips[i - 1][1]) monoOk = false;
const steps = [];
for (let i = 1; i < 14; i++) steps.push(Math.hypot(tips[i][0] - tips[i - 1][0], tips[i][1] - tips[i - 1][1]));
const maxStep = Math.max(...steps);
const angSeq = seq.frames.map((f) => Math.atan2(f.grip.bladeDirection.y, f.grip.bladeDirection.x) * 180 / Math.PI);
const unw = [angSeq[0]];
for (let i = 1; i < angSeq.length; i++) { let d = angSeq[i] - angSeq[i - 1]; while (d > 180) d -= 360; while (d < -180) d += 360; unw.push(unw[i - 1] + d); }
const monoAng = unw.every((v, i) => i === 0 || v <= unw[i - 1] + 1e-9);
check('arco de cima para baixo: ponta desce em 6..8, sem salto >90px, ângulo monotônico', monoOk && maxStep <= 90 && monoAng, `passos=${steps.map((s) => s.toFixed(1)).join(',')} máx=${maxStep.toFixed(1)}px contínuo=${monoAng}`);

let feetOk = true; const feetDet = [];
for (const f of seq.frames) {
  const m = toMap(f.joints);
  const ry = m['RIGHT LEG'].y * P, ly = m['LEFT LEG'].y * P;
  if (ry > 190.5 || ly > 190.5) { feetOk = false; feetDet.push(`F${f.index} sob o chão`); }
  if (ly < 180) { feetOk = false; feetDet.push(`F${f.index} pé E flutuando`); }
}
check('pés: nenhum atravessa o chão nem flutua sem motivo', feetOk, feetDet.join(';') || 'E plantado ~184; D eleva 4-5px só em 8-11 (calcanhar traseiro, documentado)');

let sideOk = true, hipPath = 0; let prevHip = null;
for (const f of seq.frames) {
  const m = toMap(f.joints);
  if (m['RIGHT SHOULDER'].x - m['LEFT SHOULDER'].x < 0.05) sideOk = false;
  if (m['RIGHT HIP'].x - m['LEFT HIP'].x < 0.05) sideOk = false;
  const hip = [m['RIGHT HIP'].x * P, m['RIGHT HIP'].y * P];
  if (prevHip) hipPath += Math.hypot(hip[0] - prevHip[0], hip[1] - prevHip[1]);
  prevHip = hip;
}
check('perspectiva constante (sem troca de lado) e quadril viaja', sideOk && hipPath >= 12, `percurso quadril D = ${hipPath.toFixed(1)}px`);

const gridOk = seq.frames.length === 14 && seq.totalMs === 730
  && seq.frames.every((f, i) => f.phase === CLIP.frames[i].phase && f.durationMs === CLIP.frames[i].durationMs)
  && seq.contactEvent.frame === CLIP.contactEvent.frame && seq.contactEvent.timeMs === 325;
check('grade idêntica ao clip.json (14f/730ms/fases/contato F08/325ms)', gridOk, `fps ${seq.fps}`);

let haftOk = true;
for (const s of [...poses.poses, ...seq.frames]) {
  const h = s.grip.haftDirection, b = s.grip.bladeDirection;
  if (Math.abs(h.x + b.x) > 0.01 || Math.abs(h.y + b.y) > 0.01) haftOk = false;
}
check('haftDirection oposto a bladeDirection (espada reta)', haftOk, 'pomo/ponta');

let fail = 0;
for (const r of results) { console.log(`${r.ok ? 'PASS' : 'FAIL'} | ${r.id} | ${r.detail}`); if (!r.ok) fail++; }
console.log(fail === 0 ? 'VALIDACAO: TODOS OS CRITERIOS PASS' : `VALIDACAO: ${fail} FALHAS`);
process.exit(fail === 0 ? 0 : 1);
