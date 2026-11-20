# QA independente V7

Veredito: **ARTISTIC_ISSUES_FOUND — HIGH**. Status artístico: **ARTISTIC_REVISION_REQUIRED**. **PENDING_CREATOR**.

Freeze examinado: `fde1fe23f2d637589b6abef6b9b946b6c4370cc8ae5f3927525fb038397b2579`, manifesto `characters/orc-v1/source/combat-recovery-v7/candidate28manifest.json`. Revisão nova dos pixels V7; nenhum parecer V6 foi consultado ou reutilizado. O V6 foi lido apenas como pai para diferenças e preservação. Nenhuma aprovação artística é concedida por este QA.

## Critério central: a mesma técnica nas quatro direções

**Sword: FAIL. Axe: FAIL.** Há agora elevação real em back_l e uma ordem de fases reconhecível (preparar, elevar, descer, recuperar). Isso é progresso concreto. Entretanto, a semelhança das fases não basta para reconhecer a mesma técnica corporal. Nos frontais, ombro/antebraço atravessam o peito, o corpo acompanha e o contato termina cruzado. Em back_l, o conjunto se abre e trabalha persistentemente fora do lado direito da silhueta; falta a rotação/oclusão corporal que tornaria essa trajetória uma tradução convincente do gesto frontal. Não exijo igualdade de ângulos de tela entre perspectivas. O problema é a relação entre braço, torso e plano de ataque, visível mesmo parado.

back_r apresenta elevação e descida mais compactas junto à ombreira. back_l tem abertura fina, ápice exterior e braço comprido pendente no contato. Assim, a família traseira esquerda ainda lê como uma solução articulada própria, sobretudo no Axe. A reprodução contínua poderia acrescentar informação de peso e fluidez, mas não elimina o defeito de construção já observável nas poses.

## Matriz de objeções

| Objeção | Célula / quadro | Evidência e julgamento | Resultado |
|---|---|---|---|
| back_l/Sword ataca de lado | back_l/Sword; F03, F06, F07, F08, F09, F10 | Elevação corrigida em F06; porém abertura F03 com úmero fino/horizontal e descida/contato F08–F10 permanecem exteriores ao torso, sem o cruzamento corporal reconhecível dos frontais. Ver QA-V7-01/02. | **FAIL** |
| back_l/Axe antinatural | back_l/Axe; F03, F06, F07, F08, F09, F10 | Hoist e massa da cabeça existem; úmero estreito em F03 e recuperação da espessura/curvatura em F06–F09 fazem o braço ler como segmentos articulados. Contato desce no lado externo, sem transferência equivalente ao frontal. | **FAIL** |
| Flash branco no Sword traseiro | back_r/Sword; back_l/Sword (Axe como controle); F00, F01, F10, F11, F13, F14 | PASS para a descontinuidade específica dos bookends: luma e contagens reproduzidas em preservation-luma.json. Flicker contínuo NÃO VERIFICADO. | **PASS** |
| Pegada underhand | back_r/Axe; F03, F04, F07 | Inspeção estática composta e body-only: mão fecha ao redor do cabo; punho chega abaixo da palma no hoist, acima/esquerda no contato. Não confirmada a leitura underhand anterior; rotação temporal NÃO VERIFICADA. | **PASS** |
| Axila ainda não resolvida | front_l/Sword; F03, F04 | 9 e 10 pixels de diferença RGBA contra o pai; abertura escura legível, sem a ilha solta ou chapa uniforme denunciadas. Região composta x147..152/y115..123. PASS estático localizado. | **PASS** |
| Contornos claros frontais | front_l/Sword; front_l/Axe; front_r/Sword; front_r/Axe; todos | Não identificado halo claro destacado nas imagens atuais. Highlights acompanham metal/luva; anterioridade no V5 é controle de regressão, não prova artística. Flicker NÃO VERIFICADO. | **PASS** |
| Preservar front_r/Sword | front_r/Sword; 00..12 | 13/13 compostos RGBA idênticos ao pai; duração preservada. | **PASS** |

## Achados novos desta revisão

### QA-V7-01 — HIGH

Correspondência de técnica insuficiente: frontais passam a mão/antebraço pelo plano do peito e terminam cruzados; back_l levanta e abaixa o conjunto fora do lado direito da silhueta, sem rotação/oclusão de torso que explique o mesmo corte em perspectiva. A elevação correta isoladamente não resolve o critério central.

Células: back_l/Sword, back_l/Axe; quadros: F03, F06, F07, F08, F09, F10. Coordenadas: `{"space":"native 128; somar 64,64 no composto","Sword":{"openingShoulder":[88,40],"openingElbow":[106,39],"apexPalm":[100,19],"contactPalm":[109,81]},"Axe":{"openingShoulder":[89,39],"openingElbow":[104,34],"apexPalm":[95,15],"contactPalm":[101,76]}}`.

Comparar Sword-keys.png e Axe-keys.png por fase; observação estática independente, sem inferir avaliação temporal.

### QA-V7-02 — MEDIUM

O úmero na abertura F03 sai da ombreira como faixa estreita quase horizontal; no ápice/contato vira membro espesso e curvo. A cadeia está conectada mas o volume e a união manga/ombreira não mantêm leitura anatômica convincente. Mais evidente no body-only; não é membro ausente.

