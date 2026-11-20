-- ============================================================================
-- STEP 2 (V11 POLISH): CLEANED MILITIA-AXE + 4-VIEW AXE ATTACK + UNARMED/WALK/DEFEAT
-- ============================================================================

local ASE_ROOT   = "characters/orc-v1/source/aseprite/final-candidate-v10"
local OUT_ROOT   = "characters/orc-v1/source/final-candidate-v10"
local NW_AXE_RAW = "experiments/main-orc-final-v10/pixellab/raw_axe_nw"
local NE_AXE_RAW = "experiments/main-orc-final-v10/pixellab/raw_axe_ne"
local PIX_DIR    = "experiments/main-orc-final-v10/pixellab"

local rgba = app.pixelColor.rgba
local pxA  = app.pixelColor.rgbaA
local pxR  = app.pixelColor.rgbaR
local pxG  = app.pixelColor.rgbaG
local pxB  = app.pixelColor.rgbaB

local INK          = rgba(12, 15, 18, 255)
local DARK_SHADOW  = rgba(24, 27, 33, 255)
local DARK_STEEL   = rgba(42, 47, 56, 255)
local MID_STEEL    = rgba(76, 83, 96, 255)
local HI_STEEL     = rgba(132, 140, 154, 255)
local DARK_CLOTH   = rgba(52, 24, 24, 255)
local RED_TRIM     = rgba(126, 38, 34, 255)
local LEATHER_DARK = rgba(58, 35, 24, 255)
local LEATHER_MID  = rgba(94, 57, 38, 255)
local LEATHER_HI   = rgba(126, 79, 52, 255)

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

local function openLayer(path, layerName, frameIdx)
  local s = app.open(path)
  if not s then error("Cannot open master: " .. tostring(path)) end
  local im = blank(s.width, s.height)
  for _, l in ipairs(s.layers) do
    if l.name == layerName then
      local c = l:cel(frameIdx or 1)
      if c then im:drawImage(c.image, c.position) end
      s:close()
      return im
    end
  end
  s:close()
  error("Layer " .. layerName .. " not found in " .. path)
end

-- Remove tiny floating orphans (<= maxOrphan px) + neutral bright matte halo ONLY (preserves 1px INK & spikes!)
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

local function paintBodyLeatherFist(b, gx, gy, rotDeg, rx, ry)
  rx = rx or 4
  ry = ry or 3
  local rad = math.rad(rotDeg or 0)
  local ca, sa = math.cos(rad), math.sin(rad)
  for dy = -(ry + 2), (ry + 2) do
    for dx = -(rx + 2), (rx + 2) do
      local u = dx * ca + dy * sa
      local v = -dx * sa + dy * ca
      local dist = (u / (rx + 0.4)) ^ 2 + (v / (ry + 0.4)) ^ 2
      if dist <= 1.0 then
        local x, y = gx + dx, gy + dy
        if x >= 1 and x < 255 and y >= 1 and y < 255 then
          if dist >= 0.70 then
            b:drawPixel(x, y, INK)
          elseif v < -0.7 or u < -1.2 then
            b:drawPixel(x, y, LEATHER_HI)
          elseif math.floor(v + 3.5) % 2 == 0 and u > -0.8 and u < 1.8 then
            b:drawPixel(x, y, LEATHER_MID)
          else
            b:drawPixel(x, y, LEATHER_DARK)
          end
        end
      end
    end
  end
end

local function buildSculptedHandFront(bodyImg, gx, gy, rotDeg, style)
  local hf = blank(256, 256)
  local rad = math.rad(rotDeg or 0)
  local ca, sa = math.cos(rad), math.sin(rad)

  if style == "frontal_fingers" then
    for dy = -6, 6 do
      for dx = -6, 6 do
        local u = dx * ca + dy * sa
        local v = -dx * sa + dy * ca
        local inFingers = (math.abs(u) <= 2.9 and v >= -3.0 and v <= 3.5 and ((u / 3.1)^2 + (v / 3.7)^2 <= 1.0))
        if inFingers then
          local x, y = gx + dx, gy + dy
          local edge = (math.abs(u) >= 2.1) or (v <= -2.2) or (v >= 2.7)
          if edge then
            hf:drawPixel(x, y, INK)
          else
            local groove = (math.abs((v + 3.0) % 1.8) < 0.55)
            if u < -0.6 and not groove then
              hf:drawPixel(x, y, LEATHER_HI)
            elseif groove then
              hf:drawPixel(x, y, LEATHER_DARK)
            else
              hf:drawPixel(x, y, LEATHER_MID)
            end
          end
        end
      end
    end
  elseif style == "rear_dorsal" then
    for dy = -6, 6 do
      for dx = -6, 6 do
        local u = dx * ca + dy * sa
        local v = -dx * sa + dy * ca
        local dist = (u / 4.2)^2 + (v / 3.8)^2
        if dist <= 1.0 then
          local x, y = gx + dx, gy + dy
          local pb = bodyImg:getPixel(x, y)
          if dist >= 0.72 then
            hf:drawPixel(x, y, INK)
          elseif pxA(pb) > 0 and ((pxR(pb) - pxB(pb)) >= 18 and pxR(pb) >= 52) then
            hf:drawPixel(x, y, pb)
          elseif v < -0.6 then
            hf:drawPixel(x, y, LEATHER_HI)
          elseif u < 0.8 then
            hf:drawPixel(x, y, LEATHER_MID)
          else
            hf:drawPixel(x, y, LEATHER_DARK)
          end
        end
      end
    end
  end
  return hf
