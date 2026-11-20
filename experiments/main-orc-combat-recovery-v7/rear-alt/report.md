# V7 back_l — Sword e Axe manuais completos

`V7_BACK_L_FULL_MANUAL_READY` · `TECHNICALLY_COMPLETE` · `VISUAL_REVIEW_REQUIRED` · `PENDING_CREATOR`

[Player e comparação com os dois frontais](preview.html) · [Chaves anteriores preservadas](pose-stage-preview.html) · [Medições por quadro](full-cycle/joint-metrics.json) · [Flash do ombro](full-cycle/bookend-flash-audit.json)

## Entrega e método

| Clipe | Quadros | Duração | Intervalo com arma (índice 0) |
|---|---:|---:|---|
| back_l / Sword | 15 | 860 ms | [2, 12] |
| back_l / Axe | 15 | 1230 ms | [2, 11] |

Zero chamadas/zero créditos de geração nesta frente. Nenhum PixelLab, imagegen, compra ou saldo inventado. Autoria programática manual executada no Aseprite 1.3.18.6 com --batch --noinapp, perfil tmp/aseprite-v7-alt-profile. Não é desenho manual pela GUI nem arte integral desenhada do zero: corpo/roupa/pernas e peças do membro herdam pixels V6; a nova coreografia, máscaras, braços superiores e transições são autoria Lua local. Pillow foi usado apenas para leitura/medição/validação.

Sword foi montado e inspecionado primeiro. Seus ápice e impacto escolhidos permanecem byte-preservados como representantes históricos e pixel-preservados nas quatro camadas em F06 e F09 do ciclo. As durações isoladas de 110/80 ms foram ajustadas a 70/55 ms no ciclo; PNGs/corpo/arma/luva das chaves não mudaram. O novo ritmo Sword de 860 ms está no intervalo pedido (730–950 ms).

Depois foi construído Axe com bases corporais próprias da família, caminho próprio da mão, coil mais alto, cabeça pesada conduzindo a descida e recuperação mais lenta. Não é o corpo Sword com a arma trocada. Os dois clipes têm 15 quadros por conveniência de revisão, mas fontes de tronco/pernas, trajetórias, arma, distribuição de tempos e recuperação são diferentes.

## Doadores medidos e construção

| Doador back_l | Cotovelo | Punho | Palma | Antebraço fonte | Uso |
|---|---|---|---|---:|---|
| raised · characters/orc-v1/source/artistic-reconstruction-v6/rear/back_l-axe/layers/body/03.png | [99, 35] | [93, 23] | [88, 17] | 13.416 px | elevação/coil e soltura |
| sword-low · characters/orc-v1/source/artistic-reconstruction-v6/rear/back_l-sword/layers/body/07.png | [89, 64] | [95, 83] | [94, 89] | 19.925 px | guarda, descida, contato e recuperação da própria família |
| axe-low · characters/orc-v1/source/artistic-reconstruction-v6/rear/back_l-axe/layers/body/07.png | [88, 65] | [94, 83] | [94, 89] | 18.974 px | guarda, descida, contato e recuperação da própria família |

A seleção do doador elevado mantém a medição que venceu a comparação anterior: luva real e completa, palma distinta e antebraço sem amputação. O úmero fonte estava encurtado pela perspectiva; não foi simplesmente esticado. Em cada pose, ombro/cotovelo/punho/palma foram colocados e medidos, o braço antigo retirado, o úmero/manga/cota desenhados no Aseprite e o antebraço/luva do mesmo back_l articulados ao novo cotovelo.

A primeira blocagem geométrica foi refinada por quadros com cotovelos explícitos: uma pose de abertura evita inverter o cotovelo na elevação; a soltura foi estendida para preservar leitura do antebraço. A articulação do doador usa nearest-neighbour dentro do Aseprite, com projeção longitudinal local e espessura transversal mantida; nenhum cross-fade, mistura raster temporal, espelhamento ou transformação global do personagem. A escala longitudinal por quadro está em joint-metrics.json. Ela representa uma proposta de projeção do membro, ainda sujeita à avaliação artística; não é prova de perspectiva tridimensional perfeita.

