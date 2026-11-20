# Portões de qualidade artística — contrato canônico

2026-10-25 · contrato `factory.artistic-quality-gates.v1` · machine-readable em [`config/artistic-quality-gates-v1.json`](../config/artistic-quality-gates-v1.json) · aplicado ao passe `main-orc-complete-v1` do **Orc V1 / Verde Warcraft** (`characters/orc-v1/`).

Este documento existe para impedir um erro específico e já cometido: tratar um pacote **tecnicamente completo** como se fosse **arte aprovada**. A biblioteca completa do Orc principal passou por validação, exportação e QA com zero falhas técnicas e ainda assim continha vistas traseiras construídas por cima do rosto frontal, uma reação `Hit` da amplitude da respiração e um `Defeat` que achatava o corpo em uma tira horizontal. Nada disso era detectável por hash, canvas ou contagem de quadros.

Regra central: **completude técnica é condição de entrada, não veredito artístico.** Quem aprova arte é o criador.

---

## 1. Taxonomia de status

Todo pacote apresentado a alguém precisa carregar **um** destes quatro status. Não existe "pronto" fora desta lista.

| Status | Significado | Quem pode atribuir |
|---|---|---|
| `TECHNICALLY_COMPLETE` | Dimensões, `groundY`, alpha binário, hashes, mestres `.aseprite` e contagem de quadros passam nas checagens automáticas. | Validação automática, ferramentas de auditoria, DEV |
| `VISUAL_REVIEW_REQUIRED` | Tecnicamente completo **e** sem defeitos conhecidos pelos gates abaixo; aguarda inspeção visual humana no estúdio interativo. | DEV após os gates passarem; orquestrador |
| `ARTISTIC_REVISION_REQUIRED` | Criador ou QA visual identificou defeito de anatomia, perspectiva, silhueta, coreografia ou limpeza de pixels que exige revisão. | Criador, QA visual independente, ou DEV com evidência medida |
| `CREATOR_APPROVED` | Aprovação artística explícita do criador, após inspeção visual. | **Somente o criador** |

**Como ler os status.** Há duas coisas diferentes em jogo: uma **progressão** e um **bloqueio**.

Progressão normal, cada degrau exigindo o anterior: `TECHNICALLY_COMPLETE` → `VISUAL_REVIEW_REQUIRED` → `CREATOR_APPROVED`.

Bloqueio: `ARTISTIC_REVISION_REQUIRED` sobrepõe qualquer outro rótulo enquanto o defeito estiver aberto. Um pacote nunca pode ser exibido como "em revisão visual" — e muito menos como aprovado — enquanto se sabe que há anatomia, perspectiva, silhueta ou coreografia erradas.

Duas consequências diretas:

1. Um defeito artístico conhecido rebaixa o pacote mesmo que todo o resto esteja perfeito. Não se exibe como "em revisão" algo que já se sabe estar errado.
2. `CREATOR_APPROVED` não é um estado inicial nem um selo que acompanha o pacote para sempre: vale para a versão revisada, com data e escopo registrados. Qualquer novo pixel exige nova decisão.

Rótulos proibidos: `READY`, `DONE` e `APPROVED` sem um status desta taxonomia. Aprovação vinda de ferramenta, de contagem de arquivos ou de agente não é aprovação artística.

Fluxo:

```
TECHNICAL_GATE (validate / exportAseprite / hashes / matriz de cobertura)
        ↓
ARTISTIC_DEFECT_GATES (vista direcional · coreografia · conjunto completo)
        ↓
VISUAL_REVIEW (criador abre o estúdio)
        ↓
CREATOR_APPROVED (declaração explícita, registrada)
```

---

## 2. Gate de vista direcional (`directionalViewGate`)

Aplica-se a `back_r` e `back_l`.

**Princípio:** vista traseira é construção, não repintura. Derivar um fundo pintando por cima do rosto de um sprite frontal é proibido — se crânio, nuca e armadura dorsal não foram reconstruídos, a vista falha, por mais polida que esteja a superfície.

