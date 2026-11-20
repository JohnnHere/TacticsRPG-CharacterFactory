# Relatório de Reparo Artístico — Três Ciclos Traseiros Desarmados (Repair 1)

**Status de Paragem:** `BODY_THREE_REPAIR1_READY`  
**Empacotamento Técnico:** `TECHNICALLY_COMPLETE`  
**Status Artístico Local:** `VISUAL_REVIEW_REQUIRED`  
**Status Artístico Global:** `ARTISTIC_REVISION_REQUIRED` (Preservado / Inalterado)  
**Status do Criador:** `PENDING_CREATOR`  
**Destinatário da Re-Revisão Independente:** MESMA sessão de QA (`863ae631-5582-4955-a0ef-020d51692fbb` / Gemini 3.8 Flash via Antigravity)  

---

## 1. Contexto e Admissão dos Defeitos Confirmados

No primeiro freeze dos intermediários corporais (`BODY_THREE_FULL_READY`), o QA Independente realizou a auditoria detalhada (`experiments/main-orc-combat-rescue-v5/qa-antigravity-flash/full-rear-bodies-result.json` e `report.md`) e reprovou tecnicamente os três clipes apontando três defeitos concretos:
1. **REAR-01 (HIGH — `back_r-Sword` F06):** Rastro curvo de corte (*blade swoosh trail*) pintado diretamente no cel do corpo com 272 pixels claros de branco/ciano estendendo-se do ombro (`x=105, y=20`) através do saiote de malha até a perna direita (`x=30, y=110`).
2. **REAR-02 (HIGH — `back_l-Axe` F02):** Machado embutido no próprio corpo desarmado: lâmina de ferro em `x=85..108, y=5..22` e cabo marrom em `x=70..85, y=16..18`.
3. **REAR-03 (MEDIUM — `back_l-Sword` F05):** Gancho/filamento vertical preto de 7-10 pixels projetando-se acima do ombro direito em `x=94..98, y=28..33`.

### Correção de Diagnóstico e Limite de Testes Automatizados
O atestado anterior do DEV de "100% desarmado e zero resíduos" foi um **falso positivo** decorrente de scripts baseados unicamente em limiares de luminância global e máscaras binárias. A IA de interpolação gerou armas e rastros cromáticos mesclados à paleta de armadura do corpo. Este DEV reconhece expressamente o erro metodológico anterior: igualdade de camadas e testes estatísticos globais não comprovam ausência semântica de armas; **a inspeção visual estrita de camadas desligadas (*layers-off*) é indispensável e confirmou integralmente os três apontamentos do QA.**

Todos os reparos foram executados cirurgicamente no **Aseprite 1.3.18.6** em modo batch via scripts Lua, em novos diretórios isolados (`repair1`), preservando todos os arquivos e mestres originais rejeitados e as 9 chaves estruturais aprovadas.

---

## 2. Detalhamento Cirúrgico das Correções de Pixel

### 2.1. REAR-01: Remoção de Swoosh e Reconstrução Têxtil (`back_r-Sword` F06)
- **Causa Raiz:** Na descida rápida do golpe diagonal (F06, 40 ms), a geração da IA introduziu uma curva de movimento simulando o brilho da espada cortando o ar.
- **Análise Anatômica:** O rastro cortava o fundo transparente e cruzava o saiote de couro marrom-avermelhado e a borda da perna. Apagar simplesmente os pixels causaria buracos transparentes na silhueta do Orc.
- **Correção Executada (Aseprite Lua):**
  - Pixels de swoosh no ar transparente (`y=15..52, x=94..101` e `y=65..73, x=104..113`) foram limpos para transparência pura `rgba(0,0,0,0)`.
  - No corpo (`y=87..97, x=45..62`), o material da túnica de couro vermelho-marrom foi reconstruído preenchendo a fenda entre os tecidos adjacentes com as cores canônicas `#592d2b` (`rgb(89, 45, 43)`) e `#34181e` (`rgb(52, 24, 30)`).
  - A costura de cota de malha em `y=81..86, x=55..65` foi restaurada com cinza escuro `#1f1c24` e realce de cota `#413f4c`.
  - A panturrilha interna (`y=98..100, x=48..56`) e o vão anatômico entre pernas/bota (`y=101..110, x=30..42`) foram fechados com o contorno escuro autêntico `#030304`.
