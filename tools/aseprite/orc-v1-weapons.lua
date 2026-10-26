-- Original weapon pixel art authored programmatically inside Aseprite.
local root=assert(app.params.root);local function file(p)return app.fs.joinPath(root,p)end
local pc=app.pixelColor
local function rgb(r,g,b)return pc.rgba(r,g,b,255)end
local C={ink=rgb(16,18,21),dark=rgb(39,43,47),steel=rgb(83,91,96),mid=rgb(119,129,131),light=rgb(165,177,177),edge=rgb(205,211,199),woodDark=rgb(51,30,20),wood=rgb(100,60,34),woodMid=rgb(128,80,43),woodLight=rgb(160,104,59),leather=rgb(111,67,34),stitch=rgb(178,128,74)}
local function line(im,x0,y0,x1,y1,c)
 local dx=math.abs(x1-x0);local sx=x0<x1 and 1 or -1;local dy=-math.abs(y1-y0);local sy=y0<y1 and 1 or -1;local e=dx+dy
 while true do if x0>=0 and x0<im.width and y0>=0 and y0<im.height then im:drawPixel(x0,y0,c)end;if x0==x1 and y0==y1 then break end;local v=2*e;if v>=dy then e=e+dy;x0=x0+sx end;if v<=dx then e=e+dx;y0=y0+sy end end
end
local function polygon(im,pts,color)
 local minX,maxX,minY,maxY=64,0,64,0;for _,p in ipairs(pts)do minX=math.min(minX,p[1]);maxX=math.max(maxX,p[1]);minY=math.min(minY,p[2]);maxY=math.max(maxY,p[2])end
 for y=minY,maxY do for x=minX,maxX do local inside=false;local j=#pts
  for i=1,#pts do local a,b=pts[i],pts[j];if(a[2]>y)~=(b[2]>y)and x<(b[1]-a[1])*(y-a[2])/(b[2]-a[2])+a[1]then inside=not inside end;j=i end
  if inside then im:drawPixel(x,y,color)end
 end end
 for i,p in ipairs(pts)do local q=pts[i%#pts+1];line(im,p[1],p[2],q[1],q[2],color)end
end
local function ellipse(im,cx,cy,rx,ry,color)for y=cy-ry,cy+ry do for x=cx-rx,cx+rx do if((x-cx)/rx)^2+((y-cy)/ry)^2<=1 then im:drawPixel(x,y,color)end end end end
local function save(id,metal,handle,grip)
 local out='assets/weapons/'..id;app.fs.makeAllDirectories(file(out..'/source'));app.fs.makeAllDirectories(file(out..'/sprites'))
 local s=Sprite(64,64,ColorMode.RGB);s.layers[1].name='Wood and leather';s:newCel(s.layers[1],1,handle,Point(0,0));local l=s:newLayer();l.name='Forged steel';s:newCel(l,1,metal,Point(0,0));s:saveAs(file(out..'/source/'..id..'.aseprite'))
 local flat=Image(64,64,ColorMode.RGB);flat:clear();flat:drawSprite(s,1);flat:saveAs(file(out..'/sprites/'..id..'.png'));s:close()
end
-- Straight recruit sword: pointed fuller blade, plain crossguard, stitched leather and disk pommel.
local m=Image(64,64,ColorMode.RGB);local h=Image(64,64,ColorMode.RGB);m:clear();h:clear()
polygon(m,{{32,2},{35,10},{36,42},{28,42},{29,10}},C.ink)
polygon(m,{{32,4},{34,11},{35,41},{29,41},{30,11}},C.steel)
polygon(m,{{32,5},{33,12},{33,40},{30,40},{31,12}},C.mid)
line(m,32,8,32,40,C.dark);line(m,33,10,34,40,C.light);line(m,30,11,29,39,C.edge)
line(m,31,6,32,4,C.edge);line(m,34,17,35,16,C.dark);line(m,29,31,30,30,C.steel)
polygon(m,{{23,42},{25,41},{40,41},{42,42},{41,45},{23,45}},C.ink)
line(m,24,42,40,42,C.light);line(m,24,43,40,43,C.mid);line(m,25,44,40,44,C.steel)
polygon(h,{{30,45},{34,45},{35,55},{33,58},{29,56}},C.ink)
polygon(h,{{31,45},{33,45},{34,55},{32,57},{30,55}},C.leather)
for y=46,54,4 do line(h,30,y,33,y+2,C.stitch);line(h,31,y+2,34,y+4,C.woodDark)end
ellipse(m,32,59,4,3,C.ink);ellipse(m,32,58,3,2,C.steel);line(m,30,57,33,56,C.light);m:drawPixel(32,58,C.edge);line(m,33,60,35,59,C.dark)
save('recruit-sword',m,h,{32,50})
-- Militia axe: curved ash haft, single bearded iron head and visible wedge/rivet.
m=Image(64,64,ColorMode.RGB);h=Image(64,64,ColorMode.RGB);m:clear();h:clear()
polygon(h,{{27,13},{31,12},{32,25},{30,35},{32,47},{36,57},{35,61},{31,61},{28,51},{26,37},{28,24}},C.ink)
polygon(h,{{28,14},{30,14},{31,25},{29,35},{31,47},{35,57},{34,60},{32,59},{29,50},{27,37},{29,24}},C.wood)
line(h,29,17,30,25,C.woodLight);line(h,30,26,28,35,C.woodMid);line(h,28,36,30,47,C.woodLight);line(h,31,49,34,58,C.woodMid)
line(h,30,20,29,24,C.woodDark);line(h,28,39,30,43,C.woodDark);line(h,30,50,32,52,C.woodDark)
polygon(m,{{23,11},{29,9},{35,12},{42,12},{49,8},{50,15},{50,24},{47,31},{41,28},{35,22},{28,22},{22,20}},C.ink)
polygon(m,{{24,12},{29,11},{35,14},{42,14},{48,11},{49,17},{48,25},{46,29},{41,26},{35,20},{28,20},{24,19}},C.steel)
polygon(m,{{27,12},{35,15},{42,15},{47,13},{48,18},{45,22},{38,20},{33,18},{27,18}},C.mid)
polygon(m,{{48,11},{49,17},{48,25},{46,29},{44,28},{46,22},{47,16}},C.light)
line(m,49,16,48,24,C.edge);line(m,48,24,46,28,C.edge);line(m,24,12,29,11,C.light)
line(m,30,19,35,20,C.dark);line(m,39,17,42,16,C.steel);line(m,45,25,46,24,C.dark)
ellipse(m,28,16,2,2,C.dark);m:drawPixel(27,15,C.edge);m:drawPixel(28,16,C.light)
save('militia-axe',m,h,{32,49})
