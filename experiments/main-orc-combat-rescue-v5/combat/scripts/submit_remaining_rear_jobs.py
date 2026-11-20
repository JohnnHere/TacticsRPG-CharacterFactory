import json
import base64
import subprocess
from pathlib import Path
from PIL import Image
import numpy as np

ROOT = Path(".")
EXP_DIR = ROOT / "experiments/main-orc-combat-rescue-v5/combat"
REQ_DIR = EXP_DIR / "requests"
REC_DIR = EXP_DIR / "receipts"
RAW_DIR = EXP_DIR / "raw"

# Ensure back_l_base_128.png exists
back_l_base_path = RAW_DIR / "back_l_base_128.png"
if not back_l_base_path.exists():
    src_l = ROOT / "characters/orc-v1/source/rear-reconstruction-v4/back_l/Sword/native/00.png"
    im_l = Image.open(src_l).convert("RGBA")
    im_l.save(back_l_base_path)

back_r_b64 = base64.b64encode((RAW_DIR / "back_r_base_128.png").read_bytes()).decode("ascii")
back_l_b64 = base64.b64encode(back_l_base_path.read_bytes()).decode("ascii")

def make_skel_back_r(r_sh, r_el, r_wr, l_sh, l_el, l_wr, neck, head_dx=0.0, head_dy=0.0, hip_dx=0.0, hip_dy=0.0):
    nx, ny = neck
    return [
        {"label": "NOSE", "x": round(nx + 0.01 + head_dx, 4), "y": round(ny - 0.08 + head_dy, 4), "z_index": 0},
        {"label": "NECK", "x": round(nx, 4), "y": round(ny, 4), "z_index": 1},
        {"label": "RIGHT SHOULDER", "x": round(r_sh[0], 4), "y": round(r_sh[1], 4), "z_index": 2},
        {"label": "RIGHT ELBOW", "x": round(r_el[0], 4), "y": round(r_el[1], 4), "z_index": 3},
        {"label": "RIGHT ARM", "x": round(r_wr[0], 4), "y": round(r_wr[1], 4), "z_index": 4},
        {"label": "LEFT SHOULDER", "x": round(l_sh[0], 4), "y": round(l_sh[1], 4), "z_index": 1},
        {"label": "LEFT ELBOW", "x": round(l_el[0], 4), "y": round(l_el[1], 4), "z_index": 1},
        {"label": "LEFT ARM", "x": round(l_wr[0], 4), "y": round(l_wr[1], 4), "z_index": 1},
        {"label": "RIGHT HIP", "x": round(0.55 + hip_dx, 4), "y": round(0.56 + hip_dy, 4), "z_index": 1},
        {"label": "RIGHT KNEE", "x": round(0.57 + hip_dx*0.5, 4), "y": round(0.75 + hip_dy*0.5, 4), "z_index": 1},
        {"label": "RIGHT LEG", "x": 0.58, "y": 0.94, "z_index": 1},
        {"label": "LEFT HIP", "x": round(0.42 + hip_dx, 4), "y": round(0.56 + hip_dy, 4), "z_index": 1},
        {"label": "LEFT KNEE", "x": round(0.39 + hip_dx*0.5, 4), "y": round(0.75 + hip_dy*0.5, 4), "z_index": 1},
        {"label": "LEFT LEG", "x": 0.37, "y": 0.94, "z_index": 1},
        {"label": "RIGHT EYE", "x": round(nx + 0.03 + head_dx, 4), "y": round(ny - 0.09 + head_dy, 4), "z_index": 0},
        {"label": "LEFT EYE", "x": round(nx - 0.02 + head_dx, 4), "y": round(ny - 0.09 + head_dy, 4), "z_index": 0},
        {"label": "RIGHT EAR", "x": round(nx + 0.05 + head_dx, 4), "y": round(ny - 0.08 + head_dy, 4), "z_index": 1},
        {"label": "LEFT EAR", "x": round(nx - 0.04 + head_dx, 4), "y": round(ny - 0.08 + head_dy, 4), "z_index": 1},
    ]

