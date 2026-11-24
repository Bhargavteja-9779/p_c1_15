@echo off
REM Layer B supervisor for Windows. Register with Task Scheduler (At log on) to autostart.
cd /d "%~dp0\.."
set /a i=0
:loop
python -c "import json,sys;sys.exit(0 if json.load(open('state/agent_state.json')).get('status')=='FINISHED' else 1)" && goto :eof
if exist state\STOP_SUPERVISOR goto :eof
echo %date% %time% starting agent attempt %i% >> logs\supervisor.log
pushd ..
claude -p "Read project/HANDOFF.md and project/MASTER_PROMPT.md, verify state with python project/scripts/status.py, then continue from NEXT ACTION. Do not restart finished work. Do not ask me questions." --dangerously-skip-permissions >> project\logs\agent_last_output.log 2>&1
popd
echo %date% %time% agent exited >> logs\supervisor.log
if %i%==0 (set s=300) else if %i%==1 (set s=900) else if %i%==2 (set s=1800) else (set s=3600)
set /a i+=1
timeout /t %s% /nobreak >nul
goto loop
