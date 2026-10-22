# Orc — ataque basico desarmado nas quatro vistas

Em 2026-10-19 o criador aprovou o primeiro lote: "Aprovo os ataques desarmados; continue as outras vistas." Evidencia com hashes dos 30 PNGs e seis fontes editaveis em characters/orc-unarmed-front-approval-v1.json e source/unarmed-front-v1-review.json de cada roupa. A aprovacao e restrita ao front_r; nao foi convertida em aprovacao final do pacote.

## Entrega e selecao ativa

Produzidos 90 PNGs novos e 18 arquivos .aseprite: cinco poses de soco em front_l, back_r e back_l para Squire, Archer, Apprentice Mage, Acolyte, Rogue e Scout. Os ataques basicos desarmados agora somam 32 clipes nas oito roupas, sem vistas faltantes: 120 PNGs novos/24 fontes editaveis e 40 quadros existentes de Warrior/Brawler reutilizados por caminho e hash. Cada clipe tem cinco quadros a 90ms, acao unica e weaponOverlay=false. Habilidades e gestos legados Attack permanecem separados e intactos.

A selecao vigente e exclusivamente characters/orc-equipment-actions-v1.json. Fontes em source/action-clips-v1 ou v2/basic-unarmed/<vista>/; PNGs suplementares em actions/basic-unarmed/v1 ou v2/<vista>/. Squire front_l usa v2; todas as seis back_l usam v2; Rogue front_l usa v2. Front_r previamente aprovado conserva suas versoes originais. Demais novas fontes usam v1. Versoes nao selecionadas continuam preservadas e nao devem ser descobertas por glob como se fossem alternativas ativas.

As sete variantes conservam sua baseline de 679 PNGs/168 fontes editaveis. Somadas ao Warrior, as oito roupas possuem 776 PNGs legados e 120 suplementares novos: 896 PNGs nativos ativos, incluindo 40 estaticos. A previa tem 896 **referencias de quadros animados**, das quais 856 sao arquivos unicos: 736 legados +160 unarmed, com 40 referencias reutilizadas. Esses dois totais iguais contam coisas diferentes. Nao declarar 896 quadros animados unicos.

## Autoria, reuso e correcoes

Esta etapa recebeu 26 PNGs reais da ferramenta image_gen, modelo nao exposto: 18 fontes selecionadas e oito tentativas nao selecionadas. Auditoria por fonte/prompt/referencias/SHA em characters/orc-unarmed-directions-generation-audit-v1.json; prompts exatos e generation.json acompanham cada folha. Nenhum conceito reduzido, espelhamento, rig 3D ou deformacao procedural da base substituiu os desenhos das poses.

O primeiro Squire front_l herdou protecoes metalicas do guia Warrior e foi descartado. As novas folhas usaram sua propria base aprovada como autoridade de roupa e silhuetas neutras das cinco poses reais do Warrior como referencia de movimento. As seis back_l inicialmente trocaram o soco direito distante por um jab esquerdo proximo; foram redesenhadas com guia cinza detalhado da fonte Warrior corrected-v2, preservando anatomia interna e oclusao. O braco proximo permanece baixo; o direito distante executa o soco parcialmente oculto pelo tronco. Rogue front_l foi corrigido para manter o capuz levantado nas cinco poses. Todas as tentativas anteriores e seus prompts foram preservados.

Guias locais sao derivados 2D de quadros existentes, apenas referencias, nao assets de runtime. characters/orc-unarmed-<vista>-neutral-guide-v1.json registra os quadros de origem; characters/orc-unarmed-back_l-detailed-guide-v2.json verifica RGB cinza e alfa original, com SHA da fonte e da derivacao. Reuse Assessment por componente atualizado nos sete source/production-plan.json: contratos/ferramentas/paletas REUSE_DIRECT; poses REUSE_ADAPTED; novas roupas em movimento CREATE_NEW; armas/runtime/exportador suplementar REQUIRES_EXTENSION. Brawler nao precisa de novos arquivos corporais.

## Verificacao

