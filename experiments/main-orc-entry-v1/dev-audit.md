# Auditoria DEV — entrada de combate (`main-orc-onehanded-entry-v1`)

Escopo desta nota: build e checagem técnica do candidato isolado. Aprovação artística continua sendo
decisão explícita do criador (`PENDING_CREATOR`). Documentação canônica: `docs/MAIN_ORC_COMBAT_POLISH.md`.

## Diagnóstico da base `onehanded-polish-v1`

- **Sword** (11 quadros / 690 ms): o primeiro quadro armado (`establish-grip`, 45 ms) reutilizava o corpo
  neutro do repouso — nenhuma mudança de braço, ombro ou cotovelo. O quadro seguinte (`load`) já saltava
  18,4 px / 15° e a passagem para `high-guard` concentrava **41,3 px / 75° em um único quadro**.
- **Axe** (12 quadros / 1055 ms): mesmo reaproveitamento do neutro na abertura, com `load` projetado
  (braço estendido) antes de `raise`.
- Consequência: a arma aparecia antes de existir preparo corporal correspondente.

## Correção aplicada (somente a entrada)

- Dois quadros ocultos com o corpo preparado (`inputs/prepare-body.png`, mão somente no próprio corpo),
  seguidos da primeira pegada no mesmo corpo com ângulo próprio (Sword 315°, Axe 300°).
- **Sword**: pontes `entry-elbow-lift` / `entry-shoulder-coil` (poses Axe3/Axe4, 330°/340°) antes da
  guarda alta preservada a 345°.
- **Axe**: entrada própria (`raise` 325° → `cocked-shoulder` 350°), sem o `load` projetado.
- Golpe, seguimento, recuperação e caudas: quadros herdados por hash da base. Nenhuma pose de golpe foi
  redesenhada e as armas não foram alteradas.

## Classificação dos keyposes

| Candidato | Fase | Origem | Classe |
|---|---|---|---|
| Sword 0 | rest | Sword0 | KEEP |
| Sword 1 | body-preparation (oculto) | corpo preparado | TRANSITION_FIX |
| Sword 2 | establish-grip 315° | corpo preparado | TRANSITION_FIX |
| Sword 3 | entry-elbow-lift 330° | base Axe3 | TRANSITION_FIX (ponte) |
| Sword 4 | entry-shoulder-coil 340° | base Axe4 | TRANSITION_FIX (ponte) |
| Sword 5 | high-guard 345° | base Sword3 | KEEP pose / TIMING_ONLY (100 → 65 ms) |
| Sword 6–8 | drive / crossing / impacto | base Sword4/5/6 | KEEP |
| Sword 9–10 | recovery-bridge / recovery | base Sword7/8 | KEEP |
| Sword 11–12 | action-complete / return-unarmed | base Sword9/10 | KEEP |
| Axe 0 | rest | Axe0 | KEEP |
| Axe 1 | body-preparation (oculto) | corpo preparado | TRANSITION_FIX |
| Axe 2 | establish-grip 300° | corpo preparado | TRANSITION_FIX |
| Axe 3–4 | raise 325° / cocked-shoulder 350° | base Axe2/Axe3 | KEEP pose |
| Axe 5–8 | release / impacto / seguimento / recuperação | base Axe4–Axe7 | KEEP |
| Axe 9–11 | action-complete / settle / return-unarmed | base Axe8–Axe10 | KEEP |

Removidos da base: `establish-grip` projetado (50 ms) e `load` (100 ms) do machado; `load` (65 ms) e o
`establish-grip` de 45 ms da espada — substituídos por preparação corporal + pegada própria.

## Números descritivos (diagnóstico, não aprovação)

- Maior passo de pegada **na entrada**: Sword 20,6 px / 10°; Axe 20,6 px / 25°. Base: 41,3 px / 75° em
  um quadro.
- Pegada inicial world **[101,131]** (native [37,67]), 27 px de luva dentro do raio 6, alfa 255 no ponto.
- Passo máximo do golpe preservado (Sword 63,3 px / 35°) permanece o da base: é intenção existente.
- Armas inalteradas (`recruit-sword`, `militia-axe`), escala 1, pivô compartilhado.

## Preservado e limites

- Idle/Walk copiados por hash (`alias: true`), corpo neutro idêntico, cauda retorna ao hash neutro exato.
- `characters/orc-v1/source/equipment-current.json` continua `main-orc-onehanded-v3`; nenhum ponteiro de
  candidato foi escrito.
- Somente `front_r`; rotação da arma em vizinho mais próximo; sem sacar/embainhar; nada em Unity.
- Verificação executada: `node tools/entry-main-orc.mjs verify` → 174 PASS, 0 FAIL, 4 INFO,
  2 NOT_RUN, 2 REQUIRES_HUMAN_REVIEW (relatório em `entry-check.json`). `check-entry.py` apenas valida o
  plano e delega a esse verificador; não duplica regras.
