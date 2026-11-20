# Preview Final Report — Isolated Review Studio (Orc V1 Rear Recovery v2)

**Data:** 2026-10-26
**Tarefa executada:** `experiments/main-orc-rear-recovery-v2/preview-fallback-glm-task.md` (única tarefa pendente de preview; escopo herdado de `preview-dev-task.md` + `preview-finalization.txt` + `finalization-hold-for-weapon-fix.txt`)
**Personagem/Revisão:** `orc-v1` (Verde Warcraft) · `main-orc-rear-recovery-v2`
**Procedência dos modelos (reportada com precisão):**
- **Implementação inicial do visualizador:** Gemini 3.8 Flash (via Antigravity) — histórico, não renomeada.
- **Correção de pendências, refresh de dados e checagens atuais (este relatório):** **GLM 5.3 Flash (via Cline)**.
- **QA independente (Argon, root):** NÃO INICIADO — nenhum autoaprovamento.

---

## 1. Verificação de capacidade (executada primeiro)

| Capacidade | Resultado |
| :--- | :--- |
| Terminal PowerShell | OK |
| Leitura/escrita no repositório | OK (teste de escrita criado/lido/removido em `experiments/main-orc-rear-recovery-v2/`) |
| Python | `C:/Users/João Orlando/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe` → Python 3.12.14 |
| Node | v24.20.0 |
| Playwright (módulo) | `C:/Users/João Orlando/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright` presente |
| Chromium headless | `C:/Users/João Orlando/AppData/Local/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-win64/chrome-headless-shell.exe` presente |

Sem `msedge.exe --dump-dom`; Playwright com launch próprio, limites por passo ≤45 s, prazo total 120 s, `browser.close()` em `finally`. Nenhum processo do usuário ou da root foi tocado; nenhum helper permaneceu rodando.

## 2. Estado real do manifesto (derivado, não assumido)

`characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json`: **6 `ACTIVE_CANDIDATE`** (`back_r/Walk`, `back_l/Walk`, `back_r/Unarmed`, `back_l/Unarmed`, `front_r/Defeat`, `front_l/Defeat`), **4 `ARTISTIC_REVISION_REQUIRED`** (`back_r/Sword`, `back_r/Axe`, `back_l/Sword`, `back_l/Axe` — candidatos entregues REJEITADOS: corpo+arma achatados em 1 camada, grip antigo, metadados inconsistentes; reparo local pela ART 64f9 sem chamadas pagas), **18 `UNCHANGED_ALIAS`**, **0 `IN_PRODUCTION`**. As 4 células de armas **não** são apresentadas como prontas.

## 3. Mudanças no builder (`tools/build-rear-recovery-review.py`) — implementação preservada, correção mínima

1. Vocabulário duplo: `ARTISTIC_REVISION_REQUIRED` (atual) + `IN_REVISION` (legado) em todas as ramificações (tabela, alertas JS, badges das 4 câmeras, `catalogo.json`).
2. Pacote: cabeçalho exibe **`ARTISTIC_REVISION_REQUIRED`** + `PENDING_CREATOR` enquanto houver células conhecidas por defeito (sem `TECHNICALLY_COMPLETE`/`VISUAL_REVIEW_REQUIRED` como rótulo do pacote inteiro). Validação técnica permanece como fato de build ("28/28 clipes com fonte resolvida"), sem rótulo novo de taxonomia. Quando as células forem corrigidas, o status volta ao vocabulário do contrato (`VISUAL_REVIEW_REQUIRED` + `PENDING_CREATOR`) — derivação automática, sem hardcode.
3. Cartões-resumo e `catalogo.json` calculados das células do manifesto (hoje 6/18/4/0), com warning no build se os campos-resumo divergirem do computado. Pronto para os futuros 12 ativos/16 aliases sem alteração de código.
4. Seção Antes/Depois **dinâmica para TODAS as células afetadas (10)** com frames das fontes reais: candidatos ativos (baseline vs candidato atual) e células em revisão (baseline rotulado "NÃO resolvida" + candidato entregue REJEITADO "NÃO pronto", com link para a evidência da rejeição). O narrative obsoleto do weak-punch (que fingia ser candidato atual) foi removido.
5. Alerta de pendência corrigido: frames exibidos nas células em revisão são o candidato REJEITADO (não "referência baseline", como dizia o texto antigo), marcados explicitamente como não prontos.
6. CLI preservado: `python tools/build-rear-recovery-review.py`, `--check-only`, `--manifest`, `--out-dir`; delegação `--rear-recovery` do `tools/build-main-orc-complete-review.py` intocada.

