# Confirmação de QA Independente — Normalização de Chaves de Camada (`path` &rarr; `png`)

**Veredito:** `NORMALIZATION_CONFIRMED`  
**Status Técnico:** `TECHNICALLY_COMPLETE`  
**Data/Hora:** 2026-10-29T18:27:00Z  
**Revisor:** Gemini 3.8 Flash (High) via Antigravity QA Independente  
**Recursos Utilizados:** 0 chamadas PixelLab de produção nesta revisão; custo LLM não informado.

---

## 1. Contexto e Objeto da Verificação

Em `back_r/Sword` e `back_l/Axe`, o especialista de pegada havia emitido os mapeamentos de camada por quadro com o identificador de propriedade `path` em vez do padrão canônico da fábrica (`png`).
O Root Orchestrator realizou a normalização estrita do nome dessa chave (substituindo `"path":` por `"png":`) sem alterar nenhum pixel, duração, visibilidade ou mestre, preservando os arquivos aprovados originais em `experiments/main-orc-combat-rescue-v5/rear-grip-flash/pre-normalization/`.

Esta verificação independente auditou no disco as 4 condições requeridas pelo Root.

---

## 2. Auditoria dos Quatro Critérios

### 2.1 Presença Exclusiva da Chave Canônica `png` e Integridade dos Arquivos
- **`back_r/Sword`:** Todas as 48 camadas (12 quadros × 4 camadas: `weaponBack`, `body`, `weaponFront`, `handFront`) contêm agora exclusivamente a chave `png`. Nenhuma ocorrência de `path` permanece. Cada caminho aponta para um arquivo PNG existente no disco cujo SHA-256 bate 100% com o hash declarado.
- **`back_l/Axe`:** Todas as 48 camadas contêm exclusivamente a chave `png`. Nenhuma ocorrência de `path` permanece. Cada caminho aponta para um arquivo PNG existente cujo SHA-256 bate 100% com o hash declarado.
- **Resultado:** **PASS**.

### 2.2 Preservação Rigorosa de Metadados e Hashes de Quadro
- Para cada quadro `i` (0 a 11):
  - `frames[i].sha256` (composto 256): **Idêntico** ao arquivo pré-normalização.
  - `frames[i].nativeSha256` (corpo nativo 128): **Idêntico** ao arquivo pré-normalização.
  - `durationMs`: **Idêntico** ao arquivo pré-normalização.
  - `weaponVisible`: **Idêntico** ao arquivo pré-normalização.
  - `phase`, `rightGrip`, `rotationDeg`: **Idênticos**.
- Zero alteração em dados de imagem, temporização ou visibilidade.
- **Resultado:** **PASS**.

### 2.3 Correspondência dos Mestres e Tiras
- Todos os 8 mestres Aseprite (`composite`, `body`, `native`, `hand`) e todas as 6 tiras PNG (`strip`, `nativeStrip`, `compositeStrip`, `nativeCompositeStrip`) continuam existindo nos caminhos indicados e com hashes SHA-256 byte-idênticos aos declarados em ambos os `clip.json`.
- **Resultado:** **PASS**.

### 2.4 Ausência de Divergências
- Nenhuma divergência detectada.

---

## 3. Tabela Comparativa de Hashes Confirmados no Disco

| Clipes Afetados | Hash Original Aprovado (`pre-normalization/`) | Hash Atual Confirmado no Disco (`clip.json`) | Status da Chave de Camada |
|---|---|---|:---:|
| **`back_r/Sword`** | `eb379d1d699ab51203ec633d645a29d9c63e377e36fe8b15b8fda44fc1a9aac6` | **`a63aa1ac4648eba9605fb26720a7b51d9a863539d6d76cc8e79fc3115ff8b739`** | **`png` (48/48)** |
| **`back_l/Axe`** | `9f7d01e726f3f6dc63b24aeb23da97ac9cad29a7fd31572ccdf59a3ee384a0f3` | **`b61b87deed2c547d8d01112b0f30e956f02fee12eff04dab6ba25b833eb7cbf6`** | **`png` (48/48)** |

---

## 4. Conclusão e Handoff para o Portão de Integração

A normalização técnica foi executada de forma limpa, não introduzindo qualquer alteração de arte ou metadados de animação. Os novos hashes de `clip.json` estão atestados e registrados para o portão de integração do Root.

### Artefatos de QA Persistidos:
- [layer-key-normalization-qa.json](file:///C:/Users/João%20Orlando/Documents/Projetos%20Unity/TacticsRPG-CharacterFactory/experiments/main-orc-combat-rescue-v5/qa-antigravity-flash/layer-key-normalization-qa.json)
- [layer-key-normalization-qa.md](file:///C:/Users/João%20Orlando/Documents/Projetos%20Unity/TacticsRPG-CharacterFactory/experiments/main-orc-combat-rescue-v5/qa-antigravity-flash/layer-key-normalization-qa.md)
