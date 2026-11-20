local root=app.fs.currentPath;local function f(p)return app.fs.joinPath(root,p)end
local function alpha(p)return app.pixelColor.rgbaA(p)end
local function show(path,x0,x1,y0,y1)
 local im=Image{fromFile=f(path)};print(path)
 for y=y0,y1 do local row=string.format("%03d ",y);for x=x0,x1 do row=row..(alpha(im:getPixel(x,y))>0 and "#" or ".") end;print(row) end
end
show("experiments/main-orc-rear-recovery-v2/inputs/back_l-sword-native128.png",8,34,38,62)
show("experiments/main-orc-rear-recovery-v2/raw/pixellab-skeleton-v3/back_l/00.png",8,34,22,49)
show("experiments/main-orc-rear-recovery-v2/inputs/back_r-axe-native128.png",90,116,38,65)
show("experiments/main-orc-rear-recovery-v2/raw/pixellab-skeleton-v3/back_r_axe/00.png",90,116,38,65)
show("experiments/main-orc-rear-recovery-v2/inputs/back_l-sword-native128.png",18,48,48,78)
show("experiments/main-orc-rear-recovery-v2/inputs/back_r-axe-native128.png",84,112,48,78)
show("experiments/main-orc-rear-recovery-v2/inputs/back_l-sword-native128.png",24,38,76,89)
show("experiments/main-orc-rear-recovery-v2/inputs/back_r-axe-native128.png",89,103,76,89)
show("experiments/main-orc-rear-recovery-v2/raw/pixellab-skeleton-v3/back_l/01.png",16,49,0,22)
show("experiments/main-orc-rear-recovery-v2/raw/pixellab-skeleton-v3/back_l/02.png",16,64,0,22)
show("experiments/main-orc-rear-recovery-v2/raw/pixellab-skeleton-v3/back_l/04.png",0,38,18,54)
show("experiments/main-orc-rear-recovery-v2/raw/pixellab-skeleton-v3/back_l/05.png",0,38,32,66)
