# back_l/Sword — reparo localizado V6-QA-02

**TECHNICALLY_COMPLETE** para este reparo. **ARTISTIC_REVISION_REQUIRED**, `PENDING_CREATOR`: nova revisão do mesmo QA independente continua necessária. Não é uma decisão sobre V6-QA-01, nem uma nova avaliação das demais células.

Fonte do achado: [parecer Sol](../../qa-sol/report.md) e [result.json do QA](../../qa-sol/result.json). A medição local anterior reproduziu exatamente os três grupos de pixels abaixo do chão descritos no parecer.

## Alteração

Somente o binding das camadas `weaponBack` e `weaponFront` em **F07/F08/F09** foi ajustado no Aseprite **1.3.18.6**, batch `--noinapp`, perfil `tmp/aseprite-v6-rear-profile`. Ângulos **145°/175°/185° → 125°/120°/110°**. Palmas compostas mantidas em **[158,153] / [149,155] / [151,152]**, escala **1** e asset independente original preservado. A recuperação passa de uma orientação baixa para uma saída diagonal suspensa, com elevação gradual em F09. O ajuste não desloca o item para longe da luva.

Não houve chamada PixelLab, edição do corpo ou da luva, nem alteração de duração. As quatro camadas do mestre composto mantêm ordem/nome, e as posições dos cels de body/handFront também foram conferidas após reabertura. F00–F06/F10/F11 permanecem iguais, inclusive bookends. `back_l/Axe` e os dois `back_r` são byte-idênticos em todos os seus arquivos.

## Bboxes antes/depois

Coordenadas **inclusivas**, união dos pixels opacos das duas camadas de arma, canvas composto 256; plano de apoio `groundY=190`.

| Quadro | Bbox inteira antes | Bbox inteira depois | Pixels abaixo de 190, antes → depois | y máximo depois | Folga |
|---|---|---|---|---:|---:|
| F07 | [150,142,193,201] | [147,144,207,187] | 87 → **0** | 187 | 3 px |
| F08 | [138,143,163,214] | [138,147,200,185] | 195 → **0** | 185 | 5 px |
| F09 | [138,140,163,211] | [139,144,207,173] | 166 → **0** | 173 | 17 px |

Bboxes anteriores restritas a `y>190`: F07 **[180,191,193,201]**, F08 **[148,191,158,214]**, F09 **[143,191,153,211]**. Depois: **vazias nos três quadros**. O reparo verifica ainda a condição mais estrita de nenhum pixel de arma em `y≥190`: a ponta fica acima do plano, não apenas sobre ele. Essas medidas comprovam a correção geométrica localizada; o julgamento de naturalidade e a revisão temporal independente continuam pendentes.

## Fontes e derivados

O mestre composto salvo foi reaberto antes da alteração, e suas camadas foram comparadas com os PNGs existentes. Após salvar o ajuste, foram reexportados somente os PNGs de arma e os compostos F07–F09, além da tira composta completa. O mestre nativo 128, os PNGs nativos, a tira nativa, body e handFront não foram regravados.

Foi salvo também `source/weapon-binding.aseprite`, mestre próprio das duas camadas de arma, 12 quadros com os mesmos tempos. Uma segunda reabertura dos dois mestres conferiu armas, compostos, 12 tiles da tira e tempos contra os derivados. Os mestres independentes do item Sword não foram alterados. [Roundtrip](roundtrip.json).

`clip.json` registra ângulos, hashes reais e proveniência deste reparo. Os dois patch-manifests que referenciam back_l/Sword, `weapon-patch.json` integrado e `candidate28manifest.json` receberam os hashes da célula atualizada; os registros das outras células foram preservados. Snapshots e freezes anteriores continuam históricos, pois este reparo autorizado muda explicitamente o mestre composto e três poses de arma. [Hashes e lista exata de manifestos atualizados](result.json).

Foram conferidos **299 arquivos protegidos byte-idênticos**, cobrindo os outros três clipes, corpo/luva/nativos, bookends/quadros não alvo e fontes do item independente. Toda a autoria/exportação artística ocorreu no Aseprite; Pillow somente mediu pixels e montou a folha de diagnóstico.

## Revisão

[Preview antes/depois](preview.html) com chão sobreposto pela interface, corpo preservado, 1×/0,5×, passo e escala tática. [Folha F07–F09](before-after.png), [checks do player](preview-check.json), [plano de binding](binding-plan.json), [resultado com bboxes/hashes](result.json). O antes usa cópias dos compostos anteriores ao reparo, não o V5.

Nenhuma escrita no Unity, promoção ou mudança em outro ataque. Esta entrega para neste reparo e aguarda a re-revisão independente da versão exata.