Foram removidos resíduos confirmados do braço original: Sword soltura (fonte F04, região x92..106/y57..64), mãos antigas Axe nas fontes de hoist F03/F04 (ficavam à esquerda do corte genérico de Sword), e resíduo de punho Axe fonte F08 em x82..86/y88..94. Pequenos componentes desconectados finais são registrados com coordenadas em *-author-result.json. A retirada integral do membro precede a colocação do novo.

A luva vem do próprio doador anatômico, com contorno fechado e junção ao antebraço, e a oclusão é extraída da mesma transformação. Cabo em weaponBack, corpo em body, guarda/lâmina/pomo em weaponFront e luva em handFront. Overlap de equipamento é medido como prova técnica complementar, não como aprovação de pegada natural. Os itens independentes V5 não foram modificados.

## Técnica frontal comparada fase a fase

O player apresenta front_l e front_r correspondentes do V6 satisfatório. “Alinhar fases” mostra o quadro frontal de referência para cada fase traseira; não finge que o frontal contém os intermediários extras. “Tempos próprios” reproduz os quatro clipes com as durações reais. Fontes e SHA-256 exatos dos frontais estão em phase-comparison.json e nas referências de cada quadro do clip.json. Não foram copiadas coordenadas nem espelhadas imagens frontais.

### Sword

Frontal: 730 ms. Manual traseiro: 860 ms.

| F traseiro | Fase traseira | ms | Fase frontal equivalente | F front_l / front_r | ms frontal |
|---|---|---:|---|---|---:|
| 00 | rest | 40 | rest | 00 / 00 | 30 |
| 01 | body-preparation | 55 | body-preparation | 01 / 01 | 65 |
| 02 | establish-grip | 35 | establish-grip | 02 / 02 | 35 |
| 03 | anticipation-open | 45 | anticipation | 03 / 03 | 50 |
| 04 | anticipation | 55 | anticipation | 03 / 03 | 50 |
| 05 | coil-behind | 45 | coil-behind | 04 / 04 | 45 |
| 06 | apex-hold | 70 | apex-hold | 05 / 05 | 65 |
| 07 | slash-release | 40 | slash-release | 06 / 06 | 35 |
| 08 | slash-drive | 40 | slash-release | 06 / 06 | 35 |
| 09 | contact | 55 | contact | 07 / 07 | 35 |
| 10 | follow-through | 90 | follow-through | 08 / 08 | 100 |
| 11 | recoil | 65 | recoil | 09 / 09 | 55 |
| 12 | settle-grip | 80 | settle-grip | 10 / 10 | 80 |
| 13 | release-grip | 60 | release-grip | 11 / 11 | 45 |
| 14 | return-to-guard | 85 | return-to-guard | 12 / 12 | 90 |

Identidade buscada: preparação corporal → estabelecimento de pega → coil/ápice breve com ponta acima do crânio → soltura rápida atravessando o plano vertical → contato → follow-through baixo e retorno contido. F03 (abertura) e F08 (descida intermediária) tornam legíveis as rotações do membro na vista traseira. Comparado a 730 ms frontal, os 130 ms adicionais acomodam essas ligações e a recuperação visual, sem tornar a espada um chop de machado. A progressão principal da lâmina é -10° → 25° → 70° → 115° → 128°; as reversões seguintes são recoil/settle, não reversão no golpe. Projeções angulares das vistas não são igualadas numericamente.

### Axe

Frontal: 1005 ms. Manual traseiro: 1230 ms.

