from PIL import Image
import os

ROOT = r"C:\Users\João Orlando\Documents\Projetos Unity\TacticsRPG-CharacterFactory"
os.chdir(ROOT)
ORIG_CLIP = "characters/orc-v1/source/rear-recovery-v2/back_l/Walk"

def load(p):
    return Image.open(p).convert("RGBA")

frames = [load(f"{ORIG_CLIP}/{i:02d}.png") for i in range(8)]

print("back_l Walk composite: arm region opaque-pixel bounding boxes per frame")
print("Right side = x>=128 (image-right arm), Left side = x<=126 (image-left arm)")
print("y range of interest 55-100")
print()
for i in range(8):
    px = frames[i].load()
    # right arm (image right): x in [128,146]
    right_pts = [(x,y) for y in range(55,101) for x in range(128,147) if px[x,y][3] > 0]
    # left arm (image left): x in [108,126]
    left_pts = [(x,y) for y in range(55,101) for x in range(108,127) if px[x,y][3] > 0]
    def bb(pts):
        if not pts: return None
        xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
        return (min(xs),min(ys),max(xs),max(ys),len(pts))
    print(f"F{i:02d}: rightArm={bb(right_pts)}  leftArm={bb(left_pts)}")
