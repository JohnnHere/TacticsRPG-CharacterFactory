import os
import json
import numpy as np
from PIL import Image

# Directories
candidate_dir = 'characters/orc-v1/source/rear-recovery-v2/back_r/Walk'
aseprite_dir = 'characters/orc-v1/source/aseprite/rear-recovery-v2'
os.makedirs(candidate_dir, exist_ok=True)
os.makedirs(os.path.join(aseprite_dir, 'native'), exist_ok=True)
os.makedirs(os.path.join(aseprite_dir, 'composite', 'back_r'), exist_ok=True)
os.makedirs('experiments/main-orc-rear-recovery-v2', exist_ok=True)

# Load base and keys
p_base = 'experiments/main-orc-complete-v1/pixellab-recovery/back_r_base.png'
p_k1 = 'experiments/main-orc-rear-recovery-v2/walk_back_r_key_contact1.png'
p_k2 = 'experiments/main-orc-rear-recovery-v2/walk_back_r_key_contact2.png'

im_base = Image.open(p_base).convert('RGBA')
im_k1 = Image.open(p_k1).convert('RGBA')
im_k2 = Image.open(p_k2).convert('RGBA')

# Function to align bottom to target_ground_y
def snap_ground(im, target_ground_y=126):
    bbox = im.getbbox()
    if not bbox:
        return im
    bottom = bbox[3] - 1
    dy = target_ground_y - bottom
    if dy == 0:
        return im
    out = Image.new('RGBA', im.size, (0, 0, 0, 0))
    out.paste(im, (0, dy))
    return out

# In pixel art, in-betweens blend morphological poses while retaining integer pixel crispness
# For upper body (y < 66), it is identical across base, k1, k2.
# We can add a subtle 1px contra-lateral shoulder bob on frames 2..4 and 10..12.
def build_frame(idx):
    # 16-frame cycle:
    # 0: K1 (Contact 1)
    # 1: K1 -> Pass 1 (Down/settle)
    # 2: K1 -> Pass 1 (Push-off)
    # 3: Pass 1 (Passing leg lifting)
    # 4: Pass 1 (Mid-stance)
    # 5: Pass 1 -> K2 (Extension)
    # 6: Pass 1 -> K2 (Pre-contact)
    # 7: K2 entry
    # 8: K2 (Contact 2)
    # 9: K2 -> Pass 2 (Down/settle)
    # 10: K2 -> Pass 2 (Push-off)
    # 11: Pass 2 (Passing leg lifting)
    # 12: Pass 2 (Mid-stance)
    # 13: Pass 2 -> K1 (Extension)
    # 14: Pass 2 -> K1 (Pre-contact)
    # 15: K1 entry
    
    # Weights for blending lower body
    # Keys at 0 (K1), 4 (Base/Pass1), 8 (K2), 12 (Base/Pass2)
    t = idx / 16.0
    
    # Upper body bob: subtle 1px drop at down frames (1, 2, 9, 10)
    bob_y = 1 if idx in [1, 2, 9, 10] else 0
    
    # Construct base frame
    if idx == 0:
        src = im_k1.copy()
    elif idx == 8:
        src = im_k2.copy()
    elif idx == 4 or idx == 12:
        src = im_base.copy()
    elif 0 < idx < 4:
        alpha = idx / 4.0
        # Blend K1 -> Base
        src = Image.blend(im_k1, im_base, alpha)
    elif 4 < idx < 8:
        alpha = (idx - 4) / 4.0
        # Blend Base -> K2
        src = Image.blend(im_base, im_k2, alpha)
    elif 8 < idx < 12:
        alpha = (idx - 8) / 4.0
        # Blend K2 -> Base
        src = Image.blend(im_k2, im_base, alpha)
    else: # 12 < idx < 16
        alpha = (idx - 12) / 4.0
        # Blend Base -> K1
        src = Image.blend(im_base, im_k1, alpha)
    
    # Clean threshold alpha for sharp pixel art
    arr = np.array(src)
    # Alpha threshold at 128
    alpha_mask = arr[:, :, 3] >= 128
    arr[:, :, 3] = np.where(alpha_mask, 255, 0)
    
    # Ensure upper body (y < 66) is strictly from im_base with bob_y
    base_arr = np.array(im_base)
    out_img = Image.fromarray(arr, 'RGBA')
    
    # Upper body slice
    upper_base = Image.new('RGBA', (128, 66), (0, 0, 0, 0))
    upper_base.paste(im_base.crop((0, 0, 128, 66)), (0, 0))
    
    # Paste upper body with bob_y
    final_img = Image.new('RGBA', (128, 128), (0, 0, 0, 0))
    final_img.paste(out_img, (0, 0))
    final_img.paste(upper_base, (0, bob_y))
    
    # Ground snap: ensure bottom pixel is at y = 126
    final_img = snap_ground(final_img, 126)
    return final_img