end

local function drawArmouredForearm(img, x1, y1, x2, y2, radius)
  local steps = math.max(math.abs(x2 - x1), math.abs(y2 - y1), 1)
  local dx = (x2 - x1) / steps
  local dy = (y2 - y1) / steps
  local len = math.sqrt((x2 - x1)^2 + (y2 - y1)^2)
  local nx = (len > 0) and (-(y2 - y1) / len) or 0
  local ny = (len > 0) and ((x2 - x1) / len) or 1
  for s = 0, steps do
    local cx = x1 + dx * s
    local cy = y1 + dy * s
    local t = s / steps
    for r = -radius, radius do
      local px = math.floor(cx + nx * r + 0.5)
      local py = math.floor(cy + ny * r + 0.5)
      if math.abs(r) >= radius - 0.3 then
        img:drawPixel(px, py, INK)
      elseif t > 0.25 and t < 0.38 and math.abs(r) <= radius - 1 then
        img:drawPixel(px, py, RED_TRIM)
      elseif r < -0.5 then
        img:drawPixel(px, py, HI_STEEL)
      elseif r < 1.2 then
        img:drawPixel(px, py, MID_STEEL)
      else
        img:drawPixel(px, py, DARK_STEEL)
      end
    end
  end
end

-- ============================================================================
-- PART 0: CLEAN & SAVE MILITIA-AXE MASTER (96x96, pivot [35, 48])
-- ============================================================================
local axeImg
do
  local rawAxe = openFlat("characters/orc-v1/source/combat-rescue-v5/combat/weapons/Axe/militia-axe.png", 1)
  -- Remove orphan pixel (37,24) and any 1px stray speck
  rawAxe:drawPixel(37, 24, 0)
  -- Reinforce iron collar binding at (40..46, 33..35)
  rawAxe:drawPixel(41, 34, MID_STEEL)
  rawAxe:drawPixel(42, 34, HI_STEEL)
  local axeMaster = ASE_ROOT .. "/weapons/militia-axe.aseprite"
  ensureDir(app.fs.filePath(axeMaster))
  local s = Sprite(96, 96, ColorMode.RGB)
  s.layers[1].name = "weapon"
  s:newCel(s.layers[1], 1, rawAxe, Point(0, 0))
  s:saveAs(axeMaster)
  s:close()
  local re = app.open(axeMaster)
  axeImg = blank(96, 96)
  axeImg:drawSprite(re, 1)
  re:close()
  saveImg(axeImg, OUT_ROOT .. "/weapons/Axe/militia-axe.png")
end

-- ============================================================================
-- PART 1: AXE ATTACK (4 VIEWS, 12 FRAMES, 1005 MS, CONTACT F06 @ 410 MS)
-- ============================================================================
local AXE_DURS = { 40, 65, 35, 80, 155, 35, 115, 110, 130, 50, 90, 100 }

local function composeAxeLayers(wImg, gx, gy, rotDeg, flipBlade, mode)
  local wb = blank(256, 256)
  local wf = blank(256, 256)
  local full = blank(256, 256)
  local vMap = {}

  local rad = math.rad(rotDeg)
  local ca, sa = math.cos(rad), math.sin(rad)
  local pivU, pivV = 38.0, 45.0

  local x0 = math.max(1, gx - 68)
  local x1 = math.min(254, gx + 68)
  local y0 = math.max(1, gy - 68)
  local y1 = math.min(254, gy + 68)

  for y = y0, y1 do
    for x = x0, x1 do
      local dx, dy = x - gx, y - gy
      local rx = dx * ca + dy * sa
      local ry = -dx * sa + dy * ca
      local u = flipBlade and math.floor(pivU - rx + 0.5) or math.floor(pivU + rx + 0.5)
      local v = math.floor(pivV + ry + 0.5)
      if u >= 0 and u < 96 and v >= 0 and v < 96 then
        local p = wImg:getPixel(u, v)
        if pxA(p) > 0 then
          full:drawPixel(x, y, rgba(pxR(p), pxG(p), pxB(p), 255))
          vMap[y * 256 + x] = v
        end
      end
    end
  end

  local snap = full:clone()
  for y = y0, y1 do
    for x = x0, x1 do
      local p = snap:getPixel(x, y)
      if pxA(p) > 0 then
        local exposed = (pxA(snap:getPixel(x-1,y))==0) or (pxA(snap:getPixel(x+1,y))==0)
                     or (pxA(snap:getPixel(x,y-1))==0) or (pxA(snap:getPixel(x,y+1))==0)
        if exposed and luma(p) >= 150 then
          full:drawPixel(x, y, INK)
        end
      end
    end
  end

  for y = y0, y1 do
    for x = x0, x1 do
      local p = full:getPixel(x, y)
      if pxA(p) > 0 then
        local v = vMap[y * 256 + x] or 0
        if mode == "all_back" then
          wb:drawPixel(x, y, p)
        elseif mode == "rear_dorsal" then
          -- Upper haft + axe head + gripped core (v <= 49) stay behind dorsal arm/back (wb);
          -- wooden butt-cap (v >= 50) peeks cleanly out at pinky base (wf, outside torso x=106..148)!
          if v >= 50 and (x < 106 or x > 148) then
            wf:drawPixel(x, y, p)
          else
            wb:drawPixel(x, y, p)
          end
        else
          -- "front_grip": upper haft + iron head (v <= 41) and wooden butt-cap (v >= 49) in weaponFront;
          -- gripped haft core (v = 42..48) in weaponBack, wrapped by sculpted leather fingers in handFront!
          if v >= 42 and v <= 48 then
            wb:drawPixel(x, y, p)
          else
            wf:drawPixel(x, y, p)
          end
        end
      end
    end
  end

  return wb, wf
