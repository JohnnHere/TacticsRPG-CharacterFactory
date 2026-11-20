-- Aseprite Lua script: Author and export all 8 weapon clips (4 front + 4 rear) for main-orc-combat-rescue-v5
local ROOT = "C:/Users/João Orlando/Documents/Projetos Unity/TacticsRPG-CharacterFactory"
local V4_ROOT = ROOT .. "/characters/orc-v1/source/rear-reconstruction-v4"
local CLEAN_REAR = ROOT .. "/experiments/main-orc-combat-rescue-v5/combat/cleaned_rear_bodies"
local OUT_ROOT = ROOT .. "/characters/orc-v1/source/combat-rescue-v5/combat"

local function ensureDir(p)
  app.fs.makeAllDirectories(p)
end

-- Copy independent weapon assets into OUT_ROOT/weapons/
ensureDir(OUT_ROOT .. "/weapons/Sword")
ensureDir(OUT_ROOT .. "/weapons/Axe")
do
  local sSpr = app.open(V4_ROOT .. "/weapons/Sword/recruit-sword.aseprite")
  sSpr:saveCopyAs(OUT_ROOT .. "/weapons/Sword/recruit-sword.aseprite")
  sSpr:close()
  local sIm = Image{ fromFile = V4_ROOT .. "/weapons/Sword/recruit-sword.png" }
  sIm:saveAs(OUT_ROOT .. "/weapons/Sword/recruit-sword.png")

  local aSpr = app.open(V4_ROOT .. "/weapons/Axe/militia-axe.aseprite")
  aSpr:saveCopyAs(OUT_ROOT .. "/weapons/Axe/militia-axe.aseprite")
  aSpr:close()
  local aIm = Image{ fromFile = V4_ROOT .. "/weapons/Axe/militia-axe.png" }
  aIm:saveAs(OUT_ROOT .. "/weapons/Axe/militia-axe.png")
end

local SWORD_ITEM = Image{ fromFile = OUT_ROOT .. "/weapons/Sword/recruit-sword.png" }
local AXE_ITEM   = Image{ fromFile = OUT_ROOT .. "/weapons/Axe/militia-axe.png" }

local rgba = app.pixelColor.rgba
local rgbaA = app.pixelColor.rgbaA
local INK        = rgba(12, 15, 18, 255)
local IRON_DARK  = rgba(38, 43, 50, 255)
local IRON_MID   = rgba(60, 67, 76, 255)
local IRON_LITE  = rgba(88, 96, 108, 255)
local LEATH_DARK = rgba(52, 26, 22, 255)
local LEATH_MID  = rgba(84, 38, 30, 255)

local function blank(w, h)
  local im = Image(w, h, ColorMode.RGBA)
  im:clear()
  return im
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

