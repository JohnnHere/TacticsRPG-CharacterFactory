# Estágio A — Auditoria de produção e snapshot protegido

2026-10-25/26 · `main-orc-complete-animation-v1` · personagem `orc-v1` (Verde Warcraft)
**Resultado: PASS técnico. Nenhuma arte foi criada, editada, movida ou removida por este estágio.**

Este documento é o registro do DEV para o Estágio A. Ele descreve apenas o que existe e o que falta
antes de qualquer produção nova. Aprovação artística continua sendo decisão explícita do criador; nada
aqui concede Gate, seleção ou promoção de candidato.

## A. Escopo, método e garantias

- **Read-only sobre a arte e os metadados de produção.** As únicas escritas deste estágio ficam em
  `experiments/main-orc-complete-animation-v1/` (este diretório) e no novo script
  `tools/audit-main-orc-complete-animation.mjs`.
- **Zero chamadas de nuvem, zero sessões do Aseprite, zero escrita em `../TacticsRPG`**, nenhum
  `git reset/commit/stash/clean`.
- **Escopo temporal explícito (`BASELINE_AT_SNAPSHOT`).** O relatório descreve o instante em que
  `protected-art.json` foi gravado, e não a árvore viva. Isso impede que trabalho concorrente
  altere silenciosamente o que o Estágio A afirma. `--current` audita a árvore viva quando for a hora.
- **Metadados do baseline lidos do Git HEAD, não do disco.** Como a árvore estava limpa em `a9ab1e6a`
  quando o estágio começou, HEAD *é* o estado auditado; ler do commit mantém o relatório reproduzível
  mesmo que outra linha de trabalho edite os mesmos arquivos durante o estágio. Cópias de HEAD ficam em
  `before-metadata/`. Arquivos que só existem depois do snapshot são marcados como
  `ABSENT_IN_HEAD` / `ARRIVED_AFTER_SNAPSHOT` em vez de virarem baseline por engano.
