# Orc — Idle e Walk nas demais vistas

O criador aprovou explicitamente o Idle v2: "Aprovo o Idle v2; continue as demais vistas." Walk front_r ja estava aprovado. Evidencia e hashes atuais dos14 clipes/70 quadros em characters/orc-front-locomotion-approval-v2.json e source/locomotion-front-v1/review.json de cada classe. O historico do ajuste de respiracao permanece preservado. Nenhum desses PNGs ou editaveis aprovados foi alterado nesta etapa.

## Resultado

Idle4 e Walk6 em front_l, back_r e back_l para Squire, Archer, Apprentice Mage, Acolyte, Rogue, Scout e Brawler. Sao210 PNGs novos e42 editaveis animados .aseprite. Somados ao front_r aprovado,280 quadros de locomocao e56 clipes animados; com35 PNGs e28 fontes estaticas,315 PNGs nativos e84 fontes editaveis ativas. Cada variante tem45/97 PNGs. Restam364 quadros baseline de Attack/Hit/Defeat; acao propria de cada Job ainda exige desenho e sincronizacao. Fontes arquivadas/historicas nao entram na contagem ativa.

Preview: ../characters/review-orc-locomotion-directions-v1.html. Seletor de quatro vistas, Idle/Walk, sete classes, pause/restart/scrub/velocidade/zoom/fundo; base aprovada, strip e fonte editavel mudam com a vista. Front_r indica aprovacao existente; as outras tres vistas animadas aguardam revisao do criador.

## Reuso demonstrado

- REUSE_DIRECT: identidade, conceitos/quatro bases aprovadas, paleta nativa de cada roupa, contratos128x128/ground126, duracoes Idle240ms e Walk73ms, extrator, importador e formato editavel existente.
- REUSE_ADAPTED: poses Warrior nas tres vistas em guias neutros de silhueta. Guias foram compostos dos PNGs existentes, sem espelhamento; sao apenas referencias de movimento. Novas figuras realmente desenhadas por image_gen com a roupa e a camera da propria vista aprovada. A terceira referencia preserva a amplitude discreta do Idle frontal aprovado.
- CREATE_NEW:210 desenhos finais de locomocao nas novas vistas; nao foram fabricados deformando uma base estatica nem recolorindo a armadura Warrior. Corpo nu/rig e troca dinamica de roupas continuam indisponiveis.
- REQUIRES_EXTENSION: combate especifico, armas/projeteis/VFX separados e runtime Unity. Nenhuma integracao foi executada.

## Fontes reais e tentativas

Foram22 chamadas reais image_gen: uma tentativa Squire com30 figuras em seis linhas, rejeitada por cortar a ultima linha, e21 folhas menores aceitas para extracao, cada uma com4 Idle e6 Walk de uma unica vista. Modelo de imagem nao exposto pela ferramenta. A tentativa rejeitada ficou em orc-01-squire/source/locomotion-directions-v1/rejected-30-pose-attempt-01.* com prompt e referencias reais; nunca usada em sprites.

As21 fontes integrais, prompts e generation.json ficam em cada source/locomotion-directions-v1/<vista>/. Cada fila foi isolada por componentes RGBA e recorte exato, sem reescala/espelhamento. Fontes de linha, selecoes, poses individuais, processamento e editaveis em source/animations-v1/<Idle|Walk>/<vista>/. Pixel Art Fixer usa grade alvo explicita,100px de altura base com variacoes de1-2px conforme quadro, paleta da roupa e registro inteiro de cabeca. Fontes brutas podem ter alpha parcial/haze/linhas; componentes e limiares os removem no acabamento nativo. Nao se declara recuperacao exata da grade original nem autoria manual de cada pixel.

Generation, referencia, prompt, recorte, fonte individual, saida e editavel sao vinculados por SHA256. Cada nova direcao foi desenhada por ferramenta, nunca derivada de espelhamento da oposta. Inspecao visual comparativa em source/locomotion-directions-v1/native-review.png de cada pacote: base aprovada, Idle00/02 e Walk00/03 nas tres vistas. Isso permite revisar escala, roupa e lados de acessorios; nao substitui a decisao artistica do criador.

## Verificacao

- 280/280 quadros de locomocao RGBA8,128x128, alpha estritamente0/255, ground126, paleta contida na propria roupa, poses distintas e Idle com variacao de topo no maximo2px.
- 42/42 novos editaveis foram realmente abertos/exportados por LibreSprite1.3;210/210 RGBA e duracoes identicos. Evidencia frontal anterior revalidada, total56 clipes/280 quadros.
- Os70 quadros e14 editaveis front_r correspondem exatamente aos hashes aprovados. Gates concept/base continuam validos. Warrior aprovado permanece intacto.
- Edge headless:280 PNGs carregados em HTTP e file://;280/280 quadros renderizados em canvas HTTP comparados por hash RGBA exato. Quatro vistas/dois estados, troca de bases/strips, sete filtros, controles e zoom verificados; zero erros JavaScript. O servidor efemero foi encerrado. Leituras de pixels no file:// nao executadas por restricao de origem do navegador; exibicao e controles testados.

Relatorios em characters/orc-locomotion-directions-validation-v1.json, orc-locomotion-directions-editor-v1.json e orc-locomotion-directions-browser-v1.json. Cada pacote tem reports/locomotion-directions-v1.json. Capturas reais orc-locomotion-<vista>-<idle|walk>-browser-v1.png. Sao validacoes tecnicas e revisao visual do agente; nenhuma aprovacao artistica inventada.

## Continuar

Revisar somente as42 animacoes novas nas tres vistas; front_r ja aprovado. Registrar a decisao real por hashes em cada source/locomotion-directions-v1/review.json; nunca usar Gate consistency em pacote incompleto. Depois produzir e revisar combate front_r por Job, seguindo as demais vistas. Conjuracao e disparo nao podem ser substituidos por um golpe Warrior recolorido. Armas independentes e seu runtime continuam pendentes. Exportacao final depende de inventario completo e revisao de consistencia; Unity/PlayMode continuam tarefas separadas.

Ferramentas: prepare-orc-locomotion-directions-v1.mjs e build-orc-locomotion-direction-guides.py registram aprovacao/preparam contexto; prepare-orc-locomotion-single-view.py organiza o formato aceito. extract-orc-locomotion-directions.py preserva candidatos e so extrai fontes presentes; import-verify-orc-locomotion-directions.py retoma editaveis ainda nao verificados. verify-orc-locomotion-directions.mjs valida o conjunto atual, build-orc-locomotion-directions-review.mjs monta o preview e check-orc-locomotion-directions-preview.py confere o navegador. Nao executar os importadores/verificadores historicos de front_r para sobrescrever o estado atual.

2026-10-19: criador aprovou as tres vistas de locomocao: "Aprovo as três vistas animadas; continue o combate." Toda locomocao aprovada por hashes. Primeiro combate front_r produzido com91 PNGs/21 editaveis: total406 PNGs/105 fontes ativas,273 quadros restantes. Preview atual: ../characters/review-orc-combat-front-v1.html, somente primeiro combate pendente de revisao. Detalhes em ORC_COMBAT_FRONT_V1.md.
