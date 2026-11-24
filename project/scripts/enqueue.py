#!/usr/bin/env python3
"""Add jobs for an experiment of the current plan to the queue (idempotent: existing ids are kept).
Usage: python scripts/enqueue.py {E0|E1|E2|E3|E0b|E1b|E2b|E3b} [--quick]   (v2 experiments: experiments/plan_v2.yaml)"""
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
    if exp in ("E1", "E2", "E3"):
        fz = read_json(STATE / "frozen_config.json")
        assert fz, "frozen_config.json missing: run scripts/freeze_config.py after E0"
        for p, s in itertools.product(TEST, SC):
            if exp == "E1":
                J += [dict(method="nowait"), dict(method="oracle"),
                      dict(method="wait", W=fz["wait_W"], variant=f"wait_W{fz['wait_W']}"),
                      dict(method="orb", W=fz["orb_W"], variant=f"orb_W{fz['orb_W']}"),
                      dict(method="law", delay_est="lagakos", prior="model", variant="law_lagakos_model")]
            if exp == "E2":
                J += [dict(method="law", delay_est=de, prior=pr, variant=f"law_{de}_{pr}")
                      for de, pr in [("naive", "model"), ("lagakos", "base"), ("naive", "base")]]
            if exp == "E3":
                J += [dict(method="nowait", delay_scale=2.0, variant="nowait_ds2"),
                      dict(method="wait", W=fz["wait_W"], delay_scale=2.0, variant=f"wait_W{fz['wait_W']}_ds2"),
                      dict(method="orb", W=fz["orb_W"], delay_scale=2.0, variant=f"orb_W{fz['orb_W']}_ds2"),
                      dict(method="law", delay_est="lagakos", prior="model", delay_scale=2.0, variant="law_lagakos_model_ds2")]
            J[-(5 if exp == "E1" else 3 if exp == "E2" else 4):] = [dict(j, project=p, seed=s) for j in J[-(5 if exp == "E1" else 3 if exp == "E2" else 4):]]
        for j in J: j.update(experiment=exp, split="test")
        return J, {"E1": 20, "E2": 30, "E3": 40}[exp]
    if exp == "E0b":
        fz = read_json(STATE / "frozen_config.json"); assert fz, "run scripts/freeze_config.py after E0"
        W = fz["wait_W"]
        for p, s in itertools.product(DEV, SE):
            J += [dict(j, project=p, seed=s) for j in v2_family_configs(W)]
        for j in J: j.update(experiment="E0b", split="dev")
        return J, 12
    if exp in ("E1b", "E2b", "E3b"):
        fz = read_json(STATE / "frozen_config.json"); assert fz and "v2" in fz, "run scripts/freeze_config.py --v2 after E0b"
        v2 = fz["v2"]; W, Wo = fz["wait_W"], fz["orb_W"]
        cfg = {f: dict(v2[f]["params"], variant=v2[f]["variant"]) for f in ("LAT", "MAT", "ODaSC", "OOB")}
        for p, s in itertools.product(TEST, SC):
            if exp == "E1b":
                JJ = [dict(method="nowait"), dict(method="oracle"),
                      dict(method="wait", W=W, variant=f"wait_W{W}"), dict(method="orb", W=Wo, variant=f"orb_W{Wo}"),
                      dict(method="law", delay_est="lagakos", prior="model", variant="law_lagakos_model")] + \
                     [dict(cfg[f]) for f in ("LAT", "MAT", "ODaSC", "OOB")]
            if exp == "E2b":
                JJ = [dict(cfg["LAT"], thr_policy="face", variant=cfg["LAT"]["variant"] + "_ABL_face"),
                      dict(cfg["LAT"], delay_est="naive", variant=cfg["LAT"]["variant"] + "_ABL_naive")]
            if exp == "E3b":
                JJ = [dict(method="wait", W=W, variant=f"wait_W{W}"), dict(method="orb", W=Wo, variant=f"orb_W{Wo}")] + \
                     [dict(cfg[f]) for f in ("LAT", "MAT", "ODaSC")]
                JJ = [dict(j, delay_scale=2.0, variant=j["variant"] + "_ds2") for j in JJ]
            J += [dict(j, project=p, seed=s) for j in JJ]
        for j in J: j.update(experiment=exp, split="test")
        return J, {"E1b": 20, "E2b": 30, "E3b": 40}[exp]
    raise SystemExit("unknown experiment")

def v2_family_configs(W):
    """plan_v2 configs_E0b: exactly 5 per family (equal tuning budget)."""
    C = []
    lat = [("nowait", {}, 1000), ("nowait", {}, 2000), ("nowait", {}, 500), ("wait", {"W": W}, 1000),
           ("law", {"prior": "base"}, 1000)]
    for m, extra, win in lat:
        tag = f"{m}{extra.get('W', '')}" if m != "law" else "lawbase"
        C.append(dict(method=m, **extra, thr_policy="latency", thr_window=win, delay_est="lagakos", family="LAT",
                      variant=f"LAT_{tag}_win{win}"))
    for m, extra, age in [("nowait", {}, 90), ("nowait", {}, 180), ("nowait", {}, 365), ("wait", {"W": W}, 90), ("wait", {"W": W}, 180)]:
        C.append(dict(method=m, **extra, thr_policy="mature", thr_window=1000, thr_min_age=age, family="MAT",
                      variant=f"MAT_{m}{extra.get('W', '')}_age{age}"))
    for w_, M, d in [(15, 10, 0.8), (15, 10, 0.9), (15, 20, 0.8), (15, 20, 0.9), (W, 10, 0.9)]:
        C.append(dict(method="odasc", W=w_, M=M, delta=d, theta=0.99, family="ODaSC", variant=f"ODaSC_W{w_}_M{M}_d{d}"))
    for w_, M, th in [(15, 10, 0.99), (15, 20, 0.99), (15, 10, 0.999), (W, 10, 0.99), (W, 20, 0.99)]:
        C.append(dict(method="oob", W=w_, M=M, theta=th, family="OOB", variant=f"OOB_W{w_}_M{M}_th{th}"))
    return C

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