def make_skel_back_l(l_sh, l_el, l_wr, r_sh, r_el, r_wr, neck, head_dx=0.0, head_dy=0.0, hip_dx=0.0, hip_dy=0.0):
    # In back_l (north-west), the attacking arm on screen-left is the character's LEFT arm (dominant in back_l view),
    # and the stationary off-hand on screen-right is the RIGHT arm.
    nx, ny = neck
    return [
        {"label": "NOSE", "x": round(nx - 0.01 + head_dx, 4), "y": round(ny - 0.08 + head_dy, 4), "z_index": 0},
        {"label": "NECK", "x": round(nx, 4), "y": round(ny, 4), "z_index": 1},
        {"label": "LEFT SHOULDER", "x": round(l_sh[0], 4), "y": round(l_sh[1], 4), "z_index": 2},
        {"label": "LEFT ELBOW", "x": round(l_el[0], 4), "y": round(l_el[1], 4), "z_index": 3},
        {"label": "LEFT ARM", "x": round(l_wr[0], 4), "y": round(l_wr[1], 4), "z_index": 4},
        {"label": "RIGHT SHOULDER", "x": round(r_sh[0], 4), "y": round(r_sh[1], 4), "z_index": 1},
        {"label": "RIGHT ELBOW", "x": round(r_el[0], 4), "y": round(r_el[1], 4), "z_index": 1},
        {"label": "RIGHT ARM", "x": round(r_wr[0], 4), "y": round(r_wr[1], 4), "z_index": 1},
        {"label": "LEFT HIP", "x": round(0.45 + hip_dx, 4), "y": round(0.56 + hip_dy, 4), "z_index": 1},
        {"label": "LEFT KNEE", "x": round(0.43 + hip_dx*0.5, 4), "y": round(0.75 + hip_dy*0.5, 4), "z_index": 1},
        {"label": "LEFT LEG", "x": 0.42, "y": 0.94, "z_index": 1},
        {"label": "RIGHT HIP", "x": round(0.58 + hip_dx, 4), "y": round(0.56 + hip_dy, 4), "z_index": 1},
        {"label": "RIGHT KNEE", "x": round(0.61 + hip_dx*0.5, 4), "y": round(0.75 + hip_dy*0.5, 4), "z_index": 1},
        {"label": "RIGHT LEG", "x": 0.63, "y": 0.94, "z_index": 1},
        {"label": "LEFT EYE", "x": round(nx - 0.03 + head_dx, 4), "y": round(ny - 0.09 + head_dy, 4), "z_index": 0},
        {"label": "RIGHT EYE", "x": round(nx + 0.02 + head_dx, 4), "y": round(ny - 0.09 + head_dy, 4), "z_index": 0},
        {"label": "LEFT EAR", "x": round(nx - 0.05 + head_dx, 4), "y": round(ny - 0.08 + head_dy, 4), "z_index": 1},
        {"label": "RIGHT EAR", "x": round(nx + 0.04 + head_dx, 4), "y": round(ny - 0.08 + head_dy, 4), "z_index": 1},
    ]

first_kps_r = make_skel_back_r(
    r_sh=(0.64, 0.28), r_el=(0.71, 0.43), r_wr=(0.73, 0.56),
    l_sh=(0.33, 0.28), l_el=(0.27, 0.43), l_wr=(0.26, 0.56),
    neck=(0.49, 0.22)
)

first_kps_l = make_skel_back_l(
    l_sh=(0.36, 0.28), l_el=(0.29, 0.43), l_wr=(0.27, 0.56),
    r_sh=(0.67, 0.28), r_el=(0.73, 0.43), r_wr=(0.74, 0.56),
    neck=(0.51, 0.22)
)

