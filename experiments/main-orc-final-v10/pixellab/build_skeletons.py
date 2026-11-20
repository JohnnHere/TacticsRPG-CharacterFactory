import json, math
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(r"c:\Users\João Orlando\Documents\Projetos Unity\TacticsRPG-CharacterFactory")
EXP = ROOT / "experiments/main-orc-final-v10/pixellab"
OUT = Path(r"C:\Users\João Orlando\.gemini\antigravity\brain\5fe480f6-d661-411c-b120-c9742e395c32\scratch\audit")

req_prev = json.loads((ROOT / "experiments/main-orc-artistic-reconstruction-v6/rear/sword-reference2-request.json").read_text(encoding="utf-8"))
first_kp = req_prev["first_frame_keypoints"]
base_map = {j["label"]: dict(j) for j in first_kp}

LABELS = [
    "NOSE", "NECK",
    "RIGHT SHOULDER", "RIGHT ELBOW", "RIGHT ARM",
    "LEFT SHOULDER", "LEFT ELBOW", "LEFT ARM",
    "RIGHT HIP", "RIGHT KNEE", "RIGHT LEG",
    "LEFT HIP", "LEFT KNEE", "LEFT LEG",
    "RIGHT EYE", "LEFT EYE", "RIGHT EAR", "LEFT EAR"
]

def make_pose(
    dx_head=0.0, dy_head=0.0,
    r_sh=(0.648, 0.266, 9, 136), r_el=(0.711, 0.438, 10, 142), r_wr=(0.695, 0.602, 11, 146),
    l_sh=(0.336, 0.266, 6, 132), l_el=(0.273, 0.445, 6, 136), l_wr=(0.234, 0.617, 6, 138),
    r_hip=(0.586, 0.617), r_kn=(0.633, 0.797),
    l_hip=(0.422, 0.617), l_kn=(0.375, 0.797),
):
    pts = {}
    for k in ["NOSE", "NECK", "RIGHT EYE", "LEFT EYE", "RIGHT EAR", "LEFT EAR"]:
        pts[k] = {"label": k, "x": round(base_map[k]["x"] + dx_head, 5), "y": round(base_map[k]["y"] + dy_head, 5), "z_index": base_map[k]["z_index"]}
    for lbl, tup in [
        ("RIGHT SHOULDER", r_sh), ("RIGHT ELBOW", r_el), ("RIGHT ARM", r_wr),
        ("LEFT SHOULDER", l_sh), ("LEFT ELBOW", l_el), ("LEFT ARM", l_wr),
    ]:
        pts[lbl] = {"label": lbl, "x": round(tup[0], 5), "y": round(tup[1], 5), "z_index": tup[2], "depth": tup[3]}
    pts["RIGHT HIP"] = {"label": "RIGHT HIP", "x": round(r_hip[0], 5), "y": round(r_hip[1], 5), "z_index": 8}
    pts["RIGHT KNEE"] = {"label": "RIGHT KNEE", "x": round(r_kn[0], 5), "y": round(r_kn[1], 5), "z_index": 8}
    pts["RIGHT LEG"] = dict(base_map["RIGHT LEG"])
    pts["LEFT HIP"] = {"label": "LEFT HIP", "x": round(l_hip[0], 5), "y": round(l_hip[1], 5), "z_index": 6}
    pts["LEFT KNEE"] = {"label": "LEFT KNEE", "x": round(l_kn[0], 5), "y": round(l_kn[1], 5), "z_index": 6}
    pts["LEFT LEG"] = dict(base_map["LEFT LEG"])
    return [pts[l] for l in LABELS]

