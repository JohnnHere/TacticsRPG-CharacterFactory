# Relatório de QA Independente — Ciclo Completo `back_l/Sword` (12f / 730 ms)

**Veredito:** `READY_FOR_MATRIX_REVIEW`  
**Status Técnico:** `TECHNICALLY_COMPLETE`  
**Status Artístico do Pacote:** `VISUAL_REVIEW_REQUIRED` (Global: `ARTISTIC_REVISION_REQUIRED`, `PENDING_CREATOR`)  
**Data/Hora:** 2026-10-29T18:00:00Z  
**Revisor:** Gemini 3.8 Flash (High) via Antigravity QA Independente  
**Recursos Utilizados:** 0 chamadas PixelLab de produção nesta revisão; custo LLM não informado.

---

## 1. Escopo e Objeto de Revisão

Esta auditoria independente avaliou a propagação do ciclo completo de espada traseira esquerda (**`back_l/Sword`**, 12 quadros, 730 ms), entregue pelo Especialista de Pegada (`7db0e7b6-ab88-49e9-9362-a19121c8ebf5`) em `characters/orc-v1/source/combat-rescue-v5/rear-grip-flash/full-back-l-sword/`.

### Contexto do Pacote:
- A base corporal utilizada foi o clipe `back_l-Sword-full` já aprovado formalmente por este painel de QA como `READY_FOR_REAR_GRIPS` em `experiments/main-orc-combat-rescue-v5/qa-antigravity-flash/rear-bodies-repair1-result.json` (SHA-256 `74da046b...`).
- Escopo rigorosamente delimitado a `back_l/Sword`. Não aprova os outros dois clipes traseiros sem pegada (`back_r/Sword`, `back_l/Axe`), a matriz global de 28 células ou qualquer integração em `../TacticsRPG`.

---

## 2. Verificação de Fontes e Hashes SHA-256 no Disco

| Arquivo / Ativo | Caminho Relativo | SHA-256 Confirmado no Disco | Status |
|---|---|---|:---:|
| **Clip Manifesto** | `.../full-back-l-sword/clip.json` | `9a7b2b3ba87027d3ac7e0e1a86582a9769549f6154800b87a572ab460a9497ef` | **MATCH** |
| **Mestre Composto (256, 4 camadas)** | `.../full-back-l-sword/source/composite.aseprite` | `d052b9910e96961c4386fd0b22f26e4d8f5cc324fdab41912368a26fc814cedb` | **MATCH** |
| **Mestre Corpo (256, 1 camada)** | `.../full-back-l-sword/source/body.aseprite` | `f2deef7c77155bc2b3424e25c19b8bb50dbfb6f81d4061711ddc161b97e9b931` | **MATCH** |
| **Mestre Luva/Mão (256, 1 camada)** | `.../full-back-l-sword/source/hand.aseprite` | `c16ea537a09ff8012a1e2d059afd5eb5297157bbc3e8f1c8bfb547c7bbadd130` | **MATCH** |
| **Mestre Nativo (128, 1 camada)** | `.../full-back-l-sword/source/native.aseprite` | `d9280bbfae61e229eb098bf211de2186d36fa9fa9c9dbbd477f79980a8b13b7c` | **MATCH** |
| **Tira Composta 256 (3072×256)** | `.../full-back-l-sword/composite-strip.png` | `5ad2beb39975f4fa4a3a2fdd627bf6b0c5299b6e97033e6a7d8b097b797e2202` | **MATCH** |
| **Tira Nativa Composta 128 (1536×128)** | `.../full-back-l-sword/native-composite-strip.png` | `23bb8f5851d900ea4279ebd7539126c03737438b7f16447792a64a452d9a3000` | **MATCH** |
| **Tira Nativa Corpo 128 (1536×128)** | `.../full-back-l-sword/native-strip.png` | `3aaf3d82b5dffc0b057b3af4b04a8cb3ce36e957925ebd2e34b361b56a8f7873` | **MATCH** |

---

## 3. Auditoria dos Contratos Declarados

### 3.1 Preservação Absoluta do Corpo Base (`bodyRgbaDelta == 0`)
- **Conferência Pixel a Pixel:** Todos os 12 quadros corporais (`layers/body/00.png`..`11.png`) foram comparados contra `body-specialist/final-cycles/repair1/back_l-Sword-full/body256/`:
  - **100% byte-idênticos** no canvas 256×256.
  - **0 pixels de discrepância RGBA** nas versões nativas 128×128 (`native/00.png`..`11.png`).
- **Timing:** As durações por quadro preservam fielmente `[40, 60, 60, 70, 70, 40, 40, 90, 70, 70, 60, 60] ms`, totalizando 730 ms.

### 3.2 Preservação das Chaves Estruturais F03, F04 e F07
- As chaves estruturais aprovadas anteriormente foram conferidas na fonte:
  - **F03 (`01-hoist`):** `body256` SHA `5c2f2e19...`, `native128` SHA `4d0063ba...` (**MATCH**).
  - **F04 (`02-apex`):** `body256` SHA `a9a5a860...`, `native128` SHA `206a297a...` (**MATCH**).
  - **F07 (`03-impact`):** `body256` SHA `3736cb7f...`, `native128` SHA `bc3f5c11...` (**MATCH**).

### 3.3 Política Estrita `attack-only-v1` e Bookends
- **Intervalo Visível:** Estritamente `[2, 8]`.
- **Bookends F00, F01, F09, F10, F11:**
  - Camadas `weaponBack`, `weaponFront` e `handFront` possuem **exatamente 0 pixels não transparentes**.
  - O composto 256 nesses quadros é **100% byte-idêntico** ao corpo base desarmado.
  - O retorno neutro pós-impacto (F09..F11) é limpo, sem resíduos flutuantes ou marcas pintadas no corpo.

