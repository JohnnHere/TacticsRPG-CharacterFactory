"""Emit the V7 axilla edit plan (front_l/Sword F03/F04, body layer, canvas coordinates).

Every value written here is either
  - the colour that the same pixel held in the non-escalated V6 clip (native), or
  - the colour that the adjacent column (x+1) held in the non-escalated clip on the same row,
    used only to break runs of >=3 identical colours on the new medial edge.
No new colour is invented: all values exist in the untouched rows of the same frame.

Output: experiments/main-orc-combat-recovery-v7/frontal/edit-plan-v7.json
"""

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = os.path.join(ROOT, "experiments", "main-orc-combat-recovery-v7", "frontal", "edit-plan-v7.json")

CLEAR = [0, 0, 0, 0]


def px(x, y, rgba, reason):
    return {"x": x, "y": y, "rgba": list(rgba), "reason": reason}


PLAN = {
    "3": [
        # --- flat INK plate removal (V6 painted rgb(12,15,18) over these pixels) ---
        px(148, 116, (6, 6, 8, 255), "native x148/y116; V6 had repainted ink plate"),
        px(147, 117, (2, 2, 3, 255), "native x147/y117"),
        px(147, 118, (2, 2, 3, 255), "native x147/y118"),
        px(147, 119, (20, 20, 26, 255), "native x147/y119"),
        px(147, 120, (27, 28, 34, 255), "native x148/y120 (native x147 run would reach 4 identical)"),
        px(147, 121, (20, 20, 26, 255), "native x147/y121"),
        px(147, 122, (0, 0, 1, 255), "native x148/y122; deepest point of the crease"),
        # --- detached pixel inside the opening ---
        px(149, 122, CLEAR, "orphan 95,96,99 with zero opaque 8-neighbours after V6 erasure"),
        # --- retrograde step: y=123 was 1 px narrower than y=122 and y=124 ---
        px(148, 123, CLEAR, "restores monotone left boundary of the opening (was 2b2d31)"),
    ],
    "4": [
        px(149, 115, (0, 0, 1, 255), "native x149/y115"),
        px(148, 116, (6, 6, 8, 255), "native x148/y116"),
        px(147, 117, (2, 2, 3, 255), "native x147/y117"),
        px(147, 118, (2, 2, 3, 255), "native x147/y118"),
        px(147, 119, (20, 20, 26, 255), "native x147/y119"),
        px(147, 120, (27, 28, 34, 255), "native x148/y120 (native x147 run would reach 4 identical)"),
        px(147, 121, (20, 20, 26, 255), "native x147/y121"),
        px(147, 122, (2, 2, 3, 255), "native x148/y122"),
        # --- comb tooth: 1 px island between the 2 px pinhole and the main opening ---
        px(152, 115, CLEAR, "isolated 77,79,82 island, only the top edge touches the body"),
        px(148, 123, CLEAR, "restores monotone left boundary (was 20,20,26)"),
    ],
}

with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    json.dump(PLAN, f, indent=2)
    f.write("\n")

total = sum(len(v) for v in PLAN.values())
print("wrote", OUT, "frames", sorted(PLAN), "edits", total)
