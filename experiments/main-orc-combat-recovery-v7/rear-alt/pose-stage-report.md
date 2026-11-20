# back_l Sword — alternativa manual V7

`V7_BACK_L_APEX_MANUAL_READY` · `TECHNICALLY_COMPLETE` · `VISUAL_REVIEW_REQUIRED` · `PENDING_CREATOR`

[Comparação visual e juntas](preview.html) · [Plano medido](joint-plan.json) · [Verificação](verification.json)

## Método e escopo

Duas poses isoladas, ápice e impacto; não são ciclo nem autorização de interpolação. Autoria manual/programática em Lua executada no Aseprite --batch --noinapp, perfil tmp/aseprite-v7-alt-profile. Pixels herdados são explicitados; não é desenho manual pela GUI e não houve geração PixelLab, imagegen, rasterização externa ou espelhamento. Custo de geração: zero chamadas/zero créditos. Nenhum saldo foi estimado.

## Escolha medida do doador do ápice

Juntas selecionadas visualmente sobre ampliação salva; incerteza de marcação ±1 px nativo. Precisão decimal registra somente a geometria calculada, não precisão anatômica subpixel. Coordenadas nativas 128; somar [64,64] para o composto.

| Doador (mesma vista back_l) | Ombro→cotovelo→punho→palma | Úmero px | Antebraço px | Ângulo interno | Decisão |
|---|---|---:|---:|---:|---|
| back_l-axe/03 | [89, 39] → [99, 35] → [93, 23] → [88, 17] | 10.77 | 13.416 | 85.236° | SELECT forearm+closed glove; both bounded and visible; upper arm foreshortened and must be reauthored |
| back_l-axe/02 | [89, 39] → [101, 44] → [101, 31] → [98, 27] | 13.0 | 13.0 | 67.38° | NOT_SELECTED wrist lower; broader bracer and less independent hand |
| back_l-sword/03 | [89, 39] → [103, 39] → [101, 28] → [96, 25] | 14.0 | 11.18 | 79.695° | NOT_SELECTED shortened forearm, cuff blends shoulder |
| back_l-sword/04 | [89, 40] → [104, 43] → [104, 33] → [101, 31] | 15.297 | 10.0 | 78.69° | NOT_SELECTED low wrist/hand and arm overlap |

Escolhido Axe F03: mão em cluster fechado, punho e antebraço completos; envelope da luva/manopla x82..98/y11..24. O braço superior original está encurtado por projeção. Não foi ampliado ou esticado: só antebraço+luva foram transladados [12,2] a 1:1, sem rotação/espelho; o úmero foi redesenhado. As linhas exatas da máscara estão em author-result.json e no Lua. A área doadora contém punho real (não vazio nem mero recorte de antebraço).

Referência de comprimento no braço oposto da própria base: ombro [47,40], cotovelo [39,62], punho [35,76], úmero 23,409 px e antebraço 14,560 px. O úmero final elevado tem 23,087 px (0,986× essa referência); antebraço 13,416 px (0,921×). Isso sustenta a escolha geométrica sem exigir igualdade entre projeções.

## Construção e medições finais

| Pose | Ombro | Cotovelo | Punho | Palma | Úmero | Antebraço | Ângulo |
|---|---|---|---|---|---:|---:|
| apex | [88, 39] | [111, 37] | [105, 25] | [100, 19] | 23.087 px | 13.416 px | 68.405° |
| impact | [83, 48] | [104, 56] | [110, 75] | [109, 81] | 22.472 px | 19.925 px | 128.38° |

Ápice: punho 14 px acima da linha do ombro, palma 20 px acima. Topo do crânio incluindo contorno y=9; ponta da lâmina [89, -39] no referencial nativo, ou [153, 25] no composto: 48 px acima do crânio. O item ultrapassa a área corporal 128 por desenho, mas cabe no composto 256 sem corte. O antebraço é exposto em espaço negativo: mínimo de 4 px transparentes entre corpo e braço nos cortes y24..30. Cotovelo exterior em [111,37], dobrado 68,405°, distinto do tronco.

