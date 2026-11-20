-- Aseprite Lua authoring script for back_r Unarmed
-- Authors 5-frame sequence matching complete-v1 phases
local root = app.fs.currentPath
local function file(p) return app.fs.joinPath(root, p) end

print("=== Authoring back_r Unarmed Master ===")

local rawDir = file("experiments/main-orc-rear-recovery-v2/raw")
local framesDir = app.fs.joinPath(rawDir, "frames_unarmed_r")
local candDir = file("characters/orc-v1/source/rear-recovery-v2/back_r/Unarmed")
local natMaster = file("characters/orc-v1/source/aseprite/rear-recovery-v2/native/unarmed-back_r.aseprite")
local compMaster = file("characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_r/unarmed-attack.aseprite")

app.fs.makeAllDirectories(candDir)
app.fs.makeAllDirectories(app.fs.filePath(natMaster))
app.fs.makeAllDirectories(app.fs.filePath(compMaster))

local baseImg = Image{ fromFile = app.fs.joinPath(framesDir, "frame_00.png") }
local f03Img = Image{ fromFile = app.fs.joinPath(framesDir, "frame_03.png") }
local impactImg = Image{ fromFile = app.fs.joinPath(rawDir, "punch_impact_key_back_r.png") }
local f05Img = Image{ fromFile = app.fs.joinPath(framesDir, "frame_05.png") }
local f07Img = Image{ fromFile = app.fs.joinPath(framesDir, "frame_07.png") }

-- Clean impact image: dy=+1 to pin ground at 126, preserve cranium outline/nape from base
local cleanImpact = Image(128, 128, ColorMode.RGB)
cleanImpact:clear()
cleanImpact:drawImage(impactImg, Point(0, 1))

for y = 6, 20 do
  for x = 55, 76 do
    local pb = baseImg:getPixel(x, y)
    local a = app.pixelColor.rgbaA(pb)
    if a > 10 then
      cleanImpact:drawPixel(x, y + 1, pb)
    end
  end
end

local numFrames = 5
local frameDefs = {
  { img = baseImg, dy = 1, dur = 0.08, phase = "guard-prep" },
  { img = f03Img, dy = 1, dur = 0.11, phase = "shoulder-coil" },
  { img = cleanImpact, dy = 0, dur = 0.06, phase = "heavy-gauntlet-impact" },
  { img = f05Img, dy = 2, dur = 0.09, phase = "follow-through" },
  { img = f07Img, dy = 1, dur = 0.11, phase = "recovery-settle" }
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
  
  -- Save individual native frame for inspect
  natImg:saveAs(file(string.format("experiments/main-orc-rear-recovery-v2/cand_unarmed_back_r_%02d.png", i - 1)))
  
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
strip:saveAs(file("experiments/main-orc-rear-recovery-v2/native-strip-unarmed-back_r.png"))

-- Native Master .aseprite
local s_nat = Sprite(128, 128, ColorMode.RGB)
s_nat.layers[1].name = "Unarmed_back_r"
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

print("=== back_r Unarmed Authoring Complete ===")
