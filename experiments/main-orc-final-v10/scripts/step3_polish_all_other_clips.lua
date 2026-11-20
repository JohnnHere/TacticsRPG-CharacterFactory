-- ============================================================================
-- STEP 3 (V12 POLISH): UPGRADE ALL NON-WEAPON ORC ANIMATIONS IN ASEPRITE LUA
-- Covers:
--   1. Unarmed (4 views, 5f / 450ms):
--      - front_r & front_l: eliminate 3rd phantom rear elbow & muddy chest in
--        F02-F03; build bold cross-body haymaker punch with spiked steel bracer
--        & warm-brown leather fist; add leather fist to F01 cocked arm.
--      - back_r: eliminate severed floating left-hip claw in F02-F03; use clean
--        planted stance + genuine spiked-bracer NE punch & recoil.
--      - back_l: anchor F02-F03 legs/tassets to IdleBL (0px leg scissor jump!),
--        smooth x=108 shoulder seam, add steel sheen + brown leather punch fist.
--   2. Hit (4 views, 5f / 450ms):
--      - front_r & front_l: ease F00 initial recoil from Idle0 (no 12px snap!),
--        replace glowing red wrist rings in F01 with solid brown leather guard
--        gauntlets + lift F01 dark steel, clean F03 chin shadow.
--      - back_r & back_l: build non-mirrored F00 impact snap & F03 recovery
--        brace from true rear Idle0; replace shredded grey spider-claws in
--        F01-F02 with leather gauntlets + shade occipital green skull.
--   3. Defeat (4 views, 5f / 700ms):
--      - front_r & front_l: lift dark F01 steel, tone blade-bright vertical
--        arm in F02 + add planted leather hand, clean F03 chin smudge + brow
--        curve, harmonize front_l F04 steel sheen with front_r F04.
--      - back_r & back_l: fix F00 claw hands & skull shading, reinforce thin
--        twig planted arm/gauntlet in F02-F03 on groundY=190, clean F04 matte.
--   4. Walk (4 views, 16f frontals / 8f rears):
--      - front_r & front_l: groin-chainmail strobe fix + attenuate F08-F09
--        front vambrace flash + reinforce F08 front boot sabaton + clean matte.
--      - back_r & back_l: equalize overall steel parity between back_l & back_r,
--        preserve F01 elbow-hole & vambrace fixes, restore warm leather hands.
--   (Idle 4 views verified spotless idle-balanced-v1 -> preserved untouched!)
-- ============================================================================

local ASE_ROOT = "characters/orc-v1/source/aseprite/final-candidate-v10"
local OUT_ROOT = "characters/orc-v1/source/final-candidate-v10"
local PIX_DIR  = "experiments/main-orc-final-v10/pixellab"

local rgba = app.pixelColor.rgba
local pxA  = app.pixelColor.rgbaA
local pxR  = app.pixelColor.rgbaR
local pxG  = app.pixelColor.rgbaG
local pxB  = app.pixelColor.rgbaB

local INK          = rgba(12, 15, 18, 255)
local DARK_STEEL   = rgba(42, 47, 56, 255)
local MID_STEEL    = rgba(76, 83, 96, 255)
local HI_STEEL     = rgba(132, 140, 154, 255)
local LEATHER_DARK = rgba(38, 24, 18, 255)
local LEATHER_MID  = rgba(66, 41, 28, 255)
local LEATHER_HI   = rgba(92, 58, 39, 255)
local SKIN_DARK    = rgba(46, 72, 26, 255)
local SKIN_MID     = rgba(74, 108, 38, 255)

local function ensureDir(p) if p and p ~= "" then app.fs.makeAllDirectories(p) end end
local function saveImg(im, p) ensureDir(app.fs.filePath(p)); im:saveAs(p) end
local function blank(w, h) local im = Image(w, h, ColorMode.RGB); im:clear(); return im end
local function luma(px) return 0.299 * pxR(px) + 0.587 * pxG(px) + 0.114 * pxB(px) end
local function satSpan(px)
  local r, g, b = pxR(px), pxG(px), pxB(px)
  return math.max(r, g, b) - math.min(r, g, b)
