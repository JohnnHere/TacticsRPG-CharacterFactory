"""Build a portable browsing library from canonical assets; never edits raster art."""
from pathlib import Path
import json,shutil,hashlib,html,os,re,datetime

ROOT=Path(__file__).resolve().parents[1]
LIB=ROOT/'Biblioteca de Arte'
LIB.mkdir(exist_ok=True)
if (ROOT/'docs/IDLE_ART_STANDARD.md').exists():shutil.copy2(ROOT/'docs/IDLE_ART_STANDARD.md',LIB/'PADRAO-DE-IDLE.md')
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ART_NOTES=read(ROOT/'docs/ART_LIBRARY_NOTES.json')['characters']
COMPARISONS=read(ROOT/'docs/ART_LIBRARY_COMPARISONS.json') if (ROOT/'docs/ART_LIBRARY_COMPARISONS.json').exists() else []
manifest_path=LIB/'catalogo.json'
previous=read(manifest_path) if manifest_path.exists() else {'files':[]}
old={f['file']:f['sha256'] for f in previous['files']}
files=[]
stamp=datetime.datetime.now().strftime('%Y%m%d-%H%M%S')

def copy_asset(source,dest):
    source=ROOT/source;target=LIB/dest
    if target.exists() and sha(target)!=sha(source):
        if dest not in old or sha(target)!=old[dest]:
            raise RuntimeError('Arquivo editado na biblioteca; preservar antes de atualizar: '+str(target))
        backup=LIB/'Historico de Entregas'/stamp/dest
        backup.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(target,backup)
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(source,target)
    files.append({'file':dest,'source':source.relative_to(ROOT).as_posix(),'sha256':sha(target)})
    return dest

def clean_name(name):
    return re.sub(r'\s+',' ',re.sub(r'[<>:"/\\|?*·]',' ',name)).strip()

def package(cid,category,source_base=None):
    base=source_base or 'characters/'+cid
    spec=read(ROOT/base/'character.json')
    folder=category+'/'+('Orc V1' if cid=='orc-v1' else cid.rsplit('-',1)[-1]+' - '+clean_name(spec['name']))
    concept=copy_asset(base+'/concepts/concept-selected.png',folder+'/Conceito/conceito.png')
    concept_master=copy_asset(base+'/source/aseprite/concept-selected.aseprite',folder+'/Mestres Aseprite/Conceito.aseprite')
    clips={}
    for state in ['Idle','Walk']:
        source_clip=ROOT/base/'source/studies'/state/'clip.json'
        if not source_clip.exists():continue
        clip=read(source_clip);frames=[]
        for i,f in enumerate(clip['frames']):
            png=copy_asset(f['png'],folder+'/'+state+f'/Quadros/{i:02d}.png')
            frames.append({'png':png,'durationMs':f['durationMs']})
        master=copy_asset(clip['master'],folder+'/Mestres Aseprite/'+state+'.aseprite')
        local={'state':state,'frames':[{'png':'Quadros/'+f'{i:02d}.png','durationMs':f['durationMs'],'sha256':sha(LIB/f['png'])} for i,f in enumerate(frames)],'master':'../Mestres Aseprite/'+state+'.aseprite','canonicalClip':source_clip.relative_to(ROOT).as_posix(),'revision':clip.get('revision'),'artisticApproval':clip.get('artisticApproval')}
        (LIB/folder/state/'clip.json').write_text(json.dumps(local,ensure_ascii=False,indent=2),encoding='utf-8')
        clips[state]={'frames':frames,'master':master,'revision':clip.get('revision')}
    card={'id':cid,'title':spec['name'],'folder':folder,'concept':concept,'conceptMaster':concept_master,'clips':clips,'reserved':category=='Ideias Futuras','pendingNotes':ART_NOTES.get(cid,[])}
    (LIB/folder/'ORIGEM.json').write_text(json.dumps({'canonicalPackage':base,'libraryRole':'Copia de consulta/entrega; fontes canonicas continuam no pacote original. Atualizar com tools/build-art-library.py.','files':[f for f in files if f['file'].startswith(folder+'/')]},ensure_ascii=False,indent=2),encoding='utf-8')
    if card['pendingNotes']:
        (LIB/folder/'PENDENCIAS.md').write_text('# Pendências — '+spec['name']+'\n\n'+'\n'.join('- '+n for n in card['pendingNotes'])+'\n',encoding='utf-8')
    return card

