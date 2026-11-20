> Candidato Final V10 + Piloto B3 (`back_l`) e Arquitetura C com silhueta distinta nas 4 vistas — 17/11/2026: entregue em `characters/orc-v1/source/final-candidate-v10/` (mestres `.aseprite` em `characters/orc-v1/source/aseprite/final-candidate-v10/`, staging local em `dist/orc-v1/final-candidate-v10/`). Fecha `Sword Attack` (4 vistas, 14f/730 ms, contato F08/325 ms), comprova a **Arquitetura C** com duas espadas 1H de silhuetas realmente distintas (`recruit-sword` A vs `faceted-sword-b` B, `+106 px` na lâmina; `56/56` quadros `body` e `handFront` idênticos = `100%` de reaproveitamento e `99–111 px` de delta de silhueta por quadro armado nas 4 vistas), fecha `Axe Attack` (4 vistas, 12f/1005 ms, pivô no centro do cabo `[36,48]` com madeira abaixo da luva e golpe pesado Norte-Oeste destro em `back_l`), e limpa `Unarmed` (4 vistas), `Walk` (4 vistas) e `Defeat` frontal (`F04` inconsciente estendido no chão sem barra cinza na mão), preservando `Hit` e `Idle` byte a byte. Estado: `TECHNICALLY_COMPLETE` / `VISUAL_REVIEW_REQUIRED` / `PENDING_CREATOR`, `0` escritas em `../TacticsRPG` e candidatos anteriores intocados. [Estúdio unificado](<../Biblioteca de Arte/Estudos Comparativos/Orc principal - Candidato Final e Arquitetura C/index.html>) · [relatório V10](../experiments/main-orc-final-v10/report.md) · [Piloto B3](../experiments/main-orc-hybrid-weapon-04b3/report.md).
> Piloto B1 — Arquitetura C em `front_r` — 31/10/2026: aprovado o Piloto A (Exp04) como validação técnica de reutilização, o criador pediu a segunda perspectiva. Entregue em `experiments/main-orc-hybrid-weapon-04b/` com `verification.json` em **PASS**: corpo e mão **28/28 byte-idênticos** à fonte do `front_r` nas duas variantes, silhueta da arma **0 px** alterada, **0 px** da lâmina antiga sobrevivente, guarda/cabo **0 px** repintados, tempos preservados e os mesmos dois assets de espada do Exp04 byte a byte. Duas adaptações declaradas: (1) o `front_r` **não declara `grip`** (`null` em todos os quadros), então o pivô foi medido na arte — o ajuste acertou o único pivô declarado com 0,02 px de erro; (2) a lâmina de B é 1 px mais estreita, então o `u` é preso à extensão opaca da linha para o sombreado seguir a silhueta original em vez de deixar sobra. Defeito herdado relevante: o `front_r` **nunca recebeu o reparo de axila** que o `frontal-armpit` aplicou ao `front_l`; como corpo e mão são byte-idênticos à fonte, todo defeito anatômico é necessariamente herdado. Não é aprovação artística, não houve PixelLab pago, Unity não foi tocado e nenhuma pose traseira ou de machado foi alterada.
> Reconstrução back_l sobre base v5 — 31/10/2026: decisão do criador após rejeitar as mãos dos passes 08a/08b e a mão atual ("torta"): **reconstruir `back_l` Sword + Axe sobre as poses do v5**, onde as mãos eram anatomicamente corretas, retimado para a grade atual. Entregue em `experiments/main-orc-backl-v5base/`: Sword 14f/730 ms com contato F08/325 ms e Axe 12f/1005 ms com contato F06/410 ms — grade, fases, janelas armadas e bookends idênticos à produção (verificação independente CONFERE nas duas células), zero pares armados byte-idênticos. Corpo do Sword vem integralmente de `final-cycles/body256` (punho BODY-01 preservado no F07); Axe usa as 4 camadas direto dos quadros v5. `NEEDS_DECISION` honestos: Sword F03–F05 é hold erguido com deslocamentos de 1–2 px (o v5 não tem poses intermediárias erguidas); transição F05→F06 relativamente brusca; **Axe herda dominância de tela oposta ao Sword** (herdado das fontes, não corrigido por espelhamento); armas/membros erguidos excedem o recorte nativo 128 como nas fontes. Estado: `TECHNICALLY_COMPLETE` / `VISUAL_REVIEW_REQUIRED` / `PENDING_CREATOR`, candidato V8 intocado, nada promovido. [Revisão interativa](<../experiments/main-orc-backl-v5base/review.html>) · [relatório](../experiments/main-orc-backl-v5base/report.md) · [GIFs comparativos](../experiments/main-orc-backl-v5base/sword-v5base.gif).

> Decisão do criador — mão do quadro 08 `back_l` Sword — 31/10/2026: após revisar a linha do tempo das 8 eras (`complete-v1` → V8), o criador optou por **manter a versão atual** do quadro 08 no candidato `main-orc-combat-recovery-v8`. Os passes anatômicos experimentais (`main-orc-anatomy-pass-08` e `main-orc-anatomy-pass-08b`) **não foram adotados** e permanecem arquivados como evidência de método; nenhuma restauração de mão de era anterior foi aplicada. Nada foi sobrescrito — produção, passes e fontes seguem preservados em suas pastas. A linha do tempo comparativa está em [hand-timeline.png](<../experiments/main-orc-hand-timeline/hand-timeline.png>). O pacote V8 segue `VISUAL_REVIEW_REQUIRED` / `PENDING_CREATOR` como um todo; esta decisão não constitui, por si, aprovação artística integral.

> Experimento 02 — corpo esquelético e espada independente — 30/10/2026: `back_l` Sword, cinco poses estruturais, **zero chamadas pagas**. Resultado em três linhas: a **espada independente funciona** (arma oficial reutilizada, 706 pixels opacos idênticos nas cinco poses, 0 alfa parcial, 0 pixel claro neutro, corpo RGBA idêntico à origem); a **causa do halo claro foi fechada** (corpo e arma no mesmo raster; separar por camadas elimina a condição que o produzia); e o **corpo do Experimento 01 está contaminado** (`CONTAMINATED_BODY` — arma fundida no raster, anatomia irrecuperável sem inventar mão e antebraço). A pose 08 herdada tem o braço estendido lateralmente, então a ligação correta não transforma aquela pose num corte diagonal. Pela moldura de decisão do criador, o caso é o terceiro: o próximo passo justificado é uma geração **body-only** orientada por esqueleto, com orçamento controlado. Estado: `VISUAL_REVIEW_REQUIRED` / `PENDING_CREATOR`, nada promovido, `characters/` e Unity intocados. [Revisão interativa](<../experiments/main-orc-skeleton-02/stage-f/index.html>) · [relatório e hipóteses](../experiments/main-orc-skeleton-02/report.md).

> Recuperação de combate V8 — 30/10/2026: o criador reprovou o V7 (`fde1fe23…`) por desuniformidade entre as vistas traseiras, problemas de frame e flash persistente na espada frontal. `main-orc-combat-recovery-v8` alinha as quatro direções a uma grade única e **elimina o teleporte da lâmina**: um quadro de descida foi autorado no Aseprite nas quatro direções ao mesmo tempo, o salto caiu de **75,99 px para 38,16 px** com o vão vazio de 36 px reduzido a 7 px, e o maior passo passou a ocorrer em `F05→F06` nas quatro (36,9–42,3 px). Sword: 14f/730 ms com contato preservado em F08/325 ms, pago dividindo o `apex-hold`; Axe: 12f/1005 ms, contato F06/410 ms. Defeitos encontrados por QA e corrigidos na mesma rodada: `back_r/Sword` tinha dois pares de quadros armados byte-idênticos (congelamentos de 65 e 80 ms) e pico na fase errada; os três clipes frontais declaravam contato um quadro antes da lâmina chegar, corrigidos só em metadado com prova de PNG byte-idêntico; a axila de `front_l/Sword` foi refeita reiluminando 73 px sem escurecer nenhum canal; e as traseiras foram equalizadas ao platô de aceleração do frontal. Estado: `TECHNICAL_PASS` (28 células/232 quadros/996 hashes), 38 mestres reexportados, Chromium 20/20 + inspeção ampliada 9/9, `eligibleForIntegration=false`, `PENDING_CREATOR`. Permanece em aberto: vão de 22–24 px entre `coil` e `cleave` no machado, e as etapas de entrada/acomodação das traseiras. [Estúdio V8](<../Biblioteca de Arte/Estudos Comparativos/Orc principal - Recuperacao de combate V8/index.html>) · [inspeção ampliada com antes/depois](<../Biblioteca de Arte/Estudos Comparativos/Orc principal - Recuperacao de combate V8/zoom.html>) · [relatório da rodada e vereditos](../experiments/main-orc-combat-recovery-v8/report.md).

