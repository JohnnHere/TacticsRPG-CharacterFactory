import hashlib
print(hashlib.sha256(open(r"characters/orc-v1/source/combat-rescue-v5/localized/walk-back_l-fixed.aseprite","rb").read()).hexdigest())
