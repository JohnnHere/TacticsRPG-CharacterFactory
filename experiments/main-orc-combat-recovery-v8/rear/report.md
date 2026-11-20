# V8 — traseiras alinhadas ao metrônomo frontal

`V8_REAR_ALIGNED` · `TECHNICALLY_COMPLETE` · `VISUAL_REVIEW_REQUIRED` · `PENDING_CREATOR`

[Preview das quatro direções](preview.html) · [Tabela completa de fases](phase-comparison.md) · [CSV](phase-comparison.csv) · [Manifesto das quatro candidatas](candidate4manifest.json)

## Resultado temporal

| Família | Grade comum às quatro direções | Fase de impacto | Início (todas) | Posição relativa |
|---|---|---|---|---|
| Sword | 13f / 730 ms | F07 · contact | 325 ms | 44.52% |
| Axe | 12f / 1005 ms | F06 · heavy-impact | 410 ms | 40.80% |

As durações são exatamente as canônicas pedidas: Sword [30,65,35,50,45,65,35,35,100,55,80,45,90] e Axe [40,65,35,80,155,35,115,110,130,50,90,100]. Não foi apenas normalizado o total; índice, ordem de fases, duração individual, entrada/saída armada e início do impacto são comuns.

## Mapa validado antes de montar

phase-map.md e phase-map-validation.json foram escritos antes da produção dos ciclos. O frontal protegido foi lido por posição de quadro e relógio acumulado. As transições back_l foram depois construídas e inspecionadas em trios ápice→descida→impacto; pre-propagation-validation.json registra anatomia conectada e juntas opacas antes da montagem. Não foi propagada a primeira blocagem temporal como ciclo final.

## Reuso, descarte e reautoria

| Célula | Índice V8 → índice V7 da fonte | Operação |
|---|---|---|
| back_l/Sword | 00→00, 01→01, 02→02, 03→04, 04→05, 05→06, 06→08*, 07→09, 08→10, 09→11, 10→12, 11→13, 12→14 | reuso + uma descida manual |
| back_l/Axe | 00→00, 01→01, 02→02, 03→03, 04→06, 05→08*, 06→09, 07→10, 08→11, 09→12, 10→13, 11→14 | reuso + uma descida manual |
| back_r/Sword | 00→00, 01→01 sem arma, 02→01, 03→02, 04→03, 05→03, 06→05, 07→07, 08→08, 09→09, 10→09, 11→10, 12→11 | reuso exato de camadas + retiming |
| back_r/Axe | 00→00, 01→01 sem arma, 02→01, 03→02, 04→04, 05→06, 06→07, 07→08, 08→09, 09→10, 10→10, 11→11 | reuso exato de camadas + retiming |

Asterisco = nova descida, não cópia da pose inteira de origem. Os sourceFrame e sourcePhase por quadro, com hash do clip de origem, estão em cada clip.json.

**back_l/Sword:** o ápice validado V7 F06 está em V8 F05, com as quatro camadas pixel-idênticas. O contato V7 F09 está em V8 F07. A abertura V7 F03 e as duas antigas etapas descendentes F07/F08 não foram mantidas como passos sucessivos; uma única nova ligação ocupa a fase slash-release F06. Isso retira os passos extras do ciclo de 15 quadros sem simplesmente acelerar uma sequência incompatível. A nova palma desce de [100,19] no ápice para [112,52] e [109,81] no contato: deslocamento predominantemente vertical, sem travessia lateral.

**back_l/Axe:** as etapas redundantes de hoist V7 F04/F05 e a antiga dupla de descida F07/F08 são substituídas pela grade de 12 fases. Coil V7 F06 ocupa V8 F04; contato V7 F09 ocupa V8 F06. Uma nova cleave-drive ocupa F05, com palma [110,49] entre coil [95,15] e contato [101,76]. São bases e doador de antebraço próprios de Axe, não o ciclo Sword com item trocado.

As duas ligações foram autoradas por Lua no Aseprite: retirar braço antigo, desenhar úmero/manga local, articular antebraço/luva medidos da mesma vista e compor o item independente. Doadores: Sword back_l V6 F07 (cotovelo [89,64], punho [95,83], palma [94,89]) e Axe back_l V6 F07 ([88,65]→[94,83]→[94,89]); medidas e máscaras herdadas da via manual V7. As fontes não foram editadas. A projeção longitudinal local do membro permanece explicitada no resultado da autoria; espessura transversal e clusters vêm do próprio doador, sem cross-fade ou geração.

| Ligação nova | Ombro | Cotovelo | Punho | Palma | Úmero / antebraço | Ângulo da arma |
|---|---|---|---|---|---|
| Sword | [85, 43] | [100, 38] | [111, 47] | [112, 52] | 15.811 / 14.213 px | 55° |
| Axe | [84, 46] | [98, 36] | [108, 45] | [110, 49] | 17.205 / 13.454 px | 60° |

[Trio Sword](transitions/sword/apex-descent-impact.png) · [Trio Axe](transitions/axe/apex-descent-impact.png). São evidências locais de continuidade, não aprovação artística.

