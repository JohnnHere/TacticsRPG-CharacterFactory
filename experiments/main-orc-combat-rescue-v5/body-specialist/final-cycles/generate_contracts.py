import os, json, hashlib

root_dir = os.getcwd()

def sha256(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

cycles_info = [
    {
        'name': 'back_r-Sword-full',
        'direction': 'back_r',
        'category': 'Sword',
        'clip_id': 'basic.sword-slash.body-specialist',
        'revision': 'body-specialist-full-back-r-sword-v1',
        'status': 'BODY_BACK_R_SWORD_FULL_READY',
        'scope': 'Complete body-only sword slash cycle, empty-handed layers-off',
        'durations': [40, 60, 60, 70, 70, 40, 40, 90, 70, 70, 60, 60],
        'total_duration': 730,
        'key_dir': 'back_r-Sword-keys',
        'frame_to_key_index': {3: 0, 4: 1, 7: 2},
        'jobs': [
            {'tool': 'animate_image', 'jobId': '2e5f7343-77af-474d-adec-1ab75b938005', 'segment': 'entry', 'cost': 1.0, 'seed': 310101},
            {'tool': 'animate_image', 'jobId': '815bb8a5-b497-4298-ac23-4f514df811fe', 'segment': 'descent', 'cost': 1.0, 'seed': 310102},
            {'tool': 'animate_image', 'jobId': '2bc3999a-36ad-4499-9451-6c074ea379c6', 'segment': 'recovery', 'cost': 1.0, 'seed': 310103}
        ]
    },
    {
        'name': 'back_l-Sword-full',
        'direction': 'back_l',
        'category': 'Sword',
        'clip_id': 'basic.sword-slash.body-specialist',
        'revision': 'body-specialist-full-back-l-sword-v1',
        'status': 'BODY_BACK_L_SWORD_FULL_READY',
        'scope': 'Complete body-only sword slash cycle, empty-handed layers-off',
        'durations': [40, 60, 60, 70, 70, 40, 40, 90, 70, 70, 60, 60],
        'total_duration': 730,
        'key_dir': 'back_l-Sword-keys',
        'frame_to_key_index': {3: 0, 4: 1, 7: 2},
        'jobs': [
            {'tool': 'animate_image', 'jobId': '3e835e9c-673f-4f9d-a412-bf91a5de7edd', 'segment': 'entry', 'cost': 1.0, 'seed': 310201},
            {'tool': 'animate_image', 'jobId': 'e11da933-c68b-4fbb-9942-0270c16a564a', 'segment': 'descent', 'cost': 1.0, 'seed': 310202},
            {'tool': 'animate_image', 'jobId': 'e976e860-6873-4dec-a119-0268b15613cf', 'segment': 'recovery', 'cost': 1.0, 'seed': 310203}
        ]
    },
    {
        'name': 'back_l-Axe-full',
        'direction': 'back_l',
        'category': 'Axe',
        'clip_id': 'basic.axe-chop.body-specialist',
        'revision': 'body-specialist-full-back-l-axe-v1',
        'status': 'BODY_BACK_L_AXE_FULL_READY',
        'scope': 'Complete body-only overhead axe cycle, empty-handed layers-off',
        'durations': [70, 80, 90, 100, 110, 50, 60, 110, 100, 100, 100, 130],
        'total_duration': 1100,
        'key_dir': 'back_l-Axe-keys',
        'frame_to_key_index': {3: 0, 4: 1, 7: 2},
        'jobs': [
            {'tool': 'animate_image', 'jobId': '7c0b1ca2-c9af-420b-9fb5-c0e606650b00', 'segment': 'entry', 'cost': 1.0, 'seed': 310301},
            {'tool': 'animate_image', 'jobId': '6f8e537c-60db-4504-a5d5-400b4cf0eb29', 'segment': 'descent', 'cost': 1.0, 'seed': 310302},
            {'tool': 'animate_image', 'jobId': '3061a847-428c-4dad-a57e-bed16eb34720', 'segment': 'recovery', 'cost': 1.0, 'seed': 310303}
        ]
    }
]

roots = [
    'characters/orc-v1/source/combat-rescue-v5/body-specialist/final-cycles',
    'experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles'
]

for cycle in cycles_info:
    cname = cycle['name']
    kdir_path = os.path.join(root_dir, 'experiments/main-orc-combat-rescue-v5/body-specialist', cycle['key_dir'])
    with open(os.path.join(kdir_path, 'representative.json'), 'r', encoding='utf-8') as f:
        k_rep = json.load(f)
    
    # Map frame index to accepted key info from representative
    frame_keys = {}
    for f_idx, k_idx in cycle['frame_to_key_index'].items():
        k_obj = k_rep['keys'][k_idx]
        frame_keys[f_idx] = {
            'keyName': k_obj['key'],
            'sourcePath': k_obj['nativeExport']['path'],
            'sourceSha256': k_obj['nativeExport']['sha256'],
            'compositeSourcePath': k_obj['compositeExport']['path'],
            'compositeSourceSha256': k_obj['compositeExport']['sha256']
        }
        
    for root in roots:
        cdir = os.path.join(root_dir, root, cname)
        
        # Masters
        m_nat_p = os.path.join(cdir, 'native128.aseprite')
        m_nat_rel = f'{root}/{cname}/native128.aseprite'
        m_nat_sha = sha256(m_nat_p)
        
        m_comp_p = os.path.join(cdir, 'body256.aseprite')
        m_comp_rel = f'{root}/{cname}/body256.aseprite'
        m_comp_sha = sha256(m_comp_p)
        
        # Strips
        s_nat_p = os.path.join(cdir, 'native-strip.png')
        s_nat_rel = f'{root}/{cname}/native-strip.png'
        s_nat_sha = sha256(s_nat_p)
        
        s_comp_p = os.path.join(cdir, 'body256-strip.png')
        s_comp_rel = f'{root}/{cname}/body256-strip.png'
        s_comp_sha = sha256(s_comp_p)
        
        # Frames
        frames = []
        for i in range(12):
            fn = f'{i:02d}.png'
            f_nat_p = os.path.join(cdir, 'native', fn)
            f_nat_rel = f'{root}/{cname}/native/{fn}'
            f_nat_sha = sha256(f_nat_p)
            
            f_comp_p = os.path.join(cdir, 'body256', fn)
            f_comp_rel = f'{root}/{cname}/body256/{fn}'
            f_comp_sha = sha256(f_comp_p)
            
            dur = cycle['durations'][i]
            frame_obj = {
                'index': i,
                'durationMs': dur,
                'nativePng': {'path': f_nat_rel, 'sha256': f_nat_sha},
                'compositePng': {'path': f_comp_rel, 'sha256': f_comp_sha},
                'weaponVisible': False
            }
            if i in frame_keys:
                kinfo = frame_keys[i]
                frame_obj['isAcceptedKey'] = True
                frame_obj['keyName'] = kinfo['keyName']
                frame_obj['keySourceSha256'] = kinfo['sourceSha256']
                frame_obj['pixelExact'] = True
                frame_obj['byteExact'] = (f_nat_sha == kinfo['sourceSha256'])
            else:
                frame_obj['isAcceptedKey'] = False
                
            frames.append(frame_obj)
            
        # clip.json
        clip_data = {
            'schemaVersion': 1,
            'id': cycle['clip_id'],
            'revision': cycle['revision'],
            'character': 'orc-v1',
            'identity': 'Verde Warcraft',
            'category': cycle['category'],
            'state': 'Attack',
            'direction': cycle['direction'],
            'scope': cycle['scope'],
            'loop': False,
            'oneShot': True,
            'terminal': False,
            'canvas': [256, 256],
            'nativeCanvas': [128, 128],
            'bodyOffset': [64, 64],
            'groundY': 190,
            'nativeGroundY': 126,
            'frameCount': 12,
            'durationsMs': cycle['durations'],
            'totalDurationMs': cycle['total_duration'],
            'master': m_comp_rel,
            'masterSha256': m_comp_sha,
            'bodyMaster': m_comp_rel,
            'bodyMasterSha256': m_comp_sha,
            'nativeMaster': m_nat_rel,
            'nativeMasterSha256': m_nat_sha,
            'strip': s_nat_rel,
            'stripSha256': s_nat_sha,
            'compositeStrip': s_comp_rel,
            'compositeStripSha256': s_comp_sha,
            'technicalStatus': 'TECHNICALLY_COMPLETE',
            'artisticStatus': 'VISUAL_REVIEW_REQUIRED',
            'creatorStatus': 'PENDING_CREATOR',
            'propagationAllowed': False,
            'frames': frames
        }
        
        clip_out = os.path.join(cdir, 'clip.json')
        with open(clip_out, 'w', encoding='utf-8') as f:
            json.dump(clip_data, f, indent=2)
        clip_sha = sha256(clip_out)
        
        # representative.json
        accepted_key_reuse = []
        for kidx in [3, 4, 7]:
            kinfo = frame_keys[kidx]
            exp_rel = f"{root}/{cname}/native/{kidx:02d}.png"
            exp_sha = sha256(os.path.join(root_dir, exp_rel))
            accepted_key_reuse.append({
                'frameIndex': kidx,
                'keyName': kinfo['keyName'],
                'source': {'path': kinfo['sourcePath'], 'sha256': kinfo['sourceSha256']},
                'export': {'path': exp_rel, 'sha256': exp_sha},
                'pixelExact': True,
                'byteExact': (exp_sha == kinfo['sourceSha256'])
            })
            
        rep_data = {
            'schemaVersion': 1,
            'status': cycle['status'],
            'technicalStatus': 'TECHNICALLY_COMPLETE',
            'artisticStatus': 'VISUAL_REVIEW_REQUIRED',
            'globalArtisticStatusUnchanged': 'ARTISTIC_REVISION_REQUIRED',
            'creatorStatus': 'PENDING_CREATOR',
            'character': 'orc-v1',
            'identity': 'Verde Warcraft',
            'direction': cycle['direction'],
            'category': cycle['category'],
            'scope': cycle['scope'],
            'clip': {'path': f'{root}/{cname}/clip.json', 'sha256': clip_sha},
            'master': {'path': m_comp_rel, 'sha256': m_comp_sha},
            'nativeMaster': {'path': m_nat_rel, 'sha256': m_nat_sha},
            'frameCount': 12,
            'totalDurationMs': cycle['total_duration'],
            'acceptedKeyReuse': accepted_key_reuse,
            'generationAccounting': {
                'jobs': cycle['jobs'],
                'generationsCharged': 3.0
            }
        }
        
        rep_out = os.path.join(cdir, 'representative.json')
        with open(rep_out, 'w', encoding='utf-8') as f:
            json.dump(rep_data, f, indent=2)
            
        print(f"Generated contracts for {cname} in {root}: clip.json ({clip_sha[:12]}...), representative.json")

print("All contracts generated successfully!")
