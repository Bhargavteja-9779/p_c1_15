"""Prequential (test-then-train) simulation of online JIT-SDP with verification latency.

At each update time T (every `update_every` commits) the learner is retrained on the commits made
before T, with the labels *observable at T*:
  observed positive  : y=1 and t_found <= T
  provisionally clean: everything else (true clean, or a defect not yet discovered)
Predictions for commits made in [T, T_next) are made at commit time and scored against the
FINAL dataset label y.

Label policies (`method`):
  oracle    : true labels immediately (upper bound, not a competitor)
  nowait    : all commits, observed labels at face value
  wait      : positives as soon as found; clean only after W days (Cabral et al. 2019 framework)
  orb       : 'wait' + ORB-style class-weight boosting from the moving average of predictions
  law       : latency-aware weighting (proposed): every provisionally-clean commit of age a is split
              into a positive copy with weight q and a negative copy with weight 1-q, where
              q = p S(a) / (1 - p + p S(a)), S(a)=P(not yet discovered at age a | defect-inducing),
              estimated from discovery delays observed before T; p = the previous model's
              (de-weighted) probability.  Options: delay_est in {lagakos, naive}, prior in {model, base}.
"""
import time, numpy as np, pandas as pd
import lightgbm as lgb
from sklearn.metrics import roc_auc_score, matthews_corrcoef

DAY = 86400.0
FEATS = ["fix", "ns", "nd", "nf", "entrophy", "la", "ld", "lt", "ndev", "age", "nuc", "exp", "rexp", "sexp"]

LGB_PARAMS = dict(n_estimators=150, learning_rate=0.05, num_leaves=31, min_child_samples=20,
                  subsample=0.8, subsample_freq=1, colsample_bytree=0.8, verbose=-1, n_jobs=1)

# ------------------------------------------------------------------ delay distribution estimators
def survival_from_delays(delays, trunc, grid, method="lagakos", min_risk=10):
    """Return S(a) = P(D > a | D <= horizon) on `grid` (days) for defect-inducing commits.
    delays: observed discovery delays (days) of defects found before T.
    trunc : their truncation times tau_i = T - t_commit (days); a delay is observable iff d <= tau.
    lagakos: reverse-time product-limit estimator for right-truncated data (Lagakos et al. 1988).
    naive  : empirical CDF of observed delays (ignores truncation -> biased to short delays)."""
    delays = np.asarray(delays, float)
    if len(delays) < 5:
        return np.zeros_like(grid, dtype=float)  # no information: treat everything old enough as clean
    if method == "naive":
        d = np.sort(delays)
        return 1.0 - np.searchsorted(d, grid, side="right") / len(d)
    trunc = np.asarray(trunc, float)
    s = np.unique(delays)[::-1]                        # distinct delays, descending
    m = np.array([np.sum(delays == sj) for sj in s])
    R = np.array([np.sum((delays <= sj) & (trunc >= sj)) for sj in s])   # reverse-time risk set
    fac = np.where((R >= min_risk) & (R > m), 1.0 - m / np.maximum(R, 1), 1.0)
    cum = np.concatenate([[1.0], np.cumprod(fac)])      # cum[k] = prod over the k largest delays
    idx = np.searchsorted(-s, -np.asarray(grid, float), side="left")   # number of s_j > a
    Ga = cum[idx]
    return np.clip(1.0 - Ga, 0.0, 1.0)

# ------------------------------------------------------------------ ORB boosting factors
def orb_factors(ma, th=0.4, m=1.5, l0=10, l1=12):
    if ma > th:
        f0 = (m ** ((ma - th) / (1 - th)) - 1) / (m - 1) * l0 + 1; f1 = 1.0
    else:
        f1 = (m ** ((th - ma) / th) - 1) / (m - 1) * l1 + 1; f0 = 1.0
    return f0, f1

# ------------------------------------------------------------------ core simulation
def fit_lgb(X, y, w, seed, class_mult=(1.0, 1.0)):
    """Class-balanced weighted LightGBM. Returns (model, odds_correction) where multiplying the
    model's odds by odds_correction undoes the class re-weighting (for calibrated p)."""
    pos = np.sum(w * y); neg = np.sum(w * (1 - y))
    if pos < 3 or neg < 3:
        return None, 1.0
    cw1, cw0 = (pos + neg) / (2 * pos) * class_mult[1], (pos + neg) / (2 * neg) * class_mult[0]
    ww = w * np.where(y == 1, cw1, cw0)
    m = lgb.LGBMClassifier(**LGB_PARAMS, random_state=seed)
    m.fit(X, y, sample_weight=ww)
    return m, cw0 / cw1

