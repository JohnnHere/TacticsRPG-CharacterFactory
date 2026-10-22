# Evolucao e retomada da Character Factory

Atualizado em 2026-10-19. Este arquivo orienta as proximas etapas entre conversas. O contexto persistente esta em AGENTS.md, docs/, referencias, receitas e pacotes de personagem. Ao abrir esta pasta como projeto, um agente com acesso a esses arquivos deve recuperar esse contexto antes de agir. Em outras ferramentas, anexar handoff/context.md, prompt.md e as imagens listadas.

## Como retomar

Pedidos suficientes: "continue a pipeline pela proxima etapa", "crie o conceito do orc-01", "ajuste a roupa do Orc Archer conforme minha revisao" ou "avance as melhorias tecnicas enquanto reviso o personagem". O agente le este arquivo, executa doctor e consulta as fichas e revisoes. Escolhe a primeira tarefa elegivel e informa o resultado a revisar. Autorizacao para desenvolvimento local permanece valida; decisao artistica explicita e exigida somente nos marcos documentados. Aprovacao de conceito nao autoriza integracao no Unity.

Ao terminar uma sessao, atualizar a tarefa executada, pendencias e proxima entrega revisavel. Nao marcar concluido por planejamento ou por teste tecnico quando a tarefa exige arte. As decisoes em reviews.json e hashes atuais sao a evidencia do personagem; esta lista e um resumo de planejamento.

## 1. Base tecnica — implementada

### Trabalho ativo: Orc nas outras sete classes basicas

Pedido vigente do criador: produzir as demais classes basicas aproveitando ao maximo o Orc Warrior para economizar tempo e tokens. Escopo confirmado pelo catalogo e pelo original Unity em leitura: Squire, Archer, Apprentice Mage, Acolyte, Rogue, Scout e Brawler. Sao variantes de roupa do MESMO individuo, nao sete novos Orcs. Warrior aprovado/exportado permanece intacto.

Ampliacao vigente apos feedback positivo do criador: auditar equipamentos nos dois repositorios, criar padrao faltante e garantir ataque basico desarmado separado das habilidades. Auditoria real de17 fontes do jogo e cinco contratos locais registrada em reports/equipment-source-audit-v1.json; jogo apenas lido. Padrao criado em docs/EQUIPMENT_AND_ACTIONS.md/config/equipment-actions-v1.json. A ausencia de arma no desenho nao torna uma puxada de arco ou conjuracao um soco.

- [x] Validar reuso das quatro vistas de ataque fisico do Warrior e Brawler (40 quadros existentes), sem copias ou alteracoes.
- [x] Produzir primeiro lote unarmed front_r nas seis outras roupas:30 PNGs novos/seis editaveis, LibreSprite RGBA/duracoes identicos, propria paleta/128RGBA8/ground126/alfa binario. Squire usa fonte/suplementov2 corrigidos; tentativas com ombreira trocada preservadas fora da selecao ativa.
- [x] Preview characters/review-orc-unarmed-front-v1.html com40 referencias de quadro nas oito roupas, incluindo reuso. Edge HTTP/file://,40/40 canvas RGBA exatos, controles verificados, zero erros JavaScript. Suite local9/9 PASS, tres testes novos da selecao offline por acao/equipamento.
- [x] Criador aprovou primeiro lote unarmed front_r: "Aprovo os ataques desarmados; continue as outras vistas." Evidencia/hash dos30 PNGs e seis fontes em orc-unarmed-front-approval-v1.json e source/unarmed-front-v1-review.json; sem autoaprovar consistencia final.
- [x] Produzir90 PNGs e18 fontes editaveis unarmed front_l/back_r/back_l nas seis roupas;32/32 clipes completos,160 referencias com120 PNGs novos/24 fontes e40 quadros reutilizados. LibreSprite90 novos RGBA/duracoes identicos, baseline e front_r aprovado intactos.
- [x] Previa conjunta review-orc-actions-complete-v1.html com oito roupas/seis acoes/quatro vistas. Edge:896 referencias carregadas HTTP/file://,896/896 canvas RGBA exatos, controles verificados, zero erros JavaScript; npm9/9 PASS.
- [x] Criador autorizou continuar condicionado ao hit/ataque desarmado: condicao verificada nas quatro vistas; sete Gates consistency registrados e suplemento aprovado. Implementada/verificada exportacao completa com suplemento; oito pacotes (incluindo Warrior referencia),896 PNGs/216 fontes editaveis, ZIP verificado. Evidencia em docs/ORC_PRODUCTION_EXPORT_V1.md. Exportador legado nao inclui actions/. Overlays, sockets, mascaras e gameplay desarmado no Unity continuam pendentes.

