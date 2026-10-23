-- Original pixel authorship performed entirely inside Aseprite's Lua runtime.
-- No PNG/sheet/concept is loaded, traced, sampled, recolored or rescaled.
-- The coordinate drawings below are authored for this approved Orc individual.
-- This is agent-authored scripted pixel art, NOT manual mouse drawing or an AI
-- feature of Aseprite. Shapes, shading and poses are explicitly specified here.
local output=assert(app.params.output,"output directory required")
app.fs.makeAllDirectories(output)
local C={
 ink="211b20",deep="30282a",pants="42363b",pantsLight="59454a",
 skinDark="51482e",skinShade="74643b",skin="99864d",skinLight="b4a05d",skinHigh="cfb979",
 leatherDark="3c2824",leatherShade="5b392c",leather="805039",leatherLight="a46c46",leatherHigh="c58d5c",
 ironDark="30313c",ironShade="494852",iron="68626b",ironLight="90868a",ironHigh="b4a5a3",ironEdge="deccba",
 redDark="48242a",redShade="6b2c30",red="963c38",redLight="ba5543",redHigh="d57a52",
 ivoryShade="a99a75",ivory="d6c69e",ivoryHigh="f2dfb7",eye="efab40",eyeHigh="ffd681"
}
local rgba={};local paletteNames={}
for k in pairs(C)do table.insert(paletteNames,k)end;table.sort(paletteNames)
for _,k in ipairs(paletteNames)do local h=C[k];rgba[k]=app.pixelColor.rgba(tonumber(h:sub(1,2),16),tonumber(h:sub(3,4),16),tonumber(h:sub(5,6),16),255)end
local im,ox,oy
local function pixel(x,y,c)
 x=math.floor(x+(ox or 0)+.5);y=math.floor(y+(oy or 0)+.5)
 assert(x>=0 and x<128 and y>=0 and y<128,"Authored pixel outside canvas")
 im:drawPixel(x,y,rgba[c])
end
local function line(x0,y0,x1,y1,c)
 local dx=math.abs(x1-x0);local sx=x0<x1 and 1 or -1
 local dy=-math.abs(y1-y0);local sy=y0<y1 and 1 or -1;local err=dx+dy
 while true do pixel(x0,y0,c);if x0==x1 and y0==y1 then break end
  local e=2*err;if e>=dy then err=err+dy;x0=x0+sx end;if e<=dx then err=err+dx;y0=y0+sy end
 end