Marcadores obrigatórios, todos identificáveis pelo menos nos quadros de `Idle` daquela vista:

- crânio occipital sem rosto, sobrancelha, nariz, boca, presas ou órbitas;
- nuca e trapézio visíveis entre crânio e gola;
- gola/gorjal alta traseira, aberta para as costas;
- costas com placa dorsal, canal vertebral central e placas escapulares no lugar das peitorais e das cicatrizes de peito;
- fecho de cinto/faixa nas costas, **sem** o pico esternal frontal;
- **sem** ponta abdominal frontal;
- tassets divididos na traseira e cota de malha caindo atrás;
- tiras poplíteas e grevas de panturrilha;
- **sem** poleyns frontais de joelho;
- calcanhares e bicos das botas angulados para longe do observador.

**Distinção entre as duas vistas.** `back_r` olha para Nordeste, `back_l` para Noroeste. Elas precisam diferir em perspectiva de três quartos, em oclusão de ombro (qual pauldron está à frente) e na luz vinda de cima-esquerda. Um espelho puro não serve: ele troca a fonte de luz para cima-direita e inverte o ombro próximo, coisas que a câmera e a luz não fazem.

Checagens objetivas:

| Checagem | Critério |
|---|---|
| Rosto frontal | zero pixels da paleta frontal (olhos, presas, boca) na região da cabeça |
| Marcadores | cada item da lista acima localizável na vista |
| Dependência de espelho | `back_r` × `back_l` espelhado com mais de 97% de concordância indica cópia espelhada, não vista construída |
| Lado da luz | centróide de brilho acima do centróide do corpo e no mesmo lado nos quatro sentidos |

---

## 3. Gate de coreografia (`choreographyGate`)

**Princípio:** a ação precisa comunicar seu significado em silhueta e tempo, não apenas em sombreamento. Mudar 6% dos pixels não é mudar o movimento.

### 3.1 `Hit` — reação de impacto

Leitura exigida: reação clara de impacto em corpo pesado e blindado.

- componentes obrigatórios: snapping de cabeça, encolhimento de ombro ou braço em guarda, recuo de tronco, compressão de joelho ancorada em `groundY`;
- proibido: tremor de 1-2 px apresentado como reação de dano; movimento de respiração vendido como impacto;
- 5 fases: `impact-onset` (45 ms), `peak-recoil` (95 ms), `stagger-brace` (115 ms), `recovery-rise` (95 ms), `recovery-settle` (100 ms) — 450 ms, sem loop.

Pisos mensuráveis:

| Métrica | Piso |
|---|---|
| Excursão do topo da cabeça | ≥ 6 px |
| Deslocamento do centróide | ≥ 4 px |
| Compressão de altura (quadro mais baixo) | ≥ 5 px |
| Base do corpo | presa em `groundY` em todos os quadros |
| Energia de movimento vs `Idle` | ≥ 2,0× |

Energia de movimento é a porcentagem de pixels alterados entre quadros nas faixas de tronco e cabeça, dividida pela mesma medida no `Idle` da mesma direção. É um teste barato que separa reação de respiração.

### 3.2 `Defeat` — colapso

Leitura exigida: colapso físico crível em múltiplos estágios.

- estágios: `fatal-stagger` (70 ms) → `knees-buckle` (95 ms) → `drop-to-knees` (115 ms) → `collapse-impact` (130 ms) → `terminal-defeated` (290 ms) — 700 ms, quadro terminal 4;
- **proibido**: rotação 2D global do sprite em pé combinada com achatamento vertical (por exemplo `vScale = 0.52`). Um corpo em pé esmagado não é um corpo caindo;
- volume preservado: cabeça, pauldron e peito continuam legíveis no chão; silhueta reduzida a uma tira horizontal falha.