end

local function saveAndExport4LayerClip(masterOutPath, nativeMasterPath, exportDir, durs, wbList, bodyList, wfList, hfList)
  local nF = #durs
  ensureDir(app.fs.filePath(masterOutPath))
  local spr = Sprite(256, 256, ColorMode.RGB)
  local names = { "weaponBack", "body", "weaponFront", "handFront" }
  local lyrs = {}
  for i, n in ipairs(names) do
    local l = (i == 1) and spr.layers[1] or spr:newLayer()
    l.name = n
    lyrs[n] = l
  end
  for fi = 1, nF do
    if fi > 1 then spr:newEmptyFrame() end
    spr.frames[fi].duration = durs[fi] / 1000.0
    spr:newCel(lyrs.weaponBack, fi, wbList[fi] or blank(256,256), Point(0,0))
    spr:newCel(lyrs.body, fi, bodyList[fi], Point(0,0))
    spr:newCel(lyrs.weaponFront, fi, wfList[fi] or blank(256,256), Point(0,0))
    spr:newCel(lyrs.handFront, fi, hfList[fi] or blank(256,256), Point(0,0))
  end
  spr:saveAs(masterOutPath)
  spr:close()

  if nativeMasterPath then
    ensureDir(app.fs.filePath(nativeMasterPath))
    local nspr = Sprite(128, 128, ColorMode.RGB)
    nspr.layers[1].name = "body"
    for fi = 1, nF do
      if fi > 1 then nspr:newEmptyFrame() end
      nspr.frames[fi].duration = durs[fi] / 1000.0
      local nc = blank(128, 128)
      nc:drawImage(bodyList[fi], Point(-64, -64))
      nspr:newCel(nspr.layers[1], fi, nc, Point(0,0))
    end
    nspr:saveAs(nativeMasterPath)
    nspr:close()
  end

  local re = app.open(masterOutPath)
  local lMap = {}
  for _, l in ipairs(re.layers) do lMap[l.name] = l end

  local function expSub(vWb, vB, vWf, vHf, subDir, stripName, natDir, natStripName)
    lMap.weaponBack.isVisible = vWb
    lMap.body.isVisible = vB
    lMap.weaponFront.isVisible = vWf
    lMap.handFront.isVisible = vHf
    local strip = stripName and blank(256 * nF, 256) or nil
    local nstrip = natStripName and blank(128 * nF, 128) or nil
    for fi = 1, nF do
      local im = blank(256, 256)
      im:drawSprite(re, fi)
      local fn = string.format("%02d.png", fi - 1)
      saveImg(im, exportDir .. "/" .. subDir .. "/" .. fn)
      if strip then strip:drawImage(im, Point((fi - 1) * 256, 0)) end
      if natDir then
        local nc = blank(128, 128)
        nc:drawImage(im, Point(-64, -64))
        saveImg(nc, exportDir .. "/" .. natDir .. "/" .. fn)
        if nstrip then nstrip:drawImage(nc, Point((fi - 1) * 128, 0)) end
      end
    end
    if strip then saveImg(strip, exportDir .. "/" .. stripName) end
    if nstrip then saveImg(nstrip, exportDir .. "/" .. natStripName) end
  end

  expSub(true, true, true, true, "frames", "composite-strip.png", nil, nil)
  expSub(false, true, false, false, "layers/body", nil, "native", "native-strip.png")
  expSub(false, true, false, true, "body-only", nil, nil, nil)
  expSub(true, false, true, false, "weapon-only", nil, nil, nil)
  expSub(true, false, false, false, "layers/weaponBack", nil, nil, nil)
  expSub(false, false, true, false, "layers/weaponFront", nil, nil, nil)
  expSub(false, false, false, true, "layers/handFront", nil, nil, nil)
  re:close()
