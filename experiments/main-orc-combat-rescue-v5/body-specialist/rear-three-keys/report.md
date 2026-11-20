# Orc V1 — Especialidade Corporal: 9 Chaves Anatômicas Traseiras Concluídas

**Status:** READY_FOR_QA  
**Technical Status:** TECHNICALLY_COMPLETE  
**Artistic Status:** VISUAL_REVIEW_REQUIRED  
**Global Status:** ARTISTIC_REVISION_REQUIRED (PENDING_CREATOR)  

## 1. Contexto e Assunção de Tarefa
Assumida a especialidade corporal como agente substituto em recuperação do agente bloqueado `950ff800-e30a-4a9a-9e5c-6917ed2f05c6` (status ERROR, sem turno ativo), conforme as diretrizes do handoff recebido da orquestração.
Todo o trabalho entregue anteriormente foi rigorosamente preservado:
- **full-back-r-axe**: ciclo desarmado completo 12f/1100ms (SHA-256 `2ab5ae40d7a11c0b4b271ca41f090608c3d721366da90ee1c6d1ebce9c1321c3`) mantido intacto.
- **BODY-01 resolvido**: reparo de impacto da mão direita em `body-specialist/repair1/` (freeze `e4434397532c4a42690be0acae5344a5185f0e1fbe19574cf78bd2b1672471c3`) preservado.

## 2. Escopo Concluído
Entrega completa das **9 chaves anatômicas estruturais** (3 chaves × 3 corpos traseiros restantes):
1. **back_r/Sword** (3 chaves: 01-hoist, 02-apex, 03-impact) — corte lateral diagonal de espada.
2. **back_l/Sword** (3 chaves: 01-hoist, 02-apex, 03-impact) — corte lateral diagonal de espada (perspectiva noroeste).
3. **back_l/Axe** (3 chaves: 01-hoist, 02-apex, 03-impact) — golpe vertical overhead de machado (perspectiva noroeste).

Cada corpo é estritamente **desarmado** (`layers-off`), camada única `body`, sem armas ou cabos desenhados sobre o corpo, com manoplas vinho-marrom autênticas e punhos fechados legíveis.

## 3. Refinamento Cirúrgico Local (Lição 17)
Durante a auditoria pixel-a-pixel das 9 chaves, detectou-se um defeito de geração em **back_l/Axe Chave 02 (ápice)**:
- **Sintoma:** O espaço negativo triangular entre o crânio verde, a gola e o antebraço arqueado continha uma massa opaca de 94 pixels de fundo cinzento residual (`rgb(117,118,120)`, `rgb(137,138,139)`, etc.).
- **Correção cirúrgica:** Executado script Aseprite Lua local delimitando a cavidade e convertendo os 94 pixels residuais para alfa 0 transparente (`rgba(0,0,0,0)`), preservando perfeitamente os contornos pretos do crânio, gola e braço.
- **Custo:** 0 créditos PixelLab; refinamento 100% local em Aseprite batch.

## 4. Conformidade Rígida com as Restrições
1. **Aseprite:** Todos os arquivos de mestre e exportação foram salvos via `F:\SteamLibrary\steamapps\common\Aseprite\Aseprite.exe 1.3.18.6 batch --noinapp` com perfil exclusivo `tmp/aseprite-body-specialist-v2-profile`.
2. **Duração:** Frames com `0.160` segundos em Lua (160 ms exatos).
3. **Canvas e Solo:** Nativo 128×128 cravado em `nativeGroundY = 126`; composto 256×256 com offset `Point(64,64)` cravado em `groundY = 190`.
4. **Halos:** 0 pixels com RGB todos > 190 em todas as 9 chaves.
5. **Estrutura de Pastas:** Entregue em subpastas isoladas por corpo:
   - `experiments/main-orc-combat-rescue-v5/body-specialist/back_r-Sword-keys/`
   - `experiments/main-orc-combat-rescue-v5/body-specialist/back_l-Sword-keys/`
   - `experiments/main-orc-combat-rescue-v5/body-specialist/back_l-Axe-keys/`
   - Mestres canônicos sincronizados em `characters/orc-v1/source/combat-rescue-v5/body-specialist/rear-three-keys/`.
6. **Arquivos por subpasta:**
   - `01-native.aseprite`, `01-native.png`, `01-body256.aseprite`, `01-body256.png`
   - `02-native.aseprite`, `02-native.png`, `02-body256.aseprite`, `02-body256.png`
   - `03-native.aseprite`, `03-native.png`, `03-body256.aseprite`, `03-body256.png`
   - `clip.json`
   - `representative.json`
   - `checkpoint.json`
   - `report.md`
7. **Isolamento estrito:** Nenhuma escrita em `grip-specialist/`, matriz, `integrate.mjs`, `validate.mjs`, `orchestration-report.md`, Unity ou produção ativa. Nenhum QA interno criado.

## 5. Contabilidade de Gerações PixelLab
- Jobs anteriores registrados: 16 gerações cobradas.
- Gerações consumidas nesta sessão: **0** (zero).
- Saldo verificado restante: **1351.70** gerações.

## 6. Próximo Passo
O pacote de 9 chaves está pronto para avaliação pelo **QA independente** (não Copilot). Nenhuma expansão para intermediários ou integração runtime deve ocorrer antes do parecer do QA.