- **Estado inicial do Git: árvore limpa** em `a9ab1e6a` ("integracao com aseprite e pixel lab feita com
  sucesso"). Evidência em `initial-git-status.txt`; estado corrente em `current-git-status.txt`.

## B. Resultado da auditoria

| Verificação | Resultado |
|---|---|
| Arte anterior protegida por SHA256 | **10.060 arquivos** (`characters/`, `assets/weapons/`, `ideas/`), **0 divergências**, 0 removidos |
| Biblioteca de arte entregue protegida por hash | **2.302 arquivos**, **0 divergências** |
| Clipes auditados no baseline | 24 `clip.json` (14 correntes + 10 históricos rejeitados) |
| Bindings/perfis auditados | 6 `profile.json` (Sword/Axe × 3 revisões) |
| Integridade de arquivos/hashes/canvas | **3.172 checagens, 0 falhas** |
| Invariantes entre clipes | **34 checagens, 0 falhas** |
| Doctor | PASS — Aseprite `1.3.18.6-x64`, modo batch, `--noinapp` |
| editor-check | AVAILABLE |
| Suíte do projeto | `node --test --test-concurrency=1` → **15/15 PASS** (26,9 s) |

Evidência legível por máquina: `audit.json`; verificação de baseline: `baseline-verification.json`.

## C. Inventário real de produção (baseline)

### Corpo

| Estado | Clipe canônico | Quadros | Duração | Canvas | Situação de aprovação |
|---|---|---:|---:|---|---|
| Idle | `source/studies/Idle/clip.json` | 5 | 2200 ms (400/450/500/450/400) | 128×128 | `CREATOR_SELECTED_GREEN_WARCRAFT` + `APPROVED_CREATOR_IDLE_REFERENCE` |
| Walk | `source/studies/Walk/clip.json` | 16 | 1280 ms (80 ms/frame) | 128×128 | `PENDING_CREATOR_GREEN_WALK` |

O Idle segue o padrão fixo `idle-balanced-v1` (`config/idle-art-standard-v1.json`). As cópias de
apresentação em `onehanded-*/Idle` e `onehanded-*/Walk` são aliases declarados (`alias: true`), não
novas animações.

### Ataques de uma mão (somente `front_r`)

| Revisão | Perfil | Quadros | Duração | Intervalo visível | Contato declarado |
|---|---|---:|---:|---|---|
| `main-orc-onehanded-v3` (**ativa** em `equipment-current.json`) | Sword | 8 | 775 ms | 1..6 | frame 5, **sem `timeMs`** |
| `main-orc-onehanded-v3` | Axe | 10 | 1130 ms | 1..7 | frame 5, **sem `timeMs`** |
| `main-orc-onehanded-polish-v1` (candidata isolada) | Sword | 11 | 690 ms | 1..8 | frame 6 @ 320 ms |
| `main-orc-onehanded-polish-v1` | Axe | 12 | 1055 ms | 1..8 | frame 6 @ 460 ms |
| `main-orc-onehanded-entry-v1` (candidata mais nova) | Sword | 13 | 730 ms | 2..10 | frame 8 @ 360 ms |
| `main-orc-onehanded-entry-v1` | Axe | 12 | 1005 ms | 2..8 | frame 6 @ 410 ms |

Ponteiros: `equipment-current.json` → `main-orc-onehanded-v3` → `source/onehanded-rescue-v3/manifest.json`.
`character.json.equipmentPreview` aponta para **o mesmo** manifest ativo (consistente).
`equipment-polish-candidate.json` e `equipment-entry-candidate.json` existem apenas como candidatos
(`REVIEW_ONLY`), sem promoção. Todos declaram `PENDING_CREATOR` e `runtimeImplemented: false`.

Gates: `characters/orc-v1/reviews.json` está **vazio** — a seleção de identidade não registrou Gate de
conceito, base, consistência ou quatro vistas.

### Armas

| Item | Categoria | Mãos | PPU | Canvas | Conteúdo (alfa) | Grip local |
|---|---|---|---:|---|---|---|
| `recruit-sword` | Sword | 1 | 100 | 96×96 | **26×72 px** | 48,66 |
| `militia-axe` | Axe | 1 | 100 | 96×96 | **36×47 px** | 36,55 |

Escala 1 nos dois, sem reescala por quadro. SHA256 de sprite e mestre conferem com os registros dos
clipes.

## D. Invariantes verificadas — e que precisam continuar verdadeiras

Estas são as regras que o Estágio A comprova hoje e que os próximos estágios não podem quebrar sem
declarar a mudança:

1. **Continuidade do neutro.** Em 6/6 ataques correntes, o **primeiro** e o **último** quadro são
   byte-idênticos ao quadro 0 do Idle da mesma revisão. Qualquer Hit/Defeat/ataque novo deve começar e
   terminar nesse mesmo neutro.
2. **Arma somente no ataque.** 8/8 clipes de repouso analisados não declaram arma visível nem camadas
   `weaponBack`/`weaponFront`; 6/6 ataques têm `weaponVisible` verdadeiro exatamente no intervalo
   declarado, contíguo.
3. **Registro de canvas.** Corpo nativo 128×128 colado em (64,64) do canvas 256×256; `groundY` 190;
   linha de chão do corpo em y=190 (bbox termina em 191 exclusivo). Nos PNGs nativos 128, o mesmo corpo
   ocupa y=6..127. Idle, Walk e ataques compartilham esse registro exato (bbox 86,70→170,191 nos
   compostos; 22,6→106,127 no nativo).
4. **Integridade de arquivos.** 1.126 PNGs de quadro existem com SHA256 igual ao registrado; 728
   camadas têm canvas 256×256; 24 mestres, 6 corpos, 6 mãos e as 6 duplas sprite/mestre de arma
   conferem com o hash registrado. Isso prova que os arquivos não foram alterados desde o export — não
   prova qualidade artística.

## E. Lacunas para "produção completa" (escopo `front_r`)

| Estado exigido pelo contrato | Situação em `orc-v1` |
|---|---|
| Idle | PRESENTE (aprovado como referência) |
| Walk | PRESENTE (aprovação do verde pendente) |
| Attack com espada | PRESENTE (v3 ativa + 2 candidatas) |
| Attack com machado | PRESENTE (v3 ativa + 2 candidatas) |
| **Attack desarmado (`basic.unarmed`)** | **AUSENTE** — nenhum clipe em nenhuma revisão |
| **Hit** | **AUSENTE** |
| **Defeat** | **AUSENTE** |

Observações que restringem o escopo real:

- Este personagem só possui a vista `front_r`. As outras três vistas nunca foram produzidas para
  `orc-v1`; a matriz de quatro vistas do contrato (`front_l`, `back_r`, `back_l`) continua sendo escopo
  separado e maior, não uma formalidade.
- Os clipes `Attack`/`Hit`/`Defeat`/`basic.unarmed` das **sete roupas `orc-01-*`** existem e foram
  aprovados no passado, mas pertencem a outro indivíduo/identidade. Reutilizá-los exigiria declaração
  explícita de reuso e revisão artística; não são substitutos automáticos do Orc principal.
- O corpo é weapon-independent: nenhum clipe novo pode embutir arma. Arma só existe como asset separado
  e overlay declarado no intervalo do ataque.

## F. Inconsistências e riscos registrados

Doze achados em `audit.json` → `findings` (agrupados abaixo em dez linhas: o de `contactEvent` aparece
quatro vezes, um por clipe). Nenhum é falha de integridade.

| Severidade | Área | Achado |
|---|---|---|
| WARN | cobertura | Faltam Attack desarmado, Hit e Defeat. |
| WARN | metadados | `character.json` mudou depois do snapshot (ver seção G): `profile.groundY`, `counts.Attack/Hit/Defeat`, `note`, `reuseAssessment`, `completeAnimationCandidate`. O baseline continua sendo a versão de HEAD. |
| INFO | gates | `reviews.json` vazio; nenhum Gate registrado apesar da seleção de identidade. |
| INFO | perfil | `character.json.profile.counts` lista só `Idle` e `Walk`; não representa combate. |
| INFO | metadados | `clip.json` canônicos de `studies/Idle` e `studies/Walk` **não declaram** canvas/ground/PPU/loop; só as cópias `onehanded-*` declaram 256×256, groundY 190, corpo em (64,64). Consolidar pelos metadados das cópias. |
| INFO | eventos | Os clipes **ativos** v3 declaram `contactEvent.frame` **sem `timeMs`**; só as candidatas polish/entry têm tempo explícito. |
| INFO | metadados | 10 clipes históricos (`source/equipment*`) não têm `category`/`id`; são v1/v2 rejeitados e nunca devem ser lidos como produção. |
| INFO | aprovação | Walk verde está `PENDING_CREATOR_GREEN_WALK`; "locomoção atual" ≠ "aprovada". |
| INFO | caminhos | Caminho absoluto máximo entre arquivos protegidos: 218 caracteres. Copiar entregas para pastas mais profundas estoura o limite de 260 do Windows (foi o que impediu uma cópia byte a byte da biblioteca). |
| INFO | ponteiros | `source/equipment-complete-candidate.json` existe no disco mas não em HEAD: é ponteiro do fluxo concorrente (`main-orc-complete-v1`), não o ponteiro ativo. O ativo continua `equipment-current.json` → `main-orc-onehanded-v3`. |

## G. Trabalho concorrente observado durante o estágio

Entre a criação do snapshot e o fechamento deste relatório apareceram na árvore, **sem relação com
este estágio**:

- **918 arquivos de arte** novos (ex.: `characters/orc-v1/source/aseprite/complete-v1/composite/back_l/…`),
- **37 metadados** novos (`characters/orc-v1/source/complete-v1/<direção>/{Idle,Walk,Hit,Defeat,Unarmed,Sword/Attack,Axe/Attack}/clip.json`),
- 9 entradas de Git não rastreadas, incluindo `tools/build-main-orc-complete.mjs`,
  `tools/aseprite/author-main-orc-complete.lua` e `source/equipment-complete-candidate.json`.

Registro em `concurrent-arrivals.txt`. Consequências, ditas de forma direta:

1. **A proteção do Estágio A cobre os 10.060 arquivos anteriores, e nenhum deles mudou** (0 divergências).
   Os 918 novos não estavam no snapshot porque não existiam quando ele foi gravado.
2. Nada desse trabalho concorrente foi auditado, promovido ou usado como verdade de produção aqui.
3. O baseline continua sendo a referência contra a qual o trabalho novo deve ser comparado — e é
   exatamente por isso que o snapshot foi feito antes.

### G.1 Metadado de produção também mudou no meio do estágio

Arte foi protegida por hash; metadado não precisa disso — precisa de âncora. A âncora é **HEAD**.
Um único arquivo auditado diverge do commit: `characters/orc-v1/character.json`, com exatamente as
chaves que o fluxo paralelo acrescenta:

| Chave | Agora | Leitura |
|---|---|---|
| `profile.groundY` | `126` | registro de linha de chão do conjunto novo |
| `profile.counts.Attack / .Hit / .Defeat` | `5 / 5 / 5` | contagem declarada do conjunto novo |
| `profile.note` | texto sobre "biblioteca completa em 4 direções" | descrição do fluxo paralelo |
| `reuseAssessment` | nova lista de componentes | avaliação de reuso do fluxo paralelo |
| `completeAnimationCandidate` | `source/equipment-complete-candidate.json` | ponteiro para o candidato novo |

Todos os outros 16 arquivos de metadado auditados estão **byte-idênticos** a HEAD — inclusive
`equipment-current.json` (ainda `main-orc-onehanded-v3`), `reviews.json` (ainda vazio),
`reports/orc-production-current.json` (identidade intacta) e os dois `weapon.json`.

Isso é registro, não endosso: `character.json` descrevendo o conjunto novo não o torna corrente, nem
lacuna fechada, nem aprovado. Enquanto o criador não decidir, o ponteiro ativo e a verdade de produção
continuam os do baseline.

Nota de honestidade sobre o andamento: uma execução em modo `--current`
(`audit-current.json`, não é o baseline) já vê **52 clipes / 14 bindings**, **5.492 checagens de
integridade e 74 invariantes, 0 falhas**, e **cobertura dos sete estados** (Idle, Walk, Attack
desarmado, Attack espada, Attack machado, Hit, Defeat) no conjunto em construção — com os 10.060
arquivos protegidos ainda em **0 divergências**. Isso indica que o diretório `complete-v1` endereça
justamente as lacunas da seção E — mas é trabalho de outro fluxo, ainda em escrita, e **não recebeu
revisão, comparação visual nem aprovação deste estágio**. Não ler esse número como entrega concluída.

## H. O que este estágio não fez

- Não julgou qualidade artística, peso, pegada, leitura tática ou naturalidade do movimento.
- Não abriu navegador, não capturou reprodução e não reexecutou construtores de preview (para não
  sobrescrever evidências de passes anteriores).
- Não gerou arte, não chamou PixelLab, não abriu Aseprite, não tocou Unity, `.meta`, Core, stats,
  inventário ou GUIDs.
- Não alterou `AGENTS.md`, `docs/`, `handoff/`, `config/` nem ponteiros de produção. Integração de
  documentação é decisão do orquestrador/estágio seguinte, e outro agente está escrevendo na mesma
  árvore.

## I. Artefatos e reprodução

```
experiments/main-orc-complete-animation-v1/
  audit.json                     inventário + matriz de cobertura + invariantes + achados (BASELINE)
  audit-current.json             mesma auditoria na árvore viva, quando executada com --current
  protected-art.json             10.060 SHA256 da arte anterior (criado antes de qualquer escrita)
  protected-library.json         2.302 SHA256 da biblioteca entregue
  before-metadata/               cópia dos metadados ativos (ficha, revisões, ponteiros, clipes, configs)
  baseline-verification.json     doctor + editor-check + suíte 15/15 com a saída bruta
  initial-git-status.txt         árvore limpa no início (HEAD a9ab1e6a)
  current-git-status.txt         estado corrente, verbatim
  concurrent-arrivals.txt        entradas surgidas depois do snapshot, fora deste escopo
  git-summary.json               branch/HEAD/contagens + nota de método
```

```powershell
# auditoria do baseline (não escreve fora do experimento)
node tools/audit-main-orc-complete-animation.mjs

# idem, com doctor/editor-check/suíte registrados
node tools/audit-main-orc-complete-animation.mjs --verify

# auditar a árvore viva em vez do baseline congelado (para estágios seguintes)
node tools/audit-main-orc-complete-animation.mjs --current
```

O script falha com exit code 1 se qualquer hash, canvas, intervalo de visibilidade, continuidade de
neutro ou mestre divergir — ele serve como regressão barata para os próximos estágios.

Duas regras de operação: `--current` grava `audit-current.json` e **nunca** sobrescreve o baseline; e
`protected-art.json` só deve ser regravado com `--refresh-snapshot` se o propósito for iniciar um novo
baseline — regravá-lo por conveniência apaga a única prova de que a arte anterior foi preservada.

## J. Conclusão do estágio

- **Implementado:** auditoria completa, snapshot protegido, verificação de baseline e regressão
  reexecutável.
- **Validado tecnicamente:** 3.172 checagens de integridade + 34 invariantes, 0 falhas; 15/15 testes;
  doctor/editor-check OK.
- **Não aprovado:** nenhuma arte, nenhum Gate, nenhuma promoção. Aprovação artística: `PENDING_CREATOR`.
- **Próximo passo autorizado pelos fatos:** produzir os três estados ausentes (Attack desarmado, Hit,
  Defeat) a partir do neutro atual do Idle, mantendo registro 256×256 / groundY 190, a política
  arma-somente-no-ataque e a continuidade de neutro — e então revisar com o criador antes de qualquer
  propagação.
