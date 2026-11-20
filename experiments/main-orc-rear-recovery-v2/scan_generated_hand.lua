local root=app.fs.currentPath
local function file(p) return app.fs.joinPath(root,p) end
local out=io.open(file("experiments/main-orc-rear-recovery-v2/hand-scan.txt"),"w")
for i=0,7 do
 local im=Image{fromFile=file("characters/orc-v1/source/rear-recovery-v2/back_r/Sword/body-cycle-generated-v1/native/"..string.format("%02d.png",i))}
 local rows={}
 for y=0,127 do
  local xs={}
  for x=88,127 do if app.pixelColor.rgbaA(im:getPixel(x,y))>0 then xs[#xs+1]=x end end
  if #xs>0 then rows[#rows+1]=string.format("%d:%d-%d",y,xs[1],xs[#xs]) end
 end
 out:write("frame "..i.." right:"..table.concat(rows,",").."\n"); out:flush()
end
out:close()
