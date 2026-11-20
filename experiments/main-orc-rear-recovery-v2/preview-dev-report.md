# Relatório de Desenvolvimento do Visualizador Isolado de Revisão (Orc V1 Rear Recovery v2)

**Data:** 2026-10-26  
**Revisão:** `main-orc-rear-recovery-v2`  
**Personagem:** `orc-v1` (Verde Warcraft)  
**Proprietário do Visualizador (implementação inicial):** Preview DEV — Gemini 3.8 Flash (via Antigravity)  
**Correção de pendências e refresh atual:** GLM 5.3 Flash (via Cline) — 2026-10-26  
**Status Técnico:** `TECHNICALLY_COMPLETE` (fato de build; enquanto houver células conhecidas por defeito, o status exibido do pacote é `ARTISTIC_REVISION_REQUIRED`)  
**Status Artístico:** `ARTISTIC_REVISION_REQUIRED` (retorna a `VISUAL_REVIEW_REQUIRED` quando as células conhecidas forem corrigidas)  
**Aprovação Artística:** `PENDING_CREATOR`  

---

## 1. Verificação de Capacidade e Preservação de Escopo

- **Ambiente de Execução:** Windows PowerShell; interpretador Python absoluto verificado em `C:/Users/João Orlando/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe` (Python 3.12.14); Node.js v24.20.0.
- **Isolamento de Escopo Estrito:**
  - Nenhuma modificação em arquivos de arte (`.aseprite`, PNGs de sprites), scripts de produção Lua, documentação (`docs/`), contratos (`config/`), receitas (`recipes/`) ou ponteiros ativos (`characters/orc-v1/source/equipment-current.json`).
  - Nenhuma escrita no visualizador baseline ou no jogo: `Biblioteca de Arte/Personagens Jogaveis/Orc V1` e `Biblioteca de Arte/Estudos Comparativos/Orc principal - Biblioteca completa` foram estritamente preservados.
  - **Evidência de Preservação Byte-a-Byte do Baseline:**
    - `Biblioteca de Arte/Estudos Comparativos/Orc principal - Biblioteca completa/index.html`
    - SHA-256 inicial: `d1293e8afbf72aeafd815ca0eec0ce1c217a4790e1158608b30a37e50fca7213`
    - SHA-256 após a implementação: `d1293e8afbf72aeafd815ca0eec0ce1c217a4790e1158608b30a37e50fca7213` (idêntico).
- **Destino Isolado de Entrega:**  
  `Biblioteca de Arte/Estudos Comparativos/Orc principal - Recuperacao traseira/index.html`

---

## 2. Consumo Explícito do Manifesto de 28 Células (`candidate28manifest.json`)

O visualizador ingere `characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json` consumindo os status explícitos declarados e implementando a regra obrigatória de **não realizar fallback silencioso** para células afetadas pendentes:

| Categoria de Status | Qtd | Células | Comportamento no Estúdio |
| :--- | :---: | :--- | :--- |
| **`ACTIVE_CANDIDATE`** | **6** | `back_r/Walk`, `back_l/Walk`, `back_r/Unarmed`, `back_l/Unarmed`, `front_r/Defeat`, `front_l/Defeat` | Exibe candidato ativo v2 com frames reais da fonte. Badge verde `CANDIDATO ATIVO v2`. Comparação Antes/Depois lado a lado com folha baseline. |
| **`UNCHANGED_ALIAS`** | **18** | `front_r` (Idle, Walk, Unarmed, Sword, Axe, Hit)<br>`front_l` (Idle, Walk, Unarmed, Sword, Axe, Hit)<br>`back_r` (Idle, Hit, Defeat)<br>`back_l` (Idle, Hit, Defeat) | Exibe saída canônica baseline preservada byte-a-byte. Badge azul `ALIAS INALTERADO CANÔNICO`. |
| **`ARTISTIC_REVISION_REQUIRED`** | **4** | `back_r/Sword`, `back_r/Axe`, `back_l/Sword`, `back_l/Axe` | **Aviso Explícito (NÃO pronto):** `⚠️ REVISÃO ARTÍSTICA OBRIGATÓRIA` — candidato entregue foi REJEITADO (corpo+arma achatados em 1 camada em vez de 4; grip antigo; metadados inconsistentes). Exibido apenas para diagnóstico, com baseline rotulado como NÃO resolvido na seção Antes/Depois e link para a evidência da rejeição. O vocabulário legado `IN_REVISION` continua suportado. |
| **`IN_PRODUCTION`** | **0** | — | Nenhuma célula em fila no manifesto atual. |

