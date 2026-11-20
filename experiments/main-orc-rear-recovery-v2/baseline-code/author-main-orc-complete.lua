-- Complete 4-direction x 7-action animation production & artistic recovery for Current Main Orc (orc-v1 / Verde Warcraft).
-- Executed entirely inside Aseprite (--batch --noinapp).
-- Preserves existing front_r Idle, Walk, and main-orc-onehanded-entry-v1 Sword/Axe attacks
-- (with surgical cleanup of the frontal head white-outline halo and 1-frame scalp jitter),
-- reconstructs authentic three-quarter rear views (back_r, back_l) across all 7 actions,
-- and authors expressive heavy-armored Hit reactions and volumetric multi-stage Defeat collapses.
-- Never uses historical/discarded Orc V4 artwork. Weapons are independent assets visible ONLY during Attack.

local root = assert(app.params.root)
local function file(p) return app.fs.joinPath(root, p) end
local pc = app.pixelColor

local function blank(w, h)
  local im = Image(w or 128, h or 128, ColorMode.RGB)
  im:clear()
  return im
end

local function save(im, rel)
  local full = file(rel)
  app.fs.makeAllDirectories(app.fs.filePath(full))
  im:saveAs(full)
end

local function loadImage(rel)
  local s = app.open(file(rel))
  local im = blank(s.width, s.height)
  im:drawSprite(s, 1)
  s:close()
  return im
end

local function readJson(rel)
  local f = assert(io.open(file(rel), 'r'))
  local txt = f:read('*a')
  f:close()
  return json.decode(txt)
end

local function writeJson(rel, data)
  local full = file(rel)
  app.fs.makeAllDirectories(app.fs.filePath(full))
  local f = assert(io.open(full, 'w'))
  f:write(json.encode(data))
  f:close()
end

-- Exact palette colors from orc-v1 (Warcraft green skin + dark iron + oxblood cloth + leather)
local INK       = pc.rgba(12, 15, 18, 255)
local SKIN_DARK = pc.rgba(28, 42, 18, 255)
local SKIN_SHAD = pc.rgba(42, 62, 27, 255)
local SKIN_MID  = pc.rgba(59, 86, 38, 255)
local SKIN_BASE = pc.rgba(79, 113, 51, 255)
local SKIN_LITE = pc.rgba(101, 140, 66, 255)
local SKIN_HIGH = pc.rgba(125, 166, 83, 255)

local IRON_DARK = pc.rgba(22, 25, 30, 255)
local IRON_SHAD = pc.rgba(39, 43, 50, 255)
local IRON_MID  = pc.rgba(58, 63, 72, 255)
local IRON_LITE = pc.rgba(85, 92, 102, 255)
local IRON_HIGH = pc.rgba(124, 132, 144, 255)

local WINE_DARK = pc.rgba(48, 16, 19, 255)
local WINE_MID  = pc.rgba(78, 26, 31, 255)
local WINE_LITE = pc.rgba(110, 38, 44, 255)

local LEATH_DARK = pc.rgba(36, 23, 17, 255)
local LEATH_MID  = pc.rgba(58, 38, 28, 255)
local LEATH_LITE = pc.rgba(84, 56, 41, 255)

local function bbox(im)
  local w, h = im.width, im.height
  local l, r, t, b = w, -1, h, -1
  for y = 0, h - 1 do
    for x = 0, w - 1 do
      if pc.rgbaA(im:getPixel(x, y)) >= 128 then
        if x < l then l = x end
        if x > r then r = x end
        if y < t then t = y end
        if y > b then b = y end
      end
    end
  end
  return l, r, t, b
end

-- Enforces binary alpha, bounds inside [2..w-3, 2..targetBottom], and exact groundY contact.
local function normalizeGround(im, targetBottom, preserveTopDeltaFrom)
  local w, h = im.width, im.height
  local l, r, t, b = bbox(im)
  local out = blank(w, h)
  if b < 0 then return out end
  local dy = targetBottom - b
  if preserveTopDeltaFrom ~= nil then
    dy = preserveTopDeltaFrom
  end
  local dx = 0
  if l < 2 then dx = 2 - l elseif r > w - 3 then dx = (w - 3) - r end
  for y = 0, h - 1 do
    for x = 0, w - 1 do
      local q = im:getPixel(x, y)
      if pc.rgbaA(q) >= 128 then
        local nx = math.max(2, math.min(w - 3, x + dx))
        local ny = math.max(2, math.min(targetBottom, y + dy))
        out:drawPixel(nx, ny, pc.rgba(pc.rgbaR(q), pc.rgbaG(q), pc.rgbaB(q), 255))
      end
    end
  end
  -- Guarantee a solid boot/ground contact cluster on y = targetBottom
  local _, _, _, nb = bbox(out)
  if nb < targetBottom and nb >= 0 then
    local shift = targetBottom - nb
    local shifted = blank(w, h)
    for y = 0, h - 1 do
      for x = 0, w - 1 do
        local q = out:getPixel(x, y)
        if pc.rgbaA(q) > 0 then
          local ny = math.min(targetBottom, y + shift)
          shifted:drawPixel(x, ny, q)
        end
      end
    end
    out = shifted
  end
  return out
end

local function relightPixel(q, delta)
  local a = pc.rgbaA(q)
  if a < 128 then return 0 end
  local r, g, b = pc.rgbaR(q), pc.rgbaG(q), pc.rgbaB(q)
  if r < 22 and g < 24 and b < 28 then
    return pc.rgba(r, g, b, 255)
  end
  local nr = math.max(14, math.min(240, math.floor(r + delta + 0.5)))
  local ng = math.max(14, math.min(240, math.floor(g + delta + 0.5)))
  local nb = math.max(14, math.min(240, math.floor(b + delta + 0.5)))
  return pc.rgba(nr, ng, nb, 255)
end

local function mirrorAndRelight128(src128, shiftX)
  shiftX = shiftX or 0
  local out = blank(128, 128)
  for y = 0, 127 do
    for x = 0, 127 do
      local sx = 127 - (x - shiftX)
      if sx >= 0 and sx < 128 then
        local q = src128:getPixel(sx, y)
        if pc.rgbaA(q) >= 128 then
          local delta = (x < 62) and 6 or ((x > 68) and -6 or 0)
          out:drawPixel(x, y, relightPixel(q, delta))
        end
      end
    end
  end
  return out
