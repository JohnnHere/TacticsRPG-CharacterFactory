import os
for root in [
    r"characters/orc-v1/source/combat-rescue-v5/localized",
    r"experiments/main-orc-combat-rescue-v5/localized",
]:
    print("=== ", root, " ===")
    for dirpath, dirnames, filenames in os.walk(root):
        for fn in sorted(filenames):
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, r"C:\Users\João Orlando\Documents\Projetos Unity\TacticsRPG-CharacterFactory")
            print("  ", rel)
