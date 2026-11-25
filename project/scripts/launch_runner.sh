#!/usr/bin/env bash
# Layer A: launch N detached runner workers (default: cores-1, min 1) in tmux (or setsid+nohup). Idempotent:
# each worker holds its own lock, so re-running only starts missing workers.
cd "$(dirname "$0")/.." || exit 1
mkdir -p logs
# data/ is gitignored: restore datasets after a container reset (idempotent, sha256-checked)
python3 scripts/get_data.py >> logs/get_data.log 2>&1 || echo "WARNING: data download failed (see logs/get_data.log)"
N=${1:-$(( $(nproc) > 1 ? $(nproc) - 1 : 1 ))}
for w in $(seq 0 $((N-1))); do
  if pgrep -f "run_all.py --mode full --resume --worker $w\$" >/dev/null; then echo "worker $w already running"; continue; fi
  CMD="python3 run_all.py --mode full --resume --worker $w >> logs/runner_w$w.log 2>&1"
  if command -v tmux >/dev/null; then
    tmux kill-session -t research_w$w 2>/dev/null
    tmux new-session -d -s research_w$w "$CMD"; echo "worker $w launched in tmux session research_w$w"
  else
    setsid nohup bash -c "$CMD" < /dev/null > /dev/null 2>&1 & echo "worker $w launched pid $!"
  fi
done