selection=read(ROOT/'reports/orc-study-selection.json')
current=[package(cid,'Orcs Atuais') for cid in selection['currentCandidates']]
ideas=[package(cid,'Ideias Futuras','ideas/unique-characters-or-npcs/'+cid) for cid in selection['reservedIdeas']]
archived=[package(cid,'Arquivo de Arte') for cid in selection.get('archivedCandidates',[])]

STYLE='''*{box-sizing:border-box}body{margin:0;background:#152126;color:#e7ece9;font:15px/1.5 system-ui}main{max-width:1700px;margin:auto;padding:24px}h1{font-size:32px}h2{font-size:23px;margin:0}h3,a{color:#dfc18b}a{overflow-wrap:anywhere}p{color:#bdcdca}.toolbar{display:flex;gap:14px;align-items:center;flex-wrap:wrap;position:sticky;top:0;z-index:2;background:#152126;padding:12px 0;border-bottom:1px solid #4f6469}button,select{padding:7px;font:inherit;background:#30474e;color:white;border:1px solid #6d878d;border-radius:4px}.nav{display:flex;flex-wrap:wrap;gap:12px;margin:20px 0}article{padding:18px;border:1px solid #4f6469;border-radius:8px;background:#203137;margin:20px 0;scroll-margin-top:85px}.states{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}.states>section{min-width:0}.stage{display:flex;align-items:center;justify-content:center;height:280px;overflow:auto;background:repeating-conic-gradient(#293b40 0 25%,#374d52 0 50%) 0/20px 20px}img,canvas{width:256px;height:256px;image-rendering:pixelated;object-fit:contain;flex-shrink:0}.note{font-size:13px}.links{display:flex;gap:15px;flex-wrap:wrap}article header{display:flex;justify-content:space-between;gap:15px}@media(max-width:850px){.states{grid-template-columns:1fr}main{padding:12px}}'''
SCRIPT=r'''const cache=new Map;const views=[];let playing=true,ready=false,last=0,speed=1;function asset(p){if(!cache.has(p))cache.set(p,new Promise((ok,no)=>{const im=new Image;im.onload=()=>ok(im);im.onerror=()=>no(Error(p));im.src=p}));return cache.get(p)}for(let i=0;i<data.length;i++)for(const state of ['Idle','Walk'])if(data[i].clips[state])views.push({i,state,frame:0,time:0});async function draw(v){const clip=data[v.i].clips[v.state],f=clip.frames[v.frame],im=await asset(f.png),ctx=document.getElementById('anim-'+v.i+'-'+v.state).getContext('2d');ctx.imageSmoothingEnabled=false;ctx.clearRect(0,0,128,128);ctx.drawImage(im,0,0);document.getElementById('frame-'+v.i+'-'+v.state).textContent=(v.frame+1)+'/'+clip.frames.length+' quadros · '+f.durationMs+' ms · ciclo '+clip.frames.reduce((s,f)=>s+f.durationMs,0)+' ms'}document.getElementById('play').onclick=()=>{playing=!playing;document.getElementById('play').textContent=playing?'Pausar':'Reproduzir'};document.getElementById('step').onclick=()=>{playing=false;document.getElementById('play').textContent='Reproduzir';for(const v of views){v.frame=(v.frame+1)%data[v.i].clips[v.state].frames.length;draw(v)}};document.getElementById('speed').onchange=e=>speed=Number(e.target.value);document.getElementById('zoom').onchange=e=>{const z=128*Number(e.target.value);for(const el of document.querySelectorAll('canvas,img'))el.style.width=el.style.height=z+'px';for(const el of document.querySelectorAll('.stage'))el.style.height=(z+24)+'px'};Promise.all(data.flatMap(c=>Object.values(c.clips).flatMap(c=>c.frames.map(f=>asset(f.png))))).then(()=>Promise.all(views.map(draw))).then(()=>{ready=true;document.body.dataset.ready='true'});function tick(t){const dt=last?Math.min(100,t-last)*speed:0;last=t;if(playing&&ready)for(const v of views){const clip=data[v.i].clips[v.state];v.time+=dt;if(v.time>=clip.frames[v.frame].durationMs){v.time-=clip.frames[v.frame].durationMs;v.frame=(v.frame+1)%clip.frames.length;draw(v)}}requestAnimationFrame(tick)}requestAnimationFrame(tick);'''

