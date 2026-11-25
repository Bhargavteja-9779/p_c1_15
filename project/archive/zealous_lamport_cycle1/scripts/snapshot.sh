#!/usr/bin/env bash
# Write backups/project_snapshot_<date>.tar.gz excluding checkpoints/data/backups; keep last 3.
cd "$(dirname "$0")/.." || exit 1
mkdir -p backups
F=backups/project_snapshot_$(date +%Y%m%d_%H%M).tar.gz
tar --exclude=./checkpoints --exclude=./backups --exclude=./data --exclude=./.git -czf "$F" .
ls -1t backups/project_snapshot_*.tar.gz | tail -n +4 | xargs -r rm -f
echo "$F"
