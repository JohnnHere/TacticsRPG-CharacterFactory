local src='./characters/orc-v1/source/combat-rescue-v5/body-specialist/'
local out=src..'repair1/'
local s=app.open(src..'03-impact-native.aseprite')
local img=Image(128,128,ColorMode.RGB)
img:drawSprite(s,1)
local rgba=app.pixelColor.rgba
local C={ink=rgba(12,9,15,255),shadow=rgba(27,15,22,255),leather=rgba(57,29,32,255),light=rgba(78,42,43,255),edge=rgba(92,50,48,255),steel=rgba(48,49,55,255),steelLight=rgba(70,70,75,255)}
local function put(x,y,col) img:drawPixel(x-2,y,col) end
-- Local authored glove only. Shoulder/torso/pelvis/stance pixels are inherited.
local rows={ [75]={92,97},[76]={92,98},[77]={92,98},[78]={92,98},[79]={91,99},[80]={90,100},[81]={90,100},[82]={90,100},[83]={91,100},[84]={92,99},[85]={93,98},[86]={94,97} }
for y=75,86 do local span=rows[y];for x=span[1],span[2] do
 local col=C.leather
 if y<=77 then col=C.steel end
 if x==span[1] or x==span[2] or y==86 then col=C.ink end
 put(x,y,col)
end end
-- Cuff rim joins the existing forearm; narrow wrist and rounded closed fist.
for x=93,96 do put(x,75,C.steelLight);put(x,77,C.shadow) end
for x=93,97 do put(x,76,C.steel) end
for x=93,97 do put(x,79,C.light) end
for x=94,98 do put(x,80,C.edge) end
for y=81,83 do put(94,y,C.shadow);put(97,y,C.shadow);put(99,y,C.light) end
-- Thumb wraps across the inside of a closed empty palm, not an item.
put(91,80,C.light);put(91,81,C.edge);put(92,82,C.light);put(93,82,C.shadow)
for x=94,97 do put(x,84,C.light) end
put(95,85,C.shadow);put(96,85,C.shadow)
local n=Sprite(128,128,ColorMode.RGB);n.layers[1].name='body';n.frames[1].duration=0.160
n:newCel(n.layers[1],1,img,Point(0,0));n:saveAs(out..'03-impact-native.aseprite')
app.command.SaveFileAs{ui=false,filename=out..'03-impact-native.png'}
local c=Sprite(256,256,ColorMode.RGB);c.layers[1].name='body';c.frames[1].duration=0.160
c:newCel(c.layers[1],1,img,Point(64,64));c:saveAs(out..'03-impact-composite.aseprite')
app.command.SaveFileAs{ui=false,filename=out..'03-impact-composite.png'}
s:close();n:close();c:close()
