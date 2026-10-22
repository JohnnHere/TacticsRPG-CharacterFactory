# Auditoria de capacidade por sessão

Verifique ferramentas expostas, MCPs relevantes acessíveis e executáveis/bibliotecas locais sem ler credenciais. Disponibilidade de uma ferramenta é evidência de acesso anunciado, não prova de execução bem-sucedida. Não instalar, conectar ou cobrar APIs sem autorização. Registre ferramenta, disponibilidade, limitações, autorização e evidência.

| Nível | Critério |
|---|---|
| 1 Documentação | Briefs, prompts, contratos, checklists |
| 2 Processamento | Recorte, composição, alfa/bounds, comparação, previews/export comprovados |
| 3 Geração visual | Ferramenta real de geração/edição exposta e utilizável; execução depende de autorização |
| 4 Produção validada | Arquivos nativos existentes, dimensões/alfa/alinhamento medidos e clusters/identidade revisados; nunca inferir do aspecto pixelado |

Os níveis não precisam ser cumulativos: registre capacidade por operação. Código pode compor previews ou desenhar pixels, mas não prova autoria artística adequada. Um LLM de programação sozinho permanece nível 1.

Com geração: leia anchor, prepare brief e Reuse Assessment, use referências conforme suporte da ferramenta, produza candidatos autorizados, compare/exiba e aguarde Gate 1. Imagem conceitual não é sprite. Não gere sprites finais apenas redimensionando; nearest-neighbor/limpeza de alfa/paleta são auxiliares, não conversão automática.

Sem geração: entregue [generation-prompt.md](../templates/generation-prompt.md) preenchido, referências existentes, câmera/pose/anatomia/paleta/luz, resolução alvo e checklist. Nomeie o resultado como instruções; não afirme ter produzido PNG ou animação.

Ferramentas específicas podem impor skill/workflow próprio; siga-o quando realmente disponível. A skill não depende de provedor nem de nomes de APIs. Reavalie capacidade em cada ambiente; snapshot da entrega em [delivery-audit.md](delivery-audit.md).
