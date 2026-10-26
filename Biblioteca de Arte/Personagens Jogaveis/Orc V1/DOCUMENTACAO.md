# Orc principal — resgate dos ataques de uma mão

Pedido vigente do criador, 2026-10-25. **Candidatas locais entregues para revisão artística.** Este documento substitui a política de armas permanentemente visíveis dos lotes v1/v2. Não confundir a versão do experimento de ataque com o antigo Orc V4: o personagem atual é `characters/orc-v1`, pele Verde Warcraft, identidade selecionada pelo criador para futura integração. V4 está descartada. Pedido original preservado em `experiments/main-orc-weapon-rescue-v3/creator-task.md`.

## A. Produção atual, fontes e auditoria

Conceito atual: `characters/orc-v1/concepts/concept-selected.png`; mestre `source/aseprite/concept-selected.aseprite`. Idle e Walk: `source/studies/<Idle|Walk>/clip.json`, com mestres `source/aseprite/idle-study.aseprite` e `walk-study.aseprite`. Idle5/2,2s é o padrão fixo aprovado; Walk16/1,28s é a locomoção atual. Não foram refeitos para esta tarefa.

Na abertura desta tarefa, o ponteiro equipment-current e a configuração apontavam para `source/equipment-v2/`, mas `character.json.equipmentPreview` ainda apontava para v1. As armas eram `assets/weapons/<recruit-sword|militia-axe>/source/v2/`, PNGs em sprites/v2 e weapon.json correspondente. Essas fontes e o preview foram auditados antes das novas edições. O `reviews.json` desta ficha está vazio: a seleção de identidade pelo criador não concede gates de quatro vistas ou runtime. Os ataques v1 e v2 estão rejeitados artisticamente.

Evidência da auditoria: `experiments/main-orc-weapon-rescue-v3/audit.json`; Git inicial no mesmo diretório; proteção SHA256 de 9669 PNGs/mestres anteriores em protected-art.json. Cópia portátil do preview anterior em previous-review/ e metadados anteriores em before-metadata/. Nenhum reset, limpeza destrutiva ou commit foi feito.

## B. Causas confirmadas

| Área | Constatação e consequência |
|---|---|
| Arma | Machado v2:45×75px de conteúdo para corpo de cerca de121px; cabeça longa/larga e cabo longo prejudicam leitura de uma mão. Espada:26×82px; guarda/cabo merecem proporção de equipamento inicial. |
| Corpo | O pedido de esqueleto v2 move apenas o braço direito e mantém tronco, ombros, quadril e pernas fixos. Isso impede que o corpo conduza o golpe. A estabilização de roupa/pernas também não cria mecânica corporal. |
| Composição | Ângulos pré-escolhidos250→610° completam uma volta. Palma/dedos genéricos rodam com a arma, sem corresponder à anatomia específica de cada pose. Todo o item é rigidamente rotacionado de uma imagem plana; profundidade constante. |
| Movimento | Espada e machado usam o mesmo corpo e relógio1315ms; não distinguem corte rápido de golpe com peso na cabeça do machado. |
| Preview | Os testes anteriores demonstraram igualdade entre PNG e canvas. O navegador não explica os defeitos; a correção precisa ocorrer nas fontes, não por transformações no preview. |
| Continuidade | Handoffs e documentos antigos ainda dizem V4 ativa/896 ativos ou nenhuma seleção. São históricos superados pelo Orc principal atual. Referências a pele cinza/previewv1 na ficha estavam desatualizadas. |

## C. Correções e regra canônica de visibilidade

| Estado | Espada/machado visível |
|---|---|
| Idle, Walk, repouso e inspeção livre | Não |
| Attack | Somente intervalo declarado do golpe |
| Após Attack | Não; retorno ao Idle sem arma |
| Hit e Defeat | Não por padrão |

Sem Idle/Walk armados, animações de sacar/embainhar ou inventário visual. A aparição/desaparição nos limites da ação é intencional; enquanto visível, o item acompanha a mesma mão, sem saltos de grip ou escala. Os lotes antigos armados ficam apenas em histórico claramente identificado.

## Direção da correção

Preservar face, pele, materiais, armadura e identidade atuais. Poses defeituosas não são intocáveis. Preparação, participação de quadril/tronco/ombro, aceleração, contato legível, seguimento e recuperação são obrigatórios. A mão realmente envolve o cabo com polegar/dedos e ligação plausível ao punho; não basta sobrepor âncoras.

