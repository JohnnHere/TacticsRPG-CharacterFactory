# Experimento 02 — estágios B, C, D e E

Estado técnico: **TECHNICALLY_COMPLETE** para os arquivos deste estudo. Estado artístico: **VISUAL_REVIEW_REQUIRED**, `PENDING_CREATOR`. Cinco poses estáticas não demonstram continuidade temporal nem concedem aprovação artística.

Abra `review.html` para comparar as quinze renderizações e os recortes da pegada. `evidence/overview.png` reúne corpo, arma e composição. Cada PNG está identificado por legenda na revisão e por metadado textual de procedência; não há texto desenhado sobre o sprite transparente.

## Escopo e procedência

Orc principal `orc-v1`, `back_l`, espada oficial do Recruta, quadros 00/05/08/09/13. Zero chamadas de geração. Nenhum commit, promoção ou integração. Toda saída deste trabalho está nesta pasta. Fontes canônicas foram somente lidas.

`author.lua` roda no Aseprite 1.3 em batch `--noinapp`, com perfil local separado sem carregar PixelLab. Os cinco mestres `source/NN.aseprite` contêm `weaponBack → body → weaponFront → handFront`; foram salvos, reabertos e renderizados pelo editor. Trata-se de composição e transformação programática no Aseprite sobre arte herdada, não desenho manual nem geração nova. `verify.py` produz apenas ampliações e pranchas de inspeção por nearest-neighbour. `document.py` registra contratos e valida pixels/paleta. A espada oficial não foi redesenhada. O corpo permanece RGBA idêntico à camada de origem em todos os quadros.

Os quadros 00 e 13 do clipe original estão desarmados. Aqui recebem **montagem armada diagnóstica** para cumprir a comparação de pegada em cinco poses solicitada no brief. Isso não propõe arma em repouso/recuperação no runtime: a política `attack-only-v1` de produção permanece vigente. Esta distinção substitui a intenção inicial de manter esses dois renders desarmados anunciada durante o trabalho.

## B — cinco poses anatômicas

Coordenadas no composto 256×256, X à direita, Y para baixo; nativo128 tem deslocamento [+64,+64]. Ombro/cotovelo/punho são estimativas visuais (±3 px); contato da mão é o ponto exato usado para composição. Lados são anatômicos: mão direita empunha, esquerda livre, flanco esquerdo próximo da câmera. Não houve espelhamento.

Foram consultados `poses-fixed.json` e `sequence-fixed.json` do experimento anterior. Eles fornecem a intenção de arco diagonal alto→baixo e a identificação das juntas. Não são copiados cegamente: o próprio quadro 00 da referência foi descrito a partir do 02 armado, e a arte v8 contém reposicionamentos locais posteriores. Exemplo: no 05 a referência de esqueleto põe a mão em aproximadamente (146,72), mas o contato da luva na arte atual e o contrato `rightGrip` estão em (160,81). `attachment.json` preserva a referência completa por quadro e os metadados `manualJointsNative` herdados para tornar essa diferença auditável. Forçar a arma aos pontos antigos a soltaria da mão real.

| Quadro | Ombro D | Cotovelo D | Punho D | Contato mão D | Tronco e quadril | Apoio/chão | Cabo pretendido |
|---|---|---|---|---|---|---|---|
| 00 Preparação | 150,104 | 166,121 | 162,140 | 158,145 | Dorso em três quartos; tórax vertical, quadril centrado entre as botas | Base aberta, duas botas apoiadas; sola terminal y=190 | Lâmina acima/direita, pomo abaixo/esquerda; montagem diagnóstica |
| 05 Elevação | 152,103 | 175,101 | 165,88 | 160,81 | Ombro direito elevado, cotovelo lateral e antebraço dobrado para cima; quadril mantém base | Duas botas, sem deslocamento vertical global; chão y=190 | Vertical, lâmina para cima; luva fecha abaixo da guarda |
| 08 Contato | 147,112 | 168,120 | 181,125 | 178,131 | Ombro desce e braço se estende; torso inclina discretamente à direita da imagem, quadril contrapesa | Apoio bilateral; não inventar salto ou deslizamento; chão y=190 | Lâmina abaixo/esquerda, pomo acima/direita |
| 09 Seguimento | 145,112 | 164,126 | 173,150 | 169,159 | Cotovelo e punho descem, braço volta a dobrar; tórax acompanha sem rotação global do sprite | Botas mantêm contato, base aberta; chão y=190 | Diagonal abaixo/esquerda mais aberta; arco termina baixo |
| 13 Recuperação | 150,104 | 166,121 | 162,140 | 158,145 | Retoma geometria de 00; cintura e quadril estabilizados | Mesmo apoio de 00; chão y=190 | Volta ao eixo alto/direita apenas para diagnóstico de ligação |

