# Orc V1 — resgate de combate v5, retomada de 29/10/2026

**EM PRODUÇÃO. Este registro não declara a tarefa concluída nem aprova arte.**

O criador solicitou retomar a tarefa inteira e rejeitou o encerramento anterior
em diagnóstico. A nova [autorização](authorization.json) permite usar o saldo
PixelLab conforme necessário, com inspeção representativa antes de ampliar lotes,
sem compra de créditos ou alteração de assinatura. A fonte continua no Aseprite;
Unity e aprovação artística automática continuam fora do escopo.

## Mudança de estratégia

Reautorar movimentos corporais coerentes com auxílio do PixelLab onde as chaves
anteriores não sustentam o golpe, em vez de repetir colagens de membros,
shears/offsets e oclusão sobre o ciclo rejeitado. Espada, machado e soco têm
técnicas próprias; o corpo deve estar realmente desarmado com equipamento
desligado. Retoques de Walk/Defeat têm proprietário separado e não regeneram
locomoção válida.

O pai é o manifesto diagnóstico `rear-reconstruction-v4`, preservando seus
refinamentos úteis de materiais e contorno. O [inventário de entrada](input-preservation.json)
protege 3.506 arquivos existentes. Os sete testes de contratos anteriores
passaram antes da nova produção; não são aprovação da arte nova.

## Sessões desta retomada

| Papel | Modelo/provedor | Agent ID | Motivo / resultado |
|---|---|---|---|
| DEV combate — tentativa inicial | Gemini 4 Argon High / Antigravity | `61c48dc0-3237-4b2b-bfdd-8375faf2b654` | Escolha especializada fora do Copilot; falhou na leitura inicial por cota individual, reset informado em 82h46m40s; sem produção a duplicar |
| DEV combate — fallback | Gemini 4 Argon / GitHub Copilot | `936fc94f-aaa9-406c-9326-546a1a95409c` | Mesmo modelo artístico em outra cota, após confirmação de erro e ausência de turno ativo do anterior; 12 clipes entregues, aguardando QA |
| DEV localizado | Nemotron 3.5 Super VL Free / OpenCode Free | `d7cef932-b882-4f5b-a6d1-b70bf6c15af7` | Modelo gratuito para sombreado localizado de Walk e inspeção de Defeat; fonte composta e tempos corrigidos após bloqueios de integração |
| QA independente — primeira escolha | GLM 5.3 / Cline GLM API | `76797f0a-7d99-41fc-8e1c-638dce10a345` | Produziu análise técnica parcial; voltou a idle ao abrir PNG e novamente após retomada, sem parecer persistente/erro explícito. Sem turno ou permissão pendente antes do fallback |
| QA independente — retomada limpa solicitada | GLM 5.3 / Cline GLM API | `8772a08a-d05a-4d5c-b935-7dfa52b7e197` | Contexto anterior não respondeu novamente; sessão limpa passou teste textual de leitura/hash/gravação antes de receber inspeção de uma imagem F06 |
| QA independente — fallback | Grok 4.7 / Copilot | `d13ab881-7b1f-4fa6-a6af-64017deb0da3` | Mesma sessão QA anterior, contexto preservado; retomada especificamente para julgar o novo freeze V5, sem repetir produção |
| DEV especialista de grip — escalonamento obrigatório | GPT 6.1 Sol / Codex | `47326bab-8340-4fa3-ac11-62616a07654b` | Sessão anterior reutilizada pelo conhecimento de Aseprite/itens; especialidade transferida após a segunda reprovação da mesma pegada Argon. Diretórios próprios `grip-specialist`, sem tocar o DEV de corpo |
| DEV especialista corporal — escalonamento obrigatório | GPT 6.1 Sol / Codex | `950ff800-e30a-4a9a-9e5c-6917ed2f05c6` | Transferência após segunda reprovação corporal Argon; somente três chaves estruturais `back_r/Axe` antes de ampliar; diretórios próprios `body-specialist` |

Fontes de cada DEV estão isoladas; nenhum possui a matriz global ou escreve
na área do outro. O orquestrador assume integração, validações e documentação.
Nenhum QA foi criado dentro do DEV. QA independente será sobre a versão
integrada real, na ordem de provedores solicitada; achados retornam ao produtor.

## Produção efetiva e integração

O [DEV combate](combat/report.md) entregou 12 clipes/102 quadros: quatro
corpos traseiros distintos de espada/machado, dois ciclos traseiros de soco,
recoil F03 dos dois Unarmed frontais e novas camadas de pegada nos oito
clipes com arma. As quatro coreografias corporais frontais de espada/machado
foram preservadas. A existência de poses distintas ou maior máscara de mão
não prova naturalidade; o QA deve julgar a anatomia, o peso e a continuidade.

O [DEV localizado](localized/report.md) aplicou 2.741 alterações de cor em
F04–F07 de `back_l/Walk`, sem alterar alfa ou tempos, e manteve os demais
Walk/Defeat após inspeção. Cópia entre pixels opacos, bbox semelhante,
alfa binário e ausência de brilho **não provam** correspondência material,
ausência de borrão ou correção perceptual. Essas conclusões foram
explicitamente limitadas antes do QA.

O [integrador](integrate.mjs) constrói uma matriz limpa de 28 células sem
herdar aprovações, hashes antigos ou evidências rejeitadas do pai. São
13 candidatos/110 quadros e 15 aliases exatos/100 quadros, total 210.
Idle/Hit e Defeat traseiro permanecem aliases protegidos.
O [validador](validate.mjs) confere fontes/cabeçalhos/tempos, hashes,
recomposição das quatro camadas, recorte nativo e conteúdo das tiras.
Esses testes **não certificam** ausência semântica de armas no corpo,
pegada ou coreografia.

