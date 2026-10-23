# Pedido de criacao — orc-01-aseprite-v3

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

Variante do MESMO individuo orc-01-refinement-v2. Preservar rosto, anatomia, tracos e assimetrias; preservar tambem a roupa aprovada nesta reautoria/refinamento. Base aprovada agora: true. Se pendente, produzir somente proposta e declarar a pendencia.

Hero e referencia opcional de leitura e implementacao. Seu cabelo, armadura, arma e cores nao sao um uniforme do jogo.

## Autoria obrigatoria no Aseprite

Decisao expressa do criador em 2026-10-22: TODA a producao de arte deve acontecer no Aseprite, incluindo conceitos, sprites, poses, animacoes e acabamento. A fonte .aseprite salva e o arquivo mestre; PNGs/folhas sao derivados. Autoria por scripts Lua executados no Aseprite e permitida, com codigo, procedencia e referencias registrados; declarar que e autoria programatica do agente, nao desenho manual nem geracao inteligente do editor.
Nao usar image_gen ou outra geracao externa para produzir arte nova sem nova instrucao explicita do criador. Nao desenhar/reconstruir/recolorir pixels fora do Aseprite. Ferramentas externas podem organizar metadados, comparar hashes/pixels e montar previews sem alterar a arte. Legados aprovados preservam sua procedencia original.
Usar processos batch ocultos enquanto o criador usa a maquina; nao disputar a GUI. Sem Aseprite disponivel, registrar NOT_RUN e o bloqueio real; nao substituir a ferramenta. Preservar gates e copiar referencias sem promover historicos rejeitados.

## Entrega

Salvar candidatos PNG sem substituir refs aprovadas, registrar prompt/modelo quando conhecidos, mostrar preview e solicitar avaliacao artistica do lote. Nao autoaprovar. Conceito em resolucao alta permanece em concepts/. Sprite nativo precisa de producao propria e entra em sprites/ somente via importacao validada.

## Ficha resolvida

```json
{
  "schemaVersion": 1,
  "id": "orc-01-aseprite-v3",
  "identityId": "cd362b7a-e190-4e5b-aa7c-54970cfd8353",
  "name": "Orc Warrior — autoria nativa Aseprite v3",
  "status": "candidate",
  "createdAt": "2026-10-22T06:05:46.260Z",
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
      "character": "orc-01-refinement-v2",
      "role": "same-individual-body-and-face",
      "sourceDigest": "a68160e2c23bbdf6b828c138b0bc42d931c1cd17b06a9ee7140681451b88583f"
    }
  ],
  "derivedFrom": {
    "character": "orc-01-refinement-v2",
    "purpose": "same-approved-design-reauthored-in-Aseprite",
    "mustPreserve": [
      "identityId",
      "race",
      "appearance"
    ],
    "conceptApprovalAtCreation": true
  },
  "reuseAssessment": [
    {
      "component": "Individual identity and approved outfit",
      "category": "REUSE_DIRECT",
      "evidence": "Approved V2 concept and creator statement in conversation 2026-10-22.",
      "adaptation": "Visual reference only; no raster imported.",
      "artRisk": "New explicit drawings may deviate in face and proportions.",
      "technicalRisk": "No live approved slot modified.",
      "dependencies": [
        "V2 approved reference"
      ],
      "validation": "PENDING_CREATOR",
      "productionImpact": "New isolated study."
    },
    {
      "component": "Native pixel artwork and poses",
      "category": "CREATE_NEW",
      "evidence": "characters/orc-01-aseprite-v3/source/aseprite/author-orc-v3.lua",
      "adaptation": "Native 128px original drawings, material shading and action silhouettes in Aseprite.",
      "artRisk": "Simpler shading and anatomy than V2; quality is not guaranteed by editor choice.",
      "technicalRisk": "Check compositing, bounds, palette, exact export and cels.",
      "dependencies": [
        "Aseprite Lua runtime"
      ],
      "validation": "TECHNICAL_PASS_ART_REVIEW_PENDING",
      "productionImpact": "Concept1 + Attack5 + Hit3 regional layered frames."
    },
    {
      "component": "Timing and review exporter",
      "category": "REUSE_DIRECT",
      "evidence": "V2 durations and src/aseprite.mjs.",
      "adaptation": "Same counts and total action time for equal comparison.",
      "artRisk": "Timing alone cannot establish better motion.",
      "technicalRisk": "Variable timings are not proven in Unity.",
      "dependencies": [],
      "validation": "EDITOR_EXPORT_PASS",
      "productionImpact": "Review only."
    },
    {
      "component": "Equipment rig / runtime",
      "category": "REQUIRES_EXTENSION",
      "evidence": "Regional layers do not form a complete body/clothing rig; UnitVisuals still WarriorPilot.",
      "adaptation": "Requires independent bodies, equipment sockets, occlusion and runtime integration.",
      "artRisk": "Hidden anatomy is not finished.",
      "technicalRisk": "No runtime implemented.",
      "dependencies": [
        "Artist review",
        "Unity extension task"
      ],
      "validation": "NOT_RUN",
      "productionImpact": "No Unity writes."
    }
  ],
  "authoringPolicy": {
    "master": "Aseprite",
    "method": "Agent-authored explicit pixel drawings executed by Aseprite Lua",
    "noImageGeneration": true,
    "externalRasterInputs": 0,
    "approval": "PENDING_CREATOR"
  }
}
```
