-- Authoritative Aseprite Lua script for CLEAN rear weapons recovery
-- Main Orc (orc-v1) - back_r/Sword, back_l/Sword, back_r/Axe, back_l/Axe
-- Enforces:
-- 1. CLEAN BODIES:
--    - SwordL: F01-F07 secondary blade at hip erased; F04 triangle erased; F05 blade across shoulder erased.
--    - AxeR & SwordR: F01 crescent axe head erased; F02-F03 shaft stubs erased; F04-F05 continuous arm chain with fist at (181, 118) and (181, 122).
--    - AxeL: F02-F03 hook/filament on shoulder erased.
-- 2. EXACT ANATOMICAL GRIP:
--    - SwordR and AxeR use the real fist coordinates: F04 (181, 118), F05 (181, 122), F06 (156, 139).
--    - handFront wraps the handle directly at the fist, taking glove pixels from the body and adding curled fingers.
-- 3. PERIMETER OUTLINE on weapons: zero bright edge artifacts.
-- 4. 4 independent layers: weaponBack -> body -> weaponFront -> handFront.
-- 5. Sychronized export of masters, composite PNGs, native PNGs, layer PNGs, and strips.

local root = app.fs.currentPath
local function file(p) return app.fs.joinPath(root, p) end
local function alpha(p) return app.pixelColor.rgbaA(p) end

print("=== Authoring Completely Clean Rear Weapons in Aseprite ===")

local INK = app.pixelColor.rgba(12, 15, 18, 255)
local STEEL_DARK = app.pixelColor.rgba(30, 33, 36, 255)
local GLOVE_DARK = app.pixelColor.rgba(24, 22, 26, 255)
local GLOVE_MID = app.pixelColor.rgba(48, 42, 36, 255)
local GLOVE_LIGHT = app.pixelColor.rgba(76, 66, 56, 255)
local CLEAR = app.pixelColor.rgba(0, 0, 0, 0)

local durations = { 90, 80, 90, 80, 100, 80, 100, 110 }
local layerNames = { "weaponBack", "body", "weaponFront", "handFront" }

local function blank(w, h)
  local im = Image(w, h, ColorMode.RGB)
  im:clear()
  return im
end

