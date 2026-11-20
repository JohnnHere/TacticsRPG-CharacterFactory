-- Aseprite Lua script: Author and export 4 Unarmed clips for main-orc-combat-rescue-v5
local ROOT = "C:/Users/João Orlando/Documents/Projetos Unity/TacticsRPG-CharacterFactory"
local V2_ROOT = ROOT .. "/characters/orc-v1/source/rear-recovery-v2"
local RAW_ROOT = ROOT .. "/experiments/main-orc-combat-rescue-v5/combat/raw"
local OUT_ROOT = ROOT .. "/characters/orc-v1/source/combat-rescue-v5/combat"

local DURATIONS = { 0.080, 0.110, 0.050, 0.090, 0.120 } -- 80, 110, 50, 90, 120 ms = 450 ms

local function ensureDir(p)
  app.fs.makeAllDirectories(p)
end

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

local function rgba(r, g, b, a)
  return app.pixelColor.rgba(r, g, b, a or 255)
end

local INK = rgba(12, 15, 18, 255)

-- Helper: build front_r Unarmed F03 (index 4 in 1-based Lua) from F02 base + retracted F02 punching arm
local function buildFrontRUnarmedF03(imF02, imF04)
  -- Start from F02 so torso, chest, belt, legs, and left guard arm are 100% continuous with F02!
  local out = cloneImage(imF02)
  -- 1. Clear F02's extended right forearm/fist in x = 84..112, y = 44..58
  for y = 44, 58 do
    for x = 84, 112 do
      setPx(out, x, y, 0)
    end
  end
  -- 2. Draw F02's punching forearm/fist (from x_src = 76..108, y_src = 44..58) shifted by dx = -4, dy = +2
  -- so the fist retracts 4px left and 2px down (xmax = 103, y = 47..60), connecting seamlessly to F02's elbow at x=72..83
  for y_src = 44, 58 do
    for x_src = 76, 108 do
      local c = getPx(imF02, x_src, y_src)
      if app.pixelColor.rgbaA(c) > 0 then
        local xd = x_src - 4
        local yd = y_src + 2
        if xd >= 76 then
          setPx(out, xd, yd, c)
        end
      end
    end
  end
  return out
end

-- Helper: build front_l Unarmed F03 (index 4 in 1-based Lua) from F02 base + retracted F02 left punching arm
local function buildFrontLUnarmedF03(imF02, imF04)
  local out = cloneImage(imF02)
  -- 1. Clear F02's extended left forearm/fist in x = 15..43, y = 44..58
  for y = 44, 58 do
    for x = 15, 43 do
      setPx(out, x, y, 0)
    end
  end
  -- 2. Draw F02's left punching forearm/fist (from x_src = 19..51, y_src = 44..58) shifted by dx = +4, dy = +2
  for y_src = 44, 58 do
    for x_src = 19, 51 do
      local c = getPx(imF02, x_src, y_src)
      if app.pixelColor.rgbaA(c) > 0 then
        local xd = x_src + 4
        local yd = y_src + 2
        if xd <= 51 then
          setPx(out, xd, yd, c)
        end
      end
    end
  end
  return out
end

-- Helper: shift distal right fist inward by 2px on back_r/Unarmed F02 (raw 01) so xmax <= 125
local function cleanBackRUnarmedF02(imRaw01)
  local out = cloneImage(imRaw01)
  -- Clear x = 104..127, y = 20..45
  for y = 20, 45 do
    for x = 104, 127 do
      setPx(out, x, y, 0)
    end
  end
  -- Copy x_src = 104..127, y_src = 20..45 shifted left by 2px (dx = -2)
  for y = 20, 45 do
    for x_src = 104, 127 do
      local c = getPx(imRaw01, x_src, y)
      if app.pixelColor.rgbaA(c) > 0 then
        local xd = x_src - 2
        if xd >= 104 then
          setPx(out, xd, y, c)
        end
      end
    end
  end
  -- Ensure crisp INK outline on rightmost edge if any interior pixel reached x=125
  for y = 20, 45 do
    local c = getPx(out, 125, y)
    if app.pixelColor.rgbaA(c) > 0 then
      setPx(out, 125, y, INK)
    end
  end
  return out
end

