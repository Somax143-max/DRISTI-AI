@echo off
title DRISHTI-AI Public Cloudflare Tunnel
echo ========================================================
echo  Starting DRISHTI-AI Public Cloudflare Tunnel...
echo ========================================================
echo.
cd /d "%~dp0"

if exist "%~dp0cloudflared.exe" (
    "%~dp0cloudflared.exe" tunnel --url http://localhost:8081
) else (
    cloudflared tunnel --url http://localhost:8081
)

pause
