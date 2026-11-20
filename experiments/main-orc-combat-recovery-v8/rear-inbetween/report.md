# Sword traseiro — inserção local apex-descent

Status técnico: `TECHNICALLY_COMPLETE` no escopo final definido pelo criador. Status artístico: `VISUAL_REVIEW_REQUIRED`; `PENDING_CREATOR`.

## Arte e fontes

Entregas em `characters/orc-v1/source/combat-recovery-v8/rear-inbetween/back_r-sword` e `back_l-sword`.

Cada célula contém 14 quadros, quatro camadas independentes, PNGs compostos256, corpo nativo128, dois mestres Aseprite e strips. Novo F06 com plano explícito de ombro/cotovelo/palma, manga/cota construída em clusters e luva doadora da própria vista rearticulada no Aseprite. Arma independente ligada à palma. Autoria programática real no runtime Lua do Aseprite 1.3.18.6; zero chamadas de geração IA, sem edição raster externa ou crossfade.

As 13 poses herdadas são idênticas em RGBA, inclusive corpo, arma, luva, composição e nativo; `back_r` usa exclusivamente a fonte reconstruída `rear-fix/back_r-sword`. As fontes originais não foram editadas. Nenhuma duplicata consecutiva armada introduzida. Pixels claros de armadura preservados nos 13 quadros; novo quadro mantém contagem do ápice (back_r 0, back_l 9, luminância Rec.709 >=160).

Mestres salvos, fechados, reabertos e exportados. Verificação independente `verify.lua` reabre os dois mestres de cada célula e compara RGBA de todos os 14 compostos, 56 camadas e 14 nativos por direção, além dos tempos. Resultado em `saved-source-verification.json`.

## Medições da nova transição

| Direção | F05→F06 | F06→F07 |
|---|---:|---:|
| back_r | 36,37 px | 42,56 px |
| back_l | 31,22 px | 31,38 px |

Nova descida distinta dos vizinhos, com luva acompanhando a arma, sem cruzar o chão. Inspeção visual ampliada dos trios em `back_r-trio.png` e `back_l-trio.png`. Aprovação artística não concedida.

## Decisão final expressa do criador — aplicada

Grade final: **30,65,35,50,45,35,30,35,35,100,55,80,45,90**, total **730 ms**. O follow-through fica em **100 ms**, corrigindo a inconsistência da tabela original conforme decisão expressa do criador. Contato mantido em **F08 aos 325 ms**. Arma oculta em F00/F01/F12/F13, visível em F02–F11.

O passo **slash-release→contact de 59,96 px em back_r e 60,40 px em back_l ficou preservado de propósito**. Ele já existia antes desta rodada e está fora do alvo do retoque: corrigir o teleporte ápice→descida e seu vão vazio. O criador determinou explicitamente manter as treze poses herdadas intactas. Portanto, o máximo global permanece acima de 55 px e está registrado como exceção autorizada, sem alegar que a medição global passou nesse limite. As duas etapas da transição corrigida passam no limite de 55 px.

As duas células foram reexportadas dos mestres Aseprite salvos com a grade final. Os **172 arquivos PNG das duas células permaneceram byte-idênticos após o ajuste de duração**, incluindo os quadros novos. A verificação dos mestres reabertos confirma os 14 quadros, RGBA e durações, total de 730 ms em cada direção. Sem decisões pendentes para este escopo. Aprovação artística continua reservada ao criador.

Dados completos em `validation.json`; script de autoria e hash referenciados em cada `clip.json`, plano anatômico em `source/authorship.json`. Sem alterações em Axe, Unity, outras células, manifests de integração ou fontes de origem; sem commit.
