import json

with open('experiments/main-orc-rear-recovery-v2/raw/req_poll_walk_l.json', 'w') as f:
    json.dump({'job_id': '64cd4cb7-dba7-4234-9f96-a9da268388fb'}, f)

with open('experiments/main-orc-rear-recovery-v2/raw/req_poll_unarmed_r.json', 'w') as f:
    json.dump({'job_id': '2ace783c-ff36-499b-b473-52adad36459e'}, f)

print("Polling request files written.")
