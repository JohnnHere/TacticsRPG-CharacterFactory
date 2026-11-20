local p = app.fs.joinPath(app.fs.currentPath, 'characters/orc-v1/source/aseprite/complete-v1/composite/back_r/sword-attack.aseprite')
local s = Sprite{ fromFile = p }
print("=== Cels in complete-v1 back_r sword-attack.aseprite ===")
for fi = 1, #s.frames do
  local info = {}
  for li, lay in ipairs(s.layers) do
    local cel = lay:cel(fi)
    if cel and cel.image then
      table.insert(info, string.format("%s (pos=[%d,%d], size=[%d,%d])", lay.name, cel.bounds.x, cel.bounds.y, cel.bounds.width, cel.bounds.height))
    end
  end
  print(string.format("Frame %02d: %s", fi - 1, table.concat(info, " | ")))
end
s:close()
