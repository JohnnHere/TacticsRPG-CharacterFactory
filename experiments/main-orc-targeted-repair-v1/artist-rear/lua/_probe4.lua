local root = app.fs.currentPath
local spr = app.open(app.fs.joinPath(root, "characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_r/sword-attack-representative-v2.aseprite"))
print("frames=" .. #spr.frames)
for i = 1, #spr.frames do
  local fr = spr.frames[i]
  print(string.format("f%d dur=%.1f", i, fr.duration))
end
print("layers=" .. #spr.layers)
for _, l in ipairs(spr.layers) do print("layer=" .. l.name) end
print("done")
