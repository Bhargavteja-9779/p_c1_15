"""Reimplementation of OOB and ODaSC (Song, Li, Minku & Yao, IJCNN 2022, doi 10.1109/IJCNN55064.2022.9891911)
for the prequential protocol of src/jit.py (predict at commit time, score against FINAL labels, same
evaluation window).  No public code was found, so this follows the paper's equations; choices the paper
leaves open are marked INTERPRETATION and logged in state/decisions.md.

Event stream (waiting-time framework, Cabral et al. 2019, as used by ODaSC):
  commit at t        -> predict
  defect found at tf -> training example (x, 1)
  t + W, not found   -> training example (x, 0)  (may be noisy: found later -> also (x, 1) at tf)
Learner: Oversampling Online Bagging (OOB, Wang et al.) of M Hoeffding trees (river defaults),
class proportions tracked with decay `theta`; ODaSC multiplies the Poisson rate by exp(alpha - delta)
where alpha is the micro-cluster label confidence (Eqs. 2-10) and updates class counters by Eq. 12.
"""
import time, math, numpy as np
from river import tree
from .jit import FEATS, DAY, evaluate

LAMBDA_FADE = 0.1      # DenStream fading (paper: lambda = 0.1); INTERPRETATION: time unit = days
TEMP = 10.0            # temperature T in Eqs. 3 and 4 (paper: 10)
RHO_W = 1e-5           # case-(1) threshold (paper)
MAX_MC = 300           # INTERPRETATION: cap on micro-clusters (lowest weight pruned) to bound run time

class MicroClusters:
    """DenStream-style micro-clusters with class counters C0/C1 (single list; faded weights)."""
    def __init__(self, eps, d):
        self.eps = eps; self.d = d
        self.cf1 = np.zeros((0, d)); self.cf2 = np.zeros((0, d)); self.w = np.zeros(0)
        self.tl = np.zeros(0); self.c0 = np.zeros(0); self.c1 = np.zeros(0)

    def _fade(self, now):
        if len(self.w) == 0: return
        f = 2.0 ** (-LAMBDA_FADE * np.maximum(now - self.tl, 0.0))
        self.cf1 *= f[:, None]; self.cf2 *= f[:, None]; self.w *= f; self.tl[:] = now

    def centers_radii(self):
        c = self.cf1 / self.w[:, None]
        var = np.clip(self.cf2 / self.w[:, None] - c ** 2, 0, None)
        return c, np.sqrt(var.sum(1))

    def confidence1(self, x):
        """Uncalibrated class-1 label confidence alpha1(x) (Eqs. 2-7); None for case (2)."""
        if len(self.w) == 0: return None
        c, r = self.centers_radii()
        dist = np.maximum(0.0, np.linalg.norm(x - c, axis=1) - r)
        cor = np.exp(-TEMP * dist)                                  # Eq. 3
        obs = np.tanh(self.w / TEMP)                                # Eq. 4 (CT = faded weight)
        wgt = cor * obs                                             # Eq. 5
        if wgt.sum() < RHO_W: return None                           # case (2)
        n = self.c0 + self.c1
        P1 = np.where(n > 0, self.c1 / np.maximum(n, 1e-12), 0.0); P0 = 1 - P1
        PD1 = self.c1.sum() / max(n.sum(), 1e-12); PD0 = 1 - PD1
        dd = lambda a, b: 0.5 * (a - b) / np.maximum(a + b, 1e-12)
        rep1 = P1 * (1 + dd(P1, PD1)); rep0 = P0 * (1 + dd(P0, PD0))  # Eq. 2
        rho = wgt.mean() - wgt.std()
        F = wgt >= rho
        num = (rep1[F] * wgt[F]).sum(); den = num + (rep0[F] * wgt[F]).sum()
        return float(num / den) if den > 0 else None                 # Eq. 6

    def prior1(self):
        n = (self.c0 + self.c1).sum()
        return float(self.c1.sum() / n) if n > 0 else 0.5

    def insert(self, x, now, inc0, inc1):
        self._fade(now)
        if len(self.w):
            c, _ = self.centers_radii()
            j = int(np.argmin(np.linalg.norm(x - c, axis=1)))
            cf1 = self.cf1[j] + x; cf2 = self.cf2[j] + x ** 2; w = self.w[j] + 1
            cc = cf1 / w; rad = math.sqrt(max(float((cf2 / w - cc ** 2).sum()), 0.0))
            if rad <= self.eps:
                self.cf1[j], self.cf2[j], self.w[j] = cf1, cf2, w
                self.c0[j] += inc0; self.c1[j] += inc1; return
        self.cf1 = np.vstack([self.cf1, x]); self.cf2 = np.vstack([self.cf2, x ** 2])
        self.w = np.append(self.w, 1.0); self.tl = np.append(self.tl, now)
        self.c0 = np.append(self.c0, inc0); self.c1 = np.append(self.c1, inc1)
        if len(self.w) > MAX_MC:
            k = int(np.argmin(self.w))
            for a in ("cf1", "cf2", "w", "tl", "c0", "c1"):
                setattr(self, a, np.delete(getattr(self, a), k, axis=0))


