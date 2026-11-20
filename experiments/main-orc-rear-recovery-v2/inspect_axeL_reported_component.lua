local root=app.fs.currentPath;local function f(p)return app.fs.joinPath(root,p)end
local im=Image{fromFile=f("experiments/main-orc-rear-recovery-v2/back_l-axe-repaired-native/02.png")}
local base=Image{fromFile=f("experiments/main-orc-rear-recovery-v2/inputs/back_l-sword-native128.png")}
local seen={};local function key(x,y)return y*128+x end
for y=0,127 do for x=0,127 do local k=key(x,y);if not seen[k] and app.pixelColor.rgbaA(im:getPixel(x,y))>0 then
 local q={{x,y}};seen[k]=true;local head=1;local pts={};local minx,miny,maxx,maxy=x,y,x,y
 while head<=#q do local a=q[head][1];local b=q[head][2];head=head+1;pts[#pts+1]={a,b};minx=math.min(minx,a);maxx=math.max(maxx,a);miny=math.min(miny,b);maxy=math.max(maxy,b)
  for dy=-1,1 do for dx=-1,1 do if dx~=0 or dy~=0 then local nx,ny=a+dx,b+dy;if nx>=0 and nx<128 and ny>=0 and ny<128 then local nk=key(nx,ny);if not seen[nk] and app.pixelColor.rgbaA(im:getPixel(nx,ny))>0 then seen[nk]=true;q[#q+1]={nx,ny} end end end end end
 end
 if minx>=15 and maxx<=30 and miny>=18 and maxy<=38 then
  local baseline=0;local same=0;for _,p in ipairs(pts)do local bp=base:getPixel(p[1],p[2]);if app.pixelColor.rgbaA(bp)>0 then baseline=baseline+1;if bp==im:getPixel(p[1],p[2])then same=same+1 end end end
  print(string.format("component size=%d bbox=%d,%d..%d,%d baselineOpaque=%d exactSame=%d coords=%s",#pts,minx,miny,maxx,maxy,baseline,same,(function()local t={}for _,p in ipairs(pts)do t[#t+1]=p[1]..":"..p[2]end;return table.concat(t," ")end)()))
 end
end end end
