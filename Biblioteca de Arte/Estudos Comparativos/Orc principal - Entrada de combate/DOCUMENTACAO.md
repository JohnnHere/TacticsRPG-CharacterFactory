# Entrada natural de combate — revisão incremental atual

2026-10-25 · `main-orc-onehanded-entry-v1` · **candidato local, aprovação artística do criador pendente**.

Esta revisão parte do último polimento `onehanded-polish-v1`, preservado integralmente. O Orc é **orc-v1 / Verde Warcraft**; o equipamento ativo continua apontando para v3 até decisão explícita de seleção. Não restaurar o antigo Orc V4. O relatório do passe anterior permanece abaixo como histórico de continuidade.

## Diagnóstico confirmado

A espada começava com dois quadros baixos quase horizontais (270°), sem preparação corporal antes da aparição. Em seguida a mão saltava de world93,130 para98,89 (cerca de41,30px), com mudança de75° na lâmina. A sobreposição correta da luva não resolvia essa progressão anatômica. No machado, a carga projetada aparecia antes de um gesto claro de preparação do braço. São causas verificadas nos PNGs/perfis; os timestamps do vídeo citados no pedido são relato fornecido pelo criador, não uma nova gravação anexada e inspecionada nesta execução.

A auditoria do DEV está em `experiments/main-orc-entry-v1/dev-audit.md`. Classificação principal: repouso KEEP; início/entrada TRANSITION_FIX; preparação elevada TIMING_ONLY ou reutilização adaptada; extensão, passagem limpa, impacto e recuperação KEEP. Nenhum ataque inteiro foi regenerado.

## Correção proposta e fontes

Uma única pose de preparação foi produzida por **PixelLab Pro Flash inpaint** sobre o próprio neutro atual. Apenas braço direito (à esquerda da imagem), cotovelo, antebraço e mão fechada foram retocados. Rosto, pescoço, centro do peito, outro braço, quadril e pernas permanecem nos pixels próprios. No resultado real, o grip ficou em nativo37,67 / world101,131, em vez da coordenada aproximada solicitada ao gerador. A ligação usa a luva real, inspecionada, e não uma coordenada presumida.

A montagem e todos os retoques/tempos/exportações são no **Aseprite**, por Lua em batch oculto, perfil isolado e `--noinapp`. O resultado em nuvem não é desenho manual. Mestre da preparação: `experiments/main-orc-entry-v1/inputs/prepare-arm.aseprite`; corpo e dedos exportados no mesmo diretório. Fora da máscara foram removidos apenas dois pixels herdados abaixo da mão deslocada (world97,151 e98,151); todo o restante não mascarado foi preservado. Proveniência verificável em `prep-provenance.json`, máscara e scripts no experimento.

A entrada agora é **neutro sem arma → preparação corporal sem arma → mesma pose com pegada estabelecida → elevação do cotovelo/ombro → golpe**. Não é uma animação de sacar de bainha: não há bainha, arma carregada, magia ou sistema novo. A arma aparece somente depois da preparação, no mesmo corpo e grip, dentro do Attack. O primeiro quadro armado dura35ms; o preparo anterior,65ms.

Na espada, duas poses intermediárias deste mesmo Orc (Axe3/Axe4 do polimento, corpo/dedos exatos) ligam a nova preparação à guarda existente. A orientação progride315°→330°→340°→345°. O caminho de preparação da mão passa por distâncias aproximadas17,26px (neutro→preparo),18,38px,20,59px e11px. Isto descreve o espaçamento, sem provar por números que o movimento é natural. O golpe e a recuperação anteriores são mantidos, incluindo a limpeza do resíduo de lâmina.

No machado, a entrada usa300°→325°→350°, com as próprias poses de elevação/preparação. A antiga carga projetada foi removida da sequência, não redesenhada nem apagada do acervo. As poses, impacto e recuperação do machado continuam distintos da espada. Compartilhar uma preparação curta de braço deste indivíduo não cria um movimento de ataque universal.

