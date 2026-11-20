# T1 — Forense numérica do "flash branco" nos Sword traseiros (V6)

> **Limitação declarada.** Este worker não recebeu imagens e não tem percepção visual. Nada abaixo
> foi "visto": todas as afirmações são medições de pixel (Pillow) e reexportação de mestre (Aseprite
> 1.3.18.6). Nenhum ajuste foi feito nesta tarefa — o objetivo era localizar a fonte.

- Entrada (congelada, somente leitura): `characters/orc-v1/source/artistic-reconstruction-v6/rear/back_l-sword/` e `.../back_r-sword/`
- Manifesto V6: `candidate28manifest.json`, SHA-256 `5d68b52d3e2b2a0931d689afb5a9dd438c178835d05efb02a5fb2bcf0c64b7ca` (**rejeitado artisticamente** pelo criador; nada foi promovido)
- Script: `experiments/main-orc-combat-recovery-v7/forensics/white_flash_forensics.py`
- Dados brutos: `experiments/main-orc-combat-recovery-v7/forensics/white-flash.json`
- Verificação de mestre: `experiments/main-orc-combat-recovery-v7/scripts/dump_master.lua` + `forensics/verify_master.py` → `forensics/master-vs-export.json`

## 1. Definição operacional de "branco" neste personagem

A paleta dos dois clipes satura em **L = 177,72** (`rgb(176,178,180)`, a lâmina/highlight de aço).
Não existe pixel ≥ 200. Portanto "flash branco" aqui = família cinza-neutra clara, `L ≥ 150`,
`S ≤ 0,30`:

| Cor | L | Onde aparece |
|---|---|---|
| `rgb(176,178,180)` | 177,7 | highlight de lâmina (camadas de arma) e alguns realces de metal |
| `rgb(171,173,173)` | 172,6 | realce de metal do corpo (bookends do Idle) |
| `rgb(156,158,158)` | 157,6 | realce de metal do corpo (bookend do Idle `back_r`) |
| `rgb(153,154,155)` | 153,9 | realce de metal do corpo (bookends do Idle) |

## 2. Prova de superfície — onde o defeito NÃO está

| Verificação | Resultado |
|---|---|
| Exportação nova do mestre salvo (`composite.aseprite`) vs `layers/*.png` commitados | **0 pixels diferentes** (12 quadros × 4 camadas, ambos os clipes) |
| Flat do mestre vs `frames/*.png` (composto commitado) | **0 pixels diferentes** |
| Recomposição alfa-over `weaponBack→body→weaponFront→handFront` vs `frames/*.png` | erro máximo de canal **0,0**; 0 pixels divergentes |
| `cel.position` no mestre | todos os cels em `(0,0)` 256×256 — nenhum deslocamento escondido |

**Conclusão:** o fenômeno é **conteúdo autorado no mestre**. Não é artefato de exportação, nem de
composição, nem de `cel.position`. Corrigir só no composto não adiantaria; a fonte é o `.aseprite`.

## 3. Medição por quadro (camada `body`, metade esquerda/direita do canvas)

`bodyLightL/R` = pixels claros (`L≥150, S≤0,30`) na metade esquerda/direita.
`weaponL/R` = o mesmo somado às camadas `weaponBack`+`weaponFront`.
`iso` = pixels claros temporariamente isolados (sem claro a ≤2 px em **ambos** os vizinhos).

### `back_l/Sword` (12 quadros, 950 ms)

| F | ms | bodyLightL | bodyLightR | weaponLightR | iso | meanL body |
|---|---|---|---|---|---|---|
| 00 | 90 | **61** | 11 | 0 | **9** | 36,51 |
| 01 | 80 | **13** | 1 | 89 | 0 | 35,38 |
| 02 | 80 | 15 | 0 | 88 | 0 | 36,52 |
| 03 | 110 | 15 | 0 | 89 | 0 | 36,89 |
| 04 | 50 | 15 | 0 | 87 | 0 | 36,90 |
| 05 | 40 | 17 | 0 | 84 | 5 | 36,40 |
| 06 | 40 | 14 | 0 | 89 | 0 | 36,99 |
| 07 | 80 | 21 | 0 | 88 | 0 | 37,26 |
| 08 | 100 | 19 | 0 | 87 | 0 | 37,42 |
| 09 | 90 | 24 | 0 | 89 | 0 | 36,83 |
| 10 | 90 | **21** | 0 | **0** | 0 | 35,90 |
| 11 | 100 | **61** | 11 | 0 | 0 | 36,51 |

