from PIL import Image

cand_strip = Image.new('RGBA', (128 * 6, 128))

# Load complete-v1 back_l unarmed frames (offset -64, -64 from composite 256)
for i in range(5):
    p = f'characters/orc-v1/source/complete-v1/back_l/Unarmed/{i:02d}.png'
    im256 = Image.open(p).convert('RGBA')
    # Crop center 128x128
    im128 = im256.crop((64, 64, 192, 192))
    cand_strip.paste(im128, (i * 128, 0))

imp = Image.open('experiments/main-orc-rear-recovery-v2/raw/punch_impact_key_back_l.png').convert('RGBA')
cand_strip.paste(imp, (5 * 128, 0))

cand_strip.save('experiments/main-orc-rear-recovery-v2/compare_unarmed_back_l_strip.png')
print('Saved compare_unarmed_back_l_strip.png')