| Clip | Antes (polimento) | Entrada candidata | Impacto artístico local |
|---|---:|---:|---|
| Espada |11 quadros /690ms|13 quadros /730ms|novo8, aos360ms (antes320ms)|
| Machado |12 quadros /1055ms|12 quadros /1005ms|novo6, aos410ms (antes460ms)|

Os holds de impacto continuam100/115ms. `appliesDamage:false`: nenhuma mudança de dano/eventos/turnos Unity. A espada acrescenta40ms para estabelecer a preparação; o machado reduz50ms ao retirar a carga redundante. A recuperação preserva o corpo idêntico na ocultação da arma e o retorno ao neutro sem overlay. Idle5/2200ms e Walk16/1280ms ficam exatos e sem arma.

Plano explícito e mapeamento de cada quadro: `experiments/main-orc-entry-v1/entry-plan.json`. Fontes candidatas: `characters/orc-v1/source/aseprite/onehanded-entry-v1/`; PNGs/camadas/perfis/clips: `characters/orc-v1/source/onehanded-entry-v1/`. Fork recuperável dos mestres anteriores: `characters/orc-v1/source/aseprite/main-orc-entry-v1/`. Não alterar o ponteiro ativo automaticamente.

## Reutilização, revisão e limites

Armas independentes, dimensões, grip local, PPU100, escala1 e ordem de oclusão permanecem. A própria categoria define o perfil; não se produz um corpo novo para cada espada/machado. Canvas256, corpo128 em64,64 e chão190, sem espelhamento, trim, suavização ou interpolação de preview. A inspeção de armas diferentes continua necessária para cabos/guardas incompatíveis; composição offline não implementa equipar no runtime.

Página isolada: `Biblioteca de Arte/Estudos Comparativos/Orc principal - Entrada de combate/index.html`. Compara **polimento anterior × entrada nova**, com PNGs/tempos reais, controles existentes, quadro a quadro, normal/lento, zoom, pegadas, impacto e sequência Idle→Attack→Idle. As páginas anteriores continuam preservadas.

A revisão integrada pelo QA Paseo é registrada separadamente em `experiments/main-orc-entry-v1/qa-final.md`; o pacote integrado e os resultados abaixo são congelados antes dessa revisão; o parecer final registra a versão exata revisada. O criador continua como autoridade artística. Somente front_r, sem teste no jogo, outras vistas ou propagação. A transferência de peso ampla continua limitada; o foco é a continuidade da entrada, não reconstruir a biomecânica.

### Resultado integrado e verificações deste passe

- Build `dist/editor/main-orc-onehanded-entry-v1/f600aa0675d5e5d3d093/`: **10 jobs,98 quadros exportados e comparados**. Reexportação dos mesmos mestres reutilizou o mesmo build.
- `root-safety-and-artifacts.json`: **9.923 arquivos de arte anteriores e9 metadados ativos preservados**, todos os corpos/dedos mapeados exatos, armas inalteradas, Idle/Walk exatos e visibilidade contígua.
- `entry-check.json`: verificação focada do DEV sem falhas. Passos de grip e ângulo são diagnósticos, nunca regras universais de arte ou aprovação.
- `preview-qa.json`: **69 quadros e recortes de grip comparados pixel a pixel**, zero divergências, nenhuma exceção JavaScript, abertura file:// e mobile390px sem overflow.
- `playback-capture.json`: todos os13 quadros da espada e12 do machado observados em reprodução real1× e0,25×, com capturas de canvas. `sequence-playback.json`: ambas as sequências Idle→Attack→Idle completadas no tempo real e terminando sem arma. A revisão usa essas capturas/poses; não é uma observação humana de jogo ou de vídeo contínuo.
- `test-suite.json`: `node --test --test-concurrency=1`, **14/14 PASS**. Doctor e editor-check disponíveis, Aseprite1.3.18.6. Nenhuma alteração em Unity.
- Fixtures de troca de arma: `reports/main-orc-entry-v1/reuse/{Sword|Axe}/reuse.json`,13/12 quadros recompostos com assets existentes menores, sem geração ou redesenho de corpo. São testes técnicos de reutilização, não novos itens aprovados.

