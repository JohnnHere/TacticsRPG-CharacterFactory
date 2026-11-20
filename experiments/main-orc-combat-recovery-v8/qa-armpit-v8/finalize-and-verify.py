import json,hashlib,shutil
from pathlib import Path
from collections import Counter
from PIL import Image
E=Path('experiments/main-orc-combat-recovery-v8/qa-armpit-v8');S=Path('characters/orc-v1/source/combat-recovery-v7/frontal/front_l-Sword-full');D=Path('characters/orc-v1/source/combat-recovery-v8/frontal-armpit/front_l-sword')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pixels(p):return Image.open(p).convert('RGBA')
plan=json.loads((E/'edit-plan.json').read_text());old=json.loads((S/'clip.json').read_text());clip=json.loads((S/'clip.json').read_text())
def rewrite(v):
 if isinstance(v,str):return v.replace(S.as_posix(),D.as_posix())
 if isinstance(v,list):return [rewrite(x) for x in v]
 if isinstance(v,dict):return {k:rewrite(x) for k,x in v.items()}
 return v
clip=rewrite(clip)
clip.update(revision='main-orc-combat-recovery-v8-armpit',sourceParentClip=(S/'clip.json').as_posix(),sourceParentClipSha256=sha(S/'clip.json'),technicalStatus='TECHNICALLY_COMPLETE',artisticStatus='VISUAL_REVIEW_REQUIRED',artisticApproval='PENDING_CREATOR',checkpoint='V8_ARMPIT_LOCAL_CANDIDATE',fullClipIndependentQA='PENDING')
clip['inheritedProvenance']=clip['provenance']
clip['provenance']={'authoring':'Autoria programatica Lua no Aseprite: reiluminacao localizada da superficie interna da juncao deltoide-tronco; sem alterar alpha, contorno externo, roupa vermelha ou highlights. Fontes herdadas preservadas por copia isolada.','editor':'Aseprite 1.3.18.6 --batch --noinapp; isolated ASEPRITE_USER_FOLDER=tmp/aseprite-batch-profile','script':(E/'author-armpit.lua').as_posix(),'scriptSha256':sha(E/'author-armpit.lua'),'plan':(E/'edit-plan.json').as_posix(),'planSha256':sha(E/'edit-plan.json'),'verification':(E/'verification.json').as_posix(),'bodyRgbaChanged':True,'timingChanged':False,'weaponsChanged':False,'newPixelLabCalls':0,'runtimeImplemented':False}
# Correct inherited stale event metadata; no frames or durations are changed.
clip['contactEvent']={**clip['contactEvent'],'frame':6,'timeMs':290}
clip['armpitRepair']={'frames':{f:len(edits) for f,edits in plan.items()},'visualReviewRequired':True,'report':(E/'report.md').as_posix(),'alphaChanged':False,'contactMetadataCorrection':'Parent declared frame 7/325 ms; requested canonical impact is frame 6 start/290 ms. Only event metadata corrected; no frame timing, image or weapon translation.'}
# Historical fields explicitly refer to earlier repairs, not this pass.
clip['v7AxillaRepair']['historicalInheritedPass']=True
clip['reuseAssessment']['body']='Inherited V7; only 73 dark internal joint pixels in F03/F04/F05 re-lit. No silhouette/alpha edits.'
for fr in clip['frames']:fr['armpitV8ChangedPixels']=len(plan.get(str(fr['index']),[]))
def hashes(v):
 if isinstance(v,dict):
  for k,x in list(v.items()):
   if isinstance(x,str) and Path(x).is_file():
    hk=k+'Sha256'
    if hk in v:v[hk]=sha(x)
    if k=='png' and 'sha256' in v:v['sha256']=sha(x)
   hashes(x)
 elif isinstance(v,list):
  for x in v:hashes(x)
