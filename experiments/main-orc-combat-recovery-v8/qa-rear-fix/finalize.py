from pathlib import Path
from PIL import Image
import json, hashlib, math, struct, copy

E=Path('experiments/main-orc-combat-recovery-v8/qa-rear-fix')
S=Path('characters/orc-v1/source/combat-recovery-v8/rear/back_r-sword')
D=Path('characters/orc-v1/source/combat-recovery-v8/rear-fix/back_r-sword')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def im(p): return Image.open(p).convert('RGBA')
def pixels(a): return list(a.getdata())
def equal(a,b): return pixels(a)==pixels(b)
def bright(a): return sum(c[3]>0 and .299*c[0]+.587*c[1]+.114*c[2]>=160 for c in pixels(a))
def centroid(a):
    pts=[(x,y) for y in range(a.height) for x in range(a.width) if a.getpixel((x,y))[3]]
    return [sum(p[k] for p in pts)/len(pts) for k in (0,1)] if pts else None
def durations(p):
    data=Path(p).read_bytes(); count=struct.unpack_from('<H',data,6)[0]; pos=128; out=[]
    for _ in range(count):
        size,magic=struct.unpack_from('<IH',data,pos); assert magic==0xF1FA
        out.append(struct.unpack_from('<H',data,pos+8)[0]);pos+=size
    return out
old=read(S/'clip.json');clip=copy.deepcopy(old); authored=read(E/'author-result.json')
names=old['layerOrder']; records=[];centers=[];origbright=[];newbright=[];frames=[]
reasons=[
 'Repouso traseiro original F00, preservado para manter o bookend desarmado.',
 'Preparação corporal original F01, preservada para manter a entrada desarmada.',
 'Estabelecimento de pegada original F02, preservado com arma ligada à luva.',
 'Antecipação original F03, preservada como elevação anterior ao coil.',
 'Coil original F04, preservado como início da preparação alta.',
 'Ápice derivado de F05/F04: antebraço e luva articulados -4° em torno de (163,105), com a arma acompanhando; cria compressão distinta antes da liberação.',
 'Liberação derivada de F06: antebraço e luva articulados +18° em torno de (166,121), com a arma acompanhando; antecipa a aceleração para a fase slash-release.',
 'Contato original F07, preservado como término da descida acelerada.',
 'Follow-through original F08, preservado para manter a extensão após contato.',
 'Recoil original F09, preservado como início da recuperação.',
 'Settle derivado de F10/F09: antebraço e luva articulados -15° em torno de (162,135), com a arma acompanhando; cria recolhimento distinto antes de soltar a pegada.',
 'Liberação original F11, preservada como recuperação desarmada.',
 'Retorno à guarda original F12, preservado para manter o bookend desarmado.'
]
for i,f in enumerate(old['frames']):
    q=copy.deepcopy(f);layers={n:im(D/f'layers/{n}/{i:02}.png') for n in names}
    render=Image.new('RGBA',(256,256))
    for a in layers.values(): render=Image.alpha_composite(render,a)
    assert equal(render,im(D/f'frames/{i:02}.png'))
    assert equal(layers['body'].crop((64,64,192,192)),im(D/f'native/{i:02}.png'))
    bodyold=im(f['layers']['body']['png']); before=pixels(bodyold);after=pixels(layers['body'])
    lost=sum(c[3]>0 and .299*c[0]+.587*c[1]+.114*c[2]>=160 and c!=d for c,d in zip(before,after));assert lost==0
    origbright.append(bright(bodyold));newbright.append(bright(layers['body']))
    wp=Image.alpha_composite(layers['weaponBack'],layers['weaponFront'])
    below=sum(wp.getpixel((x,y))[3]>0 for y in range(191,256) for x in range(256));assert below==0
    c=centroid(layers['weaponFront']);centers.append(c)
    overlap=sum(a[3]>0 and b[3]>0 for a,b in zip(pixels(wp),pixels(layers['handFront'])))
    if f['weaponVisible']: assert c is not None and overlap>0
    else: assert c is None and all(layers[n].getbbox() is None for n in ('weaponBack','weaponFront','handFront'))
    if i not in (5,6,10):
        assert all(equal(layers[n],im(f['layers'][n]['png'])) for n in names)
    for n in names:
        p=D/f'layers/{n}/{i:02}.png';q['layers'][n]={'png':p.as_posix(),'sha256':sha(p)}
    q['png']=(D/f'frames/{i:02}.png').as_posix();q['nativePng']=(D/f'native/{i:02}.png').as_posix()
    q['sha256']=sha(q['png']);q['nativeSha256']=sha(q['nativePng'])
    q['sourceClip']=(S/'clip.json').as_posix();q['sourceClipSha256']=sha(S/'clip.json');q['sourceFrame']=i;q['sourcePhase']=f['phase']
    edit=authored['frames'][i]['edit'];q['sourceMode']='ASEPRITE_LOCAL_DISTAL_ARTICULATION' if edit else 'REUSE_LAYER_PIXELS'
    q['poseProvenance']=reasons[i]
    if edit:
        q['articulation']=edit;q['rightGrip']=edit['rightGrip'];q['rotationDeg']=f['rotationDeg']+edit['degrees']
    frames.append(q);records.append({'index':i,'sha256':q['sha256'],'centroidWeaponFront':c,'brightBody160':newbright[-1],'brightPixelsErased':lost,'weaponBelowGround':below,'weaponGloveOverlapPixels':overlap})
    for n in names: assert sha(f['layers'][n]['png'])==f['layers'][n]['sha256']
    assert sha(f['png'])==f['sha256'] and sha(f['nativePng'])==f['nativeSha256']
