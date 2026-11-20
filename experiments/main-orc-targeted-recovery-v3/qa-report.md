# QA independente — main-orc-targeted-recovery-v3

> **Parecer corrente: seção “2ª Re-revisão”, freeze de 2026-10-27T21:43:22.059Z. PASS técnico dos assets/contratos, com ressalva documental baixa; `VISUAL_REVIEW_REQUIRED`, `PENDING_CREATOR`. Os FAIL anteriores abaixo pertencem aos freezes anteriores. Reprodução temporal artística contínua em 1×: NAO VERIFICADO.**

Data: 2026-10-27. Escopo: Orc V1 / Verde Warcraft, entrega local. Revisão independente deste agente; não é uma nova manifestação da sessão histórica Copilot `08686` nem aprovação do criador.

**Veredito técnico do pacote: FAIL. Veredito artístico: `ARTISTIC_REVISION_REQUIRED`. Aprovação: `PENDING_CREATOR`. A declaração global `TECHNICALLY_COMPLETE` não se sustenta nesta versão.** Há checks técnicos com PASS, mas também divergências visíveis entre mestres, PNGs compostos e nativos, tempos incompatíveis e aliases classificados incorretamente. Persistem defeitos críticos nos ataques traseiros.

## Versão e método

Foram lidos o snapshot, o freeze, o manifesto canônico, os scripts Lua, os quatro documentos indicados e as suites relevantes. Os PNGs foram efetivamente abertos e examinados: sequências completas, ordenadas por índice, em escala estática 1× e ampliação nearest-neighbor 2×/3×, com fundo quadriculado. As montagens de inspeção existiram somente em memória; não são nova arte nem novos arquivos. Foram examinados os quatro ataques traseiros também em `body`/`native`, com armas desligadas, e os mestres foram lidos diretamente, sem executar scripts de autoria/exportação.

**Reprodução temporal artística contínua em 1×: NAO VERIFICADO.** O teste Chromium comprovou avanço do player, redução de velocidade e hold terminal, mas não equivale a assistir ao movimento para julgar peso, ritmo, flicker ou coreografia. Os achados visuais abaixo decorrem dos quadros efetivamente vistos e da continuidade entre poses, não de uma alegada observação de vídeo.

Índices neste relatório são zero-based: F03 = `03.png`, quarto quadro.

SHA-256 da versão examinada:

| Artefato | SHA-256 |
|---|---|
| `before-snapshot.json` | `d23f65894dcb3d327bb62a4a78572246be69a469585717ac25eec39c327f01b9` |
| `delivery-freeze.json` | `9a18fbc726cb89903dd257c92fdb1efb360aba4efc20eec824ad8a34298904b3` |
| `characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json` | `66bea5614ad5b91c278f3a5a2f0f366d4ec1d582e327ee14cd88b830aedf7798` |

Os 616 registros de arquivos modificados/novos do freeze (435 + 181) conferiram com o disco, sem drift. Dos 2223 caminhos do snapshot anterior, 1788 permanecem iguais, 435 mudaram e nenhum desapareceu. Os escopos de coleta anterior/posterior diferem; estes números não devem ser confundidos com os 1784 inalterados reportados pelo coletor posterior.

## Matriz de requisitos

| Requisito | Evidência independente | Resultado |
|---|---|---|
| Preservar todos Idle e Hit, `front_r/Sword`, Axe frontal e Defeat traseiro | 13 clipes/87 quadros compostos; 261 referências conferidas diretamente com o snapshot, sem alteração. Mais 79 referências conferem com hashes nos respectivos `clip.json` preservados. Detalhamento abaixo. | PASS, com limite de cobertura explícito |
| Freeze corresponde à entrega atual | 616/616 registros modificados/novos com SHA-256 correto; nenhum arquivo anterior ausente | PASS |
| `back_r/Sword`: continuidade e pegada | F04–F05: espada/manopla de overlay separadas do punho corporal; F01–F03: resíduos de machado/haste no corpo. QA-V3-01/02. | FAIL |
| `back_l/Sword`: continuidade, pegada e corpo desarmado | F01–F07: segunda lâmina junto ao quadril direito da imagem, presente em `body` e `native`; F05: faixa clara no ombro/pescoço; arma principal cruza corpo com encaixe inconsistente. QA-V3-02. | FAIL |
| `back_r/Axe`: continuidade, pegada e corpo desarmado | F01: cabeça secundária de machado no corpo; F02–F03: haste; F04: braço/punho sem cadeia convincente; overlay não corrige anatomia. QA-V3-02. | FAIL |
| `back_l/Axe`: contorno e continuidade | F02–F03: filamento claro saliente à direita da ombreira, inclusive layers-off. Movimento pesado em tempo real não foi observado. QA-V3-03. | FAIL para limpeza; temporal NAO VERIFICADO |
| Ausência de bordas com luma arredondada ≥ 200 nas quatro armas traseiras | Script do DEV reexecutado: 32/32 compostos examinados, zero ocorrências segundo seu predicado de borda externa | PASS estritamente para essa métrica |
| Ausência visual de todos os halos/bordas claras | Limiar 200 não cobre os resíduos claros de SwordL/AxeL nem a semântica da lâmina secundária | FAIL |
| `back_l/Unarmed`: sequência consistente e sem duplicações problemáticas | Cinco compostos distintos por RGBA, mas F03 perde o braço do golpe e F04 conserva braço pendente mais fragmento de golpe. Nativos F01/F03/F04 representam outras poses. QA-V3-04/05. | FAIL |
| `back_r/Unarmed`: punho não some | No composto F03 há punho prolongando F02; `native/03.png` não incorpora o reparo (287 pixels divergentes). QA-V3-05. | PASS localizado no composto; FAIL na entrega |
| Unarmed frontal: braço oposto contínuo | Compostos F02–F03 contêm enxerto do braço de F01; PNGs nativos continuam sem esse reparo. QA-V3-05. | FAIL na entrega; melhora localizada visível |
| Back Walk: braço esquerdo não desaparece | Sequências completas F00–F07 abertas: membro presente nos quadros estáticos. Não observei reprodução contínua para excluir flicker. | PASS estático; temporal NAO VERIFICADO |
| Front Defeat: nocaute com volume preservado e fonte reprodutível | Terminal composto rebaixado por compressão regional; mestre retém silhueta antiga por baixo; nativo entregue é anterior. QA-V3-06. | FAIL |
| Não usar rotação global + vScale 0.52 | Esse procedimento específico não aparece no script atual; foi encontrado outro achatamento regional, descrito abaixo | PASS para a proibição específica; retenção de volume FAIL |
| `front_l/Sword`: axila | F00–F12 abertos, F01–F03 ampliados; não identifiquei o resíduo pontual nas posições que o reparo declara limpar. Camadas recompõem os PNGs. | PASS localizado, sem aprovação do criador |
| Front Walk: sombreado do pano | Ciclos F00–F15 abertos; quatro pixels de F08 alterados no composto, mas nativos F08 permanecem anteriores, com quatro pixels divergentes por direção | FAIL de sincronização; acabamento temporal NAO VERIFICADO |
| `weaponBack → body → weaponFront → handFront` | Ordem presente nos quatro mestres traseiros reais; recomposição das camadas dos clipes armados coincide com os PNGs compostos | PASS estrutural |
| Armas somente no ataque e corpo sem armas pintadas | Overlays separados não autorizam lâminas/hastes dentro de `body`, inclusive SwordL F07 com overlays desligados | FAIL semântico |
| Integridade dos hashes declarados nos clipes | Hashes de mestres, strips, compostos e nativos conferem. Isto não torna imagens diferentes equivalentes. | PASS de integridade, insuficiente para equivalência |
| Mestres, PNGs, nativos e tempos representam a mesma versão | Divergências de pixels e tempos listadas em QA-V3-05/06/07 | FAIL |
| 16 aliases realmente inalterados | Walk frontal nas duas vistas e Sword frontal esquerdo mudaram, embora constem como `UNCHANGED_ALIAS` | FAIL |
| Afirmação de 50/50 testes | Não repetida integralmente sob restrição de arquivo único; suites com escrita foram excluídas. Resultados efetivamente reproduzidos abaixo. | NAO VERIFICADO para 50/50 |
| Interface de revisão funciona | 20/20 checks Chromium, validação Python 28/28 e teste JS de renderização com PASS | PASS funcional |
| Documentos explicam recorrência real e distinguem hipótese de evidência | Registram técnicas úteis, mas proclamam correções definitivas contrariadas pelos arquivos, omitem reutilização de doadores antigos e falhas de exportação | FAIL |
| Nenhuma alteração Unity/PixelLab pelo DEV | Snapshot não cobre `../TacticsRPG` nem histórico auditável do serviço. Scripts examinados são locais; não há prova histórica suficiente para certificação absoluta | NAO VERIFICADO histórico |
| QA somente leitura, sem produção/PixelLab | Nenhum script de autoria, exportador ou chamada PixelLab executado pelo QA; único arquivo persistente de saída deste trabalho é este relatório | PASS |
| Aprovação do criador | Nenhuma concedida; `PENDING_CREATOR` | PASS de governança deste parecer |

