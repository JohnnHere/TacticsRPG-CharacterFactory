import json
import base64
import time
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np

ROOT = Path(".")
EXP_DIR = ROOT / "experiments/main-orc-combat-rescue-v5/combat"
QA5_DIR = EXP_DIR / "qa5-repair1"
REQ_DIR = QA5_DIR / "requests"
REC_DIR = QA5_DIR / "receipts"
RAW_DIR = QA5_DIR / "raw/back_r_axe_qa5_v1"
DIAG_DIR = QA5_DIR / "diagnostics"

for d in [REQ_DIR, REC_DIR, RAW_DIR, DIAG_DIR]:
    d.mkdir(parents=True, exist_ok=True)

base128_path = EXP_DIR / "raw/back_r_base_128.png"
b64_img = base64.b64encode(base128_path.read_bytes()).decode("ascii")

def make_pose(r_sh=(82, 36), r_el=(91, 55), r_wr=(93, 72),
              l_sh=(42, 36), l_el=(35, 55), l_wr=(33, 72),
              neck=(63, 28), nose=(64, 18),
              r_hip=(70, 72), l_hip=(54, 72),
              r_knee=(73, 96), l_knee=(50, 96),
              r_leg=(74, 120), l_leg=(47, 120),
              r_z=4, l_z=1):
    pts = [
        ("NOSE", nose[0], nose[1], 0),
        ("NECK", neck[0], neck[1], 1),
        ("RIGHT SHOULDER", r_sh[0], r_sh[1], 2),
        ("RIGHT ELBOW", r_el[0], r_el[1], 3),
        ("RIGHT ARM", r_wr[0], r_wr[1], r_z),
        ("LEFT SHOULDER", l_sh[0], l_sh[1], 1),
        ("LEFT ELBOW", l_el[0], l_el[1], l_z),
        ("LEFT ARM", l_wr[0], l_wr[1], l_z),
        ("RIGHT HIP", r_hip[0], r_hip[1], 1),
        ("RIGHT KNEE", r_knee[0], r_knee[1], 1),
        ("RIGHT LEG", r_leg[0], r_leg[1], 1),
        ("LEFT HIP", l_hip[0], l_hip[1], 1),
        ("LEFT KNEE", l_knee[0], l_knee[1], 1),
        ("LEFT LEG", l_leg[0], l_leg[1], 1),
        ("RIGHT EYE", nose[0]+3, nose[1]-2, 0),
        ("LEFT EYE", nose[0]-3, nose[1]-2, 0),
        ("RIGHT EAR", nose[0]+6, nose[1], 1),
        ("LEFT EAR", nose[0]-6, nose[1], 1),
    ]
    return [{"label": lbl, "x": round(x / 128.0, 4), "y": round(y / 128.0, 4), "z_index": z} for lbl, x, y, z in pts]

first_kp = make_pose()

# Whole-body heavy overhead right-handed axe chop in back_r (north-east) with active pelvis, knees, feet weight shift, and left off-hand counterweight:
keypoints = [
    # [0] F01 overhead-hoist: right arm hoists up-right, torso coils back-left, pelvis shifts left-up, left counter-arm swings forward-out to balance
    make_pose(
        r_sh=(81, 32), r_el=(95, 25), r_wr=(98, 16),
        l_sh=(40, 38), l_el=(29, 49), l_wr=(24, 59),
        neck=(61, 26), nose=(62, 16),
        r_hip=(68, 70), l_hip=(51, 70),
        r_knee=(71, 94), l_knee=(48, 94),
        r_leg=(73, 120), l_leg=(46, 120)
    ),
    # [1] F02 overhead-apex: deep full-body overhead coil, chest/head arch up-back, pelvis braces left-up, left counter-arm braces high-out, right fist cocked high above right pauldron
    make_pose(
        r_sh=(79, 29), r_el=(92, 18), r_wr=(94, 12),
        l_sh=(38, 39), l_el=(26, 46), l_wr=(20, 54),
        neck=(59, 25), nose=(60, 15),
        r_hip=(66, 69), l_hip=(49, 69),
        r_knee=(70, 93), l_knee=(46, 93),
        r_leg=(72, 119), l_leg=(45, 120)
    ),
    # [2] F03 cleave-drop: whole body lunges forward-right into north-east chop, pelvis & right knee drive right-down, left counter-arm whips back-down as counterweight
    make_pose(
        r_sh=(86, 33), r_el=(103, 30), r_wr=(112, 28),
        l_sh=(44, 37), l_el=(34, 54), l_wr=(29, 68),
        neck=(66, 28), nose=(68, 18),
        r_hip=(74, 73), l_hip=(57, 73),
        r_knee=(77, 97), l_knee=(53, 97),
        r_leg=(77, 120), l_leg=(48, 120)
    ),
    # [3] F04 heavy-impact: deep downward cleave commitment, pelvis & knees sink low (+4px drop, +6px right lunge), torso leans forward-right, left arm pulls back behind hip
    make_pose(
        r_sh=(89, 39), r_el=(105, 52), r_wr=(112, 64),
        l_sh=(46, 39), l_el=(37, 58), l_wr=(33, 74),
        neck=(68, 31), nose=(71, 22),
        r_hip=(76, 76), l_hip=(59, 76),
        r_knee=(79, 99), l_knee=(55, 99),
        r_leg=(78, 120), l_leg=(49, 120)
    ),
    # [4] F05 weight-sink: heavy groundward follow-through absorption, deep knee bend, fist low-right, left arm counter-braced
    make_pose(
        r_sh=(87, 40), r_el=(100, 58), r_wr=(106, 72),
        l_sh=(45, 39), l_el=(37, 57), l_wr=(34, 73),
        neck=(66, 31), nose=(68, 22),
        r_hip=(74, 76), l_hip=(57, 76),
        r_knee=(77, 99), l_knee=(53, 99),
        r_leg=(76, 120), l_leg=(48, 120)
    ),
    # [5] F06 wrench-back: torso rises and rotates back toward center, knees push up, right arm hauls axe back toward side
    make_pose(
        r_sh=(84, 38), r_el=(94, 56), r_wr=(98, 72),
        l_sh=(43, 37), l_el=(36, 56), l_wr=(34, 72),
        neck=(64, 29), nose=(65, 19),
        r_hip=(72, 74), l_hip=(55, 74),
        r_knee=(75, 97), l_knee=(51, 97),
        r_leg=(75, 120), l_leg=(47, 120)
    ),
    # [6] F07 guard-recovery: natural empty-handed settle returning cleanly into neutral rear guard stance
    make_pose(
        r_sh=(82, 36), r_el=(91, 55), r_wr=(93, 72),
        l_sh=(42, 36), l_el=(35, 55), l_wr=(33, 72),
        neck=(63, 28), nose=(64, 18),
        r_hip=(70, 72), l_hip=(54, 72),
        r_knee=(73, 96), l_knee=(50, 96),
        r_leg=(74, 120), l_leg=(47, 120)
    ),
]

