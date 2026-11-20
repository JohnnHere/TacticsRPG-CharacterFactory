# Relatório Final de Engenharia e Recuperação Artística — Passe `main-orc-targeted-recovery-v3` (Pós-Re-Revisão de QA)

**Data:** 27 de Outubro de 2026  
**Papel:** Sole DEV (Antigravity)  
**Personagem:** Orc V1 / Verde Warcraft (`characters/orc-v1/`)  
**Status do Pacote:** `TECHNICALLY_COMPLETE` · `VISUAL_REVIEW_REQUIRED` · `PENDING_CREATOR`  
**Escopo de Runtime:** `runtimeImplemented: false` (Zero escritas em `../TacticsRPG`)  
**Contabilidade de IA:** 0 gerações consumidas neste passe (Total histórico mantido em 17 jobs / 78 gerações consumidas)  
**Estúdio Interativo de Revisão:** [`Biblioteca de Arte/Estudos Comparativos/Orc principal - Recuperacao traseira/index.html`](file:///C:/Users/João%20Orlando/Documents/Projetos%20Unity/TacticsRPG-CharacterFactory/Biblioteca%20de%20Arte/Estudos%20Comparativos/Orc%20principal%20-%20Recuperacao%20traseira/index.html)  

---

## 1. Resumo Executivo e Correções Cirúrgicas de Re-Revisão (RR-01..RR-07)

Este relatório consolida a resolução de todos os 7 apontamentos de re-revisão (**RR-01 a RR-07**) formulados pelo QA Independente sobre o passe de recuperação direcionada. Todas as intervenções foram operadas exclusivamente no Aseprite (`tools/aseprite/`, perfil `tmp/aseprite-batch-profile`), sem consumo de créditos de IA (0 gerações) e sem modificações no código de runtime de Unity.

| # | Gravidade | Alvo | Diagnóstico do QA Independente | Correção Implementada no DEV | Resultado Observado / Verificação | Status |
|---|---|---|---|---|---|---|
| **RR-01** | CRÍTICO | `back_l/Unarmed` F04 | Recorte retangular destrutivo na lateral do tronco/armadura (`x=15..45, y=20..80`) e fragmento residual de luva marrom flutuante a `(30,83)` | Eliminação da máscara destrutiva em `repair_back_l_unarmed.lua`; retorno ao repouso com ancoragem em solo (`Point(0, 1)`), restaurando contorno contínuo de armadura/tronco e braço pendente de Idle | Inspecionado a 1×, 3× e 4×: contorno de tronco e armadura íntegro, silhueta anatômica contínua de ombro a punho, 0 recortes retangulares, 0 fragmentos flutuantes | Corrigido, sujeito a re-QA |
| **RR-02** | ALTO | `back_r/Unarmed` e `back_l/Unarmed` | Divergência de tempos: mestres usavam `[80, 110, 50, 90, 120]` ms enquanto os `clip.json` declaravam `[80, 110, 60, 90, 110]` ms | Durações nos `clip.json` unificadas em `[80, 110, 50, 90, 120]` ms para todos os quadros (total 450 ms idêntico) | Total concordância temporal entre cels dos mestres nativo/composto, manifests e motor de playback | Corrigido |
| **RR-03** | ALTO | Armas Traseiras (4 clipes, F01..F06) | Sockets e ângulos (`rightGrip` e `rotationDeg`) desatualizados nos `clip.json` (24 registros com divergência) | Exportação automatizada dos parâmetros reais de `author_all_rear_weapons_clean.lua` para os 4 `clip.json` | 24 registros visíveis e 32 registros totais 100% coincidentes entre script de autoria, imagem real e manifesto | Corrigido |
| **RR-04** | ALTO | Hashes Declarados | 14 digests defasados nos manifests (4 `bodyMasterSha256` e 10 `stripSha256`) | Sincronizador `sync_all_metadata_v5.mjs` recalcula integralmente todos os campos de hash de arquivo e frame | Suíte automatizada `test/test_declared_hashes.test.mjs` verifica 789 campos de hash: zero divergências | Corrigido |
| **RR-05** | MÉDIO, ARTÍSTICO | `front_r/Defeat` e `front_l/Defeat` F04 | Postura terminal lia como apoio sobre quatro apoios (cabeça elevada entre braços apoiados, joelhos sob o corpo) | Colapso volumétrico com nocaute genuíno via `author_knockout_defeat.lua`: cabeça rebaixada rente ao solo/antebraço (`cabeça baixa`), tronco desabado de bruços, braços soltos e abertos no solo, cels limpos antes do desenho | Altura terminal 52 px (nativo 128), largura 122 px, proporção 2,35, groundY=126 cravado. Sem compressão regional e sem rotação global com vScale | Corrigido, sujeito a validação visual do criador |
| **RR-06** | MÉDIO | 13 Manifestos Protegidos | Acréscimo do campo `nativeStripSha256` violou a integridade byte-a-byte dos 13 `clip.json` protegidos | Remoção do campo dos 13 `clip.json` protegidos, restaurando exatamente o conteúdo do `before-snapshot.json` | 13 de 13 arquivos `clip.json` protegidos recuperaram SHA-256 idêntico ao snapshot (13/13 MATCH byte a byte) | Corrigido |
| **RR-07** | MÉDIO | Documentação e Governança | Documentação continha afirmações de resolução total antes do parecer, contagem incorreta de quadros (98/112) e dados defasados de Defeat | Remoção de alegações prematuras; contagem corrigida para **123 afetados / 87 protegidos** (total 210); documentação técnica e lição 21 atualizadas | Governança alinhada com os fatos materiais auditados | Corrigido |

---

## 2. Contabilidade Exata de Quadros e Preservação

- **Total de clipes na matriz canônica (`candidate28manifest.json`):** 28 clipes (210 quadros compostos).
- **Clipes Alvo Afetados (`ACTIVE_CANDIDATE` / `isAffected: true`):** 15 clipes (**123 quadros compostos**):
  - `front_r/Walk` (16 frames), `front_l/Walk` (16 frames), `back_r/Walk` (8 frames), `back_l/Walk` (8 frames)
  - `front_r/Unarmed` (5 frames), `front_l/Unarmed` (5 frames), `back_r/Unarmed` (5 frames), `back_l/Unarmed` (5 frames)
  - `front_l/Sword` (13 frames), `back_r/Sword` (8 frames), `back_l/Sword` (8 frames)
  - `back_r/Axe` (8 frames), `back_l/Axe` (8 frames)
  - `front_r/Defeat` (5 frames), `front_l/Defeat` (5 frames)
- **Clipes Protegidos Intactos (`UNCHANGED_ALIAS` / `isAffected: false`):** 13 clipes (**87 quadros compostos**), preservados **byte a byte**:
  - `front_r/Idle` (5 frames), `front_l/Idle` (5 frames), `back_r/Idle` (5 frames), `back_l/Idle` (5 frames)
  - `front_r/Hit` (5 frames), `front_l/Hit` (5 frames), `back_r/Hit` (5 frames), `back_l/Hit` (5 frames)
  - `front_r/Sword` (13 frames), `front_r/Axe` (12 frames), `front_l/Axe` (12 frames)
  - `back_r/Defeat` (5 frames), `back_l/Defeat` (5 frames)
- **Total de quadros:** 123 afetados + 87 protegidos = 210 quadros no pacote completo.

---

## 3. Resultados da Suíte Completa de Testes

1. **Suíte Geral do Node (`node --test --test-concurrency=1`):**
   - **55 testes executados, 55 aprovados, 0 falhas, 0 skips** (duração: 93.1s).
   - `test/test_declared_hashes.test.mjs`: 5/5 subtestes PASS (cobrindo 789 campos de hash verificados contra os arquivos físicos, 13/13 equivalências byte-a-byte contra `before-snapshot.json`, 32/32 sockets/ângulos, 4/4 tempos de Unarmed, e métricas geométricas de Defeat e UnarmedL F04).
   - `test/browser-check-rear-recovery-review.mjs`: 20/20 verificações em Chromium headless PASS (velocidades 1×, 0.75×, 0.5×, passo a quadro, escala 128px, zoom nativo, hold de Defeat, 15/15 seções antes/depois).
   - `Candidate 28 Manifest Validator Contract Suite`: 14/14 testes PASS.
   - `test/test_review_js_runtime.mjs`: validação de execução assíncrona do player PASS.
2. **Validação da Página de Revisão em Python (`tools/test_rear_recovery_review.py`):**
   - **28/28 células validadas, zero links quebrados (0 404s)** em `index.html`.

---

## 4. Status de Entrega e Próximos Passos

- **Status Técnico do Pacote:** `TECHNICALLY_COMPLETE`. Todos os requisitos técnicos, algebraicos, de esquema e de hashing foram auditados e passaram nos testes automatizados.
- **Status Artístico do Pacote:** `VISUAL_REVIEW_REQUIRED` (sujeito a re-QA independente e avaliação do criador).
- **Aprovação do Criador:** Estritamente `PENDING_CREATOR`. Nenhuma aprovação automática é assumida. O estúdio interativo de comparação local (`Biblioteca de Arte/Estudos Comparativos/Orc principal - Recuperacao traseira/index.html`) está pronto para inspeção contínua em 1×, 0.75× e 0.5×.
- **Integração de Runtime:** Nenhuma alteração foi realizada em `../TacticsRPG` (`runtimeImplemented: false`).
