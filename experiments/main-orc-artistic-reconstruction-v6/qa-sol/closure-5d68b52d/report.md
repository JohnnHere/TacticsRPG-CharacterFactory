# Re-revisão independente de fechamento — V6 corrigida

**Os dois achados anteriores estão CLOSED/PASS na inspeção estática. Veredito global: INCONCLUSIVE. Estado: VISUAL_REVIEW_REQUIRED, PENDING_CREATOR.** Não há defeito artístico estático aberto confirmado nesta re-revisão; falta a avaliação temporal independente já explicitada no parecer anterior. Não emitir READY_FOR_CREATOR_REVIEW como se essa etapa tivesse ocorrido.

Manifesto conferido em disco: `characters/orc-v1/source/artistic-reconstruction-v6/candidate28manifest.json`, SHA-256 **5d68b52d3e2b2a0931d689afb5a9dd438c178835d05efb02a5fb2bcf0c64b7ca**. Matriz: 28 células, 13 ativas, 226 quadros. Data: 30/10/2026. Revisor: mesma sessão Codex do parecer anterior; identificador exato do modelo não exposto. O parecer favorável V5 não é evidência desta revisão.

## Fechamento dos achados

| Achado | Evidência visual nova e medição própria | Resultado |
|---|---|---|
| V6-QA-01 — front_l/Sword F03/F04, axila | Inspecionei os recortes novos F03/F04, os vizinhos F02/F05 e a sequência composta completa. A projeção preta inferior foi retirada; a sombra de contato permaneceu e o recorte sob o braço está legível. Não vi preenchimento chapado, textura repetida, buraco novo ou perda de contorno na área reparada. Comparação das folhas preservadas da revisão anterior contra as folhas montadas dos frames atuais: 30 pixels F03 e 28 pixels F04, sem outras alterações nesse body/composto. | **CLOSED / PASS estático** |
| V6-QA-02 — back_l/Sword F07–F09, ponta abaixo do chão | Inspecionei a folha composta nova, incluindo a descida e recuperação. A espada sai em diagonal, suspensa ao lado da mão; não lê mais como fincada no piso nesses quadros. Medição própria nas camadas weaponBack/weaponFront: extremos y187/y185/y173, zero pixels abaixo de groundY190. Pegadas declaradas continuam [158,153]/[149,155]/[151,152]. O body permanece idêntico na comparação das folhas. Não vi afastamento grosseiro da arma da luva nos compostos. | **CLOSED / PASS estático**; naturalidade em movimento **NÃO VERIFICADA** |

Evidências desta rodada: `front_l-Sword-F3-axilla.png`, `front_l-Sword-F4-axilla.png`, `front_l-Sword-F2-axilla.png`, `front_l-Sword-F5-axilla.png`, `front_l-Sword-composite.png`, `back_l-Sword-composite.png`, `closure-checks.json` e `inspection-checks.json`.

## Escopo e regressões

Montei novamente as 16 folhas body-only/composto a partir dos caminhos do manifesto atual. Comparei os pixels de todas essas folhas com as folhas que este QA preservou no freeze 2c2dd3b9. Só mudaram front_l/Sword F03/F04 e back_l/Sword composto F07–F09. Os outros seis ataques e o body de back_l/Sword têm folhas idênticas. Isto verifica a superfície visual exportada; não equivale a auditar todo arquivo mestre nem reexecutar a preservação global.

Os 20 clipes fora de Sword/Axe continuam nos mesmos caminhos V5 e seus hashes de clip coincidem com o manifesto. A validação técnica atual lida informa TECHNICAL_PASS, hash 5d68b52d, 226 quadros e 956 hashes; não repeti a suíte em massa. Nenhum sucesso técnico foi usado para inferir fluidez.

## Matriz de fechamento contra as objeções

| Critério original | Resultado desta rodada |
|---|---|
| 1. Sword back_l: anatomia, trajetória, recuperação, grip e ritmo | Recuperação espacial **PASS** estático; body sem alteração; temporal/grip durante movimento **NÃO VERIFICADO**. |
| 2. Axe back_l: uma mão, peso e tronco | Sem alteração visual frente ao freeze anterior; peso/rigidez/saltos **NÃO VERIFICADO**. Não é novo PASS artístico global. |
| 3. Sword/Axe back_r: pernas/apoio e continuidade | Sem alteração visual frente ao freeze anterior; continuidade durante playback **NÃO VERIFICADO**. |
| 4. Axila front_l/Sword | **PASS** estático, achado encerrado. |
| 5. Contornos claros e metal | Nenhuma regressão estática observada nas duas regiões reintegradas; demais exportações de ataque idênticas. |
| 6. Grip nas quatro vistas | Sem afastamento grosseiro observado na espada esquerda reparada; certificação integral permanece **NÃO VERIFICADO**, como antes. |
| 7. Attack-only/bookends | Bookends dos dois alvos visualmente preservados; fora dos quadros-alvo, folhas idênticas. **PASS** para preservação estática do escopo. |
| 8. Identidade V1/itens independentes/vistas próprias | Nenhuma mudança estrutural observada no escopo reparado. **PASS** estático limitado. |
| 9. Preservação frontal | Apenas 30/28 pixels em F03/F04 do alvo; demais folhas frontais idênticas. **PASS** na superfície visual comparada. |

## Limitação de fechamento

Nesta rodada, `cua.listBrowsers()` retornou **[]**. O player real não ficou disponível por esse caminho; não assisti aos oito ataques em 1×, 0,5× ou escala tática. A inspeção das folhas não resolve peso, ritmo, popping, estabilidade cinemática ou a transição F09→F10 após a arma desaparecer. Critérios temporais permanecem NÃO VERIFICADO, e por isso o fechamento global é INCONCLUSIVE, não ARTISTIC_ISSUES_FOUND nem READY_FOR_CREATOR_REVIEW. É necessária uma revisão temporal independente do hash atual em ambiente que reproduza o player.

Foram mantidos os arquivos históricos do primeiro QA. Esta rodada só escreveu evidências/relatórios sob qa-sol; não editou arte, manifesto, fontes, docs ou Unity, não criou subagentes e não chamou PixelLab. Custo LLM não informado. Aprovação artística permanece exclusiva do criador.
