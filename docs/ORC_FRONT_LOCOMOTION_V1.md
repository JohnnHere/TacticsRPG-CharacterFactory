# Orc — primeiro lote Idle e Walk front_r

O criador aprovou as quatro vistas das sete classes: "Aprovo as vistas das sete classes; continue as animações." Gate base registrado pelo CLI nos sete pacotes, com evidencia e digest. Conceitos/vistas aprovados permanecem intactos. Esta decisao nao aprova automaticamente os clipes novos.

## Entrega deste lote

Idle4 e Walk6 em front_r para Squire, Archer, Apprentice Mage, Acolyte, Rogue, Scout e Brawler: 70 PNGs nativos novos, 14 fontes animadas .aseprite e previews. Cada pacote tem agora15 PNGs (5 estaticos +10 animados); total105 PNGs e42 fontes editaveis (28 estaticas +14 animadas). Restam574 quadros animados no inventario baseline679.

Preview: ../characters/review-orc-front-locomotion-v1.html. Seletor Idle/Walk, sete classes sincronizadas, pause/restart, scrubbing, velocidade, zoom, fundo, base aprovada e fontes por classe. Os quadros sao os PNGs runtime candidatos, sem deformacao no navegador.

## Reuso e autoria reais

As dez poses aprovadas de Idle/Walk front_r do Warrior foram reunidas em guia compartilhado. A primeira fonte Squire conservou partes de armadura Warrior na caminhada e foi rejeitada. O guia seguinte removeu detalhes da roupa e cores, mantendo apenas silhuetas de movimento em cinza. Esses guias sao referencias, nao sprites runtime de outras classes. Cada roupa usa sua base nativa aprovada como referencia visual e paleta; os dez desenhos de movimento foram realmente gerados por image_gen, nao sintetizados movendo o sprite estatico.

Uma folha por classe contem duas linhas: quatro Idle e seis Walk. Foram dez chamadas reais nesta etapa: sete folhas principais, uma tentativa inicial Squire rejeitada e duas edicoes Scout. No Scout, o Idle original foi selecionado; a caminhada original e a primeira edicao foram rejeitadas por trocar/duplicar a manta de quadril. A segunda edicao seguiu um guia anotado de posicionamento e manteve a manta no lado aprovado nos seis quadros. Originais, rejeicoes, guias e prompts reais preservados em source/locomotion-front-v1/. Modelo de imagem nao exposto pela ferramenta.

As linhas selecionadas foram isoladas por componentes RGBA e recortadas sem espelhamento ou reescala. Cada pose nova foi reconstruida pela ferramenta existente Pixel Art Fixer com grade alvo explicita (forced), paleta da propria base e registro inteiro. Algumas fontes possuem haze/alpha parcial fora do personagem; essas fontes nao sao runtime. A selecao por componentes e o processamento produziram alfa final estritamente0/255. O metodo nao demonstra recuperacao exata de grade original nem desenho manual.

## Verificacoes executadas

- Setenta quadros RGBA8/128x128, ground126, sem alfa parcial e com cores contidas na paleta de cada roupa.
- Todos os quadros de cada clipe sao distintos; Idle tem variacao de topo de no maximo2 pixels. Walk possui seis desenhos com as duas metades da passada, revisados visualmente nas fontes/strips; o teste de hashes nao prova sozinho a qualidade do movimento.
- Prompts realmente enviados, referencias, origem completa, recortes de linha, poses extraidas e saidas nativas vinculados por SHA256. A fonte recortada local nao e declarada como saida direta do gerador.
- LibreSprite1.3:14/14 clipes abertos/exportados,70/70 quadros RGBA identicos, contagem e duracao verificadas (Idle240ms/quadro, Walk73ms/quadro). Fontes raster por quadro, sem rig ou separacao automatica de roupa.
- Edge headless:70 PNGs carregados em HTTP e file://. Cada um dos70 quadros renderizados em canvas HTTP foi comparado por hash RGBA ao PNG: identico, sem alfa parcial e ground126. Dois estados, sete filtros e controles de playback/velocidade/zoom/fundo verificados, zero erros JavaScript. O servidor HTTP foi fechado ao terminar; a pagina funciona por arquivo local.

