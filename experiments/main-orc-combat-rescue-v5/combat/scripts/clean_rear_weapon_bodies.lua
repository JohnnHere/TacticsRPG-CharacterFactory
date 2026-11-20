-- Aseprite Lua script: Clean and export 4 Rear Weapon body sequences (back_r/Sword, back_r/Axe, back_l/Sword, back_l/Axe)
local ROOT = "C:/Users/João Orlando/Documents/Projetos Unity/TacticsRPG-CharacterFactory"
local RAW_ROOT = ROOT .. "/experiments/main-orc-combat-rescue-v5/combat/raw"
local CLEAN_ROOT = ROOT .. "/experiments/main-orc-combat-rescue-v5/combat/cleaned_rear_bodies"

app.fs.makeAllDirectories(CLEAN_ROOT)

local function cloneImage(src)
  local dst = Image(src.width, src.height, ColorMode.RGBA)
  dst:clear()
  dst:drawImage(src, Point(0, 0))
  return dst
end

local function getPx(im, x, y)
  if x < 0 or x >= im.width or y < 0 or y >= im.height then return 0 end
  return im:getPixel(x, y)
end

local function setPx(im, x, y, c)
  if x >= 0 and x < im.width and y >= 0 and y < im.height then
    im:drawPixel(x, y, c)
  end
end

local INK = app.pixelColor.rgba(12, 15, 18, 255)

-- Anchor off-hand on back_r (left arm, x <= 44..45, y <= 84) from F00 base so off-hand has 0 shift
local function anchorOffHandBackR(im, imBase)
  local out = cloneImage(im)
  for y = 10, 84 do
    local xMax = 45
    if y >= 50 and y <= 62 then
      xMax = 43
    elseif y >= 63 then
      xMax = 42
    end
    for x = 0, xMax do
      setPx(out, x, y, getPx(imBase, x, y))
    end
  end
  -- Clear any stray pixels left of left leg below y=85
  for y = 85, 127 do
    for x = 0, 22 do
      setPx(out, x, y, 0)
    end
  end
  return out
end

-- Anchor off-hand on back_l (right arm, x >= 82..84, y <= 84) from F00 base so off-hand has 0 shift
local function anchorOffHandBackL(im, imBase)
  local out = cloneImage(im)
  for y = 10, 84 do
    local xMin = 82
    if y >= 50 and y <= 62 then
      xMin = 84
    elseif y >= 63 then
      xMin = 85
    end
    for x = xMin, 127 do
      setPx(out, x, y, getPx(imBase, x, y))
    end
  end
  for y = 85, 127 do
    for x = 105, 127 do
      setPx(out, x, y, 0)
    end
  end
  return out
end

-- Shift a rectangular region (x0..x1, y0..y1) by (dx, dy) and enforce INK on any outer border
local function shiftRegion(im, x0, x1, y0, y1, dx, dy)
  local out = cloneImage(im)
  for y = y0, y1 do
    for x = x0, x1 do
      setPx(out, x, y, 0)
    end
  end
  for y = y0, y1 do
    for x = x0, x1 do
      local c = getPx(im, x, y)
      if app.pixelColor.rgbaA(c) > 0 then
        local xd = x + dx
        local yd = y + dy
        if xd >= x0 and xd <= x1 and yd >= y0 and yd <= y1 then
          setPx(out, xd, yd, c)
        end
      end
    end
  end
  -- Ensure any pixel at x=2, x=125, or y=2 has INK outline if exposed
  for y = y0, y1 do
    for x = x0, x1 do
      local c = getPx(out, x, y)
      if app.pixelColor.rgbaA(c) > 0 then
        if x == 2 or x == 125 or y == 2 then
          setPx(out, x, y, INK)
        end
      end
    end
  end
  return out
end

local baseR = Image{ fromFile = RAW_ROOT .. "/back_r_base_128.png" }
local baseL = Image{ fromFile = RAW_ROOT .. "/back_l_base_128.png" }

-- 1. back_r_sword_v1
do
  local dirOut = CLEAN_ROOT .. "/back_r_sword"
  app.fs.makeAllDirectories(dirOut)
  baseR:saveAs(dirOut .. "/00.png")
  for idx = 0, 6 do
    local im = Image{ fromFile = string.format("%s/back_r_sword_v1/%02d.png", RAW_ROOT, idx) }
    im = anchorOffHandBackR(im, baseR)
    if idx == 3 then
      -- F04 (raw 03): shift distal right fist (x=104..127, y=24..46) left by 2px so xmax <= 125
      im = shiftRegion(im, 104, 127, 24, 46, -2, 0)
    end
    im:saveAs(string.format("%s/%02d.png", dirOut, idx + 1))
  end
end

-- 2. back_r_axe_v1
do
  local dirOut = CLEAN_ROOT .. "/back_r_axe"
  app.fs.makeAllDirectories(dirOut)
  baseR:saveAs(dirOut .. "/00.png")
  for idx = 0, 6 do
    local im = Image{ fromFile = string.format("%s/back_r_axe_v1/%02d.png", RAW_ROOT, idx) }
    im = anchorOffHandBackR(im, baseR)
    if idx == 1 then
      -- F02 (raw 01): shift overhead right fist (x=80..104, y=0..18) down by 3px so ymin >= 3
      im = shiftRegion(im, 80, 104, 0, 18, 0, 3)
    end
    im:saveAs(string.format("%s/%02d.png", dirOut, idx + 1))
  end
end

-- 3. back_l_sword_v1
do
  local dirOut = CLEAN_ROOT .. "/back_l_sword"
  app.fs.makeAllDirectories(dirOut)
  baseL:saveAs(dirOut .. "/00.png")
  for idx = 0, 6 do
    local im = Image{ fromFile = string.format("%s/back_l_sword_v1/%02d.png", RAW_ROOT, idx) }
    im = anchorOffHandBackL(im, baseL)
    if idx == 2 then
      -- F03 (raw 02): shift distal left fist (x=0..22, y=14..40) right by 3px so xmin >= 3
      im = shiftRegion(im, 0, 22, 14, 40, 3, 0)
    elseif idx == 3 then
      -- F04 (raw 03): shift distal left fist (x=0..22, y=34..56) right by 3px so xmin >= 3
      im = shiftRegion(im, 0, 22, 34, 56, 3, 0)
    end
    im:saveAs(string.format("%s/%02d.png", dirOut, idx + 1))
  end
end

-- 4. back_l_axe_v1
do
  local dirOut = CLEAN_ROOT .. "/back_l_axe"
  app.fs.makeAllDirectories(dirOut)
  baseL:saveAs(dirOut .. "/00.png")
  for idx = 0, 6 do
    local im = Image{ fromFile = string.format("%s/back_l_axe_v1/%02d.png", RAW_ROOT, idx) }
    im = anchorOffHandBackL(im, baseL)
    if idx == 0 then
      -- F01 (raw 00): shift overhead left fist (x=18..50, y=0..18) down by 3px so ymin >= 3
      im = shiftRegion(im, 18, 50, 0, 18, 0, 3)
    elseif idx == 1 then
      -- F02 (raw 01): shift overhead left fist (x=20..52, y=0..18) down by 3px so ymin >= 3
      im = shiftRegion(im, 20, 52, 0, 18, 0, 3)
    elseif idx == 3 then
      -- F04 (raw 03): shift distal left fist (x=0..22, y=52..76) right by 2px so xmin >= 3
      im = shiftRegion(im, 0, 22, 52, 76, 2, 0)
    end
    im:saveAs(string.format("%s/%02d.png", dirOut, idx + 1))
  end
end

print("Cleaned all 4 rear weapon body sequences.")