## Preservação dos protegidos

| Grupo | Referências com hash direto no before-snapshot | Referências vinculadas por hashes nos clips preservados |
|---|---:|---:|
| Idle, quatro direções | 28 | 28 |
| Hit, quatro direções | 28 | 28 |
| `front_r/Sword` | 67 | 3 |
| Axe frontal, duas direções | 124 | 6 |
| Defeat traseiro, duas direções | 14 | 14 |
| **Total** | **261** | **79** |

As 340 referências incluem manifests de clipe, quadros, camadas, strips e mestres pertinentes. Não encontrei violação dos protegidos. Limite: o coletor anterior não incluiu `characters/orc-v1/sprites` nem os mestres `source/aseprite/complete-v1`; portanto as 79 referências são verificadas contra hashes registrados nos `clip.json` byte-idênticos ao snapshot, não contra hashes diretos dos arquivos físicos anteriores. Isso permite confirmar a correspondência à referência declarada, sem inventar cobertura histórica ausente.

Os três falsos aliases não pertencem ao conjunto protegido pelo pedido atual: suas alterações eram autorizadas, sua classificação de inalterados é que está errada. A classificação correta da abrangência deste passe deve considerar 15 células tocadas e 13 protegidas, em vez de reaproveitar sem ressalvas o resumo 12/16 do passe anterior.

## Achados por gravidade

### QA-V3-01 — CRÍTICO — espada direita solta do braço

Em [back_r/Sword F04](../../characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2/04.png) e [F05](../../characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2/05.png), o cabo/manopla circular do overlay fica no espaço à direita/acima da extremidade do braço. É visível em 1× e inequívoco em 2×: a espada desloca-se independentemente do punho corporal. F06 aproxima o equipamento novamente; essa aproximação não resolve a interrupção anterior.

Causa verificável no script `author_rear_weapons_targeted.lua`: grips/ângulos são tabelas independentes da anatomia real, e SwordR usa o mesmo diretório de corpos `axe-r-cleaned-native` de AxeR. Os oito corpos de SwordR e AxeR têm pixels visíveis idênticos. O algoritmo `renderCurledGlove` desenha um disco de raio 4,2 com sulcos, mas não usa seus argumentos `angle` e `weaponType` para orientar a mão. Contorno e progressão angular não reconstroem ombro–cotovelo–punho nem garantem dedos envolvendo o cabo no ponto correto.

### QA-V3-02 — CRÍTICO — contaminação de armas dentro do corpo e recorrência dos defeitos anteriores

- [SwordL body F07](../../characters/orc-v1/source/rear-recovery-v2/back_l/Sword/Attack-representative-v1/layers/body/07.png): lâmina clara persiste ao lado do quadril direito da imagem, mesmo no retorno sem overlays. O volume aparece também em F01–F06. [Body F05](../../characters/orc-v1/source/rear-recovery-v2/back_l/Sword/Attack-representative-v1/layers/body/05.png) mantém faixa clara sobre ombro/pescoço.
- [AxeR body F01](../../characters/orc-v1/source/rear-recovery-v2/back_r/Axe/Attack-representative-v1/layers/body/01.png): cabeça secundária de machado junto ao braço erguido. [F02](../../characters/orc-v1/source/rear-recovery-v2/back_r/Axe/Attack-representative-v1/layers/body/02.png) e F03 mantêm haste marrom acima do punho. A mesma contaminação está em SwordR porque os corpos são iguais.
- Em AxeR/SwordR F04, a construção do braço termina de modo truncado; acrescentar mão/arma em outra coordenada deixa a cadeia articular sem continuidade. Em AxeR F05, a sobreposição reforça a leitura de extremidades incompatíveis.

São constatações deste freeze, não mera transcrição do QA histórico. A origem imediata é rastreável: o Lua volta a carregar `axe-r-cleaned-native` e `back_l-sword-cleaned-native`, em vez de garantir os cels reparados do estado anterior. `cleanBodyEdges` só escurece certos pixels perimetrais; não remove armas nem reconstrói anatomia. A existência de quatro camadas e seu alpha-over correto não passa o requisito semântico layers-off.

### QA-V3-03 — ALTO — filamento de ombro em AxeL permanece

[AxeL body F02](../../characters/orc-v1/source/rear-recovery-v2/back_l/Axe/Attack-representative-v1/layers/body/02.png) e F03 mostram filamento/gancho claro projetado para a direita da ombreira distante. Ele é visível com a arma desligada e continua no composto. O punho levantado existe; a limpeza do ombro não deve ser confundida com a validade desse reparo anatômico.

### QA-V3-04 — CRÍTICO — back_l/Unarmed perde o membro do golpe

[F02 composto](../../characters/orc-v1/source/rear-recovery-v2/back_l/Unarmed/02.png) tem o braço estendido para a esquerda. Em [F03 composto](../../characters/orc-v1/source/rear-recovery-v2/back_l/Unarmed/03.png), o membro praticamente desaparece, restando resíduos próximos ao ombro; não é uma recuperação intermediária legível. [F04](../../characters/orc-v1/source/rear-recovery-v2/back_l/Unarmed/04.png) combina braço pendente da base com fragmento saliente do golpe junto à ombreira.

Não há duplicatas RGBA exatas entre os cinco compostos atuais. Isso não resolve a inconsistência. O Lua de F03 apaga `(x,y)` e escreve `(x+5,y+1)` no mesmo destino durante a varredura: iterações seguintes apagam parte do que as anteriores acabaram de escrever. F04 adiciona pixels do impacto sobre a base sem substituir integralmente o membro anterior. A causa atual é montagem destrutiva/incompleta, não apenas a alegada herança de poses frontais.

### QA-V3-05 — ALTO — PNGs nativos de outra versão