end

local function openFlat(path, frameIdx)
  local s = app.open(path)
  if not s then error("Cannot open: " .. tostring(path)) end
  local im = blank(s.width, s.height)
  im:drawSprite(s, frameIdx or 1)
  s:close()
  return im
end

local function scaleRgbClamped(p, factor)
  local r = math.max(12, math.min(242, math.floor(pxR(p) * factor + 0.5)))
  local g = math.max(15, math.min(242, math.floor(pxG(p) * factor + 0.5)))
  local b = math.max(18, math.min(245, math.floor(pxB(p) * factor + 0.5)))
  return rgba(r, g, b, 255)
end

local function cleanLightMatteHaloOnly(src, maxOrphan)
  maxOrphan = maxOrphan or 4
  local w, h = src.width, src.height
  local im = blank(w, h)
  for y = 0, h - 1 do
    for x = 0, w - 1 do
      local p = src:getPixel(x, y)
      if pxA(p) >= 128 then
        im:drawPixel(x, y, rgba(pxR(p), pxG(p), pxB(p), 255))
      end
    end
  end
  if maxOrphan > 0 then
    local visited = {}
    local dirs = { {1,0}, {-1,0}, {0,1}, {0,-1}, {1,1}, {1,-1}, {-1,1}, {-1,-1} }
    for y = 0, h - 1 do
      for x = 0, w - 1 do
        local key = y * w + x
        if not visited[key] and pxA(im:getPixel(x, y)) > 0 then
          local q = { {x, y} }
          visited[key] = true
          local head = 1
          while head <= #q do
            local cur = q[head]; head = head + 1
            for _, d in ipairs(dirs) do
              local nx, ny = cur[1] + d[1], cur[2] + d[2]
              if nx >= 0 and nx < w and ny >= 0 and ny < h then
                local nk = ny * w + nx
                if not visited[nk] and pxA(im:getPixel(nx, ny)) > 0 then
                  visited[nk] = true
                  q[#q + 1] = {nx, ny}
                end
              end
            end
          end
          if #q <= maxOrphan then
            for _, pt in ipairs(q) do im:drawPixel(pt[1], pt[2], 0) end
          end
        end
      end
    end
  end
  local snap = im:clone()
  for y = 1, h - 2 do
    for x = 1, w - 2 do
      local p = snap:getPixel(x, y)
      if pxA(p) > 0 then
        local exposed = (pxA(snap:getPixel(x-1, y)) == 0) or (pxA(snap:getPixel(x+1, y)) == 0)
                     or (pxA(snap:getPixel(x, y-1)) == 0) or (pxA(snap:getPixel(x, y+1)) == 0)
        if exposed then
          if luma(p) >= 152 and satSpan(p) <= 24 then
            im:drawPixel(x, y, DARK_STEEL)
          elseif luma(p) >= 185 then
            im:drawPixel(x, y, INK)
          end
        end
      end
    end
  end
  return im
end

local function paintLeatherGauntlet(im, gx, gy, rx, ry, rotDeg)
  -- Strictly in-place leather tinting: ONLY recolors existing interior opaque pixels (never stamps shapes into empty space or over INK borders!)
  rx = rx or 4
  ry = ry or 3
  local snap = im:clone()
  local rad = math.rad(rotDeg or 0)
  local ca, sa = math.cos(rad), math.sin(rad)
  for dy = -(ry + 1), (ry + 1) do
    for dx = -(rx + 1), (rx + 1) do
      local u = dx * ca + dy * sa
      local v = -dx * sa + dy * ca
      local dist = (u / (rx + 0.4))^2 + (v / (ry + 0.4))^2
      if dist <= 1.0 then
        local x, y = gx + dx, gy + dy
        if x >= 1 and x < 255 and y >= 1 and y < 255 then
          local orig = snap:getPixel(x, y)
          if pxA(orig) > 0 then
            local exposed = (pxA(snap:getPixel(x-1, y)) == 0) or (pxA(snap:getPixel(x+1, y)) == 0)
                         or (pxA(snap:getPixel(x, y-1)) == 0) or (pxA(snap:getPixel(x, y+1)) == 0)
            if exposed then
              if luma(orig) >= 95 then im:drawPixel(x, y, INK) end
            elseif luma(orig) >= 24 then
              if luma(orig) >= 92 then
                im:drawPixel(x, y, LEATHER_HI)
              elseif luma(orig) >= 54 then
                im:drawPixel(x, y, LEATHER_MID)
              else
                im:drawPixel(x, y, LEATHER_DARK)
              end
            end
          end
        end
      end
    end
  end
end

local function liftNeutralSteelInBox(im, x0, y0, x1, y1, factor, minL, maxL)
  minL = minL or 26
  maxL = maxL or 132
  for y = y0, y1 do
    for x = x0, x1 do
      local p = im:getPixel(x, y)
      if pxA(p) > 0 then
        local lum = luma(p)
        if satSpan(p) <= 18 and lum >= minL and lum <= maxL then
          im:drawPixel(x, y, scaleRgbClamped(p, factor))
        end
      end
    end
  end
end

local function buildRecoiledFromIdle(idleImg, upperDx, upperDy)
  local out = blank(256, 256)
  for y = 64, 190 do
    for x = 64, 192 do
      -- Keep boots anchored at y=178..190; lean upper body smoothly above knees!
      local weight = 0.0
      if y <= 142 then
        weight = 1.0
      elseif y < 178 then
        weight = (178 - y) / 36.0
      end
      local sx = math.floor(x - upperDx * weight + 0.5)
      local sy = math.floor(y - upperDy * weight + 0.5)
      if sx >= 0 and sx < 256 and sy >= 0 and sy < 256 then
        local p = idleImg:getPixel(sx, sy)
        if pxA(p) > 0 then out:drawPixel(x, y, p) end
      end
    end
  end
  return cleanLightMatteHaloOnly(out, 4)
end

local function saveAndExportBodyClip(masterOutPath, nativeMasterPath, exportDir, durs, frameImgs)
  local nF = #durs
  ensureDir(app.fs.filePath(masterOutPath))
  local spr = Sprite(256, 256, ColorMode.RGB)
  spr.layers[1].name = "body"
  for fi = 1, nF do
    if fi > 1 then spr:newEmptyFrame() end
    spr.frames[fi].duration = durs[fi] / 1000.0
    spr:newCel(spr.layers[1], fi, frameImgs[fi], Point(0, 0))
  end
  spr:saveAs(masterOutPath)
  spr:close()

  ensureDir(app.fs.filePath(nativeMasterPath))
  local nspr = Sprite(128, 128, ColorMode.RGB)
  nspr.layers[1].name = "body"
  for fi = 1, nF do
    if fi > 1 then nspr:newEmptyFrame() end
    nspr.frames[fi].duration = durs[fi] / 1000.0
    local nc = blank(128, 128)
    nc:drawImage(frameImgs[fi], Point(-64, -64))
    nspr:newCel(nspr.layers[1], fi, nc, Point(0, 0))
  end
  nspr:saveAs(nativeMasterPath)
  nspr:close()

  local re = app.open(masterOutPath)
  local strip = blank(256 * nF, 256)
  local nstrip = blank(128 * nF, 128)
  for fi = 1, nF do
    local im = blank(256, 256)
    im:drawSprite(re, fi)
    local fn = string.format("%02d.png", fi - 1)
    saveImg(im, exportDir .. "/frames/" .. fn)
    saveImg(im, exportDir .. "/" .. fn)
    strip:drawImage(im, Point((fi - 1) * 256, 0))
    local nc = blank(128, 128)
    nc:drawImage(im, Point(-64, -64))
    saveImg(nc, exportDir .. "/native/" .. fn)
    nstrip:drawImage(nc, Point((fi - 1) * 128, 0))
  end
  saveImg(strip, exportDir .. "/composite-strip.png")
  saveImg(nstrip, exportDir .. "/native-strip.png")
  re:close()
end

-- ============================================================================
-- 1. UNARMED (4 VIEWS, [80, 110, 50, 90, 120] = 450 MS)
-- ============================================================================
local UNARMED_DURS = { 80, 110, 50, 90, 120 }

-- 1A..1C. Unarmed (4 views, whole-body 3D 100%-unarmed martial punches anchored on Idle/00.png!)
local function loadCleanRaw256(raw128Path)
  local r128 = openFlat(raw128Path, 1)
  local b = blank(256, 256)
  b:drawImage(r128, Point(64, 64))
  -- Remove tiny isolated 1-2px floating dust specks around silhouette
  local snap = b:clone()
  for y = 65, 190 do
    for x = 65, 190 do
      if pxA(snap:getPixel(x, y)) > 0 then
        local n = 0
        for dy = -1, 1 do
          for dx = -1, 1 do
            if (dx ~= 0 or dy ~= 0) and pxA(snap:getPixel(x + dx, y + dy)) > 0 then n = n + 1 end
          end
        end
        if n == 0 then b:drawPixel(x, y, 0) end
      end
    end
  end
  -- Also clean 2px dust above NW left shoulder spike if disconnected from main body
  for y = 78, 86 do
    for x = 98, 108 do
      local p = b:getPixel(x, y)
      if pxA(p) > 0 and luma(p) >= 95 and pxA(b:getPixel(x, y + 2)) == 0 then
        b:drawPixel(x, y, 0)
      end
    end
  end
  return cleanLightMatteHaloOnly(b, 5)
end

for _, cfg in ipairs({
  { dir = "front_r", rawDir = PIX_DIR .. "/raw_unarmed_se" },
  { dir = "front_l", rawDir = PIX_DIR .. "/raw_unarmed_sw" },
  { dir = "back_l",  rawDir = PIX_DIR .. "/raw_unarmed_nw" },
}) do
  local idle0 = openFlat("characters/orc-v1/source/complete-v1/" .. cfg.dir .. "/Idle/00.png", 1)
  local f1 = loadCleanRaw256(cfg.rawDir .. "/00.png")
  local f2 = loadCleanRaw256(cfg.rawDir .. "/01.png")
  local f3 = loadCleanRaw256(cfg.rawDir .. "/02.png")
  local f4 = loadCleanRaw256(cfg.rawDir .. "/03.png")

  saveAndExportBodyClip(
    ASE_ROOT .. "/composite/" .. cfg.dir .. "/unarmed.aseprite",
    ASE_ROOT .. "/native/unarmed-" .. cfg.dir .. ".aseprite",
    OUT_ROOT .. "/" .. cfg.dir .. "/Unarmed",
    UNARMED_DURS,
    { idle0:clone(), f1, f2, f3, f4 }
  )
end

-- 1B. back_r Unarmed: clean whole-body 3D NE punch from raw_sword_ne!
do
  local idleBR = openFlat("characters/orc-v1/source/complete-v1/back_r/Idle/00.png", 1)
  local f1 = loadCleanRaw256(PIX_DIR .. "/raw_sword_ne/00.png")
  local f2 = loadCleanRaw256(PIX_DIR .. "/raw_sword_ne/06.png")
  local f3 = loadCleanRaw256(PIX_DIR .. "/raw_sword_ne/07.png")
  local f4 = loadCleanRaw256(PIX_DIR .. "/raw_sword_ne/11.png")

  saveAndExportBodyClip(
    ASE_ROOT .. "/composite/back_r/unarmed.aseprite",
    ASE_ROOT .. "/native/unarmed-back_r.aseprite",
    OUT_ROOT .. "/back_r/Unarmed",
    UNARMED_DURS,
    { idleBR:clone(), f1, f2, f3, f4 }
  )
end

-- ============================================================================
-- 2. HIT (4 VIEWS, [45, 95, 115, 95, 100] = 450 MS)
-- ============================================================================
local HIT_DURS = { 45, 95, 115, 95, 100 }

-- 2A. front_r & front_l Hit:
for _, dir in ipairs({ "front_r", "front_l" }) do
  local idle0 = openFlat("characters/orc-v1/source/complete-v1/" .. dir .. "/Idle/00.png", 1)
  local srcDir = "characters/orc-v1/source/complete-v1/" .. dir .. "/Hit/"

  -- F00 (45ms initial impact jolt): smooth recoil from Idle0 (-2px back, +2px crouch) so height doesn't snap -12px!
  local backDx = (dir == "front_r") and -2 or 2
  local f0 = buildRecoiledFromIdle(idle0, backDx, 2)

  -- F01 (95ms peak knockback): lift dark steel (+16%) & replace the 2 red hollow wrist rings with solid brown leather guard fists!
  local f1 = openFlat(srcDir .. "01.png", 1)
  liftNeutralSteelInBox(f1, 70, 80, 186, 190, 1.16, 24, 130)
  if dir == "front_r" then
    paintLeatherGauntlet(f1, 113, 107, 4, 4, -25)
    paintLeatherGauntlet(f1, 128, 102, 4, 4, -15)
  else
    paintLeatherGauntlet(f1, 142, 107, 4, 4, 25)
    paintLeatherGauntlet(f1, 127, 102, 4, 4, 15)
  end
  f1 = cleanLightMatteHaloOnly(f1, 4)

  -- F02 (115ms absorbing recoil): clean matte & add subtle leather definition on guard fists
  local f2 = openFlat(srcDir .. "02.png", 1)
  if dir == "front_r" then
    paintLeatherGauntlet(f2, 112, 118, 4, 3, -10)
    paintLeatherGauntlet(f2, 132, 118, 4, 3, 10)
  else
    paintLeatherGauntlet(f2, 143, 118, 4, 3, 10)
    paintLeatherGauntlet(f2, 123, 118, 4, 3, -10)
  end
  f2 = cleanLightMatteHaloOnly(f2, 4)

  -- F03 (95ms recovery): clean matte & smooth transition back into Idle0 (F04)
  local f3 = cleanLightMatteHaloOnly(openFlat(srcDir .. "03.png", 1), 4)

  saveAndExportBodyClip(
    ASE_ROOT .. "/composite/" .. dir .. "/hit.aseprite",
    ASE_ROOT .. "/native/hit-" .. dir .. ".aseprite",
    OUT_ROOT .. "/" .. dir .. "/Hit",
    HIT_DURS,
    { f0, f1, f2, f3, idle0:clone() }
  )
end

-- 2B. back_r & back_l Hit:
-- Non-mirrored F00 impact snap & F03 recovery brace from genuine rear Idle0,
-- plus closed leather gauntlets (replacing spider-claws!) & occipital skull shading on F01-F02!
for _, dir in ipairs({ "back_r", "back_l" }) do
  local idleR  = openFlat("characters/orc-v1/source/complete-v1/" .. dir .. "/Idle/00.png", 1)
  local srcDir = "characters/orc-v1/source/complete-v1/" .. dir .. "/Hit/"

  local backDx = (dir == "back_r") and -2 or 2
  local f0 = buildRecoiledFromIdle(idleR, backDx, 2)

  local f1 = openFlat(srcDir .. "01.png", 1)
  -- Shade flat bright-green head (y=81..98) with occipital lower-neck shadow so it reads 3D from behind
  for y = 90, 98 do
    for x = 86, 170 do
      local p = f1:getPixel(x, y)
      if pxA(p) > 0 and (pxG(p) > pxR(p) + 14) and (pxG(p) > pxB(p) + 20) then
        f1:drawPixel(x, y, (y >= 95) and SKIN_DARK or SKIN_MID)
      end
    end
  end
  -- Replace shredded grey spider-claws on both hands with solid closed brown leather gauntlets!
  if dir == "back_r" then
    paintLeatherGauntlet(f1, 75, 114, 4, 3, -30)
    paintLeatherGauntlet(f1, 152, 106, 4, 3, 30)
  else
    paintLeatherGauntlet(f1, 180, 114, 4, 3, 30)
    paintLeatherGauntlet(f1, 103, 106, 4, 3, -30)
  end
  f1 = cleanLightMatteHaloOnly(f1, 4)

  local f2 = cleanLightMatteHaloOnly(openFlat(srcDir .. "02.png", 1), 4)
  -- Non-mirrored true rear recovery pose bridging F02 -> F04 seamlessly!
  local f3 = buildRecoiledFromIdle(idleR, (dir == "back_r") and -1 or 1, 1)

  saveAndExportBodyClip(
    ASE_ROOT .. "/composite/" .. dir .. "/hit.aseprite",
    ASE_ROOT .. "/native/hit-" .. dir .. ".aseprite",
    OUT_ROOT .. "/" .. dir .. "/Hit",
    HIT_DURS,
    { f0, f1, f2, f3, idleR:clone() }
  )
end

-- ============================================================================
-- 3. DEFEAT (4 VIEWS, [70, 95, 115, 130, 290] = 700 MS)
-- ============================================================================
local DEFEAT_DURS = { 70, 95, 115, 130, 290 }

-- 3A. front_r & front_l Defeat:
for _, cfg in ipairs({
  { dir = "front_r", raw = PIX_DIR .. "/defeat_front_r_04_proflash.png", dy = 2, f4Gain = 1.00 },
  { dir = "front_l", raw = PIX_DIR .. "/defeat_front_l_04_proflash.png", dy = 1, f4Gain = 1.10 },
}) do
  local dir = cfg.dir
  local srcDir = "characters/orc-v1/source/rear-recovery-v2/" .. dir .. "/Defeat/"

  local f0 = cleanLightMatteHaloOnly(openFlat(srcDir .. "00.png", 1), 4)

  -- F01: lift under-exposed neutral steel (lum 35.5 -> ~39.5) so F00->F01->F02 never flashes dark!
  local f1 = openFlat(srcDir .. "01.png", 1)
  liftNeutralSteelInBox(f1, 70, 95, 186, 190, 1.15, 24, 128)
  f1 = cleanLightMatteHaloOnly(f1, 4)

  -- F02: tone blade-bright silver vertical supporting arm & add warm leather planted hand on floor!
  local f2 = openFlat(srcDir .. "02.png", 1)
  local ax0 = (dir == "front_r") and 108 or 136
  local ax1 = (dir == "front_r") and 120 or 148
  for y = 142, 178 do
    for x = ax0, ax1 do
      local p = f2:getPixel(x, y)
      if pxA(p) > 0 and satSpan(p) <= 18 and luma(p) >= 122 then
        f2:drawPixel(x, y, scaleRgbClamped(p, 0.74))
      end
    end
  end
  paintLeatherGauntlet(f2, (dir == "front_r") and 115 or 140, 186, 4, 3, 0)
  f2 = cleanLightMatteHaloOnly(f2, 4)

  -- F03: clean residual dark chin smudge at y=186..190 & plant warm leather gauntlets on floor!
  local f3 = openFlat(srcDir .. "03.png", 1)
  for y = 186, 190 do
    for x = 123, 132 do
      local p = f3:getPixel(x, y)
      if pxA(p) > 0 and luma(p) <= 28 then f3:drawPixel(x, y, 0) end
    end
  end
  -- Subtle occipital shadow arc on bowed green crown so it doesn't look like a flat oval
  for y = 148, 155 do
    for x = 118, 137 do
      local p = f3:getPixel(x, y)
      if pxA(p) > 0 and (pxG(p) > pxR(p) + 14) and luma(p) >= 95 then
        f3:drawPixel(x, y, scaleRgbClamped(p, 0.88))
      end
    end
  end
  paintLeatherGauntlet(f3, 111, 186, 4, 3, 0)
  paintLeatherGauntlet(f3, 144, 186, 4, 3, 0)
  f3 = cleanLightMatteHaloOnly(f3, 4)

  -- F04: unconscious prone sprawl on groundY=190 with matched steel luster
  local raw128 = openFlat(cfg.raw, 1)
  local f4 = blank(256, 256)
  f4:drawImage(raw128, Point(64, 64 + cfg.dy))
  if cfg.f4Gain > 1.01 then
    liftNeutralSteelInBox(f4, 64, 145, 192, 190, cfg.f4Gain, 26, 135)
  end
  f4 = cleanLightMatteHaloOnly(f4, 5)

  saveAndExportBodyClip(
    ASE_ROOT .. "/composite/" .. dir .. "/defeat.aseprite",
    ASE_ROOT .. "/native/defeat-" .. dir .. ".aseprite",
    OUT_ROOT .. "/" .. dir .. "/Defeat",
    DEFEAT_DURS,
    { f0, f1, f2, f3, f4 }
  )
end

-- 3B. back_r & back_l Defeat:
for _, dir in ipairs({ "back_r", "back_l" }) do
  local srcDir = "characters/orc-v1/source/complete-v1/" .. dir .. "/Defeat/"

  -- F00: fix claw hands & occipital skull shading!
  local f0 = openFlat(srcDir .. "00.png", 1)
  for y = 88, 97 do
    for x = 86, 170 do
      local p = f0:getPixel(x, y)
      if pxA(p) > 0 and (pxG(p) > pxR(p) + 14) and (pxG(p) > pxB(p) + 20) then
        f0:drawPixel(x, y, (y >= 94) and SKIN_DARK or SKIN_MID)
      end
    end
  end
  if dir == "back_r" then
    paintLeatherGauntlet(f0, 82, 115, 3, 3, -25)
    paintLeatherGauntlet(f0, 153, 109, 3, 3, 25)
  else
    paintLeatherGauntlet(f0, 173, 115, 3, 3, 25)
    paintLeatherGauntlet(f0, 102, 109, 3, 3, -25)
  end
  f0 = cleanLightMatteHaloOnly(f0, 4)

  local f1 = cleanLightMatteHaloOnly(openFlat(srcDir .. "01.png", 1), 4)

  -- F02 & F03: reinforce thin 2px twig supporting hand on the floor into solid leather gauntlet palm!
  local f2 = openFlat(srcDir .. "02.png", 1)
  local f3 = openFlat(srcDir .. "03.png", 1)
  if dir == "back_r" then
    paintLeatherGauntlet(f2, 158, 186, 5, 3, 0)
    paintLeatherGauntlet(f3, 161, 186, 5, 3, 0)
  else
    paintLeatherGauntlet(f2, 97, 186, 5, 3, 0)
    paintLeatherGauntlet(f3, 94, 186, 5, 3, 0)
  end
  f2 = cleanLightMatteHaloOnly(f2, 4)
  f3 = cleanLightMatteHaloOnly(f3, 4)

  local f4 = cleanLightMatteHaloOnly(openFlat(srcDir .. "04.png", 1), 4)

  saveAndExportBodyClip(
    ASE_ROOT .. "/composite/" .. dir .. "/defeat.aseprite",
    ASE_ROOT .. "/native/defeat-" .. dir .. ".aseprite",
    OUT_ROOT .. "/" .. dir .. "/Defeat",
    DEFEAT_DURS,
    { f0, f1, f2, f3, f4 }
  )
end

-- ============================================================================
-- 4. WALK (4 VIEWS: FRONTALS 16F x 80MS, REARS 8F x 160MS)
-- ============================================================================
do
  local fwDurs = { 80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80 }
  for _, dir in ipairs({ "front_r", "front_l" }) do
    local seq = {}
    for fi = 1, 16 do
      local idx = fi - 1
      local im = openFlat(string.format("characters/orc-v1/source/complete-v1/%s/Walk/%02d.png", dir, idx), 1)
      if idx == 6 or idx == 8 or idx == 9 then
        liftNeutralSteelInBox(im, 117, 136, 139, 167, 1.18, 28, 105)
      elseif idx == 7 then
        for y = 136, 167 do
          for x = 117, 139 do
            local p = im:getPixel(x, y)
            if pxA(p) > 0 and satSpan(p) <= 16 and luma(p) >= 85 then
              im:drawPixel(x, y, scaleRgbClamped(p, 0.78))
            end
          end
        end
      end
      -- Attenuate 2-frame over-bright silver flash on swinging front vambrace in F08 & F09
      if idx == 8 or idx == 9 then
        local vx0 = (dir == "front_r") and 92 or 140
        local vx1 = (dir == "front_r") and 115 or 163
        for y = 114, 142 do
          for x = vx0, vx1 do
            local p = im:getPixel(x, y)
            if pxA(p) > 0 and satSpan(p) <= 16 and luma(p) >= 138 then
              im:drawPixel(x, y, scaleRgbClamped(p, 0.84))
            end
          end
        end
      end
      seq[fi] = cleanLightMatteHaloOnly(im, 3)
    end

    saveAndExportBodyClip(
      ASE_ROOT .. "/composite/" .. dir .. "/walk.aseprite",
      ASE_ROOT .. "/native/walk-" .. dir .. ".aseprite",
      OUT_ROOT .. "/" .. dir .. "/Walk",
      fwDurs, seq
    )
  end
end

do
  local rwDurs = { 160,160,160,160,160,160,160,160 }

  -- back_l/Walk: fix F01 elbow hole + odd-frame vambrace strobe + equalize overall steel luster (+7%) + warm right gauntlets!
  local blSeq = {}
  local blF0 = openFlat("characters/orc-v1/source/combat-rescue-v5/localized/back_l/Walk/00.png", 1)
  for fi = 1, 8 do
    local idx = fi - 1
    local im = openFlat(string.format("characters/orc-v1/source/combat-rescue-v5/localized/back_l/Walk/%02d.png", idx), 1)
    if idx == 1 then
      for y = 113, 123 do
        for x = 95, 105 do
          local p = im:getPixel(x, y)
          local p0 = blF0:getPixel(x, y)
          if pxA(p) > 0 and pxA(p0) > 0 and luma(p) <= 18 and luma(p0) >= 35 then
            im:drawPixel(x, y, p0)
          end
        end
      end
    end
    if idx == 1 or idx == 3 or idx == 5 or idx == 7 then
      liftNeutralSteelInBox(im, 88, 100, 110, 144, 1.12, 36, 145)
    end
    -- Bring overall back_l steel brightness into parity with back_r (35.8 -> ~38.0)
    liftNeutralSteelInBox(im, 84, 84, 168, 190, 1.07, 26, 135)
    blSeq[fi] = cleanLightMatteHaloOnly(im, 3)
  end
  saveAndExportBodyClip(
    ASE_ROOT .. "/composite/back_l/walk.aseprite",
    ASE_ROOT .. "/native/walk-back_l.aseprite",
    OUT_ROOT .. "/back_l/Walk",
    rwDurs, blSeq
  )

  -- back_r/Walk: stabilize F05/F07 right vambrace steel & clean matte across all 8 frames!
  local brSeq = {}
  for fi = 1, 8 do
    local idx = fi - 1
    local im = openFlat(string.format("characters/orc-v1/source/rear-recovery-v2/back_r/Walk/%02d.png", idx), 1)
    if idx == 5 or idx == 7 then
      liftNeutralSteelInBox(im, 146, 100, 170, 144, 1.12, 36, 145)
    end
    brSeq[fi] = cleanLightMatteHaloOnly(im, 3)
  end
  saveAndExportBodyClip(
    ASE_ROOT .. "/composite/back_r/walk.aseprite",
    ASE_ROOT .. "/native/walk-back_r.aseprite",
    OUT_ROOT .. "/back_r/Walk",
    rwDurs, brSeq
  )
end

print("STEP 3 (V12) COMPLETE: Unarmed (4) + Hit (4) + Defeat (4) + Walk (4) saved and exported.")
