#!/usr/bin/env python3
"""plan_v8 (review round 1) runs A2-A5. Idempotent: results appended to results/review1/raw.jsonl, done ids skipped.
Usage: python scripts/review1_runs.py [n_procs]"""
import sys, os, json, time, itertools, importlib.util
from multiprocessing import Pool
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, ROOT)
OUT = os.path.join(ROOT, "results", "review1", "raw.jsonl")
TEST = ["brackets", "broadleaf", "camel", "jgroups", "matplotlib", "npm", "spring-integration", "tomcat", "wagtail", "zulip"]
AJ = ["aj_activemq", "aj_cassandra", "aj_flink", "aj_groovy", "aj_hadoop-hdfs", "aj_hbase", "aj_hive", "aj_ignite", "aj_kafka"]
SC = [100, 101, 102, 103, 104]
INF = 1e9

def jobs():
    J = []
    for p, s in itertools.product(AJ, SC):                                   # A2
        for lv in (1, 2):
            J.append(dict(a="A2", sim="main", project=p, seed=s, method="decomp", kw=dict(W=90, level=lv), variant=f"decomp_L{lv}_W90"))
    for p, s in itertools.product(TEST + AJ, SC):                            # A3
        for lo, hi in [(30, 180), (180, 365), (365, 730), (730, INF)]:
            J.append(dict(a="A3", sim="main", project=p, seed=s, method="decomp", kw=dict(W=30, level="strata", strata_lo=lo, strata_hi=hi),
                          variant=f"strata_{lo}_{'inf' if hi == INF else hi}"))
    for p, s in itertools.product(TEST + AJ, SC[:2]):                        # A4
        for v, m, kw in [("wait_W30", "wait", dict(W=30)), ("decomp_L1_W30", "decomp", dict(W=30, level=1)), ("wait_W90", "wait", dict(W=90)),
                         ("nowait", "nowait", {}), ("oracle", "oracle", {})]:
            J.append(dict(a="A4", sim="main", project=p, seed=s, method=m, kw=dict(kw, eval_end_gap_days=730), variant=v + "_gap730"))
    for p, s in itertools.product(AJ, SC):                                   # A5 (lineage-2 simulator)
        for v, m, kw in [("nowait", "nowait", {}), ("wait_W30", "wait", dict(W=30)), ("wait_W90", "wait", dict(W=90)),
                         ("law_lagakos_model", "law", dict(delay_est="lagakos", prior="model")),
                         ("odasc_W30_d09_k50", "odasc", dict(W=30, odasc_delta=0.9, odasc_k=50))]:
            for thr in ("fixed", "gmax_lat"):
                J.append(dict(a="A5", sim="lineage2", project=p, seed=s, method=m, kw=dict(kw, thr_policy=thr),
                              variant=v + ("" if thr == "fixed" else "_gmax_lat")))
    for j in J: j["id"] = f"{j['a']}_{j['project']}_{j['variant']}_s{j['seed']}"
    return J

_sim = {}
def run(j):
    from src.data import load_project
    if j["sim"] not in _sim:
        if j["sim"] == "main":
            from src.jit import simulate; _sim["main"] = simulate
        else:
            spec = importlib.util.spec_from_file_location("jit2", os.path.join(ROOT, "archive", "zealous_lamport_cycle1", "src", "jit.py"))
            m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); _sim["lineage2"] = m.simulate
    t0 = time.time()
    out = _sim[j["sim"]](load_project(j["project"]), j["method"], seed=j["seed"], **j["kw"])
    row = dict(id=j["id"], analysis=j["a"], project=j["project"], variant=j["variant"], seed=j["seed"], simulator=j["sim"],
               **{k: v for k, v in j["kw"].items() if not isinstance(v, float) or v < INF}, **out["metrics"], wall=round(time.time() - t0, 1))
    return row

if __name__ == "__main__":
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    done = set()
    if os.path.exists(OUT):
        for l in open(OUT):
            try: done.add(json.loads(l)["id"])
            except Exception: pass
    todo = [j for j in jobs() if j["id"] not in done]
    todo.sort(key=lambda j: {"A5": 0, "A2": 1, "A3": 2, "A4": 3}[j["a"]])    # confirmatory first
    print(f"{len(done)} done, {len(todo)} to run", flush=True)
    with Pool(int(sys.argv[1]) if len(sys.argv) > 1 else 3) as pool, open(OUT, "a") as f:
        for i, row in enumerate(pool.imap_unordered(run, todo, chunksize=1)):
            f.write(json.dumps(row, default=float) + "\n"); f.flush()
            if i % 25 == 0: print(f"[{time.strftime('%H:%M:%S')}] {i+1}/{len(todo)} {row['id']}", flush=True)
    print("all done", flush=True)