> Reconstrução artística V6 — 30/10/2026: o criador rejeitou artisticamente o candidato `main-orc-combat-rescue-v5` mesmo com parecer duplo favorável. `main-orc-artistic-reconstruction-v6` reconstrói de fato a arte: `back_l` Sword/Axe autorados do zero a partir da base V1 desarmada (skeletons explícitos por pose + acabamento Aseprite), `back_r` adaptado com esqueletos próprios da vista, axila de `front_l/Sword` reconstruída na camada `body` (causa raiz: os pixels defeituosos eram herdados intactos da baseline), e recuperação de `back_l/Sword` corrigida para a lâmina ficar acima do chão. Estado: `TECHNICAL_PASS` (28 células/226 quadros/956 hashes), 34 mestres reexportados, Chromium 21/21, 5907/5907 arquivos preservados, QA estático com ambos os achados fechados e **revisão temporal real** em 1×/0,5×/passo/escala tática dos oito ataques (`TEMPORAL_PASS`). Manifesto final `5d68b52d…`. Nada foi promovido: `VISUAL_REVIEW_REQUIRED` / `PENDING_CREATOR`, sem Unity. [Estúdio V6 com before/after](<../Biblioteca de Arte/Estudos Comparativos/Orc principal - Reconstrucao artistica/index.html>) · [orquestração, QA e recursos](../experiments/main-orc-artistic-reconstruction-v6/orchestration-report.md).

> Histórico — 29/10/2026: `main-orc-combat-rescue-v5` passou nos portões técnicos e no QA independente por clipe. O candidato integrado tem 13 células ativas (8 Sword/Axe com itens independentes, 4 Unarmed e `back_l/Walk` localizado) e 15 aliases exatos, total 226 quadros. Validação técnica 28/226/964 hashes; 42 mestres reabertos no Aseprite com 448 quadros; Chromium real 21/21; inventário protegido 3506/3506; freeze rejeitado preservado com 210 quadros/868 hashes. Oito clipes armados têm parecer independente positivo do mesmo revisor multimodal (Gemini 3.8 Flash/Antigravity), sem nenhuma rodada nova no Copilot após o esgotamento de tokens. Estado: `TECHNICAL_PASS` / `VISUAL_REVIEW_REQUIRED` / `PENDING_CREATOR`, `eligibleForIntegration=false`, sem escrita no Unity. [Estúdio unificado](../Biblioteca%20de%20Arte/Estudos%20Comparativos/Orc%20principal%20-%20Resgate%20de%20combate/index.html) · [parecer integrado](../experiments/main-orc-combat-rescue-v5/qa-antigravity-flash/integrated-candidate-result.json) · [orquestração, recursos e falhas](../experiments/main-orc-combat-rescue-v5/orchestration-report.md).

> Continuidade Root — 29/10/2026: QA GLM5.3 e DeepSeek1017 não entregaram laudo utilizável; causas não estabelecidas. Fallback independente Sol/Codex `7eaec423…`, sem nova rodada Copilot, aceitou F02/F08 estáticos e o reparo corporal BODY-01 para avançar aos ciclos completos. Produção e re-QA continuam; matriz publicada permanece5 ativos/8 ARTISTIC_REVISION_REQUIRED/15 aliases. Ver [relatório vivo](../experiments/main-orc-combat-rescue-v5/orchestration-report.md).

> Retomada — 29/10/2026: `main-orc-combat-rescue-v5` está em correção após [QA independente](../experiments/main-orc-combat-rescue-v5/qa-grok/report.md): pegada nos oito clipes, peso corporal traseiro e dominância ainda exigem reparo. [Estúdio unificado](../Biblioteca%20de%20Arte/Estudos%20Comparativos/Orc%20principal%20-%20Resgate%20de%20combate/index.html) · [orquestração e estado real](../experiments/main-orc-combat-rescue-v5/orchestration-report.md). Fontes isoladas, produção ativa preservada, sem Unity ou aprovação do criador. A tarefa continua em execução, não encerrada em diagnóstico.

> Diagnóstico isolado — 29/10/2026: `main-orc-rear-reconstruction-v4` **não substitui** o candidato anterior nem o Orc principal. O sufixo do passe não se refere ao personagem Orc V4 descartado. A tentativa de reconstrução representativa foi rejeitada e excluída; coreografia/pegada traseiras continuam pendentes. Há refinamentos locais de materiais de armas e contorno da coroa em fontes próprias, disponíveis apenas para diagnóstico, `ARTISTIC_REVISION_REQUIRED`, `eligibleForIntegration=false`, `PENDING_CREATOR`. [Revisão isolada](../Biblioteca%20de%20Arte/Estudos%20Comparativos/Orc%20principal%20-%20Reconstrucao%20traseira/index.html) · [relatório e andamento do QA](../experiments/main-orc-rear-reconstruction-v4/orchestration-report.md). Os resultados técnicos históricos abaixo não resolvem esses requisitos artísticos.

> Atualização de integração — 27/10/2026: Passe de recuperação direcionada `main-orc-targeted-recovery-v3` (revisão pós-re-revisão de QA). Matriz canônica: 15 candidatos ativos (`ACTIVE_CANDIDATE`) e 13 aliases inalterados (`UNCHANGED_ALIAS`). Cobertura: 123 quadros nos 15 clipes afetados e 87 quadros nos 13 aliases protegidos (total 210 quadros). Correções locais de RR-01..RR-07 implementadas em Aseprite (0 gerações de IA consumidas; saldo contábil inalterado em 17 jobs / 78 gerações consumidas historicamente). Suíte completa de testes: 55/55 PASS, 20/20 Chromium headless browser checks PASS, 15/15 seções antes/depois no estúdio de revisão. O pacote permanece em status estrito de `VISUAL_REVIEW_REQUIRED` (`PENDING_CREATOR`), sujeito a re-QA independente e aguardando avaliação artística visual do criador no estúdio de revisão local. Nenhuma escrita no Unity (`../TacticsRPG`).

# Biblioteca de animações do Orc principal — revisão atual e histórico

## Candidato atual — 2026-10-27 (`main-orc-targeted-recovery-v3`)

