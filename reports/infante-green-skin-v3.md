# Infante de Ferro — pele verde v3, referência oficial Warcraft

2026-10-25. Criador pediu mais escuro novamente e a mesma paleta do Orc de World of Warcraft. A referência anterior era uma interpretação livre; nesta rodada foi consultada uma imagem oficial do Orc publicada no catálogo de raças da Blizzard.

Fonte da imagem: https://blz-contentstack-images.akamaized.net/v3/assets/blt3452e3b114fab0cd/blt88a8b95c54b38b1f/682b6c5104555b80321d9a10/Orc.png ; página https://worldofwarcraft.blizzard.com/game/races . A página individual /en-us/game/races/orc retornou 403, mas a imagem oficial foi obtida, inspecionada e usada para análise de paleta. Cópia de referência somente em tmp/, sem redistribuir a ilustração na biblioteca.

Foram amostradas 16 cores reais de pele, em regiões de rosto/orelha, com coordenadas e SHA256 registrados em experiments/infante-green-skin-v3/palette.json. Seleção dos tons mais escuros/médios para reduzir a luminosidade; excluída a iluminação especular amarela da testa. Isso ancora esta variante a uma imagem específica, não declara uma paleta universal de todos os modelos/iluminações de Warcraft.

No Aseprite, tools/aseprite/infante-green-skin-v3.lua aplica a nova rampa apenas aos pixels de pele já registrados. Não copia rosto, equipamento ou pixels da ilustração da Blizzard. Arte herdada PixelLab e retoques anteriores preservam sua procedência. Sem nova geração ou cobrança PixelLab.

Mestres novos no pacote 05 em source/aseprite/green-skin-v3/source/warcraft-green-concept.aseprite e warcraft-green-idle.aseprite. PNGs/clip/variant em source/studies/PaletteVariants/green-skin-v3/. Armadura, presas, silhueta, alpha, cinco poses do Idle e tempos 400/450/500/450/400 ms preservados. As três versões anteriores e seleção original continuam intactas. Não há alteração global de paleta, aprovação automática ou integração Unity.

Biblioteca: Estudos Comparativos/Infante de Ferro - Pele Verde/, quarta e última opção Verde Warcraft. Há conceito, Idle, mestres e PALETA-E-REFERENCIA.json. Exportação Aseprite PASS (seis quadros comparados); viewer PASS, 20 quadros e 32 hashes de cópias, abertura local/mobile e zero erros JavaScript. Check de alteração seletiva em reports/infante-green-skin-v3/check.json. Próximo: criador avaliar o tom; não propagar sem aprovação.
