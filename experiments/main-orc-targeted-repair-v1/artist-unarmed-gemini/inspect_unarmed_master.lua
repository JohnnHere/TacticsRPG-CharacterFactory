-- inspect_unarmed_master.lua
local src = app.params["src"]
if not src then
  print("No src provided")
  return
end
local spr = app.open(src)
if not spr then
  print("Could not open: " .. tostring(src))
  return
end

print("=== SPRITE INFO: " .. tostring(src) .. " ===")
print("Dimensions: " .. spr.width .. "x" .. spr.height)
print("Frames count: " .. #spr.frames)
for i, fr in ipairs(spr.frames) do
  print("  Frame " .. i .. " duration: " .. fr.duration)
end
for i, l in ipairs(spr.layers) do
  print("Layer " .. i .. ": name='" .. l.name .. "' isImage=" .. tostring(l.isImage) .. " isVisible=" .. tostring(l.isVisible))
  for f, cel in ipairs(l.cels) do
    local pos = cel.position
    local img = cel.image
    print("  Cel frame=" .. cel.frameNumber .. " pos=(" .. pos.x .. "," .. pos.y .. ") img=(" .. img.width .. "x" .. img.height .. ")")
  end
end
spr:close()