Para a futura entrega dos especialistas, o integrador aceita
`--weapon-patch <manifesto>` e exige oito clipes completos Sword/Axe, sem
duplicatas, com pai e hashes reais. Nesse modo substitui explicitamente as
oito entradas armadas antigas, preservando os quatro Unarmed e o Walk
localizado. `--output <arquivo>` permite validar fora da matriz publicada.
Os quatro testes de integração passaram, incluindo rejeição de patch incompleto,
duplicado, hash desatualizado e três chaves corporais sem ataque equipado.
Também são exigidos os quatro layers e arma oculta antes/depois da ação.
Isso prepara o contrato; nenhum protótipo foi
integrado e a matriz publicada continua em revisão.

A integração detectou e devolveu ao DEV localizado dois erros reais:
hash incorreto do manifesto pai, corrigido por SHA256 do arquivo real;
e mestre declarado composto256 mas salvo nativo128, exigindo mestre
composto separado. Na criação desse mestre, `Frame.duration=160`
foi corrigido para `0.160` segundos no Lua, evitando saturação em
65.535 ms (65,535 s). Nenhum teste foi afrouxado para aceitar a divergência.

### Primeira revisão independente e ciclo corretivo

O [parecer Grok](qa-grok/report.md) e seu [resultado estruturado](qa-grok/qa-result.json)
reprovaram o freeze `00281c86…`, preservado integralmente no
[manifesto rejeitado](qa5-rejected-manifest.json). Não foi promovido.

| Achado | Evidência independente | Encaminhamento |
|---|---|---|
| QA5-01 HIGH, pegada nos oito clipes | `handFront` é carimbo que flutua ou não liga ao antebraço; área e contato de um pixel não comprovam mão | Posicionar a arma pela palma/pulso reais em cada pose; oclusão e anatomia reais, não máscara parametrizada |
| QA5-02 HIGH, quatro corpos traseiros armados | Coluna da mão inativa é cópia F00, quadril/pernas não sustentam o peso | Remover a colagem/congelamento; reautorar movimento corporal e apoios, não só arco de braço |
| QA5-03 MEDIUM, dominância traseira | `back_l` foi produzido canhoto e `back_r` destro | Corrigir a cadeia anatômica dominante nas fontes, sem espelhar ou trocar apenas o rótulo |

O mesmo DEV retomou correções em `combat/qa5-repair1/`, preservando
as fontes/exportações rejeitadas. Primeiro marco: `back_r/Axe`
corpo/pegada e `front_r/Sword` apenas pegada, para o MESMO QA julgar
antes de expandir. Não encerrar novamente em diagnóstico.

O [re-QA estreito de pegada](qa-grok/representative-front-grip.json)
também reprovou o clip `qa5-repair1/front_r/Sword`
(`27b7574e…`): F06 continua com espada no peito e punho abaixo.
Não houve propagação. Conforme escalonamento obrigatório do pedido original,
Sol/Codex assumiu a especialidade, começando pela anatomia real de F06,
em fonte nova isolada. O [parecer do F06 Sol](qa-grok/representative-sol-F06.json)
aceitou esse quadro para explorar as próximas chaves, não os oito clipes.
O próprio QA corrigiu sua interpretação anterior: o braço ativo cruza o peito;
o punho baixo é inativo. O cabo agora fica sob a luva autêntica, com guarda e
pomo legíveis. O especialista recebeu somente F02/F08 como próximo lote,
sem autorização de propagar a matriz inteira.

O [re-QA corporal](qa-grok/representative-axe-body.json) também reprovou a
segunda tentativa Argon: mão inativa e recuperação melhoraram, mas o conjunto
ainda descreve corte lateral, sem descida pesada e entrega do tronco no impacto.
Essa especialidade também foi transferida para Sol/Codex em sessão própria,
começando por três chaves `back_r/Axe`. Argon não continua nenhuma das duas
especialidades criativas. As tentativas rejeitadas permanecem preservadas.

### Próximo QA: nova tentativa GLM 5.3

O criador informou que os tokens Copilot estão acabando e pediu explicitamente
tentar GLM 5.3 novamente no próximo QA. A sessão Cline GLM API `76797f0a…`
foi retomada em modo `act`, com escopo de apenas F06 e ferramentas seriais,
para verificar capacidade visual e produzir um parecer persistente em
`qa-glm-retry/`. Deve registrar `INCONCLUSIVE` se não conseguir perceber as
imagens, sem inventar aprovação visual. O parecer Grok de F06 já estava
concluído antes dessa troca; não foi iniciada outra rodada Copilot.
Produção segue no Codex e QA continua independente, fora do DEV.

A retomada da sessão antiga voltou a idle sem nova ferramenta ou laudo.
Para distinguir contexto travado de indisponibilidade geral, a sessão limpa
`8772a08a…` recebeu primeiro um teste somente textual: leu o JSON, calculou o
SHA256 real e gravou [checkpoint](qa-glm-fresh/checkpoint.json) corretamente.
Em seguida recebeu a inspeção visual estreita de F06. Esse teste operacional
não demonstra visão nem aprova arte; o parecer visual continua pendente.

Unarmed frontal F03, corpos limpos sem armas embutidas, ausência de
truncação/antebraço duplo, corpo frontal Sword/Axe, preservação e Defeat
frontal prostrado foram sustentados pelo QA. Walk não demonstrou colagem
de membro errado; o limite de percepção contínua continua registrado.
Esses resultados úteis não apagam a reprovação dos três requisitos acima.

### Verificações da candidata integrada

- [Validação técnica](technical-validation.json): **28/28 clipes,
  210/210 quadros, 868 hashes**, mestres e tempos reais, composição,
  recorte nativo e conteúdo pixel a pixel das tiras, `TECHNICAL_PASS`.
