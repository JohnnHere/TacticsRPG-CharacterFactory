# QA independente — main-orc-rear-reconstruction-v4

**Veredito: `ARTISTIC_REVISION_REQUIRED`. Pedido artístico amplo: FAIL. Pacote diagnóstico: integridade PASS, sem elegibilidade. `PENDING_CREATOR`. `eligibleForIntegration=false`. Movimento contínuo em 1×: `NOT_VERIFIED`.**

Revisor: fallback obrigatório Grok 4.7 / GitHub Copilot. A primeira escolha GLM 5.3 (`52f87102-89d7-44f5-a4dd-f445d3e163b1`) não produziu parecer. Não reli o especialista isolado; ele não está na matriz.

Freeze conferido: `experiments/main-orc-rear-reconstruction-v4/dev/version-freeze.json` SHA-256 `8f3c0be13e2b6e7d7f3ff4a33807cc1a4cb5519602d1f589d24194808ad49c44`. Manifesto `characters/orc-v1/source/rear-reconstruction-v4/candidate28manifest.json`, hash igual ao registro do freeze. A honestidade do handoff do DEV não foi tratada como aprovação da tarefa.

## Matriz

| Requisito | Evidência inspecionada | Veredito |
|---|---|---|
| 4. Espada traseira coerente, mesma técnica nas duas vistas | Corpos `back_r` Sword/Axe idênticos nos 8 quadros. `back_l/Sword` nativo F01 e F07 ainda têm lâmina no corpo desarmado. Nenhuma chave nova entrou na matriz. | FAIL |
| 5. Machado traseiro distinto, arco de corte, não braço rígido | O corpo de `back_r/Axe` é o mesmo ciclo da espada; a diferença visível é o overlay. Torso quase estático. Estudo F04 rejeitado e excluído. | FAIL |
| 6. Mão fecha o cabo | `handFront` igual ao pai nos 82 quadros. Zooms mostram cabo ao lado ou por cima da luva, sem dedos envolvendo o cabo. | FAIL |
| 7. Acabamento das armas, sem crescer, independentes | Machado 346 RGBA, madeira/ferro mais legíveis, alfa/96×96/grip `[36,55]` iguais. Espada 100 RGBA, retoque leve. Mestres reexportados no Aseprite batem com os PNGs. | PASS parcial só de material |
| 7. Independência e ataque-only | Definições próprias; camadas de arma vazias fora de `weaponVisible`. | PASS |
| 8. Unarmed contínuo | Quatro vistas são aliases, sem edição. Soco traseiro estático é rígido. Mão frontal sumindo não aparece nos quadros nativos. | FAIL traseiro; desaparecimento frontal `NOT_VERIFIED` |
| 9. Defeat frontal deitado; traseiro preservado | Terminais frontais F04 leem como corpo no chão, não ajoelhado. São aliases. Traseiros inalterados por hash. | PASS estático do terminal; queda em 1× `NOT_VERIFIED` |
| 9. Mão borrada no Defeat | 0 alfa parcial nos nativos; borrão não visto em quadro parado. | `NOT_VERIFIED` |
| 10. Flicker de Walk corrigido, locomoção intacta | Walk é alias. Folha estática não localiza flicker. Tempos do pai preservados. | Correção FAIL; flicker `NOT_VERIFIED`; locomoção preservada PASS |
| 11. Idle/Hit e coreografia frontal protegidos | Idle/Hit/Defeat traseiro: 10 aliases, hash do `clip.json` = pai, fora de `rear-reconstruction-v4`. Corpo não-`back_r` sem delta. | PASS |
| 12. Halo: causa e correção da fonte | Delta corporal de `back_r` = só os pontos de `scalp-outline-points.json`. F05 de `back_l/Sword` ainda tem faixa clara no pescoço. | PASS parcial, só coroa `back_r` |
| 13. Reconstruir chaves antes de propagar | Classificação existe; F04 foi tentado e rejeitado. Não há ciclo válido propagado. | FAIL da reconstrução; exclusão do estudo PASS |
| 15–16. Docs, preservação, sem Unity | Avisos em ROADMAP L3–L12, COMBAT_POLISH L1, RECIPES L29 e regras 7–8, ASEPRITE L77–L93. Preservação 2939/2939. Esta QA não escreveu Unity. | PASS com ressalva de superfície |
| 17. Aceite artístico amplo | Coreografia, pegada, Unarmed traseiro e Walk continuam sem correção demonstrada. | FAIL |
| 18. Página revisável | Chromium 20/20 na página real; 8 antes/depois; sem olho em 1×. | PASS funcional; percepção `NOT_VERIFIED` |
| 19. Relato sem autoaprovação | Handoff e manifesto de pacote dizem diagnóstico e `NOT_VERIFIED`. | PASS de honestidade; não cumpre a tarefa |