- **Resultado Quantitativo:**
  - 486 pixels modificados.
  - Contagem de pixels hiper-brilhantes (`r,g,b > 180`): reduziu de **284 para 4** (apenas pontos legítimos de reflexo especular na ombreira de aço).
  - Bounding box anatômico: `(16, 13, 113, 127)`. Zero vazamento ou buraco.

### 2.2. REAR-02: Remoção de Machado e Reconstrução do Punho Cerrado (`back_l-Axe` F02)
- **Causa Raiz:** Na pose preparatória de carregamento (F02, 90 ms), a IA desenhou uma cabeça de machado de dois gumes com cabo de madeira marrom repousando sobre o trapézio e ombro direito.
- **Análise Anatômica:** O braço direito do Orc estava flexionado preparando o hoist. Era mandatório remover a arma sem amputar o braço nem criar um contorno truncado.
- **Correção Executada (Aseprite Lua):**
  - Lâmina de ferro em projeção no ar (`y=5..15, x=70..114` e `y=16..22, x=93..114`) eliminada para transparência binária completa.
  - Cabo de madeira marrom (`y=16..18, x=73..83`) removido sobre o trapézio, restaurando o contorno da ombreira traseira.
  - Reconstrução completa da mão/manopla direita cerrada erguida em `x=83..92, y=15..20`, conectada organicamente ao antebraço e ombro. Foram utilizados exclusivamente tons da paleta de couro do Orc V1: contorno `#020203`, sombra interna `#261b17`, corpo da luva `#39241b`, e realce superior `#392b1f`.
- **Resultado Quantitativo:**
  - 703 pixels modificados.
  - Bounding box: topo retraído de `y=5` (antiga ponta do machado) para `y=9` (ápice do punho cerrado/ombreira); lateral leste retraída de `x=111` para `x=104`.
  - Braço e manopla inteiramente preservados e anatomicamente contínuos com a cadeia do ombro.

### 2.3. REAR-03: Remoção do Gancho Preto (`back_l-Sword` F05)
- **Causa Raiz:** Artefato de filamento isolado deixado pela interpolação da IA na descida (F05, 70 ms), projetando-se 7 a 10 pixels verticalmente acima do aço da ombreira.
- **Correção Executada (Aseprite Lua):**
  - Remoção cirúrgica dos 10 pixels pretos residuais em `y=28..33, x=94..98`.
  - Preservação intacta da linha de cume da ombreira em `y=34`.
- **Resultado Quantitativo:**
  - 30 pixels modificados.
  - Contorno liso e natural do ombro restaurado sem nenhuma afetação à anatomia ou armadura.

---

## 3. Matriz de Evidência Diferencial (Before vs After)

Os dados abaixo foram extraídos diretamente de `before-after-diff.json` gerado pela ferramenta analítica Python:

| Defeito | Ciclo & Quadro | Pixels Alterados | Bounding Box Anterior | Bounding Box Corrigido | Pixels Brilhantes Antes | Pixels Brilhantes Depois |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **REAR-01** | `back_r-Sword` F06 | **486** | `(16, 13, 113, 127)` | `(16, 13, 113, 127)` | 284 | **4** (especular normal) |
| **REAR-02** | `back_l-Axe` F02 | **703** | `(23, 5, 111, 127)` | `(23, 9, 104, 127)` | 46 | **19** (couro/aço) |
| **REAR-03** | `back_l-Sword` F05 | **30** | `(23, 13, 114, 127)` | `(23, 13, 114, 127)` | 2 | **1** |

Imagens compostas de comparação lado a lado geradas em:
- `experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/repair1/back_r-Sword-f06-before-after.png`
- `experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/repair1/back_l-Axe-f02-before-after.png`
- `experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/repair1/back_l-Sword-f05-before-after.png`

