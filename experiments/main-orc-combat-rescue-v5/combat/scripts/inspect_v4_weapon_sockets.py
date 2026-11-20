import json
from pathlib import Path
from PIL import Image
import numpy as np

V4_ROOT = Path("characters/orc-v1/source/rear-reconstruction-v4")
CLEAN_ROOT = Path("experiments/main-orc-combat-rescue-v5/combat/cleaned_rear_bodies")

for d in ["front_r", "front_l", "back_r", "back_l"]:
    for w in ["Sword", "Axe"]:
        clip = json.loads((V4_ROOT / d / w / "clip.json").read_text(encoding="utf-8"))
        print(f"=== {d}/{w} (frames={clip['frameCount']}, total={clip['totalDurationMs']}ms) ===")
        for f in clip["frames"]:
            if f["weaponVisible"]:
                idx = f["index"]
                wb = int((np.array(Image.open(V4_ROOT / d / w / "layers/weaponBack" / f"{idx:02d}.png"))[:,:,3]>0).sum())
                wf = int((np.array(Image.open(V4_ROOT / d / w / "layers/weaponFront" / f"{idx:02d}.png"))[:,:,3]>0).sum())
                hf = int((np.array(Image.open(V4_ROOT / d / w / "layers/handFront" / f"{idx:02d}.png"))[:,:,3]>0).sum())
                print(f"  F{idx:02d} ({f['durationMs']}ms): grip={f.get('rightGrip')}, rot={f.get('rotationDeg')}, wb={wb}, wf={wf}, hf={hf}")

# Also print exact cleaned rear distal fist centers (in 256x256 composite space) for F01..F06
print("\n=== Cleaned Rear Body Distal Fist Centers (256x256 Composite Space) ===")
for tag, side in [
    ("back_r_sword", "right"),
    ("back_r_axe",   "right"),
    ("back_l_sword", "left"),
    ("back_l_axe",   "left"),
]:
    print(f"*** {tag} ***")
    for idx in range(1, 7):
        im = np.array(Image.open(CLEAN_ROOT / tag / f"{idx:02d}.png").convert("RGBA"))
        vis = im[:, :, 3] > 0
        if side == "right":
            m_side = np.zeros_like(vis)
            m_side[:90, 74:] = vis[:90, 74:]
            ys_all, xs_all = np.where(m_side)
            xmax = int(xs_all.max())
            ymin = int(ys_all.min())
            if xmax >= 106:
                dist = m_side & (np.arange(128)[None, :] >= xmax - 10)
            elif ymin <= 10 and idx in (1, 2):
                dist = m_side & (np.arange(128)[:, None] <= ymin + 12) & (np.arange(128)[None, :] >= 82)
            else:
                dist = m_side & (np.arange(128)[None, :] >= xmax - 10) & (np.arange(128)[:, None] >= 40)
            dys, dxs = np.where(dist)
            dcx, dcy = int(np.median(dxs)), int(np.median(dys))
            print(f"  F{idx:02d}: native=({dcx},{dcy}) -> comp256=({dcx+64},{dcy+64}) [xmax={xmax}, ymin={ymin}]")
        else:
            m_side = np.zeros_like(vis)
            m_side[:90, :54] = vis[:90, :54]
            ys_all, xs_all = np.where(m_side)
            xmin = int(xs_all.min())
            ymin = int(ys_all.min())
            if xmin <= 21:
                dist = m_side & (np.arange(128)[None, :] <= xmin + 10)
            elif ymin <= 10 and idx in (1, 2):
                dist = m_side & (np.arange(128)[:, None] <= ymin + 12) & (np.arange(128)[None, :] <= 45)
            else:
                dist = m_side & (np.arange(128)[None, :] <= xmin + 10) & (np.arange(128)[:, None] >= 40)
            dys, dxs = np.where(dist)
            dcx, dcy = int(np.median(dxs)), int(np.median(dys))
            print(f"  F{idx:02d}: native=({dcx},{dcy}) -> comp256=({dcx+64},{dcy+64}) [xmin={xmin}, ymin={ymin}]")
