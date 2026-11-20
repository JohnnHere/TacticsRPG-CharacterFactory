-- Experiment 04 — Hybrid Weapon Architecture (Architecture C)
-- Pilot B2: Rear-Right Sword Reuse (back_r / Sword)
-- Deterministic Aseprite Lua composition script.
-- Preserves body and handFront 100% unchanged; reuses back_r weaponBack/weaponFront split.

local stage = app.params["stage"] or "full"
local expDir = "experiments/main-orc-hybrid-weapon-04b2"
local srcClipDir = "characters/orc-v1/source/combat-recovery-v8/rear-arc/back_r-sword"
local srcMaster = srcClipDir .. "/source/composite.aseprite"
local swordBPng = expDir .. "/variants/sword-b/sword.png"

-- Declared/fitted integer grip pivots and rotations for back_r-sword (14 frames, 1-indexed in Lua)
-- F00 (1) .. F13 (14); weapon visible F02 (3) .. F11 (12)
local frameMeta = {
  [1]  = { idx = 0,  dur = 30,  vis = false },
  [2]  = { idx = 1,  dur = 65,  vis = false },
  [3]  = { idx = 2,  dur = 35,  vis = true, gx = 163, gy = 131, rot = 20  },
  [4]  = { idx = 3,  dur = 50,  vis = true, gx = 168, gy = 98,  rot = 5   },
  [5]  = { idx = 4,  dur = 45,  vis = true, gx = 162, gy = 89,  rot = -10 },
  [6]  = { idx = 5,  dur = 35,  vis = true, gx = 155, gy = 86,  rot = -14 },
  [7]  = { idx = 6,  dur = 30,  vis = true, gx = 172, gy = 105, rot = 25  },
  [8]  = { idx = 7,  dur = 35,  vis = true, gx = 179, gy = 115, rot = 83  },
  [9]  = { idx = 8,  dur = 35,  vis = true, gx = 172, gy = 134, rot = 115 },
  [10] = { idx = 9,  dur = 100, vis = true, gx = 158, gy = 169, rot = 115 },
  [11] = { idx = 10, dur = 55,  vis = true, gx = 159, gy = 155, rot = 95  },
  [12] = { idx = 11, dur = 80,  vis = true, gx = 164, gy = 155, rot = 80  },
  [13] = { idx = 12, dur = 45,  vis = false },
  [14] = { idx = 13, dur = 90,  vis = false },
}

-- Representative frames for Stage A: F02 (prep/establish-grip), F05 (elevation/apex-hold), F08 (impact/contact), F11 (recovery/settle-grip)
local repFrameIndices = { 3, 6, 9, 12 } -- 1-based Lua frame numbers corresponding to F02, F05, F08, F11

local swordAPng = expDir .. "/variants/sword-a/sword.png"
local swordASpr = app.open(swordAPng)
if not swordASpr then
  error("Failed to open Sword A PNG: " .. swordAPng)
end
local swordAImg = Image(swordASpr.width, swordASpr.height, ColorMode.RGB)
swordAImg:drawSprite(swordASpr, 1)
swordASpr:close()

local swordBSpr = app.open(swordBPng)
if not swordBSpr then
  error("Failed to open Sword B PNG: " .. swordBPng)
end
local swordBImg = Image(swordBSpr.width, swordBSpr.height, ColorMode.RGB)
swordBImg:drawSprite(swordBSpr, 1)
swordBSpr:close()

local bladeMinUA = {}
local bladeMaxUA = {}
local bladeMinU = {}
local bladeMaxU = {}
for v = 0, 54 do
  local minUA, maxUA = nil, nil
  local minUB, maxUB = nil, nil
  for u = 0, swordBImg.width - 1 do
    local pxA = swordAImg:getPixel(u, v)
    if app.pixelColor.rgbaA(pxA) > 0 then
      if minUA == nil or u < minUA then minUA = u end
      if maxUA == nil or u > maxUA then maxUA = u end
    end
    local pxB = swordBImg:getPixel(u, v)
    if app.pixelColor.rgbaA(pxB) > 0 then
      if minUB == nil or u < minUB then minUB = u end
      if maxUB == nil or u > maxUB then maxUB = u end
    end
  end
  bladeMinUA[v] = minUA
  bladeMaxUA[v] = maxUA
  bladeMinU[v] = minUB
  bladeMaxU[v] = maxUB
end

local gripU = 48
local gripV = 66
local stats = {}

