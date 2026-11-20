"""Build the complete 4-direction x 7-action interactive review & state-transition studio for Orc V1."""
from pathlib import Path
import json, shutil, hashlib, html

R = Path(__file__).resolve().parents[1]
L = R / 'Biblioteca de Arte'
B = R / 'characters/orc-v1/source/complete-v1'
DIRECTIONS = ['front_r', 'front_l', 'back_r', 'back_l']
DIR_LABELS = {
    'front_r': 'Frente-Direita (front_r · SE)',
    'front_l': 'Frente-Esquerda (front_l · SW)',
    'back_r':  'Costas-Direita (back_r · NE)',
    'back_l':  'Costas-Esquerda (back_l · NW)',
}
ACTIONS = ['Idle', 'Walk', 'Unarmed', 'Sword', 'Axe', 'Hit', 'Defeat']
ACTION_LABELS = {
    'Idle':    'Idle · Respiração sem arma (5f · 2200 ms)',
    'Walk':    'Walk · Locomoção sem arma (16f · 1280 ms)',
    'Unarmed': 'Ataque Desarmado · Soco/Golpe físico (5f · 450 ms)',
    'Sword':   'Ataque de Espada · Espada do Recruta (13f · 730 ms)',
    'Axe':     'Ataque de Machado · Machado de Milícia (12f · 1005 ms)',
    'Hit':     'Hit · Reação de dano (5f · 450 ms)',
    'Defeat':  'Defeat · Queda e pose terminal (5f · 700 ms)',
}

read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

