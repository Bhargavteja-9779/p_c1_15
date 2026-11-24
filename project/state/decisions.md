# Decisions log

Every decision with reason and UTC timestamp. Append-only.

- **2026-11-24T03:04:37+00:00** — Place project in repo subfolder project/ on branch claude/dreamy-fermat-7983nm
  - Reason: Prompt specifies project/ layout; repo is the persistent store (container is ephemeral).

- **2026-11-24T03:04:37+00:00** — Hardware: CPU-only (4 cores, 15 GB RAM, no CUDA/MPS). All compute budgets are counted as CPU-hours.
  - Reason: nvidia-smi absent, torch.cuda.is_available()=False. This constrains topic choice to CPU-feasible experiments.

- **2026-11-24T03:11:07+00:00** — Selected journal: Journal of King Saud University – Computer and Information Sciences (Springer Nature, ISSN 1319-1578, IF 6.4 (2025))
  - Reason: Only verifiable reputable candidate with median Received→Accepted near 72 d (71 d last-12-month acceptances, 74 d 24-month window); 17 other verifiable candidates had medians 123–462 d; Elsevier fast journals could not be verified (no Crossref dates, ScienceDirect 403). G1 caveat: marginal on turnaround; 2025 JCR quartile UNVERIFIED (Q1 in 2024 JCR per KSU).

- **2026-11-24T03:11:07+00:00** — Interpretation: "submission→acceptance ≤ 72" evaluated as the MEDIAN (Accepted−Received) of a random sample
  - Reason: Section 4 asks to compute median and range; a per-paper guarantee is impossible.