armed=[f for f in frames if f['weaponVisible']];assert len({f['sha256'] for f in armed})==9
assert len({im(f['png']).tobytes() for f in armed})==9
steps=[{'from':i-1,'to':i,'distancePx':math.dist(centers[i-1],centers[i]) if centers[i-1] and centers[i] else None} for i in range(1,13)]
peak=max((s for s in steps if s['distancePx'] is not None),key=lambda s:s['distancePx'])
assert peak['from']==5 and peak['to']==6 and 56<=peak['distancePx']<=76
for key,file in [('master','source/composite.aseprite'),('nativeMaster','source/native.aseprite'),('strip','native-strip.png'),('nativeStrip','native-strip.png'),('compositeStrip','composite-strip.png')]:
    clip[key]=(D/file).as_posix();clip[key+'Sha256']=sha(D/file)
for file in ['source/composite.aseprite','source/native.aseprite']:assert durations(D/file)==old['durationsMs']
for i in [0,1,11,12]:
    assert sha(D/f'frames/{i:02}.png')==sha(S/f'frames/{i:02}.png')
    assert sha(D/f'native/{i:02}.png')==sha(S/f'native/{i:02}.png')
for file,size,sub in [('composite-strip.png',256,'frames'),('native-strip.png',128,'native')]:
    a=im(D/file);assert a.size==(size*13,size)
    for i in range(13): assert equal(a.crop((size*i,0,size*(i+1),size)),im(D/f'{sub}/{i:02}.png'))
