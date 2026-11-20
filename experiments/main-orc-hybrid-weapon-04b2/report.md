# Piloto B2 — Arquitetura C em `back_r`

Status: `TECHNICALLY_COMPLETE` / `VISUAL_REVIEW_REQUIRED` / `PENDING_CREATOR`
Data: 2026-11-02 · Escopo: Orc principal, ataque de Espada, direção traseira direita recuperada, somente piloto local.

## 1. Pergunta desta rodada

O Experimento 04 provou a Arquitetura C em `front_l` e o Piloto B1 confirmou que ela se aplica
a uma segunda direção frontal (`front_r`) com uma única adaptação (o pivô). A vista traseira
direita é o caso mais exigente: a arma se divide em duas camadas de profundidade
(`weaponBack` atrás do corpo, `weaponFront` na frente), a pegada é parcialmente ocluída
(46..119 px de sobreposição de mão) e o quadro F06 tem o cabo passando à frente do corpo por
51 px. O Piloto B2 verifica se as mesmas duas espadas podem substituir a lâmina
**sem tocar em um único pixel do corpo ou da mão de pegada**.

Resposta: **sim, sem nenhuma adaptação nova de anatomia nem de pivô** — esta direção declara
`grip` e `rotationDeg` em todos os 10 quadros armados.

## 2. Fontes confirmadas

| Item | Caminho | Situação |
|---|---|---|
| Corpo/mão da direção | `characters/orc-v1/source/combat-recovery-v8/rear-arc/back_r-sword/` | 14 quadros, 730 ms, contato F08 / 325 ms, mesmo intervalo de arma F02..F11 |
| Espada A (Recruta) | `variants/sword-a/sword.png` | **byte-idêntica** ao Exp04, B1 e aos próprios hashes |
| Espada B (aço facetado) | `variants/sword-b/sword.png` | **byte-idêntica** ao Exp04 e B1 |
| Mecanismo de composição | `author.lua` + `run.mjs` herdados | mesmas 4 camadas: `weaponBack → body → weaponFront → handFront` |

Nada sob `characters/`, `assets/` ou `reports/` foi alterado ou criado
(`protectedFilesChanged: 0`). PixelLab pago: **zero**. Unity: **não tocado**.

## 3. Por que esta direção exigiu menos adaptação que o `front_r`

O `front_r` não declarava pivôs, e o Piloto B1 teve de medi-los na arte. O `back_r`
recuperado declara `rightGrip` e `rotationDeg` nos 10 quadros armados do `clip.json`.
O trabalho aqui foi **validar** os pivôs declarados, não inventá-los
(`fit-back-r-grip.mjs`, saída em `grip-pivot-fit.json`):

1. Estimativa por centroide de transformação rígida:
   `grip ≈ centroide(arma) − R(rot)·(centroide(asset) − (48,66))`.
2. Comparação com o `grip` declarado, quadro a quadro, e confirmação do ótimo inteiro.

**Resultado:** os 10 pivôs declarados são o ótimo da busca (desvio da estimativa por
centroide ≤ 0,58 px por quadro). Nenhum pivô foi ajustado — o `grip-profile-back-r.json` registra o contrato desta
direção, reutilizável por itens da mesma família.

## 4. A adaptação que a lâmina de B exigiu

A lâmina de B é **mais estreita** que a da Espada do Recruta (bisel interior de 7..9 px contra
12 px). Como nas vistas frontais, repintar apenas onde B tem pixel deixaria metal antigo vivo.
O `author.lua` desta rodada usa **mapeamento proporcional de brilho interior**:

1. Silhueta da arma original preservada 100% (`silhouetteDeltaAB = 0` em 10/10 quadros armados).
2. Contorno escuro ( `max(R,G,B) ≤ 32`) re-apoia a linha escura de 1 px de B `(12,15,18)`.
3. Pixels interiores de metal mapeiam proporcionalmente no bisel facetado de B
   (4 tons de aço claro), por ordem de luminância na mesma linha.
4. Guarda/cabo é hereditário (2315 px preservados sem modificação); só a lâmina muda
   (4735 pixels repintados nos F02..F11).

Resultado medido: **0 px de lâmina antiga sobrevivente**, **0 px de silhueta alterada**,
**0 px de halo de matte**, **0 px de diferença fora da lâmina** em todos os 14 quadros
(não-arma A×B = 0), e a contagem de pixels da arma é idêntica em A e B em cada quadro.

## 5. Regra de profundidade traseira

Contrato de profundidade do `back_r` (herdado da recuperação, respeitado pela composição):

- `weaponBack`: pomel/cabo por trás do quadril/tronco direito (149..151 px na maioria dos
  quadros armados) e a pega de couro no F06 (53 px ocultos pelo corpo).
- `weaponFront`: **100% da guarda e da lâmina** na frente do corpo (172 px de guarda no F02;
  51 px de cabo na frente no F06; no F07, 2 px de costura de rotação arredondada em `v = 55`).
