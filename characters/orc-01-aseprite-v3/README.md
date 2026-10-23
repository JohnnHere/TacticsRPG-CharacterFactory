# Orc Warrior — estudo Aseprite V3

**Candidata para comparação com a V2 aprovada.** Mesmo indivíduo e equipamento; nenhuma aplicação na baseline ou no Unity.

- [Comparação interativa](../../reports/orc-aseprite-v3/review.html).
- [Documentação e avaliação](../../reports/orc-aseprite-authorship-v3.md).
- Mestres: `source/aseprite/authored/{concept,attack,hit}.aseprite`.
- Autoria: `source/aseprite/author-orc-v3.lua`.
- Procedência: `source/aseprite/provenance.json`.

Pixels desenhados pelo agente via Lua no runtime do Aseprite, sem image_gen, imagem importada, redução de conceito ou acabamento raster externo. Nove camadas regionais por quadro; não é um rig completo de equipamento nem desenho manual com mouse. Conceito128×128 + Attack5 + Hit3 front_r, todos candidatos.

O desenho atual é mais simples e menos fiel à V2. Não usar como substituto aprovado. Gate1 V3 permanece pendente e faltas no inventário completo de produção deste pacote são esperadas: esta é uma demonstração delimitada. Os estudos de combate reinterpretam o design V2 já aprovado; não constituem lote final baseado em um novo conceito autoaprovado.

O script reprodutível regrava os próprios derivados; copie a fonte para outra versão antes de editar manualmente e não rode o autor sobre alterações que queira manter. Para edições salvas, use o ciclo fork/edição/exportação/revisão.