**back_r/Sword e Axe:** pixels de todas as camadas selecionadas são idênticos ao rear-r-flashfixed V7, inclusive mão/oclusão, contornos e item. Foi adicionada a preparação sem arma a partir do corpo da própria pose; nenhuma luva foi redesenhada. Sword usa a posição de chamber como coil/hold e a última recuperação armada como recoil/settle; Axe usa o próprio overhead e descida/impacto existentes. Poses intermediárias incompatíveis com a nova contagem foram deixadas no histórico V7. A geometria de cada pose reaproveitada não mudou; o caminho temporal muda porque agora segue o frontal.

## Ápice e bookends

Ápice Sword re-medido no V8: ponta 48 px acima do crânio, punho 14 px acima da linha do ombro, espaço negativo mínimo 4 px (cortes y24..30), cotovelo 68.405°. Evidência em apex-measurements.json. A mão direita anatômica, a luva e a cadeia articular continuam as da vista back_l validada.

Bookends sempre desarmados. back_r F00 e último quadro conservam as normalizações V7 de 7/5 pixels claros (luma ≥145), com igualdade de pixels ao doador; nunca retorna o corpo Idle de 67 pixels. back_l mantém a guarda de ataque V7; primeiro/último corpo são idênticos, e a preparação/retorno conservam o material da ombreira de ataque. Nenhum Idle foi modificado.

## Metadados legados preservados: diferença relevante

A aproximação de impacto do enunciado não é o relógio real destes arquivos. A fase contact Sword começa em 325 ms; heavy-impact Axe em 410 ms. Alguns campos contactEvent legados divergem:

| Frontal protegido | contactEvent registrado | Fase/relógio usados nesta tarefa |
|---|---|---|
| front_r/Sword | {'frame': 6, 'timeMs': 290, 'status': 'CANDIDATE_VISUAL_ONLY', 'appliesDamage': False} | contact · F07 · 325 ms |
| front_l/Sword | {'frame': 7, 'timeMs': 325, 'status': 'CANDIDATE_VISUAL_ONLY', 'appliesDamage': False} | contact · F07 · 325 ms |
| front_r/Axe | {'frame': 6, 'timeMs': 375, 'status': 'CANDIDATE_VISUAL_ONLY', 'appliesDamage': False} | heavy-impact · F06 · 410 ms |
| front_l/Axe | {'frame': 6, 'timeMs': 375, 'status': 'CANDIDATE_VISUAL_ONLY', 'appliesDamage': False} | heavy-impact · F06 · 410 ms |

Nada foi corrigido dentro dos frontais protegidos. O player usa o início da fase e o relógio canônico; os novos contactEvent traseiros registram esse mesmo instante. Não se afirma que todos os contactEvent legados coincidem: a coincidência demonstrada é entre as fases de impacto nas quatro direções. Esta divergência deve ser tratada separadamente se esses eventos forem consumidos pelo runtime.

## Contrato e preservação

50 quadros traseiros: alpha-over das quatro camadas igual ao PNG composto, nativePng igual ao crop de body, alfa nativo binário, corpo conectado e sem corte na borda direita; zero pixels de arma abaixo de groundY190. Reuso de camadas conferido pixel a pixel contra cada quadro fonte. Mestres composto256 e nativo128 salvos, fechados, reabertos e reexportados com cel.position real; pixels e durações conferidos no Aseprite. Tiras nativas/compostas verificadas tile por tile, hashes reais em clip.json.

Arma só no intervalo do frontal: Sword F02..F10, Axe F02..F08. Ordem weaponBack → body → weaponFront → handFront. Equipamento transparente fora do intervalo, corpo desarmado nos bookends e na preparação.

863 arquivos protegidos V7/itens conferidos por SHA-256. Nenhuma escrita em V5/V6/V7, frontal protegido, matriz canônica, Unity ou commits. Perfil isolado tmp/aseprite-v8-rear-profile; toda autoria raster no Aseprite batch, Lua Frame.duration em segundos. Pillow somente leitura/medição. Zero chamadas PixelLab, sem compras nem estimativa de créditos.

## Limitações

A grade igual remove a mistura de ritmos e o descompasso de impacto; não aprova automaticamente a arte. A nova ligação descendente, a projeção do antebraço e a leitura natural de peso/pegada ainda precisam da avaliação do criador/QA em 1× e escala tática. A inspeção local não encontrou mão ausente ou salto de lado nas ligações novas; isso não substitui parecer artístico temporal independente.

O flash frontal é outra frente e não foi alterado aqui. Os arquivos frontais de referência são os V7 protegidos indicados pelo pedido. Não foram propagados os 15 quadros V7 nem concedida aprovação ao V8. Parada em V8_REAR_ALIGNED.

Player conferido em Edge/Chromium headless: 200 comparações canvas↔PNG exatas (25 posições de quadro por família somadas × 4 direções × body/composto), rótulos de fase coincidentes, verificações antes/no/depois do impacto em 325/410 ms, velocidades 1×/0,5×, passo/zoom/tático, pausa terminal e repetição, HTTP/file e zero erro JavaScript. Evidência em browser-check.json e capturas *-impact-1x.png/*-impact-tactical.png. Hashes declarados dos 50 quadros, camadas, oito mestres e oito tiras reconferidos no freeze final.
