# Production Checkpoint — main-orc-rear-recovery-v2

**Data:** 2026-10-26T03:39:00-03:00  
**Autor:** Paseo ART DEV (Produtor de Arte Exclusivo)  
**Consumidores:** Preview DEV (`512ba3d` fallback), Knowledge DEV (`2046bf` fallback), Root Orchestrator  
**Manifesto Canônico dos 28 Clipes:** [`characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json`](file:///C:/Users/Jo%C3%A3o%20Orlando/Documents/Projetos%20Unity/TacticsRPG-CharacterFactory/characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json)

---

### 1. Resumo Executivo da Matriz 4×7 (28 Células)

A matriz de 28 animações está 100% coberta e validada, com 10 candidatos ativos refinados em Aseprite Lua e 18 pseudônimos protegidos preservados byte a byte da linha de base canônica:

| Categoria | Quantidade | Células Afetadas & Status de Produção |
|---|---|---|
| **`ACTIVE_CANDIDATE`** | **10** | • `back_r / Walk`: 8f, 160ms/f, 1280ms, Method-02 temporal (Root Passed)<br>• `back_l / Walk`: 8f, 160ms/f, 1280ms, NW autêntico (Root Passed)<br>• `back_r / Unarmed`: 5f, 450ms, chave de impacto estendida em x=122 com crânio e gola alinhados à identidade do personagem<br>• `back_l / Unarmed`: 5f, 450ms, chave de impacto estendida em x=6 (NW) com crânio e gola alinhados<br>• `front_r / Defeat`: 5f, 700ms, terminal ajoelhado substituído por colapso inconsciente no solo (estágios 0..3 preservados)<br>• `front_l / Defeat`: 5f, 700ms, terminal ajoelhado substituído por colapso inconsciente no solo (estágios 0..3 preservados)<br>• `back_r / Sword`: 13f, 730ms, coreografia de corte com pose de corpo propulsora e arma independente (`recruit-sword`)<br>• `back_l / Sword`: 13f, 730ms, coreografia NW de corte com pose de corpo propulsora e arma independente<br>• `back_r / Axe`: 12f, 1005ms, coreografia de machado com pose engatilhada no ombro e arma independente (`militia-axe`)<br>• `back_l / Axe`: 12f, 1005ms, coreografia NW de machado com pose engatilhada e arma independente |
| **`UNCHANGED_ALIAS`** | **18** | Linha de base `complete-v1` (`b178422e1f7fc19f068c`) preservada byte a byte:<br>• `front_r` e `front_l` Idle, Walk, Unarmed, Sword, Axe, Hit (12 células)<br>• `back_r` e `back_l` Idle, Hit, Defeat (6 células) |
| **`IN_REVISION`** | **0** | Nenhuma célula em revisão. |
| **`IN_PRODUCTION`** | **0** | Nenhuma célula em fila de produção. |

---

### 2. Livro-Razão Contábil Rigoroso (Cap de Sessão: 66 Gerações)

| Etapa | Ferramenta | Job ID | Custo | Finalidade / Justificativa |
|---|---|---|---|---|
| **Draft-01 (rejeitado)** | `inpaint_image_pro_flash` | `af1e7ba8`, `ed109b13` | 12 gen | Morph / crossfade rejeitado; arquivado em `rejected/draft-01-crossfade/` |
| **Wave 1 Protótipo** | `animate_image` | `1bdc9771-10f8-4a2a-ab7e-ce066a79175e` | 2 gen | `back_r Walk` temporal 8f (Aprovado pelo Root) |
| **Wave 2** | `animate_image` | `64cd4cb7-dba7-4234-9f96-a9da268388fb` | 2 gen | `back_l Walk` temporal 8f base NW (Aprovado pelo Root) |
| **Wave 2** | `animate_image` | `2ace783c-ff36-499b-b473-52adad36459e` | 2 gen | `back_r Unarmed` rascunho fraco (rejeitado e arquivado em `rejected/weak-punch/`) |
| **Chave Soco R** | `inpaint_image_pro_flash` | `8ad79f7a-fa6e-47db-b002-8849121482f9` | 6 gen | Chave de impacto estendida x=122 para `back_r Unarmed` |
| **Chave Soco L** | `inpaint_image_pro_flash` | `72c2a726-a756-4511-963d-c6bfbb185985` | 6 gen | Chave de impacto estendida x=6 (NW) para `back_l Unarmed` |
| **Defeat Terminal R** | `inpaint_image_pro_flash` | `ef720a14-9a92-46be-b586-8d1295ccebf6` | 6 gen | Colapso no solo terminal para `front_r Defeat` |
| **Defeat Terminal L** | `inpaint_image_pro_flash` | `f1601bbd-bd2d-4661-88ac-70d348bc6a0c` | 6 gen | Colapso no solo terminal para `front_l Defeat` |
| **Chave Espada R** | `inpaint_image_pro_flash` | `4a000c0d-0f5f-4c8d-aaa5-247e7a243953` | 6 gen | Pose propulsora de corte traseiro para `back_r Sword` |
| **Chave Machado R** | `inpaint_image_pro_flash` | `c9f104c9-255e-4513-9388-b14ccf128b42` | 6 gen | Pose de golpe engatilhado no ombro para `back_r Axe` |
| **Chave Espada L** | `inpaint_image_pro_flash` | `4ea76c61-2dec-459c-bda5-15fde199d0b5` | 6 gen | Pose propulsora NW de corte para `back_l Sword` |
| **Chave Machado L** | `inpaint_image_pro_flash` | `ff359d8a-4614-4fed-a056-75429bff6810` | 6 gen | Pose de golpe engatilhado NW para `back_l Axe` |
| **TOTAL CONSUMIDO:** | — | — | **66 gen** | **Exatamente o teto autorizado da sessão (66 gerações)** |
| **Saldo Restante:** | — | — | **1421.70 gen** | Saldo verificado na conta |

---

### 3. Mestres Aseprite Canônicos (20 Arquivos Validados)

Todos os 20 mestres Aseprite candidatos (10 nativos 128×128 + 10 compostos 256×256) foram gerados via script Lua com perfil batch isolado e validados com `inspectAseprite`:

```
characters/orc-v1/source/aseprite/rear-recovery-v2/
├── native/
│   ├── walk-back_r.aseprite (128x128, 8f, 160ms/f)
│   ├── walk-back_l.aseprite (128x128, 8f, 160ms/f)
│   ├── unarmed-back_r.aseprite (128x128, 5f, [80,110,60,90,110]ms)
│   ├── unarmed-back_l.aseprite (128x128, 5f, [80,110,60,90,110]ms)
│   ├── defeat-front_r.aseprite (128x128, 5f, [70,95,115,130,290]ms)
│   ├── defeat-front_l.aseprite (128x128, 5f, [70,95,115,130,290]ms)
│   ├── sword-back_r.aseprite (128x128, 13f, 730ms total)
│   ├── sword-back_l.aseprite (128x128, 13f, 730ms total)
│   ├── axe-back_r.aseprite (128x128, 12f, 1005ms total)
│   └── axe-back_l.aseprite (128x128, 12f, 1005ms total)
└── composite/
    ├── back_r/walk-unarmed.aseprite (256x256, 8f)
    ├── back_l/walk-unarmed.aseprite (256x256, 8f)
    ├── back_r/unarmed-attack.aseprite (256x256, 5f)
    ├── back_l/unarmed-attack.aseprite (256x256, 5f)
    ├── front_r/defeat.aseprite (256x256, 5f)
    ├── front_l/defeat.aseprite (256x256, 5f)
    ├── back_r/sword-attack.aseprite (256x256, 13f)
    ├── back_l/sword-attack.aseprite (256x256, 13f)
    ├── back_r/axe-attack.aseprite (256x256, 12f)
    └── back_l/axe-attack.aseprite (256x256, 12f)
```

---

### 4. Status de Conformidade e Portões de Qualidade

- **Status Técnico:** `TECHNICALLY_COMPLETE`  
  Todos os arquivos de prancha, mestres `.aseprite`, frames nativos 128×128, frames compostos 256×256 e arquivos `clip.json` estão gerados, com hashes computados, durações verificadas e testes automatizados passando 100% (`node --test test/main-orc-complete.test.mjs`: 2 pass, 0 fail).
- **Status Artístico:** `VISUAL_REVIEW_REQUIRED`  
  Todos os 10 candidatos corrigem os defeitos da linha de base anterior (andar com passos alternados e pés ancorados em y=126, socos com extensão total e sem braço encolhido, derrotas frontais com colapso plano no solo, e coreografias de espada e machado com engatilhamento e propulsão verdadeiros).
- **Aprovação Artística:** `PENDING_CREATOR`  
  Apenas o criador pode conceder `CREATOR_APPROVED`.
