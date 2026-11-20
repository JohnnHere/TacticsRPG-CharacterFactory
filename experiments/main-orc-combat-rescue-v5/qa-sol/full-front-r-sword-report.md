# QA independente — front_r/Sword completo, 13f/730ms

**INCONCLUSIVE para validação artística temporal · VISUAL_REVIEW_REQUIRED · PENDING_CREATOR.** Os13 quadros foram examinados, incluindo as seis pegadas novas. Não foi identificado defeito estático bloqueante de contato/oclusão, mas esta interface não permite afirmar percepção visual contínua1×. Não se transforma o bom resultado estático ou o relógio do player em aprovação do ciclo. Global permanece **ARTISTIC_REVISION_REQUIRED**.

## Freeze e reprodução efetivamente verificada

A revisão só começou após o checkpoint **GRIP_FRONT_R_SWORD_FULL_READY**. Clip `characters/orc-v1/source/combat-rescue-v5/grip-specialist/full-front-r-sword/clip.json`: SHA-256 **`16fe8b7b30cbaa029ac4f4bd2bda5f7c8ac127007ec40a49a1f41db2580c63a1`**. Mestre composto: `3ee5755c874ccc007aa7f67af9ea5cc839d2cf98b5c0bee25dbcf0bf9acf6410`.

Foram abertas a sequência final e a sequência layers-off de todos os corpos; a localização das luvas foi conferida contra o corpo, sem tratar o centro declarado como prova. No player original `index.html`, Microsoft Edge Chromium headless percorreu F00..F12 em1× e0,5×: aproximadamente733ms e1466ms de parede, parando no F12 desarmado. Foram inspecionadas capturas próprias em F03/F04/F05/F07/F09/F10, com corpo aproximadamente128px, detalhe da pegada8× e captura tática F07 com corpo aproximadamente64px.

Essas capturas são imagens discretas. A execução contínua ocorreu no navegador e foi registrada funcionalmente; **não foi percebida visualmente de forma contínua pelo revisor**. Naturalidade do arco, peso, ritmo e possíveis saltos de oclusão em velocidade normal permanecem pendentes. Isso não é defeito comprovado da animação.

## Contato e anatomia por pose

| Quadros | Observação visual |
|---|---|
|F00/F01|Sem arma; corpo e mãos preservados. Entrada começa com preparação corporal.|
|F02|Pegada baixa na mão direita anatômica à esquerda da imagem, luva cobrindo cabo; leitura estática anterior mantida.|
|F03|Luva frontalizada à esquerda, em continuidade com braçadeira/antebraço. Guarda acima e pomo abaixo acompanham a luva; sem contato baseado apenas na ombreira.|
|F04|Luva recurvada junto à ombreira, alcançada pelo antebraço vindo de baixo/esquerda; cabo atravessa a região fechada de couro, guarda acima e pomo abaixo.|
|F05|Punho alto acima do pulso e antebraço; luva cobre a seção central do cabo sob a guarda. Não se observa luva solta.|
|F06|Braço ativo cruza o tórax para a mão direita projetada à direita; a mão baixa junto ao quadril é inativa. O representante estático isolado não é usado para aprovar a passagem temporal.|
|F07|Mão ativa além do cuff do antebraço cruzado, cabo sob a luva e lâmina para a direita. Pomo projeta-se sobre a região metálica do cuff, mas a linha do cabo continua atravessando a mão; não há gap estático evidente.|
|F08|Luva ativa baixa à direita, abaixo do antebraço cruzado; o couro do braço sobreposto acima não é confundido com a palma. Oclusão estática permanece coerente com F08 já avaliado.|
|F09|Mão ativa recua para o centro, sob o cuff; a outra mão à direita permanece inativa. Cabo acompanha a luva baixa em vez de ser preso na outra mão.|
|F10|Manopla escura sob a braçadeira pendente, à esquerda do tasset vermelho; o tecido não é usado como palma. Pomo à esquerda e guarda à direita passam pela região da manopla. Contraste baixo exige atenção no movimento.|
|F11/F12|Equipamento e handFront ausentes; retorno sem arma persistente, conforme attack-only.|

O fechamento e a oclusão são visualmente plausíveis nas poses examinadas; não se observa cabo separado da luva ou centro preso exclusivamente ao antebraço. Nenhum novo defeito estático acionável foi confirmado. F07/F08 têm projeção de pomo sobre o cuff; F09/F10 têm luvas escuras e sobreposição densa. Esses são pontos de atenção para o playback perceptual, não achados transformados em reprovação sem evidência.

Na sequência de poses, a lâmina sobe pela esquerda, passa à direita e desce durante o golpe; na recuperação muda para uma orientação mais horizontal, acima do chão. Não se observa penetração estática da ponta no solo ou arma cortada no composto256. A aceleração F05→F06, a passagem F06→F08, a reversão F08→F10 e o desaparecimento F10→F11 precisam ser vistos continuamente em1× antes de julgar arco, pulso e entrada/saída naturais. Não há exigência de saque/embainhamento: o contrato vigente admite arma somente no intervalo de ataque.

## Preservação verificada

Comparação independente: **13/13 camadas corporais com zero diferenças ARGB** contra os corpos imediatos de origem;13/13 crops128 conferem com as camadas256. Cabeçalhos dos quatro mestres preservam `[30,65,35,50,45,65,35,35,100,55,80,45,90]ms`, total730ms, iguais ao pai. Todos os hashes declarados conferem no escopo. Camadas weaponBack/weaponFront/handFront têm zero pixels não transparentes nos quatro quadros ocultos0/1/11/12. Os pixels claros presentes no corpo frontal não foram classificados automaticamente como halos: corpo byte/visualmente preservado e materiais/rosto podem conter highlights legítimos.

112 arquivos deste escopo e entradas corporais imediatas estão em `full-cycles-input-freeze.json`; detalhes de pixels e Chromium em `full-cycles-pixel-checks.json` e `full-front-r-sword-browser-check.json`. Não foi repetida a auditoria dos107 registros históricos de pegadas, nem reavaliado o antigo laudo de F06. Não se reexportaram mestres Aseprite ou reproduziu independentemente a matemática de transformação do item; esses limites não foram ocultados por checks verdes.

## Parada

**TECHNICALLY_COMPLETE** nos aspectos conferidos; **VISUAL_REVIEW_REQUIRED** para o ciclo artístico. Não se solicita alterar corpos/tempos protegidos nem regenerar arte por esta limitação. Falta a observação perceptual contínua do freeze exato em escala de jogo e velocidade normal, especialmente nos trechos destacados. Não há liberação automática de outros grips, matriz, aprovação do criador ou Unity. Todas as escritas foram em `qa-sol`; Root decide o próximo marco.
