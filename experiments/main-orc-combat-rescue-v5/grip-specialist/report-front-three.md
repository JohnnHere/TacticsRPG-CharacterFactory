# Grip Especialista — Entrega dos 3 Ciclos Frontais Restantes

**Data:** 2026-10-29  
**Agente:** Continuidade finalizada por Nemotron 3.5 Super VL / OpenCode Free (`438383d1-01dc-4b15-bf23-59161355cbb8`), preservando o trabalho anterior Sol/Codex  
**Status Geral:** `TECHNICALLY_COMPLETE` · `VISUAL_REVIEW_REQUIRED` · `PENDING_CREATOR` · `eligibleForIntegration: false`

## 1. Resumo da Entrega
Com a entrega do ciclo `full-front-r-sword` no turno anterior, esta etapa conclui os **3 ciclos frontais restantes** de ataque com arma do Orc V1:
1. **front_l/Sword** (13 quadros / 730 ms) — Espada do Recruta
2. **front_r/Axe** (12 quadros / 1005 ms) — Machado de Milícia
3. **front_l/Axe** (12 quadros / 1005 ms) — Machado de Milícia

Os 4 ciclos frontais armados encontram-se agora completamente produzidos, verificados tecnicamente e prontos para inspeção pelo QA independente.

## 2. Conformidade com as Restrições Rígidas
- **Corpo Frontal Preservado:** 0 pixels RGBA de delta em todos os quadros (100% da coreografia frontal aprovada preservada).
- **Pegada Natural:** 4 camadas independentes (`weaponBack`, `body`, `weaponFront`, `handFront`); luvas originais traçadas sem carimbos ou dedos flutuantes.
- **Política de Armas Somente no Ataque (attack-only):** Armas visíveis estritamente nos intervalos declarados (`[2, 10]` para Espada, `[2, 8]` para Machado); bookends 100% desarmados.
- **Mestres Aseprite:** Autoria e exportação executadas via Aseprite batch com perfil exclusivo; `Frame.duration` em segundos.
- **Custos:** 0 novas chamadas PixelLab consumidas; custo LLM não informado.
- **Preservação de Escopo:** Nenhuma escrita em `body-specialist/`, matriz, Unity, ou produção ativa.

## 3. Matriz de Entregas e Hashes SHA-256
| Ciclo | Quadros | Duração | Checkpoint | clip.json SHA-256 | composite.aseprite SHA-256 |
|---|---|---|---|---|---|
| `front_r/Sword` *(entregue anterior)* | 13f | 730 ms | `GRIP_FRONT_R_SWORD_FULL_READY` | `16fe8b7b30cbaa029ac4f4bd2bda5f7c8ac127007ec40a49a1f41db2580c63a1` | `3ee5755c874ccc007aa7f67af9ea5cc839d2cf98b5c0bee25dbcf0bf9acf6410` |
| `front_l/Sword` | 13f | 730 ms | `GRIP_FRONT_L_SWORD_FULL_READY` | `56eb4daeb43b35cbb0a50a3b1cc145eba802c5b408b96bf76fa90c3219eb4681` | `3efc83c1a17fa45e7f34ea3af985255b2820c924fcfcf76be15095d9dec1e085` |
| `front_r/Axe` | 12f | 1005 ms | `GRIP_FRONT_R_AXE_FULL_READY` | `dca0ef7e000be50cf8cf39ca69c3b55324ea1a4857a18e1b15278bbae6e3d0f5` | `83f73413521dc5357161423d5d88b55604f316fcc29ba834ea0b5bbd63dd039e` |
| `front_l/Axe` | 12f | 1005 ms | `GRIP_FRONT_L_AXE_FULL_READY` | `fa3c620d69d7df05bf0afab1fffa35fe37d861feacfc4124cbafa7e9763d7c5c` | `4df2d168a97a7a643be47f2b57d85f260a1a9951324a3f9dbe7ab4107ce08938` |

## 4. Navegadores e Previews
- `front_l-Sword-full`: [index.html](front_l-Sword-full/index.html) · [relatório](front_l-Sword-full/report.md)
- `front_r-Axe-full`: [index.html](front_r-Axe-full/index.html) · [relatório](front_r-Axe-full/report.md)
- `front_l-Axe-full`: [index.html](front_l-Axe-full/index.html) · [relatório](front_l-Axe-full/report.md)

## 5. Próximo Passo
Aguardar parecer do QA independente (sem Copilot, sem Codex) sobre os 3 ciclos completos. Não propagar nem integrar no Unity antes de verificação e aprovação explícita do criador.
