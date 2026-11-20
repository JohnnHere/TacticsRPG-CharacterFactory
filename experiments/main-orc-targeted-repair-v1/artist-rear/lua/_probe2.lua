local root = app.fs.currentPath
local p = app.fs.joinPath(root, "characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_r/sword-attack-representative-v2.aseprite")
print("exists=" .. tostring(app.fs.fileExists and app.fs.fileExists(p)))
local spr = app.open(p)
print("opened " .. tostring(spr))
if spr then
  print("size " .. spr.width .. "x" .. spr.height .. " frames=" .. #spr.frames)
  for i, fr in ipairs(spr.frames) do print(string.format("  f%d dur=%.1f cels=%d", i, fr.duration, #fr.cels)) end
  for _, l in ipairs(spr.layers) do print("  layer " .. l.name) end
  spr:close()
end
