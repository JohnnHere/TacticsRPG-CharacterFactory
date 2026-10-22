# Orc — entrega de producao corporal e ataque desarmado

Em2026-10-19, o criador autorizou continuar apos confirmar os assets de hit normal desarmado: "A animação de conjuração de habilidades e ataques armados é importante, vc incluiu tbm os assets de hit normal estando desarmado ? se sim, pode continuar tocando a tarefa". A condicao foi verificada: todos possuem ataque basico desarmado fisico e reacao Hit nas quatro vistas. Resposta ao preview completo, com as limitacoes de armas/VFX/Unity declaradas. Evidencia literal e interpretacao restrita em characters/orc-actions-complete-approval-v1.json; sete Gates consistency registrados pelo CLI. Gate Warrior original foi preservado. Nao foi registrada aprovacao de armas inexistentes, de todas as habilidades de talentos ou de integracao Unity.

## Arquivos entregues

[Indice dos pacotes](../dist/orc-basic-production-v1/3b2d54ccb738bc2d/index.html) · [ZIP completo](../dist/orc-basic-production-v1/3b2d54ccb738bc2d/orcs-production-v1.zip) · [Previa das animacoes](../characters/review-orc-actions-complete-v1.html).

O ZIP tem10,520,908 bytes, oito pacotes,896 PNGs nativos e216 arquivos .aseprite selecionados. Cada pacote contem Assets/Resources/Characters/<id>/, factory-manifest.json, factory-actions.json, Source/, source-manifest.json e package-hashes.json. Fontes raster editaveis por cel, sem corpo/roupa separados em camadas. Candidatos de geracao e prompts exatos permanecem nos pacotes de autoria da fabrica; somente fontes ativas entram na distribuicao.

| Classe | PNGs | Editaveis | Build completo |
|---|---:|---:|---|
| Warrior | 97 | 24 | [actions-a256d0fa8844d002](../dist/orc-01/actions-a256d0fa8844d002/ACTIONS.md) |
| Squire | 117 | 28 | [actions-3f286d1422840e34](../dist/orc-01-squire/actions-3f286d1422840e34/ACTIONS.md) |
| Archer | 117 | 28 | [actions-7de1b434775adeee](../dist/orc-01-archer/actions-7de1b434775adeee/ACTIONS.md) |
| Apprentice Mage | 117 | 28 | [actions-dfd6774b982cad62](../dist/orc-01-apprentice-mage/actions-dfd6774b982cad62/ACTIONS.md) |
| Acolyte | 117 | 28 | [actions-9bfbd057e2a38857](../dist/orc-01-acolyte/actions-9bfbd057e2a38857/ACTIONS.md) |
| Rogue | 117 | 28 | [actions-f53c7646dfc4cfce](../dist/orc-01-rogue/actions-f53c7646dfc4cfce/ACTIONS.md) |
| Scout | 117 | 28 | [actions-3bc57bf5e0124de4](../dist/orc-01-scout/actions-3bc57bf5e0124de4/ACTIONS.md) |
| Brawler | 97 | 24 | [actions-fe43acc503b37e6b](../dist/orc-01-brawler/actions-fe43acc503b37e6b/ACTIONS.md) |

Os117 PNGs das seis roupas com novos socos sao97 legados +20 unarmed. Warrior/Brawler possuem97 cada, com20 Attack referenciados novamente como basic.unarmed; nao ha duplicacao desses PNGs no mesmo pacote. Fontes:24 legadas por roupa +quatro desarmadas para seis roupas. Total896 PNGs inclui40 estaticos;896 referencias animadas na previa correspondem a856 arquivos animados unicos. Nao confundir as contagens.

## Semantica das acoes

