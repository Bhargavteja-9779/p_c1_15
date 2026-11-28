#!/usr/bin/env python3
"""Export the parameters of every queued job, grouped by experiment, to experiments/specs/<EXP>.json so that a
fresh clone can re-enqueue any experiment with scripts/enqueue_list.py. Idempotent."""
import sys, os, json, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from src.state import ROOT
q = json.load(open(ROOT / "state" / "queue.json"))["jobs"]
by = collections.defaultdict(list); prio = {}
for j in q:
    e = j["params"]["experiment"]; by[e].append(j["params"]); prio[e] = j.get("priority", 10)
d = ROOT / "experiments" / "specs"; d.mkdir(exist_ok=True)
for e, L in by.items():
    json.dump(L, open(d / f"{e}.json", "w"), indent=0)
json.dump(prio, open(d / "priorities.json", "w"), indent=1)
print({e: len(L) for e, L in by.items()})
