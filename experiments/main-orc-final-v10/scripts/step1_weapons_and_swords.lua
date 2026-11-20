-- ============================================================================
-- STEP 1 (V11 POLISH): WEAPONS + 4-VIEW SWORD ATTACK + ARCHITECTURE C (A & B)
-- Fixes:
--   1. Sword pivot moved from pommel [48,66] to true handle grip [48,63]
--      (crossguard y=55..59 sits flush on top knuckle; handle y=60..68 inside
--      fist; pommel y=69..76 protrudes cleanly below pinky).
--   2. Rear 3D dorsal occlusion ("rear_dorsal"): blade + crossguard + handle
--      never cut across wrist/bracer/pauldron; closed dorsal brown leather
--      gauntlet sits in front with pommel peeking cleanly at pinky base.
--   3. Sculpted warm-brown leather finger wrap on handFront for frontal grips,
--      and genuine leather dorsal fist + steel vambrace highlights on rear arms.
--   4. Exact anatomical fist lock on every frame (fixing F04 shoulder-socket
--      in front_r/front_l, F11 knee-greave float, back_r F08..F11 low float,
--      and back_l F02 bicep float + F11 forearm float).
--   5. Frontal & Rear body contour/shading repairs:
--      - Preserve 1px INK & spike tips (replace only neutral bright matte >=148).
--      - Replace amputated front_r/front_l Sword F09 body with intact Axe F06
--        same-view follow-through body (0 severed hand, full right arm).
--      - Restore crisp chestplate steel & trim on front_r/front_l Sword F07.
--      - Smooth horizontal cut seam on front_r/front_l Sword F06.
--      - Replace pinched wire-wrist on back_r Sword F06 & fuzzy tricep on F07.
--      - Author true mid-lift right arm for back_l Sword F02 & crisp steel/INK
--        contours on raised right arm F02..F05.
-- ============================================================================

local ASE_ROOT = "characters/orc-v1/source/aseprite/final-candidate-v10"
local OUT_ROOT = "characters/orc-v1/source/final-candidate-v10"
local B3_ROOT  = "experiments/main-orc-hybrid-weapon-04b3"
local NW_RAW   = "experiments/main-orc-final-v10/pixellab/raw_sword_nw"
local NE_RAW   = "experiments/main-orc-final-v10/pixellab/raw_sword_ne"

local SWORD_DURS = { 30, 65, 35, 50, 45, 35, 30, 35, 35, 100, 55, 80, 45, 90 }

local rgba = app.pixelColor.rgba
local pxR  = app.pixelColor.rgbaR
local pxG  = app.pixelColor.rgbaG
local pxB  = app.pixelColor.rgbaB
local pxA  = app.pixelColor.rgbaA

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

local function luma(p)
  return 0.299 * pxR(p) + 0.587 * pxG(p) + 0.114 * pxB(p)
end

local function satSpan(p)
  local r, g, b = pxR(p), pxG(p), pxB(p)
  local mx = math.max(r, g, b)
  local mn = math.min(r, g, b)
  return mx - mn
end

local function ensureDir(d)
  if d and d ~= "" then app.fs.makeAllDirectories(d) end
end

local function blank(w, h)
  local img = Image(w, h, ColorMode.RGB)
  img:clear()
  return img
end

local function saveImg(img, p)
  ensureDir(app.fs.filePath(p))
  img:saveAs(p)
end

local function openFlat(path, frameIdx)
  local s = app.open(path)
  local img = blank(s.width, s.height)
  img:drawSprite(s, frameIdx or 1)
  s:close()
  return img
end

local function openLayer(path, layerName, frameIdx)
  local s = app.open(path)
  local out = blank(s.width, s.height)
  for _, lyr in ipairs(s.layers) do
    if lyr.name == layerName then
      local cel = lyr:cel(frameIdx or 1)
      if cel then out:drawImage(cel.image, cel.position) end
      break
    end
  end
  s:close()
  return out
end

