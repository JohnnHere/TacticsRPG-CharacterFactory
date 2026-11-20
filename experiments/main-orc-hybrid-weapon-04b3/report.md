# Piloto B3 (`back_l`) e Arquitetura C com Diferença Real de Silhueta nas 4 Vistas

- **Status técnico:** `TECHNICALLY_COMPLETE`
- **Status artístico:** `VISUAL_REVIEW_REQUIRED` · `PENDING_CREATOR`
- **Mestres `.aseprite`:** `characters/orc-v1/source/aseprite/final-candidate-v10/architecture-c/<dir>/sword-a.aseprite` e `sword-b.aseprite` (+ cópia dedicada B3 em `experiments/main-orc-hybrid-weapon-04b3/full/a|b/composite.aseprite`).

## O que já existia antes deste passo e o que o B3 / V10 comprovou

1. **Piloto A (`main-orc-hybrid-weapon-04`):** cobriu `front_l/Sword` com diferença real de silhueta (`106 px` no sprite `96×96`).
2. **Pilotos B1 (`04b`, `front_r`) e B2 (`04b2`, `back_r`, QA `PASS` `3736c9dc...`):** validaram a composição de camadas e a troca de acabamento, porém travaram a silhueta da Variante B na máscara da Variante A (`silhouetteDeltaAB = 0 px`). O **Piloto B3 (`back_l`)** ainda não existia.
3. **Execução completa em V10 (`front_r`, `front_l`, `back_r`, `back_l`):**
   - Composição determinística no Aseprite Lua das duas espadas independentes `96×96` com o mesmo pivô `[48, 66]` e mesma guarda/empunhadura (`y >= 55`): **Espada do Recruta (`recruit-sword`, A)** vs **Espada Facetada de Aço Claro (`faceted-sword-b`, B, perfil de lâmina `106 px` distinto)**.
   - **Reaproveitamento corporal medido:** `56/56` quadros de `body` (`100%`) e `56/56` quadros de `handFront` (`100%`) idênticos pixel a pixel (`0 px` RGBA delta) entre A e B nas 4 vistas.
   - **Diferença real de silhueta por quadro armado (`F02..F11`):** `99..111 px` por quadro (`1041..1062 px` somados nos 10 quadros armados de cada vista), sem qualquer colisão com solo (`maxWeaponY <= 172 <= groundY 190`) e `0 px` de arma em `F00, F01, F12, F13` (`attack-only-v1`).
