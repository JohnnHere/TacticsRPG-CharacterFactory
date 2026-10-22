# Memoria visual por raca e Job

Uma ancora global mantem estilo; uma receita aprovada mantem a concepcao de Archer ou de Orc por meses. Receitas registram texto de regras e imagens copiadas para uma versao imutavel. Geracao por IA continua estocastica, mas as referencias aprovadas ficam guardadas.

Receitas de Job descrevem a identidade de classe na roupa, postura e silhueta do personagem sem depender de arma embutida. Armas permanecem assets independentes e sua aparicao depende de equipamento e acao; nao inclua arma como requisito visual de uma receita de personagem.

Depois de criar/revisar o primeiro Orc Archer:

```powershell
node src/cli.mjs recipe-save --kind jobs --from orc-01-archer
```

Isso escreve recipes/jobs/archer.candidate.json. Edite rules: silhueta do Job, materiais, proporcao dos acessorios, paleta da roupa e variacao permitida. No contexto racial, `recipe-save --kind races --from orc-01` prepara rules para anatomia e variacoes, sem universalizar rosto, Job ou faccao. Campos extras nao sao aprovados automaticamente.

Receita candidata tem rules vazias de proposito; a fabrica nao inventa canone. Requer conceito de origem aprovado e ainda correspondente ao hash. Depois da aprovacao explicita do criador:

```powershell
node src/cli.mjs recipe-review --kind jobs --name archer --decision approved --reviewer Criador --evidence "Decisao explicita da revisao visual e regras, data/contexto."
```

O comando cria recipes/jobs/archer/v1/ com recipe.json e copias dos PNGs, e aponta active.json para a versao aprovada. Uma nova aprovacao cria v2, preservando v1. O comando registra a declaracao do operador; nao substitui a avaliacao artistica. Um agente nao se autoaprova.

Uma ficha criada depois com `new --race Undead --job Archer --id undead-novo` usa automaticamente a receita Archer ativa. O prompt inclui as regras e as imagens aprovadas de Archer, com papel explicitamente limitado a linguagem do Job. A pele/rosto/corpo Orc da imagem nao se tornam regras para Undead. A ficha recebe uma copia das regras e vincula versao/hash das imagens. Receitas antigas continuam validas para fichas antigas; editar um arquivo dentro de v1 e detectado como corrupcao.

Para evoluir concepcao, crie uma nova candidata, revise, aprove nova versao e use em fichas novas. Migrar personagem existente pede revisao; nao atualizamos aprovacao/ficha antiga silenciosamente. Uma nova outfit usa a receita ativa para o Job solicitado e preserva a identidade do individuo base.

Nesta entrega ainda nao existem anatomias raciais ou uniformes de classe aprovados alem das fontes gerais/piloto. As fichas Orc/Undead sao o ponto de partida para construir essas receitas.
