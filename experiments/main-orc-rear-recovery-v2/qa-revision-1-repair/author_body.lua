-- Scoped QA-01..04 repair, authored programmatically inside Aseprite.
-- ALL coordinates below are NATIVE 128; composite registration is +64,+64.
local E="experiments/main-orc-rear-recovery-v2"
local O=E.."/qa-revision-1-repair"
local function path(p)return app.fs.joinPath(app.fs.currentPath,p)end
local function blank(w,h)local im=Image(w,h,ColorMode.RGB);im:clear();return im end
local function load(p)return Image{fromFile=path(p)}end
local function native(p)local a=load(p);if a.width==128 then return a end;assert(a.width==256);local b=blank(128,128);b:drawImage(a,Point(-64,-64));return b end
local function inside(x,y,p)local yes=false;local j=#p;for i=1,#p do local a,b=p[i],p[j];if ((a[2]>y)~=(b[2]>y)) and x<(b[1]-a[1])*(y-a[2])/(b[2]-a[2])+a[1] then yes=not yes end;j=i end;return yes end
local function region(dst,src,p,dx,dy)
 for y=0,127 do for x=0,127 do if inside(x,y,p) then local sx,sy=x-(dx or 0),y-(dy or 0);local c=0;if sx>=0 and sx<128 and sy>=0 and sy<128 then c=src:getPixel(sx,sy) end;dst:drawPixel(x,y,c) end end end
end
local function bodies(d,a,v)local q={};for i=0,7 do q[i+1]=native("characters/orc-v1/source/rear-recovery-v2/"..d.."/"..a.."/"..v.."/layers/body/"..string.format("%02d.png",i)) end;return q end
local sl=bodies("back_l","Sword","Attack-representative-v1")
local ar=bodies("back_r","Axe","Attack-representative-v1")
local al=bodies("back_l","Axe","Attack-representative-v1")
local sr=bodies("back_r","Sword","Attack-representative-v2")
local bl=native("characters/orc-v1/source/complete-v1/back_l/Idle/00.png")
local br=native("characters/orc-v1/source/complete-v1/back_r/Idle/00.png")
-- QA-01: silhouette-shaped same-view static hanging gauntlet; includes the
-- forbidden diagonal blade outside the hand, rather than a rectangular paste.
local hanging={{82,52},{95,52},{103,59},{107,71},{108,91},{98,94},{85,88},{80,79},{82,68}}
for i=2,8 do region(sl[i],bl,hanging) end
-- F04 extra pale triangle OUTSIDE far pauldron. Keep its legitimate spikes.
region(sl[5],bl,{{91,28},{98,29},{105,33},{108,37},{108,43},{104,48},{94,48},{91,42}})
-- F05 generated blade crosses the attacking shoulder. First clear only the
-- traced blade/hilt silhouette, then rebuild the upper pauldron with its own
-- F04 same-view donor. The attacking forearm is retained below/left of seam.
local clear=blank(128,128)
region(sl[6],clear,{{22,20},{25,20},{27,24},{32,22},{39,19},{45,17},{51,17},{53,20},{49,25},{42,29},{35,32},{28,34},{25,31},{24,26}})
region(sl[6],sl[5],{{33,28},{38,23},{45,21},{51,22},{56,25},{58,30},{55,34},{48,35},{41,34},{35,33}},6,-3)
-- Six source pixels, individually inspected as detached leftovers, not a
-- generic small-component filter.
for _,p in ipairs({{101,5},{100,6},{101,6},{26,22},{26,21},{27,23}}) do sl[6]:drawPixel(p[1],p[2],0) end
-- QA-02 F01: axe-head is a crescent ABOVE the folded forearm, x90..109 y20..41.
-- Remove its actual contour and restore the gauntlet knuckle cap, without
-- bringing back the static hanging arm beneath the action.
region(ar[2],clear,{{89,18},{101,18},{114,25},{120,42},{121,66},{105,68},{92,57},{86,45},{88,32}})
-- Build the visible CLOSED empty cocked fist from this same-view F02 fist,
-- adapted to the cocked forearm. This is steel/gauntlet only, no source shaft.
local reach=Image(sr[2]);reach:drawImage(native("characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2/layers/handFront/01.png"),Point(0,0))
region(ar[2],reach,{{89,29},{97,29},{107,31},{117,38},{119,49},{116,58},{108,62},{98,59},{91,52},{86,43}})
-- Shafts above the actual knuckle caps. Pixel-row cutoffs derive from the
-- actual source fist top, not screen estimates. Retain the closed fist.
for x=83,102 do for y=0,4 do ar[3]:drawPixel(x,y,0) end end
for x=83,111 do for y=0,7 do ar[4]:drawPixel(x,y,0) end end
-- Rebuild the F03 knuckle cap after cutting the last wood stub. Round closed
-- steel/leather glove, sampled shades from the adjacent same-view gauntlet.
for y=7,11 do for x=98,108 do ar[4]:drawPixel(x,y,0) end end
local ink=app.pixelColor.rgba(12,15,18,255)
local glove=app.pixelColor.rgba(38,41,45,255)
local steel=app.pixelColor.rgba(66,69,72,255)
local cap={{9,101,104},{10,99,105},{11,98,106},{12,98,106}}
for _,r in ipairs(cap) do for x=r[2],r[3] do ar[4]:drawPixel(x,r[1],(x==r[2] or x==r[3] or r[1]==9) and ink or glove) end end
for x=100,103 do ar[4]:drawPixel(x,11,steel) end
-- QA-03: erase the COMPLETE obsolete distal arm before placing one continuous
-- same-view SwordR F05 upper-arm / elbow / forearm / empty closed-gauntlet chain.
-- handFront contains real glove fingers in the accepted source, merged here
-- into BODY so this checkpoint is genuinely whole and unarmed.
local donor=Image(sr[6]);donor:drawImage(native("characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2/layers/handFront/05.png"),Point(0,0))
local erase4={{88,32},{97,32},{108,42},{119,47},{120,68},{109,71},{99,64},{92,57},{87,51},{83,45}}
local erase5={{86,38},{96,39},{109,51},{116,62},{120,74},{113,82},{101,80},{94,70},{87,62},{82,54}}
region(ar[5],clear,erase4);region(ar[6],clear,erase5)
-- The static base includes a hanging arm here and must NOT be a transparency
-- donor. Clear the distal silhouette including the wrist dangling below it.
for y=46,83 do for x=86,127 do ar[5]:drawPixel(x,y,0);ar[6]:drawPixel(x,y,0) end end
local donor4={{86,36},{92,36},{102,40},{111,47},{120,53},{123,61},{120,67},{112,70},{105,65},{100,58},{91,55},{85,50},{82,45}}
region(ar[5],donor,donor4,0,-3)
local donor5={{86,40},{92,40},{102,44},{111,51},{120,57},{123,65},{120,71},{112,74},{105,69},{100,62},{91,59},{85,54},{82,49}}
region(ar[6],donor,donor5,0,1)
-- QA-04: bent light tip above far pauldron, actual x90..96 y19..26.
-- Keep its lower spike and the two normal adjacent spikes. No edits anywhere
-- near the successful raised fist or the earlier 27 removed old-arm pixels.
for _,i in ipairs({3,4}) do
 region(al[i],bl,{{88,17},{105,17},{106,21},{98,27},{93,27},{90,26},{88,24}})