# 1. back_l/Sword: diagonal sword slash matching back_r/Sword technique (7 frames F01..F07)
kps_back_l_sword = [
    # F01: chamber/windup
    make_skel_back_l((0.35, 0.26), (0.23, 0.25), (0.17, 0.19), (0.67, 0.28), (0.73, 0.43), (0.74, 0.56), (0.50, 0.22), head_dx=-0.01),
    # F02: high chamber peak
    make_skel_back_l((0.34, 0.25), (0.20, 0.20), (0.14, 0.14), (0.68, 0.29), (0.74, 0.44), (0.75, 0.56), (0.49, 0.22), head_dx=-0.01),
    # F03: diagonal slash initiation
    make_skel_back_l((0.32, 0.26), (0.17, 0.26), (0.09, 0.24), (0.69, 0.29), (0.75, 0.44), (0.75, 0.56), (0.48, 0.22), head_dx=-0.02, hip_dx=-0.01),
    # F04: wide horizontal-diagonal impact cut
    make_skel_back_l((0.31, 0.28), (0.16, 0.34), (0.08, 0.37), (0.69, 0.29), (0.75, 0.44), (0.75, 0.56), (0.48, 0.23), head_dx=-0.02, hip_dx=-0.01, hip_dy=0.01),
    # F05: low follow-through sweep
    make_skel_back_l((0.33, 0.29), (0.21, 0.40), (0.13, 0.48), (0.68, 0.29), (0.74, 0.44), (0.75, 0.56), (0.49, 0.23), head_dx=-0.01, hip_dy=0.01),
    # F06: recovery retracting arm
    make_skel_back_l((0.35, 0.28), (0.26, 0.42), (0.22, 0.53), (0.67, 0.28), (0.73, 0.43), (0.74, 0.56), (0.50, 0.22)),
    # F07: settle back to neutral guard
    first_kps_l
]

# 2. back_r/Axe: distinct HEAVY OVERHEAD CHOP technique!
# Unlike Sword's wide lateral/diagonal slash, Axe raises steeper/higher near the head/shoulder crown (within y>=0.09 so never clipped at y=0),
# coils the torso up, and drives a steep vertical-diagonal cleave downward with heavy torso drop (hip_dy=+0.02, neck_y=+0.02) to a low cleave finish!
kps_back_r_axe = [
    # F01: heavy upward hoist (elbow rises forward-up, fist hoisted above shoulder)
    make_skel_back_r((0.64, 0.26), (0.74, 0.21), (0.77, 0.13), (0.33, 0.29), (0.27, 0.44), (0.26, 0.56), (0.49, 0.21), head_dy=-0.01),
    # F02: high overhead apex coil (arm cocked high and steep behind right shoulder, torso braced)
    make_skel_back_r((0.63, 0.24), (0.72, 0.14), (0.74, 0.08), (0.33, 0.30), (0.26, 0.45), (0.25, 0.57), (0.48, 0.21), head_dx=0.01, head_dy=-0.01, hip_dy=-0.01),
    # F03: downward overhead chop commitment (driving steeply down from overhead)
    make_skel_back_r((0.67, 0.26), (0.81, 0.24), (0.89, 0.22), (0.32, 0.29), (0.26, 0.44), (0.25, 0.56), (0.51, 0.22), head_dx=0.02, hip_dx=0.01),
    # F04: heavy downward cleave impact (torso drops into the chop, arm drives down-out)
    make_skel_back_r((0.68, 0.30), (0.81, 0.41), (0.88, 0.50), (0.32, 0.30), (0.26, 0.45), (0.25, 0.57), (0.52, 0.24), head_dx=0.02, head_dy=0.02, hip_dx=0.02, hip_dy=0.02),
    # F05: deep groundward follow-through (heavy weight absorption, low fist)
    make_skel_back_r((0.67, 0.31), (0.78, 0.45), (0.83, 0.56), (0.33, 0.30), (0.27, 0.45), (0.26, 0.57), (0.51, 0.24), head_dx=0.01, head_dy=0.02, hip_dx=0.01, hip_dy=0.02),
    # F06: hauling heavy axe arm back to guard
    make_skel_back_r((0.65, 0.29), (0.73, 0.44), (0.76, 0.56), (0.33, 0.28), (0.27, 0.43), (0.26, 0.56), (0.50, 0.23), head_dy=0.01, hip_dy=0.01),
    # F07: settle to neutral guard
    first_kps_r
]

