"""Load the Cabral et al. (ICSE'19) JIT-SDP datasets (Zenodo 10.5281/zenodo.2591761).
Each ARFF has one row per commit (commit_type 0/1/2) plus 'copy' rows (commit_type 3) placed at the
time the defect-inducing commit was discovered. We reconstruct, for every commit:
  t_commit, y (contains_bug), t_found (discovery time; inf for clean commits)."""
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "jit"
FEATS = ["fix", "ns", "nd", "nf", "entrophy", "la", "ld", "lt", "ndev", "age", "nuc", "exp", "rexp", "sexp"]
PROJECTS = ["brackets", "broadleaf", "camel", "fabric", "jgroups", "matplotlib", "neutron", "nova",
            "npm", "sentry", "spring-integration", "tomcat", "wagtail", "zulip"]

def read_arff(path):
    cols, rows, data = [], [], False
    for line in open(path):
        s = line.strip()
        if not s or s.startswith("%"): continue
        if s.lower().startswith("@attribute"):
            cols.append(s.split()[1]); continue
        if s.lower().startswith("@data"): data = True; continue
        if data: rows.append(s.split(","))
    df = pd.DataFrame(rows, columns=cols)
    for c in cols:
        if c in ("fix", "contains_bug"): df[c] = (df[c] == "True").astype(int)
        else: df[c] = pd.to_numeric(df[c])
    return df

def load_project(name, cache=True):
    cp = DATA / f"{name}.pkl"
    if cache and cp.exists():
        return pd.read_pickle(cp)
    raw = read_arff(DATA / f"{name}.arff")
    raw["_row"] = np.arange(len(raw))
    commits = raw[raw.commit_type != 3].copy()
    copies = raw[raw.commit_type == 3].copy()
    # match each copy to the earliest unmatched buggy commit with identical features & earlier time
    commits["t_found"] = np.inf
    key = lambda d: pd.Series(list(map(tuple, d[FEATS].round(6).to_numpy().tolist())), index=d.index)
    commits["_k"] = key(commits); copies["_k"] = key(copies)
    buggy = commits[commits.contains_bug == 1]
    groups = {k: list(g.sort_values("author_date_unix_timestamp").index) for k, g in buggy.groupby("_k")}
    unmatched = 0
    for idx, r in copies.sort_values("author_date_unix_timestamp").iterrows():
        cands = groups.get(r["_k"], [])
        cands = [i for i in cands if commits.at[i, "author_date_unix_timestamp"] <= r["author_date_unix_timestamp"]
                 and not np.isfinite(commits.at[i, "t_found"])]
        if cands:
            commits.at[cands[0], "t_found"] = r["author_date_unix_timestamp"]
        else:
            unmatched += 1
    commits = commits.drop(columns=["_k"]).rename(columns={"author_date_unix_timestamp": "t", "contains_bug": "y"})
    commits = commits.sort_values(["t", "_row"]).reset_index(drop=True)
    commits.attrs["unmatched_copies"] = unmatched
    commits["project"] = name
    bad = (commits.t < 946684800) | commits[FEATS + ["t"]].isna().any(axis=1)  # corrupt timestamp (<2000, 1 commit in zulip at 1970) or missing values
    commits.attrs["dropped_bad_time"] = int(bad.sum())
    commits = commits[~bad].reset_index(drop=True)
    if cache:
        commits.to_pickle(cp)
    return commits

# ---------------------------------------------------------------- ApacheJIT (second, fresh benchmark)
AJ_ROOT = ROOT / "data" / "apachejit_raw" / "apachejit"
AJ_PROJECTS = {"activemq": ("apache/activemq", "AMQ"), "cassandra": ("apache/cassandra", "CASSANDRA"),
               "flink": ("apache/flink", "FLINK"), "groovy": ("apache/groovy", "GROOVY"),
               "hbase": ("apache/hbase", "HBASE"), "ignite": ("apache/ignite", "IGNITE"),
               "hive": ("apache/hive", "HIVE"), "kafka": ("apache/kafka", "KAFKA")}

def load_apachejit(name, cache=True):
    """ApacheJIT (Keshavarz & Nagappan, MSR 2022; Zenodo 5907847). Discovery time of a bug-inducing commit =
    earliest fix_date among commit_links_<KEY>.csv rows whose bug_hash is that commit (and fix_date >= commit date).
    'lt' is not provided by ApacheJIT and is set to 0 (constant; ignored by the learner)."""
    cp = DATA / f"aj_{name}.pkl"
    if cache and cp.exists():
        return pd.read_pickle(cp)
    repo, key = AJ_PROJECTS[name]
    tot = pd.read_csv(AJ_ROOT / "dataset" / "apachejit_total.csv")
    d = tot[tot.project == repo].copy()
    L = pd.read_csv(AJ_ROOT / "data" / f"commit_links_{key}.csv")
    L = L[L.fix_date >= L.bug_date]
    first_fix = L.groupby("bug_hash").fix_date.min()
    d = d.rename(columns={"ent": "entrophy", "aexp": "exp", "arexp": "rexp", "asexp": "sexp", "author_date": "t", "buggy": "y"})
    d["fix"] = d["fix"].astype(int); d["y"] = d["y"].astype(int); d["lt"] = 0.0
    d["t_found"] = d.commit_id.map(first_fix).astype(float)
    d.loc[d.y == 0, "t_found"] = np.inf
    d["t_found"] = d["t_found"].fillna(np.inf)
    d["_row"] = np.arange(len(d)); d["project"] = name
    d = d.dropna(subset=FEATS + ["t"]).sort_values(["t", "_row"]).reset_index(drop=True)
    d.attrs["buggy_without_fix_date"] = int(((d.y == 1) & ~np.isfinite(d.t_found)).sum())
    if cache:
        d.to_pickle(cp)
    return d

def load_any(name):
    return load_apachejit(name[3:]) if name.startswith("aj_") else load_project(name)
