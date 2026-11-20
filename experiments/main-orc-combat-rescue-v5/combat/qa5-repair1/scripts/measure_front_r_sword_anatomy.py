import os, json
from PIL import Image, ImageDraw

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../.."))
SWORD_BODY_DIR = os.path.join(ROOT, "characters/orc-v1/source/combat-rescue-v5/combat/front_r/Sword/layers/body")
DIAG_DIR = os.path.join(ROOT, "experiments/main-orc-combat-rescue-v5/combat/qa5-repair1/diagnostics")

# Measured anatomical right-arm chain on front_r/Sword (256x256 composite coords)
# Note: in front_r, the character faces down-right; his anatomical right shoulder is on viewer's left (x ~ 102..112),
# and his right arm winds up to the viewer's left (F01..F05) then slashes across the chest to viewer's right (F06..F08),
# recovering back to viewer's left (F09..F12).
ANATOMY_FRONT_R_SWORD = {
    0: {"phase": "combat-entry-start", "weaponVisible": False, "shoulder": [104, 102], "elbow": [92, 118], "wrist": [94, 133], "palm": [96, 138], "fistBox": [91, 133, 101, 144]},
    1: {"phase": "readiness-dip",      "weaponVisible": False, "shoulder": [104, 103], "elbow": [95, 115], "wrist": [98, 122], "palm": [101, 125], "fistBox": [96, 120, 105, 130]},
    2: {"phase": "first-grip-hold",    "weaponVisible": True,  "shoulder": [104, 103], "elbow": [93, 117], "wrist": [96, 128], "palm": [99, 132], "fistBox": [94, 127, 103, 137], "angle": -72},
    3: {"phase": "windup-back",        "weaponVisible": True,  "shoulder": [105, 100], "elbow": [87, 108], "wrist": [82, 117], "palm": [81, 120], "fistBox": [76, 114, 87, 125],  "angle": -115},
    4: {"phase": "windup-Hold",        "weaponVisible": True,  "shoulder": [105, 97],  "elbow": [85, 103], "wrist": [78, 111], "palm": [76, 113], "fistBox": [71, 106, 82, 118],  "angle": -132},
    5: {"phase": "slash-drive",        "weaponVisible": True,  "shoulder": [107, 98],  "elbow": [89, 104], "wrist": [83, 110], "palm": [80, 112], "fistBox": [75, 105, 86, 117],  "angle": -102},
    6: {"phase": "slash-release",      "weaponVisible": True,  "shoulder": [112, 102], "elbow": [126, 109],"wrist": [137, 111],"palm": [141, 111],"fistBox": [136, 106, 146, 117], "angle": 12},
    7: {"phase": "impact-hold",        "weaponVisible": True,  "shoulder": [114, 103], "elbow": [132, 117],"wrist": [146, 125],"palm": [150, 127],"fistBox": [144, 121, 155, 133], "angle": 42},
    8: {"phase": "follow-through",     "weaponVisible": True,  "shoulder": [110, 104], "elbow": [126, 129],"wrist": [141, 140],"palm": [146, 142],"fistBox": [140, 137, 152, 148], "angle": 58},
    9: {"phase": "recover-start",      "weaponVisible": True,  "shoulder": [106, 105], "elbow": [109, 129],"wrist": [119, 144],"palm": [123, 148],"fistBox": [117, 142, 128, 153], "angle": 64},
    10:{"phase": "recover-mid",        "weaponVisible": True,  "shoulder": [104, 104], "elbow": [97, 122], "wrist": [102, 137],"palm": [106, 141],"fistBox": [100, 135, 111, 146], "angle": 48},
    11:{"phase": "recover-withdraw",   "weaponVisible": False, "shoulder": [104, 103], "elbow": [95, 120], "wrist": [99, 136], "palm": [102, 140],"fistBox": [96, 135, 107, 145]},
    12:{"phase": "idle-return",        "weaponVisible": False, "shoulder": [104, 102], "elbow": [92, 118], "wrist": [94, 133], "palm": [96, 138], "fistBox": [91, 133, 101, 144]}
}

with open(os.path.join(DIAG_DIR, "front_r_sword_anatomy.json"), "w", encoding="utf-8") as f:
    json.dump(ANATOMY_FRONT_R_SWORD, f, indent=2)

# Render verification zoom sheet of F02..F10 with anatomical markers and fist boxes
crop_box = (66, 76, 168, 162)
scale = 4
cw = (crop_box[2] - crop_box[0]) * scale
ch = (crop_box[3] - crop_box[1]) * scale

cols = 3
rows = 3
sheet = Image.new("RGBA", (cols * (cw + 8) + 8, rows * (ch + 24) + 8), (24, 28, 34, 255))
draw = ImageDraw.Draw(sheet)

for i, fidx in enumerate(range(2, 11)):
    im = Image.open(os.path.join(SWORD_BODY_DIR, f"{fidx:02d}.png")).convert("RGBA")
    sub = im.crop(crop_box).resize((cw, ch), Image.NEAREST)
    sdraw = ImageDraw.Draw(sub)
    a = ANATOMY_FRONT_R_SWORD[fidx]
    
    def pt(xy):
        return ((xy[0] - crop_box[0]) * scale + scale//2, (xy[1] - crop_box[1]) * scale + scale//2)
    
    sh = pt(a["shoulder"])
    el = pt(a["elbow"])
    wr = pt(a["wrist"])
    pa = pt(a["palm"])
    
    # Draw chain
    sdraw.line([sh, el, wr, pa], fill=(0, 255, 180, 220), width=2)
    for p, col in [(sh, (80, 180, 255)), (el, (255, 220, 60)), (wr, (255, 140, 40)), (pa, (255, 50, 80))]:
        sdraw.ellipse([p[0]-4, p[1]-4, p[0]+4, p[1]+4], fill=col, outline=(0,0,0))
    
    fb = a["fistBox"]
    bx0 = (fb[0] - crop_box[0]) * scale
    by0 = (fb[1] - crop_box[1]) * scale
    bx1 = (fb[2] - crop_box[0] + 1) * scale
    by1 = (fb[3] - crop_box[1] + 1) * scale
    sdraw.rectangle([bx0, by0, bx1, by1], outline=(255, 80, 120, 220), width=2)

    c = i % cols
    r = i // cols
    ox = 8 + c * (cw + 8)
    oy = 8 + r * (ch + 24)
    sheet.paste(sub, (ox, oy))
    draw.text((ox + 4, oy + ch + 4), f"F{fidx:02d} ({a['phase']}) palm={a['palm']} wrist={a['wrist']} ang={a['angle']}", fill=(240, 240, 240, 255))

out_p = os.path.join(DIAG_DIR, "front_r_sword_anatomy_verify.png")
sheet.save(out_p)
print("Saved:", out_p)