Comparação independente entre crop `(64,64,128,128)` do composto e `nativePng` declarado. Em ataques armados, o comparador usa `body`, pois o nativo declarado é corporal. As contagens abaixo são diferenças visíveis RGBA, ignorando RGB oculto quando ambos os pixels são totalmente transparentes.

| Clipe | Quadro | Pixels divergentes |
|---|---|---:|
| front_r/Unarmed | F02 / F03 | 883 / 934 |
| front_l/Unarmed | F02 / F03 | 878 / 923 |
| back_r/Unarmed | F03 | 287 |
| back_l/Unarmed | F01 / F03 / F04 | 6377 / 5158 / 5893 |
| front_r/Defeat | F04 | 2528 |
| front_l/Defeat | F04 | 2595 |
| front_r/Walk | F08 | 4 |
| front_l/Walk | F08 | 4 |

Nos Unarmed frontais os compostos mostram o braço enxertado, enquanto os nativos mantêm a omissão anterior. Em back_r o punho restaurado de F03 só chega ao composto/mestre. Em back_l, o viewer composto e os PNGs nativos apresentam sequências diferentes.

Causa comprovada pelos scripts: criam imagens nativas em memória e salvam mestres/strip, mas não atualizam todos os `native/*.png` apontados pelos clipes. Em Defeat, o novo nativo é salvo na pasta do experimento, não no `nativePng` do manifesto. `sync_all_metadata.mjs` recalcula hashes dos arquivos encontrados e, assim, autentica duas versões diferentes sem compará-las.

### QA-V3-06 — ALTO — Defeat comprimido e mestre com pose anterior por baixo

Os cinco quadros frontais foram abertos em ambas as vistas. No composto, F04 é mais baixo e comunica maior abatimento que a pose nativa anterior; entretanto isso não basta para certificar nocaute volumétrico. O terminal ainda conserva a organização dos apoios da pose anterior e o tórax/ombreiras ficam visivelmente comprimidos.

O script não articula um novo colapso: para `y < 165`, aplica `y' = y + floor(11 * (1 - (y - 125)/40))`, equivalente aproximadamente a `0,725*y + 45,375`, mais deslocamento horizontal de 2 px. Isso comprime regionalmente a estrutura vertical, com colisões de linhas. Não é a rotação global + `vScale=0.52` proibida, mas também não prova a alegada preservação total de volume. A área opaca passa de 5033 para 4326 pixels em front_r e de 5079 para 4350 em front_l (aproximadamente 14% a menos); a redução é diagnóstico corroborando o algoritmo e a inspeção, não um portão artístico isolado.

Medição do PNG composto F04: front_r tem bbox 120×55, y=136..190; front_l tem 121×56, y=135..190. Logo a afirmação de 55 px para ambos também é inexata.

Há ainda divergência de autoria: o código chama `cel.image:drawImage(termComp, ...)` sobre o cel existente, sem limpá-lo. Pixels antigos sob áreas transparentes da nova pose sobrevivem. Leitura direta de cels RGBA comprimidos do `.aseprite`, com posições de cel e ordem de camada, confirmou:

| Direção, F04 | Mestre composto vs PNG composto | Mestre nativo vs PNG nativo |
|---|---:|---:|
| front_r | 737 pixels visíveis | 1791 pixels visíveis |
| front_l | 759 pixels visíveis | 1836 pixels visíveis |

O mestre composto mantém topo em y=125/front_r e y=124/front_l, contra 136/135 nos PNGs. Renderizar o mestre salvo não reproduz o terminal apresentado. A pose nativa entregue também continua anterior, conforme QA-V3-05.

### QA-V3-07 — ALTO — tempos do mestre divergentes do manifesto

Nos dois Unarmed frontais, cabeçalhos de frames dos mestres composto e nativo declaram `[80,110,60,90,110]` ms. Os `clip.json` e o player declaram `[80,110,50,90,120]` ms. O total é 450 ms em ambos, mas impacto e recuperação diferem. Conferir apenas duração total e hashes não detecta isso. `author_unarmed_all.lua` altera a lista; o sincronizador não a transporta para os manifests frontais.

### QA-V3-08 — ALTO — abrangência e registros de evidência incorretos

`front_l/Sword` teve PNGs F01/F03, body F01–F03 e `clip.json` alterados; os dois Walk frontais tiveram F08 e `clip.json` alterados. Mesmo assim, os três continuam `UNCHANGED_ALIAS`, `isAffected:false`, com nota de preservação byte a byte. O teste da interface deriva a expectativa desse manifesto; por isso consegue passar com informação histórica incorreta. O antes/depois obrigatório das 12 células não cobre essas três intervenções adicionais.

O handoff enumera somente 13 clipes efetivamente protegidos, chamando-os de 16 aliases integralmente preservados. Os resumos precisam separar preservação comprovada, alterações autorizadas e revisão ainda pendente.

## Testes executados e limites

1. `node --test --test-concurrency=1 test/action-contract.test.mjs test/main-orc-complete.test.mjs test/test_review_js_runtime.mjs`: **6/6 PASS**, zero falhas/skips. O arquivo `main-orc-complete.test.mjs` contém duas verificações majoritariamente sobre a biblioteca baseline e seus contratos; não garante equivalência dos novos derivados v3.
2. `test/test_rear_recovery_review.py`, executado com o Python do runtime local e `-B`: **PASS**, 28/28 células, 0 links estáticos ausentes, strips comparativos exatos segundo seu contrato. O alias `python` do PATH não era utilizável; a execução foi repetida com o interpretador existente e teve êxito.
3. `test/browser-check-rear-recovery-review.mjs`: **20/20 PASS** em Chromium real. Para respeitar arquivo único, foi executada uma cópia textual em memória: removida somente a criação do diretório de screenshots e retirados os caminhos de saída das capturas. Asserções e lógica de navegação permaneceram iguais; nenhum arquivo de teste foi editado. Velocidade 1× avançou para 7/8 em 1000 ms e 0,5× para 4/8; escala CSS 128 px, passo a quadro e hold Defeat passaram. Isso é teste funcional do player, não avaliação estética temporal.
4. `node experiments/main-orc-targeted-recovery-v3/find_bright_pixels.mjs`: **32/32 compostos com zero pixels de borda de luma arredondada ≥ 200**, exatamente conforme a definição do script. Ele examina borda externa do composto em vizinhança de oito pixels, não toda a arma separada nem toda diferença clara percebida.
5. Auditorias independentes somente leitura: snapshot/freeze, hashes de referências, crop corporal vs nativo, recomposição de camadas, duplicatas RGBA, leitura dos tempos/cels dos mestres e comparação com os PNGs. Estes checks revelaram os FAIL acima, apesar dos testes existentes com PASS.

**50/50 da suíte completa: NAO VERIFICADO nesta execução.** `factory`, `aseprite`, `action-export` e `preview-entry` criam fixtures, builds, personagens ou arquivos; a suite de contrato do manifesto também emite relatório no repositório e arquivos temporários, e `diag.test.mjs` cria uma pasta de testes. Não executei essas suites originais com efeitos de escrita diante da restrição explícita de criar apenas este relatório. Não afirmo que falharam, nem uso um log histórico como execução independente desta versão. Os 14/14 do contrato e 17/17 de diagnóstico alegados pelo DEV também não foram repetidos aqui.

## Avaliação da documentação e causa da recorrência

