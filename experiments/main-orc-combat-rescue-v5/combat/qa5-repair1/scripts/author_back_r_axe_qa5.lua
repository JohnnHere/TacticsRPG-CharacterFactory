-- Authoring script for QA5-01/02/03 repair on back_r/Axe (whole-body + real anatomical grip)
local repo = "C:/Users/João Orlando/Documents/Projetos Unity/TacticsRPG-CharacterFactory"
local idleBaseP = repo .. "/characters/orc-v1/source/combat-rescue-v5/combat/back_r/Axe/native/00.png"
local rawDir = repo .. "/experiments/main-orc-combat-rescue-v5/combat/qa5-repair1/raw/back_r_axe_qa5_v1"
local weaponPath = repo .. "/characters/orc-v1/source/combat-rescue-v5/combat/weapons/Axe/militia-axe.png"
local outDir = repo .. "/characters/orc-v1/source/combat-rescue-v5/combat/qa5-repair1/back_r/Axe"

local durations = {85, 85, 80, 90, 95, 110, 95, 90}

-- Real anatomical coordinates measured directly on the 128x128 whole-body back_r/Axe sprites
-- Transformed to 256x256 composite space (+64, +64)
-- F01..F06 are the active weapon frames; F00 and F07 are weapon-hidden guard frames
local anatomy = {
  [1] = { visible=false, sh={144,94}, el={154,114}, wr={158,128}, pa={159,138}, deg=0, layer="weaponFront" },
  [2] = { visible=true,  sh={146,92}, el={164,95},  wr={163,83},  pa={158,76},  deg=-55, layer="weaponFront" },
  [3] = { visible=true,  sh={145,91}, el={160,92},  wr={162,79},  pa={156,72},  deg=-35, layer="weaponFront" },
  [4] = { visible=true,  sh={146,93}, el={164,92},  wr={170,84},  pa={172,77},  deg=12,  layer="weaponFront" },
  [5] = { visible=true,  sh={147,94}, el={168,107}, wr={177,114}, pa={177,121}, deg=98,  layer="weaponFront" },
  [6] = { visible=true,  sh={147,96}, el={164,114}, wr={170,127}, pa={173,136}, deg=122, layer="weaponFront" },
  [7] = { visible=true,  sh={145,95}, el={159,115}, wr={164,129}, pa={165,137}, deg=132, layer="weaponFront" },
  [8] = { visible=false, sh={144,94}, el={155,115}, wr={159,129}, pa={159,138}, deg=0,   layer="weaponFront" }
}

local wepImg = Image{ fromFile=weaponPath }
-- Actual wooden grip center on militia-axe.png is (36, 48); shaft axis toward head is -75 deg
local gripPivotX, gripPivotY = 36.0, 48.0

local function rotateWeapon(src, pivotX, pivotY, dstX, dstY, deg)
  local dst = Image(256, 256, ColorMode.RGB)
  local rad = math.rad(deg)
  local cosA = math.cos(rad)
  local sinA = math.sin(rad)
  for y = 0, 255 do
    for x = 0, 255 do
      local dx = x - dstX
      local dy = y - dstY
      local sx = math.floor(pivotX + dx * cosA + dy * sinA + 0.5)
      local sy = math.floor(pivotY - dx * sinA + dy * cosA + 0.5)
      if sx >= 0 and sx < src.width and sy >= 0 and sy < src.height then
        local p = src:getPixel(sx, sy)
        if app.pixelColor.rgbaA(p) > 0 then
          dst:drawPixel(x, y, p)
        end
      end
    end
  end
  return dst
end

local function drawDisc(img, cx, cy, r, col)
  local r2 = r * r
  local x0 = math.max(0, math.floor(cx - r - 1))
  local x1 = math.min(img.width - 1, math.ceil(cx + r + 1))
  local y0 = math.max(0, math.floor(cy - r - 1))
  local y1 = math.min(img.height - 1, math.ceil(cy + r + 1))
  for y = y0, y1 do
    for x = x0, x1 do
      local dx = x - cx
      local dy = y - cy
      if dx*dx + dy*dy <= r2 then
        img:drawPixel(x, y, col)
      end
    end
  end