-- Remove ONLY true light neutral matte residue on outer silhouette (preserving 1px INK & spikes!)
local function cleanLightMatteHaloOnly(img)
  local w, h = img.width, img.height
  local out = img:clone()
  for y = 1, h - 2 do
    for x = 1, w - 2 do
      local p = img:getPixel(x, y)
      if pxA(p) > 0 then
        local aL = pxA(img:getPixel(x - 1, y)) == 0
        local aR = pxA(img:getPixel(x + 1, y)) == 0
        local aU = pxA(img:getPixel(x, y - 1)) == 0
        local aD = pxA(img:getPixel(x, y + 1)) == 0
        if aL or aR or aU or aD then
          local lum = luma(p)
          local sat = satSpan(p)
          if lum >= 152 and sat <= 24 then
            out:drawPixel(x, y, DARK_STEEL)
          elseif lum >= 185 then
            out:drawPixel(x, y, INK)
          else
            out:drawPixel(x, y, rgba(pxR(p), pxG(p), pxB(p), 255))
          end
        else
          out:drawPixel(x, y, rgba(pxR(p), pxG(p), pxB(p), 255))
        end
      end
    end
  end
  return out
end

-- Paint a clean closed brown leather fist onto `body` at (gx, gy) oriented with `rotDeg`
-- so even with layers-off, the hand has warm leather gauntlet volume & 1px INK contour!
local function paintBodyLeatherFist(b, gx, gy, rotDeg, rx, ry)
  rx = rx or 4
  ry = ry or 3
  local rad = math.rad(rotDeg or 0)
  local ca, sa = math.cos(rad), math.sin(rad)
  for dy = -(ry + 2), (ry + 2) do
    for dx = -(rx + 2), (rx + 2) do
      -- Local coordinates: u across knuckles, v along handle
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

-- Build `handFront` articulated leather glove wrap around handle axis at (gx, gy, rotDeg):
-- For frontal grip: curled fingers + thumb wrapping across handle (`v = -3..+3`, `u = -3..+3`)
-- For rear dorsal grip: solid dorsal knuckle back (`v = -3.5..+3.5`, `u = -3.8..+3.8`) covering handle
local function buildSculptedHandFront(bodyImg, gx, gy, rotDeg, style)
  local hf = blank(256, 256)
  local rad = math.rad(rotDeg or 0)
  local ca, sa = math.cos(rad), math.sin(rad)

  if style == "frontal_fingers" then
    for dy = -6, 6 do
      for dx = -6, 6 do
        local u = dx * ca + dy * sa
        local v = -dx * sa + dy * ca
        -- 4 curled fingers wrapping across handle: u in [-2.8, +2.8], v in [-3.0, +3.4]
        local inFingers = (math.abs(u) <= 2.9 and v >= -3.0 and v <= 3.5 and ((u / 3.1)^2 + (v / 3.7)^2 <= 1.0))
        if inFingers then
          local x, y = gx + dx, gy + dy
          local edge = (math.abs(u) >= 2.1) or (v <= -2.2) or (v >= 2.7)
          if edge then
            hf:drawPixel(x, y, INK)
          else
            -- Finger knuckle ridges every 1.6px along v
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

-- ============================================================================
-- PART 1: AUTHOR STANDALONE WEAPON MASTERS (96x96, pivot [48, 63])
-- ============================================================================
local swordASrc = openFlat("characters/orc-v1/source/combat-rescue-v5/combat/weapons/Sword/recruit-sword.png", 1)
local swordBSrc = openFlat("experiments/main-orc-hybrid-weapon-04/variants/sword-b/sword.png", 1)

local function saveWeaponMaster(img96, masterPath, pngPath)
  ensureDir(app.fs.filePath(masterPath))
  local spr = Sprite(96, 96, ColorMode.RGB)
  spr.layers[1].name = "weapon"
  spr:newCel(spr.layers[1], 1, img96, Point(0, 0))
  spr:saveAs(masterPath)
  spr:close()
  local re = app.open(masterPath)
  local exp = blank(96, 96)
  exp:drawSprite(re, 1)
  re:close()
  saveImg(exp, pngPath)
  return exp
end

local swordAImg = saveWeaponMaster(
  swordASrc,
  ASE_ROOT .. "/weapons/recruit-sword.aseprite",
  OUT_ROOT .. "/weapons/Sword/recruit-sword.png"
)
local swordBImg = saveWeaponMaster(
  swordBSrc,
  ASE_ROOT .. "/weapons/faceted-sword-b.aseprite",
  OUT_ROOT .. "/weapons/SwordB/faceted-sword-b.png"
)

