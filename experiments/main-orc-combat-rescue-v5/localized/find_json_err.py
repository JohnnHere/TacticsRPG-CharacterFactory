import json
p = r"characters/orc-v1/source/combat-rescue-v5/localized/patch-manifest.json"
with open(p, "r", encoding="utf-8") as f:
    data = f.read()
try:
    json.loads(data)
    print("JSON VALID")
except json.JSONDecodeError as e:
    print("ERROR:", e)
    print("  at line", e.lineno, "col", e.colno, "pos", e.pos)
    lines = data.split("\n")
    # show context around error
    start = max(0, e.lineno - 3)
    end = min(len(lines), e.lineno + 2)
    for i in range(start, end):
        prefix = ">>> " if i == e.lineno - 1 else "    "
        print(f"{prefix}{i+1}: {lines[i]}")
