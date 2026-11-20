# Relatório de QA Independente — Ciclo Completo `front_r/Sword` (13f / 730 ms)

**Veredito:** `READY_FOR_MATRIX_REVIEW`  
**Status Técnico:** `TECHNICALLY_COMPLETE`  
**Status Artístico do Pacote:** `VISUAL_REVIEW_REQUIRED` (Global: `ARTISTIC_REVISION_REQUIRED`, `PENDING_CREATOR`)  
**Data/Hora:** 2026-10-29T17:52:00Z  
**Revisor:** Gemini 3.8 Flash (High) via Antigravity QA Independente  
**Recursos Utilizados:** 0 chamadas PixelLab de produção nesta revisão; custo LLM não informado.

---

## 1. Escopo e Histórico da Revisão

Esta auditoria independente avaliou exclusivamente a propagação do ciclo completo de espada frontal direita (**`front_r/Sword`**, 13 quadros, 730 ms), entregue pelo especialista de pegada em `characters/orc-v1/source/combat-rescue-v5/grip-specialist/full-front-r-sword/`.

### Contexto Histórico
- Este era o único dos quatro ciclos frontais que ainda não possuía parecer visual com veredito conclusivo positivo por este painel (os outros três ciclos frontais, `front_l/Sword`, `front_r/Axe` e `front_l/Axe`, foram aprovados anteriormente em `qa-result.json`).
- Um revisor anterior (Sol / GPT-6.1 via Codex) emitiu veredito `INCONCLUSIVE` em `qa-sol/full-front-r-sword-result.json` estritamente devido às limitações de sua própria interface em relação à percepção temporal contínua a 1×, registrando expressamente que **nenhum defeito estático bloqueante de contato, anatomia ou oclusão foi observado**.
- Esta revisão encerra a lacuna, realizando inspeção multimodal direta dos quadros, camadas, recortes anatômicos e verificação matemática independente de todos os contratos declarados.

---

## 2. Verificação de Fontes e Hashes

| Arquivo | Caminho | SHA-256 Confirmado no Disco | Status |
|---|---|---|:---:|
| **Clip Manifesto** | `characters/orc-v1/source/combat-rescue-v5/grip-specialist/full-front-r-sword/clip.json` | `16fe8b7b30cbaa029ac4f4bd2bda5f7c8ac127007ec40a49a1f41db2580c63a1` | **MATCH** |
| **Mestre Composto** | `.../grip-specialist/full-front-r-sword/source/composite.aseprite` | `3ee5755c874ccc007aa7f67af9ea5cc839d2cf98b5c0bee25dbcf0bf9acf6410` | **MATCH** |
| **Mestre Corpo 256** | `.../grip-specialist/full-front-r-sword/source/body.aseprite` | `b85c18f315dfed5cb37536398719b18454e59d2d27f49d166d0f0fb3b10deb38` | **MATCH** |
| **Mestre Nativo 128** | `.../grip-specialist/full-front-r-sword/source/native.aseprite` | `8fab269d162d995ed3acdbbb09b8a03a3750ca5f05d923f35d21c1e55e8a87d7` | **MATCH** |
| **Mestre Mão 256** | `.../grip-specialist/full-front-r-sword/source/hand.aseprite` | `d2c6a911295e08ac057ae81c79ec77d3fcad23cee0d1c769e28c147d165a4fce` | **MATCH** |
| **Tira Composta** | `.../grip-specialist/full-front-r-sword/composite-strip.png` | `46629b49ba9d5091731db944dfdb3006160b71e8a569dd467bff80b9ce9d0f56` | **MATCH** |
| **Tira Nativa** | `.../grip-specialist/full-front-r-sword/native-strip.png` | `43aba45bf5b4a0bc4b1a453b76a7b14ce0366b6033691cd1bd1409d738ebe78c` | **MATCH** |

---

## 3. Auditoria dos 6 Critérios Técnicos e Artísticos

