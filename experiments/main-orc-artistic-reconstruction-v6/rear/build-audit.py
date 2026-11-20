import json
from pathlib import Path

O = Path(__file__).parent
details = {
 'l-sword': [
  'Guarda desarmada: referência de identidade e apoio.',
  'Levantamento sem contrarrotação suficiente do quadril.',
  'Elevação comandada pelo braço; pernas quase iguais à guarda.',
  'Punho sobe abruptamente; encadear escápula e cotovelo.',
  'Punho salta para fora e para baixo no ápice, quebrando arco diagonal.',
  'Lâmina cruza dorsal com punho alto e pouca participação do tronco.',
  'Arco de 05 para 06 não conduz continuamente ao impacto baixo.',
  'Punho desce abruptamente ao quadril, sem peso corporal suficiente.',
  'Follow-through curto e semelhante ao impacto.',
  'Retorno inferior muda stance mais do que recupera o torso.',
  'Retorno à guarda sem desaceleração encadeada.',
  'Bookend igual ao início: preservar como referência.'],
 'l-axe': [
  'Guarda desarmada: referência de identidade.',
  'Punho elevado antes da transferência de peso.',
  'Antebraço ascende com tronco pouco comprometido.',
  'Braço horizontal sobre cabeça; dobra requer reconstrução.',
  'Sustentação alta não prepara queda corporal contínua.',
  'Cabeça do item reaparece no outro lado; revisar orientação com punho.',
  'Salto para tronco inclinado e braço lateral sem transição suficiente.',
  'Impacto repete inclinação em vez de absorver peso nos joelhos.',
  'Retorno abrupto do tronco, item acompanha quadril.',
  'Recuperação volta quase diretamente à guarda.',
  'Recuperação pouco distinta do bookend.',
  'Guarda final: referência de fechamento.'],
 'r-sword': [
  'Guarda de referência.', 'Entrada: checar continuidade do apoio.',
  'Preparação pode sustentar ajuste localizado.',
  'Encadear antecipação de ombro e quadril.',
  'Perna de apoio muda inclinação enquanto braço estende.',
  'Joelho e bota alteram stance na aceleração.',
  'Punho e perna mudam sem transferência clara.',
  'Contato baixo exige apoio coerente com 06.',
  'Follow-through mantém base incompatível com guarda.',
  'Recuperação abrupta de joelho e quadril.',
  'Rever duração do retorno depois de corrigir pernas.',
  'Guarda final de referência.'],
 'r-axe': [
  'Guarda de referência.', 'Entrada requer ajuste localizado do ombro.',
  'Levantamento pode sustentar ajuste localizado.',
  'Preparação alta exige revisão da cadeia articular.',
  'Ápice similar a 03: rever sustentação depois da mecânica.',
  'Saída alta não antecipa inclinação suficiente.',
  'Braço e inclinação mudam abruptamente.',
  'Impacto inclina mais que o apoio anterior sustenta.',
  'Recuperação lateral exige continuidade dos joelhos.',
  'Quadril retorna rapidamente sem absorção contínua.',
  'Pose quase igual à guarda: rever duração.',
  'Guarda final de referência.']}
rows=[]
clips=[]
for side in ['l','r']:
 for kind in ['sword','axe']:
  c=json.loads(Path(f'characters/orc-v1/source/combat-rescue-v5/rear-grip-flash/full-back-{side}-{kind}/clip.json').read_text(encoding='utf-8'))
  clips.append(c)
  for i,f in enumerate(c['frames']):
   cls='KEEP' if i in [0,11] else 'REAUTHOR_KEYFRAME'
   if side=='r' and i in [1,2]: cls='TARGETED_PIXEL_FIX'
   if side=='r' and i==10: cls='TIMING_FIX'
   rows.append(dict(cell=f'back_{side}/{kind.title()}',frame=i,classification=cls,reason=details[f'{side}-{kind}'][i],durationMs=f['durationMs']))
(O/'audit.json').write_text(json.dumps(dict(status='VISUAL_REVIEW_REQUIRED',frames=rows),ensure_ascii=False,indent=2),encoding='utf-8')
html='''<!doctype html><meta charset="utf-8"><title>V6 rear - auditoria V5</title>
<style>body{background:#33313b;color:#eee;font:16px sans-serif}canvas{image-rendering:pixelated;background:#55505d}section{display:inline-block;margin:14px}button,select{font:inherit}</style>
<h1>V5 rejeitada - auditoria traseira</h1><button onclick="playing=!playing">Play / pause</button><button onclick="step()">Passo</button><select id="speed"><option value="1">1x</option><option value="0.5">0,5x</option></select><select id="scale"><option value="1">Nativo 1x</option><option value="0.5">Tático 0,5x</option><option value="2">Zoom 2x</option></select><div id="clips"></div>
<script>const clips=DATA;let playing=true,time=0,last=0,manual=0;const views=[];
for(const c of clips){const s=document.createElement('section');s.innerHTML='<h2>'+c.direction+'/'+c.category+'</h2>';for(const mode of ['body','composite']){const label=document.createElement('div');label.textContent=mode;s.append(label);const cv=document.createElement('canvas');cv.width=cv.height=256;s.append(cv);const imgs=c.frames.map(f=>{const im=new Image();im.src='../../../'+(mode==='body'?f.layers.body.png:f.png);return im});views.push({c,cv,imgs})}document.querySelector('#clips').append(s)}
function step(){playing=false;manual=(manual+1)%12;draw()}
function draw(){for(const v of views){let t=time%v.c.totalDurationMs,i=0;if(playing){while(i<11&&t>=v.c.frames[i].durationMs){t-=v.c.frames[i].durationMs;i++}}else i=manual;v.cv.style.width=v.cv.style.height=(256*Number(scale.value))+'px';const x=v.cv.getContext('2d');x.clearRect(0,0,256,256);if(v.imgs[i].complete)x.drawImage(v.imgs[i],0,0)}}
function tick(n){if(last&&playing)time+=(n-last)*Number(speed.value);last=n;draw();requestAnimationFrame(tick)}requestAnimationFrame(tick);</script>'''
(O/'audit-preview.html').write_text(html.replace('DATA',json.dumps(clips)),encoding='utf-8')
(O/'audit.md').write_text('# Etapa A — auditoria V5 rejeitada\n\nVISUAL_REVIEW_REQUIRED. Corpo inteiro layers-off e composto inspecionados em folhas, sem declarar aprovação. KEEP conserva referência de identidade, não valida o ataque. A leitura temporal deve ser confrontada com audit-preview.html em 1×.\n\n| Célula | Quadro | Classificação | Justificativa |\n|---|---:|---|---|\n'+'\n'.join(f"|{r['cell']}|F{r['frame']:02}|{r['classification']}|{r['reason']}|" for r in rows)+'\n',encoding='utf-8')
