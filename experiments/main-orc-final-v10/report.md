# Relatório Consolidado — Orc Guerreiro `main-orc-final-v10`

- **Status técnico:** `TECHNICALLY_COMPLETE`
- **Status artístico:** `VISUAL_REVIEW_REQUIRED` · `PENDING_CREATOR`
- **Integração Unity:** `runtimeImplemented: false` (`0` escritas em `../TacticsRPG`; pacote local pronto em `dist/orc-v1/final-candidate-v10/`).
- **Manifesto 28 células:** `characters/orc-v1/source/final-candidate-v10/candidate28manifest.json` (`18 ACTIVE_CANDIDATE` + `10 UNCHANGED_ALIAS`, `232` quadros totais).

## Síntese das correções verificadas

1. **`Sword Attack` (4 vistas, 14f / 730 ms, contato `F08` @ 325 ms) + Arquitetura C (A × B):**
   - `back_r`: eliminado o flash cinza opaco no vão do braço esquerdo (`F01–F02`), unificada a base de pernas/botas nos 14 quadros sobre `Idle F00`, e substituído o braço direito rasgado/derretido (`F08–F11`) pelo braço direito íntegro de `combat-rescue-v5` com cabo passando pelo eixo da palma.
   - `back_l`: substituído o golpe lateral/invertido de V8/V9 por corte diagonal 3D Norte-Oeste empunhado pela mão direita (`animate_with_skeleton_v3` desarmado `3743684d`), com oclusão traseira coerente (`rear_hilt_back` na elevação/guarda e `all_back` ao cruzar atrás do crânio/tronco) e recuperação contínua para guarda direita (`F10: -56° -> F11: +30°`).
   - `front_r` e `front_l`: coreografia frontal preservada; reparadas as axilas do braço erguido (`F03–F05`), estabilizados os contornos externos claros que piscavam nos recortes e restaurados os brilhos especulares do peitoral em `F12`.
   - **Arquitetura C:** `recruit-sword` (A) e `faceted-sword-b` (B) compartilham `56/56` quadros idênticos de `body` e `handFront` nas 4 vistas com `99–111 px` de diferença real de silhueta por quadro armado.
2. **`Axe Attack` (4 vistas, 12f / 1005 ms, contato `F06` @ 410 ms):**
   - Limpeza do asset `militia-axe` (remoção do pixel órfão `(37,24)` e reforço do colarinho) e reposicionamento do pivô para o centro do cabo `(36, 48)`, eliminando a "pegada por baixo do cabo" (madeira `v=42..53` atravessa a luva; pomo `v=54..61` projeta-se abaixo do punho).
   - `back_l`: golpe pesado descendente Norte-Oeste com a mão direita (`animate_with_skeleton_v3` desarmado `5b037840`) e arrancada de recuperação coerente no lado do impacto (`F08: -76°`).
   - `back_r`, `front_r`, `front_l`: flash lateral e saltos de perna eliminados em `back_r`; frontais preservadas com axila e contorno estabilizados.
3. **Demais clipes (`Unarmed`, `Walk`, `Defeat`, `Hit`, `Idle`):**
   - `Unarmed` (5f / 450 ms): restaurado o antebraço direito ausente em `back_r F01`, eliminado o T-pose duplo em `back_l F01` + congelamento em `F03`, removido o fragmento no quadril em `F00` e restaurada a manopla em `F04` nas frontais.
   - `Walk` (16f frontais / 8f traseiras): equalizado o flash claro da cota de malha na virilha (`F06..F09`) nas frontais; fechado o buraco escuro no cotovelo esquerdo (`back_l F01`) e estabilizado o brilho par/ímpar dos braceletes traseiros.
   - `Defeat` (5f / 700 ms): `F04` terminal de `front_r` e `front_l` reautorado como corpo inconsciente estendido de bruços no chão (`groundY = 190/126`), sem a barra retangular cinza na mão e alinhado à leitura de `back_r`/`back_l`.
   - `Hit` (5f / 450 ms) e `Idle` (`idle-balanced-v1`, 5f / 2200 ms): preservados byte a byte nas 4 vistas.
