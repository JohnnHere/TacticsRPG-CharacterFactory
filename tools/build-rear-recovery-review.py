"""
Build the isolated 4-direction x 7-action interactive review studio
for Orc V1 Rear Recovery v2 (main-orc-rear-recovery-v2).

Consumes explicit candidate28manifest.json, renders active candidates,
truthful unchanged baseline aliases, and clearly displays pending / in-revision
cells without silent fallback.
"""
from pathlib import Path
import json, shutil, hashlib, html, argparse, sys, os
from PIL import Image

R = Path(__file__).resolve().parents[1]
L = R / 'Biblioteca de Arte'
DEFAULT_OUT_DIR = L / 'Estudos Comparativos/Orc principal - Recuperacao traseira'
DEFAULT_MANIFEST = R / 'characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json'
BASELINE_ROOT = R / 'characters/orc-v1/source/complete-v1'

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
    'Walk':    'Walk · Locomoção sem arma (16f / 8f)',
    'Unarmed': 'Ataque Desarmado · Soco/Golpe físico (5f · 450 ms)',
    'Sword':   'Ataque de Espada · Espada do Recruta',
    'Axe':     'Ataque de Machado · Machado de Milícia',
    'Hit':     'Hit · Reação de dano (5f · 450 ms)',
    'Defeat':  'Defeat · Queda e pose terminal (5f · 700 ms)',
}

# Status vocabulary: current manifest uses the literal ARTISTIC_REVISION_REQUIRED;
# legacy IN_REVISION remains supported. All summary cards/counts are DERIVED from
# the manifest cells — never hardcoded (future refreshes may change the counts).
READY_STATUSES = {'ACTIVE_CANDIDATE', 'UNCHANGED_ALIAS'}
REVISION_STATUSES = {'IN_REVISION', 'ARTISTIC_REVISION_REQUIRED'}
PRODUCTION_STATUSES = {'IN_PRODUCTION'}

def is_revision_status(st: str) -> bool:
    return st in REVISION_STATUSES

def read_json(p: Path) -> dict:
    return json.loads(p.read_text(encoding='utf-8-sig'))

def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def resolve_clip_path(manifest_cell: dict) -> Path:
    raw_path = R / manifest_cell['clipJson']
    if raw_path.exists():
        return raw_path
    alt_attack = raw_path.parent / 'Attack' / raw_path.name
    if alt_attack.exists():
        return alt_attack
    raise FileNotFoundError(f"Clip not found for {manifest_cell['direction']}/{manifest_cell['action']}: {raw_path}")

def cell_map_for(cells: list, label: str) -> dict:
    expected = {(d, act) for d in DIRECTIONS for act in ACTIONS}
    result = {}
    for cell in cells:
        key = (cell['direction'], cell['action'])
        if key not in expected or key in result:
            raise ValueError(f"{label}: unexpected or duplicate cell {key}")
        result[key] = cell
    missing = expected - result.keys()
    if missing:
        raise ValueError(f"{label}: missing cells {sorted(missing)}")
    return result

def resolve_baseline_clip_path(d: str, act: str, baseline_cells=None) -> Path:
    if baseline_cells is not None:
        return resolve_clip_path(baseline_cells[(d, act)])
    if act in ['Sword', 'Axe']:
        bp = BASELINE_ROOT / d / act / 'Attack' / 'clip.json'
        if bp.exists():
            return bp
        bp_alt = BASELINE_ROOT / d / act / 'clip.json'
        if bp_alt.exists():
            return bp_alt
    else:
        bp = BASELINE_ROOT / d / act / 'clip.json'
        if bp.exists():
            return bp
    raise FileNotFoundError(f"Baseline clip not found for {d}/{act}")

