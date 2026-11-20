# Perícia do "flash" frontal — F05→F06 é um teleporte de 76 px

Medição própria do orquestrador sobre o clipe que está publicado no V7
(`characters/orc-v1/source/combat-recovery-v7/frontal/full-front-r-sword`).
Objetivo: parar de discutir impressão e apontar o quadro e a camada.

## 1. A luminância da lâmina já é uniforme

Pixels claros (L >= 160) por camada, por quadro:

| Quadro | weaponBack | body | weaponFront | handFront |
|---|---|---|---|---|
| F00 | 0 | 38 | 0 | 0 |
| F01 | 0 | 35 | 0 | 0 |
| F02 | 0 | 35 | 60 | 0 |
| F03 | 0 | 8 | 56 | 0 |
| F04 | 0 | 8 | 58 | 0 |
| F05 | 0 | 3 | 57 | 0 |
| F06 | 0 | 5 | 57 | 0 |
| F07 | 0 | 1 | 58 | 0 |
| F08 | 0 | 2 | 55 | 0 |
| F09 | 0 | 2 | 62 | 0 |
| F10 | 0 | 6 | 58 | 0 |
| F11 | 0 | 6 | 0 | 0 |
| F12 | 0 | 38 | 0 | 0 |

A lâmina fica entre 55 e 62 pixels claros em todos os quadros armados. Não existe
pico especular na arma. O corpo varia 38 → 35 → 8 porque o braço sai de cima do
ombro, o que é anatômico e não um artefato.

**Consequência:** qualquer correção que mexa no *ramp* da lâmina está corrigindo um
defeito que não existe. Foi exatamente o que a tentativa V8 fez e o resultado foi
apagar highlight de armadura em cinco quadros.

## 2. O defeito real é deslocamento, não brilho

Centroide da camada `weaponFront` e distância percorrida entre quadros:

| Transição | Centroide anterior | Centroide novo | Deslocamento |
|---|---|---|---|
| F02→F03 | (86,4; 111,0) | (80,9; 95,5) | 16,5 px |
| F03→F04 | (80,9; 95,5) | (93,1; 75,2) | 23,7 px |
| F04→F05 | (93,1; 75,2) | (97,5; 63,8) | 12,2 px |
| **F05→F06** | **(97,5; 63,8)** | **(167,9; 92,4)** | **76,0 px** |
| F06→F07 | (167,9; 92,4) | (182,8; 127,1) | 37,8 px |
| F07→F08 | (182,8; 127,1) | (179,1; 163,1) | 36,2 px |
| F08→F09 | (179,1; 163,1) | (156,5; 158,4) | 23,0 px |
| F09→F10 | (156,5; 158,4) | (135,0; 153,9) | 22,0 px |

Todos os passos ficam entre 12 e 38 px, exceto **F05→F06, que é 76 px, o dobro do
maior passo vizinho**. A caixa da arma salta de `(85,30,110,101)` para
`(146,64,186,125)`, ou seja, a arma sai da coluna x≈85–110 e reaparece em
x≈146–186 sem nenhum quadro intermediário.

A área é praticamente constante (625–631 px) em todos os quadros, então não é a
arma crescendo ou trocando de forma: é o mesmo objeto em outro lugar.

## 3. Aparecimento e desaparecimento

A lâmina está ausente em F00, F01, F11 e F12; presente de F02 a F10. O
aparecimento em F02 e o desaparecimento depois de F10 são cortes secos, sem
quadro de transição. Isso é o que o criador descreve como "flash": a arma entra e
sai de cena em um único quadro.

## 4. Onde a correção deve acontecer

1. **F05→F06** (76 px): inserir ou mover um quadro intermediário para a arma
   percorrer o arco. É o defeito dominante e o único que explica a leitura de
   "salto sem arco".
2. **F01→F02 e F10→F11**: suavizar a entrada e a saída da arma com um estado
   intermediário da própria arma, sem tocar no corpo.

Fora de escopo, e proibido por medição: reduzir luminância da lâmina, escurecer
`body`, ou qualquer operação guiada por limiar em faixa de quadros.

## 5. Estado da tentativa V8 do frontal

Rejeitada. O `clip.json` entregue apontava os frames para a árvore do V6, então a
edição ficaria invisível; com os caminhos corrigidos, a curva de claros ficou
`[38,34,33,64,66,3,5,1,57,64,6,6,38]` contra `[38,35,94,64,66,60,62,59,57,64,64,6,38]`
do V7. F05 caiu de 60 para 3, F06 de 62 para 5, F07 de 59 para 1 e F10 de 64 para
6 — apagou highlight de armadura, além de não resolver o teleporte.