| Métrica | Critério |
|---|---|
| Base | presa em `groundY` em todos os quadros |
| Proporção terminal largura/altura | ≥ 1,3 |
| Crescimento de largura no terminal | ≥ 10% sobre o quadro em pé |
| Queda de altura em uma única transição | ≤ 35% da altura em pé |

### 3.3 Cabeça nos ataques frontais (`Unarmed`, `Sword`, `Axe`)

- contorno escuro em `INK` `rgb(12, 15, 18)` / `#0C0F12` ao redor da coroa;
- borda de pele verde coerente com a paleta por dentro do contorno;
- **zero** pixels de halo cinza-claro ou branco anti-aliased ao redor da coroa;
- trajetória do topo da cabeça estabilizada: pode subir e descer com a ação, mas reversão isolada acima de 5 px indica tremor, não intenção.

| Métrica | Critério |
|---|---|
| Pixels quase brancos (`min(R,G,B) ≥ 235`, alpha > 0) na faixa da cabeça | 0 |
| Reversão consecutiva máxima do topo da cabeça | ≤ 5 px |

---

## 4. Contrato de revisão do conjunto completo (`completeSetReviewContract`)

**Princípio:** o conjunto se revisa como conjunto. Uma direção bonita não sustenta uma biblioteca.

Matriz obrigatória: 4 direções (`front_r`, `front_l`, `back_r`, `back_l`) × 7 ações (`Idle`, `Walk`, `Unarmed`, `Sword Attack`, `Axe Attack`, `Hit`, `Defeat`) = **28 células**.

O estúdio de revisão precisa oferecer, em uma única página:

- as 28 células alcançáveis em um clique;
- avanço quadro a quadro, reprodução, velocidade e zoom sem sair da página;
- comparação **antes/depois** de toda ação revisada;
- transições `Idle → Attack → Idle`, `Walk → Idle`, `Hit → Idle` e `Defeat → pose terminal`;
- nenhuma suavização, nenhum quadro inventado, nenhuma interpolação no preview.

### 4.1 Integridade do antes/depois

Uma comparação antes/depois só vale se o "antes" vier do build substituído ou dos quadros arquivados antes da revisão. **Se a imagem "antes" for byte-idêntica à saída atual, a captura aconteceu depois da reescrita e a comparação é inválida.** Capture o estado anterior antes de tocar nos pixels e confirme que os hashes diferem.

Os snapshots preservados em `experiments/main-orc-complete-v1/rejected-before/` foram capturados a partir do build substituído `dist/editor/orc-v1-complete-v1/2595e12a39cc29670933` antes da re-autoria artística e possuem hashes SHA-256 distintos da saída atual (`b178422e1f7fc19f068c`).

### 4.2 Deveres do revisor

Inspecionar anatomia, perspectiva, silhueta, limpeza de clusters e movimento. Todo defeito registrado precisa nomear **ação, direção e faixa de quadros**. Contagem de arquivos, esquema JSON e hash **não** são evidência artística.

---

## 5. Como aplicar, na prática

Ordem para qualquer personagem novo ou revisão:

1. `node src/cli.mjs validate --id <id> --stage full` — portão técnico. `FAIL` bloqueia.
2. Gates artísticos desta página, por ação e por direção, com registro do que foi medido.
3. Estúdio de revisão atualizado com a matriz completa e o antes/depois válido.
4. Inspeção visual do criador.
5. Declaração explícita do criador, registrada com data, escopo e evidência.

Comandos locais úteis (nenhum deles aprova arte):

```powershell
node src/cli.mjs validate --id orc-v1 --stage full
node tools/audit-main-orc-complete-animation.mjs --current
node --test --test-concurrency=1
node src/cli.mjs editor-export --manifest characters/orc-v1/source/aseprite/complete-v1/editor.json
```

---

## 6. Estado medido do `main-orc-complete-v1`

Build de referência `dist/editor/orc-v1-complete-v1/b178422e1f7fc19f068c`; anterior substituído `…/2595e12a39cc29670933`. Medições sobre os sprites nativos e compostos reconstruídos em 2026-10-25, por silhueta (bbox/centróide), diferença de pixels por quadro e comparação antes/depois. São dados técnicos de portão: não substituem o julgamento artístico do criador.

