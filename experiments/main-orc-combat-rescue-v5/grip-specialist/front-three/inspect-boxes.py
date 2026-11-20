import json
from pathlib import Path
from PIL import Image

plan = json.loads(Path('experiments/main-orc-combat-rescue-v5/grip-specialist/front-three/anatomy-plan.json').read_text(encoding='utf-8'))

for cfg in plan['clips']:
    cid = cfg['cellId']
    print('=== Clip:', cid, '===')
    dir_path = Path('characters/orc-v1/source/combat-rescue-v5/grip-specialist/front-three') / cid
    for f in cfg['frames']:
        idx = f['index']
        fn = f'{idx:02d}.png'
        flat = Image.open(dir_path / fn)
        wb = Image.open(dir_path / 'layers/weaponBack' / fn)
        wf = Image.open(dir_path / 'layers/weaponFront' / fn)
        hf = Image.open(dir_path / 'layers/handFront' / fn)
        
        wb_box = wb.getbbox()
        wf_box = wf.getbbox()
        hf_box = hf.getbbox()
        print(f"  F{idx:02d}: grip={f['grip']}, angle={f['angleDeg']}, rows={len(f['gloveRows'])}, hf_box={hf_box}, wf_box={wf_box}, wb_box={wb_box}")