Matriz vigente:characters/orc-equipment-actions-v1.json; readiness:reports/orc-equipment-readiness-v1.json. Oito Orcs x quatro vistas exigem32 clipes unarmed;32 fontes nativas disponiveis,0 faltantes (0 quadros). Nenhum binding de arma provado. Original WeaponKind tem apenas Sword/Axe/Bow, default0=Sword; nao usar null/default como implementacao ficticia de desarmado. Detalhes de fontes, reuso, correcoes e proxima etapa em docs/ORC_UNARMED_DIRECTIONS_V1.md.

- [x] Criar seis fichas novas e retomar/atualizar a ficha Archer; identidade, appearance e referencia da base aprovada preservadas.
- [x] Gerar e importar sete conceitos reais image_gen, uma chamada por Job; prompts, referencias e hashes registrados. Todos em characters/orc-01-<job>/concepts/outfit-concept-v1.png. Sem armas e sem autoaprovacao.
- [x] Criar characters/review-orc-basic-classes-v1.html com o Warrior e sete variantes; verificar oito imagens, filtros e fundo no Edge local, sem erros JavaScript. Evidencias em characters/orc-basic-review-browser.json/.png.
- [x] Indexar os 97 PNGs e 20 clipes editaveis aprovados do Warrior por caminho/hash, sem duplicar fontes: characters/orc-basic-shared-source-index.json. Reuse Assessment por componente nas sete fichas.
- [x] Registrar aprovacao explicita dos conceitos: criador aprovou seis roupas e rejeitou Rogue v1 por semelhanca com Warrior. Rogue v2 com capuz e roupa carvao furtiva foi aprovado depois: "Aprovo o Rogue v2; siga com os sprites." Sete Gates concept vigentes; Rogue v1 historico rejeitado.
- [x] Produzir primeiras bases front_r: 14 PNGs (7 poses + 7 fallbacks), 128x128 RGBA8, altura100, ground126, 47–48 cores por roupa, alfa parcial zero. Sete fontes .aseprite com export LibreSprite RGBA identico. Base: 10 PASS/0 FAIL por pacote, aviso esperado fallback duplicado.
- [x] Primeiras bases aprovadas pelo criador: "Aprovo as sete bases; produza as outras vistas." Evidencia parcial front_r por SHA256 em cada source/native-base-v1/front-r-review.json. Essa decisao nao aprova outras vistas ou animacoes.
- [x] Produzir outras tres vistas por classe: 21 PNGs novos, total35 PNGs estaticos e 28 editaveis. Sete folhas image_gen + tres correcoes individuais; sem espelhamento, paleta da propria roupa e bases aprovadas intactas. Directions: 175 PASS/0 FAIL, sete avisos esperados fallback duplicado. LibreSprite: 28/28 fontes RGBA identicas apos export.
- [x] Criador aprovou as quatro vistas: "Aprovo as vistas das sete classes; continue as animações." Sete Gates base registrados com evidencia real e digest atual em reviews.json.
- [x] Primeiro lote Idle4/Walk6 front_r produzido nas sete roupas: 70 PNGs animados e 14 editaveis, paleta por roupa, alfa binario, ground126 e Idle com bob <=2px. LibreSprite: 70/70 quadros e duracoes identicos; navegador: 70/70 canvas RGBA identicos aos PNGs, controles e file:// verificados, zero erros JS.
- [x] Criador aprovou Walk front_r das sete classes; evidencia e hashes dos 42 quadros registrados em source/locomotion-front-v1/review.json.
- [x] Idle v2 aprovado: "Aprovo o Idle v2; continue as demais vistas." Evidencia/hashes em characters/orc-front-locomotion-approval-v2.json e registros parciais dos sete pacotes.
- [x] Produzir Idle/Walk nas outras tres vistas:210 quadros e42 editaveis novos;280 quadros/56 clipes no conjunto completo de locomocao. Native/paleta/proveniencia e LibreSprite RGBA+duracoes sem falhas. Front_r aprovado intacto.
- [x] Criador aprovou Idle/Walk nas tres vistas novas: "Aprovo as três vistas animadas; continue o combate." Evidencia/hashes nos sete source/locomotion-directions-v1/review.json e indice orc-locomotion-directions-approval-v1.json.
- [x] Produzir Attack5/Hit3/Defeat5 front_r por Job:91 novos PNGs e21 editaveis, com gestos de ataque distintos. LibreSprite91/91 RGBA e duracoes identicos; navegador91/91 canvas RGBA exatos, zero erros JS.
- [x] Criador aprovou primeiro combate: "Aprovo o combate front_r; continue as outras vistas." Evidencia e hashes em orc-combat-front-approval-v1.json e nos sete source/combat-front-v1/review.json.
- [x] Produzir273 quadros e63 editaveis nas outras tres vistas de combate, sem espelhamento. Inventario corporal completo:679 PNGs/168 fontes editaveis ativas. CLI full:3423 PASS/0 FAIL; sete avisos esperados de fallback. LibreSprite e navegador:644/644 quadros animados RGBA identicos; duracoes, controles e file:// verificados. Seis testes locais aprovados.
- [x] Preservar371 quadros animados e105 fontes editaveis anteriormente aprovados,35 PNGs estaticos e Warrior97 PNG/20 editaveis, com comparacao de hashes. Reutilizar referencias de poses validas somente em adaptacoes demonstradas visualmente. O Warrior possui quadros raster completos, sem corpo nu separado sob a armadura; nao existe rig de troca de roupas.
- [x] Consistencia artistica final conjunta aprovada condicionalmente; hit/desarmado presentes, aprovacao registrada em characters/orc-actions-complete-approval-v1.json e sete reviews.json. Pacotes e suplemento exportados. O criador gostou da baseline e pediu a extensao de equipamentos/ataque desarmado antes do fechamento. Os97 PNGs/24 editaveis legados por classe permanecem fingerprintados em source/complete-v1/review.json. Gate consistency e exportacao agora concluidos, conforme evidencia da resposta mais recente.
- [ ] Produzir assets independentes de armas/projeteis/VFX e extensoes runtime de overlays/casts/tiro sincronizado em tarefa propria. Os gestos do corpo por Job e os socos desarmados foram aprovados e exportados.