# 3. back_l/Axe: matching HEAVY OVERHEAD CHOP technique for back_l (north-west)
kps_back_l_axe = [
    # F01: heavy upward hoist
    make_skel_back_l((0.36, 0.26), (0.26, 0.21), (0.23, 0.13), (0.67, 0.29), (0.73, 0.44), (0.74, 0.56), (0.51, 0.21), head_dy=-0.01),
    # F02: high overhead apex coil
    make_skel_back_l((0.37, 0.24), (0.28, 0.14), (0.26, 0.08), (0.67, 0.30), (0.74, 0.45), (0.75, 0.57), (0.52, 0.21), head_dx=-0.01, head_dy=-0.01, hip_dy=-0.01),
    # F03: downward overhead chop commitment
    make_skel_back_l((0.33, 0.26), (0.19, 0.24), (0.11, 0.22), (0.68, 0.29), (0.74, 0.44), (0.75, 0.56), (0.49, 0.22), head_dx=-0.02, hip_dx=-0.01),
    # F04: heavy downward cleave impact
    make_skel_back_l((0.32, 0.30), (0.19, 0.41), (0.12, 0.50), (0.68, 0.30), (0.74, 0.45), (0.75, 0.57), (0.48, 0.24), head_dx=-0.02, head_dy=0.02, hip_dx=-0.02, hip_dy=0.02),
    # F05: deep groundward follow-through
    make_skel_back_l((0.33, 0.31), (0.22, 0.45), (0.17, 0.56), (0.67, 0.30), (0.73, 0.45), (0.74, 0.57), (0.49, 0.24), head_dx=-0.01, head_dy=0.02, hip_dx=-0.01, hip_dy=0.02),
    # F06: hauling arm back to guard
    make_skel_back_l((0.35, 0.29), (0.27, 0.44), (0.24, 0.56), (0.67, 0.28), (0.73, 0.43), (0.74, 0.56), (0.50, 0.23), head_dy=0.01, hip_dy=0.01),
    # F07: settle to neutral guard
    first_kps_l
]

# 4. back_r/Unarmed: 4 generated frames (for 5-frame clip F00..F04: F01 coil/cock punch, F02 full punch extension with opposite arm counter-pull, F03 follow-through hold/recoil, F04 recovery to guard)
kps_back_r_unarmed = [
    # F01: cock right fist back/inward at chest/shoulder level, left counter-arm braces forward-left
    make_skel_back_r((0.62, 0.29), (0.68, 0.42), (0.65, 0.36), (0.33, 0.27), (0.23, 0.35), (0.19, 0.32), (0.48, 0.22), head_dx=-0.01),
    # F02: explosive straight-forward punch into north-east depth (shoulder drives forward-right, elbow extends, fist punches out at chest/head height, left arm pulls back as counter-balance)
    make_skel_back_r((0.68, 0.26), (0.81, 0.27), (0.91, 0.25), (0.31, 0.29), (0.23, 0.43), (0.21, 0.52), (0.52, 0.22), head_dx=0.02, hip_dx=0.02),
    # F03: punch follow-through & initial elbow bend retraction
    make_skel_back_r((0.67, 0.27), (0.79, 0.32), (0.85, 0.33), (0.32, 0.29), (0.25, 0.43), (0.24, 0.54), (0.51, 0.22), head_dx=0.01, hip_dx=0.01),
    # F04: recovery settling back toward guard
    make_skel_back_r((0.65, 0.28), (0.72, 0.42), (0.74, 0.53), (0.33, 0.28), (0.27, 0.43), (0.26, 0.56), (0.49, 0.22))
]

# 5. back_l/Unarmed: matching 4 generated frames for north-west rear punch
kps_back_l_unarmed = [
    # F01: cock left fist back/inward, right counter-arm braces
    make_skel_back_l((0.38, 0.29), (0.32, 0.42), (0.35, 0.36), (0.67, 0.27), (0.77, 0.35), (0.81, 0.32), (0.52, 0.22), head_dx=0.01),
    # F02: explosive straight-forward punch into north-west depth
    make_skel_back_l((0.32, 0.26), (0.19, 0.27), (0.09, 0.25), (0.69, 0.29), (0.77, 0.43), (0.79, 0.52), (0.48, 0.22), head_dx=-0.02, hip_dx=-0.02),
    # F03: punch follow-through & initial retraction
    make_skel_back_l((0.33, 0.27), (0.21, 0.32), (0.15, 0.33), (0.68, 0.29), (0.75, 0.43), (0.76, 0.54), (0.49, 0.22), head_dx=-0.01, hip_dx=-0.01),
    # F04: recovery settling back toward guard
    make_skel_back_l((0.35, 0.28), (0.28, 0.42), (0.26, 0.53), (0.67, 0.28), (0.73, 0.43), (0.74, 0.56), (0.51, 0.22))
]

