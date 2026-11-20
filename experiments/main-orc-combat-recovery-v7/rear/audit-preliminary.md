# Auditoria preliminar V7 — back_l

Estado: ARTISTIC_REVISION_REQUIRED. O marco V7_BACK_L_REBUILT não foi atingido. Esta análise é preliminar; não há novos ciclos ou aprovação artística.

Comparei as tiras compostas V6 back_l Sword/Axe com front_l correspondentes e li as fases e durações dos quatro clipes. Sword frontal tem preparação, coil, ápice, liberação, contato e follow-through em 30/65/35/50/45/65/35/35/100/55/80/45/90 ms. Axe frontal enfatiza overhead-coil 155 ms, drive 35 ms, impacto 115 ms e assentamento 110 ms.

No Sword traseiro o instrumento sobe ao lado da cabeça, mas o braço se estende para a direita da imagem e o instrumento passa quase horizontal lateralmente; a placa dorsal e os ombros mudam pouco e a mão não descreve uma descida clara em direção ao alvo. Isso favorece leitura de varredura lateral apesar dos nomes de fase no JSON. A causa mecânica exata permanece hipótese visual, não medição tridimensional. No Axe traseiro também aparece extensão lateral e uma sequência de mão baixa com pouca distinção do peso da cabeça; a trajetória e a pegada precisam de reautoria, não apenas de mudar ângulos. A presença e origem exatas do flash relatado pelo criador ainda precisam de inspeção temporal em pixels.

## Classificação inicial por quadro

- Sword F00 e F11: KEEP como candidatos de bookend, sujeitos à inspeção layers-off.
- Sword F01–F04: REAUTHOR_KEYFRAME: antecipação e elevação devem mostrar carga corporal e mão alta; F04 atual não estabelece suficientemente o ápice.
- Sword F05–F09: REAUTHOR_KEYFRAME: liberação lateral, impacto e recuperação não demonstram a técnica frontal.
- Sword F10: REMOVE_OR_REPLACE: transição deve ser revista junto da nova recuperação.
- Axe F00 e F11: KEEP como candidatos de bookend, sujeitos à inspeção layers-off.
- Axe F01–F04: REAUTHOR_KEYFRAME: carga própria com cotovelo e mão elevados e peso na cabeça.
- Axe F05–F09: REAUTHOR_KEYFRAME: descida, impacto, assentamento e retirada devem formar cadeia contínua específica.
- Axe F10: REMOVE_OR_REPLACE: transição depende da nova recuperação.

## Intenção de fases para reconstrução

Sword: repouso desarmado; preparação de tronco; estabelecimento da mão; cotovelo e mão sobem com rotação do ombro; ápice legível; aceleração diagonal descendente; contato; continuação do movimento; retorno progressivo e repouso desarmado. O eixo deve ser interpretado em profundidade na vista traseira, sem copiar coordenadas frontais.

Axe: repouso; preparação; carga mais sustentada sobre o ombro; ápice alto; drive descendente curto; impacto pesado; assentamento; retirada controlada; retorno. O corpo e o ritmo não devem ser apenas uma troca de item do Sword.

Antes de composição, inspecionar cada pose inteira desarmada, confirmar mão direita anatômica e continuidade ombro–cotovelo–punho–palma; depois desenhar a oclusão da luva por pose no Aseprite. Faltam geração, auditoria layers-off, composição, mestres, verificação de flash/solo e preview comparativo.

## Execução adicional — 30/10/2026

- Sword job `3c317a5e-6d18-40df-8821-916cff08e5ef`, seed 71031, 3 gerações: rejeitado; punho elevado fundido/oculto no ombro. Raw em `raw/sword/`.
- Axe job `5778d0c6-df27-4c7c-b5d7-7dd1fb939795`, seed 71032, 3 gerações: rejeitado pela mesma ausência de punho elevado identificável. Raw em `raw/axe/`.
- Sword tentativa 2 `b05b3cb0-7b89-4ef1-a936-7a5c17398dd0`, seed 71033, 3 gerações: punho elevado mais separado em F03–F06, mas sequência de descida/impacto não estabelece continuidade visível de antebraço e palma, requer reparo ou substituição antes da arma. Raw em `raw/sword2/`.
- Saldo inicial 1282.70; saldo após 1273.70; consumo total comprovado 9 gerações; créditos USD 0.00. Pedidos e scripts preservados nesta pasta. Os corpos não foram aceitos para montagem. Nenhum mestre ou ciclo V7 foi produzido.
