#!/usr/bin/env python3
"""Mean G-mean over the 14 projects of Song et al. (IJCNN 2022) Table II, from the layout-preserving text of the PDF
(literature/pdfs/Song_IJCNN2022.pdf; needs pdftotext). Writes results/review1/song2022_table2_means.json."""
import subprocess, os, json, re
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
txt = subprocess.run(["pdftotext", "-layout", os.path.join(ROOT, "literature/pdfs/Song_IJCNN2022.pdf"), "-"], capture_output=True, text=True).stdout
L = txt.splitlines(); h = next(i for i, l in enumerate(L) if "#-opt" in l and "OOB" in l)
cols = ["ours_rmse", "random_rmse", "odasc", "odasc_opt", "odasc_flt", "odasc_rnd", "oob", "ob"]; rows = {}
for l in L[h + 1:h + 15]:
    t = l[69:].split()
    rows[t[0]] = dict(zip(cols, map(float, t[-8:])))
assert len(rows) == 14, rows.keys()
means = {c: round(sum(r[c] for r in rows.values()) / 14, 4) for c in cols[2:]}
out = dict(source="Song et al. 2022, Table II (G-mean part), 14 projects", means=means,
           opt_minus_oob=round(means["odasc_opt"] - means["oob"], 4), flt_minus_oob=round(means["odasc_flt"] - means["oob"], 4), per_project=rows)
json.dump(out, open(os.path.join(ROOT, "results/review1/song2022_table2_means.json"), "w"), indent=1); print(means, out["opt_minus_oob"], out["flt_minus_oob"])
