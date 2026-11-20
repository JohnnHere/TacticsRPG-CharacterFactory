# Orc V1 — recuperação dirigida das animações

Relatório de integração da tarefa de 26/10/2026. O pacote permanece candidato: `PENDING_CREATOR`. Não houve integração no Unity nem promoção automática da seleção de produção.

**Atualização de 27/10 — reparos locais integrados para nova revisão:** o primeiro freeze `6fa4653e…` foi reprovado pelo QA independente (GPT Sol6.1 via GitHub Copilot). A composição por camadas e os hashes estavam corretos, mas três clipes ainda apresentavam defeitos artísticos: resíduos de arma no corpo da espada esquerda e do machado direito, braço direito descontínuo/duplicado e um filamento na ombreira do machado esquerdo. Os reparos locais e a recomposição estão registrados no [relatório ART](qa-revision-1-art-escalation-report.md). O parecer original está preservado em [qa-history](qa-history/6fa4653eabe660992acc422aa32159b48e4971122df0e995b99a19261df4a843/qa-argon-final.md). O parecer corrente só se aplica à entrega corrigida quando o freezeId de qa-result.json coincidir com delivery-freeze.json; os testes e o checkpoint interno não concedem aprovação artística.

O primeiro retoque local de Luna também não foi aceito no checkpoint interno. Foi identificado um doador de256px deslocado como se fosse de128px, além de máscaras que não cobriam os resíduos confirmados. O executor encerrou o turno sem alterar a arte canônica. O trabalho pendente foi transferido a GPT-6.1 Sol via Codex/Paseo (`b8ca8bb5-e80c-4c39-ade9-09b167774d78`), mantendo o revisor independente via Copilot. Backup verificado dos192 arquivos-alvo e verificação de1.911 arquivos preservados estão registrados; o consumo PixelLab permanece78 unidades/17jobs.

## Entrega A–F após os reparos do QA

**A. Diagnóstico confirmado.** O corpo gerado ainda continha formas de arma, apesar das camadas de equipamento separadas. O enxerto anterior do punho não removia todo o antebraço antigo e permitia uma cadeia articular desconexa. Máscaras estimadas e doadores com registro incorreto agravaram o primeiro retoque. A ausência visual de arma no corpo precisa de inspeção própria; igualdade de crop, hashes e alfa-over comprovam apenas integridade estrutural.

**B. Alterações artísticas.** SwordL: restauração da mão não atacante F01..07 e dos ombros F04/F05, removendo lâmina/haste. AxeR: remoção da cabeça/haste no corpo, reconstrução da mão e substituição completa do antebraço obsoleto F04/F05 por um único membro conectado da mesma vista; arma posicionada na manopla real. AxeL: remoção do filamento, preservando o enxerto da mão e os27 pixels de limpeza anteriores. Os outros nove alvos bem-sucedidos — incluindo Walk e Unarmed traseiros, os dois F02 frontais e os terminais Defeat — permanecem como antes. Hit mantém450ms e pixels; calibração no jogo continua pendente.

**C. Evidências.** [Manifesto canônico](../../characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json), [máscaras, doadores e hashes](qa-revision-1-repair/provenance.json), [prova de reexportação](qa-revision-1-repair/source-proof.json) e [playback real capturado](qa-revision-1-repair/playback-verification.json). São168 comparações de quadros em21 exportações dos nove mestres reparados. Os três ataques mantêm8 quadros/730ms e quatro camadas; armas visíveis somente F01..F06. As14 fontes independentes de armas e1.911 arquivos protegidos permanecem intactos. Mestre/edit/export no Aseprite; Python apenas montou layouts de QA. Nenhuma nova geração:78 unidades/17jobs no experimento, sem estimar saldo corrente ou custo monetário.

**D. Aprendizado.** [Contrato](../../config/artistic-quality-gates-v1.json), [receita Orc candidata](../../recipes/races/orc.candidate.json) e [correções documentais](qa-revision-1-knowledge-report.md) exigem inspeção de corpo inteiro com equipamentos desligados, continuidade ombro–cotovelo–punho, verificação do doador e registro explícito128→256. A reutilização do braço deve substituir a silhueta antiga, inclusive transparência; uma base estática com braço pendente não serve como preenchimento automático. As12 lições semânticas e cinco operacionais mantêm seus nove campos de evidência e escopo; não universalizam anatomia ou amplitude para outras raças.