hashes(clip)
(D/'clip.json').write_text(json.dumps(clip,indent=2)+'\n')
results={};before=Counter();after=Counter()
for i in range(13):
 a=pixels(S/f'layers/body/{i:02}.png');b=pixels(D/f'layers/body/{i:02}.png')
 actual={(x,y) for y in range(256) for x in range(256) if a.getpixel((x,y))!=b.getpixel((x,y))}
 expected={(e['x'],e['y']) for e in plan.get(str(i),[])}
 assert actual==expected,(i,len(actual),len(expected))
 assert all(a.getpixel(p)[3]==b.getpixel(p)[3] for p in actual)
 assert all(all(v>=u for u,v in zip(a.getpixel(p)[:3],b.getpixel(p)[:3])) for p in actual)
 assert all(max(a.getpixel(p)[:3])<=34 for p in actual)
 for n in ['weaponBack','weaponFront','handFront']:
  assert (S/f'layers/{n}/{i:02}.png').read_bytes()==(D/f'layers/{n}/{i:02}.png').read_bytes()
  assert pixels(E/f'reopened-layers/{n}/{i:02}.png').tobytes()==pixels(D/f'layers/{n}/{i:02}.png').tobytes()
 assert pixels(D/f'frames/{i:02}.png').tobytes()==pixels(D/f'{i:02}.png').tobytes()
 if i not in [3,4,5]:assert pixels(S/f'{i:02}.png').tobytes()==pixels(D/f'{i:02}.png').tobytes()
 if actual:
  trans=Counter((a.getpixel(p),b.getpixel(p)) for p in actual)
  results[str(i)]={'bodyPixelsChanged':len(actual),'compositePixelsChanged':sum(x!=y for x,y in zip(pixels(S/f'{i:02}.png').getdata(),pixels(D/f'{i:02}.png').getdata())),'transitions':[{'before':list(u),'after':list(v),'count':n} for (u,v),n in sorted(trans.items())]}
 for p in actual:before[a.getpixel(p)]+=1;after[b.getpixel(p)]+=1
assert clip['durationsMs']==[30,65,35,50,45,65,35,35,100,55,80,45,90]
assert clip['visibleInterval']==old['visibleInterval']
# Independent comparison samples exported from saved sources; unmodified reference evidence.
refdir=E/'references';refdir.mkdir(exist_ok=True)
for j in range(4):
 for i in ([3,4,5] if j<3 else [0]):shutil.copyfile(f'tmp/armpit-source-{j}-{i}.png',refdir/f'source-{j}-F{i:02}.png')