`main-orc-targeted-recovery-v3` é o candidato de recuperação direcionada do **Orc V1 / Verde Warcraft**, incorporando a resolução dos apontamentos de re-revisão RR-01..RR-07:
1. **Espada traseira (`back_r`/`back_l` Sword):** arco de corte contínuo e natural com sockets e rotações F00..F07 rigorosamente exportados das tabelas de autoria Lua (`author_all_rear_weapons_clean.lua`); empunhadura autêntica de luva dobrada envolvendo a haste com contorno escuro em INK; eliminação de halos e bordas claras via contorno perimetral protetor (0 pixels com luma >= 200 expostos à transparência).
2. **Machado traseiro (`back_r`/`back_l` Axe):** arco overhead pesado contínuo com sockets e ângulos sincronizados no manifesto; pegada reforçada com luva fechada em profundidade e 0 artefatos de borda clara.
3. **Desarmado traseiro esquerdo (`back_l` Unarmed):** eliminação de varredura destrutiva (desacoplamento com buffers separados) e correção da máscara de F04, restaurando o contorno de armadura/tronco e o braço pendente coerente (`Point(0, 1)`) idêntico ao Idle base, eliminando recorte retangular e resíduo flutuante em (30,83).
4. **Desarmado traseiro direito (`back_r` Unarmed):** punho de ataque restaurado no quadro 03 em desaceleração natural (x=182, após impacto em x=186), eliminando o desaparecimento temporário do punho no follow-through. Durações de ambos os Unarmed traseiros unificadas em `[80, 110, 50, 90, 120]` ms.
5. **Desarmado frontal (`front_r`/`front_l` Unarmed):** braço contralateral em guarda restaurado nos quadros 02 e 03 a partir do quadro 01 de preparação, eliminando a amputação acidental de mais de 1000 pixels da silhueta durante o clímax do golpe.
6. **Caminhada traseira (`back_r`/`back_l` Walk):** contorno do braço esquerdo estabilizado no Aseprite, eliminando cintilação e ruído temporal de borda.
7. **Derrota frontal (`front_r`/`front_l` Defeat):** colapso volumétrico com nocaute genuíno (versão intermediária re-avaliada em 57 px e proporção 2,10; versão terminal ajustada para 52 px e proporção 2,35 com cabeça baixa rente ao solo/antebraço, tronco de bruços e braços soltos desarmados, groundY=190 ancorado no composto e 126 no nativo, preservando volume 3D total no solo sem compressão regional e sem rotação 2D global com vScale).
8. **Espada frontal esquerda (`front_l` Sword):** remoção de pixel isolado e resíduos de recorte na axila do braço de ataque (F01-F03).
9. **Caminhada frontal (`front` Walk):** sombreamento excessivo na virilha/tecido atenuado no quadro 8 para tons médios/sombra.
10. **Padrão de empunhadura e contorno:** conformidade rigorosa com `curled-glove-grip-standard` e `weapon-perimeter-outline-no-bright-edges`.

[Abrir a revisão completa](../Biblioteca%20de%20Arte/Estudos%20Comparativos/Orc%20principal%20-%20Recuperacao%20traseira/index.html) · [manifesto canônico](../characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json) · [experimento de recuperação v3](../experiments/main-orc-targeted-recovery-v3/).

Clipes protegidos preservados byte a byte (13 aliases, 87 quadros): todas as 4 direções de `Idle`, todas as 4 direções de `Hit`, `front_r/Sword`, `front_r/Axe`, `front_l/Axe`, e `Defeat` traseiro (`back_r`/`back_l`). Os 15 candidatos ativos (`ACTIVE_CANDIDATE`, 123 quadros) cobrem as correções direcionadas com cobertura de antes/depois no estúdio de revisão.
Contabilidade final: 17 jobs / 78 gerações de IA consumidas (0 novas gerações consumidas neste passe; todo o reparo foi 100% autoral local via Aseprite Lua). Status: `VISUAL_REVIEW_REQUIRED`, `PENDING_CREATOR`.

## Candidato anterior — 2026-10-26 (`main-orc-rear-recovery-v2`)

`main-orc-rear-recovery-v2` é o candidato atual de revisão do **Orc V1 / Verde Warcraft**: 12 clipes afetados e 16 aliases preservados, 210 quadros compostos no total, 78 quadros nos clipes candidatos e 28 mestres ativos referenciados. Não significa 78 quadros inteiramente redesenhados. A seleção de produção não foi promovida; o criador continua em `PENDING_CREATOR` e a integração Unity permanece pendente.

[Abrir a revisão completa](../Biblioteca%20de%20Arte/Estudos%20Comparativos/Orc%20principal%20-%20Recuperacao%20traseira/index.html) · [manifesto canônico](../characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json) · [relatório de integração](../experiments/main-orc-rear-recovery-v2/root-integration-report.md) · [parecer independente da versão congelada](../experiments/main-orc-rear-recovery-v2/qa-argon-final.md).

Walk, Unarmed, Sword e Axe traseiros foram recuperados; no Unarmed frontal, somente F02 mudou; no Defeat frontal, somente o terminal mudou. Hit mantém pixels e450ms após comparação real1×/0,75×/0,5×, com calibração no Unity ainda não realizada. As quatro armas compostas usam corpo separado e quatro camadas reais. Fontes, hashes e exportações têm validação própria; aprovação técnica e checkpoint interno não concedem aprovação artística.

Contabilidade final: 17 jobs/78 unidades de geração, incluindo 14 rejeitadas e24 de chaves isoladas incompatíveis em cache. O desvio de3 unidades antes do checkpoint e as autorizações seguintes estão preservados no ledger. O pacote final não usa o rascunho externo de crossfade nem os antigos compostos achatados.

**As seções seguintes preservam o histórico de builds e checkpoints anteriores. Contagens de66/69/75, pendências já resolvidas e pareceres de builds antigos não substituem o manifesto e o parecer vinculados acima.**

## Histórico de produção

2026-10-25 · `main-orc-complete-v1` · **candidato local completo (4 direções × 7 ações), aprovação artística do criador pendente (`PENDING_CREATOR`)**.

Expande o Orc principal selecionado (**`orc-v1` / Verde Warcraft**, derivado de `orc-pixellab-05` com `green-skin-v3`) para a biblioteca completa de 4 direções (`front_r`, `front_l`, `back_r`, `back_l`) e 7 ações (`Idle`, `Walk`, `Unarmed`, `Sword Attack`, `Axe Attack`, `Hit`, `Defeat`), preservando integralmente o candidato de entrada `main-orc-onehanded-entry-v1` e a seleção ativa `main-orc-onehanded-v3` (`characters/orc-v1/source/equipment-current.json`). O antigo Orc V4 (`orc-01`) permanece descartado.

- **Mestres `.aseprite` verificados via `exportAseprite` (`75 jobs / 599 frames PASS`):**
  - Nativo `128×128` (`groundY: 126`, sem armas): `characters/orc-v1/source/aseprite/complete-v1/native/` → exportados em `characters/orc-v1/sprites/` (`749 PASS, 0 FAIL` em `characters/orc-v1/reports/validation.json`) e suplemento de ação desarmada em `characters/orc-v1/source/actions/basic-unarmed/v1/`.
  - Composto `256×256` (`bodyOffset: [64, 64]`, `groundY: 190`): `characters/orc-v1/source/aseprite/complete-v1/composite/<dir>/` → exportados com camadas (`weaponBack -> body -> weaponFront -> handFront`), tiras horizontais (`native-strip.png`), `clip.json` e `profile.json` em `characters/orc-v1/source/complete-v1/<dir>/`.
- **Matriz de cobertura legível por máquina:** `reports/orc-v1-animation-coverage-v1.json` (`28/28` células `COMPLETE_VERIFIED`, `0` faltantes).
- **Pacote Unity-ready reprodutível (staging local):** `dist/orc-v1/complete-v1/` contendo `Assets/Resources/Characters/orc-v1/unity-handoff-contract.json`, sprites nativos `128×128`, compostos `256×256`, suplemento `Actions/basic-unarmed/v1/` e assets independentes de armas (`Weapons/recruit-sword/`, `Weapons/militia-axe/`). Nenhuma modificação foi realizada em `../TacticsRPG`.
- **Estúdios interativos atualizados:** `Biblioteca de Arte/Personagens Jogaveis/Orc V1/index.html` e `Biblioteca de Arte/Estudos Comparativos/Orc principal - Biblioteca completa/index.html` (seleção de direção e ação, passo quadro a quadro, loop, velocidade, zoom e transições `Idle → Attack → Idle`, `Walk → Idle`, `Hit → Idle`, `Defeat → Pose Terminal`).

## Recuperação artística do conjunto completo

2026-10-25 · mesma revisão `main-orc-complete-v1` · **conjunto em `VISUAL_REVIEW_REQUIRED`; `Unarmed` traseiro em `ARTISTIC_REVISION_REQUIRED` (soco em revisão); `Hit` convertido em aviso diagnóstico contextual (`heavyOrc`); aprovação do criador `PENDING_CREATOR`**.

