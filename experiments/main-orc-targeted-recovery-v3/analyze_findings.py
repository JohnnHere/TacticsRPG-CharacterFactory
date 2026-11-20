import os
import sys
import json
from pathlib import Path
from PIL import Image

ROOT = Path('.').resolve()

def analyze_clip(clip_json_path):
    clip_path = ROOT / clip_json_path
    if not clip_path.exists():
        print(f"NOT FOUND: {clip_json_path}")
        return None
    data = json.loads(clip_path.read_text(encoding='utf-8-sig'))
    base_dir = clip_path.parent
    frames = data.get('frames', [])
    print(f"\n=== CLIP: {clip_json_path} (frames={len(frames)}) ===")
    frame_info = []
    for idx, f in enumerate(frames):
        # find composite frame file or layers
        comp_file = f.get('file')
        comp_path = base_dir / comp_file if comp_file else None
        layers = f.get('layers', [])
        
        info = {'index': idx, 'file': comp_file, 'duration': f.get('duration')}
        if comp_path and comp_path.exists():
            im = Image.open(comp_path).convert('RGBA')
            bbox = im.getbbox()
            info['composite_size'] = im.size
            info['composite_bbox'] = bbox
        
        body_layer = next((l for l in layers if l.get('name') == 'body'), None)
        if body_layer:
            b_path = base_dir / body_layer.get('file')
            if b_path.exists():
                b_im = Image.open(b_path).convert('RGBA')
                info['body_bbox'] = b_im.getbbox()
        
        hand_layer = next((l for l in layers if l.get('name') == 'handFront'), None)
        if hand_layer:
            h_path = base_dir / hand_layer.get('file')
            if h_path.exists():
                h_im = Image.open(h_path).convert('RGBA')
                info['hand_bbox'] = h_im.getbbox()
                
        frame_info.append(info)
        print(f"  Frame {idx:02d}: comp_bbox={info.get('composite_bbox')}, body_bbox={info.get('body_bbox')}, hand_bbox={info.get('hand_bbox')}")
    return frame_info

clips_to_check = [
    'characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2/clip.json',
    'characters/orc-v1/source/rear-recovery-v2/back_l/Sword/Attack-representative-v1/clip.json',
    'characters/orc-v1/source/rear-recovery-v2/back_r/Axe/Attack-representative-v1/clip.json',
    'characters/orc-v1/source/rear-recovery-v2/back_l/Axe/Attack-representative-v1/clip.json',
    'characters/orc-v1/source/rear-recovery-v2/back_l/Unarmed/clip.json',
    'characters/orc-v1/source/rear-recovery-v2/back_r/Unarmed/clip.json',
    'characters/orc-v1/source/rear-recovery-v2/front_r/Unarmed/clip.json',
    'characters/orc-v1/source/rear-recovery-v2/front_l/Unarmed/clip.json',
    'characters/orc-v1/source/rear-recovery-v2/back_r/Walk/clip.json',
    'characters/orc-v1/source/rear-recovery-v2/back_l/Walk/clip.json',
    'characters/orc-v1/source/rear-recovery-v2/front_r/Defeat/clip.json',
    'characters/orc-v1/source/rear-recovery-v2/front_l/Defeat/clip.json',
    'characters/orc-v1/source/complete-v1/front_l/Sword/Attack/clip.json',
    'characters/orc-v1/source/complete-v1/front_r/Walk/clip.json',
    'characters/orc-v1/source/complete-v1/front_l/Walk/clip.json',
]

for c in clips_to_check:
    analyze_clip(c)