O arco da lâmina de 05→08→09 passa de alto para baixo/esquerda. Não foi minimizado deslocamento. O corpo herdado conserva braço lateralmente estendido em 08; essa pose isolada permite inspecionar pegada, mas sua naturalidade como corte diagonal ainda precisa de julgamento temporal. Não afirmo que três mudanças de orientação resolvam a coreografia inteira. Não alterei anatomia/torso para fabricar essa conclusão.

## C — espada independente

Fonte oficial: `characters/orc-v1/source/combat-rescue-v5/combat/weapons/Sword/recruit-sword.png`, contrato `weapon.json`: 96×96, uma mão direita, grip/pivô local (48,66), escala 1. Hashes reais dos arquivos de entrada e saída estão em `attachment.json`.

| Quadro | Contato mão = contato cabo = pivô destino | Rotação horária desde lâmina vertical | Eixo lâmina (dx,dy) | Decisão |
|---|---|---|---|---|
| 00 | 158,145 | +20° | +0,342 / -0,940 | Apresentação diagnóstica sobre a mão fechada existente |
| 05 | 160,81 | 0° | 0 / -1 | Vertical sem reamostragem angular, ápice alto |
| 08 | 178,131 | -138,65° | -0,661 / +0,751 | Corrige a antiga orientação para baixo/direita |
| 09 | 169,159 | -131,35° | -0,751 / +0,661 | Seguimento baixo/esquerda, sem pivotar sobre centro fixo |
| 13 | 158,145 | +20° | +0,342 / -0,940 | Mesmo encaixe de 00, diagnóstico |

Cada transformação usa o ponto da mão daquela pose como pivô destino; não há centro fixo no palco. A amostragem inversa arredonda ao pixel inteiro no Aseprite, sem interpolação de cor, blur ou escala. Não se criou rigging. Lâmina, canal, guarda e pomo mantêm os materiais oficiais; o pequeno serrilhado diagonal é próprio da grade. A perspectiva não foi encurtada artificialmente.

Separação: pixels da arma com y local 60..73 (cabo) vão a `weaponBack`; o restante a `weaponFront`. O cabo central fica atrás da luva/corpo; a guarda fica fora da mão e a pequena sobra junto ao pomo permanece visível conforme a oclusão real. A arma inteira, inclusive o cabo ocultado, pode ser conferida em `weapon-only`. `handFront` restaura os dedos/luva por último. Nos extremos 00/13, reaproveitei apenas os pixels existentes da luva na região [151..163,139..153], sem pintar máscara opaca, trocar paleta ou inventar outra mão.

## D — avaliação visual da pegada

Inspeção do corpo inteiro e das cinco ampliações em 8×, além das camadas isoladas. Avaliação do produtor, não aprovação do criador.

| Quadro | Palma, cabo e dedos/luva | Punho e antebraço | Profundidade e limite |
|---|---|---|---|
| 00 | Volume marrom fechado recobre o cabo; guarda sai acima da luva, não atravessa uma palma aberta | Placa da luva continua até a braçadeira; braço relaxado herdado | A guarda projeta-se diante da silhueta; diagnóstico de sustentação estática, sem validar entrada do ataque |
| 05 | Cabo entra sob a luva fechada e sai sob a guarda; silhueta de dedos herdada na frente | Punho elevado acompanha a dobra do antebraço; não há cabo aplicado por cima da palma | Guarda e lâmina acima do punho; fundo do cabo oculto no corpo. Leitura de mão fechada preservada |
| 08 | Cabo diagonal escondido pelo núcleo marrom da luva; guarda fica abaixo/esquerda dos dedos | Braçadeira continua a luva; punho roda em relação à vertical anterior | Lâmina cruza a frente do corpo na projeção; essa atribuição de profundidade precisa da avaliação artística do criador no movimento |
| 09 | Mesmo material e volume da luva, dedos sobre o cabo; guarda acompanha a descida | Cadeia ombro→cotovelo→punho contínua na silhueta herdada | Pomo emerge acima/direita, lâmina termina abaixo/esquerda; proximidade da perna é oclusão projetada, não arma pintada no corpo |
| 13 | Byte/pixel geometry de 00; não muda o indivíduo nem o tamanho da mão | Postura relaxada restaurada | Montagem diagnóstica; deve continuar oculto no uso runtime original |

