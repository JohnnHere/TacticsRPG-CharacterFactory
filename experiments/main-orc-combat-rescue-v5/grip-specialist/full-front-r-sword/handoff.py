from pathlib import Path
import json,hashlib,datetime
E=Path('experiments/main-orc-combat-rescue-v5/grip-specialist/full-front-r-sword');C=Path('characters/orc-v1/source/combat-rescue-v5/grip-specialist/full-front-r-sword')
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def write(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
clip=read(C/'clip.json');checks=read(E/'checks.json');preview=read(E/'preview-check.json');snap=read(E/'input-snapshot.json')
assert checks['status']=='TECHNICALLY_COMPLETE'and preview['status']=='PASS';assert clip['frameCount']==13 and clip['totalDurationMs']==730
assert all(sha(p)==h for p,h in snap['files'].items())
for p,h in snap['preservedFreezes'].items():
 assert sha(p)==h;f=read(p);assert all(sha(r['path'])==r['sha256']for r in f['files'])
gate='experiments/main-orc-combat-rescue-v5/qa-sol/grip-F02-F08-result.json';gateData=read(gate);assert gateData['verdict']=='READY_FOR_FULL_CLIP_EXPLORATION'
report=f'''# Grip especialista — ciclo completo front_r/Sword

**GRIP_FRONT_R_SWORD_FULL_READY · TECHNICALLY_COMPLETE · VISUAL_REVIEW_REQUIRED · PENDING_CREATOR.**

Entrega de **um único ciclo completo**, `front_r/Sword`,13 quadros/730ms, para QA independente organizado pelo Root, **sem Copilot**. Não é aprovação artística do ciclo, dos demais grips ou da matriz; `eligibleForIntegration=false`. Nenhum QA/agente/orquestrador foi criado dentro do DEV.

[Abrir player1×/lento/tático](index.html) · [clip.json](../../../../{str(C/'clip.json').replace(chr(92),'/')}) · [checkpoint](checkpoint.json) · [checks técnicos](checks.json) · [sequência completa](all-final-frames.png) · [seis grips novos](new-grips-final.png) · [luvas reais anotadas](new-gloves-source-annotated.png).

## Autorização, fonte e escopo

O parecer independente Sol/Codex `qa-sol/grip-F02-F08-result.json` foi lido: `READY_FOR_FULL_CLIP_EXPLORATION`, estático somente. SHA-256 `{sha(gate)}`. Ele não autorizava expansão automática; a execução do ciclo foi autorizada pelo Root na mensagem de continuidade `a499b869-ed41-4967-8da3-3e15a1aaf6fe`.

Corpos e relógio são os13 quadros frontais existentes de `combat/qa5-repair1/front_r/Sword/clip.json`. Esses corpos eram válidos; suas antigas armas/máscaras rejeitadas não foram reutilizadas como solução. Os corpos traseiros bloqueados em BODY-01 não foram abertos, selecionados ou alterados.

Escritas artísticas exclusivamente em `characters/orc-v1/source/combat-rescue-v5/grip-specialist/full-front-r-sword/`; scripts/evidências/handoff neste novo subdiretório de experiments. Todos os107 registros dos dois freezes anteriores de F06 e F02/F08 permanecem SHA-256 idênticos. Os50 arquivos de entrada inventariados também permanecem idênticos. Não houve regravação dos representantes anteriores, matriz, docs globais, outras três armas frontais, quatro traseiras, outros estados, itens independentes, produção ativa ou Unity.

## Corpo, palma e trajetória

Todos os13 corpos foram vistos em sequência, sem arma. F03/F04/F05/F07/F09/F10 receberam inspeção independente da luva/pulso em grades; `anatomy.json` registra ombro, cotovelo, antebraço, pulso e palma interpretados em cada pose equipada. São marcos visuais da arte achatada, não dados esqueletais recuperados.

**F02/F06/F08:** suas quatro camadas e compostos são RGBA visíveis exatos dos representantes que tiveram parecer estático favorável. A máscara de F06, inclusive os nove retoques internos já existentes, não foi propagada aos outros quadros.

**F03:** luva marrom frontalizada/encurtada na esquerda da imagem, palma `(90,119)`, após o cotovelo recolhido e o cuff metálico que contorna sua base. **F04:** luva marrom recurvada levantada junto à ombreira, palma/sombra interna `(98,100)`, com antebraço dobrado vindo de baixo/esquerda. **F05:** punho alto `(98,89)`, acima do pulso e antebraço. O ponto escuro de F04 foi interpretado no interior da luva visível, não escolhido sobre o torso por tabela antiga.

**F07:** o antebraço ativo cruza o corpo e termina na cunha marrom `(158,132)`, abaixo da posição de F06. **F09:** mão ativa recua para `(134,147)`, abaixo do cuff largo, separada do punho inativo da direita. **F10:** a manopla escura abaixo da braçadeira pendente, à esquerda do tasset vermelho, termina em `(110,150)`; o tecido vermelho não foi usado como palma.

| Quadro | Grip observado | Orientação do item |
|---|---|---:|
|F02|103,130|320°|
|F03|90,119|340°|
|F04|98,100|350°|
|F05|98,89|0° (=360° contínuo)|
|F06|155,114|32° (=392°)|
|F07|158,132|80° (=440°)|
|F08|159,148|128° (=488°)|
|F09|134,147|118° (=478°, recuo)|
|F10|110,150|100° (=460°, recuperação)|

O arco proposto cresce durante a preparação/descida e reverte gradualmente na recuperação. A raiz acompanha a mão real de cada corpo. Na recuperação, a orientação baixa/frontal mantém a lâmina acima do solo; a arma não foi simplesmente virada para baixo atravessando o chão. Isso descreve a intenção e a inspeção local em poses; a naturalidade em movimento precisa do parecer do ciclo.

## Grasp e profundidade

O item independente preservado continua em `combat/weapons/Sword/weapon.json`, grip próprio `(48,66)`, escala1, sem espelhamento ou retoque de material. Cores e silhueta transformadas foram conferidas contra esse item em todos os nove quadros visíveis.

Ordem: `weaponBack → body → weaponFront → handFront`. A seção de couro da empunhadura fica atrás da própria mão; lâmina, guarda e pomo permanecem independentes à frente. Nas seis poses novas, `handFront` copia exclusivamente linhas traçadas da respectiva luva original. Não há máscara fixa, centro extrapolado de F06, carimbo geométrico, cuffbridge ou mão inventada sobre a braçadeira.

Nenhum pixel novo de mão foi desenhado nas seis poses adicionais. Os nove retoques internos de F06 são apenas os do representante preservado. As contagens de pixels de `handFront` em `checks.json` são auditoria de escopo, **não prova de contato, dedos ou anatomia**.

Armas e `handFront` são vazios em F00/F01/F11/F12. F02–F10 é o único intervalo visível; não há saque, Idle armado, Walk armado nem equipamento persistente após o ataque.

## Mestres, exports e integridade

Todos os quatro mestres foram salvos no Aseprite com13 quadros e os mesmos tempos de origem:

`[30,65,35,50,45,65,35,35,100,55,80,45,90]ms =730ms`.

- Composto256: `source/composite.aseprite`, SHA-256 `{clip['masterSha256']}`.
- Corpo256: `source/body.aseprite`, SHA-256 `{clip['bodyMasterSha256']}`.
- Nativo128 do corpo: `source/native.aseprite`, SHA-256 `{clip['nativeMasterSha256']}`.
- Mão frontal256: `source/hand.aseprite`, SHA-256 `{clip['handMasterSha256']}`.
- `00.png`..`12.png`: compostos256 completos.
- `layers/{{weaponBack,body,weaponFront,handFront}}/00.png`..`12.png`:52 exports reais de camada.
- `native/00.png`..`12.png`: **crop exato do BODY**,64,64,128×128; não é um crop da arma.
- `native-strip.png`:1664×128, SHA-256 `{clip['nativeStripSha256']}`.
- `composite-strip.png`:3328×256, SHA-256 `{clip['compositeStripSha256']}`.
- `clip.json`: SHA-256 `{sha(C/'clip.json')}`; contém fontes, PNGs, tempos, camadas, hashes, item, landmarks/procedência e contrato attack-only.

O composto256 preserva toda a espada em cada pose. O canvas128 é destinado ao corpo nativo; não houve corte silencioso ou diminuição do equipamento para fazê-lo caber. A escala tática do player exibe o composto completo em128CSS, com corpo aproximadamente64px.

`checks.json`: decodificação independente dos cels reais, posições, alfa-over, corpos/mãos e cabeçalhos de tempo coincide com os exports dos quatro mestres. Todos os13 corpos têm **zero diferença RGBA visível** versus o pai. Ambos os strips reproduzem os quadros correspondentes. F02/F06/F08 têm zero diferenças nas quatro camadas e composto versus seus representantes. Todas as camadas de equipamento são vazias fora do intervalo. A transformação do item foi reproduzida em memória apenas para validação; nenhum raster foi autorado fora do Aseprite.

## Preview e validação de reprodução

`index.html` oferece antes/depois sincronizados com o pai imediato rejeitado,1×/0,75×/0,5×/0,25×, corpo128 ou64CSS, pausar/reiniciar, slider e passos anterior/próximo, loop opcional e retenção de F12 sem loop. Há modo só-corpo e alternância das quatro camadas, mais detalhe de pegada8×. O canvas usa nearest-neighbor; não adiciona suavização ou quadros.

Edge headless por file:// verificou13/13 quadros e repetição em1× e0,5×, escalas nativa/tática, passo F06↔F07, só-corpo/restauração exata e parada estável em F12 desarmado. O botão reflete o estado parado no fim one-shot. Registros completos em `preview-check.json`; capturas `preview-native.png` e `preview-tactical.png`.

**Limite:** testes do relógio/player não equivalem a assistir como jogador a um loop artístico contínuo1×. A inspeção local incluiu as poses reais, punhos, sequência completa e trajetórias propostas; o QA temporal independente continua pendente. Este pacote não usa a falta desse parecer como desculpa para substituir arte por metadados: a animação real e todas as fontes estão entregues para essa revisão.

## Pontos de atenção para o QA do ciclo

Confirmar a continuidade da luva elevada em F03–F05 e sua passagem rápida para o golpe F06–F08 no tempo original. Rever especialmente o pomo sobreposto à projeção da braçadeira de F07/F08 e a leitura da mão escura próxima ao tasset em F09/F10. Em cada caso, o corpo foi preservado e o cabo está ligado ao punho observado; sobreposição/contraste e rotação natural precisam ser julgados em movimento e escala tática, não por contato numérico. Nenhuma mudança extra foi aplicada às três referências estáticas aceitas para esconder esses pontos.

## Autoria, custo e parada

Toda autoria, gravação e exportação ocorreu em Aseprite1.3.18.6, **uma execução** oculta `--batch --noinapp`, perfil exclusivo `tmp/aseprite-grip-specialist-profile`, timeout90s. `Frame.duration` recebeu segundos. A GUI interativa não foi tocada. Python/Pillow/NumPy somente organizaram/validaram pixels e montaram evidência; o player usa os PNGs reais.

**Novas chamadas/gerações PixelLab:0.** Nenhum pacote foi instalado, nenhuma credencial transferida, nenhum token/custo/saldo foi estimado. Não houve Copilot, agentes, QA independente dentro do DEV, suíte global, commit ou integração Unity.

Parada em **GRIP_FRONT_R_SWORD_FULL_READY**, aguardando Root organizar QA independente do ciclo, sem Copilot. O patch futuro de oito células completas não foi montado; outras três frontais/quatro traseiras continuam fora deste lote. Os corpos traseiros bloqueados não foram usados como finais.
'''
(E/'report.md').write_text(report,encoding='utf-8')
checkpoint={'checkpoint':'GRIP_FRONT_R_SWORD_FULL_READY','scope':'ONLY full front_r/Sword13f','frameCount':13,'totalDurationMs':730,'technicalStatus':'TECHNICALLY_COMPLETE','artisticStatus':'VISUAL_REVIEW_REQUIRED','globalTaskStatus':'ARTISTIC_REVISION_REQUIRED','artisticApproval':'PENDING_CREATOR','eligibleForIntegration':False,'fullClipIndependentQA':'PENDING_ROOT_NO_COPILOT','validatedKeysReusedExact':[2,6,8],'bodyRgbaDeltaAllFrames':0,'hiddenFrames':[0,1,11,12],'visibleInterval':[2,10],'newPixelLabCalls':0,'clip':str(C/'clip.json').replace('\\','/'),'clipSha256':sha(C/'clip.json'),'masterSha256':clip['masterSha256'],'report':str(E/'report.md').replace('\\','/'),'reportSha256':sha(E/'report.md'),'checks':str(E/'checks.json').replace('\\','/'),'checksSha256':sha(E/'checks.json'),'preview':str(E/'index.html').replace('\\','/'),'previewCheckSha256':sha(E/'preview-check.json'),'priorFrozenRecordsPreserved':107,'sourceInputsPreserved':50,'rootAuthorizationMessageId':'a499b869-ed41-4967-8da3-3e15a1aaf6fe','staticGate':gate,'staticGateSha256':sha(gate),'nextStep':'Root independent full-cycle QA, no Copilot; no other clips before that gate.'}
(E/'snapshot').mkdir(exist_ok=True);write(E/'checkpoint.json',checkpoint);write(E/'snapshot/checkpoint.json',checkpoint)
files=sorted(p for base in [E,C]for p in base.rglob('*')if p.is_file()and '__pycache__'not in p.parts and p.name!='freeze.json')
freeze={'schemaVersion':1,'checkpoint':'GRIP_FRONT_R_SWORD_FULL_READY','createdAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'One complete front_r/Sword13f/730ms fork only','eligibleForIntegration':False,'artisticStatus':'VISUAL_REVIEW_REQUIRED','clipSha256':checkpoint['clipSha256'],'masterSha256':clip['masterSha256'],'reportSha256':checkpoint['reportSha256'],'checksSha256':checkpoint['checksSha256'],'priorFreezesPreserved':snap['preservedFreezes'],'fileCount':len(files),'exclusions':['snapshot/freeze.json itself','__pycache__/**','external disposable batch profile'],'files':[{'path':str(p).replace('\\','/'),'sizeBytes':p.stat().st_size,'sha256':sha(p)}for p in files]}
write(E/'snapshot/freeze.json',freeze)
assert all(sha(r['path'])==r['sha256']for r in freeze['files']);assert all(sha(p)==h for p,h in snap['files'].items())
for p,h in snap['preservedFreezes'].items():assert sha(p)==h and all(sha(r['path'])==r['sha256']for r in read(p)['files'])
print(json.dumps({'checkpoint':checkpoint['checkpoint'],'clipSha256':checkpoint['clipSha256'],'masterSha256':clip['masterSha256'],'reportSha256':checkpoint['reportSha256'],'freezeSha256':sha(E/'snapshot/freeze.json'),'fileCount':len(files),'eligibleForIntegration':False,'priorFreezeRecordsPreserved':107},indent=2))