end

-- Create a padded 256x256 image from a 128x128 native image at bodyOffset (64, 64)
local function pad256(im128)
  local out = blank(256, 256)
  out:drawImage(im128, Point(64, 64))
  return out
end

-- Crop a 256x256 image at bodyOffset (64, 64) back to 128x128
local function crop128(im256)
  local out = blank(128, 128)
  for y = 0, 127 do
    for x = 0, 127 do
      out:drawPixel(x, y, im256:getPixel(x + 64, y + 64))
    end
  end
  return out
end

-- Save a multi-frame Aseprite master + optional horizontal strip
local function saveMasterSprite(frames, durationsMs, tagName, masterPath, stripPath, layerName)
  local w, h = frames[1].width, frames[1].height
  local s = Sprite(w, h, ColorMode.RGB)
  s.layers[1].name = layerName or tagName
  local strip = stripPath and blank(w * #frames, h) or nil
  for i, im in ipairs(frames) do
    if i > 1 then s:newEmptyFrame() end
    s:newCel(s.layers[1], i, im, Point(0, 0))
    s.frames[i].duration = durationsMs[i] / 1000.0
    if strip then
      strip:drawImage(im, Point((i - 1) * w, 0))
    end
  end
  s:newTag(1, #frames).name = tagName
  local full = file(masterPath)
  app.fs.makeAllDirectories(app.fs.filePath(full))
  s:saveAs(full)
  s:close()
  if strip and stripPath then
    save(strip, stripPath)
  end
end

-- ============================================================================
-- LOAD CANONICAL FRONT & PIXELLAB-RECOVERED REAR / REACTION KEYFRAMES
-- ============================================================================
local REC_DIR = 'experiments/main-orc-complete-v1/pixellab-recovery/'
local backRBaseRaw = loadImage(REC_DIR .. 'back_r_base.png')
local backLBaseRaw = loadImage(REC_DIR .. 'back_l_base.png')
local backRBase = normalizeGround(backRBaseRaw, 126)
local backLBase = normalizeGround(backLBaseRaw, 126)

local defeatFrontRKeys = {
  normalizeGround(loadImage(REC_DIR .. 'defeat_front_r_00.png'), 126),
  normalizeGround(loadImage(REC_DIR .. 'defeat_front_r_01.png'), 126),
  normalizeGround(loadImage(REC_DIR .. 'defeat_front_r_02.png'), 126),
  normalizeGround(loadImage(REC_DIR .. 'defeat_front_r_03.png'), 126),
  normalizeGround(loadImage(REC_DIR .. 'defeat_front_r_04.png'), 126)
}

-- Rear defeat collapse keyframes (monotonically decreasing height into volumetric prone pose)
local function settleProneRear128(im128)
  -- Vertically settle the upper torso/head of defeat_back_r_04 by +12px toward the ground plane
  -- while keeping the foreground boot soles anchored on groundY = 126, so height is ~68px (w=119).
  local out = blank(128, 128)
  for y = 0, 127 do
    for x = 0, 127 do
      local q = im128:getPixel(x, y)
      if pc.rgbaA(q) >= 128 then
        -- Foreground boots/calves are at x < 72, y > 86; upper torso/pauldrons/head are at y <= 92
        local shiftY = 0
        if y < 108 then
          shiftY = math.floor((108 - y) * 0.22 + 0.5)
        end
        local ny = math.min(126, y + shiftY)
        out:drawPixel(x, ny, pc.rgba(pc.rgbaR(q), pc.rgbaG(q), pc.rgbaB(q), 255))
      end
    end
  end
  return normalizeGround(out, 126)
end

local defeatBackRKeys = {
  normalizeGround(loadImage(REC_DIR .. 'hit_back_r_01.png'), 126),
  normalizeGround(loadImage(REC_DIR .. 'defeat_back_r_01.png'), 126),
  normalizeGround(loadImage(REC_DIR .. 'defeat_back_r_02.png'), 126),
  normalizeGround(loadImage(REC_DIR .. 'defeat_back_r_03.png'), 126),
  settleProneRear128(loadImage(REC_DIR .. 'defeat_back_r_04.png'))
}

local hitFrontRPeak  = normalizeGround(loadImage(REC_DIR .. 'hit_front_r_01.png'), 126)
local hitFrontRBrace = normalizeGround(loadImage(REC_DIR .. 'hit_front_r_02.png'), 126)
local hitBackRPeak   = normalizeGround(loadImage(REC_DIR .. 'hit_back_r_01.png'), 126)
local hitBackRBrace  = normalizeGround(loadImage(REC_DIR .. 'hit_back_r_02.png'), 126)

-- ============================================================================
-- SURGICAL FRONTAL HEAD WHITE-OUTLINE & JITTER CLEANUP (256x256 & 128x128)
-- ============================================================================
local function isGreenPx(q)
  if pc.rgbaA(q) < 128 then return false end
  local r, g, b = pc.rgbaR(q), pc.rgbaG(q), pc.rgbaB(q)
  return (g > r + 6 and g > b + 6)
end

local function isGreyHaloPx(q, minR)
  if pc.rgbaA(q) < 128 then return false end
  local r, g, b = pc.rgbaR(q), pc.rgbaG(q), pc.rgbaB(q)
  return (math.abs(r - g) <= 12 and math.abs(g - b) <= 16 and r >= (minR or 52))
end

-- Cleans the frontal head white/grey anti-aliased outline halo and stabilizes
-- the 1-frame scalp pop on Sword frame 05 without touching weapon pixels or facial expression.
local function cleanFrontalBody256(src256, category, idx0)
  local im = Image(src256)

  -- 1. Stabilize the 1-frame 2px scalp bloat on Sword frame 05 (y = 72..73 in 256x256)
  if category == 'Sword' and idx0 == 5 then
    for y = 71, 73 do
      for x = 116, 144 do
        im:drawPixel(x, y, 0)
      end
    end
  end

  -- 2. Strip outer bright-grey anti-aliasing fringe (r >= 78) around head & upper shoulders (y = 66..102, x = 94..162)
  for pass = 1, 2 do
    local snap = Image(im)
    for y = 66, 102 do
      for x = 94, 162 do
        local q = snap:getPixel(x, y)
        if isGreyHaloPx(q, 76) then
          local adjTrans4 = false
          local opqNeighbors = 0
          local adjGreen = false
          local dirs4 = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}}
          for _, d in ipairs(dirs4) do
            local nq = snap:getPixel(x + d[1], y + d[2])
            if pc.rgbaA(nq) < 128 then
              adjTrans4 = true
            else
              opqNeighbors = opqNeighbors + 1
              if isGreenPx(nq) then adjGreen = true end
            end
          end
          if adjTrans4 and opqNeighbors >= 1 and not adjGreen then
            im:drawPixel(x, y, 0)
          end
        end
      end
    end
  end

  -- 3. Enforce crisp 1px dark INK outline on the head dome boundary (y = 68..86, x = 114..150)
  -- and convert any remaining interior grey noise inside the green scalp to SKIN_MID.
  local snap2 = Image(im)
  for y = 68, 86 do
    for x = 114, 150 do
      local q = snap2:getPixel(x, y)
      if pc.rgbaA(q) >= 128 then
        local adjTrans4 = false
        local dirs4 = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}}
        for _, d in ipairs(dirs4) do
          if pc.rgbaA(snap2:getPixel(x + d[1], y + d[2])) < 128 then
            adjTrans4 = true
            break
          end
        end
        if adjTrans4 then
          im:drawPixel(x, y, INK)
        elseif isGreyHaloPx(q, 52) then
          -- Check if near green skin (interior scalp noise)
          local nearGreen = false
          for dy = -2, 2 do
            for dx = -2, 2 do
              if isGreenPx(snap2:getPixel(x + dx, y + dy)) then
                nearGreen = true
                break
              end
            end
            if nearGreen then break end
          end
          if nearGreen then
            im:drawPixel(x, y, SKIN_MID)
          end
        end
      end
    end
  end

  return im