- Idle e Walk permanecem aprovados, com Idle sutil v2 quando aplicavel.
- Attack legado conserva o gesto por Job, incluindo conjuracao Mage/Acolyte e gestos de disparo/estocada/arremesso. O corpo foi aprovado; nenhuma arma ou magia visivel foi embutida. Esses gestos nao sao o inventario de todas as habilidades das arvores de talentos.
- basic.unarmed tem cinco poses a90ms, acao unica, weaponOverlay=false e quatro vistas por roupa. Para o comando Atacar sem arma, usar este perfil explicito; nao escolher conjuracao pelo Job.
- Hit tem tres poses a80ms nas quatro vistas e serve como reacao corporal ao receber golpe, tanto armado como desarmado. O runtime futuro deve limpar arma/efeitos/eventos ao interromper ataque por Hit/Defeat.
- Defeat tem cinco poses a120ms. Ataques/Hit/Defeat nao repetem automaticamente; a repeticao do preview e somente para revisao.

## Exportador e protecoes

Comando novo: `node tools/export-orc-actions-v1.mjs`. src/action-export.mjs planeja o suplemento, exige aprovacao explicita e fingerprint atual, quatro vistas reais, hashes, timing, RGBA/canvas/chao e fonte editavel atual. A exportacao completa exige os tres gates locais (concept/base/consistency) e validacao full da baseline. Nao busca fontes por glob nem escolhe versoes rejeitadas. Novos PNGs sao normalizados em Actions/basic-unarmed/v1/<vista>; versoes de autoria v1/v2 continuam registradas no source-manifest. Warrior/Brawler referenciam Animations/Attack existentes dentro do proprio pacote.

O comando `node src/cli.mjs export` continua entregando so a baseline; os sete builds baseline tambem foram criados e o Warrior dist/orc-01/9b89aad88c27de68 original foi preservado. A extensao gera novos builds actions-<hash>, sem modificar builds anteriores. O hash identifica baseline, aprovacao/suplemento, fontes, contratos e codigo do exportador. Todos os arquivos estagiados recebem SHA256; uma segunda execucao preservou os mesmos builds e conferiu seus bytes. Builds intermediarios anteriores foram preservados; a selecao vigente e reports/orc-actions-export-v1.json, nunca a ordem de pastas.

Arquivo consolidado: `& 'tmp/pixel-venv/Scripts/python.exe' tools/package-orc-production-v1.py`. Le somente os oito builds selecionados, verifica todos os arquivos contra package-hashes, cria ZIP e confere CRC e SHA de cada entrada. Evidencia em reports/orc-production-archive-v1.json. SHA256 ZIP:`7b26df7489d4d87ec42dc0f16d7cd6f4e4cc20a0669b2e2ab519e3e12ad0d7a2`.

## Validacao e limites

Doctor sem erros de referencias. Suite completa11/11 PASS, incluindo dois testes de exportacao que bloqueiam aprovacao ausente/desatualizada, direcao faltante, bytes nativos/editaveis alterados, overlay indevido e reuso falso. Verificador nativo completo sem falhas, preservando os hashes aprovados; ele agora conserva a aprovacao do suplemento quando o fingerprint continua igual. UI da previa atualizada para status aprovado/exportado, sem modificar pixels. As896 referencias ja passaram por verificacao exata de canvas e controles no Edge; metadados finais nao alteram a arte.

Exportacao: oito pacotes,896 PNGs,216 fontes,0 FAIL. ZIP:1186 entradas,1184 hashes de arquivos exportados verificados mais README/MANIFEST conferidos; CRC PASS. Evidencias em reports/orc-actions-export-v1.json e reports/orc-production-archive-v1.json.

Continuam pendentes:assets independentes de armas/projeteis/VFX; sockets/mascaras/oclusao/tempos com composicoes reais; bindings por familia de arma e movimento corporal; mapeamentos de habilidades especificas; gameplay desarmado no Core e selecao/carregamento de acoes em Presentation. Nenhum desses suportes foi simulado pela exportacao. readyForUnity=false, zero bindings provados. Nenhum arquivo do projeto irmao foi alterado; integracao e PlayMode/Gate3 exigem tarefa separada autorizada. Proxima entrega artistica: familia de armas e suas combinacoes, com revisoes antes de expandir o lote.