### 3.4 Composição em 4 Camadas e Mestres Aseprite
- Verificado via álgebra de pixels que `((weaponBack OVER body) OVER weaponFront) OVER handFront` reproduz fielmente os quadros compostos em todos os 12 quadros (**`alphaOverMatch: true`**).
- Os 4 mestres Aseprite gerados pelo script Lua oficial (`author.lua`) foram salvos e reexportados em perfil isolado, estando íntegros no disco.

---

## 4. Julgamento Artístico e Inspeção de Pixels

### 4.1 Cinemática da Espada e Coerência do Corte Diagonal
- **Item Autêntico:** O clipe utiliza os dados exatos da Espada do Recruta (`combat/weapons/Sword/weapon.json` SHA `7c090d89...` e `recruit-sword.png` SHA `2ea4c436...`), com dimensões 96×96, âncora `[48, 66]` e seção de empunhadura `[60, 70]`. Não é machado relabelado.
- **Arco de Corte Diagonal Suave:** A trajetória angular segue uma progressão física e cinemática natural:
  - F02: 10° (elevação inicial da lâmina ao lado do ombro direito)
  - F03: 350° / -10° (preparação alta junto à cabeça/pescoço)
  - F04: 320° / -40° (estocada/descida inicial do golpe diagonal no quadrante noroeste)
  - F05: 285° / -75° (corte descendente varrendo a linha dorsal)
  - F06: 265° / -95° (cruzamento profundo da linha média do tronco)
  - F07: 245° / -115° (impacto final com braço estendido baixo-esquerda)
  - F08: 240° / -120° (desaceleração e recuo baixo acima do chão)
- A trajetória é contínua e sem reversões bruscas ou saltos de profundidade.

### 4.2 Envoltório da Luva, Cabo e Pomo
- Em todos os quadros armados (F02..F08), a luva de couro marrom na camada `handFront` cobre a seção central da empunhadura, perfeitamente alinhada ao punho e antebraço.
- O pomo circular metálico é visível e claro, projetando-se além da mão de forma anatômica.
- A guarda transversal de aço situa-se perpendicular à lâmina sem flutuar.
- O braço esquerdo anatômico (à esquerda da imagem) permanece inativo e estendido para equilíbrio, sem contaminação por arma.

### 4.3 Folga em Relação ao Solo (`groundY = 190`)
- No ponto de impacto e extensão máxima (F07), o pixel mais baixo da arma alcança `Y = 174` (**16 pixels acima do chão**).
- No repouso baixo de desaceleração (F08), o pixel mais baixo alcança `Y = 179` (**11 pixels acima do chão**).
- A folga é visualmente convincente para uma espada que corta próximo ao solo, sem qualquer penetração subterrânea, flutuação excessiva ou colisão com os pés/pernas.

### 4.4 Legibilidade em Escala Tática (64px)
- A silhueta e o contraste da lâmina (com seu fuller central escurecido e bordas claras de aço polido) permanecem legíveis em escala tática reduzida (64×64), conforme verificado em `before-after-tactical.png`.

---

## 5. Auditoria Quadro a Quadro

| Quadro | Fase | Duração | Visível | HandFront Px | Bbox Arma [x1, y1, x2, y2] | Delta Corpo | Veredito |
|:---:|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **F00** | guard | 40 ms | Não | 0 px | N/A | 0 px | **PASS** |
| **F01** | chamber-init | 60 ms | Não | 0 px | N/A | 0 px | **PASS** |
| **F02** | hoist-lift | 60 ms | Sim | 74 px | [152, 50, 177, 120] | 0 px | **PASS** |
| **F03** | 01-hoist (key) | 70 ms | Sim | 89 px | [144, 34, 169, 104] | 0 px | **PASS** |
| **F04** | 02-apex (key) | 70 ms | Sim | 100 px | [137, 77, 185, 133] | 0 px | **PASS** |
| **F05** | slash-cleave | 40 ms | Sim | 52 px | [108, 101, 177, 127] | 0 px | **PASS** |
| **F06** | slash-descent | 40 ms | Sim | 58 px | [91, 108, 162, 133] | 0 px | **PASS** |
| **F07** | 03-impact (key) | 90 ms | Sim | 93 px | [97, 141, 162, 174] | 0 px | **PASS** |
| **F08** | recover-low | 70 ms | Sim | 64 px | [101, 140, 163, 179] | 0 px | **PASS** |
| **F09** | recover-pelvis | 70 ms | Não | 0 px | N/A | 0 px | **PASS** |
| **F10** | recover-guard | 60 ms | Não | 0 px | N/A | 0 px | **PASS** |
| **F11** | guard-return | 60 ms | Não | 0 px | N/A | 0 px | **PASS** |

---

## 6. Limitações e Fronteiras Explícitas

1. **Inspeção Multimodal Estática e Funcional:** A auditoria baseou-se na inspeção de alta resolução de todos os quadros discretos, tiras compostas, recortes 4× da pegada e player Chromium a 1× e 0.5×. A percepção final como jogador de peso e ritmo fluido em tempo real em um motor de jogo continua sendo prerrogativa exclusiva da homologação do Criador.
2. **Escopo Restrito:** Esta aprovação aplica-se **exclusivamente a `back_l/Sword`**. Não aprova automaticamente os outros dois clipes traseiros sem pegada (`back_r/Sword`, `back_l/Axe`), a matriz global de 28 células ou qualquer integração em `../TacticsRPG`.
3. **Status Artístico Global:** Permanece inalterado como `ARTISTIC_REVISION_REQUIRED` (`PENDING_CREATOR`).