# Sword 12 active poses (F01..F12; F00 and F13 are exact back_l/Idle F00)
# Reference upper-arm length ~ 0.18, forearm ~ 0.165 (when planar), foreshortened when angled in 3D
sword_kps = [
    # 1 -> F01 body-prep (coil right)
    make_pose(dx_head=0.012, dy_head=0.004,
              r_sh=(0.660, 0.275, 9, 142), r_el=(0.745, 0.415, 10, 152), r_wr=(0.735, 0.555, 11, 156),
              l_sh=(0.340, 0.268, 6, 128), l_el=(0.270, 0.440, 6, 132), l_wr=(0.235, 0.610, 6, 134)),
    # 2 -> F02 establish-grip (lift at right side)
    make_pose(dx_head=0.015, dy_head=0.002,
              r_sh=(0.662, 0.266, 9, 140), r_el=(0.760, 0.365, 10, 150), r_wr=(0.755, 0.465, 11, 154),
              l_sh=(0.342, 0.270, 6, 128), l_el=(0.272, 0.442, 6, 132), l_wr=(0.236, 0.608, 6, 134)),
    # 3 -> F03 anticipation (raise to shoulder height)
    make_pose(dx_head=0.015, dy_head=-0.004,
              r_sh=(0.655, 0.250, 9, 136), r_el=(0.765, 0.265, 10, 144), r_wr=(0.735, 0.165, 11, 146),
              l_sh=(0.345, 0.274, 6, 130), l_el=(0.275, 0.446, 6, 134), l_wr=(0.240, 0.610, 6, 136)),
    # 4 -> F04 coil (high above right shoulder)
    make_pose(dx_head=0.010, dy_head=-0.008,
              r_sh=(0.640, 0.238, 9, 132), r_el=(0.735, 0.175, 10, 136), r_wr=(0.660, 0.085, 11, 136),
              l_sh=(0.348, 0.278, 6, 132), l_el=(0.278, 0.450, 6, 136), l_wr=(0.244, 0.612, 6, 138)),
    # 5 -> F05 apex-hold (peak overhead coil)
    make_pose(dx_head=0.005, dy_head=-0.010,
              r_sh=(0.625, 0.232, 9, 128), r_el=(0.695, 0.145, 10, 130), r_wr=(0.585, 0.068, 11, 128),
              l_sh=(0.352, 0.282, 6, 134), l_el=(0.284, 0.454, 6, 138), l_wr=(0.250, 0.614, 6, 140)),
    # 6 -> F06 apex-descent (sweeping over head into NW!)
    make_pose(dx_head=-0.015, dy_head=0.000,
              r_sh=(0.560, 0.235, 8, 116), r_el=(0.485, 0.125, 9, 110), r_wr=(0.335, 0.125, 10, 105),
              l_sh=(0.370, 0.292, 7, 144), l_el=(0.315, 0.465, 7, 148), l_wr=(0.290, 0.618, 7, 150),
              r_hip=(0.572, 0.618), r_kn=(0.625, 0.798), l_hip=(0.412, 0.618), l_kn=(0.358, 0.795)),
    # 7 -> F07 slash-release (diagonal NW extension past upper-left!)
    make_pose(dx_head=-0.032, dy_head=0.012,
              r_sh=(0.495, 0.250, 5, 110), r_el=(0.315, 0.225, 5, 104), r_wr=(0.165, 0.275, 5, 100),
              l_sh=(0.395, 0.305, 8, 150), l_el=(0.355, 0.475, 9, 155), l_wr=(0.335, 0.625, 9, 158),
              r_hip=(0.560, 0.622), r_kn=(0.618, 0.802), l_hip=(0.402, 0.622), l_kn=(0.345, 0.792)),
    # 8 -> F08 contact (full NW diagonal cleave impact!)
    make_pose(dx_head=-0.042, dy_head=0.022,
              r_sh=(0.475, 0.268, 5, 108), r_el=(0.290, 0.305, 5, 102), r_wr=(0.148, 0.395, 5, 98),
              l_sh=(0.405, 0.315, 8, 152), l_el=(0.372, 0.482, 9, 158), l_wr=(0.355, 0.630, 9, 160),
              r_hip=(0.555, 0.628), r_kn=(0.615, 0.806), l_hip=(0.398, 0.628), l_kn=(0.338, 0.790)),
    # 9 -> F09 follow-through (low NW follow-through, fist clear at front-left!)
    make_pose(dx_head=-0.036, dy_head=0.025,
              r_sh=(0.485, 0.278, 5, 110), r_el=(0.305, 0.365, 5, 104), r_wr=(0.172, 0.475, 5, 100),
              l_sh=(0.400, 0.312, 8, 150), l_el=(0.365, 0.480, 9, 156), l_wr=(0.345, 0.628, 9, 158),
              r_hip=(0.558, 0.628), r_kn=(0.618, 0.806), l_hip=(0.400, 0.628), l_kn=(0.342, 0.792)),
    # 10 -> F10 recover-bridge (untwisting clockwise, arm returning right)
    make_pose(dx_head=-0.010, dy_head=0.010,
              r_sh=(0.615, 0.275, 9, 136), r_el=(0.705, 0.395, 10, 145), r_wr=(0.715, 0.515, 11, 148),
              l_sh=(0.355, 0.280, 6, 136), l_el=(0.290, 0.455, 6, 140), l_wr=(0.255, 0.618, 6, 142),
              r_hip=(0.576, 0.620), r_kn=(0.628, 0.800), l_hip=(0.415, 0.620), l_kn=(0.365, 0.796)),
    # 11 -> F11 settle-grip (settled at right side)
    make_pose(dx_head=0.004, dy_head=0.004,
              r_sh=(0.645, 0.270, 9, 138), r_el=(0.725, 0.425, 10, 144), r_wr=(0.720, 0.560, 11, 148),
              l_sh=(0.340, 0.270, 6, 132), l_el=(0.276, 0.446, 6, 136), l_wr=(0.240, 0.617, 6, 138)),
    # 12 -> F12 disarm-settle (relaxing into Idle F00)
    make_pose(dx_head=0.000, dy_head=0.000,
              r_sh=(0.648, 0.266, 9, 136), r_el=(0.715, 0.436, 9, 140), r_wr=(0.700, 0.592, 9, 142),
              l_sh=(0.336, 0.266, 6, 132), l_el=(0.273, 0.445, 6, 136), l_wr=(0.234, 0.617, 6, 138)),
]

