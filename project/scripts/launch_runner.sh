#!/usr/bin/env bash
# Layer A: launch the compute runner detached (tmux if available, else setsid+nohup). Idempotent.
cd "$(dirname "$0")/.." || exit 1
mkdir -p logs
if pgrep -f "run_all.py --mode full" >/dev/null; then echo "runner already running"; exit 0; fi
if command -v tmux >/dev/null; then
  tmux has-session -t research_runner 2>/dev/null && tmux kill-session -t research_runner
  tmux new-session -d -s research_runner "python3 run_all.py --mode full --resume >> logs/runner.log 2>&1"
  echo "launched in tmux session 'research_runner' (logs/runner.log)"
else
  setsid nohup python3 run_all.py --mode full --resume >> logs/runner.log 2>&1 < /dev/null &
  echo "launched with setsid/nohup pid $! (logs/runner.log)"
fi
