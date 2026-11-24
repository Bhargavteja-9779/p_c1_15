#!/usr/bin/env python3
"""Add jobs for an experiment of the current plan to the queue (idempotent: existing ids are kept).
Usage: python scripts/enqueue.py E0 [--quick]"""
import sys, os, itertools, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from src.state import STATE, read_json, write_json
DEV = ["fabric", "neutron", "nova", "sentry"]
TEST = ["brackets", "broadleaf", "camel", "jgroups", "matplotlib", "npm", "spring-integration", "tomcat", "wagtail", "zulip"]
SE, SC = [0, 1, 2], [100, 101, 102, 103, 104]
WGRID = [15, 30, 60, 90, 180]

def _cand(fz):
    """plan_v2 candidate chosen on dev by scripts/freeze_config.py (law_* or awt_*)."""
    c = fz["candidate"]
    if c.startswith("awt_e"):
        return dict(method="awt", eps=float(c[5:]), delay_est="lagakos", label_noise_log=True, variant=c)
    _, de, pr = c.split("_")
    return dict(method="law", delay_est=de, prior=pr, variant=c + "_cand")

def specs(exp):
    J = []
    if exp == "E0":
        for p, s in itertools.product(DEV, SE):
            J += [dict(method="nowait"), dict(method="oracle")]
            J[-2:] = [dict(j, project=p, seed=s) for j in J[-2:]]
            for W in WGRID:
                J.append(dict(method="wait", W=W, variant=f"wait_W{W}", project=p, seed=s))
                J.append(dict(method="orb", W=W, variant=f"orb_W{W}", project=p, seed=s))
            for de, pr in [("lagakos", "model"), ("naive", "model"), ("lagakos", "base"), ("naive", "base")]:
                J.append(dict(method="law", delay_est=de, prior=pr, variant=f"law_{de}_{pr}", project=p, seed=s))
        for j in J: j.update(experiment="E0", split="dev")
        return J, 10
    if exp == "E0b":   # plan_v2 dev diagnostics
        for p, s in itertools.product(DEV, SE):
            for eps in [0.2, 0.3, 0.4, 0.5]:
                J.append(dict(method="awt", eps=eps, delay_est="lagakos", label_noise_log=True, variant=f"awt_e{eps}", project=p, seed=s))
            for W in [30, 90]:
                for lv in [1, 2]:
                    J.append(dict(method="decomp", W=W, level=lv, variant=f"decomp_L{lv}_W{W}", project=p, seed=s))
        for j in J: j.update(experiment="E0b", split="dev")
        return J, 11
    if exp == "E3b":   # plan_v3 decomposition on test projects (pre-registered)
        for p, s in itertools.product(TEST, SC):
            for W in [30, 90]:
                J.append(dict(method="wait", W=W, variant=f"wait_W{W}", project=p, seed=s))
                for lv in [1, 2]:
                    J.append(dict(method="decomp", W=W, level=lv, variant=f"decomp_L{lv}_W{W}", project=p, seed=s))
        for j in J: j.update(experiment="E3b", split="test")
        return J, 25
    if exp in ("E1", "E2", "E3"):
        fz = read_json(STATE / "frozen_config.json")
        assert fz, "frozen_config.json missing: run scripts/freeze_config.py after E0"
        for p, s in itertools.product(TEST, SC):
            if exp == "E1":
                J += [dict(method="nowait"), dict(method="oracle"),
                      dict(method="wait", W=fz["wait_W"], variant=f"wait_W{fz['wait_W']}"),
                      dict(method="orb", W=fz["orb_W"], variant=f"orb_W{fz['orb_W']}"),
                      dict(method="law", delay_est="lagakos", prior="model", variant="law_lagakos_model"),
                      _cand(fz)]
            if exp == "E2":
                J += [dict(method="law", delay_est=de, prior=pr, variant=f"law_{de}_{pr}")
                      for de, pr in [("naive", "model"), ("lagakos", "base"), ("naive", "base")]]
            if exp == "E3":
                J += [dict(method="nowait", delay_scale=2.0, variant="nowait_ds2"),
                      dict(method="wait", W=fz["wait_W"], delay_scale=2.0, variant=f"wait_W{fz['wait_W']}_ds2"),
                      dict(method="orb", W=fz["orb_W"], delay_scale=2.0, variant=f"orb_W{fz['orb_W']}_ds2"),
                      dict(method="law", delay_est="lagakos", prior="model", delay_scale=2.0, variant="law_lagakos_model_ds2")]
            J[-(6 if exp == "E1" else 3 if exp == "E2" else 4):] = [dict(j, project=p, seed=s) for j in J[-(6 if exp == "E1" else 3 if exp == "E2" else 4):]]
        for j in J: j.update(experiment=exp, split="test")
        return J, {"E1": 20, "E2": 30, "E3": 40}[exp]
    raise SystemExit("unknown experiment")

if __name__ == "__main__":
    exp = sys.argv[1]; quick = "--quick" in sys.argv
    J, prio = specs(exp)
    qf = STATE / ("queue_quick.json" if quick else "queue.json")
    q = read_json(qf, {"jobs": []}); have = {j["id"] for j in q["jobs"]}
    st = read_json(STATE / "agent_state.json", {})
    if quick:  # one job per method/variant on one project
        seen, JJ = set(), []
        for j in J:
            if j.get("variant", j["method"]) not in seen and j["seed"] in (0, 100):
                seen.add(j.get("variant", j["method"])); JJ.append(j)
        J = JJ
    added = 0
    for j in J:
        jid = f"{j['experiment']}_{j['project']}_{j.get('variant', j['method'])}_s{j['seed']}" + ("_quick" if quick else "")
        if jid in have: continue
        q["jobs"].append({"id": jid, "kind": "jit_run", "params": j, "status": "pending", "attempts": 0,
                          "cycle": st.get("cycle", 1), "priority": prio + (1 if j["project"] == "nova" else 0)})
        added += 1
    write_json(qf, q); print(f"added {added} jobs to {qf.name} (total {len(q['jobs'])})")