def render(cards,page,title):
    page=LIB/page;page.parent.mkdir(parents=True,exist_ok=True)
    url=lambda p:Path(os.path.relpath(LIB/p,page.parent)).as_posix()
    esc=html.escape;rendered=[];data=[]
    for i,c in enumerate(cards):
        cd={**c,'clips':{s:{**clip,'frames':[{**f,'png':url(f['png'])} for f in clip['frames']]} for s,clip in c['clips'].items()}};data.append(cd)
        sections=[f'<section><h3>Conceito</h3><div class="stage"><img src="{esc(url(c["concept"]))}" alt="{esc(c["title"])}"></div><p class="note"><a href="{esc(url(c["concept"]))}">PNG</a> · <a href="{esc(url(c["conceptMaster"]))}">Mestre Aseprite</a></p></section>']
        for state in ['Idle','Walk']:
            clip=c['clips'].get(state)
            if clip:sections.append(f'<section><h3>{state}</h3><div class="stage"><canvas width="128" height="128" id="anim-{i}-{state}" aria-label="{esc(c["title"])} {state}"></canvas></div><p class="note" id="frame-{i}-{state}"></p><p class="note"><a href="{esc(url(clip["master"]))}">Mestre Aseprite</a> · <a href="{esc(url(c["folder"]+"/"+state+"/clip.json"))}">Quadros e tempos</a></p></section>')
            else:sections.append(f'<section><h3>{state}</h3><div class="stage"><p>Não produzido nesta etapa.</p></div></section>')
        pending_note=''.join('<p class="note"><strong>Pendência:</strong> '+esc(n)+'</p>' for n in c.get('pendingNotes',[]))
        rendered.append(f'<article id="{c["id"]}"><header><h2>{esc(c["title"])}</h2><a href="#top">Início ↑</a></header><p>{"Ideia futura de NPC e/ou jogável exclusivo/único." if c["reserved"] else "Estudos de uma vista · sem integração no jogo."}</p>{pending_note}<div class="states">'+''.join(sections)+f'</div><p class="links"><a href="{esc(url(c["folder"]+"/index.html"))}">Ficha e arquivos deste Orc</a><a href="{esc(url(c["folder"]+"/ORIGEM.json"))}">Origem dos arquivos</a></p></article>')
    nav=''.join(f'<a href="#{c["id"]}">{esc(c["title"])}</a>' for c in cards)
    payload=json.dumps(data,ensure_ascii=False).replace('<','\\u003c')
    comparison_links=''.join('<a href="'+esc(url(c['path']))+'">'+esc(c['title'])+'</a>' for c in COMPARISONS)
    page.write_text(f'''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><style>{STYLE}</style><main id="top"><h1>{esc(title)}</h1><p class="links"><a href="{esc(url('index.html'))}">Todos os Orcs atuais</a><a href="{esc(url('Ideias Futuras/index.html'))}">Vigia e Matriarca · ideias futuras</a><a href="{esc(url('LEIA-ME.md'))}">Como encontrar e atualizar os arquivos</a> <a href="{esc(url('Arquivo de Arte/index.html'))}">Arquivo de Arte · originais preservados</a> <a href="{esc(url('PADRAO-DE-IDLE.md'))}">Padrão de Idle aprovado</a></p><p class="links">{comparison_links}</p><div class="toolbar"><button id="play">Pausar</button><button id="step">Avançar quadro</button><label>Velocidade <select id="speed"><option value="1">1×</option><option value="0.5">0,5×</option><option value="0.25">0,25×</option></select></label><label>Zoom <select id="zoom"><option value="1">1×</option><option value="2" selected>2×</option><option value="3">3×</option></select></label></div><nav class="nav">{nav}</nav>{''.join(rendered)}<p>V4 ativa e Reimaginado foram descartados e não fazem parte desta biblioteca de opções atuais. Ideias reservadas ficam separadas. Fontes e histórico originais foram preservados.</p></main><script>const data={payload};{SCRIPT}</script></html>''',encoding='utf-8')