> **Correção 2026-10-26 (GLM 5.3 Flash):** a tabela acima estava obsoleta (exibia 2 ativos / 16 aliases / 1 `IN_REVISION` / 9 `IN_PRODUCTION`). Todos os cartões-resumo, badges e a seção Antes/Depois agora são **derivados do manifesto** (`candidate28manifest.json` — atualmente 6/18/4/0), sem valores fixos no builder ou nos testes.

### Resolução de Caminhos de Armas (`Sword` / `Axe`)
Conforme documentado em `manifest-note-1.txt`, os clipes baseline de armas residem na subpasta `Attack/clip.json` (ex: `characters/orc-v1/source/complete-v1/front_r/Sword/Attack/clip.json`). O builder resolve nativamente essa estrutura sem depender de suposições ou caminhos quebrados.

---

## 3. Recursos e Controles Interativos Implementados

O estúdio em `Biblioteca de Arte/Estudos Comparativos/Orc principal - Recuperacao traseira/index.html` funciona de forma autônoma via `file://` (100% de assets locais copiados com hashes SHA-256):

1. **4 Direções:** `front_r` (SE), `front_l` (SW), `back_r` (NE), `back_l` (NW) com alternância individual no palco principal e comparação síncrona na grade de 4 câmeras.
2. **7 Ações com Separação Estrita de Espada e Machado:**
   - `Idle` (5f · 2200 ms · sem arma)
   - `Walk` (16f baseline / 8f candidato ativo Method-02 · sem arma)
   - `Unarmed` (Soco/Golpe físico · sem arma)
   - `Sword Attack` (Espada do Recruta · 13f · 730 ms)
   - `Axe Attack` (Machado de Milícia · 12f · 1005 ms)
   - `Hit` (Reação de dano · 5f · 450 ms · sem arma)
   - `Defeat` (Queda e colapso terminal · 5f · 700 ms · sem arma)
3. **Controle de Velocidades (`1x / 0.75x / 0.5x`):**
   - `1×` (Normal)
   - `0,75×` (Velocidade intermediária de inspeção)
   - `0,5×` (Câmera lenta)
   - `0,25×` (Análise detalhada)
4. **Escala Prática de Jogo (`practicalscale`):**
   - Opção `Escala Prática Jogo (128×128)` renderiza o sprite na proporção nativa exata do jogo (fator 0.5× sobre o canvas 256×256), além de zooms em 1× (256px), 1,25× (320px), 1,5× (384px) e 2× (512px).
5. **Avanço de Quadro (`frameadvance`):**
   - Botões `◀ Quadro` (`#step-prev`) e `Quadro ▶` (`#step-next`) pausam a execução e permitem inspecionar quadro a quadro, atualizando a fase, pegada e recorte de socket.
6. **Retenção Terminal de Queda (`terminalhold`):**
   - Ao executar `Defeat` (ou o modo de transição `Defeat → Terminal Hold`), a animação interrompe o avanço no quadro final e mantém o orc caído no chão (`st.done = true`, aviso `TERMINAL HOLD: Pose final mantida no solo`). O ciclo não reinicia involuntariamente mesmo com loop ativo.
7. **Modos de Transição:**
   - `Clipe isolado da ação`
   - `Idle → Attack → Idle` (transição sem arma / armada / sem arma)
   - `Walk → Idle` (parada de locomoção)
   - `Hit → Idle` (recuperação de dano)
   - `Defeat → Terminal Hold`
8. **Matriz de Cobertura e Diagnóstico (28 linhas):**
   - Tabela completa detalhando contagem de quadros, duração em milissegundos, semântica de loop, visibilidade de arma, status do manifesto e notas técnicas de cada célula.
   - Coluna de Aprovação Artística registra formalmente: `<span class="badge">PENDING_CREATOR</span>`.

