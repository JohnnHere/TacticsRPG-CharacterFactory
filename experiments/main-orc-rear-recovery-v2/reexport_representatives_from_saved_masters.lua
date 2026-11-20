-- Final exports are rendered from the saved Aseprite masters, not staging images.
local root=app.fs.currentPath;local function f(p)return app.fs.joinPath(root,p)end
local names={"weaponBack","body","weaponFront","handFront"}
local specs={
 {dir="back_r",name="sword",out="characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2",comp="characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_r/sword-attack-representative-v2.aseprite",body="characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_r/sword-body-representative-v2.aseprite"},
 {dir="back_l",name="sword",out="characters/orc-v1/source/rear-recovery-v2/back_l/Sword/Attack-representative-v1",comp="characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_l/sword-attack-representative-v1.aseprite",body="characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_l/sword-body-representative-v1.aseprite"},
 {dir="back_r",name="axe",out="characters/orc-v1/source/rear-recovery-v2/back_r/Axe/Attack-representative-v1",comp="characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_r/axe-attack-representative-v1.aseprite",body="characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_r/axe-body-representative-v1.aseprite"},
 {dir="back_l",name="axe",out="characters/orc-v1/source/rear-recovery-v2/back_l/Axe/Attack-representative-v1",comp="characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_l/axe-attack-representative-v1.aseprite",body="characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_l/axe-body-representative-v1.aseprite"}
}
local function blank(w,h)local im=Image(w,h,ColorMode.RGB);im:clear();return im end
local exportOnly=os.getenv("ASEPRITE_EXPORT_ONLY")
for _,sp in ipairs(specs) do if not exportOnly or exportOnly==(sp.dir.."_"..sp.name) then
 app.fs.makeAllDirectories(f(sp.out.."/body-only"));app.fs.makeAllDirectories(f(sp.out.."/native"))
 for _,n in ipairs(names) do app.fs.makeAllDirectories(f(sp.out.."/layers/"..n)) end
 local comp=app.open(f(sp.comp));local body=app.open(f(sp.body));assert(#comp.frames==8 and #body.frames==8,"saved master frame count")
 local crops,bodyStrip,nativeStrip={},{},{};local compositeSheet=Image(256*4,256*2,ColorMode.RGB);compositeSheet:clear();local noWeaponSheet=Image(256*4,256*2,ColorMode.RGB);noWeaponSheet:clear()
 for i=1,8 do
  local flat=blank(256,256);flat:drawSprite(comp,i);flat:saveAs(f(sp.out.."/"..string.format("%02d.png",i-1)))
  compositeSheet:drawImage(flat,Point(((i-1)%4)*256,math.floor((i-1)/4)*256))
  local body256=blank(256,256);body256:drawSprite(body,i);body256:saveAs(f(sp.out.."/body-only/"..string.format("%02d.png",i-1)))
  local native=Image(128,128,ColorMode.RGB);native:clear();native:drawImage(body256,Point(-64,-64));native:saveAs(f(sp.out.."/native/"..string.format("%02d.png",i-1)))
  nativeStrip[i]=native;bodyStrip[i]=native
  noWeaponSheet:drawImage(body256,Point(((i-1)%4)*256,math.floor((i-1)/4)*256))
  for _,layerName in ipairs(names) do
   for _,l in ipairs(comp.layers) do l.isVisible=(l.name==layerName) end
   local layer=blank(256,256);layer:drawSprite(comp,i);layer:saveAs(f(sp.out.."/layers/"..layerName.."/"..string.format("%02d.png",i-1)))
  end
  for _,l in ipairs(comp.layers) do l.isVisible=true end
 end
 local ns=Image(128*8,128,ColorMode.RGB);ns:clear();local bs=Image(128*8,128,ColorMode.RGB);bs:clear()
 for i=1,8 do ns:drawImage(nativeStrip[i],Point((i-1)*128,0));bs:drawImage(bodyStrip[i],Point((i-1)*128,0)) end
 ns:saveAs(f(sp.out.."/native-strip.png"));bs:saveAs(f(sp.out.."/body-only-strip.png"));compositeSheet:saveAs(f(sp.out.."/composite-sheet-qa.png"));noWeaponSheet:saveAs(f(sp.out.."/weapon-layers-off-qa.png"))
 comp:close();body:close();print("Re-exported "..sp.dir.." "..sp.name.." from saved composite/body masters (8 frames).")
end end
