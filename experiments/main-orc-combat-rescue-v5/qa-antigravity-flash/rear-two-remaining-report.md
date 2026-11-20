# Relatório de QA Independente — Dois Últimos Ciclos Traseiros Armados (`back_r/Sword` e `back_l/Axe`)

**Veredito:**
- **`back_r/Sword`:** **`READY_FOR_MATRIX_REVIEW`**
- **`back_l/Axe`:** **`READY_FOR_MATRIX_REVIEW`**

**Status Técnico:** `TECHNICALLY_COMPLETE`  
**Status Artístico do Pacote:** `VISUAL_REVIEW_REQUIRED` (Global: `ARTISTIC_REVISION_REQUIRED`, `PENDING_CREATOR`)  
**Data/Hora:** 2026-10-29T18:25:00Z  
**Revisor:** Gemini 3.8 Flash (High) via Antigravity QA Independente  
**Recursos Utilizados:** 0 chamadas PixelLab de produção nesta revisão; custo LLM não informado.

---

## 1. Escopo e Objeto de Revisão

Esta auditoria independente avaliou a entrega dos **dois últimos ciclos traseiros equipados** (`REAR_TWO_REMAINING_FULL_READY`), completando a biblioteca de 4 vistas de combate armado do Orc V1:
1. **`back_r/Sword`** (12 quadros, 730 ms): Corte diagonal de espada sobre a base corporal reparada pela GLM (`body-specialist/glm-fixes/back_r-Sword-full`, SHA-256 `aba36d66...`).
2. **`back_l/Axe`** (12 quadros, 1100 ms): Golpe overhead pesado de machado sobre a base corporal reparada pela GLM (`body-specialist/glm-fixes/back_l-Axe-full`, SHA-256 `d87cd833...`).

Autor: DEV Especialista de Pegada (`7db0e7b6-ab88-49e9-9362-a19121c8ebf5`).

---

## 2. Verificação de Fontes e Hashes SHA-256 no Disco

### 2.1 `back_r/Sword` (12f / 730 ms)

| Ativo | Caminho Relativo | SHA-256 Confirmado no Disco | Status |
|---|---|---|:---:|
| **Clip Manifesto** | `.../full-back-r-sword/clip.json` | `eb379d1d699ab51203ec633d645a29d9c63e377e36fe8b15b8fda44fc1a9aac6` | **MATCH** |
| **Mestre Composto (256)** | `.../full-back-r-sword/source/composite.aseprite` | `cf66aa1fd30280b4b143f891bdca298d8e6ad5faca4f89b4b6d5a8af0631abfb` | **MATCH** |
| **Mestre Corpo (256)** | `.../full-back-r-sword/source/body.aseprite` | `f0c0b9f650882256242b574501191c0196c78959acf4e49931b0e3245b990e90` | **MATCH** |
| **Mestre Luva/Mão (256)** | `.../full-back-r-sword/source/hand.aseprite` | `2018e1313ca767900e6e649d7b13f790331f97eb773ca97e8b804070ccf6e7cc` | **MATCH** |
| **Mestre Nativo (128)** | `.../full-back-r-sword/source/native.aseprite` | `bea7a0cf7138e4b8dcfb85a47605ecfc82f79181ce170a180b8e83b9545ddd0a` | **MATCH** |
| **Tira Composta (256)** | `.../full-back-r-sword/composite-strip.png` | `3274241434b277823fc4bbdc7c23f2337fca9a67826c6fbd3749ad9804f1a519` | **MATCH** |
| **Tira Nativa Composta (128)** | `.../full-back-r-sword/native-composite-strip.png` | `812036e67ad3cd3ec4bff4dcb899470e4e3a57cfbac1a81936a8fe0cbc565cf4` | **MATCH** |
| **Tira Nativa Corpo (128)** | `.../full-back-r-sword/native-strip.png` | `66ce949183e77fdaa6d59dd615303cec35a74ac00dc9f4ef9e91ed103546f646` | **MATCH** |

