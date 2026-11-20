-- Pilot B1 / front_r: programmatic local Aseprite authorship.
-- No generation, no body/hand editing. Reuses the same two sword assets as Experiment 04.
-- Adaptations vs Experiment 04, and nothing else:
--   1. the direction (front_r instead of front_l);
--   2. a grip pivot table, because front_r stores grip=null for every frame.
-- The blade replacement rule is unchanged: original weapon pixels whose inverse-mapped
-- asset coordinate is v <= 54 are repainted from sword-b. A seam measurement proved that
-- no original blade pixel rounds into v >= 55 on this direction (0 colour mismatches in
-- 10 frames), so no extra seam pass is needed.
local E = 'experiments/main-orc-hybrid-weapon-04b'
local CLIP = 'characters/orc-v1/source/combat-recovery-v8/frontal-inbetween/front_r-sword/clip.json'

local function read(p)
  local f = assert(io.open(p, 'r')); local v = json.decode(f:read('*a')); f:close(); return v
end

local clip = read(CLIP)

-- Fitted from the art (rigid-transform centroid + exact integer search).
-- See fit-front-r-grip.py and grip-pivot-fit.json in this folder.
local GRIP = {
  [2] = {103, 130}, [3] = {90, 119}, [4] = {98, 100}, [5] = {98, 89}, [6] = {127, 101},
  [7] = {155, 114}, [8] = {158, 132}, [9] = {159, 148}, [10] = {134, 147}, [11] = {110, 150},
}

local function blank(w, h) local i = Image(w, h, ColorMode.RGB); i:clear(); return i end
local function save(i, p) app.fs.makeAllDirectories(app.fs.filePath(p)); i:saveAs(p) end

local function raster(s, n, f)
  local im = blank(s.width, s.height)
  for _, l in ipairs(s.layers) do
    if l.name == n then
      local c = l:cel(f); if c then im:drawImage(c.image, c.position) end
      return im
    end
  end
  error(n)
end

local function render(s, f) local im = blank(s.width, s.height); im:drawSprite(s, f); return im end

local function sameColour(c1, c2)
  local p = app.pixelColor
  return p.rgbaR(c1) == p.rgbaR(c2) and p.rgbaG(c1) == p.rgbaG(c2)
    and p.rgbaB(c1) == p.rgbaB(c2) and p.rgbaA(c1) == p.rgbaA(c2)
end

local item = Image{fromFile = E .. '/variants/sword-b/sword.png'}

-- Opaque extent of the B blade per row. sword-b's blade is one pixel narrower than the
-- original recruit blade, so painting strictly inside B's silhouette would leave a rim of
-- the old blade alive. Clamping u into this extent lets B's shading follow the ORIGINAL
-- blade silhouette instead, so no original blade pixel survives and the outline is B's.
local bladeMinU, bladeMaxU = {}, {}
for v = 0, 54 do
  local lo, hi = nil, nil
  for u = 0, 95 do
    if app.pixelColor.rgbaA(item:getPixel(u, v)) > 0 then
      if lo == nil then lo = u end
      hi = u
    end
  end
  bladeMinU[v], bladeMaxU[v] = lo, hi
end

local original = app.open(clip.master)
local selected = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13}
local stats = {}

for _, variant in ipairs({'a', 'b'}) do
  local s = Sprite(256, 256)
  local names = {'weaponBack', 'body', 'weaponFront', 'handFront'}
  local layers = {}
  for i, n in ipairs(names) do
    local l = i == 1 and s.layers[1] or s:newLayer(); l.name = n; layers[n] = l
  end
  for fi, idx in ipairs(selected) do
    if fi > 1 then s:newEmptyFrame() end
    local pf = clip.frames[idx + 1]
    local ims = {}
    for _, n in ipairs(names) do ims[n] = raster(original, n, idx + 1) end

    if variant == 'b' and pf.weaponVisible then
      local grip = GRIP[idx]
      assert(grip, 'sem pivo para o quadro ' .. idx)
      local a = math.rad(pf.rotationDeg)
      local ca, sa = math.cos(a), math.sin(a)
      local inBlade, changed, skipped = 0, 0, 0
      for y = 0, 255 do
        for x = 0, 255 do
          local dx, dy = x - grip[1], y - grip[2]
          local u = math.floor(48 + dx * ca + dy * sa + .5)
          local v = math.floor(66 - dx * sa + dy * ca + .5)
          if u >= 0 and u < 96 and v >= 0 and v <= 54 then
            local wasWeapon = app.pixelColor.rgbaA(ims.weaponBack:getPixel(x, y)) > 0
              or app.pixelColor.rgbaA(ims.weaponFront:getPixel(x, y)) > 0
            if wasWeapon then
              local lo, hi = bladeMinU[v], bladeMaxU[v]
              if lo ~= nil then
                local uc = u
                if uc < lo then uc = lo elseif uc > hi then uc = hi end
                local c = item:getPixel(uc, v)
                inBlade = inBlade + 1
                if not sameColour(ims.weaponFront:getPixel(x, y), c) then changed = changed + 1 end
                ims.weaponBack:drawPixel(x, y, 0)
                ims.weaponFront:drawPixel(x, y, c)
              else
                skipped = skipped + 1
              end
            end
          end
        end
      end
      stats[#stats + 1] = {frame = idx, grip = grip, rot = pf.rotationDeg,
                           bladePixels = inBlade, colourChanged = changed, skipped = skipped}
    end

    for _, n in ipairs(names) do s:newCel(layers[n], fi, ims[n], Point(0, 0)) end
    s.frames[fi].duration = pf.durationMs / 1000
  end

  local out = E .. '/full/' .. variant
  app.fs.makeAllDirectories(out)
  s:saveAs(out .. '/composite.aseprite'); s:close()

  s = app.open(out .. '/composite.aseprite')
  local sheet = blank(256 * #selected, 256)
  for fi, idx in ipairs(selected) do
    local fn = string.format('F%02d.png', idx)
    local wb = raster(s, 'weaponBack', fi); wb:drawImage(raster(s, 'weaponFront', fi))
    save(wb, out .. '/weapon-only/' .. fn)
    save(raster(s, 'body', fi), out .. '/body-only/' .. fn)
    for _, n in ipairs(names) do save(raster(s, n, fi), out .. '/layers/' .. n .. '/' .. fn) end
    local c = render(s, fi); save(c, out .. '/composite/' .. fn); sheet:drawImage(c, Point((fi - 1) * 256, 0))
  end
  save(sheet, out .. '/strip.png')
  local durs = {}
  for i = 1, #s.frames do durs[i] = math.floor(s.frames[i].duration * 1000 + .5) end
  local df = assert(io.open(out .. '/frame-durations.json', 'w'))
  df:write(json.encode(durs)); df:close()
  s:close()
end

original:close()

local f = assert(io.open(E .. '/blade-repaint-stats.json', 'w'))
f:write(json.encode(stats)); f:close()
print('Pilot B1 front_r: A/B saved and reopened; bodies and hands untouched.')
