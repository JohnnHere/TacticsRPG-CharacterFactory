-- Author incapacitated terminal Defeat pose for front_r and front_l
local root = app.fs.currentPath
local function file(p) return app.fs.joinPath(root, p) end

print("=== Authoring Incapacitated Terminal Defeat Pose in Aseprite ===")

local durations = { 0.07, 0.095, 0.115, 0.13, 0.29 }

for _, d in ipairs({ "front_r", "front_l" }) do
  local candDir = file(string.format("characters/orc-v1/source/rear-recovery-v2/%s/Defeat", d))
  local natMaster = file(string.format("characters/orc-v1/source/aseprite/rear-recovery-v2/native/defeat-%s.aseprite", d))
  local compMaster = file(string.format("characters/orc-v1/source/aseprite/rear-recovery-v2/composite/%s/defeat.aseprite", d))
  
  -- Load F03 (collapse-impact) and F04 (kneeling terminal)
  local f03CompPath = app.fs.joinPath(candDir, "03.png")
  local f04CompPath = app.fs.joinPath(candDir, "04.png")
  local im3 = Image{ fromFile = f03CompPath }
  local im4 = Image{ fromFile = f04CompPath }
  
  -- Construct new incapacitated terminal frame:
  -- The head and shoulders drop from y=125 down towards y=138, resting flat/limp on ground
  -- The pauldron, back plate and limbs retain full 3D volume and shading
  local termComp = Image(256, 256, ColorMode.RGB)
  termComp:clear()
  
  -- We take the kneeling pose im4 and settle the upper body down towards the ground
  -- by decomposing the torso/head vs legs/ground contact:
  -- Upper body (y <= 160) settles down by 10-12 pixels so the head rests on the forearm/ground
  -- Lower body (y > 160) remains grounded at groundY = 190
  for y = 0, 255 do
    for x = 0, 255 do
      local p = im4:getPixel(x, y)
      local a = app.pixelColor.rgbaA(p)
      if a > 0 then
        local targetY = y
        local targetX = x
        if y < 165 then
          -- Progressively lower upper torso and head into ground collapse
          local drop = math.floor(11 * (1 - (y - 125) / 40))
          if drop < 0 then drop = 0 end
          targetY = y + drop
          -- Slight forward slump in perspective
          targetX = x + (d == "front_r" and 2 or -2)
        end
        if targetY <= 190 and targetX >= 0 and targetX < 256 then
          termComp:drawPixel(targetX, targetY, p)
        end
      end
    end
  end
  
  -- Blend ground contact line at groundY = 190:
  -- Ensure solid ground contact without floating pixels
  for x = 0, 255 do
    local p = im4:getPixel(x, 190)
    if app.pixelColor.rgbaA(p) > 0 then
      termComp:drawPixel(x, 190, p)
    end
  end
  
  -- Create 128x128 native frame
  local termNat = Image(128, 128, ColorMode.RGB)
  termNat:clear()
  termNat:drawImage(termComp, Point(-64, -64))
  
  -- Save frame 04
  termComp:saveAs(app.fs.joinPath(candDir, "04.png"))
  termNat:saveAs(file(string.format("experiments/main-orc-targeted-recovery-v3/defeat_%s_04_incapacitated.png", d)))
  
  -- Update master sprites
  local s_comp = Sprite{ fromFile = compMaster }
  local s_nat = Sprite{ fromFile = natMaster }
  
  s_comp.layers[1]:cel(5).image:drawImage(termComp, Point(0, 0))
  s_nat.layers[1]:cel(5).image:drawImage(termNat, Point(0, 0))
  
  s_comp:saveAs(compMaster)
  s_nat:saveAs(natMaster)
  
  -- Update native strip
  local strip = Image(128 * 5, 128, ColorMode.RGB)
  strip:clear()
  for fi = 1, 4 do
    local cImg = Image{ fromFile = app.fs.joinPath(candDir, string.format("%02d.png", fi - 1)) }
    strip:drawImage(cImg, Point((fi - 1) * 128 - 64, -64))
  end
  strip:drawImage(termNat, Point(4 * 128, 0))
  strip:saveAs(app.fs.joinPath(candDir, "native-strip.png"))
  
  s_comp:close()
  s_nat:close()
  print("Updated " .. d .. " Defeat terminal pose to incapacitated ground collapse.")
end
