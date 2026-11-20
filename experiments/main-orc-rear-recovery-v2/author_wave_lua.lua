-- Aseprite Lua authoring script for main-orc-rear-recovery-v2
-- Authors back_l Walk (8f loop, 1280ms) and back_r Unarmed (9f one-shot with terminal neutral, 580ms)
-- Executed strictly inside Aseprite batch runner

local root = app.fs.currentPath
local function file(p) return app.fs.joinPath(root, p) end

print("=== Starting Aseprite Wave Authoring ===")

--------------------------------------------------------------------------------
-- 1. AUTHOR back_l Walk
--------------------------------------------------------------------------------
local walkL_rawDir = file("experiments/main-orc-rear-recovery-v2/raw/frames_walk_l")
local walkL_candDir = file("characters/orc-v1/source/rear-recovery-v2/back_l/Walk")
local walkL_natMaster = file("characters/orc-v1/source/aseprite/rear-recovery-v2/native/walk-back_l.aseprite")
local walkL_compMaster = file("characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_l/walk-unarmed.aseprite")

app.fs.makeAllDirectories(walkL_candDir)
app.fs.makeAllDirectories(app.fs.filePath(walkL_natMaster))
app.fs.makeAllDirectories(app.fs.filePath(walkL_compMaster))

-- Load 8 frames (0..7, trimming frame 8 duplicate loop anchor)
local walkL_numFrames = 8
local walkL_natFrames = {}
local walkL_compFrames = {}
local walkL_dy = { 1, 1, 1, 1, 1, 1, 1, 1 } -- raw bottom is 125, dy=+1 brings supporting foot to 126

for i = 1, walkL_numFrames do
  local p = app.fs.joinPath(walkL_rawDir, string.format("frame_%02d.png", i - 1))
  local src = Image{ fromFile = p }
  if not src then error("Could not load: " .. p) end
  
  -- Native 128x128
  local natImg = Image(128, 128, ColorMode.RGB)
  natImg:clear()
  natImg:drawImage(src, Point(0, walkL_dy[i]))
  walkL_natFrames[i] = natImg
  
  local expNatPath = file(string.format("experiments/main-orc-rear-recovery-v2/walk_back_l_%02d.png", i - 1))
  natImg:saveAs(expNatPath)
  
  -- Composite 256x256 (offset +64, +64)
  local compImg = Image(256, 256, ColorMode.RGB)
  compImg:clear()
  compImg:drawImage(natImg, Point(64, 64))
  walkL_compFrames[i] = compImg
  
  local compPngPath = app.fs.joinPath(walkL_candDir, string.format("%02d.png", i - 1))
  compImg:saveAs(compPngPath)
end

-- Save native strip
local walkL_strip = Image(128 * walkL_numFrames, 128, ColorMode.RGB)
walkL_strip:clear()
for i = 1, walkL_numFrames do
  walkL_strip:drawImage(walkL_natFrames[i], Point((i - 1) * 128, 0))
end
walkL_strip:saveAs(app.fs.joinPath(walkL_candDir, "native-strip.png"))
walkL_strip:saveAs(file("experiments/main-orc-rear-recovery-v2/native-strip-walk-back_l.png"))

-- Native Master .aseprite
local s_walkL_nat = Sprite(128, 128, ColorMode.RGB)
s_walkL_nat.layers[1].name = "Walk_back_l"
for i = 1, walkL_numFrames do
  if i > 1 then s_walkL_nat:newEmptyFrame() end
  s_walkL_nat:newCel(s_walkL_nat.layers[1], i, walkL_natFrames[i], Point(0, 0))
  s_walkL_nat.frames[i].duration = 0.16 -- 160ms each
end
s_walkL_nat:newTag(1, walkL_numFrames).name = "Walk"
s_walkL_nat:saveAs(walkL_natMaster)
s_walkL_nat:close()
print("Saved back_l Walk native master: " .. walkL_natMaster)

-- Composite Master .aseprite
local s_walkL_comp = Sprite(256, 256, ColorMode.RGB)
s_walkL_comp.layers[1].name = "Unarmed body"
for i = 1, walkL_numFrames do
  if i > 1 then s_walkL_comp:newEmptyFrame() end
  s_walkL_comp:newCel(s_walkL_comp.layers[1], i, walkL_compFrames[i], Point(0, 0))
  s_walkL_comp.frames[i].duration = 0.16
end
s_walkL_comp:newTag(1, walkL_numFrames).name = "Walk"
s_walkL_comp:saveAs(walkL_compMaster)
s_walkL_comp:close()
print("Saved back_l Walk composite master: " .. walkL_compMaster)