| Item | Antes (`2595e12a39cc29670933`) | Depois (`b178422e1f7fc19f068c`) | Leitura |
|---|---|---|---|
| `Defeat` terminal (`front_r` / `back_r`) | altura 112 → **21 px**, largura 82 → 109 (squash vertical) | `front_r`: alturas `112/90/86/63/66 px`, larguras `87..120 px` (`aspect = 1,82`); `back_r`: alturas `111/91/84/67/66 px`, larguras `90..119 px` (`aspect = 1,80`) | achatamento virou colapso progressivo em 5 estágios com volume 3D preservado |
| `Hit` topo da cabeça (excursão) | 3 px de excursão | **12 px** (`front_r`/`front_l`/`back_l`) a **13 px** (`back_r`) | supera o piso de 6 px com snap de cabeça e guarda |
| `Hit` compressão de altura | 3 px | **12 px** (`front_r`/`front_l`/`back_l`) a **13 px** (`back_r`) | supera o piso de 5 px |
| `Hit` deslocamento de centróide | 2,0 px | **5,74 px** (`front_r`/`front_l`) a **7,55 px** (`back_r`/`back_l`) | supera o piso de 4,0 px |
| Pixels claros/halo no contorno da cabeça dos ataques frontais | halo cinza-claro no domo verde (`Sword`/`Axe`/`Unarmed`) | **0 em todas as 8 combinações** (contorno escuro `#0C0F12` + pele verde) | halo removido cirurgicamente |
| Vistas traseiras (`back_r` / `back_l`) | frente com rosto apagado | bases e 14 clipes traseiros reconstruídos com nuca/occipital, colar elevado, placa dorsal, faixa carmesim horizontal traseira, cota de malha e grevas traseiras | reconstrução anatômica traseira efetiva |
| `front_r` Idle / Walk / coreografia Sword & Axe | aprovados pelo criador | preservados em ritmo, sincronia de arma e identidade; apenas limpeza cirúrgica do contorno da cabeça nos ataques | preservação do que já funcionava |

Status resultante: conjunto em `technicalStatus: TECHNICALLY_COMPLETE`, `artisticStatus: VISUAL_REVIEW_REQUIRED`, `artisticApproval: PENDING_CREATOR`.

Itens abertos para inspeção visual explícita do criador nos estúdios interativos:

1. Confirmar visualmente se a leitura 3/4 de costas (`back_r` NE e `back_l` NW) em repouso, marcha (`Walk`), ataques (`Unarmed`, `Sword`, `Axe`), `Hit` e `Defeat` atende ao padrão artístico desejado.
2. Confirmar se a nova reação `Hit` (recuo pesado com guarda de manopla) e o colapso `Defeat` em 5 estágios têm o peso dramático esperado para o jogo.
3. Confirmar a limpeza do contorno da cabeça nos ataques frontais (`front_r` / `front_l`).

---

## 14. As 10 lições obrigatórias de produção

Seções 7 a 13 estão reservadas para gates futuros (overlay de arma, VFX, cenário, terreno). Esta seção mantém o número 14 porque é assim que ela é referenciada em `AGENTS.md`, `handoff/AGENT_CONTEXT.md` e no bloco `productionLessons` do contrato JSON.

Valem para qualquer personagem, raça, Job ou variante desta fábrica. Cada lição traz o padrão a repetir e o atalho a nunca repetir.

### Lesson 1 — Completude técnica não é aprovação artística

Hashes, canvas, `groundY`, alpha, contagem de quadros e testes verdes provam presença e consistência. Não provam que a arte comunica.
*Nunca:* declarar um conjunto pronto porque a validação retornou 0 `FAIL`.

### Lesson 2 — Vista traseira exige construção realmente traseira