end

-- ============================================================================
-- AUTHENTIC REAR-FACING (back_r, back_l) ANATOMICAL CONSTRUCTION HELPERS
-- ============================================================================
-- Builds a rear Idle frame directly from backRBase / backLBase following idle-balanced-v1 (0, 1, 2, 1, 0 px)
local function makeRearIdleFrame128(rearBase128, breathDy)
  if breathDy == 0 then
    return Image(rearBase128)
  end
  local out = blank(128, 128)
  for y = 0, 127 do
    for x = 0, 127 do
      -- Upper torso, head, pauldrons, and arms above y = 90 shift smoothly by breathDy;
      -- lower legs and boots (y >= 96) remain planted on groundY = 126.
      local dy = 0
      if y < 86 then
        dy = breathDy
      elseif y < 96 then
        dy = math.floor(breathDy * 0.5 + 0.5)
      end
      local sy = y - dy
      if sy >= 0 and sy < 128 then
        local q = rearBase128:getPixel(x, sy)
        if pc.rgbaA(q) >= 128 then
          out:drawPixel(x, y, q)
        end
      end
    end
  end
  return normalizeGround(out, 126, 0)
end

-- Converts front leg kneecaps (y = 85..100) and front boot highlights (y = 114..126)
-- on a posed leg frame into rear popliteal leather knee-straps, calf greaves, and rear boot heels.
local function applyRearLegAndBootAnatomy128(im, dir)
  local isRight = (dir == 'back_r')
  for y = 85, 126 do
    for x = 22, 106 do
      local q = im:getPixel(x, y)
      if pc.rgbaA(q) >= 128 then
        local r, g, b = pc.rgbaR(q), pc.rgbaG(q), pc.rgbaB(q)
        local isOutline = (r < 22 and g < 22 and b < 26)
        if not isOutline then
          if y >= 87 and y <= 98 then
            -- Replace bright front kneecap poleyn highlights with rear popliteal leather crease straps
            if y == 92 or y == 93 then
              if r > 42 then im:drawPixel(x, y, LEATH_DARK) end
            elseif y == 94 or y == 95 then
              if r > 48 then im:drawPixel(x, y, LEATH_MID) end
            elseif r > 82 and g > 82 and b > 86 then
              im:drawPixel(x, y, IRON_SHAD)
            end
          elseif y >= 99 and y <= 114 then
            -- Rear calf greave vertical seam & curved calf shading
            if r > 105 then
              im:drawPixel(x, y, IRON_LITE)
            end
          elseif y >= 115 and y <= 125 then
            -- Darken front-pointing toe specular highlight so boot reads as rear heel guard angled away
            if r > 78 and g > 78 and b > 82 then
              im:drawPixel(x, y, isRight and IRON_SHAD or IRON_MID)
            end
          end
        end
      end
    end
  end
end

-- Builds a rear Walk frame (back_r or back_l) by combining the 16-frame striding legs & swinging outer arms
-- with the authentic rear head, high upward-curving rear gorget, dorsal backplate, horizontal rear belt,
-- rear lumbar plate, and rear chainmail skirt from backRBase / backLBase.
local function makeRearWalkFrame128(walkFront128, dir, stepIdx)
  local isRight = (dir == 'back_r')
  local rearBase = isRight and backRBase or backLBase

  -- 1. Orient the striding lower body & outer arms for back_r (mirror + relight) or back_l
  local basePose = isRight and mirrorAndRelight128(walkFront128, 0) or Image(walkFront128)
  applyRearLegAndBootAnatomy128(basePose, dir)

  -- 2. Compute natural walk cycle bob and contra-lateral shoulder/torso twist for stepIdx (1..16)
  local phase8 = (stepIdx - 1) % 8
  local stepDy = (phase8 >= 2 and phase8 <= 4) and 1 or 0
  local rad = ((stepIdx - 1) / 16.0) * 2.0 * math.pi
  local twistDx = math.floor(math.sin(rad) * 1.4 + 0.5) -- -1, 0, +1
  local leftShoulderDy  = math.floor(math.sin(rad) * 1.0 + 0.5)
  local rightShoulderDy = -leftShoulderDy

  local out = Image(basePose)

  -- 3. Clear any front head/collar remnants in y = 4..30 so the authentic rear head & high collar sit cleanly
  for y = 4, 28 do
    for x = 40, 88 do
      out:drawPixel(x, y, 0)
    end
  end

  -- 4. Stamp the authentic rear upper body (head, high rear gorget, dorsal backplate, pauldrons,
  --    horizontal rear crimson belt, and rear lumbar plate: y = 6..75, x = 32..96) from rearBase,
  --    animated with stepDy + contra-lateral shoulder opposition!
  for y = 6, 75 do
    for x = 32, 96 do
      local localDy = stepDy
      if x < 48 then
        localDy = localDy + leftShoulderDy
      elseif x > 78 then
        localDy = localDy + rightShoulderDy
      end
      local localDx = (y >= 26 and y <= 66) and twistDx or 0
      local sx = x - localDx
      local sy = y - localDy
      if sx >= 0 and sx < 128 and sy >= 0 and sy < 128 then
        local rq = rearBase:getPixel(sx, sy)
        if pc.rgbaA(rq) >= 128 then
          out:drawPixel(x, y, rq)
        elseif y <= 26 and x >= 44 and x <= 84 then
          out:drawPixel(x, y, 0)
        end
      end
    end
  end

  -- 5. Stamp the rear chainmail skirt & rear split leather tassets (y = 74..94, x = 44..82) with stride sway
  local skirtSwayDx = math.floor(-math.sin(rad) * 1.3 + 0.5)
  for y = 74, 92 do
    for x = 46, 80 do
      local sx = x - skirtSwayDx
      local sy = y - stepDy
      if sx >= 0 and sx < 128 and sy >= 0 and sy < 128 then
        local rq = rearBase:getPixel(sx, sy)
        if pc.rgbaA(rq) >= 128 then
          out:drawPixel(x, y, rq)
        end
      end
    end
  end

  return normalizeGround(out, 126)
