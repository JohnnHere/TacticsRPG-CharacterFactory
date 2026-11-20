local f = app.fs.joinPath(app.fs.currentPath, 'characters/orc-v1/source/aseprite/complete-v1/composite/front_r/sword-attack.aseprite')
local s = Sprite{ fromFile = f }
print('front_r sword layers:', #s.layers)
for i, l in ipairs(s.layers) do
  print('  layer ' .. i .. ': ' .. l.name)
end
s:close()

local fb = app.fs.joinPath(app.fs.currentPath, 'characters/orc-v1/source/aseprite/complete-v1/composite/back_r/sword-attack.aseprite')
local sb = Sprite{ fromFile = fb }
print('back_r sword layers:', #sb.layers)
for i, l in ipairs(sb.layers) do
  print('  layer ' .. i .. ': ' .. l.name)
end
sb:close()
