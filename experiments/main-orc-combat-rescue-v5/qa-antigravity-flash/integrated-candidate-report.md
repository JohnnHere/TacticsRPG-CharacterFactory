# Parecer Independente de QA — Candidato Integrado Orc V1 (28 Células)

**Data:** 29 de outubro de 2026  
**Revisor:** Gemini 3.8 Flash High via Antigravity (Painel de QA Independente)  
**Status do Veredito:** `READY_FOR_CREATOR_REVIEW`  
**Status Artístico Global:** `VISUAL_REVIEW_REQUIRED` (`PENDING_CREATOR`)  
**Status Técnico:** `TECHNICAL_PASS`  
**Integração Unity:** `runtimeImplemented: false` | `eligibleForIntegration: false`  

---

## 1. Escopo e Objeto de Revisão

Esta auditoria independente final avalia a **composição e integridade do pacote integrado** do Orc V1 (Verde Warcraft) declarado no manifesto canônico:
- **Arquivo:** `characters/orc-v1/source/combat-rescue-v5/candidate28manifest.json`
- **SHA-256 Confirmado:** `58152a101e16cbc031349b3308649f9ccaa38b99782d4e23bcf2ee43fddc3794`
- **Matriz Canônica:** 28 células (4 direções × 7 ações)
- **Total de Quadros:** 226 quadros (compostos e camadas)
- **Hashes Auditados:** 964 hashes verificados em disco

O objetivo desta etapa não é refazer individualmente as auditorias estáticas e cinemáticas dos 8 clipes armados já aprovados em pareceres específicos (`front-r-sword-full-result.json`, `qa-result.json`, `rear-axe-full-result.json`, `rear-sword-l-back-full-result.json`, `rear-two-remaining-result.json`), mas sim validar a **coerência do pacote integrado**, a ausência de regressões, a integridade da política `attack-only-v1`, a consistência coreográfica entre vistas e a veracidade das declarações do manifesto.

---

## 2. Composição da Matriz (28 Células)

O manifesto compõe com precisão cirúrgica **13 candidatos ativos** e **15 pseudônimos protegidos (aliases)**:

### 2.1 Células Ativas Candidatas (13 células)
1. **Ciclos de Ataque com Espada (4 vistas):**
   - `front_r/Sword`: 13f, 730 ms (corte diagonal descendente)
   - `front_l/Sword`: 13f, 730 ms (corte diagonal descendente)
   - `back_r/Sword`: 12f, 730 ms (corte diagonal traseiro, mão direita dominante)
   - `back_l/Sword`: 12f, 730 ms (corte diagonal traseiro em afastamento)
2. **Ciclos de Ataque com Machado (4 vistas):**
   - `front_r/Axe`: 12f, 1005 ms (golpe overhead pesado, apex e impacto no solo)
   - `front_l/Axe`: 12f, 1005 ms (golpe overhead pesado)
   - `back_r/Axe`: 12f, 1100 ms (golpe overhead traseiro com peso corporal e recuo)
   - `back_l/Axe`: 12f, 1100 ms (golpe overhead traseiro profundo)
3. **Ciclos de Desarmado / Soco (4 vistas):**
   - `front_r/Unarmed`: 5f, 450 ms (recoil F03 preservado)
   - `front_l/Unarmed`: 5f, 450 ms
   - `back_r/Unarmed`: 5f, 450 ms
   - `back_l/Unarmed`: 5f, 450 ms
4. **Locomoção Localizada (1 vista):**
   - `back_l/Walk`: 16f, 1600 ms (retoque de cor F04-F07 sem alteração de timing ou alfa)

### 2.2 Pseudônimos Protegidos / Unchanged Aliases (15 células)
- **Idle (4 vistas):** `front_r/Idle`, `front_l/Idle`, `back_r/Idle`, `back_l/Idle` (5 quadros, padrão `idle-balanced-v1` rigorosamente preservado).
- **Hit (4 vistas):** `front_r/Hit`, `front_l/Hit`, `back_r/Hit`, `back_l/Hit` (5 quadros, 450 ms).
- **Defeat (4 vistas):** `front_r/Defeat`, `front_l/Defeat`, `back_r/Defeat`, `back_l/Defeat` (5 quadros, colapso volumétrico com terminal estável no chão).
- **Walk Não Editado (3 vistas):** `front_r/Walk`, `front_l/Walk`, `back_r/Walk` (16 quadros, 1600 ms).

*Zero células em revisão (`inRevision: []`) e zero células em fila de produção (`inProduction: []`).*

---

## 3. Auditoria Técnica e Provas de Sustentação

A auditoria independente executou scripts dedicados sobre o disco (`audit_integrated_manifest.cjs`), confrontando os artefatos com o manifesto:

1. **Integridade de Hashes dos Clipes (28/28):**
   - Cada um dos 28 arquivos `clip.json` referenciados existe e tem SHA-256 byte-idêntico ao declarado na matriz.
2. **Validação Técnica Ampla (`technical-validation.json`):**
   - 226 quadros e 964 hashes avaliados com veredito `TECHNICAL_PASS`.
   - Compatibilidade de canais RGB, alfa e geometria `128×128` cravada em todas as camadas.
