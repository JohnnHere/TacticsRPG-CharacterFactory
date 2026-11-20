local root=app.fs.currentPath
local function p(x) return app.fs.joinPath(root,x) end
local function save(im,file) app.fs.makeAllDirectories(app.fs.filePath(file)); im:saveAs(file) end
for _,slug in ipairs({'front_r-Sword','front_l-Sword'}) do
 local dir='characters/orc-v1/source/combat-recovery-v8/frontal/'..slug
 local s=assert(app.open(p(dir..'/source/composite.aseprite')))
 assert(s.width==256 and s.height==256 and #s.frames==13)
 local layers={}; for _,l in ipairs(s.layers) do layers[l.name]=l end
 local cs=Image(256*13,256,ColorMode.RGB); cs:clear()
 for fi=1,13 do
  local ix=string.format('%02d',fi-1)
  local im=Image(256,256,ColorMode.RGB); im:clear(); im:drawSprite(s,fi)
  save(im,p(dir..'/'..ix..'.png')); save(im,p(dir..'/frames/'..ix..'.png')); cs:drawImage(im,Point((fi-1)*256,0))
  for _,name in ipairs({'body','handFront','weaponBack','weaponFront'}) do
   local layer=layers[name]; assert(layer,'layer '..name)
   local cel=layer:cel(fi); local li=Image(256,256,ColorMode.RGBA); li:clear()
   if cel then li:drawImage(cel.image,cel.position) end
   save(li,p(dir..'/layers/'..name..'/'..ix..'.png'))
  end
 end
 save(cs,p(dir..'/composite-strip.png')); s:close()
end
print('V8_EXPORT_OK')
