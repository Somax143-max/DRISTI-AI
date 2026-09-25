@echo off
title DRISHTI-AI Clinical Server (Port 8081)
echo ========================================================
echo  Starting DRISHTI-AI Server on http://127.0.0.1:8081...
echo ========================================================
echo.
cd /d "%~dp0"
python run_server.py 8081
pause
