from PIL import Image
import os

ROOT = r"C:\Users\João Orlando\Documents\Projetos Unity\TacticsRPG-CharacterFactory"
os.chdir(ROOT)

def load(p):
    return Image.open(p).convert("RGBA")

native = load("tmp/opencode_export/native_backl_f00.png")
comp = load("characters/orc-v1/source/rear-recovery-v2/back_l/Walk/00.png")

pn = native.load(); pc = comp.load()
# Test mapping: composite(64+nx, 64+ny) == native(nx, ny) ?
mismatches = 0
checked = 0
for ny in range(128):
    for nx in range(128):
        cx, cy = 64 + nx, 64 + ny
        if pc[cx, cy] != pn[nx, ny]:
            mismatches += 1
        checked += 1
print(f"Mapping composite(64+nx,64+ny)==native(nx,ny): {checked} checked, {mismatches} mismatches")
