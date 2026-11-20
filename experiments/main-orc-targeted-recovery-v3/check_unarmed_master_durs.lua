for _, d in ipairs({ "back_r", "back_l" }) do
  local s = Sprite{ fromFile = string.format("characters/orc-v1/source/aseprite/rear-recovery-v2/native/unarmed-%s.aseprite", d) }
  local durs = {}
  for i = 1, #s.frames do
    table.insert(durs, math.floor(s.frames[i].duration * 1000 + 0.5))
  end
  print(d, "native master durations:", table.concat(durs, ", "))
  
  local sc = Sprite{ fromFile = string.format("characters/orc-v1/source/aseprite/rear-recovery-v2/composite/%s/unarmed-attack.aseprite", d) }
  local cdurs = {}
  for i = 1, #sc.frames do
    table.insert(cdurs, math.floor(sc.frames[i].duration * 1000 + 0.5))
  end
  print(d, "composite master durations:", table.concat(cdurs, ", "))
end
