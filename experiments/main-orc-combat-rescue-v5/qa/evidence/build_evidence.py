# QA independente - main-orc-combat-rescue-v5 - evidencias (le fontes; escreve so em qa/evidence/)
import json, os
from PIL import Image, ImageDraw

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
OUT = os.path.join(ROOT, 'experiments', 'main-orc-combat-rescue-v5', 'qa', 'evidence')
os.makedirs(OUT, exist_ok=True)

def rp(rel):
    return os.path.join(ROOT, rel.replace('/', os.sep))

def load_clip(rel):
    with open(rp(rel), 'r', encoding='utf-8') as f:
        return json.load(f)

def zoom(img, factor):
    return img.resize((img.width * factor, img.height * factor), Image.NEAREST)

def native_crop(img):
    return img.crop((64, 64, 192, 192))

def frame_img(frame, key='png'):
    return Image.open(rp(frame[key])).convert('RGBA')

report = {}

# 1) Corpos traseiros layers-off (4 clipes x 8 quadros)
rear_cells = ['back_r/Sword', 'back_r/Axe', 'back_l/Sword', 'back_l/Axe']
tile, zf = 128, 3
sheet = Image.new('RGBA', ((8 * tile + 9) * zf, (4 * tile + 5) * zf), (24, 24, 28, 255))
d = ImageDraw.Draw(sheet)
rows_info = {}
for r, cell in enumerate(rear_cells):
    clip = load_clip('characters/orc-v1/source/combat-rescue-v5/combat/%s/clip.json' % cell)
    rows_info[cell] = [bool(f.get('weaponVisible')) for f in clip['frames']]
    for c, fr in enumerate(clip['frames']):
        body = native_crop(Image.open(rp(fr['layers']['body']['png'])).convert('RGBA'))
        x = (c * tile + c + 1) * zf
        y = (r * tile + r + 1) * zf
        sheet.paste(body, (x, y))
        vis = 'W' if fr.get('weaponVisible') else '-'
        d.text((x + 4, y + 2), '%s F%d%s' % (cell.replace('_', ''), c, vis), fill=(255, 220, 120, 255))
sheet.save(os.path.join(OUT, 'rear_bodies_layersoff_3x.png'))
report['rear_bodies_weaponVisible'] = rows_info

# 2) Compositos traseiros nativos
sheet = Image.new('RGBA', ((8 * tile + 9) * zf, (4 * tile + 5) * zf), (24, 24, 28, 255))
d = ImageDraw.Draw(sheet)
for r, cell in enumerate(rear_cells):
    clip = load_clip('characters/orc-v1/source/combat-rescue-v5/combat/%s/clip.json' % cell)
    for c, fr in enumerate(clip['frames']):
        nat = frame_img(fr, 'nativePng')
        x = (c * tile + c + 1) * zf
        y = (r * tile + r + 1) * zf
        sheet.paste(nat, (x, y))
        d.text((x + 4, y + 2), '%s F%d' % (cell.replace('_', ''), c), fill=(160, 255, 160, 255))
sheet.save(os.path.join(OUT, 'rear_composites_native_3x.png'))

# 3) Grips: janela 56x56 centrada em rightGrip; topo composto, base handFront (8 clipes, quadros visiveis)
weapon_cells = ['front_r/Sword', 'front_l/Sword', 'back_r/Sword', 'back_l/Sword',
                'front_r/Axe', 'front_l/Axe', 'back_r/Axe', 'back_l/Axe']
crop_r, gz = 28, 4
rows = []
for cell in weapon_cells:
    clip = load_clip('characters/orc-v1/source/combat-rescue-v5/combat/%s/clip.json' % cell)
    rows.append((cell, [fr for fr in clip['frames'] if fr.get('weaponVisible')]))
total_frames = sum(len(fv) for _, fv in rows)
cw = crop_r * 2 * gz
sheet = Image.new('RGBA', (total_frames * cw + total_frames + 1, len(rows) * (cw * 2 + 2) + 1), (24, 24, 28, 255))
d = ImageDraw.Draw(sheet)
report['grip_opaque_px'] = {}
y = 1
for cell, fv in rows:
    x = 1
    for fr in fv:
        gx, gy = fr.get('rightGrip', [0, 0])
        comp = frame_img(fr, 'png')
        hf = Image.open(rp(fr['layers']['handFront']['png'])).convert('RGBA')
        box = (max(0, gx - crop_r), max(0, gy - crop_r), min(256, gx + crop_r), min(256, gy + crop_r))
        sheet.paste(zoom(comp.crop(box), gz), (x, y))
        sheet.paste(zoom(hf.crop(box), gz), (x, y + cw))
        d.text((x + 2, y + 2), '%s F%d' % (cell.replace('_', ''), fr['index']), fill=(255, 255, 160, 255))
        d.text((x + 2, y + cw + 2), 'hand', fill=(160, 220, 255, 255))
        report['grip_opaque_px']['%s/F%d' % (cell, fr['index'])] = sum(1 for p in hf.split()[3].getdata() if p > 0)
        x += cw + 1
    y += cw * 2 + 2
sheet.save(os.path.join(OUT, 'grips_8clips_4x.png'))

with open(os.path.join(OUT, 'numeric-checks-part1.json'), 'w', encoding='utf-8') as f:
    json.dump(report, f, indent=2)
print('PART1 OK')
