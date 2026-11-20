# Grip especialista — ciclo completo front_r/Sword

**GRIP_FRONT_R_SWORD_FULL_READY · TECHNICALLY_COMPLETE · VISUAL_REVIEW_REQUIRED · PENDING_CREATOR.**

Entrega de **um único ciclo completo**, `front_r/Sword`,13 quadros/730ms, para QA independente organizado pelo Root, **sem Copilot**. Não é aprovação artística do ciclo, dos demais grips ou da matriz; `eligibleForIntegration=false`. Nenhum QA/agente/orquestrador foi criado dentro do DEV.

[Abrir player1×/lento/tático](index.html) · [clip.json](../../../../characters/orc-v1/source/combat-rescue-v5/grip-specialist/full-front-r-sword/clip.json) · [checkpoint](checkpoint.json) · [checks técnicos](checks.json) · [sequência completa](all-final-frames.png) · [seis grips novos](new-grips-final.png) · [luvas reais anotadas](new-gloves-source-annotated.png).

## Autorização, fonte e escopo

O parecer independente Sol/Codex `qa-sol/grip-F02-F08-result.json` foi lido: `READY_FOR_FULL_CLIP_EXPLORATION`, estático somente. SHA-256 `f321b9d7e96a13c412dbc2e2c7e969a9fce02a18a8ade220d56589793f0f5a1a`. Ele não autorizava expansão automática; a execução do ciclo foi autorizada pelo Root na mensagem de continuidade `a499b869-ed41-4967-8da3-3e15a1aaf6fe`.

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

- Composto256: `source/composite.aseprite`, SHA-256 `3ee5755c874ccc007aa7f67af9ea5cc839d2cf98b5c0bee25dbcf0bf9acf6410`.
- Corpo256: `source/body.aseprite`, SHA-256 `b85c18f315dfed5cb37536398719b18454e59d2d27f49d166d0f0fb3b10deb38`.
- Nativo128 do corpo: `source/native.aseprite`, SHA-256 `8fab269d162d995ed3acdbbb09b8a03a3750ca5f05d923f35d21c1e55e8a87d7`.
- Mão frontal256: `source/hand.aseprite`, SHA-256 `d2c6a911295e08ac057ae81c79ec77d3fcad23cee0d1c769e28c147d165a4fce`.
- `00.png`..`12.png`: compostos256 completos.
- `layers/{weaponBack,body,weaponFront,handFront}/00.png`..`12.png`:52 exports reais de camada.
- `native/00.png`..`12.png`: **crop exato do BODY**,64,64,128×128; não é um crop da arma.
- `native-strip.png`:1664×128, SHA-256 `43aba45bf5b4a0bc4b1a453b76a7b14ce0366b6033691cd1bd1409d738ebe78c`.
- `composite-strip.png`:3328×256, SHA-256 `46629b49ba9d5091731db944dfdb3006160b71e8a569dd467bff80b9ce9d0f56`.
- `clip.json`: SHA-256 `16fe8b7b30cbaa029ac4f4bd2bda5f7c8ac127007ec40a49a1f41db2580c63a1`; contém fontes, PNGs, tempos, camadas, hashes, item, landmarks/procedência e contrato attack-only.

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