### 2.2 `back_l/Axe` (12f / 1100 ms)

| Ativo | Caminho Relativo | SHA-256 Confirmado no Disco | Status |
|---|---|---|:---:|
| **Clip Manifesto** | `.../full-back-l-axe/clip.json` | `9f7d01e726f3f6dc63b24aeb23da97ac9cad29a7fd31572ccdf59a3ee384a0f3` | **MATCH** |
| **Mestre Composto (256)** | `.../full-back-l-axe/source/composite.aseprite` | `a2ed1edcdf6dc3fdba68ec5ccb9742fd5868d1734f5e725e5a805eedf9d54a4c` | **MATCH** |
| **Mestre Corpo (256)** | `.../full-back-l-axe/source/body.aseprite` | `bd39a6687551571ac0fe32143dda2c2e98143f9c30dc38ef1c6cb778884c9ddf` | **MATCH** |
| **Mestre Luva/Mão (256)** | `.../full-back-l-axe/source/hand.aseprite` | `f86067488070e61b289bff9f8d246f18438b73b2839680df852517cacb953c08` | **MATCH** |
| **Mestre Nativo (128)** | `.../full-back-l-axe/source/native.aseprite` | `c3d3d76606913bffb726efa8211a8eec9971a0da6ddcc8e81e50705ebd0251ab` | **MATCH** |
| **Tira Composta (256)** | `.../full-back-l-axe/composite-strip.png` | `506a8f01814fcbdf2ed96365a73c286300cd63e166ed90d264f8131be48a1807` | **MATCH** |
| **Tira Nativa Composta (128)** | `.../full-back-l-axe/native-composite-strip.png` | `905668ccc47f03e1a2b05a9733c005e1b0a9db6e44fd8e4e9e7187a2a8e79fc9` | **MATCH** |
| **Tira Nativa Corpo (128)** | `.../full-back-l-axe/native-strip.png` | `0a59c724f0c796963195dfd1f601c309f526895bae093110bebaf547176780ea` | **MATCH** |

---

## 3. Auditoria dos Contratos Declarados

### 3.1 Preservação Absoluta do Corpo Base (`bodyRgbaDelta == 0`)
- **`back_r/Sword`:** Todas as 12 camadas corporais (`layers/body/00.png`..`11.png`) são **100% byte-idênticas** ao corpo aprovado em `body-specialist/glm-fixes/back_r-Sword-full/body256/`. No canvas nativo 128×128, a discrepância decodificada é **exatamente 0 pixels**. Duração: 730 ms.
- **`back_l/Axe`:** Todas as 12 camadas corporais são **100% byte-idênticas** ao corpo aprovado em `body-specialist/glm-fixes/back_l-Axe-full/body256/`. Discrepância nativa: **exatamente 0 pixels**. Duração: 1100 ms.

### 3.2 Preservação de Chaves Estruturais e Auditoria dos Reparos Específicos
- **Chaves F03, F04 e F07:** Preservadas byte-a-byte em ambos os clipes, mantendo a geometria e iluminação corporal aprovadas.
- **Auditoria do Reparo F06 em `back_r/Sword`:**
  - O quadro F06 havia sido corrigido pela GLM para remover pixels flutuantes e restaurar a cota de malha de aço sobre a tasset de couro.
  - A passagem da espada por F06 (ângulo 105°, pega `[162, 135]`) não reintroduziu resíduos, halos ou rastro de swoosh. O fundo corporal permanece 100% limpo e byte-idêntico à base restaurada.
- **Auditoria do Reparo F02 em `back_l/Axe`:**
  - O quadro F02 havia sido reconstruído pela GLM com inpaint para esculpir uma mão vazia fechada anatômica, eliminando a antiga haste de madeira e bloco disforme.
  - A montagem da pegada do machado em F02 (ângulo 305°, pega `[151, 84]`) insere o cabo de madeira diretamente dentro da manopla reconstruída, preservando os nós dos dedos e a continuidade articular com o antebraço. Não há alongamento de braço, nem luva dupla, nem deformação na ombreira.