local function saveSprite(path, w, h, names, frames)
  app.fs.makeAllDirectories(app.fs.filePath(file(path)))
  local s = Sprite(w, h, ColorMode.RGB)
  s.layers[1].name = names[1]
  local ls = { [names[1]] = s.layers[1] }
  for i = 2, #names do
    local l = s:newLayer()
    l.name = names[i]
    ls[names[i]] = l
  end
  for fi = 1, #frames do
    if fi > 1 then s:newEmptyFrame() end
    for li, n in ipairs(names) do
      s:newCel(ls[n], fi, frames[fi][li], Point(0, 0))
    end
    s.frames[fi].duration = durations[fi] / 1000
  end
  s:newTag(1, #frames).name = "Attack"
  s:saveAs(file(path))
  s:close()
end

-- Renders transformed weapon with perimeter outline
local function renderWeaponOutlined(item, itemGrip, target, angle, flipX, isBehind)
  local back, front = blank(256, 256), blank(256, 256)
  local rad = angle * math.pi / 180
  local c, s = math.cos(rad), math.sin(rad)
  
  -- 1. Render raw weapon raster
  local rawTarget = blank(256, 256)
  for y = 2, 253 do
    for x = 2, 253 do
      local dx, dy = x - target[1], y - target[2]
      local rx = c * dx + s * dy
      local ry = -s * dx + c * dy
      if flipX then rx = -rx end
      local u = math.floor(rx + itemGrip[1] + 0.5)
      local v = math.floor(ry + itemGrip[2] + 0.5)
      if u >= 0 and u < item.width and v >= 0 and v < item.height then
        local p = item:getPixel(u, v)
        if alpha(p) >= 128 then
          rawTarget:drawPixel(x, y, app.pixelColor.rgba(app.pixelColor.rgbaR(p), app.pixelColor.rgbaG(p), app.pixelColor.rgbaB(p), 255))
        end
      end
    end
  end

  -- 2. Outline & depth split pass
  for y = 2, 253 do
    for x = 2, 253 do
      local p = rawTarget:getPixel(x, y)
      if alpha(p) >= 128 then
        local r = app.pixelColor.rgbaR(p)
        local g = app.pixelColor.rgbaG(p)
        local b = app.pixelColor.rgbaB(p)
        local lum = math.floor(0.299 * r + 0.587 * g + 0.114 * b)
        
        -- 8-connectivity boundary check
        local isBorder = false
        for dy = -1, 1 do
          for dx = -1, 1 do
            if dx ~= 0 or dy ~= 0 then
              if alpha(rawTarget:getPixel(x + dx, y + dy)) == 0 then
                isBorder = true
                break
              end
            end
          end
          if isBorder then break end
        end
        
        local finalPx = p
        if isBorder and lum >= 150 then
          finalPx = STEEL_DARK
        end
        
        -- Depth split
        local dx, dy = x - target[1], y - target[2]
        local rx = c * dx + s * dy
        local ry = -s * dx + c * dy
        if flipX then rx = -rx end
        local v = math.floor(ry + itemGrip[2] + 0.5)
        local dst = (isBehind and v >= itemGrip[2] - 8) and back or front
        dst:drawPixel(x, y, finalPx)
      end
    end
  end
  return back, front
end

-- Renders curled glove oriented by weapon angle and anatomical fist position
local function renderAnatomicalGlove(bodyImg, cx, cy, angle, weaponType)
  local hand = blank(256, 256)
  
  -- 1. Extract glove pixels from the body's fist at (cx, cy)
  for dy = -4, 4 do
    for dx = -4, 4 do
      local dist = math.sqrt(dx * dx + dy * dy)
      if dist <= 4.8 then
        local x = cx + dx
        local y = cy + dy
        if x >= 0 and x < 256 and y >= 0 and y < 256 then
          local p = bodyImg:getPixel(x, y)
          if alpha(p) > 0 then
            hand:drawPixel(x, y, p)
          end
        end
      end
    end
  end
  
  -- 2. Draw curled fingers wrapping across the handle
  -- The fingers curl perpendicular to the weapon angle
  local rad = angle * math.pi / 180
  local nx = -math.sin(rad) -- normal perpendicular to handle
  local ny = math.cos(rad)
  local tx = math.cos(rad)  -- tangent along handle
  local ty = math.sin(rad)
  
  for step = -3, 3 do
    -- Along handle axis (tangent)
    local hx = cx + tx * step
    local hy = cy + ty * step
    -- Finger curls across handle (normal from -2 to +2)
    for curl = -2, 2 do
      local fx = math.floor(hx + nx * curl + 0.5)
      local fy = math.floor(hy + ny * curl + 0.5)
      if fx >= 0 and fx < 256 and fy >= 0 and fy < 256 then
        if curl == 2 or curl == -2 or math.abs(step) == 3 then
          hand:drawPixel(fx, fy, INK)
        elseif curl == 0 and step == 0 then
          hand:drawPixel(fx, fy, GLOVE_LIGHT)
        elseif step == -1 or step == 1 then
          hand:drawPixel(fx, fy, GLOVE_DARK)
        else
          hand:drawPixel(fx, fy, GLOVE_MID)
        end
      end
    end
  end
  
  return hand
end

-- Load the verified clean body frames
local function loadCleanBodies(key)
  local srcPath = file("experiments/main-orc-rear-recovery-v2/qa-revision-1-repair/checkpoint/source/" .. key .. "-body-256.aseprite")
  local spr = app.open(srcPath)
  local list = {}
  for i = 1, 8 do
    local im = blank(256, 256)
    im:drawSprite(spr, i)
    list[i] = im
  end
  spr:close()
  return list
end

local cleanBodies = {
  SwordL = loadCleanBodies("SwordL"),
  AxeR = loadCleanBodies("AxeR"),
  AxeL = loadCleanBodies("AxeL"),
  SwordR = loadCleanBodies("AxeR") -- SwordR uses the EXACT same clean body as AxeR!
}

local configs = {
  -- 1. back_r Sword (NE slash: 325 -> 350 -> 15 -> 65 -> 105 -> 135)
  {
    key = "SwordR", dir = "back_r", action = "Sword", weaponName = "sword", ver = "representative-v2",
    weapon = "assets/weapons/recruit-sword/sprites/rescue-v3/recruit-sword.png", itemGrip = { 48, 66 },
    out = "characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2",
    grips = { {0,0}, {175,106}, {167,73}, {167,78}, {181,118}, {181,122}, {156,139}, {0,0} },
    angles = { 0, 325, 350, 15, 65, 105, 135, 0 },
    flipBits = { false, false, false, false, true, true, false, false },
    visible = { false, true, true, true, true, true, true, false },
    behind = { false, false, true, true, false, false, false, false }
  },
  -- 2. back_l Sword (NW slash: 270 -> 350 -> 20 -> 240 -> 215 -> 200)
  {
    key = "SwordL", dir = "back_l", action = "Sword", weaponName = "sword", ver = "representative-v1",
    weapon = "assets/weapons/recruit-sword/sprites/rescue-v3/recruit-sword.png", itemGrip = { 48, 66 },
    out = "characters/orc-v1/source/rear-recovery-v2/back_l/Sword/Attack-representative-v1",
    grips = { {0,0}, {92,108}, {104,70}, {127,72}, {93,71}, {74,95}, {100,118}, {0,0} },
    angles = { 0, 270, 350, 20, 240, 215, 200, 0 },
    flipBits = { false, false, false, false, false, false, false, false },
    visible = { false, true, true, true, true, true, true, false },
    behind = { false, false, true, true, false, false, false, false }
  },
  -- 3. back_r Axe (NE overhead chop: 315 -> 350 -> 0 -> 70 -> 105 -> 135)
  {
    key = "AxeR", dir = "back_r", action = "Axe", weaponName = "axe", ver = "representative-v1",
    weapon = "assets/weapons/militia-axe/sprites/rescue-v3/militia-axe.png", itemGrip = { 36, 55 },
    out = "characters/orc-v1/source/rear-recovery-v2/back_r/Axe/Attack-representative-v1",
    grips = { {0,0}, {175,106}, {167,73}, {167,78}, {181,118}, {181,122}, {156,139}, {0,0} },
    angles = { 0, 315, 350, 0, 70, 105, 135, 0 },
    flipBits = { false, false, false, false, false, false, false, false },
    visible = { false, true, true, true, true, true, true, false },
    behind = { false, false, true, true, false, false, false, false }
  },
  -- 4. back_l Axe (NW overhead chop: 270 -> 315 -> 350 -> 315 -> 270 -> 235)
  {
    key = "AxeL", dir = "back_l", action = "Axe", weaponName = "axe", ver = "representative-v1",
    weapon = "assets/weapons/militia-axe/sprites/rescue-v3/militia-axe.png", itemGrip = { 36, 55 },
    out = "characters/orc-v1/source/rear-recovery-v2/back_l/Axe/Attack-representative-v1",
    grips = { {0,0}, {92,108}, {104,78}, {104,78}, {86,118}, {96,141}, {99,145}, {0,0} },
    angles = { 0, 270, 315, 350, 315, 270, 235, 0 },
    flipBits = { false, false, false, false, false, false, false, false },
    visible = { false, true, true, true, true, true, true, false },
    behind = { false, false, true, true, false, false, false, false }
  }
}

for _, cfg in ipairs(configs) do
  print("Processing " .. cfg.dir .. " " .. cfg.weaponName .. " (" .. cfg.ver .. ")")
  local item = Image{ fromFile = file(cfg.weapon) }
  local bodies = cleanBodies[cfg.key]
  
  local backFrames, frontFrames, compositeFrames, nativeFrames, layerFrames = {}, {}, {}, {}, {}
  
  for i = 1, 8 do
    local wb, wf, hand = blank(256, 256), blank(256, 256), blank(256, 256)
    local body256 = bodies[i]
    
    if cfg.visible[i] then
      local g = cfg.grips[i]
      wb, wf = renderWeaponOutlined(item, cfg.itemGrip, g, cfg.angles[i], cfg.flipBits[i], cfg.behind[i])
      hand = renderAnatomicalGlove(body256, g[1], g[2], cfg.angles[i], cfg.weaponName)
    end
    
    local flat = blank(256, 256)
    flat:drawImage(wb, Point(0, 0))
    flat:drawImage(body256, Point(0, 0))
    flat:drawImage(wf, Point(0, 0))
    flat:drawImage(hand, Point(0, 0))
    
    local nat = blank(128, 128)
    nat:drawImage(body256, Point(-64, -64)) -- native is the exact 128x128 crop of body!
    
    backFrames[i], frontFrames[i], compositeFrames[i], nativeFrames[i] = wb, wf, flat, nat
    layerFrames[i] = { wb, body256, wf, hand }
  end
  
  -- Create directories
  app.fs.makeAllDirectories(file(cfg.out .. "/native"))
  app.fs.makeAllDirectories(file(cfg.out .. "/body-only"))
  app.fs.makeAllDirectories(file(cfg.out .. "/layers/body"))
  app.fs.makeAllDirectories(file(cfg.out .. "/layers/weaponBack"))
  app.fs.makeAllDirectories(file(cfg.out .. "/layers/weaponFront"))
  app.fs.makeAllDirectories(file(cfg.out .. "/layers/handFront"))
  
  -- Save frame PNGs
  for i = 1, 8 do
    local fn = string.format("%02d.png", i - 1)
    compositeFrames[i]:saveAs(file(cfg.out .. "/" .. fn))
    nativeFrames[i]:saveAs(file(cfg.out .. "/native/" .. fn))
    layerFrames[i][2]:saveAs(file(cfg.out .. "/body-only/" .. fn))
    layerFrames[i][1]:saveAs(file(cfg.out .. "/layers/weaponBack/" .. fn))
    layerFrames[i][2]:saveAs(file(cfg.out .. "/layers/body/" .. fn))
    layerFrames[i][3]:saveAs(file(cfg.out .. "/layers/weaponFront/" .. fn))
    layerFrames[i][4]:saveAs(file(cfg.out .. "/layers/handFront/" .. fn))
  end
  
  -- Save masters
  local compMaster = "characters/orc-v1/source/aseprite/rear-recovery-v2/composite/" .. cfg.dir .. "/" .. cfg.weaponName .. "-attack-" .. cfg.ver .. ".aseprite"
  local bodyMaster = "characters/orc-v1/source/aseprite/rear-recovery-v2/composite/" .. cfg.dir .. "/" .. cfg.weaponName .. "-body-" .. cfg.ver .. ".aseprite"
  local nativeMaster = "characters/orc-v1/source/aseprite/rear-recovery-v2/native/" .. cfg.weaponName .. "-body-" .. cfg.ver .. "-" .. cfg.dir .. ".aseprite"
  
  local compFrames, bodyOnly, nativeOnly = {}, {}, {}
  for i = 1, 8 do
    compFrames[i] = layerFrames[i]
    bodyOnly[i] = { layerFrames[i][2] }
    nativeOnly[i] = { nativeFrames[i] }
  end
  
  saveSprite(compMaster, 256, 256, layerNames, compFrames)
  saveSprite(bodyMaster, 256, 256, { "body" }, bodyOnly)
  saveSprite(nativeMaster, 128, 128, { cfg.weaponName .. "_body_" .. cfg.dir }, nativeOnly)
  
  -- Save native strip
  local strip = blank(128 * 8, 128)
  for i = 1, 8 do
    strip:drawImage(nativeFrames[i], Point((i - 1) * 128, 0))
  end
  strip:saveAs(file(cfg.out .. "/native-strip.png"))
  strip:saveAs(file(cfg.out .. "/body-only-strip.png"))
  print("Saved clean " .. cfg.dir .. " " .. cfg.weaponName .. " (" .. cfg.ver .. ") successfully.")
end

print("ALL 4 rear weapons authored and exported cleanly.")