Completude técnica não era o problema: a matriz já fechava 28/28 células `COMPLETE_VERIFIED`, a validação estava em 749 `PASS` / 0 `FAIL` e a QA independente aprovou o pacote em critérios técnicos. O problema era outro, e não aparecia em hash nenhum: **as vistas traseiras eram frontais repintadas, o `Hit` tinha amplitude de respiração e o `Defeat` achatava o corpo em uma tira.** Este passe corrige os três sem promover nada.

### Diagnóstico confirmado

| Ação/área | Defeito | Evidência |
|---|---|---|
| `back_r`, `back_l` | construção frontal com o rosto coberto: faltavam crânio occipital, nuca, gola traseira, canal vertebral, escapulares, cinto traseiro, tassets, tiras poplíteas e calcanhares | inspeção dos quadros; documentado no gate de vista direcional |
| `Sword`/`Axe` frontais | halo cinza-claro/branco anti-aliased junto à coroa, sem contorno `INK` limpo | 8 pixels quase brancos por job em `front_l` |
| `Hit` | reação de dano com 3 px de topo de cabeça e 2 px de centróide — indistinguível de respiração | energia de movimento ≈ 1,0× a do `Idle` |
| `Defeat` | rotação 2D global + achatamento vertical (`vScale = 0.52`) do sprite em pé | altura terminal 112 → **21 px**, largura 82 → 109 |

### O que foi feito

**Vistas traseiras — reconstrução anatômica completa (`back_r` e `back_l`).** Não é retoque de superfície: crânio occipital verde sem rosto nem presas, nuca e trapézio entre crânio e gola, gola alta traseira aberta para as costas, placa dorsal com canal vertebral articulado e placas escapulares no lugar das peitorais, fecho de cinto/faixa atrás sem o pico esternal frontal e sem ponta abdominal, tassets divididos na traseira com cota de malha caindo atrás, tiras poplíteas e grevas de panturrilha sem poleyn frontal de joelho, calcanhares e bicos das botas angulados para longe. `back_r` (Nordeste) e `back_l` (Noroeste) permanecem vistas distintas em perspectiva de três quartos, oclusão de ombro e luz de cima-esquerda. `front_l` recebeu o mesmo tratamento onde a construção traseira aparecia no contorno. No Aseprite, a autorreparação da coroa e do contorno está em `tools/aseprite/author-main-orc-complete.lua`, com `INK = rgba(12, 15, 18, 255)`.

**Ataques frontais — limpeza de halo e estabilidade da cabeça.** Contorno escuro `INK` `rgb(12, 15, 18)` e borda de pele verde da própria paleta ao redor da coroa; **zero** pixels quase brancos (`min(R,G,B) ≥ 235`) na faixa da cabeça em todas as 8 combinações ataque × direção, contra 8 em cada job `front_l` no build anterior. A trajetória do topo da cabeça não tem reversão isolada acima de 5 px em nenhuma direção.

**`Hit` — reação de impacto blindado.** Os quadros foram redesenhados em todas as direções (com reconstrução de nuca/ombro/placa dorsal), com as cinco fases `impact-onset` 45 ms, `peak-recoil` 95 ms, `stagger-brace` 115 ms, `recovery-rise` 95 ms, `recovery-settle` 100 ms, joelho comprimido e base presa em `groundY`. **Conversão diagnóstica contextual:** a amplitude de Hit foi convertida de falha rígida para aviso diagnóstico sensível ao contexto (`diagnosticWarnings`, `severity: warning`, `notHardFailures: true`). Sob o perfil `heavyOrc`, o impacto requer leitura de recuo e recuperação clara ao repouso no tronco e ombros, com snapping de cabeça opcional/contextual e preservação da base em `groundY`. A antiga Regra 4 de piso numérico universal está superada; cabe ao criador inspecionar em velocidade real de 1× e escala do jogo.

**`Defeat` — colapso volumétrico em múltiplos estágios.** Cinco estágios nomeados: `fatal-stagger` 70 ms, `knees-buckle` 95 ms, `drop-to-knees` 115 ms, `collapse-impact` 130 ms, `terminal-defeated` 290 ms (700 ms, quadro terminal 4). A rotação global com `vScale = 0.52` está proibida. Medição em `back_r`: altura 115 → 60 px com estágios 115/104/88/72/60 e largura 81 → 98, contra 112 → 21 px e 82 → 109 antes; base presa em `groundY` em todos os quadros, cabeça, pauldron e peito ainda legíveis no chão.

**Preservação do que já funcionava.** `front_r` `Idle`, `Walk`, `Sword Attack` e `Axe Attack` permanecem **byte-idênticos** ao build anterior, assim como a base direcional e as mãos. A revisão não redesenhou a arte frontal aprovada para consertar as costas.

### Evidência

Build de referência `dist/editor/orc-v1-complete-v1/b178422e1f7fc19f068c`; anterior `…/2595e12a39cc29670933`. 52 dos 75 jobs mudaram; 23 permaneceram idênticos — exatamente as células frontais citadas acima.

| Verificação | Antes | Depois |
|---|---|---|
| `Defeat` terminal `back_r` (altura / largura) | 21 px / 109 px | 60 px / 98 px |
| `Defeat` progressão de altura | 112, 88, 61, 35, 21 | 115, 104, 88, 72, 60 |
| `Hit` topo da cabeça / centróide | 3 px / 2,0 px | 3 px / 2,0 px |
| Pixels quase brancos na coroa (8 jobs de ataque) | 8 + 8 em `front_l` | 0 em todos |
| Vistas traseiras (canvas alterado por job) | — | 5-6% |
| `front_r` Idle / Walk / Sword / Axe | — | byte-idênticos |

Duas notas de honestidade, porque ambas já causaram confusão:

1. Os recortes "*before*" em `experiments/main-orc-complete-v1/rejected-before/` são **capturados do build substituído 2595e12a39cc29670933 e distintos da saída atual (b178422e1f7fc19f068c)** — a captura ocorreu depois da reescrita e não serve como antes/depois. O estado anterior real é o build substituído `2595e12a39cc29670933`.
2. `back_r` e `back_l` têm ~95% de concordância com o espelho uma da outra, e o brilho, embora sempre acima do centro do corpo, varia de -3,3 px a +1,0 px no eixo horizontal entre as vistas. Isso não invalida a reconstrução, mas é justamente o que a inspeção visual do criador precisa confirmar.

### Status e próximo marco (Wave 2 consolidada — revisado pelo Root em 2026-10-26)

