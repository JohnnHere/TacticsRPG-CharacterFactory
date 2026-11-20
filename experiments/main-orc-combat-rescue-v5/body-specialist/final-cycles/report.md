# Relatório de Produção Artística — Três Ciclos Traseiros Desarmados

**Status:** `BODY_THREE_FULL_READY`  
**Empacotamento Técnico:** `TECHNICALLY_COMPLETE`  
**Status Artístico Local:** `VISUAL_REVIEW_REQUIRED`  
**Status Artístico Global:** `ARTISTIC_REVISION_REQUIRED` (Preservado / Inalterado)  
**Status do Criador:** `PENDING_CREATOR`  
**Destinatário da Revisão Independente:** MESMA sessão de QA (`863ae631-5582-4955-a0ef-020d51692fbb` / Gemini 3.8 Flash via Antigravity)  

---

## 1. Escopo e Execução da Tarefa

Conforme instrução expressa para o **DEV ARTÍSTICO de continuação bem delimitada**, esta entrega conclui a interpolação e montagem completa dos **três ciclos corporais traseiros desarmados**:
1. `back_r / Sword` (12 quadros, 730 ms total)
2. `back_l / Sword` (12 quadros, 730 ms total)
3. `back_l / Axe` (12 quadros, 1100 ms total)

O ciclo referencial prévio `full-back-r-axe` (12 quadros, 1100 ms) em `characters/orc-v1/source/combat-rescue-v5/body-specialist/full-back-r-axe/` foi rigorosamente preservado como prior art canônico e **não foi reautorado**.

---

## 2. Preservação Rigorosa das 9 Chaves Aceitas pelo QA

As nove chaves estruturais aprovadas com o veredito `READY_FOR_NEXT_STAGE` pelo QA Independente em `experiments/main-orc-combat-rescue-v5/qa-antigravity-flash/qa-result.json` foram incorporadas com **100% de paridade RGBA e integridade byte-a-byte (SHA-256 idêntico)** nos índices exatos de cada ciclo:
- **F03:** Key 01 (`01-hoist`) — Elevação preparatória
- **F04:** Key 02 (`02-apex`) — Ponto mais alto / início da trajetória de corte
- **F07:** Key 03 (`03-impact`) — Posição de impacto / término do golpe

### Matriz de Verificação Criptográfica das Chaves

| Ciclo | Quadro | Nome da Chave | SHA-256 Esperado (QA Accepted) | SHA-256 Exportado (native/xx.png) | Byte Exact | Pixel Exact |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: |
| `back_r / Sword` | F03 | 01-hoist | `a573c039202f52315eb681da5fe375199b34fa101a1f9404b8c9263920589ff2` | `a573c039202f52315eb681da5fe375199b34fa101a1f9404b8c9263920589ff2` | **SIM** | **SIM** |
| `back_r / Sword` | F04 | 02-apex | `9607fb5c7f36b1dcd7649eba505d5eca925f2abb670d636f8a235c42c6cbb40d` | `9607fb5c7f36b1dcd7649eba505d5eca925f2abb670d636f8a235c42c6cbb40d` | **SIM** | **SIM** |
| `back_r / Sword` | F07 | 03-impact | `ac51e08bdd1cc40de255f5233d08f79916c8112b2b9c68b00eee8c509f204107` | `ac51e08bdd1cc40de255f5233d08f79916c8112b2b9c68b00eee8c509f204107` | **SIM** | **SIM** |
| `back_l / Sword` | F03 | 01-hoist | `4d0063ba3ec21af78fb490ff4f80c48ec71f5663316c9afd6fa60c4689884096` | `4d0063ba3ec21af78fb490ff4f80c48ec71f5663316c9afd6fa60c4689884096` | **SIM** | **SIM** |
| `back_l / Sword` | F04 | 02-apex | `206a297a862278cc21649f8613199cc304d58ec1b771c97c652b09c57fb40f30` | `206a297a862278cc21649f8613199cc304d58ec1b771c97c652b09c57fb40f30` | **SIM** | **SIM** |
| `back_l / Sword` | F07 | 03-impact | `bc3f5c1102377ffeba631dfef93d843bf1c12d431f4b016286c1c2a7bad147f1` | `bc3f5c1102377ffeba631dfef93d843bf1c12d431f4b016286c1c2a7bad147f1` | **SIM** | **SIM** |
| `back_l / Axe` | F03 | 01-hoist | `d240b9ac537499625f7a86fcbfcf8cf2287b26947dc164092a76f313196c79ce` | `d240b9ac537499625f7a86fcbfcf8cf2287b26947dc164092a76f313196c79ce` | **SIM** | **SIM** |
| `back_l / Axe` | F04 | 02-apex | `7adfd9f45be25ce862d261f4bf6e47881e52043969605acf9cd4f918c9e00d56` | `7adfd9f45be25ce862d261f4bf6e47881e52043969605acf9cd4f918c9e00d56` | **SIM** | **SIM** |
| `back_l / Axe` | F07 | 03-impact | `7a0c943c51f555f683ba78913150190e9b375a0091714644129b6fef7ea8c1a0` | `7a0c943c51f555f683ba78913150190e9b375a0091714644129b6fef7ea8c1a0` | **SIM** | **SIM** |