def build_rear_recovery_review(manifest_path: Path, out_dir: Path, check_only: bool = False,
                               baseline_manifest_path: Path | None = None):
    print(f"=== ORC V1 REAR RECOVERY V2 REVIEW BUILDER ===")
    print(f"Manifest: {manifest_path}")
    print(f"Output:   {out_dir}")
    print(f"Mode:     {'CHECK_ONLY' if check_only else 'BUILD'}")

    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")

    manifest_data = read_json(manifest_path)
    cells_list = manifest_data.get('cells', [])
    cell_map = cell_map_for(cells_list, str(manifest_path))
    baseline_cells = (cell_map_for(read_json(baseline_manifest_path)['cells'],
                                   str(baseline_manifest_path))
                      if baseline_manifest_path is not None else None)
    revision = manifest_data.get('revision', 'main-orc-rear-recovery-v2')
    revision_label = html.escape(revision)
    baseline_label = ('versão anterior declarada' if baseline_cells is not None else 'Baseline v1')
    eligibility = manifest_data.get('eligibleForIntegration')
    if eligibility is not None and not isinstance(eligibility, bool):
        raise ValueError("eligibleForIntegration must be boolean when declared")
    eligibility_label = ('false — não integrar nem promover sem autorização do criador'
                         if eligibility is False else
                         'true — elegibilidade declarada; não concede aprovação do criador'
                         if eligibility is True else
                         'não declarada — esta página não autoriza integração')

    if check_only:
        print("Manifest validation successful. All 28 cells present.")
        for (d, act), c in cell_map.items():
            clip_p = resolve_clip_path(c)
            base_p = resolve_baseline_clip_path(d, act, baseline_cells)
            print(f"  OK: {d:<8} {act:<10} status={c.get('status'):<16} clip={clip_p.name} base={base_p.name}")
        return {'status': 'CHECK_PASSED', 'cells': 28}

    out_dir.mkdir(parents=True, exist_ok=True)
    files = []

    def copy_file(src_rel: str, dst_rel: str) -> str:
        src = R / src_rel
        if not src.exists():
            raise FileNotFoundError(f"Source file not found: {src}")
        dst = out_dir / dst_rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        files.append({'file': dst_rel, 'source': src_rel, 'sha256': sha256_file(dst)})
        return dst_rel

    def preview_strip(clip: dict, dst_rel: str) -> str:
        # Preview layout only: copy unchanged composite pixels, never native
        # body-only strips (which would omit weapons and change display scale).
        sources = [f['png'] for f in clip['frames']]
        sheet = Image.new('RGBA', (256 * len(sources), 256))
        for i, src in enumerate(sources):
            with Image.open(R / src) as im:
                if im.size != (256, 256):
                    raise ValueError(f'Preview composite must be 256x256: {src}')
                sheet.paste(im.convert('RGBA'), (i * 256, 0))
        dst = out_dir / dst_rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        sheet.save(dst)
        files.append({'file': dst_rel, 'sourceFrames': sources,
                      'role': 'preview-only-layout', 'sha256': sha256_file(dst)})
        return dst_rel

    # 1. Concept art
    concept_png = copy_file('characters/orc-v1/concepts/concept-selected.png', 'Personagem/Conceito.png')
    concept_ase = copy_file('characters/orc-v1/source/aseprite/concept-selected.aseprite', 'Personagem/Conceito.aseprite')

    # 2. Weapons
    weapons_meta = {}
    weapon_comparisons = []
    weapon_definitions = manifest_data.get('weaponDefinitions', {})
    if set(weapon_definitions) - {'Sword', 'Axe'}:
        raise ValueError("weaponDefinitions only supports Sword and Axe")
    for category, wid in [('Sword', 'recruit-sword'), ('Axe', 'militia-axe')]:
        original_weapon_path = f'assets/weapons/{wid}/weapon.json'
        weapon_path = weapon_definitions.get(category, original_weapon_path)
        w = read_json(R / weapon_path)
        folder = f'Armas/{w["name"]}'
        sp = copy_file(w['sprite'], f'{folder}/{w["name"]}.png')
        wm = copy_file(w['master'], f'{folder}/{w["name"]}.aseprite')
        (out_dir / folder / 'weapon.json').write_text(
            json.dumps({**w, 'sprite': f'{w["name"]}.png', 'master': f'{w["name"]}.aseprite'}, ensure_ascii=False, indent=2),
            encoding='utf-8'
        )
        weapons_meta[category] = {'name': w['name'], 'sprite': sp, 'master': wm, 'grip': w['grip']}
        if weapon_path != original_weapon_path:
            original = read_json(R / original_weapon_path)
            before = copy_file(original['sprite'], f'{folder}/Antes.png')
            weapon_comparisons.append(
                f'<section><h3>{html.escape(w["name"])} — antes/depois</h3>'
                f'<p>Antes (asset preservado) / Depois (candidato independente)</p>'
                f'<img class="item" src="{before}" alt="Antes">'
                f'<img class="item" src="{sp}" alt="Depois"></section>')

    # 3. Directional static bases
    dir_bases = {}
    for d in DIRECTIONS:
        dir_bases[d] = {
            'png128': copy_file(f'characters/orc-v1/sprites/Directions/orc_v1_dir_{d}.png', f'Direcoes/{d}/base-128.png'),
            'png256': copy_file(f'characters/orc-v1/source/complete-v1/{d}/Directions/base.png', f'Direcoes/{d}/base-256.png'),
            'master128': copy_file(f'characters/orc-v1/source/aseprite/complete-v1/native/dir-{d}.aseprite', f'Direcoes/{d}/dir-{d}-128.aseprite'),
            'master256': copy_file(f'characters/orc-v1/source/aseprite/complete-v1/composite/{d}/dir-base.aseprite', f'Direcoes/{d}/dir-{d}-256.aseprite'),
        }

    # 4. Process all 28 cells
    matrix = {}
    before_after_clips = {}

    for d in DIRECTIONS:
        matrix[d] = {}
        for act in ACTIONS:
            c_meta = cell_map[(d, act)]
            status = c_meta.get('status', 'IN_PRODUCTION')
            is_affected = c_meta.get('isAffected', False)
            review_status = c_meta.get('reviewStatus', '')
            notes = c_meta.get('notes', '')
            is_pending = is_affected and (status not in READY_STATUSES)

            folder = f'Clipes/{d}/{act}'
            clip_path = resolve_clip_path(c_meta)
            base_clip_path = resolve_baseline_clip_path(d, act, baseline_cells)

            c_data = read_json(clip_path)
            base_data = read_json(base_clip_path)

            # Copy baseline strip for EVERY affected cell (before/after comparison;
            # pending/revision cells display it explicitly labelled as unresolved
            # reference — never as a ready candidate)
            if is_affected:
                before_after_clips[f'{d}_{act}_baseline_strip'] = preview_strip(
                    base_data, f'AntesDepois/{d}_{act}_baseline_strip.png')

            if act in ['Sword', 'Axe']:
                # Weapon action
                prof_path = clip_path.parent / 'profile.json'
                prof = read_json(prof_path) if prof_path.exists() else None

                frames = []
                for i, f in enumerate(c_data['frames']):
                    png = copy_file(f['png'], f'{folder}/Quadros/{i:02d}.png')
                    if 'layers' in f:
                        for lk, lv in f['layers'].items():
                            if 'png' in lv and (R / lv['png']).exists():
                                copy_file(lv['png'], f'{folder}/Camadas/{lk}/{i:02d}.png')
                    frames.append({
                        'index': i,
                        'png': png,
                        'durationMs': f['durationMs'],
                        'phase': f.get('phase', f'frame-{i:02d}'),
                        'weaponVisible': f.get('weaponVisible', True),
                        'rightGrip': f.get('rightGrip'),
                        'rotationDeg': f.get('rotationDeg'),
                        'weaponBehindBody': f.get('weaponBehindBody', False),
                        'impact': bool(c_data.get('contactEvent') and c_data['contactEvent'].get('frame') == i),
                        'terminal': False,
                    })

                master = copy_file(c_data['master'], f'{folder}/Ataque.aseprite') if c_data.get('master') and (R / c_data['master']).exists() else ''
                body_master = copy_file(c_data['bodyMaster'], f'{folder}/Corpo.aseprite') if c_data.get('bodyMaster') and (R / c_data['bodyMaster']).exists() else ''
                hand_master = copy_file(c_data['handMaster'], f'{folder}/Dedos.aseprite') if c_data.get('handMaster') and (R / c_data['handMaster']).exists() else ''
                strip = preview_strip(c_data, f'{folder}/Folha.png')

                matrix[d][act] = {
                    'action': act,
                    'direction': d,
                    'label': ACTION_LABELS[act],
                    'loop': False,
                    'oneShot': True,
                    'terminal': False,
                    'visibleInterval': c_data.get('visibleInterval', [0, len(frames)-1]),
                    'totalDurationMs': c_data.get('totalDurationMs', sum(f['durationMs'] for f in frames)),
                    'master': master,
                    'bodyMaster': body_master,
                    'handMaster': hand_master,
                    'strip': strip,
                    'clipJson': f'{folder}/clip.json',
                    'frames': frames,
                    'status': status,
                    'isAffected': is_affected,
                    'isPending': is_pending,
                    'reviewStatus': review_status,
                    'notes': notes,
                }
            else:
                # Standard actions: Idle, Walk, Unarmed, Hit, Defeat
                frames = []
                for i, f in enumerate(c_data['frames']):
                    png = copy_file(f['png'], f'{folder}/Quadros/{i:02d}.png')
                    nat = ''
                    if f.get('nativePng') and (R / f['nativePng']).exists():
                        nat = copy_file(f['nativePng'], f'{folder}/Nativo128/{i:02d}.png')
                    frames.append({
                        'index': i,
                        'png': png,
                        'nativePng': nat,
                        'durationMs': f['durationMs'],
                        'phase': f.get('phase', f'frame-{i:02d}'),
                        'weaponVisible': False,
                        'rightGrip': None,
                        'impact': bool(c_data.get('contactEvent') and c_data['contactEvent'].get('frame') == i),
                        'terminal': bool(c_data.get('terminal') and (c_data.get('terminalFrame') == i or i == len(c_data['frames']) - 1)),
                    })

                master = copy_file(c_data['master'], f'{folder}/{act}.aseprite') if c_data.get('master') and (R / c_data['master']).exists() else ''
                nat_master = copy_file(c_data['nativeMaster'], f'{folder}/{act}-128.aseprite') if c_data.get('nativeMaster') and (R / c_data['nativeMaster']).exists() else ''
                strip = preview_strip(c_data, f'{folder}/Folha.png')

                matrix[d][act] = {
                    'action': act,
                    'direction': d,
                    'label': ACTION_LABELS[act],
                    'loop': c_data.get('loop', act in ['Idle', 'Walk']),
                    'oneShot': c_data.get('oneShot', act not in ['Idle', 'Walk']),
                    'terminal': c_data.get('terminal', act == 'Defeat'),
                    'totalDurationMs': c_data.get('totalDurationMs', sum(f['durationMs'] for f in frames)),
                    'master': master,
                    'nativeMaster': nat_master,
                    'strip': strip,
                    'clipJson': f'{folder}/clip.json',
                    'frames': frames,
                    'status': status,
                    'isAffected': is_affected,
                    'isPending': is_pending,
                    'reviewStatus': review_status,
                    'notes': notes,
                }

    # 5. Derived status summary (manifest-driven; never hardcoded)
    def ids_with(statuses):
        return [c['cellId'] for c in cells_list if c.get('status') in statuses]

    active_ids = ids_with({'ACTIVE_CANDIDATE'})
    alias_ids = ids_with({'UNCHANGED_ALIAS'})
    revision_ids = ids_with(REVISION_STATUSES)
    production_ids = ids_with(PRODUCTION_STATUSES)
    affected_ids = [c['cellId'] for c in cells_list if c.get('isAffected')]
    known_bad_ids = revision_ids + production_ids
    package_status = 'ARTISTIC_REVISION_REQUIRED' if known_bad_ids else 'VISUAL_REVIEW_REQUIRED'
    active_ids_html = ', '.join(f'<code>{i}</code>' for i in active_ids)
    revision_ids_html = ', '.join(f'<code>{i}</code>' for i in revision_ids)
    production_ids_html = ', '.join(f'<code>{i}</code>' for i in production_ids)
    declared_counts = {
        'active': manifest_data.get('activeCandidatesCount'),
        'revision': manifest_data.get('inRevisionCount'),
        'production': manifest_data.get('inProductionCount'),
        'alias': manifest_data.get('unchangedAliasesCount'),
    }
    computed_counts = {
        'active': len(active_ids),
        'revision': len(revision_ids),
        'production': len(production_ids),
        'alias': len(alias_ids),
    }
    if declared_counts != computed_counts:
        print(f"WARNING: manifest summary fields {declared_counts} != computed {computed_counts}; using computed cell values.")

    # 6. Build HTML
    style = '''*{box-sizing:border-box}
body{margin:0;background:#142126;color:#e5ece8;font:15px/1.5 system-ui}
main{max-width:1920px;margin:auto;padding:22px}
a,h3{color:#e2c38c}p{color:#bdcec8}
h1{font-size:30px;margin:0 0 8px}h2{font-size:22px;margin:0 0 10px}
article{margin:20px 0;padding:18px;background:#22353c;border:1px solid #51696c;border-radius:8px;min-width:0}
.toolbar{position:sticky;top:0;z-index:10;background:#15282e;border-bottom:1px solid #68848b;padding:12px;display:flex;gap:12px;align-items:center;flex-wrap:wrap}
button,select{font:inherit;padding:7px 10px;color:white;background:#38515b;border:1px solid #789397;border-radius:4px;cursor:pointer}
button:hover,select:hover{background:#4a6773}
.hero{display:flex;flex-wrap:wrap;gap:24px;align-items:center}
.concept{width:192px;height:192px;image-rendering:pixelated}
.item{width:144px;height:144px;image-rendering:pixelated}
.grid4{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
.studio{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr) 240px;gap:18px}
.stage{height:360px;display:flex;justify-content:center;align-items:center;overflow:auto;background:repeating-conic-gradient(#2b3d43 0 25%,#3b5258 0 50%) 0/20px 20px;border-radius:6px;position:relative}
.stage canvas,.stage img{width:256px;height:256px;image-rendering:pixelated;flex-shrink:0}
.grip canvas{width:192px;height:192px;image-rendering:pixelated;background:#31464c;border:1px solid #68848b}
.gallery{display:flex;flex-wrap:wrap;gap:10px;margin-top:10px}
.gallery figure{margin:0;background:#192b31;padding:6px;border-radius:4px}
.gallery img{image-rendering:pixelated;width:128px;height:128px}
.gallery figcaption{font-size:12px;max-width:128px}
.dark .stage{background:#17242b}
.light .stage{background:#c4c6b7}
table{width:100%;border-collapse:collapse;font-size:14px}
th,td{border:1px solid #486167;padding:7px 9px;text-align:left}
th{background:#182b31;color:#e2c38c}
.badge{display:inline-block;padding:2px 7px;border-radius:4px;font-size:12px;font-weight:600}
.badge-active{background:#1e6b37;color:#d8f3e3}
.badge-alias{background:#204050;color:#c0e0f0}
.badge-revision{background:#7a2424;color:#ffd8d8}
.badge-production{background:#6b521b;color:#fce8be}
.badge-pending{background:#38515b;color:#e5ece8}
.pending-alert{background:#5a3818;border:1px solid #c97d26;color:#fff2df;padding:10px 14px;border-radius:6px;margin:10px 0;display:none}
.pending-alert.active{display:block}
.stat-box{display:flex;gap:16px;flex-wrap:wrap;margin:14px 0}
.stat-pill{background:#192b31;padding:8px 14px;border-radius:6px;border:1px solid #486167}
@media(max-width:1300px){.grid4{grid-template-columns:1fr 1fr}.studio{grid-template-columns:1fr}}'''

    dir_cards = ''.join(
        f'<section><h3>{html.escape(DIR_LABELS[d])}</h3><div class="stage" style="height:200px"><img src="{dir_bases[d]["png128"]}" style="width:128px;height:128px" alt="{d}"></div><p><a href="{dir_bases[d]["png128"]}">PNG 128</a> · <a href="{dir_bases[d]["master128"]}">Aseprite 128</a> · <a href="{dir_bases[d]["master256"]}">Aseprite 256</a></p></section>'
        for d in DIRECTIONS
    )

    dir_stage_cards = ''.join(
        f'<section><h3>{html.escape(DIR_LABELS[d])}</h3>'
        f'<div id="badge-dir-{d}" style="margin-bottom:6px"></div>'
        f'<div class="stage"><canvas id="dir-canvas-{d}" width="256" height="256"></canvas></div>'
        f'<p id="dir-info-{d}"></p><p id="dir-links-{d}"></p></section>'
        for d in DIRECTIONS
    )

    table_rows = []
    for act in ACTIONS:
        for d in DIRECTIONS:
            cell = matrix[d][act]
            vis = f'Quadros {cell["visibleInterval"][0]+1}..{cell["visibleInterval"][1]+1}' if cell.get('visibleInterval') else 'Oculta (sem arma)'
            sem = 'Loop contínuo' if cell['loop'] else ('One-shot Terminal (Hold)' if cell['terminal'] else 'One-shot → Idle')
            
            st = cell['status']
            if st == 'ACTIVE_CANDIDATE':
                badge_html = f'<span class="badge badge-active">ACTIVE_CANDIDATE</span>'
            elif st == 'UNCHANGED_ALIAS':
                badge_html = f'<span class="badge badge-alias">UNCHANGED_ALIAS</span>'
            elif is_revision_status(st):
                badge_html = f'<span class="badge badge-revision">{st}</span>'
            else:
                badge_html = f'<span class="badge badge-production">{st}</span>'
                
            rev_badge = '<span class="badge badge-pending">PENDING_CREATOR</span>'
            note_text = html.escape(cell.get('notes', ''))
            
            table_rows.append(
                f'<tr><td><strong>{act}</strong></td><td><code>{d}</code></td><td>{len(cell["frames"])}</td><td>{cell["totalDurationMs"]} ms</td>'
                f'<td>{sem}</td><td>{vis}</td><td>{badge_html}</td><td>{rev_badge}</td>'
                f'<td style="font-size:12px">{note_text}</td>'
                f'<td><a href="{cell["master"]}">Aseprite</a> · <a href="{cell["strip"]}">Folha</a></td></tr>'
            )

    item_cards = ''.join(
        f'<section><h3>{html.escape(w["name"])} · asset independente</h3><img class="item" src="{w["sprite"]}" alt="{html.escape(w["name"])}"><p><a href="{w["sprite"]}">PNG 96×96</a> · <a href="{w["master"]}">Mestre Aseprite</a></p></section>'
        for w in weapons_meta.values()
    )

    # Before/After evidence derived from the manifest for ALL affected cells:
    # active candidates show real baseline vs current candidate; revision-required
    # cells show the baseline explicitly labelled as unresolved and the delivered-
    # but-rejected candidate for diagnosis only — never presented as ready.
    ba_cards = []
    for c_meta in cells_list:
        if not c_meta.get('isAffected'):
            continue
        d, act = c_meta['direction'], c_meta['action']
        cell = matrix[d][act]
        st = cell['status']
        base_strip = before_after_clips.get(f'{d}_{act}_baseline_strip', '')
        cand_strip = cell.get('strip', '')
        notes = html.escape(cell.get('notes', ''))
        base_img = (f'<div style="overflow-x:auto;background:#192b31;padding:8px;border-radius:6px"><img src="{base_strip}" style="height:96px;image-rendering:pixelated" alt="{d} {act} baseline"></div>' if base_strip else '<p style="font-size:12px;color:#fca5a5">Folha baseline indisponível.</p>')
        base_link = f'<a href="{base_strip}">Folha Baseline</a>' if base_strip else '<em>indisponível</em>'
        if st == 'ACTIVE_CANDIDATE':
            st_badge = '<span class="badge badge-active">ACTIVE_CANDIDATE</span>'
            if cell.get('reviewStatus'):
                st_badge += f' <span class="badge badge-pending">{html.escape(cell["reviewStatus"])}</span>'
            base_label, cand_label = f'Antes ({baseline_label})', f'Depois ({revision_label})'
            cand_img = (f'<div style="overflow-x:auto;background:#192b31;padding:8px;border-radius:6px"><img src="{cand_strip}" style="height:96px;image-rendering:pixelated" alt="{d} {act} candidato"></div>' if cand_strip else '<p style="font-size:12px;color:#fca5a5">Folha do candidato indisponível.</p>')
            cand_link = f'<a href="{cand_strip}">Folha Candidato</a>' if cand_strip else ''
        else:
            st_badge = f'<span class="badge badge-revision">{st}</span>'
            base_label = f'{baseline_label} (célula NÃO resolvida — referência de inspeção)'
            cand_label = 'Candidato entregue REJEITADO (NÃO pronto — revisão artística em andamento)'
            cand_img = (f'<div style="overflow-x:auto;background:#192b31;padding:8px;border-radius:6px"><img src="{cand_strip}" style="height:96px;image-rendering:pixelated;border:2px dashed #e05353" alt="{d} {act} candidato rejeitado"></div>' if cand_strip else '<p style="font-size:12px;color:#fca5a5">Folha do candidato rejeitado indisponível.</p>')
            cand_link = f'<a href="{cand_strip}">Folha do candidato rejeitado (diagnóstico)</a>' if cand_strip else ''
        rejected_link = ''
        if c_meta.get('rejectedEvidence'):
            ev_rel = os.path.relpath(R / c_meta['rejectedEvidence'], out_dir).replace('\\', '/')
            rejected_link = f'<p style="font-size:12px"><a href="{ev_rel}">Registro vinculado de rejeição (conferir versão e escopo)</a></p>'
        ba_cards.append(f'''      <section>
        <h3><code>{d}</code> {act}</h3>
        <p style="font-size:13px"><strong>Status:</strong> {st_badge}</p>
        <p style="font-size:12px;color:#bdcec8">{notes}</p>
        <p style="font-size:13px"><strong>{base_label}:</strong> {base_link}</p>
        {base_img}
        <p style="font-size:13px;margin-top:10px"><strong>{cand_label}:</strong> {cand_link}</p>
        {cand_img}
        {rejected_link}
      </section>''')
    ba_cards_html = chr(10).join(ba_cards)
    before_after_section = f'''
  <article>
    <h2>Evidências Visuais Antes ({baseline_label}) vs Depois ({revision_label}) — {len(ba_cards)} células afetadas</h2>
    <p>Comparação derivada diretamente do manifesto <code>candidate28manifest.json</code> para TODAS as células afetadas ({len(ba_cards)}): candidatos ativos com baseline vs candidato atual; células <code>ARTISTIC_REVISION_REQUIRED</code> com baseline rotulado como NÃO resolvido e o candidato entregue rejeitado exibido apenas para diagnóstico. As folhas preservam os pixels exportados, sem suavização; anatomia, pegada e continuidade temporal exigem revisão visual independente.</p>
    <div class="grid4" style="grid-template-columns:repeat(2,minmax(0,1fr))">
{ba_cards_html}
{''.join(weapon_comparisons)}
    </div>
  </article>'''

    script = r'''
const DIRECTIONS = ['front_r', 'front_l', 'back_r', 'back_l'];
let playing = true, loop = true, speed = 1, zoom = 1;
let selectedDir = 'back_r', selectedAction = 'Walk', transitionMode = 'action-only';
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
  const cell = matrix[dir][action];
  const actFrames = cell.frames.map(f => ({ ...f, seqState: action }));
  
  if (mode === 'idle-attack-idle') {
    const idle = matrix[dir].Idle.frames.map(f => ({ ...f, seqState: 'Idle' }));
    const target = ['Sword', 'Axe', 'Unarmed'].includes(action) ? actFrames : matrix[dir].Sword.frames.map(f => ({ ...f, seqState: 'Sword' }));
    return { frames: [...idle, ...target, ...idle], isTerminal: false };
  }
  if (mode === 'walk-idle') {
    const walk = matrix[dir].Walk.frames.map(f => ({ ...f, seqState: 'Walk' }));
    const idle = matrix[dir].Idle.frames.map(f => ({ ...f, seqState: 'Idle' }));
    return { frames: [...walk, ...idle], isTerminal: false };
  }
  if (mode === 'hit-idle') {
    const hit = matrix[dir].Hit.frames.map(f => ({ ...f, seqState: 'Hit' }));
    const idle = matrix[dir].Idle.frames.map(f => ({ ...f, seqState: 'Idle' }));
    return { frames: [...hit, ...idle], isTerminal: false };
  }
  if (mode === 'defeat-terminal') {
    const def = matrix[dir].Defeat.frames.map(f => ({ ...f, seqState: 'Defeat' }));
    return { frames: def, isTerminal: true };
  }
  return { frames: actFrames, isTerminal: cell.terminal };
}

function isRevisionStatus(status) {
  return status === 'IN_REVISION' || status === 'ARTISTIC_REVISION_REQUIRED';
}
function badgeClassFor(status) {
  if (status === 'ACTIVE_CANDIDATE') return 'badge-active';
  if (status === 'UNCHANGED_ALIAS') return 'badge-alias';
  if (isRevisionStatus(status)) return 'badge-revision';
  return 'badge-production';
}
function updatePendingAlert(cell) {
  const alertEl = document.getElementById('pending-alert');
  if (cell.isPending) {
    alertEl.className = 'pending-alert active';
    if (isRevisionStatus(cell.status)) {
      alertEl.innerHTML = `<strong>⚠️ REVISÃO ARTÍSTICA OBRIGATÓRIA [${cell.direction}/${cell.action} · ${cell.status}]:</strong> ${cell.notes || 'Candidato entregue rejeitado; revisão artística em andamento.'} <em>(Exibindo o candidato entregue REJEITADO apenas para diagnóstico · NÃO está pronto · comparação com baseline na seção Antes/Depois)</em>`;
      alertEl.style.background = '#6b2020';
      alertEl.style.borderColor = '#e05353';
    } else {
      alertEl.innerHTML = `<strong>⏳ CÉLULA EM PRODUÇÃO [${cell.direction}/${cell.action} · ${cell.status}]:</strong> ${cell.notes || 'Aguardando entrega de produção.'} <em>(Exibindo referência baseline para inspeção temporária · NÃO é o candidato final)</em>`;
      alertEl.style.background = '#5a3818';
      alertEl.style.borderColor = '#c97d26';
    }
  } else if (cell.status === 'ACTIVE_CANDIDATE') {
    alertEl.className = 'pending-alert active';
    alertEl.innerHTML = `<strong>✨ CANDIDATO ATIVO v2 [${cell.direction}/${cell.action} · ${cell.status}]:</strong> ${cell.notes || 'Candidato ativo em revisão'} <em>(Aprovação artística do criador: PENDING_CREATOR)</em>`;
    alertEl.style.background = '#1b4a28';
    alertEl.style.borderColor = '#38a159';
  } else {
    alertEl.className = 'pending-alert';
    alertEl.innerHTML = '';
  }
}

async function renderMain() {
  const cell = matrix[selectedDir][selectedAction];
  updatePendingAlert(cell);

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

  let outline = 'none';
  if (f.impact) outline = '2px solid #e2b659';
  else if (f.terminal) outline = '2px solid #d96b6b';
  else if (cell.isPending) outline = '2px dashed #e29339';
  c.style.outline = outline;

  let statusBadge = `[${cell.status}]`;
  let holdText = (seq.isTerminal && mainState.n === fs.length - 1) ? ' · TERMINAL HOLD (Pose final mantida no solo)' : '';
  let impactText = f.impact ? ' · IMPACTO VISUAL' : '';

  document.getElementById('main-info').innerHTML =
    `<strong>[${selectedDir}] ${f.seqState}</strong> · Quadro ${mainState.n + 1}/${fs.length} · ${f.durationMs} ms · ${f.phase}` +
    impactText + holdText +
    ` · <span class="badge ${badgeClassFor(cell.status)}">${cell.status}</span>`;

  const g = document.getElementById('main-grip');
  const gc = g.getContext('2d');
  gc.imageSmoothingEnabled = false;
  gc.clearRect(0, 0, 24, 24);
  const pos = f.rightGrip || [128, 128];
  gc.drawImage(im, pos[0] - 12, pos[1] - 12, 24, 24, 0, 0, 24, 24);

  const gallery = document.getElementById('frame-gallery');
  if (gallery.dataset.key !== `${selectedDir}-${selectedAction}`) {
    gallery.dataset.key = `${selectedDir}-${selectedAction}`;
    gallery.innerHTML = cell.frames.map((fr, idx) =>
      `<figure><a href="${fr.png}"><img src="${fr.png}" alt="Quadro ${idx+1}"></a><figcaption>#${idx+1} · ${fr.phase} · ${fr.durationMs} ms</figcaption></figure>`
    ).join('');
  }
}

async function renderDirCard(d) {
  const cell = matrix[d][selectedAction];
  const badgeEl = document.getElementById('badge-dir-' + d);
  if (cell.status === 'ACTIVE_CANDIDATE') {
    badgeEl.innerHTML = '<span class="badge badge-active">CANDIDATO ATIVO v2</span>';
  } else if (cell.status === 'UNCHANGED_ALIAS') {
    badgeEl.innerHTML = '<span class="badge badge-alias">ALIAS CANÔNICO</span>';
  } else if (isRevisionStatus(cell.status)) {
    badgeEl.innerHTML = `<span class="badge badge-revision">${cell.status} (NÃO PRONTO)</span>`;
  } else {
    badgeEl.innerHTML = `<span class="badge badge-production">${cell.status} (PENDENTE)</span>`;
  }

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

  c.style.outline = f.impact ? '2px solid #e2b659' : (f.terminal ? '2px solid #d96b6b' : (cell.isPending ? '1px dashed #e29339' : 'none'));
  document.getElementById('dir-info-' + d).textContent =
    `${f.seqState} ${st.n + 1}/${fs.length} · ${f.durationMs} ms · ${f.weaponVisible ? 'arma visível' : 'sem arma'}`;
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
  applyScale(zoom);
};

function applyScale(z) {
  document.querySelectorAll('.stage canvas, .stage img').forEach(c => {
    c.style.width = c.style.height = Math.round(256 * z) + 'px';
  });
  document.querySelectorAll('.stage').forEach(s => {
    const minH = Math.round(256 * z + 32);
    s.style.height = Math.max(minH, 180) + 'px';
  });
}

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

    integration_report = manifest_data.get(
        'integrationReport', 'experiments/main-orc-rear-recovery-v2/root-integration-report.md')
    integration_href = os.path.relpath(R / integration_report, out_dir).replace('\\', '/')
    page = f'''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Orc V1 · {revision_label}</title>
