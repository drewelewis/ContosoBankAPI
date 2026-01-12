@echo off
echo Closing devtunnel on port 8080...

REM Find and kill any process using port 8080 (elasticsearch)
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8080') do (
    echo Killing elasticsearch process %%a
    taskkill /f /pid %%a >nul 2>&1
)

REM Stop all devtunnels
devtunnel close --all >nul 2>&1

echo Devtunnel on port 8080 closed.