render(current,'index.html','Biblioteca de Arte · Orcs atuais')
render(archived,'Arquivo de Arte/index.html','Arquivo de Arte · originais preservados')
render(ideas,'Ideias Futuras/index.html','Ideias futuras · únicos jogáveis e/ou NPCs')
for c in current+ideas+archived:render([c],c['folder']+'/index.html',c['title']+' · conceito e animações')
(LIB/'LEIA-ME.md').write_text('''# Biblioteca de Arte

Abra **index.html** para comparar os Orcs atuais, com conceito, Idle e Walk juntos. Os links no topo levam diretamente a cada personagem.

## Padrão de Idle aprovado — 2026-10-25

PADRÃO FIXO OBRIGATÓRIO na criação de personagens: mesmo Idle normal do meio-termo aprovado, cinco fases 400/450/500/450/400 ms, ciclo 2,2 s e amplitude equivalente a 2 px na cabeça de humanoide 128×128. Não variar o padrão por personagem, Job, roupa ou personalidade. Ajustar somente o encaixe à anatomia/escala, mantendo a mesma cadência e sutileza. Qualquer exceção exige autorização explícita do criador. Diretriz completa em **PADRAO-DE-IDLE.md**. O Infante já exibe a versão aprovada; demais personagens não foram alterados automaticamente.

## Pendência artística — 2026-10-25

Precisamos trabalhar melhor a armadura do **Orc Ágil (Veterano Ágil, 04)** antes de fechar sua versão de produção. A pendência também aparece na ficha visual e em PENDENCIAS.md do personagem. Notas persistentes em docs/ART_LIBRARY_NOTES.json, preservadas ao reconstruir a biblioteca.

## Pastas

- **Orcs Atuais/**: inclui o **Orc V1**, pele Verde Warcraft selecionada para futura integração, e os demais candidatos.
- **Infante de Ferro original**: permanece em **Orcs Atuais/**, com conceito, Idle, Walk e mestres, destinado a uma etapa mais avançada do jogo. **Orc V1** continua como primeiro jogável selecionado.
- **Arquivo de Arte/**: reservado a históricos; não é a categoria atual do Infante de Ferro.
- **Personagens Jogaveis/Orc V1/**: armas separadas e estudos equipados de golpe e caminhada; prévias locais, sem integração Unity.
- **Conceito/**: PNG do conceito.
- **Idle/Quadros/** e **Walk/Quadros/**: PNGs nativos em ordem. O clip.json da ação registra os tempos reais.
- **Mestres Aseprite/**: arquivos editáveis de Conceito, Idle e Walk.
- **Estudos Comparativos/**: versões alternativas lado a lado; inclui os três Idles do Infante de Ferro e **Infante de Ferro - Pele Verde/** (original × pele verde, conceito e Idle), com mestres e quadros por versão. Candidatos não substituem a seleção atual automaticamente.
- **Ideias Futuras/**: Vigia do Passo e Matriarca, separados como ideias de NPC e/ou jogáveis exclusivos/únicos. Somente conceito nesta etapa.
- **Historico de Entregas/**: criada nas atualizações quando uma cópia anterior precisa ser preservada.

Cada personagem tem seu próprio **index.html** e **ORIGEM.json**. Esta é uma cópia de consulta/entrega, autossuficiente para abrir os PNGs, mestres e páginas sem Internet. Fontes canônicas da pipeline continuam em characters/ e ideas/unique-characters-or-npcs/, identificadas em ORIGEM.json e catalogo.json. Para continuar a produção, editar a fonte canônica por fork e reconstruir a biblioteca.

Atualizar após exportar/salvar no Aseprite:

`tmp/pixel-venv/Scripts/python.exe tools/build-art-library.py`

O construtor confere hashes, preserva versões anteriores e interrompe se detectar uma cópia de arte editada diretamente nesta biblioteca, para não sobrescrever seu trabalho. Não há integração ou alteração no jogo. V4 e Reimaginado descartados não são opções atuais. A limpeza dos pés do Atlético foi feita localmente no Aseprite, preservando as oito poses e os tempos.
''',encoding='utf-8')
# Archive obsolete generated frames when a revised clip has fewer poses.
active_files={f['file'] for f in files}
for entry in previous['files']:
    if entry['file'] in active_files:continue
    target=(LIB/entry['file']).resolve()
    if not target.is_relative_to(LIB.resolve()):raise RuntimeError('Obsolete file outside library')
    if target.exists():
        if sha(target)!=entry['sha256']:raise RuntimeError('Obsolete library asset was edited: '+str(target))
        backup=(LIB/'Historico de Entregas'/stamp/entry['file']).resolve()
        if not backup.is_relative_to(LIB.resolve()):raise RuntimeError('Backup outside library')
        backup.parent.mkdir(parents=True,exist_ok=True);shutil.move(target,backup)

manifest={'schemaVersion':1,'date':'2026-10-24','role':'Portable browsing and delivery copy; canonical sources retained','root':'Biblioteca de Arte','index':'index.html','current':current,'futureIdeas':ideas,'archived':archived,'comparisons':COMPARISONS,'files':files,'unityChanged':False}
manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'library':str(LIB),'currentOrcs':len(current),'futureIdeas':len(ideas),'copiedAssets':len(files),'allHashesMatch':all(sha(LIB/f['file'])==f['sha256'] for f in files)},ensure_ascii=False))