| F traseiro | Fase traseira | ms | Fase frontal equivalente | F front_l / front_r | ms frontal |
|---|---|---:|---|---|---:|
| 00 | rest | 45 | rest | 00 / 00 | 40 |
| 01 | body-preparation | 65 | body-preparation | 01 / 01 | 65 |
| 02 | establish-grip | 40 | establish-grip | 02 / 02 | 35 |
| 03 | anticipation | 80 | anticipation | 03 / 03 | 80 |
| 04 | hoist-transition | 45 | overhead-coil | 04 / 04 | 155 |
| 05 | hoist | 95 | overhead-coil | 04 / 04 | 155 |
| 06 | overhead-coil | 155 | overhead-coil | 04 / 04 | 155 |
| 07 | cleave-drive | 45 | cleave-drive | 05 / 05 | 35 |
| 08 | downstroke | 45 | cleave-drive | 05 / 05 | 35 |
| 09 | heavy-impact | 115 | heavy-impact | 06 / 06 | 115 |
| 10 | weight-settle | 120 | weight-settle | 07 / 07 | 110 |
| 11 | wrench-recovery | 140 | wrench-recovery | 08 / 08 | 130 |
| 12 | release-grip | 50 | release-grip | 09 / 09 | 50 |
| 13 | shoulder-reset | 90 | shoulder-reset | 10 / 10 | 90 |
| 14 | return-to-guard | 100 | return-to-guard | 11 / 11 | 100 |

Identidade buscada: hoist de uma mão, coil sustentado acima da cabeça (155 ms, como o frontal), descida comprometida, contato pesado de 115 ms e weight-settle/wrench-recovery. Os 225 ms acima dos 1005 ms frontais incluem dois estágios adicionais de hoist e uma descida intermediária, mais margem de desaceleração; weight-settle de 120 ms e wrench de 140 ms excedem os 110/130 ms frontais. A progressão principal é -20° → 20° → 65° → 110° → 120°, com retorno posterior para 100°. Não foi estendido o arco da espada para simular massa de machado.

## Bookends e flash confirmado do ombro

O achado do criador foi reproduzido: body/00 V6 é byte-idêntico ao PNG do Idle back_l F00 (e também igual em RGBA). O problema não era um arquivo quebrado: o material do ombro no corpo Idle é diferente dos corpos de ataque adjacentes. ROI medida: nativo x35..60 / y25..52.

| Família | Pixels neutros claros no Idle/bookend V6 | Ataque V6 F01 | Pico luma V6 bookend → ataque | Novo F14→F00 |
|---|---:|---:|---|---|
| Sword | 17 | 3 | 172.402 → 153.815 | 0 pixels de corpo divergentes |
| Axe | 17 | 5 | 172.402 → 153.815 | 0 pixels de corpo divergentes |

Contagem diagnóstica: mínimo RGB ≥140, amplitude RGB <30; luma BT.601. Coordenadas, cores e saltos locais ≥30 estão em bookend-flash-audit.json. Não foi usado filtro global de brilho.

Os novos bookends herdam ataque F01, nunca Idle/V6 F00/F11. Ombro esquerdo é pixel-idêntico entre F00/F01 e F13/F14, e todo o corpo F14/F00 é idêntico. O Sword settle-grip F12 também foi levado à base de ataque F01: a primeira versão mantinha a fonte F10, reintroduzindo material Idle antes da volta; essa hipótese foi descartada. Assim, não foi apenas deslocado o flash para outro bookend. O corpo de guarda fica sem armas, compatível em identidade/apoio com Idle, sem modificar o próprio Idle. A transição real Idle→Attack no runtime permanece fora do escopo Unity.

[Ombro Sword antes](full-cycle/sword-bookend-before.png) · [depois](full-cycle/sword-bookend-after.png) · [Axe antes](full-cycle/axe-bookend-before.png) · [depois](full-cycle/axe-bookend-after.png). Colunas: antes F10/F11/F00/F01; depois F12/F14/F00/F01.