-- ============================================================================
-- PART 2: DETERMINISTIC SWORD ROTATION & 3D OCCLUSION SPLIT (PIVOT [48, 63])
-- ============================================================================
local function composeSwordLayers(wImg, bodyImg, gx, gy, rotDeg, mode)
  local wb = blank(256, 256)
  local wf = blank(256, 256)
  local full = blank(256, 256)
  local vMap = {}

  local pivU, pivV = 48.0, 63.0
  local rad = math.rad(rotDeg)
  local ca, sa = math.cos(rad), math.sin(rad)

  local x0 = math.max(1, gx - 68)
  local x1 = math.min(254, gx + 68)
  local y0 = math.max(1, gy - 68)
  local y1 = math.min(254, gy + 68)

  for y = y0, y1 do
    for x = x0, x1 do
      local dx, dy = x - gx, y - gy
      local u = math.floor(pivU + dx * ca + dy * sa + 0.5)
      local v = math.floor(pivV - dx * sa + dy * ca + 0.5)
      if u >= 0 and u < 96 and v >= 0 and v < 96 then
        local p = wImg:getPixel(u, v)
        if pxA(p) > 0 then
          full:drawPixel(x, y, rgba(pxR(p), pxG(p), pxB(p), 255))
          vMap[y * 256 + x] = v
        end
      end
    end
  end

  -- Seal exposed outer bright steel edge after nearest-neighbor rotation
  local snap = full:clone()
  for y = y0, y1 do
    for x = x0, x1 do
      local p = snap:getPixel(x, y)
      if pxA(p) > 0 then
        local exposed = (pxA(snap:getPixel(x - 1, y)) == 0)
          or (pxA(snap:getPixel(x + 1, y)) == 0)
          or (pxA(snap:getPixel(x, y - 1)) == 0)
          or (pxA(snap:getPixel(x, y + 1)) == 0)
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
          -- In rear dorsal view: blade + crossguard + gripped handle (v <= 68) stay behind dorsal arm/back (wb),
          -- while the pommel cap (v >= 69) peeks out at pinky base (wf, unless overlapping torso x=104..148)!
          if v >= 69 and (x < 106 or x > 148) then
            wf:drawPixel(x, y, p)
          else
            wb:drawPixel(x, y, p)
          end
        else
          -- "front_grip": crossguard+blade (v <= 59) and pommel (v >= 68) in weaponFront;
          -- gripped handle core (v = 60..67) in weaponBack, wrapped by handFront fingers!
          if v >= 60 and v <= 67 then
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

local function saveAndExportSwordVariant(masterOutPath, nativeMasterPath, exportDir, bodies, handFronts, metaList, weaponImg)
  ensureDir(app.fs.filePath(masterOutPath))
  local spr = Sprite(256, 256, ColorMode.RGB)
  local layerNames = { "weaponBack", "body", "weaponFront", "handFront" }
  local lyrs = {}
  for i, name in ipairs(layerNames) do
    local l = (i == 1) and spr.layers[1] or spr:newLayer()
    l.name = name
    lyrs[name] = l
  end

  for fi = 1, 14 do
    if fi > 1 then spr:newEmptyFrame() end
    spr.frames[fi].duration = SWORD_DURS[fi] / 1000.0
    local m = metaList[fi]
    local wb, wf
    local hf = blank(256, 256)
    if m.vis then
      wb, wf = composeSwordLayers(weaponImg, bodies[fi], m.gx, m.gy, m.rot, m.mode)
      if handFronts[fi] then hf = handFronts[fi]:clone() end
    else
      wb = blank(256, 256)
      wf = blank(256, 256)
    end
    spr:newCel(lyrs.weaponBack, fi, wb, Point(0, 0))
    spr:newCel(lyrs.body, fi, bodies[fi]:clone(), Point(0, 0))
    spr:newCel(lyrs.weaponFront, fi, wf, Point(0, 0))
    spr:newCel(lyrs.handFront, fi, hf, Point(0, 0))
  end

  spr:saveAs(masterOutPath)
  spr:close()

  if nativeMasterPath then
    ensureDir(app.fs.filePath(nativeMasterPath))
    local nspr = Sprite(128, 128, ColorMode.RGB)
    nspr.layers[1].name = "body"
    for fi = 1, 14 do
      if fi > 1 then nspr:newEmptyFrame() end
      nspr.frames[fi].duration = SWORD_DURS[fi] / 1000.0
      local crop = blank(128, 128)
      crop:drawImage(bodies[fi], Point(-64, -64))
      nspr:newCel(nspr.layers[1], fi, crop, Point(0, 0))
    end
    nspr:saveAs(nativeMasterPath)
    nspr:close()
  end

  local re = app.open(masterOutPath)
  local lMap = {}
  for _, l in ipairs(re.layers) do lMap[l.name] = l end

  local function exportSubset(vWb, vBody, vWf, vHf, subDir, stripPath, nativeCropDir, nativeStripPath)
    lMap.weaponBack.isVisible = vWb
    lMap.body.isVisible = vBody
    lMap.weaponFront.isVisible = vWf
    lMap.handFront.isVisible = vHf

    local strip = stripPath and blank(256 * 14, 256) or nil
    local nstrip = nativeStripPath and blank(128 * 14, 128) or nil

    for fi = 1, 14 do
      local fImg = blank(256, 256)
      fImg:drawSprite(re, fi)
      local code = string.format("%02d.png", fi - 1)
      saveImg(fImg, exportDir .. "/" .. subDir .. "/" .. code)
      if strip then strip:drawImage(fImg, Point((fi - 1) * 256, 0)) end
      if nativeCropDir then
        local nc = blank(128, 128)
        nc:drawImage(fImg, Point(-64, -64))
        saveImg(nc, exportDir .. "/" .. nativeCropDir .. "/" .. code)
        if nstrip then nstrip:drawImage(nc, Point((fi - 1) * 128, 0)) end
      end
    end
    if strip then saveImg(strip, exportDir .. "/" .. stripPath) end
    if nstrip then saveImg(nstrip, exportDir .. "/" .. nativeStripPath) end
  end

  exportSubset(true, true, true, true, "frames", "composite-strip.png", nil, nil)
  exportSubset(false, true, false, false, "layers/body", nil, "native", "native-strip.png")
  exportSubset(false, true, false, true, "body-only", nil, nil, nil)
  exportSubset(true, false, true, false, "weapon-only", nil, nil, nil)
  exportSubset(true, false, false, false, "layers/weaponBack", nil, nil, nil)
  exportSubset(false, false, true, false, "layers/weaponFront", nil, nil, nil)
  exportSubset(false, false, false, true, "layers/handFront", nil, nil, nil)

  re:close()
