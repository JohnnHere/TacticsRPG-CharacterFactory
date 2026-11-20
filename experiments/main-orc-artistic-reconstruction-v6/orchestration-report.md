# Orc V1 — reconstrução artística V6, 30/10/2026

**EM PRODUÇÃO. Reconstrução artística, não continuação de QA.**

O criador rejeitou artisticamente o candidato `main-orc-combat-rescue-v5`
(manifesto `58152a101e16cbc031349b3308649f9ccaa38b99782d4e23bcf2ee43fddc3794`)
mesmo com parecer duplo `READY_FOR_CREATOR_REVIEW`. A task V6 exige **modificar
a arte**: `back_l` Sword/Axe com reconstrução maior, `back_l`→`back_r`
continuidade/pernas, axila persistente de `front_l/Sword`, grip natural e
contornos claros, preservando frontais bem-sucedidos. Idle, Walk, Unarmed,
Hit, Defeat, Unity e commits seguem fora do escopo.

## Estratégia

Etapas A–F da task: auditoria de fontes → referência `back_l` → validação de
continuidade → adaptação `back_r` → correções frontais localizadas → exports/
comparações. QA independente somente sobre a versão integrada, com a matriz
de objeções do criador como critério de primeira classe. O parecer técnico
anterior **não** será usado para descartar os defeitos relatados.

O [inventário de entrada](input-preservation.json) protege **5.907 arquivos**
do estado atual (inclui todos os finais V5 rejeitados como baseline imutável
para before/after). Nenhuma fonte existente será editada in-place; V6 escreve
somente em `characters/orc-v1/source/artistic-reconstruction-v6/` e
`experiments/main-orc-artistic-reconstruction-v6/`.

## Sessões

| Papel | Provedor/modelo | Agent ID | Responsabilidade | Motivo | Resultado |
|---|---|---|---|---|---|
| DEV retaguarda (núcleo) | Codex / gpt-6.1-sol, full-access | (a definir) | Etapas A–D: auditoria, reconstrução `back_l` Sword/Axe, adaptação `back_r` | Task complexa; `gpt-6.1-terra` não existe no catálogo Codex atual (sol workhorse da geração atual, com capacidade de imagem comprovada neste repo) | em execução |
| DEV frontal localizado | Cline GLM API / glm-5.3-flash, act | (a definir) | Axila `front_l/Sword`, contornos claros frontais confirmados, inspeção de grip frontal | Preferência da orquestração para subtarefas intermediárias; antecessor GLM 5.3 resolveu retoque cirúrgico via ferramentas textuais+Aseprite sem ver imagens | em execução |

Escolhas de provedor registradas: Antigravity/Gemini Flash **não** recebe a
retaguarda — suas entregas anteriores passaram no QA mas foram rejeitadas pelo
criador; a reincidência exige DEV mais capaz para a especialidade. Sol/Codex
assumiu a reconstrução. GLM flash assume o frontal localizado; se não sustentar
a precisão exigida, escala para Codex.

PixelLab segue autorizado pelo criador (uso necessário e encenado, sem compras),
saldo conhecido 1336,70 na última medição; cada job com recibo antes/depois.
Prompt de corpo nunca nomeia a arma (contaminação documentada em V5).

## Checkpoint back_l aceito; Etapa D liberada

