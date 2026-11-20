-- Authoritative Aseprite Lua script for targeted Unarmed recovery
-- Main Orc (orc-v1) - front_r/Unarmed, front_l/Unarmed, back_r/Unarmed, back_l/Unarmed
local root = app.fs.currentPath
local function isAbs(p)
  return string.sub(p, 2, 2) == ":" or string.sub(p, 1, 1) == "/" or string.sub(p, 1, 1) == "\\"
end
local function file(p)
  if isAbs(p) then return p end
  return app.fs.joinPath(root, p)
end
local function alpha(p) return app.pixelColor.rgbaA(p) end

print("=== Authoring Targeted Unarmed Clips in Aseprite ===")

local INK = app.pixelColor.rgba(12, 15, 18, 255)
local CLEAR = app.pixelColor.rgba(0, 0, 0, 0)
local durations = { 80, 110, 60, 90, 110 } -- 450 ms total

local function blank(w, h)
  local im = Image(w, h, ColorMode.RGB)
  im:clear()
  return im
end

local function saveSprite(path, w, h, name, frames)
  local full = file(path)
  app.fs.makeAllDirectories(app.fs.filePath(full))
  local s = Sprite(w, h, ColorMode.RGB)
  s.layers[1].name = name
  for fi = 1, #frames do
    if fi > 1 then s:newEmptyFrame() end
    s:newCel(s.layers[1], fi, frames[fi], Point(0, 0))
    s.frames[fi].duration = durations[fi] / 1000
  end
  s:newTag(1, #frames).name = "Attack"
  s:saveAs(full)
  s:close()
end

-- =========================================================================
-- 1. front_r and front_l Unarmed: restore opposite arm in Frame 2 and Frame 3
-- =========================================================================
print("Processing front_r and front_l Unarmed...")
for _, d in ipairs({ "front_r", "front_l" }) do
  local candDir = file(string.format("characters/orc-v1/source/rear-recovery-v2/%s/Unarmed", d))
  local natMaster = string.format("characters/orc-v1/source/aseprite/rear-recovery-v2/native/unarmed-%s.aseprite", d)
  local compMaster = string.format("characters/orc-v1/source/aseprite/rear-recovery-v2/composite/%s/unarmed-attack.aseprite", d)
  
  local frames = {}
  for fi = 1, 5 do
    frames[fi] = Image{ fromFile = app.fs.joinPath(candDir, string.format("%02d.png", fi - 1)) }
  end
  
  -- F01 has the complete opposite arm in cocked guard
  local f01 = frames[2]
  
  -- In F02 and F03, graft the missing opposite arm from F01:
  for _, fi in ipairs({ 3, 4 }) do -- Frame 2 and Frame 3 (1-based: 3 and 4)
    local target = frames[fi]
    if d == "front_r" then
      -- Opposite arm is left arm (x: 80..112, y: 80..140 in 256 canvas)
      for y = 80, 140 do
        for x = 80, 112 do
          local sp = f01:getPixel(x, y)
          if alpha(sp) > 0 and alpha(target:getPixel(x, y)) == 0 then
            target:drawPixel(x, y, sp)
          end
        end
      end
    else
      -- Opposite arm is right arm (x: 144..176, y: 80..140 in 256 canvas)
      for y = 80, 140 do
        for x = 144, 176 do
          local sp = f01:getPixel(x, y)
          if alpha(sp) > 0 and alpha(target:getPixel(x, y)) == 0 then
            target:drawPixel(x, y, sp)
          end
        end
      end
    end
  end
  
  -- Save frames and masters
  local natFrames = {}
  for fi = 1, 5 do
    frames[fi]:saveAs(app.fs.joinPath(candDir, string.format("%02d.png", fi - 1)))
    local nat = blank(128, 128)
    nat:drawImage(frames[fi], Point(-64, -64))
    natFrames[fi] = nat
  end
  
  local strip = blank(128 * 5, 128)
  for fi = 1, 5 do
    strip:drawImage(natFrames[fi], Point((fi - 1) * 128, 0))
  end
  strip:saveAs(app.fs.joinPath(candDir, "native-strip.png"))
  
  saveSprite(compMaster, 256, 256, "Unarmed body", frames)
  saveSprite(natMaster, 128, 128, "Unarmed_" .. d, natFrames)
  print("Successfully restored opposite arm in " .. d .. " Unarmed.")
end

-- =========================================================================
-- 2. back_r Unarmed: restore striking fist follow-through in Frame 3
-- =========================================================================
print("Processing back_r Unarmed...")
do
  local candDir = file("characters/orc-v1/source/rear-recovery-v2/back_r/Unarmed")
  local natMaster = "characters/orc-v1/source/aseprite/rear-recovery-v2/native/unarmed-back_r.aseprite"
  local compMaster = "characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_r/unarmed-attack.aseprite"
  
  local frames = {}
  for fi = 1, 5 do
    frames[fi] = Image{ fromFile = app.fs.joinPath(candDir, string.format("%02d.png", fi - 1)) }
  end
  
  -- Frame 2 (idx 2) is punch impact: fist extended to x=186 at y=83..103
  -- Frame 3 (idx 3) must be follow-through recoil: fist slightly recoiled at x=178..182, y=86..106
  local f02 = frames[3]
  local f03 = frames[4]
  
  -- Render fist follow-through onto f03 from f02 with smooth 4px recoil
  for y = 80, 110 do
    for x = 160, 186 do
      local p = f02:getPixel(x, y)
      if alpha(p) > 0 then
        local rx = x - 4
        local ry = y + 2
        f03:drawPixel(rx, ry, p)
      end
    end
  end
  
  -- Connect forearm smoothly from torso (x=152) to fist (x=175)
  for y = 92, 106 do
    for x = 152, 175 do
      if alpha(f03:getPixel(x, y)) == 0 then
        f03:drawPixel(x, y, f02:getPixel(x + 4, y - 2))
      end
    end
  end
  
  -- Save frames and masters
  local natFrames = {}
  for fi = 1, 5 do
    frames[fi]:saveAs(app.fs.joinPath(candDir, string.format("%02d.png", fi - 1)))
    local nat = blank(128, 128)
    nat:drawImage(frames[fi], Point(-64, -64))
    natFrames[fi] = nat
  end
  
  local strip = blank(128 * 5, 128)
  for fi = 1, 5 do
    strip:drawImage(natFrames[fi], Point((fi - 1) * 128, 0))
  end
  strip:saveAs(app.fs.joinPath(candDir, "native-strip.png"))
  
  saveSprite(compMaster, 256, 256, "Unarmed body", frames)
  saveSprite(natMaster, 128, 128, "Unarmed_back_r", natFrames)
  print("Successfully restored striking fist follow-through in back_r Unarmed.")
end

-- =========================================================================
-- 3. back_l Unarmed: reconstruct with authentic NW rear recovery frames
-- =========================================================================
print("Processing back_l Unarmed...")
do
  local candDir = file("characters/orc-v1/source/rear-recovery-v2/back_l/Unarmed")
  local natMaster = "characters/orc-v1/source/aseprite/rear-recovery-v2/native/unarmed-back_l.aseprite"
  local compMaster = "characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_l/unarmed-attack.aseprite"
  
  local baseImg = Image{ fromFile = file("experiments/main-orc-complete-v1/pixellab-recovery/back_l_base.png") }
  local impactImg = Image{ fromFile = file("experiments/main-orc-rear-recovery-v2/punch_impact_clean_l.png") }
  
  local f00 = blank(128, 128); f00:drawImage(baseImg, Point(0, 1))
  
  -- F01: Shoulder coil
  local f01 = blank(128, 128); f01:drawImage(baseImg, Point(0, 0))
  for y = 14, 50 do
    for x = 15, 55 do
      local p = baseImg:getPixel(x, y)
      if alpha(p) > 0 then
        f01:drawPixel(x + 2, y - 1, p)
      end
    end
  end
  
  -- F02: Gauntlet impact
  local f02 = blank(128, 128); f02:drawImage(impactImg, Point(0, 0))
  
  -- F03: Follow-through
  local f03 = blank(128, 128); f03:drawImage(impactImg, Point(0, 0))
  for y = 12, 45 do
    for x = 6, 40 do
      local p = impactImg:getPixel(x, y)
      if alpha(p) > 0 then
        f03:drawPixel(x, y, CLEAR)
        f03:drawPixel(x + 5, y + 1, p)
      end
    end
  end
  
  -- F04: Recovery settle towards base
  local f04 = blank(128, 128); f04:drawImage(baseImg, Point(0, 1))
  for y = 18, 55 do
    for x = 15, 45 do
      local p = impactImg:getPixel(x, y)
      if alpha(p) > 0 then
        f04:drawPixel(x + 12, y + 2, p)
      end
    end
  end
  
  local natFrames = { f00, f01, f02, f03, f04 }
  local compFrames = {}
  for fi = 1, 5 do
    local comp = blank(256, 256)
    comp:drawImage(natFrames[fi], Point(64, 64))
    compFrames[fi] = comp
    comp:saveAs(app.fs.joinPath(candDir, string.format("%02d.png", fi - 1)))
  end
  
  local strip = blank(128 * 5, 128)
  for fi = 1, 5 do
    strip:drawImage(natFrames[fi], Point((fi - 1) * 128, 0))
  end
  strip:saveAs(app.fs.joinPath(candDir, "native-strip.png"))
  
  saveSprite(compMaster, 256, 256, "Unarmed body", compFrames)
  saveSprite(natMaster, 128, 128, "Unarmed_back_l", natFrames)
  print("Successfully reconstructed back_l Unarmed with authentic NW anatomy.")
end

print("All Unarmed clips authored successfully.")