Dois perfis pequenos de front_r: **sword-slash** e **axe-chop**. O primeiro privilegia corte controlado rápido; o segundo, preparação e recuperação mais deliberadas com peso na cabeça. Nenhuma rotação360°, IK genérica, rig universal ou corpo novo por item. Outra espada compatível reutiliza sword-slash; outro machado compatível reutiliza axe-chop. Cada item registra ponto local de pegada; cada quadro registra pose, grip, orientação, profundidade e visibilidade.

Armas compartilham a linguagem visual do jogo, sem obrigação de copiar paleta ou ornamentação Orc. Mestres independentes e composições em camadas preservam a possibilidade de troca. Qualquer item incompatível com anatomia, cabo, guarda ou silhueta precisa de adaptação e revisão próprias.

## Revisões seguras de armas

Mestres novos em `assets/weapons/<id>/source/rescue-v3/`, PNGs em sprites/rescue-v3/. Autoria de retoque por Lua **no Aseprite** sobre fontes v2 preservadas, com peças separadas. Na espada, seis linhas centrais da lâmina e quatro do cabo foram retiradas; guarda estreitada independentemente, sem reduzir a largura da empunhadura. No machado, cabeça/barba e comprimento do cabo foram ajustados separadamente, mantendo largura, curva, textura de madeira/couro e tratamento do ferro. Não foi uma redução global do compósito.

Preparação: `tools/prepare-main-orc-rescue.mjs` e `tools/aseprite/prepare-main-orc-rescue.lua`. Referências editáveis de corpo+arma em experiments/main-orc-weapon-rescue-v3/references/. Essas imagens servem para estudar o golpe; não são novos estados de Idle armado.

## Gates e escopo

Somente dois ataques em front_r, sem propagação a outras vistas, Jobs, roupas ou raças. Nenhuma alteração no projeto Unity, `.meta`, Core, stats, inventário ou sistemas de equipamento. Modelo generativo auxilia poses, mas fontes salvas/edição/exportação são Aseprite. Procedência e chamadas reais estão registradas abaixo com os resultados selecionados. Testes técnicos não comprovam naturalidade; aprovação artística final pertence ao criador.

## E. Evidências, exports e mestres atuais

| Perfil | Quadros / duração | Arma visível | Mecânica proposta |
|---|---|---|---|
| `basic.sword-slash` | 8 / 775ms | 1..6, índices começando em0 | Preparação baixa, guarda elevada, tronco/ombro avançam, corte rápido, seguimento e retorno |
| `basic.axe-chop` | 10 / 1130ms | 1..7 | Preparação mais deliberada, cotovelo/ombro armados, descida com peso, seguimento e assentamento |

O machado ocupa47px de altura em vez de75, com cabeça e cabo reduzidos separadamente. A espada ocupa72px em vez de82, com cabo de uma mão, lâmina/canal e pomo preservados. Não há escala por quadro: os dois assets permanecem nativos, scale1, PPU100. O canvas96×96 inclui margem transparente; não é o tamanho aparente da arma.

Mestres em `characters/orc-v1/source/aseprite/onehanded-rescue-v3/`:

- `sword-attack.aseprite`, `sword-body.aseprite`, `sword-hand-front.aseprite`;
- `axe-attack.aseprite`, `axe-body.aseprite`, `axe-hand-front.aseprite`;
- `idle-unarmed.aseprite` e `walk-unarmed.aseprite`, cópias de apresentação registradas, sem alterar os mestres corporais128×128.

PNGs, camadas, folhas, clip.json e profile.json: `characters/orc-v1/source/onehanded-rescue-v3/<Sword|Axe>/Attack/`. Idle/Walk sem arma no mesmo diretório-base. Manifesto: `manifest.json`; ponteiro: `source/equipment-current.json`. Cada perfil tem corpo, dedos, tempos, ângulos, profundidade e visibilidade próprios. A sequência inicia e termina na **pose0 do Idle atual**, exatamente, evitando uma troca para outra pose neutra.

Todos os compósitos usam256×256, corpo nativo128×128 registrado em(64,64), chão de referência190 e PPU100. Sem flip, trim, aumento do corpo ou rotação no navegador. A margem acomoda as armas em arco. A nova roupa não foi congelada sobre um corpo parado; as poses mudam tronco, ombros, quadril e apoio. Solas do pé próximo que atingiram a borda do bruto gerado foram retocadas no Aseprite com o próprio pé aprovado, sem congelar tronco/pernas. Duas limpezas Pro e a limpeza final da guarda/pomo removem armas geradas indevidas da camada corporal.