--------------------------------------------------------------------------------
-- 2. AUTHOR back_r Unarmed Attack
--------------------------------------------------------------------------------
local unarmR_rawDir = file("experiments/main-orc-rear-recovery-v2/raw/frames_unarmed_r")
local unarmR_candDir = file("characters/orc-v1/source/rear-recovery-v2/back_r/Unarmed")
local unarmR_natMaster = file("characters/orc-v1/source/aseprite/rear-recovery-v2/native/unarmed-back_r.aseprite")
local unarmR_compMaster = file("characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_r/unarmed-attack.aseprite")

app.fs.makeAllDirectories(unarmR_candDir)
app.fs.makeAllDirectories(app.fs.filePath(unarmR_natMaster))
app.fs.makeAllDirectories(app.fs.filePath(unarmR_compMaster))

-- All 9 frames preserved for one-shot action with terminal neutral rest
local unarmR_numFrames = 9
local unarmR_durationsSec = { 0.04, 0.06, 0.06, 0.05, 0.05, 0.08, 0.06, 0.08, 0.10 } -- 580 ms total
local unarmR_natFrames = {}
local unarmR_compFrames = {}
local unarmR_dy = { 1, 1, 1, 1, 1, 2, 1, 1, 1 } -- dy to bring planted foot to 126

for i = 1, unarmR_numFrames do
  local p = app.fs.joinPath(unarmR_rawDir, string.format("frame_%02d.png", i - 1))
  local src = Image{ fromFile = p }
  if not src then error("Could not load: " .. p) end
  
  -- Native 128x128
  local natImg = Image(128, 128, ColorMode.RGB)
  natImg:clear()
  natImg:drawImage(src, Point(0, unarmR_dy[i]))
  unarmR_natFrames[i] = natImg
  
  local expNatPath = file(string.format("experiments/main-orc-rear-recovery-v2/unarmed_back_r_%02d.png", i - 1))
  natImg:saveAs(expNatPath)
  
  -- Composite 256x256 (offset +64, +64)
  local compImg = Image(256, 256, ColorMode.RGB)
  compImg:clear()
  compImg:drawImage(natImg, Point(64, 64))
  unarmR_compFrames[i] = compImg
  
  local compPngPath = app.fs.joinPath(unarmR_candDir, string.format("%02d.png", i - 1))
  compImg:saveAs(compPngPath)
end

-- Save native strip
local unarmR_strip = Image(128 * unarmR_numFrames, 128, ColorMode.RGB)
unarmR_strip:clear()
for i = 1, unarmR_numFrames do
  unarmR_strip:drawImage(unarmR_natFrames[i], Point((i - 1) * 128, 0))
end
unarmR_strip:saveAs(app.fs.joinPath(unarmR_candDir, "native-strip.png"))
unarmR_strip:saveAs(file("experiments/main-orc-rear-recovery-v2/native-strip-unarmed-back_r.png"))

-- Native Master .aseprite
local s_unarmR_nat = Sprite(128, 128, ColorMode.RGB)
s_unarmR_nat.layers[1].name = "Unarmed_back_r"
for i = 1, unarmR_numFrames do
  if i > 1 then s_unarmR_nat:newEmptyFrame() end
  s_unarmR_nat:newCel(s_unarmR_nat.layers[1], i, unarmR_natFrames[i], Point(0, 0))
  s_unarmR_nat.frames[i].duration = unarmR_durationsSec[i]
end
s_unarmR_nat:newTag(1, unarmR_numFrames).name = "Attack"
s_unarmR_nat:saveAs(unarmR_natMaster)
s_unarmR_nat:close()
print("Saved back_r Unarmed native master: " .. unarmR_natMaster)

-- Composite Master .aseprite
local s_unarmR_comp = Sprite(256, 256, ColorMode.RGB)
s_unarmR_comp.layers[1].name = "Unarmed body"
for i = 1, unarmR_numFrames do
  if i > 1 then s_unarmR_comp:newEmptyFrame() end
  s_unarmR_comp:newCel(s_unarmR_comp.layers[1], i, unarmR_compFrames[i], Point(0, 0))
  s_unarmR_comp.frames[i].duration = unarmR_durationsSec[i]
end
s_unarmR_comp:newTag(1, unarmR_numFrames).name = "Attack"
s_unarmR_comp:saveAs(unarmR_compMaster)
s_unarmR_comp:close()
print("Saved back_r Unarmed composite master: " .. unarmR_compMaster)

print("=== Aseprite Wave Authoring Complete ===")
