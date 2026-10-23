# Direção vigente do laboratório — 2026-10-23

Leia docs/ORC_ART_LAB.md antes dos snapshots antigos. Cinco direções do mesmo Orc aprovado; escolha pendente. Paleta, materiais, luz e textura delegados ao agente. Referência individual real: characters/orc-01-aseprite-v4/source/aseprite/retouched/concept/concept_front_r_00.png. Toda nova autoria no Aseprite.

# Pedido de criacao — orc-01-art-lab-v5

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
  "id": "orc-01-art-lab-v5",
  "identityId": "cd362b7a-e190-4e5b-aa7c-54970cfd8353",
  "name": "Orc Warrior — laboratório visual / cinco direções",
  "status": "candidate",
  "createdAt": "2026-10-23T03:13:45.902Z",
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
  "form": "visual-study",
  "appearance": {
    "face": "Concept-07 escolhido e aprovado pelo criador em 2026-10-19: Orc adulto de feição bestial e brutal, testa pesada, focinho/nariz largo e achatado, maxilar anguloso, olhos ferozes e presas inferiores grandes e irregulares; expressão tensa, agressiva e battle-hardened, sem serenidade humana. Identidade deste indivíduo; não universalizar como cânone de todos os Orcs.",
    "hair": "Careca, couro cabeludo totalmente nu; preservar sobrancelhas escuras, conforme concept-07 escolhido pelo criador em 2026-10-19.",
    "ageImpression": "Adulto",
    "body": "Compacto, ombros largos e musculatura robusta, com proporção tática legível dentro do perfil de 1 tile; não copiar o corpo humanoide do piloto.",
    "palette": [
      "Cinco paletas candidatas; ver source/art-lab-render.json"
    ],
    "dominantHand": "right",
    "asymmetries": [
      "mão dominante direita, vazia no conceito base",
      "proteção de ombro assimétrica"
    ],
    "lighting": "Luz superior esquerda herdada; novas placas com planos, bordas e volume candidatos."
  },
  "outfit": {
    "id": "warrior-five-directions-candidate",
    "description": "Cinco estudos do mesmo Orc: ferro de clã, veterano de fronteira, basalto, bronze/ocre e ferro de campanha. Escolha pendente do criador.",
    "equipmentMode": "weapon-independent-base",
    "weapon": "Nenhuma arma desenhada, carregada ou embainhada."
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
      "path": "characters/orc-01-aseprite-v4/source/aseprite/retouched/concept/concept_front_r_00.png",
      "role": "approved-individual-anatomy-and-pose"
    },
    {
      "path": "docs/ORC_ART_LAB.md",
      "role": "latest-creator-direction"
    }
  ],
  "derivedFrom": null,
  "reuseAssessment": [
    {
      "component": "Face, anatomy, pose and inherited drawing",
      "category": "REUSE_DIRECT",
      "evidence": "characters/orc-01-aseprite-v4/source/aseprite/retouched/concept/concept_front_r_00.png",
      "adaptation": "Retain the approved bald Orc identity and anatomical structure.",
      "artRisk": "Inherited design language persists; originality is not established by editor choice.",
      "technicalRisk": "1254px concept is not a native runtime sprite.",
      "dependencies": [
        "V4 approved concept"
      ],
      "validation": "Visual comparison; hidden reference verified separately.",
      "productionImpact": "No production substitution."
    },
    {
      "component": "Material treatment and palette",
      "category": "REUSE_ADAPTED",
      "evidence": "tools/aseprite/orc-art-lab-v5.lua",
      "adaptation": "Five material ramps applied within Aseprite, inherited lighting and texture retained.",
      "artRisk": "Small-scale material separation still needs creator review.",
      "technicalRisk": "No palette or anatomy universalization.",
      "dependencies": [
        "Aseprite saved masters"
      ],
      "validation": "Exact saved-master export.",
      "productionImpact": "Candidate concepts only."
    },
    {
      "component": "Shoulder armour, reinforcement, motifs and accents",
      "category": "CREATE_NEW",
      "evidence": "Five independent armour-construction layers in saved masters.",
      "adaptation": "Original shapes, overlaps, rivets, repair panels and limited face accents.",
      "artRisk": "New armour and inherited body require further artistic refinement after choice.",
      "technicalRisk": "Native sprites and four views need their own production.",
      "dependencies": [
        "Creator selects and approves refined concept"
      ],
      "validation": "TECHNICAL_PASS_ART_REVIEW_PENDING",
      "productionImpact": "Do not propagate unapproved candidates."
    }
  ],
  "artExploration": {
    "date": "2026-10-23",
    "studyOf": "orc-01",
    "baseline": "aseprite-v4",
    "goal": "Orc clássico medieval; principalmente Warcraft e também Tolkien; identidade própria e um jogo com alma.",
    "creatorDelegates": [
      "palette",
      "lighting",
      "materials",
      "texture"
    ],
    "candidateSelection": null,
    "approval": "PENDING_CREATOR",
    "sameIndividual": true,
    "conceptsOnly": true
  }
}
```