### 3.3 Política Estrita `attack-only-v1`
- Em ambos os clipes, o intervalo visível é estritamente `[2, 8]`.
- Os quadros de borda F00, F01, F09, F10 e F11 têm **0 pixels não transparentes** nas camadas de equipamento (`weaponBack`, `weaponFront`, `handFront`), e os compostos finais são **100% byte-idênticos** ao corpo desarmado. Retorno neutro limpo, sem armas em Idle ou Walk.

### 3.4 Composição em 4 Camadas e Álgebra Alfa-Over
- Em todas as 24 instâncias (12 quadros × 2 clipes), a fórmula `((weaponBack OVER body) OVER weaponFront) OVER handFront` reproduz com 100% de exatidão os compostos PNG finais (**`alphaOverMatch: true`**).

---

## 4. Julgamento Artístico e Cinemática de Armas

### 4.1 `back_r/Sword`: Corte Diagonal de Espada
- **Item Autêntico:** Utiliza a Espada do Recruta (`weapon.json` SHA `7c090d89...`).
- **Trajetória:** [355°, 10°, 45°, 80°, 105°, 125°, 120°]. Lê claramente como um golpe de corte diagonal contínuo cortando o quadrante nordeste, com aceleração suave e recuperação estável.
- **Relação com o Solo:** O ponto mais baixo da espada no impacto F07 alcança `Y = 181`, mantendo **9 pixels de folga sobre `groundY = 190`**. A folga é visualmente convincente para um corte que passa rente ao chão sem penetração subterrânea.

### 4.2 `back_l/Axe`: Golpe Overhead Pesado de Machado
- **Item Autêntico:** Utiliza o Machado de Milícia (`weapon.json` SHA `8e7311ba...`).
- **Trajetória:** [305°, 320°, 335°, 15°, 80°, 120°, 105°]. O ciclo coreografa uma descida vertical violenta partindo do ápice overhead (F04, 335°), com flexão profunda de joelhos e quadril, entregando a massa corporal no impacto.
- **Relação com o Solo:** Em F07 (impacto), a lâmina toca **exatamente `Y = 190` (`nativeGroundY = 126`)**, cravando no solo com força total e sem penetração subterrânea. Em F08, o recuo elástico eleva a lâmina para `Y = 188` (2 pixels acima do solo), absorvendo o impacto de forma natural.

### 4.3 Legibilidade em Escala Tática (64px)
- Ambos os clipes mantêm alta nitidez na escala de jogo (64×64): a espada destaca-se pelo fio polido e fuller escuro; o machado destaca-se pela lâmina pesada de meia-lua e haste de madeira escura.

---

## 5. Auditoria Quadro a Quadro

### 5.1 `back_r/Sword` (12f / 730 ms)

| Quadro | Fase | Duração | Visível | HandFront Px | Bbox Arma [x1, y1, x2, y2] | Delta Corpo | Veredito |
|:---:|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **F00** | guard | 40 ms | Não | 0 px | N/A | 0 px | **PASS** |
| **F01** | chamber-init | 60 ms | Não | 0 px | N/A | 0 px | **PASS** |
| **F02** | hoist-lift | 60 ms | Sim | 80 px | [154, 55, 179, 126] | 0 px | **PASS** |
| **F03** | 01-hoist (key) | 70 ms | Sim | 88 px | [153, 50, 178, 120] | 0 px | **PASS** |
| **F04** | 02-apex (key) | 70 ms | Sim | 104 px | [170, 73, 222, 125] | 0 px | **PASS** |
| **F05** | slash-cleave | 40 ms | Sim | 67 px | [160, 116, 230, 141] | 0 px | **PASS** |
| **F06** | slash-descent (fix) | 40 ms | Sim | 80 px | [150, 125, 219, 151] | 0 px | **PASS** |
| **F07** | 03-impact (key) | 90 ms | Sim | 73 px | [140, 138, 200, 181] | 0 px | **PASS** |
| **F08** | recover-low | 70 ms | Sim | 84 px | [148, 138, 207, 182] | 0 px | **PASS** |
| **F09** | recover-pelvis | 70 ms | Não | 0 px | N/A | 0 px | **PASS** |
| **F10** | recover-guard | 60 ms | Não | 0 px | N/A | 0 px | **PASS** |
| **F11** | guard-return | 60 ms | Não | 0 px | N/A | 0 px | **PASS** |