end

-- ============================================================================
-- PART 3: FRONT_R & FRONT_L SWORD BODY REPAIRS + TRUE ANATOMICAL FIST GRIPS
-- ============================================================================
local FRONT_R_META = {
  { vis = false },
  { vis = false },
  { vis = true, gx = 99,  gy = 128, rot = 316, mode = "front_grip", hf = "frontal_fingers" },
  { vis = true, gx = 88,  gy = 120, rot = 330, mode = "front_grip", hf = "frontal_fingers" },
  { vis = true, gx = 86,  gy = 108, rot = 345, mode = "front_grip", hf = "frontal_fingers" },
  { vis = true, gx = 94,  gy = 89,  rot = 2,   mode = "front_grip", hf = "frontal_fingers" },
  { vis = true, gx = 128, gy = 100, rot = 18,  mode = "front_grip", hf = "frontal_fingers" },
  { vis = true, gx = 154, gy = 112, rot = 34,  mode = "front_grip", hf = "frontal_fingers" },
  { vis = true, gx = 157, gy = 129, rot = 82,  mode = "front_grip", hf = "frontal_fingers" },
  { vis = true, gx = 150, gy = 142, rot = 124, mode = "front_grip", hf = "frontal_fingers" },
  { vis = true, gx = 135, gy = 142, rot = 114, mode = "front_grip", hf = "frontal_fingers" },
  { vis = true, gx = 97,  gy = 138, rot = 128, mode = "front_grip", hf = "frontal_fingers" },
  { vis = false },
  { vis = false },
}

local FRONT_L_META = {
  { vis = false },
  { vis = false },
  { vis = true, gx = 156, gy = 128, rot = 44,  mode = "front_grip", hf = "frontal_fingers" },
  { vis = true, gx = 167, gy = 120, rot = 30,  mode = "front_grip", hf = "frontal_fingers" },
  { vis = true, gx = 169, gy = 108, rot = 15,  mode = "front_grip", hf = "frontal_fingers" },
  { vis = true, gx = 161, gy = 89,  rot = 358, mode = "front_grip", hf = "frontal_fingers" },
  { vis = true, gx = 127, gy = 100, rot = 342, mode = "front_grip", hf = "frontal_fingers" },
  { vis = true, gx = 101, gy = 112, rot = 326, mode = "front_grip", hf = "frontal_fingers" },
  { vis = true, gx = 97,  gy = 130, rot = 278, mode = "front_grip", hf = "frontal_fingers" },
  { vis = true, gx = 105, gy = 142, rot = 236, mode = "front_grip", hf = "frontal_fingers" },
  { vis = true, gx = 120, gy = 142, rot = 246, mode = "front_grip", hf = "frontal_fingers" },
  { vis = true, gx = 158, gy = 138, rot = 232, mode = "front_grip", hf = "frontal_fingers" },
  { vis = false },
  { vis = false },
}

