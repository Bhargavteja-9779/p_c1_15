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
    if exp == "E0b":   # plan_v2: ODaSC-style baseline, same 5-config budget (W grid, delta=0.9)
        for p, s in itertools.product(DEV, SE):
            for W in WGRID:
                J.append(dict(method="odasc", W=W, odasc_delta=0.9, variant=f"odasc_W{W}", project=p, seed=s))
        for j in J: j.update(experiment="E0", split="dev")
        return J, 11
    if exp == "E0c":   # 6.4 ladder (H2/H3): threshold policies, dev only; baselines get the same option
        for p, s in itertools.product(DEV, SE):
            for pol in ["ratematch", "gmax_lat"]:
                J.append(dict(method="nowait", thr_policy=pol, variant=f"nowait_{pol}", project=p, seed=s))
                for de in ["lagakos", "naive"]:
                    J.append(dict(method="law", delay_est=de, prior="base", thr_policy=pol, variant=f"law_{de}_base_{pol}", project=p, seed=s))
            for de in ["lagakos", "naive"]:   # added 2026-11-25 after E0: LAW-model has best dev AUC but broken operating point
                J.append(dict(method="law", delay_est=de, prior="model", thr_policy="gmax_lat", variant=f"law_{de}_model_gmax_lat", project=p, seed=s))
            for W in WGRID:
                for m, extra in [("wait", {}), ("orb", {}), ("odasc", {"odasc_delta": 0.9})]:
                    J.append(dict(method=m, W=W, thr_policy="gmax_lat", variant=f"{m}_W{W}_gmax_lat", project=p, seed=s, **extra))
        for j in J: j.update(experiment="E0", split="dev")
        return J, 12
    if exp in ("E1", "E2", "E3"):   # plan_v3: everything comes from state/frozen_config.json
        fz = read_json(STATE / "frozen_config.json")
        assert fz and fz.get("plan") == "plan_v3", "frozen_config.json (plan_v3) missing"
        P = fz["proposed"]
        if exp == "E1":
            cfgs = [P] + fz["baselines"] + [fz["oracle"]]
        elif exp == "E2":
            cfgs = [dict(variant="law_lagakos_model", method="law", delay_est="lagakos", prior="model"),
                    dict(variant="law_naive_model_gmax_lat", method="law", delay_est="naive", prior="model", thr_policy="gmax_lat"),
                    dict(variant="law_lagakos_base_gmax_lat", method="law", delay_est="lagakos", prior="base", thr_policy="gmax_lat"),
                    dict(variant="nowait_gmax_lat", method="nowait", thr_policy="gmax_lat")]
        else:
            keep = {P["variant"], "odasc_W30", "wait_W90", "odasc_W15_gmax_lat"}
            cfgs = [dict(c, delay_scale=2.0, variant=c["variant"] + "_ds2") for c in [P] + fz["baselines"] if c["variant"] in keep]
        for p, s in itertools.product(TEST, SC):
            for c in cfgs:
                J.append(dict(c, project=p, seed=s))
        for j in J: j.update(experiment=exp, split="test")
        return J, {"E1": 20, "E2": 30, "E3": 40}[exp]
    raise SystemExit("unknown experiment")

if __name__ == "__main__":
    exp = sys.argv[1]; quick = "--quick" in sys.argv
    J, prio = specs(exp)
    qf = STATE / ("queue_quick.json" if quick else "queue.json")
    from src.runner import qlock
    _lk = qlock("quick" if quick else "full"); _lk.__enter__()     # never race the running workers
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
    write_json(qf, q); _lk.__exit__(None, None, None); print(f"added {added} jobs to {qf.name} (total {len(q['jobs'])})")