def build_review_target(out_dir: Path, is_comparative: bool):
    out_dir.mkdir(parents=True, exist_ok=True)
    files = []

    def copy(src_rel: str, dst_rel: str) -> str:
        src = R / src_rel
        dst = out_dir / dst_rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        files.append({'file': dst_rel, 'source': src_rel, 'sha256': sha(dst)})
        return dst_rel

    concept = copy('characters/orc-v1/concepts/concept-selected.png', 'Personagem/Conceito.png')
    concept_master = copy('characters/orc-v1/source/aseprite/concept-selected.aseprite', 'Personagem/Conceito.aseprite')
    copy('docs/MAIN_ORC_COMBAT_POLISH.md', 'DOCUMENTACAO.md')
    copy('docs/ARTISTIC_QUALITY_GATES.md', 'PORTOES-QUALIDADE-ARTISTICA.md')
    copy('config/artistic-quality-gates-v1.json', 'artistic-quality-gates-v1.json')
    copy('docs/WEAPON_ART_STANDARD.md', 'PADRAO-DE-ARMAS.md')
    copy('docs/IDLE_ART_STANDARD.md', 'PADRAO-DE-IDLE.md')
    copy('reports/orc-v1-animation-coverage-v1.json', 'MATRIZ-COBERTURA.json')

    before_assets = {}
    before_dir = R / 'experiments/main-orc-complete-v1/rejected-before'
    if before_dir.exists():
        for p in sorted(before_dir.glob('*.png')):
            before_assets[p.name] = copy(f'experiments/main-orc-complete-v1/rejected-before/{p.name}', f'AntesDepois/{p.name}')

    weapons_meta = {}
    for category, wid in [('Sword', 'recruit-sword'), ('Axe', 'militia-axe')]:
        w = read(R / f'assets/weapons/{wid}/weapon.json')
        folder = f'Armas/{w["name"]}'
        sp = copy(w['sprite'], f'{folder}/{w["name"]}.png')
        wm = copy(w['master'], f'{folder}/{w["name"]}.aseprite')
        (out_dir / folder / 'weapon.json').write_text(
            json.dumps({**w, 'sprite': f'{w["name"]}.png', 'master': f'{w["name"]}.aseprite'}, ensure_ascii=False, indent=2),
            encoding='utf-8'
        )
        weapons_meta[category] = {'name': w['name'], 'sprite': sp, 'master': wm, 'grip': w['grip']}

    matrix = {}
    dir_bases = {}
    for d in DIRECTIONS:
        matrix[d] = {}
        dir_bases[d] = {
            'png128': copy(f'characters/orc-v1/sprites/Directions/orc_v1_dir_{d}.png', f'Direcoes/{d}/base-128.png'),
            'png256': copy(f'characters/orc-v1/source/complete-v1/{d}/Directions/base.png', f'Direcoes/{d}/base-256.png'),
            'master128': copy(f'characters/orc-v1/source/aseprite/complete-v1/native/dir-{d}.aseprite', f'Direcoes/{d}/dir-{d}-128.aseprite'),
            'master256': copy(f'characters/orc-v1/source/aseprite/complete-v1/composite/{d}/dir-base.aseprite', f'Direcoes/{d}/dir-{d}-256.aseprite'),
        }
        for act in ['Idle', 'Walk', 'Unarmed', 'Hit', 'Defeat']:
            c = read(B / d / act / 'clip.json')
            folder = f'Clipes/{d}/{act}'
            frames = []
            for i, f in enumerate(c['frames']):
                png = copy(f['png'], f'{folder}/Quadros/{i:02d}.png')
                nat = copy(f['nativePng'], f'{folder}/Nativo128/{i:02d}.png')
                frames.append({
                    'index': i,
                    'png': png,
                    'nativePng': nat,
                    'durationMs': f['durationMs'],
                    'phase': f['phase'],
                    'weaponVisible': False,
                    'rightGrip': None,
                    'impact': bool(c.get('contactEvent') and c['contactEvent']['frame'] == i),
                    'terminal': bool(c.get('terminal') and c.get('terminalFrame') == i),
                })
            master = copy(c['master'], f'{folder}/{act}.aseprite')
            nat_master = copy(c['nativeMaster'], f'{folder}/{act}-128.aseprite')
            strip = copy(c['strip'], f'{folder}/Folha.png')
            local_clip = {
                **c,
                'master': f'{act}.aseprite',
                'nativeMaster': f'{act}-128.aseprite',
                'strip': 'Folha.png',
                'frames': [{**f, 'png': f'Quadros/{i:02d}.png', 'nativePng': f'Nativo128/{i:02d}.png'} for i, f in enumerate(c['frames'])]
            }
            (out_dir / folder / 'clip.json').write_text(json.dumps(local_clip, ensure_ascii=False, indent=2), encoding='utf-8')
            matrix[d][act] = {
                'action': act,
                'direction': d,
                'label': ACTION_LABELS[act],
                'loop': c['loop'],
                'oneShot': c['oneShot'],
                'terminal': c['terminal'],
                'totalDurationMs': c['totalDurationMs'],
                'master': master,
                'nativeMaster': nat_master,
                'strip': strip,
                'clipJson': f'{folder}/clip.json',
                'frames': frames,
            }

        for cat in ['Sword', 'Axe']:
            c = read(B / d / cat / 'Attack/clip.json')
            prof = read(B / d / cat / 'Attack/profile.json')
            folder = f'Clipes/{d}/{cat}'
            frames = []
            for i, f in enumerate(c['frames']):
                png = copy(f['png'], f'{folder}/Quadros/{i:02d}.png')
                for lk, lv in f['layers'].items():
                    copy(lv['png'], f'{folder}/Camadas/{lk}/{i:02d}.png')
                frames.append({
                    'index': i,
                    'png': png,
                    'durationMs': f['durationMs'],
                    'phase': f['phase'],
                    'weaponVisible': f['weaponVisible'],
                    'rightGrip': f.get('rightGrip'),
                    'rotationDeg': f.get('rotationDeg'),
                    'weaponBehindBody': f.get('weaponBehindBody', False),
                    'impact': bool(c.get('contactEvent') and c['contactEvent']['frame'] == i),
                    'terminal': False,
                })
            master = copy(c['master'], f'{folder}/Ataque.aseprite')
            body_master = copy(c['bodyMaster'], f'{folder}/Corpo.aseprite')
            hand_master = copy(c['handMaster'], f'{folder}/Dedos.aseprite')
            strip = copy(c['strip'], f'{folder}/Folha.png')
            local_clip = {
                **c,
                'master': 'Ataque.aseprite',
                'bodyMaster': 'Corpo.aseprite',
                'handMaster': 'Dedos.aseprite',
                'strip': 'Folha.png',
                'frames': [{
                    **f,
                    'png': f'Quadros/{i:02d}.png',
                    'layers': {lk: {**lv, 'png': f'Camadas/{lk}/{i:02d}.png'} for lk, lv in f['layers'].items()}
                } for i, f in enumerate(c['frames'])]
            }
            local_prof = {
                **prof,
                'bodyMaster': 'Corpo.aseprite',
                'handMaster': 'Dedos.aseprite',
                'frames': [{
                    **f,
                    'body': {**f['body'], 'png': f'Camadas/body/{i:02d}.png'},
                    'handFront': {**f['handFront'], 'png': f'Camadas/handFront/{i:02d}.png'}
                } for i, f in enumerate(prof['frames'])]
            }
            (out_dir / folder / 'clip.json').write_text(json.dumps(local_clip, ensure_ascii=False, indent=2), encoding='utf-8')
            (out_dir / folder / 'profile.json').write_text(json.dumps(local_prof, ensure_ascii=False, indent=2), encoding='utf-8')
            matrix[d][cat] = {
                'action': cat,
                'direction': d,
                'label': ACTION_LABELS[cat],
                'loop': False,
                'oneShot': True,
                'terminal': False,
                'visibleInterval': c['visibleInterval'],
                'totalDurationMs': c['totalDurationMs'],
                'master': master,
                'bodyMaster': body_master,
                'handMaster': hand_master,
                'strip': strip,
                'clipJson': f'{folder}/clip.json',
                'profileJson': f'{folder}/profile.json',
                'frames': frames,
            }

    # Build HTML
    style = '''*{box-sizing:border-box}body{margin:0;background:#142126;color:#e5ece8;font:15px/1.5 system-ui}main{max-width:1920px;margin:auto;padding:22px}a,h3{color:#e2c38c}p{color:#bdcec8}h1{font-size:32px;margin:0 0 8px}h2{font-size:22px;margin:0 0 10px}article{margin:20px 0;padding:18px;background:#22353c;border:1px solid #51696c;border-radius:8px;min-width:0}.toolbar{position:sticky;top:0;z-index:5;background:#15282e;border-bottom:1px solid #68848b;padding:12px;display:flex;gap:12px;align-items:center;flex-wrap:wrap}button,select{font:inherit;padding:7px 10px;color:white;background:#38515b;border:1px solid #789397;border-radius:4px;cursor:pointer}.hero{display:flex;flex-wrap:wrap;gap:24px;align-items:center}.concept{width:192px;height:192px;image-rendering:pixelated}.item{width:144px;height:144px;image-rendering:pixelated}.grid4{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}.studio{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr) 240px;gap:18px}.stage{height:360px;display:flex;justify-content:center;align-items:center;overflow:auto;background:repeating-conic-gradient(#2b3d43 0 25%,#3b5258 0 50%) 0/20px 20px;border-radius:6px}.stage canvas,.stage img{width:256px;height:256px;image-rendering:pixelated;flex-shrink:0}.grip canvas{width:192px;height:192px;image-rendering:pixelated;background:#31464c;border:1px solid #68848b}.gallery{display:flex;flex-wrap:wrap;gap:10px;margin-top:10px}.gallery figure{margin:0;background:#192b31;padding:6px;border-radius:4px}.gallery img{image-rendering:pixelated;width:128px;height:128px}.gallery figcaption{font-size:12px;max-width:128px}.dark .stage{background:#17242b}.light .stage{background:#c4c6b7}table{width:100%;border-collapse:collapse;font-size:14px}th,td{border:1px solid #486167;padding:7px 9px;text-align:left}th{background:#182b31;color:#e2c38c}.badge{display:inline-block;padding:2px 7px;border-radius:4px;background:#2d5a43;color:#d8f3e3;font-size:12px}@media(max-width:1300px){.grid4{grid-template-columns:1fr 1fr}.studio{grid-template-columns:1fr}}'''

    dir_cards = ''.join(
        f'<section><h3>{html.escape(DIR_LABELS[d])}</h3><div class="stage" style="height:200px"><img src="{dir_bases[d]["png128"]}" style="width:128px;height:128px" alt="{d}"></div><p><a href="{dir_bases[d]["png128"]}">PNG 128</a> · <a href="{dir_bases[d]["master128"]}">Aseprite 128</a> · <a href="{dir_bases[d]["master256"]}">Aseprite 256</a></p></section>'
        for d in DIRECTIONS
    )

    dir_stage_cards = ''.join(
        f'<section><h3>{html.escape(DIR_LABELS[d])}</h3><div class="stage"><canvas id="dir-canvas-{d}" width="256" height="256"></canvas></div><p id="dir-info-{d}"></p><p id="dir-links-{d}"></p></section>'
        for d in DIRECTIONS
    )

    table_rows = []
    for act in ACTIONS:
        for d in DIRECTIONS:
            cell = matrix[d][act]
            vis = f'Quadros {cell["visibleInterval"][0]+1}..{cell["visibleInterval"][1]+1}' if cell.get('visibleInterval') else 'Oculta (sem arma)'
            sem = 'Loop contínuo' if cell['loop'] else ('One-shot Terminal' if cell['terminal'] else 'One-shot → Idle')
            table_rows.append(
                f'<tr><td><strong>{act}</strong></td><td><code>{d}</code></td><td>{len(cell["frames"])}</td><td>{cell["totalDurationMs"]} ms</td><td>{sem}</td><td>{vis}</td><td><span class="badge">TECHNICALLY_COMPLETE</span> <span class="badge" style="background:#5a4622;color:#f7e2b8">VISUAL_REVIEW_REQUIRED</span></td><td><a href="{cell["master"]}">Aseprite</a> · <a href="{cell["strip"]}">Folha</a> · <a href="{cell["clipJson"]}">clip.json</a></td></tr>'
            )

    before_after_section = f'''
  <article>
    <h2>Comparação Visual Antes (v1 Rejeitada) vs Depois (Recuperação Artística)</h2>
    <p>Evidência direta lado a lado da recuperação artística sobre os 4 pontos apontados pelo criador: (1) reconstrução integral das vistas traseiras 3/4 (<code>back_r</code> / <code>back_l</code>) e de todas as 14 animações de costas com dorsal real, nuca/occipital, colar elevado, faixa carmesim horizontal traseira e grevas posteriores; (2) remoção cirúrgica do halo claro no contorno do crânio verde nos ataques frontais; (3) reação <code>Hit</code> pesada e legível com recuo e guarda; (4) queda <code>Defeat</code> volumétrica em 5 estágios sem esmagamento vertical artificial.</p>
    <div class="grid4" style="grid-template-columns:repeat(2,minmax(0,1fr))">
      <section>
        <h3>1A. Base Traseira <code>back_r</code> (NE) — Antes (Frente apagada) vs Depois (Costas 3/4 real)</h3>
        <div class="stage" style="height:220px;gap:24px">
          <figure style="margin:0;text-align:center"><img src="AntesDepois/dir_back_r_before.png" style="width:128px;height:128px" alt="Antes back_r"><figcaption style="font-size:12px;color:#f2a6a6">ANTES (Rejeitado: peitoral frontal)</figcaption></figure>
          <figure style="margin:0;text-align:center"><img src="{dir_bases['back_r']['png128']}" style="width:128px;height:128px" alt="Depois back_r"><figcaption style="font-size:12px;color:#a8f0c6">DEPOIS (Costas 3/4 NE + dorsal)</figcaption></figure>
        </div>
      </section>
      <section>
        <h3>1B. Base Traseira <code>back_l</code> (NW) — Antes (Frente apagada) vs Depois (Costas 3/4 real)</h3>
        <div class="stage" style="height:220px;gap:24px">
          <figure style="margin:0;text-align:center"><img src="AntesDepois/dir_back_l_before.png" style="width:128px;height:128px" alt="Antes back_l"><figcaption style="font-size:12px;color:#f2a6a6">ANTES (Rejeitado: peitoral frontal)</figcaption></figure>
          <figure style="margin:0;text-align:center"><img src="{dir_bases['back_l']['png128']}" style="width:128px;height:128px" alt="Depois back_l"><figcaption style="font-size:12px;color:#a8f0c6">DEPOIS (Costas 3/4 NW + dorsal)</figcaption></figure>
        </div>
      </section>
      <section>
        <h3>2A. <code>back_r</code> Walk (16 quadros) — Antes vs Depois</h3>
        <p style="font-size:13px"><strong>Antes (Rejeitado):</strong> <a href="AntesDepois/back_r_walk_strip_before.png">Folha Antes</a></p>
        <div style="overflow-x:auto;background:#192b31;padding:8px;border-radius:6px"><img src="AntesDepois/back_r_walk_strip_before.png" style="height:96px;image-rendering:pixelated" alt="Walk back_r antes"></div>
        <p style="font-size:13px"><strong>Depois (Costas 3/4 real com marcha dorsal):</strong> <a href="{matrix['back_r']['Walk']['strip']}">Folha Depois</a></p>
        <div style="overflow-x:auto;background:#192b31;padding:8px;border-radius:6px"><img src="{matrix['back_r']['Walk']['strip']}" style="height:96px;image-rendering:pixelated" alt="Walk back_r depois"></div>
      </section>
      <section>
        <h3>2B. <code>back_r</code> Sword Attack (13 quadros) — Antes vs Depois</h3>
        <p style="font-size:13px"><strong>Antes (Rejeitado):</strong> <a href="AntesDepois/back_r_sword_strip_before.png">Folha Antes</a></p>
        <div style="overflow-x:auto;background:#192b31;padding:8px;border-radius:6px"><img src="AntesDepois/back_r_sword_strip_before.png" style="height:96px;image-rendering:pixelated" alt="Sword back_r antes"></div>
        <p style="font-size:13px"><strong>Depois (Costas 3/4 real + golpe para NE além do dorso):</strong> <a href="{matrix['back_r']['Sword']['strip']}">Folha Depois</a></p>
        <div style="overflow-x:auto;background:#192b31;padding:8px;border-radius:6px"><img src="{matrix['back_r']['Sword']['strip']}" style="height:96px;image-rendering:pixelated" alt="Sword back_r depois"></div>
      </section>
      <section>
        <h3>3. Reação <code>Hit</code> (5 quadros · <code>front_r</code> e <code>back_r</code>) — Antes (Tremor 2px) vs Depois (Impacto Pesado + Guarda)</h3>
        <p style="font-size:13px"><strong>Antes (<code>front_r</code> / <code>back_r</code>):</strong> <a href="AntesDepois/front_r_hit_strip_before.png">front_r Antes</a> · <a href="AntesDepois/back_r_hit_strip_before.png">back_r Antes</a></p>
        <div style="overflow-x:auto;background:#192b31;padding:8px;border-radius:6px"><img src="AntesDepois/front_r_hit_strip_before.png" style="height:96px;image-rendering:pixelated" alt="Hit front_r antes"></div>
        <p style="font-size:13px"><strong>Depois (Recuo de cabeça/tronco, guarda de manopla e compressão de joelhos):</strong> <a href="{matrix['front_r']['Hit']['strip']}">front_r Depois</a> · <a href="{matrix['back_r']['Hit']['strip']}">back_r Depois</a></p>
        <div style="overflow-x:auto;background:#192b31;padding:8px;border-radius:6px"><img src="{matrix['front_r']['Hit']['strip']}" style="height:96px;image-rendering:pixelated" alt="Hit front_r depois"></div>
      </section>
      <section>
        <h3>4. Coreografia <code>Defeat</code> (5 quadros · <code>front_r</code> e <code>back_r</code>) — Antes (Sprite em pé achatado/rotacionado) vs Depois (Colapso Volumétrico em 5 Estágios)</h3>
        <p style="font-size:13px"><strong>Antes (Rejeitado: rotação afim + squash vertical):</strong> <a href="AntesDepois/front_r_defeat_strip_before.png">front_r Antes</a> · <a href="AntesDepois/back_r_defeat_strip_before.png">back_r Antes</a></p>
        <div style="overflow-x:auto;background:#192b31;padding:8px;border-radius:6px"><img src="AntesDepois/front_r_defeat_strip_before.png" style="height:96px;image-rendering:pixelated" alt="Defeat front_r antes"></div>
        <p style="font-size:13px"><strong>Depois (Queda progressiva: desequilíbrio → joelhos cedem → apoio no solo → impacto → pose caída com volume 3D):</strong> <a href="{matrix['front_r']['Defeat']['strip']}">front_r Depois</a> · <a href="{matrix['back_r']['Defeat']['strip']}">back_r Depois</a></p>
        <div style="overflow-x:auto;background:#192b31;padding:8px;border-radius:6px"><img src="{matrix['front_r']['Defeat']['strip']}" style="height:96px;image-rendering:pixelated" alt="Defeat front_r depois"></div>
      </section>
    </div>
    <section style="margin-top:16px">
      <h3>5. Limpeza Cirúrgica do Contorno Frontal da Cabeça (<code>front_r</code> Sword Quadro 08 / índice 07)</h3>
      <div class="stage" style="height:220px;gap:32px">
        <figure style="margin:0;text-align:center"><img src="AntesDepois/front_r_sword_07_halo_before.png" style="width:192px;height:192px" alt="Antes halo"><figcaption style="font-size:12px;color:#f2a6a6">ANTES (Halo claro cinza no topo da cabeça)</figcaption></figure>
        <figure style="margin:0;text-align:center"><img src="{matrix['front_r']['Sword']['frames'][7]['png']}" style="width:192px;height:192px" alt="Depois sem halo"><figcaption style="font-size:12px;color:#a8f0c6">DEPOIS (Contorno escuro limpo · 0px halo)</figcaption></figure>
      </div>
    </section>
  </article>'''

    script = r'''
const DIRECTIONS = ['front_r', 'front_l', 'back_r', 'back_l'];
let playing = true, loop = true, speed = 1, zoom = 1.25;
let selectedDir = 'front_r', selectedAction = 'Sword', transitionMode = 'action-only';
let lastTime = 0, ready = false;
const cache = new Map();
const mainState = { n: 0, time: 0, done: false };
const dirStates = Object.fromEntries(DIRECTIONS.map(d => [d, { n: 0, time: 0, done: false }]));

function loadImg(p) {
  if (!cache.has(p)) {
    cache.set(p, new Promise((ok, no) => {
      const im = new Image();
      im.onload = () => ok(im);
      im.onerror = () => no(new Error('Imagem ausente: ' + p));
      im.src = p;
    }));
  }
  return cache.get(p);
}

function buildSequence(dir, action, mode) {
  const idle = matrix[dir].Idle.frames.map(f => ({ ...f, seqState: 'Idle' }));
  const walk = matrix[dir].Walk.frames.map(f => ({ ...f, seqState: 'Walk' }));
  const actFrames = matrix[dir][action].frames.map(f => ({ ...f, seqState: action }));
  if (mode === 'idle-attack-idle') {
    const target = ['Sword', 'Axe', 'Unarmed'].includes(action) ? actFrames : matrix[dir].Sword.frames.map(f => ({ ...f, seqState: 'Sword' }));
    return { frames: [...idle, ...target, ...idle], isTerminal: false };
  }
  if (mode === 'walk-idle') {
    return { frames: [...walk, ...idle], isTerminal: false };
  }
  if (mode === 'hit-idle') {
    const hit = matrix[dir].Hit.frames.map(f => ({ ...f, seqState: 'Hit' }));
    return { frames: [...hit, ...idle], isTerminal: false };
  }
  if (mode === 'defeat-terminal') {
    const def = matrix[dir].Defeat.frames.map(f => ({ ...f, seqState: 'Defeat' }));
    return { frames: def, isTerminal: true };
  }
  return { frames: actFrames, isTerminal: matrix[dir][action].terminal };
}

async function renderMain() {
  const seq = buildSequence(selectedDir, selectedAction, transitionMode);
  const fs = seq.frames;
  mainState.n = Math.min(mainState.n, fs.length - 1);
  const f = fs[mainState.n];
  const im = await loadImg(f.png);
  const c = document.getElementById('main-canvas');
  const ctx = c.getContext('2d');
  ctx.imageSmoothingEnabled = false;
  ctx.clearRect(0, 0, 256, 256);
  ctx.drawImage(im, 0, 0);
  c.style.outline = f.impact ? '2px solid #e2b659' : (f.terminal ? '2px solid #d96b6b' : 'none');

  document.getElementById('main-info').textContent =
    `[${selectedDir}] ${f.seqState} · Quadro ${mainState.n + 1}/${fs.length} · ${f.durationMs} ms · ${f.phase}` +
    (f.impact ? ' · IMPACTO VISUAL' : '') +
    (f.terminal ? ' · POSE TERMINAL (Defeat)' : '') +
    ` · ${f.weaponVisible ? 'arma visível' : 'sem arma'}`;

  const g = document.getElementById('main-grip');
  const gc = g.getContext('2d');
  gc.imageSmoothingEnabled = false;
  gc.clearRect(0, 0, 24, 24);
  const pos = f.rightGrip || [128, 128];
  gc.drawImage(im, pos[0] - 12, pos[1] - 12, 24, 24, 0, 0, 24, 24);

  const cell = matrix[selectedDir][selectedAction];
  const gallery = document.getElementById('frame-gallery');
  if (gallery.dataset.key !== `${selectedDir}-${selectedAction}`) {
    gallery.dataset.key = `${selectedDir}-${selectedAction}`;
    gallery.innerHTML = cell.frames.map((fr, idx) =>
      `<figure><a href="${fr.png}"><img src="${fr.png}" alt="Quadro ${idx+1}"></a><figcaption>#${idx+1} · ${fr.phase} · ${fr.durationMs} ms · ${fr.weaponVisible ? 'arma' : 'sem arma'}</figcaption></figure>`
    ).join('');
  }
}

async function renderDirCard(d) {
  const seq = buildSequence(d, selectedAction, transitionMode);
  const fs = seq.frames;
  const st = dirStates[d];
  st.n = Math.min(st.n, fs.length - 1);
  const f = fs[st.n];
  const im = await loadImg(f.png);
  const c = document.getElementById('dir-canvas-' + d);
  const ctx = c.getContext('2d');
  ctx.imageSmoothingEnabled = false;
  ctx.clearRect(0, 0, 256, 256);
  ctx.drawImage(im, 0, 0);
  c.style.outline = f.impact ? '2px solid #e2b659' : (f.terminal ? '2px solid #d96b6b' : 'none');
  document.getElementById('dir-info-' + d).textContent =
    `${f.seqState} ${st.n + 1}/${fs.length} · ${f.durationMs} ms · ${f.weaponVisible ? 'arma visível' : 'sem arma'}`;
  const cell = matrix[d][selectedAction];
  document.getElementById('dir-links-' + d).innerHTML =
    `<a href="${cell.master}">Aseprite</a> · <a href="${cell.strip}">Folha</a> · <a href="${cell.clipJson}">clip.json</a>`;
}

function renderAll() {
  renderMain();
  DIRECTIONS.forEach(renderDirCard);
}

function resetPlayback() {
  mainState.n = 0; mainState.time = 0; mainState.done = false;
  DIRECTIONS.forEach(d => { dirStates[d].n = 0; dirStates[d].time = 0; dirStates[d].done = false; });
  lastTime = 0;
  renderAll();
}

function advanceState(st, seq, dt) {
  if (st.done) return false;
  const fs = seq.frames;
  st.time += dt;
  let changed = false;
  while (st.time >= fs[st.n].durationMs && !st.done) {
    st.time -= fs[st.n].durationMs;
    if (st.n === fs.length - 1) {
      if (loop && !seq.isTerminal) {
        st.n = 0;
      } else {
        st.done = true;
        st.time = 0;
      }
    } else {
      st.n++;
    }
    changed = true;
  }
  return changed;
}

document.getElementById('play').onclick = () => {
  playing = !playing;
  document.getElementById('play').textContent = playing ? 'Pausar' : 'Reproduzir';
};
document.getElementById('reset').onclick = resetPlayback;
document.getElementById('step-prev').onclick = () => {
  playing = false;
  document.getElementById('play').textContent = 'Reproduzir';
  const seq = buildSequence(selectedDir, selectedAction, transitionMode);
  mainState.done = false;
  mainState.n = (mainState.n - 1 + seq.frames.length) % seq.frames.length;
  DIRECTIONS.forEach(d => {
    const s = buildSequence(d, selectedAction, transitionMode);
    dirStates[d].done = false;
    dirStates[d].n = (dirStates[d].n - 1 + s.frames.length) % s.frames.length;
  });
  renderAll();
};
document.getElementById('step-next').onclick = () => {
  playing = false;
  document.getElementById('play').textContent = 'Reproduzir';
  const seq = buildSequence(selectedDir, selectedAction, transitionMode);
  mainState.done = false;
  mainState.n = (mainState.n + 1) % seq.frames.length;
  DIRECTIONS.forEach(d => {
    const s = buildSequence(d, selectedAction, transitionMode);
    dirStates[d].done = false;
    dirStates[d].n = (dirStates[d].n + 1) % s.frames.length;
  });
  renderAll();
};

document.getElementById('select-dir').onchange = e => { selectedDir = e.target.value; resetPlayback(); };
document.getElementById('select-action').onchange = e => { selectedAction = e.target.value; resetPlayback(); };
document.getElementById('select-transition').onchange = e => {
  transitionMode = e.target.value;
  if (transitionMode === 'defeat-terminal') {
    selectedAction = 'Defeat';
    document.getElementById('select-action').value = 'Defeat';
  } else if (transitionMode === 'hit-idle') {
    selectedAction = 'Hit';
    document.getElementById('select-action').value = 'Hit';
  } else if (transitionMode === 'walk-idle') {
    selectedAction = 'Walk';
    document.getElementById('select-action').value = 'Walk';
  }
  resetPlayback();
};
document.getElementById('speed').onchange = e => { speed = Number(e.target.value); };
document.getElementById('loop').onchange = e => {
  loop = e.target.checked;
  mainState.done = false;
  DIRECTIONS.forEach(d => dirStates[d].done = false);
};
document.getElementById('zoom').onchange = e => {
  zoom = Number(e.target.value);
  document.querySelectorAll('.stage canvas').forEach(c => {
    c.style.width = c.style.height = Math.round(256 * zoom) + 'px';
  });
  document.querySelectorAll('.stage').forEach(s => {
    if (!s.style.height || parseInt(s.style.height, 10) > 220) {
      s.style.height = Math.round(256 * zoom + 32) + 'px';
    }
  });
};
document.getElementById('bg').onchange = e => { document.body.className = e.target.value; };

const allUrls = [];
for (const d of DIRECTIONS) {
  for (const act of Object.keys(matrix[d])) {
    for (const f of matrix[d][act].frames) allUrls.push(f.png);
  }
}
Promise.all(allUrls.map(loadImg)).then(() => {
  renderAll();
  ready = true;
  document.body.dataset.ready = 'true';
});

function tick(t) {
  const dt = lastTime ? Math.min(100, t - lastTime) * speed : 0;
  lastTime = t;
  if (ready && playing) {
    if (advanceState(mainState, buildSequence(selectedDir, selectedAction, transitionMode), dt)) {
      renderMain();
    }
    for (const d of DIRECTIONS) {
      if (advanceState(dirStates[d], buildSequence(d, selectedAction, transitionMode), dt)) {
        renderDirCard(d);
      }
    }
  }
  requestAnimationFrame(tick);
}
requestAnimationFrame(tick);
'''

    item_cards = ''.join(
        f'<section><h3>{html.escape(w["name"])} · asset independente</h3><img class="item" src="{w["sprite"]}" alt="{html.escape(w["name"])}"><p><a href="{w["sprite"]}">PNG 96×96</a> · <a href="{w["master"]}">Mestre Aseprite</a></p></section>'
        for w in weapons_meta.values()
    )

    page = f'''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Orc V1 · Biblioteca Completa de Animações (4 Vistas × 7 Ações)</title>
<style>{style}</style>
<main>
  <h1>Orc V1 (Verde Warcraft) · Biblioteca Completa 4 Vistas × 7 Ações</h1>
  <p>Pacote completo de produção local e candidato de revisão artística: 4 direções (<code>front_r</code>, <code>front_l</code>, <code>back_r</code>, <code>back_l</code>) × 7 ações (<code>Idle</code>, <code>Walk</code>, <code>Unarmed Attack</code>, <code>Sword Attack</code>, <code>Axe Attack</code>, <code>Hit</code>, <code>Defeat</code>). Política <code>attack-only-v1</code>: armas ocultas fora do ataque. Status técnico: <span class="badge">TECHNICALLY_COMPLETE</span> · Status artístico: <span class="badge" style="background:#5a4622;color:#f7e2b8">VISUAL_REVIEW_REQUIRED</span> · Aprovação: <span class="badge" style="background:#38515b">PENDING_CREATOR</span>.</p>
  <p><a href="../../index.html">Biblioteca de Arte</a> · <a href="DOCUMENTACAO.md">Documentação</a> · <a href="PORTOES-QUALIDADE-ARTISTICA.md">Portões de Qualidade Artística (10 Lições)</a> · <a href="artistic-quality-gates-v1.json">Contrato JSON de Portões</a> · <a href="PADRAO-DE-ARMAS.md">Padrão de Armas</a> · <a href="PADRAO-DE-IDLE.md">Padrão de Idle</a> · <a href="MATRIZ-COBERTURA.json">Matriz de Cobertura (JSON)</a></p>

  <div class="toolbar">
    <button id="play">Pausar</button>
    <button id="reset">Reiniciar</button>
    <button id="step-prev">◀ Quadro</button>
    <button id="step-next">Quadro ▶</button>
    <label>Direção
      <select id="select-dir">
        <option value="front_r">front_r (Frente-Direita · SE)</option>
        <option value="front_l">front_l (Frente-Esquerda · SW)</option>
        <option value="back_r">back_r (Costas-Direita · NE)</option>
        <option value="back_l">back_l (Costas-Esquerda · NW)</option>
      </select>
    </label>
    <label>Ação
      <select id="select-action">
        <option value="Idle">Idle (5f · 2200 ms · sem arma)</option>
        <option value="Walk">Walk (16f · 1280 ms · sem arma)</option>
        <option value="Unarmed">Unarmed Attack (5f · 450 ms · sem arma)</option>
        <option value="Sword" selected>Sword Attack (13f · 730 ms · Espada)</option>
        <option value="Axe">Axe Attack (12f · 1005 ms · Machado)</option>
        <option value="Hit">Hit (5f · 450 ms · reação sem arma)</option>
        <option value="Defeat">Defeat (5f · 700 ms · queda terminal)</option>
      </select>
    </label>
    <label>Transição / Estado
      <select id="select-transition">
        <option value="action-only">Clipe isolado da ação</option>
        <option value="idle-attack-idle" selected>Idle → Attack → Idle (transição armada/desarmada)</option>
        <option value="walk-idle">Walk → Idle (parada de locomoção)</option>
        <option value="hit-idle">Hit → Idle (recuperação de dano)</option>
        <option value="defeat-terminal">Defeat → Pose Terminal (sem retorno ao Idle)</option>
      </select>
    </label>
    <label>Velocidade
      <select id="speed">
        <option value="1" selected>1×</option>
        <option value="0.5">0,5×</option>
        <option value="0.25">0,25×</option>
      </select>
    </label>
    <label>Zoom
      <select id="zoom">
        <option value="1">1× (256px)</option>
        <option value="1.25" selected>1,25× (320px)</option>
        <option value="2">2× (512px)</option>
      </select>
    </label>
    <label>Fundo
      <select id="bg">
        <option value="">Xadrez transparência</option>
        <option value="dark">Escuro</option>
        <option value="light">Claro</option>
      </select>
    </label>
    <label><input type="checkbox" id="loop" checked> Repetir revisão (exceto Defeat terminal)</label>
  </div>

  <article class="hero">
    <section>
      <h3>Conceito Selecionado · Orc V1</h3>
      <img class="concept" src="{concept}" alt="Orc V1 Verde Warcraft">
      <p><a href="{concept}">PNG</a> · <a href="{concept_master}">Mestre Aseprite</a></p>
    </section>
    {item_cards}
  </article>

  <article>
    <h2>Inspeção Principal e Transição de Estados</h2>
    <div class="studio">
      <section>
        <h3>Palco Principal (256×256 com registro unificado groundY=190 / nativo 128×128 groundY=126)</h3>
        <div class="stage"><canvas id="main-canvas" width="256" height="256"></canvas></div>
        <p id="main-info"></p>
      </section>
      <section>
        <h3>Quadros do Clipe Selecionado</h3>
        <div id="frame-gallery" class="gallery"></div>
      </section>
      <section class="grip">
        <h3>Pegada / Ponto Focal · 8×</h3>
        <canvas id="main-grip" width="24" height="24"></canvas>
        <p>Recorte 24×24 sem interpolação ao redor do socket da mão direita.</p>
      </section>
    </div>
  </article>

  <article>
    <h2>Comparação Simultânea das 4 Direções (front_r, front_l, back_r, back_l)</h2>
    <p>As quatro câmeras executam sincronizadamente a ação/transição selecionada na barra superior, preservando mão direita dominante, ombreira direita de 3 espinhos e iluminação superior-esquerda.</p>
    <div class="grid4">{dir_stage_cards}</div>
  </article>

  <article>
    <h2>Fundações Direcionais Estáticas (4 Vistas · Sem Arma)</h2>
    <div class="grid4">{dir_cards}</div>
  </article>

  {before_after_section}

  <article>
    <h2>Matriz Completa de Cobertura (28 Clipes = 4 Direções × 7 Ações)</h2>
    <table>
      <thead>
        <tr><th>Ação</th><th>Direção</th><th>Quadros</th><th>Duração</th><th>Semântica</th><th>Visibilidade de Arma</th><th>Status</th><th>Fontes e Metadados</th></tr>
      </thead>
      <tbody>
        {''.join(table_rows)}
      </tbody>
    </table>
  </article>
</main>
<script>
const matrix = {json.dumps(matrix, ensure_ascii=False)};
{script}
</script>
</html>'''

    (out_dir / 'index.html').write_text(page, encoding='utf-8')
    (out_dir / 'catalogo.json').write_text(json.dumps({
        'revision': 'main-orc-complete-v1',
        'character': 'orc-v1',
        'directions': DIRECTIONS,
        'actions': ACTIONS,
        'files': files,
        'technicalStatus': 'TECHNICALLY_COMPLETE',
        'artisticStatus': 'VISUAL_REVIEW_REQUIRED',
        'artisticApproval': 'PENDING_CREATOR',
        'qualityGatesContract': 'artistic-quality-gates-v1.json',
        'runtimeImplemented': False,
    }, ensure_ascii=False, indent=2), encoding='utf-8')
    (out_dir / 'LEIA-ME.md').write_text((R / 'docs/MAIN_ORC_COMBAT_POLISH.md').read_text(encoding='utf-8'), encoding='utf-8')
    return {'page': str(out_dir / 'index.html'), 'copiedFiles': len(files)}

res_main = build_review_target(L / 'Personagens Jogaveis/Orc V1', False)
res_comp = build_review_target(L / 'Estudos Comparativos/Orc principal - Biblioteca completa', True)

comp_reg_path = R / 'docs/ART_LIBRARY_COMPARISONS.json'
reg = read(comp_reg_path)
reg = [v for v in reg if v['id'] != 'main-orc-complete-v1']
reg.insert(0, {
    'id': 'main-orc-complete-v1',
    'title': 'Orc principal · biblioteca completa 4 vistas × 7 ações (candidato)',
    'path': 'Estudos Comparativos/Orc principal - Biblioteca completa/index.html',
    'builder': 'tools/build-main-orc-complete-review.py'
})
comp_reg_path.write_text(json.dumps(reg, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'mainPage': res_main, 'comparativePage': res_comp}, ensure_ascii=False))
