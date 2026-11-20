-- Synchronize front Walk F08 across composite, native, strip, and Aseprite masters
local root = app.fs.currentPath
local function file(p) return app.fs.joinPath(root, p) end

print("=== Synchronizing Front Walk F08 ===")

local function blank(w, h)
  local im = Image(w, h, ColorMode.RGB)
  im:clear()
  return im
end

for _, d in ipairs({ "front_r", "front_l" }) do
  local candDir = file("characters/orc-v1/source/complete-v1/" .. d .. "/Walk")
  local compMaster = "characters/orc-v1/source/aseprite/complete-v1/composite/" .. d .. "/walk.aseprite"
  local natMaster = "characters/orc-v1/source/aseprite/complete-v1/native/walk-" .. d .. ".aseprite"
  
  -- Load all 16 frames
  local compFrames, natFrames = {}, {}
  for fi = 1, 16 do
    local cPath = app.fs.joinPath(candDir, string.format("%02d.png", fi - 1))
    local comp = Image{ fromFile = cPath }
    local nat = blank(128, 128)
    nat:drawImage(comp, Point(-64, -64))
    compFrames[fi] = comp
    natFrames[fi] = nat
  end
  
  -- Frame 8 native is walk_front_<dir>_08.png
  local natPngPath = file("characters/orc-v1/sprites/Animations/Walk/walk_" .. d .. "_08.png")
  natFrames[9]:saveAs(natPngPath)
  
  -- Update native strip
  local strip = blank(128 * 16, 128)
  for fi = 1, 16 do
    strip:drawImage(natFrames[fi], Point((fi - 1) * 128, 0))
  end
  strip:saveAs(app.fs.joinPath(candDir, "native-strip.png"))
  
  -- Update masters
  if app.fs.isFile(file(compMaster)) then
    local sc = Sprite{ fromFile = file(compMaster) }
    sc.layers[1]:cel(9).image:clear()
    sc.layers[1]:cel(9).image:drawImage(compFrames[9], Point(0, 0))
    sc:saveAs(file(compMaster))
    sc:close()
  end
  
  if app.fs.isFile(file(natMaster)) then
    local sn = Sprite{ fromFile = file(natMaster) }
    sn.layers[1]:cel(9).image:clear()
    sn.layers[1]:cel(9).image:drawImage(natFrames[9], Point(0, 0))
    sn:saveAs(file(natMaster))
    sn:close()
  end
  
  print("Synchronized " .. d .. " Walk F08.")
end

print("Front Walk F08 synchronized completely.")
