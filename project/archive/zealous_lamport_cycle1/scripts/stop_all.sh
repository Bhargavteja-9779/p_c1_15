#!/usr/bin/env bash
# Stop both layers (does not delete any state; resume with launch_runner.sh / supervisor.sh)
cd "$(dirname "$0")/.." || exit 1
touch state/STOP_SUPERVISOR
pkill -f supervisor.sh; pkill -f "run_all.py --mode full"; for s in $(tmux ls -F "#S" 2>/dev/null | grep research_w); do tmux kill-session -t $s; done
echo "stopped. Remove state/STOP_SUPERVISOR before restarting the supervisor."
