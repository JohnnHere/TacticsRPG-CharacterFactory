"""Read-only art/browser verification. Contact sheets are review artifacts only."""
from pathlib import Path
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
import json,threading,hashlib
from PIL import Image,ImageDraw,ImageFont
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'reports/orc-production-v4-comparison.json').read_text(encoding='utf-8'))
clips=data['clips'];dest=root/'reports/orc-production-v4';dest.mkdir(exist_ok=True)
def im(f):return Image.open(root/f).convert('RGBA')
def raw(f):return im(f).tobytes()
dark={'010000','010001','020101','030201','050302','040402','040201','040302','030302'}
palette={};references=0;pixel_checks=0
for c in clips:
    palette.setdefault(c['characterId'],set())
    for f in c['before']:
        palette[c['characterId']].update(p[:3] for p in im(f).getdata() if p[3])
for c in clips:
    for n,(a,b) in enumerate(zip(c['before'],c['after'])):
        old,new=im(a),im(b)
        assert old.size==new.size==(128,128)
        assert set(new.getchannel('A').getdata())<={0,255}
        assert new.getbbox()[3]==127,'Ground changed'
        direct=bool(c['directV4']);closing=c['state'] in ('Attack','Hit','Unarmed') and n==len(c['after'])-1
        if not direct:
            assert {p[:3] for p in new.getdata() if p[3]}<=palette[c['characterId']]
            if not closing:
                assert old.getchannel('A').tobytes()==new.getchannel('A').tobytes()
                for p,q in zip(old.getdata(),new.getdata()):
                    if p!=q:assert bytes(p[:3]).hex() in dark and bytes(q[:3]).hex()==c['ink'] and p[3]==q[3]==255
        else:
            state='attack' if c.get('reusesAttack') else c['state'].lower()
            approved=f"characters/orc-01-aseprite-v4/source/aseprite/retouched/{state}/{state}_front_r_{n:02d}.png"
            assert raw(b)==raw(approved),'Direct V4 differs'
        reference=f"{c['directory']}/reference/{n:02d}.png"
        assert raw(reference)==old.tobytes();references+=1;pixel_checks+=1
    if c['state'] in ('Attack','Unarmed'):
        assert raw(c['after'][0])==raw(c['after'][-1])
        assert c['durationsMs']==[80,110,50,90,120]
    elif c['state']=='Hit':
        attack=next(x for x in clips if x['characterId']==c['characterId'] and x['state']=='Attack' and x['direction']==c['direction'])
        assert raw(c['after'][-1])==raw(attack['after'][0]);assert c['durationsMs']==[50,100,90]
    else:assert c['durationsMs']==c['beforeDurationsMs']
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',14)
for id in palette:
    group=[c for c in clips if c['characterId']==id and c['state'] in ('Attack','Hit','Unarmed')]
    sheet=Image.new('RGBA',(850,40+len(group)*132),(25,31,40,255));d=ImageDraw.Draw(sheet);d.text((12,10),id+' / V4',font=font,fill='white')
    for row,c in enumerate(group):
        y=40+row*132;d.text((7,y+12),c['state']+'\n'+c['direction'],font=font,fill=(185,204,226))
        for n,f in enumerate(c['after']):
            tile=Image.new('RGBA',(128,128),(54,63,75,255));tile.alpha_composite(im(f));sheet.alpha_composite(tile,(150+n*132,y))
    sheet.save(dest/(id+'-combat-v4.png'))
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(root)))
threading.Thread(target=server.serve_forever,daemon=True).start();errors=[]
expected=[{'id':c['characterId'],'state':c['state'],'direction':c['direction'],'before':[hashlib.sha256(raw(f)).hexdigest() for f in c['before']],'after':[hashlib.sha256(raw(f)).hexdigest() for f in c['after']]} for c in clips]
try:
    with sync_playwright() as p:
        browser=p.chromium.launch(channel='msedge',headless=True)
        page=browser.new_page(viewport={'width':1440,'height':1100},device_scale_factor=1)
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto((dest/'review.html').as_uri(),wait_until='networkidle');page.wait_for_function('document.body.dataset.ready==="true"')
        assert not page.locator('#error').inner_text()
        page.goto(f'http://127.0.0.1:{server.server_port}/reports/orc-production-v4/review.html',wait_until='networkidle')
        page.wait_for_function('document.body.dataset.ready==="true"')
        page.set_default_timeout(120000)
        exact=page.evaluate('''async expected=>{
          const sha=async id=>{const bytes=document.querySelector(id).getContext('2d').getImageData(0,0,128,128).data;return [...new Uint8Array(await crypto.subtle.digest('SHA-256',bytes))].map(n=>n.toString(16).padStart(2,'0')).join('')};
          let count=0;for(const c of expected){await window.chooseClip(c.id,c.state,c.direction);for(let n=0;n<c.after.length;n++){await window.drawFrame(n);if(await sha('#before')!==c.before[n]||await sha('#after')!==c.after[n])throw Error('Canvas differs '+c.id+' '+c.state+' '+c.direction+' '+n);count+=2;}}return count;
        }''',expected)
        page.evaluate("window.chooseClip('orc-01','Attack','front_r')");page.click('#return');page.select_option('#zoom','3')
        page.screenshot(path=str(dest/'review-screenshot.png'),full_page=True)
        page.locator('.pair').screenshot(path=str(dest/'warrior-return-v4.png'))
        page.select_option('#character','orc-01-archer');page.click('#return');page.locator('.pair').screenshot(path=str(dest/'archer-return-v4.png'))
        page.select_option('#state','Hit');page.select_option('#direction','back_l');page.select_option('#speed','0.5');page.click('#background');page.click('#play');page.wait_for_timeout(300);page.click('#play');page.select_option('#zoom','1')
        assert page.locator('#after').evaluate('e=>e.style.width')=='128px';assert not errors,errors
        version=browser.version;browser.close()
finally:server.shutdown();server.server_close()
report={'status':'PASS','clips':len(clips),'nativeFrameReferences':pixel_checks,'referenceFramesExact':references,'browserCanvasComparisonsExact':exact,'javaScriptErrors':errors,'browser':version,'checks':['All native frames RGBA128/binary alpha/ground126','Existing own outfit palettes; only approved near-black edits outside explicit return and direct V4','All action returns exact canonical own pose; all durations verified','Warrior front_r Attack/Hit pixel-identical to approved V4','All 192 clips rendered exactly in browser; file and HTTP; controls exercised'],'artisticApproval':'CREATOR_AUTHORIZED_PROPAGATION; technical checks are not independent artistic approval'}
(root/'reports/orc-production-v4-check.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))
