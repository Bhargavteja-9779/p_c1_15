#!/usr/bin/env python3
"""Entry point for Layer A. Safe to run any number of times (lock + idempotent queue).
  python run_all.py --mode quick           # smoke test (<10 min), separate queue/results
  python run_all.py --mode full --resume   # main detached run
"""
import argparse, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("OMP_NUM_THREADS", "1")  # parallelism comes from multiple workers
from src.runner import run
from src.state import get_agent_state

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["quick", "full"], default="full")
    ap.add_argument("--resume", action="store_true", help="(always on; kept for interface compatibility)")
    ap.add_argument("--only-kind", default=None)
    ap.add_argument("--max-jobs", type=int, default=None)
    ap.add_argument("--worker", type=int, default=0)
    a = ap.parse_args()
    if get_agent_state().get("status") == "FINISHED" and a.mode == "full":
        print("[run_all] project FINISHED; nothing to do."); sys.exit(0)
    sys.exit(run(a.mode, True, a.only_kind, a.max_jobs, a.worker))