**E. Revisão visual.** O [comparador principal](../../Biblioteca%20de%20Arte/Estudos%20Comparativos/Orc%20principal%20-%20Recuperacao%20traseira/index.html) contém28 seleções,12 comparações antes/depois, controles1/.75/.5, passo a quadro e retenção terminal de Defeat. O estudo body-only e os detalhes de pegada estão ligados no relatório ART. A seleção de produção não foi promovida.

**F. Validação e limites.** [Execuções desta rodada](root-qa-revision-1-tests.json):338 checagens estritas,26 testes Node,20 verificações reais no Chromium, preview estático/pixels/links, fontes de arma, F02 protegido, quatro clipes herdados, doctor/editor-check e1.911 arquivos preservados, todos sem falhas. Playback foi inspecionado por quadros e amostras temporais de um player real; não é vídeo contínuo nem teste no Unity. O diff local é amplo e já estava sujo em main; nenhuma limpeza, commit ou escrita no projeto irmão foi realizada. O [resumo Git de escopo](root-qa-revision-1-git-status.txt) registra caminhos, sem atribuir mudanças preexistentes a esta rodada. A revisão independente usa o MESMO Copilot08686 após novo freeze. O resultado efetivo está em qa-result.json; aprovação do criador permanece PENDING_CREATOR.

Após a sincronização documental, os dois testes de main-orc-complete passaram novamente. A [preservação dos793 arquivos](root-qa-revision-1-preservation.json) confirmou792 idênticos e somente a alteração autorizada de config/artistic-quality-gates-v1.json. O script histórico verify_baseline_protection.py imprime ERROR para essa alteração e retorna0; não foi reinterpretado como proteção integral nem alterado para esconder a diferença. A comparação explícita acima registra a exceção e rejeita qualquer mudança adicional.

**Entrada de revisão:** [comparador completo](../../Biblioteca%20de%20Arte/Estudos%20Comparativos/Orc%20principal%20-%20Recuperacao%20traseira/index.html). **Versão exata submetida ao QA:** [delivery-freeze.json](delivery-freeze.json). **Parecer independente:** [qa-argon-final.md](qa-argon-final.md), com resultado estruturado em [qa-result.json](qa-result.json). Esses arquivos de QA só constituem evidência depois de produzidos; este relatório não antecipa o resultado.

## Escopo artístico

Base preservada: `dist/editor/orc-v1-complete-v1/b178422e1f7fc19f068c`. Personagem: `orc-v1`, Verde Warcraft. O manifesto candidato canônico fica em `characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json`.

O alvo são 12 células: Walk, Unarmed, Sword e Axe nas duas vistas traseiras; Unarmed e Defeat nas duas vistas frontais. As outras 16 células continuam apontando para os clipes da base. No Unarmed frontal, somente F02 recebeu reparo; 00/01/03/04 devem permanecer idênticos. No Defeat frontal, somente o terminal foi substituído; estágios0..3 permanecem. Idle, Walk, Sword e Axe frontais e Defeat traseiro são preservados.

Hit mantém os pixels e450ms. A avaliação interna usou as quatro vistas em reprodução real1×/0,75×/0,5×, no tamanho nativo e numa aproximação de64px; a reação permaneceu legível. O ajuste no jogo depende de câmera, eventos, hit-stop e cadência de combate ainda não avaliados no Unity. Evidência: [avaliação de Hit](root-hit-playback-assessment.md).

## Causas e correções

