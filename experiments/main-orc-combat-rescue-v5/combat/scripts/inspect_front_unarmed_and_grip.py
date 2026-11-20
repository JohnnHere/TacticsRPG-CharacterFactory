import json
from pathlib import Path
from PIL import Image
import numpy as np

ROOT = Path(".")
BASELINE = json.loads((ROOT / "experiments/main-orc-combat-rescue-v5/combat/stage-a-baseline-inspection.json").read_text(encoding="utf-8"))
CLIPS = {k: ROOT / v["clipJson"] for k, v in BASELINE.items()}

for d in ["front_r", "front_l"]:
    print(f"=== {d}/Unarmed ===")
    cdir = CLIPS[f"{d}/Unarmed"].parent
    for fi in range(5):
        p = cdir / "native" / f"{fi:02d}.png"
        if not p.exists():
            p = cdir / f"{fi:02d}.png"
        im = np.array(Image.open(p).convert("RGBA"))
        vis = im[:, :, 3] > 0
        ys, xs = np.where(vis)
        print(f"  F{fi:02d} ({p}): bbox=[{xs.min()},{ys.min()}..{xs.max()},{ys.max()}] vis={int(np.sum(vis))}")
    p2 = (cdir / "native/02.png") if (cdir / "native/02.png").exists() else (cdir / "02.png")
    p3 = (cdir / "native/03.png") if (cdir / "native/03.png").exists() else (cdir / "03.png")
    p4 = (cdir / "native/04.png") if (cdir / "native/04.png").exists() else (cdir / "04.png")
    f2 = np.array(Image.open(p2).convert("RGBA"))
    f3 = np.array(Image.open(p3).convert("RGBA"))
    f4 = np.array(Image.open(p4).convert("RGBA"))
    # Where is the forward punch arm in F02 vs F03?
    diff_2_3 = np.any(f2 != f3, axis=2)
    dys, dxs = np.where(diff_2_3)
    print(f"  Diff F02 vs F03: {int(np.sum(diff_2_3))} px, bbox=[{dxs.min()},{dys.min()}..{dxs.max()},{dys.max()}]")
    # Print punch region in F02 vs F03
    if d == "front_r":
        punch_reg_f2 = f2[35:68, 72:112, 3] > 0
        punch_reg_f3 = f3[35:68, 72:112, 3] > 0
        punch_reg_f4 = f4[35:68, 72:112, 3] > 0
    else:
        punch_reg_f2 = f2[35:68, 16:56, 3] > 0
        punch_reg_f3 = f3[35:68, 16:56, 3] > 0
        punch_reg_f4 = f4[35:68, 16:56, 3] > 0
    print(f"  Punch region alpha count: F02={int(np.sum(punch_reg_f2))}, F03={int(np.sum(punch_reg_f3))}, F04={int(np.sum(punch_reg_f4))}")