local function findLayer(spr, name)
  for _, lyr in ipairs(spr.layers) do
    if lyr.name == name then return lyr end
  end
  error("Layer not found: " .. name)
end

local function repaintBladeToVariantB(spr, frameNumbers, recordStats)
  local wbLyr = findLayer(spr, "weaponBack")
  local wfLyr = findLayer(spr, "weaponFront")

  for _, fNum in ipairs(frameNumbers) do
    local meta = frameMeta[fNum]
    if meta and meta.vis then
      local rad = meta.rot * math.pi / 180.0
      local c = math.cos(rad)
      local s = math.sin(rad)
      local gx = meta.gx
      local gy = meta.gy

      local replacedCount = 0
      local preservedHiltCount = 0

      for _, lyr in ipairs({ wbLyr, wfLyr }) do
        local cel = lyr:cel(fNum)
        if cel then
          local img = cel.image:clone()
          local ox = cel.position.x
          local oy = cel.position.y
          for y = 0, img.height - 1 do
            for x = 0, img.width - 1 do
              local px = img:getPixel(x, y)
              local a = app.pixelColor.rgbaA(px)
              if a > 0 then
                local cx = ox + x
                local cy = oy + y
                local dx = cx - gx
                local dy = cy - gy
                local u = math.floor(dx * c + dy * s + gripU + 0.5)
                local v = math.floor(-dx * s + dy * c + gripV + 0.5)
                local r = app.pixelColor.rgbaR(px)
                local g = app.pixelColor.rgbaG(px)
                local b = app.pixelColor.rgbaB(px)
                local maxC = math.max(r, g, b)
                -- v <= 54 is blade; v == 55 with bright blade metal (maxC > 40) is rotation rounding at blade-guard seam
                if (v >= 0 and v <= 54) or (v == 55 and maxC > 40) then
                  local vc = math.max(7, math.min(54, v))
                  local minU = bladeMinU[vc]
                  local maxU = bladeMaxU[vc]
                  local minUA = bladeMinUA[vc] or minU
                  local maxUA = bladeMaxUA[vc] or maxU
                  if minU ~= nil and maxU ~= nil then
                    local uc
                    if maxC <= 32 or maxU - minU <= 2 then
                      -- Preserve 1px dark outline on outer silhouette edge or narrow tip
                      uc = (u <= 48) and minU or maxU
                    else
                      -- Map interior blade metal proportionally onto Sword B's interior faceted steel bevel
                      local inMinA = minUA + 1
                      local inMaxA = math.max(inMinA, maxUA - 1)
                      local inMinB = minU + 1
                      local inMaxB = math.max(inMinB, maxU - 1)
                      local t = (u - inMinA) / math.max(1, inMaxA - inMinA)
                      t = math.max(0.0, math.min(1.0, t))
                      uc = math.floor(inMinB + t * (inMaxB - inMinB) + 0.5)
                    end
                    local bPx = swordBImg:getPixel(uc, vc)
                    if app.pixelColor.rgbaA(bPx) > 0 then
                      img:drawPixel(x, y, bPx)
                      replacedCount = replacedCount + 1
                    end
                  end
                else
                  preservedHiltCount = preservedHiltCount + 1
                end
              end
            end
          end
          cel.image = img
        end
      end

      if recordStats then
        local fKey = string.format("F%02d", meta.idx)
        stats[fKey] = {
          frame = meta.idx,
          rightGrip = { gx, gy },
          rotationDeg = meta.rot,
          bladePixelsRepainted = replacedCount,
          hiltPixelsPreserved = preservedHiltCount,
        }
      end
    end
  end
end

