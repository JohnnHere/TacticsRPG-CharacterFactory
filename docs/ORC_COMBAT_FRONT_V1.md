# Orc — primeiro lote de combate front_r

O criador aprovou as tres vistas de locomocao: "Aprovo as três vistas animadas; continue o combate." Evidencia e hashes de cada clipe em source/locomotion-directions-v1/review.json; indice em characters/orc-locomotion-directions-approval-v1.json. Com Idle v2 e Walk front_r aprovados anteriormente, toda locomocao das sete classes esta aprovada. Nenhuma aprovacao de combate foi inferida dessa decisao.

## Entrega

Attack5, Hit3 e Defeat5 em front_r de Squire, Archer, Apprentice Mage, Acolyte, Rogue, Scout e Brawler. Novos91 PNGs nativos e21 fontes animadas .aseprite; total406 PNGs e105 fontes editaveis ativas. Cada variante possui58/97 PNGs e15 fontes ativas (quatro estaticas +onze animadas). Restam273 quadros baseline de combate nas outras tres vistas. Fontes historicas/rejeitadas ficam fora da contagem ativa.

Preview: ../characters/review-orc-combat-front-v1.html. Seletores Attack/Hit/Defeat e classe, sete personagens sincronizados, pause/restart/scrub/velocidade/zoom/fundo, repeticao opcional da previa e parada no ultimo quadro. Os clipes sao one-shot no manifesto; repetir a previa nao altera esse dado.

## Gestos de Job

| Classe | Gesto do corpo em Attack | Momento visual principal (indice0) |
|---|---|---|
| Squire | Preparacao e golpe descendente com braco direito | 3 |
| Archer | Braco esquerdo estendido, direita puxa junto ao rosto e solta | 3 |
| Apprentice Mage | Reune maos, estende palma direita cruzando o peito | 2 |
| Acolyte | Prece, bencao com palma direita, apresenta maos | 2 |
| Rogue | Preparacao baixa e estocada rapida de direita | 2 |
| Scout | Mira, arremesso de direita e continuacao descendente | 2 |
| Brawler | Guarda, soco reto de direita, continuacao e retorno | 2 |

Estes sao gestos visuais para revisao, nao habilidades de gameplay novas nem eventos implementados no Unity. O slot baseline Attack abriga as poses do corpo; casts/disparo, contato, equipamento, projeteis e VFX precisam de runtime e sincronizacao proprios. Maos vazias em todos os quadros. Armas e efeitos nao estao embutidos nem declarados prontos.

## Reuso e fontes reais

- REUSE_DIRECT: identidade, roupas e bases aprovadas, paleta nativa de cada variante, contrato128x128/ground126, duracoes base (Attack90ms, Hit80ms, Defeat120ms), importador e escritor ASE existentes.
- REUSE_ADAPTED: Hit/Defeat Warrior aprovados como guia de silhuetas cinza; nunca sprites finais de outra roupa. Novas poses de corpo/roupa foram realmente desenhadas pela image_gen. Nenhum quadro foi criado animando uma figura estatica ou espelhando outra vista.
- CREATE_NEW: sete conjuntos de13 desenhos e as novas poses de ataque proprias por Job. Mesmo individuo, nao sete individuos novos; sem rig de corpo nu/troca de roupa.
- REQUIRES_EXTENSION: armas independentes, anexacao/oclusao e eventos das acoes, gameplay de cast/disparo, integracao Unity e PlayMode. Nada disso foi simulado por composicao offline.

Foram11 chamadas reais image_gen: sete folhas13 poses (5/3/5 em tres linhas) e quatro edicoes Attack para Mage/Brawler. Nas fontes iniciais, Mage usou a esquerda para conjurar e Brawler trocou o braco na continuacao. Primeiras edicoes v2 nao corrigiram a topologia e foram rejeitadas. Segundas v3 seguiram guias explicitos do braco direito cruzando o peito e foram selecionadas para extracao. Hit/Defeat dessas duas classes continuam vindo das folhas originais. Modelo de imagem nao exposto pela ferramenta.

Fontes integrais, prompts exatos, referencias e hashes em source/combat-front-v1/. A linha de ataque original foi recortada como referencia de edicao; Brawler recebeu guia com o terceiro gesto repetido na quarta celula SOMENTE PARA REFERENCIA da topologia, e Mage recebeu a silhueta cinza dessa pose. Os PNGs de producao resultam de desenhos novos da ferramenta, distintos nos cinco quadros. Guias nao sao animacao de producao. Tentativas v2 e seus prompts permanecem preservados e marcados rejeitados; generation.json seleciona v3 apenas para Attack.