end

-- 1A. Frontal Axes (front_r & front_l): true fist grip lock + sculpted leather fingers + F05 chestplate & F09 scar fixes!
local FRONT_AXE_META = {
  front_r = {
    { vis = false },
    { vis = false },
    { vis = true, gx = 99,  gy = 128, rot = 304, flip = false, mode = "front_grip", hf = "frontal_fingers" },
    { vis = true, gx = 88,  gy = 120, rot = 324, flip = false, mode = "front_grip", hf = "frontal_fingers" },
    { vis = true, gx = 86,  gy = 108, rot = 346, flip = false, mode = "front_grip", hf = "frontal_fingers" },
    { vis = true, gx = 154, gy = 112, rot = 64,  flip = false, mode = "front_grip", hf = "frontal_fingers" },
    { vis = true, gx = 150, gy = 141, rot = 118, flip = false, mode = "front_grip", hf = "frontal_fingers" },
    { vis = true, gx = 141, gy = 146, rot = 106, flip = false, mode = "front_grip", hf = "frontal_fingers" },
    { vis = true, gx = 135, gy = 142, rot = 96,  flip = false, mode = "front_grip", hf = "frontal_fingers" },
    { vis = false },
    { vis = false },
    { vis = false },
  },
  front_l = {
    { vis = false },
    { vis = false },
    { vis = true, gx = 156, gy = 128, rot = 56,  flip = true, mode = "front_grip", hf = "frontal_fingers" },
    { vis = true, gx = 167, gy = 120, rot = 36,  flip = true, mode = "front_grip", hf = "frontal_fingers" },
    { vis = true, gx = 169, gy = 108, rot = 14,  flip = true, mode = "front_grip", hf = "frontal_fingers" },
    { vis = true, gx = 101, gy = 112, rot = 296, flip = true, mode = "front_grip", hf = "frontal_fingers" },
    { vis = true, gx = 105, gy = 141, rot = 242, flip = true, mode = "front_grip", hf = "frontal_fingers" },
    { vis = true, gx = 114, gy = 146, rot = 254, flip = true, mode = "front_grip", hf = "frontal_fingers" },
    { vis = true, gx = 120, gy = 142, rot = 264, flip = true, mode = "front_grip", hf = "frontal_fingers" },
    { vis = false },
    { vis = false },
    { vis = false },
  },
}

for _, dir in ipairs({ "front_r", "front_l" }) do
  local srcMaster = "characters/orc-v1/source/artistic-reconstruction-v6/frontal/" .. dir .. "-Axe-full/source/composite.aseprite"
  local swdV11Body7 = openFlat(OUT_ROOT .. "/" .. dir .. "/Sword/layers/body/07.png", 1) -- repaired F07 crossing body!
  local idle0 = openFlat("characters/orc-v1/source/complete-v1/" .. dir .. "/Idle/00.png", 1)
  local metaList = FRONT_AXE_META[dir]
  local wbs, bodies, wfs, hfs = {}, {}, {}, {}

  for fi = 1, 12 do
    local idx = fi - 1
    if idx == 0 or idx == 11 then
      bodies[fi] = idle0:clone()
      wbs[fi], wfs[fi], hfs[fi] = blank(256,256), blank(256,256), blank(256,256)
    else
      local b = openLayer(srcMaster, "body", fi)

      if idx == 3 or idx == 4 then
        if dir == "front_r" then
          for y = 72, 83 do for x = 92, 118 do if pxA(b:getPixel(x,y)) > 0 and luma(b:getPixel(x,y)) >= 70 then b:drawPixel(x,y,0) end end end
          for y = 108, 124 do for x = 99, 111 do if pxA(b:getPixel(x,y)) > 0 and luma(b:getPixel(x,y)) >= 82 then b:drawPixel(x,y, (y<=114) and DARK_SHADOW or DARK_CLOTH) end end end
        else
          for y = 72, 83 do for x = 138, 164 do if pxA(b:getPixel(x,y)) > 0 and luma(b:getPixel(x,y)) >= 70 then b:drawPixel(x,y,0) end end end
          for y = 108, 124 do for x = 144, 156 do if pxA(b:getPixel(x,y)) > 0 and luma(b:getPixel(x,y)) >= 82 then b:drawPixel(x,y, (y<=114) and DARK_SHADOW or DARK_CLOTH) end end end
        end
      elseif idx == 5 then
        -- Replace muddy charcoal chestplate of Axe F05 with repaired crossing body from Sword F07!
        b = swdV11Body7:clone()
      elseif idx >= 6 and idx <= 8 then
        -- Clean any tiny old haft smudge outside outer thigh contour before recomposing clean axe
        if dir == "front_r" then
          for y = 145, 164 do for x = 152, 168 do b:drawPixel(x, y, 0) end end
        else
          for y = 145, 164 do for x = 87, 103 do b:drawPixel(x, y, 0) end end
        end
      elseif idx == 9 or idx == 10 then
        -- Completely replace diagonal white/red gash scar across central breastplate (x=113..143, y=96..138) from Idle F00!
        for y = 96, 138 do
          for x = 113, 143 do
            local p0 = idle0:getPixel(x, y)
            if pxA(p0) > 0 then b:drawPixel(x, y, p0) end
          end
        end
      end

      local m = metaList[fi]
      if m.vis then
        paintBodyLeatherFist(b, m.gx, m.gy, m.rot, 3, 3)
      end
      b = cleanLightMatteHaloOnly(b, 4)
      bodies[fi] = b

      if m.vis then
        wbs[fi], wfs[fi] = composeAxeLayers(axeImg, m.gx, m.gy, m.rot, m.flip, m.mode)
        hfs[fi] = buildSculptedHandFront(b, m.gx, m.gy, m.rot, m.hf)
      else
        wbs[fi], wfs[fi], hfs[fi] = blank(256,256), blank(256,256), blank(256,256)
      end
    end
  end

  saveAndExport4LayerClip(
    ASE_ROOT .. "/composite/" .. dir .. "/axe.aseprite",
    ASE_ROOT .. "/native/axe-" .. dir .. ".aseprite",
    OUT_ROOT .. "/" .. dir .. "/Axe",
    AXE_DURS, wbs, bodies, wfs, hfs
  )
