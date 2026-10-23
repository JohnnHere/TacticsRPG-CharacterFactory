"""Package review candidates only; never apply them to approved sprite slots."""
import hashlib
import importlib.util
import json
import struct
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8'))
def save(p, value):
    f = ROOT / p
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
def sha(p): return hashlib.sha256((ROOT / p).read_bytes()).hexdigest()

original = read('characters/orc-01/character.json')
candidate = read('characters/orc-01-refinement-v2/character.json')
candidate.update(name='Orc Warrior — estudo de refinamento v2', role=original['role'], outfit=original['outfit'])
candidate['derivedFrom']['purpose'] = 'same-outfit-artistic-refinement'
candidate['revisionIntent'] = {
    'status': 'PENDING_CREATOR',
    'scope': 'Mesmo indivíduo e equipamento; proposta de clusters, planos do rosto e materiais mais legíveis.',
    'approvedDesign': 'characters/orc-01/concepts/orc-01-warrior-concept-07.png',
    'animationRelationship': 'Os estudos de combate usam o design original aprovado, não dependem deste conceito candidato.',
    'risk': 'Gerador pode variar proporções, rosto e ferragens. Comparar antes de aprovar; não estabelecer cânone racial.'
}
for item in candidate['reuseAssessment']:
    if item['component'] == 'race anatomy/face':
        item.update(category='REUSE_DIRECT', adaptation='Preservar o indivíduo careca do concept-07.', artRisk='Variação de rosto/proporções pela geração.', technicalRisk='Nenhum runtime novo nesta proposta.', validation='PENDING_CREATOR', productionImpact='Nenhum asset aprovado substituído.')
    if item['component'] == 'job outfit':
        item.update(category='REUSE_ADAPTED', evidence='Conceito 07 aprovado + PNG front_r vigente.', adaptation='Polir clusters e separação de materiais; preservar a assimetria de equipamento.', artRisk='Conferir ferragens e espinhos entre poses.', technicalRisk='Reconstrução nativa e registro exigem revisão.', validation='PENDING_CREATOR', productionImpact='Candidatos locais; sem aplicação.')
save('characters/orc-01-refinement-v2/character.json', candidate)

spec = importlib.util.spec_from_file_location('editable', ROOT/'tools/write-animation-editable.py')
editable = importlib.util.module_from_spec(spec); spec.loader.exec_module(editable)
audit = read('reports/orc-assets-audit-v2.json')
generation = read('characters/orc-01-refinement-v2/source/generation-record.json')
base = 'characters/orc-01/source/aseprite/combat-refinement-v2'
jobs, clips = [], []
font = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 16)
for state, durations in [('Attack', [80,110,50,90,120]), ('Hit',[50,100,90])]:
    folder = ROOT/base/state
    editable.write_clip(folder)
    source = folder/f'{state.lower()}_front_r.aseprite'
    raw = bytearray(source.read_bytes()); offset = 128
    for ms in durations:
        struct.pack_into('<H', raw, offset+8, ms)
        offset += struct.unpack_from('<I', raw, offset)[0]
    source.write_bytes(raw)
    clip = read(f'{base}/{state}/clip.json')
    clip.update(durationsMs=durations, layerName='Body and Warrior outfit - weaponless', designReference='characters/orc-01/concepts/orc-01-warrior-concept-07.png', status='CANDIDATE_NOT_APPLIED', timingRuntime='Variable durations are demonstrated in editor/preview only; no Unity timing integration claimed.')
    save(f'{base}/{state}/clip.json', clip)
    new = [f'{base}/{state}/{state.lower()}_front_r_{i:02d}.png' for i in range(len(durations))]
    old = next(c for c in audit['clips'] if c['id']=='orc-01' and c['state']==state and c['direction']=='front_r')
    before = [f['file'] for f in old['frames']]
    jobs.append({'id':state.lower()+'-front-r', 'source':str(source.relative_to(ROOT)).replace('\\','/'), 'sourceSha256':sha(source.relative_to(ROOT)), 'profile':{'width':128,'height':128,'frames':len(new),'durationsMs':durations,'groundY':126,'alpha':'binary','requireContent':True,'requireTransparency':True}, 'compare':new})
    clips.append({'state':state,'direction':'front_r','before':before,'after':new,'beforeDurationsMs':[90 if state=='Attack' else 80]*len(new),'afterDurationsMs':durations,'artisticApproval':'PENDING_CREATOR'})
    # Exact-pixel comparison and lossless animated preview; no artistic edits.
    board = Image.new('RGBA',(len(new)*256,560),(27,32,40,255)); d=ImageDraw.Draw(board)
    for row, files in enumerate([before,new]):
        d.text((8,row*280+4),('ATUAL APROVADO' if row==0 else 'CANDIDATO v2')+' / '+state,fill='white',font=font)
        for i,p in enumerate(files):
            tile=Image.open(ROOT/p).convert('RGBA').resize((256,256),Image.Resampling.NEAREST)
            board.alpha_composite(tile,(i*256,row*280+24))
    board.save(ROOT/f'reports/orc-audit-v2/{state.lower()}-comparison.png')
    frames=[Image.open(ROOT/p).convert('RGBA') for p in new]
    frames[0].save(folder/'preview.png',save_all=True,append_images=frames[1:],duration=durations,loop=0,disposal=0,blend=0)
    generation[state].update(source=f'{base}/{state}/authored-sheet.png',sourceSha256=sha(f'{base}/{state}/authored-sheet.png'),editable=str(source.relative_to(ROOT)).replace('\\','/'),nativeFrames=[{'file':p,'sha256':sha(p)} for p in new],reconstruction='Existing extract-animation-sheet.py: independent authored poses, forced native grid, shared approved palette, integer registration. Not hand drawn. No concept reduced into production.')
generation['concept'].update(file='characters/orc-01-refinement-v2/concepts/warrior-refinement-v2.png',sha256=sha('characters/orc-01-refinement-v2/concepts/warrior-refinement-v2.png'))
for key in ['concept','Attack','Hit']:
    generation[key]['referenceHashes']=[{'file':p,'sha256':sha(p)} for p in generation[key]['references']]
save('characters/orc-01-refinement-v2/source/generation-record.json',generation)
save(f'{base}/editor.json',{'schemaVersion':1,'id':'orc-combat-refinement-v2','kind':'character','characterId':'orc-01','jobs':jobs})
save('reports/orc-refinement-candidates-v2.json',{'status':'PENDING_CREATOR_NOT_APPLIED','concept':generation['concept']['file'],'clips':clips,'manifest':f'{base}/editor.json','limitations':['Only front_r Attack and Hit pilots. No other direction or Job rewritten.','Concept v2 requires Gate 1 before any production sprites based on it.','Native reconstruction is lossy and needs visual approval; baseline remains authoritative.','No weapons, events, sockets, Unity registration or runtime timing implemented.']})
print('Packaged concept and 8 native candidate frames; baseline unchanged.')
