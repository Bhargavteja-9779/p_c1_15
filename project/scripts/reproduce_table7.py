#!/usr/bin/env python3
"""Re-run the independent lineage's frozen RQ5 configurations (Table 7) on the 10 Cabral test projects with that
lineage's simulator (archive/zealous_lamport_cycle1/src/jit.py) and the shared data loader.
Usage: python scripts/reproduce_table7.py [project] [seed]   (default: all 10 projects x seeds 100-104; ~3 CPU-h)
Writes results/reproduce_table7.jsonl and prints the comparison with the archived raw results."""
import sys, os, json, importlib.util, pandas as pd
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")); sys.path.insert(0, ROOT)
from src.data import load_project
spec = importlib.util.spec_from_file_location("jit2", os.path.join(ROOT, "archive", "zealous_lamport_cycle1", "src", "jit.py"))
jit2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(jit2)
fz = json.load(open(os.path.join(ROOT, "archive", "zealous_lamport_cycle1", "state", "frozen_config.json")))
CFG = [fz["proposed"]] + fz["baselines"] + [fz["oracle"]]
TEST = ["brackets", "broadleaf", "camel", "jgroups", "matplotlib", "npm", "spring-integration", "tomcat", "wagtail", "zulip"]
projects = [sys.argv[1]] if len(sys.argv) > 1 else TEST
seeds = [int(sys.argv[2])] if len(sys.argv) > 2 else [100, 101, 102, 103, 104]
arch = pd.read_json(os.path.join(ROOT, "archive", "zealous_lamport_cycle1", "results", "raw_results.jsonl"), lines=True)
out = open(os.path.join(ROOT, "results", "reproduce_table7.jsonl"), "a")
for p in projects:
    df = load_project(p)
    for s in seeds:
        for c in CFG:
            kw = {k: v for k, v in c.items() if k not in ("variant", "method")}
            m = jit2.simulate(df, c["method"], seed=s, **kw)["metrics"]
            ref = arch[(arch.experiment == "E1") & (arch.project == p) & (arch.variant == c["variant"]) & (arch.seed == s)].gmean
            out.write(json.dumps(dict(project=p, seed=s, variant=c["variant"], gmean=m["gmean"], archived=float(ref.iloc[0]) if len(ref) else None)) + "\n"); out.flush()
            print(p, s, c["variant"], round(m["gmean"], 4), "archived:", round(float(ref.iloc[0]), 4) if len(ref) else None, flush=True)