Os dedos/polegar à frente da empunhadura foram extraídos por contornos da **luva real de cada pose**, sem palma genérica girando com a arma. Camadas: weaponBack → body → weaponFront → handFront. Na preparação há profundidade própria para lâmina/cabeça atrás do corpo, com a região do cabo em primeiro plano. Matching de âncoras não é a avaliação artística; a página mostra os recortes de todas as pegadas.

## Preview e comparação

Abrir `Biblioteca de Arte/Personagens Jogaveis/Orc V1/index.html`. Contém conceito atual, armas separadas, Idle/Walk sem arma, antes/depois por categoria, poses-chave e closes8× da mão. Controles: pausa, reinício, passo por quadro, repetir, velocidade1×/0,5×/0,25×, zoom nativo1×/2×/3× e fundos de contraste.

O modo inicial mostra Idle → Attack → Idle na candidata. “Comparar somente golpes” inicia os ataques antes/depois juntos, mantendo os tempos reais diferentes. Antes é o golpe v2 intacto, claramente rejeitado; não é fonte atual nem parâmetro de qualidade. A v2 portátil completa, incluindo os antigos estados armados, fica em `Biblioteca de Arte/Historico de Entregas/Orc V1 - Armas v2/`, com aviso de superação. Cópias antigas foram movidas de forma reversível para fora das pastas atuais; não houve limpeza recursiva destrutiva.

## D. Reutilização demonstrada

`tools/compose-main-orc-item.mjs` aceita categoria, weapon.json compatível e saída de revisão. Ele lê **os PNGs corporais/dedos já exportados e vinculados aos mestres**, substitui somente o item e seu grip local e compõe no Aseprite. Não gera poses, não acessa PixelLab, não muda seleção de produção e não redesenha o corpo. Valida categoria, mão, PPU e hashes de mestres/exports; arquivos editados exigem nova revisão/exportação.

Exemplo local com um item compatível já cadastrado:

```powershell
node tools/compose-main-orc-item.mjs Sword assets/weapons/recruit-sword/weapon.json reports/minha-revisao-espada
node tools/compose-main-orc-item.mjs Axe assets/weapons/militia-axe/weapon.json reports/minha-revisao-machado
```

Para outra espada/machado compatível, passar seu próprio weapon.json com sprite/master, categoria, hands1, PPU100 e grip inteiro. A anatomia/vista permanece este Orc/front_r. Comprimento, cabeça, guarda e diâmetro do cabo precisam de revisão visual: o contrato não promete encaixe universal.

O teste usa fontes menores **já existentes do lote histórico v1**, de mesma categoria, apenas como substitutos técnicos. Nenhuma arma de produção adicional foi criada. Saídas e metadados em `reports/main-orc-weapon-rescue-v3/reuse/<Sword|Axe>/`. Dezoito quadros recompostos mantêm corpo, dedos e tempos idênticos por SHA256, com novo asset/grip, zero redesenho corporal e zero chamada em nuvem. Os substitutos históricos não são novas aprovações de arte nem direção selecionada.

## Procedência real e custos desta tarefa

Conta Pro confirmada pelo criador; método/modelo não são sinônimos do plano. Registro completo: `experiments/main-orc-weapon-rescue-v3/production-record.json`.

| Operação | Job | Gerações | Destino |
|---|---|---:|---|
| animate_image, servidor sem seletor de modelo | ee7824a2-5107-4eee-8f6b-17766f683b83 | 8 | Rejeitada: estocada e lâmina variável |
| Skeleton V3, corpo inteiro / espada | a24e803e-5fb7-44e6-b357-82455d0bc6fa | 3 | Poses0/1/3/4/5/6, com acabamento; poses2/7 não selecionadas |
| Pro Flash inpaint / recuperação | 9150a6bb-758c-4a8a-9be2-fd34b38c361f | 6 | Remove lâmina sobre roupa/quadril |
| Pro Flash inpaint / passagem | 5916387f-266d-4bf6-b628-e31fb1857972 | 6 | Remove lâmina/guarda/pomo protegendo mão |
| Skeleton V3, corpo inteiro / golpe pesado | 508388e5-5ef9-4830-b11a-46aec2c6bdff | 3 | Oito poses usadas; base final substituída pelo Idle aprovado |

**Total cobrado:26 gerações**, incluindo8 do estudo rejeitado. Não houve nova geração das armas nem nova estimativa de esqueleto: a estimativa anterior do mesmo Orc foi reutilizada após verificar igualdade SHA256 da imagem. Um pedido inicial de texto acima do limite1000 caracteres foi recusado antes de criar job, sem cobrança reportada. A solicitação livre de animação de machado foi preparada, mas não enviada.

