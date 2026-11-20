local root=app.fs.currentPath
local function abs(p)return app.fs.joinPath(root,p)end
local function read(p)local f=assert(io.open(abs(p),'r'));local t=json.decode(f:read('*a'));f:close();return t end
local function blank(w,h)local a=Image(w,h,ColorMode.RGB);a:clear();return a end
local function equal(a,b)local n=0;assert(a.width==b.width and a.height==b.height);for y=0,a.height-1 do for x=0,a.width-1 do local p,q=a:getPixel(x,y),b:getPixel(x,y);if app.pixelColor.rgbaA(p)==0 and app.pixelColor.rgbaA(q)==0 then else assert(p==q,'RGBA mismatch '..x..','..y)end end end end
local results={}
for _,d in ipairs({'back_r','back_l'})do
 local dir='characters/orc-v1/source/combat-recovery-v8/rear-inbetween/'..d..'-sword';local c=read(dir..'/clip.json');local sp=app.open(abs(c.master));local ns=app.open(abs(c.nativeMaster));assert(#sp.frames==14 and #ns.frames==14);local total=0
 for i,f in ipairs(c.frames)do
 assert(math.abs(sp.frames[i].duration*1000-f.durationMs)<.1);assert(math.abs(ns.frames[i].duration*1000-f.durationMs)<.1);total=total+f.durationMs
 local a=blank(256,256);a:drawSprite(sp,i);equal(a,Image{fromFile=abs(f.png)})
 for _,l in ipairs(sp.layers)do local b=blank(256,256);local cel=l:cel(i);if cel then b:drawImage(cel.image,cel.position)end;equal(b,Image{fromFile=abs(f.layers[l.name].png)})end
 local n=blank(128,128);n:drawSprite(ns,i);equal(n,Image{fromFile=abs(f.nativePng)})
 end
 assert(total==c.totalDurationMs);sp:close();ns:close();results[#results+1]={direction=d,frames=14,rgbaComparisons=84,totalDurationMs=total,status='PASS_SAVED_MASTER_RGBA_AND_TIMING'}
end
local f=assert(io.open(abs('experiments/main-orc-combat-recovery-v8/rear-inbetween/saved-source-verification.json'),'w'));f:write(json.encode({results=results}));f:close()
