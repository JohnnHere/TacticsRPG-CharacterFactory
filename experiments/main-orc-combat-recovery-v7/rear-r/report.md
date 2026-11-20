# V7 back_r — refinamento local

`V7_BACK_R_REFINED` · `TECHNICALLY_COMPLETE` · `VISUAL_REVIEW_REQUIRED` · `PENDING_CREATOR`

Autoria programática Lua no Aseprite sobre pixels herdados de V6; nenhum desenho manual alegado. Zero chamadas PixelLab, nenhuma compra, sem Unity ou commits.

[Preview antes/depois](preview.html) · [Auditoria inicial](audit.md) · [Medições](grip-metrics.json) · [Verificação](verification.json)

## Causa e limites da evidência

A média normal da máscara V6 em Axe F03/F04 é +0,390/+0,342 px: isto **não** demonstra por si uma palma fora do cabo. A inspeção ampliada identifica o defeito de leitura: manopla longa com massa metálica abaixo do cabo e ausência de dobras/dedos fechando a madeira. O cabo já estava atrás do corpo; inverter layers ou rotacionar só o item repetiria o erro. A causa visual é fechamento/forma local inadequados; não foi demonstrado erro de pomo.

Reparo: preservar antebraço/cotovelo e reautorar clusters de couro da própria palma em cada pose; dedos cruzam os dois lados do eixo, com sombra sob polegar e dobras transversais. Assento do Axe deslocado +2 px em x nas poses 02–05, -1 px em y nas 06–09; nenhum ângulo alterado. Sword F03 +1 px em x, demais assentos preservados. As máscaras são as linhas anatômicas por pose; nenhum doador de outra vista. O fechamento é local e precisa do parecer artístico do criador.

## Alterações por quadro

| Clipe/F | pixels corpo/pegada | contorno corpo | contorno item | preservação |
|---|---:|---:|---:|---|
| Sword/00 | 0 | 0 | 0 | pernas/tronco/tempos/ângulos |
| Sword/01 | 33 | 0 | 2 | pernas/tronco/tempos/ângulos |
| Sword/02 | 31 | 0 | 1 | pernas/tronco/tempos/ângulos |
| Sword/03 | 31 | 0 | 1 | pernas/tronco/tempos/ângulos |
| Sword/04 | 33 | 0 | 3 | pernas/tronco/tempos/ângulos |
| Sword/05 | 29 | 0 | 1 | pernas/tronco/tempos/ângulos |
| Sword/06 | 30 | 0 | 1 | pernas/tronco/tempos/ângulos |
| Sword/07 | 28 | 0 | 3 | pernas/tronco/tempos/ângulos |
| Sword/08 | 27 | 0 | 3 | pernas/tronco/tempos/ângulos |
| Sword/09 | 27 | 0 | 1 | pernas/tronco/tempos/ângulos |
| Sword/10 | 0 | 0 | 0 | pernas/tronco/tempos/ângulos |
| Sword/11 | 0 | 0 | 0 | pernas/tronco/tempos/ângulos |
| Axe/00 | 0 | 0 | 0 | pernas/tronco/tempos/ângulos |
| Axe/01 | 37 | 0 | 6 | pernas/tronco/tempos/ângulos |
| Axe/02 | 37 | 0 | 6 | pernas/tronco/tempos/ângulos |
| Axe/03 | 37 | 0 | 5 | pernas/tronco/tempos/ângulos |
| Axe/04 | 41 | 0 | 4 | pernas/tronco/tempos/ângulos |
| Axe/05 | 39 | 0 | 11 | pernas/tronco/tempos/ângulos |
| Axe/06 | 37 | 0 | 6 | pernas/tronco/tempos/ângulos |
| Axe/07 | 20 | 0 | 5 | pernas/tronco/tempos/ângulos |
| Axe/08 | 25 | 0 | 6 | pernas/tronco/tempos/ângulos |
| Axe/09 | 25 | 0 | 6 | pernas/tronco/tempos/ângulos |
| Axe/10 | 0 | 0 | 0 | pernas/tronco/tempos/ângulos |
| Axe/11 | 0 | 0 | 0 | pernas/tronco/tempos/ângulos |

## Evidência específica Axe

F03/F04/F07 usam índices 03/04/07. Recortes 40×40 ampliados 16× pelo Aseprite, centrados no respectivo assento; o deslocamento é informado nas métricas.

