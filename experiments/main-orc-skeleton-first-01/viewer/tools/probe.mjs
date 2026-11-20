// Sonda de ambiente do visualizador: dimensões do PNG de referência e grade de timing real.
import fs from 'fs';

function pngSize(p) {
  const b = fs.readFileSync(p);
  return `${b.readUInt32BE(16)}x${b.readUInt32BE(20)}`;
}
const candidates = [
  'characters/orc-v1/source/combat-recovery-v8/rear-arc/back_l-sword/02.png',
  'characters/orc-v1/source/combat-recovery-v8/rear-arc/back_l-sword/frames/02.png',
  'characters/orc-v1/source/combat-recovery-v8/rear-arc/back_l-sword/native/02.png',
  'characters/orc-v1/source/complete-v1/back_l/Idle/00.png',
];
for (const p of candidates) {
  try { console.log('PNG', p, '=>', pngSize(p)); }
  catch { console.log('PNG', p, '=> MISSING'); }
}
try {
  const c = JSON.parse(fs.readFileSync('characters/orc-v1/source/combat-recovery-v8/rear-arc/back_l-sword/clip.json', 'utf8'));
  const fr = c.frames || [];
  console.log('clip frames:', fr.length);
  for (const f of fr) {
    const keys = Object.keys(f);
    const dur = f.durationMs ?? f.duration_ms ?? f.duration ?? '?';
    console.log(' frame', f.index, f.sourcePhase ?? f.phase, 'dur=' + dur, 'weaponVisible=' + f.weaponVisible);
    if (f.index === 0) console.log(' frame keys:', keys.join(','));
  }
  console.log('contactEvent:', JSON.stringify(c.contactEvent));
  console.log('totalMs:', c.totalMs, 'fps:', c.fps);
} catch (e) {
  console.log('clip read failed:', e.message);
}
