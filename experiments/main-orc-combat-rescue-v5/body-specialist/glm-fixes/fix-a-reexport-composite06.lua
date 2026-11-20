-- fix-a-reexport-composite06.lua
-- Reexporta SOMENTE o composto 256 do frame reparado 06 a partir do nativo corrigido
-- (o empacotador sobrescreveu body256/06.png com o de repair1 por engano; este script
-- restaura o composto do pixel já autoral fixado: nativo em (64,64), ground 190).
local img = Image{ fromFile = "characters/orc-v1/source/combat-rescue-v5/body-specialist/glm-fixes/back_r-Sword-full/native/06.png" }
assert(img, "fixed native 06 not found")
local full = Image(256, 256, ColorMode.RGB)
full:drawImage(img, Point(64, 64))
for _, root in ipairs({
  "characters/orc-v1/source/combat-rescue-v5/body-specialist/glm-fixes/back_r-Sword-full/",
  "experiments/main-orc-combat-rescue-v5/body-specialist/glm-fixes/back_r-Sword-full/",
}) do
  full:saveAs(root .. "body256/06.png")
  print("re-exported " .. root .. "body256/06.png")
end
