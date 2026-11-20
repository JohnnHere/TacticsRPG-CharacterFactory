-- Specialist attempt: back_r/Axe IMPACT keypose (replaces slot F05 only), authored inside Aseprite Lua.
-- Strategy ("foreshortened forward chop"): at impact the arm no longer sweeps in the screen plane like a rod.
-- It drops forward/down, shortened and thick, with the right shoulder and head sinking (torso participation).
-- Anatomy is built from SAME-GENERATION, SAME-VIEW, SAME-INDIVIDUAL pieces of the current axe body (F00 rest arm:
-- mail sleeve + spiked vambrace + closed fist). No global rotation, no weapon in body, no external raster art.
-- Params may be overridden by the env-provided table P below (edited between iterations).
local ROOT = app.fs.currentPath
local function file(p) return app.fs.joinPath(ROOT, p) end
local OUT_EXP = 'experiments/main-orc-rear-reconstruction-v4/specialist'
local OUT_SRC = 'characters/orc-v1/source/rear-reconstruction-v4-specialist'
-- Recovery continuation: allow a frozen output-only parameter copy so the
-- prepared iter01/iter02 artifacts are never overwritten by the bounded run.
local P = dofile(file(app.params.params or (OUT_EXP .. '/params.lua')))

local function blank(w, h) local i = Image(w, h, ColorMode.RGB); i:clear(); return i end
local function inPoly(x, y, p)
  local yes = false; local j = #p
  for i = 1, #p do
    local a, b = p[i], p[j]
    if (a[2] > y) ~= (b[2] > y) and x < (b[1] - a[1]) * (y - a[2]) / (b[2] - a[2]) + a[1] then yes = not yes end
    j = i
  end
  return yes
end
local function maskPoly(src, poly)
  local o = blank(src.width, src.height)
  for y = 0, src.height - 1 do for x = 0, src.width - 1 do
    if inPoly(x + .5, y + .5, poly) then o:drawPixel(x, y, src:getPixel(x, y)) end
  end end
  return o
end
local function erasePoly(im, poly)
  for y = 0, im.height - 1 do for x = 0, im.width - 1 do
    if inPoly(x + .5, y + .5, poly) then im:drawPixel(x, y, 0) end
  end end
end
local function alphaOf(c) return app.pixelColor.rgbaA(c) end
-- Row-wise articulation: shift each row of 'im' horizontally by round((y-y0)*k) (+dx,+dy global). Keeps per-row texture.
local function shearRows(im, y0, k, dx, dy)
  local o = blank(im.width, im.height)
  for y = 0, im.height - 1 do
    local sh = math.floor((y - y0) * k + 0.5) + dx
    for x = 0, im.width - 1 do
      local c = im:getPixel(x, y)
      if alphaOf(c) > 0 then
        local nx, ny = x + sh, y + dy
        if nx >= 0 and nx < im.width and ny >= 0 and ny < im.height then o:drawPixel(nx, ny, c) end
      end
    end
  end
  return o
end
local function shift(im, dx, dy)
  local o = blank(im.width, im.height); o:drawImage(im, Point(dx, dy)); return o
end

local function frameImage(path, frameNo)
  local s = app.open(file(path)); local im = blank(128, 128); im:drawSprite(s, frameNo); s:close(); return im
end
local N = 'characters/orc-v1/source/aseprite/rear-recovery-v2/native/axe-body-representative-v1-back_r.aseprite'
local F05 = frameImage(N, 6)   -- impact slot of the current candidate
local F00 = frameImage(N, 1)   -- rest pose: intact right arm donor

-- 1) torso base: F05 with the thin rod arm and its orphan sleeve fragments removed
local base = Image(F05)
erasePoly(base, P.eraseArm)

-- 2) head/nape sink (torso participation): head blob drops, collar overlaps naturally
local head = maskPoly(F05, P.headPoly)
if P.headDrop ~= 0 then
  erasePoly(base, P.headPoly)
  -- restore collar/spike pixels that sat under the head's old position
  local under = maskPoly(F00, P.headUnderPoly or {})
end
local headMoved = shift(head, P.headDx or 0, P.headDrop)

-- 3) right pauldron + strap mass (from F05 itself) sinks forward
local paul = maskPoly(F05, P.pauldronPoly)
if P.pauldronDrop ~= 0 then erasePoly(base, P.pauldronPoly) end
local paulMoved = shift(paul, P.pauldronDx or 0, P.pauldronDrop)

