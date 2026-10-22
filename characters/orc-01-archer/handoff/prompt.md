# Pedido de criacao — orc-01-archer

Etapa: animation. Trabalhar Idle, 4 quadros/vista; iniciar por front_r e revisar antes das demais vistas. Nao criar o pacote todo automaticamente.

Leia AGENTS.md e os documentos apontados em handoff.json. Abra e observe as imagens antes de gerar.

## Identidade e fontes

Raca: Orc; perfil documentado: Robusto; fantasia: Fúria.
Job: Archer; papel: Distância. Afinidades sao contexto, sem bloqueio racial.
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
  "id": "orc-01-archer",
  "identityId": "cd362b7a-e190-4e5b-aa7c-54970cfd8353",
  "name": "orc-01-archer",
  "status": "candidate",
  "createdAt": "2026-10-18T22:29:58.074Z",
  "styleId": "tactics-core-v1",
  "race": {
    "id": "orc",
    "name": "Orc",
    "bodyProfile": "Robusto"
  },
  "job": {
    "id": "archer",
    "name": "Archer"
  },
  "role": "Distância (Job Archer)",
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
    "id": "archer-candidate-v1",
    "description": "Fitted moss-green sleeveless leather jerkin, ochre narrow sash, a diagonal leather baldric with small flat utility pouch, compact brown leather trousers and boots, reinforced left forearm archery bracer and right fingerless hand wrap. No quiver, arrows, bow or ammunition. Agile marksman outfit with exposed robust biceps, no hood or cape.",
    "equipmentMode": "weapon-independent-base",
    "weapon": "Assets independentes; nao incluidos na roupa; overlay runtime pendente"
  },
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
    "purpose": "outfit-variant",
    "mustPreserve": [
      "identityId",
      "race",
      "appearance"
    ],
    "conceptApprovalAtCreation": false
  },
  "reuseAssessment": [
    {
      "component": "individual body/face and reference contract",
      "category": "REUSE_DIRECT",
      "evidence": "orc-01 concept/base/consistency approvals + exact reference hashes",
      "adaptation": "Preserve identityId, face, bald scalp, skin, dominant right hand and robust proportions; no new individual",
      "artRisk": "Image edits may drift identity; compare against approved Warrior",
      "technicalRisk": "Existing Warrior frames are flattened: hidden body beneath armor is unavailable",
      "dependencies": [
        "approved orc-01"
      ],
      "validation": "REFERENCE_APPROVED; VARIANT_PENDING_REVIEW"
    },
    {
      "component": "Idle Walk Hit Defeat timing, ground and pose references",
      "category": "REUSE_ADAPTED",
      "evidence": "orc-01 97 approved native PNGs and 20 verified editable animation clips",
      "adaptation": "Reuse pose/registration/timing reference; redraw changed clothes per frame. Reuse exact exposed-body pixels only after registered masks demonstrate compatibility",
      "artRisk": "Long robes/mantles alter silhouette and occlusion",
      "technicalRisk": "No layered naked-body source or automatic clothing rig exists",
      "dependencies": [
        "variant concept approval",
        "native base and views approval",
        "registered clothing/body layers"
      ],
      "validation": "PLANNED_NOT_DEMONSTRATED"
    },
    {
      "component": "job outfit",
      "category": "CREATE_NEW",
      "evidence": "references/tacticsrpg/Docs/GameDesign/JOB_CATALOG.md",
      "adaptation": "Fitted moss-green sleeveless leather jerkin, ochre narrow sash, a diagonal leather baldric with small flat utility pouch, compact brown leather trousers and boots, reinforced left forearm archery bracer and right fingerless hand wrap. No quiver, arrows, bow or ammunition. Agile marksman outfit with exposed robust biceps, no hood or cape.",
      "artRisk": "Candidate Job language needs creator approval",
      "technicalRisk": "Keep four independent views and original pixel registration",
      "dependencies": [
        "Gate 1"
      ],
      "validation": "CONCEPT_PENDING"
    },
    {
      "component": "Attack and job-specific actions",
      "category": "CREATE_NEW",
      "evidence": "Warrior has a right-hand body strike; JOB_CATALOG describes different Job roles",
      "adaptation": "Author role-specific body action; Warrior punch is not archery, healing or spellcasting",
      "artRisk": "Action must read correctly without embedded weapons",
      "technicalRisk": "Cast and synchronized shooting require playback/runtime extensions",
      "dependencies": [
        "native base approval",
        "action design"
      ],
      "validation": "NOT_RUN"
    },
    {
      "component": "Unity registration and separate weapons",
      "category": "REQUIRES_EXTENSION",
      "evidence": "docs/UNITY.md",
      "adaptation": "No changes to sibling game; future separate integration",
      "artRisk": "Validate weapon contact and occlusion in game later",
      "technicalRisk": "UnitVisuals registry/overlays not implemented",
      "dependencies": [
        "authorized integration",
        "PlayMode"
      ],
      "validation": "NOT_RUN"
    }
  ]
}
```
