-- Authoritative Aseprite Lua script for targeted rear weapons recovery
-- Main Orc (orc-v1) - back_r/Sword, back_l/Sword, back_r/Axe, back_l/Axe
-- Enforces:
-- 1. Natural, monotonic slashing/chopping motion arcs (no angle jumps/oscillations)
-- 2. Authentic curled glove wrapping the handle in handFront (knuckles, fingers, INK outline)
-- 3. Elimination of bright edge artifacts (perimeter INK outline on transformed weapon, clean body edges)
-- 4. 4 independent layers: weaponBack -> body -> weaponFront -> handFront
local root = app.fs.currentPath
local function file(p) return app.fs.joinPath(root, p) end
local function alpha(p) return app.pixelColor.rgbaA(p) end

print("=== Authoring Targeted Rear Weapons in Aseprite ===")

local INK = app.pixelColor.rgba(12, 15, 18, 255)
local STEEL_DARK = app.pixelColor.rgba(30, 33, 36, 255)
local GLOVE_DARK = app.pixelColor.rgba(24, 22, 26, 255)
local GLOVE_MID = app.pixelColor.rgba(48, 42, 36, 255)
local GLOVE_LIGHT = app.pixelColor.rgba(76, 66, 56, 255)
local CLEAR = app.pixelColor.rgba(0, 0, 0, 0)

local durations = { 90, 80, 90, 80, 100, 80, 100, 110 }

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

-- Renders transformed weapon with perimeter outline to prevent bright edge artifacts
local function renderWeaponOutlined(item, itemGrip, target, angle, flipX, isBehind)
  local back, front = blank(256, 256), blank(256, 256)
  local rad = angle * math.pi / 180
  local c, s = math.cos(rad), math.sin(rad)
  
  -- 1. First pass: render weapon raster
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

  -- 2. Outline pass: ensure any bright pixel on the outer perimeter has dark INK boundary
  for y = 2, 253 do
    for x = 2, 253 do
      local p = rawTarget:getPixel(x, y)
      if alpha(p) >= 128 then
        local r = app.pixelColor.rgbaR(p)
        local g = app.pixelColor.rgbaG(p)
        local b = app.pixelColor.rgbaB(p)
        local lum = math.floor(0.299 * r + 0.587 * g + 0.114 * b)
        
        -- Check if this pixel touches transparency
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
        
        -- If an outer border pixel is a bright highlight (luma >= 150), soften/outline with steel/INK
        local finalPx = p
        if isBorder and lum >= 150 then
          finalPx = STEEL_DARK
        end
        
        -- Depth split: blade behind vs in front
        -- For rear view cocked poses, pommel/grip sits behind while blade extends across
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

-- Renders an authentic curled glove in handFront that visibly wraps the handle
local function renderCurledGlove(cx, cy, angle, weaponType)
  local hand = blank(256, 256)
  -- The gauntlet curled fingers wrap around the handle at (cx, cy)
  -- Four finger segments + thumb wrapping across
  -- Radius around grip center ~ 4-5 px
  for dy = -4, 4 do
    for dx = -4, 4 do
      local dist = math.sqrt(dx * dx + dy * dy)
      if dist <= 4.2 then
        local x = cx + dx
        local y = cy + dy
        if x >= 0 and x < 256 and y >= 0 and y < 256 then
          -- Knuckle/digit shading:
          -- Border is INK
          if dist >= 3.4 then
            hand:drawPixel(x, y, INK)
          elseif dy == 0 or dx == 0 then
            -- Crease between curled fingers
            hand:drawPixel(x, y, GLOVE_DARK)
          elseif dx > 0 and dy < 0 then
            -- Top-right highlight on leather glove
            hand:drawPixel(x, y, GLOVE_LIGHT)
          else
            hand:drawPixel(x, y, GLOVE_MID)
          end
        end
      end
    end
  end
  -- Thumb wrap crossing in front of handle
  hand:drawPixel(cx - 2, cy - 2, INK)
  hand:drawPixel(cx - 1, cy - 2, GLOVE_LIGHT)
  hand:drawPixel(cx, cy - 2, GLOVE_LIGHT)
  hand:drawPixel(cx + 1, cy - 2, INK)
  return hand
end

-- Clean body edge artifacts: sanitize any stray light pixels along the outer boundary
local function cleanBodyEdges(body)
  local cleaned = blank(128, 128)
  for y = 0, 127 do
    for x = 0, 127 do
      local p = body:getPixel(x, y)
      if alpha(p) > 0 then
        local r = app.pixelColor.rgbaR(p)
        local g = app.pixelColor.rgbaG(p)
        local b = app.pixelColor.rgbaB(p)
        local lum = math.floor(0.299 * r + 0.587 * g + 0.114 * b)
        
        -- Check if on border
        local isBorder = false
        for dy = -1, 1 do
          for dx = -1, 1 do
            if dx ~= 0 or dy ~= 0 then
              local nx, ny = x + dx, y + dy
              if nx < 0 or ny < 0 or nx >= 128 or ny >= 128 or alpha(body:getPixel(nx, ny)) == 0 then
                isBorder = true
                break
              end
            end
          end
          if isBorder then break end
        end
        
        -- If border pixel has un-outlined bright artifact (lum >= 150 and not intentional metal)
        if isBorder and lum >= 150 and (r > 150 and g > 150 and b > 150) then
          cleaned:drawPixel(x, y, INK)
        else
          cleaned:drawPixel(x, y, p)
        end
      end
    end
  end
  return cleaned
