local root=app.fs.currentPath;local function f(p)return app.fs.joinPath(root,p)end;local function a(p)return app.pixelColor.rgbaA(p)>0 end
local function show(path,x0,x1,y0,y1)
 local im=Image{fromFile=f(path)};print(path)
 for y=y0,y1 do local row=string.format("%03d ",y);for x=x0,x1 do row=row..(a(im:getPixel(x,y)) and "#" or ".")end;print(row)end
end
show("experiments/main-orc-rear-recovery-v2/raw/pixellab-skeleton-v3/back_r_axe/00.png",96,127,0,48)
show("experiments/main-orc-rear-recovery-v2/raw/pixellab-skeleton-v3/back_r_axe/01.png",96,127,0,48)
show("experiments/main-orc-rear-recovery-v2/back_l-sword-cleaned-native/05.png",0,40,30,70)
show("experiments/main-orc-rear-recovery-v2/back_l-sword-cleaned-native/06.png",0,40,30,80)
show("experiments/main-orc-rear-recovery-v2/axe-r-cleaned-native/03.png",96,127,24,68)
show("experiments/main-orc-rear-recovery-v2/axe-r-cleaned-native/04.png",84,127,36,78)