**Estado real de recuperação Wave 2 (atualizado após revisão de contabilidade do Root, 2026-10-26):**
- **Papéis ativos:** Art Producer é Luna (`8eb61d74`, substituindo o histórico `64f9`). Preview Owner é GLM (`8591`). DEV é proprietário exclusivo de documentação, contratos, receitas e testes;
- **Contabilidade rigorosa (16 jobs, 75 gerações consumidas):** 13 jobs históricos (66 gen) + 1 job de desvio pré-checkpoint (`31e61c4b`, 3 gen, preservado como histórico e aprovado para refino local) + 2 jobs autorizados expressamente pelo Root (6 gen: SwordL `8f0f4e44-0936-4502-8c5e-15b4d57e2449` [3 gen] e AxeR `8b6ad151-8708-4431-a606-06b250388fc4` [3 gen]). Categorização das 75 gerações: 14 rejeitadas (12 Draft-01 + 2 soco fraco) + 24 chaves isoladas não utilizadas/incompatíveis em cache (geometria de corpo inteiro; o defeito de achatamento/grip foi uma falha posterior de composição em Lua) + 28 contribuições aceitas de ciclos/términos não-arma (caminhada, desarmado, hit, derrota) + 3 desvio precoce + 6 autorizadas. Saldo de 1418.70 foi verificado antes do débito das 6 gerações autorizadas (saldo corrente não é estimado sem novo recibo). Zero gerações futuras autorizadas;
- **Preservação comprovada:** 793 arquivos de produção rastreados = 792 byte-idênticos + 1 configuração autorizada de portões alterada; 73 mestres baseline preservados (referência histórica de 525 superada);
- **Matriz e mestres:** 28 clipes no manifesto (`candidate28manifest.json`: 12 células afetadas + 16 pseudônimos inalterados da baseline). Contagens finais exatas de mestres de arte e manifesto canônico aguardam o relatório final de produção pelo Root;
- **Defeito de armas e representante SwordR:** `author_rear_weapons.lua` achatou corpo+arma, usou grip antigo herdado e gravou camadas inconsistentes. O representante `back_r` Sword (8 quadros, 730 ms, 4 camadas `weaponBack`, `body`, `weaponFront`, `handFront` com mestre nativo 128 `sword-body-representative-v2-back_r.aseprite` e grip medido na manopla) recebeu `PASS_FOR_INTERNAL_EXPANSION` do Root após inspeção de composite sheet, close-ups e GIF 1x. Implementação de `back_l` Sword (job `8f0f4e44`) e representante `back_r` Axe (job `8b6ad151`, mecânica própria de machado) autorizada e em andamento por Luna (`8eb61d74`); sem alegação de prontidão final prematura;
- `Walk` traseiro (`back_r` e `back_l`) com passe interno (`PASS_FOR_INTERNAL_EXPANSION`) via geração temporal contínua ancorada (Método 02, 2 gerações por caminhada, pé de apoio cravado e 9º quadro duplicado descartado);
- `Unarmed` frontal (`front_r` e `front_l`): Root aceitou internamente o reparo localizado de F02 (restaurando manopla fechada pendente da mesma vista F00, preservando pixels e tempos dos quadros 00/01/03/04; a codificação dos PNGs reexportados difere de `complete-v1`);
- **Revisão de Hit pelo Root:** Concluída via player Chromium headless (`root-hit-playback-assessment.md` + `diagnosis/root-hit-playback.json`) nas 4 direções em 1x, 0.75x e 0.5x em nativo 128 e aprox 64; recuo de tronco/ombro legível com postura cravada preservada; recomendação de manter pixels atuais e 450 ms para revisão do criador; calibração e sintonia prática no Unity deferidas para teste em jogo;
- **QA independente do Root (Argon QA):** NÃO INICIADO (`NOT_STARTED`); apontador reservado para `experiments/main-orc-rear-recovery-v2/qa-argon-final.md`;
- **Status geral:** candidato final pendente de QA independente e aprovação do criador (`PENDING_CREATOR`). `runtimeImplemented: false`; nenhuma escrita em `../TacticsRPG`. Orc V4 permanece descartado.

Contrato e lições aplicadas: [`docs/ARTISTIC_QUALITY_GATES.md`](ARTISTIC_QUALITY_GATES.md) e [`config/artistic-quality-gates-v1.json`](../config/artistic-quality-gates-v1.json).

---

# Entrada natural de combate — revisão incremental atual

2026-10-25 · `main-orc-onehanded-entry-v1` · **candidato local, aprovação artística do criador pendente**.

Esta revisão parte do último polimento `onehanded-polish-v1`, preservado integralmente. O Orc é **orc-v1 / Verde Warcraft**; o equipamento ativo continua apontando para v3 até decisão explícita de seleção. Não restaurar o antigo Orc V4. O relatório do passe anterior permanece abaixo como histórico de continuidade.

## Diagnóstico confirmado

A espada começava com dois quadros baixos quase horizontais (270°), sem preparação corporal antes da aparição. Em seguida a mão saltava de world93,130 para98,89 (cerca de41,30px), com mudança de75° na lâmina. A sobreposição correta da luva não resolvia essa progressão anatômica. No machado, a carga projetada aparecia antes de um gesto claro de preparação do braço. São causas verificadas nos PNGs/perfis; os timestamps do vídeo citados no pedido são relato fornecido pelo criador, não uma nova gravação anexada e inspecionada nesta execução.

A auditoria do DEV está em `experiments/main-orc-entry-v1/dev-audit.md`. Classificação principal: repouso KEEP; início/entrada TRANSITION_FIX; preparação elevada TIMING_ONLY ou reutilização adaptada; extensão, passagem limpa, impacto e recuperação KEEP. Nenhum ataque inteiro foi regenerado.

## Correção proposta e fontes

Uma única pose de preparação foi produzida por **PixelLab Pro Flash inpaint** sobre o próprio neutro atual. Apenas braço direito (à esquerda da imagem), cotovelo, antebraço e mão fechada foram retocados. Rosto, pescoço, centro do peito, outro braço, quadril e pernas permanecem nos pixels próprios. No resultado real, o grip ficou em nativo37,67 / world101,131, em vez da coordenada aproximada solicitada ao gerador. A ligação usa a luva real, inspecionada, e não uma coordenada presumida.

A montagem e todos os retoques/tempos/exportações são no **Aseprite**, por Lua em batch oculto, perfil isolado e `--noinapp`. O resultado em nuvem não é desenho manual. Mestre da preparação: `experiments/main-orc-entry-v1/inputs/prepare-arm.aseprite`; corpo e dedos exportados no mesmo diretório. Fora da máscara foram removidos apenas dois pixels herdados abaixo da mão deslocada (world97,151 e98,151); todo o restante não mascarado foi preservado. Proveniência verificável em `prep-provenance.json`, máscara e scripts no experimento.

A entrada agora é **neutro sem arma → preparação corporal sem arma → mesma pose com pegada estabelecida → elevação do cotovelo/ombro → golpe**. Não é uma animação de sacar de bainha: não há bainha, arma carregada, magia ou sistema novo. A arma aparece somente depois da preparação, no mesmo corpo e grip, dentro do Attack. O primeiro quadro armado dura35ms; o preparo anterior,65ms.

Na espada, duas poses intermediárias deste mesmo Orc (Axe3/Axe4 do polimento, corpo/dedos exatos) ligam a nova preparação à guarda existente. A orientação progride315°→330°→340°→345°. O caminho de preparação da mão passa por distâncias aproximadas17,26px (neutro→preparo),18,38px,20,59px e11px. Isto descreve o espaçamento, sem provar por números que o movimento é natural. O golpe e a recuperação anteriores são mantidos, incluindo a limpeza do resíduo de lâmina.

No machado, a entrada usa300°→325°→350°, com as próprias poses de elevação/preparação. A antiga carga projetada foi removida da sequência, não redesenhada nem apagada do acervo. As poses, impacto e recuperação do machado continuam distintos da espada. Compartilhar uma preparação curta de braço deste indivíduo não cria um movimento de ataque universal.

| Clip | Antes (polimento) | Entrada candidata | Impacto artístico local |
|---|---:|---:|---|
| Espada |11 quadros /690ms|13 quadros /730ms|novo8, aos360ms (antes320ms)|
| Machado |12 quadros /1055ms|12 quadros /1005ms|novo6, aos410ms (antes460ms)|

Os holds de impacto continuam100/115ms. `appliesDamage:false`: nenhuma mudança de dano/eventos/turnos Unity. A espada acrescenta40ms para estabelecer a preparação; o machado reduz50ms ao retirar a carga redundante. A recuperação preserva o corpo idêntico na ocultação da arma e o retorno ao neutro sem overlay. Idle5/2200ms e Walk16/1280ms ficam exatos e sem arma.

Plano explícito e mapeamento de cada quadro: `experiments/main-orc-entry-v1/entry-plan.json`. Fontes candidatas: `characters/orc-v1/source/aseprite/onehanded-entry-v1/`; PNGs/camadas/perfis/clips: `characters/orc-v1/source/onehanded-entry-v1/`. Fork recuperável dos mestres anteriores: `characters/orc-v1/source/aseprite/main-orc-entry-v1/`. Não alterar o ponteiro ativo automaticamente.

## Reutilização, revisão e limites

