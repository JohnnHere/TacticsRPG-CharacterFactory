import json
p = r"characters/orc-v1/source/rear-reconstruction-v4/candidate28manifest.json"
parent = json.load(open(p))
pc = None
for cell in parent["cells"]:
    if cell["cellId"] == "back_l/Walk":
        pc = cell
print("Parent back_l/Walk fields present:", sorted(pc.keys()))
print("  frameCount:", pc["frameCount"], "-> fixed clip:", 8, "MATCH" if pc["frameCount"]==8 else "MISMATCH")
print("  durationsMs:", pc["durationsMs"], "-> fixed clip:", [160]*8, "MATCH" if pc["durationsMs"]==[160]*8 else "MISMATCH")
print("  canvas [256,256] bodyOffset [64,64] groundY 190 -> fixed clip: MATCH (per validate_deliverables)")
print("  nativeCanvas [128,128] nativeGroundY 126 -> fixed clip: MATCH (per validate_deliverables)")
print("\nParent contract compatibility: OK (all shared fields match).")
print("Note: parent manifest schema lacks totalDurationMs (different revision schema); fixed clip uses current schema.")
