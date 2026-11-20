import json, hashlib
from pathlib import Path
from PIL import Image
import numpy as np

def delta(a, b):
    return int(((a != b).any(2) & ((a[:,:,3]>0) | (b[:,:,3]>0))).sum())

plan = json.loads(Path('experiments/main-orc-combat-rescue-v5/grip-specialist/front-three/anatomy-plan.json').read_text(encoding='utf-8'))
snap = json.loads(Path('experiments/main-orc-combat-rescue-v5/grip-specialist/front-three/input-snapshot.json').read_text(encoding='utf-8'))

for cfg in plan['clips']:
    cid = cfg['cellId']
    print('Checking', cid)
    parent = json.loads(Path(snap['clips'][cid]).read_text(encoding='utf-8'))
    dir_path = Path('characters/orc-v1/source/combat-rescue-v5/grip-specialist/front-three') / cid
    
    for fi, pf in enumerate(parent['frames']):
        fn = f'{fi:02d}.png'
        flat = np.array(Image.open(dir_path / fn).convert('RGBA'))
        body = np.array(Image.open(dir_path / 'layers/body' / fn).convert('RGBA'))
        wb = np.array(Image.open(dir_path / 'layers/weaponBack' / fn).convert('RGBA'))
        wf = np.array(Image.open(dir_path / 'layers/weaponFront' / fn).convert('RGBA'))
        hf = np.array(Image.open(dir_path / 'layers/handFront' / fn).convert('RGBA'))
        native = np.array(Image.open(dir_path / 'native' / fn).convert('RGBA'))
        
        orig_body = np.array(Image.open(pf['layers']['body']['png']).convert('RGBA'))
        d_body = delta(body, orig_body)
        assert d_body == 0, f'{cid} F{fi} body delta != 0 ({d_body})'
        
        assert delta(body[64:192, 64:192], native) == 0, f'{cid} F{fi} native crop mismatch'
        
        is_visible = (cfg['visibleInterval'][0] <= fi <= cfg['visibleInterval'][1])
        if not is_visible:
            assert wb[:,:,3].sum() == 0, f'{cid} F{fi} wb not empty'
            assert wf[:,:,3].sum() == 0, f'{cid} F{fi} wf not empty'
            assert hf[:,:,3].sum() == 0, f'{cid} F{fi} hf not empty'
            assert delta(flat, body) == 0, f'{cid} F{fi} flat != body when weapon hidden'
        else:
            assert wf[:,:,3].sum() > 0 or wb[:,:,3].sum() > 0, f'{cid} F{fi} weapon empty when visible'
            assert hf[:,:,3].sum() > 0, f'{cid} F{fi} handFront empty when visible'
            hand_mask = hf[:,:,3] > 0
            assert np.all(body[hand_mask, 3] > 0), f'{cid} F{fi} handFront pixels outside body'
    print(f'{cid}: all {len(parent["frames"])} frames verified perfectly!')