end

-- Measures the green head centroid/top on a 128x128 frame to track dynamic combat lunges
local function measureHeadOffset128(im128, refCx, refTop)
  local sx, cnt, minY = 0, 0, 128
  for y = 4, 34 do
    for x = 32, 96 do
      local q = im128:getPixel(x, y)
      if isGreenPx(q) then
        sx = sx + x
        cnt = cnt + 1
        if y < minY then minY = y end
      end
    end
  end
  if cnt < 10 then
    return 0, 0
  end
  local cx = sx / cnt
  local dx = math.max(-8, math.min(8, math.floor(cx - refCx + 0.5)))
  local dy = math.max(-3, math.min(6, minY - refTop))
  return dx, dy
end

-- Builds a rear posed combat body frame (for Unarmed, Sword, Axe in back_r / back_l)
-- by tracking the dynamic lunge offset (lungeDx, lungeDy) of the posed frame and grafting
-- the authentic rear occipital head, high upward-curving rear gorget collar, dorsal backplate,
-- horizontal rear crimson belt, and rear lumbar plate from backRBase / backLBase.
local function makeRearCombatBody128(srcFront128, dir)
  local isRight = (dir == 'back_r')
  local rearBase = isRight and backRBase or backLBase
  local oriented = isRight and mirrorAndRelight128(srcFront128, 0) or Image(srcFront128)
  applyRearLegAndBootAnatomy128(oriented, dir)

  local refCx = isRight and 62.5 or 63.5
  local lungeDx, lungeDy = measureHeadOffset128(oriented, refCx, 6)

  local out = Image(oriented)

  -- 1. Clear the front face & front gorget in the tracked head box so zero front facial pixels survive
  for y = math.max(2, 4 + lungeDy), math.min(125, 29 + lungeDy) do
    for x = math.max(2, 42 + lungeDx), math.min(125, 86 + lungeDx) do
      out:drawPixel(x, y, 0)
    end
  end

  -- 2. Graft the authentic rear head, high rear gorget collar, dorsal backplate,
  --    horizontal rear crimson belt, and rear lumbar plate (y = 6..74, x = 38..88)
  --    from rearBase shifted by (lungeDx, lungeDy).
  local coreLeft  = isRight and 38 or 38
  local coreRight = isRight and 87 or 86
  for y = 6, 74 do
    for x = coreLeft, coreRight do
      local tx = x + lungeDx
      local ty = y + lungeDy
      if tx >= 2 and tx <= 125 and ty >= 2 and ty <= 125 then
        local rq = rearBase:getPixel(x, y)
        if pc.rgbaA(rq) >= 128 then
          out:drawPixel(tx, ty, rq)
        elseif y <= 26 and x >= 44 and x <= 82 then
          out:drawPixel(tx, ty, 0)
        end
      end
    end
  end

  -- 3. Also graft the rear chainmail skirt & rear lumbar border (y = 73..90, x = 48..78)
  local hipDx = math.floor(lungeDx * 0.5 + 0.5)
  local hipDy = math.floor(lungeDy * 0.5 + 0.5)
  for y = 73, 90 do
    for x = 48, 78 do
      local tx = x + hipDx
      local ty = y + hipDy
      if tx >= 2 and tx <= 125 and ty >= 2 and ty <= 125 then
        local rq = rearBase:getPixel(x, y)
        if pc.rgbaA(rq) >= 128 then
          out:drawPixel(tx, ty, rq)
        end
      end
    end
  end

  return normalizeGround(out, 126)
end

-- Transform a native 128x128 front_r frame into front_r or front_l
local function buildFrontDirectionFrame128(src128, dir, opts)
  opts = opts or {}
  if dir == 'front_r' then
    local out = Image(src128)
    if opts.normalizeGround then
      out = normalizeGround(out, 126, opts.preserveTopDelta)
    end
    return out
  end
  -- front_l: mirror + top-left relighting + asymmetric chestplate battle-scars
  local out = mirrorAndRelight128(src128, 0)
  if not opts.skipChestGraft then
    local hy = opts.headDy or 0
    for y = 40 + hy, 48 + hy do
      for x = 67, 75 do
        if y >= 2 and y < 126 then
          local q = out:getPixel(x, y)
          if pc.rgbaA(q) > 0 then
            local r, g, b = pc.rgbaR(q), pc.rgbaG(q), pc.rgbaB(q)
            if r < 38 and g < 40 and b < 46 and r > 18 then
              out:drawPixel(x, y, IRON_MID)
            end
          end
        end
      end
    end
  end
  if opts.normalizeGround then
    out = normalizeGround(out, 126, opts.preserveTopDelta)
  end
  return out
end

local DIRECTIONS = {'front_r', 'front_l', 'back_r', 'back_l'}

