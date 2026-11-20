-- Authoritative Aseprite Lua script to synchronize all Unarmed clips
-- front_r, front_l, back_r
-- Ensures:
-- 1. Exact crop(64,64,128,128) of composite saved to native/*.png and actions supplement
-- 2. Master sprite cels and frame duration headers match [80, 110, 50, 90, 120] ms
-- 3. native-strip.png is rebuilt from native frames

local root = app.fs.currentPath
local function file(p) return app.fs.joinPath(root, p) end

print("=== Synchronizing Unarmed Clips Across All Representations ===")

local durations = { 0.08, 0.11, 0.05, 0.09, 0.12 }

local function blank(w, h)
  local im = Image(w, h, ColorMode.RGB)
  im:clear()
  return im
end

local function saveSpr(path, w, names, fList)
  app.fs.makeAllDirectories(app.fs.filePath(file(path)))
  local s = Sprite(w, w, ColorMode.RGB)
  s.layers[1].name = names[1]
  for fi = 1, #fList do
    if fi > 1 then s:newEmptyFrame() end
    s:newCel(s.layers[1], fi, fList[fi], Point(0, 0))
    s.frames[fi].duration = durations[fi]
  end
  s:newTag(1, #fList).name = "Attack"
  s:saveAs(file(path))
  s:close()
end

for _, d in ipairs({ "front_r", "front_l", "back_r" }) do
  local candDir = file("characters/orc-v1/source/rear-recovery-v2/" .. d .. "/Unarmed")
  local natDir = candDir .. "/native"
  app.fs.makeAllDirectories(natDir)
  
  local compMaster = "characters/orc-v1/source/aseprite/rear-recovery-v2/composite/" .. d .. "/unarmed-attack.aseprite"
  local natMaster = "characters/orc-v1/source/aseprite/rear-recovery-v2/native/unarmed-" .. d .. ".aseprite"
  
  local compFrames, natFrames = {}, {}
  for fi = 1, 5 do
    local cPath = app.fs.joinPath(candDir, string.format("%02d.png", fi - 1))
    local comp = Image{ fromFile = cPath }
    local nat = blank(128, 128)
    nat:drawImage(comp, Point(-64, -64))
    
    compFrames[fi] = comp
    natFrames[fi] = nat
    
    nat:saveAs(app.fs.joinPath(natDir, string.format("%02d.png", fi - 1)))
    
    -- Also save to actions supplement if front direction
    if d == "front_r" or d == "front_l" then
      local suppDir = file("characters/orc-v1/source/actions/basic-unarmed/v1/" .. d)
      app.fs.makeAllDirectories(suppDir)
      nat:saveAs(app.fs.joinPath(suppDir, string.format("attack_%s_%02d.png", d, fi - 1)))
    end
  end
  
  -- Save native strip
  local strip = blank(128 * 5, 128)
  for fi = 1, 5 do
    strip:drawImage(natFrames[fi], Point((fi - 1) * 128, 0))
  end
  strip:saveAs(app.fs.joinPath(candDir, "native-strip.png"))
  
  -- Save masters
  saveSpr(compMaster, 256, { "body" }, compFrames)
  saveSpr(natMaster, 128, { "unarmed_" .. d }, natFrames)
  print("Synchronized " .. d .. " Unarmed masters, composite, native and strip.")
end

print("ALL Unarmed clips synchronized successfully.")