Inspeção visual primária: a mão e o antebraço se preparam antes da aparição; a subida da espada possui caminho legível e direções progressivas, sem o salto baixo→guarda anterior. Os dedos próprios permanecem por cima do cabo. As boas poses de golpe/impacto/recuperação foram preservadas. Permanece uma troca discreta de visibilidade no limite da ação, por decisão de produto; não há efeito ou interpolação para escondê-la. A transferência ampla de peso e o apoio estático dos pés não foram refeitos.

Arquivos alterados neste passe: dois novos assemblers `tools/entry-main-orc.mjs` e `tools/aseprite/entry-main-orc.lua`, wrapper `experiments/main-orc-entry-v1/check-entry.py`, modo `--entry` no construtor existente, fontes/derivados isolados e ponteiro **somente candidato** `characters/orc-v1/source/equipment-entry-candidate.json`; notas curtas em AGENTS/handoff/roadmap, este capítulo e navegação da biblioteca. Estado inicial já sujo em `initial-git-status.txt`. O construtor já era não rastreado no Git: não há diff Git exato anterior dele; a revisão considera seu código final completo e os ramos legados. Nenhum commit/reset/clean.

Reprodução local sem nova cobrança:

```text
node tools/entry-main-orc.mjs build
node tools/entry-main-orc.mjs verify
node src/cli.mjs editor-export --manifest characters/orc-v1/source/aseprite/onehanded-entry-v1/editor.json
```

Com Python local: `experiments/main-orc-entry-v1/check-entry.py`, `tools/build-main-orc-rescue-review.py --entry` e `tools/build-art-library.py`. O plano e os PNGs de preparação são inputs congelados; estes comandos não chamam PixelLab. Auditoria de reaproveitamento em `reuse-assessment.json`; o runtime dinâmico continua como extensão futura fora do escopo.

Orquestração: DEV gratuito DeepSeek V4.1 Flash via `opencode-free` no Paseo; integração/artes controladas pelo orquestrador; QA independente final GLM5.3 via `cline-glm-api`. Catálogo, IDs, resultados e uso verificável serão registrados no experimento. Só o fluxo de orquestração organiza QA, sem agentes adicionais solicitados pelo DEV.

Custo artístico: uma chamada Pro Flash, **6 gerações cobradas**, sem retentativa paga ou nova arma. Pedido e resultado em `prep-request.json` e `cloud-record.json`; job591a50b5-227a-4808-92c9-a86b0ec13e96. Não afirmar preço monetário ou tokens que o provedor não reportou. Nenhum commit, limpeza destrutiva ou escrita em `../TacticsRPG`.

---

# Orc principal — polimento dos ataques de uma mão

2026-10-25 · `main-orc-onehanded-polish-v1` · **candidato isolado, aprovação artística do criador pendente**.

O Orc principal é **orc-v1 / Verde Warcraft**. A correção anterior `main-orc-onehanded-v3` foi uma melhoria substancial e continua ativa; não é uma versão rejeitada. O antigo Orc V4 permanece descartado. Esta tarefa não altera o jogo, a seleção de produção, o Idle/Walk aprovado, a arte das armas ou outras direções.

## A. Antes e depois

A inspeção usou os mestres salvos e PNGs atuais, suas durações e capturas de reprodução. Nenhum vídeo novo foi anexado ao pedido de polimento; não atribuímos a ele observações de uma gravação indisponível. Auditoria por quadro, motivo, pegada e deslocamento: `experiments/main-orc-polish-v1/artistic-audit.json`. Índices neste relatório começam em **zero**.

