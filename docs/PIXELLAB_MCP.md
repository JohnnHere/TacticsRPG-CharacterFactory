# PixelLab MCP — integração oficial

Configurado em 2026-10-23 a pedido do criador, após instalação da extensão Aseprite. O MCP permite enviar pedidos e acompanhar resultados sem controlar o desktop. **O arquivo `.aseprite` continua mestre**; PNGs gerados são importados/empacotados no Aseprite. O pedido atual autoriza esta interface adicional do PixelLab.

## Instalação e credencial

Servidor oficial `https://api.pixellab.ai/mcp`, transporte HTTP nativo do Codex. Configuração no arquivo de usuário `~/.codex/config.toml`, seção `[mcp_servers.pixellab]`; backup anterior preservado fora do repositório. Autenticação Bearer guardada apenas nessa configuração privada. Nenhuma credencial deve entrar em documentação, Git, prompts de arte ou manifestos. Não é necessário instalar `mcp-remote`: o Codex instalado suporta HTTP diretamente.

Conexão autenticada comprovada por `initialize` HTTP 200, servidor **PixelLab MCP Server 0.2.0**, protocolo `2024-11-05` e `tools/list` concluído. Catálogo público de esquemas em `reports/pixellab-mcp-tools.json`. A conexão já funciona pelo cliente local nesta sessão. O carregamento automático das ferramentas pelo host Codex depende de recarregar/reabrir o cliente; não reiniciar o editor do usuário como efeito colateral.

## Uso local sem mouse

`tmp/pixel-venv/Scripts/python.exe tools/pixellab-mcp.py --list --output reports/pixellab-mcp-tools.json`

`tmp/pixel-venv/Scripts/python.exe tools/pixellab-mcp.py --call NOME --input pedido.json --output resultado.json`

O cliente usa o protocolo MCP oficial (`initialize`, `notifications/initialized`, `tools/list`, `tools/call`), lendo a configuração privada do Codex. Não usa endpoints REST de geração nem copia a chave para o projeto. O resultado completo fica no destino; stdout contém só resumo. Escolher a ferramenta pelo esquema atual e não supor que todos os métodos oferecem os mesmos modelos.

Para arte, registrar ferramenta/modelo, pedido, job ID, imagens próprias de entrada, saídas brutas, tempos do mestre e avaliação visual. `animate_image` aceita primeiro e último quadro; nesta revisão ambos recebem a própria pose inicial para fixar o fechamento. O modelo não é selecionável nesse método: **licença Pro não significa que qualquer ferramenta seja um modelo Pro**. Conceito 04 foi gerado no seletor Pro da extensão; movimentos corretivos usam o método MCP registrado. A conta informou assinatura ativa na consulta autenticada; nomes de plano retornados pelo serviço e confirmação Pro do criador devem ser mantidos como evidências distintas.

MCP não concede aprovação artística, não integra Unity automaticamente e não autoriza enviar mensagens ou modificar projetos remotos fora do pedido de arte. Não chamar ferramentas destrutivas ou de publicação por padrão.

Fontes oficiais: [PixelLab Vibe Coding](https://www.pixellab.ai/mcp), [catálogo MCP](https://api.pixellab.ai/mcp/docs), [configuração MCP no Codex](https://developers.openai.com/codex/mcp).
