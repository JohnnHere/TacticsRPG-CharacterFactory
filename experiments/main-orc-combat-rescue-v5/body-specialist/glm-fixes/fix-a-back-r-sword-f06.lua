-- fix-a-back-r-sword-f06.lua
-- FIX A (DEFECT-REAR-01-RESIDUAL-A + DEFECT-REAR-01-RESIDUAL-B) — back_r-Sword-full F06
-- 1) alfa 0 nos 5 pixels flutuantes confirmados pelo QA: (112,64),(110,69),(109,70),(108,71),(107,72)
-- 2) região y88..94 / x45..55: pixels da família couro-vinho → malha de aço, usando doadores
--    F05/F07 da MESMA vista nas MESMAS coordenadas (anatomicamente compatíveis); buracos
--    transparentes preenchidos somente quando o doador é opaco; demais pixels intactos.
--    Faixa x40..44 (tasset legítimo presente em F05) preservada; sem filtro global/recolor total.
-- Procedência: corpo herdado de repair1 (geração PixelLab + reparo Aseprite anterior, QA-reviewado);
-- novo reparo cirúrgico por Lua neste script = autoria programática do DEV GLM body-specialist.
-- Frame.duration em SEGUNDOS. Nativo 128 ground 126; composto 256 offset (64,64) ground 190.

local pc = app.pixelColor
local function rgba(r, g, b, a) return pc.rgba(r, g, b, a) end
local function R(p) return pc.rgbaR(p) end
local function G(p) return pc.rgbaG(p) end
local function B(p) return pc.rgbaB(p) end
local function A(p) return pc.rgbaA(p) end
local function hexc(r, g, b) return string.format("%02x%02x%02x", r, g, b) end

local SRC = "characters/orc-v1/source/combat-rescue-v5/body-specialist/final-cycles/repair1/back_r-Sword-full/native/"
local OUT_CHARS = "characters/orc-v1/source/combat-rescue-v5/body-specialist/glm-fixes/back_r-Sword-full/"
local OUT_EXP   = "experiments/main-orc-combat-rescue-v5/body-specialist/glm-fixes/back_r-Sword-full/"

local floats = { {112,64}, {110,69}, {109,70}, {108,71}, {107,72} }
local reds = {}
for _, h in ipairs({"592d2b","482025","34181e","30171c","27181d","271218","211117","1e0e14","240e17"}) do
  reds[h] = true
end

local img06 = Image{ fromFile = SRC .. "06.png" }
local img05 = Image{ fromFile = SRC .. "05.png" }
local img07 = Image{ fromFile = SRC .. "07.png" }
assert(img06 and img05 and img07, "failed to load repair1 frames")

-- 1) floating pixels -> alpha 0
for _, c in ipairs(floats) do
  local x, y = c[1], c[2]
  local p = img06:getPixel(x, y)
  print(string.format("FLOAT (%d,%d) before=%s/%d -> cleared", x, y, hexc(R(p),G(p),B(p)), A(p)))
  img06:drawPixel(x, y, rgba(0, 0, 0, 0))
end

-- 2) mesh rebuild na região QA
local function isRed(r, g, b) return reds[hexc(r, g, b)] or false end
local function donorAt(im, x, y)
  if not im then return nil end
  local p = im:getPixel(x, y)
  if A(p) == 0 then return nil end
  if isRed(R(p), G(p), B(p)) then return nil end
  return { R(p), G(p), B(p) }
end

local replaced, filled, kept = 0, 0, 0
for y = 88, 94 do
  for x = 45, 55 do
    local p = img06:getPixel(x, y)
    if A(p) ~= 0 and isRed(R(p), G(p), B(p)) then
      local d = donorAt(img07, x, y) or donorAt(img05, x, y)
      if d then
        img06:drawPixel(x, y, rgba(d[1], d[2], d[3], 255))
      else
        -- fallback determinista (raro): trama de malha neutra
        local col
        if y % 7 == 0 then col = {0x1c,0x1c,0x22}
        elseif (x + y) % 4 < 2 then col = {0x4c,0x4d,0x51}
        else col = {0x2d,0x2e,0x33} end
        img06:drawPixel(x, y, rgba(col[1], col[2], col[3], 255))
      end
      replaced = replaced + 1
    elseif A(p) == 0 then
      local d = donorAt(img07, x, y) or donorAt(img05, x, y)
      if d then
        img06:drawPixel(x, y, rgba(d[1], d[2], d[3], 255))
        filled = filled + 1
      end
    else
      kept = kept + 1
    end
  end
end
print(string.format("FIX A region: replacedRed=%d filledHoles=%d kept=%d", replaced, filled, kept))

-- dump textual pós-fix (evidência)
print("-- F06 pos-fix (x45..55, y88..94) --")
for y = 88, 94 do
  local row = {}
  for x = 45, 55 do
    local p = img06:getPixel(x, y)
    if A(p) == 0 then row[#row+1] = ".." else row[#row+1] = hexc(R(p),G(p),B(p)) end
  end
  print(y .. ": " .. table.concat(row, " "))
end

-- montagem do ciclo completo (11 frames byte-herdados + F06 corrigido)
local times = {0.04,0.06,0.06,0.07,0.07,0.04,0.04,0.09,0.07,0.07,0.06,0.06}
local n = Sprite(128, 128, ColorMode.RGB); n.layers[1].name = "body"
local b = Sprite(256, 256, ColorMode.RGB); b.layers[1].name = "body"
local ns = Image(128 * 12, 128, ColorMode.RGB)
local bs = Image(256 * 12, 256, ColorMode.RGB)
local nat, comp = {}, {}
for i = 0, 11 do
  local fn = i + 1
  if fn > 1 then n:newFrame(); b:newFrame() end
  local img
  if i == 6 then img = img06 else img = Image{ fromFile = SRC .. string.format("%02d.png", i) } end
  assert(img, "failed to load frame " .. i)
  n.frames[fn].duration = times[fn]
  b.frames[fn].duration = times[fn]
  n:newCel(n.layers[1], fn, img, Point(0, 0))
  b:newCel(b.layers[1], fn, img, Point(64, 64))
  local full = Image(256, 256, ColorMode.RGB)
  full:drawImage(img, Point(64, 64))
  ns:drawImage(img, Point(i * 128, 0))
  bs:drawImage(full, Point(i * 256, 0))
  nat[fn] = img; comp[fn] = full
end
for _, root in ipairs({ OUT_CHARS, OUT_EXP }) do
  n:saveAs(root .. "native128.aseprite")
  b:saveAs(root .. "body256.aseprite")
  ns:saveAs(root .. "native-strip.png")
  bs:saveAs(root .. "body256-strip.png")
  for i = 1, 12 do
    nat[i]:saveAs(root .. "native/" .. string.format("%02d.png", i - 1))
    comp[i]:saveAs(root .. "body256/" .. string.format("%02d.png", i - 1))
  end
end
n:close(); b:close()
print("FIX A CYCLE AUTHORED: back_r-Sword-full glm-fixes (12f, 730ms)")
