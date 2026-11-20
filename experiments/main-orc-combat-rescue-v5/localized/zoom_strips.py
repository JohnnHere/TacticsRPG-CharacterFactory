from PIL import Image, ImageDraw
import os

ROOT = r"C:\Users\João Orlando\Documents\Projetos Unity\TacticsRPG-CharacterFactory"
os.chdir(ROOT)

def load(p):
    return Image.open(p).convert("RGBA")

def outdir():
    d = "experiments/main-orc-combat-rescue-v5/localized"
    os.makedirs(d, exist_ok=True)
    return d

def vertical_strip(frames, labels, crop, scale=6, out="strip.png"):
    """crop = (x0,y0,x1,y1). Stack each frame's crop vertically with label."""
    x0, y0, x1, y1 = crop
    cw, ch = x1 - x0, y1 - y0
    n = len(frames)
    sheet = Image.new("RGBA", (cw * scale + 120, ch * scale * n + 40 * n), (0, 0, 0, 0))
    d = ImageDraw.Draw(sheet)
    for i, (im, lab) in enumerate(zip(frames, labels)):
        c = im.crop((x0, y0, x1, y1)).resize((cw * scale, ch * scale), Image.NEAREST)
        sheet.paste(c, (60, i * (ch * scale + 40)))
        d.text((60, i * (ch * scale + 40) - 28), lab, fill=(255, 255, 255, 255))
    sheet.save(os.path.join(outdir(), out))
    print(f"Saved {os.path.join(outdir(), out)}  size={sheet.size}")

# 1. Rear walk arm strip: back_r and back_l, arm region x:100-148 y:58-100
for direction, clipdir, nframes in [
    ("back_r", "characters/orc-v1/source/rear-recovery-v2/back_r/Walk", 8),
    ("back_l", "characters/orc-v1/source/rear-recovery-v2/back_l/Walk", 8),
]:
    frames = [load(f"{clipdir}/{i:02d}.png") for i in range(nframes)]
    labels = [f"{direction} F{i:02d}" for i in range(nframes)]
    vertical_strip(frames, labels, (95, 55, 150, 105), out=f"armstrip_{direction}.png")

# 2. Front walk cloth strip: between legs region x:120-140 y:105-140
for direction, clipdir, nframes in [
    ("front_r", "characters/orc-v1/source/complete-v1/front_r/Walk", 16),
    ("front_l", "characters/orc-v1/source/complete-v1/front_l/Walk", 16),
]:
    frames = [load(f"{clipdir}/{i:02d}.png") for i in range(nframes)]
    labels = [f"{direction} F{i:02d}" for i in range(nframes)]
    vertical_strip(frames, labels, (118, 100, 142, 145), out=f"clothstrip_{direction}.png")

print("Done.")