### Critério 1: Preservação do Corpo Frontal e Coreografia
- **Conferência Pixel a Pixel:** Todas as 13 camadas corporais (`layers/body/00.png` a `12.png`) possuem **exatamente 0 pixels de diferença RGBA** contra o corpo pai em `characters/orc-v1/source/combat-rescue-v5/combat/qa5-repair1/front_r/Sword/layers/body/`.
- **Timing:** As durações por quadro preservam exatamente o array original `[30, 65, 35, 50, 45, 65, 35, 35, 100, 55, 80, 45, 90] ms`, totalizando 730 ms.
- **Resultado:** **PASS**.

### Critério 2: Anatomia da Pegada, Luva Real e Cadeia Cinética
- **Traçado da Luva:** Nos 9 quadros armados (F02 a F10), a camada `handFront` cobre a seção central do cabo da espada com pixels reais de couro derivados diretamente da mão anatômica subjacente (conforme evidenciado em `new-gloves-source-annotated.png`).
- **Sem Carimbos Geométricos:** Não há máscaras fixas, caixas artificiais ou "cuffbridges". Cada pose reflete a orientação articular correspondente (ombro &rarr; cotovelo &rarr; antebraço &rarr; punho &rarr; luva).
- **Sem Interferência em Mão Inativa:** A mão esquerda do Orc (à direita da imagem) permanece desarmada e em repouso ao lado do quadril durante toda a coreografia, sem contaminação.
- **Visibilidade de Guarda e Pomo:** A guarda em cruz e o pomo circular de aço permanecem claramente legíveis e independentes, com o cabo cruzando o volume fechado da luva.
- **Resultado:** **PASS**.

### Critério 3: Reuso Estrito dos Keyframes Validados (F02, F06, F08)
- Os quadros F02, F06 e F08 foram comparados contra as referências estáticas previamente aprovadas em `characters/orc-v1/source/combat-rescue-v5/grip-specialist/{F02,F06,F08}/`:
  - **F02:** 4 camadas (`weaponBack`, `body`, `weaponFront`, `handFront`) e composto 256 são **100% byte-idênticos**.
  - **F06:** 4 camadas e composto 256 são **100% byte-idênticos** (incluindo os 9 retoques internos de luva).
  - **F08:** 4 camadas e composto 256 são **100% byte-idênticos**.
- A propagação intermediária (F03..F05, F07, F09..F10) conecta esses keyframes sem torções de antebraço, sem armas atravessando a armadura e sem descontinuidade visual.
- **Resultado:** **PASS**.

### Critério 4: Intervalo Visível `[2, 10]` e Bookends Desarmados
- **Política `attack-only-v1`:**
  - Quadros F00, F01, F11 e F12 possuem **exatamente 0 pixels opacos** nas camadas `weaponBack`, `weaponFront` e `handFront`.
  - Os compostos 256 nesses quadros de borda são **100% byte-idênticos** ao corpo desarmado.
  - A arma aparece exclusivamente a partir de F02 (estabelecimento de pegada) e desaparece em F11 (soltura/recuperação desarmada), sem Idle ou Walk armados.
- **Resultado:** **PASS**.

### Critério 5: Legibilidade do Item, Arco de Corte e Distância do Solo
- **Progressão Angular do Arco:**
  - F02: 320° (pegada baixa)
  - F03: 340° (elevação em antecipação)
  - F04: 350° (recolhimento junto à ombreira)
  - F05: 360° / 0° (ápice vertical em espaço aberto)
  - F06: 392° / 32° (liberação do corte diagonal)
  - F07: 440° / 80° (impacto horizontal-diagonal)
  - F08: 488° / 128° (follow-through descendente)
  - F09: 478° / 118° (recuo e desaceleração)
  - F10: 460° / 100° (estabilização frontal baixa)
