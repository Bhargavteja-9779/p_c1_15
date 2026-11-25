#!/usr/bin/env bash
# Install boot/login autostart for Layer A (runner + watchdog) and Layer B (supervisor) via cron.
# Usage: bash scripts/install_autostart.sh [--no-agent]   |   bash scripts/install_autostart.sh --remove
P="$(cd "$(dirname "$0")/.." && pwd)"
TAG="# research-loop:$P"
if ! command -v crontab >/dev/null; then echo "crontab not available; use systemd/launchd/Task Scheduler manually (see HANDOFF.md)"; exit 1; fi
CUR=$(crontab -l 2>/dev/null | grep -v "$TAG")
if [ "$1" = "--remove" ]; then echo "$CUR" | crontab -; echo "autostart removed"; exit 0; fi
NEW="$CUR
@reboot cd $P && bash scripts/launch_runner.sh >> logs/autostart.log 2>&1 $TAG
*/5 * * * * cd $P && bash scripts/watchdog.sh $TAG"
if [ "$1" != "--no-agent" ]; then
NEW="$NEW
@reboot cd $P && setsid nohup bash scripts/supervisor.sh >> logs/supervisor.log 2>&1 $TAG"
fi
echo "$NEW" | crontab -; echo "installed:"; crontab -l | grep "$TAG"
