# Grip especialista — front_r/Sword F02 e F08

**GRIP_F02_F08_READY · TECHNICALLY_COMPLETE no empacotamento dos dois representantes · VISUAL_REVIEW_REQUIRED · PENDING_CREATOR.**

Entrega limitada a **F02 e F08**, para QA **GLM5.3/Cline organizado pelo Root**. Não há autorização de propagação, ciclo13f, outros grips ou matriz. A tarefa artística completa não é declarada encerrada. Nenhum QA/agente foi criado dentro do DEV.

[Preview local](index.html) · [checkpoint](checkpoint.json) · [checks](checks.json) · [F02 antes/depois](F02-before-after.png) · [F08 antes/depois](F08-before-after.png) · [anatomia F02](F02-anatomy-annotated.png) · [anatomia F08](F08-anatomy-annotated.png).

## Continuidade e preservação de F06

Foi lido o parecer `qa-grok/representative-sol-F06.json`: **READY_FOR_F02_F08_AND_FULL_CLIP_EXPLORATION**, restrito ao representante F06. A correção anatômica confirmada pelo próprio QA foi respeitada: o braço ativo cruza o corpo e a mão baixa junto ao quadril é inativa. Isso não aprova outros quadros ou a matriz.

Os54 arquivos do freeze anterior continuam SHA-256 idênticos, inclusive fontes, exports, representante, scripts, relatório e preview de F06. O freeze original permanece `676e2c60945e207c1aa89f90971bfd11afad79831614908a29e3a3606781a9da`. Novos scripts/evidências/checkpoint estão neste subdiretório `F02-F08/`, evitando regravar qualquer arquivo congelado de F06.

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

### F02

- [representative.json](../../../../characters/orc-v1/source/combat-rescue-v5/grip-specialist/F02/representative.json): SHA-256 `76b5b63dd0ff7d9a1011400b29f570eb7a53cd205e7027e764ed512f6fc14ebf`.
- Composto256: `characters/orc-v1/source/combat-rescue-v5/grip-specialist/F02/composite-256.png`, SHA-256 `008b414cdd6f8a8eb64add1a5d8a0e4282ae56a4759edceef8fc69a2a8232b3d`.
- Mestre composto: `characters/orc-v1/source/combat-rescue-v5/grip-specialist/F02/source/composite.aseprite`, SHA-256 `c131abe09e0bdba1e1143b0d686ef142bae313f752184c1858a3a5de8886cbed`.
- Mestre corpo256: `characters/orc-v1/source/combat-rescue-v5/grip-specialist/F02/source/body-256.aseprite`, SHA-256 `01e16c60a7cf0f9bba01bf0896c5e136a366101044da28b6026b96c0ac24dfc7`.
- Mestre corpo128: `characters/orc-v1/source/combat-rescue-v5/grip-specialist/F02/source/body-128.aseprite`, SHA-256 `81ba867e52aa6cceda3441086b19b0e5457131e4956914f3dfe165cd83838118`.
- Corpo nativo128: `characters/orc-v1/source/combat-rescue-v5/grip-specialist/F02/body-128.png`, SHA-256 `2258446e6bbbf9018edde13295fb0ebe3105a8996bc0b10080a14d47698c8a1c`.

### F08

- [representative.json](../../../../characters/orc-v1/source/combat-rescue-v5/grip-specialist/F08/representative.json): SHA-256 `e07c0be8a607230a0617aec5481ec5e9bc2fcdafacdaf14ec59686ee3c28184c`.
- Composto256: `characters/orc-v1/source/combat-rescue-v5/grip-specialist/F08/composite-256.png`, SHA-256 `2f47d317578f830a1ca37146be8fb70959f9b681799e2b40f63a2ea551574b18`.
- Mestre composto: `characters/orc-v1/source/combat-rescue-v5/grip-specialist/F08/source/composite.aseprite`, SHA-256 `b4950ba70f261c045b7b408e40c01b739376490d82cf0391a130d6a97cc2d4cc`.
- Mestre corpo256: `characters/orc-v1/source/combat-rescue-v5/grip-specialist/F08/source/body-256.aseprite`, SHA-256 `11b1a5381bb08226bb3f5cfb3f0e57abb173d55b2407301e7515dbc3582d04b2`.
- Mestre corpo128: `characters/orc-v1/source/combat-rescue-v5/grip-specialist/F08/source/body-128.aseprite`, SHA-256 `c9fc407cdb89965a7a6ceab43ed3d6f399201bcc5b385688329ab630a2afeec6`.
- Corpo nativo128: `characters/orc-v1/source/combat-rescue-v5/grip-specialist/F08/body-128.png`, SHA-256 `c06d99b837acf114076e3dd44be519bb16d67df2aac8949400c2efe45e872ed6`.


Todos os caminhos/hashes de camadas, itens e transformações estão nos dois `representative.json`.

## Verificação focada e custos

`checks.json` registra, nos dois quadros: corpo com **zero diferença RGBA visível**, tempos35/100ms preservados nos cabeçalhos salvos, decodificação independente dos cels reais/posições igual aos exports, alfa-over exato e transformação do item conferindo com seus pixels originais. A imagem completa256 não perde pixels do item; a limitação do crop128 em F08 está declarada. Os10 arquivos de entrada inventariados permanecem idênticos. F06 foi reconferido por seus54 hashes, sem reautoria ou inspeção redundante da arte antiga.

As diferenças visíveis versus os respectivos compostos rejeitados `qa5-repair1` são904 posições em F02 e961 em F08; esses valores não medem qualidade. O preview `index.html` foi aberto por file:// em Edge headless: imagens carregadas, camadas alternadas/restauradas exatamente e escalas de canvas128/256 verificadas. Os dois representantes são estáticos; nenhum loop ou leitura temporal foi alegado.

Autoria, gravação e exportação de produção ocorreram exclusivamente em Aseprite1.3.18.6, oculto `--batch --noinapp`, perfil exclusivo `tmp/aseprite-grip-specialist-profile`, timeout90s. Foi uma execução local para os dois quadros. Pillow/NumPy somente leram/validaram pixels e montaram evidência diagnóstica. A GUI interativa não foi tocada.

**Novas chamadas/gerações PixelLab:0.** Não houve bloqueio que exigisse geração nesta pegada local. Não houve instalação, commit, escrita em Unity ou alteração dos corpos de outro DEV. Idle/Hit/Walk/Defeat/Unarmed, corpos traseiros, itens independentes, matriz, docs e integração permanecem fora das escritas.

## Próximo portão

Parada em **GRIP_F02_F08_READY**. `representativeAcceptableForPropagation=false` significa **pendente do QA GLM5.3/Cline solicitado pelo Root**. `eligibleForIntegration=false`; nenhuma expansão automática para13 quadros ou oito grips foi feita.

O contrato futuro `integrate.mjs --weapon-patch ...` foi registrado como orientação posterior: oito células completas, `parentManifestSha256=f250f7a11ceb0e851c9a3c34f8c20e75c48da5a04e0a2229933945298aaf4017`, armas independentes preservadas. **Nenhum patch desse tipo foi produzido nesta etapa.** Corpos traseiros futuros continuam dependentes do especialista e do QA indicados pelo Root; fontes rejeitadas não foram selecionadas como finais.
