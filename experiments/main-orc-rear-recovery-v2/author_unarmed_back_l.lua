-- Aseprite Lua authoring script for back_l Unarmed
-- Authors 5-frame sequence matching complete-v1 phases
local root = app.fs.currentPath
local function file(p) return app.fs.joinPath(root, p) end

print("=== Authoring back_l Unarmed Master ===")

local rawDir = file("experiments/main-orc-rear-recovery-v2/raw")
local candDir = file("characters/orc-v1/source/rear-recovery-v2/back_l/Unarmed")
local natMaster = file("characters/orc-v1/source/aseprite/rear-recovery-v2/native/unarmed-back_l.aseprite")
local compMaster = file("characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_l/unarmed-attack.aseprite")

app.fs.makeAllDirectories(candDir)
app.fs.makeAllDirectories(app.fs.filePath(natMaster))
app.fs.makeAllDirectories(app.fs.filePath(compMaster))

local baseImg = Image{ fromFile = file("experiments/main-orc-complete-v1/pixellab-recovery/back_l_base.png") }
local cleanImpact = Image{ fromFile = file("experiments/main-orc-rear-recovery-v2/punch_impact_clean_l.png") }

local f01Img_comp = Image{ fromFile = file("characters/orc-v1/source/complete-v1/back_l/Unarmed/01.png") }
local f03Img_comp = Image{ fromFile = file("characters/orc-v1/source/complete-v1/back_l/Unarmed/03.png") }
local f04Img_comp = Image{ fromFile = file("characters/orc-v1/source/complete-v1/back_l/Unarmed/04.png") }

local function crop128(srcComp)
  local im = Image(128, 128, ColorMode.RGB)
  im:clear()
  im:drawImage(srcComp, Point(-64, -64))
  return im
end

local f01Img = crop128(f01Img_comp)
local f03Img = crop128(f03Img_comp)
local f04Img = crop128(f04Img_comp)

local numFrames = 5
local frameDefs = {
  { img = baseImg, dy = 1, dur = 0.08, phase = "guard-prep" },
  { img = f01Img, dy = 0, dur = 0.11, phase = "shoulder-coil" },
  { img = cleanImpact, dy = 0, dur = 0.06, phase = "heavy-gauntlet-impact" },
  { img = f03Img, dy = 0, dur = 0.09, phase = "follow-through" },
  { img = f04Img, dy = 0, dur = 0.11, phase = "recovery-settle" }
}

local natFrames = {}
local compFrames = {}

for i = 1, numFrames do
  local def = frameDefs[i]
  
  -- Native 128x128
  local natImg = Image(128, 128, ColorMode.RGB)
  natImg:clear()
  natImg:drawImage(def.img, Point(0, def.dy))
  natFrames[i] = natImg
  
  natImg:saveAs(file(string.format("experiments/main-orc-rear-recovery-v2/cand_unarmed_back_l_%02d.png", i - 1)))
  
  -- Composite 256x256 (offset +64, +64)
  local compImg = Image(256, 256, ColorMode.RGB)
  compImg:clear()
  compImg:drawImage(natImg, Point(64, 64))
  compFrames[i] = compImg
  
  local compPath = app.fs.joinPath(candDir, string.format("%02d.png", i - 1))
  compImg:saveAs(compPath)
end

-- Save native horizontal strip (640 x 128)
local strip = Image(128 * numFrames, 128, ColorMode.RGB)
strip:clear()
for i = 1, numFrames do
  strip:drawImage(natFrames[i], Point((i - 1) * 128, 0))
end
strip:saveAs(app.fs.joinPath(candDir, "native-strip.png"))
strip:saveAs(file("experiments/main-orc-rear-recovery-v2/native-strip-unarmed-back_l.png"))

-- Native Master .aseprite
local s_nat = Sprite(128, 128, ColorMode.RGB)
s_nat.layers[1].name = "Unarmed_back_l"
for i = 1, numFrames do
  if i > 1 then s_nat:newEmptyFrame() end
  s_nat:newCel(s_nat.layers[1], i, natFrames[i], Point(0, 0))
  s_nat.frames[i].duration = frameDefs[i].dur
end
s_nat:newTag(1, numFrames).name = "Attack"
s_nat:saveAs(natMaster)
s_nat:close()
print("Saved native master: " .. natMaster)

-- Composite Master .aseprite
local s_comp = Sprite(256, 256, ColorMode.RGB)
s_comp.layers[1].name = "Unarmed body"
for i = 1, numFrames do
  if i > 1 then s_comp:newEmptyFrame() end
  s_comp:newCel(s_comp.layers[1], i, compFrames[i], Point(0, 0))
  s_comp.frames[i].duration = frameDefs[i].dur
end
s_comp:newTag(1, numFrames).name = "Attack"
s_comp:saveAs(compMaster)
s_comp:close()
print("Saved composite master: " .. compMaster)

print("=== back_l Unarmed Authoring Complete ===")