end

local function drawCapsule(img, x0, y0, x1, y1, r, col)
  local steps = math.max(1, math.ceil(math.sqrt((x1-x0)^2 + (y1-y0)^2) * 2))
  for i = 0, steps do
    local t = i / steps
    drawDisc(img, x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, r, col)
  end
end

-- Sculpt real anatomical grip around militia-axe handle at pa=(px,py) and wrist wr=(wx,wy)
local function buildAnatomicalGrip(bodyImg, wepRotImg, wx, wy, px, py, deg)
  local handImg = Image(256, 256, ColorMode.RGB)
  local rgba = app.pixelColor.rgba

  local cInk       = rgba(14, 16, 20, 255)
  local cLeatherDk = rgba(52, 27, 25, 255)
  local cLeatherMd = rgba(78, 38, 33, 255)
  local cLeatherHi = rgba(102, 50, 42, 255)
  local cSteelDk   = rgba(48, 56, 65, 255)
  local cSteelMd   = rgba(75, 86, 98, 255)
  local cSteelHi   = rgba(106, 118, 132, 255)

  -- Shaft direction unit vector u (from grip (36,48) toward axe head (44,28) is -75 deg in militia-axe.png)
  local shaftRad = math.rad(-75 + deg)
  local ux = math.cos(shaftRad)
  local uy = math.sin(shaftRad)
  local nx = -uy
  local ny = ux

  -- Ensure finger tips point away from the wrist side of the handle
  local toWristX = wx - px
  local toWristY = wy - py
  local wristDotN = toWristX * nx + toWristY * ny
  local wrapSign = (wristDotN > 0) and -1.0 or 1.0
  local fnx = nx * wrapSign
  local fny = ny * wrapSign

  -- 1. First draw the continuous wrist-to-palm leather/cuff bridge (underneath the fingers)
  local bdx = px - wx
  local bdy = py - wy
  local blen = math.max(1.0, math.sqrt(bdx*bdx + bdy*bdy))
  local bnx = -bdy / blen
  local bny = bdx / blen

  drawCapsule(handImg, wx, wy, px - bdx*0.25, py - bdy*0.25, 3.6, cInk)
  drawCapsule(handImg, wx, wy, px - bdx*0.28, py - bdy*0.28, 2.6, cSteelDk)
  drawCapsule(handImg, wx - bnx*0.7, wy - bny*0.7, px - bdx*0.35 - bnx*0.7, py - bdy*0.35 - bny*0.7, 1.5, cSteelMd)
  drawDisc(handImg, wx, wy, 2.2, cSteelMd)
  drawDisc(handImg, wx - bnx*0.9, wy - bny*0.9, 1.2, cSteelHi)

  -- 2. Draw 4 articulated gauntlet fingers wrapping tightly across the wooden handle shaft
  -- Handle grip zone is s = -6.0 .. +6.0 (knob/pommel is s <= -7, upper shaft/blade is s >= +7)
  local fingerOffsets = {-4.2, -1.5, 1.2, 3.8}
  for idx, sOff in ipairs(fingerOffsets) do
    local fbx = px + ux * sOff - fnx * 2.2
    local fby = py + uy * sOff - fny * 2.2
    local ftx = px + ux * (sOff + 0.2) + fnx * 2.4
    local fty = py + uy * (sOff + 0.2) + fny * 2.4
    drawCapsule(handImg, fbx, fby, ftx, fty, 1.8, cInk)
  end

  for idx, sOff in ipairs(fingerOffsets) do
    local fbx = px + ux * sOff - fnx * 1.9
    local fby = py + uy * sOff - fny * 1.9
    local ftx = px + ux * (sOff + 0.2) + fnx * 2.0
    local fty = py + uy * (sOff + 0.2) + fny * 2.0
    local fillCol = (idx % 2 == 0) and cLeatherMd or cLeatherDk
    drawCapsule(handImg, fbx, fby, ftx, fty, 1.15, fillCol)
    local kkx = px + ux * sOff + fnx * 0.4
    local kky = py + uy * sOff + fny * 0.4
    drawDisc(handImg, kkx, kky, 0.9, (idx <= 2) and cSteelMd or cLeatherHi)
  end

  -- 3. Draw thumb locking around the upper handle side (s = +2.2 .. +4.8)
  local tbx = px + ux * 1.6 - fnx * 2.5
  local tby = py + uy * 1.6 - fny * 2.5
  local ttx = px + ux * 4.5 + fnx * 1.0
  local tty = py + uy * 4.5 + fny * 1.0
  drawCapsule(handImg, tbx, tby, ttx, tty, 1.9, cInk)
  drawCapsule(handImg, tbx, tby, ttx, tty, 1.15, cLeatherMd)
  drawDisc(handImg, (tbx + ttx)*0.5, (tby + tty)*0.5, 0.9, cLeatherHi)

  -- 4. Keep the upper wooden shaft + bearded steel axe head (s >= 6.2) and bottom knob (s <= -6.5) 100% clear of handFront
  for y = math.max(0, math.floor(py - 24)), math.min(255, math.ceil(py + 24)) do
    for x = math.max(0, math.floor(px - 24)), math.min(255, math.ceil(px + 24)) do
      local dx = x - px
      local dy = y - py
      local s = dx * ux + dy * uy
      local t = dx * nx + dy * ny
      if s > 6.2 or s < -6.5 then
        local wp = wepRotImg:getPixel(x, y)
        if app.pixelColor.rgbaA(wp) > 0 then
          handImg:drawPixel(x, y, rgba(0, 0, 0, 0))
        end
      end
    end
  end

  return handImg