| Arma | Problema principal | Alteração mínima aplicada | Preservação e limite |
|---|---|---|---|
| Espada | Recuperação retraía a mão cerca de49,25px em uma única troca; cadência mantinha poses de aceleração por tempo demais. | Tempos assimétricos; ponte entre o antigo5 e6 reutilizando o antigo Axe7 deste mesmo Orc. Retração passa por cerca de30,59px e19,03px; a arma continua separada, escala1. Um retoque mascarado no corpo do impacto. | Guarda, extensão, pose de recuperação e identidade mantidas. Na passagem do corte foi apagado um resíduo fino de lâmina herdado no corpo, após QA independente. Mudança de apoio corporal discreta; não se apresenta como uma nova animação corporal completa. |
| Machado | Release70ms e impacto70ms tinham ênfase semelhante; arma sumia durante o retorno do braço. | Release35ms, impacto115ms e antecipação deliberada. Retoque limitado em tronco/quadril/joelho no impacto. Ocultação em uma repetição do mesmo corpo antes do assentamento. | Machado, proporção, poses de elevação, preparação, extensão e seguimento preservados. Peso vem sobretudo da cadência e do compromisso existente da pose. |
| Ambas | Arma aparecia quando a mão já havia saído do repouso; desaparecimento coincidia com troca de corpo. | Breve quadro de pegada inicial no próprio corpo neutro; conclusão repete a recuperação sem overlay antes do retorno. | A entrada/saída continua sendo uma troca discreta, por decisão de armas somente no ataque. Não há sistema de sacar/embainhar ou transição invisível simulada. |

### Classificação de todos os quadros anteriores

| Quadro v3 | Sword | Axe |
|---:|---|---|
|0|KEEP|KEEP|
|1|TRANSITION_FIX|TRANSITION_FIX|
|2|TIMING_ONLY|TIMING_ONLY|
|3|TIMING_ONLY|TIMING_ONLY|
|4|MINOR_POLISH|TIMING_ONLY|
|5|MINOR_POLISH|MINOR_POLISH|
|6|TRANSITION_FIX|TIMING_ONLY|
|7|TRANSITION_FIX|MINOR_POLISH|
|8|—|TRANSITION_FIX|
|9|—|KEEP|

Não foi necessário classificar nenhuma pose como REWORK_POSE. A observação de MINOR_POLISH não obriga redesenhar: a recuperação Axe7 foi mantida; na passagem Sword4, a inspeção independente identificou e levou à remoção local de um resíduo de lâmina, sem alterar a pose. O teste inicial alterou **somente tempos**, com pixels idênticos, antes dos retoques. Seus mestres, exportação e captura estão em `experiments/main-orc-polish-v1/timing-only/`. Ele melhora o ritmo, mas não resolve a distância entre as poses da recuperação nem produz esforço corporal novo.

### Tempos e mapeamento finais

Espada anterior: 8 quadros / 775ms → candidato: 11 quadros / 690ms:

| Novo | Fonte do corpo | Fase | ms |
|---:|---|---|---:|
|0|Sword0|Repouso sem arma|40|
|1|Sword0, dedos traçados da própria luva|Estabelecer pegada|45|
|2|Sword1|Preparação|65|
|3|Sword2|Guarda elevada|100|
|4|Sword3|Avanço|35|
|5|Sword4, limpeza pontual de resíduo|Passagem do corte|35|
|6|Sword5 + retoque mascarado|Impacto/seguimento|100|
|7|Axe7, mesmo indivíduo atual|Ponte de recuperação|55|
|8|Sword6|Recuperação|80|
|9|Sword6, sem overlays|Conclusão|45|
|10|Sword7|Neutro exato|90|

Machado anterior: 10 quadros / 1130ms → candidato: 12 quadros / 1055ms:

| Novo | Fonte do corpo | Fase | ms |
|---:|---|---|---:|
|0|Axe0|Repouso sem arma|40|
|1|Axe0, dedos traçados da própria luva|Estabelecer pegada|50|
|2|Axe1|Preparação|100|
|3|Axe2|Elevação|80|
|4|Axe3|Ombro armado|155|
|5|Axe4|Descida|35|
|6|Axe5 + retoque mascarado|Impacto|115|
|7|Axe6|Seguimento|110|
|8|Axe7|Recuperação|130|
|9|Axe7, sem overlays|Conclusão|50|
|10|Axe8|Assentamento|90|
|11|Axe9|Neutro exato|100|

As três adições da espada são pegada inicial, ponte reutilizada e corpo repetido na conclusão. As duas do machado são pegada inicial e conclusão. Nenhum novo lote de animação foi gerado. Impacto artístico passa de430→320ms na espada e550→460ms no machado; ambos no novo quadro6. Isso é **proposta visual local**, `appliesDamage:false`, sem alteração em dano, turnos ou eventos Unity.

