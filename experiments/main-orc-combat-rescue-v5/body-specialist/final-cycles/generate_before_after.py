import os, json
from PIL import Image, ImageChops

root = os.getcwd()

diff_dir = os.path.join(root, 'experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/repair1')

comparisons = [
    {
        'id': 'REAR-01',
        'cycle': 'back_r-Sword-full',
        'frame': '06.png',
        'frame_idx': 6,
        'title': 'back_r / Sword — F06 (Swoosh Removal & Anatomy Reconstruction)',
        'before': 'experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/back_r-Sword-full/native/06.png',
        'after': 'experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/repair1/back_r-Sword-full/native/06.png',
        'diff_img': 'back_r-Sword-f06-before-after.png'
    },
    {
        'id': 'REAR-02',
        'cycle': 'back_l-Axe-full',
        'frame': '02.png',
        'frame_idx': 2,
        'title': 'back_l / Axe — F02 (Axe Blade & Haft Removal, Fist Reconstruction)',
        'before': 'experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/back_l-Axe-full/native/02.png',
        'after': 'experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/repair1/back_l-Axe-full/native/02.png',
        'diff_img': 'back_l-Axe-f02-before-after.png'
    },
    {
        'id': 'REAR-03',
        'cycle': 'back_l-Sword-full',
        'frame': '05.png',
        'frame_idx': 5,
        'title': 'back_l / Sword — F05 (7-10px Hook Removal Above Pauldron)',
        'before': 'experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/back_l-Sword-full/native/05.png',
        'after': 'experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/repair1/back_l-Sword-full/native/05.png',
        'diff_img': 'back_l-Sword-f05-before-after.png'
    }
]

diff_report = []

for comp in comparisons:
    im_b = Image.open(os.path.join(root, comp['before'])).convert('RGBA')
    im_a = Image.open(os.path.join(root, comp['after'])).convert('RGBA')
    
    diff = ImageChops.difference(im_b, im_a)
    diff_pts = []
    for y in range(128):
        for x in range(128):
            if im_b.getpixel((x, y)) != im_a.getpixel((x, y)):
                diff_pts.append((x, y, im_b.getpixel((x, y)), im_a.getpixel((x, y))))
                
    # Create side-by-side image: [Before (128x128)] [After (128x128)] [Diff (128x128)] -> 384x128
    sbs = Image.new('RGBA', (384, 128), (20, 24, 30, 255))
    sbs.paste(im_b, (0, 0))
    sbs.paste(im_a, (128, 0))
    # highlight diff in red/yellow
    diff_visual = Image.new('RGBA', (128, 128), (0, 0, 0, 255))
    for x, y, cb, ca in diff_pts:
        diff_visual.putpixel((x, y), (255, 60, 60, 255))
    sbs.paste(diff_visual, (256, 0))
    
    sbs_path = os.path.join(diff_dir, comp['diff_img'])
    sbs.save(sbs_path)
    
    bright_before = sum(1 for y in range(128) for x in range(128) if im_b.getpixel((x, y))[3] > 0 and im_b.getpixel((x, y))[0] > 160 and im_b.getpixel((x, y))[1] > 160 and im_b.getpixel((x, y))[2] > 160)
    bright_after = sum(1 for y in range(128) for x in range(128) if im_a.getpixel((x, y))[3] > 0 and im_a.getpixel((x, y))[0] > 160 and im_a.getpixel((x, y))[1] > 160 and im_a.getpixel((x, y))[2] > 160)
    
    rep_item = {
        'id': comp['id'],
        'cycle': comp['cycle'],
        'frame': comp['frame'],
        'title': comp['title'],
        'pixelsChangedCount': len(diff_pts),
        'brightPixelsBefore': bright_before,
        'brightPixelsAfter': bright_after,
        'bboxBefore': list(im_b.getbbox()),
        'bboxAfter': list(im_a.getbbox()),
        'sideBySideImage': comp['diff_img']
    }
    diff_report.append(rep_item)
    print(f"Generated diff for {comp['id']}: {len(diff_pts)} pixels changed. Bright: {bright_before} -> {bright_after}")

with open(os.path.join(diff_dir, 'before-after-diff.json'), 'w', encoding='utf-8') as f:
    json.dump(diff_report, f, indent=2)
print("before-after-diff.json written successfully!")
