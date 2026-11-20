-- QA-only source crops from the saved representative composite.
local root=app.fs.currentPath
local function file(p) return app.fs.joinPath(root,p) end
local grips={{175,106},{166,76},{164,84},{183,92},{181,121},{170,127}}
local scale=4; local size=32; local cols=3
local out=Image(cols*size*scale,2*size*scale,ColorMode.RGB); out:clear()
for k=1,6 do
 local frame=k -- composite 01..06; indices start at Lua1
 local im=Image{fromFile=file("characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2/"..string.format("%02d.png",frame))}
 local gx,gy=grips[k][1],grips[k][2]
 for y=0,size-1 do for x=0,size-1 do
  local sx=gx-16+x; local sy=gy-16+y; local p=im:getPixel(sx,sy)
  for yy=0,scale-1 do for xx=0,scale-1 do out:drawPixel(((k-1)%cols)*size*scale+x*scale+xx,math.floor((k-1)/cols)*size*scale+y*scale+yy,p) end end
 end end
end
out:saveAs(file("experiments/main-orc-rear-recovery-v2/back_r-sword-representative-grips-qa.png"))
print("Saved six actual composite hand/grip close-ups in frame order 01–06.")