<style>{style}</style>
<main>
  <h1>Orc V1 (Verde Warcraft) · {revision_label}</h1>
  <p>Compare as quatro direções e sete ações do Orc V1, com antes/depois das células afetadas e armas independentes, visíveis somente durante os ataques. Estado do pacote: <span class="badge badge-revision">{package_status}</span>; aprovação artística do criador: <code>PENDING_CREATOR</code>. Validação técnica e checkpoints internos não concedem aprovação artística. O <a href="{integration_href}">relatório de integração</a> reúne fontes, testes e o parecer independente da versão congelada.</p>
  <p id="integration-eligibility"><strong>Elegibilidade de integração:</strong> {eligibility_label}.</p>
  
  <div class="stat-box">
    <div class="stat-pill"><strong>Células Totais:</strong> {len(cells_list)} (4 vistas × 7 ações)</div>
    <div class="stat-pill"><strong>Candidatos Ativos:</strong> <span class="badge badge-active">{len(active_ids)}</span> ({active_ids_html})</div>
    <div class="stat-pill"><strong>Aliases Inalterados:</strong> <span class="badge badge-alias">{len(alias_ids)}</span> (Preservados byte-a-byte)</div>
    <div class="stat-pill"><strong>Revisão Artística Obrigatória:</strong> <span class="badge badge-revision">{len(revision_ids)}</span> ({revision_ids_html})</div>
    <div class="stat-pill"><strong>Em Produção:</strong> <span class="badge badge-production">{len(production_ids)}</span>{(' (' + production_ids_html + ')') if production_ids else ' (nenhuma fila no manifesto atual)'}</div>
    <div class="stat-pill"><strong>Aprovação Criador:</strong> <span class="badge badge-pending">PENDING_CREATOR</span></div>
  </div>

  <p><a href="../../index.html">Biblioteca de Arte</a> · <a href="../Orc principal - Biblioteca completa/index.html">Visualizador Baseline Canônico</a> · <a href="catalogo.json">Catálogo JSON</a> · <a href="manifest.json">Manifesto de Arquivos</a></p>

  <div class="toolbar">
    <button id="play">Pausar</button>
    <button id="reset">Reiniciar</button>
    <button id="step-prev">◀ Quadro</button>
    <button id="step-next">Quadro ▶</button>
    <label>Direção
      <select id="select-dir">
        <option value="front_r">front_r (Frente-Direita · SE)</option>
        <option value="front_l">front_l (Frente-Esquerda · SW)</option>
        <option value="back_r" selected>back_r (Costas-Direita · NE)</option>
        <option value="back_l">back_l (Costas-Esquerda · NW)</option>
      </select>
    </label>
    <label>Ação
      <select id="select-action">
        <option value="Idle">Idle (5f · 2200 ms · sem arma)</option>
        <option value="Walk" selected>Walk (Locomoção sem arma)</option>
        <option value="Unarmed">Unarmed Attack (Soco/Golpe físico)</option>
        <option value="Sword">Sword Attack (Espada do Recruta)</option>
        <option value="Axe">Axe Attack (Machado de Milícia)</option>
        <option value="Hit">Hit (5f · 450 ms · reação de dano)</option>
        <option value="Defeat">Defeat (5f · 700 ms · queda terminal)</option>
      </select>
    </label>
    <label>Transição / Estado
      <select id="select-transition">
        <option value="action-only" selected>Clipe isolado da ação</option>
        <option value="idle-attack-idle">Idle → Attack → Idle (transição armada/desarmada)</option>
        <option value="walk-idle">Walk → Idle (parada de locomoção)</option>
        <option value="hit-idle">Hit → Idle (recuperação de dano)</option>
        <option value="defeat-terminal">Defeat → Terminal Hold (queda sem reinício)</option>
      </select>
    </label>
    <label>Velocidade
      <select id="speed">
        <option value="1" selected>1×</option>
        <option value="0.75">0,75×</option>
        <option value="0.5">0,5×</option>
        <option value="0.25">0,25×</option>
      </select>
    </label>
    <label>Escala
      <select id="zoom">
        <option value="0.5">Escala Prática Jogo (128×128)</option>
        <option value="1" selected>1× Canvas (256×256)</option>
        <option value="1.25">1,25× (320×320)</option>
        <option value="1.5">1,5× (384×384)</option>
        <option value="2">2× (512×512)</option>
      </select>
    </label>
    <label>Fundo
      <select id="bg">
        <option value="">Xadrez transparência</option>
        <option value="dark">Escuro</option>
        <option value="light">Claro</option>
      </select>
    </label>
    <label><input type="checkbox" id="loop" checked> Repetir revisão (exceto Defeat terminal hold)</label>
  </div>

  <div id="pending-alert" class="pending-alert"></div>

  <article class="hero">
    <section>
      <h3>Conceito Selecionado · Orc V1</h3>
      <img class="concept" src="{concept_png}" alt="Orc V1 Verde Warcraft">
      <p><a href="{concept_png}">PNG</a> · <a href="{concept_ase}">Mestre Aseprite</a></p>
    </section>
    {item_cards}
  </article>

  <article>
    <h2>Inspeção Principal e Transição de Estados</h2>
    <div class="studio">
      <section>
        <h3>Palco Principal (256×256 groundY=190 / nativo 128×128 groundY=126)</h3>
        <div class="stage"><canvas id="main-canvas" width="256" height="256"></canvas></div>
        <p id="main-info"></p>
      </section>
      <section>
        <h3>Quadros do Clipe Selecionado</h3>
        <div id="frame-gallery" class="gallery"></div>
      </section>
      <section class="grip">
        <h3>Ponto Focal / Pegada (8×)</h3>
        <canvas id="main-grip" width="24" height="24"></canvas>
        <p>Recorte 24×24 ao redor do ponto focal de pegada / articulação da mão direita.</p>
      </section>
    </div>
  </article>

  <article>
    <h2>Comparação Simultânea das 4 Vistas (front_r, front_l, back_r, back_l)</h2>
    <p>As 4 câmeras executam sincronizadamente a ação selecionada na barra superior, respeitando a iluminação superior-esquerda e a mão dominante.</p>
    <div class="grid4">{dir_stage_cards}</div>
  </article>

  <article>
    <h2>Fundações Direcionais Estáticas (4 Vistas · Sem Arma)</h2>
    <div class="grid4">{dir_cards}</div>
  </article>

  {before_after_section}

  <article>
    <h2>Matriz Completa de Cobertura e Status do Manifesto (28 Clipes)</h2>
    <table>
      <thead>
        <tr><th>Ação</th><th>Direção</th><th>Quadros</th><th>Duração</th><th>Semântica</th><th>Visibilidade Arma</th><th>Status Manifesto</th><th>Aprovação Artística</th><th>Notas Técnicas / Diagnóstico</th><th>Fontes</th></tr>
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
    (out_dir / 'manifest.json').write_text(json.dumps({
        'revision': revision,
        'character': 'orc-v1',
        'files': files,
        'totalFiles': len(files),
    }, ensure_ascii=False, indent=2), encoding='utf-8')
    (out_dir / 'catalogo.json').write_text(json.dumps({
        'revision': revision,
        'character': 'orc-v1',
        'manifestSource': str(manifest_path.relative_to(R)),
        'baselineManifestSource': (str(baseline_manifest_path.relative_to(R))
                                   if baseline_manifest_path is not None else None),
        'directions': DIRECTIONS,
        'actions': ACTIONS,
        'cells': len(cells_list),
        'activeCandidates': active_ids,
        'unchangedAliases': alias_ids,
        'inRevision': revision_ids,
        'inProduction': production_ids,
        'affectedCells': affected_ids,
        'knownBadCells': known_bad_ids,
        'packageStatus': package_status,
        'technicalStatus': manifest_data.get('technicalStatus', 'NOT_VERIFIED'),
        'artisticStatus': package_status,
        'artisticApproval': 'PENDING_CREATOR',
        'eligibleForIntegration': eligibility,
        'runtimeImplemented': False,
    }, ensure_ascii=False, indent=2), encoding='utf-8')

    print(f"Build complete. Index written to: {out_dir / 'index.html'}")
    print(f"Total files copied/indexed: {len(files)}")
    return {
        'page': str(out_dir / 'index.html'),
        'copiedFiles': len(files),
        'manifestSource': str(manifest_path),
        'status': 'OK'
    }

def main():
    parser = argparse.ArgumentParser(description="Build Orc V1 Rear Recovery v2 interactive review studio.")
    parser.add_argument('--manifest', type=str, default=str(DEFAULT_MANIFEST), help="Path to candidate28manifest.json")
    parser.add_argument('--out-dir', type=str, default=str(DEFAULT_OUT_DIR), help="Output directory for isolated review")
    parser.add_argument('--baseline-manifest', type=str, help="Explicit 28-cell manifest for before comparisons; defaults to complete-v1")
    parser.add_argument('--check-only', action='store_true', help="Only validate manifest and input paths")
    args = parser.parse_args()

    manifest_p = Path(args.manifest)
    if not manifest_p.is_absolute():
        manifest_p = R / manifest_p

    out_p = Path(args.out_dir)
    if not out_p.is_absolute():
        out_p = R / out_p

    baseline_p = Path(args.baseline_manifest) if args.baseline_manifest else None
    if baseline_p is not None and not baseline_p.is_absolute():
        baseline_p = R / baseline_p
    res = build_rear_recovery_review(manifest_p, out_p, check_only=args.check_only,
                                     baseline_manifest_path=baseline_p)
    print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
