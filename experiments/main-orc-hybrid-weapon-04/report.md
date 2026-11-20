# Experimento 04 — duas espadas, mesmo corpo

Status: **TECHNICALLY_COMPLETE / VISUAL_REVIEW_REQUIRED / PENDING_CREATOR**.
Autoria programática Lua executada no Aseprite 1.3.18.6, composição offline; zero geração, zero PixelLab. Nenhum commit, integração Unity ou aprovação artística.

## Pergunta e Gate 0

Neste piloto, foi possível trocar a espada sem reconstruir corpo, braço ou mão: 14 quadros de corpo reutilizados por variante, zero quadros de corpo alterados e zero correções novas de pegada. A conclusão limita-se a estas duas espadas compatíveis e a `front_l/Sword`; não demonstra encaixe universal.

Gate 0 aceito exatamente como decidido pelo orquestrador: fonte `characters/orc-v1/source/combat-recovery-v8/frontal-inbetween/front_l-sword/clip.json`, 14 quadros, 730 ms, arma F02–F11, contato F08/325 ms. Fxx aqui é o índice zero-based do manifesto, não numeração humana do editor. As medições da escolha de direção são herdadas do brief; não foram apresentadas como nova medição deste autor.

## Fontes e variantes

- A: Espada do Recruta copiada do mestre declarado no brief para `variants/sword-a/sword.aseprite`, com PNG novamente exportado no Aseprite. A composição usa exatamente as camadas originais de arma e as recompõe no mestre isolado.
- B: `variants/sword-b/sword.aseprite`, fork da mesma espada, com camadas herdadas ocultas para procedência e camada visível nova. Apenas a lâmina y7..54 foi redesenhada no editor: perfil facetado, plano de aço azul claro, crista e fio de poucos valores com contorno escuro. Sem dither adicional, mantendo clusters sólidos na escala estreita da lâmina. Cabo, guarda e pomo y>=55 preservados pixel a pixel; canvas 96×96, pivô/contato (48,66), escala 1.
- `weapon-diff.json`: 106 pixels de diferença de silhueta; lâmina A/B com 48 px de extensão vertical, mudança de comprimento 0%. Não é apenas recoloração.
- `provenance.json` em cada variante registra fontes e hashes reais. `author.lua` contém todas as operações artísticas. Nenhuma edição raster externa produziu arte; `diagnose.mjs` apenas mede e amplia a prancha de revisão.

## Grip profile e composição

`grip-profile.json` registra mão direita anatômica, fontes, pivô, contato, posições/ângulos por quadro, tempos, contato e visibilidade. Ordem: `weaponBack → body → weaponFront → handFront`. A luva frontal original envolve/oculta o cabo, cujo trecho v60..70 permanece atrás do corpo segundo as máscaras herdadas. Guarda, pomo e lâmina ficam na frente conforme o original. B troca apenas a região da lâmina; não move cabo, guarda, mão ou punho e não cria overlay novo.

F06 conserva a transformação em dois passos inteiros herdada: lookup inverso da rotação adicional de −16° e lookup da arma de F05. Os demais quadros usam posição e ângulo do manifesto. Não há interpolação RGBA, cross-fade ou espelhamento do personagem.

## Stages A/B — inspeção antes do Stage C

Inspeção visual efetuada nos PNGs compostos e na prancha ampliada por nearest-neighbour `representative-review-2x.png`. Primeira linha A; segunda B; colunas F02/F08/F11.

| Quadro | Continuidade, pegada, orientação e oclusão | Resultado local |
|---|---|---|
| F02 preparação | Braço e luva mantêm cadeia contínua; cabo entra na luva; guarda fica acima da mão. Lâmina aponta para cima/direita nas duas variantes. | Sem problema grave novo observado; seguir. |
| F08 impacto | Antebraço cruza o tronco, luva sobre o cabo e guarda separa mão/lâmina. Espada aponta à esquerda em ambas. | Silhueta B distinta sem duplicar arma ou alterar punho; seguir. |
| F11 recuperação | Pegada baixa junto ao quadril, lâmina orientada à esquerda; luva, guarda e pomo mantêm relação original. | Mesma mão serve a A e B; seguir. |

Personagem, geometria corporal, armadura e identidade preservados. Transparência binária; a nova lâmina tem contorno escuro e planos claros internos, sem halo externo claro observado. Estes são juízos locais do autor, sem revisão independente adicional e sem aprovação do criador.

## Stage C e exportação

