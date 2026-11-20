import os

directions = ["front_r", "front_l", "back_r", "back_l"]
actions = ["Idle", "Walk", "Unarmed", "Sword", "Axe", "Hit", "Defeat"]

for d in directions:
    for a in actions:
        p1 = f"characters/orc-v1/source/complete-v1/{d}/{a}/clip.json"
        p2 = f"characters/orc-v1/source/complete-v1/{d}/{a}/Attack/clip.json"
        if os.path.exists(p1):
            print(f"OK: {d}/{a} -> {p1}")
        elif os.path.exists(p2):
            print(f"OK (Attack subfolder): {d}/{a} -> {p2}")
        else:
            print(f"MISSING: {d}/{a} not found in {p1} or {p2}")
