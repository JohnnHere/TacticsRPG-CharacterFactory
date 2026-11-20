-- Lua script to properly composite axe_chop_l with authentic base cranium
local root = app.fs.currentPath
local function file(p) return app.fs.joinPath(root, p) end

local base_l = Image{ fromFile = file("experiments/main-orc-complete-v1/pixellab-recovery/back_l_base.png") }
local raw_axe = Image{ fromFile = file("experiments/main-orc-rear-recovery-v2/raw/axe_chop_l.png") }

local comp = Image(128, 128, ColorMode.RGB)
comp:clear()
comp:drawImage(base_l, Point(0, 0))

-- Copy raised left arm and pauldron (x in [0..55], y in [14..90])
for y = 14, 90 do
  for x = 0, 55 do
    local p = raw_axe:getPixel(x, y - 1)
    local a = app.pixelColor.rgbaA(p)
    if a > 10 then
      comp:drawPixel(x, y, p)
    end
  end
end

comp:saveAs(file("experiments/main-orc-rear-recovery-v2/test_axe_l_clean.png"))
print("Saved test_axe_l_clean.png")
