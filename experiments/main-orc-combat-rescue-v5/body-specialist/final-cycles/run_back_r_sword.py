import sys
from pathlib import Path
from generate_cycle import run_animate_job, ROOT

out_dir = ROOT / "experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles/back_r-Sword-full"
out_dir.mkdir(parents=True, exist_ok=True)

can_input = ROOT / "experiments/main-orc-combat-rescue-v5/body-specialist/canonical-input.png"
key1 = ROOT / "experiments/main-orc-combat-rescue-v5/body-specialist/back_r-Sword-keys/01-native.png"
key2 = ROOT / "experiments/main-orc-combat-rescue-v5/body-specialist/back_r-Sword-keys/02-native.png"
key3 = ROOT / "experiments/main-orc-combat-rescue-v5/body-specialist/back_r-Sword-keys/03-native.png"

# Bridge 1: Entry is already done!

# Bridge 2: Descent (slash)
action_descent = (
    "Continue immediately from the shown lateral sword slash apex into the provided low finish impact. "
    "The anatomical RIGHT clenched empty gauntlet cuts diagonally downward across the forward right quadrant towards the hip, "
    "extending and following through cleanly. The bulky body leans forward into the slash, hips and knees absorb the momentum, "
    "dorsal armor and shoulder girdle follow the motion. Anatomical LEFT empty glove stabilizes the torso naturally. "
    "Rear north-east view, exact armor identity fixed. Completely unarmed, closed wine-brown gauntlet fists. "
    "No weapon, handle, face, or extra limb. Finish in the exact supplied impact stance."
)
run_animate_job("descent", action_descent, key2, key3, seed=310102, out_dir=out_dir)

# Bridge 3: Recovery
action_recovery = (
    "Recover from the supplied low sword impact stance into the exact supplied relaxed empty-handed rear guard. "
    "Straighten knees and pelvis gradually, recover dorsal plate and shoulder girdle together. "
    "Anatomical RIGHT closed empty glove relaxes back to the side from the low hip position. "
    "Left empty glove returns to relaxed guard. Bring stance smoothly back to neutral under the bulky body, no sliding or jump. "
    "Continuous shoulder-elbow-wrist articulation. Same rear north-east orc, armor, and ground line. Completely unarmed, no weapon or face."
)
run_animate_job("recovery", action_recovery, key3, can_input, seed=310103, out_dir=out_dir)

print("back_r-Sword bridges generated successfully!")
