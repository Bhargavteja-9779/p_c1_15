#!/usr/bin/env bash
# Stop both layers (does not delete any state; resume with launch_runner.sh / supervisor.sh)
cd "$(dirname "$0")/.." || exit 1
touch state/STOP_SUPERVISOR
pkill -f supervisor.sh; pkill -f "run_all.py --mode full"; tmux kill-session -t research_runner 2>/dev/null
echo "stopped. Remove state/STOP_SUPERVISOR before restarting the supervisor."