end
local function poly(points,c,outline)
 local ymin,ymax=128,0
 for _,p in ipairs(points)do ymin=math.min(ymin,p[2]);ymax=math.max(ymax,p[2])end
 for y=ymin,ymax do
  local cuts={}
  for i,a in ipairs(points)do local b=points[i%#points+1]
   if(a[2]<=y and b[2]>y)or(b[2]<=y and a[2]>y)then table.insert(cuts,a[1]+(y-a[2])*(b[1]-a[1])/(b[2]-a[2]))end
  end
  table.sort(cuts)
  for i=1,#cuts-1,2 do for x=math.ceil(cuts[i]),math.floor(cuts[i+1])do pixel(x,y,c)end end
 end
 if outline then for i,a in ipairs(points)do local b=points[i%#points+1];line(a[1],a[2],b[1],b[2],outline)end end
end
local function box(x,y,w,h,c)for yy=y,y+h-1 do for xx=x,x+w-1 do pixel(xx,yy,c)end end end
local function shape(p,c)poly(p,c,"ink")end
local layers={"01 Rear cloth","02 Far leg and boot","03 Near leg and boot","04 Torso and cuirass","05 Left armored arm","06 Neckcloth","07 Head and face","08 Belt and tabard","09 Right bare arm"}
local function surface(s,layer,frame,dx,dy,draw)
 im=Image(128,128,ColorMode.RGB);im:clear();ox=dx or 0;oy=dy or 0;draw()
 s:newCel(layer,frame,im,Point(0,0));im=nil;ox=0;oy=0
end
-- Stable lower body: no canvas deformation, no imported pose rig.
local function farLeg(p)
 local k=p.mode=="impact" and 2 or p.mode=="absorb" and 1 or 0
 shape({{67,85},{80,86},{85+k,96},{83+k,108},{87,119},{78,123},{72,113},{69,104},{63,96}},"pants")
 poly({{73,91},{78,91},{80,99},{78,109},{74,104}},"pantsLight")
 shape({{74,103},{82,101},{88,109},{86,119},{79,122},{73,115}},"leather")
 shape({{77,105},{82,104},{85,111},{82,117},{77,115}},"iron")
 poly({{77,106},{81,105},{83,110},{79,113}},"ironLight");line(77,106,79,105,"ironHigh")
 shape({{78,97},{84,98},{87,103},{82,107},{76,103}},"leatherShade")
 shape({{79,98},{84,100},{84,103},{81,105},{77,102}},"iron")
 poly({{79,99},{83,101},{80,103},{78,102}},"ironHigh");pixel(79,99,"ironEdge")
 line(82,110,81,115,"ironShade");line(78,109,78,112,"ironHigh")
 line(76,117,84,114,"leatherHigh")
 shape({{79,117},{86,116},{89,121},{95,123},{96,126},{77,126},{75,123}},"leatherShade")
 poly({{81,119},{85,119},{88,123},{80,123}},"leatherLight");line(78,125,94,125,"leather")
 shape({{87,121},{91,122},{94,124},{87,124}},"ironShade");line(88,122,91,123,"ironLight")
end
local function nearLeg(p)
 local k=p.mode=="windup" and -2 or p.mode=="impact" and 2 or p.mode=="absorb" and -1 or 0
 shape({{48,84},{64,87},{63+k,98},{56+k,108},{51,119},{40,120},{41,108},{43,97}},"pants")
 poly({{48,89},{57,91},{54,100},{48,104},{46,101}},"pantsLight")
 shape({{43,101},{52,104},{54,110},{49,119},{41,120},{37,114}},"leather")
 shape({{43,102},{50,105},{50,111},{45,116},{40,112},{39,108}},"iron")
 poly({{42,104},{48,106},{47,111},{43,113},{40,109}},"ironLight");line(42,104,46,105,"ironHigh")
 poly({{47,108},{49,107},{48,112},{44,115},{44,112}},"ironShade")
 line(41,107,42,110,"ironHigh");pixel(42,106,"ironEdge")
 shape({{45,96},{52,100},{51,105},{45,108},{39,103}},"leatherShade")
 shape({{45,98},{50,101},{46,105},{41,102}},"iron")
 poly({{45,99},{48,101},{45,103},{42,102}},"ironHigh");pixel(45,99,"ironEdge")
 line(40,115,48,118,"leatherHigh");line(39,113,48,116,"leatherShade")
 shape({{41,117},{49,118},{48,123},{44,126},{31,126},{30,123},{35,120}},"leatherShade")
 poly({{38,120},{44,120},{44,123},{34,124},{33,123}},"leatherLight")
 shape({{32,122},{36,121},{39,123},{38,125},{31,125}},"ironShade");line(33,122,36,122,"ironLight")
 line(32,126,44,126,"ink")
end
local function rearCloth(p)
 shape({{47,80},{74,80},{83,91},{81,99},{74,96},{69,100},{56,97},{50,101},{42,96}},"leatherShade")
 poly({{46,85},{54,86},{51,96},{46,98},{44,94}},"leather")
 poly({{71,84},{76,85},{80,92},{75,94},{68,91}},"leather")
 line(45,91,49,87,"leatherLight")
end
local function torso(p)
 shape({{51,49},{67,48},{79,53},{83,63},{78,76},{74,86},{53,87},{45,76},{43,63}},"skinShade")
 poly({{49,54},{54,52},{57,57},{50,66},{45,68},{45,61}},"skin")
 -- Iron planes have deliberately connected clusters rather than noise.
 shape({{54,54},{64,56},{73,53},{79,59},{77,72},{70,82},{56,81},{49,71}},"ironShade")
 poly({{54,57},{61,59},{64,65},{57,75},{52,70}},"iron")
 poly({{54,58},{57,59},{59,62},{56,64},{53,62}},"ironLight")
 poly({{67,58},{73,56},{77,60},{74,69},{67,74},{64,67}},"iron")
 poly({{68,59},{73,57},{75,60},{72,62}},"ironLight")
 poly({{59,76},{65,72},{70,75},{70,79},{63,82},{57,79}},"ironDark")
 line(55,78,60,80,"ironLight");line(72,73,75,68,"ironDark")
 line(53,56,57,58,"ironHigh");pixel(54,58,"ironEdge")
 line(73,57,76,59,"ironHigh");line(50,69,54,75,"ironDark")
 line(64,77,68,75,"ironShade");pixel(61,73,"ironLight")
 -- Same diagonal strap, fixed hardware and deliberate leather edging.
 shape({{74,52},{79,55},{53,83},{48,79}},"leather")
 line(75,54,50,80,"leatherLight");line(77,56,53,81,"leatherShade")
 shape({{63,63},{67,59},{71,63},{67,68}},"leatherHigh")
 shape({{65,63},{67,61},{69,63},{67,66}},"leatherDark");pixel(67,60,"ironHigh")
 -- Secondary short shoulder strap, no new equipment.
 shape({{52,49},{57,52},{54,63},{49,61}},"leather")
 line(52,52,51,58,"leatherHigh");pixel(52,58,"ironHigh")
end
local function pauldron(p)
 shape({{76,53},{80,50},{88,52},{95,58},{96,63},{88,68},{78,64},{74,59}},"iron")
 poly({{78,54},{81,52},{87,54},{91,58},{84,60},{77,58}},"ironLight")
 line(80,52,86,53,"ironHigh");line(77,58,82,61,"ironShade")
 poly({{86,61},{94,59},{95,63},{88,66},{82,63}},"ironShade")
 line(83,64,88,66,"ironHigh");line(89,65,94,63,"ironLight")
 poly({{80,54},{83,54},{86,56},{84,57},{81,56}},"ironHigh")
 line(81,54,83,55,"ironEdge");line(88,56,91,58,"iron")
 line(85,61,89,59,"ironShade");pixel(91,61,"ironLight")
 shape({{82,52},{83,46},{87,53}},"ironLight");line(83,48,84,51,"ironEdge")
 shape({{91,56},{96,50},{95,59}},"ironLight");line(95,52,94,56,"ironEdge")
 shape({{77,59},{80,58},{83,61},{81,64},{78,63}},"ironShade")
 box(79,60,2,2,"ironHigh");pixel(80,62,"iron")
 pixel(89,58,"ironShade");pixel(89,57,"ironHigh")
end
local function fist(x,y,kind)
 -- A closed right/left hand with its own thumb and knuckle clusters.
 shape({{x-4,y-4},{x+1,y-5},{x+5,y-2},{x+5,y+2},{x+2,y+5},{x-3,y+4},{x-5,y+1}},"skin")
 poly({{x-3,y-3},{x+1,y-3},{x+3,y-1},{x,y+1},{x-3,y}},"skinLight")
 line(x-3,y+1,x,y+3,"skinShade");line(x+2,y-2,x+2,y+1,"skinShade")
 pixel(x-1,y-3,"skinHigh");pixel(x+4,y+1,"skinDark")
end
local function leftArm(p)
 if p.mode=="impact" or p.mode=="guard" or p.mode=="absorb" then
  shape({{85,63},{93,64},{94,73},{87,79},{75,78},{70,73},{74,67}},"skinShade")
  poly({{88,65},{91,66},{91,72},{87,74},{82,72}},"skin")
  shape({{77,68},{86,71},{88,77},{80,80},{73,77},{70,73}},"iron")
  poly({{76,70},{82,72},{84,75},{78,77},{74,74}},"ironLight")
  line(73,74,78,78,"ironHigh");line(82,78,86,76,"ironShade")
  fist(71,69)
 elseif p.mode=="flinch" then
  shape({{86,62},{94,62},{98,67},{99,72},{92,77},{85,71}},"skin")
  poly({{89,64},{93,64},{95,68},{90,70}},"skinLight")
  shape({{91,69},{98,68},{101,73},{97,79},{91,77},{88,73}},"iron")
  poly({{92,70},{97,70},{98,73},{94,75},{91,73}},"ironLight")
  line(92,76,97,77,"ironHigh");fist(99,69)
 else
  shape({{84,61},{92,63},{93,71},{90,79},{86,82},{80,78},{80,69}},"skinShade")
  poly({{85,65},{89,65},{90,70},{86,75},{83,72}},"skin")
  shape({{83,76},{91,78},{91,87},{87,91},{80,88},{79,82}},"iron")
  poly({{83,78},{88,80},{87,86},{82,86},{81,82}},"ironLight")
  line(81,87,87,89,"ironHigh");line(84,81,87,82,"ironShade")
  fist(84,93)
 end
 pauldron(p)
end
local function scarf(p)
 shape({{53,48},{58,49},{65,53},{74,49},{79,52},{74,59},{65,63},{56,59},{51,54}},"redShade")
 poly({{54,51},{61,54},{67,56},{74,53},{73,57},{65,60},{57,57}},"red")
 line(56,53,63,56,"redLight");line(64,56,70,55,"redLight")
 line(58,59,65,62,"redDark")
end
local function head(p)
 -- Bald mature bestial head, same right-facing design across every frame.
 shape({{61,27},{66,26},{71,27},{75,30},{76,34},{76,37},{79,39},{79,42},{77,44},{76,47},{71,49},{63,48},{59,45},{57,40},{57,34},{58,30}},"skin")
 poly({{60,30},{63,28},{67,28},{71,30},{69,32},{64,32},{60,35},{58,34}},"skinLight")
 poly({{63,28},{66,27},{69,29},{66,30},{63,30}},"skinHigh")
 poly({{72,29},{75,31},{75,35},{72,34},{70,32}},"skinShade")
 poly({{58,35},{61,36},{62,40},{61,44},{59,42}},"skinDark")
 -- Ear projects sideways, with a thick cartilage silhouette.
 shape({{58,35},{54,34},{52,33},{53,38},{56,40},{59,39}},"skinShade")
 poly({{54,35},{57,36},{57,38},{55,37}},"skinLight");line(54,36,56,37,"skinDark")
 -- Heavy asymmetric brow, two amber eyes, broad flattened nose.
 poly({{62,35},{65,34},{69,36},{68,38},{63,37}},"skinShade")
 line(62,35,67,36,"ink");line(63,36,66,37,"ink")
 pixel(66,37,"eye");pixel(65,37,"eyeHigh");pixel(67,37,"ink")
 poly({{71,34},{75,35},{76,37},{73,38},{71,37}},"skinDark")
 line(72,35,75,35,"ink");pixel(74,37,"eye")
 poly({{69,37},{71,39},{74,39},{77,41},{73,42},{69,41}},"skinLight")
 pixel(71,41,"skinDark");pixel(75,41,"skinDark");line(70,39,72,39,"skinHigh")
 poly({{61,40},{64,39},{67,42},{64,44},{61,43}},"skinLight")
 poly({{61,44},{65,45},{72,45},{77,43},{76,47},{72,49},{64,48}},"skinShade")
 poly({{65,46},{72,46},{75,45},{74,47},{70,48},{66,47}},"skin")
 line(64,43,75,43,"ink");line(66,44,73,44,"deep")
 line(61,40,62,42,"skinHigh");line(63,39,65,40,"skinShade")
 line(72,31,74,33,"skinDark");pixel(70,33,"skinShade")
 -- Two lower tusks are separated from the jaw outline.
 shape({{64,45},{65,40},{67,43},{67,46}},"ivory")
 line(65,42,65,44,"ivoryHigh");pixel(66,45,"ivoryShade")
 shape({{74,44},{76,40},{77,43},{76,45}},"ivory")
 pixel(76,42,"ivoryHigh")
 line(65,47,71,48,"skinLight");line(61,44,62,46,"skinDark")
end
local function belt(p)
 shape({{48,80},{59,82},{74,80},{79,84},{77,88},{62,90},{48,86},{45,83}},"leatherShade")
 line(48,81,58,83,"leatherLight");line(68,83,75,82,"leatherLight")
 shape({{56,81},{66,81},{68,88},{56,89},{54,86}},"iron")
 line(57,82,65,82,"ironHigh");line(56,83,56,87,"ironHigh")
 box(59,84,5,3,"leatherDark");line(61,85,65,85,"ironLight")
 -- Small side pouches retain fixed proportions, no random texture.
 shape({{72,86},{79,85},{81,92},{76,94},{71,92}},"leather")
 line(73,87,77,87,"leatherHigh");line(74,90,78,89,"leatherShade")
 shape({{47,86},{55,89},{52,97},{45,99},{42,96}},"leather")
 line(45,95,51,90,"leatherLight");line(46,98,51,96,"leatherShade")
 shape({{70,93},{77,92},{80,97},{73,99},{68,96}},"ironShade")
 line(71,94,76,93,"ironLight");line(72,97,77,97,"iron")
 -- Long burnt-red tabard, with asymmetric torn hem.
 local flow=p.flow or 0
 shape({{57,89},{67,89},{68+flow,103},{65+flow,109},{63+flow,106},{60+flow,110},{57+flow,104},{54,99}},"redShade")
 poly({{58,90},{61,91},{62+flow,102},{60+flow,105},{57+flow,100}},"red")
 poly({{63,91},{66,90},{66+flow,101},{64+flow,105}},"redDark")
 line(58,92,59,98,"redLight");pixel(59+flow,103,"redLight")
end
local function rightArm(p)
 local mode=p.mode
 if mode=="windup" then
  shape({{47,55},{42,54},{35,57},{31,63},{32,69},{38,72},{44,68},{49,62}},"skin")
  poly({{43,56},{46,57},{43,62},{38,65},{34,64},{36,60}},"skinLight")
  poly({{34,66},{39,67},{42,65},{41,69},{37,71}},"skinShade")
  shape({{32,66},{38,69},{38,76},{33,80},{27,76},{27,71}},"leather")
  line(29,69,35,72,"leatherLight");line(29,74,34,77,"leatherDark")
  fist(29,80)
 elseif mode=="impact" then
  shape({{49,55},{44,58},{44,63},{49,68},{59,69},{71,64},{87,64},{91,60},{87,55},{72,55},{62,58},{55,54}},"skin")
  poly({{49,57},{53,56},{60,60},{66,59},{72,57},{84,57},{86,60},{71,61},{59,65},{49,64}},"skinLight")
  poly({{50,65},{58,67},{69,63},{71,64},{59,69},{50,68}},"skinShade")
  poly({{48,59},{51,57},{55,58},{57,60},{55,63},{50,64},{47,62}},"skinLight")
  line(49,58,52,58,"skinHigh");line(54,64,58,63,"skinShade")
  line(59,62,63,61,"skin");line(68,61,75,60,"skin")
  line(52,66,57,67,"skinDark");line(77,62,83,62,"skinShade")
  line(48,59,48,62,"skinHigh");line(76,57,83,57,"skinHigh")
  shape({{85,55},{94,54},{96,57},{96,63},{87,65},{84,61}},"leather")
  line(87,56,92,55,"leatherHigh");line(87,63,94,62,"leatherShade")
  line(89,56,89,62,"leatherDark");line(93,56,94,61,"leatherDark")
  fist(100,59)
 elseif mode=="guard" then
  shape({{47,56},{42,58},{40,65},{43,73},{54,79},{66,76},{68,71},{62,66},{53,69},{50,61}},"skin")
  poly({{45,59},{47,59},{48,66},{53,71},{60,70},{62,73},{54,75},{45,70},{43,65}},"skinLight")
  line(45,69,51,73,"skinHigh")
  shape({{59,67},{65,66},{70,69},{71,74},{65,78},{60,75}},"leather")
  line(61,68,66,68,"leatherLight");line(62,75,67,75,"leatherDark")
  fist(72,69)
 elseif mode=="absorb" then
  shape({{47,57},{42,59},{40,65},{42,73},{49,78},{61,80},{68,76},{66,70},{59,70},{51,70},{50,62}},"skin")
  poly({{45,60},{47,60},{48,67},{54,72},{59,73},{58,76},{50,75},{44,71},{43,65}},"skinLight")
  shape({{57,71},{64,70},{68,73},{67,80},{60,81},{56,77}},"leather")
  line(58,73,63,72,"leatherHigh");line(59,78,64,79,"leatherDark");fist(69,76)
 elseif mode=="flinch" then
  shape({{47,56},{42,56},{38,61},{36,69},{30,72},{29,77},{35,81},{43,77},{47,69},{50,61}},"skin")
  poly({{43,58},{46,58},{46,64},{42,70},{37,74},{33,74},{37,68},{40,61}},"skinLight")
  shape({{29,72},{36,75},{36,81},{32,85},{26,81},{25,76}},"leather")
  line(27,75,32,78,"leatherLight");line(29,81,33,82,"leatherDark");fist(25,82)
 else
  shape({{47,55},{42,56},{38,61},{38,68},{34,75},{34,80},{40,84},{45,78},{48,70},{51,62}},"skin")
  poly({{43,58},{46,57},{48,61},{45,67},{42,70},{39,67},{40,62}},"skinLight")
  line(41,61,43,59,"skinHigh")
  poly({{43,63},{46,63},{45,66},{42,68},{40,67}},"skin")
  line(41,67,43,68,"skinShade");line(39,64,39,66,"skinHigh")
  line(43,72,42,75,"skinDark")
  poly({{39,70},{43,70},{43,75},{39,79},{36,78}},"skinShade")
  shape({{35,76},{43,79},{42,87},{37,90},{31,85},{32,80}},"leather")
  line(34,79,40,81,"leatherLight");line(33,84,39,87,"leatherDark")
  line(35,78,41,80,"leatherHigh");pixel(34,82,"ironLight")
  fist(34,92)
 end
end
local function renderPose(s,f,p)
 local ls=s.layers
 surface(s,ls[1],f,0,0,function()rearCloth(p)end)
 surface(s,ls[2],f,0,0,function()farLeg(p)end)
 surface(s,ls[3],f,0,0,function()nearLeg(p)end)
 surface(s,ls[4],f,p.dx,p.dy,function()torso(p)end)
 surface(s,ls[5],f,p.dx,p.dy,function()leftArm(p)end)
 surface(s,ls[6],f,p.dx,p.dy,function()scarf(p)end)
 surface(s,ls[7],f,p.hx or p.dx,p.hy or p.dy,function()head(p)end)
 surface(s,ls[8],f,0,0,function()belt(p)end)
 surface(s,ls[9],f,p.dx,p.dy,function()rightArm(p)end)
end
local specs={
 {id="concept",poses={{mode="neutral",dx=0,dy=0}},ms={100}},
 {id="attack",poses={{mode="neutral",dx=0,dy=0},{mode="windup",dx=-2,dy=1,flow=-1},{mode="impact",dx=3,dy=0,hx=2,hy=0,flow=-3},{mode="guard",dx=1,dy=1,flow=-1},{mode="neutral",dx=0,dy=0}},ms={80,110,50,90,120}},
 {id="hit",poses={{mode="flinch",dx=-2,dy=-1,hx=-3,hy=-2,flow=1},{mode="absorb",dx=-1,dy=3,hx=0,hy=4,flow=0},{mode="neutral",dx=0,dy=0}},ms={50,100,90}}
}
local result={author="Codex agent",method="Explicit pixel drawings via Aseprite Lua; no imported pixels",externalImageReads=0,canvas={128,128},palette=C,documents={}}
for _,spec in ipairs(specs)do
 local s=Sprite(128,128,ColorMode.RGB)
 s.layers[1].name=layers[1]
 for i=2,#layers do s:newLayer().name=layers[i]end
 for i=2,#spec.poses do s:newEmptyFrame()end
 local pal=Palette(#paletteNames+1);pal:setColor(0,Color{r=0,g=0,b=0,a=0})
 for i,k in ipairs(paletteNames)do pal:setColor(i,Color(rgba[k]))end
 s:setPalette(pal)
 app.transaction("Author Orc pixel clusters and poses",function()
  for i,p in ipairs(spec.poses)do renderPose(s,i,p);s.frames[i].duration=spec.ms[i]/1000 end
 end)
 local tag=s:newTag(1,#spec.poses);tag.name=spec.id=="concept" and "Concept-front-r" or spec.id.."-front-r"
 local filename=app.fs.joinPath(output,spec.id..".aseprite")
 s:saveAs(filename)
 -- All raster outputs rendered and saved by Aseprite itself.
 local dir=app.fs.joinPath(output,spec.id);app.fs.makeAllDirectories(dir)
 local frames={}
 for i=1,#spec.poses do
  local render=Image(128,128,ColorMode.RGB);render:clear();render:drawSprite(s,i)
  local name=string.format("%s_front_r_%02d.png",spec.id,i-1)
  render:saveAs(app.fs.joinPath(dir,name))
  table.insert(frames,{file=name,durationMs=spec.ms[i]})
 end
 local strip=Image(128*#spec.poses,128,ColorMode.RGB);strip:clear()
 for i=1,#spec.poses do local render=Image(128,128,ColorMode.RGB);render:clear();render:drawSprite(s,i);strip:drawImage(render,Point((i-1)*128,0))end
 strip:saveAs(app.fs.joinPath(dir,"native-strip.png"))
 table.insert(result.documents,{id=spec.id,file=filename,frames=frames,layers=layers,tag=tag.name})
 s:close()
end
local f=assert(io.open(app.fs.joinPath(output,"authorship.json"),"w"));f:write(json.encode(result));f:close()
print("Aseprite authored concept + Attack5 + Hit3; zero imported image pixels")