`RECIPES.md` mantém boas exigências de layers-off e cadeia articular, mas a implementação não as cumpre. As adições em `ARTISTIC_QUALITY_GATES.md` classificam como `[Verified Evidence]` pegada, cinemática e volume que não foram demonstrados nesta entrega. `MAIN_ORC_COMBAT_POLISH.md` e `AGENT_CONTEXT.md` repetem que todos os apontamentos foram corrigidos; os quadros contradizem essa declaração.

As causas atuais verificáveis que precisam entrar nos registros são:

- Reentrada de doadores antigos contaminados, incluindo corpo de AxeR aplicado integralmente a SwordR, sem inspeção semântica obrigatória antes da composição.
- Grip definido por tabela e carimbo de mão não orientado pela anatomia, mantendo arma independente do punho em poses-chave.
- Apagar e transladar pixels para regiões ainda percorridas no mesmo destino, destruindo o próprio reparo em UnarmedL F03; adição de fragmentos sem remoção do membro anterior em F04.
- Exportação parcial: composto, mestre, strip e PNG nativo não são publicados como uma unidade verificada. Recalcular hashes valida existência/integridade, não igualdade semântica nem sincronização.
- Pintar nova pose transparente sobre cel antigo sem limpar deixa a arte anterior no mestre; exportar um PNG separado mascara o problema.
- Reusar resumos/status antigos e testes derivados desses mesmos resumos permite falsa preservação de aliases e substitui análise visual por consistência circular de metadados.

Também há problemas nas novas regras: o exemplo `rgb(176,178,180)` tem luma aproximadamente 178, não ≥ 200; a lição 18 descreve quatro vizinhos, mas o Lua verifica oito. A lição de Defeat transforma altura/aspecto em prescrição universal (`height <= 58`, aspecto ≥ 2), em tensão com a orientação anterior de diagnósticos contextuais e prioridade do volume. Uma trajetória angular monotônica tampouco garante profundidade ou continuidade articular; os próprios frames SwordR demonstram isso.

As explicações do DEV sobre processos generativos anteriores podem ser hipóteses históricas plausíveis, mas não substituem a identificação dos erros de montagem, escolha de fonte e exportação deste passe. O relatório deve distinguir essas hipóteses das causas aqui observadas em código e arquivos.

## Disposição

**FAIL técnico do pacote; `ARTISTIC_REVISION_REQUIRED`; `PENDING_CREATOR`.** Preservação dos protegidos e funcionamento do viewer têm evidência com PASS. Não conceder PASS global com base em 0 pixels acima de um limiar ou em suites verdes da baseline/interface.

A próxima submissão precisa corrigir os defeitos críticos nos corpos/pegadas e em UnarmedL, publicar derivados e tempos consistentes a partir de mestres realmente reproduzíveis, corrigir a classificação das três células tocadas e substituir afirmações documentais definitivas por evidência da versão exata. Depois disso, exigir novo freeze e revisão visual temporal em 1× e escala de jogo, mantendo a aprovação artística exclusiva do criador e o requisito histórico de retorno ao mesmo QA Copilot quando aplicável. Este parecer não substitui esse requisito de identidade do revisor anterior.

Nenhuma arte, documento canônico, configuração, aprovação ou arquivo Unity foi alterado por este QA. Não houve geração PixelLab neste trabalho.

---

## Re-revisão

2026-10-27 — nova submissão congelada em **20:19:36.600Z**, com 2403 arquivos. Esta seção avalia a versão corrigida e preserva o parecer anterior como histórico da versão anterior.

**Veredito atual: FAIL técnico do pacote, apesar de 50/50 testes com PASS; `ARTISTIC_REVISION_REQUIRED`; `PENDING_CREATOR`.** Vários reparos foram confirmados, especialmente limpeza layers-off, encaixe de SwordR F04–F05 e sincronização dos pixels. Permanecem dano de recorte em UnarmedL F04, metadados de sockets/ângulos antigos, tempos traseiros divergentes e 14 hashes de referências desatualizados. A aprovação artística continua exclusiva do criador.

### Identificação e cobertura independente

| Artefato | SHA-256 desta re-revisão |
|---|---|
| `delivery-freeze.json` | `1eb8aa8d971d3f909c1e8fe50b5680ce3106c91adaf7dfc828b8516a2801bdc0` |
| Manifesto canônico `candidate28manifest.json` | `b2b54c9f84d4bb83785fd5991ed30cfaf3f8f7f33a85d2b472059253f36b416e` |
| `before-snapshot.json`, preservado | `d23f65894dcb3d327bb62a4a78572246be69a469585717ac25eec39c327f01b9` |

Os **605 registros modificados/novos** do freeze (421 + 184) conferem com o disco; nenhum drift foi encontrado antes ou depois da suíte completa. Dos 2223 caminhos do before-snapshot, 1802 permanecem byte-idênticos, 421 mudaram e nenhum está ausente. Os 1798 inalterados do freeze posterior pertencem ao escopo de coleta desse arquivo.

Foram reabertas as sequências reais completas de Sword/Axe traseiros em 1× e 2×, inclusive os quatro corpos layers-off; os quatro Unarmed e os dois Defeat frontais em nativo 1× e 3×, com ampliação adicional 4× de UnarmedL F03–F04 e Defeat F04. Também foram conferidos os ciclos Walk traseiros e as áreas de Sword frontal/Walk frontal anteriormente corrigidas. A inspeção usou os arquivos atuais lidos do disco, sem reutilizar imagens em cache do parecer anterior.

**Avaliação artística temporal contínua em 1×: NAO VERIFICADO.** A suíte executou o player real; este QA não assistiu a uma reprodução contínua para julgar peso, ritmo, flicker ou naturalidade. Escala estática 1× e avanço automático confirmado pelo teste não são essa observação.

### Matriz Requisito → Evidência → Resultado

