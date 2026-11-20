local root=app.fs.currentPath;local function f(p)return app.fs.joinPath(root,p)end
local function char(p)
 if app.pixelColor.rgbaA(p)==0 then return "." end
 local r,g,b=app.pixelColor.rgbaR(p),app.pixelColor.rgbaG(p),app.pixelColor.rgbaB(p)
 if r>g*1.1 and g>b*1.07 then return "B" end
 if r<g*0.72 and g>b*1.18 then return "G" end
 return "#"
end
for _,idx in ipairs({4,5}) do
 local im=Image{fromFile=f("experiments/main-orc-rear-recovery-v2/back_l-axe-repaired-native/"..string.format("%02d.png",idx))}
 print("AxeL native raw frame "..idx.." ROI x0..40, y45..90; B=red-brown, G=green, #=other opaque")
 for y=45,90 do local s=string.format("%03d ",y);for x=0,40 do s=s..char(im:getPixel(x,y)) end;print(s) end
end
