"""Leakage test: the training labels used at update time T must not depend on discoveries after T.
We perturb all discovery times that happen after T0 and check that the predictions made before the
first update after T0 are unchanged."""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from src.data import load_project
from src.jit import simulate, survival_from_delays

def test_future_discoveries_do_not_leak():
    df = load_project("fabric").iloc[:3000].copy()
    cut = 1700
    T0 = df.t.iloc[cut]
    df2 = df.copy()
    late = df2.t_found > T0
    df2.loc[late & np.isfinite(df2.t_found), "t_found"] = np.inf        # hide future discoveries
    cases = [(m, {}) for m in ["nowait", "wait", "orb", "law", "awt", "lawm", "odasc"]] + \
            [("lawm", dict(mode="dual", W=30, knn_k=50))]          # Dual denoiser (added after review round 1)
    for m, kw in cases:
        a = simulate(df, m, seed=0, return_preds=True, eval_end_gap_days=0, **kw)
        b = simulate(df2, m, seed=0, return_preds=True, eval_end_gap_days=0, **kw)
        assert np.allclose(np.nan_to_num(a["prob"][:cut]), np.nan_to_num(b["prob"][:cut])), (m, kw)
        assert np.array_equal(a["pred"][:cut], b["pred"][:cut]), (m, kw)   # decisions, not only scores

def test_final_labels_of_undiscovered_commits_do_not_leak():
    """R1 review: a policy that read the final y of commits still undiscovered at T0 would pass the t_found test.
    Flip y for every commit whose defect is not discovered by T0 (making some clean commits 'buggy, never found'
    and hiding the bugs) and check that no decision before T0 changes. Oracle/decomp use y by design and are excluded."""
    for proj in ["fabric", "aj_kafka"]:
        df = load_project(proj).iloc[:3000].copy(); cut = 1700; T0 = df.t.iloc[cut]
        df2 = df.copy(); und = ~(df2.t_found <= T0)
        df2.loc[und, "y"] = 1 - df2.loc[und, "y"]; df2.loc[und, "t_found"] = np.inf
        df.loc[und, "t_found"] = np.inf                                   # same observable history in both copies
        cases = [(m, {}) for m in ["nowait", "wait", "orb", "law", "awt", "lawm", "odasc"]] + [("lawm", dict(mode="dual", W=30, knn_k=50))]
        for m, kw in cases:
            a = simulate(df, m, seed=0, return_preds=True, eval_end_gap_days=0, **kw)
            b = simulate(df2, m, seed=0, return_preds=True, eval_end_gap_days=0, **kw)
            assert np.array_equal(a["pred"][:cut], b["pred"][:cut]), (proj, m, kw)

def test_lagakos_recovers_truncated_exponential():
    rng = np.random.default_rng(0); tc = rng.uniform(0, 1000, 20000); d = rng.exponential(200, 20000)
    obs = tc + d <= 1000; grid = np.array([50, 100, 200])
    S = survival_from_delays(d[obs], 1000 - tc[obs], grid, "lagakos")
    true = (np.exp(-grid / 200) - np.exp(-5)) / (1 - np.exp(-5))
    assert np.max(np.abs(S - true)) < 0.02

if __name__ == "__main__":
    test_lagakos_recovers_truncated_exponential(); test_future_discoveries_do_not_leak(); test_final_labels_of_undiscovered_commits_do_not_leak(); print("tests passed")
