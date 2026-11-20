-- Independent saved-master roundtrip verification, no source mutation.
local E='experiments/main-orc-backl-v5base'
local function read(p)local f=assert(io.open(p,'r'));local v=json.decode(f:read('*a'));f:close();return v end
local function blank(w,h)local i=Image(w,h,ColorMode.RGB);i:clear();return i end
local function same(a,b)
 assert(a.width==b.width and a.height==b.height)
 for y=0,a.height-1 do for x=0,a.width-1 do local p,q=a:getPixel(x,y),b:getPixel(x,y);assert(p==q or (app.pixelColor.rgbaA(p)==0 and app.pixelColor.rgbaA(q)==0),'roundtrip pixel mismatch')end end
end
local checked=0
for _,c in ipairs(read(E..'/author-config.json'))do
 local out=E..'/'..c.name
 for _,name in ipairs({'composite','native','body'})do
  local s=app.open(out..'/source/'..name..'.aseprite');assert(#s.frames==#c.frames)
  if name=='body'then assert(#s.layers==1 and s.layers[1].name=='body')else
   assert(#s.layers==4);for j,n in ipairs({'weaponBack','body','weaponFront','handFront'})do assert(s.layers[j].name==n)end
  end
  for fi,f in ipairs(c.frames)do
   assert(math.abs(s.frames[fi].duration*1000-f.durationMs)<0.1)
   local im=blank(s.width,s.height);im:drawSprite(s,fi)
   local dir=name=='composite' and 'frames' or name=='native' and 'native' or 'layers/body'
   same(im,Image{fromFile=out..'/'..dir..'/'..string.format('%02d.png',fi-1)})
   checked=checked+1
  end
  s:close()
 end
end
local f=assert(io.open(E..'/master-roundtrip.json','w'));f:write(json.encode{status='PASS',masterCount=6,renderedFramesChecked=checked,layerOrder=true,durations=true,visibleRgbaExact=true});f:close()
