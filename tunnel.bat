@echo off
title DRISHTI-AI Public Tunnel
echo ========================================================
echo  Starting DRISHTI-AI Public Cloudflare Tunnel...
echo ========================================================
echo.
cd /d "%~dp0"

where python >nul 2>nul
if %errorlevel% equ 0 (
    python tunnel.py 8081
    goto :done
)

if exist "%~dp0cloudflared.exe" (
    "%~dp0cloudflared.exe" tunnel --url http://localhost:8081
    goto :done
)

if exist "%~dp0cloudflare.exe" (
    "%~dp0cloudflare.exe" tunnel --url http://localhost:8081
    goto :done
)

:done
pause
