#!/usr/bin/env bash
# Layer A watchdog (run every 5 min from cron). If the runner is alive but heartbeat is
# older than 20 min -> kill & relaunch (resumes from checkpoint). If the runner is dead and
# the queue still has pending/running work -> relaunch.
cd "$(dirname "$0")/.." || exit 1
mkdir -p logs
AGE=$(python3 -c "import sys;sys.path.insert(0,'.');from src.state import heartbeat_age_s as h;a=h();print(int(a) if a is not None else 999999)")
WORK=$(python3 -c "import sys,json;sys.path.insert(0,'.');from src.state import *;q=read_json(STATE/'queue.json',{'jobs':[]});print(sum(j['status'] in ('pending','running') or (j['status']=='failed' and j.get('attempts',0)<3) for j in q['jobs']))")
if pgrep -f "run_all.py --mode full" >/dev/null; then  # any worker alive
  if [ "$AGE" -gt 1200 ]; then
    echo "$(date -Is) heartbeat stale (${AGE}s) -> kill+relaunch" >> logs/watchdog.log
    pkill -f "run_all.py --mode full"; sleep 5; bash scripts/launch_runner.sh >> logs/watchdog.log 2>&1
  fi
elif [ "$WORK" -gt 0 ]; then
  echo "$(date -Is) runner dead with $WORK jobs left -> relaunch" >> logs/watchdog.log
  bash scripts/launch_runner.sh >> logs/watchdog.log 2>&1
fi
