"""Builds the review artefacts: an animated GIF of the generated frames at the real
frame durations, and one of the current V8 clip for comparison, plus a contact strip
of the five skeleton poses over the reference body.

No pixels are edited. Frames are only composited and timed.
"""
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
EXP = Path(__file__).resolve().parent
SEQUENCE = json.loads((EXP / "sequence-fixed.json").read_text(encoding="utf-8"))
DURATIONS = [f["durationMs"] for f in SEQUENCE["frames"]]

generated = EXP / "pixellab-frames"
frames = []
for i in range(len(DURATIONS)):
    path = generated / f"{i:02d}.png"
    if not path.exists():
        continue
    frames.append((Image.open(path).convert("RGBA"), DURATIONS[i]))

if frames:
    frames[0][0].save(
        EXP / "generated-animation.gif",
        save_all=True,
        append_images=[f[0] for f in frames[1:]],
        duration=[f[1] for f in frames],
        loop=0,
        disposal=2,
    )
    print(f"generated-animation.gif: {len(frames)} quadros, {sum(d for _, d in frames)} ms")

clip = json.loads(
    (ROOT / "characters/orc-v1/source/combat-recovery-v8/rear-arc/back_l-sword/clip.json").read_text(encoding="utf-8")
)
v8 = []
for frame in clip["frames"]:
    v8.append((Image.open(ROOT / frame["png"]).convert("RGBA"), round(frame["durationMs"])))
if v8:
    v8[0][0].save(
        EXP / "v8-reference-animation.gif",
        save_all=True,
        append_images=[f[0] for f in v8[1:]],
        duration=[f[1] for f in v8],
        loop=0,
        disposal=2,
    )
    print(f"v8-reference-animation.gif: {len(v8)} quadros, {sum(d for _, d in v8)} ms")

# Five poses side by side over the reference body, bones drawn in the accent colour.
POSES = json.loads((EXP / "poses-fixed.json").read_text(encoding="utf-8"))
REF = ROOT / "characters/orc-v1/source/combat-recovery-v8/rear-arc/back_l-sword/frames/02.png"
BONES = [
    ("NECK", "RIGHT SHOULDER"), ("RIGHT SHOULDER", "RIGHT ELBOW"), ("RIGHT ELBOW", "RIGHT ARM"),
    ("NECK", "LEFT SHOULDER"), ("LEFT SHOULDER", "LEFT ELBOW"), ("LEFT ELBOW", "LEFT ARM"),
    ("NECK", "RIGHT HIP"), ("RIGHT HIP", "RIGHT KNEE"), ("RIGHT KNEE", "RIGHT LEG"),
    ("NECK", "LEFT HIP"), ("LEFT HIP", "LEFT KNEE"), ("LEFT KNEE", "LEFT LEG"),
    ("RIGHT HIP", "LEFT HIP"), ("RIGHT SHOULDER", "LEFT SHOULDER"),
]
SCALE, PAD = 2, 8
tile = 256 * SCALE
sheet = Image.new("RGBA", ((tile + PAD) * 5 + PAD, tile + PAD * 2), (22, 23, 28, 255))
for index, pose in enumerate(POSES["poses"]):
    panel = Image.open(REF).convert("RGBA").resize((tile, tile), Image.NEAREST)
    canvas = Image.new("RGBA", (tile, tile), (0, 0, 0, 0))
    canvas.alpha_composite(panel)
    from PIL import ImageDraw

    draw = ImageDraw.Draw(canvas)
    joints = {j["label"].upper(): (j["x"] * tile, j["y"] * tile) for j in pose["joints"]}
    for a, b in BONES:
        if a in joints and b in joints:
            draw.line([joints[a], joints[b]], fill=(240, 196, 90, 255), width=2)
    for label, (x, y) in joints.items():
        colour = (255, 96, 96, 255) if label.startswith("RIGHT") else (96, 190, 255, 255)
        draw.ellipse([x - 3, y - 3, x + 3, y + 3], fill=colour)
    grip = pose.get("grip") or {}
    point = grip.get("point")
    direction = grip.get("bladeDirection")
    if point and direction:
        length = grip.get("bladeLength", 0.2305) * tile
        norm = (direction["x"] ** 2 + direction["y"] ** 2) ** 0.5 or 1
        tip = (point["x"] * tile + direction["x"] / norm * length, point["y"] * tile + direction["y"] / norm * length)
        draw.line([(point["x"] * tile, point["y"] * tile), tip], fill=(210, 235, 255, 255), width=3)
    sheet.alpha_composite(canvas, (PAD + index * (tile + PAD), PAD))
sheet.save(EXP / "poses-sheet.png")
print(f"poses-sheet.png: {sheet.size}")