-- 4) arm: rest-arm donor (sleeve + vambrace + fist), articulated by row shear, planted under pauldron
local armD = maskPoly(P.armFrom == 'F00' and F00 or F05, P.armPoly)
local arm = shearRows(armD, P.armY0, P.armK, P.armDx, P.armDy)

-- 5) individually traced seams: elbow crease, forearm cuff ink, finger curl
local seams = blank(128, 128)
local function px(list, rgba) for _, p in ipairs(list) do seams:drawPixel(p[1], p[2], rgba) end end
local ink = app.pixelColor.rgba(12, 15, 18, 255)
px(P.inkPixels or {}, ink)

local layers = {
  {'torso-base-no-arm', base},
  {'right-arm-rest-donor-sheared', arm},
  {'right-pauldron-sunk', paulMoved},
  {'head-sunk', headMoved},
  {'traced-seams', seams},
}
local body = blank(128, 128)
for _, l in ipairs(layers) do body:drawImage(l[2]) end

-- 6) weapon overlay (independent asset, transform only) + handFront (fist pixels re-drawn over handle)
local item = Image { fromFile = file('assets/weapons/militia-axe/sprites/rescue-v3/militia-axe.png') }
local weapon = blank(128, 128)
do
  local rad = P.axeDeg * math.pi / 180; local c, s = math.cos(rad), math.sin(rad)
  local tx, ty = P.grip[1], P.grip[2]
  for y = 0, 127 do for x = 0, 127 do
    local dx, dy = x - tx, y - ty
    local u = math.floor(c * dx + s * dy + 36 + .5); local v = math.floor(-s * dx + c * dy + 55 + .5)
    if u >= 0 and u < 96 and v >= 0 and v < 96 then weapon:drawPixel(x, y, item:getPixel(u, v)) end
  end end
end
local handFront = blank(128, 128)
if P.handPoly then
  local fistSrc = maskPoly(body, P.handPoly)
  handFront:drawImage(fistSrc)
end

-- save layered master
local spr = Sprite(128, 128, ColorMode.RGB)
local names = {}
local function addLayer(name, im, first)
  local l = first and spr.layers[1] or spr:newLayer(); l.name = name; spr:newCel(l, 1, im, Point(0, 0))
end
addLayer('weaponBack', P.weaponBehind and weapon or blank(128, 128), true)
for _, l in ipairs(layers) do addLayer(l[1], l[2]) end
addLayer('weaponFront', P.weaponBehind and blank(128, 128) or weapon)
addLayer('handFront', handFront)
app.fs.makeAllDirectories(file(P.outDir))
-- This is a single study of source F05, whose current duration is80ms.
spr.frames[1].duration = .080
spr:saveAs(file(P.outDir .. '/' .. P.name .. '.aseprite'))
spr:close()

local function flat(list)
  local o = blank(128, 128); for _, im in ipairs(list) do o:drawImage(im) end; return o
end
-- Export actual positioned cels after reopening the saved master. The prepared
-- artwork/parameter geometry is unchanged; this completes source/export proof.
local saved = app.open(file(P.outDir .. '/' .. P.name .. '.aseprite'))
local eq = blank(128, 128); eq:drawSprite(saved, 1)
local savedBody = blank(128, 128)
local doc = {canvas={128,128},durationMs=math.floor(saved.frames[1].duration*1000+.5),layers={}}
for _, l in ipairs(saved.layers) do
  local cel=l:cel(1);local im=blank(128,128)
  if cel then im:drawImage(cel.image,cel.position) end
  im:saveAs(file(P.outDir .. '/' .. l.name .. '.png'))
  if l.name~='weaponBack' and l.name~='weaponFront' and l.name~='handFront' then savedBody:drawImage(im) end
  doc.layers[#doc.layers+1]={name=l.name,position=cel and {cel.position.x,cel.position.y} or nil}
end
savedBody:saveAs(file(P.outDir .. '/' .. P.name .. '-body.png'))
eq:saveAs(file(P.outDir .. '/' .. P.name .. '-equipped.png'))
saved:close()
F05:saveAs(file(P.outDir .. '/source-F05.png'))
local docFile=assert(io.open(file(P.outDir .. '/document.json'),'w'));docFile:write(json.encode(doc));docFile:close()
print('ok ' .. P.name)

