# Experimento 01 — Skeleton-first: motion design do Sword `back_l`

Você é o DEV responsável pela **frente de motion design** deste experimento. Seu produto é
movimento, não arte final. Ninguém vai desenhar pixels nesta etapa e você também não deve.

## Escopo, e o que está proibido

Alvo único: **Orc principal atual (`orc-v1` / Verde Warcraft), ataque de Espada, direção `back_l`.**

Não modifique, em hipótese alguma:

- Outras direções de espada, o ataque de Machado, Idle, Walk, Unarmed, Hit ou Defeat.
- Manifests de produção, mestres aprovados, `characters/orc-v1/source/combat-recovery-v8/`.
- Nada em `../TacticsRPG` (Unity).
- Nenhum `.aseprite` existente.

Todo o seu produto vive em `experiments/main-orc-skeleton-first-01/`. É experimento isolado.

Não chame PixelLab. Não gere imagem por IA. Não faça commit. Zero gerações pagas.

## Fontes que você deve ler antes de planejar

1. Identidade atual: `reports/orc-production-current.json`, `characters/orc-v1/character.json`.
2. Corpo de referência da vista: `characters/orc-v1/source/complete-v1/back_l/Idle/*.png`
   (frames nativos, 128×128, `groundY` 126). Use F00 como referência de postura e escala.
3. Arma: `characters/orc-v1/source/combat-rescue-v5/combat/weapons/Sword/recruit-sword.png`
   e `weapon.json` (dimensões, empunhadura, pivô).
4. Timing vigente do ataque de espada: `characters/orc-v1/source/combat-recovery-v8/rear-arc/back_l-sword/clip.json`
   — 14 quadros, 730 ms, fases `rest, body-preparation, establish-grip, anticipation,
   coil-behind, apex-hold, apex-descent, slash-release, contact, follow-through, recoil,
   settle-grip, release-grip, return-to-guard`, `contactEvent` no índice 8 / 325 ms.
5. Tentativas traseiras já reprovadas, para você **não repetir os mesmos erros**:
   `combat-recovery-v7/rear-alt/back_l-sword`, `combat-recovery-v8/rear/back_l-sword`,
   `combat-recovery-v8/rear-inbetween/back_l-sword`, e o veto do criador registrado em
   `experiments/main-orc-combat-recovery-v8/report.md`.

## Que técnica você está reproduzindo

Leia as vistas frontais que o criador aceitou como demonstração de técnica:
`characters/orc-v1/source/combat-recovery-v8/frontal-inbetween/front_r-sword` e `front_l-sword`.
Elas fazem um corte diagonal de cima para baixo: a arma sobe acima e atrás da cabeça, desce num
arco contínuo, contata, segue adiante e recolhe. **Não copie coordenadas delas para `back_l`** —
extraia a *técnica*: qual articulação inicia o movimento, em que ordem, onde está o peso, em que
instante o quadril gira, quanto o ombro viaja.

O criador repetidamente reclamou que `back_l` "ataca de lado". O erro a evitar é gerar travessia
lateral na tela em vez de golpe para frente. Pense em três dimensões: a lâmina desce num plano que
vai na direção do oponente, e a projeção 2D disso numa vista de costas-esquerda é o que você deve
desenhar.

## O que você entrega

### 1. `experiments/main-orc-skeleton-first-01/poses.json`

Cinco poses-chave, na ordem: prontidão, elevação/antecipação, golpe principal, seguimento,
recuperação. Cada pose é um esqueleto de **18 juntas COCO-18**, exatamente estes rótulos, todos
presentes uma vez por pose:

`NOSE, NECK, RIGHT SHOULDER, RIGHT ELBOW, RIGHT ARM, LEFT SHOULDER, LEFT ELBOW, LEFT ARM,
RIGHT HIP, RIGHT KNEE, RIGHT LEG, LEFT HIP, LEFT KNEE, LEFT LEG, RIGHT EYE, LEFT EYE,
RIGHT EAR, LEFT EAR`

Regras do contrato (isto vem do `animate_with_skeleton_v3` do PixelLab e precisa bater 1:1):

- `x` e `y` são frações de 0 a 1 da imagem, com origem no canto superior esquerdo e `y` para baixo.
- `ARM` é o **punho**, `LEG` é o **tornozelo**.
- `LEFT`/`RIGHT` são os lados **do personagem**, não do observador.
- Cada junta aceita `z_index` (ordem de desenho, inteiro, seu) e `depth` opcional de 0 a 255,
  onde ~128 é o centro do corpo e valores maiores estão mais perto da câmera.

Além das juntas, cada pose deve carregar, em campos próprios do seu JSON, a **empunhadura**:
ponto de pega na mão, direção do cabo e direção da lâmina, em coordenadas da mesma imagem.
O cabo e a lâmina não são juntas COCO; são campos seus, e são obrigatórios.

### 2. `experiments/main-orc-skeleton-first-01/sequence.json`

A sequência interpolada de **14 quadros** entre as cinco poses-chave, na grade de 730 ms do clipe
vigente, com a fase nomeada de cada quadro igual à do `clip.json` citado acima. Os quadros 0 a 4
devem coincidir exatamente com as cinco poses. A interpolação deve ser angular nas articulações
(interpolar o ângulo do membro, não a posição linear da junta), para o membro não encurtar no meio
do arco. Este arquivo alimenta o visualizador que outro DEV vai construir; respeite o formato.

### 3. `experiments/main-orc-skeleton-first-01/report.md`

Em português, com:

- A interpretação tridimensional da postura que você adotou (de onde vem a câmera, para onde o
  orc olha, qual lado é o braço da espada, como o corpo se apoia).
- A técnica identificada nas frontais e o que você transplantou dela.
- Uma tabela por pose com: ângulo do ombro, do cotovelo, do punho, rotação de tronco, ângulo da
  lâmina em relação ao solo, e a posição do centro de massa estimada.
- Comprimentos de úmero, antebraço, coxa e canela em cada pose, provando que não variam mais que
  alguns por cento entre poses. Estabilidade de comprimento é critério de aceitação.
- Onde estão as duas mãos, e por que a mão que não segura a espada está onde está.
- A trajetória da ponta da lâmina através dos 14 quadros, com a distância percorrida por quadro.
  **Não otimize para deslocamento pequeno**: um golpe tem aceleração. O que não pode existir é
  salto sem arco, ou seja, quadro seguinte em posição sem nenhum caminho plausível.
- O que você evitou das tentativas reprovadas, nominalmente.

## Critérios de aceitação que serão medidos

1. As cinco poses formam um único ataque coerente de cima para baixo, não um golpe lateral.
2. A perspectiva `back_l` se mantém constante: ombros e quadris não trocam de lado entre poses.
3. Comprimento de úmero, antebraço, coxa e canela estáveis entre poses.
4. A mão que segura a espada está sempre no cabo; o cabo sempre na mão.
5. A ponta da lâmina traça um arco monotônico de cima para baixo durante o golpe, sem retorno
   espúrio e sem teleporte.
6. Nenhum pé atravessa o chão (`y` do tornozelo no máximo 126/128 na referência) e nenhum pé
   flutua sem motivo.
7. O peso se transfere: o quadril não fica parado enquanto a lâmina viaja.

Se você concluir que alguma dessas metas é incompatível com a vista `back_l`, escreva isso no
relatório com a razão geométrica, em vez de falsificar o número.
