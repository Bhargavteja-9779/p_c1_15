"""Leakage test for the two time-T threshold rules (ratematch, gmax_lat) of the independent analysis lineage
(archive/zealous_lamport_cycle1/src/jit.py, used for RQ5): hiding every discovery after T0 must not change
any decision made before T0. Imports that lineage's simulator by path; data loading is shared."""
import sys, os, importlib.util, numpy as np
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, ROOT)
from src.data import load_project
spec = importlib.util.spec_from_file_location("jit_lineage2", os.path.join(ROOT, "archive", "zealous_lamport_cycle1", "src", "jit.py"))
jit2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(jit2)

def test_threshold_rules_do_not_leak():
    df = load_project("fabric").iloc[:3000].copy(); cut = 1700; T0 = df.t.iloc[cut]
    df2 = df.copy(); late = (df2.t_found > T0) & np.isfinite(df2.t_found); df2.loc[late, "t_found"] = np.inf
    for m, kw in [("nowait", {}), ("law", dict(delay_est="lagakos", prior="model")), ("wait", dict(W=30))]:
        for pol in ["ratematch", "gmax_lat"]:
            a = jit2.simulate(df, m, seed=0, return_preds=True, eval_end_gap_days=0, thr_policy=pol, **kw)
            b = jit2.simulate(df2, m, seed=0, return_preds=True, eval_end_gap_days=0, thr_policy=pol, **kw)
            assert np.array_equal(a["pred"][:cut], b["pred"][:cut]), (m, pol)

if __name__ == "__main__":
    test_threshold_rules_do_not_leak(); print("threshold-rule leakage tests passed")
