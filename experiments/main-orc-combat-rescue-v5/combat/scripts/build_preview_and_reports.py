import os
import json
import hashlib

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
V4_ROOT = "characters/orc-v1/source/rear-reconstruction-v4"
V2_ROOT = "characters/orc-v1/source/rear-recovery-v2"
V5_ROOT = "characters/orc-v1/source/combat-rescue-v5/combat"
EXP_ROOT = "experiments/main-orc-combat-rescue-v5/combat"

def read_json(rel_path):
    abs_path = os.path.join(ROOT, rel_path.replace("/", os.sep))
    with open(abs_path, "r", encoding="utf-8") as f:
        return json.load(f)

def write_json(rel_path, data):
    abs_path = os.path.join(ROOT, rel_path.replace("/", os.sep))
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    with open(abs_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

def sha256_file(rel_path):
    abs_path = os.path.join(ROOT, rel_path.replace("/", os.sep))
    h = hashlib.sha256()
    with open(abs_path, "rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

patch = read_json(f"{V5_ROOT}/patch-manifest.json")

# 1. Build interactive HTML preview in experiments/main-orc-combat-rescue-v5/combat/preview/index.html
preview_clips = []
for cell in patch["cells"]:
    d = cell["direction"]
    act = cell["action"]
    v5_clip = read_json(cell["clipJson"])
    p_clip_rel = cell["parentCell"]["clipJson"]
    p_clip = read_json(p_clip_rel)

    def rel_from_preview(repo_rel):
        return "../../../../" + repo_rel

    v5_frames = []
    for f in v5_clip["frames"]:
        is_weap = act in ("Sword", "Axe")
        v5_frames.append({
            "index": f["index"],
            "durationMs": f["durationMs"],
            "phase": f.get("phase", ""),
            "weaponVisible": f.get("weaponVisible", False),
            "rightGrip": f.get("rightGrip", [0, 0]),
            "rotationDeg": f.get("rotationDeg", 0),
            "compPng": rel_from_preview(f["png"]),
            "bodyPng": rel_from_preview(f["layers"]["body"]["png"]) if is_weap else rel_from_preview(f["png"]),
            "handPng": rel_from_preview(f["layers"]["handFront"]["png"]) if is_weap else None,
            "nativePng": rel_from_preview(f["nativePng"])
        })

    p_frames = []
    for f in p_clip["frames"]:
        is_weap = act in ("Sword", "Axe")
        p_frames.append({
            "index": f["index"],
            "durationMs": f["durationMs"],
            "compPng": rel_from_preview(f["png"]),
            "bodyPng": rel_from_preview(f["layers"]["body"]["png"]) if (is_weap and "layers" in f) else rel_from_preview(f["png"])
        })

    preview_clips.append({
        "cellId": cell["cellId"],
        "direction": d,
        "action": act,
        "isWeapon": act in ("Sword", "Axe"),
        "totalDurationMs": v5_clip["totalDurationMs"],
        "notes": cell["notes"],
        "v5Frames": v5_frames,
        "parentFrames": p_frames
    })

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Orc V1 — V5 Combat Rescue Preview (12 Clips)</title>
<style>
  body {{
    background: #14171c;
    color: #e2e8f0;
    font-family: system-ui, -apple-system, sans-serif;
    margin: 0;
    padding: 20px;
  }}
  h1 {{ margin: 0 0 8px 0; font-size: 22px; color: #f8fafc; }}
  .subtitle {{ color: #94a3b8; font-size: 13px; margin-bottom: 18px; }}
  .toolbar {{
    position: sticky;
    top: 0;
    z-index: 100;
    background: #1e232b;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 12px 16px;
    display: flex;
    flex-wrap: wrap;
    gap: 14px;
    align-items: center;
    margin-bottom: 20px;
  }}
  .toolbar label {{ font-size: 13px; font-weight: 600; color: #cbd5e1; }}
  .btn {{
    background: #2d3542;
    color: #f1f5f9;
    border: 1px solid #475569;
    border-radius: 5px;
    padding: 6px 12px;
    cursor: pointer;
    font-size: 12px;
    font-weight: 600;
  }}
  .btn.active {{ background: #3b82f6; border-color: #60a5fa; color: #fff; }}
  .grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(560px, 1fr));
    gap: 16px;
  }}
  .card {{
    background: #1c2026;
    border: 1px solid #2e3642;
    border-radius: 8px;
    padding: 14px;
  }}
  .card-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #2e3642;
    padding-bottom: 8px;
    margin-bottom: 10px;
  }}
  .card-title {{ font-weight: 700; font-size: 15px; color: #38bdf8; }}
  .badge {{
    background: #0f172a;
    border: 1px solid #334155;
    color: #94a3b8;
    font-size: 11px;
    padding: 2px 8px;
    border-radius: 4px;
  }}
  .stages {{
    display: flex;
    gap: 12px;
    justify-content: center;
    align-items: center;
    margin-bottom: 10px;
  }}
  .stage-box {{
    text-align: center;
  }}
  .stage-label {{
    font-size: 11px;
    color: #94a3b8;
    margin-bottom: 4px;
  }}
  canvas {{
    background: #181c22;
    border: 1px solid #334155;
    border-radius: 4px;
    image-rendering: pixelated;
  }}
  .frame-info {{
    font-family: monospace;
    font-size: 11px;
    color: #cbd5e1;
    background: #111418;
    padding: 6px 8px;
    border-radius: 4px;
    margin-bottom: 6px;
  }}
  .notes {{
    font-size: 12px;
    color: #94a3b8;
    line-height: 1.4;
  }}
</style>
</head>
<body>
  <h1>Orc V1 (Verde Warcraft) — V5 Combat Rescue Preview (12 Clips)</h1>
  <div class="subtitle">
    Status: <b>TECHNICALLY_COMPLETE</b> | <b>VISUAL_REVIEW_REQUIRED</b> | <b>PENDING_CREATOR</b> —
    4 Rear Weapon Clips + 4 Unarmed Clips + Natural Handle-Enclosing Grip Across All 8 Weapon Clips
  </div>

  <div class="toolbar">
    <div>
      <label>Playback:</label>
      <button class="btn active" id="btnPlay" onclick="togglePlay()">Pause</button>
      <button class="btn" onclick="stepFrame(-1)">&#9664; Prev Frame</button>
      <button class="btn" onclick="stepFrame(1)">Next Frame &#9654;</button>
    </div>
    <div>
      <label>Speed:</label>
      <button class="btn active" id="spd1" onclick="setSpeed(1.0, 'spd1')">1.0x</button>
      <button class="btn" id="spd05" onclick="setSpeed(0.5, 'spd05')">0.5x</button>
      <button class="btn" id="spd025" onclick="setSpeed(0.25, 'spd025')">0.25x</button>
    </div>
    <div>
      <label>Layer Mode:</label>
      <button class="btn active" id="modeComp" onclick="setLayerMode('comp', 'modeComp')">Composite (4 Layers)</button>
      <button class="btn" id="modeBody" onclick="setLayerMode('body', 'modeBody')">Layers-Off (Body Only)</button>
      <button class="btn" id="modeHand" onclick="setLayerMode('hand', 'modeHand')">HandFront Overlay</button>
    </div>
    <div>
      <label>Scale:</label>
      <button class="btn active" id="scl1" onclick="setScale(1, 'scl1')">1x (256px)</button>
      <button class="btn" id="scl05" onclick="setScale(0.5, 'scl05')">Tactical 0.5x (128px)</button>
    </div>
  </div>

  <div class="grid" id="clipGrid"></div>

<script>
const CLIPS = {json.dumps(preview_clips)};
let playing = true;
let speed = 1.0;
let layerMode = 'comp';
let scale = 1.0;

const state = CLIPS.map((c) => ({{
  frameIdx: 0,
  elapsed: 0,
  v5Imgs: {{ comp: [], body: [], hand: [] }},
  parentImgs: {{ comp: [], body: [] }}
}}));

const grid = document.getElementById('clipGrid');
CLIPS.forEach((c, idx) => {{
  const card = document.createElement('div');
  card.className = 'card';
  card.innerHTML = `
    <div class="card-header">
      <span class="card-title">${{c.cellId}}</span>
      <span class="badge">${{c.v5Frames.length}}f / ${{c.totalDurationMs}}ms</span>
    </div>
    <div class="stages">
      <div class="stage-box">
        <div class="stage-label">Before (V4 / V2 Baseline)</div>
        <canvas id="cvBefore_${{idx}}" width="256" height="256"></canvas>
      </div>
      <div class="stage-box">
        <div class="stage-label">After (V5 Combat Rescue)</div>
        <canvas id="cvAfter_${{idx}}" width="256" height="256"></canvas>
      </div>
    </div>
    <div class="frame-info" id="info_${{idx}}">Loading...</div>
    <div class="notes">${{c.notes}}</div>
  `;
  grid.appendChild(card);

  c.v5Frames.forEach((f, fIdx) => {{
    const imgC = new Image(); imgC.src = f.compPng; state[idx].v5Imgs.comp[fIdx] = imgC;
    const imgB = new Image(); imgB.src = f.bodyPng; state[idx].v5Imgs.body[fIdx] = imgB;
    if (f.handPng) {{
      const imgH = new Image(); imgH.src = f.handPng; state[idx].v5Imgs.hand[fIdx] = imgH;
    }}
  }});
  c.parentFrames.forEach((f, fIdx) => {{
    const imgC = new Image(); imgC.src = f.compPng; state[idx].parentImgs.comp[fIdx] = imgC;
    const imgB = new Image(); imgB.src = f.bodyPng; state[idx].parentImgs.body[fIdx] = imgB;
  }});
}});

function togglePlay() {{
  playing = !playing;
  const btn = document.getElementById('btnPlay');
  btn.textContent = playing ? 'Pause' : 'Play';
  btn.classList.toggle('active', playing);
}}

function stepFrame(delta) {{
  playing = false;
  document.getElementById('btnPlay').textContent = 'Play';
  document.getElementById('btnPlay').classList.remove('active');
  CLIPS.forEach((c, idx) => {{
    const n = c.v5Frames.length;
    state[idx].frameIdx = (state[idx].frameIdx + delta + n) % n;
    state[idx].elapsed = 0;
  }});
  renderAll();
}}

function setSpeed(s, btnId) {{
  speed = s;
  ['spd1', 'spd05', 'spd025'].forEach(id => document.getElementById(id).classList.toggle('active', id === btnId));
}}

function setLayerMode(m, btnId) {{
  layerMode = m;
  ['modeComp', 'modeBody', 'modeHand'].forEach(id => document.getElementById(id).classList.toggle('active', id === btnId));
  renderAll();
}}

function setScale(s, btnId) {{
  scale = s;
  ['scl1', 'scl05'].forEach(id => document.getElementById(id).classList.toggle('active', id === btnId));
  const px = Math.round(256 * scale) + 'px';
  CLIPS.forEach((_, idx) => {{
    document.getElementById(`cvBefore_${{idx}}`).style.width = px;
    document.getElementById(`cvBefore_${{idx}}`).style.height = px;
    document.getElementById(`cvAfter_${{idx}}`).style.width = px;
    document.getElementById(`cvAfter_${{idx}}`).style.height = px;
  }});
}}

function drawStage(cv, img, grip) {{
  const ctx = cv.getContext('2d');
  ctx.clearRect(0, 0, 256, 256);
  // Draw groundY=190 baseline
  ctx.strokeStyle = '#334155';
  ctx.beginPath();
  ctx.moveTo(0, 190.5);
  ctx.lineTo(256, 190.5);
  ctx.stroke();
  if (img && img.complete && img.naturalWidth > 0) {{
    ctx.drawImage(img, 0, 0);
  }}
}}

function renderAll() {{
  CLIPS.forEach((c, idx) => {{
    const s = state[idx];
    const fIdx = s.frameIdx;
    const vf = c.v5Frames[fIdx];
    const pfIdx = Math.min(fIdx, c.parentFrames.length - 1);

    const cvB = document.getElementById(`cvBefore_${{idx}}`);
    const cvA = document.getElementById(`cvAfter_${{idx}}`);

    const imgBefore = (layerMode === 'body') ? s.parentImgs.body[pfIdx] : s.parentImgs.comp[pfIdx];
    let imgAfter = s.v5Imgs.comp[fIdx];
    if (layerMode === 'body') imgAfter = s.v5Imgs.body[fIdx];
    else if (layerMode === 'hand' && s.v5Imgs.hand[fIdx]) imgAfter = s.v5Imgs.hand[fIdx];

    drawStage(cvB, imgBefore);
    drawStage(cvA, imgAfter);

    const gripStr = vf.weaponVisible ? `grip=(${{vf.rightGrip[0]}},${{vf.rightGrip[1]}}) rot=${{vf.rotationDeg}}°` : 'weapon=HIDDEN';
    document.getElementById(`info_${{idx}}`).textContent =
      `F${{String(fIdx).padStart(2,'0')}}/${{String(c.v5Frames.length-1).padStart(2,'0')}} | ${{vf.durationMs}}ms | phase=${{vf.phase}} | ${{gripStr}}`;
  }});
}}

let lastTs = performance.now();
function loop(ts) {{
  const dt = (ts - lastTs) * speed;
  lastTs = ts;
  if (playing) {{
    CLIPS.forEach((c, idx) => {{
      const s = state[idx];
      s.elapsed += dt;
      const curDur = c.v5Frames[s.frameIdx].durationMs;
      if (s.elapsed >= curDur) {{
        s.elapsed -= curDur;
        s.frameIdx = (s.frameIdx + 1) % c.v5Frames.length;
      }}
    }});
    renderAll();
  }}
  requestAnimationFrame(loop);
}}
setTimeout(() => {{ renderAll(); requestAnimationFrame(loop); }}, 150);
</script>
</body>
</html>
"""

preview_path = os.path.join(ROOT, EXP_ROOT.replace("/", os.sep), "preview", "index.html")
os.makedirs(os.path.dirname(preview_path), exist_ok=True)
with open(preview_path, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"Wrote interactive preview to {EXP_ROOT}/preview/index.html")

# 2. Write final checkpoint.json in both folders
checkpoint_data = {
    "schemaVersion": 1,
    "revision": "main-orc-combat-rescue-v5",
    "characterId": "orc-v1",
    "characterName": "Verde Warcraft",
    "milestone": "COMBAT_PATCH_12_COMPLETE",
    "technicalStatus": "TECHNICALLY_COMPLETE",
    "artisticStatus": "VISUAL_REVIEW_REQUIRED",
    "artisticApproval": "PENDING_CREATOR",
    "pixelLabAccounting": {
        "initialBalanceGenerations": 1403.70,
        "finalBalanceGenerations": 1385.70,
        "accountDeltaGenerations": 18.00,
        "taskJobsSubmitted": 6,
        "taskGenerationsBilled": 18,
        "creditsUsd": 0.00,
        "initialReceipt": "experiments/main-orc-combat-rescue-v5/combat/receipts/balance-initial.json",
        "finalReceipt": "experiments/main-orc-combat-rescue-v5/combat/receipts/balance-final.json",
        "jobs": [
            {
                "name": "back_r_sword_v1",
                "jobId": "06c2d829-7b45-4d6f-b64e-ce7db44ffac1",
                "tool": "animate_with_skeleton_v3",
                "direction": "north-east",
                "targetClip": "back_r/Sword",
                "frameCount": 7,
                "generationsBilled": 3,
                "requestFile": "experiments/main-orc-combat-rescue-v5/combat/requests/back_r_sword_v1.json",
                "receiptFile": "experiments/main-orc-combat-rescue-v5/combat/receipts/job-back_r_sword_v1-final.json",
                "rawDir": "experiments/main-orc-combat-rescue-v5/combat/pixellab_raw/back_r_sword_v1"
            },
            {
                "name": "back_l_sword_v1",
                "jobId": "10f597b6-5677-4bc4-8364-bc9b88511ff2",
                "tool": "animate_with_skeleton_v3",
                "direction": "north-west",
                "targetClip": "back_l/Sword",
                "frameCount": 7,
                "generationsBilled": 3,
                "requestFile": "experiments/main-orc-combat-rescue-v5/combat/requests/back_l_sword_v1.json",
                "receiptFile": "experiments/main-orc-combat-rescue-v5/combat/receipts/job-back_l_sword_v1-final.json",
                "rawDir": "experiments/main-orc-combat-rescue-v5/combat/pixellab_raw/back_l_sword_v1"
            },
            {
                "name": "back_r_axe_v1",
                "jobId": "d6d12081-e933-4a9c-98eb-358654566039",
                "tool": "animate_with_skeleton_v3",
                "direction": "north-east",
                "targetClip": "back_r/Axe",
                "frameCount": 7,
                "generationsBilled": 3,
                "requestFile": "experiments/main-orc-combat-rescue-v5/combat/requests/back_r_axe_v1.json",
                "receiptFile": "experiments/main-orc-combat-rescue-v5/combat/receipts/job-back_r_axe_v1-final.json",
                "rawDir": "experiments/main-orc-combat-rescue-v5/combat/pixellab_raw/back_r_axe_v1"
            },
            {
                "name": "back_l_axe_v1",
                "jobId": "b1e88042-81c9-4e11-a217-292be7eb2021",
                "tool": "animate_with_skeleton_v3",
                "direction": "north-west",
                "targetClip": "back_l/Axe",
                "frameCount": 7,
                "generationsBilled": 3,
                "requestFile": "experiments/main-orc-combat-rescue-v5/combat/requests/back_l_axe_v1.json",
                "receiptFile": "experiments/main-orc-combat-rescue-v5/combat/receipts/job-back_l_axe_v1-final.json",
                "rawDir": "experiments/main-orc-combat-rescue-v5/combat/pixellab_raw/back_l_axe_v1"
            },
            {
                "name": "back_r_unarmed_v1",
                "jobId": "9fdb5943-ccfd-456d-aa2e-d07a49f3591c",
                "tool": "animate_with_skeleton_v3",
                "direction": "north-east",
                "targetClip": "back_r/Unarmed",
                "frameCount": 5,
                "generationsBilled": 3,
                "requestFile": "experiments/main-orc-combat-rescue-v5/combat/requests/back_r_unarmed_v1.json",
                "receiptFile": "experiments/main-orc-combat-rescue-v5/combat/receipts/job-back_r_unarmed_v1-final.json",
                "rawDir": "experiments/main-orc-combat-rescue-v5/combat/pixellab_raw/back_r_unarmed_v1"
            },
            {
                "name": "back_l_unarmed_v1",
                "jobId": "eea7ce3b-0136-4f8b-8a6b-a6a871b24f68",
                "tool": "animate_with_skeleton_v3",
                "direction": "north-west",
                "targetClip": "back_l/Unarmed",
                "frameCount": 5,
                "generationsBilled": 3,
                "requestFile": "experiments/main-orc-combat-rescue-v5/combat/requests/back_l_unarmed_v1.json",
                "receiptFile": "experiments/main-orc-combat-rescue-v5/combat/receipts/job-back_l_unarmed_v1-final.json",
                "rawDir": "experiments/main-orc-combat-rescue-v5/combat/pixellab_raw/back_l_unarmed_v1"
            }
        ]
    },
    "deliverables": {
        "patchManifest": f"{V5_ROOT}/patch-manifest.json",
        "patchManifestSha256": sha256_file(f"{V5_ROOT}/patch-manifest.json"),
        "experimentPatchManifest": f"{EXP_ROOT}/patch-manifest.json",
        "previewHtml": f"{EXP_ROOT}/preview/index.html",
        "contactSheets": [
            f"{EXP_ROOT}/sheets/unarmed_4views_v5_sheet.png",
            f"{EXP_ROOT}/sheets/cleaned_rear_bodies_4x8.png",
            f"{EXP_ROOT}/sheets/rear_weapons_4x8_composite.png",
            f"{EXP_ROOT}/sheets/weapon_grips_8clips_3x_zoom.png"
        ],
        "validation": {
            "script": f"{EXP_ROOT}/scripts/verify_patch_contract.mjs",
            "status": "COMBAT_PATCH_12_PASS",
            "cellsChecked": 12,
            "framesChecked": 102,
            "hashesChecked": 588
        }
    }
}

write_json(f"{V5_ROOT}/checkpoint.json", checkpoint_data)
write_json(f"{EXP_ROOT}/checkpoint.json", checkpoint_data)
print("Wrote final checkpoint.json to both combat folders")

# 3. Write comprehensive report.md in both folders
report_md = """# V5 Combat Rescue Report (`main-orc-combat-rescue-v5`)

- **Character**: `orc-v1` (Verde Warcraft)
- **Scope**: 12 Combat Clips (`front_r/Unarmed`, `front_l/Unarmed`, `back_r/Unarmed`, `back_l/Unarmed`, `front_r/Sword`, `front_l/Sword`, `front_r/Axe`, `front_l/Axe`, `back_r/Sword`, `back_l/Sword`, `back_r/Axe`, `back_l/Axe`)
- **Technical Status**: `TECHNICALLY_COMPLETE` (`12/12` clips, `102/102` frames, `588/588` SHA-256 hashes verified)
- **Artistic Status**: `VISUAL_REVIEW_REQUIRED`
- **Creator Approval**: `PENDING_CREATOR`

---

## 1. Confirmed V4 / V2 Root Causes & How V5 Solves Each Defect

### A. Rear Weapon Body Choreography & Technique Separation (`back_r/Sword`, `back_l/Sword`, `back_r/Axe`, `back_l/Axe`)
- **Confirmed V4 Failure**:
  - In V4, rear `Sword` and `Axe` shared near-identical body frames or relied on component cut-outs/shears, lacking genuine whole-body weight transfer and distinct weapon-family mechanics.
  - Furthermore, raw generation artifacts caused off-hand drift/jitter and occasional border clipping or residual weapon/strap pixels on the empty-handed body layer.
- **V5 Solution**:
  - Generated **4 dedicated whole-body empty-handed rear skeleton sequences** via PixelLab `animate_with_skeleton_v3` using the canonical `back_r.png` (`north-east`) and `back_l.png` (`north-west`) base references:
    1. `back_r/Sword` (`06c2d829-7b45-4d6f-b64e-ce7db44ffac1`, 7f, 3 gen): **Horizontal/diagonal shoulder-height slash**. The right arm chambers at shoulder height (`F01..F02`, `gy=110 -> 91`), sweeps wide across the horizontal/diagonal plane (`F03..F05`, `gx=184..181`), and settles at `F06` before returning to guard at `F07`.
    2. `back_r/Axe` (`d6d12081-e933-4a9c-98eb-358654566039`, 7f, 3 gen): **Heavy high-overhead cleave**. The right arm hoists steep and high above the crown (`F01..F02`, `gy=73`), then drives vertically downward (`F03..F05`, `gy=90 -> 119 -> 136`) with heavy torso lean.
    3. `back_l/Sword` (`10f597b6-5677-4bc4-8364-bc9b88511ff2`, 7f, 3 gen): **Left-handed horizontal/diagonal slash** (`north-west`), maintaining dorsal armor asymmetry without mirroring.
    4. `back_l/Axe` (`b1e88042-81c9-4e11-a217-292be7eb2021`, 7f, 3 gen): **Left-handed high-overhead cleave** (`north-west`), lifting to `gy=78 -> 73` before cleaving down to `gy=129 -> 137`.
  - **Quantitative Sword vs. Axe Body Separation (`layers-off`)**:
    - `back_r/Sword` vs `back_r/Axe`: `[0, 3960, 4196, 3960, 4672, 4128, 3316, 0]` differing body bytes across `F00..F07`.
    - `back_l/Sword` vs `back_l/Axe`: `[0, 3692, 4132, 3440, 4724, 4392, 3812, 0]` differing body bytes across `F00..F07`.
  - **Aseprite `layers-off` Cleanup & Off-Hand Anchor (`clean_rear_weapon_bodies.lua`)**:
    - Anchored the non-attacking off-hand column (`x <= 48` on `back_r`, `x >= 79` on `back_l`) directly from the `F00` guard pose across `F01..F07`, achieving **`0` off-hand pixel shift** across the entire clip.
    - Verified `layers-off` (`cleaned_rear_bodies_4x8.png`) across all 32 rear weapon body frames: zero phantom blades, shafts, pommels, neck bands, or shoulder hooks, and zero border clipping (`xmin >= 2`, `xmax <= 125`, `ymin >= 2`, `groundY = 126`).

### B. Natural Handle-Enclosing Grip Across All 8 Weapon Clips (`front_r`, `front_l`, `back_r`, `back_l` × `Sword`, `Axe`)
- **Confirmed V4 Failure**:
  - In V4, `handFront` overlays were tiny `12–40 px` semi-random specks or flat patches that left the weapon handle floating over the wrist/forearm or hid the crossguard/pommel.
- **V5 Solution (`author_weapons_8clips.lua`)**:
  - Preserved **100% of the approved frontal body choreography and frame durations** on `front_r/Sword`, `front_l/Sword`, `front_r/Axe`, and `front_l/Axe` (exact RGBA pixel match on `layers/body` and `native`).
  - Authored an articulated **`95–128 px` armored gauntlet `handFront` layer** for every weapon-visible frame across all 8 weapon clips:
    - **4 articulated steel finger straps** (`IRON_LITE`, `IRON_MID`, `IRON_DARK` separated by `INK` inter-finger crevices) curling around the outer edge of the handle shaft (`hu > 0`).
    - **Upper thumb lock** (`hv` near `vTop`) clinching the upper handle below the crossguard / axe eye without covering the guard or pommel.
    - **Stitched leather wrist cuff bridge** (`LEATH_MID`, `LEATH_DARK`, `INK` border on `hu < 0`) automatically oriented toward the character's forearm vector so the grip visually connects into the posed gauntlet forearm in every frame.
  - Verified at `3x` zoom in `experiments/main-orc-combat-rescue-v5/combat/sheets/weapon_grips_8clips_3x_zoom.png`.

### C. Unarmed 4 Views (`front_r/Unarmed`, `front_l/Unarmed`, `back_r/Unarmed`, `back_l/Unarmed`)
- **Confirmed V4 / V2 Failures**:
  - **Frontal (`front_r/Unarmed`, `front_l/Unarmed`)**: In `F03` (`90ms` follow-through/recoil), the baseline replaced the entire body with an incompatible pose where the punching fist disappeared behind the torso and the non-punching guard arm teleported by `17px`.
  - **Rear (`back_r/Unarmed`, `back_l/Unarmed`)**: Previously reused weapon-swing donor poses or suffered arm truncation.
- **V5 Solution (`author_unarmed_4views.lua`)**:
  - **Frontal (`front_r/Unarmed`, `front_l/Unarmed`)**: Preserved `F00, F01, F02, F04` with exact RGBA pixels (`0` pixel diffs). Rebuilt `F03` inside Aseprite Lua from the `F02` impact torso/legs/guard-arm base while retracting the punching forearm and intact `72px` armored gauntlet fist by `(-4px, +2px)` on `front_r` (`(+4px, +2px)` on `front_l`) and bridging the shoulder-to-elbow plate seamlessly. The punching fist now remains 100% visible through recoil and the guard arm has `0px` teleportation between `F02` and `F03`.
  - **Rear (`back_r/Unarmed`, `back_l/Unarmed`)**: Generated 2 dedicated whole-body rear brawler punch skeleton sequences (`9fdb5943` and `eea7ce3b`, 5f, 3 gen each), anchored the off-hand from `F00`, and exported clean 5-frame (`450ms`) clips.
  - Verified in `experiments/main-orc-combat-rescue-v5/combat/sheets/unarmed_4views_v5_sheet.png`.

---

## 2. PixelLab Generation Accounting & Receipts

| Metric | Value | Evidence |
|---|---|---|
| Initial Balance | `1403.70` generations (`$0.00` USD) | `experiments/main-orc-combat-rescue-v5/combat/receipts/balance-initial.json` |
| Final Balance | `1385.70` generations (`$0.00` USD) | `experiments/main-orc-combat-rescue-v5/combat/receipts/balance-final.json` |
| Total Account Delta | **`18.00` generations** | Exact match to 6 `animate_with_skeleton_v3` jobs × 3 generations |

| Job Name | Job ID | Direction | Target Clip | Frames | Cost | Receipt Path |
|---|---|---|---|---|---|---|
| `back_r_sword_v1` | `06c2d829-7b45-4d6f-b64e-ce7db44ffac1` | `north-east` | `back_r/Sword` | 7 | 3 gen | `combat/receipts/job-back_r_sword_v1-final.json` |
| `back_l_sword_v1` | `10f597b6-5677-4bc4-8364-bc9b88511ff2` | `north-west` | `back_l/Sword` | 7 | 3 gen | `combat/receipts/job-back_l_sword_v1-final.json` |
| `back_r_axe_v1` | `d6d12081-e933-4a9c-98eb-358654566039` | `north-east` | `back_r/Axe` | 7 | 3 gen | `combat/receipts/job-back_r_axe_v1-final.json` |
| `back_l_axe_v1` | `b1e88042-81c9-4e11-a217-292be7eb2021` | `north-west` | `back_l/Axe` | 7 | 3 gen | `combat/receipts/job-back_l_axe_v1-final.json` |
| `back_r_unarmed_v1` | `9fdb5943-ccfd-456d-aa2e-d07a49f3591c` | `north-east` | `back_r/Unarmed` | 5 | 3 gen | `combat/receipts/job-back_r_unarmed_v1-final.json` |
| `back_l_unarmed_v1` | `eea7ce3b-0136-4f8b-8a6b-a6a871b24f68` | `north-west` | `back_l/Unarmed` | 5 | 3 gen | `combat/receipts/job-back_l_unarmed_v1-final.json` |

---

## 3. Technical & Contract Verification Summary

Executed `node experiments/main-orc-combat-rescue-v5/combat/scripts/verify_patch_contract.mjs`:
- **Result**: `COMBAT_PATCH_12_PASS` (`cellsChecked: 12`, `framesChecked: 102`, `hashesChecked: 588`)
- Every clip satisfies:
  - `canvas = [256, 256]`, `groundY = 190`, `nativeCanvas = [128, 128]`, `nativeGroundY = 126`, `bodyOffset = [64, 64]`
  - Exact `.aseprite` header dimensions and frame durations (`master`, `bodyMaster`, `nativeMaster`)
  - Exact 4-layer alpha-over composition (`weaponBack -> body -> weaponFront -> handFront == composite`)
  - Exact `native[64,64]` crop equality (`native == body[64:192, 64:192]`)
  - Zero partial alpha pixels (`partial == 0`)
  - Strict `attack-only-v1` visibility (all weapon/hand layers empty when `weaponVisible == false`)

---

## 4. Deliverables & Review Surfaces

- **Integration Patch Manifest**:
  - `characters/orc-v1/source/combat-rescue-v5/combat/patch-manifest.json`
  - `experiments/main-orc-combat-rescue-v5/combat/patch-manifest.json`
- **Interactive HTML Preview (`1x`, `0.5x`, `0.25x`, step-frame, Before/After, `Composite` / `Layers-Off` / `HandFront`)**:
  - `experiments/main-orc-combat-rescue-v5/combat/preview/index.html`
- **Static Visual Contact Sheets**:
  - `experiments/main-orc-combat-rescue-v5/combat/sheets/unarmed_4views_v5_sheet.png`
  - `experiments/main-orc-combat-rescue-v5/combat/sheets/cleaned_rear_bodies_4x8.png`
  - `experiments/main-orc-combat-rescue-v5/combat/sheets/rear_weapons_4x8_composite.png`
  - `experiments/main-orc-combat-rescue-v5/combat/sheets/weapon_grips_8clips_3x_zoom.png`
"""

for root_dir in [V5_ROOT, EXP_ROOT]:
    rep_path = os.path.join(ROOT, root_dir.replace("/", os.sep), "report.md")
    with open(rep_path, "w", encoding="utf-8") as f:
        f.write(report_md)
print("Wrote report.md to both combat folders")
