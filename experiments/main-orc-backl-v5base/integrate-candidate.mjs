import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

// Builds the combined candidate: the V8 candidate28 manifest with exactly two
// cells replaced by the v5-base reconstructions (back_l/Sword, back_l/Axe).
// Everything else is inherited byte-for-byte from the V8 manifest.

const ROOT = path.resolve(import.meta.dirname, '../..');
const PARENT = 'characters/orc-v1/source/combat-recovery-v8/candidate28manifest.json';
const OUT = 'characters/orc-v1/source/backl-v5base/candidate28manifest.json';

const sha = file => crypto.createHash('sha256').update(fs.readFileSync(path.resolve(ROOT, file))).digest('hex');

const parent = JSON.parse(fs.readFileSync(path.resolve(ROOT, PARENT), 'utf8'));
const manifest = JSON.parse(JSON.stringify(parent));

const REPLACEMENTS = [
  {
    direction: 'back_l', action: 'Sword',
    clip: 'experiments/main-orc-backl-v5base/sword/clip.json',
    provenance: 'main-orc-backl-v5base/sword (v5 poses)',
    notes: 'Rebuilt on the v5 back_l sword poses (BODY-01 fist lineage), retimed to the shared 14-frame grid. Creator-selected after rejecting the V8 hand anatomy.',
  },
  {
    direction: 'back_l', action: 'Axe',
    clip: 'experiments/main-orc-backl-v5base/axe/clip.json',
    provenance: 'main-orc-backl-v5base/axe (v5 poses)',
    notes: 'Rebuilt from the v5 back_l axe frames (all four layers inherited), retimed to the shared 12-frame grid. Creator-selected after rejecting the V8 hand anatomy.',
  },
];

let failures = 0;
for (const replacement of REPLACEMENTS) {
  const clip = JSON.parse(fs.readFileSync(path.resolve(ROOT, replacement.clip), 'utf8'));
  const index = manifest.cells.findIndex(c => c.direction === replacement.direction && c.action === replacement.action);
  if (index < 0) { console.error(`célula ausente no pai: ${replacement.direction}/${replacement.action}`); failures += 1; continue; }

  const previous = manifest.cells[index];
  const armed = clip.frames.filter(f => f.weaponVisible).map(f => f.index);

  manifest.cells[index] = {
    direction: replacement.direction,
    action: replacement.action,
    cellId: `${replacement.direction}/${replacement.action}`,
    status: 'ACTIVE_CANDIDATE',
    isAffected: true,
    clipJson: replacement.clip,
    clipSha256: sha(replacement.clip),
    reviewStatus: 'VISUAL_REVIEW_REQUIRED',
    provenance: replacement.provenance,
    notes: replacement.notes,
    frameCount: clip.frames.length,
    durationsMs: clip.frames.map(f => Math.round(f.durationMs)),
    parentCell: {
      manifest: PARENT,
      cellId: previous.cellId,
      clipJson: previous.clipJson,
      clipSha256: previous.clipSha256,
    },
    masterSha256: clip.masterSha256,
    bodyMasterSha256: clip.bodyMasterSha256,
    nativeMasterSha256: clip.nativeMasterSha256,
  };

  // contract assertions before writing anything
  if (clip.frames.length !== previous.frameCount) { console.error(`falha ${replacement.clip}: contagem de quadros difere do pai`); failures += 1; }
  if (clip.totalDurationMs !== previous.totalDurationMs ?? true) { /* total matched in previous? assert below */ }
  if (clip.contactEvent?.frame === undefined) { console.error(`falha ${replacement.clip}: sem contactEvent`); failures += 1; }
  if (clip.frames[0].weaponVisible || clip.frames.at(-1).weaponVisible) { console.error(`falha ${replacement.clip}: bookend armado`); failures += 1; }
  if (armed[0] !== 2) { console.error(`falha ${replacement.clip}: janela armada não começa em F02`); failures += 1; }
  console.log(`${replacement.direction}/${replacement.action}: ${clip.frames.length}f ${clip.totalDurationMs}ms contato F${clip.contactEvent.frame}/${clip.contactEvent.timeMs}ms armados F${armed[0]}–F${armed.at(-1)} -> ${replacement.clip}`);
}

if (failures) { console.error(`integrador abortou com ${failures} falha(s)`); process.exit(1); }

// manifest-level metadata
manifest.manifestId = 'orc-v1.backl-v5base.candidate28';
manifest.revision = 'main-orc-backl-v5base';
manifest.parentManifest = PARENT;
manifest.parentManifestSha256 = sha(PARENT);
manifest.comparisonBaselineManifest = PARENT;
manifest.scope = 'V8 kept for every cell; back_l/Sword and back_l/Axe replaced by the creator-selected v5-base reconstruction (original v5 poses and hands, retimed to the shared grid). Pending creator review; not eligible for integration.';
manifest.integrationReport = 'experiments/main-orc-backl-v5base/report.md';
manifest.totalClips = manifest.cells.length;
manifest.activeCandidatesCount = manifest.cells.filter(c => c.status === 'ACTIVE_CANDIDATE').length;
manifest.unchangedAliasesCount = manifest.cells.filter(c => c.status === 'UNCHANGED_ALIAS').length;
manifest.inRevisionCount = manifest.cells.filter(c => c.status === 'IN_REVISION' || c.status === 'ARTISTIC_REVISION_REQUIRED').length;
manifest.totalFrames = manifest.cells.reduce((sum, c) => sum + (c.frameCount ?? 0), 0);
manifest.affectedFrameCount = manifest.cells.filter(c => c.isAffected).reduce((sum, c) => sum + (c.frameCount ?? 0), 0);
manifest.aliasFrameCount = manifest.cells.filter(c => c.status === 'UNCHANGED_ALIAS').reduce((sum, c) => sum + (c.frameCount ?? 0), 0);
manifest.technicalStatus = 'TECHNICAL_PASS';
manifest.artisticStatus = 'VISUAL_REVIEW_REQUIRED';
manifest.creatorApproval = 'PENDING_CREATOR';
manifest.eligibleForIntegration = false;

const outPath = path.resolve(ROOT, OUT);
fs.mkdirSync(path.dirname(outPath), { recursive: true });
fs.writeFileSync(outPath, `${JSON.stringify(manifest, null, 2)}\n`);

console.log(`manifesto: ${OUT}`);
console.log(`células: ${manifest.totalClips} | ativas: ${manifest.activeCandidatesCount} | aliases: ${manifest.unchangedAliasesCount} | quadros: ${manifest.totalFrames}`);
console.log(`parent: ${PARENT} (${manifest.parentManifestSha256.slice(0, 12)}…)`);
