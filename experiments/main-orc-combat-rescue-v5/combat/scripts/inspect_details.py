import json
from pathlib import Path
from PIL import Image
import numpy as np

ROOT = Path(".")

print("=== 1. Comparing raw/pixellab-skeleton-v3 vs qa-revision-1-repair vs rear-reconstruction-v4 ===")
for key, d, a, raw_sub, v2_sub in [
    ("SwordR", "back_r", "Sword", "back_r", "Attack-representative-v2"),
    ("SwordL", "back_l", "Sword", "back_l", "Attack-representative-v1"),
    ("AxeR", "back_r", "Axe", "back_r_axe", "Attack-representative-v1"),
    ("AxeL", "back_l", "Axe", "back_l_axe", "Attack-representative-v1"),
]:
    print(f"\n--- {key} ({d}/{a}) ---")
    v4_dir = ROOT / f"characters/orc-v1/source/rear-reconstruction-v4/{d}/{a}/native"
    v2_dir = ROOT / f"characters/orc-v1/source/rear-recovery-v2/{d}/{a}/{v2_sub}/native"
    qa_dir = ROOT / f"experiments/main-orc-rear-recovery-v2/qa-revision-1-repair/checkpoint/{key}/native"
    raw_dir = ROOT / f"experiments/main-orc-rear-recovery-v2/raw/pixellab-skeleton-v3/{raw_sub}"
    for i in range(8):
        fn = f"{i:02d}.png"
        v4_im = np.array(Image.open(v4_dir / fn).convert("RGBA"))
        v2_im = np.array(Image.open(v2_dir / fn).convert("RGBA"))
        d_v4_v2 = int(np.sum(np.any(v4_im != v2_im, axis=2)))
        d_v4_qa = -1
        if qa_dir.exists() and (qa_dir / fn).exists():
            qa_im = np.array(Image.open(qa_dir / fn).convert("RGBA"))
            d_v4_qa = int(np.sum(np.any(v4_im != qa_im, axis=2)))
        # raw has 00..06 which correspond to F00..F06 (or F01..F06)
        d_v4_raw = -1
        if i < 7 and (raw_dir / fn).exists():
            raw_im = np.array(Image.open(raw_dir / fn).convert("RGBA"))
            d_v4_raw = int(np.sum(np.any(v4_im != raw_im, axis=2)))
        print(f"  F{i:02d}: v4_vs_v2={d_v4_v2}px | v4_vs_qa_repair={d_v4_qa}px | v4_vs_raw[{i:02d}]={d_v4_raw}px")

print("\n=== 2. Detailed ASCII/bounding inspection of front_r and front_l Unarmed F00..F04 ===")
# Let's see what happens to the left and right arms of the orc in front_r/Unarmed and front_l/Unarmed
for d in ["front_r", "front_l"]:
    print(f"\n*** {d}/Unarmed ***")
    u_dir = ROOT / f"characters/orc-v1/source/rear-recovery-v2/{d}/Unarmed"
    for i in range(5):
        nat = np.array(Image.open(u_dir / f"{i:02d}.png").convert("RGBA"))[64:192, 64:192]
        # Let's check horizontal slices y=35..75 on both sides of torso (x=0..40 and x=85..127)
        vis = nat[:, :, 3] > 0
        left_arm_pts = np.argwhere(vis[30:85, 0:42]) # y offset +30, x offset +0
        right_arm_pts = np.argwhere(vis[30:85, 86:128]) # y offset +30, x offset +86
        l_info = f"cnt={len(left_arm_pts)} x=[{left_arm_pts[:,1].min()}..{left_arm_pts[:,1].max()}] y=[{left_arm_pts[:,0].min()+30}..{left_arm_pts[:,0].max()+30}]" if len(left_arm_pts) else "NONE"
        r_info = f"cnt={len(right_arm_pts)} x=[{right_arm_pts[:,1].min()+86}..{right_arm_pts[:,1].max()+86}] y=[{right_arm_pts[:,0].min()+30}..{right_arm_pts[:,0].max()+30}]" if len(right_arm_pts) else "NONE"
        print(f"  F{i:02d}: viewer-left(x=0..41): {l_info} | viewer-right(x=86..127): {r_info}")