## Achados

1. **Técnicas traseiras não foram reconstruídas.** `back_r/Sword/layers/body/00.png`–`07.png` são pixel-idênticos a `back_r/Axe`. Os compostos só trocam o ângulo da arma sobre o mesmo braço. O torso não conduz o golpe. Isso falha as seções 4 e 5.

2. **QA-01 permanece no corpo desarmado.** `back_l/Sword/native/01.png` tem lâmina/disco à esquerda do quadril com armas desligadas. `native/07.png` ainda tem disco à direita; não volta a desarmado. `native/05.png` mantém faixa clara no pescoço/ombro. O composto soma outra espada a esse resíduo.

3. **QA-04 ainda é visível.** `back_l/Axe/native/02.png` tem filamento claro acima da espádua direita. Não reconfirmei, neste zoom, uma segunda cabeça de machado em `back_r/Axe/native/01.png` nem antebraço literalmente duplicado em F05. A quebra que vejo é outra: F04 horizontal e F05 mais baixo, sem arco contínuo, no mesmo corpo da espada.

4. **Pegada não melhorou.** Prova de pixels: `handFront` inalterado. Em `qa/sheets/grip-neighborhoods.png`, o cabo não fica fechado pela mão nas vistas traseiras. Equivalência de máscara não é contato. A regra 8 de `docs/RECIPES.md` (L65–L66) está correta e esta entrega não a satisfaz.

5. **Materiais são reais e limitados.** Machado: 346 RGBA, alfa igual, grip `[36,55]`, 96×96. A madeira quente e o ferro separam melhor que `assets/weapons/militia-axe`. Espada: 100 RGBA, diferença sutil, grip `[48,66]`. Reexportação oculta Aseprite 1.3 dos dois mestres, em `qa/aseprite-proof/`, RGBA igual aos PNGs. Não há arma nova nem aumento de tamanho.

6. **Coroa `back_r` é correção local, não fim do halo.** Os deltas corporais F01–F07 coincidem com as coordenadas declaradas; F00 e o restante do corpo não mudam. A comparação `dev/scalp-outlines-before-after.png` mostra o rebordo cinza escurecido para `INK`. Highlights de metal permanecem. Não afirmar ausência de halo nas outras vistas.

7. **Estudo F04 deve continuar fora.** `keypose-axeR/rejection.json` não é citado pelas 28 células. Na prancha `dev/keypose-neighbors-equipped.png`, o F04 de estudo desce e o F05 vizinho volta a subir; o antebraço fica mais fino. Excluí-lo foi correto. Isso não prova que não exista solução.

8. **Defeat frontal, no quadro terminal, já lê como caído.** `front_r`/`front_l` Defeat F04, aliases do pai, mostram cabeça e tronco no chão, volume preservado, não um ajoelhar em pé. F02–F03 são etapas de queda. Não houve autoria nova. Não vi borrão de mão em quadro parado; alfa é binário. A queda contínua não foi assistida em 1×.

9. **Unarmed e Walk não foram corrigidos.** São aliases. O soco traseiro estático é um braço esticado, com pouca participação de tronco. Nos frontais, o punho continua visível em F02–F04; não confirmo o desaparecimento relatado. A folha `dev/walk.png` não permite localizar flicker. Relógio automático não substitui o olho.

10. **Página funciona e tem um rótulo adiantado.** `Biblioteca de Arte/Estudos Comparativos/Orc principal - Reconstrucao traseira/index.html` L42 aponta o relatório de orquestração como se já contivesse este parecer. `orchestration-report.md` L107 ainda diz que o parecer está em execução e não liga `qa/report.md`. L208–L238 chamam os quatro traseiros de candidato rejeitado, mas `rejectedEvidence` aponta a rejeição histórica `experiments/main-orc-rear-recovery-v2/rejected/flat-weapon-masters/`, não o F04 desta versão. A página não exibe `eligibleForIntegration=false`, embora o crachá seja `ARTISTIC_REVISION_REQUIRED` / `PENDING_CREATOR`. Conteúdo da página: 775 arquivos (772 nas subpastas + `index.html`, `catalogo.json`, `manifest.json`). O “770 copiados” do orquestrador não foi reproduzido como essa conta.

11. **`technicalStatus` do clipe não é aceite.** O pacote está `NOT_VERIFIED` (manifesto L952). Os oito `clip.json` dizem `TECHNICALLY_COMPLETE` com `choreographyChanged: false`. Isso descreve empacotamento, não movimento nem aprovação.

12. **Documentação de integração não promove o passe.** `docs/ROADMAP.md` L3–L12, `docs/MAIN_ORC_COMBAT_POLISH.md` L1, `docs/RECIPES.md` L29 e regras 7–8, `docs/ASEPRITE.md` L77–L93. A prosa antiga de arcos traseiros “corrigidos” no polimento permanece histórica; o aviso do topo impede lê-la como resultado desta versão. Nenhuma receita foi aprovada.