-- Build natural enclosing gauntlet handFront (fingers + thumb + wrist cuff) in 256x256 space
-- Build natural handle-enclosing gauntlet handFront on 256x256 canvas
-- Automatically determines which side of the handle faces the character's forearm/body
-- so that hu < 0 ALWAYS bridges toward the forearm/wrist and hu > 0 ALWAYS curls fingers around the outer edge of the handle.
local function buildNaturalHandFront(bodyIm256, gx, gy, deg, flip, isSword, forearmSide)
  local hf = blank(256, 256)
  local rad = deg * math.pi / 180.0
  local c, s = math.cos(rad), math.sin(rad)

  -- Sample body pixels in a 10px ring around (gx, gy) to find the forearm/shoulder side along the rx axis
  local sumRx = 0.0
  for sy = gy - 10, gy + 10 do
    for sx = gx - 10, gx + 10 do
      if rgbaA(getPx(bodyIm256, sx, sy)) > 0 then
        local dx, dy = sx - gx, sy - gy
        local rx = c * dx + s * dy
        sumRx = sumRx + rx
      end
    end
  end
  -- If sumRx < 0, the forearm/body is primarily on rx < 0, so fingertips point toward rx > 0 (tipSign = +1).
  -- If sumRx > 0, the forearm/body is primarily on rx > 0, so fingertips point toward rx < 0 (tipSign = -1).
  local tipSign = (sumRx <= 0) and 1 or -1

  for y = math.max(0, gy - 18), math.min(255, gy + 18) do
    for x = math.max(0, gx - 18), math.min(255, gx + 18) do
      local dx, dy = x - gx, y - gy
      local rx = c * dx + s * dy
      local ry = -s * dx + c * dy
      -- Transform into handle-normalized coordinates:
      -- hu > 0 is toward the finger tips (curling around the outer edge of the handle)
      -- hu < 0 is toward the palm/wrist cuff (connecting into the forearm)
      -- hv is along the shaft around the grip center
      local hu = rx * tipSign
      local hv = ry

      local vTop = isSword and -5.2 or -5.5
      local vBot = isSword and 5.2 or 4.8

      -- 1) 4 Articulated Finger Straps wrapping over the front of the shaft (hu in [-3.5 .. +4.2], hv in [vTop .. vBot])
      if hv >= vTop and hv <= vBot and hu >= -3.6 and hu <= 4.2 then
        -- Top or bottom outline of the closed 4-finger block
        if hv <= vTop + 0.9 or hv >= vBot - 0.9 then
          setPx(hf, x, y, INK)
        elseif hu >= 3.2 then
          -- Distal fingertip tuck outline on the far edge of the handle
          setPx(hf, x, y, INK)
        elseif hu <= -2.7 then
          -- Back-of-hand / wrist transition border
          setPx(hf, x, y, IRON_DARK)
        else
          -- Inside the 4 fingers: divide hv into 4 distinct finger segments separated by dark knuckle crevices
          local normV = (hv - (vTop + 0.9)) / ((vBot - 0.9) - (vTop + 0.9)) -- 0..1
          local fPos = normV * 3.8
          local frac = fPos - math.floor(fPos)
          if frac < 0.18 and hu >= -1.0 then
            -- Inter-finger crevice line
            setPx(hf, x, y, INK)
          else
            -- Armored finger plate shading: specular ridge on the knuckle crest (hu in [-0.8 .. +1.2]), mid steel, dark steel near tips
            if hu >= -0.8 and hu <= 1.1 then
              setPx(hf, x, y, IRON_LITE)
            elseif hu > 1.1 and hu <= 2.3 then
              setPx(hf, x, y, IRON_MID)
            else
              setPx(hf, x, y, IRON_DARK)
            end
          end
        end
      end

      -- 2) Thumb Lock on the upper/inner side of the grip (hv in [vTop - 2.2 .. vTop + 1.8], hu in [-3.8 .. +1.8])
      if hv >= vTop - 2.1 and hv < vTop + 1.6 and hu >= -3.8 and hu <= 1.8 then
        if hv <= vTop - 1.2 or hu >= 0.9 or hu <= -3.0 then
          setPx(hf, x, y, INK)
        elseif hu >= -1.2 and hu < 0.2 then
          setPx(hf, x, y, IRON_LITE)
        else
          setPx(hf, x, y, IRON_MID)
        end
      end

      -- 3) Wrist Cuff / Gauntlet Strap Bridge (hu in [-6.8 .. -2.5], hv in [vTop + 0.2 .. vBot - 0.2])
      -- Only draw where the underlying body has gauntlet/forearm pixels so it bridges seamlessly into the arm!
      if hu >= -6.8 and hu < -2.5 and hv >= vTop + 0.2 and hv <= vBot - 0.2 then
        local bPx = getPx(bodyIm256, x, y)
        if rgbaA(bPx) > 0 then
          if hv <= vTop + 1.1 or hv >= vBot - 1.1 or hu <= -5.9 then
            setPx(hf, x, y, INK)
          elseif hu >= -4.8 and hu <= -3.3 then
            setPx(hf, x, y, LEATH_MID)
          else
            setPx(hf, x, y, LEATH_DARK)
          end
        end
      end
    end
  end
  return hf
end

