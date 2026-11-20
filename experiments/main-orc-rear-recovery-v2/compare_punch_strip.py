from PIL import Image
import numpy as np

# Let's save a visual sheet comparing:
# f00, f02, f03, impact_k, f05, f06, f07
frames = [
    ('f00_guard', Image.open('experiments/main-orc-rear-recovery-v2/raw/frames_unarmed_r/frame_00.png')),
    ('f02_anticip', Image.open('experiments/main-orc-rear-recovery-v2/raw/frames_unarmed_r/frame_02.png')),
    ('f03_coil', Image.open('experiments/main-orc-rear-recovery-v2/raw/frames_unarmed_r/frame_03.png')),
    ('impact_key', Image.open('experiments/main-orc-rear-recovery-v2/raw/punch_impact_key_back_r.png')),
    ('f05_weak', Image.open('experiments/main-orc-rear-recovery-v2/raw/frames_unarmed_r/frame_05.png')),
    ('f06_recoil', Image.open('experiments/main-orc-rear-recovery-v2/raw/frames_unarmed_r/frame_06.png')),
    ('f07_settle', Image.open('experiments/main-orc-rear-recovery-v2/raw/frames_unarmed_r/frame_07.png')),
    ('f08_neutral', Image.open('experiments/main-orc-rear-recovery-v2/raw/frames_unarmed_r/frame_08.png'))
]

sheet = Image.new('RGBA', (128 * len(frames), 128))
for i, (name, img) in enumerate(frames):
    sheet.paste(img, (i * 128, 0))
sheet.save('experiments/main-orc-rear-recovery-v2/punch_comparison_strip.png')
print('Saved punch_comparison_strip.png')