-- ============================================================================
-- STAGE B & C: Directional Foundations, Idle (5f / 2200ms), Walk (16f / 1280ms)
-- ============================================================================
local idleDurations = {400, 450, 500, 450, 400}
local walkDurations = {}
for i = 1, 16 do walkDurations[i] = 80 end

local idleFrontR = {}
for i = 0, 4 do
  idleFrontR[i + 1] = loadImage(string.format('characters/orc-v1/source/studies/Idle/%02d.png', i))
end

local walkFrontR = {}
for i = 0, 15 do
  walkFrontR[i + 1] = loadImage(string.format('characters/orc-v1/source/studies/Walk/%02d.png', i))
end

local idleHeadDy = {0, 1, 2, 1, 0}

for _, dir in ipairs(DIRECTIONS) do
  -- 1. Directional static base (128x128 & 256x256)
  local base128
  if dir == 'front_r' or dir == 'front_l' then
    base128 = buildFrontDirectionFrame128(idleFrontR[1], dir, {normalizeGround = true, preserveTopDelta = 0, headDy = 0})
  elseif dir == 'back_r' then
    base128 = Image(backRBase)
  else
    base128 = Image(backLBase)
  end

  save(base128, string.format('characters/orc-v1/sprites/Directions/orc_v1_dir_%s.png', dir))
  saveMasterSprite({base128}, {100}, 'Direction_' .. dir,
    string.format('characters/orc-v1/source/aseprite/complete-v1/native/dir-%s.aseprite', dir), nil, 'Base_' .. dir)

  if dir == 'front_r' then
    save(base128, 'characters/orc-v1/sprites/orc_v1_mvp1_static_128.png')
    saveMasterSprite({base128}, {100}, 'StaticBase',
      'characters/orc-v1/source/aseprite/complete-v1/native/static-base.aseprite', nil, 'StaticBase')
  end

  local base256 = pad256(base128)
  save(base256, string.format('characters/orc-v1/source/complete-v1/%s/Directions/base.png', dir))
  saveMasterSprite({base256}, {100}, 'Direction_' .. dir,
    string.format('characters/orc-v1/source/aseprite/complete-v1/composite/%s/dir-base.aseprite', dir), nil, 'Base_' .. dir)

  -- 2. Idle (5 frames, 400/450/500/450/400 ms = 2200 ms, idle-balanced-v1)
  local idle128Frames, idle256Frames = {}, {}
  for i = 1, 5 do
    local f128
    if dir == 'front_r' or dir == 'front_l' then
      f128 = buildFrontDirectionFrame128(idleFrontR[i], dir, {
        normalizeGround = true,
        preserveTopDelta = 0,
        headDy = idleHeadDy[i]
      })
    elseif dir == 'back_r' then
      f128 = makeRearIdleFrame128(backRBase, idleHeadDy[i])
    else
      f128 = makeRearIdleFrame128(backLBase, idleHeadDy[i])
    end
    idle128Frames[i] = f128
    save(f128, string.format('characters/orc-v1/sprites/Animations/Idle/idle_%s_%02d.png', dir, i - 1))
    local f256 = pad256(f128)
    idle256Frames[i] = f256
    save(f256, string.format('characters/orc-v1/source/complete-v1/%s/Idle/%02d.png', dir, i - 1))
  end
  saveMasterSprite(idle128Frames, idleDurations, 'Idle',
    string.format('characters/orc-v1/source/aseprite/complete-v1/native/idle-%s.aseprite', dir), nil, 'Idle_' .. dir)
  saveMasterSprite(idle256Frames, idleDurations, 'Idle',
    string.format('characters/orc-v1/source/aseprite/complete-v1/composite/%s/idle-unarmed.aseprite', dir),
    string.format('characters/orc-v1/source/complete-v1/%s/Idle/native-strip.png', dir), 'Unarmed body')

  -- 3. Walk (16 frames, 80 ms each = 1280 ms, weaponless)
  local walk128Frames, walk256Frames = {}, {}
  for i = 1, 16 do
    local stepDy = (i % 8 >= 3 and i % 8 <= 5) and 1 or 0
    local f128
    if dir == 'front_r' or dir == 'front_l' then
      f128 = buildFrontDirectionFrame128(walkFrontR[i], dir, {
        normalizeGround = true,
        headDy = stepDy
      })
    else
      f128 = makeRearWalkFrame128(walkFrontR[i], dir, i)
    end
    walk128Frames[i] = f128
    save(f128, string.format('characters/orc-v1/sprites/Animations/Walk/walk_%s_%02d.png', dir, i - 1))
    local f256 = pad256(f128)
    walk256Frames[i] = f256
    save(f256, string.format('characters/orc-v1/source/complete-v1/%s/Walk/%02d.png', dir, i - 1))
  end
  saveMasterSprite(walk128Frames, walkDurations, 'Walk',
    string.format('characters/orc-v1/source/aseprite/complete-v1/native/walk-%s.aseprite', dir), nil, 'Walk_' .. dir)
  saveMasterSprite(walk256Frames, walkDurations, 'Walk',
    string.format('characters/orc-v1/source/aseprite/complete-v1/composite/%s/walk-unarmed.aseprite', dir),
    string.format('characters/orc-v1/source/complete-v1/%s/Walk/native-strip.png', dir), 'Unarmed body')
end

-- ============================================================================
-- STAGE D: Unarmed Attack, Hit, and Defeat across all 4 directions
-- ============================================================================
-- 1. Unarmed Attack (5 frames: [80, 110, 50, 90, 120] ms = 450 ms, basic.unarmed)
local unarmedDurations = {80, 110, 50, 90, 120}
local unarmedSourcePairs = {
  {'Sword', 1},  -- 00: guard-prep
  {'Axe',   3},  -- 01: shoulder-coil
  {'Sword', 6},  -- 02: heavy-gauntlet-impact
  {'Axe',   6},  -- 03: follow-through
  {'Sword', 11}  -- 04: recovery-settle
}
local unarmedFrontR128 = {}
for i, pair in ipairs(unarmedSourcePairs) do
  local cat, idx0 = pair[1], pair[2]
  local rawBody256 = loadImage(string.format('characters/orc-v1/source/onehanded-entry-v1/%s/Attack/layers/body/%02d.png', cat, idx0))
  local body256 = cleanFrontalBody256(rawBody256, cat, idx0)
  local hand256 = loadImage(string.format('characters/orc-v1/source/onehanded-entry-v1/%s/Attack/layers/handFront/%02d.png', cat, idx0))
  local merged256 = Image(body256)
  merged256:drawImage(hand256, Point(0, 0))
  local raw128 = crop128(merged256)
  unarmedFrontR128[i] = normalizeGround(raw128, 126)