| Requisito / achado anterior | Evidência da nova versão | Resultado |
|---|---|---|
| QA-V3-01: SwordR F04–F05 sem espada solta | PNGs em 1×/2× agora conectam arma à extremidade do braço. Em cada quadro, 49 dos 54 pixels opacos de `handFront` sobrepõem o corpo: 90,74%. | PASS localizado visual/raster |
| Sockets/ângulos descrevem esse mesmo reparo | `rightGrip` de SwordR F04 continua `[180,94]`, embora o overlay corrigido esteja em torno de `[181,118]`; outros 23 quadros visíveis também conservam grip e/ou ângulo antigo. RR-03. | FAIL |
| QA-V3-02: corpo desarmado de SwordL | F00–F07 layers-off vistos em 1×/2×: lâmina do quadril F01–F07 e faixa clara de F05 apontadas anteriormente não reaparecem. | PASS para os defeitos identificados |
| QA-V3-02: corpo de AxeR/SwordR | Cabeça secundária de F01 e haste F02–F03 removidas; F04–F05 agora mostram braço contínuo até a mão. Os oito corpos destas duas categorias continuam iguais, o que não certifica coreografia distinta. | PASS localizado; coreografia temporal NAO VERIFICADO |
| QA-V3-03: filamento de AxeL F02–F03 | Corpos atuais em 1×/2× sem o gancho claro projetado da ombreira distante. | PASS localizado |
| QA-V3-04: UnarmedL F03–F04 | F03 conserva o membro e elimina o desaparecimento anterior. F04 apresenta grande corte retangular na lateral esquerda e fragmento de mão junto ao quadril. RR-01. | FAIL |
| Unarmed frontal e back_r: membros presentes | Braço oposto presente em F02–F03 frontais; punho presente em F03 traseiro direito. Nativos e compostos agora mostram os mesmos reparos. | PASS estático; temporal NAO VERIFICADO |
| QA-V3-05: equivalência dos pixels publicados | 210 compostos conferem com seus mestres; 144 PNGs nativos explicitamente referenciados conferem com o crop; 160 quadros de mestres nativos conferem com o crop, inclusive Walk traseiro sem `nativePng` explícito. Body masters e strips também conferem em pixels visíveis. | PASS de equivalência de pixels |
| QA-V3-06: Defeat sem silhueta antiga no mestre | Mestre e PNG F04 agora coincidem nas duas vistas; não há o resíduo superior anterior. Algoritmo atual usa translação rígida, não a compressão regional anterior. | PASS técnico localizado |
| Defeat F04 comunica nocaute inequívoco | Mais baixo e volumoso, mas a cabeça continua elevada entre braços apoiados e joelhos recolhidos sob o corpo; a leitura de apoio/quatro apoios ainda é possível. RR-05. | FAIL de clareza artística neste parecer; temporal NAO VERIFICADO |
| QA-V3-07: tempos frontais | Mestres e manifests frontais agora usam `[80,110,50,90,120]` ms. | PASS |
| Tempos dos dois Unarmed traseiros | Mestres usam `[80,110,50,90,120]`, mas os dois manifests/players declaram `[80,110,60,90,110]`. RR-02. | FAIL |
| Hashes de todos os derivados declarados | Quatro `bodyMasterSha256` e dez `stripSha256` divergem dos arquivos atuais. RR-04. | FAIL |
| QA-V3-08: classificação das células | 15 `ACTIVE_CANDIDATE`/afetadas e 13 `UNCHANGED_ALIAS`; as três antigas falsas aliases foram reclassificadas. Antes/depois contém 15 seções. | PASS para classificação artística |
| Preservação da arte protegida | 248 referências artísticas diretamente no snapshot permanecem iguais; 79 referências adicionais correspondem aos hashes originais dos manifests, recuperáveis conforme explicado abaixo. Nenhum pixel/mestre protegido alterado foi identificado. | PASS, com cobertura histórica explicitada |
| Preservação byte a byte dos clipes protegidos como pacote | Os 13 `clip.json` protegidos ganharam `nativeStripSha256` e mudaram de hash. RR-06. | FAIL estrito de metadados; arte preservada |
| Camadas e alpha-over | Ordem real dos mestres traseiros e recomposição dos PNGs armados conferem: `weaponBack → body → weaponFront → handFront`. | PASS estrutural |
| Bordas de luma ≥ 200 | Auditoria independente dos 32 compostos: zero pixels externos com luma arredondada ≥ 200. O script diagnóstico foi alterado e agora também lista bordas abaixo desse limiar. | PASS para o limiar 200; sem equivalência automática a ausência de qualquer halo |
| Regressões locais frontais | Sword frontal esquerdo sem o resíduo pontual anterior na área examinada; Walk frontal F08 agora sincronizado com o nativo. | PASS localizado |
| Back Walk sem flicker | Membros presentes nas poses vistas; reprodução artística contínua não assistida. | PASS estático; flicker temporal NAO VERIFICADO |
| Suites completas | `node --test --test-concurrency=1`: 50/50, zero falhas/skips; Chromium 20/20 incluído; Python 28/28 com PASS. | PASS de testes executados |
| QA-V3-08: documentação corresponde à entrega | Causas foram melhor descritas, mas seguem declarações de resolução total, números de cobertura errados e narrativa anterior de Defeat. RR-07. | FAIL de precisão; melhora parcial confirmada |
| Sem aprovação do criador, Unity ou PixelLab pelo QA | Nenhuma geração, integração, edição artística ou edição de docs canônicos executada nesta re-revisão. Testes agora autorizados emitiram suas fixtures/relatórios/capturas usuais. | PASS do escopo deste QA |

### Achados atuais por gravidade

#### RR-01 — CRÍTICO — UnarmedL F04 ainda tem recorte destrutivo e resíduo de membro

O desaparecimento em [F03](../../characters/orc-v1/source/rear-recovery-v2/back_l/Unarmed/03.png) foi corrigido: há braço e punho. Porém [F04 composto](../../characters/orc-v1/source/rear-recovery-v2/back_l/Unarmed/04.png) e [F04 nativo](../../characters/orc-v1/source/rear-recovery-v2/back_l/Unarmed/native/04.png) exibem uma borda vertical/horizontal retangular removendo a lateral do tronco, armadura e parte da silhueta abaixo do braço. Um fragmento marrom de mão/manopla sobra junto ao quadril, aproximadamente em torno de `(30,83)` no nativo, sem antebraço que o sustente.

Isso é visível em 1× e inequívoco em 3×/4×. A causa está em `repair_back_l_unarmed.lua`: F04 apaga integralmente a caixa nativa `x=15..45, y=20..80`, abrangendo mais que o membro, mas deixa resíduos antigos abaixo de y=80. O novo enxerto é recortado para outra caixa e não recompõe o contorno do corpo que foi retirado. Buffers separados corrigiram o bug de F03, mas a máscara de F04 continua inadequada. A falha agora está igualmente presente no mestre, composto e nativo: igualdade técnica de pixels não sana a anatomia.

#### RR-02 — ALTO — regressão de tempos nos Unarmed traseiros

Leitura independente dos cabeçalhos de frames dos quatro arquivos mestre pertinentes:

| Clipe | Mestre composto e mestre nativo | `durationsMs` e frames no `clip.json` |
|---|---|---|
| `back_r/Unarmed` | 80, 110, **50**, 90, **120** | 80, 110, **60**, 90, **110** |
| `back_l/Unarmed` | 80, 110, **50**, 90, **120** | 80, 110, **60**, 90, **110** |

O problema frontal do QA-V3-07 foi corrigido, mas a divergência reaparece nas duas vistas traseiras. O total 450 ms é igual e mascara a diferença. `sync_all_metadata_v4.mjs` sincroniza explicitamente as durações apenas dos Unarmed frontais. O player da página e o Aseprite continuam reproduzindo o impacto e a recuperação traseiros com tempos diferentes.

#### RR-03 — ALTO — sockets e ângulos antigos em todas as armas traseiras

O reparo raster da mão de SwordR F04–F05 tem evidência positiva. O contrato dos clipes não foi atualizado junto com ele. Nos quatro ataques traseiros, **F01–F06 de cada clipe** têm `rightGrip` e/ou `rotationDeg` diferentes das configurações do novo `author_all_rear_weapons_clean.lua`, corroboradas pela posição/direção visível dos overlays atuais: 24 registros com divergência.

Exemplos suficientes para reprodução:

| Clipe / quadro | Grip declarado no clip | Grip no novo autor / overlay | Ângulo declarado → novo autor |
|---|---|---|---|
| SwordR F04 | `[180,94]` | `[181,118]` | 60° → 65° |
| SwordR F05 | `[180,120]` | `[181,122]` | 100° → 105° |
| SwordR F06 | `[168,126]` | `[156,139]` | 135° → 135° |
| SwordL F04 | `[88,88]` | `[93,71]` | 60° → 240° |
| AxeR F05 | `[162,120]` | `[181,122]` | 110° → 105° |
| AxeL F05 | `[92,130]` | `[96,141]` | 110° → 270° |

