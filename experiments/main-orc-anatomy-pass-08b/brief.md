# Passe anatômico 08b — reconstrução manual do braço direito de ataque

Segundo passe no quadro 08. O primeiro (`main-orc-anatomy-pass-08/candidate-08.png`) foi
**REJEITADO pelo criador** por leitura anatômica. Consulte-o apenas para entender o que não fazer —
**não o use como base, não parta dele**.

## Limites duros

- **Zero PixelLab, zero geração de imagem.** A autoria é manual no Aseprite, pixel por pixel ou
  por clusters desenhados.
- Não redesenhe o Orc. Não espelhe braço. Não interpole quadros. Não componha a espada.
- Não toque em `characters/`, `assets/`, `reports/`, `../TacticsRPG`. Não faça commit.
- Trabalhe em `experiments/main-orc-anatomy-pass-08b/`. A fonte canônica
  (`main-orc-skeleton-02/stage-bcde/body-only/08.png`) e o passe rejeitado ficam somente leitura.

## Por que o passe anterior falhou — não repita

O método anterior **girou segmentos rígidos** do braço original preservando comprimentos como
critério absoluto. Resultado: o membro virou uma peça segmentada — braço superior grosso (21–23 px),
depois um conector magro de **6–7 px**, depois uma luva de 15–18 px que parece solta. Volume não é
comprimento: o que faltava era massa e transição de material.

**Proibido neste passe:** rotação de segmentos como método, tolerância de comprimento como objetivo,
resolver anatomia apenas mudando ângulos de junta. Você vai **refazer os clusters e a silhueta
local**: apagar o braço atual na região do membro e reautoriá-lo com volume, contorno e transições
de material.

## Base e referências

- **Alvo (base do candidato):** `experiments/main-orc-skeleton-02/stage-bcde/body-only/08.png`.
- **Braço esquerdo no próprio 08 é sua referência de espessura, contorno e acabamento** — é o mesmo
  Orc, mesmo material, mesmo estilo de luz. Não copie nem espelhe: a pose é assimétrica e o braço
  direito está em ação, não pendente.
- **Braço direito nos quadros 05 e 09** (`body-only/05.png`, `body-only/09.png`) como referência de
  articulação em movimento: como a luva fecha, como o cotovelo dobra, como a sombra assenta.
- Dados medidos por mim, para você não começar às cegas:
  - Braço direito atual: ~21–23 px de espessura junto ao ombro, afinando para **6–7 px** no
    antebraço (x≈166–170), depois 15–18 px na luva. Esse vale magro é o defeito central.
  - Paleta do braço esquerdo, por frequência: tinta `(2,2,3)`, armadura `(33,34,40)`,
    vivos vermelhos `(51,19,28)`, `(36,14,23)`, `(72,33,38)`, metal claro `(86,88,92)`,
    cinzas `(49,51,55)`, `(58,60,64)`, sombras `(26,26,32)`, `(20,20,26)`, couro `(38,27,27)`.
  - Ombreira em torno de `(140..160, 95..115)`; a região móvel começa **sob** ela.
  - Contato da mão no quadro original: `(178,131)`. O ponto `(167,140)` do passe rejeitado
    **não está aprovado** — decida a posição da mão **depois** de resolver a anatomia, e registre o
    pivô exato que você adotar.

## O que reconstruir

Somente o braço direito de ataque: braço superior, cotovelo, antebraço, pulso e mão, mais a junção
indispensável sob a ombreira. O membro precisa ter:

1. **Volume**: espessura coerente do ombro ao punho, sem vale magro no antebraço. Compare com a
   espessura visual do braço esquerdo e do braço nos quadros 05/09.
2. **Contínuo**: contorno de tinta acompanhando toda a silhueta do membro, sem pixels órfãos, sem
   penhasco de alfa, sem "luva solta".
3. **Transições de material coerentes**: tinta → armadura → luz, como no braço esquerdo; luva
   legível como punho fechado.
4. **Leitura de golpe descendente**: o conjunto ombro→cotovelo→punho deve descer em diagonal, sem
   virar a horizontal reprovada e sem virar o Chicote segmentado do passe anterior.

A posição da mão é sua, depois da anatomia: o que manda é o membro ser crível. Registre o pivô.

## Intocável

Rosto, cabeça, tronco, cinto, pernas, botas, paleta, escala, e o contorno externo do resto do corpo.
A ombreira permanece; só a junção indispensável sob ela pode ser retratada. Tudo fora do braço e
dessa junção: **byte-idêntico**.

## Entrega, em `experiments/main-orc-anatomy-pass-08b/`

1. `candidate-08b.png` — o candidato único (body-only, 256×256).
2. `master-08b.aseprite` — mestre salvo, reaberto e verificado.
3. `before-after.png` — 1× e 8× lado a lado.
4. `comparison.png` — o candidato em 8× com os dois braços (esquerdo do próprio 08 e direito de 05
   e 09), para julgar espessura e acabamento.
5. `changed-regions.png` — mapa das regiões alteradas.
6. `pixel-diff.json` — caixas alteradas e contagem por caixa.
7. `report.md` — como você reconstruiu os clusters, o pivô adotado para a mão, a espessura do novo
   membro por trecho comparada à referência, e a confirmação de que tudo fora do braço ficou
   byte-idêntico.

## Critério para considerar o passe promissor

O braço precisa ter **volume e conexão legíveis em 1×** — não pode parecer peça segmentada nem mão
destacada em 8×. Se você não conseguir isso sem comprometer a identidade do Orc, **pare e explique
o conflito** no relatório. Não amplie o escopo.
