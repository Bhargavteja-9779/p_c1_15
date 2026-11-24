#!/usr/bin/env python3
"""G11 integrity audit: every decimal number in paper/manuscript.md must match (after rounding to the
printed precision) some number in results/*.json|csv|md, tables/*, journal_selection/*, or results/data_summary.json.
Integers <= 31 and years are ignored (section numbers, counts in prose are checked if > 31).
Exit code 1 on any unmatched number; writes results/audit_report.md."""
import re, sys, os, glob, json
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
paper = open(os.path.join(ROOT, "paper", "manuscript.md")).read()
# drop references section and DOIs/URLs
body = paper.split("## References")[0]
body = re.sub(r"https?://\S+|10\.\d{4,}/\S+|`[^`]*`", " ", body)
pool = set()
for pat in ["results/**/*.json", "results/*.csv", "results/*.md", "tables/*", "journal_selection/*.csv", "journal_selection/*.md",
            "journal_selection/turnaround/*.json", "state/frozen_config.json", "literature/*.csv", "literature/*.md"]:
    for p in glob.glob(os.path.join(ROOT, pat), recursive=True):
        if os.path.isfile(p) and os.path.getsize(p) < 30_000_000:
            for m in re.findall(r"-?\d+\.?\d*(?:e-?\d+)?", open(p, errors="ignore").read()):
                try: pool.add(float(m))
                except ValueError: pass
nums = re.findall(r"(?<![\w.])-?\d+(?:\.\d+)?(?![\w])", body)
bad = []
for s in nums:
    v = float(s)
    if "." not in s and (abs(v) <= 31 or 1900 <= v <= 2100): continue
    dec = len(s.split(".")[1]) if "." in s else 0
    ok = any(abs(round(p, dec) - v) < 1e-9 or abs(round(p * 100, dec) - v) < 1e-9 for p in pool)
    if not ok: bad.append(s)
rep = f"# Number audit\n\nNumbers checked: {len(nums)}; unmatched: {len(bad)}\n\n" + "\n".join(f"- {b}" for b in sorted(set(bad), key=float))
open(os.path.join(ROOT, "results", "audit_report.md"), "w").write(rep)
print(rep[:2000]); sys.exit(1 if bad else 0)
