p = r"characters/orc-v1/source/combat-rescue-v5/localized/patch-manifest.json"
with open(p, "r", encoding="utf-8") as f:
    data = f.read()
# Count brackets outside strings is complex; simpler: show char around pos 6356
print("char 6356 context:")
print(repr(data[6340:6380]))
print("\nLine 90 (index 89):")
lines = data.split("\n")
print(repr(lines[89]))
print("\nBrace/bracket counts:")
for ch in ['{','}','[',']']:
    print(f"  {ch}: {data.count(ch)}")