## B. Alterações técnicas e fontes

- Forks recuperáveis: `characters/orc-v1/source/aseprite/main-orc-polish-v1/`, feitos por `editor-fork` a partir dos dois mestres atuais.
- Mestres candidatos: `characters/orc-v1/source/aseprite/onehanded-polish-v1/`, com `sword-attack`, `sword-body`, `sword-hand-front` e equivalentes `axe`, todos `.aseprite`. Manifesto de exportação `editor.json` nesse diretório.
- PNGs, camadas, folhas, `clip.json` e `profile.json`: `characters/orc-v1/source/onehanded-polish-v1/{Sword|Axe}/Attack/`.
- Pacote de revisão: `characters/orc-v1/source/onehanded-polish-v1/manifest.json`; ponteiro **somente candidato** `characters/orc-v1/source/equipment-polish-candidate.json`.
- Build imutável: `dist/editor/main-orc-onehanded-polish-v1/3b6384933314a2bb64f9/`. Nova exportação dos mesmos mestres retornou o mesmo build, `reused:true`.
- Implementação incremental: `tools/polish-main-orc.mjs` e `tools/aseprite/polish-main-orc.lua`; compositor Lua e exportador já existentes reutilizados. `tools/compose-main-orc-item.mjs` ganhou um argumento opcional de perfil para testar candidatos; o padrão continua v3.
- O construtor existente `tools/build-main-orc-rescue-review.py` ganhou `--polish`, sem substituir o modo anterior ou criar outro aplicativo de preview.

Canvas256×256, corpo128×128 em64,64, chão190, PPU100, sem escala/espelhamento/trim/interpolação. Fontes corporais de início/fim são o **Idle0 atual**, não o conceito estático. Idle5 fases400/450/500/450/400ms e Walk16×80ms permanecem exatos.

A arte de Espada do Recruta e Machado de Milícia foi preservada integralmente. Pegadas locais do item continuam48,66 e36,55; escala1. A nova pegada inicial do corpo é98,148 no canvas256 (34,84 nativo). A ponte Sword7 usa grip129,148 e102°. Os demais encaixes e orientações herdados permanecem. A própria luva atual fornece a máscara de dedos; não há mão genérica girada ou transplante de outro personagem. Ordem `weaponBack → body → weaponFront → handFront`. Não se estende o machado sobre a perna neutra nem se inventa troca de profundidade para escondê-lo.

Arma visível somente em Attack1..8, intervalo único em ambas. Corpo idêntico antes/depois da aparição e ocultação. Repouso, Walk, inspeção, fim da ação e demais estados continuam sem overlay persistente. Nenhum novo clip Hit/Defeat foi produzido ou declarado validado nesta tarefa.

### Autoria e proveniência

Duas operações localizadas de **PixelLab Pro Flash inpaint**, fonte128×128 e máscara explícita, sem gerar personagens novos. Prompts/resultados completos e máscaras em `experiments/main-orc-polish-v1/`. Modelos, jobs e cobrança registrados nos arquivos `sword-cloud-record.json` e `axe-cloud-record.json`.

Além dos impactos, uma linha diagonal residual em fundo transparente no corpo do antigo Sword4/novo5 foi apagada via Lua no Aseprite (world x160..184,y99..121 e pixel isolado[181,93], total31 posições RGBA). Corpo, luva e arma real foram inspecionados separadamente. Essa correção não gerou custo e mantém o master v3 intacto. Evidências antes/depois: `crossing-residue-inspection.png` e `crossing-cleaned-inspection.png`.

Os resultados alteram 1411 posições RGBA no Sword5 e 1879 no Axe5, dentro da máscara. Cabeça, botas, mão e região ao redor do grip são protegidas e verificadas exatamente. O pedido buscou pequena compressão/participação de quadril, joelho e ombro; não se afirma uma translação rígida exata de2/3px. A alteração é sutil e inclui tratamento de clusters, não uma reconstrução anatômica. Os pixels aprovados fora da máscara são reaplicados por regra no próprio Aseprite, mesmo com a garantia do serviço.

