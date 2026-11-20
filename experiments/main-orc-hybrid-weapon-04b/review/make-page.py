"""Builds the Pilot B1 (front_r) review page.

Self-contained and file://-safe: frames are plain <img> elements scaled with CSS,
so no canvas taint and no network access. Nothing here edits art.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent

SRC = ROOT / "characters/orc-v1/source/combat-recovery-v8/frontal-inbetween/front_r-sword/clip.json"
src = json.loads(SRC.read_text(encoding="utf-8"))
durations = [round(f["durationMs"]) for f in src["frames"]]
phases = [f.get("phase", "") for f in src["frames"]]
contact = src.get("contactEvent", {})

DATA = {"durations": durations, "phases": phases, "contact": contact}

EXP = OUT.parent
ver = json.loads((EXP / "verification.json").read_text(encoding="utf-8"))
stats = json.loads((EXP / "blade-repaint-stats.json").read_text(encoding="utf-8"))
wc = ver["weaponComparison"]
rows = ver["bodyHandReuse"]["rows"]
body_identical = all(r["aEqualsSource"] and r["bEqualsSource"] and r["aEqualsB"] for r in rows)
guard_changed = sum(w["guardRegionChangedPixels"] for w in wc)
silhouette = sum(w["silhouetteChangedPixels"] for w in wc)
leftover = sum(w["leftoverOriginalBladePixels"] for w in wc)
blade_px = sum(s["bladePixels"] for s in stats)
colour_changed = sum(s["colourChanged"] for s in stats)
timing_ok = ver["timing"]["preserved"]
assets_reused = all(ver["assetReuse"].values())
ok = lambda b: '<td class="ok">sim</td>' if b else '<td class="bad">não</td>'

SUMMARY = "\n".join([
    "<tr><td>Corpo e mão byte-idênticos à fonte do <code>front_r</code></td>"
    "<td>{}/{}</td></tr>".format(sum(1 for r in rows if r["aEqualsSource"] and r["bEqualsSource"]), len(rows)),
    "<tr><td>Variante A idêntica ao original (nenhum pixel de arma alterado)</td>"
    + ok(all(w["variantAVsSourcePixels"] == 0 for w in wc)) + "</tr>",
    "<tr><td>Silhueta da arma alterada pela Variante B</td><td>{} pixels</td></tr>".format(silhouette),
    "<tr><td>Pixels da guarda/cabo repintados</td><td>{}</td></tr>".format(guard_changed),
    "<tr><td>Pixels da lâmina antiga sobreviventes</td><td>{}</td></tr>".format(leftover),
    "<tr><td>Pixels de lâmina repintados (10 quadros com arma)</td><td>{}, dos quais {} mudam de cor</td></tr>".format(blade_px, colour_changed),
    "<tr><td>Tempos preservados ({} quadros, {} ms)</td>".format(len(durations), sum(durations)) + ok(timing_ok) + "</tr>",
    "<tr><td>Mesmos dois assets de espada do Experimento 04, byte a byte</td>" + ok(assets_reused) + "</tr>",
])

PAGE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>Piloto B1 — Arquitetura C em front_r</title>
<style>
  :root { color-scheme: dark; }
  * { box-sizing: border-box; }
  body { margin:0; padding:24px 28px 64px; background:#14151a; color:#e7e8ec;
         font:15px/1.55 "Segoe UI",system-ui,sans-serif; }
  h1 { font-size:22px; margin:0 0 4px; }
  h2 { font-size:16px; margin:28px 0 10px; padding-bottom:6px; border-bottom:1px solid #2a2c34; }
  p.lead { color:#a2a5b0; margin:0 0 10px; max-width:96ch; }
  .badge { display:inline-block; padding:2px 9px; border-radius:4px; font-size:12px; font-weight:600; }
  .warn { background:#3a2f18; color:#e3bd74; }
  .ok { background:#1d3324; color:#8fc99a; }
  .bad { background:#3a1d1d; color:#e08d8d; }
  .bar { display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin:12px 0; }
  button { background:#2a2c34; color:#e7e8ec; border:1px solid #3a3d47; border-radius:5px;
           padding:6px 12px; font-size:14px; cursor:pointer; }
  button:hover { background:#343742; }
  button.active { background:#2b64d4; border-color:#2b64d4; color:#fff; }
  .grid { display:grid; grid-template-columns:repeat(4, 1fr); gap:12px; }
  .cell { background:#1b1d23; border:1px solid #2a2c34; border-radius:6px; padding:8px; }
  .cell h3 { font-size:12px; margin:0 0 8px; color:#a2a5b0; text-transform:uppercase; letter-spacing:.04em; }
  .frame { position:relative; overflow:hidden; aspect-ratio:1; display:flex; align-items:center;
           justify-content:center; border-radius:4px;
           background:repeating-conic-gradient(#20222a 0% 25%, #191b21 0% 50%) 50% / 16px 16px; }
  .frame img { width:100%; height:100%; object-fit:contain; image-rendering:pixelated;
               transform-origin:center; transition:transform .12s ease-out; }
  .hands { display:grid; grid-template-columns:repeat(2, 1fr); gap:12px; }
  .hands figure { margin:0; }
  .hands .clipbox { overflow:hidden; aspect-ratio:1; border:1px solid #2a2c34; border-radius:4px;
      background:repeating-conic-gradient(#20222a 0% 25%, #191b21 0% 50%) 50% / 16px 16px; }
  .hands img { width:100%; image-rendering:pixelated; }
  .hands figcaption { color:#8b8f9a; font-size:12px; margin-top:5px; }
  .note { border-left:3px solid #b8862f; background:#1c1a15; padding:10px 14px; margin:14px 0; }
  table { border-collapse:collapse; font-size:13px; margin:10px 0; }
  th,td { border:1px solid #2a2c34; padding:4px 9px; text-align:left; }
  th { background:#1f2128; }
  #status { color:#8fc99a; }
</style>
</head>
<body>

<h1>Piloto B1 — Arquitetura C na segunda perspectiva (<code>front_r</code>)</h1>
<p class="lead">Orc principal, ataque de Espada, direção <code>front_r</code>. A pergunta desta rodada:
a mesma arquitetura de duas espadas sobre um corpo funciona numa direção diferente <em>sem
reconstruir anatomia</em>? <span class="badge warn">VISUAL_REVIEW_REQUIRED · PENDING_CREATOR</span></p>

<div class="note">
  <strong>Leia antes de julgar.</strong> O corpo é literalmente o mesmo nas duas variantes —
  <code>body</code> e <code>handFront</code> são byte-idênticos à fonte do <code>front_r</code>
  (28/28 comparações). Só a <em>arte da arma</em> muda. A única adaptação de composição foi o
  pivô de pegada, que o <code>front_r</code> não declara: foi medido na própria arte, não estimado.
  Defeitos herdados <strong>não foram corrigidos</strong> de propósito.
</div>

<div class="bar" id="frames"></div>

<div class="bar">
  <button id="play">▶ 1×</button>
  <button id="play-half">▶ 0,5×</button>
  <button id="pause">⏸ pausar</button>
  <button id="prev">◀ quadro</button>
  <button id="next">quadro ▶</button>
  <span style="width:14px"></span>
  <span style="color:#8b8f9a">Zoom</span>
  <button data-zoom="1" class="active">1×</button>
  <button data-zoom="2">2×</button>
  <button data-zoom="4">4×</button>
</div>

<p class="lead" id="status">carregando…</p>

<div class="grid" id="views"></div>

<h2>Mão e punho ampliados</h2>
<p class="lead">É aqui que a pegada se julga. Nas duas variantes a luva, o cabo e a oclusão têm de ser
os mesmos; só a lâmina muda.</p>
<div class="hands" id="hands"></div>

<h2>Reutilização e diagnóstico — herdado versus introduzido</h2>
<table>
  <tr><th>Verificação</th><th>Resultado</th></tr>
  __SUMMARY__
</table>

<h2>Defeitos herdados (não corrigidos nesta rodada)</h2>
<p class="lead">Estes vêm da animação original do <code>front_r</code> e continuam iguais em A e B,
porque a composição não toca no corpo:</p>
<ul class="lead">
  <li><strong>Região da axila:</strong> o <code>front_l</code> recebeu um reparo de axila
      (<code>frontal-armpit</code>) que o <code>front_r</code> <em>nunca recebeu</em> — o
      <code>clip.json</code> desta direção não tem os campos de reparo.</li>
  <li><strong>Oclusão densa da mão</strong> contra o tronco no quadro de contato.</li>
  <li><strong>Coreografia original</strong>, com a mesma cadência de 730 ms.</li>
</ul>
<p class="lead">Nada nesta lista foi introduzido pela composição: <code>body</code> e
<code>handFront</code> são byte-idênticos à fonte nas duas variantes.</p>

<script>
const DATA = __DATA__;
const VARIANTS = [
  { prefix: "", label: "1 · Original recuperado", base: "../../../characters/orc-v1/source/combat-recovery-v8/frontal-inbetween/front_r-sword/frames/" },
  { prefix: "F", label: "2 · Variante A — Espada do Recruta", base: "../full/a/composite/" },
  { prefix: "F", label: "3 · Variante B — aço claro", base: "../full/b/composite/" },
  { prefix: "F", label: "4 · Somente corpo (sem arma)", base: "../full/a/body-only/" }
];
let current = 0;
let zoom = 1;
let timer = null;

const views = [];
const hands = [];

function buildFrames() {
  const bar = document.getElementById("frames");
  DATA.durations.forEach((d, i) => {
    const b = document.createElement("button");
    b.textContent = "F" + String(i).padStart(2, "0");
    b.dataset.i = i;
    b.onclick = () => { stop(); current = i; render(); };
    bar.appendChild(b);
  });
}

function buildViews() {
  const box = document.getElementById("views");
  VARIANTS.forEach(v => {
    const cell = document.createElement("div");
    cell.className = "cell";
    const h = document.createElement("h3");
    h.textContent = v.label;
    const frame = document.createElement("div");
    frame.className = "frame";
    const img = document.createElement("img");
    img.alt = v.label;
    frame.appendChild(img);
    cell.append(h, frame);
    box.appendChild(cell);
    views.push(img);
  });
}

function buildHands() {
  const box = document.getElementById("hands");
  ["a", "b"].forEach(key => {
    const fig = document.createElement("figure");
    const clipbox = document.createElement("div");
    clipbox.className = "clipbox";
    const img = document.createElement("img");
    img.alt = "mão " + key;
    clipbox.appendChild(img);
    const cap = document.createElement("figcaption");
    fig.append(clipbox, cap);
    box.appendChild(fig);
    hands.push({ img, cap, key });
  });
}

function setSrc(img, src) {
  img.onerror = () => { img.alt = "ausente: " + src; };
  if (img.getAttribute("src") !== src) img.setAttribute("src", src);
}

function render() {
  document.querySelectorAll("#frames button").forEach(b =>
    b.classList.toggle("active", Number(b.dataset.i) === current));

  const nn = String(current).padStart(2, "0");
  VARIANTS.forEach((v, i) => setSrc(views[i], v.base + (v.prefix || "") + nn + ".png"));
  hands.forEach(h => {
    setSrc(h.img, "hands/" + h.key + "/" + nn + ".png");
    h.cap.textContent = (h.key === "a" ? "Variante A" : "Variante B") +
      " · F" + nn + " · mão e punho ampliados";
  });

  const phase = DATA.phases[current] || "";
  const isContact = DATA.contact && DATA.contact.frame === current;
  document.getElementById("status").textContent =
    "Quadro " + (current + 1) + "/" + DATA.durations.length + " · F" + nn +
    " · fase " + phase + " · " + DATA.durations[current] + " ms" +
    (isContact ? " · CONTATO (" + DATA.contact.timeMs + " ms)" : "");
}

function step(delta) {
  current = (current + delta + DATA.durations.length) % DATA.durations.length;
  render();
}

function stop() { if (timer) { clearTimeout(timer); timer = null; } }

function play(mult) {
  stop();
  const tick = () => {
    render();
    const wait = Math.max(25, DATA.durations[current] / mult);
    timer = setTimeout(() => { step(1); tick(); }, wait);
  };
  step(1);
  tick();
}

document.getElementById("play").onclick = () => play(1);
document.getElementById("play-half").onclick = () => play(0.5);
document.getElementById("pause").onclick = stop;
document.getElementById("prev").onclick = () => { stop(); step(-1); };
document.getElementById("next").onclick = () => { stop(); step(1); };

document.querySelectorAll("[data-zoom]").forEach(b => {
  b.onclick = () => {
    zoom = Number(b.dataset.zoom);
    document.querySelectorAll("[data-zoom]").forEach(x => x.classList.toggle("active", x === b));
    views.forEach(img => { img.style.transform = "scale(" + zoom + ")"; });
  };
});

buildFrames();
buildViews();
buildHands();
render();
</script>
</body>
</html>
"""

out = OUT / "index.html"
out.write_text(
    PAGE.replace("__DATA__", json.dumps(DATA, ensure_ascii=False)).replace("__SUMMARY__", SUMMARY),
    encoding="utf-8",
)
print(f"{out} ({out.stat().st_size/1024:.1f} KB)")
