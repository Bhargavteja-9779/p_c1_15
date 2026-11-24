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
    for m in ["nowait", "wait", "orb", "law", "awt"]:
        a = simulate(df, m, seed=0, return_preds=True, eval_end_gap_days=0)
        b = simulate(df2, m, seed=0, return_preds=True, eval_end_gap_days=0)
        assert np.allclose(np.nan_to_num(a["prob"][:cut]), np.nan_to_num(b["prob"][:cut])), m

def test_lagakos_recovers_truncated_exponential():
    rng = np.random.default_rng(0); tc = rng.uniform(0, 1000, 20000); d = rng.exponential(200, 20000)
    obs = tc + d <= 1000; grid = np.array([50, 100, 200])
    S = survival_from_delays(d[obs], 1000 - tc[obs], grid, "lagakos")
    true = (np.exp(-grid / 200) - np.exp(-5)) / (1 - np.exp(-5))
    assert np.max(np.abs(S - true)) < 0.02

if __name__ == "__main__":
    test_lagakos_recovers_truncated_exponential(); test_future_discoveries_do_not_leak(); print("tests passed")
