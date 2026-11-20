local root=app.fs.currentPath;local function f(p)return app.fs.joinPath(root,p)end
local out="characters/orc-v1/source/rear-recovery-v2/back_l/Axe/Attack-representative-v1"
local grips={{92,108},{104,78},{104,78},{86,118},{96,141},{99,145}}
local compSheet=Image(192*3,192*2,ColorMode.RGB);compSheet:clear()
local bodySheet=Image(192*3,192*2,ColorMode.RGB);bodySheet:clear()
for i=1,6 do
 local n=string.format("%02d.png",i)
 local comp=Image{fromFile=f(out.."/"..n)};local body=Image{fromFile=f(out.."/layers/body/"..n)}
 local x,y=grips[i][1],grips[i][2];local rect=Rectangle(x-24,y-24,48,48)
 for _,pair in ipairs({{comp,compSheet},{body,bodySheet}}) do
  local src,dst=pair[1],pair[2]
  local crop=Image(48,48,ColorMode.RGB);crop:clear();crop:drawImage(src,Point(-rect.x,-rect.y));crop:resize(192,192);dst:drawImage(crop,Point(((i-1)%3)*192,math.floor((i-1)/3)*192))
 end
end
compSheet:saveAs(f("experiments/main-orc-rear-recovery-v2/back_l-axe-grip-closeups-qa.png"))
bodySheet:saveAs(f("experiments/main-orc-rear-recovery-v2/back_l-axe-grip-body-only-qa.png"))
print("Saved six actual AxeL composite and weapon-off grip crops from the four-layer Aseprite exports.")
