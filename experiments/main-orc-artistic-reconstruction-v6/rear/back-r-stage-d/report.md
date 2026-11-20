# V6 — Etapa D, adaptação back_r

Checkpoint: **V6_BACK_R_ADAPTATION_READY**. Estado técnico: **TECHNICALLY_COMPLETE**. Estado artístico: **VISUAL_REVIEW_REQUIRED**, `PENDING_CREATOR`. A Etapa D entrega as duas células back_r para revisão do orquestrador.

## Autorização e preservação

O orquestrador aceitou evidência, proveniência e honestidade do checkpoint `V6_BACK_L_REFERENCE_READY` como referência, considerou a Etapa C satisfeita pelo playback verificado e liberou expressamente a Etapa D. Isso autoriza a adaptação `back_r`; não concede `CREATOR_APPROVED`.

O freeze back_l `624776482981d71e8979c8f1dcb65ae75c28c798485a963f8393aa85f6b5f366` foi verificado antes do trabalho: **191 arquivos sem diferenças**. Seus mestres, pixels, scripts, relatórios, recibos, manifesto e preview permanecem congelados. As indicações de bloqueio C–D nos documentos históricos desse freeze são mantidas por imutabilidade; a autorização vigente está registrada aqui.

A adaptação grava novos clipes `back_r-sword` e `back_r-axe` no mesmo diretório canônico `rear/`, e evidência própria em `rear/back-r-stage-d/`. O manifesto de patch da Etapa D terá nome próprio; o manifesto congelado back_l não é reescrito. Sem Unity, commits ou mudanças em Idle/Walk/Unarmed/Hit/Defeat/frontais.

## Fundamento artístico

A [auditoria original](../audit.md) classificou os quadros back_r. O problema prioritário é a continuidade de joelhos, botas e transferência de peso, especialmente na espada. KEEP conserva somente os bookends desarmados da vista correta. Os intermediários são reconstruídos como sequência completa a partir da base `back_r` V1, sem espelhar back_l ou frontal, e sem reutilizar pixels entre famílias.

O método segue a referência back_l: `animate_with_skeleton_v3`, corpos inteiros desarmados por pose, profundidade explícita de ombro/cotovelo/punho direito, acabamento cirúrgico no Aseprite e itens independentes. A descrição corporal nunca nomeia equipamentos de ataque. Os esqueletos têm âncoras constantes de tornozelos e deslocamento encadeado de quadril/joelhos. Essa intenção não prova apoio estável no resultado: os PNGs são inspecionados layers-off e a região das pernas tem folhas próprias.

Sword mantém a curva diagonal, 12 quadros/950 ms. Axe mantém preparação sustentada, maior abaixamento e recuperação, 12 quadros/1320 ms. Esses tempos preservam o ritmo por família da referência; a arte e os esqueletos são próprios da nova vista. A mão direita é a dominante e a esquerda serve ao equilíbrio.

## Evidências e limites

Pedidos, sementes, jobs e recibos estão nesta pasta. A seleção de poses, palmas e máscaras de oclusão está documentada por quadro em [anatomy-plan.json](anatomy-plan.json) e nos `clip.json`. Pillow só lê imagens e monta diagnósticos; toda mutação e exportação artística ocorre no Aseprite **1.3.18.6**, batch `--noinapp`, perfil `tmp/aseprite-v6-rear-profile`.

| Família | Job | Seed | Saídas / consumo declarado |
|---|---|---:|---|
| Sword | `c96553ff-9ce0-44a2-88fc-0694d1831b03` | 63130 | 12 poses / 3 gerações |
| Axe | `099226ff-7b53-4b59-9cf7-40f0ce387fed` | 64130 | 12 poses / 3 gerações |

Foram **dois jobs, 24 saídas brutas e 6 gerações** nesta Etapa D. Saldo medido **1288,70 → 1282,70**, diferença de 6,00, coincidente com os dois recibos. Nenhuma compra, estimativa monetária ou contagem de tokens. A contabilidade histórica back_l permanece no freeze anterior. [Ledger da Etapa D](pixellab-ledger.json).

## KEEP, reconstrução e acabamento

F00/F11 de ambas as famílias conservam a base desarmada da própria vista back_r. F01–F10 usam os respectivos quadros completos de cada novo job, com proveniência individual no manifesto. A hipótese original de correção localizada em F01/F02 e de timing em F10 foi absorvida pela nova sequência corporal: manter intermediários V5 dentro de uma mecânica nova introduziria outra emenda. A classificação da auditoria histórica permanece intacta.