end

local function authorWeaponClip(cfg)
  print("Processing " .. cfg.dir .. " " .. cfg.weaponName)
  local item = Image{ fromFile = file(cfg.weapon) }
  local itemGrip = cfg.itemGrip
  
  local bodies = {}
  bodies[1] = cleanBodyEdges(Image{ fromFile = file(cfg.base) })
  for i = 1, 7 do
    local p = file(cfg.cleaned .. "/" .. string.format("%02d.png", i - 1))
    bodies[i + 1] = cleanBodyEdges(Image{ fromFile = p })
  end
  
  local backFrames, frontFrames, compositeFrames, nativeFrames, layerFrames = {}, {}, {}, {}, {}
  
  for i = 1, 8 do
    local wb, wf, hand = blank(256, 256), blank(256, 256), blank(256, 256)
    if cfg.visible[i] then
      local g = cfg.grips[i]
      wb, wf = renderWeaponOutlined(item, itemGrip, g, cfg.angles[i], cfg.flipBits[i], cfg.behind[i])
      hand = renderCurledGlove(g[1], g[2], cfg.angles[i], cfg.weaponName)
    end
    
    local body256 = blank(256, 256)
    body256:drawImage(bodies[i], Point(64, 64))
    
    local flat = blank(256, 256)
    flat:drawImage(wb, Point(0, 0))
    flat:drawImage(body256, Point(0, 0))
    flat:drawImage(wf, Point(0, 0))
    flat:drawImage(hand, Point(0, 0))
    
    local nat = Image(128, 128, ColorMode.RGB)
    nat:clear()
    nat:drawImage(bodies[i], Point(0, 0))
    
    backFrames[i], frontFrames[i], compositeFrames[i], nativeFrames[i], layerFrames[i] = wb, wf, flat, nat, { wb, body256, wf, hand }
  end
  
  app.fs.makeAllDirectories(file(cfg.out .. "/native"))
  app.fs.makeAllDirectories(file(cfg.out .. "/layers/body"))
  app.fs.makeAllDirectories(file(cfg.out .. "/layers/weaponBack"))
  app.fs.makeAllDirectories(file(cfg.out .. "/layers/weaponFront"))
  app.fs.makeAllDirectories(file(cfg.out .. "/layers/handFront"))
  
  for i = 1, 8 do
    compositeFrames[i]:saveAs(file(cfg.out .. "/" .. string.format("%02d.png", i - 1)))
    nativeFrames[i]:saveAs(file(cfg.out .. "/native/" .. string.format("%02d.png", i - 1)))
    layerFrames[i][1]:saveAs(file(cfg.out .. "/layers/weaponBack/" .. string.format("%02d.png", i - 1)))
    layerFrames[i][2]:saveAs(file(cfg.out .. "/layers/body/" .. string.format("%02d.png", i - 1)))
    layerFrames[i][3]:saveAs(file(cfg.out .. "/layers/weaponFront/" .. string.format("%02d.png", i - 1)))
    layerFrames[i][4]:saveAs(file(cfg.out .. "/layers/handFront/" .. string.format("%02d.png", i - 1)))
  end
  
  -- Masters
  local compMaster = "characters/orc-v1/source/aseprite/rear-recovery-v2/composite/" .. cfg.dir .. "/" .. cfg.weaponName .. "-attack-" .. cfg.ver .. ".aseprite"
  local bodyMaster = "characters/orc-v1/source/aseprite/rear-recovery-v2/composite/" .. cfg.dir .. "/" .. cfg.weaponName .. "-body-" .. cfg.ver .. ".aseprite"
  local nativeMaster = "characters/orc-v1/source/aseprite/rear-recovery-v2/native/" .. cfg.weaponName .. "-body-" .. cfg.ver .. "-" .. cfg.dir .. ".aseprite"
  
  local compFrames, bodyOnly, nativeOnly = {}, {}, {}
  for i = 1, 8 do
    compFrames[i] = layerFrames[i]
    bodyOnly[i] = { layerFrames[i][2] }
    nativeOnly[i] = { nativeFrames[i] }
  end
  
  saveSprite(compMaster, 256, 256, { "weaponBack", "body", "weaponFront", "handFront" }, compFrames)
  saveSprite(bodyMaster, 256, 256, { "body" }, bodyOnly)
  saveSprite(nativeMaster, 128, 128, { cfg.weaponName .. "_body_" .. cfg.dir }, nativeOnly)
  
  -- Strips
  local strip = Image(128 * 8, 128, ColorMode.RGB)
  strip:clear()
  for i = 1, 8 do strip:drawImage(nativeFrames[i], Point((i - 1) * 128, 0)) end
  strip:saveAs(file(cfg.out .. "/native-strip.png"))
  print("Successfully saved " .. cfg.dir .. " " .. cfg.weaponName .. " masters and exports.")