Armas independentes, dimensões, grip local, PPU100, escala1 e ordem de oclusão permanecem. A própria categoria define o perfil; não se produz um corpo novo para cada espada/machado. Canvas256, corpo128 em64,64 e chão190, sem espelhamento, trim, suavização ou interpolação de preview. A inspeção de armas diferentes continua necessária para cabos/guardas incompatíveis; composição offline não implementa equipar no runtime.

Página isolada: `Biblioteca de Arte/Estudos Comparativos/Orc principal - Entrada de combate/index.html`. Compara **polimento anterior × entrada nova**, com PNGs/tempos reais, controles existentes, quadro a quadro, normal/lento, zoom, pegadas, impacto e sequência Idle→Attack→Idle. As páginas anteriores continuam preservadas.

A revisão integrada pelo QA Paseo é registrada separadamente em `experiments/main-orc-entry-v1/qa-final.md`; o pacote integrado e os resultados abaixo são congelados antes dessa revisão; o parecer final registra a versão exata revisada. O criador continua como autoridade artística. Somente front_r, sem teste no jogo, outras vistas ou propagação. A transferência de peso ampla continua limitada; o foco é a continuidade da entrada, não reconstruir a biomecânica.

### Resultado integrado e verificações deste passe

- Build `dist/editor/main-orc-onehanded-entry-v1/f600aa0675d5e5d3d093/`: **10 jobs,98 quadros exportados e comparados**. Reexportação dos mesmos mestres reutilizou o mesmo build.
- `root-safety-and-artifacts.json`: **9.923 arquivos de arte anteriores e9 metadados ativos preservados**, todos os corpos/dedos mapeados exatos, armas inalteradas, Idle/Walk exatos e visibilidade contígua.
- `entry-check.json`: verificação focada do DEV sem falhas. Passos de grip e ângulo são diagnósticos, nunca regras universais de arte ou aprovação.
- `preview-qa.json`: **69 quadros e recortes de grip comparados pixel a pixel**, zero divergências, nenhuma exceção JavaScript, abertura file:// e mobile390px sem overflow.
- `playback-capture.json`: todos os13 quadros da espada e12 do machado observados em reprodução real1× e0,25×, com capturas de canvas. `sequence-playback.json`: ambas as sequências Idle→Attack→Idle completadas no tempo real e terminando sem arma. A revisão usa essas capturas/poses; não é uma observação humana de jogo ou de vídeo contínuo.
- `test-suite.json`: `node --test --test-concurrency=1`, **14/14 PASS**. Doctor e editor-check disponíveis, Aseprite1.3.18.6. Nenhuma alteração em Unity.
- Fixtures de troca de arma: `reports/main-orc-entry-v1/reuse/{Sword|Axe}/reuse.json`,13/12 quadros recompostos com assets existentes menores, sem geração ou redesenho de corpo. São testes técnicos de reutilização, não novos itens aprovados.

Inspeção visual primária: a mão e o antebraço se preparam antes da aparição; a subida da espada possui caminho legível e direções progressivas, sem o salto baixo→guarda anterior. Os dedos próprios permanecem por cima do cabo. As boas poses de golpe/impacto/recuperação foram preservadas. Permanece uma troca discreta de visibilidade no limite da ação, por decisão de produto; não há efeito ou interpolação para escondê-la. A transferência ampla de peso e o apoio estático dos pés não foram refeitos.

Arquivos alterados neste passe: dois novos assemblers `tools/entry-main-orc.mjs` e `tools/aseprite/entry-main-orc.lua`, wrapper `experiments/main-orc-entry-v1/check-entry.py`, modo `--entry` no construtor existente, fontes/derivados isolados e ponteiro **somente candidato** `characters/orc-v1/source/equipment-entry-candidate.json`; notas curtas em AGENTS/handoff/roadmap, este capítulo e navegação da biblioteca. Estado inicial já sujo em `initial-git-status.txt`. O construtor já era não rastreado no Git: não há diff Git exato anterior dele; a revisão considera seu código final completo e os ramos legados. Nenhum commit/reset/clean.

Reprodução local sem nova cobrança:

```text
node tools/entry-main-orc.mjs build
node tools/entry-main-orc.mjs verify
node src/cli.mjs editor-export --manifest characters/orc-v1/source/aseprite/onehanded-entry-v1/editor.json
```

Com Python local: `experiments/main-orc-entry-v1/check-entry.py`, `tools/build-main-orc-rescue-review.py --entry` e `tools/build-art-library.py`. O plano e os PNGs de preparação são inputs congelados; estes comandos não chamam PixelLab. Auditoria de reaproveitamento em `reuse-assessment.json`; o runtime dinâmico continua como extensão futura fora do escopo.

Correção pós-QA (2026-10-25): apontada pela QA independente, a montagem do modo `--entry` não depende mais de o diretório histórico `Historico de Entregas/Orc V1 - Armas v2` já existir (a fonte `previous-review` só existe no workspace do resgate v3). A página recriada com o construtor corrigido ficou byte a byte idêntica à revisada; regressão executável em `test/preview-entry.test.mjs` e registro/evidência em `experiments/main-orc-entry-v1/preview-builder-fix.json`.

Orquestração: DEV gratuito DeepSeek V4.1 Flash via `opencode-free` no Paseo; integração/artes controladas pelo orquestrador; QA independente final GLM5.3 via `cline-glm-api`. Catálogo, IDs, resultados e uso verificável serão registrados no experimento. Só o fluxo de orquestração organiza QA, sem agentes adicionais solicitados pelo DEV.

Custo artístico: uma chamada Pro Flash, **6 gerações cobradas**, sem retentativa paga ou nova arma. Pedido e resultado em `prep-request.json` e `cloud-record.json`; job591a50b5-227a-4808-92c9-a86b0ec13e96. Não afirmar preço monetário ou tokens que o provedor não reportou. Nenhum commit, limpeza destrutiva ou escrita em `../TacticsRPG`.

---

# Orc principal — polimento dos ataques de uma mão

2026-10-25 · `main-orc-onehanded-polish-v1` · **candidato isolado, aprovação artística do criador pendente**.

O Orc principal é **orc-v1 / Verde Warcraft**. A correção anterior `main-orc-onehanded-v3` foi uma melhoria substancial e continua ativa; não é uma versão rejeitada. O antigo Orc V4 permanece descartado. Esta tarefa não altera o jogo, a seleção de produção, o Idle/Walk aprovado, a arte das armas ou outras direções.

## A. Antes e depois

A inspeção usou os mestres salvos e PNGs atuais, suas durações e capturas de reprodução. Nenhum vídeo novo foi anexado ao pedido de polimento; não atribuímos a ele observações de uma gravação indisponível. Auditoria por quadro, motivo, pegada e deslocamento: `experiments/main-orc-polish-v1/artistic-audit.json`. Índices neste relatório começam em **zero**.

| Arma | Problema principal | Alteração mínima aplicada | Preservação e limite |
|---|---|---|---|
| Espada | Recuperação retraía a mão cerca de49,25px em uma única troca; cadência mantinha poses de aceleração por tempo demais. | Tempos assimétricos; ponte entre o antigo5 e6 reutilizando o antigo Axe7 deste mesmo Orc. Retração passa por cerca de30,59px e19,03px; a arma continua separada, escala1. Um retoque mascarado no corpo do impacto. | Guarda, extensão, pose de recuperação e identidade mantidas. Na passagem do corte foi apagado um resíduo fino de lâmina herdado no corpo, após QA independente. Mudança de apoio corporal discreta; não se apresenta como uma nova animação corporal completa. |
| Machado | Release70ms e impacto70ms tinham ênfase semelhante; arma sumia durante o retorno do braço. | Release35ms, impacto115ms e antecipação deliberada. Retoque limitado em tronco/quadril/joelho no impacto. Ocultação em uma repetição do mesmo corpo antes do assentamento. | Machado, proporção, poses de elevação, preparação, extensão e seguimento preservados. Peso vem sobretudo da cadência e do compromisso existente da pose. |
| Ambas | Arma aparecia quando a mão já havia saído do repouso; desaparecimento coincidia com troca de corpo. | Breve quadro de pegada inicial no próprio corpo neutro; conclusão repete a recuperação sem overlay antes do retorno. | A entrada/saída continua sendo uma troca discreta, por decisão de armas somente no ataque. Não há sistema de sacar/embainhar ou transição invisível simulada. |