O guia de articulações é dado de autoria para PixelLab, não rig/IK implementado no runtime. Nenhum pixel de outro Orc ou V4 condiciona o personagem. Produção generativa em nuvem e acabamento por Lua no Aseprite estão identificados; não chamar isso de desenho manual ou geração inteligente interna do Aseprite. Python/Node apenas organizam, verificam e apresentam os resultados. As chamadas/rasters brutos e máscaras permanecem no experimento, sem credenciais.

## F. Validação executada e avaliação artística

`reports/main-orc-weapon-rescue-v3/check.json` documenta:

- 77 quadros comparados contra10 mestres: corpo independente, dedos, compósitos, bases e itens;
- 18 reconstruções exatas de camadas, visibilidade contínua dos equipamentos somente nos intervalos, grips sobre cabo/mão, dedos da própria pose e nenhum corte nas bordas do canvas;
- 21 quadros de Idle/Walk iguais aos originais nativos, com arma ausente; início/fim dos ataques iguais à pose neutra do Idle;
- 18 substituições de item com corpo/dedos/tempo preservados;
- 9669 PNGs/mestres anteriores protegidos por hash, sem alterações;
- duas limpezas Pro preservando os pixels visíveis não mascarados;
- 63 comparações RGBA dos players, abertura file://, layout móvel, zero erro JavaScript, reprodução1× e0,25× amostrada em capturas temporais, retorno ao Idle sem arma.

A revisão visual do agente incluiu poses nativas, apresentação2×, pegadas ampliadas e capturas da reprodução normal/lenta. Um resíduo de guarda/pomo na recuperação foi encontrado **depois do primeiro PASS técnico** e removido no Aseprite, demonstrando por que os testes não bastam. Não foi realizada revisão artística independente. O criador continua sendo a autoridade final; nenhuma aprovação/Gate foi registrada.

Suíte geral: `node --test --test-concurrency=1`, **14/14 PASS**. A execução paralela inicial teve13/14 e um EPERM do Windows ao renomear um build temporário do teste Aseprite, com evidência em `tmp/aseprite/test-editor-d70e8f508a-normal-0w4onG/failure.json`. A repetição sequencial passou sem alterar o bridge/exportador; a causa específica da contenção não foi confirmada. As exportações reais das candidatas passaram. Biblioteca geral: nove Orcs,18 clipes,162 comparações RGBA,431 links locais e ideias únicas separadas, PASS.

Limites: uma vista, poses discretas de pixel art e estudo local. Qualidade do peso, pegada, transição e leitura tática ainda requer avaliação do criador. Nenhum teste prova naturalidade, nenhuma arma compatível desconhecida foi automaticamente aprovada, e o jogo ainda não consome estes overlays/tempos. Próximo passo: revisão dos dois golpes nesta página antes de propagar ou solicitar integração.

## G. Documentação, reconstrução, segurança e Git

Reexportação dos mestres salvos: `node src/cli.mjs editor-export --manifest experiments/main-orc-weapon-rescue-v3/editor.json`. Arte editada precisa de fork/revisão e manifesto atualizado; não ignorar hashes ou reaplicar receitas sobre trabalho manual. O bloqueio authored-master-lock.json impede que o compositor sobrescreva mestres alterados desde a última autoria. `editor-fork` continua sendo a rota para preservar a fonte antes de retoques.

A receita de autoria, quando as fontes permanecem intactas, usa `tools/prepare-main-orc-profiles.mjs`, `tools/compose-main-orc-rescue.mjs` e `tools/finalize-main-orc-rescue.mjs`. Não faz chamadas PixelLab: usa os brutos já baixados e as decisões/máscaras preservadas. `tools/build-main-orc-rescue-review.py` atualiza a biblioteca; `tools/check-main-orc-rescue.py` verifica a entrega. `tools/build-art-library.py` mantém a entrada geral de todos os Orcs.

Alterações relevantes: guia atual, padrão de armas, AGENTS/handoff, identidade/workflow/roadmap, política de equipamento, ponteiros/manifests e ferramentas locais de autoria/composição/revisão. Exportadores históricos v1/v2 foram bloqueados para não reativar a apresentação armada ou sobrescrever a revisão atual. O prepare carrega também este guia. Fontes antigas e outras roupas/raças/ideias permanecem preservadas.

Git inicial e resumo em `experiments/main-orc-weapon-rescue-v3/initial-git-status.txt` e `git-summary.json`. A árvore já estava suja; diff contraHEAD inclui trabalho anterior e não é apresentado como se fosse todo desta tarefa. Nenhum commit, reset ou stash foi feito. Nenhum arquivo do projeto Unity irmão foi alterado.