- [Chromium real](browser-checks/): **21/21** verificações funcionais;
  28 seleções desenham pixels, imagens carregam, velocidades 1×/0,5×,
  escala128, passo de quadro, Defeat com terminal retido e comparações
  dos 13 candidatos. Não é um parecer artístico de movimento.
- Regressão do construtor: **4/4** testes `unittest`.
- [Reexportação independente](verify-source-exports.mjs): Aseprite batch
  reabriu **42 mestres salvos** dos 13 candidatos e renderizou **384 quadros**
  (composto, nativo, corpo e mão). Todos bateram pixel a pixel e em duração
  com os exports declarados. Resultado do estado inicial marcado em revisão:
  [JSON](source-reexports/0c6072bd3c357460f25e56c752d5c185e3321ef1ca891d9fa188d4b714b61a1c/result.json).
  Demonstra fonte/exportação; não transforma carimbo em mão ou rigidez em peso.
- Inventário protegido: **3.506/3.506** arquivos preservados no
  [checkpoint](input-preservation-result.json), sujeito à nova checagem final.
- [Entrada única de revisão](../../Biblioteca%20de%20Arte/Estudos%20Comparativos/Orc%20principal%20-%20Resgate%20de%20combate/index.html).
  Os 787 itens indexados pelo builder são cópias/derivados; não significam
  787 arquivos de arte novos.

## Recursos e controle

[Medição inicial](generation-baseline.json): 1.403,70 unidades de geração no
saldo existente, sem créditos monetários. A conta inteira já tinha 596,30
unidades consumidas no ciclo; isso **não é consumo desta tarefa**. O consumo
atribuível será apurado por solicitações e recibos reais, sem inventar custo
monetário nem somar deltas afetados por atividade concorrente.