| Quadro | Antes | Depois |
|---|---|---|
| F03 | [ampliação](grip-03-before.png) | [ampliação](grip-03-after.png) |
| F04 | [ampliação](grip-04-before.png) | [ampliação](grip-04-after.png) |
| F07 | [ampliação](grip-07-before.png) | [ampliação](grip-07-after.png) |

F03/F04: eixo quase vertical; dedos cruzam a madeira lateralmente, polegar fecha no lado direito/voltado à lâmina; punho corporal continua abaixo da palma, sem deslocar antebraço. F07: eixo quase horizontal; dedos cobrem o cabo por cima e por baixo, punho chega pela região superior/esquerda da palma. O pomo permanece no sentido longitudinal positivo (cauda), cabeça do machado no negativo. A arma não passa na frente da luva no trecho de pegada: fica em weaponBack e é ocluída pela mão.

## Contornos e flash

Todo pixel de contorno alterado está em author-result.json com camada, quadro, coordenada e RGBA inteiro antes/depois. O passe do item se limita ao perímetro metálico exposto após transformação, preenchido com aço de sombra (38,43,48); highlights internos preservados. Não há aplicação de filtro global no personagem.

Inspeção numérica: nenhum pixel corporal neutro >=170 em RGB nos 24 corpos V6; isto só exclui flash branco nesse limiar, não toda falha perceptiva. A inspeção ampliada não confirmou swoosh/flash branco corporal em back_r Sword. O candidato mais evidente é o rebordo claro da própria lâmina durante a rotação: tratado no perímetro das camadas de arma. Ver flash-audit.json para as coordenadas exatas e componentes claros restantes. Reflexos internos móveis são material metálico legítimo; não eliminá-los para satisfazer regra cega de coordenadas fixas.

## Preservação e limitações

24 quadros: pernas, tronco, braço oposto, cotovelos, apoios, duração e ângulos preservados; somente pixels listados da luva/candidatos de contorno corporal mudam o corpo. Mestres composto/nativo salvos, reabertos e comparados com cel.position real. Álgebra alpha-over, recorte body→native, bookends e limite groundY verificados. Fontes V6 inventariadas permanecem byte-idênticas. Scripts e saída confinados aos dois diretórios autorizados, com perfil Aseprite separado.

A correspondência artística com back_l V7 depende da outra frente e não foi assumida. A naturalidade do movimento e da pegada ainda exige revisão visual do criador; este checkpoint não concede aprovação nem integração.

## Eixo do punho e oclusão — Axe (medição adicional)

Marcos de punho selecionados visualmente na junção luva/antebraço; não são centróides automáticos. n é normal ao cabo, t aponta para a cauda/pomo. Coordenadas compostas.

| F | punho corporal (x,y) | cabo antes → depois | punho n/t antes (px) | punho n/t depois (px) | oclusão item antes→depois |
|---|---|---|---|---|---|
| 03 | [160, 93] | [156, 84] → [158, 84] | [2.376, 9.558] | [0.407, 9.211] | 131→132 |
| 04 | [155, 91] | [151, 82] → [153, 82] | [4.0, 9.0] | [2.0, 9.0] | 121→122 |
| 07 | [162, 153] | [163, 159] → [163, 158] | [-6.064, 0.473] | [-5.068, 0.56] | 45→45 |

Em F03/F04, punho está longitudinalmente abaixo da palma e do lado normal positivo; na imagem elevada, isso corresponde a baixo/direita. Em F07, punho está acima/esquerda da palma, com normal negativa. Esses marcos foram preservados: a correção fecha a palma ao redor do eixo e não desloca o bracelete para simular nova mão. Os pixels reautorados têm projeções dos dois sinais da normal nas três poses (coordenadas em grip-metrics.json). A contagem de sobreposição é quase igual antes/depois: demonstra por que contagem de contato e socket V6 não eram prova de boa pegada.

Contorno: após o passe, 0 pixels claros neutros (mínimo RGB ≥140, amplitude RGB <28) expostos ao alfa na silhueta composta dos 24 quadros. Nenhum contorno corporal confirmou o critério de reparo; 0 pixels corporais de halo foram apagados. O reparo claro foi restrito ao item. Esse diagnóstico não equivale a afirmar ausência universal de flicker artístico.

Preview verificado em Edge/Chromium headless: 96 comparações canvas↔PNG exatas (antes/depois × corpo/composto × 12 quadros × 2 ações), controles e carregamento HTTP/file, sem erro JavaScript. Screenshot: preview-check.png.