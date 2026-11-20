import json, hashlib, os

root_dir = os.getcwd()

def sha256(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

cells = [
    {
        'direction': 'back_r',
        'action': 'Sword Attack',
        'category': 'Sword',
        'state': 'Attack',
        'cycleName': 'back_r-Sword-full',
        'clipJson': 'characters/orc-v1/source/combat-rescue-v5/body-specialist/final-cycles/back_r-Sword-full/clip.json',
        'clipSha256': sha256('characters/orc-v1/source/combat-rescue-v5/body-specialist/final-cycles/back_r-Sword-full/clip.json'),
        'experimentClipJson': 'experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/back_r-Sword-full/clip.json',
        'experimentClipSha256': sha256('experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/back_r-Sword-full/clip.json'),
        'masterAseprite': 'characters/orc-v1/source/combat-rescue-v5/body-specialist/final-cycles/back_r-Sword-full/body256.aseprite',
        'masterSha256': sha256('characters/orc-v1/source/combat-rescue-v5/body-specialist/final-cycles/back_r-Sword-full/body256.aseprite'),
        'nativeMasterAseprite': 'characters/orc-v1/source/combat-rescue-v5/body-specialist/final-cycles/back_r-Sword-full/native128.aseprite',
        'nativeMasterSha256': sha256('characters/orc-v1/source/combat-rescue-v5/body-specialist/final-cycles/back_r-Sword-full/native128.aseprite'),
        'frameCount': 12,
        'totalDurationMs': 730,
        'acceptedKeyPreservation': [
            {'index': 3, 'name': '01-hoist', 'sha256': 'a573c039202f52315eb681da5fe375199b34fa101a1f9404b8c9263920589ff2', 'byteExact': True, 'pixelExact': True},
            {'index': 4, 'name': '02-apex', 'sha256': '9607fb5c7f36b1dcd7649eba505d5eca925f2abb670d636f8a235c42c6cbb40d', 'byteExact': True, 'pixelExact': True},
            {'index': 7, 'name': '03-impact', 'sha256': 'ac51e08bdd1cc40de255f5233d08f79916c8112b2b9c68b00eee8c509f204107', 'byteExact': True, 'pixelExact': True}
        ]
    },
    {
        'direction': 'back_l',
        'action': 'Sword Attack',
        'category': 'Sword',
        'state': 'Attack',
        'cycleName': 'back_l-Sword-full',
        'clipJson': 'characters/orc-v1/source/combat-rescue-v5/body-specialist/final-cycles/back_l-Sword-full/clip.json',
        'clipSha256': sha256('characters/orc-v1/source/combat-rescue-v5/body-specialist/final-cycles/back_l-Sword-full/clip.json'),
        'experimentClipJson': 'experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/back_l-Sword-full/clip.json',
        'experimentClipSha256': sha256('experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/back_l-Sword-full/clip.json'),
        'masterAseprite': 'characters/orc-v1/source/combat-rescue-v5/body-specialist/final-cycles/back_l-Sword-full/body256.aseprite',
        'masterSha256': sha256('characters/orc-v1/source/combat-rescue-v5/body-specialist/final-cycles/back_l-Sword-full/body256.aseprite'),
        'nativeMasterAseprite': 'characters/orc-v1/source/combat-rescue-v5/body-specialist/final-cycles/back_l-Sword-full/native128.aseprite',
        'nativeMasterSha256': sha256('characters/orc-v1/source/combat-rescue-v5/body-specialist/final-cycles/back_l-Sword-full/native128.aseprite'),
        'frameCount': 12,
        'totalDurationMs': 730,
        'acceptedKeyPreservation': [
            {'index': 3, 'name': '01-hoist', 'sha256': '4d0063ba3ec21af78fb490ff4f80c48ec71f5663316c9afd6fa60c4689884096', 'byteExact': True, 'pixelExact': True},
            {'index': 4, 'name': '02-apex', 'sha256': '206a297a862278cc21649f8613199cc304d58ec1b771c97c652b09c57fb40f30', 'byteExact': True, 'pixelExact': True},
            {'index': 7, 'name': '03-impact', 'sha256': 'bc3f5c1102377ffeba631dfef93d843bf1c12d431f4b016286c1c2a7bad147f1', 'byteExact': True, 'pixelExact': True}
        ]
    },
    {
        'direction': 'back_l',
        'action': 'Axe Attack',
        'category': 'Axe',
        'state': 'Attack',
        'cycleName': 'back_l-Axe-full',
        'clipJson': 'characters/orc-v1/source/combat-rescue-v5/body-specialist/final-cycles/back_l-Axe-full/clip.json',
        'clipSha256': sha256('characters/orc-v1/source/combat-rescue-v5/body-specialist/final-cycles/back_l-Axe-full/clip.json'),
        'experimentClipJson': 'experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/back_l-Axe-full/clip.json',
        'experimentClipSha256': sha256('experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/back_l-Axe-full/clip.json'),
        'masterAseprite': 'characters/orc-v1/source/combat-rescue-v5/body-specialist/final-cycles/back_l-Axe-full/body256.aseprite',
        'masterSha256': sha256('characters/orc-v1/source/combat-rescue-v5/body-specialist/final-cycles/back_l-Axe-full/body256.aseprite'),
        'nativeMasterAseprite': 'characters/orc-v1/source/combat-rescue-v5/body-specialist/final-cycles/back_l-Axe-full/native128.aseprite',
        'nativeMasterSha256': sha256('characters/orc-v1/source/combat-rescue-v5/body-specialist/final-cycles/back_l-Axe-full/native128.aseprite'),
        'frameCount': 12,
        'totalDurationMs': 1100,
        'acceptedKeyPreservation': [
            {'index': 3, 'name': '01-hoist', 'sha256': 'd240b9ac537499625f7a86fcbfcf8cf2287b26947dc164092a76f313196c79ce', 'byteExact': True, 'pixelExact': True},
            {'index': 4, 'name': '02-apex', 'sha256': '7adfd9f45be25ce862d261f4bf6e47881e52043969605acf9cd4f918c9e00d56', 'byteExact': True, 'pixelExact': True},
            {'index': 7, 'name': '03-impact', 'sha256': '7a0c943c51f555f683ba78913150190e9b375a0091714644129b6fef7ea8c1a0', 'byteExact': True, 'pixelExact': True}
        ]
    }
]

patch_manifest = {
    'schemaVersion': 1,
    'status': 'BODY_THREE_FULL_READY',
    'technicalStatus': 'TECHNICALLY_COMPLETE',
    'artisticStatus': 'VISUAL_REVIEW_REQUIRED',
    'creatorStatus': 'PENDING_CREATOR',
    'globalArtisticStatusUnchanged': 'ARTISTIC_REVISION_REQUIRED',
    'character': 'orc-v1',
    'identity': 'Verde Warcraft',
    'cellsCount': 3,
    'cells': cells
}

with open('experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/patch-manifest.json', 'w', encoding='utf-8') as f:
    json.dump(patch_manifest, f, indent=2)

checkpoint = {
    'schemaVersion': 1,
    'checkpoint': 'BODY_THREE_FULL_READY',
    'stage': 'final-body-cycles',
    'timestamp': '2026-10-29T16:05:00Z',
    'technicalStatus': 'TECHNICALLY_COMPLETE',
    'artisticStatus': 'VISUAL_REVIEW_REQUIRED',
    'globalArtisticStatusUnchanged': 'ARTISTIC_REVISION_REQUIRED',
    'creatorStatus': 'PENDING_CREATOR',
    'character': 'orc-v1',
    'identity': 'Verde Warcraft',
    'qaTargetSession': '863ae631-5582-4955-a0ef-020d51692fbb',
    'qaModel': 'Gemini 3.8 Flash (Antigravity)',
    'accounting': {
        'initialBalance': 1351.70,
        'finalBalance': 1342.70,
        'generationsConsumed': 9.0,
        'jobsCount': 9,
        'unauthorizedOrFailedJobsCount': 0
    },
    'priorArtReference': {
        'cycle': 'full-back-r-axe',
        'status': 'BODY_BACK_R_AXE_FULL_READY',
        'preserved': True,
        'unmodified': True
    },
    'cells': cells
}

with open('experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/checkpoint.json', 'w', encoding='utf-8') as f:
    json.dump(checkpoint, f, indent=2)

print("Generated patch-manifest.json and checkpoint.json successfully!")
