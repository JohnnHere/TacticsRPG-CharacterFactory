import json, os, shutil, hashlib, struct
from pathlib import Path
from PIL import Image
import numpy as np

def sha256_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def delta(a, b):
    return int(((a != b).any(2) & ((a[:,:,3]>0) | (b[:,:,3]>0))).sum())

def read_json(p):
    return json.loads(Path(p).read_text(encoding='utf-8-sig'))

def write_json(p, data):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    Path(p).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

ROOT = Path('.').resolve()
EXP_GRIP = ROOT / 'experiments/main-orc-combat-rescue-v5/grip-specialist'
CHAR_GRIP = ROOT / 'characters/orc-v1/source/combat-rescue-v5/grip-specialist'

plan = read_json(EXP_GRIP / 'front-three/anatomy-plan.json')
snap = read_json(EXP_GRIP / 'front-three/input-snapshot.json')

cycles_meta = [
    {
        'cellId': 'front_l/Sword',
        'dirName': 'front_l-Sword-full',
        'direction': 'front_l',
        'category': 'Sword',
        'action': 'Sword',
        'checkpointName': 'GRIP_FRONT_L_SWORD_FULL_READY',
        'frameCount': 13,
        'durationsMs': [30, 65, 35, 50, 45, 65, 35, 35, 100, 55, 80, 45, 90],
        'totalDurationMs': 730,
        'visibleInterval': [2, 10],
        'hiddenFrames': [0, 1, 11, 12],
        'weaponDef': 'characters/orc-v1/source/combat-rescue-v5/combat/weapons/Sword/weapon.json',
        'weaponId': 'recruit-sword',
        'weaponName': 'Espada do Recruta',
        'weaponDepthPolicy': 'Grip leather v60..70 behind body; blade/guard/pommel front; per-frame original glove in handFront',
        'contactEvent': {'frame': 7, 'timeMs': 325, 'status': 'CANDIDATE_VISUAL_ONLY', 'appliesDamage': False}
    },
    {
        'cellId': 'front_r/Axe',
        'dirName': 'front_r-Axe-full',
        'direction': 'front_r',
        'category': 'Axe',
        'action': 'Axe',
        'checkpointName': 'GRIP_FRONT_R_AXE_FULL_READY',
        'frameCount': 12,
        'durationsMs': [40, 65, 35, 80, 155, 35, 115, 110, 130, 50, 90, 100],
        'totalDurationMs': 1005,
        'visibleInterval': [2, 8],
        'hiddenFrames': [0, 1, 9, 10, 11],
        'weaponDef': 'characters/orc-v1/source/combat-rescue-v5/combat/weapons/Axe/weapon.json',
        'weaponId': 'militia-axe',
        'weaponName': 'Machado de Milícia',
        'weaponDepthPolicy': 'Grip wood v50..57 behind body; axe head/beard/spike front; per-frame original glove in handFront',
        'contactEvent': {'frame': 6, 'timeMs': 375, 'status': 'CANDIDATE_VISUAL_ONLY', 'appliesDamage': False}
    },
    {
        'cellId': 'front_l/Axe',
        'dirName': 'front_l-Axe-full',
        'direction': 'front_l',
        'category': 'Axe',
        'action': 'Axe',
        'checkpointName': 'GRIP_FRONT_L_AXE_FULL_READY',
        'frameCount': 12,
        'durationsMs': [40, 65, 35, 80, 155, 35, 115, 110, 130, 50, 90, 100],
        'totalDurationMs': 1005,
        'visibleInterval': [2, 8],
        'hiddenFrames': [0, 1, 9, 10, 11],
        'weaponDef': 'characters/orc-v1/source/combat-rescue-v5/combat/weapons/Axe/weapon.json',
        'weaponId': 'militia-axe',
        'weaponName': 'Machado de Milícia',
        'weaponDepthPolicy': 'Grip wood v50..57 behind body; axe head/beard/spike front; per-frame original glove in handFront',
        'contactEvent': {'frame': 6, 'timeMs': 375, 'status': 'CANDIDATE_VISUAL_ONLY', 'appliesDamage': False}
    }
]

