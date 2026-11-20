-- Lua script to clean up newly generated weapon key poses in Aseprite
local root = app.fs.currentPath
local function file(p) return app.fs.joinPath(root, p) end

print("=== Cleaning Weapon Key Poses ===")

local base_r = Image{ fromFile = file("experiments/main-orc-complete-v1/pixellab-recovery/back_r_base.png") }
local base_l = Image{ fromFile = file("experiments/main-orc-complete-v1/pixellab-recovery/back_l_base.png") }

local keys = {
  { name = "sword_slash_r", base = base_r, dx = 0, dy = 1, cx1 = 55, cx2 = 76 },
  { name = "axe_chop_r", base = base_r, dx = 0, dy = 1, cx1 = 55, cx2 = 76 },
  { name = "sword_slash_l", base = base_l, dx = 0, dy = 1, cx1 = 50, cx2 = 72 },
  { name = "axe_chop_l", base = base_l, dx = 0, dy = 1, cx1 = 50, cx2 = 72 }
}

for _, k in ipairs(keys) do
  local rawPath = file(string.format("experiments/main-orc-rear-recovery-v2/raw/%s.png", k.name))
  local src = Image{ fromFile = rawPath }
  
  local clean = Image(128, 128, ColorMode.RGB)
  clean:clear()
  clean:drawImage(src, Point(k.dx, k.dy))
  
  -- Clear stray artifacts above cranium (y < 6)
  for y = 0, 5 do
    for x = 0, 127 do
      clean:drawPixel(x, y, app.pixelColor.rgba(0, 0, 0, 0))
    end
  end
  
  -- Restore cranium outline and skin from base
  for y = 6, 20 do
    for x = k.cx1, k.cx2 do
      local pb = k.base:getPixel(x, y)
      local a = app.pixelColor.rgbaA(pb)
      if a > 10 then
        clean:drawPixel(x, y + k.dy, pb)
      end
    end
  end
  
  local outPath = file(string.format("experiments/main-orc-rear-recovery-v2/raw/clean_%s.png", k.name))
  clean:saveAs(outPath)
  print("Saved clean key: " .. outPath)
end

print("=== Clean Weapon Keys Complete ===")