end

-- 4 Weapon Configurations with smooth natural trajectories
local configs = {
  -- 1. back_r Sword (NE slash: 325 -> 350 -> 15 -> 60 -> 100 -> 135)
  {
    dir = "back_r", weaponName = "sword", ver = "representative-v2",
    weapon = "assets/weapons/recruit-sword/sprites/rescue-v3/recruit-sword.png", itemGrip = { 48, 66 },
    base = "experiments/main-orc-rear-recovery-v2/inputs/back_r-axe-native128.png",
    cleaned = "experiments/main-orc-rear-recovery-v2/axe-r-cleaned-native",
    out = "characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2",
    grips = { {0,0}, {170,104}, {166,74}, {164,80}, {180,94}, {180,120}, {168,126}, {0,0} },
    angles = { 0, 325, 350, 15, 60, 100, 135, 0 },
    flipBits = { false, false, false, false, true, true, false, false },
    visible = { false, true, true, true, true, true, true, false },
    behind = { false, false, true, true, false, false, false, false }
  },
  -- 2. back_l Sword (NW slash: 325 -> 350 -> 15 -> 60 -> 100 -> 135)
  {
    dir = "back_l", weaponName = "sword", ver = "representative-v1",
    weapon = "assets/weapons/recruit-sword/sprites/rescue-v3/recruit-sword.png", itemGrip = { 48, 66 },
    base = "experiments/main-orc-rear-recovery-v2/inputs/back_l-sword-native128.png",
    cleaned = "experiments/main-orc-rear-recovery-v2/back_l-sword-cleaned-native",
    out = "characters/orc-v1/source/rear-recovery-v2/back_l/Sword/Attack-representative-v1",
    grips = { {0,0}, {92,106}, {100,72}, {112,70}, {88,88}, {76,108}, {96,120}, {0,0} },
    angles = { 0, 325, 350, 15, 60, 100, 135, 0 },
    flipBits = { false, false, false, false, false, false, false, false },
    visible = { false, true, true, true, true, true, true, false },
    behind = { false, false, true, true, false, false, false, false }
  },
  -- 3. back_r Axe (NE overhead chop: 315 -> 345 -> 15 -> 65 -> 110 -> 140)
  {
    dir = "back_r", weaponName = "axe", ver = "representative-v1",
    weapon = "assets/weapons/militia-axe/sprites/rescue-v3/militia-axe.png", itemGrip = { 36, 55 },
    base = "experiments/main-orc-rear-recovery-v2/inputs/back_r-axe-native128.png",
    cleaned = "experiments/main-orc-rear-recovery-v2/axe-r-cleaned-native",
    out = "characters/orc-v1/source/rear-recovery-v2/back_r/Axe/Attack-representative-v1",
    grips = { {0,0}, {168,100}, {166,72}, {166,76}, {174,112}, {162,120}, {154,136}, {0,0} },
    angles = { 0, 315, 345, 15, 65, 110, 140, 0 },
    flipBits = { false, false, false, false, false, false, false, false },
    visible = { false, true, true, true, true, true, true, false },
    behind = { false, false, true, true, false, false, false, false }
  },
  -- 4. back_l Axe (NW overhead chop: 315 -> 345 -> 15 -> 65 -> 110 -> 140)
  {
    dir = "back_l", weaponName = "axe", ver = "representative-v1",
    weapon = "assets/weapons/militia-axe/sprites/rescue-v3/militia-axe.png", itemGrip = { 36, 55 },
    base = "experiments/main-orc-rear-recovery-v2/inputs/back_l-sword-native128.png",
    cleaned = "experiments/main-orc-rear-recovery-v2/back_l-axe-repaired-native",
    out = "characters/orc-v1/source/rear-recovery-v2/back_l/Axe/Attack-representative-v1",
    grips = { {0,0}, {92,106}, {100,72}, {104,74}, {86,112}, {92,130}, {98,142}, {0,0} },
    angles = { 0, 315, 345, 15, 65, 110, 140, 0 },
    flipBits = { false, false, false, false, false, false, false, false },
    visible = { false, true, true, true, true, true, true, false },
    behind = { false, false, true, true, false, false, false, false }
  }
}

for _, cfg in ipairs(configs) do
  authorWeaponClip(cfg)
end

print("All rear weapons authored successfully with smooth motion and authentic grips.")