frames_128 = []
frames_256 = []

# Generate 16 frames
for i in range(16):
    f128 = build_frame(i)
    frames_128.append(f128)
    
    # Save 128x128 sprite in experiment folder
    f128.save(f'experiments/main-orc-rear-recovery-v2/walk_back_r_{i:02d}.png')
    
    # Create 256x256 composite frame (offset 64, 64)
    f256 = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    f256.paste(f128, (64, 64))
    frames_256.append(f256)
    f256.save(os.path.join(candidate_dir, f'{i:02d}.png'))

# Save native horizontal strip (2048 x 128)
strip = Image.new('RGBA', (128 * 16, 128), (0, 0, 0, 0))
for i, f in enumerate(frames_128):
    strip.paste(f, (i * 128, 0))
strip.save(os.path.join(candidate_dir, 'native-strip.png'))
strip.save('experiments/main-orc-rear-recovery-v2/native-strip.png')

# Save 4x4 review grid
grid = Image.new('RGBA', (128 * 4, 128 * 4), (0, 0, 0, 0))
for i, f in enumerate(frames_128):
    gx = (i % 4) * 128
    gy = (i // 4) * 128
    grid.paste(f, (gx, gy))
grid.save('experiments/main-orc-rear-recovery-v2/grid-walk-back_r-candidate.png')

# Save animated GIF preview for visual inspection
frames_128[0].save(
    'experiments/main-orc-rear-recovery-v2/walk_back_r_candidate.gif',
    save_all=True,
    append_images=frames_128[1:],
    duration=80,
    loop=0,
    disposal=2
)

# Write candidate clip.json
clip_meta = {
    "schemaVersion": 1,
    "revision": "main-orc-rear-recovery-v2",
    "id": "locomotion.walk-v2",
    "character": "orc-v1",
    "state": "Walk",
    "legacySlotState": "Walk",
    "direction": "back_r",
    "loop": True,
    "oneShot": False,
    "terminal": False,
    "canvas": [256, 256],
    "bodyOffset": [64, 64],
    "groundY": 190,
    "nativeCanvas": [128, 128],
    "nativeGroundY": 126,
    "ppu": 100,
    "frameCount": 16,
    "durationsMs": [80] * 16,
    "totalDurationMs": 1280,
    "master": "characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_r/walk-unarmed.aseprite",
    "nativeMaster": "characters/orc-v1/source/aseprite/rear-recovery-v2/native/walk-back_r.aseprite",
    "strip": "characters/orc-v1/source/rear-recovery-v2/back_r/Walk/native-strip.png",
    "visibilityPolicy": "attack-only-v1",
    "weaponVisible": False,
    "weaponOverlay": False,
    "contactEvent": None,
    "frames": [
        {
            "index": i,
            "png": f"characters/orc-v1/source/rear-recovery-v2/back_r/Walk/{i:02d}.png",
            "durationMs": 80,
            "phase": "stride1" if i < 8 else "stride2",
            "groundY": 190,
            "nativeGroundY": 126
        }
        for i in range(16)
    ]
}

with open(os.path.join(candidate_dir, 'clip.json'), 'w', encoding='utf-8') as f:
    json.dump(clip_meta, f, indent=2)

print("Generated 16 frames, strip, grid, and clip.json successfully.")
