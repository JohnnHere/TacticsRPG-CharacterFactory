import json,hashlib,math
from pathlib import Path
from PIL import Image
E=Path('experiments/main-orc-combat-recovery-v7/rear-r'); C=Path('characters/orc-v1/source/combat-recovery-v7/rear-r');E.mkdir(parents=True,exist_ok=True)
a=json.loads(Path('experiments/main-orc-artistic-reconstruction-v6/rear/back-r-stage-d/anatomy-plan.json').read_text())
snapshot={}; plan={}; audits=[]
for kind in ['Sword','Axe']:
 src=Path('characters/orc-v1/source/artistic-reconstruction-v6/rear/back_r-'+kind.lower());clip=json.loads((src/'clip.json').read_text())
 for p in src.rglob('*'):
  if p.is_file():snapshot[p.as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
 rows=[]
 for f in clip['frames']:
  i=f['index']; p=a[kind][i]; g=p['grip']; ang=p['angle'];rad=math.radians(ang);n=(math.cos(rad),math.sin(rad)); t=(-math.sin(rad),math.cos(rad));dx=dy=0
  if kind=='Axe' and i in [2,3,4,5]:dx=2
  if kind=='Axe' and i in [6,7,8,9]:dy=-1
  if kind=='Sword' and i==3:dx=1
  im=Image.open(f['layers']['handFront']['png']).convert('RGBA'); coords=[(x-64,y-64) for y in range(256) for x in range(256) if im.getpixel((x,y))[3]]
  projection=[(x-g[0])*n[0]+(y-g[1])*n[1] for x,y in coords]
  mean=sum(projection)/len(projection) if projection else None
  clean=[];b=Image.open(f['layers']['body']['png']).convert('RGBA')
  for y in range(65,191):
   for x in range(65,191):
    r,gg,bb,al=b.getpixel((x,y))
    if al and min(r,gg,bb)>=140 and max(r,gg,bb)-min(r,gg,bb)<28:
     nb=[b.getpixel((x+xx,y+yy)) for xx,yy in [(1,0),(-1,0),(0,1),(0,-1)]]
     if any(v[3]==0 for v in nb) and not any(min(v[:3])>=120 and v[3] for v in nb):clean.append([x,y])
  row={'index':i,'grip':[g[0]+64+dx,g[1]+64+dy],'originalGrip':f['rightGrip'],'shift':[dx,dy],'angle':ang,'rows':p['rows'],'bodyHaloCandidates':clean,'handNormalExtent': [round(min(projection),3),round(max(projection),3)] if projection else None,'handMeanNormalOffset':round(mean,3) if mean is not None else None,'classification':'TARGETED_PIXEL_FIX' if 1<=i<=9 or clean else 'KEEP','phase':f['phase'],'durationMs':f['durationMs']}
  rows.append(row)
 plan[kind]={'source':src.as_posix(),'dest':(C/('back_r-'+kind.lower())).as_posix(),'clip':clip,'frames':rows}
(E/'plan.json').write_text(json.dumps(plan,indent=2));(E/'input-hashes.json').write_text(json.dumps(snapshot,indent=2))
lines=['# Auditoria antes da autoria','', 'Coordenadas compostas; F03 = índice 03 (quarta pose). Medidas da máscara de luva são diagnóstico de suporte, não identificação automática da palma. Eixo longitudinal t=(-sin θ,cos θ), normal n=(cos θ,sin θ). Valores negativos/positivos indicam lados do cabo.','']
for k,v in plan.items():
 lines+=['## '+k,'','| F | Classe | Fase/ms | Grip V6 | média normal da luva (px) | extensão normal | ajuste de assento |','|---|---|---|---|---|---|---|']
 for p in v['frames']:lines.append(f"| {p['index']:02} | {p['classification']} | {p['phase']}/{p['durationMs']} | {p['originalGrip']} | {p['handMeanNormalOffset']} | {p['handNormalExtent']} | {p['shift']} |")
lines+=['','Axe F03/F04: máscara longa longitudinalmente inclui punho/bracelete, mas não define dedos curvados. A projeção do cabo passa pela borda esquerda superior da luva enquanto a massa metálica/punho continua abaixo e à direita; o problema visual é fechamento ausente e leitura de apoio inferior. O cabo já estava em weaponBack: não se trata simplesmente de uma camada frontal errada. A rotação e a posição do pomo não são a causa comprovada. Reparo: assento 2 px para dentro da palma nos frames 02–05, reconstrução local de couro/dedos e polegar em ambas as faces do eixo; impacto/recovery sobem assento 1 px. Nenhuma rotação nova.','', 'Sword: preservar pernas, apoios e tronco (não há justificativa para reconstruí-los neste passe); reforçar fechamento da luva em cada pose, assento de F03 +1 px, preservar progressão angular V6 e diferenciação Sword/Axe. Identidade frontal lida: Sword apex breve/release/contact/follow-through; Axe overhead-coil longo/heavy-impact/weight-settle. Tempos traseiros preservados por contrato. Compatibilidade com back_l V7 fica pendente da outra sessão.']
(E/'audit.md').write_text('\n'.join(lines),encoding='utf-8')
