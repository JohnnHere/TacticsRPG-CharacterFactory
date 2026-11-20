"""Build the T2 review artefacts: 8x before/after crops, a 13-frame axilla sheet and review.html.

Images are written with Pillow from the already-exported PNGs; this is preview composition only,
never production art authorship.
"""
import json
import os

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
V7 = os.path.join(ROOT, "characters", "orc-v1", "source", "combat-recovery-v7", "frontal", "front_l-Sword-full")
V6ESC = os.path.join(ROOT, "characters", "orc-v1", "source", "artistic-reconstruction-v6",
                     "frontal-escalated", "front_l-Sword-full")
V6PLAIN = os.path.join(ROOT, "characters", "orc-v1", "source", "artistic-reconstruction-v6",
                       "frontal", "front_l-Sword-full")
EXP = os.path.join(ROOT, "experiments", "main-orc-combat-recovery-v7", "frontal")

CROP = (140, 106, 174, 136)
ZOOM = 8
BG = (26, 28, 32, 255)


def lum(rgb):
    r, g, b = rgb[:3]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def load(d, name):
    with Image.open(os.path.join(d, name)) as im:
        return im.convert("RGBA")


def tile(img, zoom=ZOOM, crop=CROP, label=None):
    c = img.crop(crop).resize(((crop[2] - crop[0]) * zoom, (crop[3] - crop[1]) * zoom), Image.NEAREST)
    out = Image.new("RGBA", c.size, BG)
    out.alpha_composite(c)
    return out


def hstack(images, gap=6):
    w = sum(i.width for i in images) + gap * (len(images) - 1)
    h = max(i.height for i in images)
    out = Image.new("RGBA", (w, h), BG)
    x = 0
    for im in images:
        out.alpha_composite(im, (x, 0))
        x += im.width + gap
    return out


def vstack(images, gap=6):
    w = max(i.width for i in images)
    h = sum(i.height for i in images) + gap * (len(images) - 1)
    out = Image.new("RGBA", (w, h), BG)
    y = 0
    for im in images:
        out.alpha_composite(im, (0, y))
        y += im.height + gap
    return out


# --- before/after per corrected frame ---------------------------------------
for frame in (3, 4):
    ix = "%02d.png" % frame
    before = load(os.path.join(V6ESC, "layers", "body"), ix)
    after = load(os.path.join(V7, "layers", "body"), ix)
    a = tile(before)
    b = tile(after)
    hstack([a, b]).save(os.path.join(EXP, "before-after-F%02d-8x.png" % frame))
    # full composite comparison at 1x, cropped
    cb = load(V6ESC, ix)
    ca = load(V7, ix)
    hstack([tile(cb, 4), tile(ca, 4)]).save(os.path.join(EXP, "composite-before-after-F%02d-4x.png" % frame))

# --- 13 frame sheet of the repaired body layer ------------------------------
rows = []
for i in range(13):
    img = load(os.path.join(V7, "layers", "body"), "%02d.png" % i)
    rows.append(tile(img, 4))
sheet = vstack([hstack(rows[:7]), hstack(rows[7:])])
sheet.save(os.path.join(EXP, "axilla-13-frames-v7-4x.png"))

# --- numeric before/after table --------------------------------------------
with open(os.path.join(EXP, "edit-plan-v7.json"), encoding="utf-8") as f:
    plan = json.load(f)


def sample(d, frame, x, y):
    with Image.open(os.path.join(d, "layers", "body", "%02d.png" % frame)) as im:
        return im.convert("RGBA").getpixel((x, y))


rows = []
for frame in (3, 4):
    before_img = load(os.path.join(V6ESC, "layers", "body"), "%02d.png" % frame)
    for e in plan[str(frame)]:
        x, y = e["x"], e["y"]
        old = before_img.getpixel((x, y))
        new = tuple(e["rgba"])
        rows.append({
            "frame": frame, "x": x, "y": y, "reason": e["reason"],
            "before": "transparent" if old[3] == 0 else "rgb(%d,%d,%d)" % old[:3],
            "after": "transparent" if new[3] == 0 else "rgb(%d,%d,%d)" % new[:3],
            "beforeL": "%.1f" % lum(old) if old[3] else "-",
            "afterL": "%.1f" % lum(new) if new[3] else "-",
        })