local function exportStageDir(masterPath, outDir, frameMap)
  local spr = app.open(masterPath)
  if not spr then error("Failed to reopen saved master: " .. masterPath) end

  local wbLyr = findLayer(spr, "weaponBack")
  local bodyLyr = findLayer(spr, "body")
  local wfLyr = findLayer(spr, "weaponFront")
  local hfLyr = findLayer(spr, "handFront")

  local function renderVisibleSubset(visWb, visBody, visWf, visHf, subDir, makeStrip)
    wbLyr.isVisible = visWb
    bodyLyr.isVisible = visBody
    wfLyr.isVisible = visWf
    hfLyr.isVisible = visHf

    local nFrames = #spr.frames
    local stripImg = nil
    if makeStrip then
      stripImg = Image(spr.width * nFrames, spr.height, ColorMode.RGB)
    end

    for i = 1, nFrames do
      local fImg = Image(spr.width, spr.height, ColorMode.RGB)
      fImg:drawSprite(spr, i)
      local origIdx = frameMap[i]
      local fCode = string.format("F%02d", origIdx)
      local numCode = string.format("%02d", origIdx)
      fImg:saveAs(outDir .. "/" .. subDir .. "/" .. fCode .. ".png")
      fImg:saveAs(outDir .. "/" .. subDir .. "/" .. numCode .. ".png")
      if stripImg then
        stripImg:drawImage(fImg, Point((i - 1) * spr.width, 0))
      end
    end

    if stripImg then
      stripImg:saveAs(outDir .. "/strip.png")
    end
  end

  renderVisibleSubset(true, true, true, true, "composite", true)
  renderVisibleSubset(false, true, false, true, "body-only", false)
  renderVisibleSubset(true, false, true, false, "weapon-only", false)
  renderVisibleSubset(true, false, false, false, "layers/weaponBack", false)
  renderVisibleSubset(false, true, false, false, "layers/body", false)
  renderVisibleSubset(false, false, true, false, "layers/weaponFront", false)
  renderVisibleSubset(false, false, false, true, "layers/handFront", false)

  local durations = {}
  for i = 1, #spr.frames do
    local origIdx = frameMap[i]
    local ms = math.floor(spr.frames[i].duration * 1000 + 0.5)
    table.insert(durations, string.format('  { "frame": %d, "code": "F%02d", "durationMs": %d }', origIdx, origIdx, ms))
  end
  local f = io.open(outDir .. "/frame-durations.json", "w")
  f:write("[\n" .. table.concat(durations, ",\n") .. "\n]\n")
  f:close()

  spr:close()
end

local function buildRepresentative(variant)
  local outDir = expDir .. "/representative/" .. variant
  local spr = app.open(srcMaster)
  if not spr then error("Failed to open source master: " .. srcMaster) end

  for i = 1, 14 do
    spr.frames[i].duration = frameMeta[i].dur / 1000.0
  end

  if variant == "b" then
    repaintBladeToVariantB(spr, repFrameIndices, false)
  end

  -- Delete frames not in repFrameIndices in reverse order
  local keep = {}
  for _, idx in ipairs(repFrameIndices) do keep[idx] = true end
  for i = 14, 1, -1 do
    if not keep[i] then
      spr:deleteFrame(i)
    end
  end

  local masterOut = outDir .. "/composite.aseprite"
  spr:saveAs(masterOut)
  spr:close()

  local repOrigMap = { 2, 5, 8, 11 }
  exportStageDir(masterOut, outDir, repOrigMap)
end

local function buildFull(variant)
  local outDir = expDir .. "/full/" .. variant
  local spr = app.open(srcMaster)
  if not spr then error("Failed to open source master: " .. srcMaster) end

  local allFrames = {}
  local origMap = {}
  for i = 1, 14 do
    spr.frames[i].duration = frameMeta[i].dur / 1000.0
    table.insert(allFrames, i)
    origMap[i] = i - 1
  end

  if variant == "b" then
    repaintBladeToVariantB(spr, allFrames, true)
  end

  local masterOut = outDir .. "/composite.aseprite"
  spr:saveAs(masterOut)
  spr:close()

  exportStageDir(masterOut, outDir, origMap)
end

if stage == "representative" then
  buildRepresentative("a")
  buildRepresentative("b")
elseif stage == "full" then
  buildFull("a")
  buildFull("b")
  local sf = io.open(expDir .. "/blade-repaint-stats.json", "w")
  sf:write("{\n")
  local keys = {}
  for k in pairs(stats) do table.insert(keys, k) end
  table.sort(keys)
  local entries = {}
  for _, k in ipairs(keys) do
    local st = stats[k]
    table.insert(entries, string.format(
      '  "%s": { "frame": %d, "rightGrip": [%d, %d], "rotationDeg": %d, "bladePixelsRepainted": %d, "hiltPixelsPreserved": %d }',
      k, st.frame, st.rightGrip[1], st.rightGrip[2], st.rotationDeg, st.bladePixelsRepainted, st.hiltPixelsPreserved
    ))
  end
  sf:write(table.concat(entries, ",\n") .. "\n}\n")
  sf:close()
else
  error("Unknown stage: " .. tostring(stage))
end