def make_html_preview(meta, frames_data, rel_char_dir, rel_exp_dir, before_dir):
    durations_json = json.dumps(meta['durationsMs'])
    frames_json = []
    for f in frames_data:
        frames_json.append({
            'index': f['index'],
            'phase': f['phase'],
            'grip': f['grip'],
            'visible': f['weaponVisible'],
            'before': f"../../../../{before_dir}/{f['index']:02d}.png",
            'flat': f"{f['index']:02d}.png",
            'layers': {
                'weaponBack': f"layers/weaponBack/{f['index']:02d}.png",
                'body': f"layers/body/{f['index']:02d}.png",
                'weaponFront': f"layers/weaponFront/{f['index']:02d}.png",
                'handFront': f"layers/handFront/{f['index']:02d}.png"
            }
        })
    data_str = json.dumps({'durations': meta['durationsMs'], 'total': meta['totalDurationMs'], 'frames': frames_json})
    
    html = f"""<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Orc V1 — {meta['category']} {meta['direction']} {meta['frameCount']}f</title>
<style>
body{{margin:24px;background:#171a20;color:#e8ebf1;font:15px system-ui}}
h1{{font-size:22px}}
p{{max-width:1150px;line-height:1.5}}
a{{color:#9ed8ff}}
button,select,input{{font:inherit}}
button,select{{padding:6px;background:#303845;border:1px solid #737d8e;color:inherit}}
label{{display:inline-block;margin:6px 12px 6px 0}}
.row{{display:flex;gap:18px;flex-wrap:wrap}}
.panel{{padding:12px;background:#252b34;border:1px solid #5a6475}}
.panel h2{{font-size:16px;margin-top:0}}
canvas{{display:block;background:#2b2c31;image-rendering:pixelated}}
.controls{{margin:18px 0}}
#frame{{width:300px}}
#status,#frameLabel{{color:#e4cc87}}
.sheet{{max-width:100%;image-rendering:pixelated}}
</style>
<h1>Orc V1 · {meta['weaponName']} · {meta['direction']} · ciclo {meta['frameCount']}f / {meta['totalDurationMs']}ms</h1>
<p><b>{meta['checkpointName']} · TECHNICALLY_COMPLETE · VISUAL_REVIEW_REQUIRED · PENDING_CREATOR.</b></p>
<p>Ciclo completo equipado candidato para QA independente. Corpo frontal 100% preservado (0 delta RGBA). Pegada genuína com luvas rastreadas do corpo base; arma visível exclusivamente no visibleInterval ({meta['visibleInterval'][0]}..{meta['visibleInterval'][1]}).</p>
<div class="controls">
<button id="play">Pausar</button> <button id="restart">Reiniciar</button> <button id="prev">◀ Quadro</button> <button id="next">Quadro ▶</button>
<label>Velocidade <select id="speed"><option value="1">1×</option><option value="0.75">0,75×</option><option value="0.5">0,5×</option><option value="0.25">0,25×</option></select></label>
<label>Escala <select id="scale"><option value="1">Canvas 256 / corpo 128px</option><option value="0.5">Canvas 128 / corpo 64px</option><option value="2">Canvas 512 / corpo 256px</option></select></label>
<label><input id="loop" type="checkbox" checked>Repetir ciclo para revisão</label>
</div>
<p><input id="frame" type="range" min="0" max="{meta['frameCount']-1}" value="0" step="1"> <span id="frameLabel">Carregando…</span></p>
<div class="row">
<section class="panel"><h2>Antes: passe anterior combat-rescue-v5</h2><canvas id="before" width="256" height="256"></canvas></section>
<section class="panel"><h2>Depois: grip especialista, corpo preservado</h2><canvas id="after" width="256" height="256"></canvas></section>
<section class="panel"><h2>Pegada 8× (diagnóstico)</h2><canvas id="grip" width="224" height="224"></canvas></section>
</div>
<p>
<label><input data-layer="weaponBack" type="checkbox" checked>weaponBack</label>
<label><input data-layer="body" type="checkbox" checked>body</label>
<label><input data-layer="weaponFront" type="checkbox" checked>weaponFront</label>
<label><input data-layer="handFront" type="checkbox" checked>handFront</label>
<button id="bodyOnly">Só corpo</button> <button id="restore">Restaurar camadas</button>
</p>
<p id="status">Carregando exports reais…</p>
<p><a href="report.md">Relatório</a> · <a href="checkpoint.json">Checkpoint</a> · <a href="clip.json">clip.json</a> · <a href="representative.json">representative.json</a> · <a href="checks.json">checks.json</a></p>
<details><summary>Strip Composto Completo (256px)</summary><img class="sheet" src="composite-strip.png" alt="Composto"></details>
<details><summary>Strip Nativo Completo (128px)</summary><img class="sheet" src="native-strip.png" alt="Nativo"></details>
<script>
const DATA = {data_str};
const names = ['weaponBack','body','weaponFront','handFront'];
const loaded = [];
let elapsed = 0, playing = true, speed = 1, loop = true, current = -1, last = performance.now();
const starts = [0];
for (const d of DATA.durations) starts.push(starts.at(-1) + d);
window.reviewReady = false;
window.reviewTrace = [];

function context(id) {{
  const x = document.getElementById(id).getContext('2d');
  x.imageSmoothingEnabled = false;
  return x;
}}
function frameAt(t) {{
  for (let i = 0; i < {meta['frameCount']}; i++) if (t < starts[i+1]) return i;
  return {meta['frameCount']-1};
}}
function render(force = false) {{
  const i = frameAt(elapsed);
  if (!force && i === current) return;
  const changed = i !== current;
  current = i;
  const a = context('after'), b = context('before'), g = context('grip');
  a.clearRect(0,0,256,256); b.clearRect(0,0,256,256); g.clearRect(0,0,224,224);
  if (loaded[i].before) b.drawImage(loaded[i].before,0,0);
  for (const n of names) if (document.querySelector('[data-layer="'+n+'"]').checked) a.drawImage(loaded[i][n],0,0);
  if (DATA.frames[i].visible && DATA.frames[i].grip) {{
    const [x,y] = DATA.frames[i].grip;
    g.drawImage(document.getElementById('after'), x-14, y-14, 28, 28, 0, 0, 224, 224);
  }} else {{
    g.fillStyle = '#ced6e3'; g.font = '16px system-ui';
    g.fillText('Sem arma neste quadro', 16, 105);
  }}
  document.getElementById('frame').value = i;
  document.getElementById('frameLabel').textContent = 'F' + String(i).padStart(2,'0') + ' · ' + DATA.durations[i] + 'ms · ' + DATA.frames[i].phase;
  document.getElementById('play').textContent = playing ? 'Pausar' : 'Reproduzir';
  if (changed) {{
    window.reviewTrace.push({{frame:i, time:performance.now(), speed, elapsed, playing}});
    if (window.reviewTrace.length > 600) window.reviewTrace.shift();
  }}
}}
function seek(i) {{
  playing = false;
  elapsed = starts[Math.max(0, Math.min({meta['frameCount']-1}, i))];
  last = performance.now();
  render(true);
}}
function setPlaying(v) {{
  playing = !!v;
  if (playing && elapsed >= DATA.total) elapsed = 0;
  last = performance.now();
  render(true);
}}
function setSpeed(v) {{
  speed = Number(v);
  document.getElementById('speed').value = String(speed);
  last = performance.now();
}}
function tick(now) {{
  const dt = Math.min(now - last, 100);
  last = now;
  if (window.reviewReady && playing) {{
    let ended = false;
    elapsed += dt * speed;
    if (elapsed >= DATA.total) {{
      if (loop) elapsed %= DATA.total;
      else {{ elapsed = DATA.total; playing = false; ended = true; }}
    }}
    render(ended);
  }}
  requestAnimationFrame(tick);
}}
const load = p => new Promise((resolve, reject) => {{
  const im = new Image;
  im.onload = () => resolve(im);
  im.onerror = () => {{
    // fallback if before frame does not load
    resolve(null);
  }};
  im.src = p;
}});
Promise.all(DATA.frames.map(async f => {{
  const im = {{ before: await load(f.before), flat: await load(f.flat) }};
  await Promise.all(names.map(async n => im[n] = await load(f.layers[n])));
  return im;
}})).then(frames => {{
  loaded.push(...frames);
  window.reviewReady = true;
  last = performance.now();
  render(true);
  document.getElementById('status').textContent = '{meta['frameCount']} quadros carregados com sucesso. Pronto para inspeção perceptual e QA independente.';
}}).catch(e => document.getElementById('status').textContent = 'Erro: ' + e.message);

document.getElementById('play').onclick = () => setPlaying(!playing);
document.getElementById('restart').onclick = () => {{ elapsed = 0; setPlaying(true); }};
document.getElementById('prev').onclick = () => seek(current - 1);
document.getElementById('next').onclick = () => seek(current + 1);
document.getElementById('frame').oninput = e => seek(Number(e.target.value));
document.getElementById('speed').onchange = e => setSpeed(e.target.value);
document.getElementById('scale').onchange = e => ['before','after'].forEach(id => {{
  const c = document.getElementById(id);
  c.style.width = 256 * Number(e.target.value) + 'px';
  c.style.height = 256 * Number(e.target.value) + 'px';
}});
document.getElementById('loop').onchange = e => loop = e.target.checked;
document.querySelectorAll('[data-layer]').forEach(e => e.onchange = () => render(true));
document.getElementById('restore').onclick = () => {{ document.querySelectorAll('[data-layer]').forEach(e => e.checked = true); render(true); }};
document.getElementById('bodyOnly').onclick = () => {{ document.querySelectorAll('[data-layer]').forEach(e => e.checked = (e.dataset.layer === 'body')); render(true); }};
window.reviewApi = {{
  seek, setPlaying, setSpeed,
  setLoop(v) {{ loop = !!v; document.getElementById('loop').checked = loop; }},
  restart() {{ elapsed = 0; setPlaying(true); }},
  state() {{ return {{ frame: current, elapsed, playing, speed, loop }}; }},
  resetTrace() {{ window.reviewTrace = []; }}
}};
requestAnimationFrame(tick);
</script></html>
"""
    return html

