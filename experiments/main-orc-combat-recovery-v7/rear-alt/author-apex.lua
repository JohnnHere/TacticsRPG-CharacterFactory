-- Local manual/programmatic Aseprite pose reconstruction. No generative call.
local root=app.fs.currentPath;local E='experiments/main-orc-combat-recovery-v7/rear-alt';local C='characters/orc-v1/source/combat-recovery-v7/rear-alt'
local function abs(p)return app.fs.joinPath(root,p)end
local function read(p)local f=assert(io.open(abs(p),'r'));local a=json.decode(f:read('*a'));f:close();return a end
local function blank(w,h)local im=Image(w,h,ColorMode.RGB);im:clear();return im end
local function load(p)return Image{fromFile=abs(p)}end
local function save(im,p)app.fs.makeAllDirectories(app.fs.filePath(abs(p)));im:saveAs(abs(p))end
local pc=app.pixelColor;local function rgb(r,g,b)return pc.rgba(r,g,b,255)end
local ink=rgb(12,15,18)
local plan=read(E..'/joint-plan.json');local p=plan.apex
local orig256=load(p.base);local donor256=load(p.donor);local body=blank(128,128);body:drawImage(orig256,Point(-64,-64));local donor=blank(128,128);donor:drawImage(donor256,Point(-64,-64))
local original=Image(body)
local function inside(x,y,poly)local yes=false;local j=#poly;for i=1,#poly do local a,b=poly[i],poly[j];if (a[2]>y)~=(b[2]>y) and x<(b[1]-a[1])*(y-a[2])/(b[2]-a[2])+a[1]then yes=not yes end;j=i end;return yes end
local function polygon(im,poly,color)
 for y=0,127 do for x=0,127 do if inside(x+.5,y+.5,poly)then im:drawPixel(x,y,color)end end end
end
local function line(im,x0,y0,x1,y1,c)
 local dx,dy=math.abs(x1-x0),-math.abs(y1-y0);local sx=x0<x1 and 1 or -1;local sy=y0<y1 and 1 or -1;local er=dx+dy
 while true do im:drawPixel(x0,y0,c);if x0==x1 and y0==y1 then break end;local e2=2*er;if e2>=dy then er=er+dy;x0=x0+sx end;if e2<=dx then er=er+dx;y0=y0+sy end end
end
-- Reconstruct only the arm envelope, not torso/legs. Remove complete old arm
-- beyond the shoulder; no donor behind an uncleared recipient.
for y=10,51 do for x=86,127 do if x>=92 or(y>=43 and x>=86)then body:drawPixel(x,y,0)end end end
-- Sample nearest source colors, preserving inherited material palette.
local function nearest(r,g,b)
 local best,dist=ink,1e9
 for y=11,50 do for x=82,104 do local c=donor:getPixel(x,y);if pc.rgbaA(c)>0 then local d=(pc.rgbaR(c)-r)^2+(pc.rgbaG(c)-g)^2+(pc.rgbaB(c)-b)^2;if d<dist then best,dist=c,d end end end end
 return best
end
local dark=nearest(24,26,30);local steel=nearest(55,61,65);local lit=nearest(83,89,92);local burgundy=nearest(62,30,35);local redlight=nearest(82,40,43)
-- Newly drawn humerus: outward upper arm in perspective, not stretching the
-- short generated donor upper arm. Dark rounded silhouette with sleeve/links.
local upper={{86,34},{91,31},{103,31},{111,33},{115,37},{114,42},{108,46},{98,46},{91,44},{86,40}}
polygon(body,upper,ink)
local sleeve={{89,35},{94,33},{104,33},{111,35},{113,38},{111,42},{107,44},{99,44},{93,42},{89,39}}
polygon(body,sleeve,burgundy)
local mesh={{96,34},{103,33},{110,35},{112,38},{110,42},{106,44},{100,43},{96,41}}
polygon(body,mesh,dark)
for y=33,44 do for x=95,113 do if inside(x+.5,y+.5,mesh)then
 local u,v=x%3,y%3;local c=dark
 if(u==0 and v==0)or(u==1 and v==1)then c=steel elseif u==1 and v==0 then c=lit end
 body:drawPixel(x,y,c)
