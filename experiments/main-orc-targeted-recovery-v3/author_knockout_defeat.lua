-- Author genuine knockout terminal Defeat pose for front_r and front_l
-- Eliminates "kneeling on all fours with head raised" posture
-- Head low to the ground, torso prone, arms limp/loose, volume fully preserved
local root = app.fs.currentPath
local function file(p) return app.fs.joinPath(root, p) end
local function alpha(p) return app.pixelColor.rgbaA(p) end

print("=== Authoring Genuine Knockout Defeat Terminal in Aseprite ===")

local function blank(w, h)
  local im = Image(w, h, ColorMode.RGB)
  im:clear()
  return im
end

for _, d in ipairs({ "front_r", "front_l" }) do
  local candDir = file(string.format("characters/orc-v1/source/rear-recovery-v2/%s/Defeat", d))
  local natMaster = file(string.format("characters/orc-v1/source/aseprite/rear-recovery-v2/native/defeat-%s.aseprite", d))
  local compMaster = file(string.format("characters/orc-v1/source/aseprite/rear-recovery-v2/composite/%s/defeat.aseprite", d))
  
  -- Load baseline F04
  local baseF04Path = file(string.format("characters/orc-v1/source/complete-v1/%s/Defeat/04.png", d))
  local im4 = Image{ fromFile = baseF04Path }
  local termComp = blank(256, 256)
  
  -- 1. Draw grounded legs / pelvis (y >= 162)
  for y = 162, 190 do
    for x = 0, 255 do
      local p = im4:getPixel(x, y)
      if alpha(p) > 0 then
        local isLeg = (d == "front_r" and x <= 135) or (d == "front_l" and x >= 120)
        if isLeg then
          termComp:drawPixel(x, y, p)
        end
      end
    end
  end
  
  -- 2. Torso & Upper back: slump down by 14px
  local shiftX = (d == "front_r" and 2 or -2)
  for y = 120, 161 do
    for x = 0, 255 do
      local p = im4:getPixel(x, y)
      if alpha(p) > 0 then
        local isHead = (d == "front_r" and x >= 140 and y >= 148) or (d == "front_l" and x <= 115 and y >= 148)
        local isOuterArm = (d == "front_r" and x >= 165) or (d == "front_l" and x <= 90)
        if not isHead and not isOuterArm then
          local tx = x + shiftX
          local ty = y + 14
          if ty <= 190 and tx >= 0 and tx < 256 then
            termComp:drawPixel(tx, ty, p)
          end
        end
      end
    end
  end
  
  -- 3. Head: drops down by 13px into floor void, resting low (cabeça baixa)
  for y = 148, 178 do
    for x = 0, 255 do
      local p = im4:getPixel(x, y)
      if alpha(p) > 0 then
        local isHead = (d == "front_r" and x >= 138 and x <= 168) or (d == "front_l" and x >= 87 and x <= 117)
        if isHead then
          local tx = x + shiftX
          local ty = y + 13
          if ty <= 190 and tx >= 0 and tx < 256 then
            termComp:drawPixel(tx, ty, p)
          end
        end
      end
    end
  end
  
  -- 4. Front supporting arm: collapses limp onto the ground (braços soltos)
  for y = 150, 190 do
    for x = 0, 255 do
      local p = im4:getPixel(x, y)
      if alpha(p) > 0 then
        local isOuterArm = (d == "front_r" and x >= 165) or (d == "front_l" and x <= 90)
        if isOuterArm then
          local tx = x + (d == "front_r" and 3 or -3)
          local ty = y + 8
          if ty <= 190 and tx >= 0 and tx < 256 then
            termComp:drawPixel(tx, ty, p)
          end
        end
      end
    end
  end
  
  -- 5. Ground line anchor at groundY = 190
  for x = 0, 255 do
    local p = im4:getPixel(x, 190)
    if alpha(p) > 0 then
      termComp:drawPixel(x, 190, p)
    end
  end
  
  -- Create native 128x128 frame
  local termNat = blank(128, 128)
  termNat:drawImage(termComp, Point(-64, -64))
  
  -- Save PNGs
  app.fs.makeAllDirectories(candDir .. "/native")
  termComp:saveAs(app.fs.joinPath(candDir, "04.png"))
  termNat:saveAs(app.fs.joinPath(candDir .. "/native", "04.png"))
  
  -- Rebuild native-strip.png from all 5 native frames
  local strip = blank(128 * 5, 128)
  for fi = 0, 4 do
    local fnPath = app.fs.joinPath(candDir .. "/native", string.format("%02d.png", fi))
    local fImg = Image{ fromFile = fnPath }
    strip:drawImage(fImg, Point(fi * 128, 0))
  end
  strip:saveAs(app.fs.joinPath(candDir, "native-strip.png"))
  
  -- Update master sprites: CLEARS CELS FIRST
  local s_comp = Sprite{ fromFile = compMaster }
  local celComp = s_comp.layers[1]:cel(5)
  celComp.image:clear()
  celComp.image:drawImage(termComp, Point(0, 0))
  s_comp:saveAs(compMaster)
  s_comp:close()
  
  local s_nat = Sprite{ fromFile = natMaster }
  local celNat = s_nat.layers[1]:cel(5)
  celNat.image:clear()
  celNat.image:drawImage(termNat, Point(0, 0))
  s_nat:saveAs(natMaster)
  s_nat:close()
  
  print("Updated " .. d .. " Defeat terminal F04 knockout in composite, native, strip, and masters.")
end
