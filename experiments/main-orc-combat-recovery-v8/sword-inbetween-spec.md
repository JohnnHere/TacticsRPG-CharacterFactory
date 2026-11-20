# Especificação comum — inserir o quadro de descida `apex-descent` no ataque de espada

Esta especificação vale para as QUATRO direções do Sword do Orc V1, no candidato V8.
Ela existe para que as quatro continuem idênticas entre si depois do retoque. Se cada
agente inventar a sua própria grade, a rodada inteira se perde.

## O defeito que estamos corrigindo

A lâmina salta 75,99 px entre `apex-hold` (F05) e `slash-release` (F06), sem nenhum
quadro intermediário. Entre a coluna máxima da arma em F05 (x=110) e a coluna mínima em
F06 (x=146) existem 36 px de vão vazio. O jogador vê a espada teleportar. Isso não é
brilho — a lâmina tem 55 a 62 px claros em todos os quadros armados, sem pico.

## A grade nova, obrigatória e igual nas quatro direções

Treze para quatorze quadros. O total continua 730 ms e o contato continua em 325 ms.

| Índice novo | Fase | Duração | Antes |
|---|---|---|---|
| F00 | rest | 30 | igual |
| F01 | body-preparation | 65 | igual |
| F02 | establish-grip | 35 | igual |
| F03 | anticipation | 50 | igual |
| F04 | coil-behind | 45 | igual |
| F05 | apex-hold | 35 | era 65 ms |
| **F06** | **apex-descent** | **30** | **novo** |
| F07 | slash-release | 35 | era F06 |
| F08 | contact | 35 | era F07 |
| F09 | follow-through | 100 | igual |
| F10 | recoil | 55 | era F09 |
| F11 | settle-grip | 80 | era F10 |
| F12 | release-grip | 45 | era F11 |
| F13 | return-to-guard | 90 | era F12 |

Soma: 30+65+35+50+45+35+30+35+35+100+55+80+45+90 = **730 ms**. Confira antes de entregar.

O quadro novo é pago dividindo o `apex-hold`, que era um único quadro de 65 ms e passa a ser
35 ms + 30 ms. Nenhuma outra duração muda. A versão anterior desta especificação dizia
`follow-through` de 70 ms por erro de aritmética meu: isso daria 700 ms e está errado.

O tempo do `apex-hold` diminui para pagar o quadro novo sem esticar o clipe. Não mexa em
nenhuma outra duração.

## O que o quadro novo tem de ser

Uma pose REAL de descida entre o ápice e o `slash-release`, com o braço e a luva
acompanhando a arma. Ela não pode ser um clone de F05 nem de F07, e não pode ser
interpolação de pixel: tem de ser autorada no Aseprite.

Posição alvo: o centroide da lâmina deve ficar aproximadamente **a meio caminho** entre
o centroide de F05 e o do antigo `slash-release`. Com isso o salto de 76 px se divide em
dois passos de cerca de 38 px, que é a faixa dos outros passos do clipe.

## Contrato técnico que será medido

1. Quatorze quadros, durações exatamente as da tabela acima, soma 730 ms.
2. Fases com os nomes e a ordem da tabela, inclusive `apex-descent` no índice 6.
3. `contactEvent` em `frame: 8`, `timeMs: 325`, `phase: "contact"`.
4. Arma oculta em F00, F01, F12 e F13; visível de F02 a F11.
5. Nenhum par de quadros consecutivos com arma visível byte-idêntico.
6. Maior passo do centroide da lâmina **menor que 55 px**, e na transição F05→F06 como
   nas outras direções.
7. Nenhum pixel claro de armadura apagado: a série de pixels com luminância maior ou
   igual a 160 na camada `body` não pode cair em relação à versão atual.
8. A lâmina não atravessa o chão, não desconecta da luva, e o contorno escuro do membro
   permanece fechado.

## Entrega

Célula completa, no mesmo contrato das outras: `clip.json`, frames, camadas `body`,
`handFront`, `weaponBack`, `weaponFront`, `native`, `source`, mestres e strips.
Reexporte a partir do Aseprite salvo. Registre a procedência da autoria.
Não edite nenhuma célula que não seja a sua. Não mexa em Axe. Não faça commit, não
toque no Unity.