---

## 4. Testes Automatizados e Verificação no Navegador

Dois conjuntos de testes automatizados foram criados e executados com sucesso:

### A. Teste de Integridade Estática e Links (`test/test_rear_recovery_review.py`)
- **Validação de Células:** 28 células inspecionadas e validadas com expectativas **derivadas do manifesto** (atualmente 6 ativos, 18 aliases inalterados, 4 em revisão artística obrigatória, 0 em produção) — nenhuma contagem fixa no teste; status de cada célula no HTML deve bater exatamente com `candidate28manifest.json`.
- **Varredura de 404s:** 15 tags `<img>` e 82 links `<a href>` estáticos inspecionados no HTML: **Zero 404s** (todos os arquivos, folhas, mestres Aseprite e páginas irmãs resolvem no disco).
- **Controles Verificados:** `#play`, `#reset`, `#step-prev`, `#step-next`, `#select-dir`, `#select-action`, `#select-transition`, `#speed`, `#zoom`, `#loop`, `#pending-alert`.
- **Resultado:** `ALL AUTOMATED REVIEW VALIDATIONS PASSED SUCCESSFULLY (28/28 cells, 0 404s)`.

### B. Teste de Runtime JavaScript e Handlers (`test/test_review_js_runtime.mjs`)
- **Execução em Sandbox DOM:**
  - Carregamento assíncrono de imagens e resolução de promessas.
  - Renderização inicial do palco principal e das 4 vistas (`main-canvas`, `main-info`, `dir-canvas-*`).
  - Teste de troca de ação para `back_r Sword` (dispara `⚠️ REVISÃO ARTÍSTICA OBRIGATÓRIA` com o literal `ARTISTIC_REVISION_REQUIRED` e aviso de candidato entregue REJEITADO NÃO pronto) e para `back_r Walk` (`✨ CANDIDATO ATIVO`).
  - Teste de troca de ação para `Defeat` (comportamento de terminal hold).
  - Teste de eventos dos botões `#step-next` e `#step-prev`.
- **Resultado:** `ASYNC RENDER AND EVENT HANDLER TESTS PASSED COMPLETELY`.

---

## 5. CLI do Gerador e Contrato de Integração

### Linha de Comando Disponível (CLI)
Para atualizar ou regenerar a revisão isolada a qualquer momento:

```powershell
# Comando principal dedicado:
& "C:\Users\João Orlando\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" tools/build-rear-recovery-review.py

# Apenas validação de esquema/manifesto (sem escrita):
& "C:\Users\João Orlando\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" tools/build-rear-recovery-review.py --check-only

# Personalização de manifesto ou pasta de saída:
& "C:\Users\João Orlando\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" tools/build-rear-recovery-review.py --manifest "caminho/para/manifest.json" --out-dir "caminho/para/saida"

# Delegação transparente a partir do builder mestre:
& "C:\Users\João Orlando\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" tools/build-main-orc-complete-review.py --rear-recovery
```

### Contrato com o Produtor Artístico (`candidate28manifest.json`)
Quando o art producer entregar novas animações (ex: soco desarmado corrigido, espada/machado de costas, queda frontal corrigida):

1. **Atualizar o status no manifesto:**
   - Mudar `status` de `"IN_PRODUCTION"` ou `"IN_REVISION"` para `"ACTIVE_CANDIDATE"`.
   - Apontar `clipJson` para o clipe final exportado (ex: `characters/orc-v1/source/rear-recovery-v2/{dir}/{action}/clip.json`).
   - Atualizar `notes` e `reviewStatus` (ex: `"PRODUCER_DELIVERED_PENDING_REVIEW"`).
2. **Executar o build:**
   - Rodar `python tools/build-rear-recovery-review.py`.
   - O builder copiará automaticamente os novos frames, folhas e mestres, removerá o alerta de pendência para as células concluídas e gerará o visualizador atualizado sem qualquer necessidade de alteração de código.

---

## 6. Sumário de Arquivos Modificados / Criados

