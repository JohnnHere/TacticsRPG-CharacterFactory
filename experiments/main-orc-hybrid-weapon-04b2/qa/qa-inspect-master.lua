-- QA read-only inspection of Pilot B2 Aseprite masters (no edits, no saves).
local outPath = app.params["qaout"]
if not outPath then error("missing --script-param qaout=<absolute path>") end
local files = {
  { "sourceMaster", "characters/orc-v1/source/combat-recovery-v8/rear-arc/back_r-sword/source/composite.aseprite" },
  { "fullA", "experiments/main-orc-hybrid-weapon-04b2/full/a/composite.aseprite" },
  { "fullB", "experiments/main-orc-hybrid-weapon-04b2/full/b/composite.aseprite" },
}
local parts = {}
for _, e in ipairs(files) do
  local spr = app.open(e[2])
  if not spr then error("cannot open " .. e[2]) end
  local layerNames = {}
  local celCounts = {}
  for _, lyr in ipairs(spr.layers) do
    table.insert(layerNames, '"' .. lyr.name .. '"')
    local n = 0
    for i = 1, #spr.frames do
      local cel = lyr:cel(i)
      if cel and cel.image then n = n + 1 end
    end
    celCounts[lyr.name] = n
  end
  local durs = {}
  for i = 1, #spr.frames do
    table.insert(durs, math.floor(spr.frames[i].duration * 1000 + 0.5))
  end
  local cc = {}
  for k, v in pairs(celCounts) do table.insert(cc, '"' .. k .. '": ' .. v) end
  table.sort(cc)
  table.insert(parts, string.format(
    '  "%s": { "path": "%s", "canvas": [%d, %d], "frames": %d, "layersInOrder": [%s], "frameDurationsMs": [%s], "celsPerLayer": { %s } }',
    e[1], (e[2]:gsub("\\", "/")), spr.width, spr.height, #spr.frames,
    table.concat(layerNames, ", "), table.concat(durs, ", "), table.concat(cc, ", ")))
  spr:close()
end
local f = io.open(outPath, "w")
f:write("{\n" .. table.concat(parts, ",\n") .. "\n}\n")
f:close()
print("written " .. outPath)