Esse resultado elimina a descontinuidade específica do ombro na volta do ciclo. Highlights metálicos legítimos ainda existem durante o ataque; não foi alegada ausência universal de flicker perceptivo por uma regra de luminância.

## Medições de juntas por quadro

Coordenadas nativas 128; somar [64,64] no composto. Incerteza visual dos centros doadores: aproximadamente ±1 px. Precisão decimal é só cálculo geométrico.

### Sword

| F | Fase | Ombro | Cotovelo | Punho | Palma | Úmero/antebraço px | Ângulo interno |
|---|---|---|---|---|---|---|---|
| 00 | rest | [86, 40] | [102, 57] | [98, 76] | [94, 81] | 23.345 / 19.416 | 124.847° |
| 01 | body-preparation | [86, 40] | [108, 48] | [103, 67] | [99, 72] | 23.409 / 19.647 | 95.24° |
| 02 | establish-grip | [86, 40] | [109, 37] | [112, 53] | [110, 58] | 23.195 / 16.279 | 93.188° |
| 03 | anticipation-open | [88, 40] | [106, 39] | [114, 47] | [119, 50] | 18.028 / 11.314 | 131.82° |
| 04 | anticipation | [88, 40] | [108, 51] | [115, 41] | [118, 35] | 22.825 / 12.207 | 96.181° |
| 05 | coil-behind | [88, 39] | [111, 44] | [110, 31] | [108, 24] | 23.537 / 13.038 | 73.337° |
| 06 | apex-hold | [88, 39] | [111, 37] | [105, 25] | [100, 19] | 23.087 / 13.416 | 68.405° |
| 07 | slash-release | [88, 40] | [109, 50] | [114, 39] | [116, 32] | 23.259 / 12.083 | 88.981° |
| 08 | slash-drive | [85, 43] | [108, 43] | [119, 52] | [120, 56] | 23.0 / 14.213 | 140.711° |
| 09 | contact | [83, 48] | [104, 56] | [110, 75] | [109, 81] | 22.472 / 19.925 | 128.38° |
| 10 | follow-through | [81, 48] | [100, 62] | [102, 81] | [100, 87] | 23.601 / 19.105 | 132.393° |
| 11 | recoil | [82, 46] | [102, 57] | [99, 77] | [96, 82] | 22.825 / 20.224 | 110.28° |
| 12 | settle-grip | [86, 40] | [104, 56] | [98, 75] | [94, 79] | 24.083 / 19.925 | 114.108° |
| 13 | release-grip | [86, 40] | [102, 57] | [98, 76] | [94, 81] | 23.345 / 19.416 | 124.847° |
| 14 | return-to-guard | [86, 40] | [102, 57] | [98, 76] | [94, 81] | 23.345 / 19.416 | 124.847° |

### Axe

