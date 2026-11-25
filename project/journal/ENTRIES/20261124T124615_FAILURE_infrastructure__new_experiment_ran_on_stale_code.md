# FAILURE: Infrastructure: new experiment ran on stale code

*Written 2026-11-24T12:46:15+00:00*

All 96 E0b jobs failed in 0 s with 'ValueError: awt' because the long-lived workers had imported the old src/jit.py. Lesson: after any change in src/, restart the workers (bash scripts/stop_all.sh && bash scripts/launch_runner.sh 3). Jobs reset and relaunched.
