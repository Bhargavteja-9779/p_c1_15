#!/usr/bin/env python3
"""Strict G11 audit for paper/manuscript.md: every decimal number (and every integer > 31 that is not a year)
must match, at its printed precision, a value in the paper's DECLARED sources only (no catch-all pool).
Writes results/audit_strict.md; exit 1 if anything is unmatched."""
import re, os, sys, glob
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SRC = ["results/paper_numbers.json", "results/statistics.json", "paper/tables/*.md", "results/diag_law_neutron.json",
       "results/diag_survival_dev.txt", "state/frozen_config_v6.json", "tables/E0b_dev_tuning.csv", "tables/E0_dev_tuning.csv",
       "tables/rq1_*.csv", "archive/zealous_lamport_cycle1/results/statistics.json",
       "archive/zealous_lamport_cycle1/results/diag/operating_point_dev.csv", "archive/zealous_lamport_cycle1/tables/E0_dev_tuning.csv",
       "paper/references_checked.json", "results/review1/shapley.json", "results/review1/test_set_usage.json",
       "experiments/plan_v8_review1.yaml", "literature/pdfs/Song_IJCNN2022.txt", "results/review1/song2022_table2_means.json"]
pool = set()
for pat in SRC:
    for p in glob.glob(os.path.join(ROOT, pat)):
        for m in re.findall(r"-?\d+\.?\d*(?:e-?\d+)?", open(p, errors="ignore").read()):
            try: pool.add(float(m))
            except ValueError: pass
body = open(os.path.join(ROOT, "paper", "manuscript.md")).read().split("## References")[0]
body = re.sub(r"(?m)^#+ .*$", " ", body).replace("\u2212", "-").replace("SHA-256", "SHA")
body = re.sub(r"https?://\S+|10\.\d{4,}/\S+|`[^`]*`|\(figures/[^)]*\)", " ", body)
bad = []
body = re.sub(r"(?<=\d),(?=\d{3}\b)", "", body)
for s in re.findall(r"(?<![\w.])-?\d+(?:\.\d+)?(?![\w])", body):
    v = float(s)
    if "." not in s and (abs(v) <= 31 or 1900 <= v <= 2100): continue
    dec = len(s.split(".")[1]) if "." in s else 0
    if not any(abs(round(p, dec) - v) < 1e-9 or abs(round(p * 100, dec) - v) < 1e-9 for p in pool): bad.append(s)
rep = f"# Strict number audit\n\nUnmatched: {len(bad)}\n\n" + "\n".join(f"- {b}" for b in sorted(set(bad), key=float))
open(os.path.join(ROOT, "results", "audit_strict.md"), "w").write(rep); print(rep); sys.exit(1 if bad else 0)