Extracao dos cinco desenhos reais pelo Pixel Art Fixer, registro inteiro por pelve e alturas relativas documentadas; propria paleta de cada roupa, RGBA8 nativo128x128, ground126 e alfa binario. Nao foram fabricados quadros intermediarios. Os 90 novos quadros e duracoes conferem pixel a pixel com exportacoes reais do LibreSprite. Fontes sao cels raster editaveis; nao representam corpo/roupa separados em camadas.

tools/verify-orc-unarmed-complete-v1.mjs confere os 32 clipes, paletas, proveniencia, arquivos nativos, strips, duracoes e hashes. Tambem preserva os hashes da baseline, das fontes estaticas e dos 30 quadros/seis editaveis front_r aprovados. Relatorio: characters/orc-unarmed-complete-validation-v1.json, zero falhas. Readiness:32/32 clipes nativos e160 referencias, nenhum quadro desarmado faltante; zero bindings de arma provados e readyForUnity=false. Suite local:9/9 PASS.

Previa conjunta: [review-orc-actions-complete-v1.html](../characters/review-orc-actions-complete-v1.html), oito roupas, seis acoes, quatro vistas, com filtros, pausa, scrubbing, velocidade, zoom, fundo e repeticao opcional. "Gesto do Job" preserva o Attack legado; "Ataque basico sem arma" mostra o soco fisico. O navegador Edge carregou todas as896 referencias em HTTP e file://;896/896 hashes RGBA dos canvases exatos via HTTP, strips com dimensoes corretas, controles e ultimo quadro sem repeticao verificados, zero erros JavaScript. A primeira execucao encontrou timeout de carregamento de strip; a repeticao integral passou sem modificar os assets ou afrouxar as verificacoes. Servidor temporario encerrado. Evidencia: characters/orc-actions-complete-browser-v1.json e capturas front_l/back_r/back_l-unarmed-browser-v1.png. Comparacao de pixels em file:// e NOT_RUN pelas restricoes de origem; exibicao foi verificada.

## Marco pendente e retomada

O conjunto completo e o suplemento aguardam uma unica revisao artistica final do criador, conforme AGENTS.md/Gate2 e docs/WORKFLOW.md. Pergunta enviada com a previa concreta. Nenhum Gate consistency novo foi autoaprovado. Cada source/unarmed-complete-v1-review.json fixa frames/fontes por hash e candidateFingerprint; source/complete-v1/review.json conserva a evidencia da baseline das sete variantes. Warrior permanece aprovado/exportado sem alteracoes.

Depois de aprovacao explicita: registrar a decisao sobre os hashes realmente revisados; implementar/verificar exportacao do suplemento versionado, pois o exportador v0.1 ainda exporta apenas a baseline; exportar os sete pacotes e suplemento para dist/. Nao declarar actions/ incluido pelo CLI legado. Armas, projeteis, VFX, sockets/oclusao/eventos e selecao por equipamento exigem autoria/implementacao propria. O projeto Unity foi apenas lido na auditoria anterior; nao houve escrita, integracao ou PlayMode. Parametros de dano/alcance/acerto desarmado continuam TBD no Core.

```powershell
node tools/verify-orc-unarmed-complete-v1.mjs
node tools/check-equipment-readiness.mjs
node tools/build-orc-actions-complete-review.mjs
& 'tmp/pixel-venv/Scripts/python.exe' tools/check-orc-actions-complete-preview.py
```

Os comandos acima sao verificadores/preview da candidata atual; nao reexecutar preparadores, processadores e seletores historicos depois de aprovacao. O verificador atual registra candidata pendente e nao e registrador de aprovacao. Para futura aprovacao, usar evidencia explicita nova e preservar o fingerprint revisado.

## Fechamento posterior

Conjunto/suplemento aprovados condicionalmente pelo criador apos confirmar ataque e reacao Hit sem arma; condicao atendida nas quatro vistas. Exportacao completa e ZIP concluidos, com896 PNGs/216 fontes nas oito roupas. Retomada vigente e links em [ORC_PRODUCTION_EXPORT_V1.md](ORC_PRODUCTION_EXPORT_V1.md). O verificador agora preserva status aprovado se o fingerprint nao mudou. Nao repetir registradores historicos de candidata/aprovacao; consultar reviews/hashes vigentes.