Baseline preservada:679 PNGs nativos e168 fontes editaveis (28 estaticas +140 animadas) nas sete variantes, mais o Warrior ja aprovado/exportado. Isso nao comprova todos os ataques por equipamento. Extensao atual:120 PNGs e24 editaveis adicionais ativos unarmed, com reuso de fontes originais Warrior/Brawler. Plano raiz aponta EXPORTED_LOCAL_BODY_AND_UNARMED. Conceitos/bases, locomocao completa e combate front_r legados aprovados; Gate consistency e exportacao das sete variantes concluidos. Proximo: armas/projeteis/VFX independentes e bindings demonstrados, com revisoes artisticas. Integracao Unity exige tarefa autorizada separada. Armas/efeitos, bindings e integracao Unity permanecem pendentes.

- [x] Repositorio local independente e comandos Node instalados.
- [x] Contexto do TacticsRPG e skill copiados com hashes; ancora e Hero documentados com papeis distintos.
- [x] Catalogos de 28 racas e 63 Jobs.
- [x] Fichas, variantes de roupa, pacotes para geracao pela LLM, importacao e previews.
- [x] Composicao de camadas 2D nativas, validacao, revisoes por hash e staging Unity.
- [x] Receitas raciais/de Job com versoes e imagens aprovadas arquivadas.
- [x] Testes de comandos, integridade, composicao, gates e exportacao com fixtures sinteticas.

