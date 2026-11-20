-- targeted-repair-v1 / representative back_r Sword : export from the forked master.
-- Same layout as the freeze exporter (reexport_representatives_from_saved_masters.lua)
-- so the candidate is directly comparable frame by frame with the published freeze.
local root = app.fs.currentPath
local function f(p) return app.fs.joinPath(root, p) end
local names = {"weaponBack","body","weaponFront","handFront"}
local OUT = "experiments/main-orc-targeted-repair-v1/artist-rear/candidate/clip/back_r/Axe/Attack-representative-v1-microclean"
local COMP = "experiments/main-orc-targeted-repair-v1/artist-rear/candidate/aseprite/axe-attack-representative-v1-microclean.aseprite"
local BODY = "experiments/main-orc-targeted-repair-v1/artist-rear/candidate/aseprite/axe-body-representative-v1-microclean.aseprite"

local function blank(w, h) local im = Image(w, h, ColorMode.RGB); im:clear(); return im end

app.fs.makeAllDirectories(f(OUT .. "/body-only"))
app.fs.makeAllDirectories(f(OUT .. "/native"))
for _, n in ipairs(names) do app.fs.makeAllDirectories(f(OUT .. "/layers/" .. n)) end

local comp = app.open(f(COMP))
local body = app.open(f(BODY))
assert(#comp.frames == 8 and #body.frames == 8, "frame count")

local nativeStrip, bodyStrip = {}, {}
local compositeSheet = Image(256 * 4, 256 * 2, ColorMode.RGB); compositeSheet:clear()
local noWeaponSheet = Image(256 * 4, 256 * 2, ColorMode.RGB); noWeaponSheet:clear()
for i = 1, 8 do
  local flat = blank(256, 256); flat:drawSprite(comp, i)
  flat:saveAs(f(OUT .. "/" .. string.format("%02d.png", i - 1)))
  compositeSheet:drawImage(flat, Point(((i - 1) % 4) * 256, math.floor((i - 1) / 4) * 256))
  local body256 = blank(256, 256); body256:drawSprite(body, i)
  body256:saveAs(f(OUT .. "/body-only/" .. string.format("%02d.png", i - 1)))
  local native = Image(128, 128, ColorMode.RGB); native:clear(); native:drawImage(body256, Point(-64, -64))
  native:saveAs(f(OUT .. "/native/" .. string.format("%02d.png", i - 1)))
  nativeStrip[i] = native
  bodyStrip[i] = native
  noWeaponSheet:drawImage(body256, Point(((i - 1) % 4) * 256, math.floor((i - 1) / 4) * 256))
  for _, layerName in ipairs(names) do
    for _, l in ipairs(comp.layers) do l.isVisible = (l.name == layerName) end
    local layer = blank(256, 256); layer:drawSprite(comp, i)
    layer:saveAs(f(OUT .. "/layers/" .. layerName .. "/" .. string.format("%02d.png", i - 1)))
  end
  for _, l in ipairs(comp.layers) do l.isVisible = true end
end
local ns = Image(128 * 8, 128, ColorMode.RGB); ns:clear()
local bs = Image(128 * 8, 128, ColorMode.RGB); bs:clear()
for i = 1, 8 do
  ns:drawImage(nativeStrip[i], Point((i - 1) * 128, 0))
  bs:drawImage(bodyStrip[i], Point((i - 1) * 128, 0))
end
ns:saveAs(f(OUT .. "/native-strip.png"))
bs:saveAs(f(OUT .. "/body-only-strip.png"))
compositeSheet:saveAs(f(OUT .. "/composite-sheet-qa.png"))
noWeaponSheet:saveAs(f(OUT .. "/weapon-layers-off-qa.png"))
comp:close(); body:close()
print("exported candidate back_r Axe from forked master")