end end end
line(body,92,34,95,41,redlight);line(body,94,34,97,41,dark)
-- Elbow cap visible on the outside, rounded rather than a duplicate hand.
polygon(body,{{107,34},{111,33},{115,36},{116,39},{113,43},{110,43},{107,40}},ink)
polygon(body,{{109,35},{112,35},{114,37},{114,40},{112,41},{110,40}},steel)
line(body,110,35,113,37,lit)
-- Precisely traced same-view donor: 1:1 forearm+glove, translation only.
local rows={{11,87,94},{12,85,95},{13,84,96},{14,83,96},{15,82,97}}
for y=16,20 do rows[#rows+1]={y,82,98}end
for y=21,24 do rows[#rows+1]={y,84,99}end
rows[#rows+1]={25,91,99};rows[#rows+1]={26,92,100}
for y=27,30 do rows[#rows+1]={y,92,101}end
for y=31,33 do rows[#rows+1]={y,94,103}end
for y=34,36 do rows[#rows+1]={y,95,103}end
for y=37,39 do rows[#rows+1]={y,95,101}end
local donorMask=blank(128,128);local copied=0
for _,r in ipairs(rows)do for x=r[2],r[3]do local c=donor:getPixel(x,r[1]);if pc.rgbaA(c)>0 then local xx,yy=x+12,r[1]+2;body:drawPixel(xx,yy,c);donorMask:drawPixel(xx,yy,c);copied=copied+1 end end end
-- Dark clean exterior donor pixels only (not global luminance filtering).
-- Contiguous bracer/glove retained; tiny exposed gray tips on transplanted seam
-- are inked with actual silhouette knowledge.
for _,xy in ipairs({{106,15},{108,16},{110,18},{110,19},{111,22},{111,23}})do
 local x,y=xy[1],xy[2];if pc.rgbaA(body:getPixel(x,y))>0 then body:drawPixel(x,y,dark)end
end
local hfNative=blank(128,128)
for _,r in ipairs(rows)do if r[1]<=24 then for x=r[2],r[3]do local xx,yy=x+12,r[1]+2;local c=body:getPixel(xx,yy);if pc.rgbaA(c)>0 then hfNative:drawPixel(xx,yy,c)end end end end
-- Closed glove is donor-authentic; reinforce two existing leather fold pixels
-- rather than fabricate a new detached hand or hide the guard.
local gx,gy=p.grip[1],p.grip[2]
local def=read('characters/orc-v1/source/combat-rescue-v5/combat/weapons/Sword/weapon.json');local ws=app.open(abs(def.master));local wi=blank(96,96);wi:drawSprite(ws,1);ws:close()
local wb,wf,hf,b256=blank(256,256),blank(256,256),blank(256,256),blank(256,256);b256:drawImage(body,Point(64,64));hf:drawImage(hfNative,Point(64,64))
local rad=p.weaponAngleDeg*math.pi/180;local ca,sa=math.cos(rad),math.sin(rad)
for y=0,255 do for x=0,255 do local dx,dy=x-gx-64,y-gy-64;local u=math.floor(ca*dx+sa*dy+def.grip[1]+.5);local v=math.floor(-sa*dx+ca*dy+def.grip[2]+.5)
 if u>=0 and u<96 and v>=0 and v<96 then local c=wi:getPixel(u,v);if pc.rgbaA(c)>0 then
  -- hilt behind hand; guard/blade and disk pommel independently legible.
  local target=(v>=60 and v<=70)and wb or wf;target:drawPixel(x,y,c)
 end end
end end
local dst=C..'/apex';local names={'weaponBack','body','weaponFront','handFront'};local ims={wb,b256,wf,hf}
app.fs.makeAllDirectories(abs(dst..'/source'));local sp=Sprite(256,256,ColorMode.RGB)
for j,n in ipairs(names)do local l=j==1 and sp.layers[1]or sp:newLayer();l.name=n;sp:newCel(l,1,ims[j],Point(0,0))end
sp.frames[1].duration=p.durationMs/1000;sp:saveAs(abs(dst..'/source/composite.aseprite'));sp:close()
local ns=Sprite(128,128,ColorMode.RGB);ns.layers[1].name='body';ns:newCel(ns.layers[1],1,body,Point(0,0));ns.frames[1].duration=p.durationMs/1000;ns:saveAs(abs(dst..'/source/native.aseprite'));ns:close()
local function eq(a,b)for y=0,a.height-1 do for x=0,a.width-1 do local u,v=a:getPixel(x,y),b:getPixel(x,y);assert(u==v or(pc.rgbaA(u)==0 and pc.rgbaA(v)==0),'pixel mismatch')end end end
sp=app.open(abs(dst..'/source/composite.aseprite'));ns=app.open(abs(dst..'/source/native.aseprite'));assert(math.abs(sp.frames[1].duration*1000-p.durationMs)<.1);assert(math.abs(ns.frames[1].duration*1000-p.durationMs)<.1)
for j,l in ipairs(sp.layers)do local c=l:cel(1);local im=blank(256,256);if c then im:drawImage(c.image,c.position)end;eq(im,ims[j]);save(im,dst..'/layers/'..l.name..'.png')end
local composed=blank(256,256);composed:drawSprite(sp,1);save(composed,dst..'/composite.png');local ni=blank(128,128);ni:drawSprite(ns,1);eq(ni,body);save(ni,dst..'/native.png');save(donorMask,dst..'/donor-mask.png');sp:close();ns:close()
-- Enlargements and a real source comparison, all raster operations in Aseprite.
for _,which in ipairs({'before','after','body-only'})do
 local im=which=='before'and load('characters/orc-v1/source/artistic-reconstruction-v6/rear/back_l-sword/frames/04.png')or(which=='after'and composed or b256)
 local crop=blank(96,96);crop:drawImage(im,Point(-96,-64));crop:resize(768,768);save(crop,E..'/apex-'..which..'-arm-head.png')
 local full=Image(im);full:resize(768,768);save(full,E..'/apex-'..which..'-full.png')
end
-- Measured-joint overlay is separate evidence, never in master art.
local annotated=Image(b256);local points={{88,39},{111,37},{105,25},{100,19}}
for i,q in ipairs(points)do local x,y=q[1]+64,q[2]+64;local c=i==1 and rgb(255,190,60)or(i==2 and rgb(80,210,255)or rgb(230,100,210));for d=-2,2 do annotated:drawPixel(x+d,y,c);annotated:drawPixel(x,y+d,c)end end
line(annotated,152,103,175,101,rgb(255,190,60));line(annotated,175,101,169,89,rgb(80,210,255))
local crop=blank(96,96);crop:drawImage(annotated,Point(-96,-64));crop:resize(768,768);save(crop,E..'/apex-joints-overlay.png')
local f=assert(io.open(abs(E..'/author-result.json'),'w'));f:write(json.encode({pose='apex',donorPixelsCopied=copied,donorRows=rows,mastersSavedReopened=true,rgbaAndDurationVerified=true,generationCalls=0,joints=p.joints}));f:close()