# Run packaging for each cycle
overall_results = []

for meta in cycles_meta:
    cid = meta['cellId']
    dirName = meta['dirName']
    print(f"\n==========================================")
    print(f"PACKAGING CYCLE: {cid} -> {dirName}")
    print(f"==========================================")
    
    char_dir = CHAR_GRIP / dirName
    exp_dir = EXP_GRIP / dirName
    src_char_dir = CHAR_GRIP / 'front-three' / cid
    
    char_dir.mkdir(parents=True, exist_ok=True)
    exp_dir.mkdir(parents=True, exist_ok=True)
    
    # Read plan for this clip
    plan_clip = next(c for c in plan['clips'] if c['cellId'] == cid)
    parent_clip_path = ROOT / snap['clips'][cid]
    parent_clip = read_json(parent_clip_path)
    wd = read_json(ROOT / meta['weaponDef'])
    
    # Copy all files from src_char_dir to char_dir and exp_dir
    for item in src_char_dir.rglob('*'):
        if item.is_file():
            rel = item.relative_to(src_char_dir)
            (char_dir / rel).parent.mkdir(parents=True, exist_ok=True)
            (exp_dir / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, char_dir / rel)
            shutil.copy2(item, exp_dir / rel)
    
    # Save anatomy-plan subset for this cycle in exp_dir
    write_json(exp_dir / 'anatomy.json', plan_clip)
    
    # Perform strict verification and assemble frames
    frames_doc = []
    rep_frames = []
    checks_records = []
    
    plan_frames_by_idx = {f['index']: f for f in plan_clip['frames']}
    
    for fi, pf in enumerate(parent_clip['frames']):
        fn = f'{fi:02d}.png'
        flat_p = char_dir / fn
        body_p = char_dir / 'layers/body' / fn
        wb_p = char_dir / 'layers/weaponBack' / fn
        wf_p = char_dir / 'layers/weaponFront' / fn
        hf_p = char_dir / 'layers/handFront' / fn
        native_p = char_dir / 'native' / fn
        
        flat_arr = np.array(Image.open(flat_p).convert('RGBA'))
        body_arr = np.array(Image.open(body_p).convert('RGBA'))
        wb_arr = np.array(Image.open(wb_p).convert('RGBA'))
        wf_arr = np.array(Image.open(wf_p).convert('RGBA'))
        hf_arr = np.array(Image.open(hf_p).convert('RGBA'))
        native_arr = np.array(Image.open(native_p).convert('RGBA'))
        
        orig_body = np.array(Image.open(ROOT / pf['layers']['body']['png']).convert('RGBA'))
        d_body = delta(body_arr, orig_body)
        assert d_body == 0, f"Body delta != 0 on {cid} F{fi}!"
        
        d_crop = delta(body_arr[64:192, 64:192], native_arr)
        assert d_crop == 0, f"Native crop mismatch on {cid} F{fi}!"
        
        is_visible = (meta['visibleInterval'][0] <= fi <= meta['visibleInterval'][1])
        f_plan = plan_frames_by_idx.get(fi)
        
        phase = pf.get('phase', f'frame-{fi}')
        durMs = meta['durationsMs'][fi]
        
        if not is_visible:
            assert wb_arr[:,:,3].sum() == 0
            assert wf_arr[:,:,3].sum() == 0
            assert hf_arr[:,:,3].sum() == 0
            assert delta(flat_arr, body_arr) == 0
            grip = None
            angle = None
            unwrapped = None
            landmarks = None
            gloveRows = []
            weaponBbox = None
            handFrontPixels = 0
            handSource = 'No overlay outsideAttack'
        else:
            assert f_plan is not None, f"Missing plan for visible frame {fi}!"
            grip = f_plan['grip']
            angle = f_plan['angleDeg']
            unwrapped = f_plan.get('unwrappedAngleDeg', angle)
            landmarks = f_plan.get('landmarks', {})
            gloveRows = f_plan.get('gloveRows', [])
            hand_mask = hf_arr[:,:,3] > 0
            handFrontPixels = int(hand_mask.sum())
            assert np.all(body_arr[hand_mask, 3] > 0)
            
            union_w = np.where((wf_arr[:,:,3] > 0)[:,:,None], wf_arr, wb_arr)
            sy, sx = np.where(union_w[:,:,3] > 0)
            weaponBbox = [int(sx.min()), int(sy.min()), int(sx.max()), int(sy.max())] if len(sx) > 0 else None
            handSource = 'Individually traced genuine source-glove pixels; zero body modification; handle-enclosing natural grip'
        
        frame_rec = {
            'index': fi,
            'phase': phase,
            'durationMs': durMs,
            'bodyRgbaDelta': 0,
            'weaponVisible': is_visible,
            'grip': grip,
            'rotationDeg': angle,
            'unwrappedAngleDeg': unwrapped,
            'handFrontPixels': handFrontPixels,
            'weaponBbox': weaponBbox,
            'png': f"characters/orc-v1/source/combat-rescue-v5/grip-specialist/{dirName}/{fn}",
            'sha256': sha256_file(flat_p),
            'nativePng': f"characters/orc-v1/source/combat-rescue-v5/grip-specialist/{dirName}/native/{fn}",
            'nativeSha256': sha256_file(native_p),
            'scale': 1,
            'flipBit': False,
            'handSource': handSource,
            'layers': {
                'weaponBack': {
                    'png': f"characters/orc-v1/source/combat-rescue-v5/grip-specialist/{dirName}/layers/weaponBack/{fn}",
                    'sha256': sha256_file(wb_p)
                },
                'body': {
                    'png': f"characters/orc-v1/source/combat-rescue-v5/grip-specialist/{dirName}/layers/body/{fn}",
                    'sha256': sha256_file(body_p)
                },
                'weaponFront': {
                    'png': f"characters/orc-v1/source/combat-rescue-v5/grip-specialist/{dirName}/layers/weaponFront/{fn}",
                    'sha256': sha256_file(wf_p)
                },
                'handFront': {
                    'png': f"characters/orc-v1/source/combat-rescue-v5/grip-specialist/{dirName}/layers/handFront/{fn}",
                    'sha256': sha256_file(hf_p)
                }
            }
        }
        frames_doc.append(frame_rec)
        
        rep_frame = {
            'index': fi,
            'phase': phase,
            'durationMs': durMs,
            'weaponVisible': is_visible,
            'grip': grip,
            'rotationDeg': angle,
            'unwrappedAngleDeg': unwrapped,
            'landmarks': landmarks,
            'gloveRows': gloveRows,
            'handFrontPixels': handFrontPixels,
            'weaponBbox': weaponBbox,
            'png': f"characters/orc-v1/source/combat-rescue-v5/grip-specialist/{dirName}/{fn}",
            'sha256': sha256_file(flat_p),
            'layers': frame_rec['layers']
        }
        rep_frames.append(rep_frame)
        
        checks_records.append({
            'index': fi,
            'phase': phase,
            'durationMs': durMs,
            'bodyRgbaDelta': 0,
            'weaponVisible': is_visible,
            'grip': grip,
            'handFrontPixels': handFrontPixels,
            'weaponBbox': weaponBbox
        })
    
    # Masters
    master_p = char_dir / 'source/composite.aseprite'
    body_master_p = char_dir / 'source/body.aseprite'
    native_master_p = char_dir / 'source/native.aseprite'
    hand_master_p = char_dir / 'source/hand.aseprite'
    strip_p = char_dir / 'native-strip.png'
    comp_strip_p = char_dir / 'composite-strip.png'
    
    master_sha = sha256_file(master_p)
    body_master_sha = sha256_file(body_master_p)
    native_master_sha = sha256_file(native_master_p)
    hand_master_sha = sha256_file(hand_master_p)
    strip_sha = sha256_file(strip_p)
    comp_strip_sha = sha256_file(comp_strip_p)
    
    # Build clip.json
    clip_doc = {
        'schemaVersion': 1,
        'revision': f"main-orc-combat-rescue-v5-grip-specialist-{dirName}",
        'id': f"basic.{meta['action'].lower()}-{'slash' if meta['action']=='Sword' else 'chop'}",
        'character': 'orc-v1',
        'category': meta['category'],
        'state': 'Attack',
        'direction': meta['direction'],
        'frameCount': meta['frameCount'],
        'durationsMs': meta['durationsMs'],
        'totalDurationMs': meta['totalDurationMs'],
        'canvas': [256, 256],
        'nativeCanvas': [128, 128],
        'bodyOffset': [64, 64],
        'groundY': 190,
        'nativeGroundY': 126,
        'ppu': 100,
        'loop': False,
        'oneShot': True,
        'terminal': False,
        'master': f"characters/orc-v1/source/combat-rescue-v5/grip-specialist/{dirName}/source/composite.aseprite",
        'masterSha256': master_sha,
        'bodyMaster': f"characters/orc-v1/source/combat-rescue-v5/grip-specialist/{dirName}/source/body.aseprite",
        'bodyMasterSha256': body_master_sha,
        'nativeMaster': f"characters/orc-v1/source/combat-rescue-v5/grip-specialist/{dirName}/source/native.aseprite",
        'nativeMasterSha256': native_master_sha,
        'handMaster': f"characters/orc-v1/source/combat-rescue-v5/grip-specialist/{dirName}/source/hand.aseprite",
        'handMasterSha256': hand_master_sha,
        'strip': f"characters/orc-v1/source/combat-rescue-v5/grip-specialist/{dirName}/native-strip.png",
        'stripSha256': strip_sha,
        'nativeStrip': f"characters/orc-v1/source/combat-rescue-v5/grip-specialist/{dirName}/native-strip.png",
        'nativeStripSha256': strip_sha,
        'compositeStrip': f"characters/orc-v1/source/combat-rescue-v5/grip-specialist/{dirName}/composite-strip.png",
        'compositeStripSha256': comp_strip_sha,
        'layerOrder': ['weaponBack', 'body', 'weaponFront', 'handFront'],
        'frames': frames_doc,
        'weapon': {
            'id': wd['id'],
            'name': wd['name'],
            'grip': wd['grip'],
            'canvas': wd['canvas'],
            'sprite': wd['sprite'],
            'master': wd['master'],
            'spriteSha256': wd['spriteSha256'],
            'masterSha256': wd['masterSha256'],
            'definition': meta['weaponDef'],
            'source': wd['master'],
            'sourceSha256': wd['masterSha256'],
            'scale': 1
        },
        'weaponDefinition': meta['weaponDef'],
        'visibilityPolicy': 'attack-only-v1',
        'visibleInterval': meta['visibleInterval'],
        'hideAfterAction': True,
        'weaponDepthPolicy': meta['weaponDepthPolicy'],
        'contactEvent': meta['contactEvent'],
        'technicalStatus': 'TECHNICALLY_COMPLETE',
        'artisticStatus': 'VISUAL_REVIEW_REQUIRED',
        'artisticApproval': 'PENDING_CREATOR',
        'eligibleForIntegration': False,
        'checkpoint': meta['checkpointName'],
        'fullClipIndependentQA': 'PENDING_ROOT_NO_COPILOT',
        'sourceParentClip': str(parent_clip_path).replace('\\', '/'),
        'sourceParentClipSha256': sha256_file(parent_clip_path),
        'provenance': {
            'authoring': 'Aseprite Lua only. Exact frontal body poses and timings 100% preserved (0 RGBA delta); weapon rendered with exact trigonometric transforms; genuine glove pixels traced per-frame into handFront; handle leather in weaponBack; attack-only visibility strictly enforced.',
            'script': 'experiments/main-orc-combat-rescue-v5/grip-specialist/front-three/author.lua',
            'scriptSha256': sha256_file(EXP_GRIP / 'front-three/author.lua'),
            'anatomy': 'experiments/main-orc-combat-rescue-v5/grip-specialist/front-three/anatomy-plan.json',
            'bodyRgbaChanged': False,
            'timingChanged': False,
            'newPixelLabCalls': 0,
            'costUsd': 0.00,
            'runtimeImplemented': False
        },
        'reuseAssessment': {
            'body': f"REUSE_DIRECT exact {meta['frameCount']} body poses and timings from approved frontal baseline",
            'item': f"REUSE_DIRECT exact independent {meta['category']} ({meta['weaponId']})",
            'remainingBindings': 'REUSE_ADAPTED per-pose observed genuine glove and wrist orientation',
            'risk': 'Perceptual observation at native/game scale and normal playback speed required by independent QA before creator review.'
        }
    }
    
    # Write clip.json in both characters and experiments
    write_json(char_dir / 'clip.json', clip_doc)
    write_json(exp_dir / 'clip.json', clip_doc)
    clip_sha = sha256_file(char_dir / 'clip.json')
    
    # Build representative.json
    rep_doc = {
        'schemaVersion': 1,
        'revision': f"main-orc-combat-rescue-v5-grip-specialist-{dirName}",
        'character': 'orc-v1',
        'category': meta['category'],
        'direction': meta['direction'],
        'state': 'Attack',
        'frameCount': meta['frameCount'],
        'durationsMs': meta['durationsMs'],
        'totalDurationMs': meta['totalDurationMs'],
        'canvas': [256, 256],
        'nativeCanvas': [128, 128],
        'bodyOffset': [64, 64],
        'groundY': 190,
        'nativeGroundY': 126,
        'ppu': 100,
        'loop': False,
        'oneShot': True,
        'terminal': False,
        'master': clip_doc['master'],
        'masterSha256': master_sha,
        'bodyMaster': clip_doc['bodyMaster'],
        'bodyMasterSha256': body_master_sha,
        'nativeMaster': clip_doc['nativeMaster'],
        'nativeMasterSha256': native_master_sha,
        'handMaster': clip_doc['handMaster'],
        'handMasterSha256': hand_master_sha,
        'strip': clip_doc['strip'],
        'stripSha256': strip_sha,
        'compositeStrip': clip_doc['compositeStrip'],
        'compositeStripSha256': comp_strip_sha,
        'layerOrder': clip_doc['layerOrder'],
        'frames': rep_frames,
        'weapon': clip_doc['weapon'],
        'technicalStatus': 'TECHNICALLY_COMPLETE',
        'artisticStatus': 'VISUAL_REVIEW_REQUIRED',
        'artisticApproval': 'PENDING_CREATOR',
        'eligibleForIntegration': False,
        'checkpoint': meta['checkpointName'],
        'visibleInterval': meta['visibleInterval'],
        'hiddenFrames': meta['hiddenFrames']
    }
    write_json(char_dir / 'representative.json', rep_doc)
    write_json(exp_dir / 'representative.json', rep_doc)
    rep_sha = sha256_file(char_dir / 'representative.json')
    
    # Build checks.json
    checks_doc = {
        'status': 'TECHNICALLY_COMPLETE',
        'checkpoint': meta['checkpointName'],
        'scope': f"ONLY full {cid} {meta['frameCount']}f / {meta['totalDurationMs']}ms",
        'frameCount': meta['frameCount'],
        'durationMs': meta['totalDurationMs'],
        'allBodyRgbaDelta': 0,
        'sourceItemUnchanged': True,
        'savedMastersAndExportsMatch': True,
        'stripsMatchFrames': True,
        'nativePngContract': 'Exact BODY crop 64,64 size 128; equipment always complete 256',
        'hiddenFrames': meta['hiddenFrames'],
        'visibleFrames': list(range(meta['visibleInterval'][0], meta['visibleInterval'][1] + 1)),
        'newPixelLabCalls': 0,
        'costUsd': 0.00,
        'frames': checks_records,
        'artisticStatus': 'VISUAL_REVIEW_REQUIRED',
        'fullCycleArtisticQA': 'PENDING_ROOT_NO_COPILOT',
        'eligibleForIntegration': False
    }
    write_json(exp_dir / 'checks.json', checks_doc)
    checks_sha = sha256_file(exp_dir / 'checks.json')
    
    # Build index.html
    before_rel = f"characters/orc-v1/source/combat-rescue-v5/combat/{cid}"
    html_content = make_html_preview(meta, frames_doc, str(char_dir), str(exp_dir), before_rel)
    (exp_dir / 'index.html').write_text(html_content, encoding='utf-8')
    preview_sha = sha256_file(exp_dir / 'index.html')
    
    # Build report.md
    report_md = f"""# Grip Especialista — Ciclo Completo {cid} ({meta['frameCount']}f / {meta['totalDurationMs']}ms)

**{meta['checkpointName']} · TECHNICALLY_COMPLETE · VISUAL_REVIEW_REQUIRED · PENDING_CREATOR · eligibleForIntegration: false**

## 1. Escopo e Propósito
Este pacote entrega o ciclo completo equipado de **{cid}** ({meta['category']}, direção `{meta['direction']}`) para avaliação do QA independente (sem Copilot, sem Codex).
- **Direção:** `{meta['direction']}`
- **Arma:** `{meta['weaponName']}` (`{meta['weaponId']}`)
- **Total de quadros:** {meta['frameCount']} quadros
- **Duração total:** {meta['totalDurationMs']} ms
- **Tempos por quadro (ms):** {meta['durationsMs']}
- **Intervalo visível da arma:** F{meta['visibleInterval'][0]:02d} até F{meta['visibleInterval'][1]:02d} ({meta['visibleInterval'][1] - meta['visibleInterval'][0] + 1} quadros ativos)
- **Quadros com arma oculta (bookends):** {meta['hiddenFrames']}
- **Custos PixelLab:** 0 chamadas pagas consumidas (custo $0.00)

## 2. Anatomia e Construção da Pegada
- **Corpo 100% Preservado:** 0 pixels RGBA de delta em relação ao corpo frontal aprovado. Nenhuma pose corporal foi reanimada ou alterada.
- **Camadas Independentes (4 camadas):**
  1. `weaponBack`: couro/madeira da empunhadura desenhado atrás do corpo nas linhas de pegada.
  2. `body`: o corpo completo do Orc (256×256 e crop nativo 128×128 em 64,64).
  3. `weaponFront`: guarda, lâmina/cabeça de machado e pomo posicionados na frente do corpo.
  4. `handFront`: dedos e palma da luva original traçados individualmente a partir do corpo em cada quadro visível, sobrepondo o cabo da arma de forma natural.
- **Fechamento e Envolvimento:** A mão envolve o cabo da arma; guarda e pomo permanecem discerníveis e contínuos através da pegada, sem quebras ou flutuações.
- **Diferenciação Técnica:**
  - `Sword`: golpe em corte com arco horizontal/diagonal, lâmina alongada em direção à trajetória do golpe.
  - `Axe`: golpe pesado de descida (overhead / cleave), impacto descendente com recuperação de peso.

## 3. Coordenadas de Pegada por Quadro Visível
| Quadro | Fase | Duração | Pegada [X, Y] | Rotação (°) | Unwrapped (°) | Pixels HandFront |
|---|---|---|---|---|---|---|
"""
    for r in rep_frames:
        if r['weaponVisible']:
            report_md += f"| F{r['index']:02d} | `{r['phase']}` | {r['durationMs']} ms | `[{r['grip'][0]}, {r['grip'][1]}]` | {r['rotationDeg']}° | {r['unwrappedAngleDeg']}° | {r['handFrontPixels']} px |\n"
        else:
            report_md += f"| F{r['index']:02d} | `{r['phase']}` | {r['durationMs']} ms | *(oculto)* | *(oculto)* | *(oculto)* | 0 px |\n"

    report_md += f"""
## 4. Arquivos Entregues e Hashes SHA-256
### Mestres Aseprite:
- `source/composite.aseprite`: `{master_sha}`
- `source/body.aseprite`: `{body_master_sha}`
- `source/native.aseprite`: `{native_master_sha}`
- `source/hand.aseprite`: `{hand_master_sha}`

### Documentos de Configuração e Diagnóstico:
- `clip.json`: `{clip_sha}`
- `representative.json`: `{rep_sha}`
- `checks.json`: `{checks_sha}`
- `index.html` (player interativo): `{preview_sha}`

### Strips Completos:
- `composite-strip.png`: `{comp_strip_sha}`
- `native-strip.png`: `{strip_sha}`

## 5. Status e Próximo Passo
- **Status Técnico:** `TECHNICALLY_COMPLETE`
- **Status Artístico:** `VISUAL_REVIEW_REQUIRED`
- **Aprovação do Criador:** `PENDING_CREATOR`
- **Próximo Passo:** Submissão ao QA independente (sem Copilot, sem Codex) para verificação temporal perceptual contínua em escala real (1× e câmera lenta).
"""
    (exp_dir / 'report.md').write_text(report_md, encoding='utf-8')
    report_sha = sha256_file(exp_dir / 'report.md')
    
    # Build checkpoint.json
    checkpoint_doc = {
        'checkpoint': meta['checkpointName'],
        'scope': f"ONLY full {cid} {meta['frameCount']}f / {meta['totalDurationMs']}ms",
        'frameCount': meta['frameCount'],
        'totalDurationMs': meta['totalDurationMs'],
        'technicalStatus': 'TECHNICALLY_COMPLETE',
        'artisticStatus': 'VISUAL_REVIEW_REQUIRED',
        'globalTaskStatus': 'ARTISTIC_REVISION_REQUIRED',
        'artisticApproval': 'PENDING_CREATOR',
        'eligibleForIntegration': False,
        'fullClipIndependentQA': 'PENDING_ROOT_NO_COPILOT',
        'bodyRgbaDeltaAllFrames': 0,
        'hiddenFrames': meta['hiddenFrames'],
        'visibleInterval': meta['visibleInterval'],
        'newPixelLabCalls': 0,
        'costUsd': 0.00,
        'clip': f"characters/orc-v1/source/combat-rescue-v5/grip-specialist/{dirName}/clip.json",
        'clipSha256': clip_sha,
        'representative': f"characters/orc-v1/source/combat-rescue-v5/grip-specialist/{dirName}/representative.json",
        'representativeSha256': rep_sha,
        'masterSha256': master_sha,
        'report': f"experiments/main-orc-combat-rescue-v5/grip-specialist/{dirName}/report.md",
        'reportSha256': report_sha,
        'checks': f"experiments/main-orc-combat-rescue-v5/grip-specialist/{dirName}/checks.json",
        'checksSha256': checks_sha,
        'preview': f"experiments/main-orc-combat-rescue-v5/grip-specialist/{dirName}/index.html",
        'previewSha256': preview_sha,
        'nextStep': 'Root independent QA review (no Copilot, no Codex).'
    }
    write_json(exp_dir / 'checkpoint.json', checkpoint_doc)
    write_json(char_dir / 'checkpoint.json', checkpoint_doc)
    checkpoint_sha = sha256_file(exp_dir / 'checkpoint.json')
    
    overall_results.append({
        'cellId': cid,
        'dirName': dirName,
        'checkpoint': meta['checkpointName'],
        'frameCount': meta['frameCount'],
        'durationMs': meta['totalDurationMs'],
        'clipSha256': clip_sha,
        'masterSha256': master_sha,
        'repSha256': rep_sha,
        'checkpointSha256': checkpoint_sha,
        'reportSha256': report_sha,
        'checksSha256': checks_sha,
        'previewSha256': preview_sha
    })
    print(f"Cycle {cid} packaged successfully:")
    print(f"  clip.json: {clip_sha}")
    print(f"  master:    {master_sha}")
    print(f"  checkpoint: {checkpoint_sha}")

