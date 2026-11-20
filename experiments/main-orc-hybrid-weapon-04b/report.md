# Piloto B1 — Arquitetura C em `front_r`

Status: `TECHNICALLY_COMPLETE` / `VISUAL_REVIEW_REQUIRED` / `PENDING_CREATOR`
Data: 2026-10-31 · Escopo: Orc principal, ataque de Espada, direção `front_r`, somente piloto local.

## 1. Pergunta desta rodada

O Experimento 04 provou que duas espadas podem compartilhar **um corpo** em `front_l`.
O Piloto B1 verifica se a mesma arquitetura se aplica a uma **segunda direção** sem reconstruir
anatomia — mantendo o custo baixo e a produção reproduzível.

Resposta: **sim, com uma adaptação declarada** — o pivô de pegada, que o `front_r` não fornece.

## 2. Fontes confirmadas

| Item | Caminho | Situação |
|---|---|---|
| Corpo/mão da direção | `characters/orc-v1/source/combat-recovery-v8/frontal-inbetween/front_r-sword/` | 14 quadros, 730 ms, mesmo `contactEvent` F08/325 ms do `front_l` |
| Arma original | `combat-rescue-v5/combat/weapons/Sword/recruit-sword.aseprite` | idêntica ao Experimento 04 |
| Espada A (Recruta) | `variants/sword-a/sword.png` | **byte-idêntica** ao Exp04 |
| Espada B (aço claro) | `variants/sword-b/sword.png` | **byte-idêntica** ao Exp04 |
| Mecanismo de composição | `author.lua` + `run.mjs` herdados do Exp04 | mesmas camadas e regra de lâmina |

Nada sob `characters/`, `assets/` ou `reports/` foi alterado ou criado
(`protectedChanged: []`, `protectedAdded: []`).

## 3. A única adaptação de direção: o pivô

`front_r-sword/clip.json` declara `rotationDeg` quadro a quadro mas **`grip` é `null`** em todos os
10 quadros armados — diferente do `front_l`, que declara os dois. Sem pivô, a substituição da
lâmina não tem centro de rotação.

O pivô foi **medido na própria arte**, não estimado (`fit-front-r-grip.py`, saída em
`grip-pivot-fit.json`):

1. Estimativa por centroide de transformação rígida:
   `grip = centroide(arma) − R(rot)·(centroide(asset) − (48,66))`
2. Busca inteira exata em ±4 px e ±1° confirma o ótimo.

**Validação:** no quadro 6, o único que declara pivô (`[127,101]`), o ajuste devolveu
`[126.98, 101.00]` — erro de 0,02 px.

O resíduo de 643 px em 7057 px de arma (9 %) **não é erro de pivô**: a arte original não é uma
rotação rígida pixel-exata de `recruit-sword.png` (o Aseprite reamostrou a rotação). Ampliar a
busca para ±4° não reduz o resíduo.

## 4. Ajuste que o `front_l` não precisou

No Exp04 a regra era "repinta a lâmina e pronto". Em `front_r` a lâmina de B é **1 px mais estreita**
que a da Espada do Recruta (372 contra 472 px na banda da lâmina, por quadro). Repintar só onde B
tem pixel deixaria **~100 px da lâmina antiga vivos** por quadro, como uma borda do metal antigo.

Correção aplicada: o `u` de cada pixel é **preso à extensão opaca daquela linha de B**, de modo que o
sombreado de B segue a **silhueta original** em vez de deixar sobra. Resultado medido: **0 px de
lâmina antiga sobrevivente** e **0 px de mudança de silhueta** — melhor que o Exp04, que reportou
106 px de silhueta alterada.

## 5. Reutilização comprovada

| Verificação | Resultado |
|---|---|
| `body` e `handFront` byte-idênticos à fonte, nas duas variantes | **28/28** |
| `body`/`handFront` iguais entre A e B | 28/28 |
| Variante A idêntica às camadas originais da arma | **0 px** de diferença |
| Silhueta da arma alterada por B | **0 px** |
| Pixels da guarda/cabo repintados | **0 px** |
| Lâmina antiga sobrevivente | **0 px** |
| Tempos preservados (14 quadros, 730 ms) | **sim**, nas duas variantes |
| Assets de espada idênticos ao Exp04 | **sim** (`.png` e `.aseprite`) |

`verification.json`: `status: PASS`.

## 6. Herdado versus introduzido

**Herdado (não corrigido de propósito):**

- **Axila:** o `front_l` recebeu um reparo de axila (`frontal-armpit`, campos `armpitRepair` e
  `v7AxillaRepair` no clip). O `front_r` **nunca recebeu** — seu `clip.json` não tem esses campos.
  O defeito está presente e intocado.
- **Oclusão densa da mão** contra o tronco no quadro de contato.
- **Coreografia original**, incluindo a cadência.

**Introduzido por esta composição:** nada que separe de zero nos critérios acima. A lâmina de B tem
um contorno escuro mais espesso no dorso, mas isso é o desenho da própria espada B — visível
igualmente em `front_l` —, não um artefato da direção.

**Separação formal:** como `body` e `handFront` são byte-idênticos à fonte nas duas variantes,
qualquer defeito de anatomia, axila ou pegada é **necessariamente herdado**.

## 7. Limitações observadas

- A arte do `front_r` não é rotação exata do asset (9 % de ruído de contorno); qualquer medição por
  coordenada inversa nesta direção tem incerteza de ±1 px e não pode ser usada como prova de pixel.
- O piloto prova **arquitetura e reutilização**, não qualidade artística do golpe nem da espada B.
- `front_r` não pode ser promovida sozinha: a axila segue sem reparo.

## 8. Recomendação

1. Aceitar a Arquitetura C como aplicável às duas direções frontais para as **estas duas espadas**.
2. Tratar o reparo de axila do `front_r` como tarefa própria, com o mesmo rigor do `frontal-armpit`.
3. Só então avaliar as vistas traseiras (fora do escopo desta rodada).
4. A decisão artística sobre a espada B continua aberta ao criador.

## 9. Escopo respeitado

PixelLab pago: **zero**. Unity: **não tocado**. Promoção automática: **nenhuma**.
`characters/`, `assets/`, `reports/`: **inalterados**. Experimento 04: **preservado integralmente**.
Vistas traseiras e Axe Attack: **não tocados**.

## Artefatos

| Arquivo | Conteúdo |
|---|---|
| `review/index.html` | Página de revisão: original, A, B, corpo isolado, zoom da mão, playback |
| `verification.json` | Todas as comparações e critérios de aceitação |
| `grip-pivot-fit.json` | Como o pivô foi obtido e a qualidade medida |
| `grip-profile-front-r.json` | Contrato de pegada desta direção, reutilizável |
| `blade-repaint-stats.json` | Pixels de lâmina repintados por quadro |
| `representative-review-2x.png` | Original / A / B / corpo em F02, F08, F11 |
| `grip-10x-both.png` | Mão e punho em 10× |
| `full/{a,b}/` | 14 quadros por variante, com camadas e mestres Aseprite |