jobs_to_submit = [
    {
        "tag": "back_l_sword_v1",
        "payload": {
            "description": "muscular green-skinned Warcraft orc warrior in dark iron plate armor, rear three-quarter view facing north-west, completely empty-handed with closed armored gauntlet fists, no weapons, no sword, no blade",
            "action": "empty-handed diagonal left-arm slash motion with closed fist, torso twist and recovery",
            "direction": "north-west",
            "view": "low top-down",
            "first_frame_base64": back_l_b64,
            "first_frame_keypoints": first_kps_l,
            "keypoints": kps_back_l_sword,
            "no_background": True,
            "seed": 502
        }
    },
    {
        "tag": "back_r_axe_v1",
        "payload": {
            "description": "muscular green-skinned Warcraft orc warrior in dark iron plate armor, rear three-quarter view facing north-east, completely empty-handed with closed armored gauntlet fists, no weapons, no axe, no handle",
            "action": "empty-handed heavy overhead right-arm chop with closed fist, high hoist and downward cleave",
            "direction": "north-east",
            "view": "low top-down",
            "first_frame_base64": back_r_b64,
            "first_frame_keypoints": first_kps_r,
            "keypoints": kps_back_r_axe,
            "no_background": True,
            "seed": 503
        }
    },
    {
        "tag": "back_l_axe_v1",
        "payload": {
            "description": "muscular green-skinned Warcraft orc warrior in dark iron plate armor, rear three-quarter view facing north-west, completely empty-handed with closed armored gauntlet fists, no weapons, no axe, no handle",
            "action": "empty-handed heavy overhead left-arm chop with closed fist, high hoist and downward cleave",
            "direction": "north-west",
            "view": "low top-down",
            "first_frame_base64": back_l_b64,
            "first_frame_keypoints": first_kps_l,
            "keypoints": kps_back_l_axe,
            "no_background": True,
            "seed": 504
        }
    },
    {
        "tag": "back_r_unarmed_v1",
        "payload": {
            "description": "muscular green-skinned Warcraft orc warrior in dark iron plate armor, rear three-quarter view facing north-east, unarmed brawler with closed armored gauntlet fists, no weapons",
            "action": "unarmed heavy right-fist punch forward with opposite arm counter-balance and recovery",
            "direction": "north-east",
            "view": "low top-down",
            "first_frame_base64": back_r_b64,
            "first_frame_keypoints": first_kps_r,
            "keypoints": kps_back_r_unarmed,
            "no_background": True,
            "seed": 505
        }
    },
    {
        "tag": "back_l_unarmed_v1",
        "payload": {
            "description": "muscular green-skinned Warcraft orc warrior in dark iron plate armor, rear three-quarter view facing north-west, unarmed brawler with closed armored gauntlet fists, no weapons",
            "action": "unarmed heavy left-fist punch forward with opposite arm counter-balance and recovery",
            "direction": "north-west",
            "view": "low top-down",
            "first_frame_base64": back_l_b64,
            "first_frame_keypoints": first_kps_l,
            "keypoints": kps_back_l_unarmed,
            "no_background": True,
            "seed": 506
        }
    }
]

submitted = []
for item in jobs_to_submit:
    tag = item["tag"]
    req_path = REQ_DIR / f"req_{tag}.json"
    meta_path = REQ_DIR / f"req_{tag}_meta.json"
    rec_path = REC_DIR / f"job_{tag}.json"
    req_path.write_text(json.dumps(item["payload"], indent=2), encoding="utf-8")
    meta = {k: v for k, v in item["payload"].items() if k != "first_frame_base64"}
    meta["first_frame_base64_len"] = len(item["payload"]["first_frame_base64"])
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")

    subprocess.run([
        str(ROOT / "tmp/pixel-venv/Scripts/python.exe"),
        str(ROOT / "tools/pixellab-mcp.py"),
        "--call", "animate_with_skeleton_v3",
        "--input", str(req_path),
        "--output", str(rec_path)
    ], check=True)
    res_txt = rec_path.read_text(encoding="utf-8")
    print(f"Submitted {tag}:", res_txt[:300])
    submitted.append({"tag": tag, "receipt": str(rec_path)})

(REC_DIR / "batch_rear_submitted.json").write_text(json.dumps(submitted, indent=2), encoding="utf-8")