end

-- 1B. back_l/Axe (Right-Handed North-West Heavy Chop + True Mid-Lift F02 + Dorsal Leather Fists!)
local BACK_L_AXE_META = {
  { vis = false },
  { vis = false, rawIdx = 0 },
  { vis = true, gx = 160, gy = 95,  rot = 24,   flip = true, mode = "rear_dorsal", hf = "rear_dorsal", rawIdx = 1, midLiftF02 = true },
  { vis = true, gx = 156, gy = 80,  rot = 6,    flip = true, mode = "rear_dorsal", hf = "rear_dorsal", rawIdx = 2, crispRaised = true },
  { vis = true, gx = 148, gy = 77,  rot = -12,  flip = true, mode = "rear_dorsal", hf = "rear_dorsal", rawIdx = 3, crispRaised = true },
  { vis = true, gx = 114, gy = 88,  rot = -52,  flip = true, mode = "all_back",    hf = nil,           rawIdx = 4, cleanTrap = true },
  { vis = true, gx = 98,  gy = 114, rot = -96,  flip = true, mode = "all_back",    hf = nil,           rawIdx = 5 },
  { vis = true, gx = 102, gy = 122, rot = -108, flip = true, mode = "all_back",    hf = nil,           rawIdx = 6 },
  { vis = true, gx = 105, gy = 119, rot = -102, flip = true, mode = "all_back",    hf = nil,           rawIdx = 6 },
  { vis = false, rawIdx = 7 },
  { vis = false, rawIdx = 9 },
  { vis = false },
}

local function crispBackLRaisedArm(b)
  local snap = b:clone()
  for y = 72, 108 do
    for x = 142, 174 do
      local p = snap:getPixel(x, y)
      if pxA(p) > 0 then
        local exposed = (pxA(snap:getPixel(x - 1, y)) == 0)
          or (pxA(snap:getPixel(x + 1, y)) == 0)
          or (pxA(snap:getPixel(x, y - 1)) == 0)
          or (pxA(snap:getPixel(x, y + 1)) == 0)
        if exposed then
          b:drawPixel(x, y, INK)
        elseif y >= 84 and y <= 98 and x >= 153 and x <= 165 and luma(p) >= 52 and luma(p) <= 95 then
          if (x + y) % 4 == 0 then b:drawPixel(x, y, HI_STEEL) else b:drawPixel(x, y, MID_STEEL) end
        end
      end
    end
  end
end