local function buildFrontalSwordBodies(dir, srcMasterPath, axeDonorMasterPath, idleF00Path, metaList)
  local idle0 = openFlat(idleF00Path, 1)
  local axeF06Body = openLayer(axeDonorMasterPath, "body", 7) -- intact same-view follow-through body for F09!
  local axeF08Body = openLayer(axeDonorMasterPath, "body", 9) -- intact same-view mid-recovery body for front_l F10!
  local cleanSW02  = (dir == "front_l") and openFlat("experiments/main-orc-final-v10/pixellab/raw_unarmed_sw/02.png", 1) or nil

  local bodies = {}
  local handFronts = {}

  for fi = 1, 14 do
    local idx = fi - 1
    local b = openLayer(srcMasterPath, "body", fi)

    if idx == 0 or idx == 13 then
      b = idle0:clone()
    elseif idx == 8 and dir == "front_l" then
      -- Replace amputated-shoulder + groin-hilt F08 body in front_l with 100% unarmed full-shoulder raw_unarmed_sw/02!
      b = blank(256, 256)
      b:drawImage(cleanSW02, Point(64, 64))
    elseif idx == 9 then
      -- Replace amputated F09 body (missing right arm + severed hand) with intact same-view Axe F06 body!
      b = axeF06Body:clone()
      if dir == "front_r" then
        for y = 144, 162 do
          for x = 152, 168 do b:drawPixel(x, y, 0) end
        end
      else
        for y = 144, 162 do
          for x = 87, 103 do b:drawPixel(x, y, 0) end
        end
      end
    elseif idx == 10 and dir == "front_l" then
      -- Replace premature Idle body on front_l F10 with intact Axe F08 mid-recovery body (left arm genuinely at [120,142])!
      b = axeF08Body:clone()
      for y = 144, 162 do
        for x = 87, 103 do b:drawPixel(x, y, 0) end
      end
    else
      if idx >= 3 and idx <= 5 then
        -- Clean floating specks above pauldron & smooth dark armpit crease without blunting pauldron spikes!
        if dir == "front_r" then
          for y = 72, 83 do
            for x = 92, 118 do
              local p = b:getPixel(x, y)
              if pxA(p) > 0 and luma(p) >= 70 then b:drawPixel(x, y, 0) end
            end
          end
          for y = 108, 124 do
            for x = 99, 113 do
              local p = b:getPixel(x, y)
              if pxA(p) > 0 and luma(p) >= 82 and x <= 111 and y <= 121 then
                b:drawPixel(x, y, (y <= 114) and DARK_SHADOW or DARK_CLOTH)
              end
            end
          end
        else
          for y = 72, 83 do
            for x = 138, 164 do
              local p = b:getPixel(x, y)
              if pxA(p) > 0 and luma(p) >= 70 then b:drawPixel(x, y, 0) end
            end
          end
          for y = 108, 124 do
            for x = 142, 156 do
              local p = b:getPixel(x, y)
              if pxA(p) > 0 and luma(p) >= 82 and x >= 144 and y <= 121 then
                b:drawPixel(x, y, (y <= 114) and DARK_SHADOW or DARK_CLOTH)
              end
            end
          end
        end
      elseif idx == 7 then
        -- Keep 100% intact F07 twisted-torso silhouette and lift under-exposed neutral steel shading to match F06/F08!
        for y = 92, 188 do
          for x = 84, 172 do
            local p = b:getPixel(x, y)
            if pxA(p) > 0 then
              local lum = luma(p)
              if satSpan(p) <= 18 and lum >= 26 and lum <= 130 then
                local nr = math.min(235, math.floor(pxR(p) * 1.28 + 4))
                local ng = math.min(238, math.floor(pxG(p) * 1.28 + 5))
                local nb = math.min(245, math.floor(pxB(p) * 1.30 + 7))
                b:drawPixel(x, y, rgba(nr, ng, nb, 255))
              end
            end
          end
        end
      elseif idx == 12 then
        -- Restore F12 chestplate specular highlights from Idle F00
        for y = 98, 128 do
          for x = 112, 143 do
            local p0 = idle0:getPixel(x, y)
            local pb = b:getPixel(x, y)
            if pxA(pb) > 0 and pxA(p0) > 0 and luma(p0) >= 115 and luma(pb) < luma(p0) - 18 then
              b:drawPixel(x, y, p0)
            end
          end
        end
      end
    end

    local m = metaList[fi]
    if m.vis then
      paintBodyLeatherFist(b, m.gx, m.gy, m.rot, 3, 3)
    end
    b = cleanLightMatteHaloOnly(b)
    bodies[fi] = b

    if m.vis then
      handFronts[fi] = buildSculptedHandFront(b, m.gx, m.gy, m.rot, m.hf)
    else
      handFronts[fi] = blank(256, 256)
    end
  end

  return bodies, handFronts