### 5.2 `back_l/Axe` (12f / 1100 ms)

| Quadro | Fase | Duração | Visível | HandFront Px | Bbox Arma [x1, y1, x2, y2] | Delta Corpo | Veredito |
|:---:|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **F00** | guard | 70 ms | Não | 0 px | N/A | 0 px | **PASS** |
| **F01** | load-begin | 80 ms | Não | 0 px | N/A | 0 px | **PASS** |
| **F02** | hoist-begin (fix) | 90 ms | Sim | 78 px | [121, 39, 159, 91] | 0 px | **PASS** |
| **F03** | 01-hoist (key) | 100 ms | Sim | 80 px | [123, 31, 153, 86] | 0 px | **PASS** |
| **F04** | 02-apex (key) | 110 ms | Sim | 70 px | [116, 27, 142, 81] | 0 px | **PASS** |
| **F05** | drop-initiation | 50 ms | Sim | 46 px | [135, 47, 179, 91] | 0 px | **PASS** |
| **F06** | forward-cleave | 60 ms | Sim | 63 px | [155, 123, 206, 153] | 0 px | **PASS** |
| **F07** | 03-impact (key) | 110 ms | Sim | 63 px | [145, 139, 185, 190] | 0 px | **PASS** |
| **F08** | recover-low | 100 ms | Sim | 70 px | [148, 144, 192, 188] | 0 px | **PASS** |
| **F09** | recover-pelvis | 100 ms | Não | 0 px | N/A | 0 px | **PASS** |
| **F10** | recover-guard | 100 ms | Não | 0 px | N/A | 0 px | **PASS** |
| **F11** | guard-return | 130 ms | Não | 0 px | N/A | 0 px | **PASS** |

---

## 6. Marco Atingido e Limitações

### Marco Histórico de Pegadas
Com a aprovação destes dois ciclos, **todas as 8 animações armadas do Orc V1 (4 vistas × 2 perfis de arma: Sword e Axe) estão agora tecnicamente validadas e aprovadas no portão de pegadas como `READY_FOR_MATRIX_REVIEW`**:
1. `front_r/Sword` &rarr; `READY_FOR_MATRIX_REVIEW`
2. `front_l/Sword` &rarr; `READY_FOR_NEXT_STAGE` (equivalente em `qa-result.json`)
3. `front_r/Axe` &rarr; `READY_FOR_NEXT_STAGE`
4. `front_l/Axe` &rarr; `READY_FOR_NEXT_STAGE`
5. `back_r/Axe` &rarr; `READY_FOR_MATRIX_REVIEW`
6. `back_l/Sword` &rarr; `READY_FOR_MATRIX_REVIEW`
7. `back_r/Sword` &rarr; **`READY_FOR_MATRIX_REVIEW`**
8. `back_l/Axe` &rarr; **`READY_FOR_MATRIX_REVIEW`**

### Limitações:
1. Inspeção baseada em quadros discretos, recortes anatômicos 4× e players Chromium com validação de relógio. A percepção final de peso e fluidez contínua em motor de jogo permanece prerrogativa do Criador.
2. Não aprova a integração em `../TacticsRPG` nem concede promoção sem o congelamento final da matriz pelo orquestrador e revisão do Criador.