do
  local idleBL = openFlat("characters/orc-v1/source/complete-v1/back_l/Idle/00.png", 1)
  local wbs, bodies, wfs, hfs = {}, {}, {}, {}

  for fi = 1, 12 do
    local idx = fi - 1
    if idx == 0 or idx == 11 then
      bodies[fi] = idleBL:clone()
      wbs[fi], wfs[fi], hfs[fi] = blank(256,256), blank(256,256), blank(256,256)
    else
      local m = BACK_L_AXE_META[fi]
      local rIdx = m.rawIdx or (idx - 1)
      local raw128 = openFlat(string.format("%s/%02d.png", NW_AXE_RAW, rIdx), 1)
      local b = blank(256, 256)
      b:drawImage(raw128, Point(64, 64))

      if m.midLiftF02 then
        local rawLift = openFlat(string.format("%s/02.png", NW_AXE_RAW), 1)
        for y = 84, 136 do for x = 148, 174 do b:drawPixel(x, y, 0) end end
        for y = 72, 110 do
          for x = 144, 170 do
            local pl = rawLift:getPixel(x - 64, y - 64)
            if pxA(pl) > 0 then b:drawPixel(x + 4, y + 16, pl) end
          end
        end
        crispBackLRaisedArm(b)
      end
      if m.crispRaised then crispBackLRaisedArm(b) end
      if m.cleanTrap then
        for y = 80, 91 do
          for x = 101, 114 do
            local p = b:getPixel(x, y)
            if pxA(p) > 0 and (pxR(p) - pxB(p)) >= 18 then b:drawPixel(x, y, 0) end
          end
        end
      end

      if m.vis and m.hf == "rear_dorsal" then
        paintBodyLeatherFist(b, m.gx, m.gy, m.rot, 4, 3)
      end
      b = cleanLightMatteHaloOnly(b, 4)
      bodies[fi] = b

      if m.vis then
        wbs[fi], wfs[fi] = composeAxeLayers(axeImg, m.gx, m.gy, m.rot, m.flip, m.mode)
        if m.hf then
          hfs[fi] = buildSculptedHandFront(b, m.gx, m.gy, m.rot, m.hf)
        else
          hfs[fi] = blank(256, 256)
        end
      else
        wbs[fi], wfs[fi], hfs[fi] = blank(256,256), blank(256,256), blank(256,256)
      end
    end
  end

  saveAndExport4LayerClip(
    ASE_ROOT .. "/composite/back_l/axe.aseprite",
    ASE_ROOT .. "/native/axe-back_l.aseprite",
    OUT_ROOT .. "/back_l/Axe",
    AXE_DURS, wbs, bodies, wfs, hfs
  )
end

-- 1C. back_r/Axe (Whole-Body 3D NE Heavy Chop — Zero Stitching, Intact Pauldron & Wrist!)
local BACK_R_AXE_META = {
  { vis = false },
  { vis = false, rawIdx = 0 },
  { vis = true, gx = 162, gy = 100, rot = 26,  flip = false, mode = "rear_dorsal", hf = "rear_dorsal", rawIdx = 1 },
  { vis = true, gx = 149, gy = 76,  rot = 4,   flip = false, mode = "rear_dorsal", hf = "rear_dorsal", rawIdx = 2 },
  { vis = true, gx = 139, gy = 73,  rot = -16, flip = false, mode = "rear_dorsal", hf = "rear_dorsal", rawIdx = 3 },
  { vis = true, gx = 176, gy = 103, rot = 62,  flip = false, mode = "rear_dorsal", hf = "rear_dorsal", rawIdx = 4 },
  { vis = true, gx = 172, gy = 127, rot = 104, flip = false, mode = "rear_dorsal", hf = "rear_dorsal", rawIdx = 5 },
  { vis = true, gx = 165, gy = 132, rot = 114, flip = false, mode = "rear_dorsal", hf = "rear_dorsal", rawIdx = 6 },
  { vis = true, gx = 162, gy = 130, rot = 106, flip = false, mode = "rear_dorsal", hf = "rear_dorsal", rawIdx = 7 },
  { vis = false, rawIdx = 8 },
  { vis = false, rawIdx = 9 },
  { vis = false },
}

do
  local idleBR = openFlat("characters/orc-v1/source/complete-v1/back_r/Idle/00.png", 1)
  local wbs, bodies, wfs, hfs = {}, {}, {}, {}

  for fi = 1, 12 do
    local idx = fi - 1
    if idx == 0 or idx == 11 then
      bodies[fi] = idleBR:clone()
      wbs[fi], wfs[fi], hfs[fi] = blank(256,256), blank(256,256), blank(256,256)
    else
      local m = BACK_R_AXE_META[fi]
      local rIdx = m.rawIdx or (idx - 1)
      local raw128 = openFlat(string.format("%s/%02d.png", NE_AXE_RAW, rIdx), 1)
      local b = blank(256, 256)
      b:drawImage(raw128, Point(64, 64))

      if m.vis then
        paintBodyLeatherFist(b, m.gx, m.gy, m.rot, 4, 3)
      end
      b = cleanLightMatteHaloOnly(b, 4)
      bodies[fi] = b

      if m.vis then
        wbs[fi], wfs[fi] = composeAxeLayers(axeImg, m.gx, m.gy, m.rot, m.flip, m.mode)
        hfs[fi] = buildSculptedHandFront(b, m.gx, m.gy, m.rot, m.hf)
      else
        wbs[fi], wfs[fi], hfs[fi] = blank(256,256), blank(256,256), blank(256,256)
      end
    end
  end

  saveAndExport4LayerClip(
    ASE_ROOT .. "/composite/back_r/axe.aseprite",
    ASE_ROOT .. "/native/axe-back_r.aseprite",
    OUT_ROOT .. "/back_r/Axe",
    AXE_DURS, wbs, bodies, wfs, hfs
  )
end

-- ============================================================================
-- PART 2: SINGLE-LAYER BODY CLIPS HELPER (UNARMED, WALK, DEFEAT)
-- ============================================================================
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
-- PART 3: UNARMED (4 VIEWS, 5 FRAMES, [80, 110, 50, 90, 120] = 450 MS)
-- ============================================================================
local UNARMED_DURS = { 80, 110, 50, 90, 120 }