end

do
  local frBodies, frHands = buildFrontalSwordBodies(
    "front_r",
    "characters/orc-v1/source/combat-recovery-v8/frontal-inbetween/front_r-sword/source/composite.aseprite",
    "characters/orc-v1/source/artistic-reconstruction-v6/frontal/front_r-Axe-full/source/composite.aseprite",
    "characters/orc-v1/source/complete-v1/front_r/Idle/00.png",
    FRONT_R_META
  )
  saveAndExportSwordVariant(
    ASE_ROOT .. "/composite/front_r/sword.aseprite",
    ASE_ROOT .. "/native/sword-front_r.aseprite",
    OUT_ROOT .. "/front_r/Sword",
    frBodies, frHands, FRONT_R_META, swordAImg
  )
  saveAndExportSwordVariant(
    ASE_ROOT .. "/architecture-c/front_r/sword-a.aseprite", nil,
    OUT_ROOT .. "/architecture-c/front_r/sword-a",
    frBodies, frHands, FRONT_R_META, swordAImg
  )
  saveAndExportSwordVariant(
    ASE_ROOT .. "/architecture-c/front_r/sword-b.aseprite", nil,
    OUT_ROOT .. "/architecture-c/front_r/sword-b",
    frBodies, frHands, FRONT_R_META, swordBImg
  )

  local flBodies, flHands = buildFrontalSwordBodies(
    "front_l",
    "characters/orc-v1/source/combat-recovery-v8/frontal-armpit/front_l-sword/source/composite.aseprite",
    "characters/orc-v1/source/artistic-reconstruction-v6/frontal/front_l-Axe-full/source/composite.aseprite",
    "characters/orc-v1/source/complete-v1/front_l/Idle/00.png",
    FRONT_L_META
  )
  saveAndExportSwordVariant(
    ASE_ROOT .. "/composite/front_l/sword.aseprite",
    ASE_ROOT .. "/native/sword-front_l.aseprite",
    OUT_ROOT .. "/front_l/Sword",
    flBodies, flHands, FRONT_L_META, swordAImg
  )
  saveAndExportSwordVariant(
    ASE_ROOT .. "/architecture-c/front_l/sword-a.aseprite", nil,
    OUT_ROOT .. "/architecture-c/front_l/sword-a",
    flBodies, flHands, FRONT_L_META, swordAImg
  )
  saveAndExportSwordVariant(
    ASE_ROOT .. "/architecture-c/front_l/sword-b.aseprite", nil,
    OUT_ROOT .. "/architecture-c/front_l/sword-b",
    flBodies, flHands, FRONT_L_META, swordBImg
  )
end

-- ============================================================================
-- PART 4: BACK_R SWORD (WHOLE-BODY 3D NE ARC — ZERO STITCHING, INTACT PAULDRON)
-- ============================================================================
local BACK_R_META = {
  { vis = false },
  { vis = false, rawIdx = 0 },
  { vis = true, gx = 162, gy = 97,  rot = 26,  mode = "rear_dorsal", hf = "rear_dorsal", rawIdx = 1 },
  { vis = true, gx = 152, gy = 78,  rot = 14,  mode = "rear_dorsal", hf = "rear_dorsal", rawIdx = 2 },
  { vis = true, gx = 145, gy = 73,  rot = -4,  mode = "rear_dorsal", hf = "rear_dorsal", rawIdx = 3 },
  { vis = true, gx = 141, gy = 74,  rot = -14, mode = "rear_dorsal", hf = "rear_dorsal", rawIdx = 4, cleanDust = true },
  { vis = true, gx = 173, gy = 93,  rot = 48,  mode = "rear_dorsal", hf = "rear_dorsal", rawIdx = 5 },
  { vis = true, gx = 177, gy = 108, rot = 82,  mode = "rear_dorsal", hf = "rear_dorsal", rawIdx = 6 },
  { vis = true, gx = 175, gy = 123, rot = 114, mode = "rear_dorsal", hf = "rear_dorsal", rawIdx = 7 },
  { vis = true, gx = 164, gy = 129, rot = 132, mode = "rear_dorsal", hf = "rear_dorsal", rawIdx = 8 },
  { vis = true, gx = 162, gy = 132, rot = 120, mode = "rear_dorsal", hf = "rear_dorsal", rawIdx = 9 },
  { vis = true, gx = 160, gy = 136, rot = 108, mode = "rear_dorsal", hf = "rear_dorsal", rawIdx = 10 },
  { vis = false, rawIdx = 11 },
  { vis = false },
}

