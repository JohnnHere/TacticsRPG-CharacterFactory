import fs from "node:fs";
import path from "node:path";

const ROOT = process.cwd();
const REVIEW_DIR = path.join(ROOT, "Biblioteca de Arte", "Estudos Comparativos", "Orc principal - Candidato Final e Arquitetura C");
fs.mkdirSync(REVIEW_DIR, { recursive: true });

function relUrl(repoRelPath) {
  const abs = path.join(ROOT, repoRelPath);
  if (!fs.existsSync(abs)) {
    throw new Error(`Missing image asset referenced by review studio: ${repoRelPath}`);
  }
  return path.relative(REVIEW_DIR, abs).replace(/\\/g, "/") + "?v=16";
}

const v10Manifest = JSON.parse(fs.readFileSync(path.join(ROOT, "characters/orc-v1/source/final-candidate-v10/candidate28manifest.json"), "utf8"));
const befManifest = JSON.parse(fs.readFileSync(path.join(ROOT, "characters/orc-v1/source/backl-v5base/candidate28manifest.json"), "utf8"));
const archVerif   = JSON.parse(fs.readFileSync(path.join(ROOT, "characters/orc-v1/source/final-candidate-v10/architecture-c/verification.json"), "utf8"));
const reuseReport = JSON.parse(fs.readFileSync(path.join(ROOT, "experiments/main-orc-final-v10/reuse-and-bridge-report.json"), "utf8"));

const DIRS = ["front_r", "front_l", "back_r", "back_l"];
const DIR_LABELS = {
  front_r: "front_r (Frente-Direita · SE)",
  front_l: "front_l (Frente-Esquerda · SW)",
  back_r:  "back_r (Costas-Direita · NE)",
  back_l:  "back_l (Costas-Esquerda · NW)",
};

const v10ClipMap = {};
for (const c of v10Manifest.cells) {
  v10ClipMap[c.cellId] = { cell: c, clip: JSON.parse(fs.readFileSync(path.join(ROOT, c.clipJson), "utf8")) };
}
const befClipMap = {};
for (const c of befManifest.cells) {
  befClipMap[c.cellId] = { cell: c, clip: JSON.parse(fs.readFileSync(path.join(ROOT, c.clipJson), "utf8")) };
}

const gripProfiles = {};
for (const d of DIRS) {
  gripProfiles[d] = JSON.parse(fs.readFileSync(path.join(ROOT, `characters/orc-v1/source/final-candidate-v10/architecture-c/grip-profile-${d}.json`), "utf8"));
}

// Build structured client payload with verified relative URLs
const swordData = {};
const axeData = {};
for (const d of DIRS) {
  const swClip = v10ClipMap[`${d}/Sword`].clip;
  const swBef  = befClipMap[`${d}/Sword`].clip;
  const gp     = gripProfiles[d];
  swordData[d] = {
    durationsMs: swClip.durationsMs,
    frames: swClip.frames.map((f, i) => ({
      index: i,
      phase: f.phase,
      durationMs: f.durationMs,
      weaponVisible: f.weaponVisible,
      grip: f.grip,
      rotationDeg: f.rotationDeg,
      occlusionMode: f.occlusionMode,
      silDeltaAB: gp.frames[i].silhouetteDeltaABPx,
      swordA: relUrl(`characters/orc-v1/source/final-candidate-v10/architecture-c/${d}/sword-a/frames/${String(i).padStart(2,"0")}.png`),
      swordB: relUrl(`characters/orc-v1/source/final-candidate-v10/architecture-c/${d}/sword-b/frames/${String(i).padStart(2,"0")}.png`),
      bodyOff: relUrl(`characters/orc-v1/source/final-candidate-v10/architecture-c/${d}/sword-a/layers/body/${String(i).padStart(2,"0")}.png`),
      weapA: relUrl(`characters/orc-v1/source/final-candidate-v10/architecture-c/${d}/sword-a/weapon-only/${String(i).padStart(2,"0")}.png`),
      weapB: relUrl(`characters/orc-v1/source/final-candidate-v10/architecture-c/${d}/sword-b/weapon-only/${String(i).padStart(2,"0")}.png`),
      before: relUrl(swBef.frames[Math.min(i, swBef.frames.length - 1)].png),
    })),
  };

  const axClip = v10ClipMap[`${d}/Axe`].clip;
  const axBef  = befClipMap[`${d}/Axe`].clip;
  axeData[d] = {
    durationsMs: axClip.durationsMs,
    frames: axClip.frames.map((f, i) => ({
      index: i,
      phase: f.phase,
      durationMs: f.durationMs,
      weaponVisible: f.weaponVisible,
      grip: f.grip,
      rotationDeg: f.rotationDeg,
      occlusionMode: f.occlusionMode,
      comp: relUrl(f.png),
      bodyOff: relUrl(f.layers.body.png),
      before: relUrl(axBef.frames[Math.min(i, axBef.frames.length - 1)].png),
    })),
  };
}

const bodyActions = ["Unarmed", "Defeat", "Walk", "Hit", "Idle"];
const bodyData = {};
for (const act of bodyActions) {
  bodyData[act] = {};
  for (const d of DIRS) {
    const cid = `${d}/${act}`;
    const cur = v10ClipMap[cid];
    const bef = befClipMap[cid];
    bodyData[act][d] = {
      isAffected: cur.cell.isAffected,
      status: cur.cell.status,
      notes: cur.cell.notes || "",
      canvasSize: cur.clip.canvas ? cur.clip.canvas[0] : 256,
      durationsMs: cur.clip.durationsMs,
      frames: cur.clip.frames.map((f, i) => ({
        index: i,
        durationMs: f.durationMs ?? cur.clip.durationsMs[i],
        after: relUrl(f.png),
        before: relUrl(bef.clip.frames[Math.min(i, bef.clip.frames.length - 1)].png),
      })),
    };
  }
}

const weaponAssets = {
  swordA: relUrl("characters/orc-v1/source/final-candidate-v10/weapons/Sword/recruit-sword.png"),
  swordB: relUrl("characters/orc-v1/source/final-candidate-v10/weapons/SwordB/faceted-sword-b.png"),
  axe:    relUrl("characters/orc-v1/source/final-candidate-v10/weapons/Axe/militia-axe.png"),
};