`back_r` e `back_l` são desenhados a partir do crânio, da nuca, da armadura dorsal traseira e do cinto traseiro. Pintar por cima do rosto de um sprite frontal é proibido.
*Nunca:* apagar olhos e presas de um quadro frontal e chamar o resultado de vista de costas.

### Lesson 3 — A coerência direcional vale para o conjunto inteiro

`Idle`, `Walk`, `Unarmed`, `Sword`, `Axe`, `Hit` e `Defeat` precisam concordar em anatomia, perspectiva, luz e construção de armadura nas quatro direções.
*Nunca:* um `Idle` traseiro correto seguido de ataques cuja placa dorsal volta a ser peitoral frontal.

### Lesson 4 — `Hit` precisa comunicar recuo de impacto

Snapping de cabeça, encolhimento de ombro, recuo de tronco e compressão de joelho, mensuravelmente acima da respiração do `Idle`.
*Nunca:* um tremor de 1-2 px com a mesma energia de movimento do `Idle` rotulado como reação de dano. Este é exatamente o defeito medido no passe atual.

### Lesson 5 — `Defeat` é colapso coreografado em múltiplos estágios

`fatal-stagger` → `knees-buckle` → `drop-to-knees` → `collapse-impact` → `terminal-defeated`, preservando volume de cabeça, pauldron e peito sobre a linha do chão.
*Nunca:* rotação 2D global mais achatamento vertical (`vScale = 0.52`) de um sprite em pé — foi o que transformou o Orc em uma tira de 21 px de altura.

### Lesson 6 — Artefatos locais se corrigem cirurgicamente

Halo, pixel perdido ou tremor de topo de cabeça se resolvem no lugar, sem quebrar coreografia aprovada, sincronia de arma, tempos ou identidade.
*Nunca:* reconstruir um clipe aceitável para remover seis pixels e perder o ritmo aprovado.

### Lesson 7 — Preserve o que já funciona ao revisar o que está fraco

`Idle` frontal, `Walk` e os ataques frontais de `Sword`/`Axe` já aprovados permanecem byte-idênticos, salvo pedido explícito do criador.
*Nunca:* regenerar a biblioteca inteira para consertar as vistas traseiras e alterar em silêncio a arte frontal aprovada.

### Lesson 8 — A superfície de revisão tem que tornar a inspeção do conjunto trivial

Um estúdio, 4 direções × 7 ações, antes/depois por ação revisada, passo a quadro, loop e transições. E o "antes" precisa ser anterior de verdade.
*Nunca:* uma pasta de PNGs com um README dizendo ao criador quais arquivos abrir e em que ordem.

### Lesson 9 — Todo pacote passa por portão técnico **e** por revisão visual/artística

Os dois, nesta ordem, antes de qualquer apresentação como pronto. Passar em um não é passar no outro.
*Nunca:* entregar no portão técnico e deixar o criador descobrir os problemas de anatomia.

### Lesson 10 — QA independente inspeciona critério visual, não só contagem e esquema

A QA revisa anatomia, perspectiva, silhueta, coreografia e limpeza de pixels — e registra explicitamente o que não julgou.
*Nunca:* um veredito "APPROVED" montado sobre hashes recomputados enquanto o próprio relatório declara não julgar a arte.

---

## 15. Limites deste contrato

- Não concede aprovação artística, promoção de candidato, seleção de equipamento nem integração Unity.
- Não implementa suporte de runtime a overlays de arma; `runtimeImplemented: false` permanece.
- Não autoriza alterar arte canônica fora do escopo declarado da tarefa.
- Não transforma piso numérico em veredito: os números servem para barrar regressão e para tornar a discussão concreta, não para substituir o olho do criador.

Documento irmão: [`docs/WORKFLOW.md`](WORKFLOW.md) (os quatro status no fluxo de produção) e [`docs/MAIN_ORC_COMBAT_POLISH.md`](MAIN_ORC_COMBAT_POLISH.md) (o passe de recuperação artística em si).
