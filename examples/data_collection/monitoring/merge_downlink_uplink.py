import json

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

up = load_json("/home/kim/five_g_uplink_statistics.json")
down = load_json("/home/kim/five_g_downlink_statistics.json")

n_up = len(up["load"])
n_down = len(down["load"])
merged = {}

for key in ["load", "signal_strength", "cpu_limit", "memory_limit"]:
    merged[key] = up[key] + down[key]

entities = set(list(up.keys()) + list(down.keys())) - {"load", "signal_strength", "cpu_limit", "memory_limit"}

for ent in entities:
    merged[ent] = {}
    up_metrics = up.get(ent, {})
    down_metrics = down.get(ent, {})
    all_metrics = set(list(up_metrics.keys()) + list(down_metrics.keys()))

    for m in all_metrics:
        m_up = up_metrics.get(m, [None] * n_up)
        m_down = down_metrics.get(m, [None] * n_down)
        merged[ent][m] = m_up + m_down

with open("/home/kim/merged_five_g_statistics.json", "w") as f:
    json.dump(merged, f, indent=4)