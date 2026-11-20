-- author-repair1.lua
-- Assembles repair1 cycles in Aseprite:
-- Replaces defective frames with surgically retouched versions in Lua:
-- 1. back_r-Sword F06: Clears 272 swoosh pixels + trail, reconstructs red-brown tunic & leg anatomy
-- 2. back_l-Axe F02: Removes axe blade and haft, reconstructs clenched gauntlet/fist
-- 3. back_l-Sword F05: Removes 7-10px hook above pauldron

local rgba = app.pixelColor.rgba

local function repair_back_r_sword_f06(img)
  -- 1. Clear floating swoosh pixels in empty sky
  for y = 15, 52 do
    for x = 94, 101 do
      img:drawPixel(x, y, rgba(0, 0, 0, 0))
    end
  end
  for y = 65, 73 do
    for x = 104, 113 do
      local p = img:getPixel(x, y)
      local r = app.pixelColor.rgbaR(p)
      local g = app.pixelColor.rgbaG(p)
      local b = app.pixelColor.rgbaB(p)
      if r > 160 or (r == 148 and g == 151 and b == 156) or (r == 120 and g == 120 and b == 123) then
        img:drawPixel(x, y, rgba(0, 0, 0, 0))
      end
    end
  end

  -- 2. Reconstruct y = 81..111 across the body
  local swoosh_coords = {
    [81] = {90, 90},
    [82] = {89, 91},
    [83] = {88, 91},
    [84] = {86, 90},
    [85] = {85, 88},
    [86] = {83, 86},
    [87] = {81, 85},
    [88] = {80, 83},
    [89] = {79, 82},
    [90] = {77, 80},
    [91] = {76, 79},
    [92] = {74, 77},
    [93] = {72, 76},
    [94] = {71, 74},
    [95] = {69, 72},
    [96] = {67, 71},
    [97] = {65, 69},
    [98] = {63, 67},
    [99] = {61, 65},
    [100] = {59, 63},
    [101] = {57, 62},
    [102] = {55, 60},
    [103] = {53, 58},
    [104] = {50, 56},
    [105] = {48, 54},
    [106] = {46, 52},
    [107] = {44, 49},
    [108] = {41, 47},
    [109] = {39, 45},
    [110] = {39, 41}
  }

  for y, span in pairs(swoosh_coords) do
    local min_x = span[1]
    local max_x = span[2]
    -- Also include the grey trail pixels immediately to the right
    local right_bound = max_x
    for x = max_x + 1, max_x + 4 do
      local p = img:getPixel(x, y)
      local r = app.pixelColor.rgbaR(p)
      local g = app.pixelColor.rgbaG(p)
      local b = app.pixelColor.rgbaB(p)
      if (r == 148 and g == 151 and b == 156) or (r == 180 and g == 192 and b == 201) or (r == 170 and g == 174 and b == 178) or (r == 141 and g == 166 and b == 159) then
        right_bound = x
      end
    end

    if y <= 86 then
      -- Chainmail seam
      for x = min_x, right_bound do
        local col = (x % 2 == 0) and rgba(41, 41, 46, 255) or rgba(28, 28, 34, 255)
        img:drawPixel(x, y, col)
      end
    elseif y <= 97 then
      -- Red-brown leather tunic / groin fold
      for x = min_x, right_bound do
        local col
        if x == min_x then
          col = rgba(33, 17, 23, 255) -- dark fold outline
        elseif x == right_bound then
          col = rgba(48, 23, 28, 255) -- shadow edge
        else
          col = rgba(89, 45, 43, 255) -- authentic red-brown leather
        end
        img:drawPixel(x, y, col)
      end
    elseif y <= 100 then
      -- Inner calf seam & dark outline
      for x = min_x, right_bound do
        if x <= min_x + 1 then
          img:drawPixel(x, y, rgba(9, 9, 12, 255))
        else
          img:drawPixel(x, y, rgba(0, 0, 0, 0))
        end
      end
    else
      -- Left boot outer edge & empty gap between boots
      for x = min_x, right_bound do
        if x <= min_x + 1 then
          local col = (x == min_x) and rgba(24, 25, 30, 255) or rgba(0, 1, 1, 255)
          img:drawPixel(x, y, col)
        else
          img:drawPixel(x, y, rgba(0, 0, 0, 0))
        end
      end
    end
  end
end

