-- A single anatomical hand/grip hypothesis on F05 only. No propagation.
-- Source masters are the verified baseline copies. No R1/R2 or BFS masks.
local E="experiments/main-orc-targeted-repair-v1/artist-sword-sol"
local S="characters/orc-v1/source/targeted-repair-sword-sol-v1"
local function f(p)return app.fs.joinPath(app.fs.currentPath,p)end
local function blank(w,h)local im=Image(w,h,ColorMode.RGB);im:clear();return im end
local function inside(x,y,p)local yes=false;local j=#p;for i=1,#p do local a,b=p[i],p[j];if (a[2]>y)~=(b[2]>y) and x<(b[1]-a[1])*(y-a[2])/(b[2]-a[2])+a[1] then yes=not yes end;j=i end;return yes end
local function celImage(layer,i,w)
 local out=blank(w,w);local c=layer:cel(i);if c then out:drawImage(c.image,c.position) end;return out
end
local s=app.open(f(E.."/before/source/sword-attack-representative-v2.aseprite"))
assert(s.width==256 and s.height==256 and #s.frames==8 and #s.layers==4)
local layers={};for _,l in ipairs(s.layers)do layers[l.name]=l end
for _,n in ipairs({"weaponBack","body","weaponFront","handFront"})do assert(layers[n],"Missing original layer "..n)end
local originalBody=celImage(layers.body,6,256)
local body=Image(originalBody)
-- Distal hand/wrist seam traced from the actual source F05. Clear the old
-- broad palm, thumb bulb and its rim before drawing a closed gripping glove.
-- The steel forearm, elbow, pauldron and all pixels outside this hand polygon
-- stay from this exact frame. Coordinates here are composite256.
local oldHand={{177,120},{182,117},{187,119},{191,124},{190,132},{186,136},{174,136},{169,131},{168,125},{170,122},{174,124}}
for y=117,135 do for x=167,190 do if inside(x,y,oldHand) then body:drawPixel(x,y,0) end end end
-- Local leather palette sampled from the existing F05 glove, with factory ink.
local palette={
 I=app.pixelColor.rgba(12,15,18,255),
 D=originalBody:getPixel(178,125),
 M=originalBody:getPixel(180,127),
 L=originalBody:getPixel(176,126),
 H=originalBody:getPixel(176,128)
}
for k,p in pairs(palette)do assert(app.pixelColor.rgbaA(p)>0,"Palette must come from actual opaque glove: "..k)end
-- Explicit closed-hand contour and finger folds; not a radius or whole-body
-- intersection. Wrist neck joins the retained bracer at174,122; knuckles sit
-- right/below it. A shorter palm silhouette lets the pommel clear image-left.
local rows={
 {122,174,"IIDI"},
 {123,174,"IDMMDII"},
 {124,175,"IDMLMMDII"},
 {125,175,"IDMLLMMMMDI"},
 {126,176,"IDMLMMDDMDI"},
 {127,176,"IDMLMLMMDMDI"},
 {128,177,"IDLMLMMDDDI"},
 {129,177,"IDMLMMDMMDI"},
 {130,178,"IDMLMLMMDI"},
 {131,179,"IDMLMMDI"},
 {132,180,"IDMMDI"},
 {133,181,"IIII"}
}
for _,r in ipairs(rows)do for j=1,#r[3]do body:drawPixel(r[2]+j-1,r[1],palette[r[3]:sub(j,j)])end end
-- Actual finger/thumbnail contours on the near side of the hilt. These are
-- designed on the new leather glove, not copied from opaque armor next to it.
-- Guard/pommel remain in their own weapon layer and are not painted over.
local fingerGroups={
 {{179,126},{180,126},{180,127},{181,127}}, -- thumb curls down to the handle
 {{179,128},{180,128},{181,128}},          -- index finger over central leather
 {{180,129},{181,129},{182,129}},          -- middle finger
 {{182,130},{183,130},{184,130}},          -- ring/small finger curl
 {{183,131},{184,131}}
}
local hand=blank(256,256)
for gi,group in ipairs(fingerGroups)do for _,p in ipairs(group)do
 local col=(gi%2==0) and palette.L or palette.M
 body:drawPixel(p[1],p[2],col);hand:drawPixel(p[1],p[2],col)
end end
-- Seat the UNCHANGED independent sword eight pixels lower, into this closed
-- palm, keeping exact source rotation100deg/scale. Integer translation only.
-- Old pommel ~172,119 moves to~172,127 outside the smaller hand; guard remains
-- to image-right. No weapon art, blade highlight or shared asset is edited.
local oldWeapon=celImage(layers.weaponFront,6,256)
local weapon=blank(256,256);weapon:drawImage(oldWeapon,Point(0,8))
for name,img in pairs({body=body,weaponFront=weapon,handFront=hand})do
 local c=layers[name]:cel(6);c.image=img;c.position=Point(0,0)
end
app.fs.makeAllDirectories(f(S.."/source"))
s:saveAs(f(S.."/source/sword-f05-grip-composite.aseprite"));s:close()
-- Preserve actual body/native masters and edit just the corresponding F05.
local bs=app.open(f(E.."/before/source/sword-body-representative-v2.aseprite"));assert(#bs.layers==1)
local bc=bs.layers[1]:cel(6);bc.image=body;bc.position=Point(0,0)
bs:saveAs(f(S.."/source/sword-f05-grip-body.aseprite"));bs:close()
local ns=app.open(f(E.."/before/source/sword-body-representative-v2-back_r.aseprite"));assert(ns.width==128 and #ns.layers==1)
local native=blank(128,128);native:drawImage(body,Point(-64,-64));local nc=ns.layers[1]:cel(6);nc.image=native;nc.position=Point(0,0)
ns:saveAs(f(S.."/source/sword-f05-grip-native.aseprite"));ns:close()
local rec={}
for k,v in pairs(palette)do rec[k]={app.pixelColor.rgbaR(v),app.pixelColor.rgbaG(v),app.pixelColor.rgbaB(v),app.pixelColor.rgbaA(v)}end
local file=io.open(f(E.."/hand-authoring.json"),"w");file:write(json.encode({frame=5,oldHandPolygon=oldHand,palette=rec,rows=rows,fingerGroups=fingerGroups,swordTranslation={0,8},newGrip={181,129},rotationDeg=100,claim="Single-pose anatomical hypothesis; requires actual visual review"}));file:close()
print("Saved one F05 local closed-glove/palm hypothesis. All other frames/angles/timings unchanged. VISUAL_REVIEW_REQUIRED.")