---

## 3. Contabilidade Rigorosa de Gerações PixelLab

- **Saldo Inicial no Checkpoint:** 1351.70 gerações
- **Saldo Final Confirmado:** 1342.70 gerações
- **Total Consumido:** Exatamente **9.0 gerações** (3 bridges × 3 ciclos, sem retrabalho, compras ou chamadas extras)

### Detalhamento dos Jobs:
1. `back_r / Sword` — Entry (`2e5f7343-77af-474d-adec-1ab75b938005`, seed 310101): 1.0 gen
2. `back_r / Sword` — Descent (`815bb8a5-b497-4298-ac23-4f514df811fe`, seed 310102): 1.0 gen
3. `back_r / Sword` — Recovery (`2bc3999a-36ad-4499-9451-6c074ea379c6`, seed 310103): 1.0 gen
4. `back_l / Sword` — Entry (`3e835e9c-673f-4f9d-a412-bf91a5de7edd`, seed 310201): 1.0 gen
5. `back_l / Sword` — Descent (`e11da933-c68b-4fbb-9942-0270c16a564a`, seed 310202): 1.0 gen
6. `back_l / Sword` — Recovery (`e976e860-6873-4dec-a119-0268b15613cf`, seed 310203): 1.0 gen
7. `back_l / Axe` — Entry (`7c0b1ca2-c9af-420b-9fb5-c0e606650b00`, seed 310301): 1.0 gen
8. `back_l / Axe` — Descent (`6f8e537c-60db-4504-a5d5-400b4cf0eb29`, seed 310302): 1.0 gen
9. `back_l / Axe` — Recovery (`3061a847-428c-4dad-a57e-bed16eb34720`, seed 310303): 1.0 gen

Todos os arquivos de request (`request-entry.json`, etc.), recibos de polling (`poll-*.json`) e imagens puras geradas foram arquivados em suas respectivas pastas em `experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/`.

---

## 4. Autoria Técnica e Mestres no Aseprite

Toda a montagem de mestres, cels, tiras de contato e frames individuais ocorreu exclusivamente via **Aseprite 1.3.18.6** em modo batch (`--batch --noinapp`) utilizando o perfil exclusivo isolado `tmp/aseprite-final-body-flash-profile`.

### Estrutura de Artefato por Ciclo (espelhada em `characters/` e `experiments/`):
- `native128.aseprite`: Canvas 128×128, camada única `body`, linha de chão constante em `y=126`, durações em segundos atribuídas nativamente via Lua.
- `body256.aseprite`: Canvas 256×256, cel posicionado exatamente em `Point(64, 64)`, linha de chão em `y=190`, camada única `body`.
- `native/00.png` a `native/11.png`: Frames individuais 128×128 nativos.
- `body256/00.png` a `body256/11.png`: Frames individuais 256×256 compostos.
- `native-strip.png` (1536×128) e `body256-strip.png` (3072×256): Tiras de contato sequenciais.
- `clip.json` e `representative.json`: Contratos canônicos de clipe e representação com todos os caminhos, tempos, SHA-256 e metadados.

### Tempos e Ritmo dos Ciclos:
- **Espada (`back_r` e `back_l`):** 12 quadros, **730 ms**  
  `[40, 60, 60, 70, 70, 40, 40, 90, 70, 70, 60, 60] ms`  
  *Entrada rápida (0-160ms) → Preparação (160-300ms) → Golpe cortante diagonal acelerado (300-380ms) → Impacto firme (380-470ms) → Recuperação equilibrada e retorno à guarda neutra (470-730ms).*