end

-- Create 256x256 composite master sprite
local compSpr = Sprite(256, 256, ColorMode.RGB)
compSpr.filename = outDir .. "/source/composite.aseprite"

local lWepBack = compSpr.layers[1]
lWepBack.name = "weaponBack"
local lBody = compSpr:newLayer()
lBody.name = "body"
local lWepFront = compSpr:newLayer()
lWepFront.name = "weaponFront"
local lHandFront = compSpr:newLayer()
lHandFront.name = "handFront"

for f = 2, 8 do
  compSpr:newEmptyFrame()
end

for f = 1, 8 do
  compSpr.frames[f].duration = durations[f] / 1000.0
  local a = anatomy[f]

  -- Load 128x128 native frame (F00 from idle base, F01..F07 from PixelLab whole-body job)
  local srcFile = (f == 1) and idleBaseP or string.format("%s/%02d.png", rawDir, f - 2)
  local nat128 = Image{ fromFile=srcFile }

  -- Place 128x128 body at (64, 64) in 256x256 canvas (ZERO F00 column pasting!)
  local body256 = Image(256, 256, ColorMode.RGB)
  for y = 0, 127 do
    for x = 0, 127 do
      local p = nat128:getPixel(x, y)
      if app.pixelColor.rgbaA(p) > 0 then
        -- In F02 (f==3), shift only the top tip of the raised right fist (x=76..106, y=0..20) down by 3px so ymin=3
        if f == 3 and x >= 76 and x <= 106 and y <= 20 then
          body256:drawPixel(x + 64, y + 64 + 3, p)
        else
          body256:drawPixel(x + 64, y + 64, p)
        end
      end
    end
  end

  local wepBack256 = Image(256, 256, ColorMode.RGB)
  local wepFront256 = Image(256, 256, ColorMode.RGB)
  local hand256 = Image(256, 256, ColorMode.RGB)

  if a.visible then
    local px, py = a.pa[1], a.pa[2]
    local wx, wy = a.wr[1], a.wr[2]
    local rotWep = rotateWeapon(wepImg, gripPivotX, gripPivotY, px, py, a.deg)
    if a.layer == "weaponBack" then
      wepBack256 = rotWep
    else
      wepFront256 = rotWep
    end
    hand256 = buildAnatomicalGrip(body256, rotWep, wx, wy, px, py, a.deg)
  end

  compSpr:newCel(lWepBack, f, wepBack256, Point(0, 0))
  compSpr:newCel(lBody, f, body256, Point(0, 0))
  compSpr:newCel(lWepFront, f, wepFront256, Point(0, 0))
  compSpr:newCel(lHandFront, f, hand256, Point(0, 0))
