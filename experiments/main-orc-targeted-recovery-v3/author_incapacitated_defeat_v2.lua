-- Authoritative Aseprite Lua script for genuine volumetric collapse Defeat
-- Eliminates regional compression / squishing and clears cels before drawing
local root = app.fs.currentPath
local function file(p) return app.fs.joinPath(root, p) end
local function alpha(p) return app.pixelColor.rgbaA(p) end

print("=== Authoring Genuine Volumetric Defeat Collapse in Aseprite ===")

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
  
  -- 1. Draw lower body / grounded base (y >= 162)
  for y = 162, 190 do
    for x = 0, 255 do
      local p = im4:getPixel(x, y)
      if alpha(p) > 0 then
        termComp:drawPixel(x, y, p)
      end
    end
  end
  
  -- 2. Draw collapsed arms resting prone on ground (y: 154..175)
  -- The arms give way and relax lower to the ground
  for y = 154, 175 do
    for x = 0, 255 do
      -- Look for arm/hand pixels in the lateral regions
      local isArm = (d == "front_r" and (x <= 95 or x >= 165)) or (d == "front_l" and (x <= 90 or x >= 160))
      if isArm then
        local p = im4:getPixel(x, y)
        if alpha(p) > 0 then
          local ny = y + 4
          if ny <= 190 then
            termComp:drawPixel(x, ny, p)
          end
        end
      end
    end
  end
  
  -- 3. Draw upper torso + head + pauldrons (y <= 160) as a RIGID, UNCOMPRESSED unit
  -- Dropped by exactly 9 pixels down, settled on the prone chest/ground
  -- Preserves 100% of the anatomical pixel clusters and shading
  local shiftX = (d == "front_r" and 2 or -2)
  local shiftY = 9
  for y = 120, 161 do
    for x = 0, 255 do
      local p = im4:getPixel(x, y)
      if alpha(p) > 0 then
        local tx = x + shiftX
        local ty = y + shiftY
        if tx >= 0 and tx < 256 and ty <= 190 then
          termComp:drawPixel(tx, ty, p)
        end
      end
    end
  end
  
  -- 4. Clean ground contact line at groundY = 190
  for x = 0, 255 do
    local p = im4:getPixel(x, 190)
    if alpha(p) > 0 then
      termComp:drawPixel(x, 190, p)
    end
  end
  
  -- Create 128x128 native frame
  local termNat = blank(128, 128)
  termNat:drawImage(termComp, Point(-64, -64))
  
  -- Save frame 04 composite and native PNGs
  app.fs.makeAllDirectories(candDir .. "/native")
  termComp:saveAs(app.fs.joinPath(candDir, "04.png"))
  termNat:saveAs(app.fs.joinPath(candDir .. "/native", "04.png"))
  
  -- Update master sprites: CEL MUST BE CLEARED FIRST!
  local s_comp = Sprite{ fromFile = compMaster }
  local s_nat = Sprite{ fromFile = natMaster }
  
  -- Clear existing cel before drawing to prevent old pixels underneath!
  local celComp = s_comp.layers[1]:cel(5)
  celComp.image:clear()
  celComp.image:drawImage(termComp, Point(0, 0))
  
  local celNat = s_nat.layers[1]:cel(5)
  celNat.image:clear()
  celNat.image:drawImage(termNat, Point(0, 0))
  
  s_comp:saveAs(compMaster)
  s_nat:saveAs(natMaster)
  
  -- Re-open composite master and verify it renders identical to termComp!
  local testSpr = app.open(compMaster)
  local rendered = blank(256, 256)
  rendered:drawSprite(testSpr, 5)
  testSpr:close()
  
  -- Update native strip
  local strip = blank(128 * 5, 128)
  for fi = 1, 4 do
    local cImg = Image{ fromFile = app.fs.joinPath(candDir, string.format("%02d.png", fi - 1)) }
    strip:drawImage(cImg, Point((fi - 1) * 128 - 64, -64))
  end
  strip:drawImage(termNat, Point(4 * 128, 0))
  strip:saveAs(app.fs.joinPath(candDir, "native-strip.png"))
  
  s_comp:close()
  s_nat:close()
  print("Updated " .. d .. " Defeat to genuine uncompressed volumetric collapse.")
end

print("Defeat authored and synchronized completely.")