req = {
    "description": "muscular green-skinned Warcraft orc warrior in dark iron plate armor, rear three-quarter view facing north-east, completely empty-handed with closed armored gauntlet fists, no weapons, no axe, no handle",
    "action": "whole-body empty-handed heavy overhead right-arm chop with hip lunge and left arm balance",
    "direction": "north-east",
    "view": "low top-down",
    "first_frame_base64": b64_img,
    "first_frame_keypoints": first_kp,
    "keypoints": keypoints,
    "no_background": True,
    "seed": 513
}

req_path = REQ_DIR / "req_back_r_axe_qa5_v1.json"
meta_path = REQ_DIR / "req_back_r_axe_qa5_v1_meta.json"
res_path = REC_DIR / "job_back_r_axe_qa5_v1.json"

req_path.write_text(json.dumps(req, indent=2), encoding="utf-8")
meta = {k: v for k, v in req.items() if k != "first_frame_base64"}
meta["first_frame_base64_len"] = len(b64_img)
meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")

print("Submitting animate_with_skeleton_v3 for back_r_axe_qa5_v1...")
subprocess.run([
    str(ROOT / "tmp/pixel-venv/Scripts/python.exe"),
    str(ROOT / "tools/pixellab-mcp.py"),
    "--call", "animate_with_skeleton_v3",
    "--input", str(req_path),
    "--output", str(res_path)
], check=True)

res_txt = res_path.read_text(encoding="utf-8")
print("Submission response:", res_txt[:400])
res_json = json.loads(res_txt)
# Extract job_id
job_id = None
for it in res_json.get("content", []):
    txt = it.get("text", "")
    for line in txt.splitlines():
        if "job_id" in line or "Job ID" in line or "-" in line:
            import re
            m = re.search(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", line)
            if m:
                job_id = m.group(0)
                break
    if job_id:
        break

print("Parsed job_id:", job_id)
if not job_id:
    raise RuntimeError(f"Could not parse job_id from {res_txt}")

# Poll until completed
for attempt in range(40):
    p_req = REQ_DIR / "poll_back_r_axe_qa5_v1.json"
    p_res = REC_DIR / "poll_back_r_axe_qa5_v1_res.json"
    p_req.write_text(json.dumps({"job_id": job_id}), encoding="utf-8")
    subprocess.run([
        str(ROOT / "tmp/pixel-venv/Scripts/python.exe"),
        str(ROOT / "tools/pixellab-mcp.py"),
        "--call", "get_image",
        "--input", str(p_req),
        "--output", str(p_res)
    ], check=True)
    txt = p_res.read_text(encoding="utf-8")
    if "status: completed" in txt:
        print(f"Completed on attempt {attempt}!")
        break
    print(f"[Attempt {attempt}] still processing...")
    time.sleep(6)

# Fetch all 7 frames
for idx in range(7):
    idx_req = REQ_DIR / f"poll_back_r_axe_qa5_v1_f{idx:02d}.json"
    idx_res = REC_DIR / f"poll_back_r_axe_qa5_v1_f{idx:02d}_res.json"
    idx_req.write_text(json.dumps({"job_id": job_id, "index": idx}), encoding="utf-8")
    subprocess.run([
        str(ROOT / "tmp/pixel-venv/Scripts/python.exe"),
        str(ROOT / "tools/pixellab-mcp.py"),
        "--call", "get_image",
        "--input", str(idx_req),
        "--output", str(idx_res)
    ], check=True)
    r_idx = json.loads(idx_res.read_text(encoding="utf-8"))
    for it in r_idx.get("content", []):
        if it.get("type") == "image" and it.get("data"):
            (RAW_DIR / f"{idx:02d}.png").write_bytes(base64.b64decode(it["data"]))
            break

# Record current balance
bal_req = REQ_DIR / "get_balance_after_back_r_axe_qa5.json"
bal_res = REC_DIR / "balance_after_back_r_axe_qa5.json"
bal_req.write_text("{}", encoding="utf-8")
subprocess.run([
    str(ROOT / "tmp/pixel-venv/Scripts/python.exe"),
    str(ROOT / "tools/pixellab-mcp.py"),
    "--call", "get_balance",
    "--input", str(bal_req),
    "--output", str(bal_res)
], check=True)
print("Balance after job:", bal_res.read_text(encoding="utf-8")[:300])