local function repair_back_l_axe_f02(img)
  -- 1. Clear axe blade sticking into empty air (y=5..15, x >= 70)
  for y = 5, 15 do
    for x = 70, 114 do
      img:drawPixel(x, y, rgba(0, 0, 0, 0))
    end
  end

  -- 2. Clear lower blade tip (y=16..22, x >= 93)
  for y = 16, 22 do
    for x = 93, 114 do
      img:drawPixel(x, y, rgba(0, 0, 0, 0))
    end
  end

  -- 3. Clear wooden haft protruding to left (y=16..18, x in 73..83)
  for y = 16, 18 do
    for x = 73, 83 do
      img:drawPixel(x, y, rgba(0, 0, 0, 0))
    end
  end

  -- 4. Reconstruct clenched leather glove at x=83..92, y=15..20
  -- Top outline of knuckles (y=15):
  for x = 84, 90 do
    img:drawPixel(x, 15, rgba(2, 2, 3, 255))
  end
  -- Knuckle highlights and body (y=16..18):
  for x = 84, 90 do
    local c16 = (x == 86 or x == 87) and rgba(57, 36, 27, 255) or rgba(38, 27, 27, 255)
    img:drawPixel(x, 16, c16)
    local c17 = (x == 86 or x == 87) and rgba(57, 36, 27, 255) or rgba(38, 27, 27, 255)
    img:drawPixel(x, 17, c17)
    img:drawPixel(x, 18, rgba(38, 27, 27, 255))
  end
  -- Fold / seam (y=19..20):
  for x = 83, 91 do
    local c19 = (x <= 84) and rgba(20, 11, 8, 255) or rgba(38, 27, 27, 255)
    img:drawPixel(x, 19, c19)
  end
  -- Outlines:
  img:drawPixel(91, 16, rgba(2, 2, 3, 255))
  img:drawPixel(91, 17, rgba(2, 2, 3, 255))
  img:drawPixel(91, 18, rgba(2, 2, 3, 255))
  img:drawPixel(92, 19, rgba(2, 2, 3, 255))
  img:drawPixel(92, 20, rgba(2, 2, 3, 255))
  img:drawPixel(83, 16, rgba(2, 2, 3, 255))
  img:drawPixel(83, 17, rgba(2, 2, 3, 255))
  img:drawPixel(83, 18, rgba(2, 2, 3, 255))
end

local function repair_back_l_sword_f05(img)
  -- Clear 7-10px hook above pauldron at y=28..33, x=94..98
  for y = 28, 33 do
    for x = 94, 98 do
      img:drawPixel(x, y, rgba(0, 0, 0, 0))
    end
  end
end

local cycles = {
  {
    name = "back_r-Sword-full",
    source_dir = "experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/back_r-Sword-full/native/",
    times = {0.04, 0.06, 0.06, 0.07, 0.07, 0.04, 0.04, 0.09, 0.07, 0.07, 0.06, 0.06},
    repair_func = function(frame_idx, img)
      if frame_idx == 6 then -- F06
        repair_back_r_sword_f06(img)
      end
    end
  },
  {
    name = "back_l-Sword-full",
    source_dir = "experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/back_l-Sword-full/native/",
    times = {0.04, 0.06, 0.06, 0.07, 0.07, 0.04, 0.04, 0.09, 0.07, 0.07, 0.06, 0.06},
    repair_func = function(frame_idx, img)
      if frame_idx == 5 then -- F05
        repair_back_l_sword_f05(img)
      end
    end
  },
  {
    name = "back_l-Axe-full",
    source_dir = "experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/back_l-Axe-full/native/",
    times = {0.07, 0.08, 0.09, 0.10, 0.11, 0.05, 0.06, 0.11, 0.10, 0.10, 0.10, 0.13},
    repair_func = function(frame_idx, img)
      if frame_idx == 2 then -- F02
        repair_back_l_axe_f02(img)
      end
    end
  }
}

local out_roots = {
  "characters/orc-v1/source/combat-rescue-v5/body-specialist/final-cycles/repair1/",
  "experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/repair1/"
}

for _, c in ipairs(cycles) do
  print("Authoring repair1 cycle: " .. c.name)
  local times = c.times
  
  local n = Sprite(128, 128, ColorMode.RGB)
  n.layers[1].name = 'body'
  local b = Sprite(256, 256, ColorMode.RGB)
  b.layers[1].name = 'body'
  
  local ns = Image(128 * 12, 128, ColorMode.RGB)
  local bs = Image(256 * 12, 256, ColorMode.RGB)
  
  local native_images = {}
  local body256_images = {}
  
  for i = 0, 11 do
    local f_num = i + 1
    if f_num > 1 then
      n:newFrame()
      b:newFrame()
    end
    
    local in_file = c.source_dir .. string.format("%02d.png", i)
    local img = Image{fromFile = in_file}
    
    -- Apply surgical repair if this is a repaired frame
    c.repair_func(i, img)
    
    n.frames[f_num].duration = times[f_num]
    b.frames[f_num].duration = times[f_num]
    
    n:newCel(n.layers[1], f_num, img, Point(0, 0))
    b:newCel(b.layers[1], f_num, img, Point(64, 64))
    
    local full = Image(256, 256, ColorMode.RGB)
    full:drawImage(img, Point(64, 64))
    
    ns:drawImage(img, Point(i * 128, 0))
    bs:drawImage(full, Point(i * 256, 0))
    
    native_images[f_num] = img
    body256_images[f_num] = full
  end
  
  for _, root in ipairs(out_roots) do
    local out = root .. c.name .. "/"
    n:saveAs(out .. "native128.aseprite")
    b:saveAs(out .. "body256.aseprite")
    ns:saveAs(out .. "native-strip.png")
    bs:saveAs(out .. "body256-strip.png")
    
    for i = 1, 12 do
      local fn = string.format("%02d.png", i - 1)
      native_images[i]:saveAs(out .. "native/" .. fn)
      body256_images[i]:saveAs(out .. "body256/" .. fn)
    end
  end
  
  n:close()
  b:close()
end

print("ALL REPAIR1 CYCLES AUTHORED AND EXPORTED SUCCESSFULLY!")
