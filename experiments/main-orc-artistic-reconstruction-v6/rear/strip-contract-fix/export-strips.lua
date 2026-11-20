-- Read saved masters only. Never save/modify masters or individual exports.
local E='experiments/main-orc-artistic-reconstruction-v6/rear/strip-contract-fix'
local C='characters/orc-v1/source/artistic-reconstruction-v6/rear'
local function abs(p) return app.fs.joinPath(app.fs.currentPath,p) end
local function read(p) local f=assert(io.open(abs(p),'r'));local s=f:read('*a');f:close();return json.decode(s) end
local function blank(w,h) local im=Image(w,h,ColorMode.RGB);im:clear();return im end
local function equal(a,b,msg)
 assert(a.width==b.width and a.height==b.height,msg..' dimensions')
 for y=0,a.height-1 do for x=0,a.width-1 do assert(a:getPixel(x,y)==b:getPixel(x,y),msg..' RGBA mismatch at '..x..','..y) end end
end
local result={}
for _,cell in ipairs({'back_l-sword','back_l-axe','back_r-sword','back_r-axe'}) do
 local dir=C..'/'..cell;local clip=read(dir..'/clip.json');local count=clip.frameCount
 local checks={cell=cell,frames=count,exports={},roundtripReopened=true}
 for _,spec in ipairs({{key='nativeMaster',size=128,output='native-strip.png',frameKey='nativePng'},{key='master',size=256,output='composite-strip.png',frameKey='png'}}) do
  local size=spec.size;local spr=app.open(abs(clip[spec.key]));assert(spr.width==size and spr.height==size and #spr.frames==count)
  local strip=blank(size*count,size)
  for i=1,count do
   assert(math.abs(spr.frames[i].duration*1000-clip.frames[i].durationMs)<.1,'Timing mismatch')
   local frame=blank(size,size);frame:drawSprite(spr,i)
   equal(frame,Image{fromFile=abs(clip.frames[i][spec.frameKey])},cell..' saved master / frame '..i)
   strip:drawImage(frame,Point((i-1)*size,0))
  end
  strip:saveAs(abs(dir..'/'..spec.output));spr:close()
  -- Reopen both source and PNG; confirm every tile against source and exports.
  local reopened=app.open(abs(clip[spec.key]));local png=Image{fromFile=abs(dir..'/'..spec.output)}
  assert(png.width==size*count and png.height==size)
  for i=1,count do
   assert(math.abs(reopened.frames[i].duration*1000-clip.frames[i].durationMs)<.1)
   local fromMaster=blank(size,size);fromMaster:drawSprite(reopened,i)
   local fromStrip=blank(size,size);fromStrip:drawImage(png,Point(-(i-1)*size,0))
   equal(fromStrip,fromMaster,cell..' reopened strip / master '..i)
   equal(fromStrip,Image{fromFile=abs(clip.frames[i][spec.frameKey])},cell..' reopened strip / individual '..i)
  end
  reopened:close()
  checks.exports[#checks.exports+1]={path=dir..'/'..spec.output,width=size*count,height=size,exactRgbaTiles=count,timingVerified=true}
 end
 result[#result+1]=checks
end
local f=assert(io.open(abs(E..'/aseprite-roundtrip.json'),'w'));f:write(json.encode(result));f:close()