| Quadros | Função / decisão na adaptação |
|---|---|
| F00 | KEEP: identidade, direção e apoio de entrada |
| F01–F02 | REAUTHOR_KEYFRAME: preparação encadeada com a nova base de apoio |
| F03–F04 | REAUTHOR_KEYFRAME: elevação e carga próprias de cada família |
| F05–F06 | REAUTHOR_KEYFRAME: aceleração e descida com participação do tronco |
| F07–F08 | REAUTHOR_KEYFRAME: absorção/follow-through com flexão contínua dos joelhos |
| F09–F10 | REAUTHOR_KEYFRAME: recuperação encadeada até o bookend; ritmo por família preservado |
| F11 | KEEP: fechamento desarmado compatível com a entrada |

Os corpos selecionados foram inspecionados inteiros sem as camadas de equipamento. Não há equipamento de ataque reconhecível no corpo nas poses selecionadas; esse é um achado visual do DEV. A sequência dos braços conserva a cadeia ombro–cotovelo–punho visível. Cada luva vem de sua própria pose, incluindo a superfície metálica dorsal quando a mão está rodada, com palma medida e oclusão extraída dos pixels acabados. Não se infere pegada convincente apenas da coordenada do grip.

Perna, bota e tassets mantêm os pixels de seus respectivos quadros brutos, com limpeza periférica no Aseprite. A inspeção das folhas de pernas mostra flexão progressiva na descida e retorno gradual, sem a troca abrupta de stance observada no V5. O comprimento aparente das canelas permanece coerente durante o apoio; pequenas variações de pixels de luz e de contorno entre poses ainda exigem julgamento artístico em movimento.

O acabamento local normaliza alfa, escurece neutros claros apenas no contorno externo e remove componentes minúsculos desconectados. A versão inicial do binding foi arquivada em `initial-binding/`: no impacto/follow-through, a geometria real do item ficava projetada abaixo do chão. A correção ajustou os ângulos próprios de back_r em F07–F09, mantendo corpo, asset independente e escala. O machado mostra pequena acomodação depois do impacto, acompanhando a recuperação corporal; a espada mantém saída diagonal. A revisão foi feita no Aseprite, sem geração adicional.

## Contratos e playback da versão exata

Dois mestres compostos 256 e dois mestres de corpo 128 foram salvos, reabertos e reexportados. Pixels RGBA e tempos foram comparados dentro do Aseprite, respeitando `cel.position`; `Frame.duration` foi atribuído em segundos. Registro corporal `[64,64]`, `groundY` composto 190 e nativo 126 em todos os quadros. Quatro camadas `weaponBack → body → weaponFront → handFront`. `nativePng` é exclusivamente o recorte do corpo. Intervalo de equipamento inclusivo F01–F09; F00/F10/F11 têm camadas de equipamento transparentes e composto igual ao corpo.

[Preview antes/depois](preview.html): reprodução normal/0,5×, passo, slider, nativo 1×, escala tática 0,5× e zoom; corpo inteiro layers-off e composto em paralelo. O link para o preview back_l congelado permite comparação com a referência aceita. [Checks Chromium](preview-check.json) conferem os **48 renders**: 24 quadros de corpo e 24 compostos, pixels exibidos iguais aos PNGs finais, controles e relógio de reprodução. Foram exercitados 1×/0,5× e nativo/tático após a correção do binding. Leitura do DEV: preparação, aceleração, absorção e recuperação são distinguíveis; Axe sustenta mais carga e abaixamento que Sword.

[Contratos e roundtrip](technical-checks.json), [diagnósticos selecionados](selected-diagnostics.json), [pernas Sword](sword-selected-legs.png), [pernas Axe](axe-selected-legs.png) e [preservação da produção anterior](preservation-check.json). O inventário inicial de **5907 arquivos** permaneceu byte-idêntico. [Verificação final do freeze back_l](back-l-freeze-after.json) cobre também sua documentação, scripts e evidência.

O patch específico está em `characters/orc-v1/source/artistic-reconstruction-v6/rear/patch-manifest-back-r-stage-d.json`. O manifesto combinado `patch-manifest-stage-d.json` referencia as quatro células traseiras e mantém os mesmos hashes do back_l congelado; nenhum ponteiro ativo de produção foi promovido.

Controles numéricos de pés, igualdade de composição, hashes e playback funcional não equivalem a aprovação artística. A legibilidade de peso, a continuidade do comprimento aparente das pernas, a pegada e a direção projetada do golpe permanecem questões visuais. A revisão final do criador continua pendente.

Próximo marco: revisão do orquestrador sobre o freeze da Etapa D. Esta frente encerra na adaptação back_r, sem abrir produção frontal ou integração Unity.
