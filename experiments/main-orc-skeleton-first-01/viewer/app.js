'use strict';
/*
 * Visualizador skeleton-first — Experimento 01 (Orc principal, Sword back_l).
 * Consumes poses.json + sequence.json produced by the motion-design DEV.
 * No art, no generation, no network: opens over file:// or http.
 * Data honesty rules:
 *   - under file:// JSON fetch is blocked by the browser => real data loads via
 *     generated JS mirrors (viewer/data/*.js, see tools/make-data-mirrors.mjs);
 *   - when data is absent the page says so on screen and NEVER fakes motion;
 *   - ?fixture=1 loads the clearly-labeled synthetic fixture (viewer/fixtures/).
 */
(function () {
  // ===== Constantes de contrato =====
  const REF = 256; // espaço de coordenadas da correção (256×256), não 128
  const GROUND_Y_FRAC = 190 / REF; // 0.7421875 — correção: chão em y=190 de 256
  const BG_CANDIDATES = [
    // Caminho canônico declarado na correção (pode ainda não existir):
    '../../../characters/orc-v1/source/combat-recovery-v8/rear-arc/back_l-sword/02.png',
    // Fallback plausível 256×256: o próprio quadro establish-grip composto do clipe vigente.
    '../../../characters/orc-v1/source/combat-recovery-v8/rear-arc/back_l-sword/frames/02.png',
  ];
  // COCO-18 do contrato PixelLab (motion-brief/pixellab-skeleton-findings): ARM=punho, LEG=tornozelo.
  const COCO_LABELS = [
    'NOSE', 'NECK',
    'RIGHT SHOULDER', 'RIGHT ELBOW', 'RIGHT ARM',
    'LEFT SHOULDER', 'LEFT ELBOW', 'LEFT ARM',
    'RIGHT HIP', 'RIGHT KNEE', 'RIGHT LEG',
    'LEFT HIP', 'LEFT KNEE', 'LEFT LEG',
    'RIGHT EYE', 'LEFT EYE', 'RIGHT EAR', 'LEFT EAR',
  ];
  const normLabel = (s) => String(s ?? '').trim().toUpperCase().replace(/[\s_]+/g, ' ').replace(/\s+/g, ' ');
  const normKey = (s) => String(s ?? '').trim().toLowerCase().replace(/[\s_]+/g, '-').replace(/-+/g, '-');
  const BONES = [
    ['NECK', 'NOSE'],
    ['NECK', 'RIGHT SHOULDER'], ['NECK', 'LEFT SHOULDER'],
    ['RIGHT SHOULDER', 'LEFT SHOULDER'],
    ['RIGHT SHOULDER', 'RIGHT ELBOW'], ['RIGHT ELBOW', 'RIGHT ARM'],
    ['LEFT SHOULDER', 'LEFT ELBOW'], ['LEFT ELBOW', 'LEFT ARM'],
    ['RIGHT SHOULDER', 'RIGHT HIP'], ['LEFT SHOULDER', 'LEFT HIP'],
    ['RIGHT HIP', 'LEFT HIP'],
    ['RIGHT HIP', 'RIGHT KNEE'], ['RIGHT KNEE', 'RIGHT LEG'],
    ['LEFT HIP', 'LEFT KNEE'], ['LEFT KNEE', 'LEFT LEG'],
    ['NOSE', 'RIGHT EYE'], ['NOSE', 'LEFT EYE'],
    ['RIGHT EYE', 'RIGHT EAR'], ['LEFT EYE', 'LEFT EAR'],
  ];
  const BONES_NO_NECK = [['NOSE', 'RIGHT SHOULDER'], ['NOSE', 'LEFT SHOULDER']];
  const CONTACT_PHASE_RE = /contact|contato|acerto|impacto|impact|\bhit\b/i;
  const DEFAULT_BLADE_FRACTION = 0.30; // exibição; substituída por grip.bladeTip/bladeLength se existirem
  const DEFAULT_HAFT_FRACTION = 0.085; // exibição do cabo

  // ===== Estado =====
  const S = {
    source: 'loading', // 'real' | 'fixture' | 'partial' | 'none'
    sourceDetail: '',
    isFile: location.protocol === 'file:',
    fixtureMode: new URLSearchParams(location.search).get('fixture') === '1',
    notes: [], // divergências/adaptações registradas (obrigatório pelo brief)
    errors: [],
    bg: { status: 'loading', urlUsed: null, width: 0, height: 0 },
    poses: [], frames: [], schedule: [], totalMs: 0, fps: null,
    tips: [], deltas: [], maxDelta: null, maxDeltaFrame: null,
    contactFrames: [], poseMap: [],
    current: 0, playing: false, speed: 1, tMs: 0,
    zoom: 2, bladeLenF: DEFAULT_BLADE_FRACTION,
    toggles: { skeleton: true, labels: true, trail: true, weapon: true, ground: true },
    labelsDrawn: 0, trailPoints: 0, gripHandJoint: null,
  };
  window.__viewer = S;
  window.__viewerApi = {};

  const $ = (id) => document.getElementById(id);
  const canvas = $('stage');
  const ctx = canvas.getContext('2d');
  const bgImg = new Image();

  function note(text) { if (!S.notes.includes(text)) S.notes.push(text); }
  function frac(v) { return Math.max(-0.5, Math.min(1.5, Number(v))); }
  function norm2(x, y) { const m = Math.hypot(x, y) || 1; return { x: x / m, y: y / m }; }

  // ===== Carga de dados =====
  function fetchJSON(url) {
    return fetch(url).then((r) => {
      if (!r.ok) throw new Error('HTTP ' + r.status + ' em ' + url);
      return r.json();
    });
  }
  function loadScriptMirror(src, globalName) {
    return new Promise((resolve, reject) => {
      const el = document.createElement('script');
      el.src = src;
      el.onload = () => resolve(Object.prototype.hasOwnProperty.call(window, globalName) ? window[globalName] : undefined);
      el.onerror = () => reject(new Error('espelho ausente: ' + src));
      document.head.appendChild(el);
    });
  }

  async function loadData() {
    let poses = null, sequence = null;
    if (S.fixtureMode) {
      if (S.isFile) {
        poses = await loadScriptMirror('fixtures/sample-poses.js', '__SV_FIXTURE_POSES').catch(() => undefined);
        sequence = await loadScriptMirror('fixtures/sample-sequence.js', '__SV_FIXTURE_SEQUENCE').catch(() => undefined);
      } else {
        poses = await fetchJSON('fixtures/sample-poses.json').catch(() => undefined);
        sequence = await fetchJSON('fixtures/sample-sequence.json').catch(() => undefined);
      }
      if (poses == null || sequence == null) {
        note('Parâmetro ?fixture=1 pedido, mas o fixture não pôde ser carregado.');
        S.source = 'none'; S.sourceDetail = 'fixture pedido e ausente';
        return null;
      }
      S.source = 'fixture';
      S.sourceDetail = 'fixtures/sample-poses.json + fixtures/sample-sequence.json (SINTÉTICOS)';
      return { poses, sequence };
    }
    if (S.isFile) {
      // file:// bloqueia fetch de JSON; dados reais chegam por espelhos .js gerados.
      poses = await loadScriptMirror('data/poses.js', '__SV_DATA_POSES').catch(() => undefined);
      sequence = await loadScriptMirror('data/sequence.js', '__SV_DATA_SEQUENCE').catch(() => undefined);
      if (poses === undefined) note('Espelho data/poses.js não pôde ser carregado.');
      else if (poses === null) note('../poses.json ainda não existe — espelho data/poses.js vazio (gere com: node viewer/tools/make-data-mirrors.mjs — ou sirva a pasta por HTTP).');
      if (sequence === undefined) note('Espelho data/sequence.js não pôde ser carregado.');
      else if (sequence === null) note('../sequence.json ainda não existe — espelho data/sequence.js vazio (gere com: node viewer/tools/make-data-mirrors.mjs — ou sirva a pasta por HTTP).');
    } else {
      poses = await fetchJSON('../poses.json').catch((e) => { note('../poses.json indisponível (' + e.message + ').'); return null; });
      sequence = await fetchJSON('../sequence.json').catch((e) => { note('../sequence.json indisponível (' + e.message + ').'); return null; });
    }
    if (poses && sequence) { S.source = 'real'; S.sourceDetail = S.isFile ? 'espelhos de ../poses.json + ../sequence.json' : '../poses.json + ../sequence.json'; }
    else if (poses || sequence) { S.source = 'partial'; S.sourceDetail = 'apenas um dos dois JSON foi carregado'; }
    else { S.source = 'none'; S.sourceDetail = 'nenhum JSON de movimento disponível'; }
    return { poses, sequence };
  }

  // ===== Fundo de referência (256×256, correção) =====
  function tryLoadBg(idx) {
    if (idx >= BG_CANDIDATES.length) {
      S.bg.status = 'failed';
      note('Nenhuma imagem de fundo 256×256 encontrada nos caminhos conhecidos — o esqueleto é desenhado sobre grade neutra.');
      draw();
      return;
    }
    const url = BG_CANDIDATES[idx];
    const probe = new Image();
    probe.onload = () => {
      bgImg.src = url;
      S.bg.status = idx > 0 ? 'fallback' : 'ok';
      S.bg.urlUsed = url;
      S.bg.width = probe.naturalWidth; S.bg.height = probe.naturalHeight;
      if (idx > 0) note('Fundo canônico da correção ausente (back_l-sword/02.png) — usando ' + url.split('/').slice(-2).join('/') + ' (256×256, establish-grip do clipe vigente).');
      if (probe.naturalWidth !== REF || probe.naturalHeight !== REF) {
        note('Fundo carregado tem ' + probe.naturalWidth + '×' + probe.naturalHeight + ' px, mas o espaço da correção é 256×256.');
      }
      draw(); drawThumbs(); renderBanners(); updateHud();
    };
    probe.onerror = () => tryLoadBg(idx + 1);
    probe.src = url;
  }

  // ===== Adaptação ao formato real (o brief manda adaptar, não exigir mudança do outro DEV) =====
  let coordPxNoteDone = false;
  function adaptPoint(p) {
    if (!p || typeof p.x !== 'number' || typeof p.y !== 'number') return null;
    let x = frac(p.x), y = frac(p.y);
    if ((Math.abs(x) > 1.5 || Math.abs(y) > 1.5) && !coordPxNoteDone) {
      coordPxNoteDone = true;
      note('Coordenadas em pixels detectadas (valores > 1.5) — convertidas dividindo por ' + REF + '.');
    }
    if (Math.abs(x) > 1.5) x = x / REF;
    if (Math.abs(y) > 1.5) y = y / REF;
    return { x, y };
  }
  function adaptJoints(list) {
    if (!Array.isArray(list)) return null;
    const joints = [];
    for (const j of list) {
      const pt = adaptPoint(j);
      if (!pt || !j.label) continue;
      joints.push({
        label: String(j.label), x: pt.x, y: pt.y,
        z_index: Number.isFinite(j.z_index) ? j.z_index : 0,
        depth: Number.isFinite(j.depth) ? j.depth : null,
      });
    }
    return joints.length ? joints : null;
  }
  function adaptGrip(g) {
    if (!g || typeof g !== 'object') return null;
    const point = adaptPoint(g.point);
    if (!point) return null;
    const haft = g.haftDirection ? adaptPoint(g.haftDirection) : null;
    const blade = g.bladeDirection ? adaptPoint(g.bladeDirection) : null;
    const bladeN = blade ? norm2(blade.x, blade.y)
      : (haft ? (() => { const h = norm2(haft.x, haft.y); return { x: -h.x, y: -h.y }; })() : null);
    let haftN = haft ? norm2(haft.x, haft.y) : (bladeN ? { x: -bladeN.x, y: -bladeN.y } : null);
    return {
      hand: g.hand ? String(g.hand) : null,
      point,
      haftDirection: haftN,
      bladeDirection: bladeN,
      bladeTip: g.bladeTip ? adaptPoint(g.bladeTip) : null,
      bladeLength: Number.isFinite(g.bladeLength) ? frac(g.bladeLength) : null,
    };
  }
  function adaptPoses(raw) {
    if (!raw || !Array.isArray(raw.poses)) { note('poses.json sem array "poses" utilizável.'); return []; }
    const ref = raw.reference;
    if (ref && (Number(ref.width) !== REF || Number(ref.height) !== REF)) {
      note('poses.reference declara ' + ref.width + '×' + ref.height + ' — a correção manda ignorar e usar o espaço 256×256.');
    }
    return raw.poses.map((p, i) => ({
      id: p.id ? String(p.id) : 'pose-' + i,
      label: p.label ? String(p.label) : (p.id ? String(p.id) : 'Pose ' + i),
      phase: p.phase ? String(p.phase) : null,
      frameIndex: Number.isFinite(p.frameIndex) ? p.frameIndex : (Number.isFinite(p.frame) ? p.frame : null),
      joints: adaptJoints(p.joints) || [],
      grip: adaptGrip(p.grip),
    }));
  }

  function adaptSequence(raw) {
    if (!raw || !Array.isArray(raw.frames) || !raw.frames.length) { note('sequence.json sem "frames" utilizáveis.'); return []; }
    if (Number.isFinite(raw.fps)) S.fps = raw.fps;
    let missingDur = 0; const carried = [];
    const frames = raw.frames.map((f, pos) => {
      const index = Number.isFinite(f.index) ? f.index : pos;
      const phase = String(f.phase ?? f.sourcePhase ?? '(sem fase)');
      let durationMs = Number(f.durationMs);
      if (!(durationMs > 0)) {
        durationMs = (S.fps && S.fps > 0) ? 1000 / S.fps : (Number(raw.totalMs) > 0 ? Number(raw.totalMs) / raw.frames.length : 0);
        missingDur++;
      }
      let joints = adaptJoints(f.joints);
      let grip = adaptGrip(f.grip);
      if (!joints || !grip) {
        const pid = f.poseId ?? f.pose;
        const pose = (pid != null) ? S.poses.find((p) => normKey(p.id) === normKey(String(pid))) : null;
        if (pose) { if (!joints) joints = pose.joints.slice(); if (!grip) grip = pose.grip; }
      }
      return { index, phase, durationMs, joints, grip, _pos: pos };
    });
    if (missingDur > 0) note(missingDur + ' quadro(s) sem durationMs — duração derivada de ' + (S.fps ? 'fps declarado' : 'totalMs/padrão') + '.');
    let prev = null;
    for (const f of frames) {
      if (!f.joints && prev && prev.joints) { f.joints = prev.joints.slice(); carried.push('F' + f.index); }
      if (!f.grip && prev && prev.grip) f.grip = prev.grip;
      if (f.joints || f.grip) prev = f;
    }
    if (carried.length) note('Quadro(s) sem joints/grip próprios — herdados do quadro anterior: ' + carried.join(', ') + '.');
    const sum = frames.reduce((acc, f) => acc + f.durationMs, 0);
    if (Number.isFinite(raw.totalMs) && Math.abs(raw.totalMs - sum) > 0.5) {
      note('totalMs declarado (' + raw.totalMs + ') difere da soma das durações (' + Math.round(sum) + ') — usando a soma.');
    }
    S.totalMs = sum;
    const ref = raw.reference;
    if (ref && (Number(ref.width) !== REF || Number(ref.height) !== REF)) {
      note('sequence.reference declara ' + ref.width + '×' + ref.height + ' — a correção manda ignorar e usar o espaço 256×256.');
    }
    return frames;
  }

  // ===== Derivados: trilha da lâmina, deltas, cronograma, contato, pose→quadro =====
  function tipOf(grip) {
    if (!grip || !grip.point) return null;
    if (grip.bladeTip) return { x: grip.bladeTip.x, y: grip.bladeTip.y };
    if (!grip.bladeDirection) return null;
    const len = grip.bladeLength != null ? grip.bladeLength : S.bladeLenF;
    return { x: grip.point.x + grip.bladeDirection.x * len, y: grip.point.y + grip.bladeDirection.y * len };
  }
  function computeDerived() {
    S.tips = S.frames.map((f) => tipOf(f.grip));
    S.trailPoints = S.tips.filter(Boolean).length;
    S.deltas = S.tips.map((t, i) => {
      if (i === 0 || !t || !S.tips[i - 1]) return null;
      return Math.hypot(t.x - S.tips[i - 1].x, t.y - S.tips[i - 1].y) * REF;
    });
    S.maxDelta = null; S.maxDeltaFrame = null;
    S.deltas.forEach((d, i) => {
      if (d != null && (S.maxDelta == null || d > S.maxDelta)) { S.maxDelta = d; S.maxDeltaFrame = i; }
    });
    S.schedule = []; let acc = 0;
    for (const f of S.frames) { S.schedule.push(acc); acc += f.durationMs; }
    S.contactFrames = [];
    S.frames.forEach((f, i) => {
      if (f.contactFlag === true || CONTACT_PHASE_RE.test(f.phase)) S.contactFrames.push(i);
    });
    // pose → quadro: frameIndex explícito > fase declarada > id = fase > ordem (brief: quadros 0–4 = 5 poses)
    S.poseMap = S.poses.map((p, i) => {
      if (p.frameIndex != null && p.frameIndex >= 0 && p.frameIndex < S.frames.length) {
        return { frame: p.frameIndex, via: 'frameIndex declarado' };
      }
      if (p.phase) {
        for (let k = S.frames.length - 1; k >= 0; k--) {
          if (normKey(S.frames[k].phase) === normKey(p.phase)) return { frame: k, via: 'fase "' + p.phase + '"' };
        }
      }
      for (let k = S.frames.length - 1; k >= 0; k--) {
        if (normKey(S.frames[k].phase) === normKey(p.id)) return { frame: k, via: 'id = fase' };
      }
      if (i < S.frames.length) return { frame: i, via: 'ordem (brief: quadros 0–4 = poses)' };
      return null;
    });
  }

  // ===== Renderização =====
  function applyZoom() {
    canvas.width = REF * S.zoom;
    canvas.height = REF * S.zoom;
  }
  const px = (f) => f * REF * S.zoom;

  function drawCheckerboard() {
    const cell = 16 * S.zoom;
    ctx.fillStyle = '#141a20'; ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = '#1b232c';
    for (let y = 0; y < canvas.height; y += cell) {
      for (let x = 0; x < canvas.width; x += cell) {
        if (((x / cell) + (y / cell)) % 2 === 0) ctx.fillRect(x, y, cell, cell);
      }
    }
  }

  function drawGround() {
    const y = px(GROUND_Y_FRAC);
    ctx.save();
    ctx.strokeStyle = 'rgba(93,211,158,0.85)';
    ctx.lineWidth = 1.5;
    ctx.setLineDash([6 * S.zoom / 2, 5 * S.zoom / 2]);
    ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
    ctx.setLineDash([]);
    ctx.font = '600 ' + Math.round(10 * Math.max(1, S.zoom / 2)) + 'px "Segoe UI", system-ui, sans-serif';
    ctx.textAlign = 'right'; ctx.textBaseline = 'bottom';
    const label = 'chão y=190/256 (0.7422)';
    ctx.lineWidth = 3; ctx.strokeStyle = 'rgba(4,10,14,0.9)';
    ctx.strokeText(label, canvas.width - 6, y - 3);
    ctx.fillStyle = '#5dd39e';
    ctx.fillText(label, canvas.width - 6, y - 3);
    ctx.restore();
  }

  function drawTrail() {
    if (!S.toggles.trail || !S.tips.length) return;
    ctx.save();
    // segmentos entre pontas consecutivas conhecidas
    ctx.strokeStyle = 'rgba(255,210,63,0.85)';
    ctx.lineWidth = 2;
    let began = false;
    ctx.beginPath();
    for (const t of S.tips) {
      if (!t) { began = false; continue; }
      if (!began) { ctx.moveTo(px(t.x), px(t.y)); began = true; }
      else ctx.lineTo(px(t.x), px(t.y));
    }
    ctx.stroke();
    // pontos por quadro
    for (let i = 0; i < S.tips.length; i++) {
      const t = S.tips[i]; if (!t) continue;
      ctx.beginPath(); ctx.arc(px(t.x), px(t.y), 2.5, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(255,210,63,0.9)'; ctx.fill();
    }
    // marcação de contato
    ctx.font = '600 ' + Math.round(10 * Math.max(1, S.zoom / 2)) + 'px "Segoe UI", system-ui, sans-serif';
    ctx.textAlign = 'center'; ctx.textBaseline = 'bottom';
    for (const i of S.contactFrames) {
      const t = S.tips[i]; if (!t) continue;
      ctx.beginPath(); ctx.arc(px(t.x), px(t.y), 8, 0, Math.PI * 2);
      ctx.strokeStyle = '#ff6b6b'; ctx.lineWidth = 2.5; ctx.stroke();
      const lbl = 'contato';
      ctx.lineWidth = 3; ctx.strokeStyle = 'rgba(4,10,14,0.9)';
      ctx.strokeText(lbl, px(t.x), px(t.y) - 12);
      ctx.fillStyle = '#ff6b6b';
      ctx.fillText(lbl, px(t.x), px(t.y) - 12);
    }
    // ponta atual
    const cur = S.tips[S.current];
    if (cur) {
      ctx.beginPath(); ctx.arc(px(cur.x), px(cur.y), 5, 0, Math.PI * 2);
      ctx.fillStyle = '#ffffff'; ctx.fill();
      ctx.beginPath(); ctx.arc(px(cur.x), px(cur.y), 9, 0, Math.PI * 2);
      ctx.strokeStyle = 'rgba(255,255,255,0.65)'; ctx.lineWidth = 1.5; ctx.stroke();
    }
    ctx.restore();
  }

  function drawWeapon(grip) {
    if (!S.toggles.weapon || !grip || !grip.point || !grip.bladeDirection) return;
    const p = grip.point, bd = grip.bladeDirection, hd = grip.haftDirection || { x: -bd.x, y: -bd.y };
    const bladeLen = grip.bladeLength != null ? grip.bladeLength : S.bladeLenF;
    ctx.save();
    ctx.lineCap = 'round';
    // cabo
    ctx.strokeStyle = '#8a6544'; ctx.lineWidth = 4.5;
    ctx.beginPath(); ctx.moveTo(px(p.x), px(p.y));
    ctx.lineTo(px(p.x + hd.x * DEFAULT_HAFT_FRACTION), px(p.y + hd.y * DEFAULT_HAFT_FRACTION));
    ctx.stroke();
    // guarda cruzada
    const gx = -bd.y, gy = bd.x; // perpendicular
    ctx.strokeStyle = '#c9a36a'; ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(px(p.x + gx * 0.014), px(p.y + gy * 0.014));
    ctx.lineTo(px(p.x - gx * 0.014), px(p.y - gy * 0.014));
    ctx.stroke();
    // lâmina
    ctx.strokeStyle = 'rgba(20,28,36,0.9)'; ctx.lineWidth = 5.5;
    ctx.beginPath(); ctx.moveTo(px(p.x), px(p.y));
    ctx.lineTo(px(p.x + bd.x * bladeLen), px(p.y + bd.y * bladeLen));
    ctx.stroke();
    ctx.strokeStyle = '#e8f1f8'; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(px(p.x), px(p.y));
    ctx.lineTo(px(p.x + bd.x * bladeLen), px(p.y + bd.y * bladeLen));
    ctx.stroke();
    ctx.restore();
  }

  function jointByLabel(joints, wantLabel) {
    if (!joints || !wantLabel) return null;
    const want = normLabel(wantLabel);
    return joints.find((j) => normLabel(j.label) === want) || null;
  }

  function labelOffset(label) {
    const L = normLabel(label);
    if (L === 'NOSE') return { dx: 0, dy: -11, align: 'center' };
    if (L === 'NECK') return { dx: 0, dy: 16, align: 'center' };
    if (L.indexOf('LEFT ') === 0) return { dx: -8, dy: 3, align: 'right' };
    if (L.indexOf('RIGHT ') === 0) return { dx: 8, dy: 3, align: 'left' };
    if (L.indexOf(' EYE') > 0) return { dx: 0, dy: -9, align: 'center' };
    return { dx: 0, dy: -10, align: 'center' };
  }

  function drawSkeleton(frame) {
    S.labelsDrawn = 0; S.gripHandJoint = null;
    const joints = frame && frame.joints ? frame.joints : null;
    if (!S.toggles.skeleton || !joints || !joints.length) return;
    ctx.save();
    const byLabel = new Map(joints.map((j) => [normLabel(j.label), j]));
    const bones = (byLabel.has('NECK') ? BONES : BONES.concat(BONES_NO_NECK));
    ctx.lineCap = 'round';
    ctx.strokeStyle = 'rgba(89,209,255,0.9)';
    ctx.lineWidth = 2;
    ctx.beginPath();
    for (const [a, b] of bones) {
      const ja = byLabel.get(a), jb = byLabel.get(b);
      if (!ja || !jb) continue;
      ctx.moveTo(px(ja.x), px(ja.y));
      ctx.lineTo(px(jb.x), px(jb.y));
    }
    ctx.stroke();
    // juntas em ordem de z_index (z maior = por cima)
    const ordered = joints.slice().sort((p, q) => (p.z_index || 0) - (q.z_index || 0));
    for (const j of ordered) {
      ctx.beginPath(); ctx.arc(px(j.x), px(j.y), 4, 0, Math.PI * 2);
      ctx.fillStyle = '#9be7ff'; ctx.fill();
      ctx.strokeStyle = '#0a2a3a'; ctx.lineWidth = 1.5; ctx.stroke();
    }
    // punho que empunha (grip.hand) marcado de forma distinta
    const grip = frame.grip;
    if (grip && grip.hand) {
      const hand = jointByLabel(joints, grip.hand);
      if (hand) {
        S.gripHandJoint = hand.label;
        ctx.fillStyle = '#ff9f43';
        ctx.strokeStyle = '#7a3c00'; ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.rect(px(hand.x) - 6, px(hand.y) - 6, 12, 12);
        ctx.fill(); ctx.stroke();
        ctx.beginPath(); ctx.arc(px(hand.x), px(hand.y), 10, 0, Math.PI * 2);
        ctx.strokeStyle = 'rgba(255,159,67,0.75)'; ctx.lineWidth = 1.5; ctx.stroke();
      }
      // ponto de pega
      if (grip.point) {
        const gx = px(grip.point.x), gy = px(grip.point.y);
        ctx.fillStyle = '#ffe066';
        ctx.strokeStyle = '#5a4a00'; ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.moveTo(gx, gy - 7); ctx.lineTo(gx + 7, gy); ctx.lineTo(gx, gy + 7); ctx.lineTo(gx - 7, gy);
        ctx.closePath(); ctx.fill(); ctx.stroke();
      }
    }
    // rótulos legíveis (halo escuro + texto claro)
    if (S.toggles.labels) {
      ctx.font = '600 11px "Segoe UI", system-ui, sans-serif';
      ctx.lineJoin = 'round';
      for (const j of joints) {
        const off = labelOffset(j.label);
        const tx = px(j.x) + off.dx, ty = px(j.y) + off.dy;
        ctx.textAlign = off.align; ctx.textBaseline = 'middle';
        ctx.lineWidth = 3; ctx.strokeStyle = 'rgba(4,10,14,0.92)';
        ctx.strokeText(j.label, tx, ty);
        ctx.fillStyle = '#f2f8fb';
        ctx.fillText(j.label, tx, ty);
        S.labelsDrawn++;
      }
    }
    ctx.restore();
  }

  function draw() {
    applyZoom();
    if (S.bg.status === 'ok' || S.bg.status === 'fallback') {
      ctx.imageSmoothingEnabled = false;
      ctx.drawImage(bgImg, 0, 0, REF * S.zoom, REF * S.zoom);
      ctx.imageSmoothingEnabled = true;
    } else {
      drawCheckerboard();
    }
    if (S.toggles.ground) drawGround();
    drawTrail();
    const frame = S.frames[S.current] || null;
    drawWeapon(frame ? frame.grip : null);
    drawSkeleton(frame);
  }

  // ===== Faixa das cinco poses-chave =====
  function drawThumb(cv, pose) {
    const tctx = cv.getContext('2d');
    const TH = cv.width; // quadrado
    const s = TH / REF;
    tctx.clearRect(0, 0, TH, TH);
    if (S.bg.status === 'ok' || S.bg.status === 'fallback') {
      tctx.imageSmoothingEnabled = false;
      tctx.drawImage(bgImg, 0, 0, TH, TH);
      tctx.imageSmoothingEnabled = true;
    } else {
      tctx.fillStyle = '#141a20'; tctx.fillRect(0, 0, TH, TH);
    }
    // chão
    tctx.strokeStyle = 'rgba(93,211,158,0.8)'; tctx.lineWidth = 1;
    tctx.setLineDash([3, 2]);
    tctx.beginPath(); tctx.moveTo(0, GROUND_Y_FRAC * TH); tctx.lineTo(TH, GROUND_Y_FRAC * TH); tctx.stroke();
    tctx.setLineDash([]);
    if (!pose.joints.length) return;
    const byLabel = new Map(pose.joints.map((j) => [normLabel(j.label), j]));
    const bones = (byLabel.has('NECK') ? BONES : BONES.concat(BONES_NO_NECK));
    tctx.strokeStyle = 'rgba(89,209,255,0.9)'; tctx.lineWidth = 1.5; tctx.lineCap = 'round';
    tctx.beginPath();
    for (const [a, b] of bones) {
      const ja = byLabel.get(a), jb = byLabel.get(b);
      if (!ja || !jb) continue;
      tctx.moveTo(ja.x * s * REF, ja.y * s * REF);
      tctx.lineTo(jb.x * s * REF, jb.y * s * REF);
    }
    tctx.stroke();
    for (const j of pose.joints) {
      tctx.beginPath(); tctx.arc(j.x * s * REF, j.y * s * REF, 2.5, 0, Math.PI * 2);
      tctx.fillStyle = '#9be7ff'; tctx.fill();
    }
    if (pose.grip && pose.grip.bladeDirection) {
      const p = pose.grip.point, bd = pose.grip.bladeDirection;
      const len = pose.grip.bladeLength != null ? pose.grip.bladeLength : S.bladeLenF;
      tctx.strokeStyle = '#8a6544'; tctx.lineWidth = 3;
      tctx.beginPath(); tctx.moveTo(p.x * s * REF, p.y * s * REF);
      tctx.lineTo((p.x - bd.x * DEFAULT_HAFT_FRACTION) * s * REF, (p.y - bd.y * DEFAULT_HAFT_FRACTION) * s * REF);
      tctx.stroke();
      tctx.strokeStyle = '#e8f1f8'; tctx.lineWidth = 2;
      tctx.beginPath(); tctx.moveTo(p.x * s * REF, p.y * s * REF);
      tctx.lineTo((p.x + bd.x * len) * s * REF, (p.y + bd.y * len) * s * REF);
      tctx.stroke();
    }
  }
  function buildPoseStrip() {
    const wrap = $('poses-strip');
    wrap.innerHTML = '';
    S.poses.forEach((pose, i) => {
      const map = S.poseMap[i];
      const btn = document.createElement('button');
      btn.className = 'pose-chip';
      btn.dataset.poseId = pose.id;
      btn.title = map ? 'Vai ao quadro ' + map.frame + ' (' + map.via + ')' : 'Sem quadro correspondente na sequência carregada';
      if (!map) btn.disabled = true;
      const cv = document.createElement('canvas');
      cv.width = 176; cv.height = 176;
      const cap = document.createElement('span');
      cap.className = 'pose-name';
      cap.textContent = pose.label;
      const sub = document.createElement('span');
      sub.className = 'pose-via';
      sub.textContent = map ? '→ F' + String(S.frames[map.frame].index).padStart(2, '0') + ' · ' + map.via : '— sem quadro';
      btn.appendChild(cv); btn.appendChild(cap); btn.appendChild(sub);
      btn.addEventListener('click', () => goToPose(i));
      wrap.appendChild(btn);
      drawThumb(cv, pose);
    });
    markActivePose();
  }
  function drawThumbs() {
    document.querySelectorAll('#poses-strip .pose-chip canvas').forEach((cv, i) => {
      if (S.poses[i]) drawThumb(cv, S.poses[i]);
    });
  }
  function markActivePose() {
    document.querySelectorAll('#poses-strip .pose-chip').forEach((btn, i) => {
      const map = S.poseMap[i];
      btn.classList.toggle('active', !!(map && map.frame === S.current));
    });
  }

  // ===== Playback por durações reais =====
  function frameAtTime(ms) {
    if (!S.schedule.length) return 0;
    const t = Math.max(0, Math.min(ms, S.totalMs - 0.001));
    let lo = 0, hi = S.schedule.length - 1, ans = 0;
    while (lo <= hi) {
      const mid = (lo + hi) >> 1;
      if (S.schedule[mid] <= t) { ans = mid; lo = mid + 1; } else hi = mid - 1;
    }
    return ans;
  }
  function setFrame(i, opts) {
    if (!S.frames.length) return;
    S.current = ((i % S.frames.length) + S.frames.length) % S.frames.length;
    S.tMs = S.schedule[S.current] || 0;
    if (!(opts && opts.keepPlay)) draw();
    updateHud();
  }
  function step(dir) {
    pause();
    setFrame(S.current + dir);
  }
  function play(speed) {
    if (!S.frames.length) return;
    if (speed) S.speed = speed;
    $('speed-select').value = String(S.speed);
    S.playing = true;
    updateHud();
  }
  function pause() {
    S.playing = false;
    updateHud();
  }
  function goToPose(i) {
    const map = S.poseMap[i];
    if (!map) return;
    pause();
    setFrame(map.frame);
  }
  let lastTs = null;
  function tick(ts) {
    if (S.playing && S.frames.length) {
      if (lastTs != null) {
        S.tMs += (ts - lastTs) * S.speed;
        if (S.tMs >= S.totalMs) S.tMs -= S.totalMs;
        const i = frameAtTime(S.tMs);
        if (i !== S.current) { S.current = i; draw(); updateHud(); }
        else updateHudTime();
      }
      lastTs = ts;
    } else lastTs = null;
    requestAnimationFrame(tick);
  }

  // ===== HUD / painéis =====
  function updateHudTime() {
    const f = S.frames[S.current];
    if (!f) return;
    const end = (S.schedule[S.current] || 0) + f.durationMs;
    $('hud-time').textContent = 'janela ' + Math.round(S.schedule[S.current] || 0) + '–' + Math.round(end) + ' ms / ' + Math.round(S.totalMs) + ' ms';
  }
  function updateHud() {
    const n = S.frames.length;
    const f = S.frames[S.current];
    $('hud-frame').textContent = n ? 'F' + String(f ? f.index : 0).padStart(2, '0') + ' · quadro ' + (S.current + 1) + '/' + n : 'sem quadros';
    $('hud-phase').textContent = f ? f.phase : '—';
    $('hud-dur').textContent = f ? f.durationMs.toFixed(0) + ' ms' : '—';
    updateHudTime();
    const d = S.deltas[S.current];
    $('hud-delta').textContent = (d == null) ? '— (sem anterior)' : d.toFixed(1) + ' px';
    $('hud-deltamax').textContent = (S.maxDelta == null) ? 'máx: —' :
      'máx da sequência: ' + S.maxDelta.toFixed(1) + ' px (F' + String(S.frames[S.maxDeltaFrame].index).padStart(2, '0') + ')';
    const grip = f ? f.grip : null;
    $('hud-grip').textContent = grip ? (grip.hand || '—') + ' · pega (' + grip.point.x.toFixed(3) + ', ' + grip.point.y.toFixed(3) + ')' : 'sem pega neste quadro';
    $('hud-src').textContent = S.source === 'real' ? 'DADOS REAIS' : S.source === 'fixture' ? 'FIXTURE SINTÉTICO' : S.source.toUpperCase();
    $('hud-src').className = 'badge ' + (S.source === 'real' ? 'badge-real' : S.source === 'fixture' ? 'badge-fixture' : 'badge-missing');
    const scrub = $('frame-scrub');
    scrub.max = String(Math.max(0, n - 1));
    scrub.value = String(S.current);
    $('scrub-label').textContent = n ? (S.current + 1) + '/' + n : '0/0';
    markActivePose();
  }

  function renderBanners() {
    const bx = $('banner-fixture');
    bx.hidden = S.source !== 'fixture';
    const bm = $('banner-missing');
    if (S.source === 'real') { bm.hidden = true; }
    else {
      bm.hidden = false;
      bm.innerHTML = '<strong>Sem movimento real na tela.</strong> ' + escapeHtml(S.sourceDetail) +
        (S.isFile
          ? '<br>Por <code>file://</code> o navegador bloqueia <code>fetch</code> de JSON. Opções: (a) gere espelhos após os JSONs chegarem: <code>node viewer/tools/make-data-mirrors.mjs</code>; (b) sirva a pasta por HTTP (ex.: <code>npx serve experiments/main-orc-skeleton-first-01</code>) e abra por <code>http://</code>; (c) demonstração: <code>?fixture=1</code>.'
          : '<br>Verifique se <code>../poses.json</code> e <code>../sequence.json</code> existem ao lado desta pasta, ou use <code>?fixture=1</code> para demonstração.');
    }
    const bb = $('banner-bg');
    bb.hidden = !(S.bg.status === 'fallback' || S.bg.status === 'failed');
    if (S.bg.status === 'fallback') {
      bb.innerHTML = '<strong>Fundo:</strong> o caminho canônico da correção (<code>back_l-sword/02.png</code>) ainda não existe — usando <code>back_l-sword/frames/02.png</code> (256×256, establish-grip). Confirme antes de julgar o corpo.';
    } else if (S.bg.status === 'failed') {
      bb.innerHTML = '<strong>Fundo 256×256 ausente</strong> — esqueleto sobre grade neutra; a comparação com o corpo não é possível.';
    }
    const ul = $('notes-list');
    ul.innerHTML = '';
    for (const n of S.notes) {
      const li = document.createElement('li');
      li.textContent = n;
      ul.appendChild(li);
    }
    $('notes-count').textContent = String(S.notes.length);
  }
  function escapeHtml(s) { const d = document.createElement('div'); d.textContent = String(s); return d.innerHTML; }

  // ===== Controles =====
  function wireControls() {
    $('btn-play-1').addEventListener('click', () => play(1));
    $('btn-play-half').addEventListener('click', () => play(0.5));
    $('btn-pause').addEventListener('click', () => pause());
    $('btn-step-back').addEventListener('click', () => step(-1));
    $('btn-step-fwd').addEventListener('click', () => step(1));
    $('btn-restart').addEventListener('click', () => { pause(); setFrame(0); });
    $('speed-select').addEventListener('change', (e) => { S.speed = Number(e.target.value) || 1; updateHud(); });
    $('zoom-select').addEventListener('change', (e) => { S.zoom = Number(e.target.value) || 2; draw(); drawThumbs(); });
    for (const key of Object.keys(S.toggles)) {
      $(('tg-' + key)).addEventListener('change', (e) => { S.toggles[key] = e.target.checked; draw(); });
    }
    $('blade-len').addEventListener('input', (e) => {
      S.bladeLenF = Number(e.target.value) || DEFAULT_BLADE_FRACTION;
      $('blade-len-val').textContent = S.bladeLenF.toFixed(2);
      computeDerived(); draw(); updateHud();
    });
    $('frame-scrub').addEventListener('input', (e) => {
      pause();
      setFrame(Number(e.target.value) | 0);
    });
    document.addEventListener('keydown', (e) => {
      const tag = (e.target && e.target.tagName) || '';
      if (tag === 'INPUT' || tag === 'SELECT' || tag === 'TEXTAREA') return;
      if (e.code === 'Space') { e.preventDefault(); S.playing ? pause() : play(); }
      else if (e.code === 'ArrowLeft') { e.preventDefault(); step(-1); }
      else if (e.code === 'ArrowRight') { e.preventDefault(); step(1); }
    });
    // tooltip de junta
    canvas.addEventListener('mousemove', (e) => {
      const tip = $('tooltip');
      const f = S.frames[S.current];
      if (!f || !f.joints) { tip.hidden = true; return; }
      const r = canvas.getBoundingClientRect();
      const mx = e.clientX - r.left, my = e.clientY - r.top;
      let best = null, bestD = 14;
      for (const j of f.joints) {
        const d = Math.hypot(px(j.x) - mx, px(j.y) - my);
        if (d < bestD) { bestD = d; best = j; }
      }
      if (!best) { tip.hidden = true; return; }
      tip.hidden = false;
      tip.innerHTML = '<strong>' + escapeHtml(best.label) + '</strong><br>x=' + best.x.toFixed(3) + ' y=' + best.y.toFixed(3) +
        (best.z_index != null ? '<br>z_index=' + best.z_index : '') +
        (best.depth != null ? '<br>depth=' + best.depth : '');
      tip.style.left = (mx + 14) + 'px';
      tip.style.top = (my + 14) + 'px';
    });
    canvas.addEventListener('mouseleave', () => { $('tooltip').hidden = true; });
  }

  // ===== Inicialização =====
  async function init() {
    try {
      wireControls();
      applyZoom();
      draw(); // grade neutra imediata
      tryLoadBg(0);
      const raw = await loadData();
      if (raw && (raw.poses || raw.sequence)) {
        S.poses = adaptPoses(raw.poses);
        S.frames = adaptSequence(raw.sequence);
        computeDerived();
        buildPoseStrip();
        setFrame(0);
      }
      renderBanners();
      updateHud();
      requestAnimationFrame(tick);
    } catch (err) {
      S.errors.push(String(err && err.stack || err));
      renderBanners();
    }
  }
  window.__viewerApi = { setFrame, step, play, pause, frameAtTime, goToPose, draw, computeDerived };
  init();
})();