with open(os.path.join(EXP, "edit-table-v7.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(rows, f, indent=2)
    f.write("\n")

with open(os.path.join(EXP, "review.html"), "w", encoding="utf-8", newline="\n") as f:
    f.write("""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<title>V7 ECON — axila front_l/Sword</title>
<style>
body{background:#14161a;color:#dfe3e8;font:14px/1.5 system-ui,sans-serif;margin:24px auto;max-width:1180px;padding:0 16px}
h1{font-size:20px;margin:0 0 4px}h2{font-size:15px;margin:28px 0 8px;color:#9fd0ff}
p.note{color:#8b93a1;max-width:70ch}
img{image-rendering:pixelated;background:#1a1c20;border:1px solid #2c3039;display:block;max-width:100%}
table{border-collapse:collapse;font-size:12px;font-family:ui-monospace,monospace}
th,td{border-bottom:1px solid #262a31;padding:3px 8px;text-align:left;vertical-align:top}
th{color:#9fd0ff;font-weight:600}
td.t{color:#ff9f6b}code{color:#b9e28a}
.badge{display:inline-block;padding:2px 8px;border-radius:10px;font-size:11px;border:1px solid #3a4150;color:#ffd479}
</style></head><body>
<h1>V7 ECON — axila de <code>front_l/Sword</code></h1>
<p class="badge">TECHNICALLY_COMPLETE · VISUAL_REVIEW_REQUIRED · PENDING_CREATOR</p>
<p class="note">Limitação declarada: o DEV não recebeu percepção visual. Tudo aqui vem de medição de
pixels (Pillow) e autoria Lua no Aseprite. Nada foi &ldquo;visto&rdquo;. A coluna da esquerda é o candidato V6
escalonado; a da direita é o V7. Ampliação 8x com vizinho mais próximo, recorte x140..174 / y106..136.</p>

<h2>F03 — camada body, 8x</h2>
<img src="before-after-F03-8x.png" alt="F03 antes/depois">
<h2>F04 — camada body, 8x</h2>
<img src="before-after-F04-8x.png" alt="F04 antes/depois">
<h2>Composto completo, recorte 4x</h2>
<img src="composite-before-after-F03-4x.png" alt="composto F03">
<img src="composite-before-after-F04-4x.png" alt="composto F04" style="margin-top:8px">
<h2>Os 13 quadros do V7 (body, 4x)</h2>
<img src="axilla-13-frames-v7-4x.png" alt="13 quadros">
<h2>Os 19 pixels alterados</h2>
<table><thead><tr><th>Q</th><th>x</th><th>y</th><th>antes</th><th>L</th><th>depois</th><th>L</th><th>motivo</th></tr></thead><tbody>
""")
    for r in rows:
        f.write("<tr><td>F%02d</td><td>%d</td><td>%d</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td class=t>%s</td></tr>\n" % (
            r["frame"], r["x"], r["y"], r["before"], r["beforeL"], r["after"], r["afterL"], r["reason"]))
    f.write("""</tbody></table>
<h2>Provas anexas</h2>
<p class="note">84 arquivos idênticos byte a byte fora do patch; 19 pixels alterados e nenhum outro;
39/39 exportações de <code>weaponBack</code>/<code>weaponFront</code>/<code>handFront</code> idênticas ao V6 depois de
reabrir o mestre; fronteira esquerda da abertura monótona; zero pixels soltos.
Ver <code>verification-v7.json</code> e <code>../../characters/orc-v1/source/combat-recovery-v7/frontal/front_l-Sword-full/clip.json</code>.</p>
</body></html>
""")

print("previews written to", EXP)
for n in sorted(os.listdir(EXP)):
    if n.endswith((".png", ".html")) and ("before-after" in n or "13-frames" in n or n.endswith(".html")):
        print("  ", n)