for _, dir in ipairs({ "front_r", "front_l" }) do
  local idle0 = openFlat("characters/orc-v1/source/complete-v1/" .. dir .. "/Idle/00.png", 1)
  local v5Dir = "characters/orc-v1/source/combat-rescue-v5/combat/" .. dir .. "/Unarmed/"
  local seq = {}
  seq[1] = idle0:clone()
  seq[2] = cleanLightMatteHaloOnly(openFlat(v5Dir .. "01.png", 1), 6)
  seq[3] = cleanLightMatteHaloOnly(openFlat(v5Dir .. "02.png", 1), 6)
  seq[4] = cleanLightMatteHaloOnly(openFlat(v5Dir .. "03.png", 1), 6)
  local f4 = idle0:clone()
  local settleTmp = blank(256, 256)
  local sdx = (dir == "front_r") and 1 or -1
  for y = 64, 190 do
    for x = 64, 192 do
      local sx = (y <= 140) and (x - sdx) or x
      local p = f4:getPixel(sx, y)
      if pxA(p) > 0 then settleTmp:drawPixel(x, y, p) end
    end
  end
  seq[5] = cleanLightMatteHaloOnly(settleTmp, 5)

  saveAndExportBodyClip(
    ASE_ROOT .. "/composite/" .. dir .. "/unarmed.aseprite",
    ASE_ROOT .. "/native/unarmed-" .. dir .. ".aseprite",
    OUT_ROOT .. "/" .. dir .. "/Unarmed",
    UNARMED_DURS, seq
  )
end

do
  local idleBR = openFlat("characters/orc-v1/source/complete-v1/back_r/Idle/00.png", 1)
  local swdBRBody1  = openFlat(OUT_ROOT .. "/back_r/Sword/layers/body/01.png", 1)
  local swdBRBody12 = openFlat(OUT_ROOT .. "/back_r/Sword/layers/body/12.png", 1)
  local v5Dir = "characters/orc-v1/source/combat-rescue-v5/combat/back_r/Unarmed/"

  local function graftUpperStrikeOntoBR(strikeImg, braceDx)
    local out = blank(256, 256)
    for y = 64, 190 do
      for x = 70, 175 do
        local sx = (y <= 176) and (x - braceDx) or x
        local p = idleBR:getPixel(sx, y)
        if y >= 134 and pxA(p) > 0 then out:drawPixel(x, y, p) end
      end
    end
    for y = 64, 136 do
      for x = 70, 210 do
        local ps = strikeImg:getPixel(x, y)
        if pxA(ps) > 0 then out:drawPixel(x, y, ps) end
      end
    end
    return cleanLightMatteHaloOnly(out, 5)
  end

  local seq = {
    idleBR:clone(),
    swdBRBody1:clone(),
    graftUpperStrikeOntoBR(openFlat(v5Dir .. "02.png", 1), 1),
    graftUpperStrikeOntoBR(openFlat(v5Dir .. "03.png", 1), 1),
    swdBRBody12:clone(),
  }

  saveAndExportBodyClip(
    ASE_ROOT .. "/composite/back_r/unarmed.aseprite",
    ASE_ROOT .. "/native/unarmed-back_r.aseprite",
    OUT_ROOT .. "/back_r/Unarmed",
    UNARMED_DURS, seq
  )
end

do
  local idleBL = openFlat("characters/orc-v1/source/complete-v1/back_l/Idle/00.png", 1)
  local swdBLBody1  = openFlat(OUT_ROOT .. "/back_l/Sword/layers/body/01.png", 1)
  local swdBLBody12 = openFlat(OUT_ROOT .. "/back_l/Sword/layers/body/12.png", 1)
  local v5Dir = "characters/orc-v1/source/combat-rescue-v5/combat/back_l/Unarmed/"

  local f2 = cleanLightMatteHaloOnly(openFlat(v5Dir .. "02.png", 1), 5)
  local f3Raw = openFlat(v5Dir .. "03.png", 1)
  local f3 = blank(256, 256)
  for y = 64, 190 do
    for x = 64, 185 do
      if x >= 106 or y >= 118 then
        local p = f3Raw:getPixel(x, y)
        if pxA(p) > 0 then f3:drawPixel(x, y, p) end
      end
    end
  end
  for y = 78, 117 do
    for x = 64, 108 do
      local p = f3Raw:getPixel(x, y)
      if pxA(p) > 0 then f3:drawPixel(x + 3, y + 1, p) end
    end
  end
  f3 = cleanLightMatteHaloOnly(f3, 5)

  local seq = {
    idleBL:clone(),
    swdBLBody1:clone(),
    f2,
    f3,
    swdBLBody12:clone(),
  }

  saveAndExportBodyClip(
    ASE_ROOT .. "/composite/back_l/unarmed.aseprite",
    ASE_ROOT .. "/native/unarmed-back_l.aseprite",
    OUT_ROOT .. "/back_l/Unarmed",
    UNARMED_DURS, seq
  )
