# Passe anatômico 08b

Status técnico: `TECHNICALLY_COMPLETE`. Status artístico: `VISUAL_REVIEW_REQUIRED`, pendente do criador.

## Fonte e autoria

Base exclusiva: `../main-orc-skeleton-02/stage-bcde/body-only/08.png`. O candidato rejeitado foi consultado apenas nas imagens de diagnóstico, nunca como base. Zero PixelLab, geração, espada, espelhamento, interpolação ou rotação de segmentos.

Autoria por clusters explicitamente desenhados via `author.lua`, executado no runtime do Aseprite 1.3.18.6. É autoria programática local no editor, não desenho com mouse. O script apaga o membro livre original sob a ombreira e desenha nova silhueta, massas de manga vermelha, cota, cotoveleira, braçadeira, punho e dedos. Não amostra ou transforma segmentos de outras poses. As cores são selecionadas da paleta existente do quadro. Python somente mede, verifica e monta as apresentações.

## Construção

A silhueta foi desenhada como uma massa contínua da junção (147,111) até o punho, com cotovelo em torno de (163,130). Os clusters de cota assentam sobre uma sombra comum; a cotoveleira sobrepõe a manga e entra na braçadeira sem conector fino. A braçadeira usa plano escuro, crista cinza e luz curta; a luva tem massa fechada, polegar lateral e separação escura dos dedos. A direção dominante desce para a direita. A ombreira acima de y111 permanece original.

Pivô de contato adotado: **(174,148)**, coordenadas do canvas 256, origem superior esquerda, índice zero. É ponto proposto na mão fechada, não binding de espada validado.

## Espessura e referências

Medições diagnósticas por seção aproximadamente perpendicular à direção local, em pixels do canvas 256; não são objetivo de comprimento nem prova de anatomia. Centros, tangentes e resultados brutos estão em `measurements.json`.

| Trecho | 08b | Referência útil |
|---|---:|---|
| Braço superior, centro (155,120) | 13,0 px | cota e manga do braço esquerdo do 08, comparação visual em 8× |
| Cotovelo, centro (163,130) | 13,2 px | dobra e sobreposição de placas nos quadros 05/09 |
| Antebraço, centro (171,139) | 14,8 px | esquerdo 08: 16,0 px; direito 09: 15,8 px |
| Punho/mão, centro (174,147) | 14,0 px | mão esquerda 08: 14,0 px |

As sondas brutas `08 esquerdo superior` (34,2) e `05 direito antebraco` (31,5) atravessam massas adjacentes e **não são medidas válidas isoladas do membro**. Estão preservadas para transparência, excluídas da comparação quantitativa. O 05 foi referência visual de luva fechada e articulação, não doador. Não confundir os 21–23 px horizontais descritos no brief com seções perpendiculares de uma pose diferente.

## Verificação e limites

- Candidato único RGBA, body-only, 256×256.
- Mestre salvo, fechado e reaberto no Aseprite; `master-roundtrip.png` idêntico em RGBA ao candidato.
- 928 pixels modificados; 64.608 pixels preservados exatamente, incluindo os quatro bytes RGBA de todos os pixels fora da máscara [147,111,188,151].
- Zero alterações fora do braço/junção, zero cores novas. Cabeça, rosto, ombreira superior, torso, cinto, pernas e botas preservados.
- Hashes e caixas inclusivas por trecho em `pixel-diff.json`. A igualdade externa é dos bytes RGBA decodificados; o PNG candidato tem nova codificação e não é arquivo byte-idêntico ao PNG fonte.
- Nenhuma escrita em `characters/`, `assets/`, `reports/` ou Unity; nenhum commit. Todas as saídas deste passe estão nesta pasta.

Inspecionei `before-after.png` em 1× e 8× e `comparison.png`. O vale estreito desapareceu e a mão está conectada à braçadeira. O conjunto tem leitura diagonal contínua em 1×. Há uma limitação artística: a nova braçadeira tem planos mais simples e o membro está mais estendido que o esquerdo; equivalência de acabamento e naturalidade do golpe exigem julgamento do criador. Não declaro aprovação artística por essa verificação técnica.

## Entrega

`candidate-08b.png`, `master-08b.aseprite`, `before-after.png` (1× e detalhes 8× lado a lado), `comparison.png` (08b e três referências em 8×), `changed-regions.png` (pixels alterados em laranja), `pixel-diff.json` e este relatório. `author.lua`, `verify.py` e `measure.py` preservam a procedência e permitem auditar autoria e verificação.
