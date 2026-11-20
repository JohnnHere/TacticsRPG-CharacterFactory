# Experimento 02 — corpo esquelético e espada independente

`back_l` · Sword · cinco poses estruturais · **zero chamadas pagas ao PixelLab**

Página de revisão: `experiments/main-orc-skeleton-02/stage-f/index.html`

---

## A. Resultado das hipóteses

| Hipótese | Veredito | Base |
|---|---|---|
| **H1 — Anatomia do corpo** | **REJEITADA para a via gerada** | O corpo produzido no Experimento 01 tem a arma fundida no mesmo raster em todos os 14 quadros. Não há camada: separar exigiria apagar geometria de arma sobre o braço e depois inventar a mão e o antebraço que estavam atrás dela. `CONTAMINATED_BODY` nos quadros auditados. |
| **H2 — Espada independente** | **SUPORTADA** | A arma oficial foi reutilizada sem redesenho e composta em cinco poses. Em todas elas a arma mantém exatamente **706 pixels opacos** — a rotação não erodiu nem inflou a silhueta. **0** pixels de alfa parcial e **0** pixels claros neutros nas 15 renderizações. A camada de corpo permanece RGBA idêntica à origem. |
| **H3 — Pegada e composição** | **PARCIALMENTE SUPORTADA** | O contrato de ligação funciona: cada pose usa o ponto real da mão como pivô, e o cabo fica atrás da luva com a guarda fora da mão. A pegada é legível em 8×. O que limita não é o método de ligação, é o **corpo**: a pose 08 herdada tem o braço estendido lateralmente, então nenhuma ligação correta transforma aquela pose num corte diagonal. |

## B. Artefatos

| O que | Onde |
|---|---|
| Auditoria do corpo do Exp01 | `stage-a/report.md`, `stage-a/measurements.json`, `stage-a/evidence/` (19 recortes) |
| Cinco poses anatômicas + contrato | `stage-bcde/report.md`, `stage-bcde/attachment.json` |
| Corpo, arma e composição | `stage-bcde/{body-only,weapon-only,composite}/00,05,08,09,13.png` |
| Recortes de mão e punho 8× | `stage-bcde/evidence/*-hand-wrist-8x.png` (15) |
| Mestres editáveis | `stage-bcde/source/NN.aseprite` (5, camadas `weaponBack → body → weaponFront → handFront`) |
| Revisão interativa | `stage-f/index.html` |

## C. Achados técnicos

### Corpo
O Experimento 01 não entrega corpo reutilizável. A arma está no mesmo raster e, nos quadros 04–07,
o membro erguido é ambíguo a ponto de não haver base para apagar a arma e afirmar que o braço
permanece válido. A auditoria foi honesta quanto aos próprios limites: proporção de cabeça e
comprimentos de membro no raster gerado não puderam ser medidos com confiança, então estão
declarados como **não medidos**, não como aprovados.

A alternativa de corpo limpo — as camadas do clipe de produção — é de fato limpa, mas carrega a
coreografia já reprovada pelo criador. É por isso que "corpo limpo" e "corpo correto" não são a
mesma coisa neste experimento.

### Arma
A rotação por amostragem inversa no Aseprite, com arredondamento ao pixel inteiro, preserva
materiais e espessura. O serrilhado diagonal é da grade, não interpolação. Nenhum halo.

### Contorno claro — causa
Não apareceu nenhum. A separação por camadas eliminou a condição que produzia o artefato: quando
corpo e arma são desenhados juntos, a borda clara nasce do encontro de dois materiais no mesmo
raster. Com a arma em camada própria e a luva restaurando o primeiro plano, o contorno não tem onde
se formar. Isso responde ao item 5 da documentação pedida.

### Pegada
| Pose | O que se vê em 8× |
|---|---|
| 00 | luva fecha sob a guarda, pomo visível abaixo |
| 05 | cabo vertical, luva abaixo da guarda, pomo saindo por baixo |
| 08 | punho desce, guarda à frente da luva, cabo atravessando a mão |
| 09 | pegada mantida com a arma em diagonal baixa |
| 13 | mesmo encaixe de 00 |

## D. Uso de recursos

| Item | Valor |
|---|---|
| Chamadas pagas ao PixelLab | **0** — saldo 1256,70 antes e depois, inalterado |
| Arte gerada | nenhuma |
| Arte reutilizada | 5 quadros de corpo do clipe de produção, 1 arma oficial, 2 arquivos de juntas do Exp01 |
| Correções locais | nenhuma sobre o corpo; a arma foi composta e transformada no Aseprite |
| Testes executados | verificação headless da página de revisão do DEV (30 imagens, 0 quebradas, 0 erros) e da página do Estágio F (22 imagens, 0 quebradas, 0 erros, pose, zoom, passo e esqueleto exercitados) |

## E. Segurança

- **Mestres de produção: inalterados.** Nenhum arquivo em `characters/` foi criado ou modificado
  durante o experimento, verificado por data de modificação desde 16:36.
- **Unity: inalterado.** 0 arquivos modificados em `../TacticsRPG`.
- **Candidato de produção: inalterado.** Nenhum manifesto tocado, nada promovido.
- **Git:** nada commitado. Todo o experimento vive em `experiments/main-orc-skeleton-02/`.

## F. Recomendação

O método é promissor na metade que faltava provar: **compor uma arma independente sobre um corpo
separado funciona, e resolve o halo**. A metade que falta é o corpo — e não existe corpo correto
disponível hoje.

Aplicando a moldura de decisão do criador:

> *Corpo anatomicamente ruim ou contaminado → testar geração `body-only` orientada por esqueleto,
> com orçamento controlado.*

É exatamente esse o caso. O corpo do Experimento 01 está contaminado; o corpo de produção está
limpo mas tem a coreografia reprovada. O próximo passo justificado é o **Experimento 03**:

1. Gerar **somente o corpo**, sem arma nenhuma na imagem de referência nem na descrição.
2. Usar as cinco poses deste experimento como guia, com orçamento fixo e declarado.
3. Reaproveitar o contrato de ligação e as camadas já validadas aqui para compor a espada.
4. Julgar com esta mesma página de revisão.

Não é recomendável escalar para as 14 intermediárias antes de o corpo existir. Produzir 14 quadros
sobre um corpo contaminado repete o erro que consumiu as rodadas anteriores.

## G. Documentação atualizada

As lições verificadas foram registradas em `docs/RECIPES.md` e o aviso da rodada em
`docs/MAIN_ORC_COMBAT_POLISH.md`. Resumo do que ficou aprendido:

1. **Sintoma** — halo claro e lâmina inconsistente nas vistas de costas.
2. **Causa confirmada** — corpo e arma sendo desenhados no mesmo raster; nenhum ajuste de
   luminância conserta isso.
3. **Correção** — arma em camada própria, posicionada pelo ponto real da mão de cada pose, com a
   luva restaurada em primeiro plano.
4. **Evidência** — 706 pixels opacos constantes, 0 alfa parcial, 0 pixel claro neutro.
5. **Regra reutilizável** — em ataque com arma, nunca gerar corpo e arma juntos; compor por camadas.
