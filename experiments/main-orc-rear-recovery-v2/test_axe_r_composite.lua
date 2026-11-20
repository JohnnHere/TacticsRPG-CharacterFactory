-- Lua script to properly composite axe_chop_r with authentic base cranium
local root = app.fs.currentPath
local function file(p) return app.fs.joinPath(root, p) end

local base_r = Image{ fromFile = file("experiments/main-orc-complete-v1/pixellab-recovery/back_r_base.png") }
local raw_axe = Image{ fromFile = file("experiments/main-orc-rear-recovery-v2/raw/axe_chop_r.png") }

-- Start with base_r (which has authentic head, cranium, collar, left body and legs)
local comp = Image(128, 128, ColorMode.RGB)
comp:clear()
comp:drawImage(base_r, Point(0, 0))

-- Now copy the raised right arm, shoulder and torso commitment from raw_axe (x >= 75 or y <= 45 on right)
-- dy = +1 for raw_axe to align ground at 126
for y = 14, 90 do
  for x = 72, 127 do
    local p = raw_axe:getPixel(x, y - 1)
    local a = app.pixelColor.rgbaA(p)
    if a > 10 then
      comp:drawPixel(x, y, p)
    end
  end
end

-- Save to test_axe_r_clean.png
comp:saveAs(file("experiments/main-orc-rear-recovery-v2/test_axe_r_clean.png"))
print("Saved test_axe_r_clean.png")
