# Orc V1 — reconstrução traseira isolada, 2026-10-29

**ARTISTIC_REVISION_REQUIRED. Pedido artístico amplo não concluído.
Pacote apenas diagnóstico, sem elegibilidade de integração. PENDING_CREATOR.**

[Abrir a demonstração diagnóstica principal](../../Biblioteca%20de%20Arte/Estudos%20Comparativos/Orc%20principal%20-%20Reconstrucao%20traseira/index.html)
· [handoff do produtor](dev/report.md)
· [manifesto isolado](../../characters/orc-v1/source/rear-reconstruction-v4/candidate28manifest.json)
· [parecer independente](qa/report.md)
· [alternativa isolada também rejeitada](specialist/report.md).

## Escopo e preservação

Pedido: reconstruir coreografia traseira de Sword/Axe e Unarmed afetado,
melhorar pegada e armas independentes, corrigir Defeat frontal e sombreado
local de Walk. Preservar Idle/Hit, movimento frontal satisfatório e Defeat
traseiro; armas somente durante Attack. Sem Unity, commits, promoção ou novas
gerações pagas.

O repositório já continha alterações não commitadas e candidatos anteriores.
O inventário [input-preservation.json](input-preservation.json) registra
2.939 arquivos existentes de Orc V1, armas iniciais e autoridade de identidade.
A candidata nova está excluída desse inventário. A [verificação posterior](input-preservation-result.json)
conferiu os 2.939 arquivos: **PASS, zero alterações/ausências**. Não é uma
auditoria histórica de todos os arquivos da máquina.

## Equipe desta execução

| Papel | Modelo/provedor | Agent ID | Responsabilidade | Motivo da escolha | Resultado |
|---|---|---|---|---|---|
| DEV principal | GPT Sol 6.1 / Codex, high | `47326bab-8340-4fa3-ac11-62616a07654b` | Diagnóstico, keyposes e produção Aseprite isolada; depois fechamento do parcial do especialista | Coreografia e pegada já falharam em várias tentativas; especialidade exige raciocínio mais forte. Retomar contexto existente economizou uma terceira sessão DEV | Finalizou refinamentos locais; rejeitou o próprio estudo. Depois executou uma vez o script alternativo preparado e congelou outro estudo rejeitado, sem propagação |
| DEV especialista | Claude Sonnet 5.5 / Antigravity, high | `5e06cf9c-9b4a-4169-a234-257a6142cc12` | Alternativa estreita: uma keypose de Axe traseiro, em fontes próprias | A primeira montagem não resolveu cotovelo/torso; testar uma interpretação artística diferente, não repetir offsets nem delegar novamente a biblioteca inteira | Interrompido por cota individual (`Individual quota reached`, reset informado em 132h10m49s); scripts parciais preservados, restante redistribuído ao DEV principal |
| QA — primeira tentativa | GLM 5.3 / Cline GLM API | `52f87102-89d7-44f5-a4dd-f445d3e163b1` | Revisão independente integrada | Primeira escolha obrigatória do pedido | Falha ACP: `A foreground turn is already active`; status `error`, sem parecer utilizável ou permissões pendentes |
| QA — fallback | Grok 4.7 / GitHub Copilot | `d13ab881-7b1f-4fa6-a6af-64017deb0da3` | Revisão da mesma entrega e ferramentas/documentação, incluindo adendo | Segunda escolha obrigatória após falha real do GLM, sem nova tentativa idêntica | Integridade diagnóstica PASS, tarefa artística FAIL, percepção contínua NOT_VERIFIED. Re-revisão fechou o achado de apresentação com 4/4 unittest e 21/21 Chromium; sem aprovação artística |

**2 DEVs distintos; 2 sessões de QA, incluindo a tentativa falha.** Nenhum QA
foi criado dentro do DEV. Sessões históricas lidas para contexto não foram
retomadas nem contam como agentes desta execução. Os timeouts do comando de
espera do produtor não eram falhas do produtor: seu estado permaneceu em execução
e o trabalho não foi duplicado.

A retomada do DEV principal para fechar os scripts parciais do especialista não
é um terceiro DEV: mesma sessão, contexto retido, somente trabalho remanescente,
sem escrita no freeze já revisado.

Todos os produtores/revisores terminaram `idle` ou `error`, sem turno ativo.
Não ficou servidor ou monitor de espera em segundo plano.

## Entrega material e limite artístico

- 28 clipes / 210 quadros acessíveis: oito clipes armados derivados (82 quadros)
  e 20 aliases exatos da entrada (128 quadros). Quatro frontais são candidatos
  locais de materiais; quatro traseiros permanecem em revisão artística.
