"""Focused artifact and real-preview QA; technical results never grant artistic approval."""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
import json,hashlib,threading,base64,io,time
R=Path(__file__).resolve().parents[1];E=R/'experiments/main-orc-weapon-rescue-v3';B=R/'characters/orc-v1/source/onehanded-rescue-v3';L=R/'Biblioteca de Arte/Personagens Jogaveis/Orc V1';O=R/'reports/main-orc-weapon-rescue-v3';O.mkdir(parents=True,exist_ok=True)
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
im=lambda p:Image.open(p).convert('RGBA')
def equal(a,b):
 assert a.size==b.size
 for p,q in zip(a.getdata(),b.getdata()):assert p[3]==q[3] and (not p[3] or p[:3]==q[:3])
active=read(R/'reports/orc-production-current.json');assert active['characterId']=='orc-v1' and active['historicalV4StillDiscarded']
current=read(R/'characters/orc-v1/source/equipment-current.json');assert current['revision']=='main-orc-onehanded-v3' and not current['runtimeImplemented']
char=read(R/'characters/orc-v1/character.json');assert char['equipmentPreview']==current['manifest'] and not char['weaponPresentation']['armedIdle'] and not char['weaponPresentation']['armedWalk']
config=read(R/'config/equipment-actions-v1.json');assert config['oneHandedPresentation']['armedIdleWalkAllowed']==False
manifest=read(B/'manifest.json');assert manifest['profiles']=={'Sword':'basic.sword-slash','Axe':'basic.axe-chop'}
build=read(E/'build.json');assert build['summary']=={'jobs':10,'frames':77,'comparedFrames':77}
baseCount=0
for state in ['Idle','Walk']:
 c=read(B/state/'clip.json');source=read(R/f'characters/orc-v1/source/studies/{state}/clip.json');assert len(c['frames'])==len(source['frames'])
 if state=='Idle':assert [f['durationMs'] for f in c['frames']]==[400,450,500,450,400]
 for f,g in zip(c['frames'],source['frames']):
  a=im(R/f['png']);equal(a.crop((64,64,192,192)),im(R/g['png']));assert not f['weaponVisible'];assert a.getbbox()[0]>=64 and a.getbbox()[1]>=64 and a.getbbox()[2]<=192 and a.getbbox()[3]<=192;baseCount+=1
