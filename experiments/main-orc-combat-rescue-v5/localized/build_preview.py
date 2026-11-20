from PIL import Image, ImageDraw
import os

ROOT = r"C:\Users\João Orlando\Documents\Projetos Unity\TacticsRPG-CharacterFactory"
os.chdir(ROOT)

def load(p):
    return Image.open(p).convert("RGBA")

outdir = "experiments/main-orc-combat-rescue-v5/localized"
os.makedirs(outdir, exist_ok=True)

# Right arm region composite x[128,147) y[70,101); left arm x[108,127) y[70,101)
REGIONS = {
    "rightArm": (128, 147, 70, 101),
    "leftArm": (108, 127, 70, 101),
}

for region_name, (x0,x1,y0,y1) in REGIONS.items():
    cw, ch = x1-x0, y1-y0
    # Build two columns: BEFORE (orig) and AFTER (fixed), 8 rows each
    sheet_w = cw*6 + 200
    sheet_h = ch*8*2 + 100
    sheet = Image.new("RGBA", (sheet_w, sheet_h), (0,0,0,0))
    d = ImageDraw.Draw(sheet)
    d.text((10, 5), f"back_l Walk — {region_name}  BEFORE (orig) vs AFTER (fixed)", fill=(255,255,255,255))
    for i in range(8):
        orig = load(f"characters/orc-v1/source/rear-recovery-v2/back_l/Walk/{i:02d}.png").crop((x0,y0,x1,y1)).resize((cw*6, ch*6), Image.NEAREST)
        fixed = load(f"characters/orc-v1/source/combat-rescue-v5/localized/back_l/Walk/{i:02d}.png").crop((x0,y0,x1,y1)).resize((cw*6, ch*6), Image.NEAREST)
        y = 40 + i*ch*6
        sheet.paste(orig, (10, y))
        sheet.paste(fixed, (10+cw*6+20, y))
        d.text((10, y-22), f"F{i:02d}", fill=(255,255,255,255))
        d.text((10+cw*6+20, y-22), f"F{i:02d} fixed", fill=(255,255,255,255))
    # column labels
    d.text((10, 40 + 8*ch*6 + 10), "BEFORE (orig composite)", fill=(200,200,200,255))
    d.text((10+cw*6+20, 40 + 8*ch*6 + 10), "AFTER (fixed)", fill=(200,200,200,255))
    out = os.path.join(outdir, f"preview_{region_name}_before_after.png")
    sheet.save(out)
    print(f"Saved {out} size={sheet.size}")

print("Preview done.")
