import json, os

ROOT = r"C:\Users\João Orlando\Documents\Projetos Unity\TacticsRPG-CharacterFactory"
os.chdir(ROOT)

with open("experiments/main-orc-combat-rescue-v5/localized/backl_walk_arm_fixlist.json") as f:
    data = json.load(f)

fixes = data["fixes"]
by_frame = {}
for fx in fixes:
    by_frame.setdefault(fx["fix_frame"], []).append({
        "x": fx["x"] - 64,
        "y": fx["y"] - 64,
        "rgba": fx["new"],
    })

# Build fix_by_index table text
idx_lines = []
for fi in sorted(by_frame.keys()):
    items = []
    for fx in by_frame[fi]:
        r, g, b, a = fx["rgba"]
        items.append("{%d,%d,%d,%d,%d,%d}" % (fx["x"], fx["y"], r, g, b, a))
    idx_lines.append("  [%d] = {%s}" % (fi, ",".join(items)))
fix_table = "fix_by_index = {\n" + ",\n".join(idx_lines) + "\n}\n"

lua = '''local app = app
local sprite = app.open("characters/orc-v1/source/combat-rescue-v5/localized/walk-back_l-fixed.aseprite")
if not sprite then
  print("FAILED to open walk-back_l-fixed.aseprite")
  return
end
local layer = sprite.layers[1]
print("Layer:", layer.name)
''' + fix_table + '''
local fixed = 0
local skipped = 0
local fi = 0
for _, frame in ipairs(sprite.frames) do
  local flist = fix_by_index[fi]
  if flist then
    local cel = layer:cel(frame)
    if cel and cel.image then
      local img = cel.image
      for _, fx in ipairs(flist) do
        local x = fx[1]
        local y = fx[2]
        local c = Color(fx[3], fx[4], fx[5], fx[6])
        if x >= 0 and x < 128 and y >= 0 and y < 128 then
          img:putPixel(x, y, c)
          fixed = fixed + 1
        else
          skipped = skipped + 1
        end
      end
    end
  end
  fi = fi + 1
end
print(string.format("Applied %d fixes, skipped %d", fixed, skipped))
sprite:saveAs("characters/orc-v1/source/combat-rescue-v5/localized/walk-back_l-fixed.aseprite")
print("Saved master")
local outdir = "characters/orc-v1/source/combat-rescue-v5/localized/frames"
os.execute("mkdir " .. outdir)
fi = 0
for _, frame in ipairs(sprite.frames) do
  local cel = layer:cel(frame)
  if cel and cel.image then
    local sheet = Image(sprite.width, sprite.height)
    sheet:clear()
    for _, l in ipairs(sprite.layers) do
      if l.isVisible then
        local c = l:cel(frame)
        if c and c.image then
          sheet:drawImage(c.image, c.position.x, c.position.y)
        end
      end
    end
    sheet:saveAs(outdir .. "/f" .. string.format("%02d", fi) .. ".png")
  end
  fi = fi + 1
end
print("Exported frames")
'''

with open("experiments/main-orc-combat-rescue-v5/localized/apply_backl_fix.lua", "w") as f:
    f.write(lua)
print(f"Wrote apply_backl_fix.lua, total fixes = {sum(len(v) for v in by_frame.values())}")
