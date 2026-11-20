from PIL import Image

for d in ['front_r', 'front_l']:
    strip = Image.new('RGBA', (256 * 5, 256))
    for i in range(5):
        im = Image.open(f'characters/orc-v1/source/complete-v1/{d}/Defeat/{i:02d}.png')
        strip.paste(im, (i * 256, 0))
    strip.save(f'experiments/main-orc-rear-recovery-v2/defeat_{d}_strip.png')
    print(f'Saved defeat_{d}_strip.png')
