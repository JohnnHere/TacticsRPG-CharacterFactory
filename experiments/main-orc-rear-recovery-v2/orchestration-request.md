# ORQUESTRAÇÃO MULTIAGENTE — PASEO

Orquestre esta tarefa utilizando o **Paseo**. Execute `npx -y @getpaseo/cli` no terminal para consultar os modelos disponíveis, delegar tarefas e acompanhar os subagentes. Utilize autonomamente os comandos necessários.

**Objetivo:** maximizar a qualidade e a eficiência, reduzindo custos, consumo desnecessário de tokens, retrabalho e intervenções.

## 1. Planejamento e seleção

- Analise a tarefa, identifique dependências, riscos e oportunidades reais de paralelismo.
- Use a quantidade de subagentes adequada: prefira um dev quando a tarefa for pequena ou muito interdependente; use mais apenas quando houver frentes que possam avançar sem conflito.
- Priorize modelos gratuitos do OpenCode e OpenRouter. Preferências, sem ordem obrigatória: **DeepSeek Free, GLM Free, MiMo Free e Beam Free**.
- Considere outros modelos gratuitos disponíveis e compare qualidade esperada, velocidade, custo e contexto útil para a tarefa.
- MiniMax 3.1 Flash é candidato para tarefas que precisam de muito contexto; em seguida, considere DeepSeek 4.1 Flash e GLM 5.3 Flash. Confirme no catálogo atual do Paseo as versões e os limites disponíveis. Não escolha um modelo apenas por ter uma janela de contexto maior.
- Se os modelos gratuitos ficarem indisponíveis, utilize, como devs, nessa ordem de prioridade: Gemini 3.8 Flash (antigravity), GLM 5.3 Flash (Cline GLM API), Luna 6 (Codex), Deepseek 4.1 Flash 1017 (Cline Deepseek), Gemini 3.8 Flash (copilot).
- Ajuste o *reasoning effort* de cada agente, inclusive o seu, à complexidade da responsabilidade.
- Estabeleça contratos compartilhados antes de delegar tarefas interdependentes.
- Leia somente os arquivos e documentos relevantes. Não carregue ou envie o contexto inteiro do projeto quando um resumo, os arquivos pertinentes e o diff forem suficientes.

## 2. Desenvolvimento, integração e supervisão

Siga este fluxo, proporcional à complexidade da tarefa:

1. **Orquestrador planeja:** define arquitetura, critérios de aceitação, dependências e responsabilidades.
2. **Devs implementam:** recebem tarefas delimitadas, executam verificações pertinentes e reportam resultados objetivos.
3. **Orquestrador supervisiona:** acompanha checkpoints de risco, contratos e dependências; intervém quando necessário para evitar retrabalho.
4. **Orquestrador integra:** consolida as alterações, resolve incompatibilidades e verifica o funcionamento conjunto.
5. **QA independente revisa:** após a integração, revisa obrigatoriamente a entrega integrada completa, mesmo que o Orquestrador já considere o resultado satisfatório.
6. **Correções retornam ao QA:** se houver achados ou mudanças após a revisão, os devs corrigem, o Orquestrador reintegra e a versão atualizada passa novamente pelo QA.
7. **Orquestrador finaliza:** entrega somente a versão aprovada pelo QA.

### 2.1. Delegação de trabalho especializado

**O Orquestrador deve priorizar planejamento, tomada de decisões técnicas, definição de contratos, supervisão, integração, resolução de conflitos e auditoria dos resultados.**

Quando uma atividade substancial puder ser executada por um subagente com acesso às ferramentas e permissões necessárias, **delegue sua execução em vez de realizá-la diretamente no contexto principal**.

Essa regra aplica-se especialmente a:

- Desenvolvimento extensivo de código.
- Implementação de funcionalidades e correções complexas.
- Refatorações volumosas.
- Criação e manutenção de scripts de produção.
- Produção artística em lote com Aseprite.
- Geração e refinamento de sprites utilizando PixelLab MCP.
- Processamento de grandes quantidades de sprites, animações e frames.
- Operações repetitivas de exportação, transformação ou validação de assets.
- Outras tarefas especializadas que possam ser delegadas com segurança.

**O Orquestrador não deve assumir uma implementação extensa apenas porque possui acesso direto à ferramenta necessária.**

#### Verificação de capacidade antes da delegação

Antes de atribuir uma atividade a um subagente:

1. Verifique se ele possui acesso real às ferramentas necessárias.
2. Confirme as permissões e o escopo de execução.
3. Identifique os arquivos, contratos e referências indispensáveis.
4. Defina claramente o resultado esperado.
5. Evite transferir contexto desnecessário.
6. Estabeleça responsabilidades sem conflitos de edição.

Não presuma que o acesso do Orquestrador a uma ferramenta, extensão, terminal ou MCP também está automaticamente disponível aos subagentes.

#### Ferramentas disponíveis exclusivamente ao Orquestrador

Se uma ferramenta necessária estiver disponível apenas no contexto principal:

1. Verifique se existe uma maneira segura, documentada e compatível de disponibilizá-la ao subagente.
2. Não compartilhe credenciais, tokens privados ou permissões além do necessário.
3. Se o acesso direto não puder ser delegado, atribua ao subagente o planejamento operacional, a preparação de entradas, scripts, parâmetros, manifests e artefatos necessários.
4. Utilize o Orquestrador somente para executar as chamadas indispensáveis à ferramenta restrita.
5. Devolva ao subagente as etapas subsequentes que não dependam dessa ferramenta.
6. Registre a limitação e seu impacto sobre custo, tokens e execução.

**A impossibilidade de delegar uma chamada MCP não justifica transferir automaticamente toda a tarefa ao Orquestrador.**

#### Exceções legítimas

O Orquestrador pode executar diretamente:

- Pequenas correções de integração.
- Ajustes pontuais de compatibilidade.
- Verificações rápidas de contratos.
- Operações necessárias para desbloquear subagentes.
- Chamadas restritas a ferramentas inacessíveis aos executores.
- Mudanças pequenas cuja delegação custaria mais do que sua execução segura.

Essas exceções devem ser proporcionais ao trabalho.

Evite delegações artificiais de tarefas triviais.

Também não prejudique a qualidade, a segurança ou o resultado final apenas para impedir que o Orquestrador execute qualquer comando.

#### Diretriz de eficiência

**Reserve o contexto e os tokens do Orquestrador para decisões de alto valor. Utilize subagentes adequados para produção e implementação sempre que viável.**

Otimize o custo da entrega completa e validada, e não apenas o consumo individual de cada modelo.

### 2.2. Produção artística e ferramentas externas

Quando a tarefa envolver Aseprite, PixelLab MCP ou outras ferramentas de produção de assets:

- Prefira delegar preparação, implementação de scripts, produção de candidatos, processamento e validações técnicas.
- Reutilize assets, poses, receitas, referências e resultados já aprovados.
- Não repita gerações pagas quando o resultado existente puder ser reutilizado ou refinado localmente.
- Valide referências e poses representativas antes de produzir grandes lotes.
- Não considere uma geração tecnicamente válida automaticamente aprovada artisticamente.
- Preserve a identidade visual, os arquivos mestres e os contratos atuais do projeto.
- Mantenha rastreabilidade de procedência e operações externas.
- Quando possível, registre operações realizadas e consumo verificável de créditos.

O Orquestrador deve supervisionar os resultados artísticos e sua aderência aos critérios de aceitação, sem assumir automaticamente toda a criação dos assets.

As decisões sobre o que deve ser produzido, modificado ou aprovado continuam subordinadas à tarefa e aos contratos do projeto.

### 2.3. Regras gerais de eficiência

- Acompanhe resultados, diffs, testes e impedimentos; não cada ação dos devs.
- Para cada dev, compartilhe apenas o contexto necessário e os contratos relevantes.
- Supervisione durante a implementação somente checkpoints de risco significativo.
- Paralelize apenas tarefas independentes.
- Reutilize código, contexto, resultados e testes existentes. Não refaça trabalho validado sem justificativa.
- Não avance sobre falhas críticas sem resolvê-las ou registrar um impedimento real.
- Não atribua dois executores à mesma alteração sem um contrato claro de responsabilidade.
- Evite utilizar o Orquestrador como executor principal de trabalhos longos quando houver um subagente capaz de realizá-los.

## 3. Recuperação e acompanhamento de falhas

- Em falhas de autenticação, limites, indisponibilidade ou execução, preserve o trabalho parcial e redistribua somente o que estiver pendente.
- Substitua um DEV com falha por outro modelo gratuito disponível no OpenCode/OpenRouter. Se a tarefa continuar bloqueada, mude a estratégia ou escale para um modelo mais capaz.
- Evite tentativas repetidas sem mudança de estratégia. Nunca simule execução ou sucesso.
- Preserve o estado do projeto e alterações não relacionadas. Em bloqueio irrecuperável, interrompa a etapa afetada e reporte o impedimento.

**Acompanhamento de agentes Paseo (ACP):**

- Guarde o `agentId` de cada agente. Antes de reenviar, interromper ou acionar fallback, confira status, atividade recente e permissões pendentes. Uma chamada `read` ou outra atividade de ferramenta, por si só, não justifica reenviar a tarefa.
- Se houver permissão pendente, responda à solicitação específica pelo mecanismo do Paseo, usando o `requestId` e a ação corretos, dentro do escopo autorizado.
- Se o agente estiver `running` ou com turno ativo, não reenvie com `--behavior interrupt`, não execute `stop` e não crie outro agente para duplicar a tarefa. Acompanhe o mesmo agente com polling limitado. Repita o envio inicial somente se confirmar que ele não foi entregue e que o agente não tem turno ativo.
- Se receber `A foreground turn is already active`, confira o estado: se ainda estiver ativo, aguarde dentro do limite; se estiver `idle`, recupere o resultado existente e envie apenas a continuação pendente; se estiver `error` ou `closed`, preserve o progresso e use o fallback previsto nesta seção.
- Ao atingir o timeout, colete status e logs, encerre o polling e reporte o impedimento.