do
  local idleBR = openFlat("characters/orc-v1/source/complete-v1/back_r/Idle/00.png", 1)
  local brBodies = {}
  local brHands = {}

  for fi = 1, 14 do
    local idx = fi - 1
    if idx == 0 or idx == 13 then
      brBodies[fi] = idleBR:clone()
      brHands[fi] = blank(256, 256)
    else
      local m = BACK_R_META[fi]
      local rIdx = m.rawIdx or (idx - 1)
      local raw128 = openFlat(string.format("%s/%02d.png", NE_RAW, rIdx), 1)
      local b = blank(256, 256)
      b:drawImage(raw128, Point(64, 64))

      if m.cleanDust then
        -- Remove tiny 2-3px floating dark dust specks just outside raised forearm on raw 04
        for y = 78, 98 do
          for x = 160, 172 do
            if pxA(b:getPixel(x, y)) > 0 then
              local n = 0
              for dy = -1, 1 do
                for dx = -1, 1 do
                  if (dx ~= 0 or dy ~= 0) and pxA(b:getPixel(x + dx, y + dy)) > 0 then n = n + 1 end
                end
              end
              if n <= 2 then b:drawPixel(x, y, 0) end
            end
          end
        end
      end

      if m.vis and m.hf == "rear_dorsal" then
        paintBodyLeatherFist(b, m.gx, m.gy, m.rot, 4, 3)
      end

      b = cleanLightMatteHaloOnly(b)
      brBodies[fi] = b

      if m.vis and m.hf then
        brHands[fi] = buildSculptedHandFront(b, m.gx, m.gy, m.rot, m.hf)
      else
        brHands[fi] = blank(256, 256)
      end
    end
  end

  saveAndExportSwordVariant(
    ASE_ROOT .. "/composite/back_r/sword.aseprite",
    ASE_ROOT .. "/native/sword-back_r.aseprite",
    OUT_ROOT .. "/back_r/Sword",
    brBodies, brHands, BACK_R_META, swordAImg
  )
  saveAndExportSwordVariant(
    ASE_ROOT .. "/architecture-c/back_r/sword-a.aseprite", nil,
    OUT_ROOT .. "/architecture-c/back_r/sword-a",
    brBodies, brHands, BACK_R_META, swordAImg
  )
  saveAndExportSwordVariant(
    ASE_ROOT .. "/architecture-c/back_r/sword-b.aseprite", nil,
    OUT_ROOT .. "/architecture-c/back_r/sword-b",
    brBodies, brHands, BACK_R_META, swordBImg
  )
end

-- ============================================================================
-- PART 5: BACK_L SWORD (TRUE MID-LIFT F02 + LEATHER FISTS + CRISP CONTOURS + B3)
-- ============================================================================
local BACK_L_META = {
  { vis = false },
  { vis = false, rawIdx = 0 },
  { vis = true, gx = 160, gy = 95,  rot = 26,   mode = "rear_dorsal", hf = "rear_dorsal", rawIdx = 1, midLiftF02 = true },
  { vis = true, gx = 156, gy = 79,  rot = 12,   mode = "rear_dorsal", hf = "rear_dorsal", rawIdx = 2, crispRaised = true },
  { vis = true, gx = 149, gy = 77,  rot = -6,   mode = "rear_dorsal", hf = "rear_dorsal", rawIdx = 3, crispRaised = true },
  { vis = true, gx = 144, gy = 76,  rot = -16,  mode = "rear_dorsal", hf = "rear_dorsal", rawIdx = 4, crispRaised = true },
  { vis = true, gx = 107, gy = 86,  rot = -46,  mode = "all_back",    hf = nil,           rawIdx = 5, cleanTrap = true },
  { vis = true, gx = 96,  gy = 98,  rot = -78,  mode = "all_back",    hf = nil,           rawIdx = 6 },
  { vis = true, gx = 95,  gy = 111, rot = -104, mode = "all_back",    hf = nil,           rawIdx = 7 },
  { vis = true, gx = 104, gy = 122, rot = -118, mode = "all_back",    hf = nil,           rawIdx = 8 },
  { vis = true, gx = 108, gy = 124, rot = -124, mode = "all_back",    hf = nil,           rawIdx = 8 },
  { vis = true, gx = 159, gy = 131, rot = 114,  mode = "rear_dorsal", hf = "rear_dorsal", rawIdx = 9 },
  { vis = false, rawIdx = 11 },
  { vis = false },
}