Cada linha selecionada e isolada por componentes alpha e recorte RGBA exato, sem espelhamento. Algumas fontes brutas possuem haze/alpha parcial; limiares160/128 e selecao de componente produzem transparencia binaria final. Fontes de linha, poses individuais, processamento, strips/APNGs e fontes editaveis em source/animations-v1/<Attack|Hit|Defeat>/front_r/. Fonte recortada local nao e declarada saida direta do gerador.

## Extensao minima do processamento

extract-animation-sheet.py agora aceita alturas explicitas opcionais e registro por pelve. O comportamento padrao continua com as alturas/registro de cabeca anteriores. Neste lote, a primeira pose de cada linha calibra100px; as demais conservam a altura relativa desenhada. Assim um punho acima da cabeca aumenta a silhueta em vez de encolher o corpo. Registro por pelve usa a mediana da silhueta entre y79..94; evita confundir punho levantado com cabeca. Translacao inteira e limitada ao canvas, nunca deformacao de runtime. Defeat mantem a queda real e diminui progressivamente a altura.

Em algumas faixas Attack, o alcance horizontal do braco entra no mesmo intervalo X dos pes da figura vizinha, mas os componentes nao se tocam nem compartilham pixels. Essas fontes foram inspecionadas visualmente e extraidas com permissao explicita de caixas X sobrepostas; o numero de componentes completos continua sendo obrigatorio. Nao foi inventado quadro ausente.

O importador/editor existente passou a aceitar --batch e --report e estados do manifesto, mantendo o default de locomocao. Fontes existentes sao preservadas; retoma apenas clipes completos/verificacoes ainda ausentes. Nao executar verificadores historicos de estagios anteriores para rebaixar aprovacoes/contagens.

## Verificacoes

- 91/91 quadros RGBA8,128x128, alpha0/255, ground126, paleta contida na roupa, poses distintas e queda progressiva. Prompts/referencias/fontes/recortes/processamento/editaveis vinculados por SHA256.
- 21/21 clipes realmente exportados por LibreSprite1.3;91/91 RGBA e duracoes identicos aos PNGs runtime candidatos. Fontes raster por quadro, sem rig nem camadas de roupa dinamica.
- 280 quadros e56 editaveis de locomocao correspondem exatamente aos hashes aprovados. Conceitos/bases permanecem aprovados; Warrior97 PNGs e20 fontes animadas preservados por indice/hash.
- Edge headless:91 PNGs em HTTP e file://;91/91 quadros canvas HTTP com hash RGBA exato, tres estados, sete filtros, zoom/playback/scrub/fundo e parada final one-shot verificados, zero erros JavaScript. Leitura de pixels file:// nao executada por restricao de origem; exibicao/controles testados. Servidor efemero encerrado.
- Suite local npm test:6/6. Verificacao adicional do caminho antigo do extrator preservou geometria alpha/crop/registro em6/6 Walk. Reprocessar as cores NAO foi byte-identico: duas chamadas diretas ao quantizador com mesma entrada tambem diferiram em354 pixels RGBA, com alpha identico. Isso nao alterou arquivos aprovados; ensaio feito somente em tmp/. Evidencia em characters/orc-combat-extractor-compatibility-v1.json. Nao prometer reproducao bit a bit; preservar e reutilizar os PNGs finais aprovados, editaveis e hashes. A causa foi localizada no cv2.kmeans, que depende do RNG global do OpenCV apesar do seed de amostragem existente. recover-native-sprite.py agora reinicia esse RNG com seed42 por asset e registra o valor. Tres reconstrucoes novas no mesmo ambiente foram byte-identicas. Os91 quadros deste lote foram produzidos antes dessa correcao e NAO foram reprocessados; os PNGs/editaveis e hashes atuais sao a autoridade. Nao se garante identidade entre versoes/plataformas nem reproducao das cores historicas sem o estado anterior do RNG.

Relatorios: characters/orc-combat-front-validation-v1.json, orc-combat-front-editor-v1.json e orc-combat-front-browser-v1.json; cada pacote tem reports/combat-front-v1.json. Comparacao visual completa em source/combat-front-v1/native-review.png; capturas reais orc-combat-front-<attack|hit|defeat>-browser-v1.png. Validacao tecnica nao concede aprovacao artistica.

## Proxima etapa

Pergunta de revisao do primeiro lote ja enviada. Registrar decisao real e hashes dos21 clipes em cada source/combat-front-v1/review.json, sem Gate consistency em inventario incompleto. Se aprovado, expandir estes gestos para front_l/back_r/back_l (273 quadros), sem espelhamento e preservando mao/acessorios. Depois revisao completa e exportacao local; integracao Unity e tarefa separada. Nao autoaprovar conceitos, clipes, receitas, armas, VFX ou gameplay.