Toda montagem, retoque, trace de dedos, alteração de duração, gravação de mestres e exportação ocorreu dentro do **Aseprite 1.3.18.6**, por Lua em batch oculto com perfil isolado e `--noinapp`. Não é desenho manual. Python/PIL foi usado somente para organização, hashes e folhas/capturas de QA, sem autoria raster externa. Nenhuma janela aberta ou trabalho não salvo do criador foi controlado.

## C. Revisão artística

Inspeção primária: poses reais, máscara/resultados de impacto, pegadas8× e capturas do preview1× e0,25×. A recuperação da espada distribui melhor a retração; a antecipação e o impacto do machado têm acentos diferentes. A alteração corporal é deliberadamente limitada, preservando as poses boas e o desenho atual. A ausência de deslocamento dos pés evita deslizamento novo; não comprova por si só transferência de peso convincente.

Revisão independente concluída por outro agente conforme autorização expressa do criador: `experiments/main-orc-polish-v1/independent-artistic-qa.md`. Confirmou melhora de ritmo, recuperação e transições; pegadas e identidade preservadas. Detectou o resíduo da espada e um pixel isolado em world[181,93], ambos removidos no Aseprite e reinspecionados. Não identificou bloqueio artístico significativo remanescente. Transferência de peso ainda é discreta: oportunidade subjetiva futura, sem alegar biomecânica totalmente resolvida. Playback independente 1×/0,25× e sequência completa foram vistos antes da limpeza; a reinspeção final foi localizada nos body/arma/composite sem cache. Aprovação técnica ou parecer do agente nunca equivale à aceitação artística do criador.

Limites de avaliação: somente front_r, fundo de inspeção, sem alvo ou contato em jogo. A rotação nearest-neighbor da arma e a ocultação discreta ainda podem ser perceptíveis em câmera lenta. Compatibilidade de itens precisa respeitar largura de cabo/guarda, proporção, câmera e mãos; o teste de substituição não aprova visualmente qualquer arma. Não se declara o conjunto final para todas as raças/classes ou pronto no runtime.

## D. Validação e custos

| Verificação | Resultado |
|---|---|
| Exportador Aseprite existente |10 jobs / 92 quadros comparados, PASS|
| Reexportação dos mestres salvos |Mesmo build imutável, PASS|
| Verificação focada de arte/metadados |105 verificações, PASS; `technical-qa.json`|
| Fontes anteriores |9.796 PNGs/mestres preservados por SHA256|
| Metadados ativos de corpo/armas |Exatos; candidato não substitui `equipment-current.json`|
| Preview real |62 quadros/canvas e recortes de grip comparados, zero diferenças|
| Sequência/completar sem loop |Antes/depois retornam ao Idle sem overlay, PASS|
| Abertura local e responsividade |file:// carrega; mobile390px sem overflow|
| Biblioteca |202 cópias por hash, 179 links locais, página v3 anterior intacta|
| Suite do projeto |`node --test --test-concurrency=1`:14/14 PASS|
| Substituição de itens existentes |Sword11 eAxe12 recompostos, zero redesenhos/gerações|
| Unity e outras direções |NOT_RUN, fora do escopo|

O teste de reutilização usa os assets menores v1 já existentes apenas como **fixtures técnicas**, não como proposta artística ou novas armas de produção. Evidências: `reports/main-orc-polish-v1/reuse/{Sword|Axe}/reuse.json`. O mesmo corpo, dedos e duração são reaproveitados ao trocar o item compatível da categoria.

Custos externos: **2 chamadas, 6 gerações efetivamente cobradas cada, total 12 gerações PixelLab**, sem novo lote ou retentativas pagas. Jobs `f077ce3b-656d-4a98-badf-4eff1045fe3b` e `5c4b8882-c612-4ddb-bc2c-2eb7ad646481`. Não foi obtido preço monetário por geração; não estimamos reais/dólares ou consumo de tokens não medido. Reaproveitamento e testes locais não chamam geração.

Evidências: `experiments/main-orc-polish-v1/{technical-qa,preview-qa,library-qa}.json`, `build.json`, capturas normal/lenta, fontes do estudo de tempo e pedido original `creator-task.md`.

## E. Materiais de revisão