Em SwordL F04, por exemplo, o PNG aponta a lâmina para baixo/esquerda, coerente com o novo autor, enquanto o manifesto conserva o ângulo oposto. Um consumidor de sockets/ângulos recebe a versão anterior, mesmo com a arte corrigida. O sincronizador atual recalcula digests, mas não transporta as tabelas novas. Não confundir o PASS da pegada desenhada com PASS do contrato de ligação.

#### RR-04 — ALTO — 14 digests declarados não correspondem aos arquivos

Os arquivos físicos atuais são visualmente consistentes com os quadros, mas seus manifests conservam hashes antigos nestes campos:

| Campo incorreto | Células afetadas |
|---|---|
| `bodyMasterSha256` — 4 casos | `back_r/Sword`, `back_l/Sword`, `back_r/Axe`, `back_l/Axe` |
| `stripSha256` — 10 casos | `front_r/Walk`, `front_l/Walk`, `front_r/Defeat`, `front_l/Defeat`, `front_l/Sword`, `back_r/Sword`, `back_l/Sword`, `back_r/Axe`, `back_l/Axe`, `back_l/Unarmed` |

Exemplo exato, `back_r/Sword`:

- `bodyMasterSha256` declarado: `53a804bde6f19696e95afe8ea20ba648e98413844bf7baff6d9bc75632c7b535`.
- SHA-256 real do `sword-body-representative-v2.aseprite`: `943b45065ff179550b7f6c33302a375250e0e472f9d62b57a4d54f6848463c6d`.

O script v4 atualiza `masterSha256`, `nativeMasterSha256` e adiciona `nativeStripSha256`, mas deixa `bodyMasterSha256` e o já existente `stripSha256` desatualizados. Adicionar um segundo campo correto não torna verdadeiro o primeiro campo incorreto. O freeze autentica os bytes desses manifests inconsistentes; não valida suas referências internas. A suíte com 50/50 PASS não cobre integralmente esses campos.

#### RR-05 — MÉDIO, ARTÍSTICO — leitura de Defeat F04 ainda ambígua

[Front_r F04](../../characters/orc-v1/source/rear-recovery-v2/front_r/Defeat/native/04.png) e [front_l F04](../../characters/orc-v1/source/rear-recovery-v2/front_l/Defeat/native/04.png) foram examinados em 1×, 3× e 4×. A massa de armadura/crânio agora não apresenta o achatamento regional anterior, e não resta a silhueta antiga sobreposta no mestre. Estes reparos técnicos têm PASS.

A posição final conserva joelhos recolhidos sob o corpo e os dois braços apoiados à frente, com a cabeça elevada entre eles. O tórax mais baixo transmite abatimento, mas a leitura de personagem ainda sustentado nos apoios permanece possível; não considero demonstrado o pedido de nocaute inequívoco. É uma avaliação visual estática, não alegação de ter assistido ao colapso temporal. O criador deve julgar esta ambiguidade; os valores de bbox não a resolvem.

Ambos os terminais medem 120×57 px no nativo, bbox `(4,70)..(123,126)`, 4215 pixels opacos. A translação rígida atual evita a fórmula de compressão anterior, mas não constitui por si só aprovação da pose.

#### RR-06 — MÉDIO — os 13 manifests protegidos deixaram de ser byte-idênticos

Todos os 13 `clip.json` protegidos no conjunto Idle/Hit/SwordR/Axe frontal/Defeat traseiro foram regravados para acrescentar `nativeStripSha256`. Isto foi verificado contra o before-snapshot, não deduzido apenas do nome do script.

Para isolar a mudança sem escrever arquivos, removi o campo novo **somente de cópias em memória**, serializei em dois espaços com newline final e recalculei SHA-256: **13/13 recuperam exatamente o hash anterior do snapshot**. Assim foi possível confirmar que os demais campos, incluindo hashes de arte e tempos protegidos, continuam sendo os originais. As 248 referências artísticas diretas restantes conferem; as 79 referências a mestres/nativos fora da coleta direta correspondem aos hashes originais recuperados dessa forma.

Não há evidência de mutação da arte protegida. Há, porém, violação literal da alegação de que o pacote inteiro dos 13 aliases permaneceu byte-idêntico. A remediação pode ser preservar os manifests protegidos originais ou documentar uma exceção de metadados autorizada; este QA não efetuou nenhuma delas.

#### RR-07 — MÉDIO — documentação melhorou as causas, mas ainda não descreve o resultado exato

Melhoras confirmadas em `RECIPES.md` e `ARTISTIC_QUALITY_GATES.md`: agora registram as seis causas operacionais do parecer anterior; buffers separados, limpeza de cel, igualdade de pixels, luma de aproximadamente 178 e oito vizinhos estão explicitados. A regra de Defeat foi contextualizada. São correções úteis de conhecimento.

Persistem problemas verificáveis:

- `AGENT_CONTEXT.md` e a abertura de `MAIN_ORC_COMBAT_POLISH.md` afirmam que todos QA-V3-01..08 foram corrigidos, antes de este parecer confirmar isso. UnarmedL F04, tempos e contratos de referência contradizem a declaração.
- O handoff informa **98 quadros nas 15 células afetadas / 112 nos 13 aliases**. Contagem direta dos arrays de frames: **123 afetados / 87 protegidos**, total 210.
- `MAIN_ORC_COMBAT_POLISH.md` ainda descreve a versão anterior de Defeat como 66→55 px e proporção 2,18, enquanto a entrega atual mede 57 px e aproximadamente 2,105. Também conserva a explicação antiga de UnarmedL centrada na origem frontal, embora o novo registro de causas já reconheça os erros locais de montagem.
- A lição 21 declara F04 de UnarmedL sem membro fantasma, mas o fragmento residual e a caixa recortada continuam visíveis. As lições de igualdade precisam incluir os tempos e todos os digests/socket fields, além dos pixels.
- O relatório de entrega do DEV `targeted-recovery-v3-report.md` continua apresentando 2400 arquivos e 12/16 como resultado atual, sem enquadrá-los como a versão anterior.

A documentação já explica melhor por que a falha ocorreu. Ainda precisa separar técnica implementada, resultado efetivamente observado e afirmação pendente de validação.

### Testes e auditorias desta re-revisão

`node --test --test-concurrency=1` foi executado integralmente, agora com autorização explícita: **50 testes, 50 PASS, 0 falhas, 0 skips**, duração reportada de aproximadamente **57,15 s**. Inclui a suíte de diagnóstico, contrato do manifesto, bridge Aseprite, validações da fábrica, previews e teste do player.

O Chromium incluído reportou **20/20 checks**, 28/28 células selecionáveis, 42/42 imagens decodificadas, 15/15 seções antes/depois, nenhum request falho, velocidade 1× e 0,5×, escala CSS 128 px e hold terminal. O teste Python foi reexecutado separadamente com `-B`: **28/28 células e zero links estáticos ausentes**, com PASS.

A auditoria independente leu os cels reais dos mestres Aseprite (RGBA comprimido, posições e ordem de camadas), os cabeçalhos de duração e os PNGs, sem executar autoria ou salvar exportações. Resultado de pixels visíveis: zero divergências nas comparações dos compostos com mestres, dos 144 PNGs nativos declarados, dos 160 quadros de mestres nativos com seus crops, dos body masters e das strips pertinentes. Transparência de ambos os lados não foi tratada como diferença visual por causa de RGB oculto. Esta auditoria também encontrou as divergências de tempos, sockets e hashes que os testes verdes não detectaram.

