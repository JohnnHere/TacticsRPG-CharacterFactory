local root=app.params.root;local function file(p)return app.fs.joinPath(root,p)end;local p='experiments/main-orc-entry-v1/inputs/';local pc=app.pixelColor
local function load(path)local s=app.open(file(path));local im=Image(s.width,s.height,ColorMode.RGB);im:clear();im:drawSprite(s,1);s:close();return im end
local body=load('characters/orc-v1/source/onehanded-polish-v1/Sword/Attack/layers/body/00.png');local raw=load(p..'prep-raw.png');local mask=load(p..'prepare-mask.png')
for y=0,127 do for x=0,127 do if pc.rgbaR(mask:getPixel(x,y))==255 then body:drawPixel(x+64,y+64,raw:getPixel(x,y))end end end
-- Remove only two short empty-space specks beneath the moved glove; no armor redraw.
for y=84,88 do for x=25,34 do body:drawPixel(x+64,y+64,0)end end
local hand=Image(256,256,ColorMode.RGB);hand:clear()
local function inside(x,y,pts)local c=false;local j=#pts;for i=1,#pts do local a,b=pts[i],pts[j];if(a[2]>y)~=(b[2]>y)and x<(b[1]-a[1])*(y-a[2])/(b[2]-a[2])+a[1]then c=not c end;j=i end;return c end
for y=65,71 do for x=32,40 do if inside(x,y,{{33,66},{36,65},{39,66},{40,69},{37,71},{34,69}})then hand:drawPixel(x+64,y+64,body:getPixel(x+64,y+64))end end end
local s=Sprite(256,256,ColorMode.RGB);s.layers[1].name='body';s:newCel(s.layers[1],1,body,Point(0,0));local l=s:newLayer();l.name='handFront';s:newCel(l,1,hand,Point(0,0));s:saveAs(file(p..'prepare-arm.aseprite'));body:saveAs(file(p..'prepare-body.png'));hand:saveAs(file(p..'prepare-hand.png'));s:close()