## 2. Primeiro ciclo artistico — proximo trabalho

1. [x] Preencher propostas visuais e gerar conceito candidato weapon-independent de orc-01 em concepts/ (2026-10-19). Concept-07 é a versão escolhida e aprovada pelo criador; ver Gate 1 em reviews.json.
2. [x] Concept-07 careca escolhido e aprovado pelo criador em 2026-10-19; Gate 1 registrado com hash. Anteriores preservados como históricos.
3. [x] Produzir base nativa e quatro vistas candidatas: 5 PNGs 128x128 RGBA, 100px de altura, ground126, mesma paleta; validação directions sem FAIL. Revisão artística permanece no item 4.
4. [x] Base e quatro vistas aprovadas explicitamente pelo criador: "Aprovo a base e as quatro vistas; continue as animações." Gate base registrado com hash atual em reviews.json.
5. [x] Criar conceito de roupa Archer do MESMO individuo em orc-01-archer; conceito aprovado e primeira base front_r nativa produzida, em revisao junto das outras seis classes.
6. [ ] Documentar e aprovar receitas visuais de Orc/Warrior/Archer com regras e referencias reais. Apenas candidatos de regras ate a decisao do criador.
7. [ ] Criar conceito de undead-01 Archer usando a receita Archer aprovada, com anatomia racial propria. Revisao: classe reconhecivel entre racas, mesma linguagem global.

## 3. Prova de producao — conjunto aprovado e exportado

- [ ] Demonstrar fonte editavel 2D e roupa em camadas nativas compativeis numa vista, com ordem/oclusao documentadas.
- [x] Produzir Idle e Walk nas quatro vistas; revisao artistica do conjunto aprovada pelo criador.
- [x] Produzir Attack/Hit/Defeat nas quatro vistas. Tiro de arco/cast requer desenho e analise de playback proprios.
- [x] Validar os 97 PNGs: 489 PASS, 0 FAIL, 1 aviso esperado (fallback igual a front_r). Vinte clipes editaveis verificados por roundtrip RGBA e duracao no LibreSprite; seis testes locais aprovados.
- [x] Registrar revisao artistica de consistencia: "Aprovo o conjunto completo; exporte o pacote." Gate consistency vigente em reviews.json.
- [x] Exportar pacote aprovado para dist/orc-01/9b89aad88c27de68 e verificar 97 PNGs contra manifesto/hashes. Importador fornecido; compilacao Unity ainda NOT_RUN.

## 4. Melhorias tecnicas que podem acompanhar as revisoes

Estas tarefas sao backlog; as funcoes ainda nao foram implementadas.

- [ ] Comando status: mostrar personagem, revisoes atuais/desatualizadas, arquivos faltantes e proxima acao, derivando os JSONs existentes.
- [ ] Comparacao visual lado a lado entre versoes/roupas/racas e entre referencias de um mesmo Job.
- [x] Preview de animacao Orc com cinco estados, quatro vistas sincronizadas, velocidades, scrubbing e pausa; 92 quadros carregados sem erros de JavaScript no Edge. Generalizacao para outros pacotes continua no backlog.
- [ ] Exportacao assistida do editor 2D e perfis adicionais com contratos explicitos.
- [ ] Preparar migration/versionamento de fichas antes de mudar schemaVersion.
- [ ] Definir pacote compartilhado de assets de armas e estender o runtime para exibi-las separadamente somente quando equipadas e invocadas por uma acao; validar encaixe, oclusao e sincronizacao. O contrato visual esta decidido, a implementacao nao.

Se o usuario pedir para continuar engenharia enquanto avalia arte, partir da primeira tarefa desta secao ainda pendente. Conservar os marcos artisticos e registrar que a implementacao tecnica nao aprovou nenhum desenho.

## 5. Integracao no jogo — tarefa futura autorizada separadamente