O corpo-base vem de Sword F03 (chamber): retirei o membro antigo antes da transferência, redesenhei o úmero saindo da ombreira e a manga/cota, e defini a placa externa do cotovelo. O doador original não se manteve escondido sob o braço novo. Ajustes de costura e borda são locais. A luva vem do próprio membro da mesma vista, mantendo forma fechada e conexão ao punho.

Comparação artística principal é contra Sword V6 F04, fase loaded-apex rejeitada; F03 é explicitamente a base de edição, disponível separadamente na página. Não confundir a comparação entre fases com a prova pixel a pixel contra a fonte real F03.

Impacto: doador Sword back_l F07, o próprio braço da base, com cotovelo [89,64], punho [95,83], palma [94,89]. Antebraço 19,925 px preservado por translação [15,-8]; úmero reconstruído da ombreira [83,48] até o cotovelo [104,56] (22,472 px). Punho final [110,75] e palma [109,81] têm terminação legível fora do tronco. Uma sobra de três pixels do braço antigo em x85..86/y79..80 foi removida. A espada aponta para baixo e à frente (115°), ponta [163,105] em coordenadas relativas ao nativo, dentro do composto e acima do chão. O tronco/base de apoio é o F07 original: não se atribui à pose estática uma entrega de impacto temporal ainda não demonstrada.

## Item e mestres

Espada independente combat-rescue-v5/combat/weapons/Sword, sem alteração de design. Cabo no intervalo fonte v60..70 fica em weaponBack; guarda, lâmina e pomo disco em weaponFront; luva autêntica em handFront. Ordem: weaponBack → body → weaponFront → handFront. Guarda acima dos dedos e pomo abaixo da pega permanecem visíveis. Não há arma assada no corpo. Arquivos nativos são somente recorte de body; arma pode exceder canvas corporal sem contaminar o nativo.

Ambas as poses têm mestres 256 e 128 salvos, fechados, reabertos e comparados em RGBA respeitando cel.position real; tempos 110 ms (ápice) e 80 ms (impacto) são durações de representantes em segundos no Lua, não um ciclo de dois frames. representative.json por pose contém hashes reais, fontes, juntas e verificação.

## Preservação comprovada

| Pose | Pixels de corpo alterados | Envelope nativo alterado | Componentes 8-conectados finais |
|---|---:|---|---:|
| apex | 777 | [86, 13, 115, 51] | 1 |
| impact | 1238 | [80, 46, 116, 93] | 1 |

Por comparação RGBA, a metade esquerda x0..79 inteira (braço oposto, cabeça e núcleo do tronco) e região y95..127 (pernas/pés) são idênticas às respectivas fontes. Saiote/tassets foram preservados fora das máscaras do braço; não houve deformação global de corpo, rotação ou escala corporal. A edição se concentra no membro dominante/saída da ombreira. Um único componente corporal conectado por pose; juntas marcadas sobre pixels opacos; nenhuma duplicação ou amputação de membro observada nas ampliações. Igualdade composto=alpha-over das quatro camadas e native=crop(body) com zero diferenças; zero pixels de arma abaixo de groundY190.

349 arquivos protegidos V6, item V5 e entrega rear-r (arte + evidência) conferidos por SHA-256 e byte-idênticos. Nenhuma escrita em rear, rear-r, fontes V6/V5, Unity ou commits.

## Limitações e próximo portão

Autoria programática do úmero/manga tem acabamento próprio e ainda pode exigir polimento artístico de material, perspectiva e transição da ombreira. Medidas de juntas, um componente conectado e espaço negativo demonstram a proposta estrutural; não aprovam a arte. A mão do doador é distinguível na pose, mas a naturalidade de sua rotação e da pega deve ser julgada pelo criador.

Faltam antecipação anterior ao ápice, aceleração, passagem entre as duas chaves, contato, follow-through e retorno, além da revisão do arco no tempo real. Não produzir intermediários nem escalar ao ciclo antes da decisão do orquestrador/criador. Parada em V7_BACK_L_APEX_MANUAL_READY.

Preview conferido em Edge/Chromium headless: 8 comparações canvas↔PNG exatas nas duas poses, antes/depois e body-only/composto; ampliações/legendas carregadas, zoom/tático e HTTP/file funcionais, sem erros JavaScript. Evidência em browser-check.json e preview-check.png.
