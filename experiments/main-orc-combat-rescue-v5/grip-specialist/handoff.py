from pathlib import Path
import json,hashlib,datetime
E=Path('experiments/main-orc-combat-rescue-v5/grip-specialist');C=Path('characters/orc-v1/source/combat-rescue-v5/grip-specialist')
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def write(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
rep=read(C/'F06/representative.json');checks=read(E/'checks.json');preview=read(E/'preview-check.json');snap=read(E/'input-snapshot.json')
assert all(sha(p)==h for p,h in snap['files'].items())
assert checks['bodyVisibleRgbaDelta']==0 and checks['handFrontLocalRetouchDelta']==9 and preview['status']=='PASS'
report=f'''# Grip especialista — somente front_r/Sword F06

**GRIP_F06_READY · TECHNICALLY_COMPLETE no representante · VISUAL_REVIEW_REQUIRED · PENDING_CREATOR.**

Este checkpoint entrega **um quadro concreto para Root submeter ao mesmo QA Grok `d13ab881`**. Não concede aprovação anatômica, propagação ou integração; a tarefa completa continua em resgate artístico. F02/F08, os outros quadros e os demais grips não foram autorados. Nenhum agente/QA foi criado por este DEV.

[Abrir preview local](index.html) · [antes/depois](F06-before-after.png) · [diagnóstico anatômico anotado](F06-anatomy-annotated.png) · [zoom da pegada](F06-grip-final-20x.png) · [representative.json](../../../characters/orc-v1/source/combat-rescue-v5/grip-specialist/F06/representative.json) · [checks](checks.json).

## Localização anatômica real

As duas versões rejeitadas e o parecer de Grok foram lidos. F06 `frame.layers.body.png` foi aberto **sem arma**, ampliado por nearest-neighbor e examinado em grade. Seus pixels são idênticos nas duas versões rejeitadas; a fonte corporal preservada é reutilizada diretamente, não redesenhada.

Marcos visuais aproximados no composto256: ombro de ataque `(118,102)`, cotovelo `(128,110)`, antebraço metálico `(139,112)`, borda distal da braçadeira `(149,112)`, transição do pulso `(151,114)`, palma `(155,114)` e contorno externo dos nós `(159,111)`. Coordenadas nativas128 subtraem `(64,64)`. São marcos interpretados na arte achatada, não dados de esqueleto recuperados.

A luva real ocupa aproximadamente x152..159/y109..119. A mão baixa junto ao quadril `(156,142)` pertence ao braço inativo. A nova montagem acompanha a cadeia do braço que cruza a frente do torso até a luva à direita. O ponto `(142,115)` do segundo passe está sobre a braçadeira, antes da palma. O primeiro ponto `(157,112)` já era próximo da luva: **não alego que todo socket anterior estava fora da mão**. Localização próxima e uma camada estampada também não demonstram envolvimento natural do cabo.

`anatomy.json`, a grade `F06-actual-palm-grid.png` e a imagem anotada registram essa leitura antes do novo encaixe. Nenhuma tabela de sockets anterior foi usada para localizar a palma.

## Alteração executada no Aseprite

A espada independente atual foi preservada, incluindo seus materiais V4/V5, escala1, canvas96 e grip próprio `(48,66)`. O grip é levado à palma observada `(155,114)`, rotação32°, sem espelhamento. A lâmina sai diagonalmente para cima/direita a partir da mão; não nasce no metal do antebraço nem atravessa o peito como no passe `qa5-repair1` mostrado na comparação.

A separação `weaponBack → body → weaponFront → handFront` usa **a seção de couro do próprio item** atrás do corpo, enquanto lâmina, guarda e pomo permanecem na camada dianteira. `handFront` reutiliza linhas traçadas da luva original, em x152..157/y110..117. Nenhuma forma paramétrica de mão, círculo, ponte de cuff, dilatação ou retalho de torso foi criado. A mão não foi ampliada nem deslocada.

Primeiro foi salva uma montagem com os pixels da luva original. Ela está preservada em `attempt01-existing-glove/`. A segunda gravação mantém o mesmo encaixe e acrescenta **nove posições de cor internas à luva**: pequeno contorno iluminado de polegar e uma dobra dos dedos. O realce reaproveita a cor da própria luva em `(157,119)`; o restante é couro escuro e sombra. Não foi exigida a representação literal de quatro dedos em128.

Na inspeção estática de corpo inteiro, zoom e apresentações128/64, a arma agora se relaciona com a mão existente; guarda e pomo permanecem discerníveis. Essa é a avaliação local que fundamenta enviar o representante ao QA, **não uma aprovação para propagá-lo**. O mesmo QA ainda precisa julgar contato, pulso, fechamento e perspectiva. Não há alegação de validação temporal de um ataque completo a partir deste quadro.

## Fontes, exports e hashes reais

Pasta: `characters/orc-v1/source/combat-rescue-v5/grip-specialist/F06/`.

- Mestre composto: `source/composite.aseprite`, quatro camadas,256×256, um quadro35ms. SHA-256 `{rep['masterSha256']}`.
- Mestre corpo256: `source/body-256.aseprite`, pixels preservados. SHA-256 `{rep['bodyMasterSha256']}`.
- Mestre corpo128: `source/body-128.aseprite`. SHA-256 `{rep['nativeMasterSha256']}`.
- Composto256: `composite-256.png`. SHA-256 `{rep['frames'][0]['sha256']}`.
- Corpo nativo128: `body-128.png`. SHA-256 `{rep['frames'][0]['nativeSha256']}`.
- Composto nativo128: `composite-native-128.png`. SHA-256 `{rep['frames'][0]['compositeNativeSha256']}`.
- `layers/` e `native/layers/`: PNGs separados de body/weaponBack/weaponFront/handFront. `representative.json` contém seus caminhos e hashes.

O nativo128 é o crop central exato com bodyOffset `(64,64)`. **Não corta nenhum pixel opaco do composto**; guarda, ponta e pomo estão íntegros. O mestre usa um quadro interno0 correspondente ao **F06 de origem**,35ms (`Frame.duration=.035` segundos). Não é uma nova animação de um quadro para substituir o ataque13f.

## Verificação focada e limites

`checks.json`: decodificação independente dos cels reais e suas posições coincide com os PNGs, incluindo os mestres de corpo. Alfa-over das camadas e transformação do item conferem; cor/alpha do item independente não mudaram. Corpo: **0 pixels RGBA visíveis alterados**, silhueta e tempo preservados. Os43 arquivos do inventário de entrada continuam SHA-256 idênticos. O composto difere1213 posições RGBA do segundo passe rejeitado, dado descritivo sem valor de aprovação artística.

O handFront tem33 posições opacas, das quais nove são retoques locais; esse número registra o escopo, **não prova anatomia ou pegada**. Não foi usado limiar de contato, quantidade de dedos, wood-occluded ou cor de máscara como critério artístico.

`index.html` foi aberto por file:// em Edge headless, com carregamento real das imagens, alternância/restauração das camadas e displays de canvas128/256 verificados por capturas. Não usa smoothing ou interpolação. É preview de **um quadro**; nenhum player ou loop foi apresentado como validação de movimento. O teste usa capturas de canvas porque file:// impede leitura JS dos pixels de imagens em diretórios distintos; as regras do navegador não foram desabilitadas.

Toda autoria, gravação de mestres e exportação de produção ocorreu em Aseprite1.3.18.6, processo oculto `--batch --noinapp`, perfil exclusivo `tmp/aseprite-grip-specialist-profile`, timeout90s. Foram duas execuções locais: montagem inicial e acabamento interno de nove pixels. Pillow/NumPy apenas leram/validaram pixels, organizaram arquivos e criaram layouts anotados. A GUI interativa não foi tocada.

PixelLab estava autorizado em `authorization.json`; não foi necessário neste representante porque a mão já existe e o erro principal é de encaixe/oclusão. **Novas chamadas/gerações PixelLab:0.** Nenhuma compra, credencial ou código privado foi transferido. Não há estimativa inventada de tokens, dólares ou saldo.

## Portão de parada deste representante

`checkpoint.json` e `snapshot/checkpoint.json` registram **GRIP_F06_READY**. `representativeAcceptableForPropagation=false` significa **aguardando o parecer do mesmo QA**, não autorização de expansão. `eligibleForIntegration=false`. Nenhum outro quadro foi propagado.

Escritas limitadas às duas pastas de grip-specialist, além do perfil batch explicitamente solicitado. A matriz, docs, integração, fontes atuais das armas, saídas antigas V4/DEV/especialista, arquivos traseiros de Argon em `combat/qa5-repair1`, outros estados protegidos, Unity e produção ativa não foram alterados. Root continua proprietário do veredito de QA e da futura seleção/integração.
'''
(E/'report.md').write_text(report,encoding='utf-8')
checkpoint={'checkpoint':'GRIP_F06_READY','scope':'ONLY front_r/Sword F06','technicalStatus':'TECHNICALLY_COMPLETE','artisticStatus':'VISUAL_REVIEW_REQUIRED','globalTaskStatus':'ARTISTIC_REVISION_REQUIRED_UNCHANGED_PENDING_ROOT_QA','artisticApproval':'PENDING_CREATOR','independentQA':'PENDING_ROOT_SAME_GROK_d13ab881','representativeAcceptableForPropagation':False,'propagationReviewStatus':'PENDING_SAME_QA','eligibleForIntegration':False,'sourceFrameIndex':6,'durationMs':35,'bodyRgbaDelta':0,'itemGrip':[48,66],'bodyGrip':[155,114],'rotationDeg':32,'localGloveRetouchPixels':9,'newPixelLabCalls':0,'representative':str(C/'F06/representative.json').replace('\\','/'),'representativeSha256':sha(C/'F06/representative.json'),'report':str(E/'report.md').replace('\\','/'),'reportSha256':sha(E/'report.md'),'checks':str(E/'checks.json').replace('\\','/'),'checksSha256':sha(E/'checks.json'),'preview':str(E/'index.html').replace('\\','/'),'anatomy':str(E/'anatomy.json').replace('\\','/'),'inputsPreserved':43,'nextStep':'Root submits this exact representative to the SAME independent QA; no propagation before its opinion.'}
(E/'snapshot').mkdir(exist_ok=True);write(E/'checkpoint.json',checkpoint);write(E/'snapshot/checkpoint.json',checkpoint)
files=sorted(p for base in [C,E]for p in base.rglob('*')if p.is_file()and '__pycache__'not in p.parts and p.name!='freeze.json')
freeze={'schemaVersion':1,'revision':'main-orc-combat-rescue-v5-grip-specialist-F06','checkpoint':'GRIP_F06_READY','createdAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'eligibleForIntegration':False,'artisticStatus':'VISUAL_REVIEW_REQUIRED','scope':'Single F06 representative; includes preserved initial existing-glove assembly; no production matrix change','excluded':['snapshot/freeze.json itself','__pycache__/**','explicitly external disposable tmp/aseprite-grip-specialist-profile'],'representativeSha256':checkpoint['representativeSha256'],'reportSha256':checkpoint['reportSha256'],'checksSha256':checkpoint['checksSha256'],'fileCount':len(files),'files':[{'path':str(p).replace('\\','/'),'sizeBytes':p.stat().st_size,'sha256':sha(p)}for p in files]}
write(E/'snapshot/freeze.json',freeze);assert all(sha(r['path'])==r['sha256']for r in freeze['files']);assert all(sha(p)==h for p,h in snap['files'].items())
print(json.dumps({'checkpoint':checkpoint['checkpoint'],'representativeSha256':checkpoint['representativeSha256'],'masterSha256':rep['masterSha256'],'reportSha256':checkpoint['reportSha256'],'freezeSha256':sha(E/'snapshot/freeze.json'),'fileCount':len(files),'eligibleForIntegration':False,'inputsPreserved':43},indent=2))
