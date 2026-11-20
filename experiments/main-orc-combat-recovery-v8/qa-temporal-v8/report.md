# Laudo de QA Temporal Independente — Re-verificação Pós-Correções (V8)

- **Candidato:** `characters/orc-v1/source/combat-recovery-v8/candidate28manifest.json`
- **Hash do Manifesto Atualizado (SHA-256):** `0bd01b9b4b6c2a05204fe8326dd8e46d7c92982adc48675068fd3e825e379140`
- **Avaliador:** QA TEMPORAL Independente
- **Tipo de Execução:** Re-verificação independente após reconstrução do manifesto e correções de células.
- **Métricas estruturadas:** [metrics.json](file:///C:/Users/João%20Orlando/Documents/Projetos%20Unity/TacticsRPG-CharacterFactory/experiments/main-orc-combat-recovery-v8/qa-temporal-v8/metrics.json)

---

## 1. Auditoria Independente das Três Mudanças Concretas

O manifesto reconstruído alterou três componentes centrais, verificados aqui por medição raster e estrutural própria:

### Mudança 1: Reconstrução de `back_r/Sword` (`characters/orc-v1/source/combat-recovery-v8/rear-fix/back_r-sword/clip.json`)
- **Status:** **VERIFICADO E CORRIGIDO**
- **Evidências numéricas e estruturais:**
  1. **Eliminação dos quadros congelados (0.00 px):**
     - No V8 anterior (`rear/back_r-sword`), os quadros F04==F05 eram byte-idênticos (SHA-256 do corpo `15fe83525d`, arma `500510bc33`), paralisando o orc por 110 ms; e F09==F10 eram byte-idênticos (corpo `72fdedde33`, arma `e32e5dbc61`), paralisando o orc por 135 ms.
     - No V8 corrigido (`rear-fix/back_r-sword`), **todos os 13 quadros possuem hashes SHA-256 únicos**:
       - F04 (corpo `15fe83525d`, arma `500510bc33`) $\to$ F05 (corpo `c3239ed590`, arma `1220757bcd`): **deslocamento de 3.18 px** de `(156.5, 60.5)` para `(153.3, 61.1)`. Congelamento no ápice eliminado.
       - F09 (corpo `72fdedde33`, arma `e32e5dbc61`) $\to$ F10 (corpo `3683ec168e`, arma `e914a41489`): **deslocamento de 8.86 px** de `(187.9, 157.0)` para `(192.7, 149.6)`. Congelamento na recuperação eliminado.
  2. **Restauração da fase do maior passo cinético:**
     - No clipe anterior, o maior passo ocorria incorretamente na transição F06 $\to$ F07 (68.53 px), atrasado na fase de impacto.
     - No clipe reconstruído, o maior passo ocorre em **F05 $\to$ F06 (`apex-hold` $\to$ `slash-release`) = 73.23 px**, alinhando-se com a fase de pico das outras três direções (`front_r`: 75.99 px, `front_l`: 75.99 px, `back_l`: 56.82 px).
     - O passo de descida subsequente (F06 $\to$ F07) passa a ser de 57.92 px.

### Mudança 2: Reparo da Axila em `front_l/Sword` (`characters/orc-v1/source/combat-recovery-v8/frontal-armpit/front_l-sword/clip.json`)
- **Status:** **VERIFICADO E CONFIRMADO (REPARO ESTRITAMENTE ESTÁTICO)**
- **Evidências de medição raster:**
  1. **Diff pixel a pixel contra `combat-recovery-v7/frontal/front_l-Sword-full`:**
     - Camada `body`: **73 pixels alterados no total**, restritos rigorosamente a 3 quadros:
       - F03: **25 pixels** modificados.
       - F04: **15 pixels** modificados (clareamento na junção axilar em colunas $x=148..155$, $y=106..108$ para tons `[27,28,34]` e `[43,45,49]`).
       - F05: **33 pixels** modificados.
       - F00..F02 e F06..F12: **0 pixels alterados** (100% idênticos).
     - Camada `weaponFront`: **0 pixels alterados** em todos os 13 quadros.
  2. **Impacto temporal:** Zero. As durações, contagem de quadros e o deslocamento F05 $\to$ F06 da espada permanecem idênticos (75.99 px). O teleporte/flash da espada continua inalterado nesta célula.

### Mudança 3: Sincronização dos Metadados de Impacto (`contactEvent`)
- **Status:** **VERIFICADO E CORRIGIDO**
- **Evidências:**
  1. **Família Sword (todas as 4 direções unificadas):**
     - `front_r/Sword`: `{"frame": 7, "timeMs": 325, "phase": "contact", "status": "CANDIDATE_VISUAL_ONLY", "appliesDamage": false}`
     - `front_l/Sword`: `{"frame": 7, "timeMs": 325, "phase": "contact", "status": "CANDIDATE_VISUAL_ONLY", "appliesDamage": false}`
     - `back_r/Sword`:  `{"frame": 7, "timeMs": 325, "phase": "contact", "status": "CANDIDATE_VISUAL_ONLY", "appliesDamage": false}`
     - `back_l/Sword`:  `{"frame": 7, "timeMs": 325, "phase": "contact", "status": "CANDIDATE_VISUAL_ONLY", "appliesDamage": false}`
     - *A divergência anterior (onde `front_r` marcava erroneamente frame 6 / 290 ms) foi eliminada.*
  2. **Família Axe (todas as 4 direções unificadas):**
     - `front_r/Axe`: `{"frame": 6, "timeMs": 410, "phase": "heavy-impact", "status": "CANDIDATE_VISUAL_ONLY", "appliesDamage": false}`
     - `front_l/Axe`: `{"frame": 6, "timeMs": 410, "phase": "heavy-impact", "status": "CANDIDATE_VISUAL_ONLY", "appliesDamage": false}`
     - `back_r/Axe`:  `{"frame": 6, "timeMs": 410, "phase": "heavy-impact", "status": "CANDIDATE_VISUAL_ONLY", "appliesDamage": false}`
     - `back_l/Axe`:  `{"frame": 6, "timeMs": 410, "phase": "heavy-impact", "status": "CANDIDATE_VISUAL_ONLY", "appliesDamage": false}`
     - *A discrepância dos frontais (que registravam incorretamente 375 ms para o frame 6) foi eliminada.*
  3. Todos os hashes dos PNGs individuais de frames foram preservados byte a byte durante a correção dos metadados.

---

## 2. Tabela Geral de Medição Pós-Correções (8 Células Ativas)

| Célula | Proveniência no Manifesto | Quadros | Duração Total | Grade de Durações (ms) | Janela Armada | `contactEvent` | Maior Passo | Transição Pico |
|---|---|:---:|:---:|---|:---:|:---:|:---:|:---:|
| `front_r/Sword` | `combat-recovery-v7/frontal/full-front-r-sword` | 13 | 730 ms | `[30,65,35,50,45,65,35,35,100,55,80,45,90]` | F02..F10 | F07 · 325 ms | 75.99 px | F05 → F06 (`apex` → `slash`) |
| `front_l/Sword` | `combat-recovery-v8/frontal-armpit/front_l-sword` | 13 | 730 ms | `[30,65,35,50,45,65,35,35,100,55,80,45,90]` | F02..F10 | F07 · 325 ms | 75.99 px | F05 → F06 (`apex` → `slash`) |
| `back_r/Sword`  | `combat-recovery-v8/rear-fix/back_r-sword` | 13 | 730 ms | `[30,65,35,50,45,65,35,35,100,55,80,45,90]` | F02..F10 | F07 · 325 ms | **73.23 px** | **F05 → F06 (`apex` → `slash`)** |
| `back_l/Sword`  | `combat-recovery-v8/rear/back_l-sword` | 13 | 730 ms | `[30,65,35,50,45,65,35,35,100,55,80,45,90]` | F02..F10 | F07 · 325 ms | 56.82 px | F05 → F06 (`apex` → `slash`) |
| `front_r/Axe`   | `combat-recovery-v7/frontal/front_r-Axe-full` | 12 | 1005 ms | `[40,65,35,80,155,35,115,110,130,50,90,100]` | F02..F08 | F06 · 410 ms | 89.89 px | F04 → F05 (`coil` → `cleave`) |
| `front_l/Axe`   | `combat-recovery-v7/frontal/front_l-Axe-full` | 12 | 1005 ms | `[40,65,35,80,155,35,115,110,130,50,90,100]` | F02..F08 | F06 · 410 ms | 89.89 px | F04 → F05 (`coil` → `cleave`) |
| `back_r/Axe`    | `combat-recovery-v8/rear/back_r-axe` | 12 | 1005 ms | `[40,65,35,80,155,35,115,110,130,50,90,100]` | F02..F08 | F06 · 410 ms | 80.19 px | F04 → F05 (`coil` → `cleave`) |
| `back_l/Axe`    | `combat-recovery-v8/rear/back_l-axe` | 12 | 1005 ms | `[40,65,35,80,155,35,115,110,130,50,90,100]` | F02..F08 | F06 · 410 ms | 73.73 px | F04 → F05 (`coil` → `cleave`) |

---

## 3. Estado Atualizado das 7 Afirmações do Orquestrador

1. **Sword 13 quadros / 730 ms idênticos:** **CONFIRMADO.** Grade idêntica em 100% das 4 direções.
2. **Axe 12 quadros / 1005 ms idênticos:** **CONFIRMADO.** Grade idêntica em 100% das 4 direções.
3. **Instante de impacto idêntico nas 4 direções:** **AGORA PLENAMENTE CONFIRMADO.** O instante real e os metadados `contactEvent` coincidem rigorosamente em **325 ms (F07 / 44,52%)** para Sword e em **410 ms (F06 / 40,80%)** para Axe. A antiga assertiva de 290 ms / 375 ms decorria de fórmula falha do script antigo, agora sanada.
4. **Arma oculta em F00 e último quadro:** **CONFIRMADO.** Exatamente 0 pixels em todos os bookends.
5. **Maior passo na mesma fase com magnitudes comparáveis:** **AGORA PLENAMENTE CONFIRMADO NAS DUAS FAMÍLIAS.** Após o rebuild de `back_r/Sword`, todas as 4 direções de Sword têm o pico em F05 $\to$ F06 (56.8 a 76.0 px), e todas as 4 de Axe têm o pico em F04 $\to$ F05 (73.7 a 89.9 px).
6. **Bookends traseiros sem pico de brilho e curva de luma uniforme:** **CONFIRMADO.** 0 a 7 px no corpo dos bookends; lâmina entre 52 e 62 px na Sword e 11 a 17 px no Axe.
7. **Flash frontal é teleporte de 76 px sem pico de luminância:** **CONFIRMADO.** Permanece com 55 a 62 px claros e salto de 75.99 px entre F05 e F06.

---

## 4. Julgamento das Quatro Questões Centrais

### A. A uniformidade temporal entre as quatro direções foi realmente alcançada?
**SIM.**
Com a reconstrução de `back_r/Sword` e o reparo dos metadados `contactEvent`, a uniformidade temporal foi alcançada em todos os seus eixos:
1. **Grade temporal de durações:** 100% idêntica milissegundo a milissegundo nas 4 direções.
2. **Janelas armadas e bookends:** 100% sincronizadas.
3. **Instante de impacto / dano:** 100% alinhado (325 ms na Sword, 410 ms no Axe).
4. **Cinética e fases de aceleração:** 100% alinhado (o maior passo ocorre rigorosamente na mesma fase em todas as vistas de cada arma, e os congelamentos de frames em `back_r/Sword` foram eliminados).

### B. Restou na arte algum artefato de salto, pop-in ou apagão que um jogador veria?
**SIM.**
Embora os congelamentos em `back_r/Sword` tenham sido eliminados, ainda restam artefatos visuais intrínsecos à arte:
1. **Teleporte / "Flash" frontal (`front_r/Sword` e `front_l/Sword` em F05 → F06):** Salto de 75.99 px sem sobreposição de colunas (36 px de vão vazio).
2. **Teleporte no Machado frontal (`front_r/Axe` e `front_l/Axe` em F04 → F05):** Salto oblíquo de 89.89 px em 35 ms.
3. **Pop-in e Pop-out da arma:** Pela política de armas restritas ao ataque (`attack-only`), a arma surge abruptamente em F02 e é extinta em corte seco no início da recuperação.
4. **Corpo paralisado na entrada/saída em `back_r/Axe`:** F01==F02 e F09==F10 mantêm corpos byte-idênticos (100 ms e 140 ms estáticos).
5. **Colapso para repouso em `back_l`:** `back_l/Sword` (F11/F12) e `back_l/Axe` (F10/F11) utilizam o corpo exato do repouso F00.

### C. O flash frontal foi resolvido, atenuado ou continua?
**CONTINUA 100% INALTERADO.**
O reparo feito em `front_l/Sword` foi estritamente estático (sombreamento de 73 pixels na axila do corpo). **Zero pixels mudaram na lâmina**. O salto de 75.99 px permanece byte-idêntico ao V7 em ambas as vistas frontais (`front_r` e `front_l`). Continua sendo o ponto mais agudo de descontinuidade espacial da animação.

---

## 5. Veredito Final Revisado de QA Temporal

### Veredito: **`TEMPORAL_PASS_WITH_RESERVATIONS`**
*(Sob critério estrito de entrega dos objetivos declarados da rodada V8: **`TEMPORAL_FAIL`**)*

**Síntese Avaliativa:**
- **O que foi curado nesta reconstrução:**
  - `back_r/Sword` não possui mais poses duplicadas ou congeladas (13 quadros distintos).
  - O pico cinético da espada traseira direita foi alinhado com as outras direções (F05 $\to$ F06 = 73.23 px).
  - Todos os metadados `contactEvent` agora convergem perfeitamente (F07 / 325 ms na Sword e F06 / 410 ms no Axe).
- **A única reserva impeditiva remanescente:**
  - O **flash frontal da espada (salto de 75.99 px em F05 $\to$ F06) NÃO foi resolvido nem atenuado**. Ele foi mantido na íntegra a partir do V7 protegido. Como a resolução do flash frontal era um dos dois mandatos explícitos do criador para o V8, o candidato não pode obter aprovação irrestrita (`TEMPORAL_PASS`).
