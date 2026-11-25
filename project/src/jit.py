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
  odasc     : ODaSC-style baseline (Song, Li, Minku & Yao, IJCNN 2022), batch adaptation: 'wait' labels;
              when a commit is labelled clean (age >= W) its class-0 confidence alpha0 is computed once
              from the labels of its k nearest recent labelled commits (stand-in for DenStream
              micro-clusters); if alpha0 < delta it is counted as both class 0 and class 1.
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
             label_noise_log=False, odasc_delta=0.9, odasc_k=50, odasc_pool=5000, thr_policy="fixed", thr_window=2000, oracle_H=180):
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
    alpha0 = np.full(n, np.nan)  # odasc: class-0 label confidence, fixed when a commit is labelled clean
    for start in range(warmup, n, update_every):
        T = t[start]; cmult = (1.0, 1.0)
        tr = np.where(t < T)[0]
        found = tf[tr] <= T
        age = (T - t[tr]) / DAY
        if method == "oracle":
            Xi, yi, wi = X[tr], y[tr], np.ones(len(tr))
        elif method in ("oracle_young", "oracle_old"):
            # diagnostic partial oracles: true labels only for commits younger (older) than H days
            H = oracle_H
            young = age < H
            reveal = young if method == "oracle_young" else ~young
            Xi, yi, wi = X[tr], np.where(reveal, y[tr], found.astype(int)), np.ones(len(tr))
        elif method == "nowait":
            Xi, yi, wi = X[tr], found.astype(int), np.ones(len(tr))
        elif method in ("wait", "orb"):
            keep = found | (age >= W)
            Xi, yi, wi = X[tr][keep], found[keep].astype(int), np.ones(keep.sum())
            if method == "orb" and len(recent_preds) >= 10:
                cmult = orb_factors(np.mean(recent_preds[-100:]), **(orb_params or {}))
        elif method == "odasc":
            keep = found | (age >= W)
            Xi, yi = X[tr][keep], found[keep].astype(int)
            cl = tr[keep & ~found]                       # labelled clean commits
            new = cl[np.isnan(alpha0[cl])]               # just crossed W: confidence computed now, once
            if len(new):
                lab = tr[keep]; lab_lab = found[keep].astype(int)
                # pool = most recent labelled commits whose label was known before this one was labelled
                notnew = ~np.isin(lab, new); lab, lab_lab = lab[notnew], lab_lab[notnew]
                pool = lab[-odasc_pool:]; pool_y = lab_lab[-odasc_pool:]
                if pool_y.sum() >= 5 and len(pool) > odasc_k:
                    from sklearn.neighbors import NearestNeighbors
                    mu, sd = X[pool].mean(0), X[pool].std(0) + 1e-9
                    nn = NearestNeighbors(n_neighbors=odasc_k).fit((X[pool] - mu) / sd)
                    _, ind = nn.kneighbors((X[new] - mu) / sd)
                    alpha0[new] = 1.0 - pool_y[ind].mean(1)
                else:
                    alpha0[new] = 1.0
            amb = keep & ~found
            amb[amb] = alpha0[tr[amb]] < odasc_delta    # low clean-confidence -> counted as both classes
            Xi = np.vstack([Xi, X[tr][amb]]); yi = np.concatenate([yi, np.ones(amb.sum(), int)])
            wi = np.ones(len(yi))
            if label_noise_log:
                truth = y[tr][amb]
                diag.append(dict(T=T, frac_amb=float(amb.sum() / max((keep & ~found).sum(), 1)),
                                 frac_amb_true_bug=float(truth.mean()) if len(truth) else np.nan))
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
        thr = 0.5
        if thr_policy != "fixed":
            thr = choose_threshold(thr_policy, T, t, tf, prob, start, thr_window)
            if label_noise_log: diag.append(dict(T=T, thr=thr))
        if model is not None:
            pr = model.predict_proba(X[start:end])[:, 1]
            prob[start:end] = pr; pred[start:end] = (pr >= thr).astype(int)
            recent_preds.extend(pred[start:end].tolist())
    # evaluation window
    ev = (pred >= 0) & (t <= t.max() - eval_end_gap_days * DAY)
    res = evaluate(y[ev], pred[ev], prob[ev])
    res.update(n_eval=int(ev.sum()), seconds=round(time.time() - t0, 2))
    out = {"metrics": res}
    if return_preds: out.update(pred=pred, prob=prob, eval_mask=ev)
    if diag: out["diag"] = diag
    return out

def choose_threshold(policy, T, t, tf, prob, start, window, min_n=200):
    """Threshold for commits made in [T, next update) using ONLY information available at T:
    prequential (out-of-sample, commit-time) scores of past commits and labels observable at T.
      ratematch: among recent 'mature' commits (age >= 90th pct of the truncation-corrected discovery
                 delay, fallback 365 d), flag the same share as were found defective.
      gmax_lat : maximise G-mean on the last `window` scored commits, with not-yet-found commits given a
                 soft positive weight q = b S(a) / (1 - b + b S(a)) (b = defect rate of mature commits)."""
    past = np.where(np.isfinite(prob[:start]))[0]
    if len(past) < min_n:
        return 0.5
    found_all = tf[:start] <= T
    pos = np.where(found_all)[0]
    age = (T - t) / DAY
    grid = np.arange(0, 4000, 5.0)
    S = survival_from_delays((tf[pos] - t[pos]) / DAY, (T - t[pos]) / DAY, grid, "lagakos")
    a90 = float(grid[np.argmax(S <= 0.10)]) if (S <= 0.10).any() and len(pos) >= 5 else 365.0
    mature = np.where(age[:start] >= a90)[0]
    if policy == "ratematch":
        m = np.intersect1d(mature, past)[-window:]
        if len(m) < min_n:
            return 0.5
        r = found_all[m].mean()
        return float(np.quantile(prob[m], 1 - r)) if 0 < r < 1 else 0.5
    if policy == "gmax_lat":
        w = past[-window:]
        b = found_all[mature].mean() if len(mature) >= min_n else found_all[:start].mean()
        Sa = np.interp(age[w], grid, S)
        q = np.where(found_all[w], 1.0, b * Sa / np.clip(1 - b + b * Sa, 1e-9, None))
        ps, sc = q, prob[w]
        order = np.argsort(-sc); sc_o, p_o, n_o = sc[order], ps[order], (1 - ps)[order]
        tp = np.cumsum(p_o); fp = np.cumsum(n_o)
        r1 = tp / max(tp[-1], 1e-9); r0 = 1 - fp / max(fp[-1], 1e-9)
        k = int(np.argmax(np.sqrt(np.clip(r1 * r0, 0, None))))
        return float(sc_o[k])
    raise ValueError(policy)

def evaluate(y, pred, prob):
    r1 = float(np.mean(pred[y == 1] == 1)) if (y == 1).any() else np.nan
    r0 = float(np.mean(pred[y == 0] == 0)) if (y == 0).any() else np.nan
    return dict(gmean=float(np.sqrt(r0 * r1)), r0=r0, r1=r1, rdiff=abs(r0 - r1),
                auc=float(roc_auc_score(y, prob)) if len(np.unique(y)) > 1 else np.nan,
                mcc=float(matthews_corrcoef(y, pred)))