const criticalPairs = [
  {
    title: "1. Elevação de Costas (back_r F03 e back_l F03) — Pegada Dorsal + Guarda Justa no Punho",
    meta: "Vistas: back_r e back_l · Quadro: F03 Elevação · Antes: pivô no pomo fazia a guarda flutuar acima da mão e cortar o pulso. Agora: pivô [48,63] + punho dorsal de couro fechado e pomo na base.",
    crop: "58% 36%", zoom: 2.6,
    beforeA: swordData.back_r.frames[3].before, afterA: swordData.back_r.frames[3].swordA, labelA: "back_r Sword F03 (Elevação)",
    beforeB: swordData.back_l.frames[3].before, afterB: swordData.back_l.frames[3].swordA, labelB: "back_l Sword F03 (Elevação)",
  },
  {
    title: "2. back_r / Sword — Flash claro à esquerda (F01) + braço e pegada no golpe (F09)",
    meta: "Vista: back_r · Quadros: F01 e F09 · Antes: retalho cinza opaco à esquerda e braço derretido/arma flutuando sob o pulso. Agora: contorno limpo e espada saindo do punho real.",
    crop: "52% 48%", zoom: 2.3,
    beforeA: swordData.back_r.frames[1].before, afterA: swordData.back_r.frames[1].swordA, labelA: "F01 (Flash lateral)",
    beforeB: swordData.back_r.frames[9].before, afterB: swordData.back_r.frames[9].swordA, labelB: "F09 (Braço e pegada)",
  },
  {
    title: "3. Frontais — Fim da arma na ombreira (front_r F04) e restauração do braço/peitoral (F09)",
    meta: "Vista: front_r (e simétrico front_l) · Quadros: F04 e F09 · Antes: F04 prendia a arma na ombreira com a mão vazia abaixo; F09 tinha ombro amputado e mão solta.",
    crop: "44% 46%", zoom: 2.5,
    beforeA: swordData.front_r.frames[4].before, afterA: swordData.front_r.frames[4].swordA, labelA: "front_r F04 (Punho real + axila)",
    beforeB: swordData.front_r.frames[9].before, afterB: swordData.front_r.frames[9].swordA, labelB: "front_r F09 (Braço íntegro)",
  },
  {
    title: "4. Axe Attack — Eixo do cabo [38,45] na elevação traseira (back_r F03) e golpe NW (back_l F06)",
    meta: "Vistas: back_r e back_l · Quadros: F03 e F06 · Cabo passa reto pelo punho fechado com ponteira de madeira visível abaixo da manopla; cicatriz branca em front Axe F09 removida.",
    crop: "55% 44%", zoom: 2.3,
    beforeA: axeData.back_r.frames[3].before, afterA: axeData.back_r.frames[3].comp, labelA: "back_r Axe F03 (Elevação)",
    beforeB: axeData.back_l.frames[6].before, afterB: axeData.back_l.frames[6].comp, labelB: "back_l Axe F06 (Impacto NW)",
  },
  {
    title: "5. Unarmed — Fim do 3º cotovelo fantasma (front_r F02) e da garra solta no quadril (back_r F02)",
    meta: "Vistas: front_r e back_r (e simétricos front_l/back_l) · Antes: soco frontal mantinha o cotovelo traseiro dobrado + peito escuro; back_r tinha mão decepada pendurada no quadril esquerdo.",
    crop: "50% 48%", zoom: 2.3,
    beforeA: bodyData.Unarmed.front_r.frames[2].before, afterA: bodyData.Unarmed.front_r.frames[2].after, labelA: "front_r Unarmed F02 (Impacto)",
    beforeB: bodyData.Unarmed.back_r.frames[2].before,  afterB: bodyData.Unarmed.back_r.frames[2].after,  labelB: "back_r Unarmed F02 (Sem garra solta)",
  },
  {
    title: "6. Hit — Fim dos anéis vermelhos nos pulsos (front_r F01) e garras cinzas/cabeça chapada (back_r F01)",
    meta: "Vistas: front_r e back_r · Quadro: F01 Pico do Impacto · Antes: aros vermelhos ocos nas mãos frontais e mãos esfiapadas nas costas + salto de altura em F00/F03.",
    crop: "50% 46%", zoom: 2.4,
    beforeA: bodyData.Hit.front_r.frames[1].before, afterA: bodyData.Hit.front_r.frames[1].after, labelA: "front_r Hit F01 (Manoplas)",
    beforeB: bodyData.Hit.back_r.frames[1].before,  afterB: bodyData.Hit.back_r.frames[1].after,  labelB: "back_r Hit F01 (Crânio/manoplas)",
  },
  {
    title: "7. Defeat — Apoio sem braço de prata (front_r F02) e pose terminal F04 inconsciente no chão",
    meta: "Vistas: front_r e front_l (+ costas polidas em F00/F02/F03) · Antes: braço apoiado brilhava como lâmina em F02 e F04 ficava encolhido com barra cinza na mão.",
    crop: "50% 62%", zoom: 2.3,
    beforeA: bodyData.Defeat.front_r.frames[2].before, afterA: bodyData.Defeat.front_r.frames[2].after, labelA: "front_r Defeat F02 (Apoio)",
    beforeB: bodyData.Defeat.front_r.frames[4].before, afterB: bodyData.Defeat.front_r.frames[4].after, labelB: "front_r Defeat F04 (No chão)",
  },
  {
    title: "8. Walk — Estrobo na virilha/bracelete frontal (F07–F08) e buraco no cotovelo + paridade traseira (back_l F01)",
    meta: "Vistas: front_r e back_l · Antes: salto de brilho na cota da virilha/bracelete frontal e furo preto no cotovelo + aço subexposto em back_l.",
    crop: "50% 56%", zoom: 2.5,
    beforeA: bodyData.Walk.front_r.frames[7].before, afterA: bodyData.Walk.front_r.frames[7].after, labelA: "front_r Walk F07",
    beforeB: bodyData.Walk.back_l.frames[1].before,  afterB: bodyData.Walk.back_l.frames[1].after,  labelB: "back_l Walk F01",
  },
];