- **Distância do Solo (`groundY = 190`):**
  - No ponto mais baixo da trajetória (F08), a ponta da lâmina atinge `Y = 185`, mantendo uma margem segura de **5 pixels acima do solo**. A arma jamais penetra o solo.
- **Legibilidade em Escala Tática (64px):** O contraste entre a lâmina de aço, o fuller central, a guarda escura e a manopla marrom permanece nítido e legível tanto em escala nativa quanto em escala tática reduzida.
- **Resultado:** **PASS**.

### Critério 6: Integridade dos Mestres e Canvas Canônico 256
- Todos os quatro mestres Aseprite existem no repositório e foram confirmados com hashes idênticos aos declarados.
- **Diagnóstico do Canvas Nativo 128:** A pasta `native/` contém recortes centrados `[64, 64, 128, 128]` destinados estritamente ao enquadramento do corpo nativo (128×128). O canvas canônico para animações de combate é 256×256 (`00.png` a `12.png`), no qual **100% da geometria da espada está contida com folga** (mínimo Y=30, máximo X=216, máximo Y=185), sem nenhum corte ou truncamento.
- **Composição Alfa-Over:** Foi verificado matematicamente que `((weaponBack OVER body) OVER weaponFront) OVER handFront` reproduz com 100% de identidade os compostos finais em todos os 13 quadros.
- **Resultado:** **PASS**.

---

## 4. Auditoria Quadro a Quadro

| Quadro | Fase | Duração | Visível | HandFront Px | Bbox Arma [x1, y1, x2, y2] | Delta Corpo | Veredito |
|:---:|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **F00** | rest | 30 ms | Não | 0 px | N/A | 0 px | **PASS** |
| **F01** | body-preparation | 65 ms | Não | 0 px | N/A | 0 px | **PASS** |
| **F02** | establish-grip | 35 ms | Sim | 21 px | [64, 85, 112, 141] | 0 px | **PASS** |
| **F03** | anticipation | 50 ms | Sim | 35 px | [68, 63, 97, 131] | 0 px | **PASS** |
| **F04** | coil-behind | 45 ms | Sim | 43 px | [83, 42, 108, 112] | 0 px | **PASS** |
| **F05** | apex-hold | 65 ms | Sim | 41 px | [85, 30, 110, 101] | 0 px | **PASS** |
| **F06** | slash-release | 35 ms | Sim | 33 px | [146, 64, 186, 125] | 0 px | **PASS** |
| **F07** | contact | 35 ms | Sim | 26 px | [146, 117, 216, 142] | 0 px | **PASS** |
| **F08** | follow-through | 100 ms | Sim | 23 px | [149, 139, 206, 185] | 0 px | **PASS** |
| **F09** | recoil | 55 ms | Sim | 32 px | [123, 139, 187, 175] | 0 px | **PASS** |
| **F10** | settle-grip | 80 ms | Sim | 30 px | [98, 139, 168, 164] | 0 px | **PASS** |
| **F11** | release-grip | 45 ms | Não | 0 px | N/A | 0 px | **PASS** |
| **F12** | return-to-guard | 90 ms | Não | 0 px | N/A | 0 px | **PASS** |

---

## 5. Limitações e Fronteiras Explícitas

1. **Inspeção Multimodal Estática e Funcional:** A auditoria baseou-se na inspeção de alta resolução de todos os quadros discretos, tiras compostas, grades de coordenadas anatômicas, zoom 8× da pegada e players Chromium a 1× e 0.5× com contagem de tempo de parede (730 ms). A percepção final como jogador de ritmo e peso em motor de jogo real permanece prerrogativa da homologação pelo Criador.
2. **Escopo Restrito:** Esta aprovação aplica-se **exclusivamente a `front_r/Sword`**. Não aprova automaticamente os demais ciclos, a matriz global de 28 células ou qualquer integração em `../TacticsRPG`.
3. **Status Artístico Global:** Permanece inalterado como `ARTISTIC_REVISION_REQUIRED` (`PENDING_CREATOR`).