end

for _, dir in ipairs(DIRECTIONS) do
  local u128, u256 = {}, {}
  for i = 1, 5 do
    local f128
    if dir == 'front_r' or dir == 'front_l' then
      f128 = buildFrontDirectionFrame128(unarmedFrontR128[i], dir, {
        normalizeGround = true,
        skipChestGraft = (i >= 2 and i <= 4)
      })
    else
      f128 = makeRearCombatBody128(unarmedFrontR128[i], dir)
    end
    u128[i] = f128
    save(f128, string.format('characters/orc-v1/sprites/Animations/Attack/attack_%s_%02d.png', dir, i - 1))
    save(f128, string.format('characters/orc-v1/source/actions/basic-unarmed/v1/%s/attack_%s_%02d.png', dir, dir, i - 1))
    local f256 = pad256(f128)
    u256[i] = f256
    save(f256, string.format('characters/orc-v1/source/complete-v1/%s/Unarmed/%02d.png', dir, i - 1))
  end
  saveMasterSprite(u128, unarmedDurations, 'Attack',
    string.format('characters/orc-v1/source/aseprite/complete-v1/native/attack-%s.aseprite', dir), nil, 'Unarmed_' .. dir)
  saveMasterSprite(u256, unarmedDurations, 'Unarmed',
    string.format('characters/orc-v1/source/aseprite/complete-v1/composite/%s/unarmed-attack.aseprite', dir),
    string.format('characters/orc-v1/source/complete-v1/%s/Unarmed/native-strip.png', dir), 'Unarmed strike body')
end

-- 2. Hit Reaction (5 frames: [45, 95, 115, 95, 100] ms = 450 ms, reaction.hit)
-- Uses articulated heavy-armored impact keyframes (head snap, shoulder hunch, forearm guard brace,
-- torso recoil, and grounded knee compression on groundY = 126).
local hitDurations = {45, 95, 115, 95, 100}

local function shiftUpperBodyAnchored128(src128, recoilDx, compressDy)
  local out = blank(128, 128)
  for y = 0, 127 do
    for x = 0, 127 do
      local w = 0
      if y < 104 then
        w = math.min(1.0, (104 - y) / 52.0)
      end
      local dx = math.floor(recoilDx * w + 0.5)
      local dy = math.floor(compressDy * w + 0.5)
      local sx = x - dx
      local sy = y - dy
      if sx >= 0 and sx < 128 and sy >= 0 and sy < 128 then
        local q = src128:getPixel(sx, sy)
        if pc.rgbaA(q) >= 128 then
          out:drawPixel(x, y, q)
        end
      end
    end
  end
  return normalizeGround(out, 126)
end

local function buildHitSequence128(dir)
  if dir == 'front_r' then
    return {
      shiftUpperBodyAnchored128(hitFrontRBrace, -3, 1),  -- 00: impact-onset (initial brace jolt)
      shiftUpperBodyAnchored128(hitFrontRPeak,  -6, 2),  -- 01: peak-recoil (head snapped back, high guard brace)
      shiftUpperBodyAnchored128(hitFrontRBrace, -5, 4),  -- 02: stagger-brace (deepest knee/torso absorption)
      shiftUpperBodyAnchored128(defeatFrontRKeys[1], -2, 1), -- 03: recovery-rise
      shiftUpperBodyAnchored128(idleFrontR[1],  -1, 1)   -- 04: recovery-settle
    }
  elseif dir == 'front_l' then
    local fR = buildHitSequence128('front_r')
    local out = {}
    for i = 1, 5 do
      out[i] = normalizeGround(mirrorAndRelight128(fR[i], 0), 126)
    end
    return out
  elseif dir == 'back_r' then
    return {
      shiftUpperBodyAnchored128(hitBackRBrace, -3, 1),   -- 00: impact-onset
      shiftUpperBodyAnchored128(hitBackRPeak,  -6, 2),   -- 01: peak-recoil (head & dorsal backplate jolted back)
      shiftUpperBodyAnchored128(hitBackRBrace, -5, 4),   -- 02: stagger-brace (deep grounded rear brace)
      shiftUpperBodyAnchored128(hitBackRBrace, -2, 1),   -- 03: recovery-rise
      shiftUpperBodyAnchored128(backRBase,     -1, 1)    -- 04: recovery-settle
    }
  else -- back_l
    local bR = buildHitSequence128('back_r')
    local out = {}
    for i = 1, 5 do
      if i == 5 then
        out[i] = shiftUpperBodyAnchored128(backLBase, 1, 1)
      else
        out[i] = normalizeGround(mirrorAndRelight128(bR[i], 0), 126)
      end
    end
    return out
  end
end

for _, dir in ipairs(DIRECTIONS) do
  local h128 = buildHitSequence128(dir)
  local h256 = {}
  for i = 1, 5 do
    local f128 = h128[i]
    save(f128, string.format('characters/orc-v1/sprites/Animations/Hit/hit_%s_%02d.png', dir, i - 1))
    local f256 = pad256(f128)
    h256[i] = f256
    save(f256, string.format('characters/orc-v1/source/complete-v1/%s/Hit/%02d.png', dir, i - 1))
  end
  saveMasterSprite(h128, hitDurations, 'Hit',
    string.format('characters/orc-v1/source/aseprite/complete-v1/native/hit-%s.aseprite', dir), nil, 'Hit_' .. dir)
  saveMasterSprite(h256, hitDurations, 'Hit',
    string.format('characters/orc-v1/source/aseprite/complete-v1/composite/%s/hit-unarmed.aseprite', dir),
    string.format('characters/orc-v1/source/complete-v1/%s/Hit/native-strip.png', dir), 'Hit reaction body')
end