Fronteiras: `F00→F01 = −48`, `F10→F11 = +40`; todas as outras ficam entre −3 e +7.

### `back_r/Sword` (12 quadros, 950 ms)

| F | ms | bodyLightL | bodyLightR | weaponLightR | iso |
|---|---|---|---|---|---|
| 00 | 90 | 21 | **46** | 0 | **21** |
| 01 | 80 | 5 | **2** | 89 | 0 |
| 02…09 | — | 1…6 | 0…6 | 82…89 | 0 |
| 10 | 90 | 3 | 2 | **0** | 0 |
| 11 | 100 | 21 | **46** | 0 | 21 |

Fronteiras: `F00→F01 = −16` (esquerda) / **−44** (direita), `F10→F11 = +18` / **+44**.

## 4. Candidatos, com métrica

### C1 — **ALTA — `back_l/Sword` F00 e F11: colapso/retorno do realce claro do flanco esquerdo** ← mais provável

- **Quadros:** 0 (90 ms) e 11 (100 ms). Ausente nos vizinhos F01 e F10 (ambos os lados da fronteira).
- **Camada:** `body`.
- **Métrica (metade esquerda do canvas):** 61 px claros em F00 → 13 px em F01 (**−48 px, fator 4,7×**) e 21 px em F10 → 61 px em F11 (**+40 px**).
- **Massa contígua** (F00/F11), 3 componentes 8-conectadas, na metade esquerda:
  | px | bbox canvas (256) | bbox nativo (128, −64) | cor dominante |
  |---|---|---|---|
  | 12 | (103,117)–(108,121) | (39,53)–(44,57) | `rgb(153,154,155)` |
  | 12 | (98,122)–(102,131) | (34,58)–(38,67) | `rgb(153,154,155)` |
  | 5 | (97,133)–(99,137) | (33,69)–(35,73) | `rgb(153,154,155)` |
  | 9 (isolado no tempo) | (103,117)–(108,119) | — | `rgb(153,154,155)` |
- **Cores na metade esquerda do `body`:** `rgb(153,154,155)` ×36 + `rgb(171,173,173)` ×25 = 61 px.
- **O que sobra nos quadros de ataque:** no mesmo lugar há apenas uma faixa de 1–2 px de largura,
  5–8 px por quadro (`F01` (5 px em x=103, y125–129), `F02` 4, `F03` 6, `F04` 6, `F05` 6, `F06` 6,
  `F07` 7, `F08` 7, `F09` 8, `F10` 7). Ou seja: **o realce não desaparece, ele encolhe ~75–85 %**
  na fronteira bookend→ataque e volta ao tamanho cheio no quadro final.
- **Causa raiz provada:** `layers/body/00.png` e `layers/body/11.png` são **byte-idênticos** a
  `characters/orc-v1/source/complete-v1/back_l/Idle/00.png` (SHA-256 `0fb8c85a…aede19` nos três).
  Os bookends são o Idle V5 preservado; os quadros F01–F10 são corpos gerados no V6. O realce de
  metal do flanco esquerdo existe no Idle e está quase ausente nos corpos gerados → **descontinuidade
  de estilo/relevo entre bookend preservado e corpo gerado**, não um pixel intruso.
- **Por que casa com o relato:** é a maior variação clara da **metade esquerda** de todo o clipe,
  ocorre por 90 ms no início e 100 ms no fim de cada reprodução (surge e desaparece), e é a única
  estrutura clara compacta (≥8 px) temporalmente isolada em todo o clipe.

### C2 — MÉDIA — lâmina entra/sai do intervalo visível (metade **direita**), ambos os clipes

