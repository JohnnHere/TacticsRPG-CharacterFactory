import sys
from pathlib import Path
from generate_cycle import run_animate_job, ROOT

out_dir = ROOT / "experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/back_l-Sword-full"
out_dir.mkdir(parents=True, exist_ok=True)

dir_back_l = ROOT / "characters/orc-v1/sprites/Directions/orc_v1_dir_back_l.png"
key1 = ROOT / "experiments/main-orc-combat-rescue-v5/body-specialist/back_l-Sword-keys/01-native.png"
key2 = ROOT / "experiments/main-orc-combat-rescue-v5/body-specialist/back_l-Sword-keys/02-native.png"
key3 = ROOT / "experiments/main-orc-combat-rescue-v5/body-specialist/back_l-Sword-keys/03-native.png"

# Bridge 1: Entry
action_entry = (
    "From the supplied relaxed unarmed rear north-west guard, prepare a right-handed diagonal sword slash, ending in the exact supplied hoist. "
    "Flex knees, turn upper torso slightly northwest, raise anatomical RIGHT elbow and forearm, drawing closed empty glove up near collar and ear. "
    "Anatomical LEFT arm extends forward-down as dynamic counterbalance. Continuous shoulder-elbow-wrist articulation. "
    "Preserve same bulky green orc V1, occipital skull with NO face, dark iron armor, spiked pauldrons, rear north-west view. "
    "Completely unarmed, closed wine-brown gauntlets. No weapon, handle, or extra limbs. Feet planted at ground line."
)
run_animate_job("entry", action_entry, dir_back_l, key1, seed=310201, out_dir=out_dir)

# Bridge 2: Slash descent
action_descent = (
    "Continue immediately from the shown sword slash apex into the provided low impact finish. "
    "The anatomical RIGHT clenched empty gauntlet cuts downward and across the north-west diagonal quadrant towards the right flank, "
    "elbow and forearm following a continuous slashing arc. Bulky torso rotates and hinges forward with the cut, knees absorb weight. "
    "Anatomical LEFT arm counterbalances naturally. Rear north-west view, exact armor identity fixed. "
    "Completely empty handed, closed gauntlets. No weapon, handle, face, or extra limbs. Finish in the exact supplied impact stance."
)
run_animate_job("descent", action_descent, key2, key3, seed=310202, out_dir=out_dir)

# Bridge 3: Recovery
action_recovery = (
    "Recover from the supplied low sword impact finish into the exact supplied relaxed empty-handed rear north-west guard. "
    "Straighten pelvis and knees gradually, recover torso and dorsal armor to balanced upright posture. "
    "Anatomical RIGHT closed empty glove draws back up from right flank to natural guard at side. "
    "Left arm returns to relaxed resting position. Continuous joint chains, planted boots at ground line. "
    "Same rear north-west bulky orc V1, no face, no weapon or handle."
)
run_animate_job("recovery", action_recovery, key3, dir_back_l, seed=310203, out_dir=out_dir)

print("back_l-Sword bridges generated successfully!")