end
local duration={90,80,90,80,100,80,100,110}
local function save(key,ims)
 for _,dim in ipairs({128,256}) do
  local s=Sprite(dim,dim,ColorMode.RGB);s.layers[1].name="body"
  for i=1,8 do if i>1 then s:newEmptyFrame() end;local b=blank(dim,dim);b:drawImage(ims[i],Point(dim==256 and 64 or 0,dim==256 and 64 or 0));s:newCel(s.layers[1],i,b,Point(0,0));s.frames[i].duration=duration[i]/1000 end
  s:newTag(1,8).name="Attack";app.fs.makeAllDirectories(path(O.."/checkpoint/source"));local master=O.."/checkpoint/source/"..key.."-body-"..dim..".aseprite";s:saveAs(path(master));s:close()
 end
 -- Reopen saved 256 master before deriving actual body and native images.
 local s=app.open(path(O.."/checkpoint/source/"..key.."-body-256.aseprite"));app.fs.makeAllDirectories(path(O.."/checkpoint/"..key.."/body"));app.fs.makeAllDirectories(path(O.."/checkpoint/"..key.."/native"))
 for i=1,8 do local b=blank(256,256);b:drawSprite(s,i);b:saveAs(path(O.."/checkpoint/"..key.."/body/"..string.format("%02d.png",i-1)));local n=blank(128,128);n:drawImage(b,Point(-64,-64));n:saveAs(path(O.."/checkpoint/"..key.."/native/"..string.format("%02d.png",i-1))) end;s:close();print("Saved/reopened/exported body-only "..key)
end
save("SwordL",sl);save("AxeR",ar);save("AxeL",al)
