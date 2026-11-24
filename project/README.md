# Verification-latency-aware online JIT defect prediction

Research code for the study described in `topic/selected_topic.md` (state of the project: `HANDOFF.md`).

## Setup
```bash
pip install -r requirements.txt
```
Data: the Cabral et al. (ICSE 2019) artifact, Zenodo record 2591761 (`spdisc-icse19-V1.02.zip`). The data folder is git-ignored; fetch the 14 ARFF files with:
```bash
python scripts/get_data.py
```

## Reproduce
```bash
python tests/test_no_future.py                 # leakage + estimator tests
python run_all.py --mode quick                 # smoke test (<1 min)
python scripts/enqueue.py E0 && bash scripts/launch_runner.sh 3   # dev tuning (detached)
python scripts/freeze_config.py                # choose W* on dev projects only
python scripts/enqueue.py E1 && python scripts/enqueue.py E2 && python scripts/enqueue.py E3 && bash scripts/launch_runner.sh 3
python scripts/final_report.py                 # tables/, figures/, results/statistics.json, RESULTS_SUMMARY.md
python scripts/audit_numbers.py                # every number in paper/manuscript.md traced to a result file
```
Each job is one prequential simulation (`src/jit.py: simulate`); results are appended to `results/raw_results.jsonl`.
