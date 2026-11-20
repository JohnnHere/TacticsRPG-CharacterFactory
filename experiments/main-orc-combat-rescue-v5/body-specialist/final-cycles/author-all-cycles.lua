-- author-all-cycles.lua
-- Assembles native128.aseprite, body256.aseprite, native/00..11.png, body256/00..11.png, and strips

local cycles = {
  {
    name = "back_r-Sword-full",
    files = {
      "experiments/main-orc-combat-rescue-v5/body-specialist/canonical-input.png",
      "experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/back_r-Sword-full/entry-1.png",
      "experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/back_r-Sword-full/entry-2.png",
      "experiments/main-orc-combat-rescue-v5/body-specialist/back_r-Sword-keys/01-native.png",
      "experiments/main-orc-combat-rescue-v5/body-specialist/back_r-Sword-keys/02-native.png",
      "experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/back_r-Sword-full/descent-1.png",
      "experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/back_r-Sword-full/descent-2.png",
      "experiments/main-orc-combat-rescue-v5/body-specialist/back_r-Sword-keys/03-native.png",
      "experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/back_r-Sword-full/recovery-1.png",
      "experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/back_r-Sword-full/recovery-2.png",
      "experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/back_r-Sword-full/recovery-3.png",
      "experiments/main-orc-combat-rescue-v5/body-specialist/canonical-input.png"
    },
    times = {0.04, 0.06, 0.06, 0.07, 0.07, 0.04, 0.04, 0.09, 0.07, 0.07, 0.06, 0.06}
  },
  {
    name = "back_l-Sword-full",
    files = {
      "characters/orc-v1/sprites/Directions/orc_v1_dir_back_l.png",
      "experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/back_l-Sword-full/entry-1.png",
      "experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/back_l-Sword-full/entry-2.png",
      "experiments/main-orc-combat-rescue-v5/body-specialist/back_l-Sword-keys/01-native.png",
      "experiments/main-orc-combat-rescue-v5/body-specialist/back_l-Sword-keys/02-native.png",
      "experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/back_l-Sword-full/descent-1.png",
      "experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/back_l-Sword-full/descent-2.png",
      "experiments/main-orc-combat-rescue-v5/body-specialist/back_l-Sword-keys/03-native.png",
      "experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/back_l-Sword-full/recovery-1.png",
      "experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/back_l-Sword-full/recovery-2.png",
      "experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/back_l-Sword-full/recovery-3.png",
      "characters/orc-v1/sprites/Directions/orc_v1_dir_back_l.png"
    },
    times = {0.04, 0.06, 0.06, 0.07, 0.07, 0.04, 0.04, 0.09, 0.07, 0.07, 0.06, 0.06}
  },
  {
    name = "back_l-Axe-full",
    files = {
      "characters/orc-v1/sprites/Directions/orc_v1_dir_back_l.png",
      "experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/back_l-Axe-full/entry-1.png",
      "experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/back_l-Axe-full/entry-2.png",
      "experiments/main-orc-combat-rescue-v5/body-specialist/back_l-Axe-keys/01-native.png",
      "experiments/main-orc-combat-rescue-v5/body-specialist/back_l-Axe-keys/02-native.png",
      "experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/back_l-Axe-full/descent-2.png",
      "experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/back_l-Axe-full/descent-3.png",
      "experiments/main-orc-combat-rescue-v5/body-specialist/back_l-Axe-keys/03-native.png",
      "experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/back_l-Axe-full/recovery-1.png",
      "experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/back_l-Axe-full/recovery-2.png",
      "experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/back_l-Axe-full/recovery-3.png",
      "characters/orc-v1/sprites/Directions/orc_v1_dir_back_l.png"
    },
    times = {0.07, 0.08, 0.09, 0.10, 0.11, 0.05, 0.06, 0.11, 0.10, 0.10, 0.10, 0.13}
  }
}

local out_roots = {
  "characters/orc-v1/source/combat-rescue-v5/body-specialist/final-cycles/",
  "experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/"
}

for _, c in ipairs(cycles) do
  print("Authoring cycle: " .. c.name)
  local files = c.files
  local times = c.times
  
  local n = Sprite(128, 128, ColorMode.RGB)
  n.layers[1].name = 'body'
  local b = Sprite(256, 256, ColorMode.RGB)
  b.layers[1].name = 'body'
  
  local ns = Image(128 * #files, 128, ColorMode.RGB)
  local bs = Image(256 * #files, 256, ColorMode.RGB)
  
  local native_images = {}
  local body256_images = {}
  
  for i, path in ipairs(files) do
    if i > 1 then
      n:newFrame()
      b:newFrame()
    end
    local img = Image{fromFile = path}
    n.frames[i].duration = times[i]
    b.frames[i].duration = times[i]
    
    n:newCel(n.layers[1], i, img, Point(0, 0))
    b:newCel(b.layers[1], i, img, Point(64, 64))
    
    local full = Image(256, 256, ColorMode.RGB)
    full:drawImage(img, Point(64, 64))
    
    ns:drawImage(img, Point((i - 1) * 128, 0))
    bs:drawImage(full, Point((i - 1) * 256, 0))
    
    native_images[i] = img
    body256_images[i] = full
  end
  
  for _, root in ipairs(out_roots) do
    local out = root .. c.name .. "/"
    n:saveAs(out .. "native128.aseprite")
    b:saveAs(out .. "body256.aseprite")
    ns:saveAs(out .. "native-strip.png")
    bs:saveAs(out .. "body256-strip.png")
    
    for i = 1, #files do
      local fn = string.format("%02d.png", i - 1)
      native_images[i]:saveAs(out .. "native/" .. fn)
      body256_images[i]:saveAs(out .. "body256/" .. fn)
    end
  end
  
  n:close()
  b:close()
end

print("All cycles authored successfully!")