### Classificação de todos os quadros anteriores

| Quadro v3 | Sword | Axe |
|---:|---|---|
|0|KEEP|KEEP|
|1|TRANSITION_FIX|TRANSITION_FIX|
|2|TIMING_ONLY|TIMING_ONLY|
|3|TIMING_ONLY|TIMING_ONLY|
|4|MINOR_POLISH|TIMING_ONLY|
|5|MINOR_POLISH|MINOR_POLISH|
|6|TRANSITION_FIX|TIMING_ONLY|
|7|TRANSITION_FIX|MINOR_POLISH|
|8|—|TRANSITION_FIX|
|9|—|KEEP|

Não foi necessário classificar nenhuma pose como REWORK_POSE. A observação de MINOR_POLISH não obriga redesenhar: a recuperação Axe7 foi mantida; na passagem Sword4, a inspeção independente identificou e levou à remoção local de um resíduo de lâmina, sem alterar a pose. O teste inicial alterou **somente tempos**, com pixels idênticos, antes dos retoques. Seus mestres, exportação e captura estão em `experiments/main-orc-polish-v1/timing-only/`. Ele melhora o ritmo, mas não resolve a distância entre as poses da recuperação nem produz esforço corporal novo.

### Tempos e mapeamento finais

Espada anterior: 8 quadros / 775ms → candidato: 11 quadros / 690ms:

| Novo | Fonte do corpo | Fase | ms |
|---:|---|---|---:|
|0|Sword0|Repouso sem arma|40|
|1|Sword0, dedos traçados da própria luva|Estabelecer pegada|45|
|2|Sword1|Preparação|65|
|3|Sword2|Guarda elevada|100|
|4|Sword3|Avanço|35|
|5|Sword4, limpeza pontual de resíduo|Passagem do corte|35|
|6|Sword5 + retoque mascarado|Impacto/seguimento|100|
|7|Axe7, mesmo indivíduo atual|Ponte de recuperação|55|
|8|Sword6|Recuperação|80|
|9|Sword6, sem overlays|Conclusão|45|
|10|Sword7|Neutro exato|90|

Machado anterior: 10 quadros / 1130ms → candidato: 12 quadros / 1055ms:

| Novo | Fonte do corpo | Fase | ms |
|---:|---|---|---:|
|0|Axe0|Repouso sem arma|40|
|1|Axe0, dedos traçados da própria luva|Estabelecer pegada|50|
|2|Axe1|Preparação|100|
|3|Axe2|Elevação|80|
|4|Axe3|Ombro armado|155|
|5|Axe4|Descida|35|
|6|Axe5 + retoque mascarado|Impacto|115|
|7|Axe6|Seguimento|110|
|8|Axe7|Recuperação|130|
|9|Axe7, sem overlays|Conclusão|50|
|10|Axe8|Assentamento|90|
|11|Axe9|Neutro exato|100|

As três adições da espada são pegada inicial, ponte reutilizada e corpo repetido na conclusão. As duas do machado são pegada inicial e conclusão. Nenhum novo lote de animação foi gerado. Impacto artístico passa de430→320ms na espada e550→460ms no machado; ambos no novo quadro6. Isso é **proposta visual local**, `appliesDamage:false`, sem alteração em dano, turnos ou eventos Unity.

## B. Alterações técnicas e fontes

- Forks recuperáveis: `characters/orc-v1/source/aseprite/main-orc-polish-v1/`, feitos por `editor-fork` a partir dos dois mestres atuais.
- Mestres candidatos: `characters/orc-v1/source/aseprite/onehanded-polish-v1/`, com `sword-attack`, `sword-body`, `sword-hand-front` e equivalentes `axe`, todos `.aseprite`. Manifesto de exportação `editor.json` nesse diretório.
- PNGs, camadas, folhas, `clip.json` e `profile.json`: `characters/orc-v1/source/onehanded-polish-v1/{Sword|Axe}/Attack/`.
- Pacote de revisão: `characters/orc-v1/source/onehanded-polish-v1/manifest.json`; ponteiro **somente candidato** `characters/orc-v1/source/equipment-polish-candidate.json`.
- Build imutável: `dist/editor/main-orc-onehanded-polish-v1/3b6384933314a2bb64f9/`. Nova exportação dos mesmos mestres retornou o mesmo build, `reused:true`.
- Implementação incremental: `tools/polish-main-orc.mjs` e `tools/aseprite/polish-main-orc.lua`; compositor Lua e exportador já existentes reutilizados. `tools/compose-main-orc-item.mjs` ganhou um argumento opcional de perfil para testar candidatos; o padrão continua v3.
- O construtor existente `tools/build-main-orc-rescue-review.py` ganhou `--polish`, sem substituir o modo anterior ou criar outro aplicativo de preview.

Canvas256×256, corpo128×128 em64,64, chão190, PPU100, sem escala/espelhamento/trim/interpolação. Fontes corporais de início/fim são o **Idle0 atual**, não o conceito estático. Idle5 fases400/450/500/450/400ms e Walk16×80ms permanecem exatos.

A arte de Espada do Recruta e Machado de Milícia foi preservada integralmente. Pegadas locais do item continuam48,66 e36,55; escala1. A nova pegada inicial do corpo é98,148 no canvas256 (34,84 nativo). A ponte Sword7 usa grip129,148 e102°. Os demais encaixes e orientações herdados permanecem. A própria luva atual fornece a máscara de dedos; não há mão genérica girada ou transplante de outro personagem. Ordem `weaponBack → body → weaponFront → handFront`. Não se estende o machado sobre a perna neutra nem se inventa troca de profundidade para escondê-lo.

Arma visível somente em Attack1..8, intervalo único em ambas. Corpo idêntico antes/depois da aparição e ocultação. Repouso, Walk, inspeção, fim da ação e demais estados continuam sem overlay persistente. Nenhum novo clip Hit/Defeat foi produzido ou declarado validado nesta tarefa.

### Autoria e proveniência

Duas operações localizadas de **PixelLab Pro Flash inpaint**, fonte128×128 e máscara explícita, sem gerar personagens novos. Prompts/resultados completos e máscaras em `experiments/main-orc-polish-v1/`. Modelos, jobs e cobrança registrados nos arquivos `sword-cloud-record.json` e `axe-cloud-record.json`.

Além dos impactos, uma linha diagonal residual em fundo transparente no corpo do antigo Sword4/novo5 foi apagada via Lua no Aseprite (world x160..184,y99..121 e pixel isolado[181,93], total31 posições RGBA). Corpo, luva e arma real foram inspecionados separadamente. Essa correção não gerou custo e mantém o master v3 intacto. Evidências antes/depois: `crossing-residue-inspection.png` e `crossing-cleaned-inspection.png`.

Os resultados alteram 1411 posições RGBA no Sword5 e 1879 no Axe5, dentro da máscara. Cabeça, botas, mão e região ao redor do grip são protegidas e verificadas exatamente. O pedido buscou pequena compressão/participação de quadril, joelho e ombro; não se afirma uma translação rígida exata de2/3px. A alteração é sutil e inclui tratamento de clusters, não uma reconstrução anatômica. Os pixels aprovados fora da máscara são reaplicados por regra no próprio Aseprite, mesmo com a garantia do serviço.

Toda montagem, retoque, trace de dedos, alteração de duração, gravação de mestres e exportação ocorreu dentro do **Aseprite 1.3.18.6**, por Lua em batch oculto com perfil isolado e `--noinapp`. Não é desenho manual. Python/PIL foi usado somente para organização, hashes e folhas/capturas de QA, sem autoria raster externa. Nenhuma janela aberta ou trabalho não salvo do criador foi controlado.

