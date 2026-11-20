# V8 — traseiras na grade do frontal, e a verdade sobre o flash

`main-orc-combat-recovery-v8` · candidato não promovido · aprovação artística é do criador

Este relatório existe para que o criador possa auditar o que foi feito, o que falhou
e por quê. Nada aqui foi promovido, integrado ao Unity ou commitado.

## 1. Ponto de partida

O V7 foi reprovado com estas palavras: o ataque de costas ficou menos uniforme que a
versão anterior, os problemas de frame pioraram, o flash no golpe da espada frontal
continua. A medição confirmou a queixa com números: Sword frontal rodava 13f/730 ms,
Sword back_r 12f/950 ms, Sword back_l 15f/860 ms; Axe 12f/1005, 12f/1320 e 15f/1230.
Os impactos caíam em instantes diferentes, ~260, ~490 e ~425 ms. Não era impressão,
eram três relógios distintos.

## 2. Estratégia adotada

Os dois QAs do V7 foram consultados sobre duas rotas e ambos recomendaram a mesma
coisa: usar a grade do frontal protegido como metrônomo e rebasear as traseiras nela,
em vez de inventar uma grade nova. Uma das QAs alertou contra a tentação de banir
quadros abaixo de 50 ms, porque o próprio frontal protegido usa 35 ms. A decisão foi
tomada com essa ressalva.

Trabalho dividido em duas frentes independentes: reconstrução/rebase das quatro
células traseiras e correção do flash frontal.

## 3. A frente frontal falhou, e a causa importa

A frente frontal recebeu um especialista econômico. A entrega foi **rejeitada** por
dois motivos, o segundo descoberto por medição.

Primeiro, o `clip.json` gravado apontava os frames para a árvore do V6, não para os
próprios arquivos editados. A edição ficaria invisível para qualquer consumidor do
clipe. É a terceira vez que essa classe de defeito aparece nesta tarefa, e foi
corrigida por `repair-clip-paths.mjs` (78 entradas reescritas em cada célula).

Segundo, com os caminhos corretos, a curva de pixels claros (limiar 160) ficou
`[38,34,33,64,66,3,5,1,57,64,6,6,38]` contra `[38,35,94,64,66,60,62,59,57,64,64,6,38]`
do V7. F05 caiu de 60 para 3, F06 de 62 para 5, F07 de 59 para 1 e F10 de 64 para 6.
O especialista não atenuou especular de lâmina: apagou highlight legítimo de armadura
em cinco quadros, que é exatamente o que a tarefa proíbe.

## 4. O diagnóstico do flash estava errado desde o V6

Medindo por camada, o frontal do V7 mostra que a lâmina tem 55 a 62 pixels claros em
**todos** os quadros armados. Não existe pico especular na arma. A variação aparente
vinha do corpo, 38 → 35 → 8, que é o braço saindo de cima do ombro.

O defeito real é deslocamento. O centroide da lâmina percorre 16,5 / 23,7 / 12,2 px
entre F02 e F05, dá um salto de **76,0 px entre F05 e F06**, e volta a 37,8 / 36,2 /
23,0 / 22,0 px. A área é constante, 625 a 631 px: é o mesmo objeto em outro lugar,
não a arma crescendo. A arma também entra em F02 e sai depois de F10 em corte seco.

Consequência prática: qualquer correção guiada por limiar de brilho perseguia um
defeito inexistente. Perícia completa em `frontal/forensics.md`.

## 5. A frente traseira entregou o que foi pedido

As quatro células traseiras foram reconstruídas ou retimadas na grade do frontal.
Auditoria independente do orquestrador, lendo os PNGs das próprias células:

