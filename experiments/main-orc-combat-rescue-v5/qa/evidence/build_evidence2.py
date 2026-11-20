# QA parte 2: Unarmed frontal, Walk back_l, Defeat frontal, preservacao frontal, separacao Sword/Axe
import json, os
from PIL import Image, ImageDraw

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
OUT = os.path.join(ROOT, 'experiments', 'main-orc-combat-rescue-v5', 'qa', 'evidence')

def rp(rel):
    return os.path.join(ROOT, rel.replace('/', os.sep))

def load_clip(rel):
    with open(rp(rel), 'r', encoding='utf-8') as f:
        return json.load(f)

def zoom(img, factor):
    return img.resize((img.width * factor, img.height * factor), Image.NEAREST)

report = {}

def native_of(clip, i):
    fr = clip['frames'][i]
    if fr.get('nativePng'):
        return Image.open(rp(fr['nativePng'])).convert('RGBA')
    return Image.open(rp(fr['png'])).convert('RGBA').crop((64, 64, 192, 192))


# 4) Unarmed frontal F02/F03/F04: pai vs v5
cols = ['paiF02', 'paiF03', 'paiF04', 'v5F02', 'v5F03', 'v5F04']
cw2 = 128 * 3
sheet = Image.new('RGBA', (6 * cw2 + 7, 2 * cw2 + 3), (24, 24, 28, 255))
d = ImageDraw.Draw(sheet)
for r, direction in enumerate(['front_r', 'front_l']):
    v5 = load_clip('characters/orc-v1/source/combat-rescue-v5/combat/%s/Unarmed/clip.json' % direction)
    parent = load_clip('characters/orc-v1/source/rear-recovery-v2/%s/Unarmed/clip.json' % direction)
    imgs = [native_of(parent, i) for i in (2, 3, 4)] + [native_of(v5, i) for i in (2, 3, 4)]
    for c, im in enumerate(imgs):
        x = c * cw2 + c + 1
        y = r * cw2 + r + 1
        sheet.paste(zoom(im, 3), (x, y))
        d.text((x + 4, y + 3), '%s %s' % (direction, cols[c]), fill=(255, 230, 140, 255))
sheet.save(os.path.join(OUT, 'unarmed_front_F02-04_3x.png'))

# 5) back_l/Walk antes/depois + diff (nativo 128)
v5w = load_clip('characters/orc-v1/source/combat-rescue-v5/localized/back_l/Walk/clip.json')
pw = load_clip('characters/orc-v1/source/rear-recovery-v2/back_l/Walk/clip.json')
sheet = Image.new('RGBA', (8 * 384 + 8 * 2 + 3, 3 * 384 + 4), (24, 24, 28, 255))
d = ImageDraw.Draw(sheet)
walk_stats = {'perFrame': {}}
for c in range(8):
    pn = native_of(pw, c)
    vn = native_of(v5w, c)
    color_diff = 0
    alpha_mismatch = 0
    diff = Image.new('RGB', (128, 128), (0, 0, 0))
    dd = diff.load()
    for yy in range(128):
        for xx in range(128):
            p, v = pn.getpixel((xx, yy)), vn.getpixel((xx, yy))
            if p[3] != v[3]:
                alpha_mismatch += 1
            if p[3] > 0 and p[:3] != v[:3]:
                color_diff += 1
                dd[xx, yy] = (255, 40, 40)
    walk_stats['perFrame']['F0%d' % c] = {'colorOnlyDiffs': color_diff, 'alphaMismatches': alpha_mismatch}
    x0 = c * 384 + c * 2 + 1
    sheet.paste(zoom(pn.convert('RGB'), 3), (x0, 1))
    sheet.paste(zoom(vn.convert('RGB'), 3), (x0, 387))
    sheet.paste(zoom(diff, 3), (x0, 773))
    d.text((x0 + 4, 3), 'pai F0%d' % c, fill=(200, 200, 200))
    d.text((x0 + 4, 389), 'v5 F0%d d=%d' % (c, color_diff), fill=(160, 255, 160))
    d.text((x0 + 4, 775), 'diff', fill=(255, 120, 120))
sheet.save(os.path.join(OUT, 'walkl_back_before_after_diff_3x.png'))
walk_stats['durationsParent'] = [f['durationMs'] for f in pw['frames']]
walk_stats['durationsV5'] = [f['durationMs'] for f in v5w['frames']]
report['walk_back_l'] = walk_stats

# 6) Defeat frontal F02/F03/F04 zoom 2x
sheet = Image.new('RGBA', (3 * 256 + 4, 2 * 256 + 3), (24, 24, 28, 255))
d = ImageDraw.Draw(sheet)
for r, direction in enumerate(['front_r', 'front_l']):
    clip = load_clip('characters/orc-v1/source/rear-recovery-v2/%s/Defeat/clip.json' % direction)
    for c, fi in enumerate((2, 3, 4)):
        im = native_of(clip, fi)
        x = c * 256 + c + 1
        y = r * 256 + r + 1
        sheet.paste(zoom(im, 2), (x, y))
        d.text((x + 4, y + 3), '%s/Defeat F0%d' % (direction, fi), fill=(255, 230, 140, 255))
sheet.save(os.path.join(OUT, 'defeat_front_F02-04_2x.png'))

with open(os.path.join(OUT, 'numeric-checks-part2.json'), 'w', encoding='utf-8') as f:
    json.dump(report, f, indent=2)
print('PART2 OK')
