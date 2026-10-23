# Pedido de criacao — orc-01-refinement-v2

Etapa: concept. Criar candidato de conceito 2D para aprovacao; nao produzir lote de sprites/animacoes finais nesta etapa.

Leia AGENTS.md e os documentos apontados em handoff.json. Abra e observe as imagens antes de gerar.

## Identidade e fontes

Raca: Orc; perfil documentado: Robusto; fantasia: Fúria.
Job: Warrior; papel: Dano físico. Afinidades sao contexto, sem bloqueio racial.
Ficha completa: character.json anexado. Campos TBD sao lacunas/propostas, nunca fatos aprovados.

- Proporcoes compactas taticas, maturidade, silhueta legivel no zoom do jogo.
- Clusters intencionais, materiais distintos, luz coerente com a ancora observada, detalhe controlado.
- Raca, individuo, Job, cultura, faccao, equipamento e forma sao eixos independentes.
- Sem espelhamento entre vistas; preservar mao dominante e assimetrias.
- Conceitos e sprites base do personagem ficam sem armas; armas sao assets separados, exibidos somente quando equipados e invocados por uma acao.
- Conceito e sprite nativo sao entregas diferentes. Reduzir conceito nao cria sprite pronto.
- Camadas 2D precisam de canvas, registro e timeline identicos; sobrepor imagens arbitrarias nao produz roupa compativel.
- Cores de pele, presas, cultura e ornamentacao racial ausentes nas fontes permanecem TBD/proposta.
- Gera-se conceito, depois base nativa, depois vistas, depois animacoes por lotes revisados.

Variante do MESMO individuo orc-01. Preservar rosto, anatomia, tracos e assimetrias; mudar roupa/equipamento do Job. Base aprovada agora: true. Se pendente, produzir somente proposta e declarar a pendencia.

Hero e referencia opcional de leitura e implementacao. Seu cabelo, armadura, arma e cores nao sao um uniforme do jogo.

## Geracao na conversa

Se image_gen estiver disponivel, usar a ferramenta de imagem com estas referencias e salvar o resultado no workspace. Verificar a skill de imagem da sessao. Sem ferramenta, entregar instrucoes e registrar NOT_RUN; nao simular criacao com texto/SVG ou recoloracao do Hero.
Nao acionar APIs pagas ou automatizar login em Google/ChatGPT. O pacote tambem pode ser usado manualmente em outra ferramenta disponivel ao criador.

## Entrega

Salvar candidatos PNG sem substituir refs aprovadas, registrar prompt/modelo quando conhecidos, mostrar preview e solicitar avaliacao artistica do lote. Nao autoaprovar. Conceito em resolucao alta permanece em concepts/. Sprite nativo precisa de producao propria e entra em sprites/ somente via importacao validada.

## Ficha resolvida