shutil.copyfile('tmp/armpit-refs.png',refdir/'comparison.png')
shutil.copyfile('tmp/armpit-export.lua',E/'export-diagnostic-sources.lua')
protected=json.loads(Path('characters/orc-v1/source/combat-recovery-v7/frontal/full-front-r-sword/clip.json').read_text())
assert sha(protected['master'])==protected['masterSha256']
assert all(sha(f['png'])==f['sha256'] for f in protected['frames'])
verification={'status':'TECHNICALLY_COMPLETE','artisticStatus':'VISUAL_REVIEW_REQUIRED','frames':results,'totalBodyPixelsChanged':sum(len(v) for v in plan.values()),'allChangesExactlyMatchPlan':True,'noPixelDarkened':True,'allExistingHighlightsPreserved':True,'alphaUnchanged':True,'weaponAndHandLayersByteIdentical':True,'reopenedWeaponLayersMatch':True,'untargetedCompositeFramesRgbaIdentical':True,'durationsMs':clip['durationsMs'],'totalDurationMs':sum(clip['durationsMs']),'visibleInterval':clip['visibleInterval'],'impactTimeMs':290,'impactFrame':6,'protectedFrontRMasterAndFrameHashesMatch':True,'savedMasterReopenChecks':json.loads((E/'reopen-result.json').read_text()),'sourcePreservation':{p.as_posix():sha(p) for p in S.rglob('*') if p.is_file()},'candidateFiles':{p.as_posix():sha(p) for p in D.rglob('*') if p.is_file()}}
(E/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
lines=['# Axila front_l/Sword — candidato local V8','', '`TECHNICALLY_COMPLETE` · `VISUAL_REVIEW_REQUIRED` · `PENDING_CREATOR`','', '## Diagnostico antes de desenhar','', 'Foram abertos os mestres salvos no Aseprite e renderizados F03/F04/F05 do corpo front_l, front_r/Sword protegido, back_l/Sword V8 e F00 de Idle front_l. Evidencia: references/comparison.png (colunas nessa ordem; linhas F03, F04, F05; Idle apenas na primeira linha). A referencia traseira foi renderizada do composto salvo e contem equipamento; a juncao pode ser examinada sem usar a arma como evidencia anatomica.','', 'O retangulo aproximado x80..130/y60..120 informado no pedido cai predominantemente sobre cabeca, peito e o outro ombro no canvas 256 deste clipe. A juncao reclamada fica a direita da imagem: x147..158/y106..114. Tambem foi inspecionado o recorte aproximado indicado; nao foi usado para deslocar ou espelhar anatomia.','', 'Contorno legitimo medido: rgb(0,0,1), (2,2,3), (6,6,8). Sombra interna principal: rgb(20,20,26), com transicao (27,28,34) e metal sombreado (43,45,49). Idle usa as mesmas cores; front_r inclui metal (33,34,40)/(49,51,55) e back_l (26,26,32)/(33,34,40). Os numeros sao amostras reais dos mestres, nao uma paleta universal.','', 'Nao foi encontrada cor estranha responsavel pelo defeito. A faixa interna usa cores legitimas de contorno e sombra em area extensa: essa distribuicao funde a ligacao do deltoide ao tronco numa massa quase preta. Existe continuidade alfa opaca; o vazio transparente abaixo do braco e espaco externo, nao deve ser preenchido indiscriminadamente. Minha leitura visual e de perda de volume na juncao, nao de um pixel com cor ilegal.','', '## Reparo e procedencia','', 'Autoria programatica Lua executada no Aseprite, em copia isolada dos mestres V7. Reiluminacao de uma superficie curta e escalonada de cota/metal na ligacao interna, com tons existentes (27,28,34)/(43,45,49); contorno externo, alpha, tecido vermelho e highlights preservados. Nao se pintou outra placa de tinta na borda nem se preencheu todo o espaco negativo. A textura pretende explicitar a ligacao sob o deltoide; sua aceitacao perceptual continua pendente do criador.','', 'Plano exato com coordenadas e RGBA antes/depois: edit-plan.json. Script: author-armpit.lua. Mestres composto, corpo e nativo foram salvos, reabertos e reexportados; verificacoes no proprio Aseprite em reopen-result.json. 219 escritas correspondem aos mesmos 73 pixels nas tres representacoes, nao a 219 pixels diferentes.','', '## Diferencas medidas','', '| Quadro (indice 00) | Corpo | Composto visivel |','|---|---:|---:|']
for f,v in results.items():lines.append(f"| F{int(f):02} | {v['bodyPixelsChanged']} | {v['compositePixelsChanged']} |")
lines+=['','Todas as transicoes abaixo sao RGBA com alfa 255. Nenhum canal RGB diminuiu.','', '| Quadro | RGB antes | RGB depois | Pixels |','|---|---|---|---:|']
for f,v in results.items():
 for t in v['transitions']:lines.append(f"| F{int(f):02} | {tuple(t['before'][:3])} | {tuple(t['after'][:3])} | {t['count']} |")
lines+=['','## Provas e limites','', '- zoom/armpit-before.png e zoom/armpit-after.png, na pasta pai: ampliacao exata 8x nearest-neighbour, ROI [136,96,176,132), colunas F03/F04/F05; linha superior corpo layers-off, inferior composto. Fundo cinza e apenas da superficie de revisao.','- 13 quadros; duracoes 30,65,35,50,45,65,35,35,100,55,80,45,90 ms; total 730 ms. Janela armada [2,10] preservada. Nenhuma posicao/rotacao de arma alterada; tres camadas weaponBack/weaponFront/handFront byte-identicas em todos os quadros.','- Metadado herdado contactEvent apontava F07/325 ms, inconsistente com o impacto de 290 ms solicitado. No novo clip.json foi corrigido apenas para F06/290 ms (inicio de F06); os tempos e pixels desses quadros continuam identicos.','- Zero diferencas RGBA nos dez compostos fora de F03/F04/F05. Todos os 73 pixels alterados tinham max(R,G,B)<=34, logo nenhum highlight existente foi apagado. Alpha e silhueta identicos em todos os quadros.','- Igualdade do corpo do composto com body.aseprite e do recorte [64,64] com native.aseprite conferidas apos reabrir. Hashes de mestre e 13 compostos de front_r/Sword protegido conferidos contra seu contrato.','- Candidata entregue separadamente em characters/orc-v1/source/combat-recovery-v8/frontal-armpit/front_l-sword/clip.json. Patch e matriz V8 nao alterados. Sem commit, Unity, IA generativa ou PixelLab.','', 'O passe foi inspecionado em quadros estaticos ampliados e na referencia do corpo inteiro. Nao houve novo QA independente nem avaliacao temporal em 1x nesta tarefa. A melhora proposta nao concede aprovacao artistica; a leitura da juncao deve ser reavaliada pelo criador.']
(E/'report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({'frames':results,'checks':'PASS'},indent=2))