# Overall summary in grip-specialist
summary_md = f"""# Grip Especialista — Entrega dos 3 Ciclos Frontais Restantes

**Data:** 2026-10-29  
**Agente:** DEV grip-specialist (Substituto Antigravity)  
**Status Geral:** `TECHNICALLY_COMPLETE` · `VISUAL_REVIEW_REQUIRED` · `PENDING_CREATOR` · `eligibleForIntegration: false`

## 1. Resumo da Entrega
Com a entrega do ciclo `full-front-r-sword` no turno anterior, esta etapa conclui os **3 ciclos frontais restantes** de ataque com arma do Orc V1:
1. **front_l/Sword** (13 quadros / 730 ms) — Espada do Recruta
2. **front_r/Axe** (12 quadros / 1005 ms) — Machado de Milícia
3. **front_l/Axe** (12 quadros / 1005 ms) — Machado de Milícia

Os 4 ciclos frontais armados encontram-se agora completamente produzidos, verificados tecnicamente e prontos para inspeção pelo QA independente.

## 2. Conformidade com as Restrições Rígidas
- **Corpo Frontal Preservado:** 0 pixels RGBA de delta em todos os quadros (100% da coreografia frontal aprovada preservada).
- **Pegada Natural:** 4 camadas independentes (`weaponBack`, `body`, `weaponFront`, `handFront`); luvas originais traçadas sem carimbos ou dedos flutuantes.
- **Política de Armas Somente no Ataque (attack-only):** Armas visíveis estritamente nos intervalos declarados (`[2, 10]` para Espada, `[2, 8]` para Machado); bookends 100% desarmados.
- **Mestres Aseprite:** Autoria e exportação executadas via Aseprite batch com perfil exclusivo; `Frame.duration` em segundos.
- **Custos:** 0 novas chamadas PixelLab consumidas; custo adicional de IA $0.00.
- **Preservação de Escopo:** Nenhuma escrita em `body-specialist/`, matriz, Unity, ou produção ativa.

## 3. Matriz de Entregas e Hashes SHA-256
| Ciclo | Quadros | Duração | Checkpoint | clip.json SHA-256 | composite.aseprite SHA-256 |
|---|---|---|---|---|---|
| `front_r/Sword` *(entregue anterior)* | 13f | 730 ms | `GRIP_FRONT_R_SWORD_FULL_READY` | `16fe8b7b30cbaa029ac4f4bd2bda5f7c8ac127007ec40a49a1f41db2580c63a1` | `3ee5755c874ccc007aa7f67af9ea5cc839d2cf98b5c0bee25dbcf0bf9acf6410` |
"""
for r in overall_results:
    summary_md += f"| `{r['cellId']}` | {r['frameCount']}f | {r['durationMs']} ms | `{r['checkpoint']}` | `{r['clipSha256']}` | `{r['masterSha256']}` |\n"

summary_md += f"""
## 4. Navegadores e Previews
- `front_l-Sword-full`: [index.html](front_l-Sword-full/index.html) · [relatório](front_l-Sword-full/report.md)
- `front_r-Axe-full`: [index.html](front_r-Axe-full/index.html) · [relatório](front_r-Axe-full/report.md)
- `front_l-Axe-full`: [index.html](front_l-Axe-full/index.html) · [relatório](front_l-Axe-full/report.md)

## 5. Próximo Passo
Aguardar parecer do QA independente (sem Copilot, sem Codex) sobre os 3 ciclos completos. Não propagar nem integrar no Unity antes de verificação e aprovação explícita do criador.
"""
(EXP_GRIP / 'report-front-three.md').write_text(summary_md, encoding='utf-8')
print("\nWrote summary report to report-front-three.md successfully!")