| Célula | Quadros | Total | Armada | Impacto | Passo máx do centroide |
|---|---|---|---|---|---|
| front_r/Sword | 13 | 730 ms | F02–F10 | 290 ms (39,73%) | 76,0 px (#5→6) |
| front_l/Sword | 13 | 730 ms | F02–F10 | 290 ms (39,73%) | 76,0 px (#5→6) |
| back_r/Sword | 13 | 730 ms | F02–F10 | 290 ms (39,73%) | 68,5 px (#6→7) |
| back_l/Sword | 13 | 730 ms | F02–F10 | 290 ms (39,73%) | 56,8 px (#5→6) |
| front_r/Axe | 12 | 1005 ms | F02–F08 | 375 ms (37,31%) | 89,9 px (#4→5) |
| front_l/Axe | 12 | 1005 ms | F02–F08 | 375 ms (37,31%) | 89,9 px (#4→5) |
| back_r/Axe | 12 | 1005 ms | F02–F08 | 375 ms (37,31%) | 80,2 px (#4→5) |
| back_l/Axe | 12 | 1005 ms | F02–F08 | 375 ms (37,31%) | 73,7 px (#4→5) |

Não é só o total que coincide: a lista de durações por quadro é idêntica dentro de
cada família, o instante de impacto é idêntico, a janela armada é idêntica e o pico
de deslocamento cai na mesma fase. Séries de brilho da lâmina, nas quatro direções:

- Sword: `[0,0,60,56,58,57,57,58,55,62,58,0,0]` no frontal, e `[0,0,59,57,58,58,58,52,52,57,57,0,0]` / `[0,0,59,57,57,58,60,52,55,62,58,0,0]` nas costas.
- Axe: `[0,0,14,17,16,14,14,17,15,0,0,0]` no frontal, e 11–16 nas costas.

Os bookends das traseiras têm zero pixels claros: o pico de brilho na entrada e na
saída, que o criador viu como flash branco nas costas no V6, não existe mais.

## 6. Efeito colateral honesto do alinhamento

O salto de 76 px que o criador percebe no frontal agora também existe, em magnitude
comparável, nas vistas de costas, porque todas passaram a compartilhar a mesma fase.
Isso é coerente com o critério declarado pelo criador, de que a técnica tem de ser
reconhecível nas quatro direções, mas significa que o flash frontal deixou de ser um
desvio e passou a ser característica compartilhada. Corrigi-lo agora só em uma direção
quebraria a uniformidade recém-conquistada; a correção defensável é uma rodada
dedicada que insira o quadro intermediário nas quatro direções ao mesmo tempo, o que
muda a contagem de quadros de todos os clipes e por isso não foi feito aqui.

## 7. Estado técnico

- Integração: 13 candidatas ativas, 15 aliases, 228 quadros, pai = V7 `fde1fe23…`.
- Validação técnica: `TECHNICAL_PASS`, 28 células, 228 quadros, 968 hashes.
- Reexportação a partir das fontes salvas: `PASS_SAVED_SOURCE_EXPORTS`, 34 mestres, 356 quadros.
- Página comparativa: `Biblioteca de Arte/Estudos Comparativos/Orc principal - Recuperacao de combate V8/index.html`, 869 arquivos, verificação de navegador 20/20.
- `eligibleForIntegration: false`. Aprovação artística: pendente do criador.

## 8. Agentes desta rodada

| Função | Provedor | Resultado |
|---|---|---|
| Reconstrução das quatro traseiras | Codex gpt-5.6-sol | entregou; grade e fases validadas por medição independente |
| Correção do flash frontal | Codex gpt-5-6-luna | **rejeitado**; caminhos errados e highlights de armadura apagados |
| QA temporal independente | Antigravity gemini-3.8-flash | em execução |
| QA estático independente | opencode-free deepseek-v4.1-flash | em execução |

O QA estático foi deliberadamente colocado em um modelo **free**, corrigindo a falha
das rodadas anteriores, em que nenhum modelo gratuito foi usado nem em tarefas
simples e a decisão não ficou registrada.

## 9. Correções após o QA, e o que o QA ainda recusa O relatório acima é o estado do
primeiro candidato; o que segue é o que mudou por causa das reprovações.

### 9.1 O QA temporal derrubou o `back_r/Sword` que eu havia aprovado

Ele mediu o que meu audit não mediu. Dois pares de quadros com arma visível eram
byte-idênticos, `F04=F05` e `F09=F10`, ou seja, o orc congelava 65 ms no ápice e 80 ms
na recuperação, no meio do golpe. E o pico cinético estava em `F06→F07` (68,5 px)
enquanto as outras três direções aceleram em `F05→F06`. Eu tinha auditado só a grade de
tempo e o centroide agregado, e passei por cima disso.

A célula foi reconstruída em `combat-recovery-v8/rear-fix/back_r-sword`: 13 poses
distintas, nenhuma duplicata, pico em `F05→F06` com 73,23 px. O QA re-verificou e
confirmou quadro a quadro.

### 9.2 O QA temporal também derrubou um número meu

Eu calculei o instante de impacto pelo quadro do meio da janela armada, não pela fase
declarada. O impacto real é **325 ms (F07)** no Sword e **410 ms (F06)** no Axe, não os
290 ms e 375 ms que eu havia reportado. Pior: `front_r/Sword` declarava contato em
F06/290 ms, que é a fase `slash-release`, um quadro antes de a lâmina chegar. Os três
clipes frontais afetados foram corrigidos por `repair-contact-event.mjs`, com prova de
que **todo PNG de quadro permaneceu byte-idêntico** — mudou só o metadado de tempo.

### 9.3 O QA estático recusou a axila, e a axila foi refeita

O laudo do Terra foi `NEEDS_FIX`: a junção ombro–axila de `front_l/Sword` continuava
escura em F03–F05 e ele não conseguia afirmar que o buraco tinha sido fechado. A célula
nova em `combat-recovery-v8/frontal-armpit/front_l-sword` reilumina **73 pixels** da
camada `body` (F03 25, F04 15, F05 33) usando só tons que já existiam nos mestres.
Verifiquei por conta própria: nos compostos, 70 pixels mudaram e **nenhum canal RGB
diminuiu** em nenhum pixel. F00–F02 e F06–F12 estão 100% idênticos ao V7.

### 9.4 O que o QA continua recusando

O QA temporal emitiu `TEMPORAL_PASS_WITH_RESERVATIONS`, e sob o critério estrito dos
dois mandatos da rodada ele diz `TEMPORAL_FAIL`, porque um dos mandatos não foi
cumprido: **o flash frontal não foi resolvido**. Ele está certo. A lâmina continua
saltando 75,99 px entre F05 e F06, com 36 px de vão vazio entre a coluna máxima de um
quadro e a mínima do outro, e continua sem qualquer pico de luminância.

Não corrigi por decisão, não por esquecimento: inserir o quadro intermediário muda a
contagem de quadros, e as quatro direções acabaram de ser alinhadas ao mesmo relógio.
Corrigir só o frontal desfaria a uniformidade que era o outro mandato. A correção
defensável é uma rodada dedicada que altere as quatro direções juntas.

O QA também listou dois resíduos que eu conferi e classifiquei como **não sendo desvio**:
o corpo congelado na entrada existe em `front_r/Sword`, `front_r/Axe` e `back_r/Sword`
igualmente, porque a arma entra enquanto o corpo segura a pose de repouso; e o
aparecimento e o desaparecimento seco da arma é a política de arma somente no ataque,
não um artefato desta rodada.

## 10. Estado final verificado

| Portão | Resultado |
|---|---|
| `TECHNICAL_PASS` | 28 células, 228 quadros, 968 hashes |
| Reexportação das fontes salvas | `PASS_SAVED_SOURCE_EXPORTS`, 34 mestres, 356 quadros |
| Chromium da página principal | 20/20 |
| Chromium da página de inspeção ampliada | 6 imagens, 0 quebradas, 0 erros |
| Duplicatas com arma visível | 0 nas 8 células |
| Pico cinético Sword | `F05→F06` nas 4 direções (56,8 a 76,0 px) |
| Pico cinético Axe | `F04→F05` nas 4 direções (73,7 a 89,9 px) |
| `contactEvent` | `F07/325 ms` no Sword e `F06/410 ms` no Axe, nos 8 clipes |
| QA temporal | `TEMPORAL_PASS_WITH_RESERVATIONS` (reserva: flash frontal herdado) |
| QA estático | `NEEDS_FIX` na primeira passada; O5 e O6 fechados, O4 refeito, O1 parcial |

Aprovação artística continua sendo exclusiva do criador. `eligibleForIntegration=false`,
nada promovido, nada commitado, Unity intocado.

## 12. O retoque final que o criador pediu

Depois do relatório acima, o criador pediu que eu terminasse os retoques que faltavam. O
que faltava era exatamente o flash frontal, que eu havia deixado em aberto. Foi feito.

A correção exige um quadro de descida que não existia. Inserir quadro muda a contagem, e
mudar a contagem de uma direção quebraria o alinhamento, então o quadro foi autorado no
Aseprite **nas quatro direções ao mesmo tempo**, com a mesma grade:

`30, 65, 35, 50, 45, 35, 30, 35, 35, 100, 55, 80, 45, 90` — quatorze quadros, **730 ms**,
contato preservado em **325 ms** no índice 8. O quadro novo é pago dividindo o
`apex-hold`, que era 65 ms e passa a 35 + 30.

| Medida | Antes | Depois |
|---|---|---|
| Salto do centroide da lâmina | 75,99 px | **38,16 px** |
| Vão vazio entre as duas posições da arma | 36 px | **7 px** |
| Maior passo, nas quatro direções | 76,0 / 76,0 / 68,5 / 56,8 px, fases diferentes | **38,2 / 38,2 / 42,3 / 36,9 px, todas em F05→F06** |

Depois disso, a comparação do perfil de aceleração mostrou que as traseiras ainda espicavam
57,9 px na entrada do contato enquanto o frontal mantinha um platô de 38. Elas foram
equalizadas em `rear-arc/`:

| Transição | `front_r` | `back_r` antes | `back_r` depois | `back_l` depois |
|---|---|---|---|---|
| 5→6 | 38,2 | 35,6 | 42,3 | 36,9 |
| 6→7 | 37,9 | 38,1 | 38,1 | 34,1 |
| 7→8 | 37,8 | **57,9** | 36,2 | 34,1 |
| 8→9 | 36,2 | 8,6 | 37,7 | 35,0 |

O quase-congelamento de 3,2 px em `4→5` do `back_r` também desapareceu.

### Erro meu que os autores pegaram

A tabela de grade que escrevi somava 700 ms, não 730: eu paguei o quadro novo duas vezes,
reduzindo também o `follow-through`. O autor frontal recusou fechar com o número errado e
perguntou. Corrigido, e o `follow-through` voltou a 100 ms.

### O que segue em aberto, com número

- **Machado:** vão vazio de 22–24 px entre `coil` e `cleave` nas quatro direções. Mesmo tipo
  de defeito, mesma solução, não foi feito porque a queixa era a espada.
- **Entrada e acomodação das traseiras:** `F02→F03` em `back_r` é 34,6 px contra 16,5 px do
  frontal, e o último passo é 8,9 px contra 22,0 px. É entrada e acomodação, não a descida.
- **Corpo mais escuro nas traseiras:** a camada `body` de `back_r` não tem nenhum pixel com
  luminância ≥ 160, contra 38 nos bookends do frontal. É arte herdada, não desta rodada.

## 13. Estado final depois do retoque

| Portão | Resultado |
|---|---|
| `TECHNICAL_PASS` | 28 células, 232 quadros, 996 hashes |
| Reexportação das fontes salvas | `PASS_SAVED_SOURCE_EXPORTS`, 38 mestres, 424 quadros |
| Chromium da página principal | 20/20 |
| Chromium da inspeção ampliada | 9 imagens, 0 quebradas, 0 erros |
| Contrato do quadro novo | `PASS`, 4 células, 14 quadros, 730 ms, contato F08/325 ms |
| Duplicatas com arma visível | 0 nas 8 células |
| Maior passo do Sword | `F05→F06`, 36,9 a 42,3 px nas quatro direções |
| `contactEvent` | F08/325 ms (Sword) e F06/410 ms (Axe) nos 8 clipes |


