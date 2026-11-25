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

# ---- ApacheJIT (Keshavarz & Nagappan, MSR 2022; Zenodo 5907847, CC-BY-4.0): FRESH confirmation benchmark (plan_v7)
AJ = ROOT / "data" / "apachejit_raw" / "apachejit"
AJ_PROJECTS = ["ignite", "flink", "hbase", "cassandra", "groovy", "hive", "activemq", "hadoop-hdfs", "kafka"]  # >=2000 commits; camel excluded (overlaps Cabral test project); hadoop excluded (0 buggy commits in ApacheJIT)
AJ_LINK = {"ignite": "IGNITE", "hadoop": None, "flink": "FLINK", "hbase": "HBASE", "cassandra": "CASSANDRA", "groovy": "GROOVY",
           "hive": "HIVE", "activemq": "AMQ", "hadoop-hdfs": "HDFS", "kafka": "KAFKA"}

def load_apachejit(name, cache=True):
    """One ApacheJIT project in the same format as load_project. Discovery time t_found = earliest fix_date
    among the SZZ links of a buggy commit (all links of all projects are searched by bug hash). Feature map:
    entrophy<-ent, exp<-aexp, rexp<-arexp, sexp<-asexp; 'lt' is absent in ApacheJIT -> constant 0."""
    import glob
    cp = ROOT / "data" / f"aj_{name}.pkl"
    if cache and cp.exists(): return pd.read_pickle(cp)
    t = pd.read_csv(AJ / "dataset" / "apachejit_total.csv"); t = t[t.project == f"apache/{name}"].copy()
    L = pd.concat([pd.read_csv(f) for f in glob.glob(str(AJ / "data" / "commit_links_*.csv"))])
    first_fix = L.groupby("bug_hash").fix_date.min()
    df = pd.DataFrame({"fix": t.fix.astype(int), "ns": t.ns, "nd": t.nd, "nf": t.nf, "entrophy": t.ent, "la": t.la, "ld": t.ld,
                       "lt": 0.0, "ndev": t.ndev, "age": t.age, "nuc": t.nuc, "exp": t.aexp, "rexp": t.arexp, "sexp": t.asexp,
                       "t": t.author_date.astype(float), "y": t.buggy.astype(int)})
    df["t_found"] = np.where(df.y == 1, t.commit_id.map(first_fix).astype(float).values, np.inf)
    # a fix cannot precede its bug; a buggy commit without a valid link keeps its label but is 'found' at its first fix or never
    bad_order = (df.y == 1) & (df.t_found < df.t); df.loc[bad_order, "t_found"] = df.loc[bad_order, "t"]
    df.loc[(df.y == 1) & ~np.isfinite(df.t_found), "t_found"] = np.inf
    df = df.dropna(subset=[c for c in df.columns if c != "t_found"]).sort_values("t").reset_index(drop=True)
    df["project"] = "aj_" + name
    df.attrs.update(n_fix_before_bug=int(bad_order.sum()))
    if cache: df.to_pickle(cp)
    return df

def load_project(name, cache=True):
    if name.startswith("aj_"): return load_apachejit(name[3:], cache)
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
