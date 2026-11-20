-- Authoritative Aseprite Lua script for back_l Unarmed repair
-- Completely eliminates in-place sweep bugs and doubled limbs
local root = app.fs.currentPath
local function file(p) return app.fs.joinPath(root, p) end
local function alpha(p) return app.pixelColor.rgbaA(p) end

print("=== Authoring Clean back_l Unarmed ===")

local function blank(w, h)
  local im = Image(w, h, ColorMode.RGB)
  im:clear()
  return im
end

local baseImg = Image{ fromFile = file("experiments/main-orc-complete-v1/pixellab-recovery/back_l_base.png") }
local impactImg = Image{ fromFile = file("experiments/main-orc-rear-recovery-v2/punch_impact_clean_l.png") }

-- F00: Stance / preparation
local f00 = blank(128, 128)
f00:drawImage(baseImg, Point(0, 1))

-- F01: Shoulder coil & anticipation
local f01 = blank(128, 128)
f01:drawImage(baseImg, Point(0, 0))
-- Coiling left arm: pulled back slightly up and right
for y = 14, 55 do
  for x = 15, 55 do
    local p = baseImg:getPixel(x, y)
    if alpha(p) > 0 then
      f01:drawPixel(x, y, app.pixelColor.rgba(0, 0, 0, 0))
    end
  end
end
for y = 14, 55 do
  for x = 15, 55 do
    local p = baseImg:getPixel(x, y)
    if alpha(p) > 0 then
      f01:drawPixel(x + 2, y - 2, p)
    end
  end
end

-- F02: Full punch impact extension
local f02 = blank(128, 128)
f02:drawImage(impactImg, Point(0, 0))

-- F03: Recoil follow-through (SEPARATE BUFFER, NO IN-PLACE OVERWRITE)
local f03 = blank(128, 128)
-- Copy body from impactImg, but exclude the extended fist area (x < 42, y < 55)
for y = 0, 127 do
  for x = 0, 127 do
    if not (x <= 42 and y >= 14 and y <= 55) then
      local p = impactImg:getPixel(x, y)
      if alpha(p) > 0 then f03:drawPixel(x, y, p) end
    end
  end
end

-- Now draw the recoiling arm from impactImg translated by (+8, +2)
for y = 15, 55 do
  for x = 6, 42 do
    local p = impactImg:getPixel(x, y)
    if alpha(p) > 0 then
      local tx = x + 8
      local ty = y + 2
      if tx < 128 and ty < 128 then
        f03:drawPixel(tx, ty, p)
      end
    end
  end
end
-- Bridge shoulder seam at x=40..48, y=20..35
for y = 20, 35 do
  for x = 40, 48 do
    if alpha(f03:getPixel(x, y)) == 0 and alpha(impactImg:getPixel(x, y)) > 0 then
      f03:drawPixel(x, y, impactImg:getPixel(x, y))
    end
  end
end

-- F04: Recovery settle to base stance with intact torso/armor contour and coherent hanging arm
-- Completely eliminates rectangular mask cutout and detached glove fragment
local f04 = blank(128, 128)
f04:drawImage(baseImg, Point(0, 1))

local natFrames = { f00, f01, f02, f03, f04 }
local compFrames = {}
local candDir = file("characters/orc-v1/source/rear-recovery-v2/back_l/Unarmed")
app.fs.makeAllDirectories(candDir)
app.fs.makeAllDirectories(candDir .. "/native")

for fi = 1, 5 do
  local comp = blank(256, 256)
  comp:drawImage(natFrames[fi], Point(64, 64))
  compFrames[fi] = comp
  comp:saveAs(app.fs.joinPath(candDir, string.format("%02d.png", fi - 1)))
  natFrames[fi]:saveAs(app.fs.joinPath(candDir .. "/native", string.format("%02d.png", fi - 1)))
end

-- Save native strip
local strip = blank(128 * 5, 128)
for fi = 1, 5 do
  strip:drawImage(natFrames[fi], Point((fi - 1) * 128, 0))
end
strip:saveAs(app.fs.joinPath(candDir, "native-strip.png"))

-- Save Aseprite masters
local compMaster = "characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_l/unarmed-attack.aseprite"
local natMaster = "characters/orc-v1/source/aseprite/rear-recovery-v2/native/unarmed-back_l.aseprite"

local durationsMs = { 80, 110, 50, 90, 120 }

local function saveSpr(path, w, names, fList)
  app.fs.makeAllDirectories(app.fs.filePath(file(path)))
  local s = Sprite(w, w, ColorMode.RGB)
  s.layers[1].name = names[1]
  for fi = 1, #fList do
    if fi > 1 then s:newEmptyFrame() end
    s:newCel(s.layers[1], fi, fList[fi], Point(0, 0))
    s.frames[fi].duration = durationsMs[fi] / 1000
  end
  s:newTag(1, #fList).name = "Attack"
  s:saveAs(file(path))
  s:close()
end

saveSpr(compMaster, 256, { "body" }, compFrames)
saveSpr(natMaster, 128, { "unarmed_back_l" }, natFrames)

print("Saved clean back_l Unarmed masters, composite, native and strip.")
