-- Authoritative Aseprite Lua script for stabilizing the left arm in back_r and back_l Walk
-- Eliminates contour temporal noise, holes and flickering
local root = app.fs.currentPath
local function isAbs(p)
  return string.sub(p, 2, 2) == ":" or string.sub(p, 1, 1) == "/" or string.sub(p, 1, 1) == "\\"
end
local function file(p)
  if isAbs(p) then return p end
  return app.fs.joinPath(root, p)
end
local function alpha(p) return app.pixelColor.rgbaA(p) end

print("=== Stabilizing Walk Left Arm in Aseprite ===")

local INK = app.pixelColor.rgba(12, 15, 18, 255)
local CLEAR = app.pixelColor.rgba(0, 0, 0, 0)
local ARMOR_SHADOW = app.pixelColor.rgba(32, 34, 38, 255)

local function blank(w, h)
  local im = Image(w, h, ColorMode.RGB)
  im:clear()
  return im
end

local function saveSprite(path, w, h, name, framesList)
  local full = file(path)
  app.fs.makeAllDirectories(app.fs.filePath(full))
  local s = Sprite(w, h, ColorMode.RGB)
  s.layers[1].name = name
  for i = 1, #framesList do
    if i > 1 then s:newEmptyFrame() end
    s:newCel(s.layers[1], i, framesList[i], Point(0, 0))
    s.frames[i].duration = 0.16 -- 160ms
  end
  s:newTag(1, #framesList).name = "Walk"
  s:saveAs(full)
  s:close()
end

for _, d in ipairs({ "back_r", "back_l" }) do
  local candDir = file(string.format("characters/orc-v1/source/rear-recovery-v2/%s/Walk", d))
  local natMaster = string.format("characters/orc-v1/source/aseprite/rear-recovery-v2/native/walk-%s.aseprite", d)
  local compMaster = string.format("characters/orc-v1/source/aseprite/rear-recovery-v2/composite/%s/walk-unarmed.aseprite", d)
  
  local frames = {}
  for fi = 1, 8 do
    frames[fi] = Image{ fromFile = app.fs.joinPath(candDir, string.format("%02d.png", fi - 1)) }
  end
  
  -- Temporal smoothing for left arm box: x: 88..115, y: 78..145
  for y = 78, 145 do
    for x = 88, 115 do
      local occ = {}
      for fi = 1, 8 do
        occ[fi] = alpha(frames[fi]:getPixel(x, y)) > 0
      end
      
      for fi = 1, 8 do
        local prev = fi == 1 and 8 or fi - 1
        local next = fi == 8 and 1 or fi + 1
        
        -- If pixel drops out for only 1 frame (101 pattern), fill it from prev frame
        if (not occ[fi]) and occ[prev] and occ[next] then
          local p = frames[prev]:getPixel(x, y)
          frames[fi]:drawPixel(x, y, p)
        end
        
        -- If pixel is on for only 1 isolated frame with no neighbors (010 pattern with isolated pixel)
        if occ[fi] and (not occ[prev]) and (not occ[next]) then
          local nOpaque = 0
          for dy = -1, 1 do
            for dx = -1, 1 do
              if (dx ~= 0 or dy ~= 0) and alpha(frames[fi]:getPixel(x + dx, y + dy)) > 0 then
                nOpaque = nOpaque + 1
              end
            end
          end
          if nOpaque <= 1 then
            frames[fi]:drawPixel(x, y, CLEAR)
          end
        end
      end
    end
  end
  
  -- Clean edge outline for left arm
  for fi = 1, 8 do
    for y = 78, 145 do
      for x = 88, 115 do
        if alpha(frames[fi]:getPixel(x, y)) > 0 then
          local isEdge = false
          for dy = -1, 1 do
            for dx = -1, 1 do
              if (dx ~= 0 or dy ~= 0) and alpha(frames[fi]:getPixel(x + dx, y + dy)) == 0 then
                isEdge = true
                break
              end
            end
            if isEdge then break end
          end
          if isEdge then
            local p = frames[fi]:getPixel(x, y)
            local r = app.pixelColor.rgbaR(p)
            local g = app.pixelColor.rgbaG(p)
            local b = app.pixelColor.rgbaB(p)
            local lum = math.floor(0.299 * r + 0.587 * g + 0.114 * b)
            if lum >= 150 then
              frames[fi]:drawPixel(x, y, ARMOR_SHADOW)
            end
          end
        end
      end
    end
  end
  
  -- Save frames and masters
  local natFrames = {}
  for fi = 1, 8 do
    frames[fi]:saveAs(app.fs.joinPath(candDir, string.format("%02d.png", fi - 1)))
    local nat = blank(128, 128)
    nat:drawImage(frames[fi], Point(-64, -64))
    natFrames[fi] = nat
  end
  
  local strip = blank(128 * 8, 128)
  for fi = 1, 8 do
    strip:drawImage(natFrames[fi], Point((fi - 1) * 128, 0))
  end
  strip:saveAs(app.fs.joinPath(candDir, "native-strip.png"))
  
  saveSprite(compMaster, 256, 256, "Unarmed body", frames)
  saveSprite(natMaster, 128, 128, "Walk_" .. d, natFrames)
  print("Successfully stabilized left arm in " .. d .. " Walk.")
end

print("Walk left arm stabilization complete.")
