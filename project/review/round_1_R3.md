# Round 1 — Reviewer 3 (clarity, reproducibility, journal fit, ethics) — score 6/10, MAJOR REVISION
(Simulated reviewer, fresh context. Full report preserved as received; summary of concerns:)
1 MAJOR README cannot reproduce Tables 3/5/7 (E3b, E8, freeze_v5/v6, archived lineage, paper_numbers.py not documented)
2 MAJOR Cabral checksum only printed, not asserted
3 MAJOR data cleaning undocumented; Table 1 differs from raw ARFF/MSTDP (commit_type==3 copy rows removed)
4 MAJOR leakage-test claim overstated (dual, decomp, threshold rules untested; probabilities only)
5 MAJOR "pre-registered" needs definition; undisclosed deviations (H6 family change, H2a->H3, E3 not run)
6 MAJOR AI-agent / two-lineage disclosure too vague; Springer AI policy
7 MAJOR declarations placeholders; code DOI needed
8 MINOR Fig.2 axis bug (duplicated projects), in-image titles, few figures
9 MINOR wrong Wilcoxon statement: 8/1 split at n=9 gives p 0.0078-0.129
10 MINOR recovered share >1 unexplained
11 MINOR no variability in tables; supplementary tables unlabeled
12 MINOR RQ5 abstract overstated (dev-only numbers)
13 MINOR terminology (prequential, ORB, SZZ, theta/delta, truncation)
14 MINOR missing limitations (single learner, kNN ODaSC validation, lt constant, E7 unreported)
15 MINOR reference list short (31 vs 36-63)
Checks run by reviewer: tests pass; strict audit 0 unmatched; Holm p-values consistent with exact Wilcoxon.