- F01 `weaponL/R = 0/89`, F09 `0/89`, F10 `0/0`. Cor dominante `rgb(176,178,180)` = **L 177,7, o
  valor mais claro da paleta inteira**; componente principal de 37 px em (166,73)–(178,98) em
  `back_l` e (170,76)–(182,101) em `back_r`.
- É o maior degrau de luminância do clipe, mas é **política attack-only** (`visibleInterval [1,9]`),
  não conteúdo errado, e está na metade **direita** do canvas.
- Relevante se o criador falou do "lado esquerdo **do personagem**": na vista traseira o lado
  esquerdo do personagem cai na metade direita do canvas. Se a intenção era essa, o candidato passa
  a ser C2 em `back_r/Sword` (vista espelhada).

### C3 — BAIXA — `back_r/Sword` F00/F11, fenômeno espelhado de C1

- Metade direita: 46 px claros em F00 → 2 px em F01 (**−44**) → 46 px em F11 (**+44**).
  Cor única `rgb(156,158,158)`; cluster temporalmente isolado de 11 px em (151,117)–(155,122),
  lado direito. Metade esquerda: 21 → 5 px.
- Mesma causa de C1 (bookend = Idle preservado), **espelhada**: em `back_r` a massa clara do Idle
  cai à direita do canvas; em `back_l` cai à esquerda. Isso é consistente com as duas vistas serem
  espelhos uma da outra.

### Sem candidatos internos ao ataque
Entre F01 e F10 não há nenhum cluster claro **temporalmente isolado** ≥8 px em nenhum dos clipes —
os grupos internos chegam a 8 px (`back_l` F09, `(97,126)–(98,133)`), mas estão presentes nos
quadros vizinhos, então não são realce intermitente. O "flash" **não** está no meio da coreografia;
está nas duas fronteiras bookend↔ataque.

## 5. Resposta direta

1. **Onde está:** no **mestre salvo** e em todas as suas derivações (camada e composto idênticos).
2. **Quadro/camada:** `back_l/Sword` **F00 (90 ms) e F11 (100 ms)**, camada `body`.
3. **Bounding box:** (97,117)–(108,137) em canvas 256 (realce do flanco esquerdo); núcleo isolado
   9 px em (103,117)–(108,119).
4. **Contagem:** 61 px claros na metade esquerda vs 13 px no vizinho F01 (Δ −48); 21 px em F10 vs
   61 px em F11 (Δ +40).
5. **Cor RGBA dominante:** `rgb(153,154,155)` (secundária `rgb(171,173,173)`), opacas.
6. **Presente nos vizinhos?** Não: ausente em F01 **e** em F10.
7. **Mais provável como "flash branco no lado esquerdo":** **C1 (`back_l/Sword`, F00/F11, metade
   esquerda do canvas)** — 48 px de claros entram/saem de uma vez, num bloco compacto, duas vezes
   por reprodução de 950 ms.

## 6. Direção de reparo (para o produtor da vista traseira — NÃO executada aqui)

Duas opções mutuamente exclusivas; a escolha é artística, não minha:

- **A (preservar o Idle):** levar a mesma intensidade de realce (`rgb(153,154,155)`/`(171,173,173)`,
  largura 3–6 px no canvas, ao longo de x 97–108 / y 117–137) para os corpos F01–F10, de modo que a
  passagem bookend→ataque não mude a potência do realce. Custo alto: os corpos F01–F10 vêm de geração
  e o realce precisa ser reconstruído quadro a quadro.
- **B (uniformizar para baixo):** atenuar o realce somente nos bookends F00/F11 até o nível dos
  quadros de ataque. Barato, mas **altera o Idle V5 herdado** (hoje byte-idêntico) e a identidade do
  livro-caixa — precisa de autorização explícita do criador, pois viola "preservar o que já funciona".

Recomendação numérica: qualquer que seja a opção, o alvo mensurável é reduzir
`|bodyLightLeft(F00) − bodyLightLeft(F01)|` de 48 px para ≤ 8 px, com o realce mantido contíguo
(nenhum pixel claro isolado sem vizinho claro) para não criar flicker.