end

-- ============================================================================
-- PART 4: WALK (4 VIEWS)
-- ============================================================================
local function scaleRgbClamped(p, factor)
  local r = math.max(12, math.min(245, math.floor(pxR(p) * factor + 0.5)))
  local g = math.max(15, math.min(245, math.floor(pxG(p) * factor + 0.5)))
  local b = math.max(18, math.min(245, math.floor(pxB(p) * factor + 0.5)))
  return rgba(r, g, b, 255)
end

do
  local fwDurs = { 80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80 }
  for _, dir in ipairs({ "front_r", "front_l" }) do
    local seq = {}
    for fi = 1, 16 do
      local idx = fi - 1
      local im = openFlat(string.format("characters/orc-v1/source/complete-v1/%s/Walk/%02d.png", dir, idx), 1)
      if idx == 6 or idx == 8 or idx == 9 then
        for y = 136, 167 do
          for x = 117, 139 do
            local p = im:getPixel(x, y)
            if pxA(p) > 0 then
              local r, b = pxR(p), pxB(p)
              if (math.abs(r - b) <= 14) and (luma(p) >= 28 and luma(p) <= 105) then
                im:drawPixel(x, y, scaleRgbClamped(p, 1.18))
              end
            end
          end
        end
      elseif idx == 7 then
        for y = 136, 167 do
          for x = 117, 139 do
            local p = im:getPixel(x, y)
            if pxA(p) > 0 then
              local r, b = pxR(p), pxB(p)
              if (math.abs(r - b) <= 16) and (luma(p) >= 85) then
                im:drawPixel(x, y, scaleRgbClamped(p, 0.78))
              end
            end
          end
        end
      end
      seq[fi] = im
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
      for y = 100, 144 do
        for x = 88, 110 do
          local p = im:getPixel(x, y)
          if pxA(p) > 0 then
            local r, b = pxR(p), pxB(p)
            if (math.abs(r - b) <= 14) and (luma(p) >= 38 and luma(p) <= 145) then
              im:drawPixel(x, y, scaleRgbClamped(p, 1.12))
            end
          end
        end
      end
    end
    blSeq[fi] = im
  end
  saveAndExportBodyClip(
    ASE_ROOT .. "/composite/back_l/walk.aseprite",
    ASE_ROOT .. "/native/walk-back_l.aseprite",
    OUT_ROOT .. "/back_l/Walk",
    rwDurs, blSeq
  )

  local brSeq = {}
  for fi = 1, 8 do
    local idx = fi - 1
    local im = openFlat(string.format("characters/orc-v1/source/rear-recovery-v2/back_r/Walk/%02d.png", idx), 1)
    if idx == 5 or idx == 7 then
      for y = 100, 144 do
        for x = 146, 170 do
          local p = im:getPixel(x, y)
          if pxA(p) > 0 then
            local r, b = pxR(p), pxB(p)
            if (math.abs(r - b) <= 14) and (luma(p) >= 38 and luma(p) <= 145) then
              im:drawPixel(x, y, scaleRgbClamped(p, 1.10))
            end
          end
        end
      end
    end
    brSeq[fi] = im
  end
  saveAndExportBodyClip(
    ASE_ROOT .. "/composite/back_r/walk.aseprite",
    ASE_ROOT .. "/native/walk-back_r.aseprite",
    OUT_ROOT .. "/back_r/Walk",
    rwDurs, brSeq
  )
end

-- ============================================================================
-- PART 5: DEFEAT (FRONT_R & FRONT_L)
-- ============================================================================
local DEFEAT_DURS = { 70, 95, 115, 130, 290 }

for _, cfg in ipairs({
  { dir = "front_r", raw = PIX_DIR .. "/defeat_front_r_04_proflash.png", dy = 2 },
  { dir = "front_l", raw = PIX_DIR .. "/defeat_front_l_04_proflash.png", dy = 1 },
}) do
  local seq = {}
  for fi = 1, 4 do
    seq[fi] = openFlat(string.format("characters/orc-v1/source/rear-recovery-v2/%s/Defeat/%02d.png", cfg.dir, fi - 1), 1)
  end
  local raw128 = openFlat(cfg.raw, 1)
  local f4 = blank(256, 256)
  f4:drawImage(raw128, Point(64, 64 + cfg.dy))
  f4 = cleanLightMatteHaloOnly(f4, 5)
  seq[5] = f4

  saveAndExportBodyClip(
    ASE_ROOT .. "/composite/" .. cfg.dir .. "/defeat.aseprite",
    ASE_ROOT .. "/native/defeat-" .. cfg.dir .. ".aseprite",
    OUT_ROOT .. "/" .. cfg.dir .. "/Defeat",
    DEFEAT_DURS, seq
  )
end

print("STEP 2 (V11) COMPLETE: Axe Attack (4 views) + Unarmed + Walk + Defeat saved and exported.")
