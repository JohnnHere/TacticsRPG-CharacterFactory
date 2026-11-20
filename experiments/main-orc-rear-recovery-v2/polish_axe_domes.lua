-- Polish cranium dome on axe chop keys in Aseprite
local root = app.fs.currentPath
local function file(p) return app.fs.joinPath(root, p) end

local darkInk = app.pixelColor.rgba(12, 15, 18, 255)
local skinMid = app.pixelColor.rgba(86, 122, 42, 255)
local skinDark = app.pixelColor.rgba(58, 86, 28, 255)

-- Polish axe_chop_r
local p_r = file("experiments/main-orc-rear-recovery-v2/raw/clean_axe_chop_r.png")
local im_r = Image{ fromFile = p_r }

-- Clear y < 18
for y = 0, 17 do
  for x = 0, 127 do
    im_r:drawPixel(x, y, app.pixelColor.rgba(0, 0, 0, 0))
  end
end

-- Draw nice rounded dome at y=18..20
for x = 50, 60 do im_r:drawPixel(x, 18, darkInk) end
for x = 48, 62 do im_r:drawPixel(x, 19, skinMid) end
im_r:drawPixel(47, 19, darkInk)
im_r:drawPixel(63, 19, darkInk)

im_r:saveAs(p_r)

-- Polish axe_chop_l
local p_l = file("experiments/main-orc-rear-recovery-v2/raw/clean_axe_chop_l.png")
local im_l = Image{ fromFile = p_l }

-- Clear y < 18
for y = 0, 17 do
  for x = 0, 127 do
    im_l:drawPixel(x, y, app.pixelColor.rgba(0, 0, 0, 0))
  end
end

for x = 45, 55 do im_l:drawPixel(x, 18, darkInk) end
for x = 43, 57 do im_l:drawPixel(x, 19, skinMid) end
im_l:drawPixel(42, 19, darkInk)
im_l:drawPixel(58, 19, darkInk)

im_l:saveAs(p_l)

print("Polished axe chop domes.")
