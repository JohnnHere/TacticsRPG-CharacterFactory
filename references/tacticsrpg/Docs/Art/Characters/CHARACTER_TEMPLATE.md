# CHARACTER_TEMPLATE — Especificação de novo personagem

> Preencher este template ao criar um novo personagem. Processo completo e padrões técnicos:
> `../CHARACTER_PIPELINE.md` (v1.0). Linguagem visual: `../../ART_DIRECTION.md`. Exemplo
> preenchido (referência de implementação): `HUMAN_WARRIOR_PILOT.md`.
> **Não implementar nada antes do gate 1 (referência visual aprovada).**

## 1. Identidade

- **CharacterId** (pasta/prefixo de assets, minúsculo): `______`
- **Nome de trabalho:** ______
- **Raça / ancestralidade visual:** ______
- **Classe / arquétipo:** ______
- **Papel:** jogável (time 0) · inimigo · NPC — ______
- **Status:** protótipo técnico · produção final — ______
- **Observação de canônica:** (o piloto NÃO é template visual obrigatório; protagonista é
  decisão separada — Estágio 8)

## 2. Silhueta e proporções

- Silhueta distinguishing em zoom-out (1 frase): ______
- Proporções: compactas táticas padrão (128×128, ~100 px de altura útil) ·
  variação: ______
- A identidade do personagem e do Job sem arma: roupa, corpo, armadura e postura: ______
- Assets de arma separados e ações que os invocam quando equipados: ______

## 3. Paleta e traços

- Paleta principal (3–5 cores): ______
- Cabelo/couro/metal/capa: ______
- Traços distinguíveis: ______
- Referência visual aprovada (gate 1): `Docs/Art/References/…` — ______

## 4. Vistas direcionais (4 — rótulos de TELA)

| Vista | Arquivo | Status (a fazer / feito / aprovado) |
|---|---|---|
| `front_r` | `<id>/Directions/<prefixo>_dir_front_r.png` | ______ |
| `front_l` | `…front_l.png` | ______ |
| `back_r`  | `…back_r.png` | ______ |
| `back_l`  | `…back_l.png` | ______ |

Regras: rosto nas `front_*`, costas/capa nas `back_*`, `_l/_r` = lado da TELA, **nunca
espelhar**. O corpo não contém arma; ativos de arma separados seguem a mão/encaixe quando uma
ação os invoca. Mapeamento: `HUMAN_WARRIOR_DIRECTIONS.md` §2.

## 5. Inventário de animações (padrão do piloto — ver `../CHARACTER_PIPELINE.md` §6)

| Clipe | Quadros/vista | Timing/quadro | Pasta | Status |
|---|---|---|---|---|
| Idle | 4 | 0,24 s (ciclo 0,96 s) | `Animations/Idle/` | ______ |
| Walk | 6 (3/passo, ciclo = 2 passos) | derivado do passo 0,22 s | `Animations/Walk/` | ______ |
| Attack | 5 | 0,09 s (~0,45 s) | `Animations/Attack/` | ______ |
| Hit | 3 | 0,08 s (~0,24 s) | `Animations/Hit/` | ______ |
| Defeat | 5 | 0,12 s (~0,60 s) | `Animations/Defeat/` | ______ |

Naming: `<state>_<vista>_<NN>.png` (`NN` = 00.., sem pular) · linha do chão y=126 ·
bob de idle ≤2 px · sem espelhamento. Contagens diferentes exigem acordo prévio
(o carregador aceita 1–15 por vista; consistência entre vistas é gate 2).

## 6. Local dos assets

- `Assets/Resources/Characters/<CharacterId>/…` (§8 do pipeline) — ______
- Metas com configuração aprovada (Sprite/Single/PPU 100/Point/sem compressão/sem mipmap)? —
  ______

## 7. Tratamento de equipamento

- Arma como asset independente (ID/referência): ______
- Ações em que a arma equipada é invocada e aparece: ______
- Estado de suporte no runtime (atual: overlay dinâmico não implementado): ______
- Encaixe na mão, oclusão e sincronização de animação: ______

## 8. Integração técnica (Presentation)

- Registrado em `UnitVisuals` (gate + caminhos)? — ______
- Unidade de destino no mapa (`BattleSandbox.CreateViews`)? — ______
- Fallback verificado (clipe → estático → cápsula)? — ______
- Escala visual aplicada (padrão ×1,15)? — ______

## 9. Testes

- Técnica (compilação, Test Runner, metas 92/92+ Sprite/Single, medição y=126): ______
- PlayMode (`../CHARACTER_PIPELINE.md` §14.2 — 16 itens): ______
- Data da última validação e por quem: ______

## 10. Aprovação

- Gate 1 (referência): ______ · Gate 2 (consistência): ______ · Gate 3 (final em jogo): ______

## 11. Limitações e pendências conhecidas

- ______

## 12. Histórico

- 2026-__-__ — criação da especificação · ______