Relatorios em characters/: orc-front-locomotion-validation-v1.json, orc-front-locomotion-editor-verification-v1.json e orc-front-locomotion-browser-v1.json. Capturas reais: orc-front-locomotion-idle-browser-v1.png e orc-front-locomotion-walk-browser-v1.png. Cada pacote possui reports/front-locomotion-validation-v1.json e fontes em source/animations-v1/<Idle|Walk>/front_r/.

## Continuar sem repetir trabalho

Walk front_r foi aprovado pelo criador (42 quadros); Idle recebeu pedido de reduzir expansao do peitoral no quadro3. A revisao do Idle v2 esta solicitada e pendente. docs/WORKFLOW.md e os handoffs de animation orientam revisar Idle/Walk front_r antes das demais vistas; por isso nao se produziu o pacote inteiro automaticamente. Depois da decisao real, registrar evidencia/digest dos clipes aprovados em source/locomotion-front-v1/review.json ou registro equivalente de lote, sem usar Gate consistency como substituto de revisao parcial. So entao expandir Idle/Walk para outras tres vistas (210 quadros), seguindo depois Attack/Hit/Defeat por classe (364 quadros baseline). Disparo Archer e conjuracao Mage/Acolyte precisam de novas poses e sincronizacao; nao usar um soco Warrior recolorido.

Gate consistency completo exige pacote completo e decisao real do criador. Export, Unity e PlayMode continuam pendentes. Nenhuma arma, overlay de equipamento, roupa dinamica ou receita visual foi autoaprovada/implementada.

Ferramentas reutilizaveis: prepare-orc-front-locomotion.mjs, extract-front-locomotion.py, import-animation-clip.mjs, import-verify-front-locomotion.py, verify-orc-front-locomotion.mjs, build-orc-front-locomotion-review.mjs e check-orc-front-locomotion-preview.py. O preparador bloqueia fonte existente; o extrator preserva candidatos existentes. No LibreSprite, definir --format antes de --data e do input garante exportacao correta dos metadados.

## Revisao Idle v2

Feedback literal e hashes anteriores em cada source/locomotion-front-v1/review.json. Sete edicoes reais pela ferramenta image_gen (modelo nao exposto); PNGs integrais, prompts e referencias em source/idle-subtle-v2/. A ferramenta alterou partes que deveriam ficar fixas; por isso o acabamento recompôs somente torso/ombros na regiao nativa [24,47,104,74], preservando todos os pixels externos do quadro original. Grade alvo100, paleta da propria roupa e registro de cabeca; largura por linha limitada ao quadro neutro mais1 pixel por lado no pico, com transicao para pescoco/pulsos. Este acabamento local de poses ja desenhadas nao constitui rig nem geracao de movimento de figura estatica.

Somente idle_front_r_02.png mudou em cada pacote. Os63 outros quadros e os sete editaveis Walk permanecem byte-identicos. Fontes anteriores em previous-idle/, novo historico misto por quadro em clip.json e assets.json. Sete Idle .aseprite exportados no LibreSprite:28 quadros RGBA e duracoes240ms identicos. Verificacao de todos70 PNGs e navegador repetida sem falhas. characters/orc-idle-subtle-v2-validation.json demonstra regiao alterada e preservacao; characters/review-orc-front-locomotion-v2.html permite revisar loops finais. Walk ja aprovado; pedir somente revisao do Idle antes das outras vistas.

## Etapa seguinte concluida

O criador aprovou Idle v2: "Aprovo o Idle v2; continue as demais vistas." Aprovacoes/hashes atuais em characters/orc-front-locomotion-approval-v2.json. Idle/Walk front_l,back_r,back_l produzidos e em revisao; conjunto atual315 PNGs/84 editaveis ativos e364 quadros de combate pendentes. Documento atual: ORC_LOCOMOTION_DIRECTIONS_V1.md; verificacoes historicas acima descrevem o lote inicial.