## 4. Comandos executados e resultados reais

| Comando | Resultado |
| :--- | :--- |
| `python -m py_compile tools/build-rear-recovery-review.py` | OK |
| `python tools/build-rear-recovery-review.py --check-only` | `CHECK_PASSED` — 28/28 células, todas as fontes de clip e baseline resolvem (6 ACTIVE / 18 ALIAS / 4 ARTISTIC_REVISION_REQUIRED) |
| `python tools/build-rear-recovery-review.py` | Build OK — **856 arquivos** copiados/indexados (5 imagens de evidência obsoletas do weak-punch deixaram de ser copiadas) |
| `python test/test_rear_recovery_review.py` | **PASS** — 28/28 células com status idêntico ao manifesto; pílulas derivadas (6/18/4/0); pacote `ARTISTIC_REVISION_REQUIRED`; Antes/Depois cobre 10 células afetadas; zero 404s (27 `<img>`, 98 `<a>`); controles 1×/0,75×/0,5×, escala prática 128×128, terminal hold, Sword/Axe separados, `PENDING_CREATOR` |
| `node test/test_review_js_runtime.mjs` | **PASS** — `back_r/Sword` dispara `REVISÃO ARTÍSTICA OBRIGATÓRIA` com literal `ARTISTIC_REVISION_REQUIRED` e "NÃO está pronto"; `back_r/Walk` mostra `CANDIDATO ATIVO`; step-next/prev OK |
| `node test/browser-check-rear-recovery-review.mjs` (novo, in-repo, reproduzível) | **PASS 20/20 em 7,5 s** — Chromium headless real em `file://`: 28/28 células selecionáveis com canvas pintando pixels reais e badge = literal do manifesto; 32/32 `<img>` decodificados; 0 requisições falhas/4xx; velocidade medida 1× (quadro 7/8 após 1 s) vs 0,5× (4/8); escala prática 128 px; step ±1; `Defeat` atinge TERMINAL HOLD 5/5 e mantém sem reinício; alerta `ARTISTIC_REVISION_REQUIRED` "NÃO está pronto" em `back_r/Sword`; sem alerta em alias; `CANDIDATO ATIVO`+`PENDING_CREATOR` em `back_r/Walk`; Antes/Depois com 10/10 cartões e baseline+candidato decodificados; `catalogo.json` derivado bate com o manifesto |

**Screenshots reais (Chromium headless):** `experiments/main-orc-rear-recovery-v2/browser-checks/` — `studio-overview.png`, `before-after-affected-cells.png`, `pending-alert-revision-sword.png`, `defeat-terminal-hold.png`.

**Preservação comprovada:**
- Baseline canônico `Biblioteca de Arte/Estudos Comparativos/Orc principal - Biblioteca completa/index.html`: SHA-256 `d1293e8afbf72aeafd815ca0eec0ce1c217a4790e1158608b30a37e50fca7213` — **byte-idêntico**.
- Viewer isolado atualizado `Biblioteca de Arte/Estudos Comparativos/Orc principal - Recuperacao traseira/index.html`: SHA-256 `a3ea5a89a72e21a17b2d773c6dedaf8c1160bd6b650b5e139018820546c669c3` (build atual).

## 5. Limites respeitados

Nenhuma edição em arte/mestres/metadata Lua (ART 64f9), docs/config/recipes (knowledge2046) ou ponteiros ativos. Sem chamadas pagas, sem Unity, sem commits, sem novos agentes de QA. `preview-dev-report.md` corrigido (contagens obsoletas 2/16/1/9 → derivadas 6/18/4/0; procedência correta: implementação inicial por Gemini 3.8 Flash, não "Argon"; correção atual por GLM 5.3 Flash via Cline).

## 6. Pendências verdadeiras (relatório idle — sem espera infinita)

1. **Refresh final dos dados:** reexecutar `python tools/build-rear-recovery-review.py` + os 3 testes quando o produtor artístico publicar o `production-final-report` com as fontes corrigidas de Sword/Axe traseiros e nova checagem de camadas. As contagens podem mudar (ex.: 12 ativos/16 aliases) — tudo é derivado do manifesto.
2. **Sword/Axe traseiros** permanecem `ARTISTIC_REVISION_REQUIRED` (reparo local da ART 64f9 em curso; 4 células não são review-ready).
3. **QA independente Argon (root):** NÃO INICIADO; só após o freeze final do viewer.
4. **Aprovação artística:** `PENDING_CREATOR` (nunca autoconcedida). `runtimeImplemented: false`; nenhuma escrita em `../TacticsRPG`.