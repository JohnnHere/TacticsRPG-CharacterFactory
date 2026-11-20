# Reconstrução do `back_l` Sword + Axe sobre as poses do v5

**Decisão do criador:** devolver o `back_l` à linhagem em que a mão era anatomicamente correta.
Os punhos originais vivem nas poses do v5 — e as poses atuais (linhagem v6→v7→v8) perderam essa
anatomia. Este passe reconstrói as duas células **sobre as poses do v5**, **retimadas para a grade
atual**, preservando as mãos originais intactas.

Isto substitui as tentativas anteriores (passe 08a rejeitado, 08b rejeitado, transplante parcial
com 24 quadros `NEEDS_DECISION`). Nenhum desses métodos deve voltar.

## Limites duros

- **Zero PixelLab, zero geração.** Autoria no Aseprite (manual ou Lua registrada).
- **Poses vêm do v5.** Os clusters de corpo, braço e mão de cada quadro vêm dos quadros v5.
  Adaptação local permitida; **invenção de anatomia, não**.
- **Grade atual obrigatória** (é o que mantém as quatro direções sincronizadas):
  - Sword: **14 quadros**, durações `[30,65,35,50,45,35,30,35,35,100,55,80,45,90]` (soma 730 ms),
    fases `rest, body-preparation, establish-grip, anticipation, coil-behind, apex-hold,
    apex-descent, slash-release, contact, follow-through, recoil, settle-grip, release-grip,
    return-to-guard`, `contactEvent` **F08 / 325 ms / contact**, arma visível **F02–F11**,
    bookends desarmados.
  - Axe: **12 quadros**, durações `[40,65,35,80,155,35,115,110,130,50,90,100]` (soma 1005 ms),
    fases `rest, body-preparation, establish-grip, anticipation, overhead-coil, cleave-drive,
    heavy-impact, follow-through, recoil, settle-grip, release-grip, return-to-guard`,
    `contactEvent` **F06 / 410 ms / heavy-impact**, arma visível **F02–F08**, bookends desarmados.
- Não toque em `characters/`, `assets/`, `reports/`, `../TacticsRPG`. Não faça commit.
- Não mexa nas outras direções nem nas outras ações. Trabalhe em
  `experiments/main-orc-backl-v5base/`.

## Fontes v5

**Sword (corpo):** `characters/orc-v1/source/combat-rescue-v5/body-specialist/final-cycles/back_l-Sword-full/body256/`
— 12 poses planas em 256×256, **com o punho reparado BODY-01 validado** (F06 é o melhor punho da
história do Orc: nós de dedos, polegar, sombra comum).

**Sword (referência de camadas/arma):** `characters/orc-v1/source/combat-rescue-v5/combat/back_l/Sword/`
— 8 quadros com camadas `weaponBack/body/weaponFront/handFront` e fases
`guard-start, chamber-grip, lateral-windup, slash-release, slash-contact, follow-through,
recoil-settle, guard-recovery`.

**Axe (tudo):** `characters/orc-v1/source/combat-rescue-v5/combat/back_l/Axe/`
— 8 quadros com camadas completas, fases iguais às da espada do v5.

**Armas:** as mesmas da produção — Espada do Recruta e Machado de Milícia
(`combat-rescue-v5/combat/weapons/{Sword,Axe}/`), com `weapon.json` (grip, pivô). Elas já estão
dentro dos quadros v5; o registro atual dessas armas não mudou.

## Como mapear poses do v5 na grade atual

Mapeamento **semântico por fase**, não amostragem mecânica por timestamp:

- Cada fase da grade atual recebe a pose v5 mais adequada ao seu significado.
  Exemplo (Sword): `rest` ← guard-start · `establish-grip` ← chamber-grip ·
  `anticipation` ← lateral-windup · `contact` ← slash-contact · `follow-through` ← follow-through ·
  `recoil` ← recoil-settle · `return-to-guard` ← guard-recovery. Você decide o mapa final e o
  registra; as fases intermediárias (`coil-behind`, `apex-hold`, `apex-descent`,
  `slash-release`) podem reutilizar poses v5 vizinhas adaptadas localmente.
- **Reuso de pose em quadros consecutivos é permitido apenas para poses desarmadas** (bookends).
  Dois quadros armados consecutivos byte-idênticos recriam o congelamento já reprovado — se isso
  acontecer, adapte localmente (pequenos ajustes de sombra/1 px de deslocamento registados) ou
  redistribua o mapa, e documente.
- `apex-descent` (F06) é o quadro de transição entre ápice e descida: derive-o da pose v5 vizinha
  com adaptação local mínima, ou propõe outra solução no relatório.

## Contrato de camadas por quadro

`weaponBack → body → weaponFront → handFront`. Corpo e mão vêm do v5; a arma fica no topo com a
oculsão original daquela pose (cabo atrás da luva quando for o caso, via `weaponBack`/`handFront`).
Os bookends F00–F01 e F12–F13 (Sword) e F00–F01, F09–F11 (Axe) são **desarmados**: sem pixels de
arma em nenhuma camada, corpo em repouso/guarda coerente com o Idle.

## O que fica intocável

As outras 26 células do Orc, as fontes v5 e v8 (somente leitura), `characters/`, `assets/`,
`reports/`, `../TacticsRPG`. Nada de commit.

## Entrega, em `experiments/main-orc-backl-v5base/`

1. `sword/` e `axe/` completos: `clip.json`, `layers/{weaponBack,body,weaponFront,handFront}/NN.png`,
   `frames/NN.png` (composto), mestres `.aseprite`, `native/`, strips.
2. `pose-map.md` — o mapa v5→grade: para cada quadro alvo, o quadro-fonte v5, a operação
   (reuso direto / adaptação local / derivação), e o motivo.
3. `temporal-check.json` — durações, fases, `contactEvent`, janela armada, contagem de pares
   armados byte-idênticos (deve ser 0 ou justificado).
4. `before-after/` — cada quadro novo ao lado do quadro atual do V8, 1×.
5. `hands-8x/` — recorte do punho em 8× de cada quadro armado, para julgar a mão.
6. `report.md` — procedência por quadro, decisões de mapa, limitações, e a declaração honesta do
   que é reuso e o que é adaptação local.

## Critério

- A mão, em todos os quadros armados, é **a mão original do v5** — punho fechado com massa e
  acabamento da época, reconhecível em 8×.
- A coreografia lê como corte descendente coerente com as vistas frontais, não como golpe lateral.
- Grade, fases, contato e janelas armadas idênticos aos da produção atual.
- Se algum quadro não puder ser resolvido sem inventar anatomia, marque `NEEDS_DECISION`,
  preserve a melhor alternativa honesta e siga.

O criador vai julgar as poses, a mão e a continuidade antes de qualquer promoção ou integração.