assert Image.open(E/'F04-F07-4x.png').size==(4096,1024)
clip.update(revision='main-orc-combat-recovery-v8-rear-fix',checkpoint='V8_REAR_FIX',frames=frames,sourceParentClip=(S/'clip.json').as_posix(),sourceParentClipSha256=sha(S/'clip.json'),technicalStatus='TECHNICALLY_COMPLETE',artisticStatus='VISUAL_REVIEW_REQUIRED',creatorApproval='PENDING_CREATOR')
clip['provenance']={'method':'Autoria programática Aseprite Lua: articulação distal local de doadores back_r da própria célula; sem geração ou edição raster externa.','authorScript':(E/'author.lua').as_posix(),'authorScriptSha256':sha(E/'author.lua'),'generationCalls':0,'mastersSavedReopened':True,'timingVerified':True,'referenceClips':['characters/orc-v1/source/combat-recovery-v8/rear/back_l-sword/clip.json','characters/orc-v1/source/combat-recovery-v7/frontal/full-front-r-sword/clip.json']}
(D/'clip.json').write_text(json.dumps(clip,ensure_ascii=False,indent=2),encoding='utf-8')
backl=read('characters/orc-v1/source/combat-recovery-v8/rear/back_l-sword/clip.json');backlbright=[bright(im(f['layers']['body']['png'])) for f in backl['frames']]
metrics={'technicalStatus':'TECHNICALLY_COMPLETE','artisticStatus':'VISUAL_REVIEW_REQUIRED','records':records,'steps':steps,'peak':peak,'originalBodyBright160':origbright,'candidateBodyBright160':newbright,'backlBodyBright160':backlbright,'unchangedBookends':[0,1,11,12],'armedDuplicatePairs':0,'timingAndPhasesUnchanged':True,'newGenerationCalls':0,'manifestIntegrated':False}
(E/'metrics.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2),encoding='utf-8')
lines=['# Reparo local back_r/Sword — V8','','Status: `TECHNICALLY_COMPLETE` / `VISUAL_REVIEW_REQUIRED` / `PENDING_CREATOR`.','','Entrega: `'+D.as_posix()+'/clip.json`. Nenhuma integração no manifesto, nenhuma outra célula alterada, nenhum commit e nenhuma escrita no Unity.','',
'## Verificação dos critérios','',
'- 9 quadros armados distintos por SHA-256 e por pixels RGBA decodificados; nenhum par duplicado.',
f'- Maior passo: **F05 → F06 = {peak["distancePx"]:.4f} px**, dentro de 56–76 px; F06 → F07 = {steps[6]["distancePx"]:.4f} px.',
'- Grade preservada: 13 quadros / 730 ms; durações `[30,65,35,50,45,65,35,35,100,55,80,45,90]`; fases e janela armada F02–F10 idênticas à origem. Bookends desarmados F00/F01/F11/F12 byte-idênticos.',
'- **0 pixels claros de armadura apagados** (L = 0,299R + 0,587G + 0,114B ≥ 160). A origem back_r já contém zero desses pixels em todos os quadros; sua série `[0,0,0,0,0,0,0,0,0,0,0,0,0]` foi preservada. A referência back_l contém `'+str(backlbright)+'`. Não se afirma igualdade entre essas séries. Fechamento conforme esclarecimento do usuário: preservar os pixels claros existentes satisfaz este ponto.',
'- Zero pixels de arma abaixo de groundY=190. Em F02–F10 há interseção raster entre arma e luva handFront em todos os quadros; arma, luva e antebraço transformados juntos nos reparos. Inspeção ampliada local confirma ligação visual.',
'- Composição alfa-over das quatro camadas idêntica aos frames; native128 idêntico ao crop body[64:192,64:192]. Tempos lidos dos dois mestres .aseprite salvos; strips conferidos quadro a quadro.','',
'## Procedência e decisões','',
'Autoria **programática local no Aseprite 1.3.18.6**, via [author.lua](author.lua), sem IA/PixelLab. Imagens e mestres exportados pelo editor; Python usado apenas para medição, metadados e relatório. Fontes back_r herdadas preservadas. back_l/Sword V8 e front_r/Sword referenciado pelo V8 serviram de comparação visual para preparação, liberação e recuperação; nenhum pixel dessas vistas foi espelhado ou transplantado. Os doadores raster são da própria vista back_r e do mesmo item.','',
'As únicas articulações novas são F05, F06 e F10; máscaras, pivôs e ângulos estão em author.lua e author-result.json. Restante do corpo preservado fora das máscaras locais. Não houve mudança de relógio nem redesenho integral.','',
'| Quadro | Fase | ms | Pose usada e motivo |','|---|---|---:|---|']
for i,f in enumerate(frames):lines.append(f'| F{i:02} | {f["phase"]} | {f["durationMs"]} | {reasons[i]} |')
lines+=['','## SHA-256 dos 13 quadros compostos','','| Quadro | SHA-256 |','|---|---|']
for f in frames:lines.append(f'| F{f["index"]:02} | `{f["sha256"]}` |')
lines+=['','## Centroide da lâmina e passos','','Centroide geométrico dos pixels não transparentes de `weaponFront`, canvas composto 256×256, mesmo método que reproduz os valores do QA original. Transições sem lâmina nos dois extremos são N/A; surgimento e desaparecimento não são passos cinéticos.','','| Transição | Centroide anterior (x,y) | Centroide seguinte (x,y) | Passo px |','|---|---|---|---:|']
def fmt(c):return f'({c[0]:.4f}, {c[1]:.4f})' if c else '—'
for s in steps:
    v=f'{s["distancePx"]:.4f}' if s['distancePx'] is not None else 'N/A'
    lines.append(f'| F{s["from"]:02} → F{s["to"]:02} | {fmt(centers[s["from"]])} | {fmt(centers[s["to"]])} | {v} |')
lines+=['','## Strip F04–F07 em 4×','','Exportação Aseprite: 4096×1024, quatro canvases compostos de 256×256 ampliados em 4×.','','![F04–F07 em 4×](F04-F07-4x.png)','','Métricas completas: [metrics.json](metrics.json). Contrato, hashes das camadas, native e mestres: `'+(D/'clip.json').as_posix()+'`. Aprovação artística permanece reservada ao criador.']
(E/'report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({'peak':peak,'armedDistinctFrames':9,'brightPixelsErased':0,'report':str(E/'report.md'),'status':'TECHNICALLY_COMPLETE'}))
