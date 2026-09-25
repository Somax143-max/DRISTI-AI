@echo off
title DRISHTI-AI Public Tunnel
echo ========================================================
echo  Starting DRISHTI-AI Public Cloudflare Tunnel...
echo ========================================================
echo.
cd /d "%~dp0"
"%~dp0cloudflared.exe" tunnel --url http://localhost:8081
pause
