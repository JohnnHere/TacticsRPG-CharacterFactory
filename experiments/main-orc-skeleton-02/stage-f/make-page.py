"""Generates the Stage F review page with the pose data embedded.

The page must open by file:// without a server, so the joint data is inlined
instead of fetched. Nothing here edits art; it only renders existing artefacts.
"""
import json
from pathlib import Path

EXP = Path(__file__).resolve().parent
ROOT = EXP.parents[1]
SRC = EXP.parent / "stage-bcde"
POSES = json.loads((EXP.parent / ".." / "main-orc-skeleton-first-01" / "poses-fixed.json").read_text(encoding="utf-8"))

LABELS = {"00": "Preparação", "05": "Elevação / antecipação", "08": "Golpe principal",
          "09": "Seguimento", "13": "Recuperação"}
PHASES = {"00": "rest", "05": "apex-hold", "08": "contact", "09": "follow-through", "13": "return-to-guard"}
ORDER = ["00", "05", "08", "09", "13"]

# Map the five structural poses onto the key poses designed in Experiment 01.
JOINTS = {p["id"]: [{"label": j["label"], "x": j["x"], "y": j["y"]} for j in p["joints"]] for p in POSES["poses"]}
MAPPING = {"00": "ready", "05": "raise", "08": "strike", "09": "follow", "13": "recover"}
GRIP = {p["id"]: p.get("grip") for p in POSES["poses"]}

BONES = [["NECK", "RIGHT SHOULDER"], ["RIGHT SHOULDER", "RIGHT ELBOW"], ["RIGHT ELBOW", "RIGHT ARM"],
         ["NECK", "LEFT SHOULDER"], ["LEFT SHOULDER", "LEFT ELBOW"], ["LEFT ELBOW", "LEFT ARM"],
         ["NECK", "RIGHT HIP"], ["RIGHT HIP", "RIGHT KNEE"], ["RIGHT KNEE", "RIGHT LEG"],
         ["NECK", "LEFT HIP"], ["LEFT HIP", "LEFT KNEE"], ["LEFT KNEE", "LEFT LEG"],
         ["RIGHT HIP", "LEFT HIP"], ["RIGHT SHOULDER", "LEFT SHOULDER"]]

data = {
    "labels": LABELS, "phases": PHASES, "order": ORDER, "mapping": MAPPING,
    "joints": JOINTS, "grip": GRIP, "bones": BONES,
}

HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>Experimento 02 — corpo, espada independente e pegada</title>
<style>
  :root { color-scheme: dark; }
  * { box-sizing: border-box; }
  body { margin:0; padding:26px 30px 60px; background:#14151a; color:#e7e8ec;
         font:15px/1.55 "Segoe UI",system-ui,sans-serif; }
  h1 { font-size:22px; margin:0 0 4px; }
  h2 { font-size:16px; margin:30px 0 10px; padding-bottom:6px; border-bottom:1px solid #2a2c34; }
  p.lead { color:#a2a5b0; margin:0 0 10px; max-width:96ch; }
  .status { display:inline-block; padding:2px 9px; border-radius:4px; font-size:12px; font-weight:600; }
  .warn { background:#3a2f18; color:#e3bd74; }
  .ok { background:#1d3324; color:#8fc99a; }
  .bar { display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin:14px 0; }
  button { background:#2a2c34; color:#e7e8ec; border:1px solid #3a3d47; border-radius:5px;
           padding:7px 13px; font-size:14px; cursor:pointer; }
  button:hover { background:#343742; }
  button.active { background:#2b64d4; border-color:#2b64d4; color:#fff; }
  .views { display:grid; grid-template-columns:repeat(4, 1fr); gap:14px; }
  .view { background:#1b1d23; border:1px solid #2a2c34; border-radius:6px; padding:8px; }
  .view h3 { font-size:13px; margin:0 0 8px; color:#a2a5b0; font-weight:600; text-transform:uppercase; letter-spacing:.04em; }
  .frame { position:relative; overflow:hidden; contain:paint; background:
      repeating-conic-gradient(#20222a 0% 25%, #191b21 0% 50%) 50% / 16px 16px;
      border-radius:4px; overflow:hidden; aspect-ratio:1; display:flex; align-items:center; justify-content:center; }
  .frame img { image-rendering:pixelated; width:100%; height:100%; object-fit:contain; transform-origin:center; transition:transform .12s ease-out; }
  .frame svg { position:absolute; inset:0; width:100%; height:100%; pointer-events:none; }
  .zoombox { background:#1b1d23; border:1px solid #2a2c34; border-radius:6px; overflow:auto; max-height:460px; padding:10px; }\n  .zoombox img { image-rendering:pixelated; display:block; }\n  .hands { display:grid; grid-template-columns:repeat(3, 1fr); gap:14px; margin-top:12px; }
  .hands figure { margin:0; }
  .hands img { width:100%; image-rendering:pixelated; border:1px solid #2a2c34; border-radius:4px;
               background:repeating-conic-gradient(#20222a 0% 25%, #191b21 0% 50%) 50% / 16px 16px; }
  .hands figcaption { color:#8b8f9a; font-size:12px; margin-top:5px; }
  .strip { display:flex; gap:6px; overflow-x:auto; padding-bottom:8px; }
  .strip figure { margin:0; flex:0 0 auto; }
  .strip img { width:104px; image-rendering:pixelated; border:1px solid #2a2c34; border-radius:4px;
               background:repeating-conic-gradient(#20222a 0% 25%, #191b21 0% 50%) 50% / 12px 12px; }
  .strip figcaption { font-size:11px; color:#8b8f9a; text-align:center; }
  .note { border-left:3px solid #b8862f; background:#1c1a15; padding:10px 14px; margin:16px 0; }
  .missing { color:#e08a7a; }
  table { border-collapse:collapse; font-size:13px; margin:10px 0; }
  th,td { border:1px solid #2a2c34; padding:4px 9px; text-align:left; }
  th { background:#1f2128; }
</style>
</head>
<body>

<h1>Experimento 02 — corpo, espada independente e pegada</h1>
<p class="lead">Orc principal, ataque de Espada, direção <code>back_l</code> apenas. Cinco poses
estruturais comparadas em quatro vistas. <span class="status warn">VISUAL_REVIEW_REQUIRED · PENDING_CREATOR</span></p>

<div class="note">
  <strong>Isto não é uma animação validada.</strong> São cinco marcos estruturais, não um clipe.
  Não há reprodução em velocidade de jogo porque as poses intermediárias não foram produzidas.
  00 e 13 estão desarmados no clipe de produção; aqui receberam montagem armada apenas para
  diagnóstico da ligação, o que <em>não</em> propõe arma em repouso.
</div>

<div class="bar" id="poses"></div>

<div class="bar">
  <span style="color:#8b8f9a">Zoom</span>
  <button data-zoom="2" class="active">2×</button>
    <button data-zoom="4">4×</button>
    <button data-zoom="8">8×</button>
  <span style="width:18px"></span>
  <button id="toggle-skeleton" class="active">Esqueleto ligado</button>
</div>

<div class="views">
  <div class="view"><h3>1 · Esqueleto / guia</h3><div class="frame" id="v-skeleton"><img id="i-skeleton" alt="guia de esqueleto"><svg id="svg" viewBox="0 0 256 256" preserveAspectRatio="xMidYMid meet"></svg></div></div>
  <div class="view"><h3>2 · Somente corpo</h3><div class="frame"><img id="i-body" alt="somente corpo"></div></div>
  <div class="view"><h3>3 · Somente arma</h3><div class="frame"><img id="i-weapon" alt="somente arma"></div></div>
  <div class="view"><h3>4 · Composição final</h3><div class="frame"><img id="i-composite" alt="composição final"></div></div>
</div>

<h2>Inspeção detalhada</h2>
<p class="lead">Composição final em pixel puro, com rolagem própria, para examinar ombro, cotovelo,
punho, luva e a conexão do cabo sem perder resolução.</p>
<div class="zoombox"><img id="i-zoom" alt="composição em zoom"></div>

<h2>Mão e punho em 8×</h2>
<p class="lead">É aqui que a pegada se julga. Um cabo que atravessa uma palma aberta está alinhado e
errado ao mesmo tempo; o que importa é a luva fechar no cabo.</p>
<div class="hands" id="hands"></div>

<h2>De onde viemos</h2>
<p class="lead">Quadros do clipe de produção atual, para comparação direta.</p>
<div class="strip" id="strip"></div>

<h2>O que foi verificado nas imagens</h2>
<table>
  <tr><th>Verificação</th><th>Resultado</th></tr>
  <tr><td>Pixels com alfa parcial (contaminação de máscara)</td><td class="ok">0 nas 15 imagens</td></tr>
  <tr><td>Pixels claros neutros (halo branco)</td><td class="ok">0 nas 15 imagens</td></tr>
  <tr><td>Pixels opacos da arma, todas as poses</td><td class="ok">706 idêntico — rotação não erodiu a silhueta</td></tr>
  <tr><td>Corpo comparado à camada de origem</td><td class="ok">RGBA idêntico</td></tr>
</table>

<script>
const DATA = __DATA__;
const BASE = "../stage-bcde";
const PROD = "../../../characters/orc-v1/source/combat-recovery-v8/rear-arc/back_l-sword/frames/";
let current = "00";
let zoom = 2;
let skeletonOn = true;
let boneClicks = {};

function markBroken(img, path) {
  img.addEventListener("error", () => {
    img.replaceWith(Object.assign(document.createElement("span"),
      { className: "missing", textContent: "ausente: " + path }));
  });
}

function buildPoseBar() {
  const bar = document.getElementById("poses");
  DATA.order.forEach(id => {
    const b = document.createElement("button");
    b.textContent = id + " · " + DATA.labels[id];
    b.dataset.pose = id;
    if (id === current) b.classList.add("active");
    b.onclick = () => { current = id; render(); };
    bar.appendChild(b);
  });
}

function drawSkeleton(id) {
  const svg = document.getElementById("svg");
  const pose = DATA.mapping[id];
  const joints = DATA.joints[pose] || [];
  const map = Object.fromEntries(joints.map(j => [j.label.toUpperCase(), j]));
  let out = "";
  for (const [a, b] of DATA.bones) {
    const ja = map[a], jb = map[b];
    if (ja && jb) out += `<line x1="${ja.x*256}" y1="${ja.y*256}" x2="${jb.x*256}" y2="${jb.y*256}" stroke="#f0c45a" stroke-width="1.4"/>`;
  }
  for (const j of joints) {
    const right = j.label.toUpperCase().startsWith("RIGHT");
    out += `<circle cx="${j.x*256}" cy="${j.y*256}" r="1.9" fill="${right ? "#ff6060" : "#60beff"}"/>`;
  }
  svg.innerHTML = out;
}

function render() {
  document.querySelectorAll("#poses button").forEach(b =>
    b.classList.toggle("active", b.dataset.pose === current));

  const set = (imgId, path) => {
    const img = document.getElementById(imgId);
    const clone = img.cloneNode();
    clone.src = path;
    clone.alt = path;
    markBroken(clone, path);
    img.replaceWith(clone);
  };
  set("i-skeleton", `${BASE}/composite/${current}.png`);
  set("i-body", `${BASE}/body-only/${current}.png`);
  set("i-weapon", `${BASE}/weapon-only/${current}.png`);
  set("i-composite", `${BASE}/composite/${current}.png`);
  set("i-zoom", `${BASE}/composite/${current}.png`);

  const zoomImg = document.getElementById("i-zoom");
  zoomImg.style.width = (256 * zoom) + "px";
  zoomImg.style.height = (256 * zoom) + "px";
  const box = zoomImg.parentElement;
  requestAnimationFrame(() => {
    box.scrollLeft = Math.max(0, (zoomImg.clientWidth - box.clientWidth) / 2);
    box.scrollTop = Math.max(0, (zoomImg.clientHeight - box.clientHeight) / 2);
  });

  drawSkeleton(current);
  document.getElementById("svg").style.display = skeletonOn ? "block" : "none";

  const hands = document.getElementById("hands");
  hands.innerHTML = "";
  [["body-only", "corpo"], ["weapon-only", "arma"], ["composite", "composição"]].forEach(([sub, label]) => {
    const fig = document.createElement("figure");
    const img = document.createElement("img");
    const path = `${BASE}/evidence/${current}-${sub}-hand-wrist-8x.png`;
    img.src = path;
    markBroken(img, path);
    const cap = document.createElement("figcaption");
    cap.textContent = `Pose ${current} · ${label} · mão e punho em 8×`;
    fig.append(img, cap);
    hands.appendChild(fig);
  });
}

function buildStrip() {
  const strip = document.getElementById("strip");
  for (let i = 0; i <= 13; i += 1) {
    const id = String(i).padStart(2, "0");
    const fig = document.createElement("figure");
    const img = document.createElement("img");
    img.src = `${PROD}${id}.png`;
    markBroken(img, `${PROD}${id}.png`);
    const cap = document.createElement("figcaption");
    cap.textContent = "F" + id;
    fig.append(img, cap);
    strip.appendChild(fig);
  }
}

document.querySelectorAll("[data-zoom]").forEach(b => {
  b.onclick = () => {
    zoom = Number(b.dataset.zoom);
    document.querySelectorAll("[data-zoom]").forEach(x => x.classList.toggle("active", x === b));
    render();
  };
});
document.getElementById("toggle-skeleton").onclick = (e) => {
  skeletonOn = !skeletonOn;
  e.target.classList.toggle("active", skeletonOn);
  e.target.textContent = skeletonOn ? "Esqueleto ligado" : "Esqueleto desligado";
  render();
};

buildPoseBar();
buildStrip();
render();
</script>
</body>
</html>
"""

out = EXP / "index.html"
out.write_text(HTML.replace("__DATA__", json.dumps(data, ensure_ascii=False)), encoding="utf-8")
print(f"{out}  ({out.stat().st_size/1024:.1f} KB)")
