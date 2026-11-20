import json,math,hashlib
from pathlib import Path
E=Path('experiments/main-orc-combat-recovery-v7/rear-r');m=json.loads((E/'grip-metrics.json').read_text());plan=json.loads((E/'plan.json').read_text());lines=['','## Eixo do punho e oclusão — Axe (medição adicional)','','Marcos de punho selecionados visualmente na junção luva/antebraço; não são centróides automáticos. n é normal ao cabo, t aponta para a cauda/pomo. Coordenadas compostas.','','| F | punho corporal (x,y) | cabo antes → depois | punho n/t antes (px) | punho n/t depois (px) | oclusão item antes→depois |','|---|---|---|---|---|---|']
wrists={3:[160,93],4:[155,91],7:[162,153]}
for row in m['Axe']:
 i=row['frame']
 if i not in wrists:continue
 p=plan['Axe']['frames'][i];w=wrists[i];n=row['axis']['normal'];t=row['axis']['towardPommel']
 def rel(g):return [round(sum((w[j]-g[j])*v[j]for j in range(2)),3)for v in [n,t]]
 row['observedWrist']=w;row['wristNormalLongitudinalBefore']=rel(p['originalGrip']);row['wristNormalLongitudinalAfter']=rel(p['grip'])
 lines.append(f"| {i:02} | {w} | {p['originalGrip']} → {p['grip']} | {rel(p['originalGrip'])} | {rel(p['grip'])} | {row['handCoversItemPixelsBefore']}→{row['handCoversItemPixelsAfter']} |")
lines+=['','Em F03/F04, punho está longitudinalmente abaixo da palma e do lado normal positivo; na imagem elevada, isso corresponde a baixo/direita. Em F07, punho está acima/esquerda da palma, com normal negativa. Esses marcos foram preservados: a correção fecha a palma ao redor do eixo e não desloca o bracelete para simular nova mão. Os pixels reautorados têm projeções dos dois sinais da normal nas três poses (coordenadas em grip-metrics.json). A contagem de sobreposição é quase igual antes/depois: demonstra por que contagem de contato e socket V6 não eram prova de boa pegada.','', 'Contorno: após o passe, 0 pixels claros neutros (mínimo RGB ≥140, amplitude RGB <28) expostos ao alfa na silhueta composta dos 24 quadros. Nenhum contorno corporal confirmou o critério de reparo; 0 pixels corporais de halo foram apagados. O reparo claro foi restrito ao item. Esse diagnóstico não equivale a afirmar ausência universal de flicker artístico.','', 'Preview verificado em Edge/Chromium headless: 96 comparações canvas↔PNG exatas (antes/depois × corpo/composto × 12 quadros × 2 ações), controles e carregamento HTTP/file, sem erro JavaScript. Screenshot: preview-check.png.']
(E/'grip-metrics.json').write_text(json.dumps(m,indent=2));r=E/'report.md';r.write_text(r.read_text(encoding='utf-8')+'\n'+'\n'.join(lines),encoding='utf-8')
# Handoff freezes only the final deliverables, not a misleading production promotion.
clips=[]
for k,v in plan.items():
 p=Path(v['dest'])/'clip.json';clips.append({'direction':'back_r','action':k,'clip':p.as_posix(),'clipSha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(E/'handoff.json').write_text(json.dumps({'checkpoint':'V7_BACK_R_REFINED','technicalStatus':'TECHNICALLY_COMPLETE','artisticStatus':'VISUAL_REVIEW_REQUIRED','creatorApproval':'PENDING_CREATOR','runtimeImplemented':False,'pixelLabCalls':0,'clips':clips,'report':(E/'report.md').as_posix(),'preview':(E/'preview.html').as_posix(),'gripEvidence':[(E/f'grip-{i:02}-{when}.png').as_posix()for i in [3,4,7]for when in ['before','after']]},indent=2))
print('V7_BACK_R_REFINED')
