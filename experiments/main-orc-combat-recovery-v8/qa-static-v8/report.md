# QA estático independente — Orc V1, candidato V8

**Veredito: NEEDS_FIX. Status artístico: ARTISTIC_REVISION_REQUIRED; PENDING_CREATOR.** Esta revisão estática não é aprovação artística e não avalia o movimento em reprodução. Inspecionei PNGs compostos reais e as camadas de armas, comparando os manifestos V7 e V8. Quadros são indexados a partir de 00.

| Objeção | Veredito | Evidência |
|---|---|---|
| O1 — back_l Sword lateral | PARCIALMENTE RESOLVIDA | Na projeção 2D a descida F05→F07 desloca o centroide de (159,6;60,8) para (193,8;154,2): Δx=34,2 e Δy=93,4 px no canvas 256. Predomina a componente vertical, mas há deslocamento lateral perceptível; F06–F10 mostram a espada estendida à direita. A coordenada de profundidade e a intenção de golpe para frente não são verificáveis pelo centroide 2D. Não considero a objeção inteiramente resolvida. |
| O2 — back_l Axe antinatural | NAO_VERIFICAVEL_POR_MEDICAO | F04→F06 passa de (161,0;56,1) a (181,2;156,2), Δx=20,2 e Δy=100,1; F05 desloca-se para (196,8;110,9). A descida é predominantemente vertical na tela com desvio lateral. F04 mostra braço dobrado elevado e F05 estendido; a naturalidade e a continuidade temporal não são demonstráveis por esse índice nem por quadros estáticos. Exigem revisão em reprodução. |
| O3 — back_r Axe pegada invertida | NAO_VERIFICAVEL_POR_MEDICAO | Inspecionado F06 `heavy-impact` e F05: o cabo segue para a direita e a luva escura está na junção com o antebraço. A resolução e a sobreposição não permitem distinguir com segurança polegar e palma para confirmar orientação overhand. Não há prova visual suficiente de correção da pegada. |
| O4 — front_l Sword axila | CONTINUA IGUAL AO V7 | Os manifestos apontam para o mesmo `combat-recovery-v7/frontal/front_l-Sword-full/clip.json`; nos 13 compostos houve **0 pixels RGBA alterados** entre V7 e V8. O manifesto menciona reparo anterior de 19 px no V7, não uma diferença V8−V7. A junção permanece escura em F03–F05; não consigo afirmar visualmente que o buraco ou chapa foi resolvido. |
| O5 — front_r Sword protegida | RESOLVIDA | Ambos apontam ao mesmo clip, SHA-256 `6809bfaaab103156f9a5bf4009e80e2c0f84df7f175a0430ab794f654c12d791`, e mesmo master, `e69cbcfb320e5f1a2ab9e7f07027f71a2d92f5c5383bcaad9e6f44854ac78431`. Os 13 PNGs compostos têm hashes idênticos e 0 diferenças RGBA. Isso prova preservação em relação ao V7, não aprovação da pose. |
| O6 — flash branco espada traseira | RESOLVIDA NO ESCOPO ESTÁTICO | Em ambas as vistas, F02 é o primeiro quadro armado e F10 o último; inspecionei os quatro compostos e camadas `weaponBack`/`weaponFront`. Não vi brilho branco anormal na entrada ou saída. Nessas camadas há 0 pixels com R, G e B simultaneamente ≥230 nos quatro quadros. Esse limiar é apenas evidência complementar, não prova de ausência de flash temporal em todos os monitores. |

## Medições reproduzíveis

Centroides em pixels do canvas 256×256, origem no canto superior esquerdo, eixo y para baixo. União das máscaras alfa não zero de `weaponBack` e `weaponFront`, sem `handFront`; o centroide inclui cabo e lâmina e pode variar com rotação e oclusão. `—` significa arma ausente. Estes números descrevem posição na tela, não profundidade, intenção ou naturalidade.

| F | back_l Sword (x,y) | back_l Axe (x,y) |
|---|---|---|
| 00 | — | — |
| 01 | — | — |
| 02 | 181,3; 100,6 | 187,1; 103,2 |
| 03 | 181,5; 76,5 | 190,8; 87,4 |
| 04 | 165,7; 66,3 | 161,0; 56,1 |
| 05 | 159,6; 60,8 | 196,8; 110,9 |
| 06 | 194,0; 102,8 | 181,2; 156,2 |
| 07 | 193,8; 154,2 | 172,2; 159,8 |
| 08 | 182,0; 164,5 | 181,8; 147,1 |
| 09 | 180,2; 156,2 | — |
| 10 | 180,3; 146,5 | — |
| 11 | — | — |
| 12 | — | não existe |

## Prioridades para entrega

1. **O4:** reavaliar e corrigir se necessário a axila frontal esquerda, preservada sem alteração em relação ao V7 rejeitado; apresentar evidência visual da junção.
2. **O3:** tornar a orientação da pegada de back_r Axe legível e verificar polegar, palma e cabo no contato.
3. **O1/O2:** revisar a direção do golpe e a anatomia em animação à escala e velocidade de jogo; corrigir se a travessia lateral ou movimento antinatural persistirem. A inspeção estática não resolve a profundidade nem o gosto do criador.

As folhas de contato nesta pasta são derivados de revisão dos PNGs compostos; não alteram a arte. Nenhuma edição em `characters/`, Unity ou commit foi realizada.
