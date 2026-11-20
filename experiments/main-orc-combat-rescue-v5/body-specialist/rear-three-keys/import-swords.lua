local out='./characters/orc-v1/source/combat-rescue-v5/body-specialist/rear-three-keys/'
local exp='./experiments/main-orc-combat-rescue-v5/body-specialist/rear-three-keys/'
local records={}
for _,group in ipairs({{'back_r-Sword','clean-back_r-Sword'},{'back_l-Sword','back_l-Sword'}}) do
 for i=0,2 do
  local rawName='raw-'..group[2]..'-'..i..'.png'
  local raw=Image{fromFile=exp..rawName};local minY=128;local maxY=-1
  for y=0,raw.height-1 do for x=0,raw.width-1 do if app.pixelColor.rgbaA(raw:getPixel(x,y))>0 then minY=math.min(minY,y);maxY=math.max(maxY,y) end end end
  local dy=126-maxY
  assert(minY+dy>=0,'Top clipping would occur; reject registration')
  local body=Image(128,128,ColorMode.RGB);body:drawImage(raw,Point(0,dy))
  local prefix=out..group[1]..'/'..string.format('%02d',i+1)
  local n=Sprite(128,128,ColorMode.RGB);n.layers[1].name='body';n.frames[1].duration=0.160
  n:newCel(n.layers[1],1,body,Point(0,0));n:saveAs(prefix..'-native.aseprite');body:saveAs(prefix..'-native.png')
  local full=Image(256,256,ColorMode.RGB);full:drawImage(body,Point(64,64))
  local c=Sprite(256,256,ColorMode.RGB);c.layers[1].name='body';c.frames[1].duration=0.160
  c:newCel(c.layers[1],1,body,Point(64,64));c:saveAs(prefix..'-body256.aseprite');full:saveAs(prefix..'-body256.png')
  records[#records+1]={group=group[1],key=i+1,raw=rawName,groundRegistrationY=dy,minRawY=minY,maxRawY=maxY}
  n:close();c:close()
 end
end
local f=io.open(exp..'registration-swords.json','w');f:write(json.encode(records));f:close()