- Machado independente: 346 posições RGBA refinadas; espada: 100. Canvas,
  silhueta alfa, dimensão e encaixe originais preservados. São retoques
  programáticos no Aseprite sobre arte herdada, não geração nova nem desenho
  manual declarado.
- Contorno da coroa `back_r`: 83 substituições por clipe Sword/Axe (166
  frame-pixels), em coordenadas explicitamente traçadas. Os 19 pontos de F04
  examinados já estavam no bruto gerado; não eram interpolação do preview.
  Nenhuma generalização para os demais highlights.
- 82 quadros com fontes/exports/camadas/tempos próprios. O estudo de reconstrução
  F04 está preservado como **rejeitado e excluído**, pois afina o cotovelo e
  introduz uma trajetória descendente que volta a subir no vizinho.
- Confirmado: os oito corpos de `back_r` Sword/Axe são idênticos no pai.
  Trocar arma/ângulo sobre esse ciclo não demonstrou técnicas distintas.
- Unarmed, Defeat frontal e Walk não receberam correções especulativas nesta
  rodada. O relato de mão sumindo/flicker não foi localizado temporalmente; a
  aparência terminal de Defeat continua dependente de avaliação visual.
- Idle/Hit e fontes anteriores preservados. Nenhuma seleção de produção ou
  receita foi promovida. O sufixo do passe não restaura o personagem Orc V4.

### Segunda abordagem e encerramento do bloqueio

O especialista produziu `iter01`/`iter02` antes da cota. O DEV principal retomou
somente o restante: uma execução Aseprite com os parâmetros preparados, fonte
salva reaberta e exports do estudo nativo 128×128, um quadro de 80 ms. A
recuperação reproduziu `iter02` com **zero diferenças RGBA**; não inventou uma
terceira anatomia.

A [comparação com F04/F05/F06](specialist/recovery/pose-vs-neighbors.png)
continua sem pegada convincente; `handFront` e retoques de costura estão vazios
nos parâmetros recebidos. Torso/peso também não ficaram estabelecidos.
**Alternativa rejeitada localmente, fora da matriz e sem QA artístico próprio.**
84 artefatos parciais e 761 arquivos do freeze diagnóstico original permaneceram
idênticos. [Freeze do estudo](specialist/version-freeze.json):
`b42d5c9419eb167b2dd390fe9468026d03c133f26a42ebb7591a0b116db33e37`.

O bloqueio final é artístico e específico: duas abordagens locais não
estabeleceram chaves válidas de golpe/torso/pegada para propagação segura, e o
especialista foi interrompido por cota durante a segunda abordagem. Isso **não
prova inexistência de solução**, nem ausência de autorização para reautorar.
Continuar repetindo o mesmo tipo de montagem não seria uma entrega correta.
As correções amplas pedidas permanecem pendentes; não há promoção automática.

## Trabalho direto do orquestrador

- Leitura dos dois anexos e identificação de versões/limites.
- Consulta do Paseo via CLI e MCP, confirmação de Aseprite e doctor.
- Coordenação de um único produtor para evitar edições concorrentes.
- Integração pontual do construtor de revisão: baseline explícita, versão e
  relatório corretos, fontes candidatas de armas, comparação antes/depois das
  armas, matriz de exatamente 28 células e ausência de selo técnico automático.
- Parametrização do teste Chromium para uma página isolada.
- Atualização de orientações de receitas sobre luminância versus halo e contato
  numérico versus mão anatomicamente convincente.

Essas alterações pequenas de integração foram executadas diretamente para não
abrir outro DEV nem duplicar contexto de produção artística.

## Verificações já executadas

| Verificação | Resultado | Limite |
|---|---|---|
| `editor-check` | AVAILABLE, Aseprite 1.3.18.6, batch | Disponibilidade não comprova qualidade |
| `doctor` | Sem erros de referência | Nenhuma geração de arte |
| Node: `main-orc-complete` + `test_declared_hashes` | 7/7 PASS sobre entrada anterior | Nomes/métricas artísticas dos testes não comprovam aparência |
| Unittest do construtor | 4/4 PASS | Matriz exata, baseline declarada com pixels copiados e arma candidata selecionada |
| Chromium na página anterior | 20/20 PASS | Relógio, seleção, imagens, escala e hold |
| Build isolado em diretório temporário + Chromium com flags | 20/20 PASS | Testa ferramenta, não a arte nova |
| Página diagnóstica real, com os novos exports | 20/20 Chromium PASS; 770 arquivos copiados | 28 células, oito comparações de clipes, armas antes/depois, 1×/0,5×, passo, terminal; sem aprovação artística |
| Apresentação corrigida após QA | 21/21 Chromium PASS e 4/4 unittest PASS | Aviso explícito de `eligibleForIntegration=false` na página/catálogo; registro herdado de rejeição rotulado com versão/escopo |
| Regressão final do construtor | 4/4 PASS | Após remoção de alegação genérica de anatomia correta |
| Preservação de entradas | 2.939/2.939 PASS | Escopo exato no inventário |