-- Helper: save native 128x128 master, composite 256x256 master, frame PNGs, and native-strip.png
local function exportUnarmedClip(dirName, nativeFrames)
  local clipDir = OUT_ROOT .. "/" .. dirName .. "/Unarmed"
  local nativeDir = clipDir .. "/native"
  local aseDir = OUT_ROOT .. "/aseprite/" .. dirName
  ensureDir(clipDir)
  ensureDir(nativeDir)
  ensureDir(aseDir)

  -- 1. Build and save 128x128 native .aseprite master
  local sprNat = Sprite(128, 128, ColorMode.RGBA)
  sprNat.layers[1].name = "body"
  for i = 2, #nativeFrames do
    sprNat:newEmptyFrame()
  end
  for i, im in ipairs(nativeFrames) do
    sprNat.frames[i].duration = DURATIONS[i]
    sprNat:newCel(sprNat.layers[1], sprNat.frames[i], im, Point(0, 0))
  end
  local natAsePath = aseDir .. "/unarmed-native.aseprite"
  sprNat:saveCopyAs(natAsePath)

  -- Export native/00..04.png and 640x128 native-strip.png
  local stripIm = Image(128 * #nativeFrames, 128, ColorMode.RGBA)
  stripIm:clear()
  for i, im in ipairs(nativeFrames) do
    local idx0 = i - 1
    im:saveAs(string.format("%s/%02d.png", nativeDir, idx0))
    stripIm:drawImage(im, Point(idx0 * 128, 0))
  end
  stripIm:saveAs(clipDir .. "/native-strip.png")
  sprNat:close()

  -- 2. Build and save 256x256 composite .aseprite master (with body at Point(64, 64))
  local sprComp = Sprite(256, 256, ColorMode.RGBA)
  sprComp.layers[1].name = "body"
  for i = 2, #nativeFrames do
    sprComp:newEmptyFrame()
  end
  for i, im in ipairs(nativeFrames) do
    sprComp.frames[i].duration = DURATIONS[i]
    local im256 = Image(256, 256, ColorMode.RGBA)
    im256:clear()
    im256:drawImage(im, Point(64, 64))
    sprComp:newCel(sprComp.layers[1], sprComp.frames[i], im256, Point(0, 0))
    local idx0 = i - 1
    im256:saveAs(string.format("%s/%02d.png", clipDir, idx0))
  end
  local compAsePath = aseDir .. "/unarmed.aseprite"
  sprComp:saveCopyAs(compAsePath)
  sprComp:close()
  print("Exported Unarmed clip: " .. dirName)
end

-- A. Author front_r/Unarmed
do
  local p = V2_ROOT .. "/front_r/Unarmed/native"
  local f00 = Image{ fromFile = p .. "/00.png" }
  local f01 = Image{ fromFile = p .. "/01.png" }
  local f02 = Image{ fromFile = p .. "/02.png" }
  local f04 = Image{ fromFile = p .. "/04.png" }
  local f03 = buildFrontRUnarmedF03(f02, f04)
  exportUnarmedClip("front_r", { f00, f01, f02, f03, f04 })
end

-- B. Author front_l/Unarmed
do
  local p = V2_ROOT .. "/front_l/Unarmed/native"
  local f00 = Image{ fromFile = p .. "/00.png" }
  local f01 = Image{ fromFile = p .. "/01.png" }
  local f02 = Image{ fromFile = p .. "/02.png" }
  local f04 = Image{ fromFile = p .. "/04.png" }
  local f03 = buildFrontLUnarmedF03(f02, f04)
  exportUnarmedClip("front_l", { f00, f01, f02, f03, f04 })
end

-- C. Author back_r/Unarmed (F00 base + 4 PixelLab skeleton-v3 punch frames)
do
  local f00 = Image{ fromFile = RAW_ROOT .. "/back_r_base_128.png" }
  local f01 = Image{ fromFile = RAW_ROOT .. "/back_r_unarmed_v1/00.png" }
  local f02 = cleanBackRUnarmedF02(Image{ fromFile = RAW_ROOT .. "/back_r_unarmed_v1/01.png" })
  local f03 = Image{ fromFile = RAW_ROOT .. "/back_r_unarmed_v1/02.png" }
  local f04 = Image{ fromFile = RAW_ROOT .. "/back_r_unarmed_v1/03.png" }
  exportUnarmedClip("back_r", { f00, f01, f02, f03, f04 })
end

-- D. Author back_l/Unarmed (F00 base + 4 PixelLab skeleton-v3 punch frames)
do
  local f00 = Image{ fromFile = RAW_ROOT .. "/back_l_base_128.png" }
  local f01 = Image{ fromFile = RAW_ROOT .. "/back_l_unarmed_v1/00.png" }
  local f02 = Image{ fromFile = RAW_ROOT .. "/back_l_unarmed_v1/01.png" }
  local f03 = Image{ fromFile = RAW_ROOT .. "/back_l_unarmed_v1/02.png" }
  local f04 = Image{ fromFile = RAW_ROOT .. "/back_l_unarmed_v1/03.png" }
  exportUnarmedClip("back_l", { f00, f01, f02, f03, f04 })
end
