from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np

OUT_ROOT = Path("characters/orc-v1/source/combat-rescue-v5/combat")
SHEET_DIR = Path("experiments/main-orc-combat-rescue-v5/combat/sheets")
SHEET_DIR.mkdir(parents=True, exist_ok=True)

def alpha_over(bottom: np.ndarray, top: np.ndarray) -> np.ndarray:
    b = bottom.astype(np.float32) / 255.0
    t = top.astype(np.float32) / 255.0
    a_t = t[:, :, 3:4]
    a_b = b[:, :, 3:4]
    out_a = a_t + a_b * (1.0 - a_t)
    out_rgb = np.where(out_a > 0, (t[:, :, :3] * a_t + b[:, :, :3] * a_b * (1.0 - a_t)) / np.maximum(out_a, 1e-6), 0.0)
    out = np.concatenate([out_rgb, out_a], axis=2)
    return np.clip(np.round(out * 255.0), 0, 255).astype(np.uint8)

# 1. Verify all 8 weapon clips
for d in ["front_r", "front_l", "back_r", "back_l"]:
    for w in ["Sword", "Axe"]:
        clip_dir = OUT_ROOT / d / w
        n_frames = 13 if (d.startswith("front") and w == "Sword") else (12 if (d.startswith("front") and w == "Axe") else 8)
        hf_counts = []
        for i in range(n_frames):
            f_im = np.array(Image.open(clip_dir / f"{i:02d}.png").convert("RGBA"))
            n_im = np.array(Image.open(clip_dir / "native" / f"{i:02d}.png").convert("RGBA"))
            wb = np.array(Image.open(clip_dir / "layers/weaponBack" / f"{i:02d}.png").convert("RGBA"))
            b  = np.array(Image.open(clip_dir / "layers/body" / f"{i:02d}.png").convert("RGBA"))
            wf = np.array(Image.open(clip_dir / "layers/weaponFront" / f"{i:02d}.png").convert("RGBA"))
            hf = np.array(Image.open(clip_dir / "layers/handFront" / f"{i:02d}.png").convert("RGBA"))

            # Verify exact native[64,64] crop of layers/body
            assert np.array_equal(b[64:192, 64:192], n_im), f"Body crop mismatch in {d}/{w} F{i:02d}"
            # Verify alpha-over composition
            comp = alpha_over(alpha_over(alpha_over(wb, b), wf), hf)
            assert np.array_equal(comp, f_im), f"Alpha-over mismatch in {d}/{w} F{i:02d}"

            hf_px = int((hf[:, :, 3] > 0).sum())
            hf_counts.append(hf_px)
        print(f"Verified {d}/{w} ({n_frames}f): handFront pixel counts = {hf_counts}")

# 2. Build Rear 4x8 Composite Sheet (256x256 per cell)
rear_sheet = Image.new("RGBA", (8 * 256, 4 * 256), (28, 32, 38, 255))
draw_r = ImageDraw.Draw(rear_sheet)
for r_idx, (d, w) in enumerate([("back_r", "Sword"), ("back_r", "Axe"), ("back_l", "Sword"), ("back_l", "Axe")]):
    clip_dir = OUT_ROOT / d / w
    for i in range(8):
        im = Image.open(clip_dir / f"{i:02d}.png").convert("RGBA")
        x0, y0 = i * 256, r_idx * 256
        rear_sheet.alpha_composite(im, (x0, y0))
        draw_r.rectangle([x0, y0, x0 + 255, y0 + 255], outline=(55, 62, 72, 255), width=1)
        draw_r.text((x0 + 8, y0 + 8), f"{d}/{w} F{i:02d} (256x256 comp)", fill=(235, 240, 245, 255))
rear_sheet.save(SHEET_DIR / "rear_weapons_4x8_composite.png")

# 3. Build Grip Zoom Sheet (3x zoom on a 64x64 window around the grip) for all 8 weapon clips across active frames
# 8 rows (one per weapon clip), 9 cols (up to 9 active frames)
cell_z = 192 # 64 * 3
grip_sheet = Image.new("RGBA", (9 * cell_z, 8 * cell_z), (24, 28, 34, 255))
draw_g = ImageDraw.Draw(grip_sheet)

clips_8 = [
    ("front_r", "Sword", range(2, 11)),
    ("front_l", "Sword", range(2, 11)),
    ("front_r", "Axe",   range(2, 9)),
    ("front_l", "Axe",   range(2, 9)),
    ("back_r",  "Sword", range(1, 7)),
    ("back_r",  "Axe",   range(1, 7)),
    ("back_l",  "Sword", range(1, 7)),
    ("back_l",  "Axe",   range(1, 7)),
]

for r_idx, (d, w, f_range) in enumerate(clips_8):
    clip_dir = OUT_ROOT / d / w
    for c_idx, i in enumerate(f_range):
        im = Image.open(clip_dir / f"{i:02d}.png").convert("RGBA")
        hf = np.array(Image.open(clip_dir / "layers/handFront" / f"{i:02d}.png").convert("RGBA"))
        ys, xs = np.where(hf[:, :, 3] > 0)
        cx, cy = int(np.median(xs)), int(np.median(ys))
        crop = im.crop((cx - 32, cy - 32, cx + 32, cy + 32)).resize((cell_z, cell_z), Image.NEAREST)
        x0, y0 = c_idx * cell_z, r_idx * cell_z
        grip_sheet.alpha_composite(crop, (x0, y0))
        draw_g.rectangle([x0, y0, x0 + cell_z - 1, y0 + cell_z - 1], outline=(65, 72, 84, 255), width=1)
        draw_g.text((x0 + 6, y0 + 6), f"{d}/{w} F{i:02d}\nhf={len(xs)}px @({cx},{cy})", fill=(240, 245, 250, 255))

grip_sheet.save(SHEET_DIR / "weapon_grips_8clips_3x_zoom.png")
print("Saved sheets: rear_weapons_4x8_composite.png and weapon_grips_8clips_3x_zoom.png")