- [ ] Auditar o codigo atual do jogo novamente e definir registro minimo multi-personagem para UnitVisuals.
- [ ] Integrar um pacote aprovado em ../TacticsRPG/Assets/Resources/Characters/<id>/ preservando GUIDs.
- [ ] Compilar o importador, confirmar Resources.Load/importacao e executar revisao PlayMode.
- [ ] Registrar aprovacao final em jogo pelo criador.

O staging local ja esta implementado. O registro multi-personagem e a integracao real ainda estao pendentes. Camadas de equipamento no runtime e novos estados sao extensoes futuras; combinacoes completas compostas offline sao o fluxo inicial.

## Estado dos exemplos na entrega

| Pacote | Conteudo atual | Proxima entrega |
|---|---|---|
| hero-reference | 97 PNGs historicos, preview, relatorio; reference_only | Consultar como referencia; 34 divergencias de chao registradas, sem retoque automatico |
| orc-01 | Concept-07 careca e base aprovados; 97 PNGs nativos, 20 clipes animados editaveis e 4 fontes estaticas; prompts/fontes/hashes preservados | Conjunto aprovado e exportado em dist/orc-01/9b89aad88c27de68. Integracao Unity, PlayMode e armas independentes permanecem pendentes. |
| orc-01-archer | Baseline97 PNGs/24 editaveis +20 PNGs/4 editaveis unarmed; primeiro front_r desarmado aprovado | Conjunto/suplemento aprovados e exportados; proximos assets de armas e bindings |
| orc-01-squire / apprentice-mage / acolyte / rogue / scout / brawler | Baseline97 PNGs/24 editaveis por roupa; +20 PNGs/4 editaveis unarmed por roupa exceto Brawler, que reusa Attack; prefixo completo orc-01- em cada ID | Conjunto/suplemento aprovados e exportados; proximos assets de armas e bindings |
| undead-01 | Ficha Archer e handoff; conceitos ausentes | Conceito com receita Archer aprovada |

## Historico

- 2026-10-19: criador aprovou quatro vistas das sete classes e autorizou animacoes; Gates base registrados. Primeiro lote real Idle/Walk front_r:70 quadros,14 clipes editaveis. Reuso das dez poses Warrior como guia neutro de silhuetas e ferramentas existentes; novas roupas realmente desenhadas pela image_gen. Primeira fonte Squire rejeitada por herdar armadura Warrior; Scout Idle original selecionado, Walk corrigido com guia anotado apos uma edicao rejeitada por manter/duplicar manta no quadril errado. Dez chamadas reais nesta etapa; PNGs/prompts/referencias/origens/recortes/hashes preservados. Verificacao nativa e de proveniencia sem falhas; LibreSprite70/70 RGBA e duracao identicos; Edge70/70 canvas RGBA identicos em HTTP e exibicao file://, zero erros JS, servidor local encerrado. Total105 PNGs/42 editaveis; restante574 quadros. Primeiro lote aguarda revisao artistica antes das demais vistas; consistency/export/Unity pendentes.

- 2026-10-19: criador aprovou as sete primeiras bases para expandir outras vistas. Evidencia parcial com hashes preservada, sem autoaprovar Gate base completo. Produzidas 21 vistas novas via sete folhas e tres correcoes (Squire front_l, Mage back_l, faixa Brawler back_l). Todas importadas com prompts/fontes/hashes reais; paleta comum por roupa, alfa binario, altura100/ground126, frontais aprovadas intactas. 35 PNGs no total e 28 editaveis conferidos no LibreSprite RGBA identico. Validacao175 PASS/0 FAIL; preview Edge com 28 vistas/filtros/zoom/fundo e zero erros JS. Quatro vistas aguardam revisao conjunta; Gate base, animacoes das roupas, export e Unity ainda pendentes.

- 2026-10-19: criador aprovou seis roupas e pediu Rogue mais escuro/furtivo; Rogue v2 gerado/importado e depois aprovado explicitamente. Sete fontes novas de sprite image_gen, usando conceito aprovado + Warrior nativo como referencias, sem reduzir conceitos. Processamento Pixel Art Fixer forced/100px/paleta48; 14 PNGs importados pelo CLI com hashes/prompts reais. Sete fontes .aseprite exportadas no LibreSprite e verificadas RGBA identico. Preview testado no Edge: oito nativos e oito conceitos carregados, zoom1x/2x/3x, fundo e zero erros JS. Relatorios em characters/orc-native-base-*.json; fontes em cada source/native-base-v1. Primeiras bases aguardam criador antes das demais vistas. Nenhum Gate base/consistency/in-game autoaprovado; nenhuma escrita no jogo.

