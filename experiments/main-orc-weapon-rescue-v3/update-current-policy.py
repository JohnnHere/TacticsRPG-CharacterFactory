"""Current policy/continuity only. Preserve unrelated documentation and historical evidence."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[2]
notice='''## Política vigente — Orc principal e armas somente no ataque, 2026-10-25

O Orc principal atual é **orc-v1 / Verde Warcraft**, em characters/orc-v1/. O antigo Orc V4 está descartado e nunca é fonte de restauração ou direção atual. A identidade atual é a referência; poses de ataque defeituosas podem ser substituídas.

Espada/machado ficam **ocultos no Idle, Walk, repouso, inspeção, Hit/Defeat e após a ação**. Aparecem somente no intervalo declarado do Attack. Os pedidos anteriores de Idle/Walk armados e o corte único compartilhado entre Sword/Axe estão **SUPERADOS**. São dois perfis: corte de espada e golpe de machado, reutilizáveis entre itens compatíveis da própria categoria. Sem sacar/embainhar, rig universal ou animação corporal por item.

Guia atual: docs/MAIN_ORC_ONE_HANDED_RESCUE.md; autoridade de identidade: reports/orc-production-current.json. Armas seguem a linguagem visual do jogo, sem obrigação de copiar a paleta/cultura Orc. Aseprite continua mestre; PixelLab autorizado auxilia poses; toda edição/exportação artística é no Aseprite. Esta tarefa não modifica Unity nem concede aprovação artística. **Nos registros anteriores abaixo, toda afirmação conflitante de V4 ativa, nenhuma seleção, arma em Idle/Walk ou movimento universal é histórica e superada.**

'''
files=['AGENTS.md','handoff/AGENT_CONTEXT.md','docs/VISUAL_IDENTITY.md','docs/WORKFLOW.md','docs/EQUIPMENT_AND_ACTIONS.md','docs/ASEPRITE.md','docs/PIXELLAB_ASEPRITE.md']
for path in files:
 p=R/path;s=p.read_text(encoding='utf-8');
 if not s.startswith('## Política vigente — Orc principal e armas somente no ataque'):s=notice+s
 s=s.replace('## Produção Orc ativa — Aseprite V4','## Histórico SUPERADO — produção antiga Aseprite V4')
 s=s.replace('Producao Orc vigente: [Aseprite V4 aplicada]','Produção HISTÓRICA SUPERADA: [Aseprite V4 aplicada]')
 s=s.replace('Adendo vigente de arte Orc: [Aseprite V4 aplicada]','Adendo HISTÓRICO SUPERADO de arte Orc: [Aseprite V4 aplicada]')
 p.write_text(s,encoding='utf-8')
for path in ['docs/ORC_V1_WEAPONS.md','docs/ORC_V1_WEAPONS_V2.md']:
 p=R/path;s=p.read_text(encoding='utf-8');prefix='> **HISTÓRICO REJEITADO / SUPERADO.** Ataques artisticamente rejeitados pelo criador. Idle/Walk armados e movimento comum Sword/Axe não são política atual. Consulte [resgate do Orc principal](MAIN_ORC_ONE_HANDED_RESCUE.md). Preservado como procedência e comparação, nunca como receita de produção.\n\n'
 if not s.startswith('> **HISTÓRICO REJEITADO'):p.write_text(prefix+s,encoding='utf-8')
p=R/'config/equipment-actions-v1.json';q=json.loads(p.read_text(encoding='utf-8'));w=q['weaponBinding'];old=w.pop('armedWalkAuthorization',None)
if old:w['supersededArmedWalkAuthorization']={**old,'status':'SUPERSEDED_BY_ATTACK_ONLY_V1'}
q['oneHandedPresentation']={'id':'attack-only-v1','authority':'Creator latest explicit rescue task, 2026-10-25','scope':'Current one-handed melee sword and axe','hiddenStates':['Idle','Walk','Rest','Inspection','Hit','Defeat','AfterAttack'],'visibleState':'Attack','visibleInterval':'Per-profile frame interval only','armedIdleWalkAllowed':False,'drawingSheathingRequired':False,'runtimeImplemented':False}
p.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=R/'characters/orc-v1/character.json';q=json.loads(p.read_text(encoding='utf-8'));q['appearance']['body']='Orc principal de pele Verde Warcraft, alto e imponente; mesma identidade e armadura do indivíduo selecionado, com poses de combate revisáveis.';q['weaponPresentation']={'policy':'attack-only-v1','dominantHand':'right','oneHanded':True,'armedIdle':False,'armedWalk':False,'bodySourcesWeaponIndependent':True,'visibility':'Only declared Attack interval; hidden in all resting states and after action.'};p.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Current policy recorded; old armed presentation explicitly superseded. Asset selection changes only after candidates are exported.')
