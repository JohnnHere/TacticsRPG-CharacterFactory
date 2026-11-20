-- Sole ART bounded F03 retraction proposal. No canonical writes.
-- All design coordinates are native128; source cels are rendered using their
-- actual cel.position. Only the F03 cel in copied forks is replaced.
local E="experiments/main-orc-targeted-repair-v1/artist-unarmed-sol"
local S="characters/orc-v1/source/targeted-repair-unarmed-sol-v1"
local function f(p)return app.fs.joinPath(app.fs.currentPath,p)end
local function blank(w,h)local im=Image(w,h,ColorMode.RGB);im:clear();return im end
local function pointIn(x,y,p)local yes=false;local j=#p;for i=1,#p do local a,b=p[i],p[j];if (a[2]>y)~=(b[2]>y) and x<(b[1]-a[1])*(y-a[2])/(b[2]-a[2])+a[1] then yes=not yes end;j=i end;return yes end
local function renderCel(s,i)
 local out=blank(s.width,s.height)
 -- The current source has one flattened body layer. Position is still applied
 -- explicitly, so later trimmed cels will not be treated as full canvases.
 assert(#s.layers==1,"Expected the actual current single body layer")
 local cel=s.layers[1]:cel(i);assert(cel,"Missing source cel")
 out:drawImage(cel.image,cel.position)
 return out
end
local nat=app.open(f(E.."/before/unarmed-back_l.aseprite"));assert(nat.width==128 and #nat.frames==5)
local impact=renderCel(nat,3)
local proposal=renderCel(nat,4)
-- Remove only the old distal cuff visible below the elbow. It lies outside
-- the torso/hip outline at these exact native coordinates; preserve the
-- chainmail upper arm and every head/torso/pauldron/leg/opposite-arm pixel.
local remove={{47,63},{49,61},{53,62},{55,65},{55,70},{53,74},{50,77},{47,75},{47,70}}
for y=60,77 do for x=45,56 do if pointIn(x,y,remove) then proposal:drawPixel(x,y,0) end end end
-- Same individual/view/action donor: F02 CLOSED gauntlet and forearm only.
-- Translate +24,+25: extended impact fist retracts towards the shoulder and
-- lowers gradually before unchanged F04. No crossfade, mirror or body warp.
local donor={{5,20},{8,18},{14,18},{20,19},{27,21},{31,25},{32,31},{29,35},{25,36},{19,33},{13,31},{8,29},{5,26}}
for y=17,36 do for x=4,32 do if pointIn(x,y,donor) then local p=impact:getPixel(x,y);if app.pixelColor.rgbaA(p)>0 then proposal:drawPixel(x+24,y+25,p) end end end end
-- Re-establish the elbow seam as short native clusters, reusing the existing
-- leather/ink shades of this same F03 sleeve, not a second arm or broad fill.
local ink=app.pixelColor.rgba(12,15,18,255)
local leather=app.pixelColor.rgba(60,30,29,255)
for _,p in ipairs({{52,59},{53,59},{53,60},{54,60},{54,61},{53,62},{52,63},{51,63},{50,63}})do proposal:drawPixel(p[1],p[2],ink)end
for _,p in ipairs({{52,60},{52,61},{53,61},{51,62},{52,62}})do proposal:drawPixel(p[1],p[2],leather)end
app.fs.makeAllDirectories(f(S.."/source"));app.fs.makeAllDirectories(f(S.."/native"));app.fs.makeAllDirectories(f(S.."/composite"))
-- Fork the actual native source: replace F03 only; no new production layers
-- are inferred from the original flattened body.
local nc=nat.layers[1]:cel(4);nc.image=proposal;nc.position=Point(0,0)
nat:saveAs(f(S.."/source/unarmed-back_l-f03-retraction-native.aseprite"));nat:close()
local comp=app.open(f(E.."/before/unarmed-attack.aseprite"));assert(comp.width==256 and #comp.frames==5 and #comp.layers==1)
local c=comp.layers[1]:cel(4);c.image=proposal;c.position=Point(64,64)
comp:saveAs(f(S.."/source/unarmed-back_l-f03-retraction-composite.aseprite"));comp:close()
-- Export by reopening the saved fork. Exported images are source-derived.
for _,spec in ipairs({{"native",128,"unarmed-back_l-f03-retraction-native.aseprite"},{"composite",256,"unarmed-back_l-f03-retraction-composite.aseprite"}})do
 local s=app.open(f(S.."/source/"..spec[3]));local strip=blank(spec[2]*5,spec[2])
 for i=1,5 do local im=renderCel(s,i);im:saveAs(f(S.."/"..spec[1].."/"..string.format("%02d.png",i-1)));strip:drawImage(im,Point((i-1)*spec[2],0)) end
 strip:saveAs(f(S.."/"..spec[1].."-strip.png"));s:close()
end
print("Saved exclusive F03 native/composite forks and reopened exports. F00/F01/F02/F04 untouched;450ms preserved. VISUAL_REVIEW_REQUIRED.")
