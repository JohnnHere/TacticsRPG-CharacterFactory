import json
import base64
import time
import subprocess
from pathlib import Path
from PIL import Image
import numpy as np

ROOT = Path(".")
EXP_DIR = ROOT / "experiments/main-orc-combat-rescue-v5/combat"
REQ_DIR = EXP_DIR / "requests"
REC_DIR = EXP_DIR / "receipts"
RAW_DIR = EXP_DIR / "raw/back_r_sword_v1"
RAW_DIR.mkdir(parents=True, exist_ok=True)

base_path = ROOT / "characters/orc-v1/source/complete-v1/back_r/Idle/00.png"
base256 = Image.open(base_path).convert("RGBA")
base128 = base256.crop((64, 64, 192, 192))
base128_path = EXP_DIR / "raw/back_r_base_128.png"
base128.save(base128_path)

b64_img = base64.b64encode(base128_path.read_bytes()).decode("ascii")

def make_pose(r_sh=(76, 36), r_el=(86, 50), r_wr=(96, 63),
              l_sh=(52, 36), l_el=(42, 50), l_wr=(32, 63),
              neck=(64, 29), nose=(64, 17),
              r_hip=(71, 73), l_hip=(57, 73),
              r_knee=(75, 96), l_knee=(53, 96),
              r_leg=(75, 118), l_leg=(51, 118),
              r_z=165, l_z=105):
    pts = [
        ("NOSE", nose[0], nose[1], 128),
        ("NECK", neck[0], neck[1], 128),
        ("RIGHT SHOULDER", r_sh[0], r_sh[1], 128),
        ("RIGHT ELBOW", r_el[0], r_el[1], r_z),
        ("RIGHT ARM", r_wr[0], r_wr[1], r_z),
        ("LEFT SHOULDER", l_sh[0], l_sh[1], 128),
        ("LEFT ELBOW", l_el[0], l_el[1], l_z),
        ("LEFT ARM", l_wr[0], l_wr[1], l_z),
        ("RIGHT HIP", r_hip[0], r_hip[1], 128),
        ("RIGHT KNEE", r_knee[0], r_knee[1], 128),
        ("RIGHT LEG", r_leg[0], r_leg[1], 128),
        ("LEFT HIP", l_hip[0], l_hip[1], 128),
        ("LEFT KNEE", l_knee[0], l_knee[1], 128),
        ("LEFT LEG", l_leg[0], l_leg[1], 128),
        ("RIGHT EYE", nose[0]+3, nose[1]-2, 128),
        ("LEFT EYE", nose[0]-3, nose[1]-2, 128),
        ("RIGHT EAR", nose[0]+9, nose[1]+4, 128),
        ("LEFT EAR", nose[0]-9, nose[1]+4, 128),
    ]
    return [{"label": lbl, "x": round(x / 128.0, 6), "y": round(y / 128.0, 6), "z_index": z} for lbl, x, y, z in pts]

first_kp = make_pose()

# 7 posed frames for diagonal/horizontal sword slash (back_r / north-east)
# [0] reach-prep: right arm draws out and back-right (elbow 90,46, wrist 106,50)
# [1] coil-back: torso coils right, elbow pulls back-high (94,34), fist loads at shoulder height (110,28)
# [2] apex-coil: deepest horizontal/diagonal load, shoulder (78,35), elbow (96,30), fist (114,24), left counter-arm (38,48 / 26,56)
# [3] slash-drive: explosive diagonal cut forward-left (into NE), shoulder shifts forward (75,35), elbow sweeps out (96,38), fist extends wide right-forward (118,38)
# [4] slash-cross-follow: follow-through sweeping forward-across, elbow (90,44), fist (112,50), torso committed forward (neck 65,28)
# [5] settle-low: arm lowers from follow-through toward side (elbow 88,49, fist 103,58)
# [6] return-guard: settles cleanly back to neutral guard pose
keypoints = [
    make_pose(r_sh=(77,36), r_el=(90,46), r_wr=(106,50), l_sh=(52,36), l_el=(41,50), l_wr=(31,62)),
    make_pose(r_sh=(78,35), r_el=(94,34), r_wr=(110,28), l_sh=(51,37), l_el=(40,49), l_wr=(29,59), neck=(63,29)),
    make_pose(r_sh=(79,35), r_el=(96,30), r_wr=(114,24), l_sh=(50,37), l_el=(39,48), l_wr=(27,57), neck=(63,29)),
    make_pose(r_sh=(76,35), r_el=(96,38), r_wr=(118,38), l_sh=(52,36), l_el=(41,50), l_wr=(30,61), neck=(65,28), nose=(65,17), r_hip=(72,73)),
    make_pose(r_sh=(75,36), r_el=(90,44), r_wr=(112,50), l_sh=(53,36), l_el=(42,51), l_wr=(32,63), neck=(65,28), nose=(65,17), r_hip=(72,73)),
    make_pose(r_sh=(76,36), r_el=(88,49), r_wr=(103,58), l_sh=(52,36), l_el=(42,50), l_wr=(32,63), neck=(64,29)),
    make_pose(),
]

req = {
    "first_frame_base64": b64_img,
    "first_frame_keypoints": first_kp,
    "keypoints": keypoints,
    "action": "empty-handed diagonal sword slash motion, closed armored gauntlet fist, no weapon in hand",
    "description": "Verde Warcraft Orc warrior in dark steel plate armor with spiked pauldrons and muted red-brown straps, seen from his own back-right (northeast) direction, empty-handed with closed armored gauntlet fists, no sword, no blade, no weapon; preserve rear skull, dorsal backplate, and original lighting.",
    "direction": "north-east",
    "view": "low top-down",
    "no_background": True,
    "seed": 501
}

req_path = REQ_DIR / "req_back_r_sword_v1.json"
res_path = REC_DIR / "job_back_r_sword_v1.json"
req_path.write_text(json.dumps(req, indent=2), encoding="utf-8")

# Also save a sanitized request log without the huge base64 string for easy inspection
req_meta = {k: v for k, v in req.items() if k != "first_frame_base64"}
req_meta["first_frame_path"] = str(base128_path)
(REQ_DIR / "req_back_r_sword_v1_meta.json").write_text(json.dumps(req_meta, indent=2), encoding="utf-8")

print("Submitting animate_with_skeleton_v3 for back_r_sword_v1...")
subprocess.run([
    str(ROOT / "tmp/pixel-venv/Scripts/python.exe"),
    str(ROOT / "tools/pixellab-mcp.py"),
    "--call", "animate_with_skeleton_v3",
    "--input", str(req_path),
    "--output", str(res_path)
], check=True)

res = json.loads(res_path.read_text(encoding="utf-8"))
print("Submission response:", json.dumps(res, indent=2))
