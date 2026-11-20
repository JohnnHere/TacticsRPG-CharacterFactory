local root=app.fs.currentPath;local p=app.fs.joinPath(root,"characters/orc-v1/source/rear-recovery-v2/back_r/Axe/Attack-representative-v1/layers/body/04.png");local im=Image{fromFile=p};local function a(p)return app.pixelColor.rgbaA(p)>0 end
for y=70,98 do local row=string.format("%03d ",y);for x=154,178 do row=row..(a(im:getPixel(x,y)) and "#" or ".")end;print(row)end