O construtor indexa 770 cópias/derivados; o diretório da página contém **775
arquivos**, incluindo dois `weapon.json` gerados e os três arquivos de página,
catálogo e manifesto. Não são 770 arquivos totais.

## Confronto com o aceite e achados independentes

| Requisito | Evidência independente | Resultado |
|---|---|---|
| Sword/Axe traseiros naturais e distintos | Corpos `back_r` idênticos; chaves novas não aceitas; torso pouco participante | FAIL |
| Pegada natural | `handFront` preservado, cabo sem fechamento convincente dos dedos | FAIL |
| Corpo desarmado / ataque-only sem resíduos | Overlays ocultos fora do intervalo; lâmina/disco ainda presentes no corpo `back_l/Sword` F01/F07 | PASS estrutural dos overlays; FAIL semântico do corpo |
| Materiais e independência dos itens | Reexportação independente no Aseprite bate com PNG; alfa/96×96/grip preservados | PASS parcial de materiais, não de pegada |
| Unarmed | Aliases preservados; rigidez traseira permanece; mão frontal sumindo não localizada temporalmente | FAIL traseiro; NOT_VERIFIED no desaparecimento relatado |
| Defeat frontal e mão | Terminal estático já lê caído segundo QA; queda/borrão não confirmados em reprodução contínua | PASS estático; NOT_VERIFIED temporal |
| Walk | Locomoção/tempos preservados; nenhuma correção de flicker demonstrada | PASS preservação; FAIL da correção, localização temporal NOT_VERIFIED |
| Halo | Coroa `back_r` corrigida localmente; faixa clara em `back_l/Sword` F05 e filamento em Axe F02 persistem | PASS local; FAIL da solução geral |
| Idle/Hit e rear Defeat | Aliases e dependências preservados, conferidos por hash | PASS |
| Página revisável | Controles, 28 células, oito comparações, imagens reais, hold | PASS funcional; fluidez artística em 1× NOT_VERIFIED |

O QA localizou os defeitos nos próprios arquivos e reexportou os dois itens
independentes; não dependeu exclusivamente do relatório do DEV. A conclusão
ampla é **FAIL artístico**, não uma aprovação condicional.

Achados de apresentação corrigidos pelo orquestrador: o relatório agora liga o
parecer real; a página e o catálogo exibem ineligibilidade explícita; o link
herdado de rejeição foi rotulado como registro cujo escopo/versão precisam ser
conferidos, sem fingir ser o estudo F04 atual. Nenhuma correção artística foi
simulada para encerrar o QA.

A ferramenta de testes da IDE não descobriu os testes Node; foram executados
diretamente pelo runner existente. O alias `python` do sistema não executou;
foi usado o ambiente já instalado `tmp/pixel-venv/Scripts/python.exe`, sem
instalação de dependências.

## Custos e evidências

Nenhuma chamada PixelLab iniciada pelo orquestrador; o contrato do DEV proíbe
novas gerações. Não há total verificado de tokens/custo monetário nesta etapa.
Disponibilidade de provedor no catálogo não garante cota de execução; eventuais
falhas e substituições devem ser registradas após ocorrerem.

O [freeze do produtor](dev/version-freeze.json) tem SHA-256
`8f3c0be13e2b6e7d7f3ff4a33807cc1a4cb5519602d1f589d24194808ad49c44`.
O estudo parcial foi fechado pelo DEV principal e permanece fora da matriz.
A re-revisão pelo mesmo QA fechou o achado de apresentação; a arte continua FAIL.
Nenhum teste de relógio ou inspeção estática aqui equivale a percepção contínua
da fluidez em 1×.

## Resumo das alterações e situação final

As alterações anteriores não commitadas foram mantidas, sem atribuí-las a esta
execução. Superfícies alteradas diretamente pelo orquestrador: um construtor,
dois arquivos de teste e quatro documentos (`ASEPRITE`, `RECIPES`,
`MAIN_ORC_COMBAT_POLISH`, `ROADMAP`). Novos diretórios isolam fontes/exports,
estudos rejeitados, evidências de QA e a página diagnóstica. Não houve commit,
limpeza destrutiva, restauração de V4, integração Unity ou aprovação do criador.

O próximo passo artístico exige uma solução convincente para chaves traseiras
antes de produzir intermediários. A entrega atual serve para inspecionar
materiais locais e os defeitos ainda presentes; **não atende ao aceite completo
do pedido original**.
