-- Aseprite Lua authoring script for main-orc-rear-recovery-v2 back_r Walk
-- Runs strictly inside Aseprite batch mode via executeAseprite

local root = app.fs.currentPath
local function file(p) return app.fs.joinPath(root, p) end

print("=== Starting Aseprite Lua Walk Authoring ===")

local rawFramesDir = file("experiments/main-orc-rear-recovery-v2/raw/frames")
local candDir = file("characters/orc-v1/source/rear-recovery-v2/back_r/Walk")
local natMasterPath = file("characters/orc-v1/source/aseprite/rear-recovery-v2/native/walk-back_r.aseprite")
local compMasterPath = file("characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_r/walk-unarmed.aseprite")

app.fs.makeAllDirectories(candDir)
app.fs.makeAllDirectories(app.fs.filePath(natMasterPath))
app.fs.makeAllDirectories(app.fs.filePath(compMasterPath))

-- Load 8 frames (indices 0 to 7 of the continuous animation)
local numFrames = 8
local rawImages = {}

for i = 0, numFrames - 1 do
  local p = app.fs.joinPath(rawFramesDir, string.format("frame_%02d.png", i))
  local img = Image{ fromFile = p }
  if not img then error("Failed to load: " .. p) end
  rawImages[i + 1] = img
end

-- Ground registration: measure supporting foot bottom for each frame
-- Native target groundY = 126
local nativeFrames = {}
local compFrames = {}
local groundOffsets = { 1, 1, 1, 0, 0, 0, 2, 2 } -- dy to bring supporting foot to 126

for i = 1, numFrames do
  local src = rawImages[i]
  local dy = groundOffsets[i] or 0
  
  -- 1. Native 128x128
  local natImg = Image(128, 128, ColorMode.RGB)
  natImg:clear()
  natImg:drawImage(src, Point(0, dy))
  nativeFrames[i] = natImg
  
  -- Save candidate native PNG
  local natPngPath = app.fs.joinPath(candDir, string.format("walk_back_r_%02d.png", i - 1))
  -- Also save into experiment directory for visual inspection
  local expNatPath = file(string.format("experiments/main-orc-rear-recovery-v2/walk_back_r_%02d.png", i - 1))
  natImg:saveAs(expNatPath)
  
  -- 2. Composite 256x256 (offset +64, +64, ground at 190)
  local compImg = Image(256, 256, ColorMode.RGB)
  compImg:clear()
  compImg:drawImage(natImg, Point(64, 64))
  compFrames[i] = compImg
  
  local compPngPath = app.fs.joinPath(candDir, string.format("%02d.png", i - 1))
  compImg:saveAs(compPngPath)
end

-- 3. Save Native Strip (128 * 8 x 128 = 1024 x 128)
local strip = Image(128 * numFrames, 128, ColorMode.RGB)
strip:clear()
for i = 1, numFrames do
  strip:drawImage(nativeFrames[i], Point((i - 1) * 128, 0))
end
local stripPath = app.fs.joinPath(candDir, "native-strip.png")
strip:saveAs(stripPath)
local expStripPath = file("experiments/main-orc-rear-recovery-v2/native-strip.png")
strip:saveAs(expStripPath)

-- 4. Build Native Aseprite Master
local natSprite = Sprite(128, 128, ColorMode.RGB)
natSprite.layers[1].name = "Walk_back_r"
for i = 1, numFrames do
  if i > 1 then natSprite:newEmptyFrame() end
  natSprite:newCel(natSprite.layers[1], i, nativeFrames[i], Point(0, 0))
  natSprite.frames[i].duration = 0.16 -- 160 ms per frame = 1280 ms total
end
natSprite:newTag(1, numFrames).name = "Walk"
natSprite:saveAs(natMasterPath)
natSprite:close()
print("Saved native master: " .. natMasterPath)

-- 5. Build Composite Aseprite Master
local compSprite = Sprite(256, 256, ColorMode.RGB)
compSprite.layers[1].name = "Unarmed body"
for i = 1, numFrames do
  if i > 1 then compSprite:newEmptyFrame() end
  compSprite:newCel(compSprite.layers[1], i, compFrames[i], Point(0, 0))
  compSprite.frames[i].duration = 0.16 -- 160 ms per frame = 1280 ms total
end
compSprite:newTag(1, numFrames).name = "Walk"
compSprite:saveAs(compMasterPath)
compSprite:close()
print("Saved composite master: " .. compMasterPath)

print("=== Aseprite Lua Walk Authoring Complete ===")
