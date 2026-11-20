-- V7 ECON DEV — T2 surgical axilla repair for front_l/Sword (body layer only).
-- Reads the edit plan and applies it to the composite master's `body` layer, to the
-- standalone body master and to the native master (offset 64,64), then re-exports every
-- frame PNG and proves three things before finishing:
--   1. frame durations still match clip.durationsMs
--   2. composite.body cel == body master (canvas-space, cel.position honoured)
--   3. native == body crop at (64,64)
-- Reads nothing from stdin. All paths are relative to the repository root (cwd in batch).
local E = 'experiments/main-orc-combat-recovery-v7/frontal'
local C = 'characters/orc-v1/source/combat-recovery-v7/frontal/front_l-Sword-full'

local function read(p)
  local f = assert(io.open(p), 'cannot open ' .. p)
  local t = json.decode(f:read('*a'))
  f:close()
  return t
end
local function save(im, p)
  app.fs.makeAllDirectories(app.fs.filePath(p))
  im:saveAs(p)
end
local function layer(s, n)
  for _, l in ipairs(s.layers) do if l.name == n then return l end end
  error('missing layer ' .. n)
end

local plan = read(E .. '/edit-plan-v7.json')
local clip = read(C .. '/clip.json')

-- 1. apply the plan to the three masters -------------------------------------
local applied = 0
for _, kind in ipairs({ 'composite', 'body', 'native' }) do
  local s = app.open(C .. '/source/' .. kind .. '.aseprite')
  assert(s, 'cannot open ' .. kind)
  local l = kind == 'composite' and layer(s, 'body') or s.layers[1]
  for fs, edits in pairs(plan) do
    local cel = l:cel(tonumber(fs) + 1)
    assert(cel, 'no cel for frame ' .. fs .. ' on ' .. kind)
    local im = Image(cel.image)
    for _, v in ipairs(edits) do
      local ox = kind == 'native' and 64 or 0
      local x = v.x - ox - cel.position.x
      local y = v.y - ox - cel.position.y
      assert(x >= 0 and y >= 0 and x < im.width and y < im.height,
        string.format('out of cel bounds %d,%d on %s/%s', v.x, v.y, kind, fs))
      im:drawPixel(x, y, app.pixelColor.rgba(table.unpack(v.rgba)))
      applied = applied + 1
    end
    cel.image = im
  end
  s:saveAs(C .. '/source/' .. kind .. '.aseprite')
  s:close()
end

-- 2. reopen, verify, export ---------------------------------------------------
local comp = app.open(C .. '/source/composite.aseprite')
local body = app.open(C .. '/source/body.aseprite')
local nat = app.open(C .. '/source/native.aseprite')
assert(#comp.layers == 4, 'composite must keep 4 layers')
assert(#comp.frames == 13 and #body.frames == 13 and #nat.frames == 13, 'frame count')
assert(comp.layers[1].name == 'weaponBack' and comp.layers[2].name == 'body'
  and comp.layers[3].name == 'weaponFront' and comp.layers[4].name == 'handFront', 'layer order')

local cs = Image(13 * 256, 256); cs:clear()
local ns = Image(13 * 128, 128); ns:clear()
local function render(s, i)
  local im = Image(s.width, s.height); im:clear(); im:drawSprite(s, i); return im
end

for i = 1, 13 do
  for _, s in ipairs({ comp, body, nat }) do
    assert(math.abs(s.frames[i].duration * 1000 - clip.durationsMs[i]) < 0.01, 'duration drift')
  end
  local c = render(comp, i)
  local b = render(body, i)
  local n = render(nat, i)
  local bc = layer(comp, 'body'):cel(i)
  local bi = Image(256, 256); bi:clear(); bi:drawImage(bc.image, bc.position)
  for y = 0, 255 do
    for x = 0, 255 do assert(b:getPixel(x, y) == bi:getPixel(x, y), 'body master mismatch') end
  end
  for y = 0, 127 do
    for x = 0, 127 do assert(n:getPixel(x, y) == b:getPixel(x + 64, y + 64), 'native crop mismatch') end
  end
  local ix = string.format('%02d', i - 1)
  save(c, C .. '/' .. ix .. '.png')
  save(c, C .. '/frames/' .. ix .. '.png')
  save(b, C .. '/layers/body/' .. ix .. '.png')
  save(n, C .. '/native/' .. ix .. '.png')
  cs:drawImage(c, Point((i - 1) * 256, 0))
  ns:drawImage(n, Point((i - 1) * 128, 0))
  for _, name in ipairs({ 'weaponBack', 'weaponFront', 'handFront' }) do
    local cel = layer(comp, name):cel(i)
    local im = Image(256, 256); im:clear()
    if cel then im:drawImage(cel.image, cel.position) end
    save(im, E .. '/reopened-layers/' .. name .. '/' .. ix .. '.png')
  end
end
save(cs, C .. '/composite-strip.png')
save(ns, C .. '/native-strip.png')

local f = assert(io.open(E .. '/reopen-result-v7.json', 'w'))
f:write(json.encode({
  frames = 13,
  mastersReopened = 3,
  layerOrderPreserved = true,
  durationsVerified = true,
  bodyMasterMatchesComposite = true,
  nativeIsBodyCrop = true,
  editsApplied = applied,
}))
f:close()
comp:close(); body:close(); nat:close()
print('APPLIED ' .. applied .. ' EDITS')
