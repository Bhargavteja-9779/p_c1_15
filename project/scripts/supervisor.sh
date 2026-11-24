#!/usr/bin/env bash
# Layer B: keeps re-launching the agent CLI headlessly until state says FINISHED.
# Backoff 5 -> 15 -> 30 -> 60 min (max 60); if output contains a reset time, sleep until then.
# Stop: touch state/STOP_SUPERVISOR  (or: pkill -f supervisor.sh)
cd "$(dirname "$0")/.." || exit 1
mkdir -p logs
LOG=logs/supervisor.log
BACKOFFS=(300 900 1800 3600)
detect_cli() {
  if command -v claude >/dev/null; then echo "claude"; return; fi
  echo ""
}
CLI=$(detect_cli)
if [ -z "$CLI" ]; then
  echo "$(date -Is) no headless agent CLI found; supervisor cannot auto-restart the agent. Paste BOOTSTRAP_PROMPT.txt manually." | tee -a $LOG
  exit 1
fi
i=0
while true; do
  STATUS=$(python3 -c "import json;print(json.load(open('state/agent_state.json')).get('status',''))" 2>/dev/null)
  if [ "$STATUS" = "FINISHED" ]; then echo "$(date -Is) state FINISHED -> supervisor exits" >> $LOG; exit 0; fi
  if [ -f state/STOP_SUPERVISOR ]; then echo "$(date -Is) STOP file -> supervisor exits" >> $LOG; exit 0; fi
  echo "$(date -Is) starting agent ($CLI) attempt $i" >> $LOG
  OUT=$(mktemp)
  # --dangerously-skip-permissions is needed for unattended runs; remove it if you want prompts.
  (cd .. && claude -p "$(cat project/BOOTSTRAP_PROMPT.txt)" --dangerously-skip-permissions) > "$OUT" 2>&1
  RC=$?
  tail -c 4000 "$OUT" >> logs/agent_last_output.log; echo "$(date -Is) agent exited rc=$RC" >> $LOG
  STATUS=$(python3 -c "import json;print(json.load(open('state/agent_state.json')).get('status',''))" 2>/dev/null)
  [ "$STATUS" = "FINISHED" ] && { echo "$(date -Is) FINISHED" >> $LOG; exit 0; }
  SLEEP=${BACKOFFS[$(( i < 3 ? i : 3 ))]}
  # Try to parse a reset time such as "resets at 5pm" / "reset at 2026-11-24T17:00"
  RESET=$(grep -oiE "reset[s]? (at|on) [^.|\"]{3,40}" "$OUT" | head -1 | sed -E 's/reset[s]? (at|on) //I')
  if [ -n "$RESET" ]; then
    TGT=$(date -d "$RESET" +%s 2>/dev/null)
    if [ -n "$TGT" ]; then NOW=$(date +%s); D=$((TGT - NOW + 60)); [ $D -gt 0 ] && [ $D -lt 86400 ] && SLEEP=$D; fi
  fi
  # A clean exit (rc=0) without a limit message means the agent finished a work chunk: restart sooner.
  if [ $RC -eq 0 ] && ! grep -qiE "usage limit|rate limit|limit reached" "$OUT"; then SLEEP=60; i=0; else i=$((i+1)); fi
  rm -f "$OUT"
  echo "$(date -Is) sleeping ${SLEEP}s before restart" >> $LOG
  sleep $SLEEP
done