| F | Fase | Ombro | Cotovelo | Punho | Palma | Úmero/antebraço px | Ângulo interno |
|---|---|---|---|---|---|---|---|
| 00 | rest | [88, 41] | [104, 57] | [98, 75] | [94, 80] | 22.627 / 18.974 | 116.565° |
| 01 | body-preparation | [88, 41] | [110, 49] | [101, 66] | [97, 70] | 23.409 / 19.235 | 82.086° |
| 02 | establish-grip | [89, 39] | [110, 37] | [111, 53] | [110, 58] | 21.095 / 16.031 | 88.136° |
| 03 | anticipation | [89, 39] | [104, 34] | [113, 42] | [119, 45] | 15.811 / 12.042 | 119.932° |
| 04 | hoist-transition | [89, 39] | [108, 48] | [114, 38] | [116, 31] | 21.024 / 11.662 | 95.618° |
| 05 | hoist | [89, 39] | [111, 43] | [107, 31] | [103, 24] | 22.361 / 12.649 | 61.26° |
| 06 | overhead-coil | [89, 39] | [110, 31] | [101, 20] | [95, 15] | 22.472 / 14.213 | 71.565° |
| 07 | cleave-drive | [88, 42] | [109, 50] | [114, 39] | [116, 32] | 22.472 / 12.083 | 93.589° |
| 08 | downstroke | [84, 46] | [107, 45] | [117, 53] | [119, 57] | 23.022 / 12.806 | 138.851° |
| 09 | heavy-impact | [82, 49] | [105, 52] | [103, 71] | [101, 76] | 23.195 / 19.105 | 91.422° |
| 10 | weight-settle | [81, 50] | [104, 54] | [98, 72] | [95, 77] | 23.345 / 18.974 | 81.431° |
| 11 | wrench-recovery | [83, 47] | [106, 46] | [102, 65] | [99, 70] | 23.022 / 19.416 | 75.622° |
| 12 | release-grip | [87, 43] | [107, 55] | [99, 73] | [95, 77] | 23.324 / 19.698 | 97.001° |
| 13 | shoulder-reset | [88, 41] | [104, 57] | [98, 75] | [94, 80] | 22.627 / 18.974 | 116.565° |
| 14 | return-to-guard | [88, 41] | [104, 57] | [98, 75] | [94, 80] | 22.627 / 18.974 | 116.565° |

## Preservação e verificações

372 arquivos protegidos conferidos por SHA-256: fontes traseiras V6, armas V5, chaves manuais anteriores e entrega rear-r (arte/evidência). Nenhuma escrita foi executada em rear, rear-r, frontal, V6/V5, Unity ou commits. A leitura dos frontais de referência não os modifica.

Nos dois ciclos: 30 quadros com um único componente corporal 8-conectado e centros das juntas sobre corpo opaco; zero pixel de arma abaixo de groundY190; equipamento e handFront transparentes fora do intervalo de ataque. NativePng é recorte body com zero diferenças; composição alpha-over das quatro camadas igual ao PNG com zero diferenças. Mestres 256/128 salvos, fechados, reabertos e reexportados com cel.position real e tempos em segundos, comparados aos buffers em RGBA. Tiras 15×128 e 15×256 presentes e com hashes reais.

A cabeça, o núcleo do tronco, pernas, tassets e braço oposto herdam as poses de ataque da própria vista/família; não foram congelados em um único corpo nem trocados por V4. As alterações de reconstrução incidem sobre o membro dominante, ligação à ombreira e resíduos antigos; variação de apoio/tronco vem das poses V6 de ataque já existentes.

## Limitações e checkpoint

Completude técnica e análise de juntas não concedem aprovação artística. O criador ainda precisa avaliar acabamento do úmero/cota redesenhados, rotação do punho em profundidade, peso do Axe e fluidez em velocidade normal/tática. A comparação frontal registra a identidade técnica pretendida; não é uma afirmação de equivalência artística já aprovada.

Nenhuma fase foi entregue como membro ausente, punho fundido ao ombro ou forearm sem terminação: as poses foram examinadas em body-only e compostas e os resíduos encontrados foram corrigidos. A projeção curta do antebraço nas fases de giro continua sendo uma decisão artística local a revisar, explicitada pelas medidas. Nenhuma interpolação de IA ou geração futura foi autorizada/usada.

Parada em V7_BACK_L_FULL_MANUAL_READY. Sem promoção da matriz canônica ou integração automática.

Player conferido em Edge/Chromium headless: 240 comparações canvas↔PNG exatas (15 quadros × 2 famílias × body/composto × 4 painéis), alinhamento por fase e tempos próprios, relógio 1×/0,5×, pausa terminal sem repetir, passo/zoom/tático, juntas e HTTP/file. Nenhum erro JavaScript. browser-check.json e capturas *-preview-check.png/*-tactical-check.png registram a verificação. Contrato final: todos os hashes declarados conferem, alfa nativo binário {0,255}, corpo sem corte nas bordas do canvas e mestres separados 256/128.