```json
{
  "schemaVersion": 1,
  "id": "orc-01-refinement-v2",
  "identityId": "cd362b7a-e190-4e5b-aa7c-54970cfd8353",
  "name": "Orc Warrior — estudo de refinamento v2",
  "status": "candidate",
  "createdAt": "2026-10-22T05:40:54.842Z",
  "styleId": "tactics-core-v1",
  "race": {
    "id": "orc",
    "name": "Orc",
    "bodyProfile": "Robusto"
  },
  "job": {
    "id": "warrior",
    "name": "Warrior"
  },
  "role": "Dano físico (papel do Job Warrior)",
  "culture": "TBD",
  "faction": "TBD",
  "form": "base",
  "appearance": {
    "face": "Concept-07 escolhido e aprovado pelo criador em 2026-10-19: Orc adulto de feição bestial e brutal, testa pesada, focinho/nariz largo e achatado, maxilar anguloso, olhos ferozes e presas inferiores grandes e irregulares; expressão tensa, agressiva e battle-hardened, sem serenidade humana. Identidade deste indivíduo; não universalizar como cânone de todos os Orcs.",
    "hair": "Careca, couro cabeludo totalmente nu; preservar sobrancelhas escuras, conforme concept-07 escolhido pelo criador em 2026-10-19.",
    "ageImpression": "Adulto",
    "body": "Compacto, ombros largos e musculatura robusta, com proporção tática legível dentro do perfil de 1 tile; não copiar o corpo humanoide do piloto.",
    "palette": [
      "verde-oliva acinzentado",
      "ferro escuro",
      "couro castanho gasto",
      "vermelho queimado"
    ],
    "dominantHand": "right",
    "asymmetries": [
      "mão dominante direita, vazia no conceito base",
      "proteção de ombro assimétrica"
    ],
    "lighting": "Proposta de luz superior esquerda, com clusters e contraste alinhados à âncora; direção ainda candidata."
  },
  "outfit": {
    "id": "warrior-candidate",
    "description": "Proposta candidata: proteção de ferro escuro e couro, faixa curta vermelho queimado e um ombro reforçado. Conceito/base sem armas, escudo ou capa; ainda sem receita visual aprovada.",
    "equipmentMode": "weapon-independent-base",
    "weapon": "Possível machado de batalha de uma mão como asset independente, ainda não criado; aparece somente equipado e invocado por ação."
  },
  "styleRecipes": [],
  "profile": {
    "width": 128,
    "height": 128,
    "groundY": 126,
    "ppu": 100,
    "counts": {
      "Idle": 4,
      "Walk": 6,
      "Attack": 5,
      "Hit": 3,
      "Defeat": 5
    },
    "note": "Baseline do piloto humanoide 1 tile; anatomias diferentes exigem perfil e revisao. Walk atual usa 3 quadros/tile."
  },
  "references": [
    {
      "path": "references/tacticsrpg/Docs/Art/References/character_style_anchor_v1.png",
      "role": "global-style-anchor"
    },
    {
      "character": "orc-01",
      "role": "same-individual-body-and-face",
      "sourceDigest": "a9d373f7d295a04866bab2c6f23f7cb63ffc1e34a129ba69c3fe61b59a9b8a80"
    }
  ],
  "derivedFrom": {
    "character": "orc-01",
    "purpose": "same-outfit-artistic-refinement",
    "mustPreserve": [
      "identityId",
      "race",
      "appearance"
    ],
    "conceptApprovalAtCreation": true
  },
  "reuseAssessment": [
    {
      "component": "rendering/reference contract",
      "category": "REUSE_DIRECT",
      "evidence": "Docs/ART_DIRECTION.md + ancora",
      "adaptation": "Aplicar ao novo corpo; revisar em escala de jogo."
    },
    {
      "component": "race anatomy/face",
      "category": "REUSE_DIRECT",
      "evidence": "orc-01",
      "adaptation": "Preservar o indivíduo careca do concept-07.",
      "artRisk": "Variação de rosto/proporções pela geração.",
      "technicalRisk": "Nenhum runtime novo nesta proposta.",
      "dependencies": [],
      "validation": "PENDING_CREATOR",
      "productionImpact": "Nenhum asset aprovado substituído."
    },
    {
      "component": "job outfit",
      "category": "REUSE_ADAPTED",
      "evidence": "Conceito 07 aprovado + PNG front_r vigente.",
      "adaptation": "Polir clusters e separação de materiais; preservar a assimetria de equipamento.",
      "artRisk": "Conferir ferragens e espinhos entre poses.",
      "technicalRisk": "Reconstrução nativa e registro exigem revisão.",
      "dependencies": [],
      "validation": "PENDING_CREATOR",
      "productionImpact": "Candidatos locais; sem aplicação."
    },
    {
      "component": "Unity registration",
      "category": "REQUIRES_EXTENSION",
      "evidence": "UnitVisuals fixa WarriorPilot.",
      "adaptation": "Registro multi-personagem externo a esta fabrica.",
      "validation": "NOT_RUN"
    }
  ],
  "revisionIntent": {
    "status": "PENDING_CREATOR",
    "scope": "Mesmo indivíduo e equipamento; proposta de clusters, planos do rosto e materiais mais legíveis.",
    "approvedDesign": "characters/orc-01/concepts/orc-01-warrior-concept-07.png",
    "animationRelationship": "Os estudos de combate usam o design original aprovado, não dependem deste conceito candidato.",
    "risk": "Gerador pode variar proporções, rosto e ferragens. Comparar antes de aprovar; não estabelecer cânone racial."
  }
}
```
