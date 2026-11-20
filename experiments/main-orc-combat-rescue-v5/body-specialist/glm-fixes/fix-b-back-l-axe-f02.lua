-- fix-b-back-l-axe-f02.lua
-- FIX B (DEFECT-REAR-02-PERSISTENT) — back_l-Axe-full F02
-- Composição cirúrgica: F02 final = original repair1 FORA da máscara (x68..100/y8..33)
-- + resultado do inpaint PixelLab (job 540302e4-2690-4282-8de5-c609f15b1142, seed 20261029,
-- 6.0 gerações) DENTRO da máscara. Delta declarado: 510 px confinados à máscara
-- (validado textualmente: trave/bloco/pino removidos, braço conectado, punho presente).
-- PROVENIÊNCIA: pixel art editada por PixelLab (inpaint condicionado ao próprio F02) e
-- composta/exportada no Aseprite via Lua — imagem importada/retocada, NÃO desenho manual
-- do zero. Demais 11 frames copiados byte-idênticos de repair1 pelo empacotador.
-- Frame.duration em SEGUNDOS. Nativo 128 ground 126; composto 256 offset (64,64) ground 190.

local pc = app.pixelColor
local function rgba(r, g, b, a) return pc.rgba(r, g, b, a) end
local function R(p) return pc.rgbaR(p) end
local function G(p) return pc.rgbaG(p) end
local function B(p) return pc.rgbaB(p) end
local function A(p) return pc.rgbaA(p) end

local SRC = "characters/orc-v1/source/combat-rescue-v5/body-specialist/final-cycles/repair1/back_l-Axe-full/native/"
local EDIT = "experiments/main-orc-combat-rescue-v5/body-specialist/glm-fixes/pixellab-f02-edit1.png"
local OUT_CHARS = "characters/orc-v1/source/combat-rescue-v5/body-specialist/glm-fixes/back_l-Axe-full/"
local OUT_EXP   = "experiments/main-orc-combat-rescue-v5/body-specialist/glm-fixes/back_l-Axe-full/"

local MX0, MY0, MX1, MY1 = 68, 8, 100, 33

local orig = Image{ fromFile = SRC .. "02.png" }
local edit = Image{ fromFile = EDIT }
assert(orig and edit, "failed to load F02 sources")
assert(orig.width == 128 and edit.width == 128, "expected 128x128 sources")

local copied = 0
for y = MY0, MY1 do
  for x = MX0, MX1 do
    local p = edit:getPixel(x, y)
    orig:drawPixel(x, y, rgba(R(p), G(p), B(p), A(p)))
    copied = copied + 1
  end
end
print("FIX B composite: " .. copied .. " px copiados da máscara (" .. MX0 .. ".." .. MX1 .. " / " .. MY0 .. ".." .. MY1 .. ")")

-- dump textual pós-composição (evidência)
print("-- F02 pós-fix (x68..98, y8..33) --")
for y = 8, 33 do
  local row = {}
  for x = 68, 98 do
    local p = orig:getPixel(x, y)
    if A(p) == 0 then row[#row+1] = ".." else row[#row+1] = string.format("%02x%02x%02x", R(p), G(p), B(p)) end
  end
  print(y .. ": " .. table.concat(row, " "))
end

-- montagem do ciclo completo
local times = {0.07,0.08,0.09,0.10,0.11,0.05,0.06,0.11,0.10,0.10,0.10,0.13}
local n = Sprite(128, 128, ColorMode.RGB); n.layers[1].name = "body"
local b = Sprite(256, 256, ColorMode.RGB); b.layers[1].name = "body"
local ns = Image(128 * 12, 128, ColorMode.RGB)
local bs = Image(256 * 12, 256, ColorMode.RGB)
local nat, comp = {}, {}
for i = 0, 11 do
  local fn = i + 1
  if fn > 1 then n:newFrame(); b:newFrame() end
  local img
  if i == 2 then img = orig else img = Image{ fromFile = SRC .. string.format("%02d.png", i) } end
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
print("FIX B CYCLE AUTHORED: back_l-Axe-full glm-fixes (12f, 1100ms)")
