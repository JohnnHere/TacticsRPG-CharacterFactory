-- Prototype clean knockout Defeat F04
local root = app.fs.currentPath
local function file(p) return app.fs.joinPath(root, p) end
local function alpha(p) return app.pixelColor.rgbaA(p) end

local function blank(w, h)
  local im = Image(w, h, ColorMode.RGB)
  im:clear()
  return im
end

for _, d in ipairs({ "front_r", "front_l" }) do
  local baseF04Path = file(string.format("characters/orc-v1/source/complete-v1/%s/Defeat/04.png", d))
  local im4 = Image{ fromFile = baseF04Path }
  local out = blank(256, 256)
  
  -- 1. Draw grounded legs / pelvis (y >= 165, x in leg region)
  for y = 162, 190 do
    for x = 0, 255 do
      local p = im4:getPixel(x, y)
      if alpha(p) > 0 then
        -- In front_r, legs are mainly on left (x <= 135)
        -- In front_l, legs are mainly on right (x >= 120)
        local isLeg = (d == "front_r" and x <= 135) or (d == "front_l" and x >= 120)
        if isLeg then
          out:drawPixel(x, y, p)
        end
      end
    end
  end
  
  -- 2. Torso & Upper back: slump down by 14px
  -- In front_r: x: 80..145, y <= 160
  -- In front_l: x: 110..175, y <= 160
  local shiftX = (d == "front_r" and 2 or -2)
  for y = 120, 161 do
    for x = 0, 255 do
      local p = im4:getPixel(x, y)
      if alpha(p) > 0 then
        -- Exclude head region and outer arm region
        local isHead = (d == "front_r" and x >= 140 and y >= 148) or (d == "front_l" and x <= 115 and y >= 148)
        local isOuterArm = (d == "front_r" and x >= 165) or (d == "front_l" and x <= 90)
        if not isHead and not isOuterArm then
          local tx = x + shiftX
          local ty = y + 14
          if ty <= 190 and tx >= 0 and tx < 256 then
            out:drawPixel(tx, ty, p)
          end
        end
      end
    end
  end
  
  -- 3. Head: drops down by 16px into the floor void, resting low (cabeça baixa)
  for y = 148, 178 do
    for x = 0, 255 do
      local p = im4:getPixel(x, y)
      if alpha(p) > 0 then
        local isHead = (d == "front_r" and x >= 138 and x <= 168) or (d == "front_l" and x >= 87 and x <= 117)
        if isHead then
          local tx = x + shiftX
          local ty = y + 13
          if ty <= 190 and tx >= 0 and tx < 256 then
            out:drawPixel(tx, ty, p)
          end
        end
      end
    end
  end
  
  -- 4. Front supporting arm: collapses limp onto the ground (braços soltos)
  -- Sits flat on the floor at y: 176..190
  for y = 150, 190 do
    for x = 0, 255 do
      local p = im4:getPixel(x, y)
      if alpha(p) > 0 then
        local isOuterArm = (d == "front_r" and x >= 165) or (d == "front_l" and x <= 90)
        if isOuterArm then
          local tx = x + (d == "front_r" and 3 or -3)
          local ty = y + 8
          if ty <= 190 and tx >= 0 and tx < 256 then
            out:drawPixel(tx, ty, p)
          end
        end
      end
    end
  end
  
  -- 5. Ground line anchor at groundY = 190
  for x = 0, 255 do
    local p = im4:getPixel(x, 190)
    if alpha(p) > 0 then
      out:drawPixel(x, 190, p)
    end
  end
  
  local outNat = blank(128, 128)
  outNat:drawImage(out, Point(-64, -64))
  
  out:saveAs(file(string.format("experiments/main-orc-targeted-recovery-v3/test_defeat_%s_comp.png", d)))
  outNat:saveAs(file(string.format("experiments/main-orc-targeted-recovery-v3/test_defeat_%s_nat.png", d)))
end
print("Done testing defeat knockout prototype.")