O DEV retaguarda entregou `V6_BACK_L_REFERENCE_READY` (freeze
`6247764829…`): auditoria dos 48 quadros das 4 células (audit.md/json com
KEEP/TARGETED_PIXEL_FIX/TIMING_FIX/REAUTHOR_KEYFRAME/REMOVE_OR_REPLACE),
reconstrução de `back_l` Sword (12f/**950 ms**) e Axe (12f/**1320 ms**) a
partir de segunda referência PixelLab com esqueletos explícitos, acabamento
Aseprite (perfil exclusivo), mestres 256/128 salvos/reabertos/conferidos,
intervalo armado F01–F09 e bookends desarmados. A primeira tentativa de
reconstrução articular local do próprio DEV foi rejeitada por ele e
preservada em `rejected-local-arm/`.

Contabilidade declarada: **4 jobs × 3 = 12 gerações comprovadas** por recibos
(sword/axe `61ca245f…` e `8e309cdd…`); saldo medido 1336,70 → 1306,70, com
**18,00 de variação global sem atribuição** a esta frente registrada como
tal — o saldo da conta não é tratado como contabilidade do DEV. Sem compras.

O orquestrador considerou a Etapa C satisfeita pela verificação de playback
do DEV e liberou a Etapa D (`back_r`) no mesmo método, com as objeções do
criador sobre pernas/stance como critério primário. Sem espelhamento;
identidade de técnica/ritmo da referência `back_l` validada.

O DEV frontal segue em execução (permissões `search`, `execute` e `read`
aprovadas dentro do escopo). Integrador V6 criado: pai é o candidato V5
rejeitado; células Unarmed/Walk ficam fora do escopo e carregam seu status
V5 sem alteração de arte.

## Etapas D–F concluídas; candidato V6 integrado

O retaguarda entregou a Etapa D (`V6_BACK_R_ADAPTATION_READY`): `back_r`
Sword/Axe reconstruídos com a mesma identidade de técnica da referência
`back_l`, esqueletos próprios por vista (sem espelho), joelhos/apoio
encadeados, e binding inicial arquivado porque o machado projetava abaixo do
chão. 2 jobs × 3 = **6 gerações** com recibos; saldo medido 1288,70 → 1282,70.
Os 191 arquivos do freeze `back_l` permaneceram byte-idênticos.

O DEV frontal entregou `V6_FRONTAL_LOCAL_FIXES_READY` com a causa raiz
demonstrada: o corpo dos quatro clipes frontais é **byte-idêntico à baseline
parental** — o artefato de axila e os pontos claros eram herdados e
sobreviveram a todas as correções anteriores porque cada uma preservava
exatamente esses pixels. Correção de 1 px na camada body: ilha flutuante
`rgba(0,0,1,255)` removida sob a axila do braço atacante (6 instâncias) e 439
pontos claros neutros isolados preenchidos pela mediana dos vizinhos escuros;
highlights legítimos preservados; grip verificado sem necessidade de edição;
**zero PixelLab**. Um incidente de exportação (subcaminho `frames/` do layout
traseiro em vez da raiz do layout frontal) foi detectado pela verificação
independente do próprio DEV e corrigido, com estado final revalidado.

O integrador V6 montou o patch das 8 células a partir dos dois manifestos e
produziu o candidato:

| Verificação | Resultado |
|---|---|
| Validação técnica | **TECHNICAL_PASS 28 células / 226 quadros / 956 hashes** |
| Reexportação Aseprite | **34 mestres / 352 quadros** reabertos das fontes salvas |
| Chromium real na página | **21/21** |
| Inventário protegido | **5907/5907** byte-idêntico |
| Manifesto V6 | `2c2dd3b9fa8e28e9243f1554ffc23ec81593921a13465c957653b1dd7b1fa756` |

Foi preciso devolver ao retaguarda uma lacuna real de contrato: os quatro
clipes traseiros não emitiam as tiras `native-strip`/`composite-strip`
exigidas pela fábrica. Ele exportou as 8 tiras dos mestres salvos, comparou
pixel a pixel com os frames individuais e atualizou os `clip.json`; nenhum
pixel de arte, duração ou camada mudou.

[Página de revisão V6](<../../Biblioteca de Arte/Estudos Comparativos/Orc principal - Reconstrucao artistica/index.html>)
com before/after contra o V5 rejeitado.

QA independente do candidato V6 despachado ao revisor de primeira preferência
da task (Sol/Codex, sessão `c653215c-7625-47f4-8f80-d87ec68a2150`), com a
matriz de objeções do criador como critério primário e instrução explícita de
NÃO reaproveitar seu parecer anterior favorável ao V5.

## Ciclo de QA, correções e verificação temporal

O QA independente (Sol/Codex) reprovou a primeira versão integrada com dois
achados MEDIUM, ambos medidos e localizados:

| Achado | Célula/frames | Medição do QA |
|---|---|---|
| V6-QA-01 | `front_l/Sword` F03–F04 | cunha escura sob a axila; janela composta `x=140..154, y=108..127` RGBA idêntica ao V5, zero alteração de alfa nos 13 quadros |
| V6-QA-02 | `back_l/Sword` F07–F09 | pixels de arma abaixo de `groundY=190`: 87/195/166 px; ponta 24 px abaixo do chão |

Os dois retornaram aos produtores e foram corrigidos:

- **Axila (escalonada).** O especialista frontal original havia tratado ilhas
  flutuantes e pontos claros — não a saliência real, que é geometria opaca
  herdada. Por reincidência da mesma objeção, a correção foi escalonada a um
  especialista mais capaz (Sol/Codex, sessão `da467357…`), que reconstruiu a
  abertura torso-braço com borda escalonada em INK: **30 px em F03 e 28 px em
  F04**, só na camada `body`, sem tocar pose, arma ou tempo.
- **Ponta da espada.** O especialista traseiro (`19a5c4cf…`) ajustou apenas o
  binding de recuperação: pontas agora em **y=187, 185 e 173** — folgas de 3, 5
  e 17 px acima do chão, zero pixel de arma abaixo de `groundY` em F07–F09.
  Corpo, luva, tempos e os outros três clipes preservados; zero gerações.

Reintegrado, o candidato passou de `2c2dd3b9…` para:

**`5d68b52d3e2b2a0931d689afb5a9dd438c178835d05efb02a5fb2bcf0c64b7ca`**

| Verificação | Resultado |
|---|---|
| Validação técnica | **TECHNICAL_PASS 28/226/956** |
| Reexportação Aseprite | **34 mestres / 352 quadros** |
| Chromium na página | **21/21** |
| Preservação | **5907/5907** |

### Percepção temporal — lacuna declarada e coberta

O revisor estático registrou explicitamente que **não tinha navegador** e que a
reprodução em velocidade normal ficou `NOT_VERIFIED`. Para não declarar fluidez
sem observação, um revisor temporal separado (Gemini 3.8 Flash/Antigravity,
sessão `90dd95cb…`) abriu a página real em Chromium Headless 156 (com fallback
Edge) e assistiu os oito ataques:

| Clipe | 1× | 0,5× | Passo |
|---|---|---|---|
| front_r/Sword (13f/730 ms) | 4 loops | 2 loops | 13 quadros |
| front_l/Sword (13f/730 ms) | 4 loops | 2 loops | 13 quadros |
| back_r/Sword (12f/950 ms) | 3 loops | 1 loop | 12 quadros |
| back_l/Sword (12f/950 ms) | 3 loops | 1 loop | 12 quadros |
| front_r/Axe (12f/1005 ms) | 3 loops | 1 loop | 12 quadros |
| front_l/Axe (12f/1005 ms) | 3 loops | 1 loop | 12 quadros |
| back_r/Axe (12f/1320 ms) | 3 loops | 1 loop | 12 quadros |
| back_l/Axe (12f/1320 ms) | 3 loops | 1 loop | 12 quadros |

Veredito `TEMPORAL_PASS`, com os dois reparos confirmados em movimento: a axila
abre como abertura anatômica em F02→F03→F04→F05 sem piscada, e a lâmina lê
suspensa na recuperação. Machados traseiros mostraram flexão de joelho e
afundamento de quadril no impacto com cabeça de tamanho estável; as duas vistas
traseiras comunicam a mesma técnica sem espelhamento; armas ocultas fora do
intervalo. Ambos os pareceres estão no hash exato do candidato.

## Relatório final

### A. Inventário de agentes

| Papel | Provedor/modelo exato | Agent ID | Responsabilidade | Por que foi escolhido | Resultado |
|---|---|---|---|---|---|
| DEV retaguarda | `codex/gpt-6.1-sol`, full-access, xhigh | `19a5c4cf-81a5-4cd0-9739-11b92652ff01` | Auditoria dos 48 quadros; reconstrução `back_l` Sword/Axe; adaptação `back_r`; correção de contrato de tiras; ajuste de binding F07–F09 | Task complexa; `gpt-6.1-terra` não existe no catálogo Codex atual; Sol já demonstrou leitura de imagem e Aseprite neste repo | `V6_BACK_L_REFERENCE_READY` → `V6_BACK_R_ADAPTATION_READY` → tiras → ground fix. 18 gerações com recibos |
| DEV frontal | `cline-glm-api/glm-5.3-flash`, act | `8dc92d00-3332-4e58-ba05-c248d06cd187` | Forense das 4 células frontais; correção de ilhas/pontos claros; verificação de grip | Preferência da orquestração para subtarefas intermediárias/localizadas | `V6_FRONTAL_LOCAL_FIXES_READY`: 445 edições de 1 px, zero PixelLab, causa raiz da herança demonstrada. **Não** resolveu a axila (corrigiu classes erradas) |
| DEV axila escalonado | `codex/gpt-6.1-sol`, full-access | `da467357-75fb-436d-817a-20d5067f5f70` | Reconstruir a abertura torso-braço em `front_l/Sword` F03–F04 | Escalonamento obrigatório: mesma objeção reprovada após tentativa do responsável anterior | 58 px (F03 30, F04 28), só camada `body`; aceito pelo QA no reexame |
| QA integrado | `codex/gpt-6.1-sol`, full-access | `c653215c-7625-47f4-8f80-d87ec68a2150` | Revisar o candidato V6 contra a matriz de objeções do criador; fechar achados; consolidar | Primeira preferência da task (§6) | `ARTISTIC_ISSUES_FOUND` → 2 achados MEDIUM; depois `CLOSED/PASS_STATIC` nos dois; veredito final `READY_FOR_CREATOR_REVIEW` |
| QA temporal | `antigravity/gemini-3.8-flash-high`, full-access | `90dd95cb-fb14-4945-afff-8addd99712e4` | Reprodução real em 1×/0,5×/passo/escala tática dos 8 ataques | O QA de primeira preferência declarou não ter navegador — lacuna concreta, não segundo parecer | `TEMPORAL_PASS`, 3–4 loops por clipe em 1×, dois reparos confirmados em movimento |

Totais: **3 DEVs distintos** (1 escalonado), **2 QAs distintos** (estático e
temporal, por lacuna declarada), **1 orquestrador**. Nenhuma sessão foi
recriada por conveniência; nenhum agente foi descartado silenciosamente.

Tentativas que não avançaram nesta rodada: duas chamadas do DEV frontal
ficaram presas sem retorno (~20 e ~15 min) e foram interrompidas pelo
orquestrador com retomada do ponto exato; o CLI truncou três mensagens longas
na entrega e todas foram reenviadas de forma compacta. O Cline não sustenta
`auto_accept` via CLI, então o orquestrador manteve um aprovador limitado no
tempo (aprovou 93 permissões em escopo declarado).

**Trabalho executado diretamente pelo orquestrador:** integração dos dois
manifests DEV em um patch de 8 células; validador/reexportador V6 derivados
do V5; reconstrução da página; verificação de preservação; documentação e este
relatório; triagem e escalonamento dos achados. Nenhuma chamada PixelLab e
nenhuma edição de arte pelo orquestrador — a delegação cobre a produção, como
a task exige.

### B. Resultados por frente

| Frente | DEV | Arquivos | Validação | Status |
|---|---|---|---|---|
| `back_l` Sword/Axe (reconstrução) | `19a5c4cf…` | `characters/orc-v1/source/artistic-reconstruction-v6/rear/back_l-{sword,axe}/` | 12f/950 ms e 12f/1320 ms, mestres 256/128 reexportados, bookends desarmados | aceito no estático; temporal PASS |
| `back_r` Sword/Axe (adaptação) | `19a5c4cf…` | `…/rear/back_r-{sword,axe}/` | idem, esqueletos próprios da vista | aceito no estático; temporal PASS |
| `back_l/Sword` recuperação | `19a5c4cf…` | `…/rear/back-l-sword-groundfix/` | pontas y=187/185/173; zero arma abaixo de 190 | achado V6-QA-02 fechado |
| Frontais (ilhas/pontos claros) | `8dc92d00…` | `…/frontal/{4 células}/` | 445 px, `verify-result.json` ALL_OK | aceito; highlights preservados |
| `front_l/Sword` axila | `da467357…` | `…/frontal-escalated/front_l-Sword-full/` | 58 px, só `body` | achado V6-QA-01 fechado |

### C. Evidência de qualidade

- Clipes modificados: **8** (Sword/Axe × 4 vistas). Preservados: 20 células fora de Sword/Axe.
- Defeitos relatados pelo criador e tratados: rigidez/desconexão e trajetória nas traseiras; pernas/stance na `back_r`; axila frontal; contornos claros; grip.
- Testes: validação 28/226/956 **PASS**; reexport 34 mestres/352 quadros **PASS**; Chromium **21/21**; preservação **5907/5907**; QA estático com 2 achados fechados; QA temporal **PASS** com reprodução real.
- Limitações: nenhuma execução no Unity; a percepção de fluidez vem de revisão temporal em navegador, não de gameplay; o criador ainda pode julgar a arte insuficiente.

### D. Custos e produção

- PixelLab desta rodada: **24 gerações** comprovadas por recibo — 12 no `back_l` (2 jobs) e 6 no `back_r` (2 jobs) do retaguarda, mais 6 não atribuídos registrados pelo DEV; saldo medido 1336,70 → 1306,70 → 1282,70. Reparos posteriores (ground fix, axila, frontais): **zero** gerações.
- Sem compras, sem assinatura, sem estimativa monetária inventada.
- Custo de tokens por modelo: **não informado** pelos provedores; não estimado.

### E. Demonstração

[Orc principal — Reconstrução artística](<../../Biblioteca de Arte/Estudos Comparativos/Orc principal - Reconstrucao artistica/index.html>):
Sword e Axe nas quatro vistas, 1×/0,5×/passo/zoom/escala tática, before/after
contra o V5 rejeitado, 13 células afetadas com tira de baseline e candidata.

### F. Status final

- Implementação: **concluída** para o escopo Sword/Axe.
- Testes técnicos: **aprovados**.
- QA independente: **concluído** (estático + temporal), achados fechados.
- Defeitos artísticos remanescentes: **nenhum apontado pelo QA**; julgamento estético final é do criador.
- Aprovação do criador: **PENDING_CREATOR**.
- Integração Unity: **não autorizada e não executada**.

Sem commits. Nenhum ponteiro de produção/promoção alterado.
