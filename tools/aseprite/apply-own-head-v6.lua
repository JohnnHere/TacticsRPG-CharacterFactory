local f=assert(io.open(app.params.plan,'r'));local p=json.decode(f:read('*a'));f:close()
local function openImage(file)local s=app.open(file);local im=Image(s.cels[1].image);s:close();return im end
local original=openImage(p.original);local ref=openImage(p.repaired)
local palette,seen={},{}
for y=7,24 do for x=56,79 do local c=original:getPixel(x,y);if app.pixelColor.rgbaA(c)>0 and not seen[c] then seen[c]=true;palette[#palette+1]=c end end end
local function match(c)
 if app.pixelColor.rgbaA(c)==0 then return 0 end
 local best,score=nil,math.huge
 for _,v in ipairs(palette) do local r=app.pixelColor.rgbaR(c)-app.pixelColor.rgbaR(v);local g=app.pixelColor.rgbaG(c)-app.pixelColor.rgbaG(v);local b=app.pixelColor.rgbaB(c)-app.pixelColor.rgbaB(v);local d=r*r+g*g+b*b;if d<score then score=d;best=v end end
 return best
end
for y=5,27 do for x=55,80 do local c=ref:getPixel(x,y);if app.pixelColor.rgbaA(c)>0 then ref:drawPixel(x,y,match(c)) end end end
local rs=Sprite(128,128,ColorMode.RGB);rs:newCel(rs.layers[1],1,ref,Point(0,0));rs.layers[1].name='Only Orc 07 source, palette matched to original head';rs:saveAs(p.referenceMaster);ref:saveAs(p.referencePng);rs:close()
local function inside(x,y)return (y>=3 and y<=20 and x>=52 and x<=83) or (y>=21 and y<=24 and x>=55 and x<=81) or (y>=25 and y<=28 and x>=60 and x<=79) end
local s=Sprite(128,128,ColorMode.RGB);s.layers[1].name='Own Orc 07 head, neck registered to torso, original gait'
for i,frame in ipairs(p.frames) do
 local im=openImage(frame.input)
 for y=3,28 do for x=52,83 do if inside(x,y) then im:drawPixel(x+frame.dx,y+frame.dy,ref:getPixel(x,y)) end end end
 if i>1 then s:newEmptyFrame() end
 s:newCel(s.layers[1],i,im,Point(0,0));s.frames[i].duration=frame.durationMs/1000;im:saveAs(frame.output)
end
s:saveAs(p.master);s:close()
