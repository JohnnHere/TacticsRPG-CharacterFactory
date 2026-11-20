from pathlib import Path
import json,hashlib,datetime
E=Path('experiments/main-orc-combat-rescue-v5/grip-specialist/F02-F08');C=Path('characters/orc-v1/source/combat-rescue-v5/grip-specialist')
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def write(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
snap=read(E/'input-snapshot.json');checks=read(E/'checks.json');preview=read(E/'preview-check.json')
assert all(sha(p)==h for p,h in snap['files'].items());old=read(snap['F06Freeze']);assert all(sha(r['path'])==r['sha256']for r in old['files'])
assert checks['status']=='TECHNICALLY_COMPLETE'and preview['status']=='PASS'
reps={key:read(C/key/'representative.json')for key in ['F02','F08']}
sources=''
for key,r in reps.items():
 sources+=f'''### {key}

- [representative.json](../../../../{str(C/key/'representative.json').replace(chr(92),'/')}): SHA-256 `{sha(C/key/'representative.json')}`.
- Composto256: `{r['frames'][0]['png']}`, SHA-256 `{r['frames'][0]['sha256']}`.
- Mestre composto: `{r['master']}`, SHA-256 `{r['masterSha256']}`.
- Mestre corpo256: `{r['bodyMaster']}`, SHA-256 `{r['bodyMasterSha256']}`.
- Mestre corpo128: `{r['nativeMaster']}`, SHA-256 `{r['nativeMasterSha256']}`.
- Corpo nativo128: `{r['frames'][0]['nativePng']}`, SHA-256 `{r['frames'][0]['nativeSha256']}`.

'''
report=f'''# Grip especialista — front_r/Sword F02 e F08

**GRIP_F02_F08_READY · TECHNICALLY_COMPLETE no empacotamento dos dois representantes · VISUAL_REVIEW_REQUIRED · PENDING_CREATOR.**

Entrega limitada a **F02 e F08**, para QA **GLM5.3/Cline organizado pelo Root**. Não há autorização de propagação, ciclo13f, outros grips ou matriz. A tarefa artística completa não é declarada encerrada. Nenhum QA/agente foi criado dentro do DEV.

[Preview local](index.html) · [checkpoint](checkpoint.json) · [checks](checks.json) · [F02 antes/depois](F02-before-after.png) · [F08 antes/depois](F08-before-after.png) · [anatomia F02](F02-anatomy-annotated.png) · [anatomia F08](F08-anatomy-annotated.png).

## Continuidade e preservação de F06

Foi lido o parecer `qa-grok/representative-sol-F06.json`: **READY_FOR_F02_F08_AND_FULL_CLIP_EXPLORATION**, restrito ao representante F06. A correção anatômica confirmada pelo próprio QA foi respeitada: o braço ativo cruza o corpo e a mão baixa junto ao quadril é inativa. Isso não aprova outros quadros ou a matriz.

Os54 arquivos do freeze anterior continuam SHA-256 idênticos, inclusive fontes, exports, representante, scripts, relatório e preview de F06. O freeze original permanece `{snap['F06FreezeSha256']}`. Novos scripts/evidências/checkpoint estão neste subdiretório `F02-F08/`, evitando regravar qualquer arquivo congelado de F06.

## Anatomia rastreada em cada corpo real

Os dois `frame.layers.body.png` foram abertos sem armas, ampliados em nearest-neighbor e examinados em grade. Os marcos abaixo são interpretações da arte achatada, não esqueleto recuperado ou coordenadas de tabela reaproveitadas. `anatomy.json`, os PNGs `*-body-source.png`, `*-palm-grid.png` e as imagens anotadas registram essa leitura.

| Marco no composto256 | F02 | F08 |
|---|---|---|
| Ombro de ataque |109,107|118,107|
| Cotovelo |98,117|131,128|
| Antebraço |97,122|146,142|
| Borda distal da braçadeira |99,127|154,143|
| Pulso |100,129|156,145|
| Palma / grip proposto |**103,130**|**159,148**|
| Nós dos dedos |105,132|162,148|

**F02:** o braço direito anatômico está à esquerda da imagem, descendo da ombreira, passando pelo cotovelo e pela braçadeira até a luva marrom baixa. A outra mão, à direita da imagem, permanece inativa. O item sai para cima/esquerda, fora do antebraço, com guarda acima da mão e pomo saindo para baixo/direita.

**F08:** o braço ativo cruza diagonalmente o abdômen. A massa metálica larga do antebraço termina na luva marrom **abaixo e à direita**, em aproximadamente x156..164/y146..151. O couro vertical acima, perto de `(155,136)`, pertence ao braço inativo sobreposto. A nova raiz não foi deixada sobre a chapa do antebraço. A lâmina sai para baixo/direita a partir da luva baixa; a guarda fica além da mão e o pomo junto da borda superior do punho. A leitura do pomo sobre a projeção da braçadeira deve ser julgada pelo QA, sem presumir que contagem de contato a demonstra.

## Montagem e oclusão

O mesmo item independente preservado `combat/weapons/Sword/weapon.json` foi usado, sem alterar pixels, materiais, tamanho ou grip do item `(48,66)`. Transformações propostas:

- **F02:** grip do corpo `(103,130)`,320°, escala1, sem espelhar;35ms.
- **F08:** grip do corpo `(159,148)`,128°, escala1, sem espelhar;100ms.

Cada fonte tem `weaponBack → body → weaponFront → handFront`. A seção de couro da empunhadura do item passa atrás da mão existente; lâmina, guarda e pomo permanecem independentes à frente. `handFront` copia somente linhas traçadas da **respectiva luva real**: F02 x101..105/y128..133; F08 x157..162/y146..150. Não foi usada a palma `(155,114)` de F06 nem sua máscara. Não houve palma fixa, dilatação, cuffbridge, desenho geométrico de dedos ou mudança de pose.

Não foi necessário redesenhar pixels destas duas luvas: seus clusters já fornecem a leitura de mão fechada. `handFront` usa21 e23 posições existentes, respectivamente, **sem retoque de cor**. Os números descrevem o escopo e não são critério de aceitação anatômica. A inspeção estática local do corpo inteiro e das pegadas fundamenta encaminhar os representantes ao QA; não substitui seu veredito nem demonstra o ataque inteiro em movimento.

## Mestres e exports reais

Cada chave tem seu próprio `representative.json`, três mestres Aseprite (composto256, corpo256 e corpo128), quatro camadas PNG256, composto completo256 e corpo nativo128. Os índices internos0 representam somente F02/F08 de origem, com a duração individual preservada. Não são clipes completos para substituir o ataque.

**F02** também possui crop composto128 e camadas128 íntegros. **F08 não entrega um composto128 cortado:**144 pixels do equipamento ficam além do retângulo do corpo128, dentro do composto256 completo. O corpo128 está íntegro. A espada não foi encolhida nem rotacionada para esconder esse limite; o contrato existente256 com `bodyOffset=[64,64]` é utilizado. O preview de canvas128 é a exibição a0,5× do composto completo, com corpo aproximadamente64px, não um asset de arma comprimida.

{sources}
Todos os caminhos/hashes de camadas, itens e transformações estão nos dois `representative.json`.

## Verificação focada e custos

`checks.json` registra, nos dois quadros: corpo com **zero diferença RGBA visível**, tempos35/100ms preservados nos cabeçalhos salvos, decodificação independente dos cels reais/posições igual aos exports, alfa-over exato e transformação do item conferindo com seus pixels originais. A imagem completa256 não perde pixels do item; a limitação do crop128 em F08 está declarada. Os10 arquivos de entrada inventariados permanecem idênticos. F06 foi reconferido por seus54 hashes, sem reautoria ou inspeção redundante da arte antiga.

As diferenças visíveis versus os respectivos compostos rejeitados `qa5-repair1` são904 posições em F02 e961 em F08; esses valores não medem qualidade. O preview `index.html` foi aberto por file:// em Edge headless: imagens carregadas, camadas alternadas/restauradas exatamente e escalas de canvas128/256 verificadas. Os dois representantes são estáticos; nenhum loop ou leitura temporal foi alegado.

Autoria, gravação e exportação de produção ocorreram exclusivamente em Aseprite1.3.18.6, oculto `--batch --noinapp`, perfil exclusivo `tmp/aseprite-grip-specialist-profile`, timeout90s. Foi uma execução local para os dois quadros. Pillow/NumPy somente leram/validaram pixels e montaram evidência diagnóstica. A GUI interativa não foi tocada.

**Novas chamadas/gerações PixelLab:0.** Não houve bloqueio que exigisse geração nesta pegada local. Não houve instalação, commit, escrita em Unity ou alteração dos corpos de outro DEV. Idle/Hit/Walk/Defeat/Unarmed, corpos traseiros, itens independentes, matriz, docs e integração permanecem fora das escritas.

## Próximo portão

Parada em **GRIP_F02_F08_READY**. `representativeAcceptableForPropagation=false` significa **pendente do QA GLM5.3/Cline solicitado pelo Root**. `eligibleForIntegration=false`; nenhuma expansão automática para13 quadros ou oito grips foi feita.

O contrato futuro `integrate.mjs --weapon-patch ...` foi registrado como orientação posterior: oito células completas, `parentManifestSha256=f250f7a11ceb0e851c9a3c34f8c20e75c48da5a04e0a2229933945298aaf4017`, armas independentes preservadas. **Nenhum patch desse tipo foi produzido nesta etapa.** Corpos traseiros futuros continuam dependentes do especialista e do QA indicados pelo Root; fontes rejeitadas não foram selecionadas como finais.
'''
(E/'report.md').write_text(report,encoding='utf-8')
checkpoint={'checkpoint':'GRIP_F02_F08_READY','scope':'ONLY front_r/Sword F02,F08','sourceFrameIndices':[2,8],'technicalStatus':'TECHNICALLY_COMPLETE','artisticStatus':'VISUAL_REVIEW_REQUIRED','globalTaskStatus':'ARTISTIC_REVISION_REQUIRED','artisticApproval':'PENDING_CREATOR','nextIndependentQA':'Root-owned GLM5.3/Cline','representativeAcceptableForPropagation':False,'eligibleForIntegration':False,'F06Preserved':True,'F06FreezeSha256':snap['F06FreezeSha256'],'F06FrozenFilesPreserved':54,'newPixelLabCalls':0,'fullClipAuthored':False,'eightGripPatchAuthored':False,'representatives':{k:{'path':str(C/k/'representative.json').replace('\\','/'),'sha256':sha(C/k/'representative.json'),'masterSha256':reps[k]['masterSha256']}for k in reps},'report':str(E/'report.md').replace('\\','/'),'reportSha256':sha(E/'report.md'),'checksSha256':sha(E/'checks.json'),'preview':str(E/'index.html').replace('\\','/'),'nextStep':'Root reviews exactly these2 representatives with GLM5.3/Cline; no full cycle/eight-grip production before its verdict.'}
(E/'snapshot').mkdir(exist_ok=True);write(E/'checkpoint.json',checkpoint);write(E/'snapshot/checkpoint.json',checkpoint)
files=sorted(p for base in [E,C/'F02',C/'F08']for p in base.rglob('*')if p.is_file()and '__pycache__'not in p.parts and p.name!='freeze.json')
freeze={'schemaVersion':1,'checkpoint':'GRIP_F02_F08_READY','createdAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'eligibleForIntegration':False,'artisticStatus':'VISUAL_REVIEW_REQUIRED','scope':'Only F02/F08 representative sources, exports and handoff; original F06 files excluded/preserved','F06FreezeSha256':snap['F06FreezeSha256'],'reportSha256':checkpoint['reportSha256'],'checksSha256':checkpoint['checksSha256'],'representatives':checkpoint['representatives'],'fileCount':len(files),'files':[{'path':str(p).replace('\\','/'),'sizeBytes':p.stat().st_size,'sha256':sha(p)}for p in files]}
write(E/'snapshot/freeze.json',freeze);assert all(sha(r['path'])==r['sha256']for r in freeze['files']);assert all(sha(r['path'])==r['sha256']for r in old['files']);assert all(sha(p)==h for p,h in snap['files'].items())
print(json.dumps({'checkpoint':checkpoint['checkpoint'],'freezeSha256':sha(E/'snapshot/freeze.json'),'reportSha256':checkpoint['reportSha256'],'representatives':checkpoint['representatives'],'filesFrozen':len(files),'F06Preserved':True,'eligibleForIntegration':False},indent=2))