end

compSpr:saveCopyAs(outDir .. "/source/composite.aseprite")
compSpr:saveCopyAs(outDir .. "/master256.aseprite")

-- Export per-layer PNGs, composite 256 PNGs, and native 128 PNGs
local natSpr = Sprite(128, 128, ColorMode.RGB)
local lNat = natSpr.layers[1]
lNat.name = "native"
for f = 2, 8 do natSpr:newEmptyFrame() end

local bodySpr = Sprite(256, 256, ColorMode.RGB)
local lBodyOnly = bodySpr.layers[1]
lBodyOnly.name = "body"
for f = 2, 8 do bodySpr:newEmptyFrame() end

local handSpr = Sprite(256, 256, ColorMode.RGB)
local lHandOnly = handSpr.layers[1]
lHandOnly.name = "handFront"
for f = 2, 8 do handSpr:newEmptyFrame() end

local compStrip = Image(256 * 8, 256, ColorMode.RGB)
local natStrip = Image(128 * 8, 128, ColorMode.RGB)

for f = 1, 8 do
  local idxStr = string.format("%02d", f - 1)
  local wb = lWepBack:cel(f).image
  local bd = lBody:cel(f).image
  local wf = lWepFront:cel(f).image
  local hf = lHandFront:cel(f).image

  wb:saveAs(string.format("%s/layers/weaponBack/%s.png", outDir, idxStr))
  bd:saveAs(string.format("%s/layers/body/%s.png", outDir, idxStr))
  wf:saveAs(string.format("%s/layers/weaponFront/%s.png", outDir, idxStr))
  hf:saveAs(string.format("%s/layers/handFront/%s.png", outDir, idxStr))

  bodySpr.frames[f].duration = durations[f] / 1000.0
  bodySpr:newCel(lBodyOnly, f, bd, Point(0, 0))

  handSpr.frames[f].duration = durations[f] / 1000.0
  handSpr:newCel(lHandOnly, f, hf, Point(0, 0))

  local flat256 = Image(256, 256, ColorMode.RGB)
  flat256:drawImage(wb, Point(0, 0))
  flat256:drawImage(bd, Point(0, 0))
  flat256:drawImage(wf, Point(0, 0))
  flat256:drawImage(hf, Point(0, 0))

  flat256:saveAs(string.format("%s/%s.png", outDir, idxStr))
  flat256:saveAs(string.format("%s/frames/%s.png", outDir, idxStr))
  compStrip:drawImage(flat256, Point((f - 1) * 256, 0))

  local crop128 = Image(128, 128, ColorMode.RGB)
  for y = 0, 127 do
    for x = 0, 127 do
      local p = bd:getPixel(x + 64, y + 64)
      if app.pixelColor.rgbaA(p) > 0 then
        crop128:drawPixel(x, y, p)
      end
    end
  end
  crop128:saveAs(string.format("%s/native/%s.png", outDir, idxStr))
  natSpr.frames[f].duration = durations[f] / 1000.0
  natSpr:newCel(lNat, f, crop128, Point(0, 0))
  natStrip:drawImage(crop128, Point((f - 1) * 128, 0))
end

bodySpr:saveCopyAs(outDir .. "/source/body.aseprite")
bodySpr:saveCopyAs(outDir .. "/bodyMaster256.aseprite")
bodySpr:close()

handSpr:saveCopyAs(outDir .. "/source/hand.aseprite")
handSpr:saveCopyAs(outDir .. "/handMaster256.aseprite")
handSpr:close()

natSpr:saveCopyAs(outDir .. "/source/native.aseprite")
natSpr:saveCopyAs(outDir .. "/nativeMaster128.aseprite")
natSpr:close()

compStrip:saveAs(outDir .. "/composite-strip.png")
natStrip:saveAs(outDir .. "/native-strip.png")

compSpr:close()
print("SUCCESS_BACK_R_AXE_QA5_REPAIR1")
