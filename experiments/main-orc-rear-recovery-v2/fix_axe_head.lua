-- Fix floating head patch on axe chop keys in Aseprite
local root = app.fs.currentPath
local function file(p) return app.fs.joinPath(root, p) end

for _, name in ipairs({ "clean_axe_chop_r", "clean_axe_chop_l" }) do
  local p = file(string.format("experiments/main-orc-rear-recovery-v2/raw/%s.png", name))
  local im = Image{ fromFile = p }
  
  -- Clear floating patch above the tucked head: y in [0..17], x in [45..75]
  for y = 0, 17 do
    for x = 45, 75 do
      im:drawPixel(x, y, app.pixelColor.rgba(0, 0, 0, 0))
    end
  end
  
  im:saveAs(p)
  print("Fixed: " .. p)
end