Após inspeção dos três representativos, foram compostos e salvos os 14 quadros completos de A/B, preservando a sequência de tempos `[30,65,35,50,45,35,30,35,35,100,55,80,45,90]` ms. Cada pasta `full/{a,b}/` contém mestre de quatro camadas, `body-only/`, `weapon-only/`, `composite/`, camadas individuais e tira de revisão. Os mesmos grupos existem em `representative/{a,b}/` para F02/F08/F11.

Exportação padrão existente executada sem modificar seu código: `export-pipeline.mjs` copia os módulos do pipeline e o bridge para uma raiz isolada `pipeline/`, pois o exportador fixa seus destinos em `dist/editor` e `tmp`. Assim todos os destinos ficam dentro deste experimento. `pipeline-result.json` registra **PASS**, build `pipeline/dist/editor/hybrid-weapon-04/822a6b68ef2b23b8a766/`, com preview, atlas, PNGs individuais, metadados, hashes e mestres. O pipeline valida 14 quadros, canvas 256×256, tempos e alfa binário. As exportações de camadas foram feitas no Aseprite reabrindo os mestres salvos, pelo mesmo método Lua da fonte.

## Corpo sem armas e diagnóstico de borda

A inspeção de `body-only` dos representativos não revelou lâmina/haste embutida; os detalhes claros visíveis são da armadura/luva herdadas. A escolha do corpo sem contaminação também integra o Gate 0 prévio. Identidade de hash isoladamente não é tratada como prova semântica de ausência de arma.

`pixel-diff.json` prova 28 comparações (14 quadros × body/handFront): igualdade dos bytes PNG A=B=fonte, além de RGBA decodificado. As duas variantes também preservam esses arquivos nos representativos. Pastas protegidas foram inventariadas antes da autoria e conferidas depois, sem arquivos alterados ou adicionados.

Inventário protegido: **22.556 arquivos**. `delivery-verification.json` acrescenta 40 checks: 12 comparações byte a byte dos representativos e 28 comparações dos pixels exportados pelo pipeline contra os compostos completos. Todas passaram. Arquivos `02.png`/`08.png`/`11.png` (e 00..13 no lote completo) são aliases byte-idênticos dos arquivos `Fxx.png`, para consumo pela página de revisão separada. `full/{a,b}/clip.json` explicita tempos e hashes dos compostos. `hashes.json` acompanha cada variante.

`edge-diagnostics.json` separa as evidências: A recomposta tem zero pixels diferentes da fonte em todos os quadros; B tem zero alfa parcial e zero pixels quase brancos neutros novos (limiar diagnóstico: menor canal >=225, amplitude RGB <=20). Armas ficam vazias em F00/F01/F12/F13. Corpo e luva não sofreram escurecimento global nem alteração de highlights.

- Herdado: contraste metálico forte, textura de armadura e oclusão densa da mão contra o tronco em F08; movimentos e eventuais limitações da coreografia original permanecem. Sem alegação de que este experimento corrigiu a animação fonte.
- Introduzido intencionalmente: silhueta facetada e aço mais claro da lâmina B. A rotação inteira produz degraus de pixel esperados na lâmina; não usa suavização alfa.
- Não observado: novo halo relevante, arma duplicada, reconstrução anatômica ou quebra nova de pegada nos representativos. O limiar numérico não substitui inspeção visual nem garante ausência de todo defeito possível.

## Métricas e limites

14 quadros de corpo únicos reutilizados, 28 instâncias de composição; corpo alterado **0**; quadros de luva alterados **0**; variantes entregues **2**, variante nova criada **1**; desenho específico de arma **1 lâmina**; ajustes específicos de encaixe para B **0**; correções novas de pegada **0**; chamadas PixelLab **0**; novas gerações **0**. Sem estimativa inventada de custo ou economia.

Inspeção estática dos representativos e tira completa realizada; player do pipeline entregue para avaliação contínua a 1× pelo criador. Não foi feita alegação de teste perceptual de playback contínuo nem de QA independente. Este piloto não altera outras direções/ações, `characters/`, `assets/`, `reports/` ou o projeto irmão. Documentação e próximos passos ficam aqui por determinação de confinamento do brief. Próximo marco: julgamento artístico explícito do criador; não promover automaticamente.

## Reprodução

Na raiz do repositório: `node experiments/main-orc-hybrid-weapon-04/run.mjs representative`; inspecionar os representativos antes de continuar; `node experiments/main-orc-hybrid-weapon-04/run.mjs full`; `node experiments/main-orc-hybrid-weapon-04/export-pipeline.mjs`; `node experiments/main-orc-hybrid-weapon-04/run.mjs verify`; `node experiments/main-orc-hybrid-weapon-04/diagnose.mjs`. O primeiro comando registra novo inventário protegido; não executar simultaneamente com autoria externa nessas pastas.