Células: back_l/Sword, back_l/Axe; quadros: F03, F04, F06, F09. Coordenadas: `{"space":"native 128","roi":[86,30,116,58]}`.

Sword-body.png e Axe-body.png, última linha; comparar espessura proximal F03 com F06/F09.

Os centros de junta acima são marcos declarados no clipe, conferidos visualmente como localização aproximada; não são uma medição automática independente da anatomia. As conclusões de volume e técnica são juízos visuais, não consequência de comprimentos ou contagem de componentes. Prioridade de reparo: aprovar poses body-only de abertura/ápice/contato em comparação frontal antes de refazer intermediários ou recolocar equipamento.

## Verificações independentes

- SHA-256 exato do freeze confirmado; 28/28 hashes de clip.json conferem. Matriz real 13 ativos / 15 aliases / 232 quadros coerente com o prompt.
- 15 aliases mantêm hash do clipe do pai e hashes declarados dos PNGs; comparação direta adicional dos 20 clipes sem Sword/Axe confirmou todos os quadros byte-idênticos e todos os tempos iguais ao V6. Isto exclui regressão introduzida nesses exports; não os aprova artisticamente.
- front_r/Sword: 13/13 compostos RGBA sem diferença. front_r/Axe e front_l/Axe: 12/12 sem diferença. front_l/Sword: somente F03 (9 pixels) e F04 (10 pixels), coerentes com as 19 correções declaradas. Região da axila composta x147..152/y115..123; não confundir com coordenadas nativas.
- back_l/Sword F06: topo real da máscara da arma y25 composto; primeiro pixel verde do crânio y74, diferença **49 px**. A alegação exata de 48 não foi reproduzida com esse marco; discrepância de 1 px não muda a elevação inequívoca. Punho nativo y25 contra ombro y39: **14 px acima**. Não usei isso para aprovar técnica ou anatomia.
- Nas 8 células de equipamento, varredura alfa de weaponBack/weaponFront: **0 pixels abaixo de groundY190**; **0 pixels de arma em todos os quadros declarados desarmados**. Extremos nas tiras atuais parecem desarmados também semanticamente. Não se deduziu ausência semântica no corpo pela transparência dessas camadas.

### Flash: medições novas, sem substituir observação temporal

Luma BT.601 em pixels corporais opacos, limiar 145. back_r/Sword F00/F01 têm 7/7 claros; F10/F11, 5/5. Médias do corpo 37,401→37,822 (delta +0,420) e 37,158→37,534 (+0,376), dentro dos demais deltas internos (até 1,002 em módulo). back_r/Axe: 7/9 e 5/5 claros; deltas de média +0,114 e −0,223, contra máximo interno 1,662. Assim não reproduzo o salto específico dos bookends.

back_l/Sword F00/F01: 14/14; F13/F14: 14/14; médias delta +0,029 e 0. back_l/Axe: 23/23 nas duas extremidades, deltas −0,075 e 0. A comparação F10→F11 é a saída do clipe de 12 quadros back_r; nos novos back_l de 15 quadros ela é recuperação interna, não bookend. Todos os valores, inclusive a ROI adicional de ombro composto x99..124/y89..116, estão em preservation-luma.json e measurements.json. A ROI complementar usa opacidade variável e é diagnóstico, não teste perceptivo universal.

## Evidência visual e limites

Tiras integrais atuais: [Sword](Sword-all.png), [Axe](Axe-all.png). Cada linha é front_r, front_l, back_r, back_l; colunas F00 em diante. Quadros-chave ampliados: [Sword](Sword-keys.png), [Axe](Axe-keys.png); versões [Sword body-only](Sword-body.png), [Axe body-only](Axe-body.png). As ampliações são apenas previews nearest-neighbour de PNGs existentes; não alteram arte.

Nas chaves, linhas na mesma ordem. Sword frontal: F03/05/06/07/08; back_r: F02/03/04/06/07; back_l: F03/06/07/09/10. Axe frontal: F03/04/05/06/07; back_r: F02/04/05/06/07; back_l: F03/06/07/09/10. Conferidos também o recorte existente de pegada back_r/Axe F04 e o painel existente das 13 axilas front_l/Sword. São apoio às imagens atuais, não substituição do freeze.

**Reprodução 1×, 0,5× e contínua em escala tática: NÃO VERIFICADO.** A tentativa de criar aba iab retornou indisponibilidade; a lista de navegadores disponíveis veio vazia. Não atribuo a mim a reprodução registrada pelos checks anteriores. Fluidez, flicker residual e mudança da pega durante movimento seguem para o revisor temporal separado.

Os recibos existentes de validação técnica e reexports Aseprite são coerentes com a identidade do pacote; não reabri mestres nem repeti 994 verificações. Isso não prejudica os achados visuais nos PNGs deste freeze. Não foi feita nova inspeção estética completa dos 20 clipes não alvo; a preservação deles foi verificada diretamente. Nenhuma arte, fonte, manifesto, documentação ou Unity foi alterada. Sem subagentes, sem PixelLab; custo LLM não informado.

Resultado destinado à correção local e nova submissão, mantendo PENDING_CREATOR. As correções de flash, elevação, axila e preservação não compensam o FAIL do critério central.