O especialista em `source/rear-reconstruction-v4-specialist` não foi julgado. Não está nas células.

## Pacote técnico versus tarefa artística

Integridade do pacote diagnóstico: **PASS**. 761/761 hashes do freeze; 28 células únicas, 210 quadros, 8 afetados/82 e 20 aliases/128; alfa-over, recorte nativo `[64,64]`, tempos e `handFront` dos 82 quadros; armas ocultas vazias; preservação 2939/2939; unittest do construtor 4/4; Chromium 20/20 na página real, capturas só em `qa/browser-checks`.

Tarefa artística original: **FAIL**. Não há espada e machado traseiros naturais e distintos, nem pegada convincente, nem Unarmed traseiro reparado, nem flicker de Walk corrigido. Verde técnico e disclaimers verdadeiros não fecham as seções 4–8, 10 e 17.

## Limitações e ferramentas

Não assisti reprodução contínua em 1× nem na escala tática como movimento. O teste Chromium avançou quadros e aplicou canvas de 128 px; isso é relógio, não olho. Inspeção visual foi estática, nearest-neighbor, em `qa/sheets/` e nas pranchas do DEV.

Ferramentas reais desta sessão: leitura de arquivo, `view` de PNG, Python `tmp/pixel-venv` com Pillow, Node + Playwright no caminho já indicado pelo teste, Chromium headless desse teste, Aseprite `--batch --noinapp` só para reexportar os dois mestres de arma. Não usei MCP de browser, não lancei agentes, não editei arte, docs ou Unity, não instalei pacotes e não houve geração paga.

Não rerrodei a suíte Node 7/7 da entrada anterior. O corpo `.aseprite` completo não foi reexportado; a álgebra das camadas PNG cobre os 82 compostos.

Evidência: `qa/checks.json`, `qa/qa-result.json`, `qa/sheets/`, `qa/browser-checks/`, `qa/aseprite-proof/`.

## Adendo — re-revisão estreita de apresentação, 2026-10-29

Mesma sessão de QA. Sem nova arte, sem novo freeze e sem reinspeção dos quadros. O veredito global permanece **`ARTISTIC_REVISION_REQUIRED`**, tarefa artística **FAIL**, pacote diagnóstico sem elegibilidade, `PENDING_CREATOR`. O estudo do especialista continua fora da matriz; a cota interrompida não entra neste parecer.

O achado 10 de apresentação foi conferido nas superfícies alteradas e fica **fechado**, sem promover a arte.

| Correção pedida | Conferência | Resultado |
|---|---|---|
| `orchestration-report.md` liga `qa/report.md` e registra FAIL artístico / PASS diagnóstico | Abertura aponta `qa/report.md`. O corpo repete o FAIL amplo e separa overlay vazio de resíduo no corpo. | PASS de apresentação |
| 775 totais versus 770 indexados | Contagem atual: 775 arquivos; 2 `weapon.json`; 3 de topo (`index.html`, `catalogo.json`, `manifest.json`). 770+2+3=775, como o relatório agora distingue. | PASS |
| Página e catálogo mostram `eligibleForIntegration=false` | `index.html` tem `#integration-eligibility`: “false — somente diagnóstico; não integrar nem promover.” `catalogo.json` L77 é `false`. O construtor rejeita valor não booleano e propaga o rótulo. | PASS |
| Link herdado não finge ser o F04 desta versão | Os quatro links dizem “Registro vinculado de rejeição (conferir versão e escopo)” e ainda apontam `rear-recovery-v2/rejected/flat-weapon-masters/`. | PASS |
| Testes focados | Unittest do construtor 4/4 PASS. Chromium na página real 21/21 PASS, inclusive o check novo de inelegibilidade. Capturas em `qa/browser-checks-addendum/`, sem sobrescrever as anteriores. | PASS funcional; 1× contínuo continua `NOT_VERIFIED` |

Ressalva não bloqueante: `index.html` L42 ainda manda o leitor ao relatório de integração, em vez de ligar `qa/report.md` direto. O relatório de integração agora contém o parecer e o link, então a alegação antiga deixou de ser falsa. Não reabre o achado.

**Esclarecimento da matriz, linha de ataque-only.** O PASS anterior cobre só overlays vazios fora do intervalo e fontes de arma separadas. Não satisfaz a política. `back_l/Sword` nativo F01 e F07 ainda têm lâmina/disco pintados no corpo com as camadas de arma desligadas. Independência semântica do corpo: **FAIL**. O PASS de overlay vazio não pode ser lido como ataque-only cumprido.