3. **Reexportação de Mestres Aseprite em Lote (`source-reexports`):**
   - O diretório `experiments/main-orc-combat-rescue-v5/source-reexports/58152a101e16cbc031349b3308649f9ccaa38b99782d4e23bcf2ee43fddc3794/` contém a re-renderização em lote via Aseprite CLI de **42 mestres salvos**.
   - Veredito registrado: `PASS_SAVED_SOURCE_EXPORTS`, declarando explicitamente `artisticallyApproved: false`.
4. **Preservação de Entradas Protegidas (`input-preservation-result.json`):**
   - 3.506 arquivos protegidos de entrada verificados contra a baseline. Divergências: 0 (`PASS 3506 0`).
5. **Verificações de Navegador e Estúdio (`browser-checks-final`):**
   - 21 verificações aprovadas em player Chromium headless (`BROWSER CHECK PASSED`).
   - Evidências gráficas capturadas sem regressão de layout, sem imagens quebradas e com correta renderização do estúdio comparativo em `Biblioteca de Arte/Estudos Comparativos/Orc principal - Resgate de combate/index.html`.

---

## 4. Auditoria Semântica e Coreográfica

### 4.1 Conformidade Estrita com `attack-only-v1`
A política exige que armas sejam itens isolados, aparecendo **exclusivamente** durante a execução do ataque:
- **Repouso e Locomoção:** Todas as 15 células de alias e os 4 ciclos de desarmado possuem exatamente **zero** pixels de equipamento e nenhuma camada ativa de arma.
- **Entrada e Recuperação do Golpe:** Nos 8 ciclos armados (`Sword` e `Axe` nas 4 vistas), os quadros iniciais de antecipação (`F00` e `F01`) possuem as camadas `weaponBack`, `weaponFront` e `handFront` preenchidas com o PNG vazio transparente (`3c6c50f94ab3...`, 0 pixels).
- **Término Limpo:** Nos quadros finais de recuperação pós-golpe (`F11-F12` na espada; `F09-F11` no machado), todas as camadas de arma retornam ao estado vazio e transparente, assegurando que o orc conclui o golpe desarmado, pronto para retransição suave a Idle/Walk desarmado.

### 4.2 Consistência Entre Vistas e Famílias de Armas
- **Família Sword (Corte Diagonal):**
  - Duração cravada de **730 ms** nas quatro vistas (13f nas vistas frontais, 12f nas traseiras).
  - Trajetória coerente de corte em arco diagonal, respeitando a postura do orc sem torção não anatômica.
- **Família Axe (Golpe Overhead Pesado):**
  - Duração cravada de **1005 ms** (frontais) e **1100 ms** (traseiras).
  - Arco descendente vertical completo: elevação acima da cabeça (apex em F04), queda com peso corporal concentrado e impacto/recuo legível no solo (F07).
- **Dominância Anatômica e Não-Espelhamento:**
  - O orc permanece estritamente destro nas 4 direções, com a mão direita conduzindo a empunhadura e o braço esquerdo atuando no equilíbrio e contra-apoio.
  - Pares de vistas opostas (`front_r` vs `front_l`, `back_r` vs `back_l`) foram verificados por hash e decodificação: todos possuem hashes e geometrias distintos. **Zero espelhamento horizontal (flip 2D) detectado.**

---

## 5. Limites e Trava de Governança

Esta aprovação de QA independente é estrita e delimitada:
1. **Completude Técnica != Aprovação Artística:** O veredito `READY_FOR_CREATOR_REVIEW` atesta que o pacote integrado está técnica e formalmente apto a ser inspecionado pelo criador, sem inconsistências estruturais internas.
2. **Aprovação Artística Final:** Permanece exclusiva do criador humano (`PENDING_CREATOR`). Nenhum agente ou revisor técnico pode declarar o orc artisticamente aprovado.
3. **Isolamento de Runtime Unity:**
   - `eligibleForIntegration`: `false`
   - `runtimeImplemented`: `false`
   - Nenhuma escrita, modificação ou cópia foi efetuada no repositório Unity (`../TacticsRPG`).
4. **Percepção Temporal Contínua:**
   - A avaliação técnica valida a anatomia, camadas, temporizações e reprodução em player headless Chromium; a avaliação cinemática estética contínua a 1× em contexto de jogo real cabe à revisão soberana do criador.

---

## 6. Veredito Final de Integração

| Critério | Resultado |
|---|---|
| Integridade do Manifesto (SHA-256) | **PASS** (`58152a101e...`) |
| Cobertura Canônica (28 células / 226 quadros) | **PASS** (13 ativas / 15 aliases) |
| Política `attack-only-v1` | **PASS** (100% conforme) |
| Independência Direcional (Zero espelhamento) | **PASS** (4 vistas autônomas) |
| Reexportação de Mestres Aseprite (42 masters) | **PASS** (`PASS_SAVED_SOURCE_EXPORTS`) |
| Preservação de Entradas (3.506 arquivos) | **PASS** (0 divergências) |
| Travas de Governança Unity / Criador | **PASS** (`eligibleForIntegration: false`) |

**Veredito:** **`READY_FOR_CREATOR_REVIEW`**  
O candidato integrado `candidate28manifest.json` está pronto para a inspeção interativa do criador no estúdio de comparação visual (`Biblioteca de Arte/Estudos Comparativos/Orc principal - Resgate de combate/index.html`).

---

## 7. Contabilidade de Geração

> **Nota Obrigatória:** 0 chamadas PixelLab de produção nesta revisão; custo LLM não informado.
