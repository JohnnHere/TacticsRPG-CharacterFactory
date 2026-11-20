# Experimento 02 — Estágios B, C, D e E: corpo, espada independente, pegada e composição

Você produz a peça central do experimento. O alvo é único: **Orc principal atual, ataque de Espada,
direção `back_l`, cinco poses estruturais.** Nada além disso.

## Limites duros

- **Zero chamadas pagas ao PixelLab.** Não invoque geração de nenhum tipo.
- Não gere espada nova. Reutilize a arma oficial.
- Não toque em `characters/`, `assets/`, `reports/`, nem em `../TacticsRPG`.
- Não promova nada, não mexa em manifesto de produção, não faça commit.
- Escreva apenas em `experiments/main-orc-skeleton-02/stage-bcde/`.

## O achado que muda o jogo

O clipe atual **já tem corpo e arma em camadas independentes**:

`characters/orc-v1/source/combat-recovery-v8/rear-arc/back_l-sword/layers/{body,handFront,weaponBack,weaponFront}/NN.png`

Ou seja, o contrato de camadas que a task pede já existe: `weaponBack → body → weaponFront →
handFront`. Seu trabalho é usar esse contrato, não inventar outro.

As cinco poses estruturais correspondem a estes índices do clipe de 14 quadros:

| Pose | Índice | Fase |
|---|---|---|
| 1. Preparação | 00 | `rest` |
| 2. Elevação / antecipação | 05 | `apex-hold` |
| 3. Golpe principal | 08 | `contact` |
| 4. Seguimento | 09 | `follow-through` |
| 5. Recuperação | 13 | `return-to-guard` |

## Estágio B — as cinco poses anatômicas

Para cada pose, documente ombro, cotovelo, punho, mão que empunha, orientação do tronco, quadril,
base de apoio, contato com o chão e a orientação pretendida do cabo. Use como referência anatômica
as juntas que já existem em
`experiments/main-orc-skeleton-first-01/poses-fixed.json` e `sequence-fixed.json`, que foram
medidas a partir desta mesma arte.

**Não otimize o movimento para reduzir deslocamento entre quadros.** Anatomia plausível vale mais que
uniformidade numérica. O golpe é um corte diagonal de cima para baixo, como nas vistas frontais, e
não um ataque lateral.

## Estágio C — a espada independente

A arma oficial é
`characters/orc-v1/source/combat-rescue-v5/combat/weapons/Sword/recruit-sword.png`
com o contrato em `weapon.json` (canvas 96×96, `grip` em `48,66`, uma mão, mão direita).

Para cada pose, defina e registre:

- ponto de contato da mão, ponto de contato do cabo, pivô da arma, orientação,
- trecho visível do cabo, atribuição de camada perto/longe, e requisitos de oclusão.

A arma tem de seguir o movimento real da mão daquela pose. Não a posicione por um centro de rotação
fixo qualquer.

Restrições de pixel art: nada de borda borrada, cor interpolada, halo branco, silhueta quebrada,
espessura de lâmina inconsistente ou conexão de cabo deformada. Rotação deve preservar a grade de
pixels. Se uma rotação ficar visivelmente inadequada, use uma apresentação da arma específica para a
perspectiva ou correção localizada no Aseprite — não crie um sistema de rigging.

## Estágio D — a pegada, que é o critério mais importante

O orc tem de **parecer** que está segurando a espada. Alinhamento de coordenada não é pegada: um cabo
que passa por cima de uma palma aberta está matematicamente alinhado e artisticamente errado.

Examine palma, colocação do cabo, sobreposição de dedos e luva, orientação do punho, continuidade do
antebraço, profundidade da arma e oclusão. Uma pequena sobreposição de mão ou dedo em primeiro plano
é aceitável quando necessária para comunicar que a luva fecha no cabo. A pegada tem de continuar
coerente entre as cinco poses, sem virar uma mão diferente em cada quadro.

## Estágio E — contorno claro e sombreamento

Para cada uma das cinco poses, produza **três renderizações separadas**:

- `body-only/NN.png` — só o corpo do orc, sem espada e sem sobreposição de arma.
- `weapon-only/NN.png` — só a arma com a transformação pretendida.
- `composite/NN.png` — corpo, arma e camadas de pegada/oclusão juntos.

Inspecione em cada uma: contorno branco ou pálido, pixel opaco perdido, contaminação de alfa,
máscara errada, brilho duplicado, cor de borda e desalinhamento de camada.

**Se aparecer artefato, ache a origem antes de corrigir**: ele nasceu no corpo, na arma ou na
composição? Localize quadro e região, aplique só a correção localizada justificada, e verifique que
não danificou sombreamento legítimo.

Proibido: escurecer o orc globalmente, trocar a paleta do personagem, esconder defeito com máscara
opaca grande. Se o defeito vier do corpo de origem e não puder ser corrigido com segurança, relate.

## Entrega

Em `experiments/main-orc-skeleton-02/stage-bcde/`:

1. `body-only/00.png`, `05.png`, `08.png`, `09.png`, `13.png`
2. `weapon-only/` com os mesmos índices
3. `composite/` com os mesmos índices
4. `attachment.json` — para cada pose, os pontos, pivô, orientação, camada e oclusão que você usou
5. `report.md` — a tabela anatômica do Estágio B, as decisões do Estágio C, a avaliação da pegada
   do Estágio D pose a pose, e a análise de artefato do Estágio E com a origem identificada
6. Recortes em 8× da mão e do punho de cada pose, em `evidence/`, porque é ali que o criador vai
   julgar a pegada

As fontes continuam editáveis e a procedência rastreável. Diga em cada imagem se ela foi composta
por script ou retocada no Aseprite.
