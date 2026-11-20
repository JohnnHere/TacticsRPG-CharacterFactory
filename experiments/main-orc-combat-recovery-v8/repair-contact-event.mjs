import fs from 'node:fs';
import path from 'node:path';
import { ROOT, hash } from '../../src/core.mjs';

// contactEvent is the frame the runtime will use for damage timing. It must point
// at the frame whose phase is contact/heavy-impact, not at a neighbour. The
// frontal clips declared frame 6 / 290 ms while their own `contact` phase is
// frame 7 / 325 ms, so the sword would apply damage one frame before it lands.
// Only clip metadata is rewritten; every frame PNG is re-hashed to prove identity.

const clips = [
  'combat-recovery-v7/frontal/full-front-r-sword',
  'combat-recovery-v7/frontal/front_l-Sword-full',
  'combat-recovery-v7/frontal/front_r-Axe-full',
  'combat-recovery-v7/frontal/front_l-Axe-full',
  'combat-recovery-v8/frontal-armpit/front_l-sword',
  'combat-recovery-v8/rear/back_r-sword',
  'combat-recovery-v8/rear/back_l-sword',
  'combat-recovery-v8/rear/back_r-axe',
  'combat-recovery-v8/rear/back_l-axe',
];

const absolute = file => path.resolve(ROOT, file);
const digest = file => hash(fs.readFileSync(absolute(file)));
const CONTACT_PHASES = new Set(['contact', 'heavy-impact']);

const results = [];
for (const dir of clips) {
  const clipPath = `characters/orc-v1/source/${dir}/clip.json`;
  const before = digest(clipPath);
  const clip = JSON.parse(fs.readFileSync(absolute(clipPath), 'utf8'));
  const frameHashes = clip.frames.map(f => f.sha256);

  let elapsed = 0;
  let contact = null;
  for (const frame of clip.frames) {
    if (CONTACT_PHASES.has(frame.phase)) contact = { frame: frame.index, timeMs: elapsed, phase: frame.phase };
    elapsed += frame.durationMs;
  }
  if (!contact) throw new Error(`no contact phase declared in ${clipPath}`);

  const previous = clip.contactEvent ? { ...clip.contactEvent } : null;
  clip.contactEvent = {
    ...clip.contactEvent,
    frame: contact.frame,
    timeMs: contact.timeMs,
    phase: contact.phase,
  };
  fs.writeFileSync(absolute(clipPath), `${JSON.stringify(clip, null, 2)}\n`);

  const after = digest(clipPath);
  const reloaded = JSON.parse(fs.readFileSync(absolute(clipPath), 'utf8'));
  const framesUnchanged = reloaded.frames.every((f, i) => f.sha256 === frameHashes[i]);
  const pngsUnchanged = reloaded.frames.every(f => digest(f.png) === f.sha256);
  if (!framesUnchanged || !pngsUnchanged) throw new Error(`pixel identity broken in ${clipPath}`);

  results.push({
    clip: dir,
    previous,
    corrected: clip.contactEvent,
    changed: previous?.frame !== contact.frame || previous?.timeMs !== contact.timeMs,
    clipShaBefore: before.slice(0, 12),
    clipShaAfter: after.slice(0, 12),
    pixelsIdentical: true,
  });
}

for (const r of results) {
  const flag = r.changed ? 'CORRIGIDO' : 'ja correto';
  console.log(`${r.clip.padEnd(44)} ${flag.padEnd(11)} ${JSON.stringify(r.previous)} -> frame ${r.corrected.frame}/${r.corrected.timeMs}ms ${r.corrected.phase}`);
}
console.log(`\nall clips: frame PNGs byte-identical after metadata repair`);
fs.writeFileSync(
  path.resolve(ROOT, 'experiments/main-orc-combat-recovery-v8/contact-event-repair.json'),
  `${JSON.stringify(results, null, 2)}\n`,
);
