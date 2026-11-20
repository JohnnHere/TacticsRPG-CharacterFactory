local logFile = io.open("tmp/aseprite_master_log.txt", "w")
local function log(msg)
  if logFile then
    logFile:write(msg .. "\n")
    logFile:flush()
  end
end

log("Starting create_walk_masters.lua")
local root = app.fs.currentPath
local function file(p) return app.fs.joinPath(root, p) end

local function saveAseprite(pngPaths, durationSec, tagName, masterPath, layerName)
  log("Processing " .. masterPath)
  local frames = {}
  for i, p in ipairs(pngPaths) do
    local fullPath = file(p)
    local img = Image{ fromFile = fullPath }
    if not img then
      log("ERROR: could not load " .. fullPath)
      error("Could not load " .. fullPath)
    end
    frames[i] = img
  end
  local w, h = frames[1].width, frames[1].height
  local s = Sprite(w, h, ColorMode.RGB)
  s.layers[1].name = layerName or tagName
  for i, im in ipairs(frames) do
    if i > 1 then s:newEmptyFrame() end
    s:newCel(s.layers[1], i, im, Point(0, 0))
    s.frames[i].duration = durationSec
  end
  s:newTag(1, #frames).name = tagName
  local fullMaster = file(masterPath)
  app.fs.makeAllDirectories(app.fs.filePath(fullMaster))
  s:saveAs(fullMaster)
  s:close()
  log("Successfully saved " .. fullMaster)
end

-- 1. Native 128x128 master
local nativePaths = {}
for i = 0, 15 do
  nativePaths[i + 1] = string.format("experiments/main-orc-rear-recovery-v2/walk_back_r_%02d.png", i)
end
saveAseprite(nativePaths, 0.08, "Walk", "characters/orc-v1/source/aseprite/rear-recovery-v2/native/walk-back_r.aseprite", "Walk_back_r")

-- 2. Composite 256x256 master
local compPaths = {}
for i = 0, 15 do
  compPaths[i + 1] = string.format("characters/orc-v1/source/rear-recovery-v2/back_r/Walk/%02d.png", i)
end
saveAseprite(compPaths, 0.08, "Walk", "characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_r/walk-unarmed.aseprite", "Unarmed body")

log("Finished create_walk_masters.lua")
if logFile then logFile:close() end