- A anatomia traseira estática correta estava combinada com pernas e poses incompatíveis com a perspectiva. Os ciclos traseiros receberam movimento próprio e registro no Aseprite.
- O ataque desarmado anterior misturava poses de outras ações. A nova sequência prioriza preparação, extensão do punho, impacto e recuperação.
- Os primeiros ataques com armas usavam corpo e arma achatados e âncoras herdadas. Foram rejeitados. Os candidatos novos mantêm camadas reais `weaponBack`, `body`, `weaponFront`, `handFront`, corpo nativo separado e armas independentes.
- Testes de poses isoladas mudaram proporções e não encaixaram no ciclo. A solução útil empregou ciclos de corpo coerentes e ajuste local de trajetória, pegada e oclusão no Aseprite.
- PixelLab inseriu armas em algumas saídas solicitadas sem armas. Esses elementos foram removidos no Aseprite, preservando os brutos. A vista final do machado também precisou de reparo de dois punhos cortados pela borda, reaproveitando braço/manopla da mesma vista e do mesmo indivíduo, com ajuste local.
- O Unarmed frontal tinha um punho ausente. O reparo aproveita a manopla aprovada da mesma vista; recortes iniciais inadequados foram rejeitados.
- O terminal frontal de Defeat parecia uma posição ajoelhada ativa. O candidato termina caído, preservando os estágios anteriores.

Os checkpoints do orquestrador permitiram expansão interna. Não equivalem a aprovação do criador nem substituem QA independente. Métricas de deslocamento de Hit passaram a diagnóstico contextual; integridade de arquivos, fontes e exportações continua obrigatória.

## Fontes e procedência

Mestres: `characters/orc-v1/source/aseprite/rear-recovery-v2/`. Clipes e derivados: `characters/orc-v1/source/rear-recovery-v2/`. O manifesto, os `clip.json` e o congelamento da entrega relacionam os caminhos e hashes exatos. Não usar os diretórios experimentais rejeitados como seleção vigente.

Geração de imagens: PixelLab em nuvem. Edição, composição, reparos, registro e exportação: Aseprite, inclusive autoria Lua registrada. Não se trata de desenho manual integral. Python e navegador foram usados para diagnóstico, recortes de QA e prévias, sem editar a arte final. Um rascunho antigo de crossfade externo foi rejeitado e arquivado; não foi promovido à produção.

Preservação verificada durante a integração:793 arquivos rastreados, dos quais792 permaneceram idênticos e um é a alteração autorizada de configuração de qualidade; os73 mestres da base ficaram intactos. As14 fontes/derivados de armas comparados ao snapshot feito durante a produção permaneceram iguais. Esse snapshot de armas não é uma medição anterior ao início de toda a sessão. As bibliotecas anteriores foram preservadas. A árvore Git já estava suja na branch `main`; não houve checkout, reset, limpeza destrutiva ou commit.

## Consumo verificável

Total da recuperação:78 unidades de geração em17 jobs:13 iniciais/66 unidades; um teste de ciclo/3; dois jobs autorizados/6; última vista do machado/3. O teste intermediário de3 unidades foi executado antes do checkpoint interno e permanece registrado como desvio, sem aprovação retroativa. As autorizações seguintes foram explícitas e limitadas.

Do conjunto inicial,14 unidades foram rejeitadas e24 produziram chaves isoladas incompatíveis mantidas em cache; não são contabilizadas como resultados aprovados. As28 restantes contribuíram para Walk, Unarmed e Defeat. Os12 adicionais correspondem aos quatro ciclos de corpo para armas, com refinamento local posterior. Não houve geração nova de Hit. O registro definitivo é [cost-provenance-ledger.json](cost-provenance-ledger.json), com recibos e hashes. Não há autorização restante para geração.

As ferramentas não fornecem um total confiável de tokens ou preço monetário da tarefa inteira. Uso parcial de um turno, cache e valores0 reportados por um provedor não foram convertidos em custo total ou em afirmação de serviço gratuito. Execuções locais do Aseprite não são chamadas pagas do PixelLab.

## Orquestração e responsabilidades

