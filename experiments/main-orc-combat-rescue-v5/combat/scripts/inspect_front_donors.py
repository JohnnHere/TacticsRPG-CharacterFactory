from pathlib import Path
from PIL import Image
import numpy as np

ROOT = Path(".")

# Let's check Sword F07, F08, F09, F10 and Axe F06, F07, F08 in front_r
for cat, idxs in [("Sword", [1, 5, 6, 7, 8, 9, 10, 11]), ("Axe", [3, 5, 6, 7, 8])]:
    print(f"=== front_r {cat} body+handFront ===")
    for idx0 in idxs:
        bp = ROOT / f"characters/orc-v1/source/rear-reconstruction-v4/front_r/{cat}/layers/body/{idx0:02d}.png"
        hp = ROOT / f"characters/orc-v1/source/rear-reconstruction-v4/front_r/{cat}/layers/handFront/{idx0:02d}.png"
        b = np.array(Image.open(bp).convert("RGBA"))
        h = np.array(Image.open(hp).convert("RGBA"))
        # merge h over b
        m = b.copy()
        mask = h[:, :, 3] > 0
        m[mask] = h[mask]
        nat = m[64:192, 64:192]
        vis = nat[:, :, 3] > 0
        # check right side x=70..115, y=40..78
        r_pts = np.argwhere(vis[40:78, 70:115])
        if len(r_pts):
            xmax = int(r_pts[:, 1].max() + 70)
            ymax_at_xmax = int(r_pts[r_pts[:, 1] == r_pts[:, 1].max(), 0].mean() + 40)
        else:
            xmax, ymax_at_xmax = -1, -1
        print(f"  {cat} F{idx0:02d}: right_reach_xmax={xmax} at y~{ymax_at_xmax} (vis_in_zone={len(r_pts)})")
