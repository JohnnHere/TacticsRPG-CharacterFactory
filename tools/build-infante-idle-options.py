"""Portable three-way Idle comparison; source art is copied without raster edits."""
from pathlib import Path
import json,hashlib,shutil,html
ROOT=Path(__file__).resolve().parents[1]
LIB=ROOT/'Biblioteca de Arte'
REL='Estudos Comparativos/Infante de Ferro - Idle'
OUT=LIB/REL;OUT.mkdir(parents=True,exist_ok=True)
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
source='experiments/orc-infante-idle-subtle-v2/before'
old=read(ROOT/source/'source/studies/Idle/clip.json')
old['frames']=[{**f,'png':source+f'/source/studies/Idle/{i:02d}.png'} for i,f in enumerate(old['frames'])]
old['master']=source+'/original-idle.aseprite'
entries=[('01 - Anterior','Anterior',old,4),('02 - Mais sutil','Mais sutil',read(ROOT/'experiments/orc-infante-idle-subtle-v2/after/clip.json'),1),('03 - Meio termo','Meio-termo',read(ROOT/'characters/orc-pixellab-05/source/studies/IdleCandidates/balanced-v3/clip.json'),2)]
data=[];files=[]
for folder,title,clip,excursion in entries:
    frames=[]
    for i,f in enumerate(clip['frames']):
        rel=folder+f'/Quadros/{i:02d}.png';dest=OUT/rel;dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(ROOT/f['png'],dest)
        frames.append({'png':rel,'durationMs':f['durationMs']})
        files.append({'file':rel,'source':f['png'],'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
    master=folder+'/Idle.aseprite';shutil.copy2(ROOT/clip['master'],OUT/master)
    files.append({'file':master,'source':clip['master'],'sha256':hashlib.sha256((OUT/master).read_bytes()).hexdigest()})
    item={'title':title,'frames':frames,'master':master,'headExcursionPx':excursion,'cycleMs':sum(f['durationMs'] for f in frames),'selected':bool(clip.get('selectedAsCurrent',False))}
    (OUT/folder/'clip.json').write_text(json.dumps(item,ensure_ascii=False,indent=2),encoding='utf-8')
    data.append(item)
cards=[]
for i,c in enumerate(data):
    cards.append(f'<article><h2>{html.escape(c["title"])}{" · aprovado" if c['selected'] else ""}</h2><p>{c["headExcursionPx"]} px de oscilação da cabeça · {c["cycleMs"]/1000:g} s por ciclo</p><div class="stage"><canvas id="anim-{i}" width="128" height="128"></canvas></div><p id="frame-{i}"></p><a href="{c["master"]}">Mestre Aseprite</a></article>')
script=r'''const cache=new Map;const views=data.map(()=>({frame:0,time:0}));let ready=false,playing=true,last=0,speed=1;function asset(p){if(!cache.has(p))cache.set(p,new Promise((ok,no)=>{const im=new Image;im.onload=()=>ok(im);im.onerror=()=>no(Error(p));im.src=p}));return cache.get(p)}async function draw(i){const f=data[i].frames[views[i].frame],im=await asset(f.png),ctx=document.getElementById('anim-'+i).getContext('2d');ctx.imageSmoothingEnabled=false;ctx.clearRect(0,0,128,128);ctx.drawImage(im,0,0);document.getElementById('frame-'+i).textContent='Quadro '+(views[i].frame+1)+'/'+data[i].frames.length+' · '+f.durationMs+' ms'}Promise.all(data.flatMap(c=>c.frames.map(f=>asset(f.png)))).then(()=>Promise.all(data.map((_,i)=>draw(i)))).then(()=>{ready=true;document.body.dataset.ready='true'});document.getElementById('play').onclick=()=>{playing=!playing;document.getElementById('play').textContent=playing?'Pausar':'Reproduzir'};document.getElementById('reset').onclick=()=>{views.forEach((v,i)=>{v.frame=0;v.time=0;draw(i)})};document.getElementById('step').onclick=()=>{playing=false;document.getElementById('play').textContent='Reproduzir';views.forEach((v,i)=>{v.frame=(v.frame+1)%data[i].frames.length;draw(i)})};document.getElementById('zoom').onchange=e=>{const size=128*Number(e.target.value);document.querySelectorAll('canvas').forEach(c=>c.style.width=c.style.height=size+'px');document.querySelectorAll('.stage').forEach(c=>c.style.height=(size+24)+'px')};document.getElementById('speed').onchange=e=>speed=Number(e.target.value);function tick(t){const dt=last?Math.min(100,t-last)*speed:0;last=t;if(ready&&playing)views.forEach((v,i)=>{v.time+=dt;if(v.time>=data[i].frames[v.frame].durationMs){v.time-=data[i].frames[v.frame].durationMs;v.frame=(v.frame+1)%data[i].frames.length;draw(i)}});requestAnimationFrame(tick)}requestAnimationFrame(tick);'''
payload=json.dumps(data,ensure_ascii=False).replace('<','\\u003c')
page='''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Infante de Ferro · três opções de Idle</title><style>*{box-sizing:border-box}body{margin:24px;background:#15252a;color:#e3ebe8;font:16px/1.5 system-ui}a{color:#e3c38d}.options{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}article{padding:18px;background:#23363d;border:1px solid #536f75;border-radius:8px}h2{margin:0}p{color:#bdcfca}.stage{height:280px;display:flex;align-items:center;justify-content:center;overflow:auto;background:repeating-conic-gradient(#2b3f45 0 25%,#3a5259 0 50%) 0/20px 20px}canvas{width:256px;height:256px;image-rendering:pixelated;flex-shrink:0}.toolbar{display:flex;gap:12px;flex-wrap:wrap;margin:20px 0}button,select{font:inherit;color:white;background:#344c54;padding:8px;border:1px solid #6e8a91;border-radius:4px}.opinion{max-width:1100px}@media(max-width:1000px){.options{grid-template-columns:1fr}}</style><h1>Infante de Ferro · três opções de Idle</h1><p><a href="../../index.html">Voltar à Biblioteca de Arte</a></p><p class="opinion">Minha preferência para gameplay é o meio-termo: mantém o personagem vivo com menos agitação que o anterior. O sutil favorece repouso; o anterior transmite maior esforço ou tensão. Esta é uma comparação de arte; a leitura final poderá ser conferida em cena com várias unidades.</p><div class="toolbar"><button id="play">Pausar</button><button id="reset">Reiniciar juntos</button><button id="step">Avançar um quadro</button><label>Zoom <select id="zoom"><option value="1">1× nativo</option><option value="2" selected>2×</option><option value="3">3×</option></select></label><label>Velocidade <select id="speed"><option value="1">1× real</option><option value="0.5">0,5×</option></select></label></div><div class="options">CARDS</div><p>Poses completas originais, sem redimensionar a anatomia, comprimir o tronco ou misturar pixels entre quadros. Cada versão conserva sua cadência real. O meio-termo foi aprovado pelo criador, é o Idle atual do Infante e a referência artística para os próximos Idles.</p><script>const data=DATA;SCRIPT</script></html>'''.replace('CARDS',''.join(cards)).replace('DATA',payload).replace('SCRIPT',script)
(OUT/'index.html').write_text(page,encoding='utf-8')
(OUT/'catalogo.json').write_text(json.dumps({'date':'2026-10-25','variants':data,'files':files,'productionSelected':False,'selectedRevision':'infante-idle-balanced-v3'},ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'LEIA-ME.md').write_text('# Três opções de Idle — Infante de Ferro\n\nAbra index.html para comparar. Anterior: 4 px/1,6 s; mais sutil: 1 px/2,8 s; meio-termo: 2 px/2,2 s. Oscilação medida na altura da cabeça, não no corpo inteiro. Arquivos completos e editáveis separados por versão. Meio-termo aprovado pelo criador, selecionado no Infante e adotado como referência artística para os próximos Idles. Fontes e procedência em catalogo.json. Atualizar esta comparação com tools/build-infante-idle-options.py.\n',encoding='utf-8')
registry=[{'id':'infante-idle-three-options','title':'Infante de Ferro · três opções de Idle','path':REL+'/index.html','builder':'tools/build-infante-idle-options.py'}]
(ROOT/'docs/ART_LIBRARY_COMPARISONS.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2),encoding='utf-8')
report=ROOT/'reports/orc-idle-balanced-v3';report.mkdir(exist_ok=True)
url='../../Biblioteca de Arte/'+REL+'/index.html'
(report/'review.html').write_text('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0;url='+url+'"><a href="'+url+'">Comparar os três Idles</a>',encoding='utf-8')
print(json.dumps({'comparison':str(OUT/'index.html'),'variants':3,'artFiles':len(files),'originalsUnchanged':True},ensure_ascii=False))