-- 3. Defeat (5 frames: [70, 95, 115, 130, 290] ms = 700 ms, reaction.defeat, terminal = true)
-- Multi-stage volumetric physical collapse:
--   00: fatal-stagger -> 01: knees-buckle -> 02: drop-to-knees -> 03: collapse-impact -> 04: terminal-defeated
local defeatDurations = {70, 95, 115, 130, 290}

local function buildDefeatSequence128(dir)
  if dir == 'front_r' then
    return defeatFrontRKeys
  elseif dir == 'front_l' then
    local out = {}
    for i = 1, 5 do
      out[i] = normalizeGround(mirrorAndRelight128(defeatFrontRKeys[i], 0), 126)
    end
    return out
  elseif dir == 'back_r' then
    return defeatBackRKeys
  else -- back_l
    local out = {}
    for i = 1, 5 do
      out[i] = normalizeGround(mirrorAndRelight128(defeatBackRKeys[i], 0), 126)
    end
    return out
  end
end

for _, dir in ipairs(DIRECTIONS) do
  local d128 = buildDefeatSequence128(dir)
  local d256 = {}
  for i = 1, 5 do
    local f128 = d128[i]
    save(f128, string.format('characters/orc-v1/sprites/Animations/Defeat/defeat_%s_%02d.png', dir, i - 1))
    local f256 = pad256(f128)
    d256[i] = f256
    save(f256, string.format('characters/orc-v1/source/complete-v1/%s/Defeat/%02d.png', dir, i - 1))
  end
  saveMasterSprite(d128, defeatDurations, 'Defeat',
    string.format('characters/orc-v1/source/aseprite/complete-v1/native/defeat-%s.aseprite', dir), nil, 'Defeat_' .. dir)
  saveMasterSprite(d256, defeatDurations, 'Defeat',
    string.format('characters/orc-v1/source/aseprite/complete-v1/composite/%s/defeat-unarmed.aseprite', dir),
    string.format('characters/orc-v1/source/complete-v1/%s/Defeat/native-strip.png', dir), 'Defeat body')
end

-- ============================================================================
-- STAGE E & F: One-Handed Sword Attack (13f / 730ms) & Axe Attack (12f / 1005ms)
-- Across all 4 directions (front_r, front_l, back_r, back_l)
-- ============================================================================
local LAYER_ORDER = {'weaponBack', 'body', 'weaponFront', 'handFront'}
local swordClipFrontR = readJson('characters/orc-v1/source/onehanded-entry-v1/Sword/Attack/clip.json')
local axeClipFrontR   = readJson('characters/orc-v1/source/onehanded-entry-v1/Axe/Attack/clip.json')

local swordItem = loadImage('assets/weapons/recruit-sword/sprites/rescue-v3/recruit-sword.png')
local axeItem   = loadImage('assets/weapons/militia-axe/sprites/rescue-v3/militia-axe.png')

-- Rotate weapon sprite around local grip to canvas targetGrip (in 256x256).
-- In rear views during forward strike (behindBody=true), any weapon pixel overlapping
-- the dorsal backplate or extending away into depth goes to weaponBack so the dorsal
-- backplate naturally occludes the weapon in 3/4 rear perspective.
local function renderWeaponLayers(itemImg, itemGrip, targetGrip, angleDeg, behindBody, flipBit, isRearForwardStrike)
  local back, front = blank(256, 256), blank(256, 256)
  local rad = angleDeg * math.pi / 180.0
  local c, s = math.cos(rad), math.sin(rad)
  local gx, gy = targetGrip[1], targetGrip[2]
  for y = 2, 253 do
    for x = 2, 253 do
      local dx, dy = x - gx, y - gy
      local rx = c * dx + s * dy
      local ry = -s * dx + c * dy
      if flipBit then rx = -rx end
      local u = math.floor(rx + itemGrip[1] + 0.5)
      local v = math.floor(ry + itemGrip[2] + 0.5)
      if u >= 0 and u < itemImg.width and v >= 0 and v < itemImg.height then
        local q = itemImg:getPixel(u, v)
        if pc.rgbaA(q) >= 128 then
          local px = pc.rgba(pc.rgbaR(q), pc.rgbaG(q), pc.rgbaB(q), 255)
          local toBack = false
          if isRearForwardStrike then
            toBack = true
          elseif behindBody and v < itemGrip[2] - 9 then
            toBack = true
          end
          local dst = toBack and back or front
          dst:drawPixel(x, y, px)
        end
      end
    end
  end
  return back, front
end

local authoredGeometry = { Sword = {}, Axe = {} }