- `tools/build-rear-recovery-review.py`: Script principal do gerador isolado de revisão (criado).
- `tools/build-main-orc-complete-review.py`: Extensão mínima com `if __name__ == '__main__':` e suporte a delegação CLI `--rear-recovery` (protege integralmente o baseline contra escritas acidentais).
- `Biblioteca de Arte/Estudos Comparativos/Orc principal - Recuperacao traseira/index.html`: Estúdio visualizador interativo completo (861 arquivos copiados/indexados).
- `Biblioteca de Arte/Estudos Comparativos/Orc principal - Recuperacao traseira/catalogo.json`: Metadados estruturados e matriz de status da revisão.
- `Biblioteca de Arte/Estudos Comparativos/Orc principal - Recuperacao traseira/manifest.json`: Manifesto com hashes SHA-256 de todos os 861 arquivos copiados.
- `test/test_rear_recovery_review.py`: Validador automatizado estático e de links (criado).
- `test/test_review_js_runtime.mjs`: Teste automatizado de runtime JS e eventos (criado).
- `experiments/main-orc-rear-recovery-v2/preview-dev-report.md`: Este relatório (criado).

Nenhuma fila de arte ou integração Unity foi bloqueada; a entrega do visualizador está completa e aguarda a finalização dos ativos pendentes pelo produtor artístico.

---

## 7. Correção de pendências e refresh atual (2026-10-26 · GLM 5.3 Flash via Cline)

Correções aplicadas mantendo o CLI e o comportamento padrão do builder (incl. delegação `--rear-recovery` do builder mestre, intocada):

1. **Vocabulário de status:** suporte a `ARTISTIC_REVISION_REQUIRED` (atual) e `IN_REVISION` (legado) em todos os pontos de ramificação (badges da tabela, alertas JS, badges das 4 câmeras, `catalogo.json`).
2. **Status do pacote:** enquanto houver células conhecidas por defeito, o cabeçalho exibe `ARTISTIC_REVISION_REQUIRED` + `PENDING_CREATOR` (sem `TECHNICALLY_COMPLETE`/`VISUAL_REVIEW_REQUIRED` como rótulo do pacote inteiro); resultados técnicos permanecem como fatos de build (28/28 fontes resolvidas). Sem rótulos novos de taxonomia.
3. **Resumo derivado:** cartões de contagem calculados das células do manifesto (6 ativos / 18 aliases / 4 revisão / 0 produção), com aviso no build se os campos-resumo do manifesto divergirem do computado.
4. **Antes/Depois dinâmico:** cobre TODAS as células afetadas (10) a partir das fontes reais — candidatos ativos com baseline vs candidato atual; células `ARTISTIC_REVISION_REQUIRED` com baseline rotulado NÃO resolvido e o candidato entregue rejeitado exibido apenas para diagnóstico (o narrative obsoleto do weak-punch foi removido).
5. **Alerta de pendência corrigido:** textos agora refletem que os frames exibidos nas células em revisão são o candidato REJEITADO (não baseline), marcados "NÃO está pronto".
6. **Testes manifest-driven:** `test/test_rear_recovery_review.py` e `test/test_review_js_runtime.mjs` derivam expectativas do manifesto (sem contagens fixas) e validam cartões derivados, status do pacote, cobertura Antes/Depois de 10 células e alertas explícitos.
7. **Checagem real de navegador:** novo `test/browser-check-rear-recovery-review.mjs` (Playwright + Chromium headless próprio, `file://`, espera limitada ≤45 s por passo, prazo total 120 s, browser fechado em `finally`): 20/20 verificações aprovadas em ~7,5 s, com screenshots em `experiments/main-orc-rear-recovery-v2/browser-checks/`.
8. **Preservação:** baseline `Orc principal - Biblioteca completa/index.html` byte-idêntico (`d1293e8afbf72aeafd815ca0eec0ce1c217a4790e1158608b30a37e50fca7213`); nenhuma edição de arte/metadados/docs/config/recipes; sem chamadas pagas, Unity ou commits.

**Refresh final pendente:** reexecutar `python tools/build-rear-recovery-review.py` + testes quando o produtor artístico publicar o `production-final-report` com as fontes corrigidas de Sword/Axe traseiros (contagens podem mudar; tudo é derivado). QA independente Argon (root): NÃO INICIADO.