A sobreposição provém da própria luva, não de um disco/retângulo pintado para esconder ligação ruim. Ainda há limite de leitura: a luva escura não separa cada dedo individual na escala 1×, e a aprovação da pegada cabe ao criador. Não foi declarada consistência temporal entre os quadros intermediários que não integram este estudo.

## E — contorno, sombreamento e origem de artefatos

| Região/quadros | Origem identificada | Ação localizada | Verificação / limite |
|---|---|---|---|
| Lâmina em 08/09 do antes | Camadas de arma transformadas: rotações herdadas +115°/+128° apontavam abaixo/direita | Recompus só a arma oficial no Aseprite em -138,65°/-131,35°, ancorada nas mesmas mãos; corpo intacto | Arco projetado abaixo/esquerda, largura/material mantidos; inspeção 1× e 8× |
| Cabo/palma em 00/13 | Composição: originalmente sem arma e sem `handFront` útil | Montagem diagnóstica, cabo atrás do corpo e pixels da luva herdada na frente | Não existe máscara sólida nova; corpo original igual em RGBA |
| Fragmento de pomo separado na arma isolada do antes | Empacotamento da arma: cabo central estava na outra camada (`weaponBack`) | `weapon-only` reúne ambas as partes; não remover o pomo como pixel perdido | Arma isolada nova apresenta cabo contínuo; partes ocultas no composto têm explicação anatômica |
| Cinzas claros nas ombreiras, braçadeiras e guarda | Sombreamento legítimo de aço herdado do corpo/arma | Preservado integralmente; nenhum escurecimento global | Corpo igual em RGBA; cores opacas da arma são subconjunto exato da paleta oficial |
| Contorno externo dos cinco corpos e lâminas | Camadas separadas inspecionadas contra fundo cinza e transparência | Nenhuma limpeza adicional injustificada | Não identifiquei halo branco/pálido, brilho duplicado ou pixel solto inexplicado na inspeção; esta é observação visual, não prova universal |

`pixel-checks.json`: os 15 PNGs têm 256×256 e zero pixels de alfa parcial. O detector restrito de neutros pálidos (mínimo RGB≥180 e amplitude≤18) marcou zero em todos. Essa métrica não substitui a inspeção visual nem prova ausência de qualquer tom de halo. `verification.json` confirma identidade RGBA dos cinco corpos e preservação da paleta opaca da espada nas cinco transformações. A imagem de aço e o escuro do contorno não foram normalizados nem recoloridos.

Não encontrei defeito do corpo que justificasse retoque seguro neste recorte de tarefa. A limitação herdada mais importante é a diferença entre juntas planejadas no esqueleto e a anatomia realmente reposicionada no v8: está registrada, não escondida. Se a pose corporal de contato for rejeitada artisticamente, ela exigirá um passe anatômico próprio no Aseprite, não reposicionar a espada por uma referência antiga.

## Arquivos e reprodução

- `body-only/`, `weapon-only/`, `composite/`: quinze PNGs transparentes, índices 00/05/08/09/13.
- `source/`: cinco mestres editáveis com quatro camadas independentes.
- `attachment.json`: pivôs, contatos, orientação, oclusão, anatomia, fontes e hashes.
- `evidence/NN-*-hand-wrist-8x.png`: quinze recortes (corpo/arma/composição), exatamente 40×40 pixels do original ampliados a 320×320 sem interpolação.
- `inspection.png` e `grip-before.png`: evidências do estado anterior, somente pranchas de inspeção.
- `author.lua`: autoria/composição Aseprite. Executar na raiz com `Aseprite.exe --batch --noinapp --script experiments/main-orc-skeleton-02/stage-bcde/author.lua`, usando `ASEPRITE_USER_FOLDER` apontado para `stage-bcde/batch-profile`.
- `verify.py` e `document.py`: previews e validação/metadados; não produzem arte nova.

Nenhum recurso foi promovido. Próximo marco deste estudo: parecer artístico do criador sobre as cinco pegadas e sobre a pose de contato.
