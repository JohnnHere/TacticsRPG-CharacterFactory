# Grip Especialista — Ciclo Completo front_l/Sword (13f / 730ms)

**GRIP_FRONT_L_SWORD_FULL_READY · TECHNICALLY_COMPLETE · VISUAL_REVIEW_REQUIRED · PENDING_CREATOR · eligibleForIntegration: false**

## 1. Escopo e Propósito
Este pacote entrega o ciclo completo equipado de **front_l/Sword** (Sword, direção `front_l`) para avaliação do QA independente (sem Copilot, sem Codex).
- **Direção:** `front_l`
- **Arma:** `Espada do Recruta` (`recruit-sword`)
- **Total de quadros:** 13 quadros
- **Duração total:** 730 ms
- **Tempos por quadro (ms):** [30, 65, 35, 50, 45, 65, 35, 35, 100, 55, 80, 45, 90]
- **Intervalo visível da arma:** F02 até F10 (9 quadros ativos)
- **Quadros com arma oculta (bookends):** [0, 1, 11, 12]
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
| F00 | `rest` | 30 ms | *(oculto)* | *(oculto)* | *(oculto)* | 0 px |
| F01 | `body-preparation` | 65 ms | *(oculto)* | *(oculto)* | *(oculto)* | 0 px |
| F02 | `establish-grip` | 35 ms | `[152, 130]` | 40° | -320° | 21 px |
| F03 | `anticipation` | 50 ms | `[165, 119]` | 20° | -340° | 35 px |
| F04 | `coil-behind` | 45 ms | `[157, 100]` | 10° | -350° | 43 px |
| F05 | `apex-hold` | 65 ms | `[157, 89]` | 0° | -360° | 41 px |
| F06 | `slash-release` | 35 ms | `[100, 114]` | 328° | -392° | 33 px |
| F07 | `contact` | 35 ms | `[97, 132]` | 280° | -440° | 26 px |
| F08 | `follow-through` | 100 ms | `[96, 148]` | 232° | -488° | 23 px |
| F09 | `recoil` | 55 ms | `[121, 147]` | 242° | -478° | 32 px |
| F10 | `settle-grip` | 80 ms | `[145, 150]` | 260° | -460° | 30 px |
| F11 | `release-grip` | 45 ms | *(oculto)* | *(oculto)* | *(oculto)* | 0 px |
| F12 | `return-to-guard` | 90 ms | *(oculto)* | *(oculto)* | *(oculto)* | 0 px |

## 4. Arquivos Entregues e Hashes SHA-256
### Mestres Aseprite:
- `source/composite.aseprite`: `3efc83c1a17fa45e7f34ea3af985255b2820c924fcfcf76be15095d9dec1e085`
- `source/body.aseprite`: `37e4ed5c76e06fb22cc840ce80ad2c531b71ff28141e80fbea4c44de0fba36c2`
- `source/native.aseprite`: `38a9865dc23f909bd971b2cadc58c4ad1b9ad6d48b7cfc8533b5d0b41f40789f`
- `source/hand.aseprite`: `ef3b39734317c7e60fea6be473486efbb366f613061af8f8c4039d20c71815df`

### Documentos de Configuração e Diagnóstico:
- `clip.json`: `56eb4daeb43b35cbb0a50a3b1cc145eba802c5b408b96bf76fa90c3219eb4681`
- `representative.json`: `baa4c3c4cc37fa150662e5116aa824395de17b6a73423aa5f91677ced9c85041`
- `checks.json`: `5486bd349daf38742e96d45b8e828482f972fc5a60b29495773d31db403cf55d`
- `index.html` (player interativo): `5a06fecdf10f85e5eab22f93d95196d362110634751959248f626aaf911a1d70`

### Strips Completos:
- `composite-strip.png`: `7c3fb74fbee6f12c70ce0a2ebfff0b2223c96f5a896449a1a9cdf7b4b1929428`
- `native-strip.png`: `0e693e1ed2cf3806d37e37f45557d20326fcdff64f88d90edb37b76c82dd63bf`

## 5. Status e Próximo Passo
- **Status Técnico:** `TECHNICALLY_COMPLETE`
- **Status Artístico:** `VISUAL_REVIEW_REQUIRED`
- **Aprovação do Criador:** `PENDING_CREATOR`
- **Próximo Passo:** Submissão ao QA independente (sem Copilot, sem Codex) para verificação temporal perceptual contínua em escala real (1× e câmera lenta).
