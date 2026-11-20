-- ============================================================================
-- Script de autoria (Aseprite Lua) — targeted-repair-unarmed-v1
-- Restaura o braco esquerdo desaparecido no frame F03 (index 3) de back_l/Unarmed.
--
-- Defeito confirmado (Round 3 + reprodicao visual 1x):
--   back_l/Unarmed F02: braco esquerdo estendido (soco), presente.
--   back_l/Unarmed F03: braco esquerdo SUMIU (band rows ~96-112: 347->0), sem
--   frame intermediario de retorno ao quadril.
--   back_l/Unarmed F04: braco esquerdo de volta ao quadril (presente).
--
-- Correcao cirurgica (lesson 17: surgical-same-view-donor-repair):
--   Copia apenas pixels opacos do braco esquerdo do F04 (mesma vista, mesmo
--   individuo, braco ja no quadril) para os locais correspondentes do F03
--   onde aquele mesmo pixel esta transparente (ausente). Nao sobrepoe nada
--   existente no F03; apenas preenche o que falta.
-- ============================================================================

local spritePath = arg[1]
if not spritePath then
  app.alert("Uso: aseprite --batch --noinapp --script restore_backl_unarmed_f03.lua <caminho.aseprite>")
  return
end

local sprite = app.open(spritePath)
if not sprite then
  app.alert("Nao foi possivel abrir: " .. spritePath)
  return
end

-- Encontrar layer "body"
local bodyLayer = nil
for _, layer in ipairs(sprite.layers) do
  if layer.name == "body" then
    bodyLayer = layer
    break
  end
end

if not bodyLayer then
  app.alert("Layer 'body' nao encontrada em " .. spritePath)
  app.close(sprite)
  return
end

-- Cel da layer body por frameNumber
local celByFrame = {}
for _, cel in ipairs(bodyLayer.cels) do
  celByFrame[cel.frameNumber] = cel
end

-- Aseprite frames sao 1-based: index 3 = frame 4, index 4 = frame 5
local f03 = celByFrame[sprite.frames[4].frameNumber]  -- frame index 3
local f04 = celByFrame[sprite.frames[5].frameNumber]  -- frame index 4

if not f03 or not f04 then
  app.alert("Cels F03/F04 nao encontradas na layer body.")
  app.close(sprite)
  return
end

local img03 = f03.image
local img04 = f04.image

if img03.width ~= img04.width or img03.height ~= img04.height then
  app.alert("Canvas divergente entre F03 e F04.")
  app.close(sprite)
  return
end

-- Copia apenas pixels opacos do lado esquerdo (braco esquerdo, back view)
-- do F04 para posicoes transparentes do F03.
local restored = 0
local half = math.floor(img04.width / 2)
for y = 0, img04.height - 1 do
  for x = 0, half - 1 do
    local c04 = img04:getPixel(x, y)
    local c03 = img03:getPixel(x, y)
    if c04.alpha > 0 and c03.alpha == 0 then
      img03:putPixel(x, y, c04)
      restored = restored + 1
    end
  end
end

app.alert(string.format("Restaurados %d pixels do braco esquerdo no F03.", restored))

-- Salvar (sobrescreve o fork de trabalho)
app.command("Save")
app.close(sprite)
