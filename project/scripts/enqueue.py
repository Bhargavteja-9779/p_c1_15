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

def variant_params(v):
    """Inverse of the variant naming used in E0/E0b/E0c. Suffix '|ds2' = delay_scale 2 (robustness)."""
    import re
    ds = v.endswith("|ds2"); base = v.replace("|ds2", "")
    d = {"variant": base + ("_ds2" if ds else "")}
    if ds: d["delay_scale"] = 2.0
    b = base
    if b.endswith("_calnaive"): d["thr_cal"] = "naive"; b = b[:-9]
    elif b.endswith("_cal"): d["thr_cal"] = "lat"; b = b[:-4]
    m = re.match(r"^(wait|orb|fsc)_W(\d+)(?:_fr(\d+))?$", b)
    if m:
        d.update(method=m.group(1), W=int(m.group(2)))
        if m.group(3): d["fixed_rate"] = int(m.group(3)) / 100
    elif b.startswith("law_"):
        _, de, pr = b.split("_"); d.update(method="law", delay_est=de, prior=pr)
    elif b in ("nowait", "oracle"):
        d["method"] = b
    else:
        raise ValueError(v)
    return d

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
    if exp == "E0b":
        for p, s in itertools.product(DEV, SE):
            J += [dict(method="nowait", thr_cal="lat", variant="nowait_cal"),
                  dict(method="nowait", thr_cal="naive", variant="nowait_calnaive"),
                  dict(method="law", delay_est="lagakos", prior="model", thr_cal="naive", variant="law_lagakos_model_calnaive")]
            for W in WGRID:
                J += [dict(method="wait", W=W, thr_cal="lat", variant=f"wait_W{W}_cal"),
                      dict(method="orb", W=W, thr_cal="lat", variant=f"orb_W{W}_cal"),
                      dict(method="fsc", W=W, variant=f"fsc_W{W}"),
                      dict(method="fsc", W=W, thr_cal="lat", variant=f"fsc_W{W}_cal")]
            for de, pr in [("lagakos", "model"), ("naive", "model"), ("lagakos", "base"), ("naive", "base")]:
                J.append(dict(method="law", delay_est=de, prior=pr, thr_cal="lat", variant=f"law_{de}_{pr}_cal"))
            J = [dict(j, project=p, seed=s) if "project" not in j else j for j in J]
        for j in J: j.update(experiment="E0b", split="dev")
        return J, 12
    if exp == "E0c":   # fixed defect-prediction-rate baseline (Pessoa 2021), plan_v3
        for p, s in itertools.product(DEV, SE):
            for W in WGRID:
                for fr in [0.2, 0.3, 0.4, 0.5, 0.6]:
                    J.append(dict(method="wait", W=W, fixed_rate=fr, variant=f"wait_W{W}_fr{int(fr*100)}", project=p, seed=s))
        for j in J: j.update(experiment="E0c", split="dev")
        return J, 13
    if exp in ("E1v3", "E2v3", "E3v3"):   # plan_v2/v3 test-project experiments (frozen_config_v3.json)
        fz = read_json(STATE / "frozen_config_v3.json"); assert fz, "run scripts/freeze_config_v3.py first"
        sel = fz["selected"]
        if exp == "E1v3":
            V = ["nowait", "oracle", fz["proposed"]] + [sel[k] for k in ("wait", "orb", "fsc", "fr", "wait_cal", "fsc_cal") if k in sel]
        elif exp == "E2v3":
            V = ["law_lagakos_model", "law_lagakos_model_calnaive", "nowait_cal", "law_naive_model_cal", "law_lagakos_base_cal"]
        else:
            V = [v + "|ds2" for v in [fz["proposed"]] + [sel[k] for k in ("wait", "fsc", "fr", "wait_cal") if k in sel]]
        V = list(dict.fromkeys(V))
        for p, s in itertools.product(TEST, SC):
            for v in V:
                J.append(dict(variant_params(v), project=p, seed=s, experiment=exp, split="test"))
        return J, {"E1v3": 20, "E2v3": 30, "E3v3": 40}[exp]
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
    raise SystemExit("unknown experiment")

if __name__ == "__main__":
    exp = sys.argv[1]; quick = "--quick" in sys.argv
    J, prio = specs(exp)
    qf = STATE / ("queue_quick.json" if quick else "queue.json")
    from src.runner import qlock
    _ql = qlock("quick" if quick else "full"); _ql.__enter__()
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
    write_json(qf, q); _ql.__exit__(None, None, None); print(f"added {added} jobs to {qf.name} (total {len(q['jobs'])})")