# Axe 10 active poses (F01..F10; F00 and F11 are exact back_l/Idle F00)
axe_kps = [
    # 1 -> F01 body-prep
    make_pose(dx_head=0.014, dy_head=0.006,
              r_sh=(0.662, 0.278, 9, 142), r_el=(0.752, 0.405, 10, 152), r_wr=(0.742, 0.535, 11, 156),
              l_sh=(0.340, 0.270, 6, 128), l_el=(0.270, 0.442, 6, 132), l_wr=(0.236, 0.610, 6, 134)),
    # 2 -> F02 establish-grip
    make_pose(dx_head=0.016, dy_head=0.000,
              r_sh=(0.660, 0.260, 9, 140), r_el=(0.765, 0.320, 10, 148), r_wr=(0.750, 0.390, 11, 152),
              l_sh=(0.342, 0.272, 6, 130), l_el=(0.274, 0.446, 6, 134), l_wr=(0.240, 0.612, 6, 136)),
    # 3 -> F03 hoist (high overhead lift)
    make_pose(dx_head=0.012, dy_head=-0.008,
              r_sh=(0.642, 0.238, 9, 134), r_el=(0.740, 0.180, 10, 138), r_wr=(0.675, 0.095, 11, 138),
              l_sh=(0.348, 0.278, 6, 132), l_el=(0.280, 0.452, 6, 136), l_wr=(0.246, 0.614, 6, 138)),
    # 4 -> F04 coil-hold (155ms heavy overhead coil!)
    make_pose(dx_head=0.006, dy_head=-0.014,
              r_sh=(0.618, 0.225, 9, 126), r_el=(0.675, 0.125, 10, 128), r_wr=(0.555, 0.055, 11, 124),
              l_sh=(0.355, 0.285, 6, 136), l_el=(0.288, 0.458, 6, 140), l_wr=(0.254, 0.616, 6, 142)),
    # 5 -> F05 cleave (steep overhead-NW downward drive!)
    make_pose(dx_head=-0.025, dy_head=0.008,
              r_sh=(0.515, 0.242, 6, 112), r_el=(0.365, 0.165, 6, 106), r_wr=(0.210, 0.205, 6, 100),
              l_sh=(0.390, 0.302, 8, 148), l_el=(0.345, 0.472, 9, 154), l_wr=(0.325, 0.622, 9, 156),
              r_hip=(0.564, 0.622), r_kn=(0.620, 0.802), l_hip=(0.405, 0.622), l_kn=(0.348, 0.792)),
    # 6 -> F06 heavy-impact (115ms heavy chop crouch into NW!)
    make_pose(dx_head=-0.045, dy_head=0.032,
              r_sh=(0.470, 0.282, 5, 108), r_el=(0.285, 0.340, 5, 102), r_wr=(0.155, 0.455, 5, 98),
              l_sh=(0.408, 0.325, 8, 154), l_el=(0.376, 0.492, 9, 160), l_wr=(0.358, 0.638, 9, 162),
              r_hip=(0.554, 0.638), r_kn=(0.614, 0.812), l_hip=(0.396, 0.638), l_kn=(0.334, 0.794)),
    # 7 -> F07 absorb-follow (110ms weight absorption low-NW)
    make_pose(dx_head=-0.040, dy_head=0.035,
              r_sh=(0.480, 0.288, 5, 110), r_el=(0.300, 0.380, 5, 104), r_wr=(0.175, 0.505, 5, 100),
              l_sh=(0.402, 0.322, 8, 152), l_el=(0.368, 0.490, 9, 158), l_wr=(0.350, 0.635, 9, 160),
              r_hip=(0.558, 0.638), r_kn=(0.616, 0.812), l_hip=(0.400, 0.638), l_kn=(0.338, 0.795)),
    # 8 -> F08 recover-haul (130ms hauling back to right side)
    make_pose(dx_head=-0.008, dy_head=0.014,
              r_sh=(0.615, 0.280, 9, 138), r_el=(0.708, 0.410, 10, 146), r_wr=(0.715, 0.540, 11, 150),
              l_sh=(0.352, 0.282, 6, 136), l_el=(0.288, 0.456, 6, 140), l_wr=(0.252, 0.620, 6, 142),
              r_hip=(0.576, 0.624), r_kn=(0.628, 0.802), l_hip=(0.415, 0.624), l_kn=(0.365, 0.796)),
    # 9 -> F09 disarm-rise (50ms)
    make_pose(dx_head=0.004, dy_head=0.004,
              r_sh=(0.645, 0.270, 9, 138), r_el=(0.720, 0.430, 9, 142), r_wr=(0.708, 0.578, 9, 144),
              l_sh=(0.338, 0.268, 6, 132), l_el=(0.274, 0.445, 6, 136), l_wr=(0.236, 0.617, 6, 138)),
    # 10 -> F10 settle (90ms)
    make_pose(dx_head=0.000, dy_head=0.000,
              r_sh=(0.648, 0.266, 9, 136), r_el=(0.712, 0.437, 9, 140), r_wr=(0.696, 0.598, 9, 142),
              l_sh=(0.336, 0.266, 6, 132), l_el=(0.273, 0.445, 6, 136), l_wr=(0.234, 0.617, 6, 138)),
]