## 4. Quality Assurance (QA)

Após a implementação e a integração, delegue uma revisão independente ao **Gemini Argon (antigravity)**. Essa revisão é obrigatória para a entrega integrada, mesmo que o Orquestrador já aprove o resultado.

Se estiver indisponível, utilize o **GLM 5.3 (Cline GLM API)**. Se também estiver indisponível, utilize o **GPT Sol 6.1 do GitHub Copilot** (não o Codex). Se nenhum estiver disponível, utilize o modelo gratuito mais apropriado para revisão de código disponível no OpenCode ou OpenRouter.

Para reduzir contexto sem reduzir cobertura, forneça ao QA:

- O pedido original e os critérios de aceitação.
- Um resumo curto do que foi implementado.
- A lista de arquivos alterados e os diffs.
- Os contratos e documentos diretamente relevantes.
- Os comandos e resultados reais dos testes.

O QA deve examinar os diffs e os arquivos relevantes por conta própria; não deve se limitar ao resumo do DEV. Deve revisar todos os componentes incluídos na entrega, mas não precisa reler o projeto inteiro sem necessidade.

O QA deve:

- Verificar requisitos, contratos, arquitetura, integração, bugs, regressões e segurança conforme o escopo e o risco.
- Executar novamente verificações relevantes quando isso ajudar a confirmar os achados. Rode a suíte completa quando o impacto da alteração ou os requisitos do projeto justificarem.
- Classificar problemas por gravidade, apresentar evidências e sugerir correções objetivas.
- Distinguir defeitos comprovados de riscos hipotéticos.

Se o QA encontrar problemas, o Orquestrador coordena as correções e solicita nova revisão da versão integrada. A revisão pode focar nas partes afetadas e nas regressões pertinentes, ampliando o escopo quando o impacto justificar. Qualquer alteração feita depois da aprovação do QA, inclusive pelo Orquestrador, precisa ser revisada antes da entrega.

Nunca apresente uma versão como aprovada pelo QA se aquela versão específica não foi revisada. Se não for possível revisar a versão final, reporte o impedimento ou que ela permanece sem validação.

Ajuste o *reasoning effort* do QA conforme a complexidade e o risco.

## 5. Relatório final

Apresente um relatório conciso contendo:

- Modelos utilizados e responsabilidades.
- Entregas concluídas e pendências.
- Falhas, substituições e retrabalho relevante.
- Testes executados e resultados reais.
- Resultado do QA, achados e correções aplicadas.
- Consumo ou custo por modelo somente quando disponível e verificável.
- Trabalho especializado executado diretamente pelo Orquestrador, quando relevante, e por que não foi delegado.
- Operações e custos externos verificáveis, como chamadas ao PixelLab, quando aplicável e disponível.

**Diretriz principal:** use a capacidade do Orquestrador para decisões importantes, não para microgerenciamento. Delegue implementações aos modelos gratuitos quando adequados, supervisione por risco e mantenha a validação independente. Otimize o custo total da tarefa concluída e validada, não apenas o número de tokens.

Execute a tarefa integralmente, sem parar no planejamento e sem solicitar que eu execute comandos manualmente, exceto diante de impedimentos que realmente exijam minha intervenção.

## Processos longos no Windows

- Para Unity/Test Runner e outros executáveis nativos, prefira a chamada direta do executável, por exemplo, `& $unity ...`. Evite `Start-Process -Wait`: no Windows, ele espera pelo processo e todos os descendentes, e workers remanescentes podem prender o PowerShell depois que o executável principal termina.
- Se precisar de `Start-Process`, use `-PassThru` sem `-Wait` e aguarde somente pelo PID principal com `Wait-Process -Id $proc.Id -Timeout <limite>`. Defina um prazo total para a execução.
- Considere o teste concluído quando o processo principal terminar e o artefato esperado estiver completo, por exemplo, XML válido com `end-time`. Falhas no XML são resultado final, não motivo para esperar indefinidamente.
- Nunca use loops `while ($true)` sem limite. Valide que PID/task ID foi capturado; limite o polling e, no timeout, colete status/logs, encerre o monitoramento e reporte o impedimento.
- Não use `git checkout`, `reset` ou `clean` para apagar alterações locais de `ProjectSettings` ou de outros arquivos. Preserve o estado existente e remova apenas temporários criados e identificados pela própria execução.

**Encerramento obrigatório:** quando todas as entregas exigidas estiverem concluídas e a versão final estiver aprovada pelo QA — ou houver um impedimento real conforme a seção 3 — pare a iteração e o polling, recupere os resultados finais dos subagentes, apresente o relatório da seção 5 e encerre a execução. Não deixe tarefas de monitoramento em segundo plano nem aguarde notificações redundantes após confirmar a conclusão.