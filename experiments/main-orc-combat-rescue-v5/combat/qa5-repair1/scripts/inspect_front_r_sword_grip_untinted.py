import os, json
from PIL import Image, ImageDraw

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../.."))
CLIP_DIR = os.path.join(ROOT, "characters/orc-v1/source/combat-rescue-v5/combat/qa5-repair1/front_r/Sword")
DIAG_DIR = os.path.join(ROOT, "experiments/main-orc-combat-rescue-v5/combat/qa5-repair1/diagnostics")

with open(os.path.join(DIAG_DIR, "front_r_sword_anatomy.json"), "r", encoding="utf-8") as f:
    ANAT = json.load(f)

# Visible frames are F02..F10 (9 frames)
# For each frame, show 3 side-by-side 4x zoom panels centered around the fist/forearm/hilt:
# 1. Body only (untinted)
# 2. Body + Weapon (untinted)
# 3. Final Composite: Body + Weapon + HandFront (untinted) + non-zero HandFront pixel count
scale = 4
half_r = 28 # 56x56 crop -> 224x224 panel
pw = half_r * 2 * scale
ph = half_r * 2 * scale

rows = 9
cols = 3
sheet = Image.new("RGBA", (cols * (pw + 12) + 12, rows * (ph + 26) + 12), (24, 28, 34, 255))
draw = ImageDraw.Draw(sheet)

for r, fidx in enumerate(range(2, 11)):
    fn = f"{fidx:02d}.png"
    b_im = Image.open(os.path.join(CLIP_DIR, "layers/body", fn)).convert("RGBA")
    wb_im = Image.open(os.path.join(CLIP_DIR, "layers/weaponBack", fn)).convert("RGBA")
    wf_im = Image.open(os.path.join(CLIP_DIR, "layers/weaponFront", fn)).convert("RGBA")
    hf_im = Image.open(os.path.join(CLIP_DIR, "layers/handFront", fn)).convert("RGBA")
    comp_im = Image.open(os.path.join(CLIP_DIR, "frames", fn)).convert("RGBA")

    # Body + Weapon without handFront
    bw_im = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    bw_im.alpha_composite(wb_im)
    bw_im.alpha_composite(b_im)
    bw_im.alpha_composite(wf_im)

    # Count non-zero handFront pixels
    hf_pixels = sum(1 for px in hf_im.getdata() if px[3] > 0)

    a = ANAT[str(fidx)]
    cx, cy = a["palm"]
    box = (cx - half_r, cy - half_r, cx + half_r, cy + half_r)

    panels = [
        (b_im, f"F{fidx:02d} Body Only ({a['phase']})"),
        (bw_im, f"F{fidx:02d} Body+Weapon (before handFront)"),
        (comp_im, f"F{fidx:02d} Final Grip (handFront={hf_pixels}px, palm={cx},{cy})")
    ]
    for c, (pim, label) in enumerate(panels):
        sub = pim.crop(box).resize((pw, ph), Image.NEAREST)
        ox = 12 + c * (pw + 12)
        oy = 12 + r * (ph + 26)
        sheet.paste(sub, (ox, oy))
        draw.text((ox + 4, oy + ph + 4), label, fill=(235, 240, 245, 255))

out_p = os.path.join(DIAG_DIR, "front_r_sword_grip_untinted_zoom.png")
sheet.save(out_p)
print("Saved:", out_p)