desc = (
    "Adult muscular green orc warrior seen from behind in three-quarter north-west view, "
    "bald green occipital skull, powerful arms with dark steel spiked shoulder plates, "
    "chainmail sleeves, articulated bracers and closed empty brown leather gauntlets, "
    "dark broad back plate with spinal ridge, red cloth tassets, dark steel greaves and grounded boots. "
    "Empty hands, completely unarmed. Refined tactical pixel art with clean clusters and dark outlines."
)

sword_payload = {
    "description": desc,
    "action": "powerful unarmed right-arm overhead reaching motion rotating upper torso forward-left",
    "direction": "north-west",
    "view": "low top-down",
    "no_background": True,
    "seed": 71042,
    "first_frame_url": "upload:cf338c26-2d00-4a49-b1b0-2cd710ccbc8d",
    "first_frame_keypoints": first_kp,
    "keypoints": sword_kps,
}

axe_payload = {
    "description": desc,
    "action": "heavy unarmed right-arm high overhead reaching motion driving torso forward-left and crouching",
    "direction": "north-west",
    "view": "low top-down",
    "no_background": True,
    "seed": 72042,
    "first_frame_url": "upload:cf338c26-2d00-4a49-b1b0-2cd710ccbc8d",
    "first_frame_keypoints": first_kp,
    "keypoints": axe_kps,
}

