-- Rework only Orc 07's OWN prior frontal repair, never another character.
local root=app.params.root
local function load(p)local s=app.open(app.fs.joinPath(root,p));local im=Image(s.cels[1].image);s:close();return im end
local original=load('experiments/pixellab-orc-refinement-v4/before/orc-pixellab-07/source/studies/Walk/00.png')
local frontal=load('experiments/pixellab-orc-refinement-v4/07-HeadForward/raw/0.png')
local palette,seen={},{}
for y=7,24 do for x=56,79 do local c=original:getPixel(x,y);if app.pixelColor.rgbaA(c)>0 and not seen[c] then palette[#palette+1]=c;seen[c]=true end end end
local function ownColor(c)
 if app.pixelColor.rgbaA(c)==0 then return 0 end
 local best,score=nil,math.huge
 for _,v in ipairs(palette) do local r=app.pixelColor.rgbaR(c)-app.pixelColor.rgbaR(v);local g=app.pixelColor.rgbaG(c)-app.pixelColor.rgbaG(v);local b=app.pixelColor.rgbaB(c)-app.pixelColor.rgbaB(v);local d=r*r+g*g+b*b;if d<score then best=v;score=d end end
 return best
end
for _,shift in ipairs({1,2}) do
 local im=Image(original)
 for y=3,24 do for x=52,83 do im:drawPixel(x,y,0) end end
 for ty=0,23 do for tx=0,22 do
  local ux=tx
  if ty>=8 and ty<=19 and tx>=2 and tx<=21 then
   local middle=11.5+shift
   if tx<=middle then ux=2+(tx-2)*9.5/(middle-2) else ux=11.5+(tx-middle)*9.5/(21-middle) end
  end
  local sx=53+math.min(29,math.floor(ux*30/23));local sy=4+math.min(27,math.floor(ty*28/24))
  im:drawPixel(56+tx,5+ty,ownColor(frontal:getPixel(sx,sy)))
 end end
 local s=Sprite(128,128,ColorMode.RGB);s:newCel(s.layers[1],1,im,Point(0,0));s.layers[1].name='Own Orc 07 face, proportional perspective retouch, original palette'
 s:saveAs(app.fs.joinPath(root,'experiments/pixellab-orc-refinement-v6/own-perspective-'..shift..'.aseprite'));im:saveAs(app.fs.joinPath(root,'experiments/pixellab-orc-refinement-v6/own-perspective-'..shift..'.png'));s:close()
end
