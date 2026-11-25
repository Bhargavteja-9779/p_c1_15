#!/usr/bin/env bash
# Keeps Layer A alive in an ephemeral container: relaunches dead workers, commits+pushes results every
# 5 min, exits when the queue has no pending/running jobs. Idempotent. Usage: bash scripts/watch_and_checkpoint.sh [branch]
cd "$(dirname "$0")/.." || exit 1
BR=${1:-$(git rev-parse --abbrev-ref HEAD)}
ckpt() { git add -A results state logs tables >/dev/null 2>&1; git commit -qm "auto checkpoint: dev/test results

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01Hw1gvFQTLbtuenyPpWzJqa" >/dev/null 2>&1; for i in 1 2 3; do git push -q origin "$BR" >/dev/null 2>&1 && break; sleep $((i*5)); done; }
left() { python3 -c "import json;q=json.load(open('state/queue.json'));print(sum(j['status'] in ('pending','running') for j in q['jobs']))"; }
n=0
while [ "$(left)" -gt 0 ]; do
  pgrep -f "run_all.py --mode full" >/dev/null || bash scripts/launch_runner.sh 3 >/dev/null
  sleep 30; n=$((n+1)); [ $((n % 10)) -eq 0 ] && ckpt
done
ckpt; echo "queue drained"; python3 scripts/status.py | sed -n '/COMPUTE/,/QUEUE (quick)/p'
