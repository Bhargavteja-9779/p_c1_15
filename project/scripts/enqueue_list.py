#!/usr/bin/env python3
"""Enqueue an explicit list of jit_run jobs from a JSON file (list of param dicts). Idempotent (job id from params).
Usage: python scripts/enqueue_list.py specs.json PRIORITY"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from src.state import STATE, read_json, write_json, FileLock
specs = json.load(open(sys.argv[1])); prio = int(sys.argv[2])
with FileLock(STATE / "queue_full.qlock", blocking=True):
    q = read_json(STATE / "queue.json", {"jobs": []}); have = {j["id"] for j in q["jobs"]}
    st = read_json(STATE / "agent_state.json", {}); n = 0
    for p in specs:
        jid = f"{p['experiment']}_{p['project']}_{p.get('variant', p['method'])}_s{p['seed']}"
        if jid in have: continue
        q["jobs"].append({"id": jid, "kind": "jit_run", "params": p, "status": "pending", "attempts": 0,
                          "cycle": st.get("cycle"), "priority": prio}); n += 1
    write_json(STATE / "queue.json", q)
print("added", n)
