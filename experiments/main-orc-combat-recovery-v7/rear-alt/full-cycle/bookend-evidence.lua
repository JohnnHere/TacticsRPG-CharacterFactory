local root=app.fs.currentPath;local E='experiments/main-orc-combat-recovery-v7/rear-alt/full-cycle';local function abs(p)return app.fs.joinPath(root,p)end
for _,k in ipairs({'sword','axe'})do
 for _,which in ipairs({'before','after'})do
  local src=which=='before'and('characters/orc-v1/source/artistic-reconstruction-v6/rear/back_l-'..k)or('characters/orc-v1/source/combat-recovery-v7/rear-alt/back_l-'..k)
  local ids=which=='before'and{10,11,0,1}or{12,14,0,1};local out=Image(26*4,28,ColorMode.RGB);out:clear()
  for j,i in ipairs(ids)do local im=Image{fromFile=abs(src..'/layers/body/'..string.format('%02d',i)..'.png')};local tile=Image(26,28,ColorMode.RGB);tile:clear();tile:drawImage(im,Point(-99,-89));out:drawImage(tile,Point((j-1)*26,0))end
  out:resize(832,224);out:saveAs(abs(E..'/'..k..'-bookend-'..which..'.png'))
 end
end