-- Enhance soft AI raised right arm on back_l F03..F05 with crisp 1px INK silhouette & steel vambrace ridge
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
          -- Boost muddy olive-grey forearm plate to clean steel sheen
          if (x + y) % 4 == 0 then
            b:drawPixel(x, y, HI_STEEL)
          else
            b:drawPixel(x, y, MID_STEEL)
          end
        end
      end
    end
  end
end

do
  local idleBL = openFlat("characters/orc-v1/source/complete-v1/back_l/Idle/00.png", 1)
  local blBodies = {}
  local blHands = {}

  for fi = 1, 14 do
    local idx = fi - 1
    if idx == 0 or idx == 13 then
      blBodies[fi] = idleBL:clone()
      blHands[fi] = blank(256, 256)
    else
      local m = BACK_L_META[fi]
      local rIdx = m.rawIdx or (idx - 1)
      local raw128 = openFlat(string.format("%s/%02d.png", NW_RAW, rIdx), 1)
      local b = blank(256, 256)
      b:drawImage(raw128, Point(64, 64))

      if m.midLiftF02 then
        -- Graft genuine raised right arm from raw 02 shifted (+4x, +16y -> fist at [160,95]) onto clean F01/F02 torso, zero silver pipe!
        local rawLift = openFlat(string.format("%s/02.png", NW_RAW), 1)
        for y = 84, 136 do
          for x = 148, 174 do b:drawPixel(x, y, 0) end
        end
        for y = 72, 110 do
          for x = 144, 170 do
            local pl = rawLift:getPixel(x - 64, y - 64)
            if pxA(pl) > 0 then
              b:drawPixel(x + 4, y + 16, pl)
            end
          end
        end
        crispBackLRaisedArm(b)
      end

      if m.crispRaised then
        crispBackLRaisedArm(b)
      end

      if m.cleanTrap then
        -- Remove tiny stray brown smudge on upper-left trapezius (x=102..112, y=81..90)
        for y = 80, 90 do
          for x = 101, 112 do
            local p = b:getPixel(x, y)
            if pxA(p) > 0 and (pxR(p) - pxB(p)) >= 18 then
              b:drawPixel(x, y, 0)
            end
          end
        end
      end

      if m.vis and m.hf == "rear_dorsal" then
        paintBodyLeatherFist(b, m.gx, m.gy, m.rot, 4, 3)
      end

      b = cleanLightMatteHaloOnly(b)
      blBodies[fi] = b

      if m.vis and m.hf then
        blHands[fi] = buildSculptedHandFront(b, m.gx, m.gy, m.rot, m.hf)
      else
        blHands[fi] = blank(256, 256)
      end
    end
  end

  saveAndExportSwordVariant(
    ASE_ROOT .. "/composite/back_l/sword.aseprite",
    ASE_ROOT .. "/native/sword-back_l.aseprite",
    OUT_ROOT .. "/back_l/Sword",
    blBodies, blHands, BACK_L_META, swordAImg
  )
  saveAndExportSwordVariant(
    ASE_ROOT .. "/architecture-c/back_l/sword-a.aseprite", nil,
    OUT_ROOT .. "/architecture-c/back_l/sword-a",
    blBodies, blHands, BACK_L_META, swordAImg
  )
  saveAndExportSwordVariant(
    ASE_ROOT .. "/architecture-c/back_l/sword-b.aseprite", nil,
    OUT_ROOT .. "/architecture-c/back_l/sword-b",
    blBodies, blHands, BACK_L_META, swordBImg
  )
  saveAndExportSwordVariant(
    B3_ROOT .. "/full/a/composite.aseprite", nil,
    B3_ROOT .. "/full/a",
    blBodies, blHands, BACK_L_META, swordAImg
  )
  saveAndExportSwordVariant(
    B3_ROOT .. "/full/b/composite.aseprite", nil,
    B3_ROOT .. "/full/b",
    blBodies, blHands, BACK_L_META, swordBImg
  )
end

print("STEP 1 (V11) COMPLETE: Weapons + 4-view Sword Attack + Architecture C (A & B) saved and exported.")