-- Transform 96x96 weapon sprite onto 256x256 weaponBack and weaponFront layers
local function renderWeaponLayers(itemIm, itemGripX, itemGripY, gx, gy, deg, flip, splitMode)
  local wb = blank(256, 256)
  local wf = blank(256, 256)
  local rad = deg * math.pi / 180.0
  local c, s = math.cos(rad), math.sin(rad)

  for y = 0, 255 do
    for x = 0, 255 do
      local dx, dy = x - gx, y - gy
      local rx = c * dx + s * dy
      local ry = -s * dx + c * dy
      if flip then rx = -rx end
      local u = math.floor(rx + itemGripX + 0.5)
      local v = math.floor(ry + itemGripY + 0.5)
      if u >= 0 and u < 96 and v >= 0 and v < 96 then
        local col = itemIm:getPixel(u, v)
        if rgbaA(col) > 0 then
          if splitMode == "front_behind_coil" then
            -- In front coil frames (F04/F05 Sword, F04 Axe), blade/head above crossguard (ry < -6) goes behind shoulder/head (weaponBack),
            -- while hilt/crossguard/pommel (ry >= -6) stays in weaponFront so the hand grasps it in front of the arm
            if ry < -6 then
              setPx(wb, x, y, col)
            else
              setPx(wf, x, y, col)
            end
          elseif splitMode == "rear_overhead" then
            -- In rear overhead frames (F02/F03), pommel/lower handle (ry >= -4) goes in weaponBack, blade/head (ry < -4) in weaponFront
            if ry >= -4 then
              setPx(wb, x, y, col)
            else
              setPx(wf, x, y, col)
            end
          else
            setPx(wf, x, y, col)
          end
        end
      end
    end
  end
  return wb, wf
end

