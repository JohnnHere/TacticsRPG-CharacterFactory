# Relatório de Re-Revisão de QA Independente — Três Ciclos Traseiros Desarmados (Repair 1)

**Data / Hora:** 2026-10-29T16:51:30Z  
**Papel:** QA Independente (fora do Copilot / não orquestração / não produtor)  
**Modelo Revisor:** Gemini 3.8 Flash (High) via Antigravity  
**Veredito Global:** `REVISIONS_REQUIRED`  
**Status Artístico Global da Tarefa:** `ARTISTIC_REVISION_REQUIRED` (Preservado / Inalterado)  
**Status do Criador:** `PENDING_CREATOR`  
**Escalonamento Obrigatório:** **SIM** (Segunda reprovação consecutiva de `DEFECT-REAR-02` em `back_l-Axe-full` pela mesma sessão produtora `3c2b5bd7`)  
**Promoção Runtime / Unity:** `runtimeImplemented: false` (nenhuma escrita em `../TacticsRPG`)  
**Arquivo Estruturado:** [`rear-bodies-repair1-result.json`](file:///C:/Users/Jo%C3%A3o%20Orlando/Documents/Projetos%20Unity/TacticsRPG-CharacterFactory/experiments/main-orc-combat-rescue-v5/qa-antigravity-flash/rear-bodies-repair1-result.json)

---

## 1. Escopo e Objeto de Avaliação

Re-revisão cirúrgica independente do pacote **`BODY_THREE_REPAIR1_READY`** entregue pelo DEV `3c2b5bd7`, cobrindo os 3 ciclos traseiros desarmados:
1. `back_l-Sword-full` (12f / 730 ms) — Reparo do defeito REAR-03 (F05)
2. `back_r-Sword-full` (12f / 730 ms) — Reparo do defeito REAR-01 (F06)
3. `back_l-Axe-full` (12f / 1100 ms) — Reparo do defeito REAR-02 (F02)

*(Nota de escopo: O ciclo `full-back-r-axe`, previamente aprovado com `READY_FOR_REAR_GRIPS`, permaneceu intocado e preservado fora do escopo desta re-revisão)*.

---

## 2. Matriz de Hashes e Vereditos Individuais

| Ciclo | Ação / Categoria | Duração / Quadros | SHA-256 do `clip.json` em `repair1` | Veredito |
|---|---|---|---|---|
| `back_l-Sword-full` | `back_l` / Sword Attack | 730 ms / 12f | `74da046b19f98297410327063db70b5a8dad644fea9a53f0f4f5f589fcb5ab32` | **`READY_FOR_REAR_GRIPS`** |
| `back_r-Sword-full` | `back_r` / Sword Attack | 730 ms / 12f | `e022c53bf240ad312aff191eb95a8371522f15e422af10bac0f2115238b768a1` | **`REVISIONS_REQUIRED`** |
| `back_l-Axe-full` | `back_l` / Axe Attack | 1100 ms / 12f | `d0bf1f8be1f7d8f33e15ffa1564f370fd92a02d0d9e42c25ed59cc42daa9f702` | **`REVISIONS_REQUIRED`** *(2ª Reprovação)* |

---

## 3. Auditoria Detalhada dos Três Reparos

### 3.1. `back_l-Sword-full` — REAR-03: APROVADO (`READY_FOR_REAR_GRIPS`)
- **Auditoria do Defeito:** O gancho/filamento preto de 7-10 pixels projetando-se no ar acima da ombreira direita em F05 (`x=94..98, y=28..33`) foi **totalmente removido** (0 pixels de gancho restantes, transparência pura `rgba(0,0,0,0)` confirmada).
- **Integridade da Ombreira:** A linha de crista da ombreira em `y=34` foi preservada sem erosão ou buracos.
- **Auditoria de 12 Quadros:** Todas as 9 chaves aprovadas mantêm-se 100% byte-idênticas; 0 pixels de halo (`RGB > 190`); alinhamento de chão exato (`y=126` nativo, `y=190` composto); ausência de contaminação por armas no corpo.
- **Veredito:** **`READY_FOR_REAR_GRIPS`** (apto para acoplamento de pegada).

---

### 3.2. `back_r-Sword-full` — REAR-01: REPROVADO COM RESSALVAS LOCAIS (`REVISIONS_REQUIRED`)
- **Auditoria do Defeito Principal:** O grande rastro curvo de corte (*swoosh*) de 272 pixels claros foi em sua maior parte eliminado, reduzindo os halos globais para 0.
- **Defeitos Residuais Críticos Identificados em F06:**
  1. **Pixels Flutuantes no Ar (DEFECT-REAR-01-RESIDUAL-A):**
     - **Evidência:** Foram deixados **5 pixels cinzentos desconectados** flutuando no vazio à direita da mão em `(112,64)`, `(110,69)`, `(109,70)`, `(108,71)` e `(107,72)` (`rgba 134..151, 255`). Trata-se da ponta externa do rastro original que o script de limpeza não apagou. Esses pixels formam uma linha pontilhada flutuante visível a 2-7 pixels de distância da silhueta do corpo.
  2. **Inconsistência Material na Túnica/Malha (DEFECT-REAR-01-RESIDUAL-B):**
     - **Evidência:** Na reconstrução em `y=88..94, x=45..55`, o DEV preencheu a ranhura do antigo rastro com vermelho-marrom de couro de túnica (`#592d2b` / `#34181e`) diretamente sobre a região central do saiote de cota de malha, gerando uma faixa vermelha diagonal espúria através da malha de aço que em F05 e F07 é uniformemente cinza/aço (`#413f4c` / `#1f1c24`).
- **Sugestão Segura de Reparo:**
  - Converter os 5 pixels em `(112,64)` e `(107..110, 69..72)` para alfa 0 transparente.
  - Ajustar o preenchimento da malha em `y=88..94, x=45..55` para a paleta de aço de F05/F07.
  - **Custo: 0 créditos PixelLab** (retoque cirúrgico local no Aseprite).

---

### 3.3. `back_l-Axe-full` — REAR-02: REPROVADO CRITICAMENTE (`REVISIONS_REQUIRED` — 2ª Reprovação)
- **Auditoria do Defeito Principal:** O prompt exigia explicitamente: *"machado+cabo devem sumir mantendo braço/punho fechado compatível F03"*.
- **Constatação Perceptual em F02 (`02.png`):**
  - O DEV removeu apenas a lâmina de ferro metálica saliente.
  - **A haste horizontal de madeira marrom do machado continua repousando sobre o trapézio e o pescoço.**
  - No término direito dessa haste, o DEV apenas pintou um bloco retangular de couro marrom em `x=83..92, y=15..20`, acompanhado de um pino vertical preto em `x=70, y=14..18`.
  - O membro superior direito em F02 **não representa uma mão erguendo-se organicamente** entre F01 (braço baixo, mão no quadril) e F03 (hoist erguido com punho fechado junto à nuca). Permanece uma trave horizontal de madeira com um toco retangular apoiado transversalmente sobre o pescoço.
- **Impacto:** Persistência direta de violação `layers-off`. Ao acoplar a camada de equipamento independente `weaponFront`/`weaponBack`, haverá colisão e duplicação da haste do machado.
- **Escalonamento Mandatório:** Conforme regra expressa do usuário (*"Se problema original confirmado persistir, é segunda reprovação mesma especialidade, Root deverá escalonar produtor conforme pedido; não afrouxar critérios para só passar"*), este QA não afrouxa os critérios e registra formalmente a **SEGUNDA REPROVAÇÃO DA MESMA ESPECIALIDADE** para `back_l-Axe-full`. O Root deve proceder com o escalonamento do produtor.

---

## 4. Auditoria Técnica dos 36 Quadros em `repair1`

- **Preservação de Hashes das 9 Chaves:** Auditados F03, F04 e F07 nos 3 ciclos. **100% de paridade criptográfica** com as chaves aceitas pelo QA.
- **Linhas de Chão:** Cravadas em `y=126` em todos os 36 quadros nativos 128×128; cravadas em `y=190` em todos os 36 quadros compostos 256×256.
- **Contagem de Halos:** 0 pixels de halo (`RGB > 190`) em 35 dos 36 quadros (F06 de `back_l-Sword` contém 1 pixel especular cinza 191 legítimo na borda de armadura).
- **Durações e Metadados:** Durations nominais (730 ms para Sword, 1100 ms para Axe) e cabeçalhos Lua compatíveis com o padrão do projeto.

---

## 5. Limitação Perceptual Declarada

A inspeção foi executada quadro a quadro em repouso, em matrizes de pixel nativas (128×128), escalas táticas (64×64) e comparações diferenciais antes/depois. **Não foi realizada observação contínua de reprodução a 1× em tempo real em navegador/player contínuo.** Conforme diretrizes formais do Root, essa limitação de interface é conhecida, transparente e não invalida o diagnóstico estático de pixels acima.

---

## 6. Contabilidade de Recursos

- **Gerações PixelLab de Produção:** 0 chamadas consumidas nesta revisão de QA.
- **Custo LLM:** Custo LLM não informado (sem estimativas inventadas de $0.00).
- **Edição de Arquivos de Arte:** Nenhuma. Todos os arquivos de arte originais permanecem intactos.

---

## 7. Conclusão e Encaminhamento ao Root

1. **`back_l-Sword-full`:** **`READY_FOR_REAR_GRIPS`**. Reparo de F05 validado com sucesso. Apto para receber pegada traseira.
2. **`back_r-Sword-full`:** **`REVISIONS_REQUIRED`**. O swoosh foi removido, restando apenas um retoque cirúrgico rápido de 5 pixels flutuantes em F06 e ajuste de cor da malha.
3. **`back_l-Axe-full`:** **`REVISIONS_REQUIRED` (2ª Reprovação)**. O machado/haste em F02 não foi resolvido anatomicamente, persistindo como trave no ombro. **Requer escalonamento de produtor pelo Root.**
4. **Governança:** O status global permanece **`ARTISTIC_REVISION_REQUIRED (PENDING_CREATOR)`**. Parando e aguardando decisões do Root sobre o escalonamento e retoques.