## C. Revisão artística

Inspeção primária: poses reais, máscara/resultados de impacto, pegadas8× e capturas do preview1× e0,25×. A recuperação da espada distribui melhor a retração; a antecipação e o impacto do machado têm acentos diferentes. A alteração corporal é deliberadamente limitada, preservando as poses boas e o desenho atual. A ausência de deslocamento dos pés evita deslizamento novo; não comprova por si só transferência de peso convincente.

Revisão independente concluída por outro agente conforme autorização expressa do criador: `experiments/main-orc-polish-v1/independent-artistic-qa.md`. Confirmou melhora de ritmo, recuperação e transições; pegadas e identidade preservadas. Detectou o resíduo da espada e um pixel isolado em world[181,93], ambos removidos no Aseprite e reinspecionados. Não identificou bloqueio artístico significativo remanescente. Transferência de peso ainda é discreta: oportunidade subjetiva futura, sem alegar biomecânica totalmente resolvida. Playback independente 1×/0,25× e sequência completa foram vistos antes da limpeza; a reinspeção final foi localizada nos body/arma/composite sem cache. Aprovação técnica ou parecer do agente nunca equivale à aceitação artística do criador.

Limites de avaliação: somente front_r, fundo de inspeção, sem alvo ou contato em jogo. A rotação nearest-neighbor da arma e a ocultação discreta ainda podem ser perceptíveis em câmera lenta. Compatibilidade de itens precisa respeitar largura de cabo/guarda, proporção, câmera e mãos; o teste de substituição não aprova visualmente qualquer arma. Não se declara o conjunto final para todas as raças/classes ou pronto no runtime.

## D. Validação e custos

| Verificação | Resultado |
|---|---|
| Exportador Aseprite existente |10 jobs / 92 quadros comparados, PASS|
| Reexportação dos mestres salvos |Mesmo build imutável, PASS|
| Verificação focada de arte/metadados |105 verificações, PASS; `technical-qa.json`|
| Fontes anteriores |9.796 PNGs/mestres preservados por SHA256|
| Metadados ativos de corpo/armas |Exatos; candidato não substitui `equipment-current.json`|
| Preview real |62 quadros/canvas e recortes de grip comparados, zero diferenças|
| Sequência/completar sem loop |Antes/depois retornam ao Idle sem overlay, PASS|
| Abertura local e responsividade |file:// carrega; mobile390px sem overflow|
| Biblioteca |202 cópias por hash, 179 links locais, página v3 anterior intacta|
| Suite do projeto |`node --test --test-concurrency=1`:14/14 PASS|
| Substituição de itens existentes |Sword11 eAxe12 recompostos, zero redesenhos/gerações|
| Unity e outras direções |NOT_RUN, fora do escopo|

O teste de reutilização usa os assets menores v1 já existentes apenas como **fixtures técnicas**, não como proposta artística ou novas armas de produção. Evidências: `reports/main-orc-polish-v1/reuse/{Sword|Axe}/reuse.json`. O mesmo corpo, dedos e duração são reaproveitados ao trocar o item compatível da categoria.

Custos externos: **2 chamadas, 6 gerações efetivamente cobradas cada, total 12 gerações PixelLab**, sem novo lote ou retentativas pagas. Jobs `f077ce3b-656d-4a98-badf-4eff1045fe3b` e `5c4b8882-c612-4ddb-bc2c-2eb7ad646481`. Não foi obtido preço monetário por geração; não estimamos reais/dólares ou consumo de tokens não medido. Reaproveitamento e testes locais não chamam geração.

Evidências: `experiments/main-orc-polish-v1/{technical-qa,preview-qa,library-qa}.json`, `build.json`, capturas normal/lenta, fontes do estudo de tempo e pedido original `creator-task.md`.

## E. Materiais de revisão

Abra **`Biblioteca de Arte/Estudos Comparativos/Orc principal - Polimento de combate/index.html`**. A biblioteca principal também lista o candidato, preservando o link da base v3.

Na mesma página: Espada antes/depois, Machado antes/depois, modo somente ataques ou Idle→Attack→Idle, velocidades1×/0,5×/0,25×, pausar, avançar quadro, repetir/desligar loop, zoom nativo/2×/3×, pegada8× e galeria de poses/tempos. O contorno dourado identifica o impacto no canvas de revisão; não faz parte do PNG ou de um evento de dano. Não há suavização ou frames inventados no preview.

Fontes portáteis em `Ataques/{Espada|Machado}/`, comparação com a base em `Comparacao/Antes - {Espada|Machado}/`, armas independentes em `Armas/`. Cada ataque tem mestre composto, corpo, dedos, folha, clip e perfil. O original v3 continua em `Biblioteca de Arte/Personagens Jogaveis/Orc V1/index.html`.

## F. Segurança, Git e continuidade

Estado inicial já continha numerosas mudanças locais. Registro: `experiments/main-orc-polish-v1/initial-git-status.txt`; arte protegida e cópia portátil completa da base em `protected-art.json` e `baseline-review/`; metadados ativos em `baseline-metadata/`. Não houve reset, limpeza destrutiva, commit, push ou escrita em `../TacticsRPG`.

Escopo desta tarefa: novos mestres/exports isolados, estudo/QA local, ponteiro de candidato, extensão pequena do preview/compositor, este documento e notas em AGENTS, handoff, roadmap e registro da biblioteca. Mudanças anteriores em runtime/configuração/fábrica não foram revertidas nem atribuídas a este passe. O diff do repositório inteiro inclui trabalho anterior; não representa apenas esta tarefa.

Orc V1 mantém autoridade. Armas continuam independentes e a política é somente no ataque. Nenhum gate, receita de produção, seleção de equipamento, registro de personagem ou GUID Unity foi autoaprovado/substituído. Infante de Ferro permanece atual; Vigia/Matriarca seguem na categoria separada de ideias futuras para únicos jogáveis e/ou NPCs.

## G. Aceitação e próximo marco

- **Implementado:** polimento incremental dos dois ataques e preview comparativo.
- **Validado tecnicamente:** exportações, referências, duração, visibilidade, reutilização e preservação descritas acima.
- **Revisado visualmente:** evidências primárias e parecer independente concluído; resíduo corrigido e reinspecionado.
- **Aprovação artística do criador: PENDENTE.** Nenhuma promoção ou propagação automática.

Depois da avaliação do criador, registrar decisão explícita e só então considerar selecionar este candidato. Outras vistas e futura integração no jogo são tarefas separadas. Não recriar o sistema de equipamentos para resolver problemas locais de animação.

### Reproduzir sem gastar gerações

```text
node tools/polish-main-orc.mjs build
node src/cli.mjs editor-export --manifest characters/orc-v1/source/aseprite/onehanded-polish-v1/editor.json
node tools/compose-main-orc-item.mjs Sword experiments/orc-v1-weapons-v2/preserved-v1/weapons/recruit-sword/weapon.json reports/main-orc-polish-v1/reuse/Sword characters/orc-v1/source/onehanded-polish-v1/Sword/Attack/profile.json
node tools/compose-main-orc-item.mjs Axe experiments/orc-v1-weapons-v2/preserved-v1/weapons/militia-axe/weapon.json reports/main-orc-polish-v1/reuse/Axe characters/orc-v1/source/onehanded-polish-v1/Axe/Attack/profile.json
node --test --test-concurrency=1
```

Com Python local disponível: `experiments/main-orc-polish-v1/check-polish.py` valida os contratos; `tools/build-main-orc-rescue-review.py --polish` reconstrói a página a partir dos PNGs reais. `tools/build-art-library.py` atualiza a navegação. O modo `prepare` recria o estudo/inputs/solicitações, **não envia** chamadas pagas. As duas imagens de retoque já baixadas são os inputs congelados do modo build. Não rodar scripts antigos de promoção de V4/v1/v2.
