#!/usr/bin/env node
// Builds the review comparator for the targeted-repair pool.
// Access modes: works from file:// (all asset URLs are relative to this page) and from
// the local static server. The page reports its own asset load status on screen so the
// creator can verify loading without devtools.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const CAND = 'experiments/main-orc-targeted-repair-v1/artist-rear/candidate';
const OUT = `${CAND}/comparator.html`;
const PREFIX = path.relative(path.dirname(path.join(ROOT, OUT)), ROOT).split(path.sep).join('/');

const pairs = [
  {
    key: 'axe',
    title: 'back_r / Axe · micro-limpeza v1',
    verdict: 'HIPÓTESE NÃO INTEGRADA · NÃO PROMOVER',
    verdictClass: 'reject',
    note:
      'Os 11 pixels NÃO são correção artística provada. Medição sobre o freeze: os 8 px de y=191 são faixa pálida uniforme (122,123,125) logo abaixo do contorno ink (2,2,3) de y=190 — rebordo da sola 1 px abaixo do contorno, e o mesmo defeito sistêmico de rebordo pálido que este pool decidiu não tocar; ' +
      'os 2 px de (144,64)/(145,64) estão na primeira linha do recorte nativo sem vizinhos e podem ser fragmento de membro/arma cortado pelo recorte; o px de (171,151) está a 2 px de um aglomerado escuro real e pode ser fleco dele. ' +
      'Conectividade e limiar de cor não decidem intenção. Hipótese documentada para decisão do criador, não integrada.',
    base: 'characters/orc-v1/source/rear-recovery-v2/back_r/Axe/Attack-representative-v1',
    cand: `${CAND}/clip/back_r/Axe/Attack-representative-v1-microclean`,
    changedFrames: [1, 2, 6],
    pixels: 11,
  },
  {
    key: 'sword',
    title: 'back_r / Sword · expansão de handFront (rejeitada)',
    verdict: 'EXPERIMENTO REJEITADO · NÃO PROMOVER',
    verdictClass: 'reject',
    note:
      'Auditoria semântica: os 110 pixels restaurados escondem guarda (14) e pomo (50), não o punho. ' +
      'A máscara não corrige a pegada — o defeito é de posicionamento da arma. Mantido como evidência.',
    base: 'characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2',
    cand: `${CAND}/clip/back_r/Sword/Attack-representative-v2-occlusion-v1`,
    changedFrames: [1, 4, 5, 6],
    pixels: 110,
  },
];

const rel = (p) => `${PREFIX}/${p.split(path.sep).join('/')}`;
const payload = pairs.map((p) => {
  const baseClip = JSON.parse(fs.readFileSync(`${p.base}/clip.json`, 'utf8'));
  const candClip = JSON.parse(fs.readFileSync(`${p.cand}/clip.json`, 'utf8'));
  const fr = (clip, dir) =>
    clip.frames.map((f) => ({
      index: f.index,
      phase: f.phase,
      weaponVisible: f.weaponVisible,
      comp: rel(f.png),
      bodyOnly: rel(`${dir}/body-only/${String(f.index).padStart(2, '0')}.png`),
      handFront: rel(f.layers.handFront.png),
      native: rel(f.nativePng),
    }));
  return {
    ...p,
    durations: baseClip.durationsMs,
    total: baseClip.totalDurationMs,
    frameCount: baseClip.frameCount,
    baseFrames: fr(baseClip, p.base),
    candFrames: fr(candClip, p.cand),
    masterSha: candClip.masterSha256,
  };
});

