#!/usr/bin/env node
// Builds candidate clip.json files from their published parents: re-points art paths,
// recomputes hashes, records the repair provenance and the honest status.
// Never writes to the freeze.
import fs from 'node:fs';
import crypto from 'node:crypto';

const ROOT = process.cwd();
const CAND = 'experiments/main-orc-targeted-repair-v1/artist-rear/candidate';
const sha = (p) => crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');

const pawn = JSON.parse(fs.readFileSync('experiments/main-orc-targeted-repair-v1/artist-rear/dryrun/back_r-sword/cand-summary.json', 'utf8'));
const axeVerify = JSON.parse(fs.readFileSync(`${CAND}/verify-axe-vs-freeze.json`, 'utf8'));
const swordVerify = JSON.parse(fs.readFileSync(`${CAND}/verify-vs-freeze.json`, 'utf8'));

const jobs = [
  {
    base: 'characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2/clip.json',
    dir: `${CAND}/clip/back_r/Sword/Attack-representative-v2-occlusion-v1`,
    master: `${CAND}/aseprite/sword-attack-representative-v2-occlusion-v1.aseprite`,
    bodyMaster: `${CAND}/aseprite/sword-body-representative-v2.aseprite`,
    reuseNativeMaster: true,
    verify: swordVerify,
    status: 'REJECTED_BY_SEMANTIC_AUDIT',
    decision:
      'REJECTED. The expansion restores glove pixels over the weapon, but the band audit proves those pixels hide guard (14) and pommel (50) rather than the grip: it removes exactly the features that make a grip legible. The real defect is weapon placement (the pommel lands inside the fist silhouette), not the handFront mask. Kept only as evidence; not a candidate.',
    pixels: pawn.frames.reduce((a, b) => a + b.added, 0),
    frames: pawn.frames.filter((f) => f.added > 0).map((f) => f.index),
    authoringScript: 'experiments/main-orc-targeted-repair-v1/artist-rear/lua/author_handfront_occlusion_back_r_sword.lua',
    exportScript: 'experiments/main-orc-targeted-repair-v1/artist-rear/lua/export_candidate_back_r_sword.lua',
    audit: `${CAND}/audit-expansion-bands.txt`,
    notAddressed: [
      'pale grey rim of the generated rear body (systemic; not touched)',
      'guard/pommel occlusion arithmetic: a mask change cannot fix it',
      'glove leather and handle wood share one brown ramp',
    ],
  },
  {
    base: 'characters/orc-v1/source/rear-recovery-v2/back_r/Axe/Attack-representative-v1/clip.json',
    dir: `${CAND}/clip/back_r/Axe/Attack-representative-v1-microclean`,
    master: `${CAND}/aseprite/axe-attack-representative-v1-microclean.aseprite`,
    bodyMaster: `${CAND}/aseprite/axe-body-representative-v1-microclean.aseprite`,
    reuseNativeMaster: false,
    nativeMaster: `${CAND}/aseprite/axe-body-representative-v1-back_r-microclean.aseprite`,
    verify: axeVerify,
    status: 'HYPOTHESIS_NOT_INTEGRATED',
    decision:
      'HIPOTESE NAO INTEGRADA. Os 11 pixels NAO constituem correcao artistica provada. Medido sobre o freeze: (a) os 8 pixels de y=191 sao uma faixa palida uniforme (122,123,125) imediatamente abaixo da linha de contorno ink (2,2,3)/(7,7,10) de y=190, isto e, o rebordo claro da sola projetando 1 px abaixo do contorno - remover recorta a sola e e o MESMO defeito sistemico de rebordo palido que este pool decidiu nao tocar nos outros quadros; (b) os 2 pixels de (144,64)/(145,64) estao na primeira linha do recorte nativo, sem vizinhos em nenhuma direcao, e podem ser fragmento de membro/arma cortado pelo recorte e nao sujeira independente; (c) o pixel de (171,151) esta a 2 px de um aglomerado escuro real em (168,152)-(169,154) e pode ser um fleco intencional dele. Conectividade e limiar de cor nao decidem intencao. Nenhum dos tres casos foi validado como defeito; ficam como hipotese aguardando decisao do criador.',
    risks: [
      'os 8 px de y=191 podem ser a sola/rebordo da bota: a remocao encurta a silhueta em 1 px e deixa o contorno ink como borda inferior',
      'os 2 px de (144,64)/(145,64) podem ser fragmento de membro ou de arma cortado pelo recorte nativo 128',
      'o px de (171,151) pode ser fleco intencional do aglomerado (168,152)-(169,154)',
      'conectividade 8 e limiar de cor sao medidas geometricas, nao provas de intencao artistica',
      'remover o rebordo palido de y=191 contradiz a decisao de nao tocar o rebordo palido sistemico dos demais quadros',
    ],
    pixels: 11,
    frames: [1, 2, 6],
    authoringScript: 'experiments/main-orc-targeted-repair-v1/artist-rear/lua/author_axe_microclean.lua',
    exportScript: 'experiments/main-orc-targeted-repair-v1/artist-rear/lua/export_candidate_back_r_axe.lua',
    notAddressed: [
      'pale grey rim of the generated rear body (systemic; not touched) - the y=191 row is the same rim',
      'weapon-over-fist occlusion: 42/30/22 px of the fist are painted by the axe in frames 1/4/5',
      'pommel buried inside the fist (placement, not mask)',
      'whether any of the three micro-cleanup sites is actually an artifact at all',
    ],
  },
];