rest=im(R/read(B/'Idle/clip.json')['frames'][0]['png']);composed=0;reuseCount=0;stats={}
for category,wid in [('Sword','recruit-sword'),('Axe','militia-axe')]:
 c=read(B/category/'Attack/clip.json');profile=read(B/category/'Attack/profile.json');assert sha(R/c['master'])==c['masterSha256'];assert sha(R/c['bodyMaster'])==c['bodyMasterSha256'];assert sha(R/c['handMaster'])==c['handMasterSha256'];assert not c['loop'] and not c['runtimeImplemented'] and not c['contactEvent']['appliesDamage']
 n=len(c['frames']);strip=im(B/category/'Attack/native-strip.png');assert strip.size==(256*n,256);equal(im(R/c['frames'][0]['png']),rest);equal(im(R/c['frames'][-1]['png']),rest)
 visible=[i for i,f in enumerate(c['frames']) if f['weaponVisible']];assert visible==list(range(c['visibleInterval'][0],c['visibleInterval'][1]+1))
 for i,f in enumerate(c['frames']):
  assert sha(R/f['png'])==f['sha256'];layers={};result=Image.new('RGBA',(256,256))
  for name in c['layerOrder']:
   q=f['layers'][name];assert sha(R/q['png'])==q['sha256'];layers[name]=im(R/q['png']);result=Image.alpha_composite(result,layers[name])
  equal(result,im(R/f['png']));equal(result,strip.crop((256*i,0,256*(i+1),256)))
  weapon=Image.alpha_composite(layers['weaponBack'],layers['weaponFront']);body=layers['body'];hand=layers['handFront'];assert f['scale']==1
  assert f['layers']['body']==profile['frames'][i]['body'] and f['layers']['handFront']==profile['frames'][i]['handFront']
  if f['weaponVisible']:
   box=weapon.getbbox();assert box and min(box[:2])>0 and max(box[2:])<256;assert weapon.getpixel(tuple(f['rightGrip']))[3]>0;assert body.getpixel(tuple(f['rightGrip']))[3]>0,'Grip outside actual body/hand'
   overlap=sum(a[3]>0 and b[3]>0 for a,b in zip(weapon.getdata(),hand.getdata()));assert overlap>=3,f'No foreground fingers on handle {category} frame{i}'
  else:assert weapon.getbbox() is None and hand.getbbox() is None
  for a,b in zip(hand.getdata(),body.getdata()):
   if a[3]:assert a==b,'Generic/repainted hand instead of actual pose pixels'
  composed+=1
 w=read(R/f'assets/weapons/{wid}/weapon.json');assert w['category']==category and w['hands']==1 and w['ppu']==100;assert 'rescue-v3' in w['master'];assert sha(R/w['master'])==w['masterSha256'];bbox=im(R/w['sprite']).getbbox();height=bbox[3]-bbox[1];assert height==(72 if category=='Sword' else 47)
 alt=read(O/'reuse'/category/'reuse.json');assert alt['cloudCalls']==0 and alt['bodyRedraws']==0 and alt['item']['sprite']!=w['sprite'];assert len(alt['frames'])==n
 for i,f in enumerate(alt['frames']):
  original=c['frames'][i];assert f['retainedBodySha256']==original['layers']['body']['sha256'] and f['retainedHandSha256']==original['layers']['handFront']['sha256'];assert f['durationMs']==original['durationMs'] and f['grip']==original['rightGrip'];equal(im(O/'reuse'/category/'layers/body'/f'{i:02d}.png'),im(R/original['layers']['body']['png']));reuseCount+=1
 assert any(im(R/f['png']).tobytes()!=im(R/g['png']).tobytes() for f,g in zip(alt['frames'],c['frames']))
 stats[category]={'frames':n,'totalMs':sum(f['durationMs'] for f in c['frames']),'visibleInterval':c['visibleInterval'],'weaponHeightPx':height}
assert stats['Sword']['totalMs']!=stats['Axe']['totalMs']
inpaint=[]
for name,index in [('recovery',6),('strike',4)]:
 a=im(E/f'sword-posed/raw/{index:02d}.png');b=im(E/f'sword-{name}/raw/00.png');mask=im(E/f'sword-{name}-mask.png');outside=0
 for p,q,m in zip(a.getdata(),b.getdata(),mask.getdata()):
  if m[0]==0:assert p[3]==q[3] and (not p[3] or p[:3]==q[:3]);outside+=1
 inpaint.append({'region':name,'unmaskedVisibleRGBAIdentical':True,'protectedPixelCount':outside})
