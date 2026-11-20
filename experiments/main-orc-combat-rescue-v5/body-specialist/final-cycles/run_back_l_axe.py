import sys
from pathlib import Path
from generate_cycle import run_animate_job, ROOT

out_dir = ROOT / "experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/back_l-Axe-full"
out_dir.mkdir(parents=True, exist_ok=True)

dir_back_l = ROOT / "characters/orc-v1/sprites/Directions/orc_v1_dir_back_l.png"
key1 = ROOT / "experiments/main-orc-combat-rescue-v5/body-specialist/back_l-Axe-keys/01-native.png"
key2 = ROOT / "experiments/main-orc-combat-rescue-v5/body-specialist/back_l-Axe-keys/02-native.png"
key3 = ROOT / "experiments/main-orc-combat-rescue-v5/body-specialist/back_l-Axe-keys/03-native.png"

# Bridge 1: Entry
action_entry = (
    "From the supplied relaxed unarmed rear north-west guard, prepare a heavy right-handed overhead axe cleave, ending in the exact supplied high hoist. "
    "Flex knees deeply to load weight through planted boots, load pelvis and dorsal plate, raise anatomical RIGHT elbow and forearm high above the head "
    "with clenched empty glove. Anatomical LEFT arm moves naturally as dynamic counterweight. Shoulder-elbow-wrist stays continuous. "
    "Preserve same bulky green orc V1, occipital skull with NO face, dark iron armor, spiked pauldrons, rear north-west perspective. "
    "Completely empty handed, closed wine-brown gauntlets. No weapon, handle, or face. Ground line constant."
)
run_animate_job("entry", action_entry, dir_back_l, key1, seed=310301, out_dir=out_dir)

# Bridge 2: Heavy descent
action_descent = (
    "Continue immediately from the shown high arched overhead apex into the provided heavy downward impact. "
    "The anatomical RIGHT clenched empty gauntlet descends from above the crown in a crushing vertical forward-downward smash, "
    "bending and extending elbow continuously. The whole bulky body hinges forward, head and neck drop, dorsal armor compresses, "
    "pelvis sinks, knees bend deeply as weight transfers into the wide planted boots. Anatomical LEFT arm reacts as counterweight and drops naturally. "
    "Rear north-west view, exact armor fixed. Completely unarmed, closed gauntlets. No weapon, handle, or face. Negative space clean. "
    "Finish in the exact supplied heavy impact stance."
)
run_animate_job("descent", action_descent, key2, key3, seed=310302, out_dir=out_dir)

# Bridge 3: Recovery
action_recovery = (
    "Recover from the supplied deep forward-hinged heavy axe impact stance into the exact supplied relaxed empty-handed rear north-west guard. "
    "Begin with brief grounded follow-through, then straighten knees, hips and torso gradually, lifting head and recovering dorsal armor. "
    "Anatomical RIGHT closed empty glove relaxes down beside the right hip, never swinging back overhead. Left arm counterbalances and returns to side. "
    "Bring stance smoothly back to neutral under bulky body. Continuous shoulder-elbow-wrist chain. Same rear north-west orc V1, no weapon or face."
)
run_animate_job("recovery", action_recovery, key3, dir_back_l, seed=310303, out_dir=out_dir)

print("back_l-Axe bridges generated successfully!")
