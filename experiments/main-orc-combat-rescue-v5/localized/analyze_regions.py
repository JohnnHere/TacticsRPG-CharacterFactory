from PIL import Image, ImageDraw
import os

ROOT = r"C:\Users\João Orlando\Documents\Projetos Unity\TacticsRPG-CharacterFactory"
os.chdir(ROOT)

def load(p):
    return Image.open(p).convert("RGBA")

def save(im, p):
    im.save(p)

# ---- Build comparison sheets ----
outdir = "experiments/main-orc-combat-rescue-v5/localized"
os.makedirs(outdir, exist_ok=True)

# Helper: make a side-by-side with labels
def side_by_side(images, labels, scale=3, out="comparison.png"):
    # images: list of PIL Images same size
    w, h = images[0].size
    n = len(images)
    sheet = Image.new("RGBA", (w * n + 20 * (n + 1), h + 60), (0, 0, 0, 0))
    d = ImageDraw.Draw(sheet)
    for i, im in enumerate(images):
        x = 20 * (i + 1) + w * i
        sheet.paste(im, (x, 30))
        # label
        d.text((x + 10, 5), labels[i], fill=(255, 255, 255, 255))
    # scale up for viewing
    sheet = sheet.resize((sheet.size[0] * scale, sheet.size[1] * scale), Image.NEAREST)
    sheet.save(os.path.join(outdir, out))
    print(f"Saved {os.path.join(outdir, out)}")

# 1. Rear walk arm comparison: F(i) vs F(i+4) (same arm position, half cycle)
for direction, clipdir, nframes in [
    ("back_r", "characters/orc-v1/source/rear-recovery-v2/back_r/Walk", 8),
    ("back_l", "characters/orc-v1/source/rear-recovery-v2/back_l/Walk", 8),
]:
    imgs = []
    labels = []
    half = nframes // 2
    for i in range(half):
        a = load(f"{clipdir}/{i:02d}.png")
        b = load(f"{clipdir}/{i+half:02d}.png")
        imgs.extend([a, b])
        labels.extend([f"{direction} F{i:02d}", f"{direction} F{i+half:02d}"])
    side_by_side(imgs, labels, out=f"walk_arm_compare_{direction}.png")

# 2. Front walk cloth comparison: F(i) vs F(i+8) (same cloth position, half cycle)
for direction, clipdir, nframes in [
    ("front_r", "characters/orc-v1/source/complete-v1/front_r/Walk", 16),
    ("front_l", "characters/orc-v1/source/complete-v1/front_l/Walk", 16),
]:
    imgs = []
    labels = []
    half = nframes // 2
    for i in range(half):
        a = load(f"{clipdir}/{i:02d}.png")
        b = load(f"{clipdir}/{i+half:02d}.png")
        imgs.extend([a, b])
        labels.extend([f"{direction} F{i:02d}", f"{direction} F{i+half:02d}"])
    side_by_side(imgs, labels, out=f"walk_cloth_compare_{direction}.png")

# 3. Defeat F02, F03, F04 for hand smear + terminal
for direction, clipdir in [
    ("front_r", "characters/orc-v1/source/rear-recovery-v2/front_r/Defeat"),
    ("front_l", "characters/orc-v1/source/rear-recovery-v2/front_l/Defeat"),
]:
    imgs = [load(f"{clipdir}/02.png"), load(f"{clipdir}/03.png"), load(f"{clipdir}/04.png")]
    labels = [f"{direction} F02 drop-to-knees", f"{direction} F03 collapse-impact", f"{direction} F04 terminal"]
    side_by_side(imgs, labels, out=f"defeat_hands_{direction}.png")

print("All comparison sheets generated.")