const html = `<!doctype html>
<html lang="pt-BR"><meta charset="utf-8">
<title>Orc V1 · ataques traseiros · reparo local v1</title>
<style>
 :root{--bg:#14161b;--panel:#1c1f26;--line:#2c313b;--ink:#e8ebf0;--dim:#98a0ae;--accent:#7fb2ff;--warn:#ffb86b;--bad:#ff7a7a;--ok:#7ddc9b}
 *{box-sizing:border-box}
 body{margin:0;padding:18px;background:var(--bg);color:var(--ink);font:13px/1.5 system-ui,Segoe UI,sans-serif}
 h1{font-size:16px;margin:0 0 6px}
 .sub{color:var(--dim);margin:0 0 12px;max-width:1150px}
 .bar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:10px;margin-bottom:12px}
 button,select{font:inherit;background:#232833;color:var(--ink);border:1px solid var(--line);border-radius:6px;padding:5px 9px}
 button:hover{border-color:var(--accent)}
 button.primary{background:#2b3f60;border-color:#3d5c8c}
 .verdict{display:inline-block;padding:2px 8px;border-radius:999px;font-size:11px;border:1px solid var(--line);margin-left:6px}
 .verdict.open{color:var(--warn)}
 .verdict.reject{color:var(--bad)}
 .stage{display:grid;grid-template-columns:1fr 1fr;gap:12px}
 .col{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:10px}
 .col h2{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--dim);margin:0 0 8px;font-weight:600}
 .col.cand h2{color:var(--accent)}
 canvas{display:block;image-rendering:pixelated;background:repeating-conic-gradient(#191c22 0% 25%,#20242c 0% 50%) 50%/16px 16px;border:1px solid var(--line);border-radius:4px}
 .readout{margin-top:10px;background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:10px;font-variant-numeric:tabular-nums}
 .readout b{color:var(--accent);font-weight:600}
 .timeline{display:flex;gap:2px;margin-top:8px;height:22px}
 .seg{background:#2a3040;border-radius:3px;display:flex;align-items:center;justify-content:center;font-size:9px;color:#9aa4b6}
 .seg.on{background:#3d5c8c;color:#eaf1ff}
 .seg.changed{outline:1px solid var(--warn)}
 .legend{color:var(--dim);font-size:11px;margin-top:6px}
 .health{margin-top:12px;background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:10px;font-variant-numeric:tabular-nums}
 .health b{color:var(--ok)}
 .health .fail{color:var(--bad)}
 .diffwrap{margin-top:12px;background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:10px;display:none}
 .diffwrap.show{display:block}
 code{background:#232833;padding:1px 4px;border-radius:3px;font-size:11px}
</style>
<h1>Orc V1 · ataques traseiros · pool local <span class="verdict open" id="pairVerdict">—</span></h1>
<p class="sub">Reprodução com as durações reais do clipe (${pairs[0].key === 'axe' ? '8 quadros / 730 ms' : ''}), passo a quadro, escalas de jogo e camadas separadas.
Todos os recursos usam caminho <b>relativo a esta página</b>: abre por <code>file://</code> ou pelo servidor local
(<code>node experiments/main-orc-targeted-repair-v1/artist-rear/tools/serve.mjs</code> → <code>http://127.0.0.1:8791/…/comparator.html</code>).
O painel de saúde abaixo lista qualquer recurso que não carregou.</p>

<div class="bar">
  <label>par
    <select id="pair">${payload.map((p) => `<option value="${p.key}">${p.title}</option>`).join('')}</select>
  </label>
  <button id="play" class="primary">▶ tocar 1×</button>
  <button id="pause">⏸ pausar</button>
  <button id="prev">◀ quadro</button>
  <button id="next">quadro ▶</button>
  <button id="restart">↺ início</button>
  <label>velocidade
    <select id="speed"><option value="1">1×</option><option value="0.75">0.75×</option><option value="0.5">0.5×</option></select>
  </label>
  <label>escala
    <select id="scale"><option value="128">128 (nativo)</option><option value="256" selected>256</option><option value="384">384</option></select>
  </label>
  <label>camadas
    <select id="mode"><option value="comp">composição</option><option value="body">só corpo</option><option value="hand">só handFront</option></select>
  </label>
  <label><input type="checkbox" id="diff"> destacar pixels alterados</label>
</div>

<p class="sub" id="pairNote"></p>

<div class="stage">
  <div class="col"><h2 id="labA">freeze publicado</h2><canvas id="ca" width="256" height="256"></canvas></div>
  <div class="col cand"><h2 id="labB">candidato</h2><canvas id="cb" width="256" height="256"></canvas></div>
</div>

<div class="diffwrap" id="diffwrap"><h2 style="font-size:11px;color:var(--dim);margin:0 0 8px">diferença (amarelo = alterado)</h2><canvas id="cd" width="256" height="256"></canvas></div>

<div class="readout" id="readout"></div>
<div class="timeline" id="timeline"></div>
<div class="legend">clique num segmento para ir ao quadro; contorno amarelo = quadro com pixels alterados</div>
<div class="health" id="health">saúde dos recursos: carregando…</div>
<div class="health" id="selftest">autoteste: aguardando recursos…</div>

<script>
const PAIRS = ${JSON.stringify(payload)};
const state = { key: 'axe', frame: 0, elapsed: 0, playing: false, speed: 1, mode: 'comp', diff: false, raf: null, playStart: 0, playFrom: 0 };
const pair = () => PAIRS.find((p) => p.key === state.key);
const changedSet = () => new Set(pair().changedFrames);
const cache = new Map();
const started = [];
let repaintQueued = false;
let repaintCount = 0;
let selftestAt = 0;
function queueRepaint(){
  if(repaintQueued || repaintCount > 4000) return;
  repaintQueued = true;
  requestAnimationFrame(() => { repaintQueued = false; repaintCount += 1; selftestAt = 0; paint(); });
}
function img(src){
  if(!cache.has(src)){
    const i = new Image();
    i.__src = src; i.__ok = null;
    i.onload = () => { i.__ok = i.naturalWidth > 0; health(); queueRepaint(); };
    i.onerror = () => { i.__ok = false; health(); queueRepaint(); };
    i.src = src; cache.set(src, i); started.push(i);
  }
  return cache.get(src);
}
function srcFor(side, f){ if(state.mode === 'body') return f.bodyOnly; if(state.mode === 'hand') return f.handFront; return f.comp; }
function health(){
  const total = started.length;
  const bad = started.filter((i) => i.__ok === false);
  const pending = started.filter((i) => i.__ok === null);
  const el = document.getElementById('health');
  if(pending.length) el.innerHTML = 'saúde dos recursos: ' + total + ' pedidos · ' + (total - pending.length - bad.length) + ' ok · ' + pending.length + ' carregando' + (bad.length ? ' · <span class="fail">' + bad.length + ' falharam</span>' : '');
  else if(bad.length) el.innerHTML = '<span class="fail">saúde dos recursos: ' + bad.length + ' de ' + total + ' FALHARAM</span><br>' + bad.slice(0,6).map((i) => 'falhou: ' + i.__src.split('/').slice(-4).join('/')).join('<br>');
  else el.innerHTML = 'saúde dos recursos: <b>' + total + ' de ' + total + ' carregados</b> · nenhuma falha de caminho';
  window.__cmp.lastHealth = { total, ok: total - bad.length - pending.length, pending: pending.length, failed: bad.map((i) => i.__src) };
}
function failMark(ctx, src){
  ctx.fillStyle = 'rgba(120,20,20,0.55)'; ctx.fillRect(0,0,256,256);
  ctx.strokeStyle = '#ff7a7a'; ctx.lineWidth = 6; ctx.beginPath();
  ctx.moveTo(14,14); ctx.lineTo(242,242); ctx.moveTo(242,14); ctx.lineTo(14,242); ctx.stroke();
  ctx.fillStyle = '#ffe0e0'; ctx.font = 'bold 14px system-ui';
  ctx.fillText('FALHOU: recurso nao carregou', 18, 122);
  ctx.font = '12px system-ui'; ctx.fillText(String(src).split('/').slice(-3).join('/'), 18, 142);
}
function drawSide(id, frames){
  const cv = document.getElementById(id); const ctx = cv.getContext('2d');
  const scale = Number(document.getElementById('scale').value);
  cv.style.width = scale + 'px'; cv.style.height = scale + 'px';
  ctx.clearRect(0,0,256,256);
  const f = frames[state.frame]; if(!f) return;
  const src = srcFor(state.key, f);
  const im = img(src);
  if(im.__ok) ctx.drawImage(im, 0, 0, im.naturalWidth, im.naturalHeight, 0, 0, 256, 256);
  else if(im.__ok === false) failMark(ctx, src);
}
function drawDiff(){
  const on = state.diff; document.getElementById('diffwrap').classList.toggle('show', on);
  if(!on) return;
  const p = pair(); const a = img(p.baseFrames[state.frame].comp); const b = img(p.candFrames[state.frame].comp);
  const cv = document.getElementById('cd'); const ctx = cv.getContext('2d');
  const scale = Number(document.getElementById('scale').value);
  cv.style.width = scale + 'px'; cv.style.height = scale + 'px';
  ctx.clearRect(0,0,256,256);
  if(!(a.__ok && b.__ok)){ if(a.__ok === false || b.__ok === false) failMark(ctx, 'composicao do par'); return; }
  const off = document.createElement('canvas'); off.width = 256; off.height = 256;
  const o = off.getContext('2d');
  let da, db;
  try {
    o.drawImage(a,0,0,256,256); da = o.getImageData(0,0,256,256).data;
    o.clearRect(0,0,256,256); o.drawImage(b,0,0,256,256); db = o.getImageData(0,0,256,256).data;
  } catch(err) {
    state.diffUnavailable = String((err && err.name) || err);
    ctx.fillStyle = '#0e1016'; ctx.fillRect(0,0,256,256);
    ctx.fillStyle = '#ffb86b'; ctx.font = 'bold 13px system-ui';
    ctx.fillText('modo diff indisponivel neste acesso', 14, 116);
    ctx.fillStyle = '#98a0ae'; ctx.font = '12px system-ui';
    ctx.fillText('leitura de pixels bloqueada (canvas restrito)', 14, 136);
    ctx.fillText('use o servidor local para comparar pixels', 14, 156);
    ctx.fillText(String(state.diffUnavailable), 14, 176);
    return;
  }
  state.diffUnavailable = null;
  const out = ctx.createImageData(256,256);
  for(let i=0;i<da.length;i+=4){
    const d = da[i]!==db[i]||da[i+1]!==db[i+1]||da[i+2]!==db[i+2]||da[i+3]!==db[i+3];
    out.data[i] = d?255:db[i]*0.3; out.data[i+1] = d?176:db[i+1]*0.3; out.data[i+2] = d?64:db[i+2]*0.3; out.data[i+3] = d?255:Math.max(50,db[i+3]*0.3);
  }
  ctx.putImageData(out,0,0);
}
function opaqueCount(id){
  const cv = document.getElementById(id); const ctx = cv.getContext('2d');
  try {
    const d = ctx.getImageData(0,0,cv.width,cv.height).data;
    let n = 0; for(let i = 3; i < d.length; i += 4) if(d[i] > 0) n += 1;
    return { pixels: n, tainted: false };
  } catch(err) {
    return { pixels: null, tainted: true, error: String((err && err.name) || err) };
  }
}
function fmtCount(c){ return c.tainted ? 'restrito' : (c.pixels + ' px opacos'); }
function selftest(){
  const r = {
    pair: state.key, frame: state.frame, mode: state.mode, speaking: false,
    loaded: started.filter((i) => i.__ok === true).length,
    failed: started.filter((i) => i.__ok === false).length,
    pending: started.filter((i) => i.__ok === null).length,
    ca: opaqueCount('ca'), cb: opaqueCount('cb'),
    diff: state.diff, diffUnavailable: state.diffUnavailable || null, cd: state.diff ? opaqueCount('cd') : null,
  };
  const okOpaque = (c, src) => (c.tainted ? (img(src).__ok === true) : (c.pixels || 0) > 0);
  const blank = (c, src) => !okOpaque(c, src);
  r.resourcesOk = r.failed === 0 && r.pending === 0;
  r.nonBlank = !blank(r.ca, srcFor(state.key, pair().baseFrames[state.frame])) && !blank(r.cb, srcFor(state.key, pair().candFrames[state.frame]));
  // ok = the page loaded and rendered; a blank canvas can be legitimate (empty layer in that frame)
  r.ok = r.resourcesOk;
  if(window.__cmp) window.__cmp.lastSelftest = r;
  try {
    document.documentElement.setAttribute('data-selftest', JSON.stringify({
      ok: r.ok, nonBlank: r.nonBlank, pair: r.pair, frame: r.frame, mode: r.mode,
      caOpaque: r.ca.pixels, cbOpaque: r.cb.pixels, cdOpaque: r.cd ? r.cd.pixels : null,
      tainted: r.ca.tainted || r.cb.tainted,
      loaded: r.loaded, failed: r.failed, pending: r.pending, diffUnavailable: r.diffUnavailable,
    }));
  } catch(err) { /* attribute is diagnostic only */ }
  const el = document.getElementById('selftest');
  if(el) el.innerHTML = 'autoteste: #ca ' + fmtCount(r.ca) + ' &middot; #cb ' + fmtCount(r.cb)
    + (r.cd ? ' &middot; #cd ' + fmtCount(r.cd) : '')
    + ' &middot; recursos ' + r.loaded + '/' + started.length
    + (r.pending ? ' &middot; ' + r.pending + ' carregando' : '')
    + (r.failed ? ' &middot; <span class="fail">' + r.failed + ' falharam</span>' : '')
    + ' &middot; ' + (r.ok ? (r.nonBlank ? '<b>recursos ok · canvas com pixels</b>' : '<b>recursos ok</b> &middot; canvas vazio nesta camada/quadro (pode ser vazio legítimo)') : '<span class="fail">recurso pendente ou falho</span>');
  return r;
}
function maybeSelftest(){
  if(state.playing) return;
  const now = performance.now();
  if(now - selftestAt < 200) return;
  selftestAt = now;
  selftest();
}
function paint(){
  const p = pair(); drawSide('ca', p.baseFrames); drawSide('cb', p.candFrames); drawDiff(); readout(); timeline();
  maybeSelftest();
}
function readout(){
  const p = pair(); const f = p.baseFrames[state.frame] || {};
  const d = p.durations[state.frame] || 0;
  const t0 = p.durations.slice(0, state.frame).reduce((a,b)=>a+b,0);
  document.getElementById('readout').innerHTML =
    'quadro <b>' + String(state.frame).padStart(2,'0') + '</b> / ' + String(p.frameCount-1).padStart(2,'0') +
    ' · fase <b>' + (f.phase || '-') + '</b> · duração ' + d + ' ms · início ' + t0 + ' ms de ' + p.total + ' ms · decorrido <b>' + Math.round(state.elapsed) + ' ms</b>' +
    ' · ' + state.speed + '× · ' + (state.playing ? '<b>em reprodução</b>' : 'pausado') +
    ' · arma: ' + (f.weaponVisible ? 'visível' : 'oculta');
}
function timeline(){
  const p = pair(); const tl = document.getElementById('timeline'); tl.innerHTML = '';
  p.durations.forEach((d,i) => {
    const s = document.createElement('div');
    s.className = 'seg' + (i===state.frame?' on':'') + (changedSet().has(i)?' changed':'');
    s.style.flex = d + ' 1 0'; s.textContent = i; s.title = 'quadro ' + i + ' · ' + d + ' ms';
    s.onclick = () => { pause(); state.frame = i; state.elapsed = p.durations.slice(0,i).reduce((a,b)=>a+b,0); paint(); };
    tl.appendChild(s);
  });
}
function schedule(){
  if(state.raf) cancelAnimationFrame(state.raf);
  if(!state.playing) return;
  const p = pair();
  const starts = p.durations.map((_,i)=>p.durations.slice(0,i).reduce((a,b)=>a+b,0));
  const loop = () => {
    if(!state.playing) return;
    const elapsed = (performance.now() - state.playStart) * state.speed + state.playFrom;
    let idx = 0; for(let i=0;i<starts.length;i++) if(elapsed >= starts[i]) idx = i;
    state.elapsed = Math.min(elapsed, p.total);
    if(state.frame !== idx){ state.frame = idx; paint(); }
    if(elapsed >= p.total){ state.playing = false; state.frame = p.frameCount-1; state.elapsed = p.total; paint(); return; }
    state.raf = requestAnimationFrame(loop);
  };
  state.raf = requestAnimationFrame(loop);
}
function play(){ if(state.playing) return; if(state.frame >= pair().frameCount-1){ state.frame = 0; state.elapsed = 0; } state.playing = true; state.playStart = performance.now(); state.playFrom = state.elapsed; paint(); schedule(); }
function pause(){ if(state.playing){ state.playFrom = state.elapsed; state.playStart = performance.now(); } state.playing = false; if(state.raf) cancelAnimationFrame(state.raf); paint(); }
function selectPair(key){
  pause(); state.key = key; state.frame = 0; state.elapsed = 0;
  const p = pair();
  document.getElementById('pairNote').textContent = p.note;
  const v = document.getElementById('pairVerdict'); v.textContent = p.verdict; v.className = 'verdict ' + p.verdictClass;
  document.getElementById('labA').textContent = 'freeze publicado · ' + p.title.split('·')[0].trim();
  document.getElementById('labB').textContent = 'candidato · ' + p.pixels + ' px';
  // preload every asset of both sides so the health panel is meaningful
  for(const f of p.baseFrames){ img(f.comp); img(f.bodyOnly); img(f.handFront); }
  for(const f of p.candFrames){ img(f.comp); img(f.bodyOnly); img(f.handFront); }
  paint(); health();
}
document.getElementById('pair').onchange = (e) => selectPair(e.target.value);
document.getElementById('play').onclick = play;
document.getElementById('pause').onclick = pause;
document.getElementById('restart').onclick = () => { pause(); state.frame = 0; state.elapsed = 0; paint(); };
document.getElementById('prev').onclick = () => { pause(); state.frame = Math.max(0, state.frame-1); state.elapsed = pair().durations.slice(0,state.frame).reduce((a,b)=>a+b,0); paint(); };
document.getElementById('next').onclick = () => { pause(); state.frame = Math.min(pair().frameCount-1, state.frame+1); state.elapsed = pair().durations.slice(0,state.frame).reduce((a,b)=>a+b,0); paint(); };
document.getElementById('speed').onchange = (e) => { const was = state.playing; pause(); state.speed = Number(e.target.value); paint(); if(was) play(); };
document.getElementById('scale').onchange = paint;
document.getElementById('mode').onchange = (e) => { state.mode = e.target.value; paint(); };
document.getElementById('diff').onchange = (e) => { state.diff = e.target.checked; drawDiff(); };

window.__cmp = {
  get pair(){ return state.key; }, get frame(){ return state.frame; }, get elapsed(){ return state.elapsed; },
  get playing(){ return state.playing; }, get speed(){ return state.speed; },
  pairs: PAIRS.map((p) => ({ key: p.key, verdict: p.verdict, durations: p.durations, total: p.total, changedFrames: p.changedFrames, pixels: p.pixels })),
  durations: () => pair().durations,
  frameStart: (i) => pair().durations.slice(0,i).reduce((a,b)=>a+b,0),
  selectPair, setFrame(i){ pause(); state.frame = Math.max(0, Math.min(pair().frameCount-1, i)); state.elapsed = this.frameStart(state.frame); paint(); },
  setMode(m){ state.mode = m; selftestAt = 0; paint(); }, play, pause,
  health: () => { health(); return window.__cmp.lastHealth; },
  selftest,
  waitReady(timeoutMs = 5000){
    const t0 = performance.now();
    return new Promise((resolve) => {
      const tick = () => {
        const pending = started.filter((i) => i.__ok === null).length;
        const waited = Math.round(performance.now() - t0);
        if(pending === 0 || waited > timeoutMs) resolve({ pending, waited });
        else setTimeout(tick, 50);
      };
      tick();
    });
  },
  now: () => performance.now(),
};
selectPair('axe');
if(new URLSearchParams(location.search).get('autoplay') === '1') setTimeout(play, 150);
</script>
</html>
`;

fs.writeFileSync(OUT, html);
console.log(`wrote ${OUT} (${html.length} bytes) prefix=${PREFIX}`);
for (const p of payload) console.log(`  pair ${p.key}: ${p.frameCount}f ${p.total}ms changed=${p.changedFrames.join(',')} px=${p.pixels} master=${p.masterSha.slice(0,12)}`);