def simulate_odasc(df, seed=0, W=15, M=10, theta=0.99, delta=0.9, use_conf=True, warmup=500,
                   eval_end_gap_days=365, delay_scale=1.0, calib_window=50, return_preds=False):
    """use_conf=False -> plain OOB.  Returns {"metrics": ...} like jit.simulate."""
    t0 = time.time(); rng = np.random.default_rng(seed)
    df = df.reset_index(drop=True)
    X = np.log1p(np.clip(df[FEATS].to_numpy(float), 0, None))
    t = df["t"].to_numpy(float) / DAY; y = df["y"].to_numpy(int)
    tf = df["t_found"].to_numpy(float) / DAY
    if delay_scale != 1.0:
        fin = np.isfinite(tf); tf = tf.copy(); tf[fin] = t[fin] + (tf[fin] - t[fin]) * delay_scale
    n = len(df)
    # INTERPRETATION: standardisation and DenStream radius eps from the first `warmup` commits' FEATURES
    # only (no labels): eps = median nearest-neighbour distance among them.
    mu, sd = X[:warmup].mean(0), X[:warmup].std(0) + 1e-9
    Z = (X - mu) / sd
    A = Z[:warmup]; D2 = ((A[:, None, :] - A[None, :, :]) ** 2).sum(-1); np.fill_diagonal(D2, np.inf)
    eps = float(np.median(np.sqrt(D2.min(1))))
    mc = MicroClusters(eps, Z.shape[1])
    trees = [tree.HoeffdingTreeClassifier() for _ in range(M)]
    prop = np.array([0.5, 0.5])            # tracked class proportions (OOB)
    recent_a1 = []                         # alpha1 of recent class-1 examples (calibration, Eqs. 8-9)
    # events: (time, order, kind, idx); kind 0=predict, 1=train
    ev = [(t[i], 0, 0, i, -1) for i in range(n)]
    for i in range(n):
        if np.isfinite(tf[i]) and y[i] == 1:
            ev.append((tf[i], 1, 1, i, 1))
            if tf[i] - t[i] > W: ev.append((t[i] + W, 1, 1, i, 0))
        else:
            ev.append((t[i] + W, 1, 1, i, 0))
    ev.sort(key=lambda e: (e[0], e[1], e[3]))
    prob = np.full(n, np.nan); pred = np.full(n, -1)
    feats = [dict(enumerate(z)) for z in Z]
    n_trained = 0
    for (now, _, kind, i, lab) in ev:
        if kind == 0:
            if n_trained == 0: continue
            votes = [tr.predict_one(feats[i]) for tr in trees]
            v = np.mean([1 if vv == 1 else 0 for vv in votes])
            prob[i] = v; pred[i] = int(v > 0.5)        # majority vote (ties -> clean)
            continue
        # ---- label confidence (ODaSC)
        alpha = None
        if use_conf:
            a1 = mc.confidence1(Z[i])
            if a1 is None: a1 = 1.0 if lab == 1 else mc.prior1()     # Eq. 7
            if lab == 1:
                recent_a1.append(a1); del recent_a1[:-calib_window]
            if len(recent_a1) >= 2:                                    # Eqs. 8-9 (INTERPRETATION: rolling window)
                m_, s_ = np.mean(recent_a1), np.std(recent_a1); amin = min(recent_a1)
                k = next((k for k in (1, 2, 3) if m_ - k * s_ <= amin), 3)
                bench = max(m_ - k * s_, 0.0)
                if a1 >= bench and amin > 0: a1 = min(1.0, a1 / amin)
            alpha = a1 if lab == 1 else 1 - a1                         # Eq. 10
            inc1 = 1 if (lab == 1 or alpha < 1 - delta) else 0        # Eq. 12
            mc.insert(Z[i], now, inc0=1 if lab == 0 else 0, inc1=inc1)
        # ---- OOB update
        prop = theta * prop + (1 - theta) * np.array([lab == 0, lab == 1], float)
        minority = int(np.argmin(prop))
        lam = prop[1 - minority] / max(prop[minority], 1e-9) if lab == minority else 1.0
        if alpha is not None:
            lam *= math.exp(alpha - delta)                             # Eq. 11 (INTERPRETATION: both classes)
        for tr in trees:
            k = rng.poisson(lam)
            for _ in range(k): tr.learn_one(feats[i], lab)
        n_trained += 1
    idx = np.arange(n)
    evm = (pred >= 0) & (idx >= warmup) & (t <= t.max() - eval_end_gap_days)
    res = evaluate(y[evm], pred[evm], prob[evm])
    res.update(n_eval=int(evm.sum()), seconds=round(time.time() - t0, 2), eps=eps)
    out = {"metrics": res}
    if return_preds: out.update(pred=pred, prob=prob, eval_mask=evm)
    return out
