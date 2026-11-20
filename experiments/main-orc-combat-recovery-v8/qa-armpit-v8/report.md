# Axila front_l/Sword — candidato local V8

`TECHNICALLY_COMPLETE` · `VISUAL_REVIEW_REQUIRED` · `PENDING_CREATOR`

## Diagnostico antes de desenhar

Foram abertos os mestres salvos no Aseprite e renderizados F03/F04/F05 do corpo front_l, front_r/Sword protegido, back_l/Sword V8 e F00 de Idle front_l. Evidencia: references/comparison.png (colunas nessa ordem; linhas F03, F04, F05; Idle apenas na primeira linha). A referencia traseira foi renderizada do composto salvo e contem equipamento; a juncao pode ser examinada sem usar a arma como evidencia anatomica.

O retangulo aproximado x80..130/y60..120 informado no pedido cai predominantemente sobre cabeca, peito e o outro ombro no canvas 256 deste clipe. A juncao reclamada fica a direita da imagem: x147..158/y106..114. Tambem foi inspecionado o recorte aproximado indicado; nao foi usado para deslocar ou espelhar anatomia.

Contorno legitimo medido: rgb(0,0,1), (2,2,3), (6,6,8). Sombra interna principal: rgb(20,20,26), com transicao (27,28,34) e metal sombreado (43,45,49). Idle usa as mesmas cores; front_r inclui metal (33,34,40)/(49,51,55) e back_l (26,26,32)/(33,34,40). Os numeros sao amostras reais dos mestres, nao uma paleta universal.

Nao foi encontrada cor estranha responsavel pelo defeito. A faixa interna usa cores legitimas de contorno e sombra em area extensa: essa distribuicao funde a ligacao do deltoide ao tronco numa massa quase preta. Existe continuidade alfa opaca; o vazio transparente abaixo do braco e espaco externo, nao deve ser preenchido indiscriminadamente. Minha leitura visual e de perda de volume na juncao, nao de um pixel com cor ilegal.

## Reparo e procedencia

Autoria programatica Lua executada no Aseprite, em copia isolada dos mestres V7. Reiluminacao de uma superficie curta e escalonada de cota/metal na ligacao interna, com tons existentes (27,28,34)/(43,45,49); contorno externo, alpha, tecido vermelho e highlights preservados. Nao se pintou outra placa de tinta na borda nem se preencheu todo o espaco negativo. A textura pretende explicitar a ligacao sob o deltoide; sua aceitacao perceptual continua pendente do criador.

Plano exato com coordenadas e RGBA antes/depois: edit-plan.json. Script: author-armpit.lua. Mestres composto, corpo e nativo foram salvos, reabertos e reexportados; verificacoes no proprio Aseprite em reopen-result.json. 219 escritas correspondem aos mesmos 73 pixels nas tres representacoes, nao a 219 pixels diferentes.

## Diferencas medidas

| Quadro (indice 00) | Corpo | Composto visivel |
|---|---:|---:|
| F03 | 25 | 25 |
| F04 | 15 | 12 |
| F05 | 33 | 33 |

Todas as transicoes abaixo sao RGBA com alfa 255. Nenhum canal RGB diminuiu.

| Quadro | RGB antes | RGB depois | Pixels |
|---|---|---|---:|
| F03 | (0, 0, 1) | (27, 28, 34) | 4 |
| F03 | (2, 2, 3) | (27, 28, 34) | 7 |
| F03 | (2, 2, 3) | (43, 45, 49) | 4 |
| F03 | (6, 6, 8) | (27, 28, 34) | 1 |
| F03 | (6, 6, 8) | (43, 45, 49) | 1 |
| F03 | (20, 20, 26) | (27, 28, 34) | 5 |
| F03 | (20, 20, 26) | (43, 45, 49) | 2 |
| F03 | (27, 28, 34) | (43, 45, 49) | 1 |
| F04 | (2, 2, 3) | (27, 28, 34) | 3 |
| F04 | (2, 2, 3) | (43, 45, 49) | 1 |
| F04 | (6, 6, 8) | (27, 28, 34) | 2 |
| F04 | (20, 20, 26) | (27, 28, 34) | 5 |
| F04 | (20, 20, 26) | (43, 45, 49) | 3 |
| F04 | (27, 28, 34) | (43, 45, 49) | 1 |
| F05 | (2, 2, 3) | (27, 28, 34) | 10 |
| F05 | (2, 2, 3) | (43, 45, 49) | 6 |
| F05 | (6, 6, 8) | (27, 28, 34) | 11 |
| F05 | (6, 6, 8) | (43, 45, 49) | 5 |
| F05 | (27, 28, 34) | (43, 45, 49) | 1 |

## Provas e limites

- zoom/armpit-before.png e zoom/armpit-after.png, na pasta pai: ampliacao exata 8x nearest-neighbour, ROI [136,96,176,132), colunas F03/F04/F05; linha superior corpo layers-off, inferior composto. Fundo cinza e apenas da superficie de revisao.
- 13 quadros; duracoes 30,65,35,50,45,65,35,35,100,55,80,45,90 ms; total 730 ms. Janela armada [2,10] preservada. Nenhuma posicao/rotacao de arma alterada; tres camadas weaponBack/weaponFront/handFront byte-identicas em todos os quadros.
- Metadado herdado contactEvent apontava F07/325 ms, inconsistente com o impacto de 290 ms solicitado. No novo clip.json foi corrigido apenas para F06/290 ms (inicio de F06); os tempos e pixels desses quadros continuam identicos.
- Zero diferencas RGBA nos dez compostos fora de F03/F04/F05. Todos os 73 pixels alterados tinham max(R,G,B)<=34, logo nenhum highlight existente foi apagado. Alpha e silhueta identicos em todos os quadros.
- Igualdade do corpo do composto com body.aseprite e do recorte [64,64] com native.aseprite conferidas apos reabrir. Hashes de mestre e 13 compostos de front_r/Sword protegido conferidos contra seu contrato.
- Candidata entregue separadamente em characters/orc-v1/source/combat-recovery-v8/frontal-armpit/front_l-sword/clip.json. Patch e matriz V8 nao alterados. Sem commit, Unity, IA generativa ou PixelLab.

O passe foi inspecionado em quadros estaticos ampliados e na referencia do corpo inteiro. Nao houve novo QA independente nem avaliacao temporal em 1x nesta tarefa. A melhora proposta nao concede aprovacao artistica; a leitura da juncao deve ser reavaliada pelo criador.