local function buildWeaponCategory(category, clipFrontR, itemImg, itemGrip)
  authoredGeometry[category] = {}
  local framesMeta = clipFrontR.frames
  local durations = {}
  for i, fm in ipairs(framesMeta) do durations[i] = fm.durationMs end

  for _, dir in ipairs(DIRECTIONS) do
    local outDir = string.format('characters/orc-v1/source/complete-v1/%s/%s/Attack', dir, category)
    local masterDir = string.format('characters/orc-v1/source/aseprite/complete-v1/composite/%s', dir)
    local compSprite = Sprite(256, 256, ColorMode.RGB)
    local compLayers = {}
    for li, lname in ipairs(LAYER_ORDER) do
      local l = (li == 1) and compSprite.layers[1] or compSprite:newLayer()
      l.name = lname
      compLayers[lname] = l
    end
    local bodyFrames, handFrames, compFrames = {}, {}, {}
    local strip = blank(256 * #framesMeta, 256)
    local dirGeom = {}

    for i, fm in ipairs(framesMeta) do
      local idx0 = i - 1
      local rawSrcBody256 = loadImage(string.format('characters/orc-v1/source/onehanded-entry-v1/%s/Attack/layers/body/%02d.png', category, idx0))
      -- Clean frontal head white-outline halo and 1-frame scalp jitter on the source body layer
      local srcBody256 = cleanFrontalBody256(rawSrcBody256, category, idx0)
      local srcHand256 = loadImage(string.format('characters/orc-v1/source/onehanded-entry-v1/%s/Attack/layers/handFront/%02d.png', category, idx0))

      local body256, hand256, wBack256, wFront256
      local gripDir, angleDir, behindDir = nil, nil, false

      if dir == 'front_r' then
        -- Preserve exact main-orc-onehanded-entry-v1 weapon & hand layers in front_r,
        -- paired with the halo-cleaned body256 so the white head-outline flash is eliminated.
        body256   = srcBody256
        hand256   = srcHand256
        wBack256  = loadImage(string.format('characters/orc-v1/source/onehanded-entry-v1/%s/Attack/layers/weaponBack/%02d.png', category, idx0))
        wFront256 = loadImage(string.format('characters/orc-v1/source/onehanded-entry-v1/%s/Attack/layers/weaponFront/%02d.png', category, idx0))
        gripDir   = fm.rightGrip
        angleDir  = fm.rotationDeg
        behindDir = fm.weaponBehindBody and true or false
      else
        local srcBody128 = crop128(srcBody256)
        local dirBody128
        if dir == 'front_l' then
          dirBody128 = buildFrontDirectionFrame128(srcBody128, 'front_l', {
            normalizeGround = true,
            preserveTopDelta = 0,
            skipChestGraft = (i >= 3 and i <= #framesMeta - 2)
          })
        else
          dirBody128 = makeRearCombatBody128(srcBody128, dir)
        end
        body256 = pad256(dirBody128)
        hand256 = blank(256, 256)
        wBack256 = blank(256, 256)
        wFront256 = blank(256, 256)

        if fm.weaponVisible then
          local origGx, origGy = fm.rightGrip[1], fm.rightGrip[2]
          local origAngle = fm.rotationDeg
          local flipHoriz = (dir == 'front_l' or dir == 'back_r')
          local isRear = (dir == 'back_r' or dir == 'back_l')
          local isRearForwardStrike = isRear and (i >= 6 and i <= #framesMeta - 3)

          -- Map handFront glove fingers with the same horizontal coordinate mapping as the posed arm
          for y = 64, 191 do
            for x = 64, 191 do
              local q = srcHand256:getPixel(x, y)
              if pc.rgbaA(q) >= 128 then
                local tx = flipHoriz and (255 - x) or x
                local ty = y
                -- In rear forward strikes, do not draw front-crossing hand fingers over the middle of the dorsal backplate
                local inDorsalCore = isRearForwardStrike and (tx >= 108 and tx <= 148 and ty >= 90 and ty <= 138)
                if not inDorsalCore and pc.rgbaA(body256:getPixel(tx, ty)) > 0 then
                  hand256:drawPixel(tx, ty, pc.rgba(pc.rgbaR(q), pc.rgbaG(q), pc.rgbaB(q), 255))
                end
              end
            end
          end

          local gx = flipHoriz and (255 - origGx) or origGx
          local gy = origGy
          if pc.rgbaA(body256:getPixel(gx, gy)) == 0 then
            local hl, hr, ht, hb = bbox(hand256)
            if hb >= 0 then
              gx = math.floor((hl + hr) * 0.5)
              gy = math.floor((ht + hb) * 0.5)
            end
          end
          local _, _, _, hb = bbox(hand256)
          if hb < 0 then
            for dy = -3, 3 do
              for dx = -3, 3 do
                if dx * dx + dy * dy <= 10 then
                  local bq = body256:getPixel(gx + dx, gy + dy)
                  if pc.rgbaA(bq) > 0 then
                    hand256:drawPixel(gx + dx, gy + dy, bq)
                  else
                    hand256:drawPixel(gx + dx, gy + dy, LEATH_MID)
                    body256:drawPixel(gx + dx, gy + dy, LEATH_DARK)
                  end
                end
              end
            end
          end

          gripDir = {gx, gy}
          local flipBit = false
          if dir == 'front_l' then
            angleDir = (360 - origAngle) % 360
            behindDir = fm.weaponBehindBody and true or false
            flipBit = true
          elseif dir == 'back_r' then
            angleDir = (360 - origAngle) % 360
            behindDir = isRearForwardStrike
            flipBit = true
          elseif dir == 'back_l' then
            angleDir = origAngle
            behindDir = isRearForwardStrike
            flipBit = false
          end

          wBack256, wFront256 = renderWeaponLayers(itemImg, itemGrip, gripDir, angleDir, behindDir, flipBit, isRearForwardStrike)
        end
      end

      if i > 1 then compSprite:newEmptyFrame() end
      local layerImgs = {
        weaponBack  = wBack256,
        body        = body256,
        weaponFront = wFront256,
        handFront   = hand256
      }
      for _, lname in ipairs(LAYER_ORDER) do
        compSprite:newCel(compLayers[lname], i, layerImgs[lname], Point(0, 0))
        save(layerImgs[lname], string.format('%s/layers/%s/%02d.png', outDir, lname, idx0))
      end
      compSprite.frames[i].duration = fm.durationMs / 1000.0

      local compImg = blank(256, 256)
      compImg:drawSprite(compSprite, i)
      save(compImg, string.format('%s/%02d.png', outDir, idx0))
      strip:drawImage(compImg, Point(idx0 * 256, 0))

      bodyFrames[i] = body256
      handFrames[i] = hand256
      compFrames[i] = compImg

      dirGeom[i] = {
        index = idx0,
        durationMs = fm.durationMs,
        phase = fm.phase,
        weaponVisible = fm.weaponVisible and true or false,
        rightGrip = gripDir,
        rotationDeg = angleDir,
        weaponBehindBody = behindDir
      }
    end

    compSprite:newTag(1, #framesMeta).name = clipFrontR.id
    local stem = string.format('%s/%s', masterDir, category:lower())
    app.fs.makeAllDirectories(file(masterDir))
    compSprite:saveAs(file(stem .. '-attack.aseprite'))
    compSprite:close()

    saveMasterSprite(bodyFrames, durations, clipFrontR.id .. '_body',
      stem .. '-body.aseprite', nil, 'Weapon independent posed body')
    saveMasterSprite(handFrames, durations, clipFrontR.id .. '_hand',
      stem .. '-hand-front.aseprite', nil, 'Pose-specific original glove/fingers')
    save(strip, outDir .. '/native-strip.png')

    authoredGeometry[category][dir] = dirGeom
  end
end

buildWeaponCategory('Sword', swordClipFrontR, swordItem, {48, 66})
buildWeaponCategory('Axe',   axeClipFrontR,   axeItem,   {36, 55})

writeJson('characters/orc-v1/source/complete-v1/authored-geometry.json', authoredGeometry)
print('author-main-orc-complete.lua: artistic recovery complete across all 4 directions x 7 actions.')
