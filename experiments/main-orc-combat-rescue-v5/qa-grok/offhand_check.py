from PIL import Image
from pathlib import Path
ROOT = Path(r"C:\Users\João Orlando\Documents\Projetos Unity\TacticsRPG-CharacterFactory")

def load(rel):
    return Image.open(ROOT / rel).convert("RGBA")

def column_delta(direction, action, n):
    frames = [load(f"characters/orc-v1/source/combat-rescue-v5/combat/{direction}/{action}/native/{i:02d}.png") for i in range(n)]
    base = frames[0].load()
    out = []
    for i, im in enumerate(frames):
        pix = im.load()
        changed = 0
        checked = 0
        for y in range(10, 85):
            if direction == "back_r":
                x_max = 45 if y < 50 else (43 if y <= 62 else 42)
                xs = range(0, x_max + 1)
            else:
                x_min = 82 if y < 50 else (84 if y <= 62 else 85)
                xs = range(x_min, 128)
            for x in xs:
                checked += 1
                if pix[x, y] != base[x, y]:
                    changed += 1
        out.append(changed)
    return out

for key, n in (("back_r/Sword", 8), ("back_r/Axe", 8), ("back_l/Sword", 8), ("back_l/Axe", 8), ("back_r/Unarmed", 5), ("back_l/Unarmed", 5)):
    d, a = key.split("/")
    print(key, column_delta(d, a, n))
