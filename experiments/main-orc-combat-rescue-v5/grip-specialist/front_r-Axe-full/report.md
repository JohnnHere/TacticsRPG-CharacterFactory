# Grip Especialista — Ciclo Completo front_r/Axe (12f / 1005ms)

**GRIP_FRONT_R_AXE_FULL_READY · TECHNICALLY_COMPLETE · VISUAL_REVIEW_REQUIRED · PENDING_CREATOR · eligibleForIntegration: false**

## 1. Escopo e Propósito
Este pacote entrega o ciclo completo equipado de **front_r/Axe** (Axe, direção `front_r`) para avaliação do QA independente (sem Copilot, sem Codex).
- **Direção:** `front_r`
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
| F02 | `establish-grip` | 35 ms | `[103, 130]` | 300° | 300° | 21 px |
| F03 | `anticipation` | 80 ms | `[90, 119]` | 320° | 320° | 35 px |
| F04 | `overhead-coil` | 155 ms | `[98, 100]` | 350° | 350° | 43 px |
| F05 | `cleave-drive` | 35 ms | `[150, 132]` | 60° | 420° | 22 px |
| F06 | `heavy-impact` | 115 ms | `[151, 144]` | 120° | 480° | 18 px |
| F07 | `weight-settle` | 110 ms | `[141, 151]` | 105° | 465° | 14 px |
| F08 | `wrench-recovery` | 130 ms | `[134, 147]` | 95° | 455° | 32 px |
| F09 | `release-grip` | 50 ms | *(oculto)* | *(oculto)* | *(oculto)* | 0 px |
| F10 | `shoulder-reset` | 90 ms | *(oculto)* | *(oculto)* | *(oculto)* | 0 px |
| F11 | `return-to-guard` | 100 ms | *(oculto)* | *(oculto)* | *(oculto)* | 0 px |

## 4. Arquivos Entregues e Hashes SHA-256
### Mestres Aseprite:
- `source/composite.aseprite`: `83f73413521dc5357161423d5d88b55604f316fcc29ba834ea0b5bbd63dd039e`
- `source/body.aseprite`: `5d61850d2a33057dfc7ebe532a715b0736db31185b2e8d459a9358dbb196deb2`
- `source/native.aseprite`: `d86b36cccba891e2f91d4f24fb76867e3e35df42c64293b8ab45424b932d138b`
- `source/hand.aseprite`: `4cc7675331ac2a965c931cacdf11b11a22cb022d480faa1b450a087cd959ac0d`

### Documentos de Configuração e Diagnóstico:
- `clip.json`: `dca0ef7e000be50cf8cf39ca69c3b55324ea1a4857a18e1b15278bbae6e3d0f5`
- `representative.json`: `4542bbb8ae77ca526d3f5a4d913c4d73cfc30446b21341540955dccb50a35925`
- `checks.json`: `429861193fd242e644e238562ae35e028748ae0840b8f92237786492e34516e9`
- `index.html` (player interativo): `533edef0fbf234ab080f2b6492061560730675453a5c5c20f3f09f58295fd67e`

### Strips Completos:
- `composite-strip.png`: `3c528ec88686fd14827a4a1a01dee24377cf70e4d8bc3321fdd531be1a9acf4e`
- `native-strip.png`: `0caca1544325007fe1e76c055e36ebc7e5b33f8f9350772fdcd9bdf2d5a630a7`

## 5. Status e Próximo Passo
- **Status Técnico:** `TECHNICALLY_COMPLETE`
- **Status Artístico:** `VISUAL_REVIEW_REQUIRED`
- **Aprovação do Criador:** `PENDING_CREATOR`
- **Próximo Passo:** Submissão ao QA independente (sem Copilot, sem Codex) para verificação temporal perceptual contínua em escala real (1× e câmera lenta).