-- Export a complete 4-layer weapon clip
local function exportWeaponClip(dirName, cat, durationsMs, bodyFrames128, frameSpecs)
  local key = dirName .. "/" .. cat
  local outDir = OUT_ROOT .. "/" .. key
  local srcDir = outDir .. "/source"
  local natDir = outDir .. "/native"
  local lwbDir = outDir .. "/layers/weaponBack"
  local lbDir  = outDir .. "/layers/body"
  local lwfDir = outDir .. "/layers/weaponFront"
  local lhfDir = outDir .. "/layers/handFront"
  ensureDir(srcDir)
  ensureDir(natDir)
  ensureDir(lwbDir)
  ensureDir(lbDir)
  ensureDir(lwfDir)
  ensureDir(lhfDir)

  local isSword = (cat == "Sword")
  local itemIm = isSword and SWORD_ITEM or AXE_ITEM
  local itemGripX = isSword and 48 or 36
  local itemGripY = isSword and 66 or 55

  -- Create 4-layer 256x256 composite Sprite
  local sprComp = Sprite(256, 256, ColorMode.RGBA)
  local l_wb = sprComp.layers[1]; l_wb.name = "weaponBack"
  local l_b  = sprComp:newLayer(); l_b.name  = "body"
  local l_wf = sprComp:newLayer(); l_wf.name = "weaponFront"
  local l_hf = sprComp:newLayer(); l_hf.name = "handFront"

  local sprBody = Sprite(256, 256, ColorMode.RGBA)
  sprBody.layers[1].name = "body"

  local sprHand = Sprite(256, 256, ColorMode.RGBA)
  sprHand.layers[1].name = "handFront"

  local sprNat = Sprite(128, 128, ColorMode.RGBA)
  sprNat.layers[1].name = "body"

  for i = 2, #bodyFrames128 do
    sprComp:newEmptyFrame()
    sprBody:newEmptyFrame()
    sprHand:newEmptyFrame()
    sprNat:newEmptyFrame()
  end

  local natStrip = blank(128 * #bodyFrames128, 128)
  local compStrip = blank(256 * #bodyFrames128, 256)

  for i, natIm in ipairs(bodyFrames128) do
    local durSec = durationsMs[i] / 1000.0
    sprComp.frames[i].duration = durSec
    sprBody.frames[i].duration = durSec
    sprHand.frames[i].duration = durSec
    sprNat.frames[i].duration  = durSec

    local body256 = blank(256, 256)
    body256:drawImage(natIm, Point(64, 64))

    local wb256 = blank(256, 256)
    local wf256 = blank(256, 256)
    local hf256 = blank(256, 256)

    local spec = frameSpecs[i]
    if spec and spec.vis then
      wb256, wf256 = renderWeaponLayers(
        itemIm, itemGripX, itemGripY,
        spec.gx, spec.gy, spec.rot, spec.flip, spec.split
      )
      hf256 = buildNaturalHandFront(
        body256, spec.gx, spec.gy, spec.rot, spec.flip, isSword, spec.forearmSide
      )
    end

    sprComp:newCel(l_wb, i, wb256, Point(0, 0))
    sprComp:newCel(l_b,  i, body256, Point(0, 0))
    sprComp:newCel(l_wf, i, wf256, Point(0, 0))
    sprComp:newCel(l_hf, i, hf256, Point(0, 0))

    sprBody:newCel(sprBody.layers[1], i, body256, Point(0, 0))
    sprHand:newCel(sprHand.layers[1], i, hf256, Point(0, 0))
    sprNat:newCel(sprNat.layers[1], i, natIm, Point(0, 0))

    -- Flatten composite frame inside Aseprite
    local flat256 = blank(256, 256)
    flat256:drawImage(wb256, Point(0, 0))
    flat256:drawImage(body256, Point(0, 0))
    flat256:drawImage(wf256, Point(0, 0))
    flat256:drawImage(hf256, Point(0, 0))

    local idx0 = i - 1
    flat256:saveAs(string.format("%s/%02d.png", outDir, idx0))
    natIm:saveAs(string.format("%s/%02d.png", natDir, idx0))
    wb256:saveAs(string.format("%s/%02d.png", lwbDir, idx0))
    body256:saveAs(string.format("%s/%02d.png", lbDir, idx0))
    wf256:saveAs(string.format("%s/%02d.png", lwfDir, idx0))
    hf256:saveAs(string.format("%s/%02d.png", lhfDir, idx0))

    natStrip:drawImage(natIm, Point(idx0 * 128, 0))
    compStrip:drawImage(flat256, Point(idx0 * 256, 0))
  end

  natStrip:saveAs(outDir .. "/native-strip.png")
  compStrip:saveAs(outDir .. "/composite-strip.png")

  sprComp:saveCopyAs(srcDir .. "/composite.aseprite")
  sprBody:saveCopyAs(srcDir .. "/body.aseprite")
  sprHand:saveCopyAs(srcDir .. "/hand.aseprite")
  sprNat:saveCopyAs(srcDir .. "/native.aseprite")

  -- Also save a copy in OUT_ROOT/aseprite/<dirName>/<catLower>.aseprite for convenience
  ensureDir(OUT_ROOT .. "/aseprite/" .. dirName)
  sprComp:saveCopyAs(OUT_ROOT .. "/aseprite/" .. dirName .. "/" .. string.lower(cat) .. ".aseprite")

  sprComp:close()
  sprBody:close()
  sprHand:close()
  sprNat:close()
  print("Exported 4-layer weapon clip: " .. key)
end

-- Helper to load N native frames from a folder
local function loadNativeFrames(folder, count)
  local list = {}
  for i = 0, count - 1 do
    list[#list + 1] = Image{ fromFile = string.format("%s/%02d.png", folder, i) }
  end
  return list
end

-- 1. front_r/Sword (13 frames, 730ms)
exportWeaponClip(
  "front_r", "Sword",
  { 30, 65, 35, 50, 45, 65, 35, 35, 100, 55, 80, 45, 90 },
  loadNativeFrames(V4_ROOT .. "/front_r/Sword/native", 13),
  {
    [1]  = { vis = false },
    [2]  = { vis = false },
    [3]  = { vis = true, gx = 101, gy = 131, rot = 315, flip = false, split = "front", forearmSide = -1 },
    [4]  = { vis = true, gx = 88,  gy = 118, rot = 330, flip = false, split = "front", forearmSide = -1 },
    [5]  = { vis = true, gx = 98,  gy = 100, rot = 340, flip = false, split = "front_behind_coil", forearmSide = -1 },
    [6]  = { vis = true, gx = 98,  gy = 89,  rot = 345, flip = false, split = "front_behind_coil", forearmSide = -1 },
    [7]  = { vis = true, gx = 157, gy = 112, rot = 20,  flip = false, split = "front", forearmSide = -1 },
    [8]  = { vis = true, gx = 158, gy = 134, rot = 55,  flip = false, split = "front", forearmSide = -1 },
    [9]  = { vis = true, gx = 159, gy = 142, rot = 100, flip = false, split = "front", forearmSide = -1 },
    [10] = { vis = true, gx = 129, gy = 148, rot = 102, flip = false, split = "front", forearmSide = -1 },
    [11] = { vis = true, gx = 110, gy = 147, rot = 105, flip = false, split = "front", forearmSide = -1 },
    [12] = { vis = false },
    [13] = { vis = false },
  }
)

-- 2. front_l/Sword (13 frames, 730ms)
exportWeaponClip(
  "front_l", "Sword",
  { 30, 65, 35, 50, 45, 65, 35, 35, 100, 55, 80, 45, 90 },
  loadNativeFrames(V4_ROOT .. "/front_l/Sword/native", 13),
  {
    [1]  = { vis = false },
    [2]  = { vis = false },
    [3]  = { vis = true, gx = 154, gy = 131, rot = 45,  flip = true, split = "front", forearmSide = -1 },
    [4]  = { vis = true, gx = 167, gy = 118, rot = 30,  flip = true, split = "front", forearmSide = -1 },
    [5]  = { vis = true, gx = 157, gy = 100, rot = 20,  flip = true, split = "front_behind_coil", forearmSide = -1 },
    [6]  = { vis = true, gx = 157, gy = 89,  rot = 15,  flip = true, split = "front_behind_coil", forearmSide = -1 },
    [7]  = { vis = true, gx = 98,  gy = 112, rot = 340, flip = true, split = "front", forearmSide = -1 },
    [8]  = { vis = true, gx = 97,  gy = 134, rot = 305, flip = true, split = "front", forearmSide = -1 },
    [9]  = { vis = true, gx = 96,  gy = 142, rot = 260, flip = true, split = "front", forearmSide = -1 },
    [10] = { vis = true, gx = 126, gy = 148, rot = 258, flip = true, split = "front", forearmSide = -1 },
    [11] = { vis = true, gx = 145, gy = 147, rot = 255, flip = true, split = "front", forearmSide = -1 },
    [12] = { vis = false },
    [13] = { vis = false },
  }
)

-- 3. front_r/Axe (12 frames, 1005ms)
exportWeaponClip(
  "front_r", "Axe",
  { 40, 65, 35, 80, 155, 35, 115, 110, 130, 50, 90, 100 },
  loadNativeFrames(V4_ROOT .. "/front_r/Axe/native", 12),
  {
    [1]  = { vis = false },
    [2]  = { vis = false },
    [3]  = { vis = true, gx = 101, gy = 131, rot = 300, flip = false, split = "front", forearmSide = -1 },
    [4]  = { vis = true, gx = 88,  gy = 118, rot = 325, flip = false, split = "front", forearmSide = -1 },
    [5]  = { vis = true, gx = 98,  gy = 100, rot = 350, flip = false, split = "front_behind_coil", forearmSide = -1 },
    [6]  = { vis = true, gx = 146, gy = 119, rot = 35,  flip = false, split = "front", forearmSide = -1 },
    [7]  = { vis = true, gx = 148, gy = 143, rot = 85,  flip = false, split = "front", forearmSide = -1 },
    [8]  = { vis = true, gx = 138, gy = 148, rot = 90,  flip = false, split = "front", forearmSide = -1 },
    [9]  = { vis = true, gx = 129, gy = 148, rot = 80,  flip = false, split = "front", forearmSide = -1 },
    [10] = { vis = false },
    [11] = { vis = false },
    [12] = { vis = false },
  }
)

-- 4. front_l/Axe (12 frames, 1005ms)
exportWeaponClip(
  "front_l", "Axe",
  { 40, 65, 35, 80, 155, 35, 115, 110, 130, 50, 90, 100 },
  loadNativeFrames(V4_ROOT .. "/front_l/Axe/native", 12),
  {
    [1]  = { vis = false },
    [2]  = { vis = false },
    [3]  = { vis = true, gx = 154, gy = 131, rot = 60,  flip = true, split = "front", forearmSide = -1 },
    [4]  = { vis = true, gx = 167, gy = 118, rot = 35,  flip = true, split = "front", forearmSide = -1 },
    [5]  = { vis = true, gx = 157, gy = 100, rot = 10,  flip = true, split = "front_behind_coil", forearmSide = -1 },
    [6]  = { vis = true, gx = 109, gy = 119, rot = 325, flip = true, split = "front", forearmSide = -1 },
    [7]  = { vis = true, gx = 107, gy = 143, rot = 275, flip = true, split = "front", forearmSide = -1 },
    [8]  = { vis = true, gx = 117, gy = 148, rot = 270, flip = true, split = "front", forearmSide = -1 },
    [9]  = { vis = true, gx = 126, gy = 148, rot = 280, flip = true, split = "front", forearmSide = -1 },
    [10] = { vis = false },
    [11] = { vis = false },
    [12] = { vis = false },
  }
)

-- 5. back_r/Sword (8 frames, 730ms) - NEW PixelLab whole-body slash choreography + natural grip
exportWeaponClip(
  "back_r", "Sword",
  { 90, 80, 90, 80, 100, 80, 100, 110 },
  loadNativeFrames(CLEAN_REAR .. "/back_r_sword", 8),
  {
    [1] = { vis = false },
    [2] = { vis = true, gx = 172, gy = 110, rot = 335, flip = false, split = "front", forearmSide = -1 },
    [3] = { vis = true, gx = 180, gy = 91,  rot = 355, flip = false, split = "rear_overhead", forearmSide = -1 },
    [4] = { vis = true, gx = 184, gy = 87,  rot = 25,  flip = false, split = "rear_overhead", forearmSide = -1 },
    [5] = { vis = true, gx = 185, gy = 99,  rot = 70,  flip = true,  split = "front", forearmSide = -1 },
    [6] = { vis = true, gx = 181, gy = 113, rot = 105, flip = true,  split = "front", forearmSide = -1 },
    [7] = { vis = true, gx = 172, gy = 124, rot = 130, flip = false, split = "front", forearmSide = -1 },
    [8] = { vis = false },
  }
)

-- 6. back_r/Axe (8 frames, 730ms) - NEW PixelLab whole-body overhead cleave choreography + natural grip
exportWeaponClip(
  "back_r", "Axe",
  { 90, 80, 90, 80, 100, 80, 100, 110 },
  loadNativeFrames(CLEAN_REAR .. "/back_r_axe", 8),
  {
    [1] = { vis = false },
    [2] = { vis = true, gx = 160, gy = 73,  rot = 325, flip = false, split = "rear_overhead", forearmSide = -1 },
    [3] = { vis = true, gx = 157, gy = 73,  rot = 345, flip = false, split = "rear_overhead", forearmSide = -1 },
    [4] = { vis = true, gx = 180, gy = 90,  rot = 25,  flip = false, split = "front", forearmSide = -1 },
    [5] = { vis = true, gx = 184, gy = 119, rot = 75,  flip = false, split = "front", forearmSide = -1 },
    [6] = { vis = true, gx = 173, gy = 136, rot = 110, flip = false, split = "front", forearmSide = -1 },
    [7] = { vis = true, gx = 164, gy = 133, rot = 130, flip = false, split = "front", forearmSide = -1 },
    [8] = { vis = false },
  }
)

-- 7. back_l/Sword (8 frames, 730ms) - NEW PixelLab whole-body left-handed slash choreography + natural grip
exportWeaponClip(
  "back_l", "Sword",
  { 90, 80, 90, 80, 100, 80, 100, 110 },
  loadNativeFrames(CLEAN_REAR .. "/back_l_sword", 8),
  {
    [1] = { vis = false },
    [2] = { vis = true, gx = 80, gy = 86,  rot = 25,  flip = true, split = "front", forearmSide = -1 },
    [3] = { vis = true, gx = 76, gy = 76,  rot = 5,   flip = true, split = "rear_overhead", forearmSide = -1 },
    [4] = { vis = true, gx = 71, gy = 87,  rot = 335, flip = true, split = "rear_overhead", forearmSide = -1 },
    [5] = { vis = true, gx = 70, gy = 109, rot = 290, flip = false, split = "front", forearmSide = -1 },
    [6] = { vis = true, gx = 71, gy = 130, rot = 255, flip = false, split = "front", forearmSide = -1 },
    [7] = { vis = true, gx = 86, gy = 136, rot = 230, flip = true, split = "front", forearmSide = -1 },
    [8] = { vis = false },
  }
)

-- 8. back_l/Axe (8 frames, 730ms) - NEW PixelLab whole-body left-handed overhead cleave choreography + natural grip
exportWeaponClip(
  "back_l", "Axe",
  { 90, 80, 90, 80, 100, 80, 100, 110 },
  loadNativeFrames(CLEAN_REAR .. "/back_l_axe", 8),
  {
    [1] = { vis = false },
    [2] = { vis = true, gx = 92, gy = 78,  rot = 35,  flip = true, split = "rear_overhead", forearmSide = -1 },
    [3] = { vis = true, gx = 98, gy = 73,  rot = 15,  flip = true, split = "rear_overhead", forearmSide = -1 },
    [4] = { vis = true, gx = 72, gy = 88,  rot = 335, flip = true, split = "front", forearmSide = -1 },
    [5] = { vis = true, gx = 72, gy = 129, rot = 285, flip = true, split = "front", forearmSide = -1 },
    [6] = { vis = true, gx = 82, gy = 137, rot = 250, flip = true, split = "front", forearmSide = -1 },
    [7] = { vis = true, gx = 91, gy = 136, rot = 230, flip = true, split = "front", forearmSide = -1 },
    [8] = { vis = false },
  }
)
