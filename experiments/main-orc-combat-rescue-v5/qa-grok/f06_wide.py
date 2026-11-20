from pathlib import Path
from PIL import Image, ImageDraw
ROOT = Path(r"C:\Users\João Orlando\Documents\Projetos Unity\TacticsRPG-CharacterFactory")
base = ROOT / "characters/orc-v1/source/combat-rescue-v5/combat/qa5-repair1/front_r/Sword"
out = ROOT / "experiments/main-orc-combat-rescue-v5/qa-grok/evidence"

def load(rel):
    return Image.open(base / rel).convert("RGBA")

frames = []
for i in (2, 6, 7, 8):
    body = load(f"layers/body/{i:02d}.png")
    hand = load(f"layers/handFront/{i:02d}.png")
    wf = load(f"layers/weaponFront/{i:02d}.png")
    wb = load(f"layers/weaponBack/{i:02d}.png")
    comp = Image.alpha_composite(Image.alpha_composite(Image.alpha_composite(wb, body), wf), hand)
    # mark hand pixels cyan on a copy so the stamp is locatable without replacing the read
    marked = comp.copy()
    mp, hp = marked.load(), hand.load()
    for y in range(256):
        for x in range(256):
            if hp[x, y][3]:
                mp[x, y] = (0, 220, 255, 255)
    pair = Image.new("RGBA", (256 * 2 * 2 + 8, 256 * 2 + 16), (10, 14, 18, 255))
    pair.paste(comp.resize((512, 512), Image.NEAREST), (0, 16))
    pair.paste(marked.resize((512, 512), Image.NEAREST), (520, 16))
    ImageDraw.Draw(pair).text((2, 1), f"F{i:02d} composite | cyan=handFront pixels", fill=(230, 200, 120, 255))
    frames.append(pair)
sheet = Image.new("RGBA", (frames[0].width, sum(f.height for f in frames)), (8, 10, 14, 255))
y = 0
for f in frames:
    sheet.paste(f, (0, y))
    y += f.height
sheet.save(out / "repair1_f06_wide.png")
print("saved", sheet.size)
