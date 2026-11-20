import json
from PIL import Image
import numpy as np

directions = ['front_r', 'front_l', 'back_r', 'back_l']

print("=== Main Orc Hit Reaction Inspection ===")
for d in directions:
    p = f'characters/orc-v1/source/complete-v1/{d}/Hit/clip.json'
    with open(p) as f:
        data = json.load(f)
    
    total_dur = data.get('totalDurationMs', sum(data.get('durationsMs', [])))
    print(f"\n--- Direction: {d} (Total Duration: {total_dur}ms, Frames: {len(data['frames'])}) ---")
    print(f"Durations: {data.get('durationsMs')}")
    
    strip = Image.new('RGBA', (256 * len(data['frames']), 256))
    for fr in data['frames']:
        idx = fr['index']
        png = 'characters/orc-v1/source/complete-v1/' + fr['png'] if not fr['png'].startswith('characters') else fr['png']
        im = Image.open(png).convert('RGBA')
        arr = np.array(im)
        ys, xs = np.where(arr[:, :, 3] > 10)
        
        # Calculate centroid
        cy = np.mean(ys)
        cx = np.mean(xs)
        bottom = ys.max()
        
        print(f"  Frame {idx:02d} ({fr.get('phase', 'phase'):18s}, {fr.get('durationMs')}ms): bbox x=[{xs.min()},{xs.max()}] y=[{ys.min()},{ys.max()}] bottom={bottom} centroid=({cx:.1f}, {cy:.1f})")
        strip.paste(im, (idx * 256, 0))
        
    strip.save(f'experiments/main-orc-rear-recovery-v2/hit_{d}_strip.png')
    print(f"  Saved strip: experiments/main-orc-rear-recovery-v2/hit_{d}_strip.png")