for (const job of jobs) {
  const base = JSON.parse(fs.readFileSync(job.base, 'utf8'));
  const out = structuredClone(base);
  out.revision = `main-orc-targeted-repair-v1-${job.dir.split('/').slice(-2, -1)[0].toLowerCase()}-${job.dir.split('/').slice(-1)[0].toLowerCase()}`;
  out.parentClip = job.base;
  out.parentClipSha256 = sha(job.base);
  out.master = job.master;
  out.masterSha256 = sha(job.master);
  out.bodyMaster = job.bodyMaster;
  out.bodyMasterSha256 = sha(job.bodyMaster);
  out.nativeMaster = job.reuseNativeMaster ? base.nativeMaster : job.nativeMaster;
  out.nativeMasterSha256 = sha(out.nativeMaster);
  out.strip = `${job.dir}/native-strip.png`;
  out.stripSha256 = sha(out.strip);
  for (const frame of out.frames) {
    const i = String(frame.index).padStart(2, '0');
    frame.png = `${job.dir}/${i}.png`;
    frame.sha256 = sha(frame.png);
    frame.nativePng = `${job.dir}/native/${i}.png`;
    frame.nativeSha256 = sha(frame.nativePng);
    for (const layer of Object.keys(frame.layers)) {
      frame.layers[layer].png = `${job.dir}/layers/${layer}/${i}.png`;
      frame.layers[layer].sha256 = sha(frame.layers[layer].png);
    }
  }
  out.targetedRepair = {
    candidateId: 'main-orc-targeted-repair-v1',
    clip: job.base.split('/').slice(-3, -2)[0] + '/' + job.base.split('/').slice(-4, -3)[0],
    pool: 'main-orc-targeted-repair-v1/artist-rear',
    status: job.status,
    decision: job.decision,
    authoring: 'Aseprite 1.3.18.6, Lua, programmatic authorship by the agent (not manual drawing)',
    authoringScript: job.authoringScript,
    exportScript: job.exportScript,
    semanticAudit: job.audit ?? null,
    pixelsChanged: job.pixels,
    framesTouched: job.frames,
    frameCount: out.frameCount,
    durationsMs: out.durationsMs,
    timingChanged: false,
    generationCalls: 0,
    externalCost: 0,
    filesByteIdenticalToParent: job.verify.identical.length,
    changedFiles: job.verify.changed.map((c) => ({ file: c.file, diffPixels: c.diffPixels ?? null, bbox: c.diffBBox ?? null })),
    notAddressed: job.notAddressed,
    risks: job.risks ?? null,
    artisticApproval: 'PENDING_CREATOR',
  };
  out.technicalStatus = 'TECHNICALLY_COMPLETE';
  out.artisticStatus = job.status === 'REJECTED_BY_SEMANTIC_AUDIT' ? 'ARTISTIC_REVISION_REQUIRED' : 'ARTISTIC_REVISION_REQUIRED';
  out.artisticApproval = 'PENDING_CREATOR';
  out.reviewEvidence = {
    ...out.reviewEvidence,
    targetedRepairComparator: `${CAND}/comparator.html`,
    verifyVsFreeze: job.verify === axeVerify ? `${CAND}/verify-axe-vs-freeze.json` : `${CAND}/verify-vs-freeze.json`,
    creatorApproval: 'PENDING_CREATOR',
  };
  fs.writeFileSync(`${job.dir}/clip.json`, `${JSON.stringify(out, null, 2)}\n`);
  console.log(`${job.dir}/clip.json  master=${out.masterSha256.slice(0, 12)}  pixels=${job.pixels}  identical=${job.verify.identical.length}`);
}