O script `find_bright_pixels.mjs` **mudou de predicado**: atualmente lista bordas com luma ≥ 150 ou cores claras correlatas. Sua execução listou sete ocorrências, todas atribuídas ao `body`: SwordR/AxeR F00 duas cada; SwordL/AxeL F00 uma cada; AxeL F06 uma. Isso não contradiz o zero independente no limiar 200, nem torna todo realce metálico um halo defeituoso. Os antigos ganchos/lâminas foram julgados pela imagem, separadamente desses limiares.

Os testes emitiram seus artefatos usuais fora da arte/docs canônicos, conforme autorização atual. A conferência posterior manteve o mesmo SHA-256 do freeze e zero drift nos seus 605 registros modificados/novos. Este QA não executou PixelLab, não editou arte, não editou docs canônicos nem integrou Unity; a saída editorial desta revisão é esta seção no mesmo relatório.

### Disposição atual

**Não conceder PASS técnico global ainda.** A equivalência de pixels e diversos reparos visuais passaram, mas os tempos traseiros, digests e sockets/ângulos precisam representar a versão que realmente foi desenhada. A preservação da arte protegida tem evidência positiva; a exceção de escrita dos 13 manifests deve ser corrigida ou explicitamente tratada.

**Manter `ARTISTIC_REVISION_REQUIRED` e `PENDING_CREATOR`.** UnarmedL F04 requer novo reparo localizado; a leitura de nocaute de Defeat continua merecendo revisão do criador. A naturalidade temporal dos quatro ataques traseiros e ausência de flicker em Walk ficam **NAO VERIFICADO** neste parecer. Novo freeze e reinspeção dos arquivos efetivamente alterados são necessários após os ajustes; nenhum PASS da suíte ou desta revisão localizada concede aprovação artística do criador.

---

## 2ª Re-revisão

2026-10-27 — versão exata do `delivery-freeze.json` emitido em **21:43:22.059Z**.

**Veredito: PASS técnico dos assets e contratos examinados (`TECHNICALLY_COMPLETE`), com ressalva documental baixa. Recomendo `VISUAL_REVIEW_REQUIRED` e `PENDING_CREATOR`.** Os bloqueios técnicos e defeitos estáticos RR-01..RR-06 foram sanados nas áreas reinspecionadas. Não encontrei nesses reparos um defeito estático remanescente que sustente `ARTISTIC_REVISION_REQUIRED` para este freeze. Isso não concede aprovação artística nem certifica naturalidade temporal.

**Reprodução artística contínua em 1× não foi assistida: NAO VERIFICADO.** O teste Chromium confirmou funcionamento temporal do player, mas não substitui assistir ao movimento. Peso dos ataques, ritmo de retorno e flicker continuam pendentes dessa avaliação e da decisão do criador.

### Identidade da versão

| Artefato | SHA-256 |
|---|---|
| `delivery-freeze.json` | `dc64bd8b62bbe02ea885720b24f74fc8c9ad396f1cfe2263c3e37b7db380bacd` |
| `candidate28manifest.json` canônico | `51f18754dbb588d9c2c5571b03ca92d5dac8236432137cf14dd5a0976df30e18` |
| `before-snapshot.json`, preservado | `d23f65894dcb3d327bb62a4a78572246be69a469585717ac25eec39c327f01b9` |

Freeze: **2403 arquivos**, 408 modificados, 184 novos e 1811 inalterados no seu escopo. Os **592 registros modificados/novos** conferiram com o disco antes e depois dos testes, sem drift. No escopo anterior de 2223 caminhos, 1815 permanecem iguais ao before-snapshot e 408 diferem; os escopos de coleta não são idênticos.

### Matriz Requisito → Evidência → Resultado

| Requisito | Evidência independente desta versão | Resultado |
|---|---|---|
| RR-01: UnarmedL F04 sem recorte ou fragmento | PNG nativo aberto em 1×, 3× e 4×; composto e cel real do mestre examinados. Lateral do tronco/armadura e cadeia ombro–punho contínuas; resíduo em torno de `(30,83)` removido. | PASS localizado |
| UnarmedL F03–F04 e pose de fechamento | F03 mantém braço/punho; F04 retorna à base íntegra. F04 e F00 têm zero diferenças visíveis: fechamento deliberado, não repetição acidental de quadros intermediários. | PASS estático; fluidez temporal NAO VERIFICADO |
| RR-02: tempos Unarmed traseiros | Mestres composto/nativo, `durationsMs` e tempos por frame dos dois clipes conferem: `[80,110,50,90,120]` ms, 450 ms. Frontais também conferem. | PASS |
| RR-03: sockets/ângulos contra imagem real | 32 registros conferem com autoria; validação independente das transformações reproduziu exatamente `weaponBack`/`weaponFront` das 24 poses visíveis, usando os PNGs reais das armas e os parâmetros declarados. Poses ocultas têm camadas vazias. | PASS |
| RR-04: todos os digests dos clipes canônicos | Varredura recursiva verificou **825 campos SHA-256**, incluindo hashes aninhados de armas, suplementos, entrada de procedência e nove GIFs referenciados: zero divergências ou campos sem mapeamento. | PASS de integridade |
| Digests nas células do manifesto | **116 campos** declarados conferidos contra os arquivos correspondentes: zero divergências. | PASS |
| Digests do pacote de revisão | **775 hashes** das cópias conferem; também conferem as 732 fontes diretamente copiadas. As outras entradas são layouts gerados de frames, conferidos como arquivos de saída e pelos checks de strips. | PASS |
| Equivalência mestre/composto/nativo/strip | Zero diferenças visíveis nos 210 compostos versus mestres, 144 PNGs nativos explicitamente referenciados, 160 quadros de mestres nativos versus crops, body masters e strips. Tempos de todos os mestres declarados também conferem. | PASS |
| RR-05: Defeat frontal F04 lê como nocaute | Duas vistas abertas em 1× e 4×: cabeça agora rente ao chão, peito assentado e braços baixos; leitura estática de corpo abatido mais clara que na versão de quatro apoios. | PASS visual localizado, sujeito ao criador |
| Defeat mantém volume sem achatamento proibido | Crânio, ombreiras e tórax continuam volumosos na imagem ampliada. Autor atual separa/translada massas, sem compressão regional nem rotação global + vScale 0.52; mestres reproduzem os PNGs. | PASS qualitativo/contextual |
| Defeat F00–F03 intactos | Os 16 PNGs anteriores ao terminal (8 compostos + 8 nativos nas duas vistas) mantêm SHA-256 do snapshot. Cels atuais reproduzem esses mesmos frames. | PASS |
| RR-06: 13 `clip.json` protegidos restaurados | **13/13** voltaram diretamente ao SHA-256 do snapshot, sem normalização ou exclusão de campos durante a comparação. | PASS byte a byte |
| Arte protegida | 261 referências diretas ao snapshot e 79 ligadas pelos hashes dos manifests protegidos conferem; nenhum protegido divergente. | PASS, com limite histórico de coleta já descrito |
| Regressão layers-off Sword/Axe traseiros | F00–F07 dos quatro corpos reabertos; lâmina de quadril/faixa de SwordL, cabeça/haste de AxeR/SwordR e gancho de AxeL não reaparecem nas áreas apontadas. | PASS estático localizado |
| Regressão grip SwordR F04–F05 | Compostos reais em 1× e 2× mantêm cabo/manopla unidos à extremidade do braço; parâmetros agora descrevem a mesma posição. | PASS localizado |
| Regressão Unarmed frontais e back_r | F02–F03 frontais ampliados e F03 traseiro direito mantêm os membros/punho reparados; publicação nativa e composta consistente. | PASS estático localizado |
| Regressão Walk e axila Sword frontal | Ciclos Walk traseiros reabertos, braços presentes nas poses; tecido frontal F08 e axila SwordL F01–F03 reinspecionados, sem retorno dos resíduos pontuais. | PASS estático; flicker temporal NAO VERIFICADO |
| Política de equipamento e ordem das camadas | Camadas independentes e recomposição conferem. Armas separadas visíveis somente no intervalo declarado do ataque; corpos layers-off examinados separadamente. | PASS no escopo inspecionado |
| RR-07: contagens e documentação | Manifesto/página/handoff com 15/13 células e **123/87** frames; causas locais, tempos, hashes e novo terminal documentados. Lista individual de frames no relatório DEV ainda tem erros. | PASS do resumo e das causas; FAIL documental baixo, C2R-01 |
| Suíte completa | `node --test --test-concurrency=1`: **55/55 PASS**, zero falhas/skips; Chromium **20/20** incluído. Python: 28/28 células, zero links estáticos ausentes. | PASS |
| Naturalidade dos ataques, transições e ausência de flicker em velocidade real | Não assisti reprodução artística contínua em 1× nesta revisão. | NAO VERIFICADO |
| Aprovação do criador / integração | Nenhuma aprovação do criador concedida; nenhum trabalho de integração autorizado/executado por este QA. | `PENDING_CREATOR` |