- **Machado (`back_l`):** 12 quadros, **1100 ms**  
  `[70, 80, 90, 100, 110, 50, 60, 110, 100, 100, 100, 130] ms`  
  *Carregamento pesado de peso nas pernas e dorsal (0-340ms) → Ápice erguido (340-450ms) → Descida vertical veloz de esmagamento (450-560ms) → Impacto profundo com joelhos dobrados e pelve rebaixada (560-670ms) → Rebound e recuperação pesada do tronco (670-1100ms).*

---

## 5. Inspeção Semântica e Conformidade Layers-Off

1. **Layers-off Rigoroso:** Cada quadro foi auditado individualmente. O corpo está 100% desarmado. Zero pixels de armas, lâminas, hastes ou discos estranhos desenhados sobre o tronco, peitoral ou costas. `weaponVisible: false` em 100% dos quadros nos contratos.
2. **Dominância Anatômica Direita:** O braço direito anatômico é o membro executor do ataque em ambas as vistas (`back_r` com visão noroeste do dorso, `back_l` com visão nordeste do dorso). Não houve espelhamento de sprites.
3. **Braço Inativo Dinâmico:** O braço esquerdo anatômico atua ativamente como contrapeso cinético em todas as fases, flexionando ombro, cotovelo e luva naturalmente sem repetição estática de coluna congelada.
4. **Continuidade Articular:** Cadeia ombro-cotovelo-punho contínua e orgânica ao longo de toda a subida, descida e follow-through.
5. **Cavidade e Espaço Negativo:** A cavidade triangular entre cabeça e braço erguido no machado (`back_l/Axe`) mantém transparência binária perfeita (0 pixels residuais cinzas/artefatos).
6. **Integridade da Luva de Impacto:** No impacto de espada em ambas as vistas (F07), a manopla de couro marrom/vinho do punho direito mantém separação visual nítida em relação à placa do tasset e quadril, eliminando o antigo defeito BODY-01 de fusão.
7. **Construção Traseira Pura:** Crânio occipital verde sem olhos, presas ou elementos faciais vazados; placa dorsal, costura vertebral e correias traseiras construídas anatomicamente.

---

## 6. Ferramentas de Revisão Interativa

Foi criado um **Master Review Studio** e estúdios dedicados em:
- **Master Studio:** `experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/review.html`
- **Dedicados:**
  - `experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/back_r-Sword-full/review.html`
  - `experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/back_l-Sword-full/review.html`
  - `experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/back_l-Axe-full/review.html`

**Recursos de Inspeção no Studio:**
- Reprodução 1.0× (tempo real de jogo), 0.5× (câmera lenta) e 0.25× (super slow motion).
- Navegação quadro a quadro (passo a passo para frente e para trás).
- Barra de seek interativa (F00..F11).
- Visualização simultânea em 3 escalas: 3× Diagnóstico (384×384), 1× Nativo (128×128) e 0.5× Tático (64×64).
- Tira de quebra de quadros com identificação de chaves aceitas `[QA KEY]` e tempos nominais.

> [!NOTE]
> **Aviso Perceptual Obrigatório:** A inspeção realizada neste DEV foi discreta e analítica (quadro a quadro, bounding boxes, paridade de canais RGBA, tempos em segundos e contratos de arquivos). A percepção contínua da fluidez natural em 1× em tempo real cabe exclusivamente à avaliação do QA Independente e posterior decisão do Criador.

---

## 7. Arquivos e Manifestos Entregues

- `experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/patch-manifest.json`: Manifesto das 3 células com caminhos, tempos e SHA-256 dos clipes.
- `experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/checkpoint.json`: Checkpoint completo com contabilidade de gerações, targets de QA e status de paragem.
- `characters/orc-v1/source/combat-rescue-v5/body-specialist/final-cycles/`: Diretório de produção canônico contendo os mestres `.aseprite`, PNGs nativos/compostos e contratos `clip.json`/`representative.json`.

---

## 8. Handoff e Parada

- O pacote local atinge a marcação **`BODY_THREE_FULL_READY`**.
- Nenhuma escrita foi realizada em `../TacticsRPG`, commits do git ou no arquivo de produção ativa `equipment-current.json`.
- A próxima etapa autorizada é a avaliação independente deste freeze pelo **MESMO revisor QA** (`863ae631-5582-4955-a0ef-020d51692fbb` / Gemini 3.8 Flash via Antigravity).
