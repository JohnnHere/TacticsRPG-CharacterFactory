import os
from PIL import Image

p1 = 'experiments/main-orc-complete-v1/pixellab-recovery/back_r_base.png'
p2 = 'experiments/main-orc-rear-recovery-v2/walk_back_r_key_contact1.png'
p3 = 'experiments/main-orc-rear-recovery-v2/walk_back_r_key_contact2.png'

im_base = Image.open(p1).convert('RGBA')
im_k1 = Image.open(p2).convert('RGBA')
im_k2 = Image.open(p3).convert('RGBA')

print("Base bbox:", im_base.getbbox())
print("K1 bbox:", im_k1.getbbox())
print("K2 bbox:", im_k2.getbbox())

# Check bottom-most Y
def get_bottom_y(im):
    for y in range(im.height - 1, -1, -1):
        for x in range(im.width):
            if im.getpixel((x, y))[3] > 0:
                return y
    return -1

print("Base bottom Y:", get_bottom_y(im_base))
print("K1 bottom Y:", get_bottom_y(im_k1))
print("K2 bottom Y:", get_bottom_y(im_k2))

# Verify that upper body (y < 66) is identical to base
diff_k1 = sum(1 for y in range(66) for x in range(128) if im_base.getpixel((x, y)) != im_k1.getpixel((x, y)))
diff_k2 = sum(1 for y in range(66) for x in range(128) if im_base.getpixel((x, y)) != im_k2.getpixel((x, y)))
print(f"Upper body diff (y < 66) K1 vs Base: {diff_k1} pixels")
print(f"Upper body diff (y < 66) K2 vs Base: {diff_k2} pixels")

# Create contact sheet of the keyposes: Base (Passing), K1 (Contact 1), K2 (Contact 2)
sheet = Image.new('RGBA', (128 * 3, 128), (0, 0, 0, 0))
sheet.paste(im_base, (0, 0))
sheet.paste(im_k1, (128, 0))
sheet.paste(im_k2, (256, 0))
sheet.save('experiments/main-orc-rear-recovery-v2/contact_sheet_keys.png')
print("Saved experiments/main-orc-rear-recovery-v2/contact_sheet_keys.png")
