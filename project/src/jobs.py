"""Job registry: every queue job's `kind` is a function name in this module.
Signature: fn(params: dict, ctx: runner.Ctx) -> None (results via ctx.write_result)."""

def smoke(params, ctx):
    """Infrastructure self-test job."""
    import time
    for i in range(3):
        ctx.heartbeat(f"smoke {i}"); time.sleep(0.2)
    ctx.write_result({"kind": "smoke", "ok": True, "seed": params.get("seed", 0)})

def jit_run(params, ctx):
    """One prequential simulation: params = {experiment, project, method, seed, W, delay_est, prior,
    delay_scale, label_noise_log, variant}. quick=True -> first 3000 commits only."""
    import numpy as np, json
    from .data import load_project
    from .jit import simulate
    df = load_project(params["project"])
    if params.get("quick"):
        df = df.iloc[:3000]
    kw = {k: params[k] for k in ["W", "delay_est", "prior", "delay_scale", "label_noise_log", "thr_cal"] if k in params}
    ctx.heartbeat(f"{params['project']} {params['method']}")
    out = simulate(df, params["method"], seed=params["seed"],
                   eval_end_gap_days=0 if params.get("quick") else 365, **kw)
    row = {"experiment": params["experiment"], "project": params["project"], "method": params["method"],
           "variant": params.get("variant", params["method"]), "seed": params["seed"],
           "split": params.get("split"), **{k: v for k, v in kw.items()}, **out["metrics"]}
    if "diag" in out:
        d = out["diag"]
        for key in ("frac_false_clean", "mean_q_true_bug", "mean_q_clean"):
            vals = [x[key] for x in d if key in x and x[key] == x[key]]
            if vals: row[key + "_mean"] = float(np.mean(vals))
        (ctx.res_dir / "diag").mkdir(exist_ok=True)
        json.dump(d, open(ctx.res_dir / "diag" / f"{ctx.job['id']}.json", "w"))
    ctx.write_result(row)
