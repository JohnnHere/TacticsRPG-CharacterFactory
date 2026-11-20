# Grip Especialista — Ciclo Completo front_l/Axe (12f / 1005ms)

**GRIP_FRONT_L_AXE_FULL_READY · TECHNICALLY_COMPLETE · VISUAL_REVIEW_REQUIRED · PENDING_CREATOR · eligibleForIntegration: false**

## 1. Escopo e Propósito
Este pacote entrega o ciclo completo equipado de **front_l/Axe** (Axe, direção `front_l`) para avaliação do QA independente (sem Copilot, sem Codex).
- **Direção:** `front_l`
- **Arma:** `Machado de Milícia` (`militia-axe`)
- **Total de quadros:** 12 quadros
- **Duração total:** 1005 ms
- **Tempos por quadro (ms):** [40, 65, 35, 80, 155, 35, 115, 110, 130, 50, 90, 100]
- **Intervalo visível da arma:** F02 até F08 (7 quadros ativos)
- **Quadros com arma oculta (bookends):** [0, 1, 9, 10, 11]
- **Custos PixelLab:** 0 chamadas pagas consumidas (custo $0.00)

## 2. Anatomia e Construção da Pegada
- **Corpo 100% Preservado:** 0 pixels RGBA de delta em relação ao corpo frontal aprovado. Nenhuma pose corporal foi reanimada ou alterada.
- **Camadas Independentes (4 camadas):**
  1. `weaponBack`: couro/madeira da empunhadura desenhado atrás do corpo nas linhas de pegada.
  2. `body`: o corpo completo do Orc (256×256 e crop nativo 128×128 em 64,64).
  3. `weaponFront`: guarda, lâmina/cabeça de machado e pomo posicionados na frente do corpo.
  4. `handFront`: dedos e palma da luva original traçados individualmente a partir do corpo em cada quadro visível, sobrepondo o cabo da arma de forma natural.
- **Fechamento e Envolvimento:** A mão envolve o cabo da arma; guarda e pomo permanecem discerníveis e contínuos através da pegada, sem quebras ou flutuações.
- **Diferenciação Técnica:**
  - `Sword`: golpe em corte com arco horizontal/diagonal, lâmina alongada em direção à trajetória do golpe.
  - `Axe`: golpe pesado de descida (overhead / cleave), impacto descendente com recuperação de peso.

## 3. Coordenadas de Pegada por Quadro Visível
| Quadro | Fase | Duração | Pegada [X, Y] | Rotação (°) | Unwrapped (°) | Pixels HandFront |
|---|---|---|---|---|---|---|
| F00 | `rest` | 40 ms | *(oculto)* | *(oculto)* | *(oculto)* | 0 px |
| F01 | `body-preparation` | 65 ms | *(oculto)* | *(oculto)* | *(oculto)* | 0 px |
| F02 | `establish-grip` | 35 ms | `[152, 130]` | 60° | -300° | 21 px |
| F03 | `anticipation` | 80 ms | `[165, 119]` | 40° | -320° | 35 px |
| F04 | `overhead-coil` | 155 ms | `[157, 100]` | 10° | -350° | 43 px |
| F05 | `cleave-drive` | 35 ms | `[105, 132]` | 300° | -420° | 22 px |
| F06 | `heavy-impact` | 115 ms | `[104, 144]` | 240° | -480° | 18 px |
| F07 | `weight-settle` | 110 ms | `[114, 151]` | 255° | -465° | 14 px |
| F08 | `wrench-recovery` | 130 ms | `[121, 147]` | 265° | -455° | 32 px |
| F09 | `release-grip` | 50 ms | *(oculto)* | *(oculto)* | *(oculto)* | 0 px |
| F10 | `shoulder-reset` | 90 ms | *(oculto)* | *(oculto)* | *(oculto)* | 0 px |
| F11 | `return-to-guard` | 100 ms | *(oculto)* | *(oculto)* | *(oculto)* | 0 px |

## 4. Arquivos Entregues e Hashes SHA-256
### Mestres Aseprite:
- `source/composite.aseprite`: `4df2d168a97a7a643be47f2b57d85f260a1a9951324a3f9dbe7ab4107ce08938`
- `source/body.aseprite`: `871e283bf7ef6a76a041b322d438e296939b7d72673bb8de91ef3820d8acc118`
- `source/native.aseprite`: `60443ef5d7c2e8ed13ad0c8db935c0ba57d96f13f57b6909f0b6b62eb6c6a885`
- `source/hand.aseprite`: `8413a438e0db29f486b8b1095fad62aa68c70741c551e6ac7bb162c36c874956`

### Documentos de Configuração e Diagnóstico:
- `clip.json`: `fa3c620d69d7df05bf0afab1fffa35fe37d861feacfc4124cbafa7e9763d7c5c`
- `representative.json`: `09c2b3189f0e5adeee682a0a7fcc2ab848c31a7b8c4a40a1ec5db40dfa7befcd`
- `checks.json`: `5f18f5c9239fd1c94c2b75a46d9b0037a675449709e59af20d8e77314dae1a59`
- `index.html` (player interativo): `2338dfdc00ef8e26a48b7541485989297284423d067069c04a0c8394f20b1c8c`

### Strips Completos:
- `composite-strip.png`: `033157cdedc85160a79c8bcb1e39c20a736316e16d76b528e767066322f4dead`
- `native-strip.png`: `ba6fa7c40759bdeaa1302ac9fcaa90505ff65c2ad483efce6d3824113eb65f33`

## 5. Status e Próximo Passo
- **Status Técnico:** `TECHNICALLY_COMPLETE`
- **Status Artístico:** `VISUAL_REVIEW_REQUIRED`
- **Aprovação do Criador:** `PENDING_CREATOR`
- **Próximo Passo:** Submissão ao QA independente (sem Copilot, sem Codex) para verificação temporal perceptual contínua em escala real (1× e câmera lenta).
