-- Five concept forks. All artistic pixels are authored inside Aseprite.
-- Inherited anatomy/pose: approved V4 concept (original image_gen ancestry).
-- New material ramps, armour construction, ornaments and marks: agent Lua artwork.
local root=assert(app.params.root)
local function file(p)return app.fs.joinPath(root,p)end
local base='characters/orc-01-art-lab-v5'
local input=app.open(file('characters/orc-01-aseprite-v4/source/aseprite/orc-art-lab-v5-baseline/source/concept-front-r.aseprite'))
local W,H=input.width,input.height
local reference=Image(W,H,ColorMode.RGB);reference:clear();reference:drawSprite(input,1);input:close()
local function rgba(h,a)return app.pixelColor.rgba(tonumber(h:sub(1,2),16),tonumber(h:sub(3,4),16),tonumber(h:sub(5,6),16),a or 255)end
local function palette(s)local p={};for h in s:gmatch('%x%x%x%x%x%x')do p[#p+1]=h end;return p end
local themes={
 {id='01-ferro-do-cla',title='Ferro do Clã',skin=palette('292d20 454d2c 64743b 82974b a8b664 c5cd85 e0d9a0'),metal=palette('1d2025 303640 46505b 606e77 839390 abb8ba d3d5c9'),cloth=palette('351d22 592329 7d2c30 a83d37 c85b45 e08259 eeb282'),leather=palette('241c1b 3c2923 5a3a29 795134 9d7048 be9462 d7b985')},
 {id='02-veterano-da-fronteira',title='Veterano da Fronteira',skin=palette('292b22 424a34 5f704b 809269 a2ac83 c3c6a0 ded6b4'),metal=palette('242626 343b3a 4c5551 67736a 879184 a9b0a0 cdd1be'),cloth=palette('232c25 354535 4d6041 6c7c50 8a9763 acb485 c9cba5'),leather=palette('28201c 443024 65462e 87623e a78857 c5ad7d dfcba2')},
 {id='03-bastiao-de-basalto',title='Bastião de Basalto',skin=palette('202e27 354b35 4c6943 698752 8ba86c b2bf88 d4d3aa'),metal=palette('181f2c 283449 3b4c61 526a7b 718d99 9ab3b7 c5d3cd'),cloth=palette('20232d 343c50 4d586d 68778a 8d9aab b4bfcb d7d9d3'),leather=palette('231e1d 39302a 534638 71604b 958267 b7a386 d6c5a7')},
 {id='04-campeao-do-ocre',title='Campeão do Ocre',skin=palette('30291f 50442a 74633b 99834b b8a363 d6bf84 ebd7a9'),metal=palette('2a2425 47372b 695035 8d6f44 b3955b d2b67d e9d5a7'),cloth=palette('39312d 615344 8a785b b3a17b d1c49a e6dbb8 f2e8ce'),leather=palette('291e1b 452921 693a29 925038 b5734c d49b70 eac5a0')},
 {id='05-ferro-de-campanha',title='Ferro de Campanha',skin=palette('282d22 414b2e 61713f 85964e a8b465 c7ce86 e0dba7'),metal=palette('262128 3f3435 604944 846153 a68169 c5a78b e1d0b1'),cloth=palette('1c2832 2e4151 445d70 617e8c 86a2a9 abc2bf d2d9ca'),leather=palette('251c1c 412a25 603d2d 865539 aa7850 cba071 e4c5a0')}
}
local function lum(r,g,b)return .24*r+.62*g+.14*b end
local function ramp(p,v,a)
 local q=math.max(0,math.min(#p-1,(v-18)/37));local n=math.min(#p-1,math.floor(q)+1);local f=q-(n-1)
 local a1,b1=rgba(p[n]),rgba(p[n+1]);local function ch(fn)return math.floor(fn(a1)*(1-f)+fn(b1)*f+.5)end
 return app.pixelColor.rgba(ch(app.pixelColor.rgbaR),ch(app.pixelColor.rgbaG),ch(app.pixelColor.rgbaB),a)
end
local reports={}
for idx,t in ipairs(themes)do
 local s=Sprite(W,H,ColorMode.RGB)
 local ref=s.layers[1];ref.name='00 V4 approved reference - inherited origin';ref.isVisible=false;s:newCel(ref,1,reference,Point(0,0))
 local inherited=Image(reference)
 -- Deliberate material ramps. No random noise, external raster tool or AI call.
 for y=0,H-1 do for x=0,W-1 do
  local p=reference:getPixel(x,y);local a=app.pixelColor.rgbaA(p)
  if a>0 then
   local r,g,b=app.pixelColor.rgbaR(p),app.pixelColor.rgbaG(p),app.pixelColor.rgbaB(p)
   local v=lum(r,g,b);local family=nil
   local skinArea=(y<319 and x>550 and x<772)or(y>285 and y<579 and x>375 and x<503)or(y>640 and y<779 and x<395)or(y>441 and y<576 and x>830)or(y>710 and y<797 and x>843 and x<931)
   if v>27 then
    if skinArea and g>r*.76 and r>b*1.17 and g>b*1.16 then family=t.skin
    elseif ((y>248 and y<380 and x>526 and x<752)or(y>612 and y<965 and x>550 and x<690))and r>g*1.65 and r>b*1.5 then family=t.cloth
    elseif r>g*1.19 and g>b*1.15 then family=t.leather
    elseif math.max(r,g,b)-math.min(r,g,b)<46 and not(y<276 and x>640 and x<760)then family=t.metal end
   end
   if family then inherited:drawPixel(x,y,ramp(family,v,a))end
  end
 end end
 -- Clear the previous shoulder armour so each design has its own silhouette.
 for y=216,450 do for x=711,978 do
  if (y<355 and x>727)or(y>=355 and x>765)then inherited:drawPixel(x,y,0)end
 end end
 local body=s:newLayer();body.name='10 Inherited anatomy - material direction';s:newCel(body,1,inherited,Point(0,0))
 local armour=s:newLayer();armour.name='20 New armour construction';local img=Image(W,H,ColorMode.RGB);img:clear()
 local ink='191b21'
 local function rect(x,y,w,h,c)
  for py=math.max(0,y),math.min(H-1,y+h-1)do for px=math.max(0,x),math.min(W-1,x+w-1)do img:drawPixel(px,py,rgba(c))end end
 end
 local function line(x1,y1,x2,y2,c,th)
  th=th or 3;local dx,dy=x2-x1,y2-y1;local n=math.max(math.abs(dx),math.abs(dy))
  for k=0,n do local f=n==0 and 0 or k/n;rect(math.floor(x1+dx*f-th/2),math.floor(y1+dy*f-th/2),th,th,c)end
 end
 local function poly(pts,c)
  local minY,maxY,minX,maxX=H,0,W,0;for _,p in ipairs(pts)do minY=math.min(minY,p[2]);maxY=math.max(maxY,p[2]);minX=math.min(minX,p[1]);maxX=math.max(maxX,p[1])end
  local metal=false;for j=2,6 do if c==t.metal[j]then metal=true end end
  local leather=false;for j=2,6 do if c==t.leather[j]then leather=true end end
  local cc=rgba(c);local cr,cg,cb=app.pixelColor.rgbaR(cc),app.pixelColor.rgbaG(cc),app.pixelColor.rgbaB(cc)
  for y=math.max(0,minY),math.min(H-1,maxY)do
   local cuts={};for j=1,#pts do local a,b=pts[j],pts[j%#pts+1]
    if(a[2]<=y and b[2]>y)or(b[2]<=y and a[2]>y)then cuts[#cuts+1]=a[1]+(y-a[2])*(b[1]-a[1])/(b[2]-a[2])end
   end
   table.sort(cuts);for j=1,#cuts-1,2 do
    for x=math.ceil(cuts[j]),math.floor(cuts[j+1])do
     if x>=0 and x<W then
      if metal or leather then
       local nx,ny=(x-minX)/math.max(1,maxX-minX),(y-minY)/math.max(1,maxY-minY)
       local source=reference:getPixel(815+math.floor(nx*85),302+math.floor(ny*58))
       local sv=lum(app.pixelColor.rgbaR(source),app.pixelColor.rgbaG(source),app.pixelColor.rgbaB(source))
       local d=22-26*nx-19*ny+(sv-110)*(metal and .14 or .09)
       local function ch(v)return math.max(0,math.min(255,math.floor(v+d)))end
       img:drawPixel(x,y,app.pixelColor.rgba(ch(cr),ch(cg),ch(cb),255))
      else img:drawPixel(x,y,cc)end
     end
    end
   end
  end
 end
 local function edge(pts,c,th)for j=1,#pts do local a,b=pts[j],pts[j%#pts+1];line(a[1],a[2],b[1],b[2],c,th)end end
 local function plate(pts,c)
  poly(pts,c);edge(pts,ink,5)
  for j=1,#pts do local a,b=pts[j],pts[j%#pts+1];local dx,dy=b[1]-a[1],b[2]-a[2]
   if dy<0 or(dx>0 and math.abs(dy)<math.abs(dx)*.65)then
    line(a[1]+4,a[2]+5,b[1]-2,b[2]+5,t.metal[5],3)
   end
  end
 end
 local function rivet(x,y,c)
  for dy=-6,6 do for dx=-6,6 do if dx*dx+dy*dy<=37 then
   local shade=dx+dy<-3 and t.metal[7]or(dx+dy<4 and(c or t.metal[5])or t.metal[2])
   img:drawPixel(x+dx,y+dy,rgba(shade))
  end end end
 end
 local function notch(x,y,c)
  line(x-17,y-14,x,y+6,c,6);line(x,y+6,x+17,y-14,c,6);line(x,y+6,x,y+30,c,6)
 end
 local function studs(pts)for _,p in ipairs(pts)do rivet(p[1],p[2])end end
 -- Scarf return and leather suspension remain visible under every pauldron.
 for y=216,324 do for x=712,782 do
  local p=reference:getPixel(x,y);local r,g,b=app.pixelColor.rgbaR(p),app.pixelColor.rgbaG(p),app.pixelColor.rgbaB(p)
  if app.pixelColor.rgbaA(p)>0 and r>g*1.5 and r>b*1.4 then img:drawPixel(x,y,ramp(t.cloth,lum(r,g,b),app.pixelColor.rgbaA(p)))end
 end end
 poly({{792,349},{926,370},{949,448},{923,462},{905,449},{889,475},{868,450},{850,468},{831,437},{808,447},{795,400}},t.leather[3])
 poly({{813,373},{917,394},{934,446},{917,440},{905,451},{893,434},{875,453},{857,434},{840,442}},t.leather[5])
 if idx==1 then
  -- Broad, asymmetrical forged shoulder; three broken ridges and a split-anvil mark.
  plate({{735,272},{776,226},{831,235},{877,272},{935,307},{965,389},{901,431},{809,408},{756,363}},t.metal[3])
  poly({{776,236},{830,246},{867,280},{830,317},{750,281}},t.metal[5])
  poly({{837,321},{882,282},{927,315},{951,385},{899,415}},t.metal[4])
  line(750,283,831,323,t.metal[6],7);line(831,323,897,416,t.metal[2],8)
  plate({{789,248},{785,201},{817,236}},t.metal[5]);plate({{856,269},{869,217},{884,283}},t.metal[4])
  plate({{910,311},{946,269},{935,346}},t.metal[4])
  plate({{821,411},{901,435},{960,400},{963,443},{901,467},{830,442}},t.metal[2])
  line(832,416,902,443,t.metal[5],5);line(902,443,956,410,t.metal[5],5)
  studs({{773,280},{812,389},{930,380},{854,435},{943,433}})
  notch(868,342,t.cloth[5]);notch(604,731,t.cloth[2]);notch(605,735,t.leather[6])
  -- Chest reinforcement follows the inherited diagonal strap rather than obscuring it.
  plate({{536,365},{570,379},{610,414},{586,444},{530,422},{518,392}},t.metal[3])
  poly({{538,372},{572,391},{586,411},{538,402}},t.metal[5]);rivet(541,393)
  line(559,647,558,814,t.cloth[5],5);line(636,651,647,865,t.cloth[2],5)
 elseif idx==2 then
  -- Low shoulder silhouette, overlapping lames, exposed mail and repaired leather.
  plate({{735,288},{772,247},{825,249},{878,281},{911,330},{901,374},{838,388},{779,364}},t.leather[4])
  plate({{751,283},{789,266},{827,275},{857,300},{827,327},{772,312}},t.metal[4])
  plate({{774,319},{828,334},{866,309},{893,342},{857,367},{794,351}},t.metal[3])
  plate({{796,357},{852,377},{894,351},{907,386},{865,409},{810,390}},t.metal[3])
  line(758,283,789,273,t.metal[6],5);line(780,323,826,339,t.metal[5],4);line(801,362,850,382,t.metal[5],4)
  studs({{769,297},{847,308},{808,345},{879,347},{822,384},{892,386}})
  -- Chain links are purposefully confined to two textile-sized panels.
  poly({{534,384},{575,399},{598,426},{567,455},{530,440}},t.metal[2])
  for row=0,5 do for col=0,5 do local x=538+col*8+(row%2)*3;local y=397+row*7
   if x<579 and y<435 then line(x,y,x+3,y+3,t.metal[5],2);line(x+3,y+3,x+6,y,t.metal[4],2)end
  end end
  poly({{472,700},{526,661},{537,706},{483,744}},t.metal[2])
  for row=0,5 do for col=0,4 do local x=483+col*9+(row%2)*3;local y=696+row*7;if x<527 then line(x,y,x+3,y+4,t.metal[5],2);line(x+3,y+4,x+6,y,t.metal[4],2)end end end
  -- Binding and repaired seams: a veteran's readable history, no uniform scratches.
  line(561,648,563,817,t.cloth[6],7);line(641,649,650,854,t.cloth[3],7)
  for k=0,6 do line(565+k*11,678,570+k*11,686,t.cloth[2],3)end
  poly({{579,730},{614,724},{624,765},{590,770}},t.cloth[3]);edge({{579,730},{614,724},{624,765},{590,770}},t.cloth[6],3)
  for k=0,3 do line(582+k*9,729,585+k*9,736,t.cloth[2],2)end
 elseif idx==3 then
  -- Architectural armour: broad planar cuts and one recessed jade inlay.
  plate({{731,279},{775,218},{844,225},{925,294},{951,382},{896,435},{811,415},{756,360}},t.metal[2])
  poly({{775,230},{839,237},{877,280},{834,322},{745,281}},t.metal[4])
  poly({{842,328},{884,286},{915,302},{938,377},{893,420}},t.metal[3])
  line(748,285,834,328,t.metal[6],7);line(834,328,893,421,t.metal[5],6)
  plate({{811,421},{895,443},{952,391},{969,418},{906,477},{824,448}},t.metal[2])
  line(829,436,902,461,t.metal[4],5);line(902,461,960,414,t.metal[4],5)
  plate({{850,323},{875,306},{905,355},{883,390}},t.metal[1])
  poly({{861,326},{873,320},{890,354},{881,373}},'7d9e8b');line(866,329,880,355,'b5c9b0',3)
  -- A tall embossed chest plate creates a different rhythm from a diagonal harness.
  plate({{538,366},{575,381},{620,420},{592,467},{539,449},{520,408}},t.metal[3])
  poly({{538,376},{568,392},{592,422},{573,445},{541,432}},t.metal[4]);line(540,379,542,430,t.metal[6],4)
  studs({{769,286},{817,399},{929,380},{840,440},{944,428}})
  line(577,654,583,846,t.cloth[5],6);line(606,656,619,879,t.cloth[3],6)
  poly({{582,721},{605,708},{626,748},{604,778}},t.metal[2]);poly({{589,725},{602,717},{616,748},{604,764}},'7d9e8b')
 elseif idx==4 then
  -- Bronze lamellae, a pale oath sash, circular hammered shoulder without spikes.
  plate({{734,285},{769,246},{822,236},{882,267},{923,325},{927,376},{880,418},{817,410},{764,368}},t.metal[3])
  poly({{770,255},{821,247},{866,270},{842,301},{761,297}},t.metal[5])
  poly({{850,304},{874,277},{910,329},{913,368},{881,400},{848,370}},t.metal[4])
  line(743,286,768,255,t.metal[7],6);line(768,255,820,246,t.metal[7],6)
  plate({{780,370},{820,392},{874,398},{921,370},{929,403},{884,436},{818,427},{793,407}},t.metal[3])
  line(804,398,819,416,t.metal[6],5);line(819,416,883,424,t.metal[6],5)
  -- Individual overlapping plates on the chest, independent of the inherited straps.
  for row=0,2 do for col=0,2 do local x=533+col*20+row*4;local y=375+row*22+col*12
   plate({{x,y},{x+20,y+9},{x+21,y+30},{x+8,y+33},{x,y+22}},t.metal[4]);line(x+4,y+7,x+16,y+12,t.metal[6],3)
  end end
  studs({{767,296},{813,382},{900,364},{838,413},{908,400}})
  -- Split chevron, original motif: no borrowed Horde symbol.
  line(845,310,858,335,t.cloth[6],8);line(858,335,880,325,t.cloth[6],8);line(851,325,856,352,t.cloth[6],8)
  line(568,653,573,829,t.leather[4],6);line(634,652,649,872,t.leather[4],6)
  notch(605,740,t.leather[4]);notch(606,779,t.leather[4])
 elseif idx==5 then
  -- Field repair: bolted plates have distinct joins and a replaced darker patch.
  plate({{738,283},{779,238},{837,249},{897,285},{933,349},{938,392},{875,425},{801,399},{758,360}},t.metal[3])
  poly({{782,251},{831,260},{874,289},{842,321},{753,285}},t.metal[5])
  plate({{844,318},{885,291},{923,347},{925,383},{878,410}},t.metal[4])
  plate({{784,304},{836,326},{855,375},{814,367},{775,333}},'374953')
  line(792,314,828,330,'78909a',5)
  plate({{808,407},{876,433},{936,402},{951,432},{887,464},{818,439}},t.metal[2])
  studs({{770,282},{831,283},{802,326},{833,358},{883,317},{912,376},{840,435},{927,432}})
  -- A functional harness brace replaces the polished central breast facet.
  plate({{539,372},{570,382},{593,407},{565,432},{533,413}},t.metal[3])
  line(542,378,569,391,t.metal[6],4);rivet(552,404)
  -- Repair patches and two large stitching runs, restrained to cloth/leather.
  poly({{580,708},{616,701},{627,758},{589,765}},t.cloth[3]);edge({{580,708},{616,701},{627,758},{589,765}},t.cloth[5],3)
  for k=0,5 do line(584,714+k*8,592,717+k*8,t.leather[6],3)end
  line(568,652,569,824,t.cloth[5],5);line(637,651,648,862,t.cloth[2],5)
  -- Three short hammered strikes form an original maker mark.
  for k=0,2 do line(874+k*9,353-k*5,881+k*9,367-k*5,t.metal[2],4)end
 end
 s:newCel(armour,1,img,Point(0,0))
 -- Limited, intentional face marks; layers remain editable independently.
 local face=s:newLayer();face.name='30 Identity accents - candidate';local accents=Image(W,H,ColorMode.RGB);accents:clear()
 local armourImage=img;img=accents
 if idx==1 then line(645,178,640,209,t.cloth[3],6);line(641,211,635,228,t.cloth[3],5)
 elseif idx==2 then line(638,140,649,166,t.skin[3],4);line(642,145,647,145,t.skin[6],3)
 elseif idx==3 then line(645,170,639,195,t.skin[2],6);line(646,171,640,196,t.skin[5],2)
 elseif idx==4 then line(630,168,623,199,t.cloth[5],9);line(645,169,639,197,t.cloth[5],7)
 elseif idx==5 then line(643,149,650,169,t.skin[3],5);line(649,171,650,183,t.skin[3],4)end
 s:newCel(face,1,accents,Point(0,0));img=armourImage
 local output=base..'/source/aseprite/'..t.id
 app.fs.makeAllDirectories(file(output))
 s:saveAs(file(output..'/concept.aseprite'))
 local result=Image(W,H,ColorMode.RGB);result:clear();result:drawSprite(s,1)
 result:saveAs(file(output..'/concept.png'))
 local changed=0;for y=0,H-1 do for x=0,W-1 do if result:getPixel(x,y)~=reference:getPixel(x,y)then changed=changed+1 end end end
 reports[#reports+1]={id=t.id,title=t.title,width=W,height=H,changedPixels=changed,source=output..'/concept.aseprite',png=output..'/concept.png',layers={'hidden inherited V4 reference','material direction','new armour construction','identity accents'},skin=t.skin,metal=t.metal,cloth=t.cloth,leather=t.leather}
 s:close();print(t.id..' saved')
end
local out=assert(io.open(file(base..'/source/art-lab-render.json'),'w'));out:write(json.encode(reports));out:close()
print('Five concept studies complete; creator review pending.')