- 2026-10-19: pedido de producao das outras classes basicas Orc com economia por reuso. Produzidos sete conceitos distintos e preservada a arte aprovada Warrior. Reuso planejado com evidencia por componente; fontes do Warrior indexadas sem copias redundantes. Alpha original dos conceitos preservado (inclusive pixels parciais/perifericos; nao adequado a runtime sem autoria nativa). Conferencia dos sete conceitos RGBA/procedencia e preview real sem falhas; Gate 1 solicitado numa unica revisao, ainda pendente. Nenhum sprite novo de variante, receita aprovada ou integracao Unity foi declarado/executado.

- 2026-10-19: criador aprovou explicitamente todo o conjunto animado e pediu exportacao. Gate consistency registrado com evidencia real; 97 PNGs exportados localmente em dist/orc-01/9b89aad88c27de68, com manifesto de hashes, validacao e importador opcional. Nenhuma integracao Unity ou aprovacao em jogo foi registrada.

- 2026-10-19: criador aprovou base e quatro vistas e autorizou continuar animacoes. Produzidos 92 quadros (Idle 16, Walk 24, Attack 20, Hit 12, Defeat 20), completando 97 PNGs 128x128 RGBA, paleta comum de 46 cores, alpha binario e ground126. Fontes artisticas novas image_gen, grade alvo explicita, registro e acabamento RGB documentado; modelo nao exposto pela ferramenta. Walk front_r usa selecao de poses de duas geracoes (tentativa intermediaria rejeitada); Attack back_l foi redesenhado para manter ataque com braco direito; materiais das pernas Walk corrigidos sem mudar silhueta. Historicos rejeitados preservados. Vinte arquivos animados .aseprite foram exportados no LibreSprite e comparados pixel a pixel e por duracao. Verificacao completa: 489 PASS/0 FAIL/1 aviso esperado; npm test 6/6; preview real testado em HTTP e file:// com 92 PNGs e cinco estados. Manifesto em source/animations-v1/manifest.json; relatorios em characters/orc-01/reports/. Revisao artistica de consistencia solicitada e pendente; exportacao e PlayMode ainda NOT_RUN. Nenhuma escrita no projeto Unity.

- 2026-10-19: decisao do criador: conceitos e sprites base de personagens ficam sem armas; armas sao assets separados e aparecem somente quando equipadas e invocadas por uma acao. O conceito armado anterior de orc-01 foi preservado como historico e uma versao weapon-independent foi gerada; Gate 1 continua pendente. Runtime ainda exige extensao.
- 2026-10-19: feedback do criador aprovou a armadura do Orc, mas pediu feicao mais selvagem/brutal e cabelo menos humano/arrumado. Gerado `concept-03` preservando armadura e mãos vazias; Gate 1 continua pendente.
- 2026-10-19: o criador aprovou a feição do conceito 03, mas pediu reduzir muito o volume do cabelo e afastá-lo de um penteado humano. Revisar apenas o cabelo; preservar rosto, armadura e mãos vazias.
- 2026-10-19: o conceito 04 reduziu o cabelo, porém a crista ainda foi lida como humana. Próxima revisão: apenas cerdas curtas e irregulares junto ao couro cabeludo, sem crista; manter rosto e armadura.
- 2026-10-19: o criador considerou o conceito 05 melhor, mas calvo demais. Ajustar para mais cobertura e volume moderado de cabelo curto, áspero e irregular; manter rosto e armadura.
- 2026-10-19: a pedido do criador, gerada variante totalmente careca `concept-07` para comparação. `concept-06` permanece candidato principal até escolha explícita; ambas as versões preservam rosto/armadura e ficam sem arma.
- 2026-10-19: gerado/importado `orc-01-warrior-concept-01.png` como candidato Orc Warrior, Job básico inicial com afinidade Orc. Prompt e referências foram registrados no pacote; Gate 1 segue pendente da revisão do criador.
- 2026-10-18: entrega da base tecnica, documentacao, referencias e quatro pacotes de exemplo. Nenhuma arte nova ou aprovacao de personagem produzida.
- 2026-10-18: instrucoes de continuidade, destinos automaticos e backlog de evolucao explicitados para retomada com prompts curtos.