Abra **`Biblioteca de Arte/Estudos Comparativos/Orc principal - Polimento de combate/index.html`**. A biblioteca principal também lista o candidato, preservando o link da base v3.

Na mesma página: Espada antes/depois, Machado antes/depois, modo somente ataques ou Idle→Attack→Idle, velocidades1×/0,5×/0,25×, pausar, avançar quadro, repetir/desligar loop, zoom nativo/2×/3×, pegada8× e galeria de poses/tempos. O contorno dourado identifica o impacto no canvas de revisão; não faz parte do PNG ou de um evento de dano. Não há suavização ou frames inventados no preview.

Fontes portáteis em `Ataques/{Espada|Machado}/`, comparação com a base em `Comparacao/Antes - {Espada|Machado}/`, armas independentes em `Armas/`. Cada ataque tem mestre composto, corpo, dedos, folha, clip e perfil. O original v3 continua em `Biblioteca de Arte/Personagens Jogaveis/Orc V1/index.html`.

## F. Segurança, Git e continuidade

Estado inicial já continha numerosas mudanças locais. Registro: `experiments/main-orc-polish-v1/initial-git-status.txt`; arte protegida e cópia portátil completa da base em `protected-art.json` e `baseline-review/`; metadados ativos em `baseline-metadata/`. Não houve reset, limpeza destrutiva, commit, push ou escrita em `../TacticsRPG`.

Escopo desta tarefa: novos mestres/exports isolados, estudo/QA local, ponteiro de candidato, extensão pequena do preview/compositor, este documento e notas em AGENTS, handoff, roadmap e registro da biblioteca. Mudanças anteriores em runtime/configuração/fábrica não foram revertidas nem atribuídas a este passe. O diff do repositório inteiro inclui trabalho anterior; não representa apenas esta tarefa.

Orc V1 mantém autoridade. Armas continuam independentes e a política é somente no ataque. Nenhum gate, receita de produção, seleção de equipamento, registro de personagem ou GUID Unity foi autoaprovado/substituído. Infante de Ferro permanece atual; Vigia/Matriarca seguem na categoria separada de ideias futuras para únicos jogáveis e/ou NPCs.

## G. Aceitação e próximo marco

- **Implementado:** polimento incremental dos dois ataques e preview comparativo.
- **Validado tecnicamente:** exportações, referências, duração, visibilidade, reutilização e preservação descritas acima.
- **Revisado visualmente:** evidências primárias e parecer independente concluído; resíduo corrigido e reinspecionado.
- **Aprovação artística do criador: PENDENTE.** Nenhuma promoção ou propagação automática.

Depois da avaliação do criador, registrar decisão explícita e só então considerar selecionar este candidato. Outras vistas e futura integração no jogo são tarefas separadas. Não recriar o sistema de equipamentos para resolver problemas locais de animação.

### Reproduzir sem gastar gerações

```text
node tools/polish-main-orc.mjs build
node src/cli.mjs editor-export --manifest characters/orc-v1/source/aseprite/onehanded-polish-v1/editor.json
node tools/compose-main-orc-item.mjs Sword experiments/orc-v1-weapons-v2/preserved-v1/weapons/recruit-sword/weapon.json reports/main-orc-polish-v1/reuse/Sword characters/orc-v1/source/onehanded-polish-v1/Sword/Attack/profile.json
node tools/compose-main-orc-item.mjs Axe experiments/orc-v1-weapons-v2/preserved-v1/weapons/militia-axe/weapon.json reports/main-orc-polish-v1/reuse/Axe characters/orc-v1/source/onehanded-polish-v1/Axe/Attack/profile.json
node --test --test-concurrency=1
```

Com Python local disponível: `experiments/main-orc-polish-v1/check-polish.py` valida os contratos; `tools/build-main-orc-rescue-review.py --polish` reconstrói a página a partir dos PNGs reais. `tools/build-art-library.py` atualiza a navegação. O modo `prepare` recria o estudo/inputs/solicitações, **não envia** chamadas pagas. As duas imagens de retoque já baixadas são os inputs congelados do modo build. Não rodar scripts antigos de promoção de V4/v1/v2.
