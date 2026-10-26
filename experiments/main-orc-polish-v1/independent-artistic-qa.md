# QA artística independente — Main Orc / polish v1

Revisor: agente separado `/root/artistic_qa`. Data: 2026-10-25. Parecer de revisão, **não aprovação do criador**. Baseline v3 permanece a referência ativa; este documento não promove candidatos.

## Escopo e método

Revisados os PNGs realmente exportados, strips de candidatos, crops de mãos e comparação dos dois patches corporais. Também executei a página comparativa em Chromium local, por HTTP, e capturei independentemente mudanças de quadro do canvas durante reprodução real a 1x e 0,25x, sem loop. Todos os 11 quadros de espada e 12 de machado apareceram. Executei a sequência Idle → Attack → Idle a 1x e examinei seus limites, inclusive retorno ao Idle desarmado.

O julgamento usa essas sequências capturadas e os tempos declarados, não uma observação humana contínua de vídeo nem um teste no jogo. O sampling apresenta pequena variação temporal do navegador; não serve para medir latência de gameplay. A revisão não depende dos resultados dos testes técnicos. Nenhum asset foi alterado pelo revisor. A limitação inicial de leitura de canvas em file:// foi contornada com servidor HTTP e não constitui defeito visual da página.

## Resultado e problemas confirmados

O polimento preserva a identidade e as boas poses da v3. O ganho mais claro é a organização temporal e espacial: preparação legível, aceleração curta, impacto sustentado e retorno menos brusco. Não confirmei nova cabeça desproporcional, mão evidentemente solta, troca de paleta ou salto arbitrário de profundidade da arma.

**Defeito confirmado e corrigido durante esta revisão:** o quadro Sword 5, `crossing`, conservava uma segunda linha diagonal fina cinza/clara atrás e acima da espada verdadeira. A separação body / weaponFront / composite demonstrou que a linha estava no body, não na arma. Crop composto x154–192 / y94–144 (canvas nativo do personagem: aproximadamente x90–128 / y30–80). Era um resíduo visual, não um efeito de movimento deliberado. O autor confirmou herança do antigo Sword 4 e limpou somente esse ramo no Aseprite. A reinspeção final confirmou a limpeza sem regenerar pose ou espada.

## Espada — classificação por quadro, índice zero

| Quadro | Classe | Parecer |
|---|---|---|
| 0 rest | KEEP | Repouso desarmado coerente com o Idle. |
| 1 establish-grip | KEEP | Estabelece a arma na mão atual antes de elevar o braço; escala e direção plausíveis. |
| 2 load | KEEP | Transição para carga preservada. |
| 3 high-guard | KEEP | Boa pose, agora funciona como antecipação sustentada. Não redesenhar. |
| 4 drive | KEEP | Deslocamento grande funciona como aceleração curta; não necessita interpolação indiscriminada. |
| 5 crossing | MINOR_POLISH → KEEP | Resíduo diagonal no body removido e reinspecionado; luva, antebraço e arma real preservados. |
| 6 strike-follow-through | KEEP | Impacto mais legível pela relação entre aceleração curta e hold. Patch corporal é discreto. |
| 7 recovery-bridge | KEEP | Reutilização da pose do mesmo Orc é coerente. Diminui o recuo brusco; grip/guarda plausíveis no crop. |
| 8 recovery | KEEP | Bom retorno após o novo bridge. |
| 9 action-complete | KEEP | Corpo permanece na pose anterior quando a arma some. Evita somar salto corporal ao desaparecimento. |
| 10 return-unarmed | KEEP | Retorno para Idle consistente, sem arma residual. |

Não foi confirmado um problema de penetração de guarda ou desconexão da mão no novo bridge. Uma inspeção em crop não prova anatomia perfeita em toda ampliação, mas não há motivo visual suficiente para substituir a pose boa.

## Machado — classificação por quadro, índice zero

| Quadro | Classe | Parecer |
|---|---|---|
| 0 rest | KEEP | Desarmado, estável. |
| 1 establish-grip | KEEP | Aparição antes da subida do braço melhora o início. |
| 2 load | KEEP | Carga legível. |
| 3 raise | KEEP | Preserva desenho e ligação de ombro/braço. |
| 4 cocked-shoulder | KEEP | Hold maior diferencia o peso do machado; manter arte. |
| 5 release | KEEP | Liberação curta torna a aceleração mais convincente. |
| 6 impact | KEEP | Hold de impacto agora se distingue da liberação; sem regressão corporal evidente. |
| 7 follow-through | KEEP | Continuidade consistente após o contato. |
| 8 recovery | KEEP | Machado baixo e mão recuperando são legíveis; não confirmei penetração da cabeça no joelho. |
| 9 action-complete | KEEP | Remove a arma sem alterar simultaneamente o corpo ou inverter profundidade. |
| 10 after-attack-settle | KEEP | Assentamento desarmado funciona. |
| 11 return-unarmed | KEEP | Alinha com o retorno ao Idle. |

## Peso, impacto e limites das melhorias

A espada de 690 ms se lê mais rápida e o machado de 1055 ms se distingue pela preparação mais longa. Os holds de impacto não transformam os dois golpes em uma mesma animação. A espada deixou de recolher diretamente da extensão até perto da cintura: o bridge fornece progressão espacial mais razoável.

Os patches de tronco/quadril são pequenos e não provocaram mudança evidente de rosto, equipamento ou anatomia. A melhoria de esforço corporal é **sutil**. Ainda há pouca transferência ampla de centro de massa e pouca mudança do apoio dos pés: isto é uma oportunidade artística subjetiva de evolução, não uma falha nova comprovada nem justificativa para reconstruir o conjunto nesta tarefa. Não declarar biomecânica refeita ou peso físico plenamente resolvido.

O desaparecimento da arma continua instantâneo, por política attack-only, mas ocorre em corpo estável. A 0,25x a breve pose desarmada de conclusão é perceptível; a 1x não identifiquei quebra significativa no retorno. Não se deve introduzir saque/embainhamento ou Idle armado para esconder esse limite.

## Encaminhamento

A limpeza localizada de Sword 5 foi confirmada. O conjunto pode ser apresentado ao criador como candidato de polimento, com a ressalva sobre esforço corporal discreto. Não recomendo novas gerações, mudança de proporções, troca das poses de guarda ou ampliação do escopo. Não restou bloqueio artístico significativo confirmado nesta revisão. A aprovação final continua exclusivamente com o criador; esta revisão não concede Gate artístico nem valida integração Unity.

## Reinspeção da limpeza

Primeira reexportação inspecionada diretamente, além do crop `crossing-cleaned-inspection.png`: o ramo diagonal foi removido e a luva permaneceu íntegra. Restou um pixel isolado em world **[181,93]**, RGBA [141,142,143,255], pertencente ao extremo superior do resíduo. Encaminhado ao autor e removido no Aseprite.

Reexportação final informada pelo autor: build `3b6384933314a2bb64f9`. Recarreguei diretamente os PNGs body / weaponFront / composite, com cache-busting, e inspecionei o mesmo crop ampliado: ramo removido e conexão da luva preservada. Conferência adicional de leitura de pixels confirmou [181,93] transparente e nenhum pixel opaco na região x170–189 / y90–98. Os cinzas próximos à luva permanecem ligados à anatomia/guarda e não justificam limpeza ampla. Não repeti toda a reprodução após essa remoção estritamente local; as conclusões de ritmo e continuidade referem-se à sequência imediatamente anterior, cuja única mudança artística posterior declarada foi essa limpeza.
