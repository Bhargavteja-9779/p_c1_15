#!/usr/bin/env python3
"""Count every configuration ever run on the 10 Cabral test projects, across ALL commits of ALL branches in git history.
Writes results/review1/test_set_usage.json and paper/tables/S3_test_set_usage.md. Covers committed results only."""
import subprocess, re, json, os, collections
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
REPO = os.path.dirname(ROOT)
TEST = ["brackets","broadleaf","camel","jgroups","matplotlib","npm","spring-integration","tomcat","wagtail","zulip"]
g = lambda *a: subprocess.run(["git", "-C", REPO, *a], capture_output=True, text=True).stdout
commits = sorted(set(g("log", "--all", "--format=%h", "--", "project/results", "project/archive").split()))
rx = re.compile(r"/results/(quick/)?([A-Za-z0-9]+)_(" + "|".join(map(re.escape, TEST)) + r")_(.+?)_s(\d+)(_quick)?\.json$")
cfg = collections.defaultdict(set)
for c in commits:
    for f in g("ls-tree", "-r", "--name-only", c, "project/results", "project/archive").split():
        m = rx.search(f)
        if m and "/diag/" not in f: cfg[(m.group(2), m.group(4), "quick" if m.group(1) or m.group(6) else "full")].add((m.group(3), m.group(5)))
branches = [b.strip() for b in g("branch", "-r").split() if "claude/" in b]
where = {}
for b in branches:
    for f in g("ls-tree", "-r", "--name-only", b, "project/results", "project/archive").split():
        m = rx.search(f)
        if m and "/diag/" not in f: where.setdefault((m.group(2), m.group(4), "quick" if m.group(1) or m.group(6) else "full"), set()).add(b.split("/")[-1].rsplit("-", 1)[0])
# results stored in jsonl files (review analyses, plan_v8/v9) are scanned too
for jf in ["results/review1/raw.jsonl"]:
    fp = os.path.join(ROOT, jf)
    if os.path.exists(fp):
        for l in open(fp):
            try: r = json.loads(l)
            except Exception: continue
            if r.get("project") in TEST:
                k = (r["analysis"], r["variant"], "full"); cfg[k].add((r["project"], str(r["seed"]))); where.setdefault(k, set()).add("zealous-lamport")
rows = [dict(experiment=e, variant=v, mode=("smoke" if mo == "quick" else "complete" if len({p for p, _ in s}) == len(TEST) else "partial"),
             projects=len({p for p, _ in s}), runs=len(s), uses_true_labels=any(k in v for k in ("decomp", "strata", "oracle")) or v.startswith("out"),
             branches=", ".join(sorted(where.get((e, v, mo), [])))) for (e, v, mo), s in sorted(cfg.items())]
pre = [r for r in rows if r["experiment"][0] == "E"]; rev = [r for r in rows if r["experiment"][0] != "E"]
out = dict(n_commits_scanned=len(commits),
           n_configs_complete_pre_review=sum(r["mode"] == "complete" for r in pre), n_configs_partial_pre_review=sum(r["mode"] == "partial" for r in pre),
           n_configs_smoke_only=len({(r["experiment"], r["variant"]) for r in rows if r["mode"] == "smoke"} - {(r["experiment"], r["variant"]) for r in rows if r["mode"] != "smoke"}),
           n_configs_review_analyses=len(rev), rows=rows)
json.dump(out, open(os.path.join(ROOT, "results", "review1", "test_set_usage.json"), "w"), indent=1)
import pandas as pd
pd.DataFrame(rows).to_markdown(os.path.join(ROOT, "paper", "tables", "S3_test_set_usage.md"), index=False)
print({k: v for k, v in out.items() if k != "rows"})
