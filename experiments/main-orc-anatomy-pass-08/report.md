# Passe anatômico experimental — 08

Status técnico: `TECHNICALLY_COMPLETE`. Status artístico: `VISUAL_REVIEW_REQUIRED`. Candidato experimental de um quadro; sem aprovação artística ou promoção.

## Resultado e leitura

O antebraço passa a descer a partir do cotovelo, em vez de prolongar a linha quase horizontal do braço. Na inspeção do quadro isolado em 1× e 4×, a cadeia tem leitura descendente; a mão fica abaixo do cotovelo. O rosto, a cabeça, a ombreira metálica, o tronco e o restante do indivíduo foram preservados. A validação de pixels é técnica e não substitui o julgamento do criador sobre a força do corte.

## Juntas e proporções

Coordenadas em pixels do canvas 256×256, origem superior esquerda, y positivo para baixo. Juntas são marcos anatômicos estimados visualmente, não pontos inferidos automaticamente de um rig. Os valores anteriores usam o diagnóstico do brief.

| Marco | Antes | Depois |
|---|---|---|
| Ombro | (147,112) | (147,112) |
| Cotovelo | (168,120) | (166,124) |
| Pulso | (181,125) | (173,136) |
| Contato da mão | (178,131) | **(167,140)** |

| Segmento projetado | Antes | Depois | Diferença |
|---|---:|---:|---:|
| Úmero, ombro–cotovelo | 22,472 px | 22,472 px | 0% |
| Antebraço, cotovelo–pulso | 13,928 px | 13,892 px | −0,26% |

Ângulo do úmero com a horizontal: 20,85° → 32,28°. Ângulo do antebraço: 21,04° → 59,74°. A mão desloca o ponto de contato em (−11,+9), distância de 14,21 px. Esse deslocamento permite a descida preservando os comprimentos; não é proposta de binding de arma validado. A espada ficou integralmente fora do passe. A composição posterior deverá usar (167,140) como contato candidato e verificar a pegada visualmente.

## Autoria e fontes

Autoria **programática Lua executada no Aseprite 1.3.18.6**, registrada em `author.lua`, em perfil batch isolado `batch-profile/`, com `--batch --noinapp`, processo oculto. Não é desenho manual nem geração de IA. A fonte única de pixels foi `../main-orc-skeleton-02/stage-bcde/body-only/08.png`. Os quadros 05 e 09 foram consultados visualmente, sem colagem. Os JSONs de movimento foram lidos apenas como contexto.

O método rearticula separadamente os dois segmentos do próprio 08, por amostragem inteira de vizinho mais próximo, sem escala, blur, mistura de cores ou interpolação entre quadros. O ponto do cotovelo é o pivô da região distal; a união é resolvida por sobreposição de um pixel entre as máscaras. Não houve redesenho global, espelhamento ou transformação do corpo inteiro.

O mestre final contém **um quadro e uma camada de corpo**, sem espada. O carregamento final usa `Image{fromFile=...}` para impedir a abertura automática de sequência numérica do Aseprite. O mestre foi reaberto e exportado; seus pixels RGBA coincidem integralmente com o PNG candidato.

## Escopo e validação

**As mudanças ficaram limitadas ao braço direito e à junção indispensável do ombro.** A ombreira metálica foi preservada; a região móvel começa sob ela. O contorno escuro foi mantido como linguagem e paleta do membro; sua posição acompanha a nova articulação. O contorno externo do restante do corpo é idêntico.

Foram alterados 648 pixels, todos em x=147..185 e y=111..144. A máscara de autorização testada foi x=147..188, y=111..148; **zero pixels alterados fora dela**. Os demais 64.888 pixels conservam os mesmos bytes RGBA decodificados, inclusive os pixels transparentes. A identidade aqui se refere a pixels decodificados: o arquivo PNG inteiro necessariamente recebe outra codificação após exportação.

Nenhuma cor RGBA nova. Nenhuma mudança em `characters/`, `assets/`, `reports/`, nas fontes stage-bcde ou em `../TacticsRPG`. Nenhum commit. Zero chamadas ao PixelLab ou a qualquer gerador. Todos os arquivos escritos por este passe ficam nesta pasta experimental. `audit-diff.mjs`, encontrado durante a execução, foi preservado sem alteração e não foi usado como prova de anatomia.

As três caixas disjuntas em `pixel-diff.json` cobrem faixas de y para contabilização, incluindo a posição antiga apagada e a posição nova; seus rótulos não são segmentação anatômica exata. Contagens: 268 + 197 + 183 = 648 pixels. `changed-regions.png` marca essas caixas sobre o candidato. `before-after.png` contém os quadros completos lado a lado em 1× e 4×, sem alterar os pixels da arte.

Hashes SHA-256 reais de entrada, PNG, mestre e Lua estão em `pixel-diff.json`. Verificações reproduzíveis de escopo, paleta e roundtrip: `verify-and-preview.py`. Os previews foram montados externamente apenas para comparação; toda alteração artística e exportação do candidato ocorreu no Aseprite.

## Entrega

- `candidate-08.png`
- `master-08.aseprite`
- `before-after.png`
- `changed-regions.png`
- `report.md`
- `pixel-diff.json`