def simulate(df, method, seed=0, W=90, update_every=100, warmup=500, delay_est="lagakos",
             prior="model", orb_params=None, eval_end_gap_days=365, delay_scale=1.0, return_preds=False,
             label_noise_log=False, eps=0.3, level=1):
    """df: one project's commits sorted by time (columns FEATS, t, y, t_found).
    delay_scale>1 stretches discovery delays (robustness: slower bug discovery)."""
    t0 = time.time()
    df = df.reset_index(drop=True)
    X = np.log1p(np.clip(df[FEATS].to_numpy(float), 0, None))
    t = df["t"].to_numpy(float); y = df["y"].to_numpy(int)
    tf = df["t_found"].to_numpy(float)
    if delay_scale != 1.0:
        fin = np.isfinite(tf); tf = tf.copy(); tf[fin] = t[fin] + (tf[fin] - t[fin]) * delay_scale
    n = len(df)
    prob = np.full(n, np.nan); pred = np.full(n, -1)
    model, oc = None, 1.0
    recent_preds = []; diag = []
    for start in range(warmup, n, update_every):
        T = t[start]; cmult = (1.0, 1.0)
        tr = np.where(t < T)[0]
        found = tf[tr] <= T
        age = (T - t[tr]) / DAY
        if method == "oracle":
            Xi, yi, wi = X[tr], y[tr], np.ones(len(tr))
        elif method == "nowait":
            Xi, yi, wi = X[tr], found.astype(int), np.ones(len(tr))
        elif method in ("wait", "orb"):
            keep = found | (age >= W)
            Xi, yi, wi = X[tr][keep], found[keep].astype(int), np.ones(keep.sum())
            if method == "orb" and len(recent_preds) >= 10:
                cmult = orb_factors(np.mean(recent_preds[-100:]), **(orb_params or {}))
        elif method == "awt":
            # adaptive waiting time (plan_v2): W_T = smallest age a with S_T(a) <= eps, S_T from the
            # truncation-corrected delay estimate on discoveries observed before T (no future info)
            pos_idx = tr[found]
            d_obs = (tf[pos_idx] - t[pos_idx]) / DAY; tau = (T - t[pos_idx]) / DAY
            grid = np.arange(1, 731, 1.0)
            Sg = survival_from_delays(d_obs, tau, grid, method=delay_est)
            below = np.where(Sg <= eps)[0]
            W_T = grid[below[0]] if (len(d_obs) >= 5 and len(below)) else 90.0
            keep = found | (age >= W_T)
            Xi, yi, wi = X[tr][keep], found[keep].astype(int), np.ones(keep.sum())
            if label_noise_log: diag.append(dict(T=T, W_T=float(W_T)))
        elif method == "decomp":
            # DIAGNOSTIC ONLY (uses true labels -> not a competitor). Decomposes the wait->oracle gap:
            # level 1: same examples as wait(W) but true labels (pure denoising)
            # level 2: level 1 + young not-yet-found true bugs (adds fresh positives)
            # oracle  : level 2 + young clean commits
            keep = found | (age >= W)
            if level >= 2: keep = keep | (y[tr] == 1)
            Xi, yi, wi = X[tr][keep], y[tr][keep], np.ones(keep.sum())
        elif method == "law":
            pos_idx = tr[found]
            d_obs = (tf[pos_idx] - t[pos_idx]) / DAY; tau = (T - t[pos_idx]) / DAY
            unl = ~found
            S = survival_from_delays(d_obs, tau, age[unl], method=delay_est)
            if prior == "model" and model is not None:
                p_raw = model.predict_proba(X[tr][unl])[:, 1]
                odds = p_raw / np.clip(1 - p_raw, 1e-6, None) * oc
                p = odds / (1 + odds)
            else:
                mature = age >= 365
                p = np.full(unl.sum(), found[mature].mean() if mature.sum() > 50 else found.mean())
            q = p * S / np.clip(1 - p + p * S, 1e-9, None)
            Xi = np.vstack([X[tr][found], X[tr][unl], X[tr][unl]])
            yi = np.concatenate([np.ones(found.sum()), np.ones(unl.sum()), np.zeros(unl.sum())]).astype(int)
            wi = np.concatenate([np.ones(found.sum()), q, 1 - q])
            keepw = wi > 1e-4
            Xi, yi, wi = Xi[keepw], yi[keepw], wi[keepw]
            if label_noise_log:
                diag.append(dict(T=T, mean_q_true_bug=float(q[y[tr][unl] == 1].mean()) if (y[tr][unl] == 1).any() else np.nan,
                                 mean_q_clean=float(q[y[tr][unl] == 0].mean())))
        else:
            raise ValueError(method)
        if label_noise_log and method in ("nowait", "wait", "orb"):
            truth = y[tr] if method == "nowait" else y[tr][found | (age >= W)]
            diag.append(dict(T=T, n_train=len(yi), frac_false_clean=float(np.mean((yi == 0) & (truth == 1)) / max(np.mean(yi == 0), 1e-9))))
        m_new, oc_new = fit_lgb(Xi, yi, wi, seed, cmult)
        if m_new is not None:
            model, oc = m_new, oc_new
        end = min(start + update_every, n)
        if model is not None:
            pr = model.predict_proba(X[start:end])[:, 1]
            prob[start:end] = pr; pred[start:end] = (pr >= 0.5).astype(int)
            recent_preds.extend(pred[start:end].tolist())
    # evaluation window
    ev = (pred >= 0) & (t <= t.max() - eval_end_gap_days * DAY)
    res = evaluate(y[ev], pred[ev], prob[ev])
    res.update(n_eval=int(ev.sum()), seconds=round(time.time() - t0, 2))
    out = {"metrics": res}
    if return_preds: out.update(pred=pred, prob=prob, eval_mask=ev)
    if diag: out["diag"] = diag
    return out

def evaluate(y, pred, prob):
    r1 = float(np.mean(pred[y == 1] == 1)) if (y == 1).any() else np.nan
    r0 = float(np.mean(pred[y == 0] == 0)) if (y == 0).any() else np.nan
    return dict(gmean=float(np.sqrt(r0 * r1)), r0=r0, r1=r1, rdiff=abs(r0 - r1),
                auc=float(roc_auc_score(y, prob)) if len(np.unique(y)) > 1 else np.nan,
                mcc=float(matthews_corrcoef(y, pred)))
