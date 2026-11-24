#!/usr/bin/env bash
# Durability loop for ephemeral containers: commit+push results/state every 10 min while runners are alive.
cd "$(dirname "$0")/../.." || exit 1
BR=$(git branch --show-current)
while true; do
  git add -A project >/dev/null 2>&1
  git commit -qm "auto: results/state checkpoint $(date -u +%FT%TZ)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01Y77AU2SVVvhT3Wp8j3mJpe" >/dev/null 2>&1 && \
    for i in 1 2 3 4; do git push -q origin "$BR" && break; sleep $((i*15)); done
  sleep 600
done