- `handFront`: luva de pegada por cima do cabo, 38..83 px de sobreposição com as camadas
  da arma, byte-idêntico à fonte.

## 6. Reutilização comprovada

| Verificação | Resultado |
|---|---|
| `body` byte-idêntico à fonte, nas duas variantes (14 camadas × 2) | **28/28** |
| `handFront` byte-idêntico à fonte, nas duas variantes (14 camadas × 2) | **28/28** |
| Corpo isolado idêntico entre A e B (14/14 quadros comparados) | **28/28 em camadas** |
| Variante A idêntica à fonte recuperação (composto) | **0 px** (14/14) |
| Quadros desarmados sem nenhum pixel de arma | **sim** (F00, F01, F12, F13) |
| Silhueta da arma alterada por B | **0 px** |
| Pixels da lâmina A sobreviventes em B | **0 px** |
| Pixels da guarda/cabo repintados | **0 px** |
| Tempos preservados (14 quadros, 730 ms) | **sim**, nas duas variantes |
| Assets de espada idênticos ao Exp04/B1 | **sim** (`.png` e `.aseprite` byte a byte) |
| Camadas de arma intactas em A (weaponBack/weaponFront = fonte) | **sim** |

`verification.json` registra status `TECHNICALLY_COMPLETE` com 12/12 verificações verdadeiras.

## 7. Herdado versus introduzido

**Herdado (não corrigido de propósito):**

- **Coreografia original** do `back_r` recuperado, com a mesma cadência de 730 ms e contato em
  325 ms (`CANDIDATE_VISUAL_ONLY`; dano é decisão do runtime).
- **Qualquer característica anatômica, de armadura ou de oclusão** do tronco e da mão: como
  `body` e `handFront` são byte-idênticos à fonte nas duas variantes, nada disso pôde ser
  introduzido pela composição.
- A recuperação de `back_r/Sword` **não recebeu defeitos confirmados pelo QA independente da Wave 2**
  (os apontados naquela onda foram `back_l/Sword`, `back_r/Axe` e `back_l/Axe`), mas possui
  3 características herdadas do corpo base V8 (`INHERITED_BODY_DEFECT`) que permanecem intocadas
  por contrato:
  1. **Paleta/contraste do corpo traseiro V8 (`F02..F11`)**: mais escura (`luma ~34`) em relação aos
     bookends `F00..F01` / `F12..F13` e ao `back_r/Idle` (`luma ~62`).
  2. **Salto de entrada `F02 → F03`**: transição de pose entre `establish-grip` (`rightGrip [163,131]`)
     e `anticipation` (`rightGrip [168,98]`, elevação de `33 px` em `35 ms`).
  3. **Escorço distal do antebraço direito em `F07..F09`**: na descida rápida do golpe traseiro
     (`[179,115] → [172,134] → [158,169]`), o braço opera em escorço curto atrás/ao lado do ombro direito.

**Introduzido por esta composição (`COMPOSITION_REGRESSION` = 0):** apenas a lâmina de B (as cores da própria espada B,
idênticas em todas as direções), com **0 px** de delta fora da lâmina (`nonWeaponCompositeDiffAB = 0` nos 14 quadros).

## 8. Limitações observadas

- O piloto prova **arquitetura e reutilização**, não qualidade artística do golpe nem da
  espada B — a decisão visual segue aberta ao criador.
- O pivô é válido para esta direção; direções novas devem replicar o mesmo procedimento de
  validação (declarado ou medido) antes da substituição de lâmina.
- Ataques de Machado e as outras vistas traseiras continuam fora do escopo desta rodada.

## 9. Escopo respeitado

PixelLab pago: **zero**. Unity: **não tocado**. Promoção automática: **nenhuma**.
`characters/`, `assets/`, `reports/`: **inalterados**. Experimentos 04 e B1:
**preservados integralmente**. Axe Attack, `back_l` e vistas frontais: **não tocados**.

## Artefatos

| Arquivo | Conteúdo |
|---|---|
| `review/index.html` | Página de revisão: original, A, B, corpo isolado, zoom da mão, playback |
| `verification.json` | Todas as comparações e critérios de aceitação, por quadro |
| `grip-pivot-fit.json` | Validação dos 10 pivôs declarados desta direção |
| `grip-profile-back-r.json` | Contrato de pegada/profundidade do `back_r`, reutilizável |
| `blade-repaint-stats.json` | Pixels de lâmina repintados e de cabo preservados por quadro |
| `representative-review-2x.png` | Original / A / B / corpo / arma em F02, F05, F08, F11 |
| `grip-10x-both.png` | Mão e punho no contato F08 em 10× |
| `review/hands/{a,b}/` | Mão ampliada nos 14 quadros, por variante |
| `full/{a,b}/` | 14 quadros por variante, com camadas e mestres Aseprite |
