# Auditoria independente — Estágio A

**Veredito parcial: ARTISTIC_REVISION_REQUIRED.** O corpo do Experimento 01 **não está demonstrado como base limpa utilizável**. Em vários quadros a espada é parte do mesmo raster; nos quadros 04–07 o membro erguido é visualmente ambíguo e não há base para apagar a geometria e afirmar que o braço permanecerá válido. A alternativa de produção apresenta corpo separado visualmente, mas os resultados abaixo não constituem aprovação artística.

## Método e limites

As coordenadas são do canvas 256×256, origem no canto superior esquerdo; bbox é inclusiva e conta todo alfa > 0. No experimento esta é a silhueta **corpo + arma**, não uma bbox do corpo isolado. Na produção mede-se somente a camada body, sem weaponBack, weaponFront ou handFront; a mão eventualmente separada não está incluída. Última linha é apenas um indicador da base da silhueta, comparado ao groundY=190 declarado no clip; não mede individualmente os tornozelos. Recortes 3× por vizinho mais próximo em evidence preservam os pixels.

Não foi possível segmentar com confiança cabeça, articulações, arma fundida ou contornos: proporção cabeça/corpo, comprimentos de úmero/antebraço/coxa/canela, sua variação, número de pixels de contaminação e contagem de pixels órfãos ou penhascos de alfa permanecem **não medidos**, não zero. Perspectiva e oclusão também impedem tratar variações projetadas como variações de comprimento real. Sem essas medições a auditoria exigida pelo brief está incompleta; não se deve interpretar este relatório como verificação integral.

## Medições objetivas disponíveis

| Conjunto e quadro | bbox [xmin,ymin,xmax,ymax] | Dimensão px | pixels alfa > 0 | alfa parcial | y inferior (diferença de 190) |
|---|---|---:|---:|---:|---:|
| experimento01 00 | [90, 66, 195, 190] | 106×125 | 6169 | 0 | 190 (+0) |
| experimento01 01 | [85, 66, 195, 190] | 111×125 | 6478 | 0 | 190 (+0) |
| experimento01 02 | [85, 66, 195, 190] | 111×125 | 6531 | 0 | 190 (+0) |
| experimento01 03 | [86, 72, 192, 190] | 107×119 | 6353 | 0 | 190 (+0) |
| experimento01 04 | [86, 71, 182, 190] | 97×120 | 6142 | 0 | 190 (+0) |
| experimento01 05 | [86, 66, 167, 190] | 82×125 | 6237 | 0 | 190 (+0) |
| experimento01 06 | [88, 72, 170, 190] | 83×119 | 5959 | 0 | 190 (+0) |
| experimento01 07 | [88, 73, 188, 190] | 101×118 | 5739 | 0 | 190 (+0) |
| experimento01 08 | [88, 74, 185, 190] | 98×117 | 5952 | 0 | 190 (+0) |
| experimento01 09 | [89, 78, 167, 190] | 79×113 | 5438 | 0 | 190 (+0) |
| experimento01 10 | [87, 76, 175, 190] | 89×115 | 5868 | 0 | 190 (+0) |
| experimento01 11 | [85, 73, 179, 190] | 95×118 | 6027 | 0 | 190 (+0) |
| experimento01 12 | [83, 73, 176, 190] | 94×118 | 6172 | 0 | 190 (+0) |
| experimento01 13 | [83, 73, 191, 190] | 109×118 | 6547 | 0 | 190 (+0) |
| producao_body 00 | [90, 72, 173, 190] | 84×119 | 5803 | 0 | 190 (+0) |
| producao_body 05 | [92, 73, 178, 190] | 87×118 | 5628 | 0 | 190 (+0) |
| producao_body 08 | [81, 78, 185, 190] | 105×113 | 5729 | 0 | 190 (+0) |
| producao_body 09 | [83, 76, 177, 190] | 95×115 | 6109 | 0 | 190 (+0) |
| producao_body 13 | [90, 72, 173, 190] | 84×119 | 5803 | 0 | 190 (+0) |

## Observações visuais por pose

Os rótulos abaixo são julgamentos conservadores provisórios, pois não há segmentação anatômica ou contagem semântica de arma. As imagens correspondentes estão em evidence.

| Pose | Rótulo provisório | Evidência e limite |
|---|---|---|
| Experimento 00 | CONTAMINATED_BODY | Lâmina e guarda visíveis junto à mão; a sobreposição impede provar mão íntegra após remoção. |
| Experimento 01 | CONTAMINATED_BODY | Lâmina e guarda visíveis junto à mão; a sobreposição impede provar mão íntegra após remoção. |
| Experimento 02 | CONTAMINATED_BODY | Lâmina e guarda visíveis junto à mão; a sobreposição impede provar mão íntegra após remoção. |
| Experimento 03 | CONTAMINATED_BODY | Lâmina e guarda visíveis junto à mão; a sobreposição impede provar mão íntegra após remoção. |
| Experimento 04 | CONTAMINATED_BODY | Braço erguido com extremidade ambígua e sem separação confiável de arma e mão. |
| Experimento 05 | CONTAMINATED_BODY | Braço erguido com extremidade ambígua e sem separação confiável de arma e mão. |
| Experimento 06 | CONTAMINATED_BODY | Braço erguido com extremidade ambígua e sem separação confiável de arma e mão. |
| Experimento 07 | CONTAMINATED_BODY | Braço erguido com extremidade ambígua e sem separação confiável de arma e mão. |
| Experimento 08 | CONTAMINATED_BODY | Resíduo de lâmina junto ao braço/mão; separação da pegada não demonstrada. |
| Experimento 09 | CONTAMINATED_BODY | Resíduo de lâmina junto ao braço/mão; separação da pegada não demonstrada. |
| Experimento 10 | CONTAMINATED_BODY | Resíduo de lâmina junto ao braço/mão; separação da pegada não demonstrada. |
| Experimento 11 | CONTAMINATED_BODY | Resíduo de lâmina junto ao braço/mão; separação da pegada não demonstrada. |
| Experimento 12 | CONTAMINATED_BODY | Resíduo de lâmina junto ao braço/mão; separação da pegada não demonstrada. |
| Experimento 13 | CONTAMINATED_BODY | Lâmina e guarda visíveis junto à mão; a sobreposição impede provar mão íntegra após remoção. |
| Produção 00 | CLEAN_BODY | Camada body isolada sem espada evidente na inspeção; integridade anatômica e ausência de resíduos finos não quantificadas. |
| Produção 05 | CLEAN_BODY | Camada body isolada sem espada evidente na inspeção; integridade anatômica e ausência de resíduos finos não quantificadas. |
| Produção 08 | CLEAN_BODY | Camada body isolada sem espada evidente na inspeção; integridade anatômica e ausência de resíduos finos não quantificadas. |
| Produção 09 | CLEAN_BODY | Camada body isolada sem espada evidente na inspeção; integridade anatômica e ausência de resíduos finos não quantificadas. |
| Produção 13 | CLEAN_BODY | Camada body isolada sem espada evidente na inspeção; integridade anatômica e ausência de resíduos finos não quantificadas. |

As classificações não substituem a medição por pose exigida: é necessária revisão adicional com marcação justificada de articulações visíveis, intervalos de incerteza e máscaras de regiões suspeitas para obter os números faltantes. Nenhum pixel foi apagado ou modificado nas fontes.
