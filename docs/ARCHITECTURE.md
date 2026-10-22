# Arquitetura v0.1

Node.js >=20, modulos ESM e pngjs 7.0.0. JSON como fonte de dados, sem banco, servidor, bundler ou chaves. Tudo local apos npm ci. LibreSprite opcional. Node substitui o Python sugerido na conversa porque esta maquina ja tinha Node utilizavel; contratos JSON e PNG sao portaveis.

src/core.mjs: caminhos confinados, IDs, JSON, inventario e hashes. references.mjs: snapshot, manifestos e catalogos. workflow.mjs: fichas, contexto, prompts e previews. recipes.mjs: receitas raciais/de Job e arquivo de versoes/imagens. images.mjs: PNG, medicao, composicao e validacao. cli.mjs: comandos e gates. config/style.json deriva regras das fontes e nao torna propostas em canone. unity/ contem apenas importador de staging.

characters/<id>/character.json e fonte editavel. identityId identifica individuo; id identifica pacote/roupa. reviews.json guarda decisoes informadas pelo operador. assets.json guarda historico de entradas e camadas. concepts/ e separado de sprites/ para impedir que canvas conceitual vire exportacao. source/ guarda fontes 2D originais. handoff/ e pacote para agente/provedor. reports/ e evidencia de validacao. dist/ e build imutavel local, ignorado no Git.

## Gates e hashes

Gate concept: ficha + conjunto de PNGs de conceito + snapshot de referencias. Marco base: ficha + fallback/quatro vistas + snapshot, permitindo adicionar animacoes sem invalida-lo. Gate consistency: ficha + todos os sprites + snapshot. Gate in-game usa mesmo conteudo final e evidencia de PlayMode fornecida pelo operador. Alterar arquivo/ficha/snapshot invalida gates correspondentes. Ultima rejeicao de cada gate vence; manter um registro aprovado antigo nao permite burlar changes_requested.

Review registra declaracao humana, nao autentica o operador. Agentes seguem AGENTS.md e so registram decisao explicitamente dada pelo criador. Hero reference_only e bloqueado para aprovacao/exportacao. Export exige Gates1/2 atuais; Gate3 fica pendente ate jogo real. Builds incluem hashes de conteudo/revisoes, e builds antigos nao sao sobrescritos.

## Limites deliberados

- Geracao visual depende de ferramenta na sessao ou autoria em editor. CLI nao desenha novos racas/Jobs por conta propria.
- Sem inferencia de camadas a partir de PNG chapado, espelhamento, upscale/downscale de producao ou retarget de animacao.
- Validacao nao mede qualidade de clusters, identidade entre vistas, luz, mao dominante ou loop. Cores/bounds e alfa sao medidas, nao parecer artistico.
- Perfil baseline e verificacoes geometricas rigorosas podem apontar falhas em arte historica. Mantemos relatorio e original, sem corrigir automaticamente.
- Sem integracao automatica no jogo e sem registro multi-personagem pronto.
- O contrato de arte exige corpo/base sem arma e assets de arma separados, acionados apenas por equipamento + acao. A fabrica ainda nao tem schema/comando para pacotes compartilhados de armas; o jogo atual usa um unico SpriteRenderer por personagem e nao implementa overlays, encaixe, oclusao ou sincronizacao dinamicos.
- O sync depende de fontes esperadas e confere 28/63; mudanca de catalogo exige revisao do importador. Catalogos/fichas locais usam IDs que ainda nao sao canone runtime.
- A geracao por IA pode variar mesmo com referencias e prompts identicos; os artefatos aprovados sao o contrato visual persistente.

## Evolucao indicada

Primeiro aprovar conceito racial de Orc e receita de Warrior/Archer. Demonstrar corpo/roupa sem arma em uma vista nativa. Produzir vistas e Idle/Walk revisados. Em paralelo, definir o pacote independente de armas e a extensao de render acionada por equipamento/acao antes de criar overlays em jogo. Em seguida validar o mesmo Archer no Undead para testar linguagem de classe entre racas. So entao ampliar biblioteca de pecas e integrar registro minimo no Unity. Nao produzir 28x63 combinacoes de uma vez.
