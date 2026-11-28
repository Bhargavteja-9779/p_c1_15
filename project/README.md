# Where does verification latency hurt online JIT defect prediction?

Code, data pointers, frozen plans and results for the manuscript in `paper/manuscript.md`. Tested with Python 3.13 on Linux (CPU only, 4 cores).

## Setup
```bash
pip install -r requirements.txt
```
Data (git-ignored; downloaded and SHA-256-verified by the script):
- Cabral et al. (ICSE 2019) artifact, Zenodo record 2591761 (`spdisc-icse19-V1.02.zip`, 14 ARFF files);
- ApacheJIT (MSR 2022), Zenodo record 5907847 (CC-BY-4.0).
```bash
python scripts/get_data.py
```
The development/test split of the Cabral projects (dev = fabric, neutron, nova, sentry) was drawn once with `numpy.random.default_rng(0)` before any modelling, as recorded in `experiments/plan_v1.yaml`; it is hard-coded in the scripts and reproduced by `python -c "import numpy as np; print(sorted(np.random.default_rng(0).choice(sorted(['brackets','broadleaf','camel','fabric','jgroups','matplotlib','neutron','nova','npm','sentry','spring-integration','tomcat','wagtail','zulip']), 4, replace=False)))"`.

`torch` is used only by the job runner to write checkpoints (`src/runner.py`); no model in the paper uses it.

## Reproducing the paper

**Fast path (no simulation, ~1 min):** all simulation outputs are committed (`results/raw_results.jsonl`, `results/review1/raw.jsonl`, `archive/zealous_lamport_cycle1/results/raw_results.jsonl`). Regenerate every table, figure and number of the manuscript and check them:
```bash
python scripts/get_data.py            # Cabral (ARFF checksums asserted) + ApacheJIT (zip checksum asserted)
python scripts/review1_shapley.py     # 2x2 / Shapley decomposition, W=30 and W=90 (Table 6)
python scripts/paper_numbers.py       # paper/tables/*.md, paper/figures/*.png, results/paper_numbers.json
python scripts/test_set_usage.py      # Supplementary Table S3: every configuration ever run on the Cabral test projects (scans all branches)
python scripts/build_references.py    # reference list from Crossref metadata + citation cross-check
python scripts/audit_paper_strict.py  # every number in the manuscript traced to a declared source (must print Unmatched: 0)
python tests/test_no_future.py && python tests/test_no_future_threshold_rules.py   # leakage tests
```

**Full re-simulation** (order matters: development runs, then freeze, then confirmation). CPU-hours are for 1 core.

| Manuscript item | Experiments | Commands | approx. CPU-h |
|---|---|---|---|
| Dev tuning (Sect. 4.3) | E0, E0b, E0c, E0d, E0e (dev projects) | `python scripts/enqueue.py E0` (same for E0b, E0c, E0d, E0e) `&& bash scripts/launch_runner.sh 3`, then `python scripts/freeze_config.py`, `python scripts/freeze_v5.py`, `python scripts/freeze_v6.py` | 12 |
| Table 8 (RQ3) | E1 (Cabral test) | `python scripts/enqueue.py E1 && bash scripts/launch_runner.sh 3` | 4 |
| Tables 5-6, Cabral (RQ2) | E3b (Cabral test) | `python scripts/enqueue.py E3b && bash scripts/launch_runner.sh 3` | 4 |
| Tables 5-6, ApacheJIT W=30; Table 9 (RQ4) | E8 (ApacheJIT) | `python scripts/enqueue.py E8 && bash scripts/launch_runner.sh 3` | 3 |
| Tables 5-6 ApacheJIT W=90 (A2), Table 7 / Fig. 3 (A3), Table S5 (A4), Tables 12-13 (A5) | plan_v8 | `python scripts/review1_runs.py 3` | 5 |
| Table 10 (RQ5 diagnostic) | lineage 2, dev | `python archive/zealous_lamport_cycle1/scripts/diag_operating_point.py fabric,neutron` (run from `archive/zealous_lamport_cycle1/` with `data/` linked) | 0.2 |
| Table 11 (RQ5 confirmation, Cabral) | lineage 2, E1 | `python scripts/reproduce_table7.py` (named after the table's number in an earlier draft; compares with the archived values) | 3 |
| Table 8 / S6 inputs: RQ3 diagnostics (`results/diag_law_neutron.json`, `results/diag_survival_dev.txt`) | dev | `python scripts/diag_law.py` | 0.5 |
| Table 7 / Fig. 3 additions (plan_v9: W=90 strata B1, leave-one-band-out B3) | plan_v9 | `python scripts/review1_runs.py 3` (same script; jobs are idempotent) | 4 |
| Table S3: flip counts per age band (plan_v9 B2) | model-free | `python scripts/review2_flip_counts.py` | 0.1 |

Then run the fast path. `run_all.py --mode quick` is a smoke test of the queue infrastructure (a few minutes).

**Manuscript table/figure → generated file.**

| Manuscript | File |
|---|---|
| Table 3 (datasets) | `paper/tables/T1_datasets.md` |
| Table 4 (RQ1) | `paper/tables/T2_rq1_label_noise.md` |
| Table 5 (decomposition cells) | `T3_rq2_decomposition_means.md`, `T8_A2_apachejit_W90.md` |
| Table 6 (factorial split) | `T3b_shapley.md` |
| Table 7 (age bands) | `T9_A3_age_strata.md`, `T12_age_bands_W90_and_leave_one_out.md` |
| Table 8 (RQ3) | `T4_rq3_age_only_cabral_test.md`, per project `T4b` |
| Table 9 (RQ4, ApacheJIT) | `T5_rq4_apachejit_all_metrics.md`, per project `T5b` |
| Table 10 (operating point, dev) | `T6_rq5_operating_point_dev.md` |
| Table 11 (threshold, Cabral) | `T7_rq5_threshold_cabral_test_independent_lineage.md` (script `reproduce_table7.py`) |
| Tables 12–13 (threshold, ApacheJIT) | `T11_A5_threshold_apachejit.md`, `T11b_A5_tests.md` |
| Supplementary S1–S6 | S1 `S3_test_set_usage.md`; S2 `S2_cabral_rows_vs_mstdp.md`; S3 `results/review1/flip_counts.json`; S4 `T9`, `T12` (G-mean rows), `T4b`, `T5b`, `T3c`; S5 `T10_A4_eval_gap730.md`; S6 `S1_delay_estimator.md` (file names predate the final numbering) |
| Figs. 1–3 | `paper/figures/F1_discovery_delay.png`, `F2_gap_recovered.png`, `F3_age_strata.png` |
Plans that fixed each configuration before its confirmatory run: `experiments/plan_v1.yaml` … `plan_v9_review2.yaml` (main lineage) and `archive/zealous_lamport_cycle1/experiments/plan_v1-v3.yaml` (lineage 2). Every configuration evaluated is listed in `state/variants_tried.csv` and `archive/zealous_lamport_cycle1/state/variants_tried.csv`.