### Evidência visual e encerramento dos achados anteriores

**RR-01:** [UnarmedL F04 nativo](../../characters/orc-v1/source/rear-recovery-v2/back_l/Unarmed/native/04.png) e [composto](../../characters/orc-v1/source/rear-recovery-v2/back_l/Unarmed/04.png) agora apresentam a armadura lateral inteira e a mão pendente ligada ao antebraço. O reparo substitui a máscara retangular destrutiva pela base da mesma vista, deslocada em 1 px para ancoragem. A comparação dos pixels confirma igualdade com F00. Essa igualdade de fechamento é intencional; a avaliação do salto temporal F03→F04 fica NAO VERIFICADO, pois não foi assistida.

**RR-03:** a checagem não se limitou ao teste que compara dois conjuntos de constantes. Recalculei em memória, a partir dos PNGs reais dos itens, as transformações nearest-neighbor com `rightGrip`, `rotationDeg`, grip do item, flip aplicável, separação de profundidade e contorno perimetral documentados. Resultado: **zero diferenças visíveis em todas as camadas de arma das 24 poses visíveis**. Isto demonstra correspondência entre metadados e imagem, sem alegar naturalidade biomecânica.

**RR-04:** a auditoria dos 825 campos foi mais abrangente que os 789 campos principais cobertos pelo novo teste. Incluiu `supplementSha256`, hashes aninhados de arma, `inputSha256` e `reviewEvidence.gifExports.*.sha256`. Os nove GIFs têm os bytes declarados; não os tratei como prova de que representam ou demonstram a coreografia temporal do freeze atual. O resultado de integridade é separado da avaliação artística.

**RR-05:** [front_r F04](../../characters/orc-v1/source/rear-recovery-v2/front_r/Defeat/native/04.png) e [front_l F04](../../characters/orc-v1/source/rear-recovery-v2/front_l/Defeat/native/04.png) mostram a cabeça baixa ocupando o vazio que antes permanecia sob o rosto, com o corpo de bruços e membros assentados. A massa de ombreiras/tórax permanece legível em ampliação; não identifiquei o achatamento das versões anteriores. O mestre e os PNGs têm a mesma pose.

Medições independentes do terminal: front_r bbox `(4,75)..(125,126)`; front_l `(2,75)..(123,126)`. Ambos têm **122×52 px**, aspecto aproximadamente **2,346**, 4011 pixels opacos e chão em y=126 nativo. Estes números apenas descrevem a imagem inspecionada: não provam nocaute, não medem volume físico 3D e não concedem aprovação artística. A leitura estática favorável decorre da posição da cabeça, repouso do corpo e conservação visual das massas.

**RR-06:** os 13 manifests protegidos agora conferem diretamente com o snapshot. As 261 referências diretas incluem esses 13 arquivos restaurados. As 79 referências adicionais a mestres/nativos não tinham hash físico direto na coleta anterior, mas seus digests estão nos manifests novamente byte-idênticos e correspondem aos arquivos atuais. Esta distinção de cobertura permanece; não foi inventado um snapshot anterior mais amplo.

**RR-07:** os documentos atuais passaram a reconhecer a nova submissão como sujeita a re-QA e à avaliação do criador. A lição 21 explica a máscara que destruía o torso e a correção por retorno à base íntegra; o novo terminal de Defeat substitui os valores intermediários no contexto correto. Os resumos 123/87 e 15/13 conferem com a contagem independente dos arrays de frames.

### Achados remanescentes por gravidade

**Críticos/altos nas áreas reinspecionadas:** nenhum identificado nesta versão. RR-01, RR-02, RR-03, RR-04 e RR-06 têm correção confirmada; RR-05 tem parecer estático favorável, condicionado à avaliação do criador e sem certificação temporal.

**C2R-01 — BAIXO, documental, não bloqueia o PASS técnico dos assets:** a seção “Contabilidade Exata de Quadros e Preservação” de `targeted-recovery-v3-report.md` ainda informa `front_r/Walk` e `front_l/Walk` com **8** frames e cada Hit com **4**. Os manifests e arquivos têm **16** frames por Walk frontal e **5** por Hit. Os totais corretos são 123 afetados + 87 protegidos = 210; a lista individual do texto deve acompanhar esses totais. Nenhum arquivo canônico foi corrigido por este QA.

Os novos testes geométricos de Unarmed/Defeat são úteis como regressão localizada, mas nomes como “genuine knockout” não convertem bbox ou contagem de pixels em prova artística. Este parecer favorável ao terminal inclui inspeção real das imagens e continua distinto da aprovação do criador.

### Execução e limites finais

Suíte completa: **55 testes, 55 PASS, 0 falhas, 0 skips**, duração desta execução de aproximadamente **57,76 s**. O Chromium incluído confirmou 28 células selecionáveis, 42 imagens decodificadas, 15 seções antes/depois, controles de velocidade/passo e hold terminal. A validação Python foi repetida com o interpretador local e `-B`, com PASS em 28/28 células e zero links estáticos ausentes.

Também foram lidos diretamente os cels RGBA, posições e tempos dos mestres Aseprite. Comparações de pixels ignoraram RGB oculto somente quando ambos os lados eram totalmente transparentes. Não executei scripts de autoria nem exportei nova arte. Montagens e reconstruções de validação permaneceram em memória. Os testes produziram suas fixtures/capturas/relatórios autorizados; os 592 registros do freeze permaneceram sem drift após a execução.

**Disposição desta versão: PASS técnico / `TECHNICALLY_COMPLETE`; `VISUAL_REVIEW_REQUIRED`; `PENDING_CREATOR`.** Não mantenho uma exigência de revisão artística pelos defeitos estáticos RR-01..RR-06 agora sanados. Isso não é `CREATOR_APPROVED`: o criador decide a aceitação artística, e a reprodução temporal contínua em 1× permanece **NAO VERIFICADO**. Não há promoção, edição de arte/docs canônicos, integração Unity ou geração PixelLab por este QA. A ressalva C2R-01 fica registrada para ajuste documental.
