#!/usr/bin/env python3
"""Regenerate HANDOFF.md from state/ (plus the hand-maintained sections in state/handoff_notes.md).
Run after every step:  python scripts/write_handoff.py"""
import os, sys, re, subprocess
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from src.state import ROOT, STATE, read_json, atomic_write_text, now_iso, heartbeat_age_s
from collections import Counter

s = read_json(STATE / "agent_state.json", {})
b = read_json(STATE / "budget.json", {})
q = read_json(STATE / "queue.json", {"jobs": []})
gates = read_json(STATE / "gates.json", {f"G{i}": {"status": "unknown", "evidence": ""} for i in range(1, 12)})
notes = (STATE / "handoff_notes.md").read_text() if (STATE / "handoff_notes.md").exists() else ""
dec = (STATE / "decisions.md").read_text() if (STATE / "decisions.md").exists() else ""
items = re.findall(r"^- \*\*(.+?)\*\* — (.+)$", dec, flags=re.M)[-10:]
fails = sorted((ROOT / "journal" / "ENTRIES").glob("*_FAILURE_*.md"))[-10:] + sorted((ROOT / "journal" / "ENTRIES").glob("*_DEAD END_*.md"))[-3:]
c = Counter(j["status"] for j in q["jobs"])
running = [j["id"] for j in q["jobs"] if j["status"] == "running"]
try:
    procs = subprocess.run(["pgrep", "-af", "run_all.py|supervisor.sh"], capture_output=True, text=True).stdout.strip()
except Exception:
    procs = "?"
g = b.get("global_seconds", 0) / 3600
cyc = b.get("per_cycle_seconds", {}).get(str(s.get("cycle")), 0) / 3600
age = heartbeat_age_s()
L = []
L += [f"# HANDOFF — read this first", f"*Auto-generated {now_iso()} by scripts/write_handoff.py*", ""]
L += ["## READ ALSO: USER_DIRECTIVES.md (owner standing orders)\n\n## Where we are",
      f"- **Status:** {s.get('status')}   **Cycle:** {s.get('cycle')} / {s.get('config',{}).get('MAX_CYCLES')}   **Phase:** {s.get('phase')}   **Pivots:** {s.get('pivots')} / {s.get('config',{}).get('MAX_PIVOTS')}",
      f"- **Step:** {s.get('step')}",
      f"- **Last action:** {s.get('last_action')}",
      f"- **NEXT ACTION:** {s.get('next_action')}", "",
      f"- **Selected journal:** {s.get('journal')}",
      f"- **Topic:** {s.get('topic')}",
      f"- **Hypothesis:** {s.get('hypothesis')}", ""]
L += ["## Running right now",
      f"- Queue (full): {dict(c)}; running jobs: {running or 'none'}",
      f"- Processes: `{procs or 'none'}`",
      f"- Heartbeat age: {'n/a' if age is None else f'{age:.0f}s'}", ""]
L += ["## Compute",
      f"- Cycle {s.get('cycle')}: {cyc:.2f} h / {b.get('cycle_budget_s',54000)/3600:.0f} h   Global: {g:.2f} h / {b.get('global_budget_s',432000)/3600:.0f} h (CPU-hours; machine has no GPU)", ""]
L += ["## Gate status (Section 7)", "| Gate | Status | Evidence |", "|---|---|---|"]
for k in [f"G{i}" for i in range(1, 12)]:
    v = gates.get(k, {}); L.append(f"| {k} | {v.get('status','unknown')} | {v.get('evidence','')} |")
L += ["", "## Last 10 decisions"] + [f"- {t}: {d}" for t, d in items] + [""]
L += ["## Last failures (journal entries)"] + ([f"- journal/ENTRIES/{p.name}" for p in fails] or ["- none yet"]) + [""]
L += [notes]
atomic_write_text(ROOT / "HANDOFF.md", "\n".join(L) + "\n")
print("HANDOFF.md written")
