#!/usr/bin/env python3
"""Print project status from state files only. Usage: python scripts/status.py"""
import os, sys, json, subprocess
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from src.state import ROOT, STATE, read_json, heartbeat_age_s
from collections import Counter

s = read_json(STATE / "agent_state.json", {})
print("=== AGENT STATE ===")
for k in ["status", "cycle", "phase", "step", "pivots", "journal", "topic_id", "last_action", "next_action", "updated"]:
    print(f"  {k:12s}: {s.get(k)}")
b = read_json(STATE / "budget.json", {})
g = b.get("global_seconds", 0) / 3600; pc = {k: round(v / 3600, 3) for k, v in b.get("per_cycle_seconds", {}).items()}
print(f"=== COMPUTE === global {g:.3f} h / {b.get('global_budget_s',0)/3600:.0f} h ; per cycle (h) {pc} / {b.get('cycle_budget_s',0)/3600:.0f} h")
for mode, fn in [("full", "queue.json"), ("quick", "queue_quick.json")]:
    q = read_json(STATE / fn, {"jobs": []})
    c = Counter(j["status"] for j in q["jobs"])
    print(f"=== QUEUE ({mode}) === {dict(c)} total={len(q['jobs'])}")
    for j in q["jobs"]:
        if j["status"] in ("running", "failed", "failed_permanent"):
            print(f"    {j['status']:16s} {j['id']} attempts={j.get('attempts')}")
age = heartbeat_age_s()
print(f"=== HEARTBEAT === age {'n/a' if age is None else f'{age:.0f}s'}")
try:
    out = subprocess.run(["pgrep", "-af", "run_all.py"], capture_output=True, text=True).stdout.strip()
    print("=== RUNNER PROCESSES ===\n" + (out or "  none"))
    out = subprocess.run(["pgrep", "-af", "supervisor.sh"], capture_output=True, text=True).stdout.strip()
    print("=== SUPERVISOR PROCESSES ===\n" + (out or "  none"))
except FileNotFoundError:
    pass