protected=read(E/'protected-art.json');changed=[p for p,h in protected.items() if sha(R/p)!=h];assert not changed,changed[:6]
catalog=read(L/'catalogo.json');assert catalog['revision']==current['revision'];assert all(sha(L/f['file'])==f['sha256'] for f in catalog['files'])
errors=[];viewed=0;timelines={}
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(channel='msedge',headless=True);page=browser.new_page(viewport={'width':1900,'height':1000});page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(f'http://127.0.0.1:{server.server_port}/Biblioteca%20de%20Arte/Personagens%20Jogaveis/Orc%20V1/index.html');page.wait_for_function('document.body.dataset.ready==="true"');page.wait_for_function('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)');page.click('#play');page.select_option('#mode','attack');assert page.locator('canvas').count()==8
  for i,c in enumerate(catalog['players']):
   for n,f in enumerate(c['frames']):
    page.evaluate('async a=>{views[a.i].n=a.n;await draw(a.i)}',{'i':i,'n':n});encoded=page.locator(f'#anim-{i}').evaluate('e=>e.toDataURL().split(",")[1]');equal(Image.open(io.BytesIO(base64.b64decode(encoded))).convert('RGBA'),im(L/f['png']));viewed+=1
  page.evaluate('async()=>{views.forEach((v,i)=>v.n=[0,7,5,4,5,5][i]);await Promise.all(data.map((_,i)=>draw(i)))}')
  page.screenshot(path=str(O/'review-all.png'),full_page=True)
  for i,article in enumerate(page.locator('article').all()):article.screenshot(path=str(O/f'review-panel-{i}.png'))
  for speed,wait in [('1',1700),('0.25',5700)]:
   page.select_option('#speed',speed);page.uncheck('#loop');page.click('#reset');page.evaluate('''()=>{window.playback=[];window.seen={};window.timer=setInterval(()=>{for(const i of [3,5]){const n=views[i].n;if(window.seen[i]!==n){window.seen[i]=n;window.playback.push({i,n,t:performance.now(),png:document.getElementById('anim-'+i).toDataURL().split(',')[1]})}}},10)}''');page.click('#play');page.wait_for_timeout(wait);page.click('#play');logs=page.evaluate('()=>{clearInterval(window.timer);return window.playback}')
   for i,category in [(3,'Sword'),(5,'Axe')]:
    sampled=[a for a in logs if a['i']==i];assert sorted(set(a['n'] for a in sampled))==list(range(len(catalog['players'][i]['frames'])))
    cell=300;sheet=Image.new('RGB',(cell*4,cell*((len(sampled)+3)//4)),(42,50,54));d=ImageDraw.Draw(sheet)
    for n,a in enumerate(sampled):
     actual=Image.open(io.BytesIO(base64.b64decode(a['png']))).convert('RGBA');expected=im(L/catalog['players'][i]['frames'][a['n']]['png']);equal(actual,expected);resized=actual.resize((288,288),Image.Resampling.NEAREST);x=(n%4)*cell;y=(n//4)*cell;sheet.paste(resized,(x,y+12),resized);d.text((x+3,y+1),str(a['n']),fill='white')
    sheet.save(O/f'{category.lower()}-playback-{speed}x.png')
   timelines[speed]=[{k:v for k,v in a.items() if k!='png'} for a in logs]
  page.select_option('#mode','sequence');page.select_option('#speed','1');page.click('#reset');page.click('#play');page.wait_for_timeout(5900);page.click('#play');assert page.evaluate('views[3].done&&views[5].done');assert 'sem arma' in page.locator('#info-3').inner_text() and 'sem arma' in page.locator('#info-5').inner_text()
  page.select_option('#zoom','1');page.set_viewport_size({'width':410,'height':900});assert not page.locator('body').evaluate('e=>e.scrollWidth>innerWidth+1');page.select_option('#bg','light');page.select_option('#bg','dark')
  page.goto((L/'index.html').as_uri());page.wait_for_function('document.body.dataset.ready==="true"');assert not errors;browser.close()
finally:server.shutdown();server.server_close()
(O/'playback-timelines.json').write_text(json.dumps(timelines,indent=2),encoding='utf-8')
report={'status':'TECHNICAL_PASS_ART_REVIEW_PENDING','mainOrc':'orc-v1','historicalV4Selected':False,'unarmedIdleWalkFramesExact':baseCount,'compositeLayerReconstructions':composed,'separateBodyItemHandMastersRoundtripFrames':77,'profiles':stats,'compatibleReplacementFramesBodyAndHandUnchanged':reuseCount,'newProductionWeaponsForReuseTest':0,'protectedArtFilesUnchanged':len(protected),'inpaint':inpaint,'viewerRGBAComparisons':viewed,'portableCopiedHashes':len(catalog['files']),'normalAndQuarterSpeedPlaybackSampled':True,'returnToActualUnarmedIdle':True,'noCanvasClippingOrScaling':True,'fileOpening':True,'mobileNoOverflow':True,'javascriptErrors':errors,'artisticApproval':'PENDING_CREATOR','independentArtisticReview':'NOT_PERFORMED; agent visual inspection and creator review only','unityModified':False,'limits':'Pixel/contact tests do not prove natural grip, convincing body mechanics or artistic acceptance.'};(O/'check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False))
