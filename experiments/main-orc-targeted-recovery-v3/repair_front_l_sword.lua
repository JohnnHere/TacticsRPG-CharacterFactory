-- Repair front_l Sword Attack armpit defect in Aseprite
local root = app.fs.currentPath
local function file(p) return app.fs.joinPath(root, p) end

print("=== Repairing front_l Sword Attack in Aseprite ===")

local compMasterPath = file("characters/orc-v1/source/aseprite/complete-v1/composite/front_l/sword-attack.aseprite")
local bodyMasterPath = file("characters/orc-v1/source/aseprite/complete-v1/composite/front_l/sword-body.aseprite")
local clipDir = file("characters/orc-v1/source/complete-v1/front_l/Sword/Attack")

local compSprite = Sprite{ fromFile = compMasterPath }
if not compSprite then error("Could not open compSprite: " .. compMasterPath) end

local bodySprite = Sprite{ fromFile = bodyMasterPath }
if not bodySprite then error("Could not open bodySprite: " .. bodyMasterPath) end

local INK = app.pixelColor.rgba(12, 15, 18, 255)
local SHADOW = app.pixelColor.rgba(24, 26, 30, 255)
local CLEAR = app.pixelColor.rgba(0, 0, 0, 0)

-- Find body layer in compSprite and bodySprite
local compBodyLayer = nil
for _, l in ipairs(compSprite.layers) do
  if l.name == "body" then compBodyLayer = l break end
end

local bBodyLayer = bodySprite.layers[1]

-- 1. Frame 1 & 2: remove stray pixel at (166, 131)
for _, fNum in ipairs({ 2, 3 }) do -- 1-based index in Aseprite
  local celComp = compBodyLayer:cel(fNum)
  if celComp then
    celComp.image:drawPixel(166, 131, CLEAR)
  end
  local celB = bBodyLayer:cel(fNum)
  if celB then
    celB.image:drawPixel(166, 131, CLEAR)
  end
end

-- 2. Frame 3 (fNum = 4): armpit defect repair
-- Remove floating debris at (162, 92) and (163, 92)
local celComp4 = compBodyLayer:cel(4)
local celB4 = bBodyLayer:cel(4)

if celComp4 and celB4 then
  celComp4.image:drawPixel(162, 92, CLEAR)
  celComp4.image:drawPixel(163, 92, CLEAR)
  celB4.image:drawPixel(162, 92, CLEAR)
  celB4.image:drawPixel(163, 92, CLEAR)

  -- Smooth out the armpit contour notch at (156..161, 91..93)
  -- The torso connects at (155, 92), arm starts around (160, 93)
  -- Fill the notch smoothly with torso shadow and outline
  celComp4.image:drawPixel(156, 92, SHADOW)
  celComp4.image:drawPixel(157, 92, SHADOW)
  celComp4.image:drawPixel(158, 92, SHADOW)
  celComp4.image:drawPixel(159, 92, SHADOW)
  celComp4.image:drawPixel(156, 91, INK)
  celComp4.image:drawPixel(157, 91, INK)
  celComp4.image:drawPixel(158, 91, INK)
  celComp4.image:drawPixel(159, 91, INK)

  celB4.image:drawPixel(156, 92, SHADOW)
  celB4.image:drawPixel(157, 92, SHADOW)
  celB4.image:drawPixel(158, 92, SHADOW)
  celB4.image:drawPixel(159, 92, SHADOW)
  celB4.image:drawPixel(156, 91, INK)
  celB4.image:drawPixel(157, 91, INK)
  celB4.image:drawPixel(158, 91, INK)
  celB4.image:drawPixel(159, 91, INK)
end

-- Save masters
compSprite:saveAs(compMasterPath)
bodySprite:saveAs(bodyMasterPath)

-- Re-export the modified frames
for _, fNum in ipairs({ 2, 3, 4 }) do
  local fi = fNum - 1
  -- Render flattened composite frame
  local flat = Image(256, 256, ColorMode.RGB)
  flat:clear()
  for _, l in ipairs(compSprite.layers) do
    local cel = l:cel(fNum)
    if cel then flat:drawImage(cel.image, Point(0, 0)) end
  end
  flat:saveAs(app.fs.joinPath(clipDir, string.format("%02d.png", fi)))
  
  -- Save body layer frame
  local bCel = compBodyLayer:cel(fNum)
  if bCel then
    bCel.image:saveAs(app.fs.joinPath(clipDir, "layers/body", string.format("%02d.png", fi)))
  end
end

compSprite:close()
bodySprite:close()

print("front_l Sword Attack armpit repair complete.")