(EXP / "sword_nw_request.json").write_text(json.dumps(sword_payload, indent=2), encoding="utf-8")
(EXP / "axe_nw_request.json").write_text(json.dumps(axe_payload, indent=2), encoding="utf-8")

# Render quick stick-figure preview
ref = Image.open(EXP / "back_l_base_128.png").convert("RGBA")
dim_ref = Image.eval(ref, lambda v: v // 2)
for i in range(128):
    for j in range(128):
        r, g, b, a = ref.getpixel((i, j))
        dim_ref.putpixel((i, j), (r//2, g//2, b//2, a//2))

BONES = [
    ("NECK", "RIGHT SHOULDER", (255,140,40,255)),
    ("RIGHT SHOULDER", "RIGHT ELBOW", (255,210,40,255)),
    ("RIGHT ELBOW", "RIGHT ARM", (255,255,80,255)),
    ("NECK", "LEFT SHOULDER", (80,180,255,255)),
    ("LEFT SHOULDER", "LEFT ELBOW", (80,210,255,255)),
    ("LEFT ELBOW", "LEFT ARM", (120,240,255,255)),
    ("RIGHT HIP", "RIGHT KNEE", (180,255,140,255)),
    ("RIGHT KNEE", "RIGHT LEG", (180,255,140,255)),
    ("LEFT HIP", "LEFT KNEE", (140,220,180,255)),
    ("LEFT KNEE", "LEFT LEG", (140,220,180,255)),
]

prev = Image.new("RGBA", (12 * 132, 2 * 146), (24, 28, 36, 255))
dr = ImageDraw.Draw(prev)
for row_i, (name, kplist) in enumerate([("Sword", sword_kps), ("Axe", axe_kps)]):
    for ci, kp in enumerate(kplist):
        cell = Image.new("RGBA", (128, 128), (34, 38, 48, 255))
        cell.alpha_composite(dim_ref)
        cdr = ImageDraw.Draw(cell)
        m = {p["label"]: (p["x"]*128, p["y"]*128) for p in kp}
        for a, b, col in BONES:
            cdr.line([m[a], m[b]], fill=col, width=2)
        rx, ry = m["RIGHT ARM"]
        cdr.ellipse([rx-3, ry-3, rx+3, ry+3], fill=(255,60,60,255))
        lx, ly = m["LEFT ARM"]
        cdr.ellipse([lx-2, ly-2, lx+2, ly+2], fill=(60,200,255,255))
        prev.alpha_composite(cell, (ci*132 + 2, row_i*146 + 16))
        dr.text((ci*132 + 4, row_i*146 + 2), f"{name} P{ci+1:02d}", fill=(230,235,245,255))

prev.save(OUT / "skeleton_nw_preview.png")
print("Saved skeleton_nw_preview.png")
