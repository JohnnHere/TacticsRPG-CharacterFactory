local compR = Sprite{ fromFile = "characters/orc-v1/source/aseprite/rear-recovery-v2/composite/front_r/defeat.aseprite" }
local pngR = Image{ fromFile = "characters/orc-v1/source/rear-recovery-v2/front_r/Defeat/04.png" }
local celR = compR.layers[1]:cel(5)
local diff = 0
for y = 0, 255 do
  for x = 0, 255 do
    if celR.image:getPixel(x, y) ~= pngR:getPixel(x, y) then diff = diff + 1 end
  end
end
print("Diff between master cel 5 and PNG 04:", diff)