---

## 4. Preservação Criptográfica das 9 Chaves Aprovadas pelo QA

Nenhuma das 9 chaves estruturais aceitas foi tocada. As chaves residem nos índices **F03** (`01-hoist`), **F04** (`02-apex`) e **F07** (`03-impact`), mantendo **100% de paridade byte-a-byte (SHA-256 rigorosamente idêntico)**:

| Ciclo | Quadro | Nome da Chave | SHA-256 Aceito pelo QA | SHA-256 no Pacote Repair1 | Byte Exact | Pixel Exact |
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

## 5. Contabilidade de Gerações e Saldo

- **Saldo no Freeze Anterior:** 1342.70 gerações
- **Saldo Atual no Pacote Repair 1:** **1342.70 gerações**
- **Gerações Consumidas no Reparo:** **0.0 gerações**  
  *Todo o trabalho de correção foi cirúrgico e executado 100% em ambiente local no Aseprite via Lua. Nenhuma chamada de API ou crédito PixelLab foi gasto.*

---

## 6. Mestres e Empacotamento Técnico em `repair1`

Todos os novos mestres `.aseprite` e exportações foram gerados em modo batch e verificados via script Lua com o perfil exclusivo `tmp/aseprite-final-body-flash-profile`:
- **`native128.aseprite`:** Canvas 128×128, camada única `body`, linha de chão constante em `y=126`, durações de frames em segundos (ex: 0.040s, 0.060s, etc.).
- **`body256.aseprite`:** Canvas 256×256, cel em `Point(64, 64)`, linha de chão em `y=190`, camada única `body`.
- **PNGs:** Frames individuais `native/00..11.png`, `body256/00..11.png` e tiras de contato `native-strip.png` e `body256-strip.png`.
- **Contratos:** `clip.json` e `representative.json` atualizados em cada ciclo com hashes SHA-256 e metadados de reparo.
- **Estruturas Espelhadas:**
  - `characters/orc-v1/source/combat-rescue-v5/body-specialist/final-cycles/repair1/`
  - `experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/repair1/`

---

## 7. Superfície de Revisão Interativa

Foi montado um estúdio interativo completo contendo:
- **Master Review Studio:** `experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/repair1/review.html`
- **Seção Diferencial Visual (Side-by-Side):** Comparações diretas dos quadros reparados F06, F02 e F05 antes e depois do conserto.
- **Player Interativo:** Reprodução em tempo real 1.0× (jogo), 0.75×, 0.5× e 0.25×, além de controle passo a passo quadro a quadro.
- **Três Escalas Simultâneas:** 3× Diagnóstico (384×384), 1× Nativo (128×128) e 0.5× Tático (~64×64).
- **Estúdios Dedicados:** `review.html` em cada pasta individual de ciclo.

> [!NOTE]
> **Aviso Perceptual Obrigatório:** Este DEV realizou a conferência quadro a quadro em repouso e a validação analítica das matrizes de pixel, do alinhamento de solo (`y=126`), das durações nominais e da integridade criptográfica. Este relatório não simula parecer de QA independente nem declara percepção contínua cinematográfica em 1×, a qual cabe exclusivamente à sessão de QA designada e ao Criador.

---

## 8. Preservação de Escopo e Handoff

- **Nenhuma alteração externa:** Os arquivos em `../TacticsRPG`, commits do Git, e `equipment-current.json` permanecem completamente intocados.
- **Nenhuma interferência com empunhaduras (grips):** Nenhuma camada de arma ou pegada traseira foi introduzida nesta etapa, reservada estritamente à especialidade subsequente sobre a base validada.
- **Ponto de Parada:** O DEV conclui a etapa e para em **`BODY_THREE_REPAIR1_READY`**, submetendo o pacote `repair1` ao Root para reavaliação pelo **MESMO revisor QA Independente** (`863ae631-5582-4955-a0ef-020d51692fbb` / Gemini 3.8 Flash via Antigravity).
