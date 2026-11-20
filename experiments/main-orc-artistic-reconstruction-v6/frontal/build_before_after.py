# V6 frontal: before/after diagnostic boards (layout only) + index.
import json
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path.cwd()
OUT = Path('experiments/main-orc-artistic-reconstruction-v6/frontal')
NEW = ROOT / 'characters/orc-v1/source/artistic-reconstruction-v6/frontal'
BEF = OUT / 'before'
CELLS = {
    'front_l/Sword': 'front_l-Sword-full',
    'front_r/Sword': 'full-front-r-sword',
    'front_r/Axe':   'front_r-Axe-full',
    'front_l/Axe':   'front_l-Axe-full',
}
plan = json.loads((OUT / 'fixes-plan.json').read_text(encoding='utf-8'))['plan']
BA = OUT / 'before-after'
BA.mkdir(parents=True, exist_ok=True)
Z = 3
index = []
for key, slug in CELLS.items():
    for fid_str, edits in plan[key].items():
        i = int(fid_str)
        bef = Image.open(BEF / slug / f'{i:02d}.png').convert('RGBA')
        aft = Image.open(NEW / slug / f'{i:02d}.png').convert('RGBA')
        xs = [e['x'] + 64 for e in edits]; ys = [e['y'] + 64 for e in edits]
        x0 = max(0, min(xs) - 10); y0 = max(0, min(ys) - 10)
        x1 = min(256, max(xs) + 11); y1 = min(256, max(ys) + 11)
        zw, zh = (x1 - x0) * Z, (y1 - y0) * Z
        W = 256 * 2 + 16
        H = 256 + 8 + zh + 4
        board = Image.new('RGBA', (W, H), (250, 250, 250, 255))
        board.paste(bef, (0, 0))
        board.paste(aft, (272, 0))
        bz = bef.crop((x0, y0, x1, y1)).resize((zw, zh), Image.NEAREST)
        az = aft.crop((x0, y0, x1, y1)).resize((zw, zh), Image.NEAREST)
        board.paste(bz, (0, 264))
        board.paste(az, (zw + 16, 264))
        d = ImageDraw.Draw(board)
        d.rectangle([0, 0, 255, 255], outline=(120, 120, 120, 255))
        d.rectangle([272, 0, 527, 255], outline=(120, 120, 120, 255))
        d.text((4, 2), f'BEFORE F{fid_str}', fill=(0, 0, 0, 255))
        d.text((276, 2), f'AFTER F{fid_str}', fill=(0, 0, 0, 255))
        d.text((4, 264 + zh + 0), f'{key} edits={len(edits)} zoom {Z}x crop=({x0},{y0})-({x1},{y1})', fill=(0, 0, 0, 255))
        p = BA / f'ba-{slug}-F{fid_str}.png'
        board.convert('RGB').save(p)
        index.append({'cell': key, 'frame': i, 'file': 'experiments/main-orc-artistic-reconstruction-v6/frontal/before-after/' + p.name, 'edits': len(edits),
                      'islands': sum(1 for e in edits if e['kind'] == 'island')})
(OUT / 'before-after-index.json').write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding='utf-8')
print('before/after boards:', len(index))