| Frente | Execução efetiva |
|---|---|
| Diagnóstico e contratos iniciais | MiMo/Beam gratuitos e Nemotron gratuito; trabalho parcial preservado após limites de uso |
| Primeiros candidatos e biblioteca de conhecimento | Gemini3.8Flash via Antigravity; candidatos com armas achatadas foram rejeitados |
| Preview | Implementação inicial Gemini3.8Flash, correções GLM5.3Flash via Cline; uma tentativa ficou presa no navegador e outra terminou em erro de turno |
| Handoff de coordenadas | GLM5.3Flash via Cline; estimativas não foram tratadas como pegadas aprovadas |
| Reparos finais de arte e fontes | Luna6 via Codex/Aseprite; retomado após limite, sem repetir gerações |
| Contratos e validador final | Gemini3.8Flash via Antigravity, com testes negativos em cópias temporárias |
| Revisão independente integrada | Parecer e modelo efetivos registrados em `qa-result.json` |

O orquestrador conduziu decisões, checkpoints visuais, integração, auditoria de recibos, verificação de preservação e pequenas correções de compatibilidade nos testes do visualizador. Essas correções retiram expectativas fixas de que uma espada já corrigida deva continuar rejeitada. Não assumiu a autoria artística em lote. Falhas de provedores e mudanças de responsável estão em [orchestration.json](orchestration.json).

Outra correção de integração nas prévias: as folhas nativas de128px dos candidatos não podiam ser comparadas, na mesma altura de tela, às folhas compostas de256px da base; nas armas, também omitiam o equipamento. O visualizador agora monta folhas exclusivas de revisão com cópias exatas dos quadros compostos de256px. Essa montagem externa é apenas layout de preview, sem redesenho, recoloração, escala ou alteração dos pixels de produção. Um teste compara cada tile aos pixels do quadro correspondente. Os mestres e as folhas nativas produzidas no Aseprite permanecem intactos.

## Conhecimento e validação

Os contratos, receitas candidatas, checklist, workflow, handoff e roadmap foram atualizados com as12 lições exigidas e seus9 campos de evidência. Métodos bem-sucedidos e falhos têm escopo explícito; não se transformam em anatomia ou fórmulas universais para outras raças.

Inventário final: 28 clipes/210 quadros compostos, sendo78 quadros nos12 clipes candidatos e132 nos16 aliases preservados. Os candidatos referenciam28 mestres ativos. A preservação dos quadros reaproveitados dentro dos candidatos é medida pelos pixels RGBA decodificados e pelos tempos; a codificação PNG pode mudar na reexportação. Os arquivos da base original permanecem intactos.

| Verificação executada | Resultado |
|---|---|
| Validador estrito do manifesto | PASS: grade28/28, partição12/16, fontes, hashes e políticas de armas |
| Testes do validador, incluindo casos negativos | 14 passaram; detectam fontes ausentes e hashes/quadro/camadas inválidos |
| Quatro arquivos de testes compartilhados | 12 passaram |
| Composição e fontes dos quatro ataques com armas | PASS, com leitura apenas, corpo nativo e tempos/GIFs conferidos |
| Reparo frontal F02 | PASS: dois quadros reparados, oito preservados em pixels/tempos |
| Quatro clipes antigos com metadados completados | PASS:20 nativos coincidem com exportações Aseprite e recortes compostos |
| Preview estático e pixels das folhas | PASS:28 células,12 comparações,links resolvidos; nenhum quadro antigo excedente |
| Navegador Chromium real | 20 verificações passaram: seleção, desenho, velocidade, passos e terminal de Defeat |
| Doctor e editor-check | Sem erros de referência; Aseprite1.3.18.6 disponível |
| Preservação de fontes e build anterior | PASS:715 arquivos compostos e903 da build anterior sem alterações;73 mestres preservados |

Evidência estruturada: [root-integration-tests.json](root-integration-tests.json), [root-final-inventory.json](root-final-inventory.json), [root-final-preservation.json](root-final-preservation.json) e [root-immutable-build-preservation.json](root-immutable-build-preservation.json). A revisão anterior da pasta candidata foi preservada em `rejected/preview-before-final-clean-build/` antes da reconstrução limpa; isso não alterou as bibliotecas aprovadas anteriores.

O arquivo de congelamento e o parecer independente identificam a versão efetivamente revisada. A aprovação artística continua sendo decisão do criador.