- 2026-10-19: produção completa de concept-07 solicitada. Plano de 97 PNGs em characters/orc-01/source/production-plan.json. Primeira geração image_gen ignorou o pedido 128x128 e retornou 1254x1254: arquivada em source/orc-01-base-front-r-attempt-01.png, sem redução. Validação base FAIL: sprite nativo ausente. Próximo: produzir base nativa e revisar antes de expandir vistas/animações. Export/Unity NOT_RUN; armas independentes e runtime ainda exigem extensão.

- 2026-10-19: criador reiterou produção de TODOS os assets de produção Orc Warrior. Duas novas tentativas reais image_gen (02 e 03) buscaram desenho pequeno em canvas maior, para recorte sem reescala; ambas falharam em escala nativa, com alfa parcial excessivo, e 03 introduziu halo/alteração da armadura. PNGs e prompts preservados em source; relatórios em reports/base-attempt-02.json e base-attempt-03.json. Inventário full: 97 ausentes, 0 PNGs de produção aceitos. Pedido permanece incompleto por limitação de geração nativa; não depende de nova autorização do usuário. Necessária autoria 2D nativa que preserve concept-07. Nenhuma alteração Unity, export ou aprovação artística nova.

- 2026-10-19: autorização ampliada do criador para linguagens/dependências/ferramentas gratuitas. Instalados uv, Python 3.12.15, Pixel Art Fixer MIT (ef376e5) e LibreSprite 1.3 portátil. Solução executada: novas fontes artísticas para sprites + reconstrução estrutural de grade alvo explícita (forced), paleta nativa comum e registro. Produzidos fallback + 4 vistas em sprites (5/97); 4 fontes editáveis em source/pixel-grid-v1, roundtrip RGBA idêntico, reprocessamento front_r byte idêntico. Corrigida faixa traseira inconsistente de back_r; v1 preservada rejeitada. Directions: 25 PASS, 0 FAIL, 1 aviso esperado fallback duplicado; npm test 6/6. Preview concreto: characters/orc-01/review-base-v1.html. Gate base aguarda criador; nenhuma autoaprovação. Próximo: registrar revisão real, produzir/revisar Idle front_r e Walk front_r; depois outras vistas e combate. Armas independentes, export e Unity permanecem pendentes.

- 2026-10-19: feedback real do criador: Walk esta otimo; reduzir expansao exagerada do peitoral no terceiro Idle. Walk aprovado por hashes em sete registros parciais. Sete edicoes reais image_gen preservadas em source/idle-subtle-v2/, prompt e referencias com hashes; acabamento nativo local somente no torso do quadro02, silhueta limitada pela neutra +1pixel por lado no pico. Cabeca, maos e membros inferiores preservados; 63 outros quadros e sete editaveis Walk intactos. Originais em previous-idle/. Sete fontes Idle reconstruidas, exportacao LibreSprite28/28 RGBA+duracoes identicas; contrato/paleta/proveniencia70/70 e navegador70/70 canvas identicos, sem erros JS. Preview v2 pronto; somente Idle revisado aguarda criador. Total105 PNGs/42 editaveis e574 quadros restantes.

- 2026-10-19: criador aprovou Idle v2 das sete classes e autorizou demais vistas; evidencia e hashes parciais registrados. Produzidas21 folhas10 poses image_gen, apos uma tentativa30 poses cortada rejeitada, total22 chamadas reais. Fontes/prompts/referencias/recortes/processamento/hashes preservados. Novos210 PNGs e42 editaveis Idle/Walk front_l,back_r,back_l; conjunto280 quadros/56 clipes. LibreSprite210 novos RGBA e duracoes identicos; paleta/contrato/proveniencia e preservacao dos70 quadros/14 clipes front_r aprovados verificados. Edge280/280 canvas RGBA identicos, quatro vistas/dois estados, controles e exibicao file:// testados, zero erros JS; servidor fechado. Total315 PNGs/84 fontes editaveis ativas,364 quadros de combate pendentes. Review novo enviado antes de combate conforme WORKFLOW. Warrior e Unity intactos.