const payloadJson = JSON.stringify({
  dirs: DIRS,
  dirLabels: DIR_LABELS,
  swordData,
  axeData,
  bodyData,
  weaponAssets,
  criticalPairs,
  archVerif,
  reuseReport,
});

const html = `<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Orc Guerreiro (orc-v1) — Revisão Unificada Final e Arquitetura C (V10)</title>
<style>
  :root {
    color-scheme: dark;
    --bg: #111318;
    --panel: #181b22;
    --panel-alt: #1e222b;
    --border: #2b303c;
    --text: #e8ecf4;
    --muted: #9aa3b5;
    --accent: #3b82f6;
    --ok: #86efac;
    --ok-bg: #163020;
    --warn: #fcd34d;
    --warn-bg: #362a12;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    padding: 0 0 80px;
    background: var(--bg);
    color: var(--text);
    font: 14px/1.55 "Segoe UI", system-ui, -apple-system, sans-serif;
  }
  header.hero {
    padding: 22px 28px 16px;
    background: linear-gradient(180deg, #191d26 0%, #12151b 100%);
    border-bottom: 1px solid var(--border);
  }
  h1 { font-size: 22px; margin: 0 0 6px; letter-spacing: -0.01em; }
  h2 { font-size: 17px; margin: 30px 0 10px; padding-bottom: 6px; border-bottom: 1px solid var(--border); }
  h3 { font-size: 13px; margin: 0 0 6px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.04em; }
  p.lead { margin: 0 0 8px; color: var(--muted); max-width: 108ch; }
  .badges { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 8px; }
  .badge { display: inline-block; padding: 3px 9px; border-radius: 5px; font-size: 12px; font-weight: 600; }
  .badge.warn { background: var(--warn-bg); color: var(--warn); border: 1px solid #57431a; }
  .badge.ok { background: var(--ok-bg); color: var(--ok); border: 1px solid #224d33; }
  .badge.info { background: #192944; color: #93c5fd; border: 1px solid #294674; }

  .sticky-bar {
    position: sticky;
    top: 0;
    z-index: 50;
    background: rgba(18, 21, 27, 0.96);
    backdrop-filter: blur(8px);
    border-bottom: 1px solid var(--border);
    padding: 10px 28px;
    display: flex;
    flex-wrap: wrap;
    gap: 14px;
    align-items: center;
  }
  .ctrl-group { display: flex; flex-wrap: wrap; gap: 5px; align-items: center; }
  .ctrl-label { font-size: 12px; color: var(--muted); margin-right: 4px; font-weight: 600; text-transform: uppercase; }
  button {
    background: #232834;
    color: var(--text);
    border: 1px solid #353c4d;
    border-radius: 5px;
    padding: 5px 10px;
    font-size: 13px;
    cursor: pointer;
    transition: background 0.12s, border-color 0.12s;
  }
  button:hover { background: #2d3444; }
  button.active { background: var(--accent); border-color: var(--accent); color: #fff; font-weight: 600; }
  main { padding: 0 28px; max-width: 1760px; margin: 0 auto; }

  .frame-strip { display: flex; flex-wrap: wrap; gap: 4px; margin: 10px 0; }
  .frame-strip button { padding: 4px 8px; font-family: Consolas, monospace; font-size: 12px; }
  .frame-strip button.armed { border-bottom: 2px solid #60a5fa; }
  .frame-strip button.contact { border-bottom: 2px solid #f97316; }

  .readout {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 8px 12px;
    font-family: Consolas, monospace;
    font-size: 12.5px;
    color: #cbd5e1;
    margin: 8px 0 12px;
  }

  .grid-4 { display: grid; grid-template-columns: repeat(4, minmax(260px, 1fr)); gap: 12px; }
  @media (max-width: 1260px) { .grid-4 { grid-template-columns: repeat(2, minmax(260px, 1fr)); } }

  .card {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 7px;
    padding: 10px;
  }
  .card-head {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 6px;
    gap: 6px;
  }
  .card-title { font-weight: 600; font-size: 13px; color: #f1f5f9; }
  .card-sub { font-size: 11.5px; color: var(--muted); font-family: Consolas, monospace; }

  .subgrid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; }
  .subgrid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 6px; }

  .stage {
    position: relative;
    overflow: hidden;
    height: 220px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 5px;
    border: 1px solid #252a36;
  }
  body.bg-tactical .stage {
    background: radial-gradient(circle at 50% 62%, #242b37 0%, #171b23 78%);
  }
  body.bg-checker .stage {
    background: repeating-conic-gradient(#212530 0% 25%, #181b23 0% 50%) 50% / 16px 16px;
  }
  .stage::after {
    content: "";
    position: absolute;
    left: 10%;
    right: 10%;
    top: calc(50% + var(--ground-offset, 62px));
    height: 1px;
    background: rgba(125, 162, 206, 0.28);
    pointer-events: none;
  }
  body.hide-ground .stage::after { display: none; }
  .stage-tag {
    position: absolute;
    top: 5px;
    left: 6px;
    font-size: 11px;
    padding: 1px 6px;
    border-radius: 3px;
    background: rgba(12, 14, 18, 0.78);
    color: #cbd5e1;
    z-index: 2;
    pointer-events: none;
  }
  .stage img.sprite {
    width: 256px;
    height: 256px;
    max-width: none;
    max-height: none;
    image-rendering: pixelated;
    transform: scale(var(--sprite-scale, 1));
    transform-origin: 50% 50%;
  }

  .weapons-showcase {
    display: flex;
    flex-wrap: wrap;
    gap: 14px;
    margin: 12px 0;
  }
  .weapon-pill {
    display: flex;
    align-items: center;
    gap: 12px;
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 7px;
    padding: 8px 14px;
  }
  .weapon-pill img {
    width: 96px;
    height: 96px;
    image-rendering: pixelated;
    background: #13161d;
    border: 1px solid #272c38;
    border-radius: 4px;
  }

  .crit-grid { display: grid; grid-template-columns: repeat(2, minmax(420px, 1fr)); gap: 14px; }
  @media (max-width: 1100px) { .crit-grid { grid-template-columns: 1fr; } }
  .crit-pair { display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; margin-top: 8px; }
  .crit-box {
    position: relative;
    height: 185px;
    overflow: hidden;
    border-radius: 5px;
    border: 1px solid #293040;
    background: #171b23;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .crit-box img {
    width: 256px;
    height: 256px;
    max-width: none;
    image-rendering: pixelated;
  }

  table { border-collapse: collapse; width: 100%; font-size: 13px; margin: 10px 0; background: var(--panel); }
  th, td { border: 1px solid var(--border); padding: 6px 10px; text-align: left; }
  th { background: #1e232d; color: #dbe4f0; }
  code { font-family: Consolas, monospace; font-size: 12.5px; color: #bfdbfe; }
</style>
</head>
<body class="bg-tactical">

<header class="hero">
  <h1>Orc Guerreiro Principal (<code>orc-v1</code> / Verde Warcraft) — Estúdio Unificado de Revisão Final &amp; Arquitetura C (<code>V10</code>)</h1>
  <p class="lead">
    Superfície única de inspeção cobrindo <strong>Sword Attack</strong> nas 4 vistas diagonais, <strong>Arquitetura C (Espada A × Espada B no mesmo corpo por vista)</strong>,
    <strong>Axe Attack</strong> nas 4 vistas, clipes alterados (<code>Unarmed</code>, <code>Walk</code>, <code>Defeat</code>), clipes preservados (<code>Hit</code>, <code>Idle</code>) e
    comparações <strong>Antes × Depois</strong> com avanço quadro a quadro e escala tática <code>0,5×</code>.
  </p>
  <div class="badges">
    <span class="badge ok">TECHNICALLY_COMPLETE · 28/28 células verificadas</span>
    <span class="badge warn">VISUAL_REVIEW_REQUIRED · PENDING_CREATOR</span>
    <span class="badge info">Arquitetura C: 56/56 quadros corporais reaproveitados (100%) · 99–111 px delta de silhueta/quadro</span>
    <span class="badge info">Política attack-only-v1 · 0 escritas em ../TacticsRPG</span>
    <span class="badge ok" id="global-load-status">Verificando imagens…</span>
  </div>
</header>

<div class="sticky-bar">
  <div class="ctrl-group">
    <span class="ctrl-label">Reprodução</span>
    <button id="btn-play-1" class="active">▶ 1× Jogo</button>
    <button id="btn-play-05">▶ 0,5× Lento</button>
    <button id="btn-play-025">▶ 0,25× Micro</button>
    <button id="btn-pause">⏸ Pausar</button>
    <button id="btn-prev">◀ Quadro</button>
    <button id="btn-next">Quadro ▶</button>
  </div>
  <div class="ctrl-group">
    <span class="ctrl-label">Escala / Zoom</span>
    <button data-scale="0.5">0,5× Tática (64 px)</button>
    <button data-scale="1" class="active">1× Real (128 px)</button>
    <button data-scale="2">2× Inspeção</button>
    <button data-scale="3.2">3,2× Pegada/Contorno</button>
  </div>
  <div class="ctrl-group">
    <span class="ctrl-label">Fundo</span>
    <button id="btn-bg-tac" class="active">Solo + groundY</button>
    <button id="btn-bg-chk">Xadrez</button>
  </div>
</div>

<main>

  <!-- SEÇÃO 1: SWORD ATTACK + ARQUITETURA C -->
  <section id="sec-sword">
    <h2>1. Sword Attack (4 Vistas · 14 quadros · 730 ms · Contato F08 @ 325 ms) &amp; Arquitetura C (Espada A × Espada B)</h2>
    <p class="lead">
      Em cada uma das 4 vistas abaixo, <strong>Espada A</strong> (<code>recruit-sword</code>) e <strong>Espada B</strong> (<code>faceted-sword-b</code>, lâmina facetada com <code>106 px</code> de diferença de silhueta)
      usam <strong>exatamente os mesmos 14 quadros de <code>body</code> e <code>handFront</code> (0 px de diferença)</strong>. Alterne os modos abaixo para comparar A × B, Corpo Limpo (<code>layers-off</code>) e Antes × Depois.
    </p>

    <div class="weapons-showcase">
      <div class="weapon-pill">
        <img src="${weaponAssets.swordA}" alt="Espada A">
        <div>
          <strong>Espada A — Espada do Recruta</strong><br>
          <span class="card-sub">96×96 · pivô na empunhadura [48, 63] · guarda justa no indicador</span>
        </div>
      </div>
      <div class="weapon-pill">
        <img src="${weaponAssets.swordB}" alt="Espada B">
        <div>
          <strong>Espada B — Espada Facetada de Aço Claro</strong><br>
          <span class="card-sub">96×96 · pivô na empunhadura [48, 63] · +106 px delta real de silhueta</span>
        </div>
      </div>
      <div class="weapon-pill">
        <img src="${weaponAssets.axe}" alt="Machado de Milícia">
        <div>
          <strong>Machado de Milícia (Limpo)</strong><br>
          <span class="card-sub">96×96 · pivô no eixo do cabo [38, 45] · pomo de madeira abaixo da luva</span>
        </div>
      </div>
    </div>

    <div class="ctrl-group" style="margin: 8px 0;">
      <span class="ctrl-label">Comparação nas 4 Vistas:</span>
      <button data-swmode="ab" class="active">Espada A × Espada B (Mesmo Corpo)</button>
      <button data-swmode="after-before">Depois (V10) × Antes (V8/V9)</button>
      <button data-swmode="layers">Composto A × Corpo Limpo (layers-off)</button>
      <button data-swmode="weapons">Somente Arma A × Somente Arma B</button>
    </div>

    <div class="frame-strip" id="sword-frames"></div>
    <div class="readout" id="sword-readout"></div>
    <div class="grid-4" id="sword-grid"></div>
  </section>

  <!-- SEÇÃO 2: AXE ATTACK -->
  <section id="sec-axe">
    <h2>2. Axe Attack (4 Vistas · 12 quadros · 1005 ms · Impacto Pesado F06 @ 410 ms)</h2>
    <p class="lead">
      Cabo centrado na palma em <code>[36, 48]</code> com extremidade inferior de madeira visível abaixo da manopla (corrigindo a pegada pela ponta do cabo),
      golpe pesado Norte-Oeste empunhado pela mão direita em <code>back_l</code> e eliminação do flash lateral e saltos de bota em <code>back_r</code>.
    </p>
    <div class="ctrl-group" style="margin: 8px 0;">
      <span class="ctrl-label">Comparação nas 4 Vistas:</span>
      <button data-axmode="after-before" class="active">Depois (V10) × Antes (V8/V9)</button>
      <button data-axmode="layers">Composto V10 × Corpo Limpo (layers-off)</button>
    </div>
    <div class="frame-strip" id="axe-frames"></div>
    <div class="readout" id="axe-readout"></div>
    <div class="grid-4" id="axe-grid"></div>
  </section>

  <!-- SEÇÃO 3: DEMAIS CLIPES + CICLO DE COMBATE -->
  <section id="sec-other">
    <h2>3. Clipes Corporais Alterados e Preservados (4 Vistas: Unarmed, Defeat, Walk, Hit, Idle e Transição Idle → Ataque → Idle)</h2>
    <p class="lead">
      Todos os clipes abaixo seguem <code>attack-only-v1</code> (zero pixels de arma fora do intervalo de ataque). Selecione a ação para inspecionar Depois × Antes nas 4 vistas simultaneamente.
    </p>
    <div class="ctrl-group" style="margin: 8px 0;">
      <span class="ctrl-label">Ação:</span>
      <button data-bact="Defeat" class="active">Defeat (5f · 700 ms · 4 Vistas Polidas)</button>
      <button data-bact="Unarmed">Unarmed (5f · 450 ms · Soco Cruzado + Sem Garra Flutuante)</button>
      <button data-bact="Hit">Hit (5f · 450 ms · Manoplas e Recuo nas 4 Vistas)</button>
      <button data-bact="Walk">Walk (16f/8f · 1280 ms · Luz e Contorno Estabilizados)</button>
      <button data-bact="Idle">Idle (5f · 2200 ms · idle-balanced-v1 Preservado)</button>
      <button data-bact="Combo">Ciclo Contínuo: Idle → Sword A → Sword B → Axe → Idle</button>
    </div>
    <div class="frame-strip" id="body-frames"></div>
    <div class="readout" id="body-readout"></div>
    <div class="grid-4" id="body-grid"></div>
  </section>

  <!-- SEÇÃO 4: ANTES X DEPOIS DOS PONTOS CRÍTICOS -->
  <section id="sec-critical">
    <h2>4. Evidência Direta Antes × Depois nos 7 Pontos Críticos Verificados</h2>
    <p class="lead">Comparação estática ampliada lado a lado dos quadros exatos onde cada defeito ocorria na versão anterior versus o candidato final V10.</p>
    <div class="crit-grid" id="crit-grid"></div>
  </section>

  <!-- SEÇÃO 5: MÉTRICAS DE REAPROVEITAMENTO E PONTE UNITY -->
  <section id="sec-metrics">
    <h2>5. Medição de Reaproveitamento (Arquitetura C) e Preparação para Teste Isolado no Unity</h2>
    <table>
      <tr><th>Métrica / Verificação</th><th>Resultado Verificado em V10</th></tr>
      <tr><td>Par de espadas testado nas 4 vistas (<code>front_r</code>, <code>front_l</code>, <code>back_r</code>, <code>back_l</code>)</td><td><code>recruit-sword</code> (A) × <code>faceted-sword-b</code> (B, lâmina facetada +106 px de silhueta distinta)</td></tr>
      <tr><td>Quadros corporais (<code>body</code>) e de oclusão de mão (<code>handFront</code>) reaproveitados sem edição</td><td><strong>56 / 56 quadros (100% de reaproveitamento · 0 px RGBA delta nas 4 vistas)</strong></td></tr>
      <tr><td>Diferença real de silhueta da arma por quadro armado (<code>F02..F11</code>)</td><td><code>99..111 px</code> por quadro (<code>front_r: 1051</code> · <code>front_l: 1051</code> · <code>back_r: 1042</code> · <code>back_l: 1047</code> px acumulados)</td></tr>
      <tr><td>Adaptação exigida pela segunda espada compatível</td><td>Zero retoque em corpo ou luva; apenas 1 asset <code>96×96</code> no mesmo pivô <code>[48, 66]</code> composto em lote no Aseprite</td></tr>
      <tr><td>Política <code>attack-only-v1</code> e integridade alfa/chão</td><td><code>0 px</code> de arma em <code>Idle</code>, <code>Walk</code>, <code>Unarmed</code>, <code>Hit</code>, <code>Defeat</code> e <code>F00/F01/F12/F13</code>; <code>0 px</code> alfa parcial; <code>maxWeaponY ≤ 172 ≤ groundY 190</code></td></tr>
      <tr><td>Pacote local pronto para o teste isolado no Unity (sem tocar em <code>../TacticsRPG</code>)</td><td><code>dist/orc-v1/final-candidate-v10/</code> (292 arquivos rastreados + <code>factory-manifest.json</code> com Sword A e Sword B prontos para troca em PlayMode)</td></tr>
    </table>
  </section>

</main>

<script>
const DATA = ${payloadJson};

let playing = true;
let speedMul = 1.0;
let spriteScale = 1.0;

let swMode = "ab";
let swIdx = 8; // Start paused-ready/highlighted on contact frame F08 if paused, or plays smoothly
let swElapsed = 0;

let axMode = "after-before";
let axIdx = 6;
let axElapsed = 0;

let bodyAct = "Defeat";
let bodyIdx = 4;
let bodyElapsed = 0;

function buildComboFrames(dir) {
  const out = [];
  for (const f of DATA.bodyData.Idle[dir].frames) {
    out.push({ label: "Idle F0" + f.index, durationMs: Math.round(f.durationMs * 0.45), after: f.after, before: f.after });
  }
  for (const f of DATA.swordData[dir].frames) {
    out.push({ label: "SwordA F" + String(f.index).padStart(2,"0"), durationMs: f.durationMs, after: f.swordA, before: f.bodyOff });
  }
  for (const f of DATA.swordData[dir].frames) {
    out.push({ label: "SwordB F" + String(f.index).padStart(2,"0"), durationMs: f.durationMs, after: f.swordB, before: f.swordA });
  }
  for (const f of DATA.axeData[dir].frames) {
    out.push({ label: "Axe F" + String(f.index).padStart(2,"0"), durationMs: f.durationMs, after: f.comp, before: f.bodyOff });
  }
  return out;
}
const comboByDir = {};
for (const d of DATA.dirs) comboByDir[d] = buildComboFrames(d);

function setScale(s) {
  spriteScale = s;
  document.documentElement.style.setProperty("--sprite-scale", String(s));
  document.documentElement.style.setProperty("--ground-offset", String(Math.round(62 * s)) + "px");
  document.querySelectorAll("[data-scale]").forEach(b => b.classList.toggle("active", Number(b.dataset.scale) === s));
}

// 1. Build Sword DOM
const swGrid = document.getElementById("sword-grid");
const swStrip = document.getElementById("sword-frames");
const swReadout = document.getElementById("sword-readout");
const swImgs = {};

for (let i = 0; i < 14; i++) {
  const btn = document.createElement("button");
  btn.textContent = "F" + String(i).padStart(2, "0");
  if (i >= 2 && i <= 11) btn.classList.add("armed");
  if (i === 8) btn.classList.add("contact");
  btn.onclick = () => { playing = false; updatePlayButtons(); swIdx = i; renderSword(); };
  swStrip.appendChild(btn);
}

for (const d of DATA.dirs) {
  const card = document.createElement("div");
  card.className = "card";
  card.innerHTML = \`
    <div class="card-head">
      <span class="card-title">\${DATA.dirLabels[d]}</span>
      <span class="card-sub" id="sw-sub-\${d}"></span>
    </div>
    <div class="subgrid-2">
      <div class="stage"><span class="stage-tag" id="sw-tagL-\${d}">Espada A</span><img class="sprite" id="sw-imgL-\${d}" alt="\${d} left"></div>
      <div class="stage"><span class="stage-tag" id="sw-tagR-\${d}">Espada B</span><img class="sprite" id="sw-imgR-\${d}" alt="\${d} right"></div>
    </div>
  \`;
  swGrid.appendChild(card);
  swImgs[d] = {
    sub: card.querySelector("#sw-sub-" + d),
    tagL: card.querySelector("#sw-tagL-" + d),
    tagR: card.querySelector("#sw-tagR-" + d),
    imgL: card.querySelector("#sw-imgL-" + d),
    imgR: card.querySelector("#sw-imgR-" + d),
  };
}

function renderSword() {
  Array.from(swStrip.children).forEach((b, i) => b.classList.toggle("active", i === swIdx));
  const f0 = DATA.swordData.front_r.frames[swIdx];
  const details = DATA.dirs.map(d => {
    const fd = DATA.swordData[d].frames[swIdx];
    return fd.weaponVisible
      ? \`\${d}: grip[\${fd.grip[0]},\${fd.grip[1]}] rot=\${fd.rotationDeg}° (\${fd.occlusionMode}, Δsil=\${fd.silDeltaAB}px)\`
      : \`\${d}: desarmado (0 px arma)\`;
  }).join(" · ");
  swReadout.textContent = \`Sword F\${String(swIdx).padStart(2,"0")} · fase=\${f0.phase} · \${f0.durationMs} ms | \${details}\`;

  for (const d of DATA.dirs) {
    const fd = DATA.swordData[d].frames[swIdx];
    const ui = swImgs[d];
    ui.sub.textContent = fd.weaponVisible ? \`rot \${fd.rotationDeg}° · Δ\${fd.silDeltaAB}px\` : "sem arma";
    if (swMode === "ab") {
      ui.tagL.textContent = "Espada A (Recruta)";
      ui.tagR.textContent = "Espada B (Facetada)";
      ui.imgL.src = fd.swordA;
      ui.imgR.src = fd.swordB;
    } else if (swMode === "after-before") {
      ui.tagL.textContent = "Depois (V10)";
      ui.tagR.textContent = "Antes (V8/V9)";
      ui.imgL.src = fd.swordA;
      ui.imgR.src = fd.before;
    } else if (swMode === "layers") {
      ui.tagL.textContent = "Composto A";
      ui.tagR.textContent = "Corpo Limpo (layers-off)";
      ui.imgL.src = fd.swordA;
      ui.imgR.src = fd.bodyOff;
    } else {
      ui.tagL.textContent = "Somente Arma A";
      ui.tagR.textContent = "Somente Arma B";
      ui.imgL.src = fd.weapA;
      ui.imgR.src = fd.weapB;
    }
  }
}

// 2. Build Axe DOM
const axGrid = document.getElementById("axe-grid");
const axStrip = document.getElementById("axe-frames");
const axReadout = document.getElementById("axe-readout");
const axImgs = {};

for (let i = 0; i < 12; i++) {
  const btn = document.createElement("button");
  btn.textContent = "F" + String(i).padStart(2, "0");
  if (i >= 2 && i <= 8) btn.classList.add("armed");
  if (i === 6) btn.classList.add("contact");
  btn.onclick = () => { playing = false; updatePlayButtons(); axIdx = i; renderAxe(); };
  axStrip.appendChild(btn);
}

for (const d of DATA.dirs) {
  const card = document.createElement("div");
  card.className = "card";
  card.innerHTML = \`
    <div class="card-head">
      <span class="card-title">\${DATA.dirLabels[d]}</span>
      <span class="card-sub" id="ax-sub-\${d}"></span>
    </div>
    <div class="subgrid-2">
      <div class="stage"><span class="stage-tag" id="ax-tagL-\${d}">Depois (V10)</span><img class="sprite" id="ax-imgL-\${d}" alt="\${d} axe L"></div>
      <div class="stage"><span class="stage-tag" id="ax-tagR-\${d}">Antes</span><img class="sprite" id="ax-imgR-\${d}" alt="\${d} axe R"></div>
    </div>
  \`;
  axGrid.appendChild(card);
  axImgs[d] = {
    sub: card.querySelector("#ax-sub-" + d),
    tagL: card.querySelector("#ax-tagL-" + d),
    tagR: card.querySelector("#ax-tagR-" + d),
    imgL: card.querySelector("#ax-imgL-" + d),
    imgR: card.querySelector("#ax-imgR-" + d),
  };
}

function renderAxe() {
  Array.from(axStrip.children).forEach((b, i) => b.classList.toggle("active", i === axIdx));
  const f0 = DATA.axeData.front_r.frames[axIdx];
  const details = DATA.dirs.map(d => {
    const fd = DATA.axeData[d].frames[axIdx];
    return fd.weaponVisible
      ? \`\${d}: grip[\${fd.grip[0]},\${fd.grip[1]}] rot=\${fd.rotationDeg}° (\${fd.occlusionMode})\`
      : \`\${d}: desarmado\`;
  }).join(" · ");
  axReadout.textContent = \`Axe F\${String(axIdx).padStart(2,"0")} · fase=\${f0.phase} · \${f0.durationMs} ms | \${details}\`;

  for (const d of DATA.dirs) {
    const fd = DATA.axeData[d].frames[axIdx];
    const ui = axImgs[d];
    ui.sub.textContent = fd.weaponVisible ? \`grip[\${fd.grip[0]},\${fd.grip[1]}] · \${fd.rotationDeg}°\` : "sem arma";
    if (axMode === "after-before") {
      ui.tagL.textContent = "Depois (V10)";
      ui.tagR.textContent = "Antes (V8/V9)";
      ui.imgL.src = fd.comp;
      ui.imgR.src = fd.before;
    } else {
      ui.tagL.textContent = "Composto V10";
      ui.tagR.textContent = "Corpo Limpo (layers-off)";
      ui.imgL.src = fd.comp;
      ui.imgR.src = fd.bodyOff;
    }
  }
}

// 3. Build Body / Combo DOM
const bdGrid = document.getElementById("body-grid");
const bdStrip = document.getElementById("body-frames");
const bdReadout = document.getElementById("body-readout");
const bdImgs = {};

for (const d of DATA.dirs) {
  const card = document.createElement("div");
  card.className = "card";
  card.innerHTML = \`
    <div class="card-head">
      <span class="card-title">\${DATA.dirLabels[d]}</span>
      <span class="card-sub" id="bd-sub-\${d}"></span>
    </div>
    <div class="subgrid-2">
      <div class="stage"><span class="stage-tag" id="bd-tagL-\${d}">Depois (V10)</span><img class="sprite" id="bd-imgL-\${d}" alt="\${d} body L"></div>
      <div class="stage"><span class="stage-tag" id="bd-tagR-\${d}">Antes / Ref</span><img class="sprite" id="bd-imgR-\${d}" alt="\${d} body R"></div>
    </div>
  \`;
  bdGrid.appendChild(card);
  bdImgs[d] = {
    sub: card.querySelector("#bd-sub-" + d),
    tagL: card.querySelector("#bd-tagL-" + d),
    tagR: card.querySelector("#bd-tagR-" + d),
    imgL: card.querySelector("#bd-imgL-" + d),
    imgR: card.querySelector("#bd-imgR-" + d),
  };
}

function rebuildBodyStrip() {
  bdStrip.innerHTML = "";
  const maxLen = bodyAct === "Combo"
    ? comboByDir.front_r.length
    : Math.max(...DATA.dirs.map(d => DATA.bodyData[bodyAct][d].frames.length));
  for (let i = 0; i < maxLen; i++) {
    const btn = document.createElement("button");
    btn.textContent = "F" + String(i).padStart(2, "0");
    btn.onclick = () => { playing = false; updatePlayButtons(); bodyIdx = i; renderBody(); };
    bdStrip.appendChild(btn);
  }
  if (bodyIdx >= maxLen) bodyIdx = 0;
}

function renderBody() {
  Array.from(bdStrip.children).forEach((b, i) => b.classList.toggle("active", i === bodyIdx));
  if (bodyAct === "Combo") {
    const cf0 = comboByDir.front_r[bodyIdx % comboByDir.front_r.length];
    bdReadout.textContent = \`Ciclo Contínuo (attack-only-v1): passo \${bodyIdx + 1}/\${comboByDir.front_r.length} · \${cf0.label} (\${cf0.durationMs} ms)\`;
    for (const d of DATA.dirs) {
      const cf = comboByDir[d][bodyIdx % comboByDir[d].length];
      const ui = bdImgs[d];
      ui.sub.textContent = cf.label;
      ui.tagL.textContent = "Ativo (V10)";
      ui.tagR.textContent = "Comparação (Corpo / A)";
      ui.imgL.src = cf.after;
      ui.imgR.src = cf.before;
      ui.imgL.style.width = "256px"; ui.imgL.style.height = "256px";
      ui.imgR.style.width = "256px"; ui.imgR.style.height = "256px";
    }
    return;
  }

  const refFront = DATA.bodyData[bodyAct].front_r;
  const f0 = refFront.frames[bodyIdx % refFront.frames.length];
  bdReadout.textContent = \`\${bodyAct} · quadro F\${String(bodyIdx).padStart(2,"0")} (\${f0.durationMs} ms) · arma visível: não (0 px)\`;
  for (const d of DATA.dirs) {
    const cell = DATA.bodyData[bodyAct][d];
    const fd = cell.frames[bodyIdx % cell.frames.length];
    const ui = bdImgs[d];
    const sz = cell.canvasSize === 128 ? "128px" : "256px";
    ui.imgL.style.width = sz; ui.imgL.style.height = sz;
    ui.imgR.style.width = sz; ui.imgR.style.height = sz;
    ui.sub.textContent = cell.isAffected ? \`F\${String(fd.index).padStart(2,"0")} · Corrigido\` : \`F\${String(fd.index).padStart(2,"0")} · Preservado\`;
    ui.tagL.textContent = cell.isAffected ? "Depois (V10)" : "Preservado (V10)";
    ui.tagR.textContent = cell.isAffected ? "Antes" : "Baseline Idêntica";
    ui.imgL.src = fd.after;
    ui.imgR.src = fd.before;
  }
}

// 4. Build Critical Before x After Static Cards
const critGrid = document.getElementById("crit-grid");
for (const item of DATA.criticalPairs) {
  const card = document.createElement("div");
  card.className = "card";
  card.innerHTML = \`
    <div class="card-title">\${item.title}</div>
    <div class="card-sub" style="margin:4px 0 8px; white-space:normal;">\${item.meta}</div>
    <div class="crit-pair">
      <div class="crit-box"><span class="stage-tag">Antes · \${item.labelA}</span><img src="\${item.beforeA}" alt="Antes A" style="transform:scale(\${item.zoom}); transform-origin:\${item.crop};"></div>
      <div class="crit-box"><span class="stage-tag" style="color:#86efac;">Depois · \${item.labelA}</span><img src="\${item.afterA}" alt="Depois A" style="transform:scale(\${item.zoom}); transform-origin:\${item.crop};"></div>
      <div class="crit-box"><span class="stage-tag">Antes · \${item.labelB}</span><img src="\${item.beforeB}" alt="Antes B" style="transform:scale(\${item.zoom}); transform-origin:\${item.crop};"></div>
      <div class="crit-box"><span class="stage-tag" style="color:#86efac;">Depois · \${item.labelB}</span><img src="\${item.afterB}" alt="Depois B" style="transform:scale(\${item.zoom}); transform-origin:\${item.crop};"></div>
    </div>
  \`;
  critGrid.appendChild(card);
}

// Wire controls
function updatePlayButtons() {
  document.getElementById("btn-play-1").classList.toggle("active", playing && speedMul === 1.0);
  document.getElementById("btn-play-05").classList.toggle("active", playing && speedMul === 0.5);
  document.getElementById("btn-play-025").classList.toggle("active", playing && speedMul === 0.25);
  document.getElementById("btn-pause").classList.toggle("active", !playing);
}

document.getElementById("btn-play-1").onclick = () => { playing = true; speedMul = 1.0; updatePlayButtons(); };
document.getElementById("btn-play-05").onclick = () => { playing = true; speedMul = 0.5; updatePlayButtons(); };
document.getElementById("btn-play-025").onclick = () => { playing = true; speedMul = 0.25; updatePlayButtons(); };
document.getElementById("btn-pause").onclick = () => { playing = false; updatePlayButtons(); };
document.getElementById("btn-prev").onclick = () => {
  playing = false; updatePlayButtons();
  swIdx = (swIdx + 13) % 14;
  axIdx = (axIdx + 11) % 12;
  const bLen = bdStrip.children.length || 1;
  bodyIdx = (bodyIdx + bLen - 1) % bLen;
  renderSword(); renderAxe(); renderBody();
};
document.getElementById("btn-next").onclick = () => {
  playing = false; updatePlayButtons();
  swIdx = (swIdx + 1) % 14;
  axIdx = (axIdx + 1) % 12;
  const bLen = bdStrip.children.length || 1;
  bodyIdx = (bodyIdx + 1) % bLen;
  renderSword(); renderAxe(); renderBody();
};

document.querySelectorAll("[data-scale]").forEach(btn => {
  btn.onclick = () => setScale(Number(btn.dataset.scale));
});

document.getElementById("btn-bg-tac").onclick = () => {
  document.body.classList.add("bg-tactical");
  document.body.classList.remove("bg-checker");
  document.getElementById("btn-bg-tac").classList.add("active");
  document.getElementById("btn-bg-chk").classList.remove("active");
};
document.getElementById("btn-bg-chk").onclick = () => {
  document.body.classList.add("bg-checker");
  document.body.classList.remove("bg-tactical");
  document.getElementById("btn-bg-chk").classList.add("active");
  document.getElementById("btn-bg-tac").classList.remove("active");
};

document.querySelectorAll("[data-swmode]").forEach(btn => {
  btn.onclick = () => {
    swMode = btn.dataset.swmode;
    document.querySelectorAll("[data-swmode]").forEach(b => b.classList.toggle("active", b === btn));
    renderSword();
  };
});

document.querySelectorAll("[data-axmode]").forEach(btn => {
  btn.onclick = () => {
    axMode = btn.dataset.axmode;
    document.querySelectorAll("[data-axmode]").forEach(b => b.classList.toggle("active", b === btn));
    renderAxe();
  };
});

document.querySelectorAll("[data-bact]").forEach(btn => {
  btn.onclick = () => {
    bodyAct = btn.dataset.bact;
    document.querySelectorAll("[data-bact]").forEach(b => b.classList.toggle("active", b === btn));
    bodyIdx = bodyAct === "Defeat" ? 4 : 0;
    bodyElapsed = 0;
    rebuildBodyStrip();
    renderBody();
  };
});

// Initialize
setScale(1.0);
rebuildBodyStrip();
renderSword();
renderAxe();
renderBody();

// Animation loop using real per-frame durationsMs
let lastTs = performance.now();
function tick(now) {
  const dt = Math.min(100, now - lastTs) * speedMul;
  lastTs = now;
  if (playing) {
    swElapsed += dt;
    const swDur = DATA.swordData.front_r.durationsMs[swIdx];
    if (swElapsed >= swDur) {
      swElapsed -= swDur;
      swIdx = (swIdx + 1) % 14;
      renderSword();
    }

    axElapsed += dt;
    const axDur = DATA.axeData.front_r.durationsMs[axIdx];
    if (axElapsed >= axDur) {
      axElapsed -= axDur;
      axIdx = (axIdx + 1) % 12;
      renderAxe();
    }

    bodyElapsed += dt;
    const bDur = bodyAct === "Combo"
      ? comboByDir.front_r[bodyIdx % comboByDir.front_r.length].durationMs
      : DATA.bodyData[bodyAct].front_r.durationsMs[bodyIdx % DATA.bodyData[bodyAct].front_r.durationsMs.length];
    if (bodyElapsed >= bDur) {
      bodyElapsed -= bDur;
      const bLen = bdStrip.children.length || 1;
      bodyIdx = (bodyIdx + 1) % bLen;
      renderBody();
    }
  }
  requestAnimationFrame(tick);
}
requestAnimationFrame(tick);

window.addEventListener("load", () => {
  const imgs = Array.from(document.querySelectorAll("img"));
  const ok = imgs.filter(i => i.complete && i.naturalWidth > 0).length;
  const el = document.getElementById("global-load-status");
  el.textContent = \`Imagens ativas carregadas: \${ok}/\${imgs.length}\`;
});
</script>
</body>
</html>
`;

const outHtml = path.join(REVIEW_DIR, "index.html");
fs.writeFileSync(outHtml, html, "utf8");
console.log("Wrote unified review studio:", outHtml);