Produção inicial de combate: **6 jobs × 3 = 18,00 unidades**; saldo
1.385,70 após esses jobs, delta de 18,00, consistente com os seis recibos identificados
no [ledger do DEV](combat/report.md#2-pixellab-generation-accounting--receipts).
O representante corporal posteriormente rejeitado consumiu outras **3,00**
unidades, job `f0235167-519c-4994-86a2-1260b0e3a23e`, saldo 1.382,70.
Total conhecido até esse marco: **21,00 unidades**. O F06 Sol não usou
PixelLab; eventual consumo do novo especialista corporal ainda será apurado.
Os valores `$0.00` dos recibos são o campo de saldo monetário, não
prova de custo econômico zero nem preço de assinatura. Não houve compra.

Telemetria bruta `lastUsage` observada no Paseo após as entregas DEV:

| Sessão | inputTokens | cachedInputTokens | outputTokens | totalCostUsd |
|---|---:|---:|---:|---|
| Argon/Copilot `936fc94f…` | 15.455.991 | 14.300.676 | 127.782 | Não informado |
| Nemotron/OpenCode Free `d7cef932…` | 6.572.534 | 22.625.248 | 64.483 | 0 reportado |

Campos brutos `lastUsage` fornecidos pelos provedores; sua agregação temporal
não foi presumida uniforme. Cache não foi somado novamente nem normalizado
entre provedores. Não inferem preço por token ou custo do Copilot.
Antigravity falhou por quota antes de produzir; consumo não informado.
Telemetria de QA será registrada após seu encerramento.

GLM não expôs `lastUsage`; consumo não estimado. Antes da retomada Grok,
o contador cumulativo da sessão já existente era input4.203.122,
cache4.040.448, output48.866. Os totais posteriores devem ser distinguidos
desse histórico; não atribuir todo o contador da sessão antiga à V5.

Ao retomar Sol/Codex, o snapshot anterior exibia input214.539,
cache214.016, output286. São campos do turno/sessão anterior, não consumo
comprovado deste resgate. Comparações posteriores devem preservar essa distinção.
As demais sessões e falhas do primeiro diagnóstico constam no
[histórico anterior](../main-orc-rear-reconstruction-v4/orchestration-report.md).

Aseprite 1.3.18.6 e cliente oficial PixelLab autenticado foram verificados.
Credenciais não foram expostas nem copiadas para o projeto. Não houve
instalação de dependências, compra, commit ou escrita no Unity nesta retomada.

Entrega final, comparações, testes e parecer serão registrados aqui após a
integração. Não interpretar o status de execução como substituição da candidata
anterior ou como aprovação de produção.

### Continuidade Root — 29/10/2026, cotas fora do Copilot

Root retomou o relatório e os dois anexos originais em modo somente leitura.
O QA DeepSeek1017/Cline `7b37b320-72a6-49cf-9889-46dff3e6f21e`
foi encontrado idle com somente o prompt inicial. Uma continuação curta na
mesma sessão também terminou idle, sem ferramentas, parecer, arquivos ou erro
explícito. Causa **não estabelecida**; não há evidência para atribuir cota,
credencial ou incapacidade visual. Nenhuma nova rodada Copilot foi iniciada.

Conforme fallback expressamente autorizado, QA independente Sol/Codex
`7eaec423-562c-490d-a76e-daba3a6e3a14`, `gpt-6.1-sol`, high/full-access,
assumiu somente as três chaves corporais e F02/F08 quando o especialista
encerrar. Produção e QA estão em sessões distintas e pastas exclusivas.
A matriz publicada continua 5 candidatos ativos, 8 em revisão e 15 aliases;
representantes não foram integrados como ciclos completos.

Especialista corporal: 12 unidades comprovadas em dois jobs, saldo medido
1370,70; total conhecido desta retomada **33 gerações** (18 + 3 + 12).
As três chaves aguardam parecer antes de intermediários ou outras vistas.
Especialista de pegada continua limitado a F02/F08, preservando F06 aceito.

Verificações Root nesta continuidade: testes de integração **3/3 PASS**;
inventário protegido **3506/3506 PASS**, em 2026-10-29T13:37:40.219Z.
Esses resultados não aprovam a arte nova nem substituem a reexportação final.

### Parecer independente fora do Copilot e encaminhamento

QA Sol/Codex `7eaec423-562c-490d-a76e-daba3a6e3a14` persistiu
[corpo](qa-sol/keys-axe-result.json) e [pegadas](qa-sol/grip-F02-F08-result.json).
Freeze de entradas QA: `1124ffb3e415cadd801a3370509b654c8114bfe6f0a60034618f70ff7921896a`.
Inspeção real dos PNGs demonstrada,51 entradas conferidas sem mudança.
Não foi observada animação contínua nesta revisão estática.

- Corpo: **REVISIONS_REQUIRED / ARTISTIC_REVISION_REQUIRED**. Hoist/apex
  estruturalmente utilizáveis. BODY-01 MEDIUM: mão dominante de impacto
  termina como cunha escura fundida ao quadril em x89..98/y75..85 nativo;
  não se afirma amputação ou causa de oclusão comprovada. Especialista corporal
  retomado somente para reparo local em `body-specialist/repair1`, preservando
  as duas chaves elevadas e a entrega corporal. Intermediários bloqueados.
- Pegada: **READY_FOR_FULL_CLIP_EXPLORATION / VISUAL_REVIEW_REQUIRED** para
  F02/F08 estáticos. Root autorizou ciclo completo `front_r/Sword` ao mesmo
  produtor, em `grip-specialist/full-front-r-sword`, antes de outros clipes.
  Corpo/timing protegidos, palma real por quadro e item independente.
- Snapshot rejeitado preservado: SHA256
  `00281c8608821eecb1848d187a3508eb575781cf9172f40134f1125818df4659`;
  nova validação estrutural28/210/868 em `rejected-snapshot-preservation.json`.

Nenhum representante substituiu célula da matriz. Próximo QA será a mesma
sessão Sol/Codex, sem reativar revisores Copilot.

### BODY-01 resolvido no repair1; ciclo em produção

O [re-QA da mesma sessão Sol](qa-sol/impact-repair1-result.json) confirmou
**READY_FOR_INTERMEDIATES**. Inspeção real de nativo/composto e before/after:
luva e pulso direitos agora distinguíveis, sem regressão da entrega corporal.
Comparação independente:97 pixels locais, zero mudança fora de x88..98/y75..86;
oito hashes das chaves elevadas preservados. Retoque Aseprite,0 gerações.
Freeze representative repair1:
`e4434397532c4a42690be0acae5344a5185f0e1fbe19574cf78bd2b1672471c3`.

Root autorizou o mesmo especialista a criar somente o ciclo corporal completo
`back_r/Axe`, desarmado, reutilizando essas chaves em diretório próprio
`body-specialist/full-back-r-axe`, antes das outras três coreografias traseiras.
Pegada frontal completa continua na outra frente. Status global permanece
**ARTISTIC_REVISION_REQUIRED / PENDING_CREATOR** até revisão da versão completa.

### Primeiros ciclos completos entregues aos mesmos olhos independentes

- `body-specialist/full-back-r-axe`:12 quadros/1100ms, sem equipamento;
  clip SHA256 `2ab5ae40d7a11c0b4b271ca41f090608c3d721366da90ee1c6d1ebce9c1321c3`.
  Três chaves válidas preservadas, sete transições novas. Três jobs temporais
  (`aadca5fb-4042-4c54-9290-1d025019e685`,
  `ab74883b-045d-4458-ae80-9b340083e14b`,
  `bef66c10-ac0b-4425-9aef-a36b14cd210e`),1 geração cada.
  Total conhecido desta retomada36 (18+3+12+3); saldo medido1367,70.
- `grip-specialist/full-front-r-sword`:13 quadros/730ms equipado;
  clip SHA256 `16fe8b7b30cbaa029ac4f4bd2bda5f7c8ac127007ec40a49a1f41db2580c63a1`.
  Corpos/timing preservados; F02/F06/F08 reutilizados exatamente;0 gerações.
- Os dois freezes foram encaminhados à MESMA sessão QA Sol/Codex, sem
  expansão ou integração prematura. Revisão temporal e equipamento traseiro
  continuam pendentes; testes do player não são percepção contínua1×.
- Regressão do builder:4/4 unittest PASS nesta continuidade.

### Limitação temporal encontrada; alternativa em teste

O mesmo QA Sol terminou os dois ciclos com **INCONCLUSIVE** para a validação
artística temporal, sem defeito estático bloqueante. Percorreu todos os frames
em Chromium1×/0,5×, inspecionou PNGs e capturas reais em escalas128/64, mas não
recebeu percepção contínua da animação pela interface. Não se converte trace
funcional em parecer de fluidez. Detalhes em `qa-sol/full-back-r-axe-result.json`
e `qa-sol/full-front-r-sword-result.json`. Esse limite não é nova reprovação
BODY-01, não justifica regeneração e não aprova expansão ou integração.

Root iniciou teste suplementar estritamente temporal em outra cota:
Gemini3.8 Flash High/Antigravity, sessão
`e795a93d-07ab-421e-b033-7eff00c3e4b4`, full-access, pasta exclusiva
`qa-temporal-antigravity`. Catálogo e provedor foram consultados antes.
Escolha: modelo multimodal disponível fora do Copilot, para verificar
capacidade temporal que a interface Sol não ofereceu; não repetir auditoria
estática nem criar outra orquestração. Capacidade ainda não estabelecida.
Produção permanece parada nos marcos, matriz intacta.

### Decisão Root: continuar autoria local; limite temporal não é defeito de arte

Os dois QAs não-Copilot expuseram um limite real de observação contínua.
Esse limite mantém a validação temporal **não verificada**, mas não indica
uma correção de pixels. Root não transforma isso em aprovação artística.
Também não encerra a tarefa neste diagnóstico: o portão original de três
chaves foi satisfeito no re-QA repair1, e a revisão completa de poses não
identificou bloqueante estático. Por isso Root autoriza a **autoria de
candidatos restantes**, sem promoção, seleção da matriz ou declaração de
naturalidade1× comprovada.

Especialista corporal retomado para nove chaves dos três corpos traseiros
restantes, com mesmoQA antes de intermediários; especialista de pegada
retomado para os três ciclos frontais restantes, preservando o SwordR já
entregue. Novas fontes isoladas. A decisão autoriza produção reversível para
review, não suplanta o parecer INCONCLUSIVE nem a avaliação do criador.
A entrega integral e seu re-QA continuam sendo o objetivo; o limite temporal
será carregado explicitamente até a revisão final.

### Bloqueios de conta e recuperação sem Copilot

Em 29/10, às 14:30 UTC, Codex bloqueou o orquestrador auxiliar
`e0c04455-0df6-43f5-a5ce-d4243e7083c1` e os dois especialistas Sol com
`You've hit your usage limit`, indicando `3:03 PM` sem fuso explícito.
Uma única retomada após 15:03 UTC confirmou o mesmo bloqueio; não se presume
que o horário informado fosse UTC. Não houve compra ou troca de assinatura.

O auxiliar Nemotron VL/OpenCode Free `579b1e6b-8a6d-4884-8742-ca65fa8f1dec`
continuou dos fontes existentes, com produtores separados:
corpo `d145b472-8f98-4d77-ab3b-00199c10ab9f` e pegadas
`438383d1-01dc-4b15-bf23-59161355cbb8`. Foram relatadas nove chaves traseiras
e três ciclos frontais entregues para QA, não integrados nem aprovados.
Os hashes, consumo e aceitação dessas entregas ainda precisam de consolidação.

A rota OpenCode Zen então expôs `Free usage limit reached`. A mesma sessão,
sem descartar contexto, foi transferida para a rota configurada
`openrouter/nvidia/nemotron-3.5-super-vl:free`, que funcionou até o bloqueio
`Rate limit exceeded: free-models-per-day`. Não foram adicionados créditos.
O QA frontal `394481b2-8b9b-4a3d-83f2-798f93c57f1e` encerrou com análise
técnica e anúncio de iniciar inspeção visual; isso **não é parecer artístico**.

O orquestrador Copilot mantém a responsabilidade e retomou a supervisão,
sem iniciar novos trabalhadores Copilot. Próxima alternativa concreta:
QA Gemini 3.8 Flash High/Antigravity
`863ae631-5582-4955-a0ef-020d51692fbb`, limitado às seis novas entregas
(três ciclos frontais e três conjuntos de chaves), em
`qa-antigravity-flash/`. Não é repetição do teste temporal anterior nem
autorização para preencher lacunas da matriz com protótipos.

### QA das seis novas entregas; intermediários em retomada

O [parecer Flash/Antigravity](qa-antigravity-flash/qa-result.json) entregou
`READY_FOR_NEXT_STAGE` para cada um dos três ciclos frontais e dos três
conjuntos de chaves traseiras. Houve inspeção real das imagens em escala
nativa/tática e por sequência de quadros; observação contínua 1× não foi
declarada. Esse parecer libera autoria da próxima etapa, não o criador,
uma integração Unity ou aprovação dos ciclos traseiros ainda inexistentes.
O custo LLM da revisão não foi informado; zero chamadas PixelLab de produção
não significa zero inferência de IA.

O DEV Gemini 3.8 Flash High/Antigravity
`3c2b5bd7-b270-453c-a198-b77ab7b021e5` assumiu exclusivamente os três
ciclos traseiros desarmados em `body-specialist/final-cycles/`.
Deve preservar as nove chaves aceitas, criar os intermediários no Aseprite,
comprovar reexportação e parar para o mesmo QA antes das pegadas traseiras.
Não refaz o `back_r/Axe` completo já existente nem modifica fontes anteriores.

Checkpoint Root de 15:17 UTC: matriz publicada preservada, **28 células,
210 quadros, 868 hashes** técnicos; inventário **3506/3506 PASS**.
Os quatro testes do contrato de integração passaram após adicionar a proteção
contra publicar chaves corporais como clipe equipado. Nenhum desses testes
substitui o parecer da arte nova ou representa a integração final.

### Três ciclos traseiros completos entregues; re-QA em execução

O [DEV final](body-specialist/final-cycles/report.md) entregou os três corpos
completos, todos com 12 quadros: Sword 730 ms nas duas vistas e Axe 1100 ms
em `back_l`. As nove chaves foram preservadas nos índices F03/F04/F07.
As fontes finais estão isoladas em `body-specialist/final-cycles/`.
O [checkpoint](body-specialist/final-cycles/checkpoint.json) declara mestres
128/256, recortes e reexports; o mesmo QA Flash recebeu os três ciclos e
o `full-back-r-axe` anterior para julgar todos os intermediários antes de
liberar as quatro pegadas traseiras. Nenhuma célula publicada foi trocada.

Contabilidade consolidada até esse marco: 18 gerações iniciais, 3 no
representante rejeitado, 12 nas primeiras chaves, 3 no primeiro ciclo,
16 nos outros conjuntos de chaves e 9 nos três ciclos finais: **61 unidades**.
O substituto Nemotron corporal não gerou novas poses, apenas concluiu a
limpeza/empacotamento dos jobs anteriores. Saldo inicial 1403,70; último
recibo 1342,70, consistente com o ledger. Não houve compra. O custo LLM
continua não informado e não é inferido do saldo monetário `$0.00`.

### Primeiro re-QA dos intermediários: três correções locais

O [parecer dos quatro corpos](qa-antigravity-flash/full-rear-bodies-result.json)
liberou `full-back-r-axe` para pegada, mas reprovou os três ciclos novos:

| Achado | Local | Correção encaminhada |
|---|---|---|
| DEFECT-REAR-01 HIGH | `back_r/Sword` F06, rastro claro de corte pintado no corpo | Remover o efeito e reconstruir materiais/contorno sob ele; não abrir buracos por limiar de brilho |
| DEFECT-REAR-02 HIGH | `back_l/Axe` F02, machado embutido no ombro | Remover item e reconstruir manopla/anatomia, preservando a passagem para a chave F03 |
| DEFECT-REAR-03 MEDIUM | `back_l/Sword` F05, gancho preto residual | Limpar somente o filamento confirmado, não a ombreira |

As nove chaves permanecem exatas. A declaração de limpeza integral no
relatório DEV anterior foi contradita por inspeção independente; não é
evidência de conformidade. O mesmo DEV recebeu os achados em nova
`final-cycles/repair1/`, sem sobrescrever o freeze rejeitado e sem geração
adicional prevista. Retorna ao mesmo QA após reexportar os mestres.

Em paralelo, o especialista de pegada
`7db0e7b6-ab88-49e9-9362-a19121c8ebf5`, Gemini 3.8 Flash/Antigravity,
recebeu apenas F04/F07 do `back_r/Axe` já liberado, em `rear-grip-flash/`.
Deve demonstrar palma/pulso/oclusão autênticos antes de compor o ciclo
inteiro; não usa os três corpos ainda em reparo. Não há edição concorrente
dos mesmos mestres ou criação de QA dentro do DEV.

### Segunda reprovação corporal e escalonamento obrigatório

O [re-QA repair1](qa-antigravity-flash/rear-bodies-repair1-result.json)
liberou `back_l/Sword`: filamento resolvido, sem regressão. Os outros dois
clipes continuam reprovados. Em `back_r/Sword` F06 restaram cinco pixels
flutuantes e o reparo usou couro avermelhado sobre cota de malha. Em
`back_l/Axe` F02 a haste ainda atravessa o trapézio e a luva substituta é um
bloco, não uma mão anatomicamente convincente. Não houve integração.

Após a segunda reprovação, o mesmo produtor Flash **não continua** esses
reparos. A especialidade foi transferida a Claude Opus 5.5 Medium/Antigravity,
sessão `1e82d18d-5ddf-43b4-be6e-5df7b9b75a0c`, limitada aos dois quadros
em `body-specialist/escalated-fixes/`. A capacidade maior se justifica pela
falha reiterada da reconstrução anatômica, não por empacotamento simples.
Codex e as duas rotas gratuitas continuam bloqueados, sem novas compras.

Os dois representantes de pegada `back_r/Axe` F04/F07 foram entregues em
`rear-grip-flash/` e enviados ao mesmo QA, com corpo preservado. Ainda não
autorizam propagação para os 12 quadros. O QA também deve confirmar a
proveniência Aseprite e a ligação palma-pulso real, não apenas os ângulos
declarados ou o contato da lâmina com o chão.

### Cota do especialista e alternativa textual verificável

Opus/Antigravity retornou quota individual, reset informado
**120h56m34s**, sem entrega dos reparos. A sessão Sonnet anterior registra
132h10m49s desde 05:40 UTC; seu prazo também não expirou, portanto não foi
reexecutada. Nenhuma assinatura ou crédito foi comprado.

GLM 5.3/Cline, sessão DEV nova `15ef8466-7a3d-431c-baee-4abbf7da3698`,
recebeu os dois reparos em `body-specialist/glm-fixes/`. É uma alternativa
de raciocínio/implementação e operação PixelLab/Aseprite, **não um revisor
visual substituto**: o teste anterior comprovou ferramentas textuais, mas
não inspeção PNG nesse runtime. O produtor foi instruído a não abrir PNG
no contexto, não afirmar visão e submeter qualquer resultado ao mesmo QA
multimodal independente. Esse desvio é necessário pelas cotas, sem reduzir
o critério anatômico nem reaproveitar o bloco de mão reprovado.

O [QA dos dois representantes de pegada](qa-antigravity-flash/rear-axe-grip-keys-result.json)
liberou apenas a extensão para `back_r/Axe` completo. O especialista
`7db0e7b6…` recebeu os 12 quadros, preservando F04/F07 e o corpo aceito,
sem os outros três clipes. O recorte equipado128 pode cortar a cabeça
erguida; a fonte canônica256 deve preservá-la integralmente. Hashes de
relatório digitados incorretamente devem ser corrigidos sem alterar
os representantes JSON corretos ou os pixels congelados.

### Ciclo `back_r/Axe` completo aceito; correções corporais em QA

O [parecer do ciclo completo](qa-antigravity-flash/rear-axe-full-result.json)
deu `READY_FOR_MATRIX_REVIEW` ao `back_r/Axe` de 12 quadros/1100 ms.
Verificou corpo com delta zero, F04/F07 byte-idênticos aos representantes
já aceitos, `visibleInterval [2,8]`, bookends transparentes, lâmina em
`groundY 190` sem penetração em F08, mestres reais reexportados e recorte
nativo diagnóstico sem afetar a fonte canônica 256. Não aprova os outros
três corpos, a matriz, o criador ou o Unity.

O produtor GLM `15ef8466-7a3d-431c-baee-4abbf7da3698` entregou
`GLM_BODY_FIXES_READY` para os dois quadros reprovados, em
`body-specialist/glm-fixes/`: F06 de `back_r/Sword` corrigido só com Lua no
Aseprite (resíduos para alfa 0 e malha restaurada com doadores das mesmas
coordenadas em F05/F07) e F02 de `back_l/Axe` reautorado por um job PixelLab
`inpaint_image_pro_flash` (`540302e4-2690-4282-8de5-c609f15b1142`) restrito
à máscara x68..100/y8..33, composto no Aseprite. Consumo medido
**1342,70 → 1336,70** (6,0 unidades), sem compra; total conhecido desta
retomada passa a **67,00 unidades**.

Esse produtor declarou explicitamente que **não abriu imagens**: seus deltas
e componentes são hipóteses técnicas, não verificação visual. O mesmo QA
multimodal `863ae631…` recebeu o pacote com essa limitação escrita. Se
reprovar novamente o mesmo frame pela terceira vez, a próxima decisão exige
mudança de método, não repetição de retoque.

Em paralelo, o especialista de pegada `7db0e7b6…` recebeu `back_l/Sword`,
cujo corpo já está liberado, para compor o ciclo completo na família Sword
com o item independente correto. Não há edição concorrente dos mesmos
mestres: cada frente escreve em diretório próprio e o Root só integra
depois do parecer.

### Situação após o QA das correções escalonadas

O [parecer das correções GLM](qa-antigravity-flash/glm-body-fixes-result.json)
resolveu os três resíduos e liberou os dois corpos:
`back_r/Sword` (`aba36d6652…`) e `back_l/Axe` (`d87cd8331b…`), ambos
`READY_FOR_REAR_GRIPS`. Confirmou os 5 pixels flutuantes em alfa 0, a malha
restaurada com doadores de F05/F07, o desaparecimento da haste e do pino em
F02, os 11 quadros restantes byte-idênticos e as 9 chaves preservadas.
Nenhuma geração PixelLab nessa revisão.

O [ciclo `front_r/Sword`](qa-antigravity-flash/front-r-sword-full-result.json)
recebeu `READY_FOR_MATRIX_REVIEW`, fechando a lacuna que o revisor anterior
havia deixado como `INCONCLUSIVE` apenas temporal. Com isso os quatro ciclos
frontais têm agora parecer independente positivo do mesmo revisor.

O ciclo `back_l/Sword` foi entregue (`REAR_SWORD_L_BACK_FULL_READY`) e está
em revisão; os dois últimos ciclos traseiros (`back_r/Sword` e `back_l/Axe`)
foram atribuídos ao mesmo especialista, cada um com o item da família correta.
Quando esses três passarem, existirão os oito clipes armados finais.

Para a integração, o Root criou `assemble-weapon-patch.mjs`, que monta o patch
das oito células a partir de uma configuração explícita e **falha** se algum
clipe não tiver hash de QA independente correspondente ao arquivo exato,
família de arma divergente de `direction/action`, ciclo de um quadro, arma
visível no bookend, camada ausente, mestre com hash obsoleto ou definição de
item inexistente. Nada foi integrado ainda.

### Seis dos oito clipes armados aceitos

O QA independente aceitou, cada um com parecer próprio e hash exato:

| Célula | Fonte | Parecer |
|---|---|---|
| `front_r/Sword` | `grip-specialist/full-front-r-sword` | `front-r-sword-full-result.json` |
| `front_l/Sword` | `grip-specialist/front_l-Sword-full` | `qa-result.json` |
| `front_r/Axe` | `grip-specialist/front_r-Axe-full` | `qa-result.json` |
| `front_l/Axe` | `grip-specialist/front_l-Axe-full` | `qa-result.json` |
| `back_r/Axe` | `rear-grip-flash/full-back-r-axe` | `rear-axe-full-result.json` |
| `back_l/Sword` | `rear-grip-flash/full-back-l-sword` | `rear-sword-l-back-full-result.json` |

`back_l/Sword` foi aceito como corte diagonal genuíno, com corpo reconstruído
byte-idêntico, bookends limpos, F03/F04/F07 preservados, pomo e guarda
legíveis e folga de solo convincente. Os dois restantes (`back_r/Sword` e
`back_l/Axe`) estão em produção com o item correto de cada família.

O `assemble-weapon-patch.mjs` foi exercitado em modo `probe` sobre esses seis
clipes e passou por todos os contratos e pelo portão de evidência de QA.
Ainda faltam os dois clipes em produção; nada foi integrado.

## Entrega final da rodada — 29/10/2026

**Pacote pronto para o criador revisar. Não é aprovação artística dele, nem
integração, nem promoção de produção.**

O [parecer integrado](qa-antigravity-flash/integrated-candidate-result.json)
deu `READY_FOR_CREATOR_REVIEW` ao manifesto
`candidate28manifest.json`, SHA-256
`58152a101e16cbc031349b3308649f9ccaa38b99782d4e23bcf2ee43fddc3794`:
13 células ativas, 15 aliases exatos, 226 quadros.

### O que foi aceito e por quem

Todos os oito ciclos armados têm parecer positivo do mesmo revisor
multimodal independente, em sessões separadas do produtor:

| Célula | Parecer |
|---|---|
| `front_r/Sword`, `front_l/Sword`, `front_r/Axe`, `front_l/Axe` | `front-r-sword-full-result.json`, `qa-result.json` |
| `back_r/Axe`, `back_l/Sword`, `back_r/Sword`, `back_l/Axe` | `rear-axe-full-result.json`, `rear-sword-l-back-full-result.json`, `rear-two-remaining-result.json` |

Os quatro `Unarmed` vêm do lote anterior e foram sustentados pelo QA prévio,
sem nova defesa; `back_l/Walk` continua com a limitação de percepção contínua
declarada. Nenhuma dessas células tem aprovação do criador.

### Verificação real do pacote

- Validação técnica: **28 células, 226 quadros, 964 hashes**, `TECHNICAL_PASS`,
  com hash do manifesto conferido.
- Reexportação independente: **42 mestres, 448 quadros** reabertos no Aseprite
  a partir das fontes salvas, `PASS_SAVED_SOURCE_EXPORTS`, com
  `artisticallyApproved: false` explícito.
- Chromium real: **21/21** verificações funcionais na página publicada,
  incluindo velocidades, passo de quadro, escala tática, terminal de Defeat
  e cobertura antes/depois dos 13 candidatos.
- Inventário protegido: **3506/3506** arquivos.
- Freeze rejeitado: revalidado **210 quadros / 868 hashes**, íntegro.
- Testes: construtor **4/4**, integração **4/4**.

### Recursos e falhas de provedor desta retomada

Consumo PixelLab atribuível: 18 iniciais + 3 do representante rejeitado +
12 das primeiras chaves + 3 do primeiro ciclo + 16 das outras chaves +
9 dos três ciclos + 6 do reparo F02 = **67 unidades**; saldo medido de
1403,70 para 1336,70. Nenhuma compra ou assinatura. Custo de inferência LLM
não foi informado por nenhum provedor e não é estimado.

| Sessão | Provedor/modelo | Desfecho |
|---|---|---|
| `61c48dc0…` | Gemini 4 Argon/Antigravity | quota individual na largada, sem produção |
| `936fc94f…` | Gemini 4 Argon/Copilot | produziu o lote inicial; supersedido em pegada e corpo após duas reprovações de cada especialidade |
| `d7cef932…` | Nemotron VL/OpenCode Free | Walk localizado; entrega mantida |
| `76797f0a…`, `8772a08a…` | GLM 5.3/Cline GLM API | texto, hash e gravação OK; ficaram idle após abrir PNG, sem laudo e sem erro explícito |
| `7b37b320…` | DeepSeek 1017/Cline | idle sem ferramenta nem laudo; causa não estabelecida |
| `d13ab881…` | Grok 4.7/Copilot | primeira QA completa; rejeitou pegada, peso traseiro e dominância |
| `47326bab…`, `950ff800…`, `e0c04455…` | GPT 6.1 Sol/Codex | pegada anatômica, corpo traseiro e orquestração; interrompidos por limite de conta |
| `579b1e6b…` | Nemotron VL/OpenCode Free | continuou dos fontes; produziu 9 chaves e 3 ciclos; parou por limite gratuito |
| `3c2b5bd7…` | Gemini 3.8 Flash/Antigravity | três ciclos traseiros; duas reprovações levaram ao escalonamento |
| `1e82d18d…` | Claude Opus 5.5/Antigravity | quota individual 120h, sem entregar os reparos |
| `15ef8466…` | GLM 5.3/Cline | reparou F06 e F02 com Aseprite e um job de edição; aprovado no re-QA |
| `7db0e7b6…` | Gemini 3.8 Flash/Antigravity | compôs os quatro ciclos traseiros equipados; dois exigidos em re-entrega |
| `863ae631…` | Gemini 3.8 Flash/Antigravity | QA independente de todas as etapas finais e do pacote integrado |

O próximo marco é a avaliação artística explícita do criador na página
[Orc principal - Resgate de combate](<../../Biblioteca de Arte/Estudos Comparativos/Orc principal - Resgate de combate/index.html>).
Não há autorização para copiar para `../TacticsRPG`, promover
`equipment-current.json` ou tratar este parecer como aprovação de arte.

## Continuidade 30/10 — QA de primeira preferência confirma o pacote

O criador reeditou a task de arte e a orquestração com nova ordem de QA
(Sol/Codex → DeepSeek 1017 → gratuito) e orquestrador no GitHub Copilot.
Como a produção V5 já estava entregue e `READY_FOR_CREATOR_REVIEW`, nenhuma
arte foi reautorada — o passo pendente era a revisão independente pelo
revisor de primeira preferência, cuja cota renovou após as 15:03 UTC.

**Resultado:** [parecer Sol/Codex](qa-independent-final/report.md) e
[resultado estruturado](qa-independent-final/qa-result.json), sessão
`c3ca3523-1aaa-464b-bae5-4b2cbb2d66d7` (`gpt-6.1-sol`, xhigh, full-access):

- **`READY_FOR_CREATOR_REVIEW`** para o mesmo SHA `58152a101e16cbc031349b3308649f9ccaa38b99782d4e23bcf2ee43fddc3794`.
- Validações próprias: 964 hashes, 42 reexportações/448 comparações de
  quadros, 21 checks Chromium, **226 comparações pixel/duração no player** e
  **24 execuções de ataques assistidas**, com todos os quadros observados em
  cada volta e cada execução cruzando o loop completo.
- Corpos inspecionados com equipamento desligado; nenhum defeito bloqueante
  confirmado em corpos, composições ou pegadas.
- Achado não bloqueante **DOC-01 (LOW)**: o parecer anterior do Antigravity
  declarou contagens/duração de Walk incorretas; os valores canônicos são
  Walk frontal 16f/1280 ms e traseiro 8f/1280 ms. O artefato do revisor
  anterior permanece preservado sem edição; esta nota é a correção de
  registro.
- Zero chamadas PixelLab; custo LLM não reportado; nenhuma edição de arte,
  manifesto, docs ou Unity.

O pacote agora tem confirmação dupla e independente (revisor de fallback
multimodal Gemini 3.8 Flash + revisor de primeira preferência Sol) sobre o
mesmo hash. O único marco restante continua sendo a avaliação artística
explícita do criador no
[estúdio de revisão](<../../Biblioteca de Arte/Estudos Comparativos/Orc principal - Resgate de combate/index.html>),
sem promoção, Unity ou autoaprovação.