- 2026-10-19: criador aprovou as tres vistas de locomocao e autorizou combate; registros parciais atualizados por hashes, sem Gate consistency incompleto. Produzidos Attack5/Hit3/Defeat5 front_r nas sete classes:91 PNGs/21 editaveis. Onze chamadas image_gen reais: sete folhas13 poses e quatro edicoes de Attack Mage/Brawler; v2 rejeitadas por manter mao incorreta, v3 selecionadas apos guias explicitos de braco direito. Hit/Defeat originais preservados. Extrator aceita alturas relativas e registro por pelve opcionais para manter escala de bracos erguidos; importador/editor existente generalizado por --batch/--report. Native/paleta/proveniencia91/91; LibreSprite91/91 RGBA+duracoes identicos, Edge91/91 canvas exatos e parada final one-shot, exibicao file:// e controles, zero erros JS; npm6/6. Locomocao280 quadros/56 editaveis e Warrior97 PNGs/20 animados intactos. Ensaio legado preservou alpha/crop/registro6/6 mas detectou cores nao reprodutiveis no OpenCV; seed42 por asset corrigido para trabalho futuro, tres reconstrucoes iguais no mesmo ambiente; lote existente nao reprocessado. Total406 PNGs/105 editaveis ativos,273 quadros restantes. Review primeiro combate enviado conforme WORKFLOW; export/Unity ainda pendentes. Detalhes em docs/ORC_COMBAT_FRONT_V1.md.

- 2026-10-19: criador aprovou unarmed front_r;90 novos quadros e18 editaveis completaram front_l/back_r/back_l das seis roupas.26 PNGs reais image_gen nesta etapa,18 fontes selecionadas/oito tentativas preservadas: Squire corrigido para remover metal herdado, seis back_l redesenhadas com soco direito distante/oclusao, Rogue front_l com capuz restaurado. Guias de poses reais Warrior/roupas proprias reutilizados sem espelhamento ou alteracao da baseline.32/32 clipes unarmed nativos,160 referencias (120 novas/40 reutilizadas),24 novas fontes; zero quadros faltantes. Paleta/RGBA/proveniencia/roundtrip LibreSprite/hashes PASS; frente aprovada e baseline intactas. Previa final conjunta oito roupas/seis estados/quatro vistas:896 referencias carregadas,896 hashes RGBA canvas exatos HTTP, exibicao file:// e controles PASS, zero erros JS; npm9/9 PASS. Uma revisao final artistica enviada conforme Gate2. Exportacao suplementar ainda exige extensao, Gate consistency/export nao autoaprovados, nenhuma escrita Unity. Evidencias:docs/ORC_UNARMED_DIRECTIONS_V1.md.

- 2026-10-19: criador autorizou continuar se incluido hit normal desarmado; condicao verificada (soco fisico e reacao Hit nas quatro vistas). Sete Gates consistency registrados com evidencia literal, suplemento aprovado por fingerprint, Warrior original intacto. Exportador complementar implementado com bloqueio de aprovacao desatualizada/hashes/canvas/overlay e fontes escolhidas; baseline CLI preservada. Oito builds completos exportados com896 PNGs e216 fontes, hashes conferidos; reexecucao idempotente preservou builds. ZIP10.52MB,1186 entradas, CRC e1184 hashes +README/MANIFEST verificados. Doctor PASS; suite11/11 PASS. Previa/plans/docs atualizados para EXPORTED_LOCAL_BODY_AND_UNARMED. Detalhes e links em docs/ORC_PRODUCTION_EXPORT_V1.md. Armas/VFX/bindings e Unity continuam pendentes, sem escrita no jogo ou Gate3.
