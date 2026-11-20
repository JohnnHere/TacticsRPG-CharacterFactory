-- Aseprite Lua authoring script for front_r and front_l Defeat
local root = app.fs.currentPath
local function file(p) return app.fs.joinPath(root, p) end

print("=== Authoring front_r and front_l Defeat Masters ===")

local durations = { 0.07, 0.095, 0.115, 0.13, 0.29 }
local phases = { "fatal-stagger", "knees-buckle", "drop-to-knees", "collapse-impact", "terminal-defeated" }

for _, d in ipairs({ "front_r", "front_l" }) do
  local candDir = file(string.format("characters/orc-v1/source/rear-recovery-v2/%s/Defeat", d))
  local natMaster = file(string.format("characters/orc-v1/source/aseprite/rear-recovery-v2/native/defeat-%s.aseprite", d))
  local compMaster = file(string.format("characters/orc-v1/source/aseprite/rear-recovery-v2/composite/%s/defeat.aseprite", d))
  
  app.fs.makeAllDirectories(candDir)
  app.fs.makeAllDirectories(app.fs.filePath(natMaster))
  app.fs.makeAllDirectories(app.fs.filePath(compMaster))
  
  local cand_native = file(string.format("experiments/main-orc-rear-recovery-v2/raw/defeat_%s_04_candidate.png", d))
  local newTermImg = Image{ fromFile = cand_native }
  
  local natFrames = {}
  local compFrames = {}
  
  -- Frames 0..3 from complete-v1
  for i = 1, 4 do
    local p = file(string.format("characters/orc-v1/source/complete-v1/%s/Defeat/%02d.png", d, i - 1))
    local compImg = Image{ fromFile = p }
    compFrames[i] = compImg
    
    -- Native 128x128 cropped from composite center
    local natImg = Image(128, 128, ColorMode.RGB)
    natImg:clear()
    natImg:drawImage(compImg, Point(-64, -64))
    natFrames[i] = natImg
    
    compImg:saveAs(app.fs.joinPath(candDir, string.format("%02d.png", i - 1)))
  end
  
  -- Frame 4 (idx 4): new terminal ground collapse
  natFrames[5] = newTermImg
  local compTerm = Image(256, 256, ColorMode.RGB)
  compTerm:clear()
  compTerm:drawImage(newTermImg, Point(64, 64))
  compFrames[5] = compTerm
  compTerm:saveAs(app.fs.joinPath(candDir, "04.png"))
  
  -- Native strip (640 x 128)
  local strip = Image(128 * 5, 128, ColorMode.RGB)
  strip:clear()
  for i = 1, 5 do
    strip:drawImage(natFrames[i], Point((i - 1) * 128, 0))
  end
  strip:saveAs(app.fs.joinPath(candDir, "native-strip.png"))
  
  -- Native Master
  local s_nat = Sprite(128, 128, ColorMode.RGB)
  s_nat.layers[1].name = "Defeat_" .. d
  for i = 1, 5 do
    if i > 1 then s_nat:newEmptyFrame() end
    s_nat:newCel(s_nat.layers[1], i, natFrames[i], Point(0, 0))
    s_nat.frames[i].duration = durations[i]
  end
  s_nat:newTag(1, 5).name = "Defeat"
  s_nat:saveAs(natMaster)
  s_nat:close()
  print("Saved native master: " .. natMaster)
  
  -- Composite Master
  local s_comp = Sprite(256, 256, ColorMode.RGB)
  s_comp.layers[1].name = "Defeat body"
  for i = 1, 5 do
    if i > 1 then s_comp:newEmptyFrame() end
    s_comp:newCel(s_comp.layers[1], i, compFrames[i], Point(0, 0))
    s_comp.frames[i].duration = durations[i]
  end
  s_comp:newTag(1, 5).name = "Defeat"
  s_comp:saveAs(compMaster)
  s_comp:close()
  print("Saved composite master: " .. compMaster)
end

print("=== Defeat Authoring Complete ===")
